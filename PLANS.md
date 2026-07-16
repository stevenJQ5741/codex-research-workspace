# PLANS.md

## Current Plans

### Active Objective

Build a cross-computer Codex workflow using GitHub as the persistent project memory.

### Current Status

The repository has been initialized as a general research workspace. Important context should be written into version-controlled files instead of being left only in temporary chat history.

## Current workflow policy

The repository now uses a token-efficient layered rule system.

Default session start:

1. Read `AGENTS.md`.
2. Read `README.md`.
3. Read `PLANS.md`.
4. Select only relevant files from `docs/rules/`.
5. Do not read all rule files by default.

Default session end:

1. Summarize modified files.
2. Record durable decisions only.
3. Update `PLANS.md` only when task status changes.
4. Keep summaries short.

## Current skills policy

The repository now includes a research-oriented skills system.

Default behavior:

1. Install Skills with `scripts/install_skills.ps1`.
2. Select relevant Skills automatically from concise metadata.
3. Use `skills/router/ask-jiang/SKILL.md` for ambiguous or multi-workflow tasks.
4. Use at most one primary and two supporting Skills.
5. Ask once before method-sensitive or scope-expanding workflows.
6. Keep scientific rules in `docs/rules/`.
7. Keep shared terms in `docs/shared_language/CONTEXT.md`.
8. Keep hard-to-reverse decisions in `docs/adr/`.
9. Report actual Skill use in every final response.

Immediate next tasks:

- [ ] Test automatic routing on real manuscript, analysis, and email tasks.
- [ ] Review Skill usage receipts after several sessions for overlap or missing workflows.
- [ ] Add project-specific shared language entries as future projects require.

### Integrated skills status

Current status:

- [x] Merge the pilot improvements into one canonical `skills/` tree.
- [x] Add manuscript pipeline, claim-evidence audit, artifact QA, and Skill usage reporting.
- [x] Add implicit-invocation metadata and a confirmation gate.
- [x] Add explicit completion criteria to every Skill.
- [x] Add a cross-computer installer.
- [x] Add separate research-brief editing and native Office release Skills.
- [x] Validate Word/PDF and PowerPoint/PDF release paths on the primary Windows workstation.
- [ ] Evaluate invocation precision and revise descriptions from real usage evidence.

### Immediate Tasks

- [x] Initialize research workspace directory structure.
- [x] Create core instruction and planning files.
- [x] Add reusable prompts for starting and ending Codex sessions.
- [x] Add templates for Japanese emails and academic manuscript writing.
- [x] Refactor rules into a token-efficient layered system.
- [ ] Test the workflow on another computer using `git clone`, `git pull`, and Codex.
- [ ] Add project-specific research briefs as new projects begin.
- [ ] Add data-analysis scripts when experimental datasets are available.
- [ ] Recheck Office preflight and native release smoke tests after Office, Windows, or Codex runtime updates.

### Standard Workflow

At the beginning of each major session:

1. Run `git pull`.
2. Ask Codex to read `AGENTS.md`, `README.md`, `PLANS.md`, and relevant notes.
3. Ask Codex to summarize the current state.
4. Start the actual task.

At the end of each major session:

1. Ask Codex to summarize what changed.
2. Update `PLANS.md`.
3. Update `notes/decision_logs/decision_log.md` if decisions were made.
4. Update `notes/session_summaries/`.
5. Commit changes locally.
6. Push only after explicit user approval.

### Do Not

- Do not overwrite raw data.
- Do not delete existing files without explicit confirmation.
- Do not claim uncertain scientific conclusions as facts.
- Do not leave important decisions only in chat history.

### Next Steps

1. Add project briefs under `docs/project_briefs/`.
2. Add writing rules or journal-specific instructions under `docs/writing_rules/`.
3. Record meaningful decisions in `notes/decision_logs/decision_log.md`.
4. Save future session summaries under `notes/session_summaries/`.

### Unresolved Issues

- No project-specific datasets, manuscripts, or slide decks have been added yet.
