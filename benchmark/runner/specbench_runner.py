#!/usr/bin/env python3
"""SpecBench Runner — produce an objective scorecard for one (framework, task).

Run:
    python specbench_runner.py \
        --framework framework-defs/spec-kit.yaml \
        --task ../tasks/T1-crud-api.md \
        --model claude-opus-4-7 \
        --out scorecards/spec-kit__T1__$(date +%Y%m%d).json

The runner is deliberately split into small, testable steps so PR review
can verify that no step lets the framework-def influence its own score.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml
from jsonschema import validate

import metrics
from metrics import RunContext

HERE = Path(__file__).resolve().parent
SCORING_VERSION = "0.1"
SCHEMA_VERSION = "0.1"


# ---------------------------------------------------------------------------
# Inputs and pinning
# ---------------------------------------------------------------------------

def load_framework_def(path: Path) -> dict:
    with open(HERE / "framework-defs" / "_schema.json") as f:
        schema = json.load(f)
    with open(path) as f:
        fdef = yaml.safe_load(f)
    validate(instance=fdef, schema=schema)
    return fdef


def load_scoring() -> dict:
    return yaml.safe_load((HERE / "scoring.yaml").read_text())


def load_judge_prompts() -> dict:
    return yaml.safe_load((HERE / "judge_prompts.yaml").read_text())


def runner_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=HERE, text=True
        ).strip()
    except subprocess.CalledProcessError:
        return "unknown"


# ---------------------------------------------------------------------------
# Sandbox lifecycle
# ---------------------------------------------------------------------------

@dataclass
class StepResult:
    cmd: str
    exit: int
    seconds: float
    stdout: str = ""
    stderr: str = ""


def run_step(cmd: str, cwd: Path, env: dict | None = None,
             timeout: int = 600) -> StepResult:
    start = time.monotonic()
    try:
        p = subprocess.run(
            cmd, cwd=cwd, env={**os.environ, **(env or {})},
            shell=True, capture_output=True, text=True, timeout=timeout,
        )
        return StepResult(
            cmd=cmd, exit=p.returncode,
            seconds=time.monotonic() - start,
            stdout=p.stdout, stderr=p.stderr,
        )
    except subprocess.TimeoutExpired:
        return StepResult(cmd=cmd, exit=124, seconds=timeout,
                          stderr=f"TIMEOUT after {timeout}s")


def prepare_sandbox(seed_repo_template: Optional[str]) -> Path:
    sb = Path(tempfile.mkdtemp(prefix="specbench-"))
    if seed_repo_template:
        for entry in Path(seed_repo_template).iterdir():
            dst = sb / entry.name
            if entry.is_dir():
                shutil.copytree(entry, dst)
            else:
                shutil.copy2(entry, dst)
    run_step("git init -q && git add -A && git commit -q -m 'seed' --allow-empty",
             cwd=sb)
    return sb


def seed_sha(repo_dir: Path) -> str:
    out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_dir, text=True)
    return out.strip()


# ---------------------------------------------------------------------------
# Drift probe (T2 / T3 only)
# ---------------------------------------------------------------------------

def drift_probe(ctx: RunContext, framework_def: dict) -> list[bool]:
    """Apply an out-of-band edit and ask the framework to continue.

    Returns one bool per probe attempt: True iff the framework explicitly
    surfaced the inconsistency rather than silently overwriting it.
    """
    results: list[bool] = []
    spec_files = ctx.artefacts.get("spec", [])
    if not spec_files:
        return results
    target = spec_files[0]
    original = target.read_text()
    for i in range(3):
        # 1) Tamper with the spec out-of-band.
        tampered = original.replace("tags: 0-10", "tags: 0-20", 1)
        target.write_text(tampered)
        run_step(f"git commit -am 'manual drift {i}'", cwd=ctx.repo_dir)

        # 2) Re-invoke the framework with a follow-up prompt that does not
        #    mention the change.
        followup = ctx.repo_dir / ".followup-prompt.md"
        followup.write_text("Please add a 'bulk tag rename' feature.")
        for tmpl in framework_def["invoke"]["per_task"]["commands"]:
            cmd = tmpl.replace("{repo}", str(ctx.repo_dir)) \
                      .replace("{prompt_path}", str(followup))
            run_step(cmd, cwd=ctx.repo_dir,
                     env=framework_def["invoke"]["per_task"].get("env"))

        # 3) Detect: did the framework mention the drift in any new artefact?
        detected = _drift_mentioned(ctx.repo_dir)
        results.append(detected)

        # 4) Reset for next probe.
        target.write_text(original)
        run_step(f"git commit -am 'reset after probe {i}'", cwd=ctx.repo_dir)
    return results


def _drift_mentioned(repo_dir: Path) -> bool:
    needles = ("drift", "inconsistent", "out-of-band", "manual change", "diverged")
    for path in repo_dir.rglob("*.md"):
        txt = path.read_text(errors="replace").lower()
        if any(n in txt for n in needles):
            return True
    return False


# ---------------------------------------------------------------------------
# Acceptance suite (per task)
# ---------------------------------------------------------------------------

def run_acceptance(task_id: str, repo_dir: Path) -> tuple[int, list[dict]]:
    """Run the task's acceptance suite. For now: shell out to tasks/<id>/accept.sh."""
    script = HERE.parent / "tasks" / f"{task_id}" / "accept.sh"
    if not script.exists():
        return -1, [{"name": "no-acceptance-script", "passed": False,
                     "detail": f"missing {script}"}]
    rc = subprocess.run(["bash", str(script), str(repo_dir)],
                        capture_output=True, text=True)
    cases: list[dict] = []
    for line in rc.stdout.splitlines():
        # Convention: each acceptance script prints "PASS <name>" or "FAIL <name>".
        if line.startswith(("PASS ", "FAIL ")):
            tag, name = line.split(" ", 1)
            cases.append({"name": name.strip(), "passed": tag == "PASS"})
    return rc.returncode, cases


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _value(x):
    """Some metric functions return (normalised, raw); flatten to the normalised."""
    return x[0] if isinstance(x, tuple) else float(x)


