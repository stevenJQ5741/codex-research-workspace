---
name: presentation-review
description: Review or revise academic presentations for narrative, evidence representation, audience fit, language, visual consistency, user-guided aesthetic calibration, notes, editability, and deterministic PPTX change control. Use for PowerPoint or exported Google Slides work before final release; delegate a declared final native PowerPoint and PDF pair to office-native-release.
---

# Presentation Review

## Procedure

1. Load only the needed reference:
   - [aesthetic-collaboration.md](references/aesthetic-collaboration.md) for visual
     style or user feedback
   - [style-and-language.md](references/style-and-language.md) for narrative,
     evidence form, visible wording, or notes
   - [qa-and-release.md](references/qa-and-release.md) for validation profiles and
     the native-release boundary
2. Select one authorized mode: `review-only`, `controlled-revision`,
   `aesthetic-calibration`, or `release-handoff`. A review request does not
   authorize file revision.
3. Freeze the authoritative source, SHA-256, output path, audience, talk time,
   protected slides and objects, mutation lane, exclusions, and validation
   profile. Export native Google Slides to a fixed PPTX snapshot before package
   comparison.
4. Label consequential slide claims as observation, calculation, model,
   literature, interpretation, assumption, or proposal. Stop on untraceable
   high-impact claims.
5. Check the deck story and one dominant takeaway per slide; choose evidence form
   before layout.
6. For aesthetic work, change one visual dimension or one to three representative
   slides per round, preserve manual edits as the next baseline, and record
   accepted, rejected, and pending preferences.
7. Use the least invasive mutation method and preserve editable charts, tables,
   media, equations, and notes unless the request authorizes conversion.
8. Keep visible language concise and notes natural, aligned, and evidence-safe.
9. Run `scripts/audit_pptx_revision.py` with the smallest profile that proves the
   mutation: `inventory`, `aesthetic-round`, `controlled-revision`, or
   `notes-only`. Explain every changed package part and re-run invalidated checks.
10. For an explicitly declared final PPTX/PDF release candidate, complete the
    package preflight and hand the exact PPTX, hashes, release spec, and remaining
    status to `office-native-release`; do not duplicate native export or pair QA.
11. Report authoritative input and output, hashes, changed and protected scope,
    validation results, aesthetic status, risks, and next action.

## Stop conditions

Stop when source identity is ambiguous, revision is unauthorized, a high-impact
claim lacks evidence, a package change exceeds the mutation lane, the baseline
hash changes unexpectedly, user aesthetic approval is still pending but release
is claimed, or native release is required but not delegated.

## Completion criterion

This skill is complete when:

1. mode, authoritative source, scope, exclusions, and validation profile are explicit
2. review findings or authorized revisions are evidence-calibrated
3. the latest user-approved source and editable content are preserved as required
4. every package change is explained and invalidated checks are rerun
5. affected slides or notes are inspected for the selected profile
6. aesthetic status is user-approved or explicitly pending
7. a final native release is handed to `office-native-release` with exact identity
