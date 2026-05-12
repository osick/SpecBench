# SpecBench Methodology

A benchmark for spec-driven development frameworks. Unlike a coding-eval
benchmark (HumanEval, SWE-bench), SpecBench measures the **process artefacts**
and **lifecycle properties** that a framework produces — because that, not raw
code-completion accuracy, is what differentiates SDD tools.

## Design principles

1. **Model-agnostic** — every task must be runnable with at least two of
   {Claude, GPT, Gemini, a local model}. Frameworks that only work with one
   model are scored down on portability, not excluded.
2. **Artefact-first** — we score the spec, plan, and task list that the
   framework emits, not only the final code.
3. **Reproducible** — every task ships a fixed seed repo and a written
   acceptance script.
4. **Honest** — scorecards record the model, framework version, date, and
   commit SHA of the seed repo. Stale runs are marked as such.

## Rubric

Each framework is scored 0–4 on eight dimensions. 0 = absent, 4 = best-in-class.

| # | Dimension | What "4" looks like |
| - | --- | --- |
| 1 | **Spec quality** | The emitted spec is unambiguous, testable, has acceptance criteria, and a non-engineer can read it. |
| 2 | **Traceability** | Every code change links back to a spec section; every spec section has at least one test or task. |
| 3 | **Lifecycle coverage** | Framework covers intent → spec → plan → tasks → code → verify → maintenance, not just one phase. |
| 4 | **Reviewability** | Artefacts are plain files diffable in a normal PR; reviewers can comment line-by-line. |
| 5 | **Portability** | Works with ≥3 agents/models and any editor; not locked to a vendor IDE or proprietary format. |
| 6 | **Drift resistance** | After 5 unrelated edits, the spec and code are still consistent (or the framework detects the drift). |
| 7 | **Onboarding cost** | A new contributor productive in < 30 min from `README` alone. |
| 8 | **Verification loop** | Framework runs or generates tests/contracts that mechanically prove acceptance. |

The total is reported as a **radar chart** rather than a single number — the
right framework depends on which dimensions you value.

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

1. Clone the seed repo at the pinned SHA.
2. Install the framework according to its quickstart, capturing time-to-first-spec.
3. Run the task using its canonical workflow. Record:
   - The spec file(s) produced.
   - The plan / task list.
   - The final diff against the seed repo.
   - The agent transcript (redacted of secrets).
4. Run the task's acceptance script. Record pass/fail.
5. Apply the **drift probe** (T2/T3 only): make 3 small unrelated commits and
   re-ask the framework for a new feature. Did it detect the inconsistency?
6. Score against the rubric, citing evidence (file paths, transcript line
   numbers) for each dimension. **No score without evidence.**

## What the benchmark is *not*

- Not a leaderboard of LLMs. The model is a variable, the framework is the
  unit under test.
- Not a measure of code-completion accuracy. Use SWE-bench or LiveCodeBench
  for that.
- Not a vendor showdown. Each scorecard is reproducible and links to
  primary sources; vendors are invited to submit corrected runs.

## v0.1 caveats

- Scorecards in this commit are **paper evaluations** based on public docs
  and our own informal usage, not controlled task runs. They are starting
  points for community correction, not final verdicts.
- Tasks T4 and T5 are specified but not yet executed.
- A machine-readable scorecard schema (YAML) is planned for v0.2 so results
  can be aggregated programmatically.
