---
name: presentation-review
description: Review, create, or revise academic presentations for narrative, evidence representation, audience fit, language, visual consistency, and release safety. Use for PowerPoint, Google Slides, conference talks, proposal decks, slide-level review or revision, long-running user-guided aesthetic calibration, speaker-note alignment, simple oral English, preservation of editable charts and media, recovery after user edits, deterministic PPTX comparison, or final native PowerPoint release on Windows.
---

# Presentation Review and Revision

Review or produce defensible academic slides while preserving the latest user-authored source and proving what changed. Treat review, content, visible design, speaker notes, and release rendering as separate work lanes.

## Load only the needed references

- Read [aesthetic-collaboration.md](references/aesthetic-collaboration.md) whenever appearance, style, layout quality, visual polish, or manual user feedback is in scope.
- Read [style-and-language.md](references/style-and-language.md) when changing layout, visible wording, evidence form, or speaker notes.
- Read [qa-and-release.md](references/qa-and-release.md) when selecting a validation profile, interpreting invalidated evidence, or preparing a release candidate.

## Choose the operating mode

Select the smallest mode authorized by the request:

- `review-only`: inspect narrative, evidence, audience fit, language, notes, and visual consistency; report findings without changing files or external systems
- `controlled-revision`: create or modify an explicitly bounded deck while preserving the authoritative source and user edits
- `aesthetic-calibration`: revise one visual dimension or a small representative slide set with repeated manual user feedback
- `release`: prepare an explicitly declared final PPTX/PDF pair through native Microsoft PowerPoint

Do not infer permission to revise from a request to review. Escalate modes only when the user authorizes the additional mutation or release scope.

The deterministic audit operates on local PPTX packages. Review or edit native Google Slides through the connected Slides workflow, then export an exact PPTX snapshot before package comparison or release validation.

## Non-negotiable rules

1. Treat the latest user-approved PPTX as the source of truth. Do not rebuild from an older builder output after the user has edited a later file.
2. Never overwrite the input. Record its SHA-256 and create a new revision path.
3. Define the authorized mutation lane before editing: narrative, visible slide content, visual layout, data or charts, speaker notes, or release only.
4. When only notes are authorized, preserve every slide, chart, media, theme, and layout part exactly. Verify this at the OOXML-package level.
5. Keep experimental results, calculations, literature values, interpretations, possible causes, and proposals visibly distinct.
6. Preserve scientific meaning while simplifying language. Do not replace a precise technical term merely to satisfy a readability metric.
7. Keep charts and tables editable unless the user explicitly accepts rasterization.
8. Use the lightest validation profile that proves the current mutation lane. Require native Microsoft Office export and full-size inspection of every slide only for an explicitly declared release candidate.
9. Treat the user's aesthetic judgment and manual edits as authoritative training evidence. Automated scores, consistency checks, and Codex's visual review can identify defects, but cannot certify that a slide is aesthetically successful or matches the user's taste.
10. Preserve the original review capability: summarize the deck-level story, identify slide-level problems, propose concrete fixes, flag high-risk claims, and state the next revision action.

## Workflow

### 1. Freeze the presentation contract

Record:

- audience, venue, language, talk time, and required outcome
- authoritative input path, modification time, and SHA-256
- output paths and revision naming
- main-talk and backup-slide boundaries
- protected slides, objects, terminology, equations, and source assets
- exact mutation lane and explicitly excluded changes
- aesthetic review state, current feedback, accepted and rejected patterns, and the scope of the next visual round
- validation profile, authorized slide range, allowed package-part prefixes, and checks that may be reused
- required and forbidden wording
- validation thresholds and release renderer

If several candidates exist, compare modification times, slide counts, visible text, notes, and user instructions. Do not infer the source of truth from a filename such as `final` alone.

### 2. Audit claims before designing

For each main-slide message, label the support as experiment, calculation, model, literature, interpretation, assumption, or proposal. Calibrate verbs to the evidence.

