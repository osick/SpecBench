# SpecMeta AI Decision Workflow

A reproducible, AI-driven workflow that takes a short project description
and emits a concrete [`specmeta.yaml`](./specmeta.schema.yaml) composition
with reasoning. Designed to run with any general-purpose coding agent
(Claude Code, Cursor, Copilot, Codex, Gemini CLI, …).

## Goal

Replace the static [decision tree](./decision-tree.md) with an AI-mediated
interview that:

1. Elicits seven dimensions of the project profile in a fixed order.
2. Scores candidate tools per slot using the
   [SpecBench rubric](../BENCHMARK.md#rubric).
3. Applies cross-slot constraints from [`components.md`](./components.md).
4. Emits a *justified* `specmeta.yaml` — every slot choice cites the rule
   or evidence that drove it.
5. Stops early when the user provides enough information; asks the minimum
   number of clarifying questions.

The workflow is the AI agent's analogue of a 1-hour design conversation
with a senior engineer. Output is a file you commit, not a chat reply.

## Workflow shape

```
┌──────────────────────────────────────────────────────────────┐
│ Phase 0 — Initialise                                         │
│  Load: components.md, results.md, decision-tree.md, schema    │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Phase 1 — Project intake (≤ 7 questions, batched)            │
│  Q1 Greenfield vs existing?                                  │
│  Q2 Non-engineering stakeholders in spec review?             │
│  Q3 Portability vs vendor-IDE tolerance?                     │
│  Q4 Drift-resistance importance (low/med/critical)?          │
│  Q5 Formal verification needed anywhere?                     │
│  Q6 Team size / review culture?                              │
│  Q7 Editor / agent preference?                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Phase 2 — Constraint propagation                             │
│  Apply cross-slot rules from components.md.                  │
│  Eliminate options that violate a hard constraint.           │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Phase 3 — Per-slot scoring                                   │
│  For each of 7 slots, score remaining candidates on the      │
│  rubric dimensions weighted by Phase-1 answers.              │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Phase 4 — Compose & justify                                  │
│  Pick the top-scored option per slot; write specmeta.yaml    │
│  with a `rationale` field per slot.                          │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Phase 5 — Sanity check                                       │
│  Re-validate against constraints; check against the closest  │
│  recipe; flag if the result is unusual ("not like any        │
│  shipped recipe — review carefully").                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
                       specmeta.yaml
```

## Constraint catalogue

These are hard rules the AI must respect; violation invalidates the
composition.

| ID | Rule |
| -- | --- |
| C1 | If `portability` weight > 0.7, exclude every option with portability score ≤ 1 in [`results.md`](../benchmark/results.md). |
| C2 | If `spec = tessl`, slots `plan` / `tasks` / `implementation` may be `null` (Tessl subsumes them). |
| C3 | If `implementation = copilot-coding-agent`, slot `context` must contain `AGENTS.md`. |
| C4 | If any element of `verification` includes `schemathesis`, slot `spec` must embed an OpenAPI document. |
| C5 | If `formal_verification = true`, slot `spec` must include `tla-plus` *or* `alloy` (additive, not replacing the human-readable spec). |
| C6 | If `team_size < 5`, prefer onboarding-cost ≥ 3; exclude BMAD-METHOD unless user explicitly opts in. |
| C7 | If `team_size ≥ 20`, prefer drift-resistance ≥ 3; require an explicit verification slot. |
| C8 | If `greenfield = false`, prefer `openspec` for `spec` unless another option dominates by ≥ 1 point on every other relevant dimension. |
| C9 | Never emit `null` for `context`, `spec`, or `implementation` — these slots are required by the schema. |
| C10 | If two candidates tie within 0.5 points, pick the one with lower onboarding cost. |

## Dimension weighting from Phase-1 answers

A simple, transparent mapping; the AI must show its work.

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

Default weights start at 1.0 per dimension; each "matters" adjustment adds
+0.5 (max 3.0). The agent must print the resolved weight vector before
scoring.

## Prompt template

Drop this into a file the agent reads (e.g.
`.claude/commands/pick-specmeta.md` for Claude Code, or
`/specmeta` rule in Cursor) and invoke as a slash command.

````markdown
# /pick-specmeta — decide a SpecMeta composition

You are the SpecMeta Decision Agent. Your job is to produce a
`specmeta.yaml` that fits this project, with a per-slot rationale.

## Inputs you have

- This repo's existing files (read them; note any signals).
- `meta-framework/components.md` (the slot catalogue).
- `benchmark/results.md` (per-framework scores on 8 dimensions).
- `meta-framework/decision-tree.md` (the human decision tree).
- `meta-framework/ai-decision-workflow.md` (this file — the procedure
  and the constraint catalogue C1–C10).
- `meta-framework/specmeta.schema.yaml` (output schema).
- `meta-framework/recipes/*.md` (reference compositions).

## Procedure (follow in order)

1. **Read** the inputs listed above. If a file is missing, stop and
   ask the user to point you at it.
2. **Interview** the user with the seven intake questions from
   `ai-decision-workflow.md` § Phase 1. Batch them when possible.
   Re-use any answers already evident from the repo (e.g. detect an
   existing `.cursor/rules/` folder and infer editor preference).
3. **Print the resolved weight vector** for the eight rubric dimensions
   in a small table. Do not skip this step — the user must be able to
   challenge the weights before you score.
4. **Apply constraints C1–C10**, listing each elimination.
5. **Score** each slot's candidates as: `weighted_score = Σ (weight_d ×
   framework_score_d)` over the dimensions in `results.md`. Show a
   small per-slot scoring table.
6. **Compose** `specmeta.yaml` at the repo root using the schema. Each
   slot must carry a `# rationale: …` comment citing (a) the top one or
   two dimensions that decided it and (b) any constraint that pinned it.
