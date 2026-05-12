# Scorecard — BMAD-METHOD

| Field | Value |
| --- | --- |
| Framework version | v4.x (2026-05) |
| Date scored | 2026-05-12 |
| Model(s) used | Any (agent-prompt based) |
| Seed-repo SHA | n/a (paper eval) |
| Evaluator | SpecBench v0.1 |
| Run type | `paper` |

## Scores

| # | Dimension | Score | Evidence |
| - | --- | :-: | --- |
| 1 | Spec quality | 4 | PRD + architecture + sharded stories are detailed and templated. |
| 2 | Traceability | 4 | Stories reference PRD epics; QA agent re-validates against them. |
| 3 | Lifecycle coverage | 4 | Covers analyst → PM → architect → SM → dev → QA across the full lifecycle. |
| 4 | Reviewability | 3 | Many files; reviewable but volume is high. |
| 5 | Portability | 3 | Works in any agent that can be prompted; some agents handle role-switching better. |
| 6 | Drift resistance | 3 | SM/QA agents periodically re-read; not automatic. |
| 7 | Onboarding cost | 1 | Steep — many roles, files, and conventions to learn. |
| 8 | Verification loop | 3 | Dedicated QA persona writes and runs tests. |

## Strengths

- Probably the most thorough lifecycle of any free framework.
- Role separation models real product-team structure well.
- Strong QA persona forces a verification step.

## Weaknesses

- Ceremony cost is real; small projects suffocate under it.
- Many concurrent files mean PRs are noisy.
- Mental load: contributors must learn ~6 personas before being effective.

## Best fit

**Mid-sized teams shipping product features who want PM/Architect/QA discipline without hiring all three roles.**
