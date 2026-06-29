# Heat-Transfer and Reheating Rules

## Purpose

Rules for moving heat-source models, surface reheating, feed-rate effects, and ILSS-related thermal discussion.

## Known working context

- Spherical metal indenter radius: approximately 10 mm.
- Head temperature: approximately 260°C.
- Specimen or bed temperature: approximately 80°C.
- Feed rates include 100, 300, 700, 1000, and 2000 mm/min.
- Indentation displacement: approximately 0.15 mm.
- Thermal contact coefficient sensitivity has been considered around 4000, 5000, and 6000 W/(m²·K).
- Differences among these h_c values are generally only several degrees Celsius.
- Feed rates not higher than 1000 mm/min can bring the calculated surface temperature into a high-softening or partial-melting range within the model assumptions.

## Core rules

1. State that calculated temperature depends on model assumptions.
2. Do not present calculated temperature as directly measured temperature.
3. Emphasize trends more than exact absolute values.
4. Lower feed rate increases contact time and therefore increases surface temperature.
5. Treat h_c as a sensitivity parameter, not as an exact fixed truth.
6. Link calculated temperature to ILSS improvement cautiously.

## Preferred wording

> Within the assumptions of the moving heat-source model, the calculated surface temperature reached the high-softening or partial-melting range when the feed rate was not higher than 1000 mm/min. The sensitivity analysis for h_c = 4000-6000 W/(m²·K) produced only several degrees of difference, indicating that the qualitative temperature trend is relatively insensitive to this parameter within the examined range.

## Avoid

- measured surface temperature
- proved melting
- h_c has no effect
- exact prediction
- ILSS improvement is solely caused by melting
