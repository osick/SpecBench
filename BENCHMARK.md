# SpecBench Methodology

A benchmark for spec-driven development frameworks. Unlike a coding-eval
benchmark (HumanEval, SWE-bench), SpecBench measures the **process artefacts**
and **lifecycle properties** that a framework produces — because that, not raw
code-completion accuracy, is what differentiates SDD tools.

A scorecard you can't reproduce is barely a scorecard, so the v0.2 release
ships with an **automated runner** ([`benchmark/runner/`](./benchmark/runner/))
that turns every (framework, task, model) tuple into a deterministic,
machine-readable scorecard. The runner is the regulator: it owns the
scoring rules and refuses to load framework definitions that try to
influence their own score.

## Design principles

1. **Objective by default.** Seven of the eight rubric dimensions are
   scored from signals the runner measures directly (file presence,
   structure, traceability counts, drift-probe outcomes, test pass
   rates). The one remaining dimension that involves judgement is
   bounded by a frozen LLM-as-judge prompt with `n=5` samples and
   variance reported alongside the score.
2. **Model-agnostic.** Frameworks must be runnable with at least two of
   {Claude, GPT, Gemini, local}. Single-model frameworks are scored down
   on portability, not excluded.
3. **Artefact-first.** We score the spec, plan, and task list the
   framework emits, not only the final code.
4. **Reproducible.** Every scorecard records the runner SHA, framework
   version, model + temperature, judge model + temperature + sample
   count, seed-repo SHA, and a gzipped transcript hash.
5. **Anti-gaming.** Scoring rules live in
   [`benchmark/runner/scoring.yaml`](./benchmark/runner/scoring.yaml) and
   apply uniformly. Framework definitions are validated against
   [`framework-defs/_schema.json`](./benchmark/runner/framework-defs/_schema.json);
   extra keys are rejected.

## Rubric

Each framework is scored 0–4 on eight dimensions. 0 = absent, 4 =
best-in-class.

