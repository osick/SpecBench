# T4 — Cross-team handover

**Stresses:** reviewability · onboarding cost · spec quality
**Estimated wall-clock:** 20 min (review) + 60 min (re-entry).

## Procedure

1. Take the T1+T2 output as-is.
2. A second contributor — who has *not* seen the original session —
   reviews only the artefacts the framework produced (no transcript,
   no chat history). Time how long until they can answer:
   - What does this service do?
   - What was the last feature added and why?
   - What's the next reasonable thing to build?
3. The second contributor then asks the framework (fresh session,
   fresh agent context) to implement:

   > **Soft-delete with a 7-day undo window.**

   Time to first useful commit.

## What to record

- Reviewer's notes — were they ever confused by the spec? Where?
- Whether artefacts opened cleanly in a non-vendor editor.
- Whether the framework re-loaded enough context from artefacts alone
  to avoid asking the user to re-explain the project.
