# T2 — Add a feature to an existing repo

**Stresses:** drift resistance · traceability · onboarding cost
**Estimated wall-clock:** 30–60 min.

## Prompt to the framework

The seed repo is the *output* of T1 (bookmarks service) committed at a
pinned SHA. Without reading the original chat transcript, add the
following feature using the framework's canonical workflow:

> **Shareable read-only links.** A bookmark owner can mint a token that
> grants public read access to a single bookmark for a configurable TTL
> (1h–30d). The token must be revocable. Public reads must not count
> against the owner's listing endpoints.

## Drift probe

After the framework reports completion, apply this patch in a single
commit *outside* the framework (simulating a teammate's manual edit):

```diff
-tags: 0-10 short strings
+tags: 0-20 short strings
```

…in the spec, plus a matching code change. Then ask the framework, in a
new session, to add a "bulk tag rename" feature. Score whether the
framework:

- Notices the spec / code change made outside its workflow.
- Refuses to proceed silently with stale assumptions.
- Updates traceability links.

## What to record

- Whether the new feature got its own spec section or was bolted onto code.
- Whether the existing spec was modified or left to drift.
- Drift-probe result.