- Use `shows` or `demonstrates` only for direct support.
- Use `supports`, `indicates`, or `suggests` for limited or indirect support.
- Use `may`, `possible cause`, or `proposed` for unvalidated mechanisms and future methods.
- State when several values are derived from one curve rather than independent measurements.
- Move exact values, sensitivity analyses, derivations, and defensive explanations to backup slides when they would overload the main story.

Stop and request evidence when a high-impact statement cannot be traced to a source, calculation, or labeled interpretation.

### 3. Build the narrative and evidence map

Define one dominant audience takeaway per slide. Prefer this short-talk spine when it fits the project:

1. motivation and practical problem
2. research gap or validation need
3. purpose and workflow
4. materials and method
5. method logic and equations
6. representative results
7. agreement and variation
8. failure modes or limitations
9. conclusions and next steps

Do not force every project into this order. Choose the evidence form before choosing the layout:

- chart for trend, comparison, or sensitivity
- table for exact values and test conditions
- photo for physical reality
- schematic for mechanism, geometry, or procedure
- equation when the calculation logic is part of the claim
- source figure only when its provenance and labels remain readable

### 4. Run user-guided aesthetic calibration

Treat aesthetic refinement as an empirical, long-running collaboration rather than a one-pass optimization task.

- Default to one visual dimension or one to three representative slides per round unless the user authorizes a broader pass.
- Separate objective defects such as clipping, overlap, illegible text, or broken alignment from subjective choices such as density, hierarchy, whitespace, color balance, image scale, and overall character.
- Present a before/after comparison or at most two clearly differentiated alternatives. Do not generate many weak variants.
- Invite and preserve manual user edits. When the user returns a modified PPTX, hash it and treat it as the new authoritative source.
- Record what the user accepted, rejected, or changed manually, together with the slide type and presentation context.
- Append that evidence to a workspace-specific aesthetic decision ledger. Default to `presentation_aesthetic_decision_ledger.md` unless the workspace declares another canonical path.
- Promote a preference into a stable style rule only after repeated acceptance across comparable slides or explicit user confirmation.
- Keep unresolved aesthetic questions visible. Use `aesthetic review pending` instead of claiming `polished`, `final`, or `user style matched`.

A revision round may end with aesthetic review pending. A deck must not be called aesthetically release-ready until the user explicitly approves it.

### 5. Select the smallest safe mutation method

Use the least invasive method that can produce the requested result.

- Use a controlled builder for a new deck or an explicitly authorized structural rebuild.
- Use targeted PowerPoint automation for a small set of slide objects while preserving editability.
- Use direct OOXML editing for speaker notes or another precisely bounded package part.
- Do not perform a full regeneration to make a notes-only or wording-only change.

Before execution, list the slides and package parts expected to change. After execution, compare this expectation with the actual diff.

### 6. Separate visible and spoken language

Treat the slide and the speech as two synchronized tracks.

- Keep visible English compact, defensible, and readable at presentation distance.
- Write notes as natural spoken sentences that explain the visual sequence; do not recite every label or table cell.
- Align notes to the latest visible slide, especially after user edits.
- In simple oral-English mode, target an average of at most 10 words per sentence and a maximum of 18 words per sentence unless technical accuracy requires an exception.
- Maintain a project-specific difficult-word list, but protect necessary terms, symbols, units, material names, and equations.
- Use transitions that tell the audience why the next slide is needed.

Do not treat sentence length as proof of clarity. Review meaning, rhythm, pronunciation burden, and alignment with the visual.

### 7. Implement with traceable provenance

Reuse approved figures, logos, equations, and source data. Record the source of every high-impact visual and derived number.

For charts and tables:

- verify values against the authoritative data or calculation
- show units and define statistics such as population or sample standard deviation
- keep axes, legends, labels, and annotations readable after native rendering
- preserve native chart editability when feasible
- avoid adding uncertainty marks or causal annotations that the data do not support

For each revision, produce a compact ledger containing the source hash, output path, modified slides, expected object changes, selected validation profile, invalidated evidence, reusable evidence, claims touched, and unresolved issues.

