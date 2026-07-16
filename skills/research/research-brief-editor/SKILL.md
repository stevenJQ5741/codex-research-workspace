---
name: research-brief-editor
description: Plan and revise evidence-grounded academic profiles, brief CVs, research summaries, publisher-meeting briefs, and conference introductions. Use when Codex must distill dissertations or papers, calibrate scientific claims, preserve an approved visual baseline, select traceable source figures, and produce an authoritative DOCX or PPTX source. Do not use for generic Office conversion, release rendering, full manuscripts, or slide-deck storytelling; use office-native-release for final export and QA.
---

# Research Brief Editor

Produce an audience-centered, evidence-safe Office source artifact. Keep renderer and release mechanics outside this Skill.

## 1. Define the editorial contract

Record:

- audience, meeting purpose, language, and decision need
- required page or slide budget and approved baseline
- immutable source files and baseline SHA-256 hashes
- required sections, figures, numerical claims, disclaimers, and privacy exclusions
- authoritative DOCX or PPTX output name

Inspect the baseline before editing. Preserve stable pages, slides, geometry, reading order, palette, and typography unless the request changes them.

## 2. Establish the claim-evidence ledger

For each consequential claim, record the source file, page or figure, evidence type, permitted wording, and limitation. Distinguish:

- experimental result
- calculation
- model-derived quantity
- interpretation
- proposal or future direction

State studied systems and validation ranges with quantitative claims. Do not convert correlation into causation or a modeled quantity into a direct measurement. Use optimization language when performance depends on balanced mechanisms. Keep unconfirmed book directions or future plans explicitly provisional.

Do not finalize prose until every headline claim is covered by the ledger.

## 3. Build the audience-centered narrative

Organize around the audience's decision need instead of automatically following dissertation chronology. Prefer one positioning sentence followed by three or four linked themes:

1. measurement or method
2. mechanism or model
3. validation or quantification
4. application or design implication

Keep CV facts separate from research interpretation. Place evidence boundaries near the associated claim. Remove side topics that do not support the meeting purpose.

## 4. Preserve source and visual provenance

- Work from a copy; never overwrite evidence or the baseline.
- Prefer direct source crops for scientific figures.
- Preserve complete axes, end ticks, legends, labels, symbols, and aspect ratio.
- Record source page, figure identifier, crop coordinates, and permitted caption wording in code or the ledger.
- Reuse source-derived styles and builder helpers instead of repeated manual formatting.
- Keep internal traceability notes in the working artifact until the clean external source is generated.

## 5. Produce one authoritative Office source

Maintain one canonical builder after requirements stabilize. Generate the clean external DOCX or PPTX from the traceable working version; do not create or patch a PDF independently.

Before release, verify that the Office source contains all required claims and critical glyphs, excludes private or internal-only text, and matches the ledger. Then explicitly invoke `$office-native-release` with the authoritative source and release spec.

## Completion criterion

This skill is complete when:

1. the editorial contract and immutable source hashes are recorded
2. every consequential claim has evidence, type, permitted wording, and limitation
3. the narrative is audience-centered and excludes unrelated material
4. figures and captions remain traceable to authoritative sources
5. one clean authoritative DOCX or PPTX is produced reproducibly
6. release responsibility is handed to `office-native-release` without an independently edited PDF
