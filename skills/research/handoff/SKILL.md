---
name: handoff
description: Compact cross-session or cross-computer handoff for continuing research work with another Codex session.
disable-model-invocation: true
---

# Handoff

## Purpose

Create a compact handoff document so another Codex session or another computer can continue the work.

## Process

### 1. Identify continuation target

Ask or infer:

- what the next session will continue
- which files matter
- what should not be repeated
- what risks remain

### 2. Avoid duplication

Do not repeat content already captured in:

- `PLANS.md`
- `notes/decision_logs/decision_log.md`
- `docs/shared_language/CONTEXT.md`
- project briefs
- existing reports
- commits

Reference paths instead.

### 3. Redact sensitive information

Do not include:

- API keys
- passwords
- visa details
- residence card details
- passport information
- private identifiers

### 4. Write handoff

Save under:

```text
notes/session_summaries/
```

Use filename:

```text
YYYY-MM-DD-handoff-[short-topic].md
```

## Handoff format

```markdown
# Handoff - [Topic]

## Purpose of next session

## Current state

## Important files

## Confirmed decisions

## Unresolved issues

## Suggested skills

## First next action

## Sensitive information excluded
```

## Completion criterion

This skill is complete when:

1. a compact handoff file is written
2. it references existing files instead of duplicating them
3. sensitive information is excluded
4. next session has a clear first action