# PLANS.md

## Active objective

Evaluate the existing research workflow on real tasks while keeping the
repository compact, non-duplicative, and stable across computers.

## Current status

- The repository uses a compact root entrypoint, reusable professional rules,
  project briefs, canonical terminology, ADRs, and one canonical 16-Skill tree.
- Skill responsibilities were consolidated in August 2026 without adding a
  parallel version tree.
- Rolling default branches remain active; half-year branch maintenance is
  governed by ADR 0004.
- Native Word and PowerPoint remain authoritative only for declared final Office
  releases; LibreOffice is diagnostic.
- Native Office export is hardened around PowerShell-supervised
  `ExportAsFixedFormat`, a 90-second default hard timeout, deterministic repeat
  renders, and a fail-closed visual-review state.
- Presentation review now separates overview, full-size, and narrowly permitted
  ROI evidence, and uses task-specific PPTX invariants for numbering, repeated
  page chrome, Office Math, visible language, and image resolution.
- Half-year branch maintenance now has a deterministic dry-run gate that treats
  unknown activity as protected and cannot delete remote branches.
- The native release path passed repeat-render validation on one real 8-page
  DOCX and one real 23-slide PPTX without modifying either source.
- The validated repository is published on the rolling default branch
  `agent/20260805-1634-repository-stability`; the previous default remains
  preserved and `snapshot/2026-H1` is published as an annotated checkpoint.

## Immediate tasks

- [ ] Evaluate automatic routing on real manuscript, analysis, Japanese-email,
      presentation, and Office-release tasks.
- [ ] Review Skill usage receipts after several sessions for false positives,
      missed triggers, or unnecessary multi-Skill loading.
- [ ] Test clone, pull, Skill installation, and discovery on another computer.
- [ ] Re-run native Office smoke tests after material Office, Windows, or Codex
      runtime changes.
- [ ] Evaluate the presentation invariant and token-aware visual-review protocol
      on an unrelated academic deck after its real-project regression tests pass.
- [x] Validate the hardened native Office release path on a real long DOCX/PPTX
      pair after synthetic deterministic smoke tests pass.
- [ ] Add or revise project briefs only when validated project evidence changes.

## Maintenance schedule

### Every material Skill change

1. Validate every Skill and `openai.yaml`.
2. Check completion criteria and placeholders.
3. Parse PowerShell and Python scripts.
4. Install to an isolated destination and verify file-hash parity.
5. Record real-task validation still required.

### Every six months

1. Refresh remote branch, tag, default-branch, and open-PR state.
2. Create the annotated `snapshot/YYYY-H1` or `snapshot/YYYY-H2` checkpoint.
3. Generate the branch-pruning dry-run using branch-tip commit time.
4. Protect current and previous defaults, open-PR branches, active work,
   user milestones, and unarchived unique commits.
5. Delete no remote branch without explicit approval.
6. Record the cycle in `notes/branch_maintenance/branch_pruning_log.md`.

## Unresolved issues

- Skill structure and installation can be validated mechanically, but routing
  quality still requires real user tasks.
- The repository has not yet been verified end-to-end on a second computer.
- Project briefs remain working context and must not be treated as validated
  evidence unless their own sources support them.
