# SpecMeta decision tree

Answer the questions in order. Each answer constrains the next.

## 1. Is the project greenfield or an existing codebase?

- **Greenfield** → continue to Q2.
- **Existing** → prioritise slots that work with whatever already exists.
  Default: `AGENTS.md` for context, `openspec` for spec (it grafts onto
  any repo), keep your current test infra for verification. Go to Q3.

## 2. Is the spec going to be reviewed by non-engineers?

- **Yes** (PM, designer, compliance) → `spec-kit` or `kiro-ears`.
  Choose `kiro-ears` only if you can accept the IDE.
- **No, engineers only** → `openspec` if you want minimum ceremony, or
  `spec-kit` if you want phased commands.

## 3. Is portability across models/agents a hard requirement?

- **Yes** (e.g. you anticipate model swaps, multi-vendor org, OSS project)
  → exclude `kiro`, `tessl`, vendor-IDE-only tooling. Default
  composition: `AGENTS.md + spec-kit + claude-code-or-cursor + schemathesis`.
- **No** → vendor-integrated tools are on the table; pick what your IDE
  supports best.

## 4. How important is drift resistance after the first release?

- **Critical** (long-lived service, regulated, multi-team) → `tessl`
  (if you can accept the platform), `kiro` (if you can accept the IDE),
  or *strictly enforce* a "no PR without spec edit" rule with `openspec`.
- **Nice-to-have** → any framework + a quarterly spec review.

## 5. Do you need formal verification anywhere?

- **Yes, for one critical subsystem** → add `tla-plus` to the spec slot
  for that subsystem only. The rest of the project stays informal.
- **No** → property tests + schemathesis cover most needs.

## 6. Team size and review culture?

- **Solo or pair** → BMAD's role play feels silly; `openspec` or
  `spec-kit` are right-sized.
- **5–20 with strong PR review** → `spec-kit` + `openspec` change-proposal
  pattern.
- **20+ with PM / Architect / QA roles** → BMAD-METHOD models your org;
  the ceremony pays off.

## 7. Where does the team live?

- **Terminal-first** → `claude-code` or `aider` for implementation.
- **IDE-first (VS Code, JetBrains)** → `cursor`, `continue`, `cline`.
- **GitHub-centric** → `copilot-coding-agent` and mirror tasks to Issues.

---

After Q1–Q7 you should have one tool per slot. Write it into
`specmeta.yaml` and commit it. If two reasonable answers compete, pick the
one with the **lower onboarding cost** — you can upgrade slots later
without rewriting the spec.
