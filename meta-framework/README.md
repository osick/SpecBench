# SpecMeta — a meta-framework for spec-driven development

No single framework wins on every benchmark dimension. SpecMeta decomposes
spec-driven development into **7 reusable slots** and lets you fill each
slot with the concrete tool that fits your project. The output is a small,
explicit composition that lives in your repo — not a new framework to learn,
but a structured way to combine the ones that already exist.

## The seven slots

```
┌──────────────────────────────────────────────────────────────────┐
│                     1. CONTEXT                                   │
│              (what the agent always knows)                       │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. INTENT          →   3. SPEC          →   4. PLAN              │
│ (what we want)         (what "done" is)     (how we'll get there)│
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ 5. TASKS           →   6. IMPLEMENTATION →  7. VERIFICATION      │
│ (work breakdown)       (the code)           (proof it's done)    │
└──────────────────────────────────────────────────────────────────┘
```

| # | Slot | Question it answers | Common choices |
| - | --- | --- | --- |
| 1 | **Context** | What background does the agent always need? | AGENTS.md · CLAUDE.md · Cursor rules · Cline Memory Bank |
| 2 | **Intent** | What problem are we solving and why? | PRFAQ · ChatPRD · BMAD analyst persona · plain `intent.md` |
| 3 | **Spec** | What does "done" look like, testably? | Spec Kit `/specify` · Kiro EARS · OpenSpec spec · TLA+/Alloy for safety-critical |
| 4 | **Plan** | What's the technical approach? | Spec Kit `/plan` · Claude Code plan mode · Aider architect · BMAD architect |
| 5 | **Tasks** | What concrete steps and in what order? | Spec Kit `/tasks` · TaskMaster · Backlog.md · BMAD SM sharded stories |
| 6 | **Implementation** | Who writes the code, in what loop? | Claude Code · Cursor · Cline act-mode · Aider editor · Roo dev mode |
| 7 | **Verification** | How do we mechanically prove the spec is met? | Property tests · Schemathesis from OpenAPI · Pact · BMAD QA persona · plain unit tests |

A SpecMeta composition picks **one tool per slot** (sometimes two — context
and verification compose well) and writes the choice into a single
`specmeta.yaml` at the repo root.

See:

- [`components.md`](./components.md) — catalogue of options per slot with
  trade-offs.
- [`decision-tree.md`](./decision-tree.md) — questions to ask, in order, to
  arrive at a composition.
- [`ai-decision-workflow.md`](./ai-decision-workflow.md) — an AI-driven
  workflow that runs the decision tree as a slash-command and emits a
  justified `specmeta.yaml`.
- [`recipes/`](./recipes/) — ready-made compositions for common project
  profiles.
- [`specmeta.schema.yaml`](./specmeta.schema.yaml) — the file format.

## Example: `specmeta.yaml` for a 5-person startup

```yaml
specmeta_version: 0.1
profile: greenfield-startup
slots:
  context:        AGENTS.md
  intent:         intent.md          # plain markdown, no tool
  spec:           spec-kit
  plan:           spec-kit
  tasks:          spec-kit
  implementation: claude-code
  verification:
    - pytest
    - schemathesis  # OpenAPI is checked into the spec
notes: |
  Spec Kit gives us reviewable artefacts.
  Schemathesis closes the loop because our spec embeds an OpenAPI document.
  We'll reconsider when we hit ~10 engineers or our first multi-team feature.
```

The point of writing this down is the same as picking a license or a
linter: future-you (or a new hire) can see at a glance which conventions
this repo follows, and any tool authored against SpecMeta knows what to
expect.

## Why not a monolithic framework?

Because the dimensions a framework optimises for trade off against each
other — best spec quality conflicts with lowest onboarding cost; tightest
verification conflicts with vendor-neutrality. SpecMeta admits that
explicitly and lets you make the trade-off once, in writing, instead of
hiding it inside a tool choice.