| # | Dimension | What "4" looks like | How the runner measures it |
| - | --- | --- | --- |
| 1 | **Spec quality** | The spec is unambiguous, testable, has acceptance criteria, and a non-engineer can read it. | Artefact presence + acceptance-criterion count + Flesch reading ease + **LLM-as-judge** (ambiguity, n=5). |
| 2 | **Traceability** | Every code change links back to a spec section; every spec section has at least one task or test. | % of tasks that reference a `REQ-/SPEC-/AC-` ID; % of commits with an ID in the message; % of spec IDs covered. |
| 3 | **Lifecycle coverage** | Framework covers intent → spec → plan → tasks → code → verify. | Presence of each artefact kind (declared in the framework definition). |
| 4 | **Reviewability** | Plain files diffable in a normal PR. | % of artefacts tracked by git; markdown share; max-file-LoC. |
| 5 | **Portability** | Works with ≥3 agents/models; not locked to a vendor IDE. | Declared supported-agents count (parsed from framework's README); model-swap probe (T5). |
| 6 | **Drift resistance** | After unrelated edits, spec + code stay consistent (or the framework surfaces the drift). | Drift probe run 3×; detection rate; consistency across runs. |
| 7 | **Onboarding cost** | A new contributor productive in < 30 min from README alone. | Wall-clock time-to-first-spec; quickstart LoC; #commands the user must learn. |
| 8 | **Verification loop** | Framework runs or generates tests/contracts that prove acceptance. | Test count vs. AC count; `pytest` exits 0; % of acceptance cases passing. |

The total is reported as a **radar chart** rather than a single number —
the right framework depends on which dimensions you value.

## Tasks

See [`benchmark/tasks/`](./benchmark/tasks/). The v0.1 suite is small on
purpose; we'd rather have 5 tasks scored well than 50 scored badly.

| ID | Title | What it stresses |
| -- | --- | --- |
| T1 | CRUD API from a PRD | Spec quality, lifecycle coverage, verification loop |
| T2 | Add a feature to an existing repo | Drift resistance, traceability |
| T3 | Refactor with behaviour preservation | Verification loop, drift resistance |
| T4 | Cross-team handover | Reviewability, onboarding cost |
| T5 | Model swap mid-project | Portability |

## Procedure (per framework, per task)

The runner handles all of it:

```bash
cd benchmark/runner
python specbench_runner.py \
    --framework framework-defs/spec-kit.yaml \
    --task ../tasks/T1-crud-api.md \
    --model claude-opus-4-7 \
    --out scorecards/spec-kit__T1__claude-opus-4-7__$(date +%Y%m%d).json
```

What the runner does, in order:

1. **Pin and install** the framework at the version declared in
   [`framework-defs/<name>.yaml`](./benchmark/runner/framework-defs/).
2. **Sandbox** a fresh working directory; record its seed SHA.
3. **Invoke** the framework on the task's prompt using the templated
   commands from the framework def. Capture transcript + tokens + wall
   clock.
4. **Discover artefacts** at the paths declared by the framework def
   (intent / spec / plan / tasks / code / tests).
5. **Run signal collectors** in [`metrics.py`](./benchmark/runner/metrics.py).
6. **Apply scoring rules** from [`scoring.yaml`](./benchmark/runner/scoring.yaml)
   — weighted sum, clipped to `[0, 4]`, rounded to one decimal.
7. **Drift-probe** (T2 only): make an out-of-band edit, re-invoke the
   framework, look for the framework explicitly surfacing the
   inconsistency. Repeat 3× and record the detection rate.
8. **LLM judge** the spec for ambiguity using a frozen prompt
   (`ambiguity_v1`) with `n=5` samples; record median + variance.
9. **Run acceptance suite** for the task. Record pass / fail per case.
10. **Emit** a JSON scorecard conforming to
    [`scorecard.schema.json`](./benchmark/runner/scorecard.schema.json),
    plus a gzipped transcript with SHA-256.

To run the full matrix:

```bash
python specbench_runner.py --matrix   # all framework-defs × all tasks
```

## Objectivity guarantees

- **Scoring rules are normative and outside the framework's control.**
  A framework def cannot raise its own score by declaring different
  weights — it only declares *where to find* artefacts.
- **Judge prompts are pinned by ID.** Once `ambiguity_v1` ships in a
  scorecard, the prompt text is frozen; revisions become `ambiguity_v2`
  and re-scoring is explicit.
- **Variance is reported.** Any dimension that includes a judge signal
  ships with its inter-sample variance. Reviewers can discard runs with
  high variance.
- **Transcripts are hashed.** A scorecard with a transcript SHA that
  doesn't match the attached transcript is rejected by the schema
  validator.
- **The runner SHA is recorded.** Re-runs with the same inputs and the
  same runner SHA should reproduce within judge variance.

## What the benchmark is *not*

- Not a leaderboard of LLMs. The model is a variable; the framework is
  the unit under test.
- Not a measure of code-completion accuracy. Use SWE-bench or
  LiveCodeBench for that.
- Not a vendor showdown. Each scorecard is reproducible and the
  framework definitions are open; vendors are invited to submit
  corrected runs.

## v0.2 caveats

- The markdown scorecards in [`benchmark/scorecards/`](./benchmark/scorecards/)
  are still **paper evaluations** from public documentation. They will be
  superseded by JSON scorecards from controlled runner runs as those
  arrive.
- The acceptance scripts (`benchmark/tasks/T*/accept.sh`) ship as stubs;
  the runner reports `total: 0` until they are filled in.
- The `--matrix` mode is documented but not yet implemented; current
  scope is single-pair runs.
- Drift probe currently looks for keyword mentions of the inconsistency
  in framework output. A future version will use a dedicated judge
  prompt for higher-signal detection.

## Files

| Path | Purpose |
| --- | --- |
| [`benchmark/runner/specbench_runner.py`](./benchmark/runner/specbench_runner.py) | CLI entry point. |
| [`benchmark/runner/metrics.py`](./benchmark/runner/metrics.py) | Deterministic signal collectors. |
| [`benchmark/runner/judge.py`](./benchmark/runner/judge.py) | LLM-as-judge wrapper. |
| [`benchmark/runner/scoring.yaml`](./benchmark/runner/scoring.yaml) | Normative scoring rules. |
| [`benchmark/runner/judge_prompts.yaml`](./benchmark/runner/judge_prompts.yaml) | Frozen judge prompts. |
| [`benchmark/runner/scorecard.schema.json`](./benchmark/runner/scorecard.schema.json) | Output schema. |
| [`benchmark/runner/framework-defs/`](./benchmark/runner/framework-defs/) | Per-framework definitions + schema. |
| [`benchmark/tasks/`](./benchmark/tasks/) | Task prompts and acceptance suites. |
| [`benchmark/scorecards/`](./benchmark/scorecards/) | Markdown scorecards (paper evals). |
| [`benchmark/results.md`](./benchmark/results.md) | Aggregated current results. |
