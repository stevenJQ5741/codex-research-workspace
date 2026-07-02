---
name: research-grill
description: Relentless research interview for clarifying experiments, manuscript arguments, presentations, proposals, or analysis plans before execution.
disable-model-invocation: true
---

# Research Grill

## Purpose

Clarify a research plan before Codex writes, analyzes, or modifies files.

Use this when the task is ambiguous, high-stakes, or likely to suffer from hidden assumptions.

## Process

### 1. Establish the task boundary

Identify:

- target output
- audience
- language
- deadline if relevant
- source files or data
- what must not be changed

### 2. Identify hidden assumptions

Check for assumptions about:

- sample identity
- fiber type
- matrix type
- experimental condition
- temperature range
- baseline correction
- model parameters
- sensor position
- figure meaning
- manuscript conclusion

### 3. Ask one question at a time

Ask only one question per turn.

For each question:

1. state why it matters
2. provide a recommended answer if possible
3. wait for the user response

Do not ask a batch of questions.

### 4. Explore files instead of asking when possible

If the answer can be obtained by reading available files, inspect the files instead of asking the user.

### 5. Produce a clarified task brief

When enough information is resolved, create a concise task brief:

```markdown
## Clarified task brief

### Goal

### Inputs

### Constraints

### Assumptions

### Confirmed decisions

### Unresolved risks

### Next action
```

## Completion criterion

This skill is complete when:

1. the task goal is clear
2. required inputs are identified
3. critical assumptions are listed
4. unresolved risks are explicit
5. the next action is safe and specific