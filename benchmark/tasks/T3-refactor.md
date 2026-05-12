# T3 — Refactor with behaviour preservation

**Stresses:** verification loop · drift resistance
**Estimated wall-clock:** 30–45 min.

## Prompt to the framework

The seed repo is T1's output. Refactor the persistence layer from SQLite
to an in-memory repository behind an interface, without changing any
observable HTTP behaviour. Use the framework's canonical workflow.

## Acceptance script

The same black-box HTTP tests from T1 must still pass, unmodified, against
the refactored code. If the framework regenerated the tests, the *new*
tests must be a strict superset of T1's acceptance cases.

## What to record

- Did the framework produce a refactor *spec* (or only a code diff)?
- Did it verify behaviour preservation before declaring done?
- Were any spec lines changed that shouldn't have been (silent semantic drift)?
