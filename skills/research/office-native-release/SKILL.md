---
name: office-native-release
description: Export and verify final DOCX or PPTX artifacts and their PDFs on Windows. Use when a release candidate must be rendered by native Microsoft Word or PowerPoint, checked structurally and semantically against a JSON spec, rasterized with Poppler, and visually inspected page by page or slide by slide. Do not use for research claim selection, manuscript writing, content restructuring, or generic figure and spreadsheet QA; LibreOffice is diagnostic only and never an automatic release fallback.
---

# Office Native Release

Release an authoritative DOCX or PPTX through Microsoft Office and require both structural and visual evidence before approval.

## 1. Confirm inputs and environment

Require:

- one authoritative DOCX or PPTX
- one target PDF path
- one UTF-8 release spec containing expected structure, required and forbidden wording, and protected hashes
- one fresh render directory

After Office, LibreOffice, Windows, or Codex runtime updates, resolve bundled scripts from the directory containing this `SKILL.md`; do not assume the current project contains a copy. Set `$skillRoot` to that directory, then run:

```powershell
powershell -ExecutionPolicy Bypass -File (Join-Path $skillRoot 'scripts\office_preflight.ps1') -OutputJson _work/office_preflight.json
```

Treat Word or PowerPoint as the authoritative release renderer. Do not fall back automatically to LibreOffice; use it only for optional renderer-drift diagnosis.

## 2. Run the guarded release pipeline

Use the one-command runner:

```powershell
powershell -ExecutionPolicy Bypass -File (Join-Path $skillRoot 'scripts\run_release.ps1') -Spec release_spec.json -RenderDir _work/release_render
```

Pass `-OverwritePdf` only when replacing the target PDF is explicitly authorized. Pass `-SkipExport` only when validating an already generated PDF with known provenance.

The runner must:

1. resolve the Codex-bundled Python runtime
2. export the Office source to PDF through Word or PowerPoint COM
3. run structural and semantic pair QA
4. render every PDF page with Poppler
5. stop with `visual_inspection_pending: true`

Never report release completion from the runner alone.

## 3. Enforce Layer A: structural and semantic QA

Use `scripts/qa_release.py` to check:

- source and protected-baseline hashes
- PDF page count and geometry
- DOCX sections, tables, and inline images
- PPTX slides, shapes, pictures, charts, and tables
- PPTX slide count versus PDF page count
- required and forbidden wording in both the Office source and PDF
- critical glyph survival such as Greek symbols, subscripts, superscripts, and equations
- optional slide-to-PDF text-token coverage

Treat any Office-source/PDF mismatch as a release failure even when the page images look acceptable.

## 4. Enforce Layer B: native visual QA

Use `scripts/render_pdf.py` at 180 dpi or higher. Review the montage for triage, then inspect every full-size page or slide after the latest material change.

Check:

- clipping, overlap, blank pages, broken fields, and unstable page breaks
- font substitution, missing glyphs, unexpected wrapping, and unreadable captions
- complete axes, ticks, legends, labels, and figure boundaries
- headers, footers, numbering, and page or slide geometry
- privacy exclusions and absence of internal-only provenance text

For PPTX, also run the available slide-overflow checker and inspect each slide individually. Use an independent artifact-tool render only to diagnose renderer drift; do not require strict cross-renderer pixel equality.

## 5. Preserve failure evidence

Do not delete or overwrite the failed source, PDF, logs, spec, or render manifest. Record the exact failed check, correct the authoritative Office source or builder, regenerate the PDF, and repeat both layers.

## Completion criterion

This skill is complete when:

1. the exact Office source, PDF, spec, and protected hashes are identified
2. the PDF is exported from the authoritative source through native Microsoft Office
3. every structural and semantic check passes for both artifacts
4. every latest rendered page or slide is inspected at full size
5. no unresolved layout, glyph, figure, privacy, or cross-file defect remains
6. logs, reports, and the release decision are recorded without overwriting raw evidence
