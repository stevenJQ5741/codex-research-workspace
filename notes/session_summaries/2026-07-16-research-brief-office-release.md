# 2026-07-16 - Research Brief and Native Office Release Skills

## Outcome

Promoted the validated project pilot into two canonical Skills and prepared the repository for cross-computer installation.

## Changes

- Added `research-brief-editor` for evidence, claims, audience-centered narrative, source-figure provenance, and authoritative DOCX/PPTX generation.
- Added `office-native-release` for Word/PowerPoint native PDF export, Office/PDF pair QA, Poppler rendering, and mandatory full-size visual inspection.
- Narrowed `artifact-qa` so final native Office pair release routes to `office-native-release`.
- Updated `ask-jiang`, `AGENTS.md`, `README.md`, `PLANS.md`, the decision log, and ADR 0003.
- Enabled implicit invocation for both canonical Skills.

## Validation

- 16/16 Skills passed the official validator.
- 16/16 Skills contain Completion criterion text and implicit-invocation metadata.
- PowerShell and Python scripts passed syntax parsing.
- Word and PowerPoint pair QA passed using previously native-exported PDFs.
- The central runner produced page images identical by SHA-256 to the full-size images already inspected.
- The installer copied 16/16 Skills with source/install SHA-256 parity.

## Remaining operational step

Push the current branch after GitHub CLI authentication, then run `git pull` and `scripts/install_skills.ps1` on each additional computer.
