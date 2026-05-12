"""Deterministic metric collectors for SpecBench.

Every function in this module takes a `RunContext` and returns either a
single scalar in [0, 1] or a numeric raw value. The scoring layer in
`specbench_runner.py` maps these to the 0..4 dimension scores via the
weights declared in `scoring.yaml`.

Functions are pure where possible: same artefacts in, same number out.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field
from glob import glob
from pathlib import Path
from typing import Iterable

try:
    import textstat  # type: ignore
except ImportError:  # pragma: no cover - optional at import time
    textstat = None


ACCEPTANCE_CRITERION_RE = re.compile(
    r"^\s*(?:[-*]\s+\[ \]|\d+\.)\s+", re.MULTILINE
)
SPEC_ID_RE = re.compile(r"\b(?:REQ|SPEC|FR|NFR|US|AC)-\d+\b")


@dataclass
class RunContext:
    repo_dir: Path
    framework_def: dict
    task_id: str
    artefacts: dict[str, list[Path]] = field(default_factory=dict)
    seed_sha: str = ""


# ---------------------------------------------------------------------------
# Artefact discovery
# ---------------------------------------------------------------------------

def discover_artefacts(ctx: RunContext) -> dict[str, list[Path]]:
    """Resolve glob patterns from framework_def['artefacts'] into Path lists."""
    out: dict[str, list[Path]] = {}
    patterns = ctx.framework_def.get("artefacts", {})
    for kind, globs in patterns.items():
        found: list[Path] = []
        for pat in globs:
            for hit in glob(str(ctx.repo_dir / pat), recursive=True):
                p = Path(hit)
                if p.is_file():
                    found.append(p)
        out[kind] = sorted(set(found))
    return out


# ---------------------------------------------------------------------------
# Dim 1 — Spec quality
# ---------------------------------------------------------------------------

def spec_present(ctx: RunContext) -> float:
    return 1.0 if ctx.artefacts.get("spec") else 0.0


def acceptance_criteria_count(ctx: RunContext) -> float:
    """Counts list-style and numbered acceptance criteria; returns min(1, n/10)."""
    text = _concat(ctx.artefacts.get("spec", []))
    n = len(ACCEPTANCE_CRITERION_RE.findall(text))
    return min(1.0, n / 10.0), n


def flesch_reading_ease(ctx: RunContext) -> float:
    text = _concat(ctx.artefacts.get("spec", []))
    if not text or textstat is None:
        return 0.0, None
    score = float(textstat.flesch_reading_ease(text))
    # 60+ is "easily readable by 13-15-year-olds". <30 is academic.
    normalised = max(0.0, min(1.0, (score - 30) / 60))
    return normalised, score


# ---------------------------------------------------------------------------
# Dim 2 — Traceability
# ---------------------------------------------------------------------------

def tasks_reference_spec_pct(ctx: RunContext) -> float:
    spec_ids = _spec_ids(_concat(ctx.artefacts.get("spec", [])))
    tasks_text = _concat(ctx.artefacts.get("tasks", []))
    if not tasks_text:
        return 0.0
    task_blocks = [b for b in re.split(r"\n(?=[-*]|\d+\.)", tasks_text) if b.strip()]
    if not task_blocks:
        return 0.0
    refd = sum(1 for b in task_blocks if SPEC_ID_RE.search(b))
    return refd / len(task_blocks)


def commits_reference_id_pct(ctx: RunContext) -> float:
    try:
        out = subprocess.check_output(
            ["git", "log", "--pretty=%s"], cwd=ctx.repo_dir, text=True
        )
    except subprocess.CalledProcessError:
        return 0.0
    msgs = [m for m in out.splitlines() if m.strip()]
    if not msgs:
        return 0.0
    return sum(1 for m in msgs if SPEC_ID_RE.search(m)) / len(msgs)


def spec_sections_covered_pct(ctx: RunContext) -> float:
    spec_ids = set(SPEC_ID_RE.findall(_concat(ctx.artefacts.get("spec", []))))
    if not spec_ids:
        return 0.0
    refd_in_tasks = set(SPEC_ID_RE.findall(_concat(ctx.artefacts.get("tasks", []))))
    return len(spec_ids & refd_in_tasks) / len(spec_ids)


# ---------------------------------------------------------------------------
# Dim 3 — Lifecycle coverage
# ---------------------------------------------------------------------------

def artefact_present(ctx: RunContext, kind: str) -> float:
    return 1.0 if ctx.artefacts.get(kind) else 0.0


# ---------------------------------------------------------------------------
# Dim 4 — Reviewability
# ---------------------------------------------------------------------------

def all_artefacts_in_git(ctx: RunContext) -> float:
    all_files = _flatten_artefacts(ctx)
    if not all_files:
        return 0.0
    try:
        out = subprocess.check_output(
            ["git", "ls-files"], cwd=ctx.repo_dir, text=True
        )
    except subprocess.CalledProcessError:
        return 0.0
    tracked = {ctx.repo_dir / p for p in out.splitlines() if p}
    return sum(1 for f in all_files if f in tracked) / len(all_files)


def markdown_share(ctx: RunContext) -> float:
    artefacts = [p for k, ps in ctx.artefacts.items() if k != "code" for p in ps]
    if not artefacts:
        return 0.0
    md = sum(1 for p in artefacts if p.suffix.lower() in {".md", ".markdown"})
    return md / len(artefacts)


def max_file_loc(ctx: RunContext) -> float:
    files = _flatten_artefacts(ctx)
    if not files:
        return 1.0
    max_loc = max(_count_lines(f) for f in files)
    if max_loc <= 500:
        return 1.0, max_loc
    if max_loc >= 2000:
        return 0.0, max_loc
    return 1.0 - (max_loc - 500) / 1500, max_loc


# ---------------------------------------------------------------------------
# Dim 5 — Portability
# ---------------------------------------------------------------------------

def declared_agent_count(ctx: RunContext) -> float:
    agents = ctx.framework_def.get("declared", {}).get("supported_agents", [])
    n = len(agents)
    # Saturate at 6.
    return min(1.0, n / 6.0), n


def model_swap_probe(ctx: RunContext, second_model_ok: bool | None) -> float:
    # Computed externally by the T5 runner; just a passthrough.
    if second_model_ok is None:
        return 0.0
    return 1.0 if second_model_ok else 0.0


# ---------------------------------------------------------------------------
# Dim 6 — Drift resistance
# ---------------------------------------------------------------------------

def drift_probe_detected(ctx: RunContext, probe_results: list[bool]) -> float:
    if not probe_results:
        return 0.0
    detections = sum(1 for r in probe_results if r)
    return detections / len(probe_results)


def drift_repeat_consistency(probe_results: list[bool]) -> float:
    if len(probe_results) < 2:
        return 0.0
    return 1.0 if len(set(probe_results)) == 1 else 0.0


# ---------------------------------------------------------------------------
# Dim 7 — Onboarding cost (lower-is-better → returned as 0..1, higher=better)
# ---------------------------------------------------------------------------

def time_to_first_spec_score(seconds: float) -> float:
    if seconds <= 300:
        return 1.0
    if seconds >= 1800:
        return 0.0
    return 1.0 - (seconds - 300) / 1500


def quickstart_loc_score(ctx: RunContext) -> float:
    n = ctx.framework_def.get("declared", {}).get("quickstart_loc", 1000)
    if n <= 50:
        return 1.0
    if n >= 500:
        return 0.0
    return 1.0 - (n - 50) / 450


def commands_to_learn_score(ctx: RunContext) -> float:
    n = ctx.framework_def.get("declared", {}).get("user_commands", 12)
    if n <= 4:
        return 1.0
    if n >= 12:
        return 0.0
    return 1.0 - (n - 4) / 8


# ---------------------------------------------------------------------------
# Dim 8 — Verification loop
# ---------------------------------------------------------------------------

def tests_generated_count(ctx: RunContext) -> float:
    test_files = ctx.artefacts.get("tests", [])
    # Count test functions across all test files.
    n_tests = 0
    for f in test_files:
        try:
            txt = f.read_text(errors="replace")
        except OSError:
            continue
        n_tests += len(re.findall(r"^\s*def\s+test_", txt, re.MULTILINE))
        n_tests += len(re.findall(r"^\s*it\(", txt, re.MULTILINE))
    acc_n = len(ACCEPTANCE_CRITERION_RE.findall(_concat(ctx.artefacts.get("spec", []))))
    if acc_n == 0:
        return 0.0, n_tests
    return min(1.0, n_tests / acc_n), n_tests


def tests_pass_against_code(ctx: RunContext, pytest_exit: int | None) -> float:
    if pytest_exit is None:
        return 0.0
    return 1.0 if pytest_exit == 0 else 0.0


def acceptance_case_coverage_pct(ctx: RunContext, n_pass: int, n_total: int) -> float:
    if n_total == 0:
        return 0.0
    return n_pass / n_total


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _concat(paths: Iterable[Path]) -> str:
    chunks: list[str] = []
    for p in paths:
        try:
            chunks.append(p.read_text(errors="replace"))
        except OSError:
            continue
    return "\n".join(chunks)


def _spec_ids(text: str) -> set[str]:
    return set(SPEC_ID_RE.findall(text))


def _flatten_artefacts(ctx: RunContext) -> list[Path]:
    return [p for ps in ctx.artefacts.values() for p in ps]


def _count_lines(p: Path) -> int:
    try:
        return sum(1 for _ in p.open(errors="replace"))
    except OSError:
        return 0
