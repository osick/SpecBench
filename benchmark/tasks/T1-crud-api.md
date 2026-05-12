# T1 — CRUD API from a PRD

**Stresses:** spec quality · lifecycle coverage · verification loop
**Estimated wall-clock:** 60–90 min for a fresh user.

## Prompt to the framework

You are starting a new project. Read `PRD.md` (below) and produce, in order:

1. A reviewable specification.
2. A technical plan.
3. A task breakdown.
4. The implementation.
5. Tests that demonstrate every acceptance criterion in the spec.

Use the framework's canonical workflow. Do not skip phases.

### PRD.md (provided to the framework)

> **Bookmarks service**
>
> A single-tenant HTTP service for storing personal bookmarks.
>
> - Users can create, read, update, and delete bookmarks.
> - A bookmark has: `id` (server-assigned), `url` (required, valid http(s)),
>   `title` (optional, ≤ 200 chars), `tags` (0–10 short strings),
>   `created_at`, `updated_at`.
> - Listing supports filtering by tag and full-text search over `title`+`url`.
> - Duplicate `url` for the same user returns 409.
> - All endpoints return JSON. Errors follow RFC 7807 (Problem Details).
> - Persistence: any embedded store is fine (SQLite acceptable).

## Seed repo

Empty directory plus a `README.md` containing only the PRD above. Pinned via
the SHA listed at the top of each scorecard.

## Acceptance script

Black-box HTTP tests, run against whatever the framework produces, exercising:

- Happy-path CRUD for each verb.
- Validation: empty URL, malformed URL, oversized title, 11 tags.
- Duplicate-URL → 409.
- Filter-by-tag and search both work and combine.
- All error responses are RFC 7807-shaped.

Acceptance is **binary pass/fail per case**; the rubric scores *how well the
framework's own artefacts predicted these cases* before they were written.

## What to record

- Time from `git init` to first spec file committed.
- Word count and structure of the spec.
- Whether the framework auto-derived tests from acceptance criteria.
- Final code LoC and test LoC.
- Number of agent turns to completion.
