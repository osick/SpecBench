# Recipe — Solo prototype / weekend project

**Profile.** One person. Throwaway-ish code. Wants *some* discipline so
the prototype is salvageable if it works, but cannot afford ceremony.

## `specmeta.yaml`

```yaml
specmeta_version: 0.1
profile: solo-prototype
slots:
  context:        AGENTS.md
  intent:         intent.md
  spec:           openspec
  plan:           claude-plan-mode
  tasks:          backlog-md
  implementation: claude-code
  verification:   unit-tests
notes: |
  OpenSpec change-proposal pattern is the lightest spec discipline
  that still produces a reviewable artefact if this prototype graduates.
```

## Why these choices

- **OpenSpec** — markdown only, no platform, three concepts to learn.
- **Plan mode** — built into the editor, no separate tool.
- **`backlog.md`** — task tracking without a JIRA-shaped hole.
- **Unit tests only** — anything more is overkill at this stage.

## Graduation path

If the prototype survives, switch `spec` to `spec-kit` and add
`schemathesis` once you have an API worth contract-testing. Everything
else stays.
