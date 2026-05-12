# SpecMeta AI Decision Workflow

A reproducible, AI-driven workflow that takes a short project description
and emits a justified [`specmeta.yaml`](./specmeta.schema.yaml). Runs with
any general-purpose coding agent (Claude Code, Cursor, Copilot, Codex,
Gemini CLI, …).

**The workflow drives a panel of [eight personas](./personas/) — Consultant,
Senior Engineer, Architect, Critic, Product Manager, QA Lead, Security /
Compliance, Coach — through six rounds.** Each persona has a defined remit,
scoring heuristic, and veto right. The orchestrator (the agent running this
workflow) plays each persona in turn and records the proceedings.

See [`personas/README.md`](./personas/README.md) for the voting model and
[`personas/<name>.md`](./personas/) for each persona's full prompt.

## Goal

Replace ad-hoc framework-picking with a structured decision conference
that:

1. Elicits seven dimensions of the project profile in a fixed order
   (Consultant).
2. Proposes a draft composition (Architect) based on the closest shipped
   recipe.
3. Subjects the draft to a panel vote with weighted persona scoring.
4. Applies hard constraints (C1–C10) via the Critic's veto right and the
   Senior Engineer's technical veto.
5. Resolves ties by onboarding cost (Coach).
6. Emits a *justified* `specmeta.yaml` plus a `dissents.md` capturing any
   −2 votes that survived the rounds.

The workflow is the AI agent's analogue of a 1-hour design conversation
with a senior engineer, a sceptical CTO, a PM, and a QA lead in the room.

## Workflow shape

```
┌──────────────────────────────────────────────────────────────┐
│ Round 0 — Initialise                                         │
│  Load: components.md, results.md, decision-tree.md, schema,  │
│        personas/*.md, recipes/*.md                           │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Round 1 — 🧭 CONSULTANT runs intake (≤ 7 questions, batched) │
│  Q1 Greenfield vs existing?                                  │
│  Q2 Non-engineering stakeholders in spec review?             │
│  Q3 Portability vs vendor-IDE tolerance?                     │
│  Q4 Drift-resistance importance (low/med/critical)?          │
│  Q5 Formal verification needed anywhere?                     │
│  Q6 Team size / review culture?                              │
│  Q7 Editor / agent preference?                               │
│  Outputs: intake.json + repo-signal inferences               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Round 2 — 🏗️ ARCHITECT proposes draft composition            │
│  Start from closest shipped recipe; modify minimally.        │
│  Each slot gets a one-line rationale.                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Round 3 — Panel vote (parallel, structured)                  │
│  👴 SENIOR · 📋 PM · 🧪 QA · 🔒 SECURITY · 🎓 COACH cast      │
│  scored votes (-2..+2) per slot. Weights from persona/README. │
│  🔍 CRITIC runs the C1-C10 constraint check.                 │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Round 4 — Vetoes and amendments                              │
│  Apply CRITIC + SENIOR vetoes. ARCHITECT amends. Re-vote     │
│  only the slots that changed.                                │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Round 5 — 🎓 COACH tie-breaks on onboarding cost             │
│  Slot ties within 0.5 pts → lower onboarding wins.           │
│  > 6 distinct tools → drop the lowest-value one.             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Round 6 — Write outputs                                      │
│  specmeta.yaml at repo root (with per-slot rationale)         │
│  dissents.md (only if any −2 vote survived)                  │
│  short chat summary (≤ 8 lines)                              │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
                       specmeta.yaml + dissents.md
```

Most projects converge in Round 3 with no vetoes. Rounds 4–5 exist for the
rare cases where structured disagreement matters.

## Persona weighting

The base weight is 1.0 per persona. Phase-1 answers adjust weights as
follows (also documented in [`personas/README.md`](./personas/README.md)):

| If Phase-1 says… | …then weight these higher |
| --- | --- |
| Greenfield + small team | Coach +0.5, Senior +0.3 |
| Brownfield / monorepo | Critic +0.5, Senior +0.5 |
| Non-engineering reviewers | Product Manager +0.5 |
| Drift critical | QA Lead +0.5 |
| Formal verification needed | Senior +0.5, Security +1.0 (un-muted) |
| Team ≥ 20 | Architect +0.5, Coach +0.5 |
| Mixed editors | Critic +0.3 |

Weights are printed before any vote.

