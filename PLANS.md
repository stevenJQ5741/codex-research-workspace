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

1. Do not load all skills by default.
2. Use `skills/router/ask-jiang/SKILL.md` when unsure which workflow fits.
3. Use task-specific skills only when relevant.
4. Keep scientific rules in `docs/rules/`.
5. Keep shared terms in `docs/shared_language/CONTEXT.md`.
6. Keep hard-to-reverse decisions in `docs/adr/`.

Immediate next tasks:

- [ ] Test `ask-jiang` on a real task.
- [ ] Test `research-grill` before the next complex manuscript or experiment task.
- [ ] Add project-specific shared language entries as future projects require.

### Immediate Tasks

- [x] Initialize research workspace directory structure.
- [x] Create core instruction and planning files.
- [x] Add reusable prompts for starting and ending Codex sessions.
- [x] Add templates for Japanese emails and academic manuscript writing.
- [x] Refactor rules into a token-efficient layered system.
- [ ] Test the workflow on another computer using `git clone`, `git pull`, and Codex.
- [ ] Add project-specific research briefs as new projects begin.
- [ ] Add data-analysis scripts when experimental datasets are available.

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
