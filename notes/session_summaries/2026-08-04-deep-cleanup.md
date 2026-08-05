# 2026-08-04 - Repository Deep Cleanup

## Outcome

Shifted the repository from workflow expansion toward real-use evaluation,
consolidated policy, project-knowledge separation, and half-year branch
governance.

## Changes

- Kept 16 canonical Skills while tightening responsibility boundaries.
- Reduced active rules and moved named project context into project briefs.
- Standardized maintenance terminology and added ADR 0004.
- Added an audit report and branch-pruning dry-run.
- Preserved rolling defaults; proposed no remote branch deletion.

## Validation

- 16/16 Skills and metadata validated.
- Isolated installation achieved 16/16 SHA-256 parity.
- Script syntax, command help, link, stale-path, leakage, placeholder, metadata,
  and whitespace checks passed.
- Native Office preflight passed; no artifact pair was released.
- Three independent routing tests selected the intended Skill boundaries.
- Local annotated `snapshot/2026-H1` was created and not pushed.

## Next start point

Use real manuscript, analysis, email, presentation, and Office-release tasks to
measure routing precision before adding or splitting any Skill.
