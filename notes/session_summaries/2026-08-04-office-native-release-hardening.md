# 2026-08-04 Office native release hardening

## Outcome

The Windows release path now uses PowerShell-supervised Word and PowerPoint COM
workers with native `ExportAsFixedFormat`, an explicit timeout, staged promotion,
PDF header and stable-file checks, and a fail-closed visual-review status.
The default hard timeout is 90 seconds.

## Validation

- Generated project-neutral DOCX and PPTX fixtures with a random token,
  multilingual characters, Unicode formulas, and a native Word equation.
- Exported each fixture twice through Office 16.0.20228.20124.
- All four source/PDF pair QA runs passed.
- All four PDFs rendered at 180 dpi.
- DOCX run 1 and run 2 page PNG hashes matched exactly.
- PPTX run 1 and run 2 page PNG hashes matched exactly.
- Full-size visual review passed after correcting a Windows PowerShell 5.1
  source-encoding failure exposed by the first visual inspection.
- `run_release.ps1` returned exit code 2 with
  `VISUAL_REVIEW_REQUIRED`, preventing a pending review from being treated as a
  successful release.
- No residual WINWORD or POWERPNT process remained.
- All 16 Skills, all 16 `openai.yaml` files, five PowerShell scripts, and three
  Python scripts passed validation.
- Isolated installation of all 16 Skills had zero SHA-256 mismatches.

## Real-artifact validation on 2026-08-05

- Exported one real 8-page DOCX and one real 23-slide PPTX twice through the
  globally installed managed Skill.
- All four exports completed within the 90-second default timeout.
- Source hashes were unchanged; four source/PDF pair QA reports passed.
- All DOCX page images and all PPTX slide images matched exactly between repeat
  runs at 180 dpi.
- Inspected all 31 latest full-size page images. No export-induced clipping,
  overlap, missing glyph, blank image, formula loss, or chart-boundary failure
  was found.
- The runner returned exit code 2 and `VISUAL_REVIEW_REQUIRED` for both real
  artifacts until visual inspection was complete.
- Source-level review items remain distinct from renderer defects: the DOCX has
  a sparse final reference page and crowded table-header wrapping; the PPTX has
  slide-number labels `21/14` through `23/14` after its backup divider.
- Reinstalled all 16 managed Skills globally and verified SHA-256 parity with
  the repository. Exactly one global `office-native-release` copy remains.

## Remaining validation

Test clone, installation, and discovery on a second computer. The default printer
was Adobe PDF during successful tests; Microsoft Print to PDF is not required
for the authoritative export path.

No commit, push, or remote branch change was made.
