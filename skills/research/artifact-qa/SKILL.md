---
name: artifact-qa
description: Verify research figures, tables, spreadsheets, DOCX, and PDF artifacts structurally, numerically, and visually before release. Use automatically after generating or revising files when rendering, pagination, labels, image quality, numbering, formulas, or cross-file consistency can fail. For final native Word/PowerPoint-to-PDF pair release on Windows, use office-native-release instead.
---

# Artifact QA

## Process

### 1. Define the release candidate

Identify the exact files and expected format. Do not review an obsolete version by filename guess.

### 2. Run structural checks

Check that files open, required sections exist, tables and figures are present, numbering is continuous, links or references resolve, and placeholders are intentional.

### 3. Run numerical checks

Compare displayed values, units, signs, axis data, captions, and formulas with authoritative machine-readable outputs or source tables.

### 4. Render and inspect

Render DOCX or PDF pages and inspect all pages or a justified representative set. Check clipping, overlap, blank pages, font substitution, image resolution, caption placement, table overflow, and page balance.

For final Windows-native DOCX/PPTX-to-PDF pair release, hand off to `office-native-release` rather than duplicating native export, pair consistency, and glyph-survival checks.

### 5. Inspect figure communication

Check legibility at final size, color and grayscale distinction, experimental-point conventions, fit-range limits, uncertainty depiction, and whether the visual implies more evidence than exists.

### 6. Correct and re-render

After material corrections, repeat affected checks. Do not claim visual completion from source-code inspection alone.

## Completion criterion

This skill is complete when:

1. the exact release candidate is identified
2. structural and numerical checks pass
3. rendered output has been visually inspected
4. figures and tables remain defensible at final size
5. placeholders and unresolved visual defects are explicit
6. corrected artifacts are rechecked
7. the response includes a Skill usage receipt
