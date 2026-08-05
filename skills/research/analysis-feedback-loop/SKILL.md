---
name: analysis-feedback-loop
description: Run reproducible experimental or model analysis with provenance, formula audits, unit checks, staged outputs, scientific sanity checks, and manuscript-ready handoff. Use for calculations, workbooks, plots, tables, fitting, or updates that must remain traceable to raw sources.
---

# Analysis Feedback Loop

## Procedure

1. Read `docs/rules/data_management_rules.md` and only the applicable scientific
   rule or project brief.
2. Record input path, role, sample identity, units, sheet or range, missing
   values, expected output, and protected raw files.
3. Classify preprocessing, constants, formulas, normalization, sign conventions,
   fits, and substitutions by evidence source.
4. Reproduce a recorded baseline value or calculation before extending the
   analysis.
5. Implement rerunnable code with deterministic outputs and preserved
   intermediate audit values.
6. Check dimensions, conversions, signs, mappings, repeated constants, solver
   targets, fit degrees of freedom, ranges, trends, and sensitivity.
7. Generate figures and tables from verified machine-readable results and
   cross-check their labels and reported values.
8. Report inputs, assumptions, baseline, deltas, outputs, limitations, and the
   next validation step.

## Stop conditions

Stop when raw inputs would be overwritten, source identity is ambiguous, a
baseline mismatch is unresolved, dimensions or signs fail, required calibration
is missing, or the available sample size cannot support the intended inference.

## Completion criterion

This skill is complete when:

1. raw inputs are unchanged and provenance is recorded
2. assumptions and evidence classes are explicit
3. the baseline is reproduced or its mismatch is resolved
4. formulas, units, signs, and mappings pass audit
5. results and communication artifacts are reproducible
6. limitations and supported inference strength are stated