### 8. Run deterministic revision QA

Use `inventory`, `aesthetic-round`, `controlled-revision`, and `notes-only` across projects and operating systems with a local PPTX and Python standard library. Treat `release-candidate` as a Windows-native extension that additionally requires Microsoft PowerPoint and `$office-native-release`.

Select one profile before editing and keep it until the mutation scope changes:

| Profile | Use | Required validation |
| --- | --- | --- |
| `inventory` | identify and hash a candidate | structure and text inventory only |
| `aesthetic-round` | one visual dimension or a few slides | package scope plus affected-slide rendering |
| `controlled-revision` | content, chart, media, or mixed targeted edits | package scope plus only invalidated semantic, data, note, and visual checks |
| `notes-only` | direct speaker-note patch | exact visible-part preservation plus note language and timing; no slide rendering |
| `release-candidate` | final distributable PPTX/PDF | full native Office release and every-slide inspection |

Run `scripts/audit_pptx_revision.py` with the chosen `--profile`. Read:

- `change_summary` for direct and indirect slide impact
- `validation_reuse` for evidence that remains valid or became stale
- `validation_plan.render_slides` for the minimum visual-review scope
- `validation_plan.native_office_release_required_now` for the Office-release gate

Use `--allowed-slide-changes` for visible slide scope and repeated `--allow-changed-prefix` only for expected shared objects such as charts, embeddings, media, or notes. Do not broaden scope merely to make a failed audit pass.

See [qa-and-release.md](references/qa-and-release.md) for commands, the invalidation matrix, and stop rules.

### 9. Release through native Microsoft Office

Enter this step only after the file is explicitly designated a `release-candidate`. Use `$office-native-release` for the final PPTX/PDF pair on Windows.

1. Create a UTF-8 release spec with expected structure, required and forbidden wording, protected source hashes, and target PDF.
2. Export through Microsoft PowerPoint, not an automatic LibreOffice fallback.
3. Compare PPTX and PDF structure and semantic content.
4. Render every PDF page at 180 dpi or higher.
5. Review a montage for triage, then inspect every full-size slide after the latest material change.
6. Preserve failed artifacts, logs, specs, and renders for diagnosis.
7. Record aesthetic review as explicitly user-approved or still pending. Native rendering proves fidelity, not taste.

Check clipping, overlap, line wrapping, glyphs, equations, figure boundaries, axes, citations, page numbers, backup markers, notes alignment, and unintended internal text.

### 10. Hand off the authoritative result

Report:

- authoritative input and output paths with hashes
- what changed and what was intentionally preserved
- main and backup slide counts
- structural, language, pair-QA, and visual-QA results
- accepted, rejected, and still-pending aesthetic decisions
- remaining evidence, wording, timing, or design risks
- the exact next action if the deck is not release-ready

## Completion criterion

This skill is complete when:

1. the operating mode, authoritative source, authorized scope, and excluded actions are explicit
2. a `review-only` task summarizes the deck-level story, identifies the main slide-level problems, proposes concrete fixes, flags high-risk claims, and states the next revision action without mutating files
3. every consequential claim touched by a review or revision is traceable and evidence-calibrated
4. a revision protects the latest user-approved source by hash and changes visible slides, notes, charts, and media only as intended
5. the selected validation profile passes with no unexplained package changes, and every invalidated check is rerun while reusable evidence is tied to exact hashes
6. the profile-specific review is complete: affected slides for visual revisions, notes for a notes-only patch, or every slide for a release candidate
7. a release candidate on Windows is exported through native PowerPoint and its PPTX/PDF pair passes structural, semantic, and full-size visual QA; intermediate revisions and Google Slides without an exported PPTX snapshot are not mislabeled as released
8. aesthetic status is either explicitly user-approved or clearly marked `aesthetic review pending`; no automated metric or Codex judgment substitutes for user approval
9. raw sources and failed evidence are preserved, and the handoff identifies the authoritative output and remaining risks
