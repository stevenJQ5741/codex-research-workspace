# AGENTS.md

## Purpose

This repository is the persistent, version-controlled memory for Codex-assisted
research work. Keep this file as a compact entrypoint; do not expand it into a
handbook.

## Non-negotiable rules

1. Be precise and do not invent data, citations, parameters, files, or conditions.
2. Separate observations, calculations, assumptions, literature interpretation,
   and speculation.
3. Do not describe model outputs as measurements or overstate causal support.
4. Do not overwrite raw data or delete files without explicit approval.
5. Do not commit credentials, private identifiers, or identity documents.
6. Preserve the user's scientific logic unless restructuring is requested.
7. Prefer reproducible workflows and record unresolved evidence.

## Language

- Use Chinese for discussion and planning unless requested otherwise.
- Use academic English for manuscripts, reports, captions, and conference material.
- Use concise, natural Japanese for academic and administrative email.

## Start with the smallest context

Read first:

1. `AGENTS.md`
2. `README.md`
3. `PLANS.md`

Then load only the rule, Skill, project brief, decision, or source file required
by the task. Do not read all historical notes or all `docs/rules/` by default.

## Information homes

| Content | Authoritative location |
| --- | --- |
| active task state | `PLANS.md` |
| reusable professional rules | `docs/rules/` |
| project-specific knowledge | `docs/project_briefs/` |
| durable terminology | `docs/shared_language/CONTEXT.md` |
| hard-to-reverse decisions | `docs/adr/` |
| historical decisions and sessions | `notes/` |
| reusable workflows | `skills/` |

Do not duplicate a complete workflow or professional rule in this file.

## Skills and authorization

Use `skills/router/ask-jiang/SKILL.md` when routing is unclear. Select at most one
primary and two supporting Skills. The Skill inventory and responsibility
boundaries are in `README.md`.

Automatic Skill discovery does not authorize deletion, external messages,
commits, pushes, remote branch changes, or sensitive-data handling.

## Repository governance

- Treat the repository `skills/` tree as authoritative; install managed copies
  with `scripts/install_skills.ps1`.
- Follow the rolling-default and half-year branch policy in
  `docs/adr/0004-maintenance-boundaries-and-branch-retention.md`.
- Record branch dry-runs and approved actions in
  `notes/branch_maintenance/branch_pruning_log.md`.
- Do not commit or push unless explicitly authorized.

## End of a major session

1. List modified and deleted files.
2. Record durable decisions only when future work depends on them.
3. Update `PLANS.md` only when active state changes.
4. Add a short session summary only when it has continuation value.
5. Run relevant validation and `git status`.
6. Report unresolved risks and the exact next action.
