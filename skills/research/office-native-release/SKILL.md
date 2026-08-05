---
name: office-native-release
description: Export and verify an explicitly declared final DOCX or PPTX and its PDF through native Microsoft Word or PowerPoint on Windows. Use for release candidates requiring protected hashes, JSON-spec structural and semantic pair QA, Poppler rendering, and full-page or full-slide inspection; do not use for content authoring, manuscript review, presentation revision, or generic artifact QA.
---

# Office Native Release

## Procedure

1. Require one authoritative DOCX or PPTX, target PDF, UTF-8 release spec,
   protected hashes, expected structure, required and forbidden wording, and a
   fresh render directory.
2. Resolve scripts from this Skill directory and run
   `scripts/office_preflight.ps1`. After an Office, Windows, font, printer, or
   runtime change, run `scripts/test_office_export.ps1`; require two identical
   full-page renders for both its DOCX and PPTX fixtures. Treat Word or
   PowerPoint as authoritative; LibreOffice and PDF printers are diagnostic only.
3. Run `scripts/run_release.ps1` with the release spec and render directory.
   Use `-OverwritePdf` only with explicit overwrite authorization and
   `-SkipExport` only for a PDF with known native provenance. Treat exit code 2
   and `VISUAL_REVIEW_REQUIRED` as a hard pending state, not a successful release.
4. Require `scripts/qa_release.py` to pass source hashes, PDF geometry, Office
   structure, source/PDF wording, critical glyphs, and applicable slide-to-page
   consistency.
5. Render every PDF page with `scripts/render_pdf.py` at 180 dpi or higher.
   Inspect the montage for triage, then every latest full-size page or slide.
6. Check clipping, overlap, wrapping, page breaks, glyphs, axes, citations,
   numbering, geometry, privacy exclusions, and internal-only text.
7. Preserve the source, PDF, spec, logs, reports, and renders. Record the release
   decision and exact failed check when approval is withheld.

## Stop conditions

Stop when the source is not an explicit release candidate, a protected hash
changes, native Office is unavailable, export times out, repeated renders differ,
any source/PDF pair check fails, the runner reports `VISUAL_REVIEW_REQUIRED`, any
latest page remains uninspected, or overwrite authority is missing.

## Completion criterion

This skill is complete when:

1. source, PDF, spec, hashes, and render directory are explicit
2. native Word or PowerPoint produced the PDF
3. the exporter returned an explicit `EXPORTED` result without timeout
4. every structural and semantic pair check passes
5. every latest rendered page or slide is inspected at full size
6. no unresolved layout, glyph, figure, privacy, or cross-file defect remains
7. evidence and the release decision are preserved
