# Scorecard — Tessl

| Field | Value |
| --- | --- |
| Framework version | Public (2026-05) |
| Date scored | 2026-05-12 |
| Model(s) used | Tessl-managed |
| Seed-repo SHA | n/a (paper eval) |
| Evaluator | SpecBench v0.1 |
| Run type | `paper` |

## Scores

| # | Dimension | Score | Evidence |
| - | --- | :-: | --- |
| 1 | Spec quality | 4 | Specs are the unit of work; templated and registry-tracked. |
| 2 | Traceability | 4 | Code is *regenerated* from specs, so the mapping is mechanical. |
| 3 | Lifecycle coverage | 3 | Strong on spec→code; thinner on intent capture. |
| 4 | Reviewability | 2 | Specs live in a platform; PR-only review loses fidelity. |
| 5 | Portability | 1 | Platform-dependent. |
| 6 | Drift resistance | 4 | "Spec is the source" means drift is impossible by construction. |
| 7 | Onboarding cost | 2 | Conceptually new — engineers must accept that code is downstream of spec. |
| 8 | Verification loop | 3 | Spec-derived tests are part of the value prop. |

## Strengths

- Most aggressive answer to drift: regenerate code from spec.
- Spec-registry idea is genuinely novel.

## Weaknesses

- Platform lock-in.
- Requires cultural shift; teams used to code-first workflows will resist.

## Best fit

**New services where you're willing to commit to spec-first as a team rule.**
