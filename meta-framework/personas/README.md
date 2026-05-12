# SpecMeta Personas — a panel that picks your SDD approach

A single AI agent picking your spec-driven setup is fragile: it tends to
default to whichever framework is most prominent in its training data, and
it has no built-in dissent. SpecMeta instead runs a **round-table of eight
personas**, each with a defined remit, scope of authority, and dissent
right.

The panel produces three things: a justified `specmeta.yaml`, a short
written rationale, and a *dissents.md* if any persona voted against the
final composition.

## The panel

| # | Persona | Symbol | Remit | Authority |
| - | --- | :-: | --- | --- |
| 1 | [Consultant](./consultant.md) | 🧭 | Interviews user, surfaces priorities, runs Phase 1. | Owns the **intake**. Can rephrase but not override user statements. |
| 2 | [Senior Engineer](./senior-engineer.md) | 👴 | Judges technical fit; knows the gotchas. | **Veto** on technically untenable choices. |
| 3 | [Architect](./architect.md) | 🏗️ | Composes the slots into a coherent whole. | Owns the **first-draft** composition. |
| 4 | [Critic](./critic.md) | 🔍 | Plays devil's advocate; challenges every choice. | **Hard veto** on constraint violations (C1–C10). Must justify. |
| 5 | [Product Manager](./product-manager.md) | 📋 | Represents stakeholder + business priorities. | Owns the **intent** and **spec** slots. |
| 6 | [QA Lead](./qa-lead.md) | 🧪 | Speaks for testability and verification. | Owns the **verification** slot. |
| 7 | [Security / Compliance](./security-compliance.md) | 🔒 | Risk view; speaks louder when safety-critical. | **Veto** on safety-critical paths. Mute by default. |
| 8 | [Coach](./coach.md) | 🎓 | Long-term maintainability and onboarding lens. | Tie-breaker by lowest onboarding cost. |

## Voting model

Each persona casts a **scored vote per slot**, with a *strength* in
`[-2, +2]`:

| Vote | Meaning |
| :-: | --- |
| +2 | Champion: this is clearly the right call for my remit. |
| +1 | Lean in favour. |
|  0 | Neutral / out of remit. |
| −1 | Concern: another option would be better. |
| −2 | Hard objection: this violates my remit. |

A persona who casts −2 must file a *dissent* — a one-paragraph rationale
appended to `dissents.md`. The Architect can override a single −2 only if
no constraint (C1–C10) is breached; two or more −2 votes block the slot
choice and force a re-round.

The Critic's votes are weighted ×1 like any other persona, but the Critic
has an additional **hard-veto trigger**: if any choice violates the
[constraint catalogue (C1–C10)](../ai-decision-workflow.md#constraint-catalogue),
the Critic can veto regardless of the other votes' arithmetic.

The Senior Engineer holds a similar hard veto for technically unsound
combinations (e.g. picking Schemathesis without any OpenAPI document
anywhere in the spec slot).

## Round structure

```
Round 0 — Consultant runs the intake (7 questions, batched).
Round 1 — Architect proposes a draft composition (one tool per slot).
Round 2 — Each persona reads the draft and casts votes per slot.
Round 3 — Critic challenges; constraint check; Senior + Critic exercise vetoes
          if warranted.
Round 4 — Architect amends; second vote.
Round 5 — Coach breaks ties by onboarding cost; final composition written.
Round 6 — Any dissenting persona files a paragraph in dissents.md.
```

Most projects converge in Round 2 with no vetoes. The structure exists to
make the rare-but-important disagreements explicit and reviewable.

## Why personas, not a single agent?

Three reasons:

1. **Diversity of failure mode.** A single agent that's wrong tends to be
   wrong in one direction; a panel that's wrong shows up as a 4-4 split
   the user can read.
2. **Auditability.** "Why did we pick X?" answered with "because Consultant
   logged this from the user, Architect proposed it, Critic raised Y, the
   panel resolved it by Z" is much better than "the model decided".
3. **Different attention surfaces.** The Critic actively looks for
   problems; the Coach actively looks for onboarding cost; the QA Lead
   actively looks for verification gaps. These are different *attention
   policies*, and forcing the model to enact them separately produces
   better composite reasoning than asking one agent to "consider all
   angles".

## Activation rules

The panel is always 8 personas, but their weights adapt:

| If Phase-1 says… | …then weight these higher |
| --- | --- |
| Greenfield + small team | Coach +0.5, Senior +0.3 |
| Brownfield / monorepo | Critic +0.5, Senior +0.5 |
| Non-engineering reviewers | Product Manager +0.5 |
| Drift critical | QA Lead +0.5 |
| Formal verification needed | Senior +0.5, Security +1.0 (un-muted) |
| Team ≥ 20 | Architect +0.5, Coach +0.5 |
| Mixed editors | Critic +0.3 (portability bias) |

Weights are visible in the final report; nothing is hidden inside the
agent.

## File layout

```
personas/
├── README.md                  ← this file
├── consultant.md
├── senior-engineer.md
├── architect.md
├── critic.md
├── product-manager.md
├── qa-lead.md
├── security-compliance.md
└── coach.md
```

Each persona file declares: remit, knowledge it brings, its veto / authority,
its scoring heuristics, and example dissents.

## Implementing the panel

For a single Claude / GPT / Gemini agent, the cheapest implementation is
**sequential role play**: the orchestrator reads each persona file in
turn, prompts the model to *adopt* that persona, and records the vote.
The orchestrator then runs the constraint check and tie-break logic
itself. This is what the
[AI decision workflow](../ai-decision-workflow.md) prescribes.

For a multi-agent harness (CrewAI, AutoGen, BMAD's Party Mode), each
persona becomes a separate agent with its file as the system prompt.

For deterministic / scriptable runs, populate
[`intake.schema.json`](../intake.schema.json) and run with
`temperature=0` — the panel proceedings become reproducible.
