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
   profile. A user-edited candidate becomes the next baseline and must not be
   silently replaced by an older file. Export native Google Slides to a fixed
   PPTX snapshot before package comparison.
4. Before bulk authoring, map each planned slide to its message, evidence,
   consequential claim label, figure or equation provenance, and review risk.
   Stop on untraceable high-impact claims or formulas without a defensible source.
5. Check the deck story and one dominant takeaway per slide; choose evidence form
   before layout. For aesthetic work, change one visual dimension or one to three
   representative slide archetypes per round, then propagate only an accepted
   pattern.
6. Use the least invasive mutation method and preserve editable charts, tables,
   media, Office Math equations, and notes unless conversion is authorized. Give
   repeated objects semantic names or stable selectors instead of identifying
   them only by approximate position.
7. Keep visible language concise and notes natural, aligned, and evidence-safe.
8. Run `scripts/audit_pptx_revision.py` with the smallest profile that proves the
   mutation. When numbering, repeated page chrome, Office Math, language, or
   image resolution can fail, also run `scripts/audit_pptx_invariants.py` with a
   task-specific spec.
9. Apply the visual-scale contract in `references/qa-and-release.md`: overview
   images assess narrative only; inspect affected slides at full size; create
   local ROI views only for the school logo, equation regions, and chart axes,
   ticks, or legends when those regions changed or remain uncertain.
10. Report status precisely. Objective checks do not establish user aesthetic
   approval, and no deck is `unified`, `final`, or `release-ready` while a named
   invariant or required visual review remains incomplete.
11. For an explicitly declared final PPTX/PDF release candidate, complete the
   package preflight and hand the exact PPTX, hashes, release spec, and remaining
   status to `office-native-release`; do not duplicate native export or pair QA.
12. Report authoritative input and output, hashes, changed and protected scope,
   validation results, aesthetic status, risks, and next action.

## Stop conditions

Stop when source identity is ambiguous, revision is unauthorized, a high-impact
claim lacks evidence, a package change exceeds the mutation lane, the baseline
hash changes unexpectedly, user aesthetic approval is still pending but release
is claimed, a required invariant or visual review is incomplete, or native
release is required but not delegated.

## Completion criterion

This skill is complete when:

1. mode, authoritative source, scope, exclusions, and validation profile are explicit
2. review findings or authorized revisions are evidence-calibrated
3. the latest user-approved source and editable content are preserved as required
4. slide evidence and formula provenance are traceable where consequential
5. every package change is explained and invalidated checks are rerun
6. required invariants pass and affected slides are inspected at the right scale
7. aesthetic status is user-approved or explicitly pending
8. a final native release is handed to `office-native-release` with exact identity
