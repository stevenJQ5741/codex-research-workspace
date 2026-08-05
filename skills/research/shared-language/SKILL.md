---
name: shared-language
description: Control durable research terminology, symbols, units, sign conventions, and evidence labels across calculations, figures, manuscripts, and sessions. Use when terms are overloaded, translations drift, symbols conflict, or definitions differ across artifacts.
---

# Shared Language

## Procedure

1. Identify only ambiguity that changes calculation, interpretation, validation,
   or wording.
2. Resolve meaning from equations, sources, scripts, figures, and current usage
   before asking the user.
3. Define canonical term, definition, symbol, unit, sign convention, evidence
   class, preferred translation, avoid terms, and caveats as applicable.
4. Identify and check affected scripts, tables, figures, captions, manuscripts,
   and release specifications.
5. Update `docs/shared_language/CONTEXT.md` only for recurring language; use an
   ADR for a hard-to-reverse convention.

## Stop conditions

Stop propagation when sources contradict each other, a scientific meaning cannot
be resolved, or changing the term would silently change a formula, dataset, or
claim. Mark the entry unresolved instead.

## Completion criterion

This skill is complete when:

1. consequential ambiguity is resolved or explicitly unresolved
2. canonical wording, symbols, units, and signs are explicit
3. affected artifacts are identified and checked
4. durable entries are recorded without duplicating project background
