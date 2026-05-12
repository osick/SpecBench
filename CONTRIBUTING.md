# Contributing to SpecBench

Thank you for considering a contribution. SpecBench is most useful when it
reflects the broader community's experience, not one author's view.

## Three kinds of contribution

### 1. Add a framework to the awesome list

Open a PR editing the [`README.md`](./README.md) (which is the awesome list).
Each entry needs:

- Name and primary link.
- Status emojis (see legend at the top of the list).
- One sentence on *what makes it spec-driven* — not "uses AI".
- If proposing a new category, a one-line definition.

We will reject promotional language, vendor announcements, and entries that
are really just prompt collections.

### 2. Add a framework definition for the runner

Open a PR adding a file in
[`benchmark/runner/framework-defs/`](./benchmark/runner/framework-defs/).

A framework definition tells the automated runner how to install the
framework, invoke it on a task, and locate the artefacts it produces.
Reuse [`_template.yaml`](./benchmark/runner/framework-defs/_template.yaml).

The runner will then produce a controlled scorecard automatically — no
hand-scoring required.

### 3. Submit or correct a scorecard

Open a PR adding or editing a file in
[`benchmark/scorecards/`](./benchmark/scorecards/).

- Prefer the runner — controlled scorecards must be produced by it.
- For `paper` scorecards (documentation review only), use the markdown
  [`_template.md`](./benchmark/scorecards/_template.md) and cite evidence
  for every score: file paths, transcript excerpts, links.
- Vendors are very welcome to submit corrected runs for their own
  framework. Disclose the relationship in the scorecard's *Notes*.

A "score without evidence" PR will be asked for evidence before merge.

## Code of conduct

Be kind. Disagree with ideas, not with people. Vendor-bashing and
framework-tribalism are out of place here.

## What we won't merge

- "Framework X is the best, scrap the rest" PRs.
- Sponsored placements.
- Scorecards inflated past available evidence.
- Framework definitions that secretly hard-code high scores (the runner
  uses signed metric formulas — see
  [`benchmark/runner/scoring.yaml`](./benchmark/runner/scoring.yaml)).

## Local checks

CI (when added) will lint markdown, validate framework-definition YAMLs
against
[`benchmark/runner/framework-defs/_schema.json`](./benchmark/runner/framework-defs/_schema.json),
and validate scorecards against
[`benchmark/runner/scorecard.schema.json`](./benchmark/runner/scorecard.schema.json).
