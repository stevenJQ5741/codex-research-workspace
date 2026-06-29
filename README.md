# Codex Research Workspace

This repository stores project context, working plans, decision logs, reusable prompts, analysis scripts, writing rules, and templates for Codex-assisted research work.

## Purpose

The purpose of this repository is to make Codex usable across multiple computers by storing important project context in version-controlled files.

Codex itself should not be treated as the only memory source. Instead, this repository acts as the persistent project memory.

## Main folders

- `docs/`: research background, writing rules, project briefs, and technical context.
- `notes/`: decision logs, session summaries, and recurring Codex mistakes.
- `scripts/`: reproducible scripts for data analysis, figure generation, and utilities.
- `templates/`: reusable templates for emails, manuscripts, reports, presentations, and prompts.
- `data/raw/`: original data files. Do not overwrite.
- `data/processed/`: cleaned or processed data.
- `outputs/`: generated figures, tables, reports, and presentations.
- `archive/`: old or inactive materials.

## Core files

- `AGENTS.md`: operating instructions for Codex.
- `PLANS.md`: current tasks, priorities, and next steps.
- `notes/decision_logs/decision_log.md`: important decisions and rationale.
- `notes/codex_mistakes/codex_mistakes.md`: recurring errors that should be avoided.
- `templates/prompts/start_session_prompt.md`: prompt used at the beginning of a Codex session.
- `templates/prompts/end_session_prompt.md`: prompt used at the end of a Codex session.

## Basic workflow

At the start of work on any computer:

```bash
git pull
codex
```

At the end of a work session:

```bash
git status
git add .
git commit -m "Update research workspace"
```

Push only after explicit approval:

```bash
git push
```

## Token-efficient rule system

This repository uses a layered rule system to reduce unnecessary context usage.

### Layer 1: Global rules

Optional global rules can be installed at:

```text
~/.codex/AGENTS.md
```

A template is available at:

```text
templates/codex/global_AGENTS.md
```

### Layer 2: Repository rules

The root `AGENTS.md` is a compact rule index.
It should remain short and should not contain all project details.

### Layer 3: Detailed rule files

Detailed rules are stored in:

```text
docs/rules/
```

Codex should read only the rule files relevant to the current task.

Examples:

- DSC task: read `docs/rules/dsc_analysis_rules.md`
- manuscript task: read `docs/rules/manuscript_writing_rules.md`
- Japanese email task: read `docs/rules/japanese_email_rules.md`
- presentation task: read `docs/rules/presentation_rules.md`

### Principle

Do not load the whole knowledge base by default.
Load only the smallest context needed for the current task.
