---
name: ask-jiang
description: Router for Quan Jiang's research skills. Use manually when unsure which workflow, rule file, or skill should be used.
disable-model-invocation: true
---

# Ask Jiang Router

## Purpose

Recommend the smallest suitable workflow for the user's current task.

This skill should not execute the full task.  
It should classify the task and recommend:

1. which skill to invoke
2. which rule files to read
3. whether shared language or decision logs need updating
4. the minimum next action

## Process

### 1. Classify the task

Choose one primary category:

- research planning
- manuscript writing or revision
- DSC or thermal analysis
- heat-transfer or reheating analysis
- IFSS or interface interpretation
- presentation or slide review
- Japanese email
- data analysis
- handoff or cross-computer continuation
- repository maintenance

### 2. Recommend a skill

Use this map:

| Task | Skill |
| --- | --- |
| unclear plan or experimental design | `skills/research/research-grill/SKILL.md` |
| terminology or shared language update | `skills/research/shared-language/SKILL.md` |
| data analysis with reproducibility requirements | `skills/research/analysis-feedback-loop/SKILL.md` |
| manuscript review | `skills/research/manuscript-review/SKILL.md` |
| DSC interpretation | `skills/research/dsc-analysis/SKILL.md` |
| heat-transfer or ILSS reheating | `skills/research/heat-transfer-analysis/SKILL.md` |
| presentation or PPT review | `skills/research/presentation-review/SKILL.md` |
| Japanese email | `skills/research/japanese-email/SKILL.md` |
| session transfer or cross-computer continuation | `skills/research/handoff/SKILL.md` |

### 3. Recommend rule files

Use only the smallest relevant set.

Default:

- `AGENTS.md`
- `README.md`
- `PLANS.md`

Then add one or two relevant files from:

- `docs/rules/manuscript_writing_rules.md`
- `docs/rules/dsc_analysis_rules.md`
- `docs/rules/heat_transfer_rules.md`
- `docs/rules/ifss_interface_rules.md`
- `docs/rules/natural_fiber_project_rules.md`
- `docs/rules/data_management_rules.md`
- `docs/rules/japanese_email_rules.md`
- `docs/rules/presentation_rules.md`
- `docs/rules/current_research_context.md`
- `docs/shared_language/CONTEXT.md`

### 4. Completion criterion

The router is complete when it outputs:

1. recommended skill
2. recommended rule files
3. reason for the recommendation
4. first concrete next instruction for the user

Do not perform the actual task unless the user explicitly asks.