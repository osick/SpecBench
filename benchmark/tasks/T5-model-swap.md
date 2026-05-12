# T5 — Model swap mid-project

**Stresses:** portability
**Estimated wall-clock:** 30 min.

## Procedure

1. Run T1 with Model A (e.g. Claude).
2. Switch to Model B (e.g. GPT or Gemini) **using the same framework and
   the same artefacts**, no re-prompting beyond what the framework
   itself requires.
3. Ask Model B to implement T2's "shareable links" feature.

## What to record

- Did the framework even *let* you swap models? (Vendor-locked tools
  fail here by definition — record N/A and score 0 on portability.)
- Did Model B produce a recognisably consistent style with Model A's
  output, or did it diverge?
- Any prompts or scaffolding the framework had to rewrite for Model B.

## Why this matters

Spec-driven development's killer feature, in principle, is that the spec
is the durable artefact and the model is fungible. Frameworks that
*claim* portability but secretly rely on one model's quirks will be
exposed by this task.
