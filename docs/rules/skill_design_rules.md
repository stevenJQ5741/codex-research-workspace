# Skill Design Rules

## Purpose

These rules define how to write and maintain research skills for this repository.

A skill should make Codex follow a predictable process, not produce identical output every time.

## Core principles

1. Prefer predictable process over long instruction blocks.
2. Use skills for workflows, not for storing all background knowledge.
3. Keep root `AGENTS.md` short.
4. Put detailed reusable rules in `docs/rules/`.
5. Put project terminology in `docs/shared_language/`.
6. Put hard-to-reverse decisions in `docs/adr/`.
7. Prefer user-invoked skills unless automatic invocation is clearly worth the context cost.
8. Each skill must have a clear completion criterion.
9. Do not duplicate the same rule in many files.
10. Use the smallest context needed for the task.

## User-invoked skills

User-invoked skills are called manually by the user.

Use them when:

- human judgement is required
- the skill is not needed every session
- the skill would create unnecessary context load if always visible
- the workflow is specialized

For user-invoked skills, include this in frontmatter:

```yaml
disable-model-invocation: true
```

## Model-invoked skills

Model-invoked skills may be triggered automatically by the agent.

Use them only when:

- the agent must reach the skill without the user remembering it
- the trigger is frequent and clear
- the description is short
- the permanent context cost is justified

In this repository, most skills should remain user-invoked.

## Router skill

When user-invoked skills become too many to remember, create one router skill.

The router does not execute the task.
It recommends which skill to invoke and which rule files to read.

For this repository, the router is:

```text
skills/router/ask-jiang/SKILL.md
```

## Information hierarchy

Use this hierarchy:

1. Skill steps: what Codex must do now.
2. In-skill reference: short rules needed every time the skill runs.
3. External reference: detailed rules loaded only when needed.

Do not put large research background directly in `SKILL.md`.

## Completion criterion

Every skill must define how Codex knows the workflow is complete.

Good completion criteria are:

- observable
- checkable
- task-specific
- resistant to premature completion

## Feedback loop

Every major workflow should include:

1. input check
2. assumption check
3. first output
4. self-review
5. correction
6. final output
7. memory update if durable

## Shared language

When a term becomes important, record it in:

```text
docs/shared_language/CONTEXT.md
```

When a decision is hard to reverse, surprising, or trade-off based, record it in:

```text
docs/adr/
```

## Pruning

Remove or avoid:

- duplicated rules
- stale background
- generic advice
- no-op instructions
- long explanations that do not change Codex behavior