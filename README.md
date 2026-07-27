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
powershell -ExecutionPolicy Bypass -File scripts/install_skills.ps1
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

### Rolling default versions

Each approved upload becomes a new timestamped version branch:

```text
agent/YYYYMMDD-HHmm-topic
```

The timestamp is the first successful Push time in Japan Standard Time. After validation, promote that branch to the GitHub default and update local `origin/HEAD`. Keep the previous default branch as a historical backup. Do not delete older timestamped branches unless explicitly approved.

A pull request is optional for this repository's version-promotion workflow. Use one when review or comparison is useful; otherwise the validated upload branch may be promoted directly.

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

## Research skills system

This repository includes a research-oriented skills system under:

```text
skills/
```

The skills are designed to provide repeatable workflows for common research tasks while keeping token usage controlled.

### Design principles

- Installed skills may be selected automatically from concise metadata.
- `ask-jiang` routes ambiguous or multi-workflow tasks.
- Use at most one primary and two supporting skills.
- Ask once before method-sensitive or scope-expanding workflows.
- Detailed rules remain in `docs/rules/`.
- Shared terminology lives in `docs/shared_language/CONTEXT.md`.
- Hard-to-reverse decisions live in `docs/adr/`.
- Each skill has a completion criterion.
- Major workflows should include a feedback loop.
- Every final response includes a Skill usage receipt.

### Common skills

| Task | Skill |
| --- | --- |
| choose the right workflow | `skills/router/ask-jiang/SKILL.md` |
| clarify research plans | `skills/research/research-grill/SKILL.md` |
| maintain shared language | `skills/research/shared-language/SKILL.md` |
| reproducible analysis | `skills/research/analysis-feedback-loop/SKILL.md` |
| review manuscript text | `skills/research/manuscript-review/SKILL.md` |
| produce a full manuscript | `skills/research/manuscript-pipeline/SKILL.md` |
| audit scientific claims | `skills/research/claim-evidence-audit/SKILL.md` |
| analyze DSC data | `skills/research/dsc-analysis/SKILL.md` |
| analyze reheating or heat transfer | `skills/research/heat-transfer-analysis/SKILL.md` |
| review presentations | `skills/research/presentation-review/SKILL.md` |
| draft Japanese emails | `skills/research/japanese-email/SKILL.md` |
| edit a research profile, brief CV, or research summary | `skills/research/research-brief-editor/SKILL.md` |
| release a DOCX/PPTX and PDF pair through native Office | `skills/research/office-native-release/SKILL.md` |
| verify research artifacts | `skills/research/artifact-qa/SKILL.md` |
| create handoff summaries | `skills/research/handoff/SKILL.md` |
| report Skill use | `skills/governance/skill-usage-report/SKILL.md` |

### Principle

Do not load the whole knowledge base by default.
Load only the smallest context needed for the current task.

## Install or update Skills

The repository is the source of truth. Install managed copies into the local Codex directory:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_skills.ps1
```

Run the command after `git pull`, then restart Codex so the updated skill catalog is discovered. The installer replaces only copies marked as managed by this repository.
