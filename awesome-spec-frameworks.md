# Awesome Spec-Driven Frameworks

> A curated list of frameworks, conventions, and tools that put a **written
> specification** at the centre of AI-assisted software development.
>
> Last refreshed: 2026-05-12. Entries are sourced from primary repositories
> and documentation — see the *Sources* section at the bottom.

**Spec-driven development (SDD)** treats the spec as the source of truth and
code as its output, the inversion of "code-first, document-later". Frameworks
in this list typically: (1) define a structured spec artefact, (2) impose a
phased intent→spec→plan→tasks→code workflow, or (3) provide conventions that
let humans and agents agree on "done" before any code is written. Prompt
collections, generic agent SDKs, and rule files with no methodology are out
of scope.

Legend: 🟢 active · 🟡 maintained but slow · 🔴 archived ·
🏢 vendor-backed · 🌱 community · 🔒 closed source · ⭐ flagship in its category.

## Table of contents

- [End-to-end SDD frameworks](#end-to-end-sdd-frameworks)
- [Lightweight spec frameworks](#lightweight-spec-frameworks)
- [Vendor-IDE SDD platforms](#vendor-ide-sdd-platforms)
- [Multi-agent / role-play frameworks](#multi-agent--role-play-frameworks)
- [Convention and context files](#convention-and-context-files)
- [Spec languages and notations](#spec-languages-and-notations)
- [Planning, plan/act and architect modes](#planning-planact-and-architect-modes)
- [Task management and orchestration](#task-management-and-orchestration)
- [PRD / intent capture](#prd--intent-capture)
- [Verification and contract layers](#verification-and-contract-layers)
- [Adjacent and supporting tools](#adjacent-and-supporting-tools)
- [Other awesome lists](#other-awesome-lists)
- [Reading list](#reading-list)

---

## End-to-end SDD frameworks

Cover the full intent → spec → plan → tasks → code lifecycle.

- ⭐ **[GitHub Spec Kit](https://github.com/github/spec-kit)** 🟢🏢 — Python
  CLI toolkit, ~93k stars as of May 2026. Four-phase flow with slash commands
  `/specify`, `/plan`, `/tasks`, `/implement`. Supports 30+ coding agents
  (Claude Code, Copilot, Cursor, Gemini CLI, Codex, …). The closest thing to a
  reference implementation of SDD.
- **[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** 🟢🌱 —
  "Breakthrough Method for Agile AI-Driven Development". MIT-licensed,
  ~46k stars. 21 specialised agents (Mary the Analyst, Preston the PM, Winston
  the Architect, Sally the PO, Simon the SM, Devon the Dev, Quinn the QA …)
  plus 50+ workflows. "Party Mode" puts multiple personas in one session.
- **[Agent OS](https://github.com/buildermethods/agent-os)** 🟢🌱 — Three-layer
  context (Standards / Product / Specs). v3 defers spec writing to the host
  agent's plan mode and adds `/shape-spec`, `/discover-standards`. Works with
  Claude Code, Cursor, Antigravity.
- **[Claude Code Spec Workflow (Pimzino)](https://github.com/Pimzino/claude-code-spec-workflow)** 🟢🌱 —
  Requirements → Design → Tasks → Implementation for Claude Code, with a
  parallel bug-fix flow (Report → Analyze → Fix → Verify). Sister project
  [`spec-workflow-mcp`](https://github.com/Pimzino/spec-workflow-mcp) exposes
  the same workflow as an MCP server with a web dashboard and VS Code extension.
- **[SPARC](https://github.com/ruvnet/sparc) / [SPARC2](https://github.com/agenticsorg/sparc2)** 🟢🌱 —
  Specification → Pseudocode → Architecture → Refinement → Completion.
  Integrated into Roo Code's Boomerang orchestration and `claude-flow`.

## Lightweight spec frameworks

Minimal ceremony, plain markdown, designed to graft onto any repo.

- ⭐ **[OpenSpec](https://github.com/Fission-AI/OpenSpec)** 🟢🌱 — Three-phase
  state machine (`propose` → `apply` → `archive`) and *delta specs*
  (`ADDED` / `MODIFIED` / `REMOVED` markers). Explicitly designed for
  brownfield. Each change becomes a folder with `proposal.md`, `specs/`,
  `design.md`, `tasks.md`.
- **[LeanSpec](https://github.com/codervisor/lean-spec)** 🟢🌱 — Lightweight
  SDD built on five "first principles": context economy (specs < 2k tokens),
  signal-to-noise, intent over implementation, bridge the human/AI gap,
  progressive disclosure. Targets <100 lines per spec.
- **[lean-spec / cc-sdd / spec-driver](https://github.com/topics/spec-driven)** 🌱 —
  smaller community frameworks listed under the `spec-driven` GitHub topic.

## Vendor-IDE SDD platforms

Tightly integrated, IDE-bound, vendor-stewarded.

- ⭐ **[Kiro](https://kiro.dev/)** 🟢🏢🔒 — AWS agentic IDE. Spec is "the unit
  of work": `requirements.md` (EARS notation), `design.md`, `tasks.md` per
  feature, plus cross-cutting *steering docs*. Builds a dependency graph from
  tasks and runs independent tasks in concurrent "waves". Agent Hooks and
  MCP integration.
- ⭐ **[Tessl](https://tessl.io/)** 🟢🏢🔒 — "Agent enablement platform".
  Installs "tiles" into `.tessl/`; any MCP-compatible agent (Claude Code,
  Cursor, …) reads them. The
  [spec-driven-development tile](https://github.com/tesslio/spec-driven-development-tile)
  forces interview-first then spec-first behaviour. The
  [Tessl Spec Registry](https://tessl.io/registry/) has 10k+ pre-built specs
  describing OSS libraries so agents don't hallucinate APIs.

## Multi-agent / role-play frameworks

Use named personas to model a real product team.

- **BMAD-METHOD** (see above) — the canonical example.
- **[Roo Code Orchestrator / Boomerang Tasks](https://docs.roocode.com/features/boomerang-tasks)** 🟢🌱 —
  An "Orchestrator" mode breaks a complex task into sub-tasks, each
  delegated to a specialised mode (Code / Architect / Debug). Each runs in
  isolated context; only summaries return to the parent ("boomerang").
- **[claude-flow / Claude-SPARC](https://gist.github.com/ruvnet/e8bb444c6149e6e060a785d1a693a194)** 🟢🌱 —
  Multi-agent SPARC orchestration; swarm mode pursues parallel sub-tasks.

## Convention and context files

Single-file or single-folder conventions any agent can consume.

- ⭐ **[AGENTS.md](https://agents.md/)** 🟢🌱 — Vendor-neutral "README for
  agents". Adopted by OpenAI Codex, GitHub Copilot, Cursor, Aider, Continue,
  Google Jules, Factory, Amp. Stewarded by the
  [Agentic AI Foundation](https://agents.md/) under the Linux Foundation;
  60k+ open-source projects.
- **[CLAUDE.md](https://docs.claude.com/en/docs/claude-code/memory)** 🟢🏢 —
  Claude Code's project-memory convention; hierarchical user/project/local
  scopes.
- **[Cursor Rules](https://docs.cursor.com/context/rules)** 🟢🏢 —
  `.cursor/rules/*.mdc` with YAML frontmatter (`description`, `globs`,
  `alwaysApply`). Four activation modes: Always / Auto-Attached / Agent-Requested
  / Manual. Replaces the older single-file `.cursorrules`.
- **[Aider CONVENTIONS.md](https://aider.chat/docs/usage/conventions.html)** 🟢🌱 —
  Plain-markdown conventions loaded with `/read CONVENTIONS.md` or via
  `.aider.conf.yml`.
- **[Cline Memory Bank](https://docs.cline.bot/features/memory-bank)** 🟢🌱 —
  Six-file structured memory (`projectBrief.md`, `productContext.md`,
  `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`)
  that survives context resets. Pairs with Cline's Plan / Act modes.
- **[Continue.dev rules](https://docs.continue.dev/customization/rules)** 🟢🌱 —
  Composable rule files attached per workspace or model.
- **[GitHub Copilot custom instructions](https://docs.github.com/en/copilot/customizing-copilot/about-customizing-github-copilot-chat-responses)** 🟢🏢 —
  `.github/copilot-instructions.md` repo-level guidance.

## Spec languages and notations

Formal-ish languages designed for AI- or human-readable specs.

- ⭐ **[EARS](https://alistairmavin.com/ears/)** 🟢🌱 — Easy Approach to
  Requirements Syntax. "WHEN … THE SYSTEM SHALL …" patterns developed at
  Rolls-Royce; used by Kiro and many newer frameworks.
- **[Gherkin / Cucumber](https://cucumber.io/docs/gherkin/)** 🟢🌱 —
  Given/When/Then scenarios. Predates AI; re-emerging as spec input.
- **[TLA+](https://lamport.azurewebsites.net/tla/tla.html)** 🟢🌱 — Formal
  spec language for state machines; increasingly paired with LLMs for
  safety-critical systems.
- **[Alloy](https://alloytools.org/)** 🟡🌱 — Lightweight formal modelling.
- **[OpenAPI](https://www.openapis.org/)** /
  **[AsyncAPI](https://www.asyncapi.com/)** /
  **[JSON Schema](https://json-schema.org/)** 🟢🌱 — Structural contracts
  embedded as the "interface" layer of many spec frameworks.
- **[FPF — First Principles Framework](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Rigorous specification framework for modelling systems and knowledge.

## Planning, plan/act and architect modes

Turn an approved spec into an executable plan before any edit lands.

- **[Claude Code plan mode](https://docs.claude.com/en/docs/claude-code/common-workflows)** 🟢🏢 —
  Read-only plan phase; the default planning slot for many other frameworks.
- **[Cline Plan / Act](https://docs.cline.bot/features/memory-bank)** 🟢🌱 —
  Two-mode flow; Plan evaluates Memory Bank completeness, Act executes and
  documents.
- **[Aider architect / editor mode](https://aider.chat/docs/usage/modes.html)** 🟢🌱 —
  Two-model split: a smart "architect" proposes, a cheaper "editor" emits
  the diffs.
- **[Roo Code Architect mode](https://docs.roocode.com/basic-usage/using-modes)** 🟢🌱 —
  Dedicated planning mode; often the entry point to a Boomerang orchestration.

## Task management and orchestration

Spec → task graph → execution.

- **[TaskMaster (`claude-task-master`)](https://github.com/eyaltoledano/claude-task-master)** 🟢🌱 —
  PRD-to-task system, MCP-served. `parse-prd`, `list`, `next`. Topologically
  ordered, dependency-aware task graphs. Works in Cursor, Lovable, Windsurf,
  Roo.
- **[Backlog.md](https://github.com/MrLesk/Backlog.md)** 🟢🌱 — Markdown-first
  task tracking that pairs with most spec frameworks.
- **[Spec Kitty](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  workflow helper for spec-driven repos.
- **[vibe-kanban](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Kanban-style task UI tuned for AI workflows.

## PRD / intent capture

Front-of-the-funnel: capturing what we want before we spec it.

- **[ChatPRD](https://www.chatprd.ai/)** 🟢🏢🔒 — AI co-pilot for PMs;
  drafts and iterates PRDs from briefs. ~100k PM users. Feeds into the
  spec slot of most frameworks.
- **[Amazon PRFAQ / Working Backwards](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/)** 🟢🌱 —
  Press-release-first product definition. The cultural ancestor of much of
  SDD; produces a strong intent artefact.
- **BMAD Analyst persona** — structured discovery as the first BMAD phase.

## Verification and contract layers

Closing the loop: mechanically proving the spec is satisfied.

- ⭐ **[Schemathesis](https://schemathesis.io/)** 🟢🌱 — Property-based API
  testing generated from OpenAPI / GraphQL specs; built on Hypothesis. Finds
  500s, schema violations, validation bypasses, stateful bugs.
- **[Hypothesis](https://hypothesis.works/)** /
  **[fast-check](https://fast-check.dev/)** 🟢🌱 — Property-based testing
  libraries; pair well with spec-derived invariants.
- **[Pact](https://pact.io/)** 🟢🌱 — Consumer-driven contract tests for
  service-to-service.
- **[Stainless](https://www.stainless.com/)** 🟢🏢 — Code generation from
  OpenAPI; useful as the "code-from-spec" half.
- **[BMAD QA persona (Quinn)](https://docs.bmad-method.org/)** — workflow-encoded
  verification gate.
- **[TLA+ model checker (TLC)](https://lamport.azurewebsites.net/tla/tla.html)** 🟢🌱 —
  Exhaustive checking for critical state machines.

## Adjacent and supporting tools

- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** 🟢🌱 —
  Transport that many spec frameworks expose themselves over.
- **[Specstory](https://specstory.com/)** 🟢🏢 — Captures and curates agent
  session history; raw material for after-the-fact specs.
- **[mcp-server-spec-driven-development](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Generic MCP server for SDD workflows.
- **[VibeDoc](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Documentation companion for spec-driven repos.

## Other awesome lists

- [Engineering4AI/awesome-spec-driven-development](https://github.com/Engineering4AI/awesome-spec-driven-development)
- [Software-Engineering-Arena/awesome-spec-driven-development](https://github.com/Software-Engineering-Arena/awesome-spec-driven-development)
- [zhimin-z/Awesome-Spec-Driven-Development](https://github.com/zhimin-z/Awesome-Spec-Driven-Development)
- [aabs/awesome-specification-driven-development](https://github.com/aabs/awesome-specification-driven-development)
- [wearetechnative/awesome-openspec](https://github.com/wearetechnative/awesome-openspec)
- [GitHub topic: `spec-driven`](https://github.com/topics/spec-driven)
- [GitHub topic: `spec-driven-development`](https://github.com/topics/spec-driven-development)

## Reading list

- *"Spec-driven development with AI: get started with a new open source toolkit"* —
  [GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/), 2025.
- *"Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl"* —
  [martinfowler.com](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html).
- *"Diving Into Spec-Driven Development with GitHub Spec Kit"* —
  [Microsoft for Developers](https://developer.microsoft.com/blog/spec-driven-development-spec-kit).
- *"Separating code reasoning and editing"* —
  [Aider blog](https://aider.chat/2024/09/26/architect.html) — the architect/editor pattern.
- *Working Backwards* — Bryar & Carr — the Amazon PRFAQ tradition.
- *"Out of the Tar Pit"* — Moseley & Marks, 2006 — argument for separating
  essential state and logic, which is what a good spec captures.

---

## How to contribute

PRs welcome. Each entry needs: name, link, status emojis, one sentence on
*what makes it spec-driven*, and — if proposing a new category — a one-line
definition. See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Promotional language
and "uses AI" tags-without-substance will be rejected.

## Sources

This refresh was built from web research in May 2026. Key sources:

- GitHub repos and READMEs: github/spec-kit, bmad-code-org/BMAD-METHOD,
  Fission-AI/OpenSpec, buildermethods/agent-os, eyaltoledano/claude-task-master,
  Pimzino/claude-code-spec-workflow, codervisor/lean-spec, tesslio/spec-driven-development-tile,
  RooCodeInc/Roo-Code, Aider-AI/aider, schemathesis/schemathesis.
- Docs sites: kiro.dev/docs, docs.cline.bot, docs.roocode.com, docs.tessl.io,
  aider.chat/docs, agents.md, chatprd.ai, lean-spec.dev.
- Surveys: MarkTechPost "9 Best AI Tools for SDD in 2026"; Augment Code
  "Best SDD Tools 2026"; Medium overviews by Vishal Mysore and Tim Wang;
  Martin Fowler "Exploring Gen AI — SDD with 3 tools".
- Existing awesome lists (linked above).
