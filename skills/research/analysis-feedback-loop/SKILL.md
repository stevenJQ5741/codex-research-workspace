---
name: analysis-feedback-loop
description: Run reproducible experimental or model analysis with provenance, formula audits, unit checks, staged outputs, scientific sanity checks, and manuscript-ready handoff. Use automatically for calculations, workbooks, plots, tables, fitting, or updates that must remain traceable to raw sources.
---

# Analysis Feedback Loop

## Required rules

Read docs/rules/data_management_rules.md and one relevant scientific rule when needed.

## Process

### 1. Inventory inputs

Record source path, file role, sample identity, units, sheet or range, missing values, and expected output. Do not modify raw inputs.

### 2. Register assumptions

Label preprocessing, constants, formulas, normalization, sign conventions, fitting choices, and substitutions as measured, calculated, literature-derived, or assumed.

### 3. Establish a baseline

Reproduce an existing known value, workbook row, or reference calculation before extending the analysis. Treat baseline mismatch as a stop condition requiring diagnosis.

### 4. Implement the calculation

Create rerunnable code with relative paths and deterministic outputs. Save machine-readable results and a source manifest where practical.

### 5. Audit formulas and units

Check dimensions, conversions, signs, row and column mappings, repeated constants, and solver targets. Preserve intermediate values needed to diagnose disagreement.

### 6. Validate scientifically

Check physical ranges, trends, sensitivity, sample count, fit degrees of freedom, and whether the result supports correlation, interpretation, or causation.

### 7. Generate communication artifacts

Create figures and tables from verified results. Cross-check labels, legends, captions, and manuscript values against machine-readable output.

### 8. Report deltas

Report inputs, assumptions, baseline result, changes from the prior version, generated files, limitations, and next validation step.

## Completion criterion

This skill is complete when:

1. raw inputs are unchanged and provenance is recorded
2. assumptions and evidence classes are explicit
3. a baseline is reproduced or the mismatch is resolved
4. formulas, units, and signs pass audit
5. results and communication artifacts are reproducible
6. scientific limitations and fit strength are stated
7. the response includes a Skill usage receipt
