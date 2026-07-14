---
name: skill-usage-report
description: Disclose which Skills materially affected a Codex task and capture concise feedback for measuring workflow frequency and deciding revisions. Use automatically at the end of every task, including when no task-specific Skill was used.
---

# Skill Usage Report

## Process

### 1. Record actual use

List only Skills whose instructions materially affected routing, actions, validation, or output. Do not list a Skill merely because it was available or inspected.

### 2. Label the role

Classify each used Skill as primary, supporting, or reporting. State its concrete contribution in one short phrase.

### 3. Report non-use

When no task-specific Skill was used, write task Skill: none. Still disclose skill-usage-report as the reporting mechanism when it was active.

### 4. Capture revision signals

Mention one concise issue only when a Skill was missing, redundant, ambiguous, too costly, or insufficient. Do not invent feedback on routine successful runs.

### 5. Use the fixed receipt

End the final response with:

- Skill usage
- Primary: skill-name - concrete contribution
- Supporting: skill-name - concrete contribution
- Reporting: skill-usage-report - usage disclosure
- Revision signal: none, or one evidence-based issue

When the response language is Chinese, translate field labels into concise Chinese. For very small responses, compress the receipt to one line without omitting names.

## Completion criterion

This skill is complete when:

1. every materially used Skill is named
2. considered-but-unused Skills are excluded
3. roles and concrete contributions are visible
4. non-use is explicitly reported
5. a revision signal is included only when evidence exists
