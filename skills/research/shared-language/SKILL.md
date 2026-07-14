---
name: shared-language
description: Control durable research terminology, symbols, units, sign conventions, and evidence labels across calculations, figures, manuscripts, and sessions. Use automatically when terms are overloaded, translations drift, symbols conflict, or concepts differ across artifacts.
---

# Shared Language

## Process

### 1. Detect consequential drift

Find terms or symbols whose ambiguity changes calculation, interpretation, or wording. Ignore harmless temporary phrasing.

### 2. Resolve from evidence

Check equations, source documents, scripts, figure labels, and manuscript usage. Ask only when evidence cannot resolve the meaning.

### 3. Define the canonical entry

Record canonical term, definition, symbol, unit, sign convention, evidence class, preferred English or Japanese wording, avoid terms, and unresolved caveats as applicable.

### 4. Propagate the decision

Identify affected scripts, tables, figures, captions, and manuscript passages. Do not update the glossary while leaving contradictory active artifacts unnoticed.

### 5. Persist durable language

Update docs/shared_language/CONTEXT.md only for recurring language. Use an ADR when changing a hard-to-reverse convention.

## Completion criterion

This skill is complete when:

1. consequential ambiguity is resolved or marked unresolved
2. canonical wording, symbols, units, and signs are explicit
3. affected artifacts are identified and checked
4. durable entries are recorded without duplicating background
5. the response includes a Skill usage receipt
