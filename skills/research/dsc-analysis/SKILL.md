---
name: dsc-analysis
description: Analyze DSC data with explicit cycle selection, preprocessing assumptions, transition tables, cautious thermal interpretation, and manuscript-ready wording. Use for DSC curves, Tg, Tc, Tm, crystallization, broad endotherms, softening, or partial-melting discussion.
---

# DSC Analysis

## Procedure

1. Read `docs/rules/dsc_analysis_rules.md`,
   `docs/rules/data_management_rules.md`, and an applicable project brief only
   when material-specific context is required.
2. Confirm sample identity, cycle, rates, atmosphere, mass, range, heat-flow
   direction, and raw file.
3. State baseline, smoothing, normalization, trimming, and peak-selection
   assumptions.
4. Analyze cycles separately and generate cleaned data, a curve, a transition
   table, and cautious interpretation when data permit.
5. Distinguish observed curve features from assignments such as glass
   transition, crystallization, softening, or melting.
6. Save rerunnable analysis and directly usable manuscript wording when requested.

## Stop conditions

Stop when sample or cycle identity is unknown, heat-flow direction is ambiguous,
preprocessing materially changes the interpretation without justification, the
signal does not support a requested transition, or raw data are unavailable.

## Completion criterion

This skill is complete when:

1. input, sample, and cycle are identified
2. preprocessing assumptions are explicit
3. figures and transition tables are generated when data permit
4. observation and interpretation remain separate
5. thermal wording matches the signal strength
