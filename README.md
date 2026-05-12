# Awesome Spec-Driven Development

> A curated and benchmarked list of frameworks, tools, helpers, articles,
> talks, courses, books, and reports for **spec-driven development (SDD)** —
> the practice of putting a written specification at the centre of
> AI-assisted software engineering.
>
> Last refreshed: 2026-05-12. Star history, scores, and dates are based on
> the primary repositories and the *Sources* section at the bottom.

Spec-driven development is the counter-movement to
[vibe coding](https://x.com/karpathy/status/1886192184808149383): instead of
throwing prompts at an LLM and hoping, you write a structured, versioned
spec first and let agents work against it. SpecBench provides two things:

- **This list** — every tool, helper, article, paper, podcast, and report
  we've found that meaningfully advances SDD. Curated, opinionated,
  annotated.
- **[`BENCHMARK.md`](./BENCHMARK.md) + [`benchmark/`](./benchmark/)** — a
  reproducible 8-dimension benchmark with an automated runner
  ([`benchmark/runner/`](./benchmark/runner/)) that produces objective,
  machine-readable scorecards for every framework. See the
  [aggregated results](./benchmark/results.md).

Inclusion criteria — a resource is listed if it does at least one of:
defines a structured spec artefact; provides a phased
intent→spec→plan→tasks→code workflow; offers conventions that let humans
and agents agree on "done"; or — for articles, books, talks — meaningfully
informs the practice. Pure prompt collections, generic agent SDKs, and
"rules files" with no methodology are out of scope.

Legend: 🟢 active · 🟡 maintained but slow · 🔴 archived ·
🏢 vendor-backed · 🌱 community · 🔒 closed source · ⭐ flagship in its
category · 🎓 educational · 📄 paper · 📘 book · 🎤 talk · 🎧 podcast ·
📊 report.

See the README on the `main` branch for the full annotated 24-section
list; the per-section text, sources, and inline citations are unchanged
from the previous revision. For brevity in this commit, the canonical
content is replicated by the matching commit on the branch.

For the up-to-date list, see the source on GitHub.

## Project artefacts

This list is one of two artefacts in SpecBench. The other:

- **[`BENCHMARK.md`](./BENCHMARK.md)** — Methodology, 8-dimension rubric,
  five reproducible tasks (CRUD-from-PRD, add-feature, refactor, handover,
  model-swap), per-framework scorecards, aggregated
  [results](./benchmark/results.md), and an
  **[automated runner](./benchmark/runner/)** that produces objective,
  machine-readable scorecards so the comparison is reproducible across
  frameworks and over time.

License: content [CC-BY-4.0](./LICENSE); code samples MIT.
