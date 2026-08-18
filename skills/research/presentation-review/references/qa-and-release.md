# Validation Profiles and Native Release

## Contents

1. Validation objective
2. Profile selection
3. Change-driven invalidation
4. Audit commands
5. Visual-scale contract
6. Presentation invariants
7. Reading the report
8. Stop rules
9. Native release boundary

## 1. Validation objective

Prove the requested change with the smallest sufficient check set. Do not run full-deck rendering, native Office export, literature review, note analysis, and chart verification after every small edit.

The audit script is project-independent and uses only Python standard-library access to local PPTX packages. For native Google Slides, complete review or editing through the Slides workflow and export a fixed PPTX snapshot before using these profiles. Only `release-candidate` requires Windows, Microsoft PowerPoint, and `$office-native-release`.

Always preserve:

- authoritative baseline path and SHA-256
- candidate path and SHA-256
- mutation lane and authorized slides
- expected shared-object or package-part changes
- audit report and unresolved failures

Reuse earlier evidence only when the current report identifies it as reusable for the exact recorded hashes.

## 2. Profile selection

| Profile | Select when | Baseline | Visual scope | Native Office now |
| --- | --- | --- | --- | --- |
| `inventory` | selecting or freezing a candidate | optional | none | no |
| `aesthetic-round` | layout, hierarchy, spacing, crop, or typography changes on bounded slides | required | reported impacted slides | no |
| `controlled-revision` | visible text, charts, media, notes, or mixed targeted revisions | required | reported impacted slides | no |
| `notes-only` | direct OOXML speaker-note changes with visible slides protected | required | none | no |
| `release-candidate` | final distributable PPTX/PDF pair | optional for audit; protected hashes required in release spec | every slide | yes |

Use `custom` only for backward-compatible or unusual checks whose scope is explicitly described.

### Profile escalation

Escalate only when the mutation changes:

- `inventory` to the lane that will actually edit the deck
- `aesthetic-round` to `controlled-revision` when visible wording, charts, media, notes, or shared objects change
- any intermediate profile to `release-candidate` only when the user or workflow declares a final distributable candidate

Do not escalate merely because an intermediate audit succeeds.

## 3. Change-driven invalidation

| Detected change | Re-run | Reuse when unchanged |
| --- | --- | --- |
| visible text | scientific and semantic review; note alignment for those slides | chart, media, and unaffected-slide review |
| geometry or slide XML with identical text | visual review for impacted slides | visible-text semantics and notes |
| speaker notes only | note language, alignment, pronunciation, and timing | visible-slide semantics, charts, media, and prior visual review |
| chart XML or embedded workbook | data values, editability, axes, labels, and every slide referencing the chart | unrelated media and slides |
| media | provenance, resolution, crop, and every slide referencing the media | unrelated charts and slides |
| theme, layout, master, presentation, or table style | full-deck visual review | scientific data only when visible content remains unchanged |
| normal PowerPoint metadata | protected hash identity | content and visual evidence if no other part changed |
| unexplained package part | all potentially affected evidence | nothing until explained |

Any candidate hash change invalidates the previous protected release identity. Intermediate evidence may still be reusable, but the final release must be tied to the exact release-candidate hash.

The audit follows slide relationships so a shared chart or image can expand the impacted-slide list beyond the slides edited directly.

## 4. Audit commands

Run from the Skill directory or use an absolute script path.

### Inventory

```powershell
python scripts/audit_pptx_revision.py candidate.pptx `
  --profile inventory `
  --output _work/inventory.json `
  --expected-slides 23
```

This performs no baseline diff, rendering, or Office export.

### Bounded aesthetic round

```powershell
python scripts/audit_pptx_revision.py candidate.pptx `
  --baseline baseline.pptx `
  --profile aesthetic-round `
  --allowed-slide-changes 14 `
  --output _work/aesthetic_round.json `
  --expected-slides 23
```

Render only `validation_plan.render_slides`. Normal PowerPoint metadata drift is ignored in this profile unless `--strict-metadata` is supplied.

If a new image was intentionally added, authorize its package family explicitly:

```powershell
  --allow-changed-prefix ppt/media/
```

Do not authorize chart, media, embedding, theme, or note prefixes unless they are part of the approved mutation lane.

### Controlled revision

```powershell
python scripts/audit_pptx_revision.py candidate.pptx `
  --baseline baseline.pptx `
  --profile controlled-revision `
  --allowed-slide-changes 9-14,18-20,22-24 `
  --allow-changed-prefix ppt/charts/ `
  --allow-changed-prefix ppt/embeddings/ `
  --allow-changed-prefix ppt/media/ `
  --allow-changed-prefix ppt/notesSlides/ `
  --output _work/controlled_revision.json `
  --expected-slides 24
```

Authorize the narrowest expected range. If the first audit reports shared-object dependencies outside the planned slides, stop and confirm whether those indirect changes are legitimate before expanding scope.

### Notes only

```powershell
python scripts/audit_pptx_revision.py candidate.pptx `
  --baseline baseline.pptx `
  --profile notes-only `
  --output _work/notes_only.json `
  --expected-slides 23 `
  --notes-required 1-14,16-23 `
  --max-note-average 10 `
  --max-note-sentence 18 `
  --forbid-notes deterministic
