# Workflow Governance Rules

## Purpose

Keep repository context, Skills, validation, and installation predictable without
duplicating active policy.

## Context loading

1. Read `AGENTS.md`, `README.md`, and `PLANS.md` first.
2. Load only files required by the current task.
3. Prefer current sources and durable decisions over historical summaries.
4. Use targeted search before opening broad folders or large artifacts.
5. Do not repeat full rules in responses or session summaries.

## Content boundaries

- Keep root guidance compact and index-like.
- Keep repeatable procedures in Skills.
- Keep reusable professional rules in `docs/rules/`.
- Keep project facts, files, parameters, and event details in
  `docs/project_briefs/`.
- Keep canonical terms in `docs/shared_language/CONTEXT.md`.
- Keep hard-to-reverse decisions in `docs/adr/`.
- Keep historical evidence in `notes/`; do not treat it as active policy.

## Skill design

Each Skill must contain:

1. frontmatter with `name` and a precise trigger description
2. operational steps
3. explicit stop conditions
4. an observable `Completion criterion`
5. `agents/openai.yaml` with current interface metadata and
   `allow_implicit_invocation: true`

Use one primary and no more than two supporting Skills. Automatic invocation does
not grant authority for destructive, external, sensitive, commit, push, or remote
branch actions.

## Validation and installation

After a material Skill change:

1. run the official validator on every Skill
2. parse every `agents/openai.yaml`
3. check completion criteria and TODO placeholders
4. parse bundled PowerShell and Python scripts
5. run relevant script smoke tests
6. install to an isolated directory and verify SHA-256 parity
7. run `git diff --check`

Repository Skills are not discoverable merely because they exist in Git. Install
managed copies with `scripts/install_skills.ps1`; never replace an unmarked
personal Skill.

## Branch maintenance

- Treat `docs/adr/0004-maintenance-boundaries-and-branch-retention.md` as the
  authoritative policy.
- Generate the half-year table with
  `scripts/branch_pruning_dry_run.ps1`; missing activity attestation is a
  protection condition, not evidence of inactivity.
- Keep dry-run generation, remote deletion approval, deletion, and post-delete
  verification as distinct steps.
- Validate before rolling-default publication, preserve the previous default,
  and update `origin/HEAD` after promotion.

## Stop conditions

Stop and resolve the issue before release when:

- an active document conflicts with an accepted ADR
- a universal Skill contains project-specific identifiers or parameters
- two active files claim authority for the same policy
- validation depends on a missing tool or unrecorded exception
- a destructive or remote action lacks explicit authorization
