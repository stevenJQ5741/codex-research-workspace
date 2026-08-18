# Presentation QA Validation and Publication - 2026-08-18

## Outcome

The repository retained its canonical 16-Skill architecture while strengthening
presentation review with a token-aware visual-scale contract, task-declared PPTX
invariants, and reusable validation templates. The validated state was published
as rolling default branch
`agent/20260818-2121-presentation-qa-invariants`; previous default
`agent/20260805-1634-repository-stability` was preserved.

No pull request was required and no historical branch was deleted.

## Changes

- Kept overview images limited to narrative and rhythm review.
- Required full-size review only for changed, dependent, or protected slides.
- Limited local ROI review to the school logo, equation regions, and chart axes,
  ticks, or legends, and rejected undeclared ROI types.
- Added `audit_pptx_invariants.py` for page sequence, repeated page chrome,
  Office Math, forbidden visible text, effective image resolution, and duplicate
  overlapping text warnings.
- Added reusable PPTX validation-spec and presentation-revision-ledger templates.
- Preserved the boundary between bounded presentation revision, generic artifact
  QA, and final native Office release.

## Validation

- All 16 Skills passed the official validator.
- All 16 `openai.yaml` files parsed successfully.
- Four Python scripts compiled, seven PowerShell scripts parsed, and JSON
  templates parsed with no error.
- `git diff --check` passed; no credential-pattern or project-specific identifier
  was found in the universal Skills.
- Isolated and global managed installations contained 44 source files with zero
  SHA-256 parity mismatch.
- The known 34-slide failure fixture correctly failed inconsistent page-number
  and school-logo geometry.
- The corrected 33-slide deck passed slide count, page-number, logo, and 83
  Office Math checks.
- The three-slide P32-P34 deck passed partial-sequence and Office Math checks.
- Invalid ROI, page-number, and Office Math specifications failed as expected.

## Branch publication evidence

- Workflow commit: `3acf449a59117d9ace271002f4ee8671d26455fd`.
- Provisional ref: `agent/upload-presentation-qa-invariants`.
- The public event stream did not expose the first push. GitHub server
  `repository.pushedAt` was captured immediately after the single controlled
  push as `2026-08-18T12:21:35Z`, with no intervening push.
- The corresponding JST time is 2026-08-18 21:21, producing canonical branch
  `agent/20260818-2121-presentation-qa-invariants`.
- The provisional branch was atomically renamed through GitHub's branch-rename
  endpoint; no remote deletion command was used.
- The previous default and all older historical branches remain preserved.

## Remaining validation

- Evaluate the invariant and visual-scale protocol on an unrelated academic deck.
- Continue reviewing Skill usage receipts for missed triggers or unnecessary
  multi-Skill loading.
- Verify clone, managed installation, and discovery on a second computer.