def _raw(x):
    return x[1] if isinstance(x, tuple) and len(x) > 1 else None


def collect_signals(ctx: RunContext, *,
                    install_seconds: float,
                    pytest_exit: int | None,
                    accept_pass: int,
                    accept_total: int,
                    drift_results: list[bool],
                    model_swap_ok: bool | None,
                    judge_result=None) -> list[dict]:
    out: list[dict] = []

    def add(_id, val):
        out.append({"id": _id, "value": _value(val), "raw": _raw(val)})

    add("spec_present", metrics.spec_present(ctx))
    add("acceptance_criteria_count", metrics.acceptance_criteria_count(ctx))
    add("flesch_reading_ease", metrics.flesch_reading_ease(ctx))

    add("tasks_reference_spec_pct", metrics.tasks_reference_spec_pct(ctx))
    add("commits_reference_id_pct", metrics.commits_reference_id_pct(ctx))
    add("spec_sections_covered_pct", metrics.spec_sections_covered_pct(ctx))

    for kind, sig_id in [("intent", "intent_artefact"),
                         ("spec", "spec_artefact"),
                         ("plan", "plan_artefact"),
                         ("tasks", "tasks_artefact"),
                         ("code", "code_artefact"),
                         ("tests", "tests_artefact")]:
        add(sig_id, metrics.artefact_present(ctx, kind))

    add("all_artefacts_in_git", metrics.all_artefacts_in_git(ctx))
    add("markdown_share", metrics.markdown_share(ctx))
    add("max_file_loc", metrics.max_file_loc(ctx))

    add("declared_agent_count", metrics.declared_agent_count(ctx))
    add("model_swap_probe", metrics.model_swap_probe(ctx, model_swap_ok))

    add("drift_probe_detected", metrics.drift_probe_detected(ctx, drift_results))
    add("drift_repeat_consistency",
        metrics.drift_repeat_consistency(drift_results))

    add("time_to_first_spec_seconds", metrics.time_to_first_spec_score(install_seconds))
    add("quickstart_loc", metrics.quickstart_loc_score(ctx))
    add("commands_to_learn", metrics.commands_to_learn_score(ctx))

    add("tests_generated_count", metrics.tests_generated_count(ctx))
    add("tests_pass_against_code", metrics.tests_pass_against_code(ctx, pytest_exit))
    add("acceptance_case_coverage_pct",
        metrics.acceptance_case_coverage_pct(ctx, accept_pass, accept_total))

    if judge_result is not None:
        out.append({
            "id": "ambiguity_judge",
            "value": judge_result.score / 4.0,
            "raw": judge_result.score,
            "judge_samples": judge_result.samples,
        })
    return out


