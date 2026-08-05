# 0004 - Maintenance Boundaries and Half-Year Branch Retention

## Status

Accepted

## Context

The repository had accumulated duplicated active policy, overlapping Skill
descriptions, project details inside reusable rules and Skills, and rolling
default branches without a long-term pruning standard.

## Decision

### Content boundaries

1. Keep `AGENTS.md` as a compact entrypoint.
2. Keep repeatable procedures in Skills, reusable professional constraints in
   `docs/rules/`, project-specific facts in `docs/project_briefs/`, canonical
   terms in `docs/shared_language/CONTEXT.md`, and durable policy in ADRs.
3. Do not place project filenames, experiment parameters, private identifiers,
   fixed artifact hashes, or project history in universal Skills.
4. Treat ADRs as active policy and decision/session logs as historical evidence.
   Mark superseded historical policy rather than silently presenting it as current.

### Skill boundaries

1. `manuscript-pipeline` orchestrates full production;
   `manuscript-review` reviews an existing draft.
2. `claim-evidence-audit` evaluates claims; `manuscript-review` covers the broader
   manuscript argument, language, consistency, and readiness.
3. `artifact-qa` performs general artifact checks; `office-native-release`
   performs final native Word/PowerPoint export and Office/PDF pair release.
4. `ask-jiang` routes workflows; `research-grill` resolves consequential
   assumptions within the selected work.
5. `presentation-review` reviews and revises presentations and validates bounded
   PPTX changes; `office-native-release` owns final native PowerPoint release.

### Half-year branch governance

1. Keep the rolling default branch mechanism.
2. Run branch maintenance every six months and create an annotated
   `snapshot/YYYY-H1` or `snapshot/YYYY-H2` tag.
3. Use the branch-tip commit time to determine age; use branch-name time only as
   supporting evidence.
4. Permanently protect the current default, previous default, open-PR branches,
   active work, and user-designated milestones.
5. A branch becomes a deletion candidate only when all are true:
   - its tip is more than six months old
   - it has no open pull request
   - it has no active work
   - it has no unarchived unique commit
   - it is covered by the current default or a snapshot tag
6. Before deleting a branch with unique commits, create an archive tag or record
   an explicit abandonment reason.
7. Generate a dry-run table and obtain explicit user approval before any remote
   deletion.
8. After approved deletion, verify the default branch, `origin/HEAD`, tags, and
   reachability of every protected or archived commit.
9. Record each cycle in
   `notes/branch_maintenance/branch_pruning_log.md`.

### Deterministic pruning gate

1. Generate each dry-run with `scripts/branch_pruning_dry_run.ps1`.
2. Require the previous default branch and any active work or user milestones to
   be declared explicitly.
3. Treat a branch with unknown activity as protected. Only an explicit
   `-InactiveBranch` attestation can satisfy the no-active-work condition.
4. Query the GitHub default branch and open pull requests at run time; do not
   infer them from local notes or branch names.
5. Keep the script dry-run-only. Remote deletion is a separate, user-approved
   operation and must never be added as a convenience switch.

### Rolling-default publication

1. Validate the complete intended repository state before publication.
2. Push one provisional upload branch, obtain its first successful GitHub
   `PushEvent`, and rename the branch to `agent/YYYYMMDD-HHmm-topic` using that
   event time in JST.
3. Verify the renamed ref and commit before promoting it to GitHub default.
4. Preserve the previous default and synchronize local `origin/HEAD`.
5. Use pull requests only when review or comparison is requested.
6. Publish the applicable half-year annotated snapshot tag when the maintenance
   cycle is approved for GitHub publication.

## Consequences

- The active rule set is smaller and project knowledge has a stable home.
- Skill count may remain unchanged while responsibility and instruction load are
  reduced.
- Snapshot tags complement rolling defaults but do not replace branches used for
  active work.
- Mechanical validation can prove structure and parity; real tasks are still
  required to evaluate routing precision.
