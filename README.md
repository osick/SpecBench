# SpecBench

**A benchmark, curated list, and meta-framework for spec-driven development tools.**

Spec-driven development (SDD) is the practice of letting written specifications —
not chat prompts or vibe-coded snippets — drive how AI coding agents plan,
implement, and verify software. A spec is a durable artifact: reviewable,
versionable, testable. Over the past 18 months the ecosystem of "spec frameworks"
has exploded (Spec Kit, Kiro, BMAD-METHOD, OpenSpec, Tessl, AGENTS.md, …), but
there is no neutral way to compare them or to pick the right pieces for a given
team and project.

SpecBench tries to fill that gap. It contains:

| Artifact | What it is |
| --- | --- |
| [`awesome-spec-frameworks.md`](./awesome-spec-frameworks.md) | A curated, opinionated list of spec-driven frameworks, conventions, and supporting tools. |
| [`BENCHMARK.md`](./BENCHMARK.md) | Methodology, criteria, and rubric for evaluating spec frameworks. |
| [`benchmark/tasks/`](./benchmark/tasks/) | Reproducible tasks each framework is run against. |
| [`benchmark/scorecards/`](./benchmark/scorecards/) | Per-framework scorecards filled in against the rubric. |
| [`benchmark/results.md`](./benchmark/results.md) | Aggregated, comparable results. |
| [`meta-framework/`](./meta-framework/) | **SpecMeta** — a small meta-framework that lets you compose pieces of existing frameworks for a specific use case. |

## Why a benchmark?

Most "comparisons" today are vendor blog posts. They show a happy-path demo and
move on. The questions teams actually ask are harder:

- Does the framework keep the spec and code in sync after week 6?
- Does it work for a 3-person greenfield project *and* a 200-engineer monorepo?
- Can a non-engineering PM contribute to the spec?
- Is the artefact reviewable in a normal PR, or only inside a vendor IDE?
- How well does it survive a model swap (Claude ↔ GPT ↔ Gemini ↔ local)?

The [rubric](./BENCHMARK.md#rubric) captures 8 dimensions designed to surface
these questions. Each framework is scored on each dimension with evidence drawn
from running the [benchmark tasks](./benchmark/tasks/).

## Why a meta-framework?

After scoring a dozen frameworks it is obvious that **no single framework wins
every dimension**. Spec Kit produces a beautifully reviewable plan but has no
runtime contract layer. BMAD has rich agent roles but heavyweight ceremony.
Kiro has tight IDE integration but is vendor-locked. AGENTS.md is universal but
minimal.

[`meta-framework/`](./meta-framework/) (SpecMeta) decomposes spec-driven
development into 7 reusable **slots** and gives you a decision tree for picking
a concrete implementation for each slot based on your project profile.

## Status

**v0.1 — first public draft.** Scorecards are seeded from public documentation,
not yet from controlled task runs. Contributions are very welcome — see
[`CONTRIBUTING.md`](./CONTRIBUTING.md).

## License

Content is published under [CC-BY-4.0](./LICENSE); any code samples under MIT.