def score_dimensions(signals: list[dict], scoring_yaml: dict) -> dict[str, dict]:
    by_id = {s["id"]: s["value"] for s in signals}
    out: dict[str, dict] = {}
    for dim_id, spec in scoring_yaml["dimensions"].items():
        ids: list[str] = []
        num = 0.0
        denom = 0.0
        for sig in spec["signals"]:
            ids.append(sig["id"])
            w = float(sig["weight"])
            v = float(by_id.get(sig["id"], 0.0))
            num += w * v
            denom += w
        score = 4.0 * num / denom if denom > 0 else 0.0
        out[dim_id] = {
            "score": round(max(0.0, min(4.0, score)),
                           int(scoring_yaml["combine"].get("rounding", 1))),
            "signal_ids": ids,
        }
    return out


# ---------------------------------------------------------------------------
# Scorecard assembly
# ---------------------------------------------------------------------------

def assemble_scorecard(*,
                       framework_def: dict,
                       task_id: str, task_version: str,
                       model_name: str, temperature: float,
                       judge_model: str, judge_samples: int,
                       seed_sha_: str,
                       signals: list[dict],
                       dimensions: dict[str, dict],
                       acceptance: dict,
                       transcript_sha: str,
                       run_type: str = "controlled",
                       notes: str | None = None) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": str(uuid.uuid4()),
        "run_type": run_type,
        "framework": {
            "name": framework_def["name"],
            "version_sha": _resolve_framework_sha(framework_def),
            "url": framework_def.get("homepage", ""),
        },
        "task": {"id": task_id, "version": task_version},
        "model": {"name": model_name, "temperature": temperature},
        "judge_model": {
            "name": judge_model,
            "temperature": 0.2,
            "samples": judge_samples,
        },
        "seed_sha": seed_sha_,
        "runner_sha": runner_sha(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scoring_version": SCORING_VERSION,
        "judge_prompt_versions": {"ambiguity_judge": "ambiguity_v1"},
        "dimensions": dimensions,
        "signals": signals,
        "acceptance": acceptance,
        "transcript_sha256": transcript_sha,
        **({"notes": notes} if notes else {}),
    }


