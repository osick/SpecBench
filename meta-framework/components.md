# SpecMeta components

Catalogue of concrete options per slot, with the trade-off in one line each.

## Slot 1 — Context

| Option | When to choose |
| --- | --- |
| `AGENTS.md` | Default. Multi-agent repos, vendor-neutral. |
| `CLAUDE.md` | Claude-Code-only repos that want hierarchical memory. |
| `cursor-rules` | Cursor-only teams; need path-scoped rules. |
| `cline-memory-bank` | Long-running projects where context resets are a real problem. |
| `combine` | Use AGENTS.md as the canonical file, symlink or duplicate to others. |

## Slot 2 — Intent

| Option | When to choose |
| --- | --- |
| `intent.md` | You already do PRFAQ-ish docs. Lowest tool overhead. |
| `chatprd` | Non-engineering PM owns intent and wants help shaping it. |
| `bmad-analyst` | You want a structured discovery phase before any spec. |
| `prfaq` | Long-term vision documents (Amazon-style). |

## Slot 3 — Spec

| Option | Strength | Watch out for |
| --- | --- | --- |
| `spec-kit` | Reviewable markdown, multi-agent. | No drift detection. |
| `kiro-ears` | Best precision; great for compliance. | Vendor-locked unless you mimic the format manually. |
| `openspec` | Lowest ceremony; pure git. | You provide the rigour. |
| `tessl` | Eliminates drift by construction. | Platform lock-in. |
| `tla-plus` | Formal proofs. | Steep learning curve; reserved for critical paths. |

## Slot 4 — Plan

| Option | When to choose |
| --- | --- |
| `spec-kit` | If you picked Spec Kit for slot 3, stay in it. |
| `claude-plan-mode` | Quick read-only plan; useful inside any framework. |
| `aider-architect` | Two-model setup with cheap edits + smart planner. |
| `bmad-architect` | You need a real architecture document, not just a plan. |

## Slot 5 — Tasks

| Option | When to choose |
| --- | --- |
| `spec-kit-tasks` | Stay in family. |
| `taskmaster` | You want an MCP-served task graph queryable by multiple agents. |
| `backlog-md` | You already manage work in markdown task files. |
| `bmad-sm` | You want sharded stories with QA gates. |
| `github-issues` | Your team's source of truth is Issues; mirror tasks there. |

## Slot 6 — Implementation

| Option | When to choose |
| --- | --- |
| `claude-code` | Default for CLI-centric teams. |
| `cursor` | IDE-centric teams; tight editor integration. |
| `cline` | You want plan/act mode discipline. |
| `aider` | Strong git-diff workflow; small models OK. |
| `copilot-coding-agent` | GitHub-native PR-based execution. |

## Slot 7 — Verification

| Option | Pairs well with | Notes |
| --- | --- | --- |
| `unit-tests` | anything | Baseline. |
| `property-tests` (Hypothesis, fast-check) | OpenSpec, Spec Kit | Best ROI when the spec defines invariants. |
| `schemathesis` | any spec with OpenAPI | Mechanically derives API tests. |
| `pact` | service-to-service | Consumer-driven contracts. |
| `bmad-qa` | BMAD | Persona writes and runs tests as a phase gate. |
| `tla-model-check` | TLA+ | For safety-critical workflows. |

## Cross-slot constraints

- If `spec=tessl`, slots 4–7 are largely subsumed; leave them blank.
- If `implementation=copilot-coding-agent`, slot 1 must include `AGENTS.md`
  (Copilot reads it natively).
- If `verification` includes `schemathesis`, slot 3 must embed an OpenAPI doc.
- If portability matters, avoid any choice with score 1 on dimension 5 in
  [`benchmark/results.md`](../benchmark/results.md).
