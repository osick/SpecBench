# SpecBench Runner

An automated harness that produces objective, reproducible scorecards for
spec-driven-development frameworks. The point of this tool is to remove
the **author judgement** from as much of the scoring as possible, and to
isolate the parts where judgement is unavoidable behind a frozen LLM
prompt and multiple judge samples.

## Objectivity model

Each of the 8 rubric dimensions
([`BENCHMARK.md`](../../BENCHMARK.md#rubric)) is decomposed into one or
more **signals**. A signal is anything that can be measured deterministically
from the framework's output:

- artefact presence and structure (file paths, headings, schema validity)
- artefact metrics (line counts, readability scores, link counts)
- behaviour (did the framework detect a drift probe? does its test
  command exit 0 against a reference HTTP suite?)
- declared metadata from the framework's docs (parsed once, snapshotted)

Each signal maps to a numeric score via a rule in
[`scoring.yaml`](./scoring.yaml). Dimensions are the weighted sum of
their signals, clipped to `[0, 4]`. The full chain is auditable: every
final dimension score can be traced back to the raw signals it came from.

For the residual subjective parts (e.g. "is this spec actually
unambiguous?"), the runner calls an **LLM-as-judge** with a frozen prompt
from [`judge_prompts.yaml`](./judge_prompts.yaml). Each judge call is
made `n=5` times at `temperature=0.2`; the score is the median; the
inter-sample variance is reported alongside the score. A dimension with
high variance is flagged in the scorecard.

```
┌─────────────────────────────────────────────────────────────────┐
│ Framework definition (framework-defs/*.yaml)                       │
│   install:    how to install the framework                         │
│   invoke:     how to run it on a task                              │
│   artefacts:  where to find spec/plan/tasks/code/tests             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Task definition (../tasks/T*.md + tasks.yaml)                       │
│   seed:       the seed repo SHA                                    │
│   prompt:     the PRD or change request                            │
│   accept:     the acceptance script (exit code is truth)            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Runner                                                             │
│   1. Sandbox a fresh dir, check out seed repo at SHA                │
│   2. Install framework (capture install_time, install_exit)         │
│   3. Run framework on task (capture artefacts, transcript, tokens) │
│   4. Run acceptance script (capture pass/fail per case)             │
│   5. Run drift probe (T2/T3 only)                                   │
│   6. Collect signals (metrics.py)                                   │
│   7. Apply scoring.yaml rules → dimension scores                    │
│   8. For subjective signals, invoke judge (judge.py, n=5)           │
│   9. Emit scorecard.json conforming to scorecard.schema.json        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Scorecard                                                          │
│   run_id, framework@version, model@version, seed SHA, timestamp    │
│   per-dimension score, per-signal values, judge variance, transcripts│
│   verdict: pass / fail per acceptance case                         │
└─────────────────────────────────────────────────────────────────┘
```

## What is automated vs. judged

| Rubric dimension | Automated signals | Judged signals |
| --- | --- | --- |
| 1 Spec quality | file present; headings present; acceptance criteria count; Flesch reading-ease | "ambiguity score" (judge) |
| 2 Traceability | % of acceptance criteria referenced by tasks; % of code commits referencing IDs | — |
| 3 Lifecycle coverage | presence of intent/spec/plan/tasks/code/tests artefacts | — |
| 4 Reviewability | all artefacts in git tree; % markdown; max-file-LoC | — |
| 5 Portability | declared agent count parsed from docs; model-swap probe exit code | — |
| 6 Drift resistance | drift-probe detection (yes/no); % of drift probes detected over 3 runs | — |
| 7 Onboarding cost | time-to-first-spec (wall clock); quickstart LoC; #commands user must learn | — |
| 8 Verification loop | tests generated (count); tests pass against produced code (boolean); acceptance-case coverage % | — |

Seven of eight dimensions are fully automatable. Only "spec quality"
involves judgement, and that judgement is confined to a single signal
inside dimension 1 (with variance reported).

## Install and quickstart

```bash
cd benchmark/runner
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run a single (framework, task) pair
python specbench_runner.py \
    --framework framework-defs/spec-kit.yaml \
    --task ../tasks/T1-crud-api.md \
    --model claude-opus-4-7 \
    --out scorecards/spec-kit__T1__claude-opus-4-7__$(date +%Y%m%d).json

# Run all frameworks against all tasks (the matrix)
python specbench_runner.py --matrix
```

The runner expects an `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` /
`GOOGLE_API_KEY` env var matching whichever model you select. The judge
sub-component will use whichever model is set via `--judge-model` (defaults
to a small fixed model so judges don't drift when the implementation
model changes).

## Reproducibility guarantees

Every scorecard records:

- runner version (this repo SHA)
- framework version (its SHA, pulled and pinned at run time)
- model name + version + temperature
- judge model name + version + temperature + sample count
- seed repo SHA
- timestamp (UTC)
- raw transcript (gzipped, secrets redacted)
- per-signal raw values

A scorecard with the same input quintuple
(runner, framework, model, judge, seed) should reproduce within judge
variance. We report `run_type: controlled` only when all five are pinned
and the transcript is attached. Anything less is `run_type: paper`.

## Anti-gaming

The framework-definition YAML cannot influence dimension scores beyond
declaring where artefacts are. Scoring rules live exclusively in
[`scoring.yaml`](./scoring.yaml) and apply to every framework. PR review
will reject framework-defs that:

- declare false artefact paths to skip metric collection
- bundle a custom judge prompt
- alter the seed repo, model, or judge

The runner refuses to load a framework-def with extra keys beyond the
schema.

## Files

- [`specbench_runner.py`](./specbench_runner.py) — entry point.
- [`metrics.py`](./metrics.py) — signal collectors.
- [`judge.py`](./judge.py) — LLM-as-judge wrapper.
- [`scoring.yaml`](./scoring.yaml) — signal → dimension score rules.
- [`judge_prompts.yaml`](./judge_prompts.yaml) — frozen judge prompts.
- [`scorecard.schema.json`](./scorecard.schema.json) — output schema.
- [`framework-defs/_template.yaml`](./framework-defs/_template.yaml) — copy
  for new frameworks.
- [`framework-defs/_schema.json`](./framework-defs/_schema.json) — schema
  for framework definitions.
- [`framework-defs/{spec-kit,openspec,bmad-method}.yaml`](./framework-defs/) —
  three reference definitions.
- [`requirements.txt`](./requirements.txt) — Python deps.
