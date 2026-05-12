# Awesome Spec-Driven Development

> A curated and benchmarked list of frameworks, tools, helpers, articles,
> talks, courses, books, and reports for **spec-driven development (SDD)** —
> the practice of putting a written specification at the centre of
> AI-assisted software engineering.
>
> Last refreshed: 2026-05-12. Star history, scores, and dates are based on
> the primary repositories and the *Sources* section at the bottom.

Spec-driven development is the counter-movement to
[vibe coding](https://x.com/karpathy/status/1886192184808149383): instead of
throwing prompts at an LLM and hoping, you write a structured, versioned
spec first and let agents work against it. SpecBench provides three things:

- **This list** — every tool, helper, article, paper, podcast, and report
  we've found that meaningfully advances SDD. Curated, opinionated,
  annotated.
- **[`BENCHMARK.md`](./BENCHMARK.md) + [`benchmark/`](./benchmark/)** — a
  reproducible 8-dimension benchmark with scorecards for the main
  frameworks; see [aggregated results](./benchmark/results.md).
- **[`meta-framework/`](./meta-framework/) — SpecMeta** — a meta-framework
  that decomposes SDD into 7 reusable slots and uses a **panel of AI
  personas** (Consultant, Senior, Architect, Critic, PM, QA, Security,
  Coach) to compose a `specmeta.yaml` for your specific project.

Inclusion criteria — a resource is listed if it does at least one of:
defines a structured spec artefact; provides a phased
intent→spec→plan→tasks→code workflow; offers conventions that let humans
and agents agree on "done"; or — for articles, books, talks — meaningfully
informs the practice. Pure prompt collections, generic agent SDKs, and
"rules files" with no methodology are out of scope.

Legend: 🟢 active · 🟡 maintained but slow · 🔴 archived ·
🏢 vendor-backed · 🌱 community · 🔒 closed source · ⭐ flagship in its
category · 🎓 educational · 📄 paper · 📘 book · 🎤 talk · 🎧 podcast ·
📊 report.

## Table of contents

**Frameworks & tools**
1. [End-to-end SDD frameworks](#1-end-to-end-sdd-frameworks)
2. [Lightweight spec frameworks](#2-lightweight-spec-frameworks)
3. [Vendor-IDE SDD platforms](#3-vendor-ide-sdd-platforms)
4. [Multi-agent / role-play frameworks](#4-multi-agent--role-play-frameworks)
5. [Context and convention files](#5-context-and-convention-files)
6. [Spec languages and notations](#6-spec-languages-and-notations)
7. [Planning, plan/act, architect modes](#7-planning-planact-architect-modes)
8. [Task management and orchestration](#8-task-management-and-orchestration)
9. [PRD / intent capture](#9-prd--intent-capture)
10. [Verification, contracts, formal methods](#10-verification-contracts-formal-methods)
11. [Helpers, linters, validators](#11-helpers-linters-validators)
12. [MCP servers and dashboards](#12-mcp-servers-and-dashboards)
13. [Prompt and skill libraries](#13-prompt-and-skill-libraries)
14. [Adjacent and supporting tools](#14-adjacent-and-supporting-tools)

**Learning & community**
15. [Courses and trainings](#15-courses-and-trainings) 🎓
16. [Books](#16-books) 📘
17. [Articles and essays](#17-articles-and-essays)
18. [Academic papers](#18-academic-papers) 📄
19. [Talks and videos](#19-talks-and-videos) 🎤
20. [Podcasts](#20-podcasts) 🎧
21. [Industry reports and statistics](#21-industry-reports-and-statistics) 📊
22. [Historical lineage](#22-historical-lineage)
23. [Other awesome lists](#23-other-awesome-lists)
24. [Communities](#24-communities)

[Contributing](#contributing) · [Sources](#sources)

---

## 1. End-to-end SDD frameworks

Cover the full intent → spec → plan → tasks → code lifecycle.

- ⭐ **[GitHub Spec Kit](https://github.com/github/spec-kit)** 🟢🏢 — Python
  CLI toolkit. Four-phase slash-command flow: `/specify`, `/plan`,
  `/tasks`, `/implement`. Supports 30+ coding agents
  (Claude Code, Copilot, Cursor, Gemini CLI, Codex). The most adopted
  open-source SDD reference implementation; ~93k stars as of May 2026.
- **[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** 🟢🌱 —
  "Breakthrough Method for Agile AI-Driven Development". MIT, ~46k stars.
  21 named-persona agents (Mary the Analyst, Preston the PM, Winston the
  Architect, Sally the PO, Simon the SM, Devon the Dev, Quinn the QA …)
  and 50+ workflows. "Party Mode" puts multiple personas in one session.
- **[Agent OS](https://github.com/buildermethods/agent-os)** 🟢🌱 —
  Three-layer context (Standards / Product / Specs). v3 defers spec
  writing to the host agent's plan mode and adds `/shape-spec` and
  `/discover-standards`. Works with Claude Code, Cursor, Antigravity.
- **[Claude Code Spec Workflow (Pimzino)](https://github.com/Pimzino/claude-code-spec-workflow)** 🟢🌱 —
  Requirements → Design → Tasks → Implementation flow for Claude Code,
  with a parallel bug-fix workflow (Report → Analyze → Fix → Verify).
- **[cc-sdd](https://github.com/gotalab/cc-sdd)** 🟢🌱 — A minimal,
  adaptable SDD harness packaged as Agent Skills. Supports Claude Code,
  Codex, Cursor, Copilot, Windsurf, OpenCode, Gemini CLI, Antigravity.
  Phase-gated: agents write the spec, humans approve the contract.
- **[MoAI-ADK](https://github.com/modu-ai/moai-adk)** 🟢🌱 — Agentic
  Development Kit for Claude Code with 24 specialised agents and 52
  skills. Auto-applies TDD on greenfield, DDD on brownfield-with-no-tests.
- **[Colign](https://github.com/colign/colign)** 🟢🌱 — AI-powered
  spec-writing and team-alignment platform. Exposes specs as an MCP
  server so Claude Code, Cursor, Windsurf, and VS Code Copilot can all
  read/write them.
- **[SPARC](https://github.com/ruvnet/sparc) / [SPARC2](https://github.com/agenticsorg/sparc2) / [claude-flow](https://github.com/ruvnet/ruflo)** 🟢🌱 —
  Specification → Pseudocode → Architecture → Refinement → Completion.
  Integrated with Roo Boomerang orchestration and `claude-flow` swarm mode.
- **[cc-spex](https://github.com/rhuss/cc-spex)** 🟢🌱 — SDD based on
  Spec Kit, extended with custom traits.

## 2. Lightweight spec frameworks

Minimal ceremony, plain markdown, designed to graft onto any repo.

- ⭐ **[OpenSpec](https://github.com/Fission-AI/OpenSpec)** 🟢🌱 — Three-phase
  state machine (`propose` → `apply` → `archive`) and *delta specs*
  (`ADDED` / `MODIFIED` / `REMOVED` markers). Explicitly designed for
  brownfield. Each change becomes a folder with `proposal.md`, `specs/`,
  `design.md`, `tasks.md`. Companion list:
  [awesome-openspec](https://github.com/wearetechnative/awesome-openspec).
- **[LeanSpec](https://github.com/codervisor/lean-spec)** 🟢🌱 — Five
  first principles: context economy (specs < 2k tokens), signal-to-noise,
  intent over implementation, bridge the human/AI gap, progressive
  disclosure. Targets <100 lines per spec.
- **[fspec](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Gherkin-based spec system that auto-generates tests and links code to
  business rules.
- **[spec-driver](https://github.com/topics/spec-driven)** 🌱 — small
  community framework from the `spec-driven` topic.
- **[Shotgun / get-shit-done / MetaSpec / quint-code / adversarial-spec](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  smaller experimental frameworks tracked by the Engineering4AI list.

## 3. Vendor-IDE SDD platforms

Tightly integrated, IDE-bound, vendor-stewarded.

- ⭐ **[Kiro](https://kiro.dev/)** 🟢🏢🔒 — AWS agentic IDE. Spec is "the unit
  of work": `requirements.md` (EARS notation), `design.md`, `tasks.md`
  per feature, plus cross-cutting *steering docs*. Builds a dependency
  graph from tasks and runs independent tasks in concurrent "waves".
  Agent Hooks and MCP integration.
- ⭐ **[Tessl](https://tessl.io/)** 🟢🏢🔒 — Agent Enablement Platform.
  Installs "tiles" into `.tessl/`; any MCP-compatible agent reads them.
  The
  [spec-driven-development tile](https://github.com/tesslio/spec-driven-development-tile)
  forces interview-first then spec-first behaviour. The
  [Tessl Spec Registry](https://tessl.io/registry/) has 10k+ pre-built
  specs of OSS libraries so agents don't hallucinate APIs.
- **[Zencoder](https://docs.zencoder.ai/user-guides/tutorials/spec-driven-development-guide)** 🟢🏢🔒 —
  IDE assistant with a documented spec-driven workflow.

## 4. Multi-agent / role-play frameworks

Use named personas to model a real product team.

- **BMAD-METHOD** (see §1) — the canonical example with 21 personas.
- **[Roo Code Orchestrator / Boomerang Tasks](https://docs.roocode.com/features/boomerang-tasks)** 🟢🌱 —
  An "Orchestrator" mode breaks a complex task into sub-tasks,
  each delegated to a specialised mode (Code / Architect / Debug). Each
  sub-task runs in isolated context; only summaries return to the parent
  ("boomerang").
- **[CrewAI](https://github.com/crewaiinc/crewai)** 🟢🌱 — Framework for
  orchestrating role-playing autonomous agents — each agent has a role,
  goal, and backstory. Not SDD-specific but widely used to *build* SDD
  pipelines.
- **[Microsoft AutoGen](https://github.com/microsoft/autogen)** 🟢🏢 —
  Conversational multi-agent framework with the classic Solver/Critic
  pattern. Often the substrate under custom SDD orchestrations.
- **[awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)** 🟢🌱 —
  100+ specialised Claude Code subagents covering many development use
  cases.
- **[claude-flow swarm mode](https://github.com/ruvnet/ruflo/wiki/SPARC-Methodology)** 🟢🌱 —
  Parallel SPARC sub-tasks with a swarm coordinator.

## 5. Context and convention files

Single-file or single-folder conventions any agent can consume.

- ⭐ **[AGENTS.md](https://agents.md/)** 🟢🌱 — Vendor-neutral "README
  for agents". Adopted by OpenAI Codex, GitHub Copilot, Cursor, Aider,
  Continue, Google Jules, Factory, Amp. Stewarded by the
  Agentic AI Foundation under the Linux Foundation; 60k+ open-source
  projects.
- **[CLAUDE.md](https://docs.claude.com/en/docs/claude-code/memory)** 🟢🏢 —
  Claude Code's project-memory convention; hierarchical user/project/local
  scopes.
- **[Cursor Rules `.mdc`](https://docs.cursor.com/context/rules)** 🟢🏢 —
  YAML frontmatter (`description`, `globs`, `alwaysApply`). Four
  activation modes: Always / Auto-Attached / Agent-Requested / Manual.
  Replaces the older single-file `.cursorrules`. Reference list:
  [awesome-cursor-rules-mdc](https://github.com/sanjeed5/awesome-cursor-rules-mdc).
- **[GitHub Copilot custom instructions](https://docs.github.com/en/copilot/customizing-copilot/about-customizing-github-copilot-chat-responses)** 🟢🏢 —
  `.github/copilot-instructions.md` repo-level guidance.
- **[Aider CONVENTIONS.md](https://aider.chat/docs/usage/conventions.html)** 🟢🌱 —
  Plain-markdown conventions loaded via `/read CONVENTIONS.md` or
  `.aider.conf.yml`.
- **[Cline Memory Bank](https://docs.cline.bot/features/memory-bank)** 🟢🌱 —
  Six-file structured memory (`projectBrief.md`, `productContext.md`,
  `systemPatterns.md`, `techContext.md`, `activeContext.md`,
  `progress.md`) that survives context resets. Pairs with Cline Plan/Act.
- **[Continue.dev rules](https://docs.continue.dev/customization/rules)** 🟢🌱 —
  Composable rule files attached per workspace or model.

## 6. Spec languages and notations

Formal-ish languages designed for human + AI consumption.

- ⭐ **[EARS](https://alistairmavin.com/ears/)** 🟢🌱 — Easy Approach to
  Requirements Syntax. "WHEN … THE SYSTEM SHALL …" patterns developed at
  Rolls-Royce; used by Kiro and many newer frameworks.
- **[Gherkin / Cucumber](https://cucumber.io/docs/gherkin/)** 🟢🌱 —
  Given/When/Then BDD scenarios. Predates AI; re-emerging as spec input.
- **[SpecFlow / Reqnroll](https://reqnroll.net/)** 🟢🌱 — .NET BDD framework
  (Reqnroll is the maintained Reqnroll fork of SpecFlow).
- **[TLA+](https://lamport.azurewebsites.net/tla/tla.html)** 🟢🌱 — Formal
  spec language for state machines; increasingly paired with LLMs for
  safety-critical systems.
- **[Alloy](https://alloytools.org/)** 🟡🌱 — Lightweight formal modelling.
- **[Spec# / JML / OCL](https://en.wikipedia.org/wiki/Design_by_contract)** —
  Design-by-Contract heirs to Eiffel.
- **[OpenAPI](https://www.openapis.org/) /
  [AsyncAPI](https://www.asyncapi.com/) /
  [JSON Schema](https://json-schema.org/) /
  [Protocol Buffers](https://protobuf.dev/) /
  [GraphQL SDL](https://graphql.org/learn/schema/)** 🟢🌱 — Structural
  contracts embedded as the "interface" layer of many spec frameworks.
- **[FPF — First Principles Framework](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Rigorous specification framework for modelling systems and knowledge.

## 7. Planning, plan/act, architect modes

Turn an approved spec into an executable plan before any edit lands.

- **[Claude Code plan mode](https://docs.claude.com/en/docs/claude-code/common-workflows)** 🟢🏢 —
  Read-only plan phase; the default planning slot for many other frameworks.
- **[Cline Plan / Act](https://docs.cline.bot/features/memory-bank)** 🟢🌱 —
  Plan evaluates Memory Bank completeness, Act executes and documents.
- **[Aider architect / editor mode](https://aider.chat/docs/usage/modes.html)** 🟢🌱 —
  Two-model split: smart "architect" proposes, cheaper "editor" emits diffs.
- **[Roo Code Architect mode](https://docs.roocode.com/basic-usage/using-modes)** 🟢🌱 —
  Dedicated planning mode; entry point to Boomerang orchestration.
- **[Goose plan mode](https://block.github.io/goose/)** 🟢🌱 — Block's
  open-source agent with a separate planning step.

## 8. Task management and orchestration

Spec → task graph → execution.

- **[TaskMaster (`claude-task-master`)](https://github.com/eyaltoledano/claude-task-master)** 🟢🌱 —
  PRD-to-task system, MCP-served. `parse-prd`, `list`, `next`.
  Topologically ordered, dependency-aware. Works in Cursor, Lovable,
  Windsurf, Roo.
- **[Backlog.md](https://github.com/MrLesk/Backlog.md)** 🟢🌱 — Markdown-first
  task tracking.
- **[Spec Kitty](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Workflow helper for spec-driven repos.
- **[vibe-kanban](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Kanban UI tuned for AI workflows.

## 9. PRD / intent capture

Front-of-the-funnel: capturing what we want before we spec it.

- **[ChatPRD](https://www.chatprd.ai/)** 🟢🏢🔒 — AI PM co-pilot; drafts
  and iterates PRDs from briefs. ~100k PM users.
- **[Amazon PRFAQ / Working Backwards](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/)** 🟢🌱 —
  Press-release-first product definition. Cultural ancestor of much SDD.
- **[Vibe Coding Prompt Template](https://github.com/KhazP/vibe-coding-prompt-template)** 🟢🌱 —
  Templates and workflow for generating PRDs, tech designs, MVPs via LLMs.
- **BMAD Analyst persona (Mary)** — structured discovery phase.

## 10. Verification, contracts, formal methods

Closing the loop: mechanically proving the spec is satisfied.

- ⭐ **[Schemathesis](https://schemathesis.io/)** 🟢🌱 — Property-based
  API testing generated from OpenAPI / GraphQL. Built on Hypothesis.
  Finds 500s, schema violations, validation bypasses, stateful bugs.
- **[Pact](https://docs.pact.io/)** 🟢🌱 — Consumer-driven contract
  testing — HTTP and message integrations. JavaScript, .NET, JVM, Python,
  Ruby, Go.
- **[Hypothesis](https://hypothesis.works/) /
  [fast-check](https://fast-check.dev/) /
  [PropEr](https://propertesting.com/)** 🟢🌱 — Property-based testing
  libraries; pair well with spec-derived invariants.
- **[Stainless](https://www.stainless.com/)** 🟢🏢 — Code generation
  from OpenAPI; the "code-from-spec" half.
- **[TLA+ model checker (TLC)](https://lamport.azurewebsites.net/tla/tla.html)** 🟢🌱 —
  Exhaustive checking for critical state machines.
- **[Reqnroll / SpecFlow](https://reqnroll.net/)** 🟢🌱 — .NET acceptance
  test runners for Gherkin specs.
- **BMAD QA persona (Quinn)** — workflow-encoded verification gate.

## 11. Helpers, linters, validators

Quality gates for the spec itself.

- ⭐ **[RequirementLinter](https://github.com/jonverrier/RequirementLinter)** 🟢🌱 —
  LLM-powered linter that checks user stories against the INCOSE "Guide
  to Writing Requirements" — vague terms, active voice, measurable
  performance criteria, structural completeness. IDE feedback in <10s.
- **[gherkin-lint](https://github.com/gherkin-lint/gherkin-lint)** 🟢🌱 /
  **[gherlint (Python)](https://github.com/DudeNr33/gherlint)** /
  **[@gherlint/gherlint (Node)](https://www.npmjs.com/package/@gherlint/gherlint)** —
  Style and structure linters for Gherkin feature files.
- **[Redocly CLI](https://github.com/Redocly/redocly-cli)** /
  **[IBM openapi-validator](https://github.com/IBM/openapi-validator)** /
  **[superfaceai/openapi-linter](https://github.com/superfaceai/openapi-linter)** 🟢🌱 —
  Lint OpenAPI documents against API style guides.
- **[Spectral](https://stoplight.io/open-source/spectral)** 🟢🌱 —
  Flexible JSON/YAML linter; ships rulesets for OpenAPI, AsyncAPI.
- **[PaceAI SRS Generator](https://paceai.co/tools/requirements-specification-generator/) /
  [Sommo SRS](https://www.sommo.io/software-requirements-specification) /
  [Taskade SRS](https://www.taskade.com/generate/ai-software-development/software-requirement-specification)** 🏢🔒 —
  AI generators for Software Requirements Specifications.

## 12. MCP servers and dashboards

- ⭐ **[spec-workflow-mcp (Pimzino)](https://github.com/Pimzino/spec-workflow-mcp)** 🟢🌱 —
  MCP server exposing the Requirements → Design → Tasks → Implementation
  workflow. Real-time web dashboard (port 5000), VS Code sidebar
  extension, approval workflow, task progress bars. Works with Claude
  Desktop, Cursor, Continue, Cline, and others.
- **[mcp-server-spec-driven-development](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Generic MCP server for SDD.
- **[Glama MCP catalogue](https://glama.ai/mcp/servers)** — index of MCP
  servers including several SDD-relevant ones.

## 13. Prompt and skill libraries

Reusable building blocks.

- **[Claude Code skills](https://github.com/anthropics/skills)** 🟢🏢 —
  Anthropic's official skills repository.
- **[awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)** 🟢🌱 —
  100+ specialised subagents.
- **[repowise-dev/claude-code-prompts](https://github.com/repowise-dev/claude-code-prompts)** 🟢🌱 —
  System prompts, tool prompts, agent delegation, memory management,
  multi-agent coordination patterns.
- **[shawnewallace/prompt-library](https://github.com/shawnewallace/prompt-library)** 🟢🌱 —
  Personal library of prompts and agent definitions.
- **[awesome-prompt-engineering](https://github.com/promptslab/Awesome-Prompt-Engineering)** 🟢🌱 —
  Broader prompt-engineering reference.
- **[Microsoft prompt-engine](https://github.com/microsoft/prompt-engine)** 🟡🏢 —
  Helps codify prompt patterns and practices.

## 14. Adjacent and supporting tools

- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** 🟢🌱 —
  Transport many spec frameworks expose themselves over.
- **[Specstory](https://specstory.com/)** 🟢🏢 — Captures and curates agent
  session history; raw material for after-the-fact specs.
- **[VibeDoc](https://github.com/Engineering4AI/awesome-spec-driven-development)** 🌱 —
  Documentation companion for spec-driven repos.

---

## 15. Courses and trainings 🎓

- **[DeepLearning.AI — Spec-Driven Development with Coding Agents](https://learn.deeplearning.ai/courses/spec-driven-development-with-coding-agents/information)** —
  Short course built with JetBrains; taught by Paul Everitt. Free.
- **[Microsoft Learn — Implement SDD using GitHub Spec Kit (enterprise)](https://learn.microsoft.com/en-us/training/modules/spec-driven-development-github-spec-kit-enterprise-developers/)**
- **[Microsoft Learn — Get Started with SDD and GitHub Spec Kit (greenfield intro)](https://learn.microsoft.com/en-us/training/modules/spec-driven-development-github-spec-kit-greenfield-intro/)**
- **[Udemy — SDD: From Vibe-Coding to AI Engineering](https://www.udemy.com/course/spec-driven-development-sdd-from-vibe-coding-to-reliable/)** —
  ~3h 45m, paid.
- **[Udemy — Master AI Spec-Driven Development with BMAD Method](https://www.udemy.com/course/master-ai-spec-driven-development-with-bmad-method/)** —
  Upstream-thinking / Downstream-building split.
- **[Class Central — Hello, Spec-Driven Development (AWS Events)](https://www.classcentral.com/course/youtube-hello-spec-driven-development-484502)** —
  Free.
- **[LinkedIn Learning — Spec-Driven Development with GitHub Spec Kit](https://github.com/LinkedInLearning/spec-driven-development-with-github-spec-kit-4641001)** —
  With course code repo.
- **[Anthropic — Introduction to Agent Skills](https://anthropic.skilljar.com/introduction-to-agent-skills)** —
  Free, official.
- **[DeepLearning.AI — Multi-AI-Agent Systems with crewAI](https://www.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai)** —
  Free, builds the role-based-personas mental model SpecMeta uses.

## 16. Books 📘

- **[AI Engineering — Chip Huyen, O'Reilly 2025](https://www.oreilly.com/library/view/ai-engineering/9781098166298/)** —
  Foundation-model app engineering; relevant chapters on evaluation,
  prompt engineering, agents. Companion repo:
  [chiphuyen/aie-book](https://github.com/chiphuyen/aie-book).
- **Working Backwards — Colin Bryar & Bill Carr, 2021** — Authoritative
  account of Amazon's PR/FAQ method. The cultural ancestor of intent-first
  SDD.
- **Specification by Example — Gojko Adzic, 2011** — How successful teams
  deliver the right software via collaborative spec workshops; the
  foundational ATDD text.
- **Bridging the Communication Gap — Gojko Adzic, 2009** — Original ATDD
  / "agile acceptance testing" book.
- **ATDD by Example — Markus Gärtner, 2012** — Practical guide to
  acceptance-test-driven development.
- **Object-Oriented Software Construction — Bertrand Meyer, 1997
  (2nd ed.)** — Design by Contract; pre + post conditions and class
  invariants. The intellectual ancestor of executable specs.
- **The PRFAQ Framework — Marcelo Calbucci, 2024** — Modern, opinionated
  guide to running the PR/FAQ at non-Amazon companies.

## 17. Articles and essays

- **[Andrej Karpathy on "vibe coding"](https://x.com/karpathy/status/1886192184808149383)** —
  The tweet that started the counter-movement. February 2025.
- **[Spec-Driven Development: From Vibe Coding to Structured Development — Zarar's Blog](https://zarar.dev/spec-driven-development-from-vibe-coding-to-structured-development/)**
- **[Spec-Driven Development: Stop Vibe Coding, Ship Real Code — Agentic Blog](https://blog.appxlab.io/2026/03/27/spec-driven-development-ai-coding/)**
- **[Karpathy's Vibe Coding Movement Considered Harmful — nmn.gl](https://nmn.gl/blog/dangers-vibe-coding)**
- **[Spec-driven development with AI: a new open-source toolkit — GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)** —
  GitHub's announcement of Spec Kit.
- **[Understanding Spec-Driven Development: Kiro, Spec Kit, Tessl — Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)** —
  Hands-on comparison.
- **[Diving Into SDD with GitHub Spec Kit — Microsoft for Developers](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)**
- **[Beyond Vibe Coding: A Guide to Spec Kit, BMAD, Kiro — Agentic SaaS Talks](https://agentic-saas-talks.com/blog/beyond-vibe-coding-a-guide-to-spec-kit-bmad-and-kiro)**
- **[I Tested Three Spec-Driven AI Tools — Ran The Builder](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/)**
- **[9 Best AI Tools for SDD in 2026 — MarkTechPost](https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/)**
- **[6 Best SDD Tools for AI Coding — Augment Code](https://www.augmentcode.com/tools/best-spec-driven-development-tools)**
- **[Spec-Driven Development is Eating Software Engineering — Vishal Mysore, Medium](https://medium.com/@visrow/spec-driven-development-is-eating-software-engineering-a-map-of-30-agentic-coding-frameworks-6ac0b5e2b484)** —
  Map of 30+ frameworks.
- **[Spec-driven AI coding: Spec-kit, BMAD, Agent OS, Kiro — Tim Wang](https://medium.com/@tim_wang/spec-kit-bmad-and-agent-os-e8536f6bf8a4)**
- **[Equipping agents for the real world with Agent Skills — Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)**
- **[Building agents with the Claude Agent SDK — Anthropic](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)**
- **[Best Practices for Claude Code — Anthropic docs](https://code.claude.com/docs/en/best-practices)** —
  "Ask Claude questions you'd ask a senior engineer."
- **[Claude's Context Engineering Secrets — Bojie Li](https://01.me/en/2025/12/context-engineering-from-claude/)**
- **[Applied BMAD — Reclaiming Control in AI Development — Benny Cheung](https://bennycheung.github.io/bmad-reclaiming-control-in-ai-dev)**
- **[OpenSpec Deep Dive — redreamality.com](https://redreamality.com/garden/notes/openspec-guide/)**
- **[How Tessl's Products Pioneer SDD — Tessl Blog](https://tessl.io/blog/how-tessls-products-pioneer-spec-driven-development/)**
- **[Spec-Driven Development on AWS — Lefteris Karageorgiou](https://blog.thecloudengineers.com/p/spec-driven-development-on-aws)**
- **[What is vibe coding, exactly? — MIT Technology Review](https://www.technologyreview.com/2025/04/16/1115135/what-is-vibe-coding-exactly/)**
- **["Out of the Tar Pit" — Moseley & Marks, 2006](https://curtclifton.net/papers/MoseleyMarks06a.pdf)** —
  The classic argument for separating essential state and logic, which
  is what a good spec captures.

## 18. Academic papers 📄

- *Large Language Models for Requirements Engineering: A Systematic
  Literature Review* — 74 primary studies (2023–2024). Arxiv:
  [`2509.11446`](https://arxiv.org/html/2509.11446v1).
- *Using LLMs in Software Requirements Specifications: An Empirical
  Evaluation* — Arxiv: [`2404.17842`](https://arxiv.org/pdf/2404.17842).
- *LLM-Assisted Repository-Level Generation with Structured Spec-Driven
  Engineering* — Arxiv: [`2605.02455`](https://arxiv.org/html/2605.02455).
- *Leveraging LLMs for Formal Software Requirements: Challenges and
  Prospects* (VERIFAI project) — Arxiv:
  [`2507.14330`](https://www.arxiv.org/pdf/2507.14330v2).
- *Exploring the Use of LLMs for Requirements Specification in an IT
  Consulting Company* — Arxiv:
  [`2507.19113`](https://arxiv.org/html/2507.19113v1).
- *Aligning Requirements for LLM Code Generation* (Specine) — Arxiv:
  [`2509.01313`](https://arxiv.org/html/2509.01313).
- *Improving LLM Code Generation via Requirement-Aware …* — Arxiv:
  [`2605.00433`](https://arxiv.org/pdf/2605.00433).
- *Vibe Coding: Programming through Conversation with AI* — Arxiv:
  [`2506.23253`](https://arxiv.org/html/2506.23253v1).
- *From Online User Feedback to Requirements: Evaluating LLMs for …* —
  Arxiv: [`2510.23055`](https://arxiv.org/pdf/2510.23055).
- *Design by Contract* — Bertrand Meyer, IEEE Computer, 1992
  ([ACM DL](https://dl.acm.org/doi/10.1109/2.161279)). The foundational
  paper for executable specifications.

## 19. Talks and videos 🎤

- **[Hello, Spec-Driven Development — AWS Events](https://www.classcentral.com/course/youtube-hello-spec-driven-development-484502)** —
  Building an application from scratch with AI-guided specs.
- **[New course! Spec-Driven Development — DeepLearning.AI announcement](https://www.youtube.com/watch?v=bJ8F43j1Fqw)**
- **[How I Code With AI Agents (Spec-Driven Development)](https://www.youtube.com/watch?v=RhaF4LVAVng)** —
  Practitioner walkthrough.
- **[Cline Memory Bank setup walkthrough](https://www.youtube.com/watch?v=tOYJpzRYR7s)**
- **[QCon AI Boston 2026](https://boston.qcon.ai/)** /
  **[QCon AI NYC 2025](https://ai.qconferences.com/)** —
  AI-engineering tracks; multi-agent and SDD sessions.
- **[QCon London 2026](https://qconlondon.com/)** — AI Engineering and
  Building Teams tracks.

## 20. Podcasts 🎧

- **[Latent Space: The AI Engineer Podcast](https://www.latent.space/podcast)** —
  Recurring coverage of SDD, "ghost libraries", agent skills.
- **[Tessl podcast — Revolutionising SDD with Framework & Registry](https://tessl.io/podcast/revolutionising-spec-driven-development-with-tessl-s-framework-registry/)**
- **[Practical AI](https://changelog.com/practicalai)** — Episodes on
  agent design, evaluation, requirements.
- **[The AI Native Dev](https://tessl.io/podcast/)** — Tessl-produced
  series on agent enablement.

## 21. Industry reports and statistics 📊

- **[McKinsey — Unleash developer productivity with generative AI](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai)** —
  2026 update: surveyed 4,500+ developers across 150 enterprises; AI
  reduces routine-coding time by ~46 %; complex-task completion +25–30 %.
- **[SWE-bench Leaderboard](https://www.swebench.com/)** /
  **[SWE-bench Pro](https://www.codeant.ai/blogs/swe-bench-scores)** —
  Verified benchmark for AI coding agents on real GitHub issues; the
  Verified set is now known to contain training-data contamination,
  motivating Pro (multi-file, 1,865 tasks, 4.1 files avg).
- **[LiveCodeBench](https://benchlm.ai/coding)** — Contamination-resistant
  competitive-programming benchmark; fresh problems post-cutoff.
- **[BenchLM coding leaderboard](https://benchlm.ai/coding)** — Weighted
  composite of SWE-bench Pro + LiveCodeBench.
- **[Modall — AI in Software Development Trends 2026](https://modall.ca/blog/ai-in-software-development-trends-statistics)**
- **[Index.dev — Top 100 Developer Productivity Statistics with AI Tools 2026](https://www.index.dev/blog/developer-productivity-statistics-with-ai-tools)**
- **[Shiftmag — "93 % of developers use AI but productivity is only 10 %"](https://shiftmag.dev/this-cto-says-93-of-developers-use-ai-but-productivity-is-still-10-8013/)** —
  Counterpoint to optimistic numbers.
- **[Tech Insider — Best AI Coding Tools 2026 ranked](https://tech-insider.org/ai-coding-tools-2026-transforming-software-development/)**
- **[Trigi Digital — AI Coding Impact 2026: 90 % AI-generated code](https://trigidigital.com/blog/ai-coding-impact-2026/)** —
  Read with appropriate skepticism.

## 22. Historical lineage

SDD didn't appear from nothing. Useful prior art:

- **[Design by Contract (DbC) — Bertrand Meyer / Eiffel](https://en.wikipedia.org/wiki/Design_by_contract)** —
  Preconditions, postconditions, invariants as executable contracts;
  1986 onward.
- **[Behavior-Driven Development (BDD) — Dan North](https://cucumber.io/docs/bdd/)** —
  Given/When/Then; the cultural template for human-readable acceptance
  tests.
- **[Acceptance-Test-Driven Development (ATDD) — Gojko Adzic & Janet Gregory](https://janetgregory.ca/atdd-vs-bdd-vs-specification-by-example-vs/)**
- **[Working Backwards / PR-FAQ — Amazon](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/)** —
  Press-release-first product definition; mid-2000s.
- **[Specification by Example — Gojko Adzic](https://less.works/less/technical-excellence/specification-by-example)**
- **[Literate Programming — Donald Knuth](https://en.wikipedia.org/wiki/Literate_programming)** —
  Code and rationale woven together; 1984.

## 23. Other awesome lists

- [Engineering4AI/awesome-spec-driven-development](https://github.com/Engineering4AI/awesome-spec-driven-development)
- [Software-Engineering-Arena/awesome-spec-driven-development](https://github.com/Software-Engineering-Arena/awesome-spec-driven-development)
- [zhimin-z/Awesome-Spec-Driven-Development](https://github.com/zhimin-z/Awesome-Spec-Driven-Development)
- [aabs/awesome-specification-driven-development](https://github.com/aabs/awesome-specification-driven-development)
- [wearetechnative/awesome-openspec](https://github.com/wearetechnative/awesome-openspec)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [sanjeed5/awesome-cursor-rules-mdc](https://github.com/sanjeed5/awesome-cursor-rules-mdc)
- [promptslab/Awesome-Prompt-Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering)
- [caramaschiHG/awesome-ai-agents-2026](https://github.com/caramaschiHG/awesome-ai-agents-2026)
- GitHub topics:
  [`spec-driven`](https://github.com/topics/spec-driven),
  [`spec-driven-development`](https://github.com/topics/spec-driven-development)

## 24. Communities

- **[r/ChatGPTCoding](https://www.reddit.com/r/ChatGPTCoding/)** — large
  active community on AI coding workflows, including SDD discussions.
- **[BMAD Discord](https://docs.bmad-method.org/)** — linked from the
  BMad Method docs.
- **OpenSpec / Spec Kit issue trackers** — primary venue for framework
  questions.
- **[Cursor Forum](https://forum.cursor.com/)** — practitioner threads on
  rules, planning, SDD recipes.

---

## Contributing

PRs welcome. Each entry needs: name, link, status emojis, one sentence on
*what makes it spec-driven*, and — if proposing a new category — a one-line
definition. See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Promotional language,
sponsored placements, and entries that are only "AI assisted" without an
SDD angle will be rejected.

## Sources

This refresh was built from May 2026 web research; full per-section sources
in commit history. Key primary sites:

- Framework repos: github/spec-kit, bmad-code-org/BMAD-METHOD,
  Fission-AI/OpenSpec, buildermethods/agent-os, eyaltoledano/claude-task-master,
  Pimzino/claude-code-spec-workflow + spec-workflow-mcp, gotalab/cc-sdd,
  modu-ai/moai-adk, colign/colign, codervisor/lean-spec,
  tesslio/spec-driven-development-tile, RooCodeInc/Roo-Code,
  Aider-AI/aider, schemathesis/schemathesis, jonverrier/RequirementLinter,
  crewaiinc/crewai, microsoft/autogen, anthropics/skills.
- Docs sites: kiro.dev/docs, docs.cline.bot, docs.roocode.com,
  docs.tessl.io, aider.chat/docs, agents.md, chatprd.ai, lean-spec.dev,
  cucumber.io, reqnroll.net, modelcontextprotocol.io, schemathesis.io,
  pact.io.
- Surveys & comparisons: MarkTechPost, Augment Code, Medium (Vishal
  Mysore, Tim Wang), Martin Fowler, Microsoft for Developers, Class
  Central, DeepLearning.AI, Anthropic engineering blog.
- Academic: arXiv 2509.11446, 2404.17842, 2605.02455, 2507.14330,
  2507.19113, 2509.01313, 2605.00433, 2506.23253, 2510.23055.
- Existing awesome lists (linked above).

## Project artefacts

This list is one of three artefacts in SpecBench. The others:

- **[`BENCHMARK.md`](./BENCHMARK.md)** — Methodology, 8-dimension rubric,
  five reproducible tasks (CRUD-from-PRD, add-feature, refactor, handover,
  model-swap), per-framework scorecards, aggregated
  [results](./benchmark/results.md).
- **[`meta-framework/`](./meta-framework/) — SpecMeta** — A decomposition
  of SDD into 7 reusable slots (context, intent, spec, plan, tasks,
  implementation, verification) with a **panel of AI personas**
  (Consultant, Senior Engineer, Architect, Critic, Product Manager, QA
  Lead, Security/Compliance, Coach) that compose a `specmeta.yaml` for
  your specific project profile. See
  [`meta-framework/personas/`](./meta-framework/personas/) and the
  [AI decision workflow](./meta-framework/ai-decision-workflow.md).

License: content [CC-BY-4.0](./LICENSE); code samples MIT.
