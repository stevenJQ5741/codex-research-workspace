# 0002 - Integrated Skills and Invocation Policy

## Status

Accepted

## Context

The original Skills provided reusable workflows, while the manuscript pilot added stronger provenance, claim auditing, artifact QA, and usage reporting. Keeping separate V1 and V2 trees created duplicate instructions and prevented a clear installation path.

Repository files also are not automatically discoverable as installed Codex Skills.

## Decision

1. Keep one canonical skills/ tree.
2. Merge the approved pilot improvements into the canonical Skills.
3. Remove the parallel skills_v2/ tree.
4. Allow every canonical Skill to be discovered implicitly.
5. Use an invocation gate for ambiguous, method-sensitive, expensive, or scope-expanding work.
6. Use at most one primary and two supporting Skills.
7. Report actual Skill use in every final response.
8. Install managed copies with scripts/install_skills.ps1.

## Reason

One canonical tree removes drift. Automatic discovery reduces the need to remember Skill names. The confirmation gate preserves scientific and operational control without adding a question to routine work.

## Consequences

- Skill descriptions become part of the routing interface and must remain precise.
- Automatic invocation does not authorize destructive, external, sensitive, commit, or push actions.
- The repository remains the source of truth across computers.
- Installed copies may be replaced only when marked as repository-managed.
- Invocation precision should be revised from real usage receipts.
