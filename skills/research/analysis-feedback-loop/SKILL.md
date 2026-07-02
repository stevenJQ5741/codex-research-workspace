---
name: analysis-feedback-loop
description: Reproducible experimental data analysis workflow with input checks, assumption checks, script execution, output validation, and compact reporting.
disable-model-invocation: true
---

# Analysis Feedback Loop

## Purpose

Analyze experimental data without overwriting raw files and with a reproducible feedback loop.

Use this for:

- CSV data
- DSC data
- temperature data
- mechanical testing data
- figure generation
- table generation

## Required rules

Read:

- `docs/rules/data_management_rules.md`

Read additional scientific rules only when needed.

## Process

### 1. Input check

Identify:

- raw input files
- file format
- units
- sample names
- missing values
- expected columns
- output target

Do not modify raw files.

### 2. Assumption check

State assumptions before analysis:

- preprocessing
- baseline correction
- smoothing
- filtering
- fitting
- normalization
- model parameters

### 3. Reproducible script

Create or update a script under:

```text
scripts/data_analysis/
```

or:

```text
scripts/figure_generation/
```

Use relative paths.

### 4. Output generation

Save outputs to:

```text
outputs/figures/
outputs/tables/
outputs/reports/
data/processed/
```

as appropriate.

### 5. Validation

Check:

- whether outputs were created
- whether values are physically reasonable
- whether plots match the intended interpretation
- whether any conclusion is overclaimed

### 6. Compact report

Report:

1. input files
2. preprocessing
3. assumptions
4. outputs generated
5. key results
6. limitations
7. next step

## Completion criterion

This skill is complete when:

1. raw data are untouched
2. reproducible script exists
3. outputs are saved in the correct folders
4. assumptions are recorded
5. limitations are explicit