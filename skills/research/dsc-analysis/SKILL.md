---
name: dsc-analysis
description: Analyze DSC data with explicit cycle selection, baseline and smoothing assumptions, transition tables, cautious thermal interpretation, and manuscript-ready wording. Use automatically for DSC curves, Tg, Tc, Tm, crystallization, broad endotherms, softening, or partial-melting discussion.
---

# DSC Analysis

## Required rules

Read docs/rules/dsc_analysis_rules.md and docs/rules/data_management_rules.md. Read current research context only when project background is needed.

## Process

### 1. Identify input

Confirm sample name, heating and cooling cycle, rates, atmosphere, sample mass, temperature range, heat-flow direction, and raw data file.

### 2. Define preprocessing

State baseline range, smoothing, normalization, and whether first heating, cooling, and second heating are analyzed separately.

### 3. Analyze

Generate cleaned data if needed, a plot, a transition table, and a cautious interpretation.

### 4. Interpret cautiously

Do not claim a sharp melting point unless the signal supports it. Prefer broad endothermic behavior, high-softening range, partial-melting range, or weak melting-related signal when appropriate.

### 5. Save outputs

Save the script, figure, processed data when generated, and a short report when useful.

## Completion criterion

This skill is complete when:

1. input file and cycle are identified
2. baseline and smoothing assumptions are stated
3. figure and table are generated when data are available
4. thermal interpretation is cautious
5. manuscript wording is safe when requested
6. the response includes a Skill usage receipt
