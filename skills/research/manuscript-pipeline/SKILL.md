---
name: manuscript-pipeline
description: Run an evidence-led research manuscript from source inventory through reproducible calculations, figures, drafting, cross-checks, and rendered release review. Use automatically for full-paper production, multi-file revision, or writing that combines data, model outputs, figures, tables, DOCX, or PDF artifacts.
---

# Manuscript Pipeline

## Required rules

Read docs/rules/manuscript_writing_rules.md and docs/rules/data_management_rules.md. Read one project-specific scientific rule only when the paper requires it.

For lessons generalized from the PLA/CF paper, read references/pla-cf-paper-lessons.md.

## Workflow

### 1. Define the release target

Record the target artifact, audience, language, reference format, required sections, source files, and items that must remain unchanged. Mark missing inputs before drafting.

### 2. Build an evidence inventory

Classify every input as raw measurement, processed result, calculated result, literature source, model assumption, or visual reference. Preserve raw files and record units and provenance.

### 3. Freeze symbols and units

Resolve overloaded terms, canonical symbols, sign conventions, and unit conversions before generating prose or figures. Use shared-language when ambiguity is durable.

### 4. Generate reproducible results

Use analysis-feedback-loop for calculations and figure data. Save scripts, intermediate audit outputs, and source manifests. Do not manually transcribe derived values when a script can generate them.

### 5. Build the claim-evidence ledger

Use claim-evidence-audit. Every central claim must identify its evidence type, source, strength, limitation, and permitted wording. Treat correlation, decomposition, and causal validation as different levels.

### 6. Draft in dependency order

Draft methods and results from verified artifacts first, then discussion, introduction, conclusion, and abstract. Keep simulation plans and missing validation explicitly labeled as placeholders.

### 7. Cross-check artifacts

Confirm that repeated values, symbols, captions, table entries, and conclusions agree across scripts, manifests, figures, tables, manuscript text, and supplementary files.

### 8. Run release gates

Use manuscript-review for evidence and writing review. Use artifact-qa for DOCX/PDF rendering, page layout, figure legibility, numbering, and placeholder detection.

### 9. Close the session

List generated artifacts, unresolved scientific risks, intentionally deferred work, and the exact next action. Use handoff when another session will continue the paper.

## Completion criterion

This skill is complete when:

1. source, assumption, symbol, and unit inventories are explicit
2. calculations and figures are reproducible from recorded inputs
3. central claims are traceable to evidence with calibrated wording
4. cross-artifact values and terminology agree
5. placeholders and unresolved validation are visible
6. the final document passes scientific and rendered visual review
7. the response includes a Skill usage receipt
