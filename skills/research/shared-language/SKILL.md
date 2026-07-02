---
name: shared-language
description: Build or refine shared research terminology, glossary entries, and durable project language.
disable-model-invocation: true
---

# Shared Language

## Purpose

Maintain concise, stable terminology between the user and Codex.

Use this when:

- a term is ambiguous
- a term is repeatedly used
- two terms are being confused
- a project needs a controlled vocabulary
- a manuscript or slide deck needs consistent language

## Required files

Read:

- `docs/shared_language/CONTEXT.md`

Read relevant rule files only if needed.

## Process

### 1. Detect candidate terms

Look for:

- repeated phrases
- overloaded terms
- terms with multiple possible meanings
- terms that affect interpretation
- terms that should become canonical

### 2. Challenge ambiguous language

If a term is unclear, ask:

```text
You used X. Do you mean A or B? These have different implications.
```

### 3. Propose canonical wording

For each important term, propose:

- canonical term
- short definition
- avoid terms
- usage note if needed

### 4. Update CONTEXT.md

Update `docs/shared_language/CONTEXT.md` only when the term is durable.

Do not add temporary scratch notes.

### 5. Consider ADR

Offer an ADR only when the decision is:

1. hard to reverse
2. surprising without context
3. based on a real trade-off

## Completion criterion

This skill is complete when:

1. ambiguous terms are resolved or marked unresolved
2. canonical terms are proposed
3. durable terms are added to `CONTEXT.md`
4. any necessary ADR is suggested or created