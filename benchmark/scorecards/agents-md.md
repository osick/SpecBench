# Scorecard — AGENTS.md (+ CLAUDE.md / Cursor rules family)

| Field | Value |
| --- | --- |
| Framework version | n/a — convention, not code |
| Date scored | 2026-05-12 |
| Model(s) used | Any |
| Seed-repo SHA | n/a (paper eval) |
| Evaluator | SpecBench v0.1 |
| Run type | `paper` |

## Scores

| # | Dimension | Score | Evidence |
| - | --- | :-: | --- |
| 1 | Spec quality | 1 | Convention is "drop guidance for agents in this file"; not a real spec. |
| 2 | Traceability | 0 | None. |
| 3 | Lifecycle coverage | 1 | Context only; no phased workflow. |
| 4 | Reviewability | 4 | Single markdown file in repo root. |
| 5 | Portability | 4 | Read by OpenAI Codex, Cursor, Aider, Continue, Jules, etc. |
| 6 | Drift resistance | 1 | Static file; drifts unless humans maintain it. |
| 7 | Onboarding cost | 4 | One file. Done. |
| 8 | Verification loop | 0 | None. |

## Strengths

- Universally consumed across agents — the closest thing to an industry standard.
- Zero ceremony.

## Weaknesses

- Not a spec framework on its own. Treat as the **context slot** of a larger
  framework, not as a complete solution.

## Best fit

**Always include one.** Use as the substrate underneath any other framework you choose.
