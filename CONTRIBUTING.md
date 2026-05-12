# Contributing to SpecBench

Thank you for considering a contribution. SpecBench is most useful when it
reflects the broader community's experience, not one author's view.

## Three kinds of contribution

### 1. Add a framework to the awesome list

Open a PR editing [`awesome-spec-frameworks.md`](./awesome-spec-frameworks.md).
Each entry needs:

- Name and primary link.
- Status emojis (see legend at the top of the list).
- One sentence on *what makes it spec-driven* — not "uses AI".
- If proposing a new category, a one-line definition.

We will reject promotional language, vendor announcements, and entries that
are really just prompt collections.

### 2. Submit or correct a scorecard

Open a PR adding or editing a file in [`benchmark/scorecards/`](./benchmark/scorecards/).

- Use [`_template.md`](./benchmark/scorecards/_template.md).
- Cite evidence for every score — file paths, transcript excerpts, links.
- Mark the run as `paper` (documentation review) or `controlled`
  (actual task run with pinned SHA).
- Vendors are very welcome to submit corrected runs for their own
  framework. Disclose the relationship in the scorecard's *Notes*.

A "score without evidence" PR will be asked for evidence before merge.

### 3. Add a recipe to the meta-framework

Open a PR adding a file in [`meta-framework/recipes/`](./meta-framework/recipes/).

- One file per profile.
- Include a complete `specmeta.yaml`.
- Explain *why* each slot was filled the way it was.
- Note the trade-offs you accepted.

## Code of conduct

Be kind. Disagree with ideas, not with people. Vendor-bashing and
framework-tribalism are out of place here.

## What we won't merge

- "Framework X is the best, scrap the rest" PRs.
- Sponsored placements.
- Scorecards inflated past available evidence.
- Recipes that are really vendor pitches in disguise.

## Local checks

There is no build. CI (when added) will lint markdown and validate
`specmeta.yaml` files against [the schema](./meta-framework/specmeta.schema.yaml).
