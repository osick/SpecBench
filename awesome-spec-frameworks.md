# Awesome Spec-Driven Frameworks

> A curated list of frameworks, conventions, and tools that put a **written
> specification** at the centre of AI-assisted software development.

Inclusion criteria — a project is listed if it does at least one of:

1. Defines a structured spec artefact (markdown, YAML, EARS, Gherkin, …) that
   drives agent behaviour.
2. Provides a phased workflow (intent → spec → plan → tasks → code) that an
   AI agent follows.
3. Offers conventions or contracts that let humans and agents agree on
   what "done" means before code is written.

Pure prompt collections, generic agent SDKs, and "rules files" with no
methodology behind them are out of scope.

Legend: 🟢 active · 🟡 maintained but slow · 🔴 archived/abandoned ·
🏢 vendor-backed · 🌱 community · 🔒 closed source.

---

## End-to-end spec frameworks

These define a full intent→spec→plan→code lifecycle.

- **[GitHub Spec Kit](https://github.com/github/spec-kit)** 🟢🏢 — `/specify`,
  `/plan`, `/tasks`, `/implement` slash-command flow producing markdown specs,
  technical plans, and task lists; works with Claude Code, Cursor, Copilot,
  Gemini CLI. The reference implementation of "phased SDD".
- **[Kiro](https://kiro.dev/)** 🟢🏢🔒 — AWS IDE that codifies SDD with
  `requirements.md` (EARS notation), `design.md`, and `tasks.md` per feature;
  steering docs hold cross-cutting context. Tight IDE integration, vendor-locked.
- **[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** 🟢🌱 —
  "Breakthrough Method of Agile AI-Driven Development". Multi-agent role play
  (Analyst, PM, Architect, SM, Dev, QA) producing a PRD, architecture, sharded
  stories, and code. Heavy but thorough.
- **[OpenSpec](https://github.com/Fission-AI/OpenSpec)** 🟢🌱 — Lightweight
  "spec → change-proposal → archive" workflow stored entirely in markdown in
  the repo. Agent-agnostic; designed to be reviewed in normal PRs.
- **[Tessl](https://www.tessl.io/)** 🟢🏢🔒 — Commercial platform that treats
  specs as the source of truth and regenerates code from them; introduces the
  idea of a "spec registry".
- **[Agent OS](https://buildermethods.com/agent-os)** 🟢🌱 — Three-layer
  context system (Standards / Product / Specs) with phased commands for
  Claude Code and Cursor.
- **[ChatPRD](https://www.chatprd.ai/)** 🟢🏢🔒 — Focused on the
  *product-requirements* end of the pipeline; outputs feed into other frameworks.

## Convention / context files

Single-file or single-folder conventions that any agent can consume.

- **[AGENTS.md](https://agents.md/)** 🟢🌱 — Vendor-neutral counterpart to
  `README.md` aimed at agents. Adopted by OpenAI Codex, Cursor, Aider,
  Continue, Jules and others.
- **[CLAUDE.md](https://docs.claude.com/en/docs/claude-code/memory)** 🟢🏢 —
  Claude Code's project-memory convention; hierarchical (user/project/local).
- **[Cursor Rules](https://docs.cursor.com/context/rules)** 🟢🏢 — `.cursor/rules/*.mdc`
  files with frontmatter for scoping; can be auto-attached by path globs.
- **[Aider CONVENTIONS.md](https://aider.chat/docs/usage/conventions.html)** 🟢🌱
   — Plain-markdown conventions file read on every turn.
- **[Cline Memory Bank](https://docs.cline.bot/prompting/cline-memory-bank)** 🟢🌱
   — Structured set of markdown files (projectbrief, productContext,
  systemPatterns, …) that survive context resets.
- **[Continue.dev rules](https://docs.continue.dev/customization/rules)** 🟢🌱 —
  Composable rule files attached per workspace or per model.

## Spec languages and notations

Formal-ish languages designed for AI-readable specs.

- **[EARS](https://alistairmavin.com/ears/)** 🟢🌱 — Easy Approach to
  Requirements Syntax. The "WHEN … THE SYSTEM SHALL …" pattern used by Kiro
  and many others.
- **[Gherkin / Cucumber](https://cucumber.io/docs/gherkin/)** 🟢🌱 — Given/When/Then
  scenarios; long predates AI but is re-emerging as a spec input.
- **[TLA+](https://lamport.azurewebsites.net/tla/tla.html)** 🟢🌱 — Formal
  spec language; increasingly paired with LLMs for safety-critical systems.
- **[Alloy](https://alloytools.org/)** 🟡🌱 — Lightweight formal modelling,
  similar role.
- **[JSON Schema](https://json-schema.org/)** / **[OpenAPI](https://www.openapis.org/)**
  / **[AsyncAPI](https://www.asyncapi.com/)** 🟢🌱 — Structural contracts that
  many spec frameworks embed as the "interface" layer.

## Planning / task-graph tools

Tools that turn a spec into an executable plan.

- **[Claude Code plan mode](https://docs.claude.com/en/docs/claude-code/common-workflows#use-extended-thinking)** 🟢🏢 —
  Read-only plan phase before edits.
- **[Cline Plan / Act](https://docs.cline.bot/features/plan-and-act)** 🟢🌱 —
  Two-mode flow inspired by Aider's `architect` / `editor`.
- **[Aider architect/editor modes](https://aider.chat/docs/usage/modes.html)** 🟢🌱
   — Separate "design" model and "diff" model.
- **[TaskMaster](https://github.com/eyaltoledano/claude-task-master)** 🟢🌱 —
  PRD → task graph → execution, MCP-compatible.
- **[Roo Code "Orchestrator"](https://docs.roocode.com/features/boomerang-tasks)** 🟢🌱 —
  Breaks a spec into delegated sub-tasks ("boomerang tasks").

## Verification / contract layers

Closing the loop so the agent can prove the spec is satisfied.

- **[Property-based testing](https://hypothesis.works/)** (Hypothesis, fast-check)
  — Pair well with spec-derived invariants.
- **[Pact](https://pact.io/)** 🟢🌱 — Consumer-driven contract tests.
- **[Schemathesis](https://schemathesis.readthedocs.io/)** 🟢🌱 — Generates
  tests from OpenAPI specs.
- **[Stainless](https://www.stainless.com/)** 🟢🏢 — Code generation from
  OpenAPI; useful as the "code-from-spec" half.

## Adjacent / supporting

- **[MCP (Model Context Protocol)](https://modelcontextprotocol.io/)** 🟢🌱 —
  Transport layer; many spec frameworks expose themselves as MCP servers.
- **[Specstory](https://specstory.com/)** 🟢🏢 — Captures and curates
  agent-session history; useful raw material for after-the-fact specs.
- **[Backlog.md](https://github.com/MrLesk/Backlog.md)** 🟢🌱 — Markdown-first
  task management that pairs with most spec frameworks.

## Reading list

- *"Spec-driven development"* — GitHub Engineering blog, 2025.
- *"Working backwards from the README"* — Amazon PRFAQ tradition that
  inspired much of SDD.
- *"Out of the Tar Pit"* — Moseley & Marks, 2006. Still the clearest
  argument for separating essential state and logic, which is what a good
  spec captures.
- *"AI Engineering"* — Chip Huyen, 2025, ch. 6 on evaluation harnesses.

---

## How to contribute an entry

PRs welcome. Each entry needs: name, link, status emojis, one sentence on
*what makes it spec-driven* (not just "uses AI"), and — if you're proposing
a new category — a one-line definition of the category. See
[`CONTRIBUTING.md`](./CONTRIBUTING.md).
