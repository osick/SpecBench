# Recipe — Safety-critical subsystem

**Profile.** A bounded part of a larger system where bugs are
catastrophic: payments, medical devices, distributed-state machines,
infra control plane. The rest of the codebase may use a lighter recipe.

## `specmeta.yaml` (for the critical subsystem only)

```yaml
specmeta_version: 0.1
profile: safety-critical
slots:
  context:        AGENTS.md
  intent:         prfaq
  spec:
    - kiro-ears        # human-readable requirements
    - tla-plus         # formal model for the state machine
  plan:           bmad-architect
  tasks:          spec-kit-tasks
  implementation: claude-code
  verification:
    - property-tests
    - tla-model-check
    - pact
notes: |
  EARS is for stakeholders; TLA+ is for the model checker.
  CI must run TLC and the property tests on every PR touching this folder.
```

## Why these choices

- **Dual spec (EARS + TLA+)** — humans review the EARS; the model
  checker proves invariants over the TLA+. They cover different failure
  modes; you want both.
- **`bmad-architect`** — architecture document carries weight when an
  auditor asks "why this design?".
- **Property tests + TLC** — closes the verification loop with both
  random and exhaustive checks.

## What this trades away

- Onboarding cost is the highest of any recipe.
- This is *not* the recipe for the whole repo. Use it only for the
  subfolder that warrants it.
