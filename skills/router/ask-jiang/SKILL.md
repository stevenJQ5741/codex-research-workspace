---
name: ask-jiang
description: Route Quan Jiang's task to the smallest effective combination of installed research Skills and rule files. Use when a task spans workflows, the primary deliverable is unclear, or Skill invocation may expand cost or scope; do not use to resolve domain assumptions after a workflow is selected.
---

# Ask Jiang Router

## Procedure

1. Classify the primary deliverable: research decision, analysis, manuscript,
   artifact QA, presentation, Office release, email, repository change, or
   handoff.
2. Identify available sources, scientific stakes, mutation risk, external
   effects, missing inputs, and whether read-only work is sufficient.
3. Select one primary and no more than two supporting Skills from the
   responsibility matrix in `README.md`. Load only their required rules.
4. Proceed when the match is clear and the request already authorizes the work.
   Ask once when workflows compete, a method changes the result, cost is
   substantial, or scope would expand.
5. Keep destructive actions, external messages, sensitive data, commits, pushes,
   and remote changes separately authorized.
6. Record only the Skills that materially affected the task.

## Stop conditions

Stop routing when the repository or deliverable is still ambiguous, more than one
primary Skill remains necessary, or the proposed workflow exceeds authorization.
Use `research-grill` only after routing when scientific assumptions remain
consequential.

## Completion criterion

This skill is complete when:

1. deliverable, evidence, and risk are classified
2. one primary and at most two supporting Skills are selected
3. only relevant rules are loaded
4. execution or confirmation matches the invocation gate
5. separate authorization boundaries remain explicit