7. **Sanity check**: compare the composition to the four shipped
   recipes (`greenfield-startup`, `enterprise-monorepo`,
   `solo-prototype`, `safety-critical`). If the result matches none of
   them within 2 slots, append a `notes:` warning to the file.
8. **Stop**. Do not implement any spec yet; do not modify other files.

## Output

A single new file `specmeta.yaml` at the repo root, plus a short summary
in chat (≤ 8 lines) that lists each slot, its choice, and the dominant
reason. No code edits, no PRs.

## Anti-patterns (refuse to emit)

- Picking a vendor-locked tool when the user said portability matters.
- Picking BMAD for a 2-person team without an explicit opt-in.
- Filling `verification` with only `unit-tests` when the user marked
  drift-resistance as critical.
- Skipping the weight-vector print-out.
````

## Example run (abbreviated)

```
User: 4-engineer fintech startup, new repo, building a payments API,
      need audit trail, willing to use Cursor.

Agent: Detected new repo. Reading inputs… done.

       Intake answers (inferred + confirmed):
       Q1 greenfield: yes
       Q2 non-eng reviewers: yes (auditor)
       Q3 portability: medium
       Q4 drift: critical (audit)
       Q5 formal verification: no
       Q6 team: 4
       Q7 editor: Cursor

       Resolved weights:
       spec-quality 2.0  traceability 2.0  lifecycle 1.0
       reviewability 2.0  portability 1.5  drift 2.5
       onboarding 1.5    verification 2.5

       Constraints applied: C6 excludes BMAD; C4 not triggered;
       C8 N/A (greenfield).

       Top picks per slot (full scoring tables omitted here):
       context        AGENTS.md + cursor-rules
       intent         intent.md
       spec           spec-kit         (reviewability 4, portability 4)
       plan           spec-kit
       tasks          spec-kit
       implementation cursor
       verification   pytest, schemathesis, pact

       Closest recipe: greenfield-startup (matches 6/7 slots).
       Wrote specmeta.yaml.
```

## Running it without an interactive user

For CI or onboarding scripts, pass a JSON answer file:

```json
{
  "greenfield": true,
  "non_engineer_reviewers": true,
  "portability_priority": "medium",
  "drift_priority": "critical",
  "formal_verification": false,
  "team_size": 4,
  "editor": "cursor"
}
```

The agent treats this as if the user had answered Phase 1; Phases 2–5
proceed unchanged. This makes the workflow scriptable and
deterministic when paired with `temperature=0`.

## Why an AI workflow and not a script?

A pure scoring script collapses the moment your project has a
constraint the rubric didn't anticipate — "we use Bazel and our specs
need to live next to BUILD files" or "we just hired an engineer who
hates Cursor". The AI agent's value is reading those signals out of
the repo and the conversation and pulling in the relevant rules
without you having to encode every edge case.

The structure here (fixed phases, explicit weight vector, listed
constraints, mandatory rationales) is deliberately *over*-specified to
keep the agent from hand-waving. The output should look like a
checklist someone could redo by hand and reach the same answer.

## Roadmap

- v0.2: add a `specmeta-lint` script that validates a written
  `specmeta.yaml` against C1–C10 mechanically.
- v0.3: ship per-agent invocation files (`.claude/commands/`,
  `.cursor/rules/`, `.github/copilot-instructions.md`) so the workflow
  is one slash-command away.
- v0.4: feed real benchmark scorecard YAML (not paper evals) into
  Phase 3 so the agent picks based on measured numbers.
