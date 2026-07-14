# Skill Design Rules

## Purpose

Define how to create, invoke, validate, install, and maintain research Skills in this repository.

## Core principles

1. Use Skills for repeatable workflows, not background storage.
2. Keep root AGENTS.md compact and index-like.
3. Keep detailed scientific rules in docs/rules/.
4. Keep durable terminology in docs/shared_language/.
5. Keep hard-to-reverse decisions in docs/adr/.
6. Load only the smallest context needed.
7. Give every Skill a checkable Completion criterion.
8. Prefer one primary and no more than two supporting Skills.
9. Report actual Skill use at the end of every task.
10. Remove duplicated, stale, or no-op instructions.

## Skill structure

Each Skill must contain:

- SKILL.md with name and description frontmatter only
- a concise workflow body
- an explicit Completion criterion
- agents/openai.yaml with interface metadata and invocation policy

Descriptions must state both what the Skill does and the concrete situations that trigger it.

## Automatic invocation

All canonical Skills use:

```yaml
policy:
  allow_implicit_invocation: true
```

Automatic discovery does not grant extra authority. File deletion, sensitive-data handling, external messages, commits, pushes, and other consequential actions still follow user authorization and platform approval rules.

## Invocation gate

Proceed automatically when:

- the task-to-Skill match is clear
- the requested action already authorizes the work
- the Skill does not materially expand scope

Ask once before execution when:

- two or more primary workflows compete
- a methodological choice can change the scientific result
- required assumptions are unresolved
- the workflow adds substantial cost or context
- the proposed work materially expands the request

Use ask-jiang to resolve ambiguous or multi-workflow tasks.

## Context hierarchy

Use this order:

1. Skill workflow: actions required now.
2. Short in-Skill rules: required every run.
3. External rules or references: load only when relevant.

Do not duplicate long scientific background inside SKILL.md.

## Completion criterion

Completion criteria must be observable, task-specific, and resistant to premature completion. Major workflows should check inputs, assumptions, output generation, self-review, correction, final verification, and unresolved risks.

## Skill usage receipt

Every final response must disclose:

1. primary Skill
2. supporting Skills
3. reporting Skill
4. an evidence-based revision signal, or none

List only Skills that materially affected routing, actions, validation, or output.

## Installation

The canonical source is the repository skills/ directory.

Run scripts/install_skills.ps1 after cloning or pulling on each computer. Installed copies are disposable and may be replaced only when they contain the repository management marker.

Restart Codex after installation so the catalog is refreshed.

## Validation

Before commit:

1. run the Skill validator on every SKILL.md
2. parse every agents/openai.yaml
3. check all Completion criterion headings
4. scan for TODO placeholders
5. run git diff --check

## Pruning

Delete or consolidate:

- parallel version trees after approval
- duplicated rules
- stale pilot language
- generic advice that does not change behavior
- obsolete paths or invocation metadata
