---
name: skill-name
description: State what the Skill does, concrete triggers, and the nearest boundary or exclusion.
---

# Skill Title

## Procedure

1. Load only the required reusable rules or project brief.
2. Define the authorized inputs, outputs, protected content, and evidence state.
3. Perform the smallest reproducible workflow that satisfies the request.
4. Validate affected outputs and record unresolved risks.

## Stop conditions

Stop when required evidence is missing, the authoritative source is ambiguous,
validation fails, or the next action exceeds authorization.

## Completion criterion

This skill is complete when:

1. inputs, scope, and evidence state are explicit
2. the requested output is produced reproducibly
3. affected validation passes
4. unresolved risks and next action are visible

Maintain matching `agents/openai.yaml` metadata with
`policy.allow_implicit_invocation: true`.
