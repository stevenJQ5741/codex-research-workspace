---
name: manuscript-pipeline
description: Orchestrate an evidence-led research manuscript from source inventory through reproducible analysis, drafting, cross-artifact review, and release handoff. Use for full-paper production or multi-file revision that combines data, models, figures, tables, and manuscript artifacts; do not use for reviewing an already bounded draft.
---

# Manuscript Pipeline

## Procedure

1. Read `docs/rules/manuscript_writing_rules.md`,
   `docs/rules/data_management_rules.md`, and only the applicable project brief or
   scientific rule.
2. Define the target artifact, audience, language, required sections, protected
   content, source files, and missing inputs.
3. Inventory raw observations, processed results, calculations, literature,
   assumptions, and visual sources with units and provenance.
4. Freeze canonical symbols, units, sign conventions, and evidence labels.
5. Use `analysis-feedback-loop` for material calculations or generated figures;
   preserve scripts, machine-readable results, and audit outputs.
6. Use `claim-evidence-audit` for central novelty, mechanism, or conclusion
   claims before final prose.
7. Draft in dependency order: methods and verified results, discussion,
   introduction, conclusion, then abstract. Keep unresolved work visible.
8. Cross-check repeated values, terminology, captions, tables, figures, and
   conclusions. Use `manuscript-review` for the complete draft and `artifact-qa`
   for generic rendered QA.
9. Record authoritative outputs, validation performed, unresolved risks, and the
   next action. Use `handoff` when another session will continue.

## Stop conditions

Stop before drafting or release when a central source is missing, raw and derived
values cannot be distinguished, a baseline calculation cannot be reproduced,
project terminology is unresolved, a central claim lacks support, or the
authoritative manuscript version is ambiguous.

## Completion criterion

This skill is complete when:

1. sources, assumptions, symbols, units, and protected content are explicit
2. material calculations and figures are reproducible
3. central claims are traceable and wording is calibrated
4. manuscript and supporting artifacts agree
5. placeholders and unresolved validation remain visible
6. the authoritative manuscript passes the selected scientific and artifact checks
