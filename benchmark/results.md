# Aggregated results (v0.1 — paper eval)

> ⚠️ These are paper evaluations based on public documentation and our own
> informal usage, not controlled task runs. They are intended as a starting
> point for community correction. Vendors are invited to submit corrected
> runs via PR.

Scoring scale: 0 (absent) — 4 (best-in-class). See [`BENCHMARK.md`](../BENCHMARK.md).

| Framework | Spec qual. | Trace. | Lifecycle | Review. | Portab. | Drift | Onboard | Verify | Σ |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [Spec Kit](./scorecards/spec-kit.md)         | 4 | 3 | 4 | 4 | 4 | 2 | 3 | 2 | 26 |
| [Kiro](./scorecards/kiro.md)                 | 4 | 4 | 4 | 3 | 1 | 3 | 3 | 3 | 25 |
| [BMAD-METHOD](./scorecards/bmad-method.md)   | 4 | 4 | 4 | 3 | 3 | 3 | 1 | 3 | 25 |
| [OpenSpec](./scorecards/openspec.md)         | 3 | 3 | 3 | 4 | 4 | 3 | 4 | 2 | 26 |
| [Tessl](./scorecards/tessl.md)               | 4 | 4 | 3 | 2 | 1 | 4 | 2 | 3 | 23 |
| [AGENTS.md family](./scorecards/agents-md.md)| 1 | 0 | 1 | 4 | 4 | 1 | 4 | 0 | 15 |

## How to read the totals

**Don't sum and rank.** The total is mostly a hint that frameworks address
different problems — Spec Kit and OpenSpec land at the same Σ for very
different reasons. Use the per-dimension scores against your own priorities.

The [meta-framework](../meta-framework/decision-tree.md) helps turn project
constraints into a recommended composition rather than picking a single winner.

## Frameworks still to score

Agent OS · ChatPRD · Cline Memory Bank · TaskMaster · Aider conventions ·
Continue.dev rules · Roo Code orchestrator. PRs welcome.
