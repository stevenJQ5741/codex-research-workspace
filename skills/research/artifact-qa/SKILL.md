---
name: artifact-qa
description: Verify figures, tables, spreadsheets, DOCX, and PDF artifacts structurally, numerically, and visually after generation or revision. Use when layout, labels, formulas, rendering, numbering, or cross-file consistency can fail; use office-native-release instead for a declared final Word/PowerPoint and PDF pair on Windows.
---

# Artifact QA

## Procedure

1. Identify the exact candidate artifact, authoritative sources, expected format,
   and selected validation scope. Do not guess from a `final` filename.
2. Check file readability, required structure, references, numbering,
   placeholders, and expected objects.
3. Compare values, units, signs, formulas, axes, captions, and labels with
   authoritative machine-readable outputs or source tables.
4. Render the artifact and inspect every page or a justified bounded set for
   clipping, overlap, blank pages, font substitution, image quality, caption
   placement, and overflow. Use overview images for triage only and inspect the
   affected artifact at final size; follow a format-specific Skill when it
   defines narrower local-detail views.
5. Check that figures and tables remain legible and evidence-safe at final size.
   Prefer structural, numerical, or geometry checks over repeated image review
   when they prove the same invariant more directly.
6. Correct material defects and repeat all invalidated checks.
7. Hand a declared final native DOCX/PPTX and PDF pair to
   `office-native-release`.

## Stop conditions

Stop when the candidate identity is ambiguous, the source comparison is missing,
the renderer fails, numerical disagreement is unexplained, visual inspection has
not occurred after the latest material change, or final native Office release is
required.

## Completion criterion

This skill is complete when:

1. candidate, sources, and validation scope are explicit
2. structural and numerical checks pass
3. rendered output is visually inspected at a scale appropriate to the defect
4. figures and tables are defensible at final size
5. placeholders and unresolved defects are explicit
6. corrected artifacts are rechecked
