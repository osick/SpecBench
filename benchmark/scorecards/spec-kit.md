# Scorecard — GitHub Spec Kit

| Field | Value |
| --- | --- |
| Framework version | 0.x (HEAD as of 2026-05) |
| Date scored | 2026-05-12 |
| Model(s) used | Claude, GPT, Gemini (any agent supporting slash commands) |
| Seed-repo SHA | n/a (paper eval) |
| Evaluator | SpecBench v0.1 |
| Run type | `paper` |

## Scores

| # | Dimension | Score | Evidence |
| - | --- | :-: | --- |
| 1 | Spec quality | 4 | `/specify` produces a structured markdown spec with explicit acceptance criteria; templates enforce shape. |
| 2 | Traceability | 3 | `/tasks` derives a numbered task list from the plan; tasks reference plan sections but no automatic spec-↔-code linker. |
| 3 | Lifecycle coverage | 4 | Covers `/specify` → `/plan` → `/tasks` → `/implement` end-to-end. |
| 4 | Reviewability | 4 | All artefacts are plain markdown in the repo; reviewable in a normal PR. |
| 5 | Portability | 4 | Works with Claude Code, Cursor, Copilot, Gemini CLI, Codex; vendor-neutral. |
| 6 | Drift resistance | 2 | No built-in drift detector; relies on the user to re-run `/specify`. |
| 7 | Onboarding cost | 3 | Quickstart is short; mental model of four commands is easy; sample repo helps. |
| 8 | Verification loop | 2 | Task list often includes "write tests" but no enforced verification gate. |

## Strengths

- Best-in-class artefact quality for "the spec you'd want to review".
- True multi-agent portability — the same flow works across Claude/Cursor/Copilot.
- Simple mental model: four phases, four commands.

## Weaknesses

- No first-party mechanism for keeping spec and code in sync over time.
- Verification is aspirational, not enforced.
- Doesn't natively support multi-feature repos (one folder per feature is on the user).

## Best fit

**Greenfield features where the spec needs to survive code review by a PM.**
