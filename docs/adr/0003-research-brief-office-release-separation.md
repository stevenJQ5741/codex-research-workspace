# 0003 - Separate Research Brief Editing from Native Office Release

## Status

Accepted

## Context

A project-level research-brief workflow combined claim calibration, figure provenance, DOCX/PPTX construction, native Office export, structural pair checks, and visual release review in one Skill. The combined workflow loaded device-specific release mechanics during editorial work and overlapped with general artifact QA.

LibreOffice has also been unreliable on the primary Windows workstation, while Word and PowerPoint native export preserved critical glyphs in the validated samples.

## Decision

1. Keep `research-brief-editor` responsible for evidence, claims, audience-centered narrative, visual provenance, and one authoritative DOCX or PPTX source.
2. Keep `office-native-release` responsible for native Word/PowerPoint PDF export, Office/PDF pair QA, Poppler rendering, and page-by-page or slide-by-slide visual inspection.
3. Keep `artifact-qa` responsible for general research artifact verification and route final native Office pair releases to `office-native-release`.
4. Treat LibreOffice as an optional diagnostic renderer on devices where it is unreliable; do not use it as an automatic release fallback.
5. Install both Skills from this repository so every computer receives the same canonical workflow after `git pull` and `scripts/install_skills.ps1`.

## Validation evidence

On the primary Windows workstation:

- both Skills passed the official Skill validator
- Word 16.0 exported and passed pair QA for a three-page DOCX/PDF sample
- PowerPoint 16.0 exported and passed pair QA for a one-slide PPTX/PDF sample
- critical strings including Greek symbols and subscripts survived native export
- a negative critical-glyph test failed as expected
- all four rendered pages/slides were visually inspected at full size

## Consequences

- Editorial tasks load fewer release-specific instructions.
- Native release checks become reusable outside the original project.
- Automatic invocation descriptions must keep `office-native-release` and `artifact-qa` mutually distinguishable.
- Visual inspection remains a human release gate; the runner deliberately reports it as pending.
- Future discomfort or routing errors should be corrected from real usage evidence without recreating parallel version trees.
