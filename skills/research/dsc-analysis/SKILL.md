---
name: dsc-analysis
description: DSC analysis workflow for baseline correction, thermal-transition interpretation, and cautious manuscript wording.
disable-model-invocation: true
---

# DSC Analysis

## Purpose

Analyze DSC data and interpret thermal transitions cautiously.

## Required rules

Read:

- `docs/rules/dsc_analysis_rules.md`
- `docs/rules/data_management_rules.md`

Read `docs/rules/current_research_context.md` only if project background is needed.

## Process

### 1. Identify input

Confirm:

- sample name
- heating/cooling cycle
- heating rate
- cooling rate
- atmosphere
- sample mass
- temperature range
- heat-flow direction
- raw data file

### 2. Preprocessing plan

State:

- baseline range
- smoothing method if used
- normalization method if used
- whether first heating, cooling, and second heating are analyzed separately

### 3. Analyze

Generate:

- cleaned data if needed
- plot
- transition table
- cautious interpretation

### 4. Interpretation rules

Do not claim a sharp melting point unless clear.

Use cautious language such as:

- broad endothermic behavior
- high-softening temperature range
- partial-melting temperature range
- weak melting-related signal

### 5. Output

Save:

- script
- figure
- processed data if generated
- short report if useful

## Completion criterion

This skill is complete when:

1. input file and cycle are identified
2. baseline and smoothing assumptions are stated
3. figure and table are generated if data are available
4. thermal interpretation is cautious
5. manuscript wording is safe if requested