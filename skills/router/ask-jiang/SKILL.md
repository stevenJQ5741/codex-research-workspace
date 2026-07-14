---
name: ask-jiang
description: Route Quan Jiang's research task to the smallest effective combination of installed skills and rule files. Use automatically when a task spans multiple workflows, the correct workflow is unclear, or invoking a skill may require user confirmation.
---

# Ask Jiang Router

## Process

### 1. Classify the deliverable

Identify the primary output: research decision, analysis, manuscript, figure or table set, presentation, email, repository change, or handoff.

### 2. Check evidence and risk

Identify source files, missing inputs, scientific stakes, file-mutation risk, and whether the task can be answered read-only.

### 3. Select the smallest workflow

Choose one primary skill and at most two supporting skills:

| Need | Skill |
| --- | --- |
| consequential ambiguity | research-grill |
| reproducible calculations or figures | analysis-feedback-loop |
| full manuscript production | manuscript-pipeline |
| manuscript evidence and language review | manuscript-review |
| scientific claim audit | claim-evidence-audit |
| terminology or symbol control | shared-language |
| DSC interpretation | dsc-analysis |
| heat-transfer or reheating analysis | heat-transfer-analysis |
| presentation review | presentation-review |
| Japanese email | japanese-email |
| DOCX, PDF, figure, or table verification | artifact-qa |
| cross-session continuation | handoff |
| skill-use disclosure | skill-usage-report |

Read only the rule files required by the selected skills.

### 4. Apply the invocation gate

Proceed automatically when the match is clear and the requested action already authorizes the work. Ask once before execution when the workflow is ambiguous, method-sensitive, unusually expensive, or materially expands scope.

Always obtain separate authorization for destructive actions, external messages, commits, pushes, or sensitive-data handling when the user has not already authorized them.

### 5. Report actual use

End with a Skill usage receipt. List only skills whose instructions materially affected the work.

## Completion criterion

This skill is complete when:

1. the deliverable and risk are classified
2. one primary and no more than two supporting skills are selected
3. only relevant rule files are loaded
4. automatic execution or confirmation matches the invocation gate
5. actual skill use is disclosed