```

This profile automatically:

- requires identical structure
- permits only `ppt/notesSlides/`
- requires unchanged visible text
- requires zero visual-slide impact
- sets visual inspection to false

If creating notes requires slide relationships or other visible package parts to change, use `controlled-revision` instead.

### Release-candidate preflight

```powershell
python scripts/audit_pptx_revision.py candidate.pptx `
  --profile release-candidate `
  --output _work/release_preflight.json `
  --expected-slides 23 `
  --require-text "Thank you for your attention" `
  --forbid-text "internal only"
```

A passing preflight does not release the file. Continue with `$office-native-release`.

### Presentation invariant audit

Use a task-specific JSON spec only when the requested change can invalidate
numbering, repeated page chrome, Office Math, forbidden visible text, or image
resolution. Keep project filenames, coordinates, slide counts, and thresholds in
the task spec rather than the reusable Skill.

```powershell
python scripts/audit_pptx_invariants.py candidate.pptx `
  --spec work/pptx_validation_spec.json `
  --output work/pptx_invariants.json
```

This audit complements `audit_pptx_revision.py`: the revision audit proves what
changed, while the invariant audit proves whether the resulting object state
meets the declared contract.

## 5. Visual-scale contract

Use the smallest view that can prove the question:

| View | Use | Must not prove |
| --- | --- | --- |
| overview or montage | story order, rhythm, density, obvious outliers | crop completeness, small text, equation spacing, page-chrome uniformity |
| full-size slide | layout, legibility, overlap, figure-to-text balance | exact object identity, editability, or cross-slide geometry |
| local ROI | school logo; equation region; chart axes, ticks, or legends | unrelated slide regions or aesthetic approval |
| package or geometry audit | sequence, object type, Office Math, repeated geometry, protected scope | semantic crop completeness or user taste |

Token-aware planning rules:

1. Build one overview for the bounded review scope, not one per retry.
2. Inspect full-size renders only for changed, dependent, or explicitly protected
   slides whose state must be reconfirmed.
3. Generate an ROI only when one of the three permitted regions changed, failed
   an invariant, or remains unreadable at full size.
4. Reuse prior visual evidence only for an exact recorded hash and only when the
   audit marks it reusable.
5. Prefer numeric geometry, object-type, sequence, and hash checks over repeated
   image inspection when they answer the question directly.

Semantic crop completeness cannot be certified from package geometry alone. A
changed chart crop still requires a full-size view and, when its axes, ticks, or
legend are at risk, the permitted chart ROI.

## 6. Presentation invariants

Declare only invariants that the task actually requires. Common checks include:

- exactly one page number per slide with a complete `1/N` through `N/N` sequence
- identical page-number geometry within a configurable point tolerance
- exactly one selected school-logo object per slide and identical declared
  geometry; relative enlargement of several pre-existing size systems is not
  unification
- minimum total or per-slide Office Math counts for equation-bearing slides
- forbidden visible-text patterns such as a language that must not remain
- image effective-resolution warnings at the displayed size
- warnings for exact duplicate text placed at nearly identical geometry

Repeated objects should be selected by semantic name, description, or stable
task-specific selectors. Positional heuristics are a fallback and must be narrow
enough to avoid selecting unrelated figures.

Use these honest status labels:

- `structural checks passed`
- `objective visual QA passed; aesthetic review pending`
- `user-approved baseline`
- `release candidate`
- `native Office release passed`

Do not claim `unified`, `final`, or `matches the user's style` from an overview,
package audit, or renderer success alone.

## 7. Reading the report

Read these fields first:

- `profile`: selected validation contract
- `candidate` and `baseline`: exact paths, hashes, and structure
- `authorized_scope`: allowed slides and package prefixes
- `change_summary.direct_slide_changes`: directly changed slide XML or relationships
- `change_summary.dependent_object_slides`: slides affected through shared charts or media
- `change_summary.visual_impacted_slides`: minimum render scope
- `validation_reuse.reusable`: checks that may be carried forward
- `validation_reuse.invalidated`: checks that must be repeated
- `validation_plan.next_steps`: next workflow actions
- `checks` and `all_checks_pass`: deterministic decision

Treat `all_checks_pass: false` or a nonzero exit code as a stop.

## 8. Stop rules

- Do not expand allowed slides or prefixes merely to obtain a pass.
- Investigate every unexpected added, removed, or changed package part.
- Do not reuse a report when either recorded hash no longer matches.
- Do not render the full deck when `render_slides` is a bounded list.
- Do not skip dependent slides that reference a changed shared object.
- Do not run native Office release for `inventory`, `aesthetic-round`, `controlled-revision`, or `notes-only`.
- Do not claim aesthetic acceptance from objective visual QA.
- Do not use an overview as evidence for crop completeness, formula-region
  legibility, or repeated-object uniformity.
- Do not expand ROI generation beyond the school logo, equation regions, and
  chart axes, ticks, or legends.
- Record justified exceptions with the exact part, slide, reason, and approver.

## 9. Native release boundary

Use `$office-native-release` only for `release-candidate`.

Require:

- authoritative PPTX and target PDF
- UTF-8 release spec
- protected hashes and expected structure
- required and forbidden wording
- fresh native render directory
- native PowerPoint export
- PPTX/PDF structural and semantic pair QA
- every-slide full-size visual inspection
- explicit aesthetic status

LibreOffice remains diagnostic only. A passing revision audit never replaces native release.

Preserve the source, PDF, spec, logs, reports, render manifest, montage, full-size slide images, and release decision. Do not overwrite failed evidence.
