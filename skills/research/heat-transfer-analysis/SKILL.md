---
name: heat-transfer-analysis
description: Heat-transfer and reheating analysis workflow for moving heat-source models, feed-rate effects, h_c sensitivity, and ILSS interpretation.
disable-model-invocation: true
---

# Heat-Transfer Analysis

## Purpose

Analyze or write about reheating, moving heat-source models, feed-rate effects, and ILSS-related thermal interpretation.

## Required rules

Read:

- `docs/rules/heat_transfer_rules.md`
- `docs/rules/manuscript_writing_rules.md`

Read DSC rules only if DSC evidence is discussed.

## Process

### 1. Identify model scope

Confirm:

- geometry
- boundary assumptions
- heat source temperature
- specimen temperature
- feed rate
- contact time
- thermal contact coefficient
- material properties
- whether values are measured or calculated

### 2. State assumptions

Before calculation or writing, state model assumptions explicitly.

### 3. Sensitivity check

If `h_c` is discussed, treat it as sensitivity analysis.

Do not claim `h_c` has no effect.  
Use:

```text
limited influence within the examined range
```

### 4. Link to experiment cautiously

When linking to ILSS:

- do not say the model proves melting
- do not say ILSS improvement is solely caused by melting
- state consistency between calculated temperature and observed trend

### 5. Output

Produce:

- calculation table if applicable
- figure if applicable
- cautious manuscript paragraph if requested

## Completion criterion

This skill is complete when:

1. model assumptions are explicit
2. calculated values are not described as measurements
3. sensitivity interpretation is cautious
4. ILSS mechanism is not overclaimed
5. final wording is directly usable if requested