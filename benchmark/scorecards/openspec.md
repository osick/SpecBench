# Scorecard — OpenSpec

| Field | Value |
| --- | --- |
| Framework version | HEAD (2026-05) |
| Date scored | 2026-05-12 |
| Model(s) used | Any |
| Seed-repo SHA | n/a (paper eval) |
| Evaluator | SpecBench v0.1 |
| Run type | `paper` |

## Scores

| # | Dimension | Score | Evidence |
| - | --- | :-: | --- |
| 1 | Spec quality | 3 | Plain markdown; quality depends on the user, but template guides shape. |
| 2 | Traceability | 3 | Change proposals reference the spec deltas they modify; archived after merge. |
| 3 | Lifecycle coverage | 3 | Spec → proposal → archive is solid; planning/tasks are lighter. |
| 4 | Reviewability | 4 | Everything is markdown in the repo; PR review is the native workflow. |
| 5 | Portability | 4 | Agent-agnostic by design. |
| 6 | Drift resistance | 3 | The "proposal" gate before code changes is a structural defence against drift. |
| 7 | Onboarding cost | 4 | Three concepts (spec, proposal, archive) plus normal git workflow. |
| 8 | Verification loop | 2 | No first-party test integration; relies on existing project test infra. |

## Strengths

- Pure markdown, pure git — fits any existing repo.
- Lowest cognitive overhead of any full framework.
- Change-proposal pattern is elegant drift defence.

## Weaknesses

- Light on planning and tasks; pair with another tool if you need those.
- No verification harness.

## Best fit

**Teams that already have strong PR review culture and want SDD without new tooling.**
