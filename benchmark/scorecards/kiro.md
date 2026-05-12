# Scorecard — Kiro

| Field | Value |
| --- | --- |
| Framework version | Public preview (2026-05) |
| Date scored | 2026-05-12 |
| Model(s) used | Kiro-managed (closed) |
| Seed-repo SHA | n/a (paper eval) |
| Evaluator | SpecBench v0.1 |
| Run type | `paper` |

## Scores

| # | Dimension | Score | Evidence |
| - | --- | :-: | --- |
| 1 | Spec quality | 4 | EARS notation in `requirements.md`; explicit `design.md`; consistent shape across features. |
| 2 | Traceability | 4 | Tasks in `tasks.md` reference requirement IDs; IDE surfaces them. |
| 3 | Lifecycle coverage | 4 | Requirements → design → tasks → implementation built into the IDE. |
| 4 | Reviewability | 3 | Artefacts are markdown but optimised for the Kiro IDE; PR review works but loses some affordances. |
| 5 | Portability | 1 | Vendor-locked IDE; cannot swap to another agent or model without rebuilding the workflow. |
| 6 | Drift resistance | 3 | Steering docs and per-feature folders reduce drift; not automatic but well-structured. |
| 7 | Onboarding cost | 3 | IDE handles most ceremony; concept of "spec sessions" is novel and needs explanation. |
| 8 | Verification loop | 3 | Tasks can be tied to test stubs; verification is workflow-encouraged, not enforced. |

## Strengths

- Best EARS-style requirements out of the box.
- IDE traceability is genuinely useful when you stay inside it.
- Steering docs solve a real problem (cross-cutting context) that markdown-only frameworks punt on.

## Weaknesses

- Vendor lock-in is total; portability score reflects this.
- Closed model means you cannot tune cost / privacy.
- Limited fit for repos that already have a heavy existing workflow.

## Best fit

**Teams committed to AWS tooling that want SDD without writing their own scaffolding.**
