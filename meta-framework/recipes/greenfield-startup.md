# Recipe — Greenfield startup (3–8 engineers)

**Profile.** Small team. New codebase. Speed of iteration matters more
than long-term ceremony. PM exists but doubles as engineer.

## `specmeta.yaml`

```yaml
specmeta_version: 0.1
profile: greenfield-startup
slots:
  context:        AGENTS.md
  intent:         intent.md
  spec:           spec-kit
  plan:           spec-kit
  tasks:          spec-kit
  implementation: claude-code
  verification:
    - pytest
    - schemathesis
notes: |
  Spec Kit gives the PM something reviewable in PRs.
  Schemathesis hooks into the OpenAPI doc we keep in /spec.
  Revisit when we hit ~10 engineers.
```

## Why these choices

- **`AGENTS.md`** — works with whichever model the founders prefer
  this month; cheap to maintain.
- **`spec-kit`** — phased commands give just enough structure without
  the BMAD ceremony tax.
- **`claude-code`** — terminal-friendly, no IDE lock-in.
- **`schemathesis`** — automatic API tests pay back immediately given
  how often the API shape changes early on.

## What this trades away

- Drift resistance is only "medium" — accepted because the spec is
  rewritten often anyway.
- No QA persona — small team, the same human reviews everything.
