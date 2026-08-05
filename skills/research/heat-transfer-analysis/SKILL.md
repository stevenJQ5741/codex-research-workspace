---
name: heat-transfer-analysis
description: Analyze heat transfer, reheating, moving heat sources, feed-rate effects, contact-coefficient sensitivity, and links between calculated temperature and mechanical behavior. Use for thermal model calculations, sensitivity studies, figures, tables, or cautious manuscript interpretation.
---

# Heat-Transfer Analysis

## Procedure

1. Read `docs/rules/heat_transfer_rules.md`,
   `docs/rules/data_management_rules.md`, and only the applicable project brief.
2. Confirm geometry, boundaries, initial conditions, time or speed, thermal
   properties, contact parameters, and whether each value is measured,
   literature-derived, fitted, or assumed.
3. Register equations, units, sign conventions, simplifications, and model range.
4. Reproduce a baseline or limiting case before calculating new conditions.
5. Check sensitivity for uncertain parameters and report the examined range.
6. Compare calculated trends with experiments without calling model outputs
   measurements or treating consistency as causal proof.
7. Generate traceable tables, figures, and qualified manuscript wording.

## Stop conditions

Stop when required geometry or boundary conditions are missing, units or time
scales are inconsistent, a baseline cannot be reproduced, sensitivity is
untested for a consequential uncertain parameter, or the requested mechanism
claim exceeds the evidence.

## Completion criterion

This skill is complete when:

1. scope, inputs, assumptions, and evidence classes are explicit
2. baseline, units, and limiting behavior pass
3. uncertain parameters have an appropriate sensitivity check
4. calculated and measured quantities remain distinct
5. outputs and wording match the model's validated range