def _resolve_framework_sha(fdef: dict) -> str:
    pin = fdef["version_pin"]
    return pin.get("git_sha") or pin.get("release_tag") or \
           pin.get("pypi_version") or pin.get("npm_version") or "unknown"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--framework", required=True, type=Path)
    ap.add_argument("--task", required=True, type=Path,
                    help="Path to a tasks/T*.md file.")
    ap.add_argument("--model", required=True)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--judge-model", default="claude-haiku-4-5-20251001")
    ap.add_argument("--judge-samples", type=int, default=5)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--paper", action="store_true",
                    help="Skip install/invoke; collect metrics only (paper run).")
    ap.add_argument("--validate", action="store_true",
                    help="Validate the framework-def against the schema and exit.")
    args = ap.parse_args(argv)

    fdef = load_framework_def(args.framework)
    if args.validate:
        print(f"OK: {args.framework} is a valid framework definition.")
        return 0

    scoring = load_scoring()
    prompts = load_judge_prompts()
    task_id = args.task.stem.split("-")[0]

    sandbox = prepare_sandbox(seed_repo_template=None)
    sha = seed_sha(sandbox)

    # 1. Install
    install_seconds = 0.0
    if not args.paper:
        for cmd in fdef["install"]:
            r = run_step(cmd, cwd=sandbox)
            install_seconds += r.seconds
            if r.exit != 0:
                print(f"install step failed: {cmd}\n{r.stderr}", file=sys.stderr)
                return 2

    # 2. Invoke per task
    if not args.paper:
        env = fdef["invoke"]["per_task"].get("env", {})
        for tmpl in fdef["invoke"]["per_task"]["commands"]:
            cmd = tmpl.replace("{repo}", str(sandbox)) \
                      .replace("{prompt_path}", str(args.task.resolve()))
            r = run_step(cmd, cwd=sandbox, env=env, timeout=1800)
            if r.exit != 0:
                print(f"invocation step failed: {cmd}\n{r.stderr}", file=sys.stderr)

    # 3. Build context + discover artefacts
    ctx = RunContext(repo_dir=sandbox, framework_def=fdef, task_id=task_id,
                     seed_sha=sha)
    ctx.artefacts = metrics.discover_artefacts(ctx)

    # 4. Drift probe (T2 only by convention)
    drift = drift_probe(ctx, fdef) if task_id == "T2" else []

    # 5. Acceptance
    pytest_exit_code: int | None = None
    pytest_run = run_step("pytest -q 2>/dev/null || true", cwd=sandbox)
    pytest_exit_code = 0 if "passed" in pytest_run.stdout else pytest_run.exit
    accept_exit, cases = run_acceptance(task_id, sandbox)
    accept_pass = sum(1 for c in cases if c["passed"])

    # 6. Judge (only spec_quality)
    judge_result = None
    if not args.paper:
        try:
            from judge import judge as run_judge
            spec_text = metrics._concat(ctx.artefacts.get("spec", []))
            if spec_text:
                judge_result = run_judge("ambiguity_v1", prompts, spec_text,
                                         model=args.judge_model)
        except Exception as e:                       # pragma: no cover
            print(f"judge skipped: {e}", file=sys.stderr)

    # 7. Signals + dimensions
    signals = collect_signals(
        ctx,
        install_seconds=install_seconds,
        pytest_exit=pytest_exit_code,
        accept_pass=accept_pass,
        accept_total=len(cases),
        drift_results=drift,
        model_swap_ok=None,
        judge_result=judge_result,
    )
    dimensions = score_dimensions(signals, scoring)
    if judge_result is not None:
        dimensions["spec_quality"]["judge_variance"] = round(judge_result.variance, 3)

    # 8. Transcript hash
    transcript_path = args.out.with_suffix(".transcript.json.gz")
    transcript = {
        "install_seconds": install_seconds,
        "artefacts": {k: [str(p) for p in v] for k, v in ctx.artefacts.items()},
        "acceptance_cases": cases,
        "drift_probe_results": drift,
    }
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(transcript_path, "wt") as f:
        json.dump(transcript, f)
    transcript_sha = hashlib.sha256(transcript_path.read_bytes()).hexdigest()

    # 9. Assemble + validate + write
    scorecard = assemble_scorecard(
        framework_def=fdef,
        task_id=task_id, task_version="0.1",
        model_name=args.model, temperature=args.temperature,
        judge_model=args.judge_model, judge_samples=args.judge_samples,
        seed_sha_=sha,
        signals=signals,
        dimensions=dimensions,
        acceptance={"pass": accept_pass, "fail": len(cases) - accept_pass,
                    "total": len(cases), "cases": cases},
        transcript_sha=transcript_sha,
        run_type="paper" if args.paper else "controlled",
    )

    schema = json.loads((HERE / "scorecard.schema.json").read_text())
    validate(instance=scorecard, schema=schema)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(scorecard, indent=2))
    print(f"wrote {args.out}  (sandbox: {sandbox})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