## Constraint catalogue

Hard rules. The Critic must veto any composition that violates one; the
Senior Engineer must veto any that violates 1, 4, or 7.

| ID | Rule |
| -- | --- |
| C1 | If `portability_priority = high`, exclude every option with portability score ≤ 1 in [`results.md`](../benchmark/results.md). |
| C2 | If `spec = tessl`, slots `plan` / `tasks` / `implementation` may be `null` (Tessl subsumes them). |
| C3 | If `implementation = copilot-coding-agent`, slot `context` must contain `AGENTS.md`. |
| C4 | If any element of `verification` is `schemathesis`, slot `spec` must embed an OpenAPI document. |
| C5 | If `formal_verification = true`, slot `spec` must include `tla-plus` *or* `alloy` (additive, not replacing the human-readable spec). |
| C6 | If `team_size < 5`, prefer onboarding-cost ≥ 3; exclude BMAD-METHOD unless user explicitly opts in. |
| C7 | If `team_size ≥ 20`, prefer drift-resistance ≥ 3; require an explicit verification slot. |
| C8 | If `greenfield = false`, prefer `openspec` for `spec` unless another option dominates by ≥ 1 point on every other relevant dimension. |
| C9 | Never emit `null` for `context`, `spec`, or `implementation` — these slots are required by the schema. |
| C10 | If two candidates tie within 0.5 points after weighted voting, pick the one with lower onboarding cost (Coach's tie-break). |

## Per-slot scoring formula

```
weighted_score(slot, framework) =
    Σ_personas  persona_weight * persona_vote(slot, framework)
  + Σ_dimensions  dimension_weight * framework_score(dimension)
```

Persona votes are in `[-2, +2]`; dimension scores come from
[`results.md`](../benchmark/results.md). Dimension weights start at 1.0
and adjust per the Phase-1 answers — see
[the dimension table in the previous workflow draft](#dimension-weighting-from-phase-1-answers)
(retained below for backwards compatibility).

## Dimension weighting from Phase-1 answers

| Phase-1 answer | Adjusts these dimension weights |
| --- | --- |
| Existing codebase | +drift, +reviewability |
| Non-engineering reviewers | +spec quality, +reviewability |
| Portability matters | +portability |
| Drift-resistance critical | +drift, +verification |
| Formal verification needed | +verification (and triggers C5) |
| Team ≥ 20 | +traceability, +drift |
| Team ≤ 5 | +onboarding cost (lower is better) |
| Editor preference = IDE | unlocks Kiro / Cursor-IDE family |

Default weights start at 1.0; each "matters" adjustment adds +0.5 (max 3.0).

## Orchestrator prompt template

Drop this into `.claude/commands/pick-specmeta.md` (Claude Code),
`.cursor/rules/pick-specmeta.mdc` (Cursor), or
`.github/prompts/pick-specmeta.md` (Copilot Coding Agent).

````markdown
# /pick-specmeta — run the SpecMeta panel

You are the SpecMeta Orchestrator. Your job is NOT to decide alone — it is
to run the eight-persona panel in sequence and faithfully record its
output. You will adopt each persona one round at a time, using the
persona file as that round's system prompt.

## Inputs

Read these files first. If any is missing, stop and ask the user.

- meta-framework/personas/README.md
- meta-framework/personas/consultant.md
- meta-framework/personas/senior-engineer.md
- meta-framework/personas/architect.md
- meta-framework/personas/critic.md
- meta-framework/personas/product-manager.md
- meta-framework/personas/qa-lead.md
- meta-framework/personas/security-compliance.md
- meta-framework/personas/coach.md
- meta-framework/components.md
- meta-framework/ai-decision-workflow.md (this file)
- meta-framework/specmeta.schema.yaml
- meta-framework/recipes/*.md
- benchmark/results.md

## Procedure

Run the six rounds defined in ai-decision-workflow.md § Workflow shape.
For each round, prefix your output with the round number and the persona
symbol. Examples:

  ## Round 1 — 🧭 Consultant
  Intake answers: { greenfield: true, … }

  ## Round 2 — 🏗️ Architect
  Draft composition: …

  ## Round 3 — 👴 Senior says …
  ## Round 3 — 📋 PM says …
  …

After Round 5, write:

- `specmeta.yaml` at the repo root with per-slot `# rationale:` comments.
- `dissents.md` ONLY if any −2 vote survived the rounds.
- A ≤ 8-line summary in chat.

## Hard rules

- Print the persona weight vector and the dimension weight vector before
  any vote.
- Cite the constraint ID (C1–C10) for every veto.
- A persona may not act outside its declared authority. If you are
  tempted to (e.g. PM vetoing implementation), file a dissent instead.
- Stop after writing the files. Do not edit anything else.
````

## Example panel transcript (abbreviated)

```
## Round 1 — 🧭 Consultant
Detected .cursor/ folder ⇒ editor=cursor (inferred).
Asked Q1, Q2, Q4, Q5, Q6 in one message.

Intake:
  greenfield: true
  non_engineer_reviewers: true   (auditor)
  portability_priority: medium
  drift_priority: critical       (audit)
  formal_verification: false
  team_size: 4
  editor: cursor
  notes: "fintech, SOC 2 next year"

Note: "SOC 2" un-mutes 🔒 Security.

## Round 2 — 🏗️ Architect
Closest recipe: greenfield-startup. Modifications:
  - Add `cursor-rules` to context (user said editor=cursor).
  - Verification: pytest + schemathesis + pact (drift critical, audit).

Draft:
  context: [AGENTS.md, cursor-rules]
  intent: intent.md
  spec: spec-kit
  plan: spec-kit
  tasks: spec-kit
  implementation: cursor
  verification: [pytest, schemathesis, pact]

## Round 3 — votes (weights: Senior 1.0, PM 1.5, QA 1.5, Security 1.0,
##                         Coach 1.0, Critic 1.3, Architect 1.0)
👴 Senior        +1 / +1 / +1 / +1 / +1 / +1 / +1     (note: needs OpenAPI in spec for C4)
📋 PM            +2 spec, +1 elsewhere
🧪 QA            +2 verification, +1 elsewhere
🔒 Security      0 (no IDs in spec — recommend EARS supplement)
🎓 Coach         +1 elsewhere, −1 verification (3 tools — at the limit)
🔍 Critic        flags C4 (Schemathesis needs OpenAPI) — Senior agrees.

## Round 4 — amendment
Architect amends spec slot: spec-kit + OpenAPI document required in
/specify template. Re-vote on spec only — all positive.

## Round 5 — Coach
6 distinct tools. At the limit but acceptable. No tie-break needed.

## Round 6 — Outputs
Wrote specmeta.yaml + a short summary. No dissents.md (no −2 survived).
```

## Non-interactive (CI) mode

Pass [`intake.schema.json`](./intake.schema.json)-conforming JSON instead
of running the Consultant interactively:

```json
{
  "greenfield": true,
  "non_engineer_reviewers": true,
  "portability_priority": "medium",
  "drift_priority": "critical",
  "formal_verification": false,
  "team_size": 4,
  "editor": "cursor",
  "notes": "fintech, SOC 2 next year"
}
```

The Consultant reads this as if the user had answered Phase 1; Rounds 2–6
proceed unchanged. With `temperature=0` the proceedings are reproducible.

## Why a panel of personas, not a single agent?

Three reasons (also in [`personas/README.md`](./personas/README.md)):

1. **Diversity of failure mode.** A single agent that's wrong is wrong
   in one direction; a panel that's wrong shows up as a 4–4 split the
   user can read and resolve.
2. **Auditability.** "Why did we pick X?" answered with "Consultant
   logged Y from the user, Architect proposed Z, Critic raised C4, the
   panel resolved it as W" is much better than "the model decided".
3. **Different attention surfaces.** The Critic actively looks for
   problems; the Coach actively looks for onboarding cost; the QA Lead
   actively looks for verification gaps. Forcing the model to enact
   these *attention policies* separately produces better composite
   reasoning than "consider all angles".

## Roadmap

- v0.2: add a `specmeta-lint` script that validates a written
  `specmeta.yaml` against C1–C10 mechanically.
- v0.3: ship per-agent invocation files (`.claude/commands/`,
  `.cursor/rules/`, `.github/copilot-instructions.md`) so the workflow
  is one slash-command away.
- v0.4: feed real benchmark scorecard YAML (not paper evals) into the
  scoring step so the panel picks based on measured numbers.
- v0.5: add a `panel-replay` mode where you re-run the proceedings on a
  different intake and see only the diff in the composition.
