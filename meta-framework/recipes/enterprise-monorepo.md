# Recipe — Enterprise monorepo (50+ engineers, multiple teams)

**Profile.** Long-lived codebase. Compliance matters. Multiple agents
in use across the org. Spec must survive years and team turnover.

## `specmeta.yaml`

```yaml
specmeta_version: 0.1
profile: enterprise-monorepo
slots:
  context:
    - AGENTS.md           # universal substrate
    - cline-memory-bank   # for long-running per-service context
  intent:         bmad-analyst
  spec:           kiro-ears      # EARS notation, requirement IDs
  plan:           bmad-architect
  tasks:          bmad-sm
  implementation: copilot-coding-agent
  verification:
    - unit-tests
    - pact                # cross-service contracts
    - bmad-qa
notes: |
  EARS gives auditors something they recognise.
  BMAD's QA persona supplies the missing review gate.
  Copilot agent lives in GitHub, where our review process already lives.
```

## Why these choices

- **EARS spec** — compliance reviewers expect "WHEN…THE SYSTEM SHALL…"
  style. Adopting Kiro's notation (whether or not you use the IDE) makes
  the artefact familiar to non-technical stakeholders.
- **BMAD personas** — at this scale, role separation is real, and the
  ceremony pays back.
- **Pact** — service-to-service drift is the dominant failure mode in a
  monorepo; consumer-driven contracts catch it.
- **Copilot agent** — code lives in GitHub; embedding the agent in PRs
  matches existing review culture.

## What this trades away

- Onboarding cost is high — new engineers need a week to learn the flow.
- Portability inside the spec slot is limited if you commit to the Kiro
  IDE; you can mitigate by using Kiro's EARS *format* without its IDE.
