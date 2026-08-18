# User-Guided Aesthetic Collaboration

## Principle

Treat aesthetic quality as a user-led calibration problem. Codex can detect objective defects, produce bounded alternatives, and learn from repeated feedback, but it cannot infer the user's taste reliably from generic design rules or certify that a deck feels right.

Expect the collaboration to continue across many revisions. Do not pressure the user to finalize the aesthetic model, and do not interpret repeated manual correction as workflow failure. Each correction is evidence for the next round.

## Separate two review classes

### Objective visual QA

Codex may decide whether the slide has:

- clipping, overlap, or broken alignment
- unreadable text, labels, citations, or legends
- inconsistent page chrome or accidental formatting drift
- low-resolution, distorted, or misleading images
- missing units, truncated axes, or broken glyphs

These checks may block technical release.

### Subjective aesthetic review

Defer to the user on:

- visual hierarchy and where the eye should go first
- density, whitespace, and the amount of explanation shown
- typography character, weight, and rhythm
- color balance and emphasis strength
- figure scale, crop, placement, and page composition
- whether the slide resembles the user's own presentation style
- whether a technically consistent layout still feels awkward

Do not convert a subjective preference into an objective defect without evidence.

## Iteration protocol

### 1. Define a bounded round

Choose one visual dimension or one to three representative slides. Examples include title hierarchy, figure-to-text balance, conclusion layout, chart annotation, or backup-slide density.

Avoid deck-wide restyling until a representative pattern has been accepted.

### 2. Preserve the baseline

Hash the latest user-approved PPTX and create a new output. If the user manually edits the candidate, preserve that file unchanged and make it the next baseline.

### 3. Offer limited alternatives

Provide one recommended revision and, only when the trade-off is meaningful, one contrasting alternative. State the difference in plain language, such as:

- more compact versus more explanatory
- stronger figure dominance versus stronger textual guidance
- restrained emphasis versus stronger conclusion emphasis

Do not generate a large gallery that transfers design work back to the user.

### 4. Make comparison easy

Provide before/after slide renders or a small comparison montage. Keep slide size
and rendering conditions consistent. Treat a montage as narrative and rhythm
evidence only; it cannot prove crop completeness, small-text legibility, equation
spacing, or repeated-object alignment.

Inspect affected slides at full size. Generate a local ROI view only when the
changed or uncertain region is one of:

- the school logo
- an equation region
- chart axes, ticks, or legends

Do not generate ROIs for unchanged regions or as a substitute for full-slide
review. Prefer a deterministic geometry or package check when the question is
object identity, sequence, editability, or cross-slide consistency.

Run the `aesthetic-round` validation profile and render only the slides listed in `validation_plan.render_slides`. If a shared chart, media object, theme, layout, or master expands the reported scope, review every reported dependent slide. Do not run full native Office release during an aesthetic round.

### 5. Capture manual feedback as evidence

Record:

- slide number and archetype
- what Codex changed
- what the user accepted or rejected
- what the user changed manually
- the likely preference being expressed
- confidence: one-off, emerging, or stable
- context limits such as language, audience, and slide type

Describe observed actions before inferring a general preference.

### 6. Promote rules conservatively

Promote an aesthetic preference to the stable style baseline only when:

- the user explicitly states it as a general rule, or
- the same preference is accepted repeatedly in comparable contexts

Keep isolated choices in the task ledger. A conclusion-slide preference may not apply to a methods slide, and an English conference preference may not apply to a Japanese lecture.

### 7. Close the round honestly

Use one of these states:

- `objective visual QA passed; aesthetic review pending`
- `user accepted this slide pattern; deck-wide propagation pending`
- `user approved aesthetics for release`

Never use `polished`, `final design`, or `matches the user's style` solely because automatic checks passed.

## Efficiency rules for a long collaboration

- Reuse accepted slide archetypes instead of redesigning every page.
- Propagate only confirmed patterns and keep each propagation reversible.
- Batch mechanically equivalent changes after the representative slide is approved.
- Use the overview once per bounded round, full-size renders only for impacted
  slides, and ROIs only for the three permitted high-risk regions.
- Use `inventory` once per authoritative baseline and `aesthetic-round` for each bounded visual iteration.
- Reuse semantic, chart, media, note, and visual evidence only when the audit report marks it reusable for the recorded hashes.
- Keep a compact accepted/rejected decision ledger rather than rereading the full conversation.
- Compare new manual edits with the previous candidate before making the next revision.
- Stop changing a slide that the user has accepted unless new content makes the layout invalid.

## Completion criterion for an aesthetic round

An aesthetic round is complete when:

1. its scope and baseline are explicit
2. objective defects are separated from subjective choices
3. the user can compare the revision with the prior state
4. accepted, rejected, and manual changes are recorded
5. the next baseline and any stable-rule promotion are identified
6. the status is honestly labeled as approved or pending
