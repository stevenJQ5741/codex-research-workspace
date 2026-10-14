# Scientific theory grounding — field evaluation (B final acceptance candidate)

## Purpose

Determine whether preflight improves scientific inference without unnecessary triggering or large overhead. Use identical prompts, source files and context for **before versus after** runs; this initial package contains **structural unit tests**, not live-agent success rates.

## Pilot protocol

1. On an isolated research-project checkout, run a matched baseline without the global preflight rule, then the same task with the B pilot. Do not allow the first run's generated answers to leak into the second run's prompt context.
2. Use `tests/real_task_cases.json` as positive/negative routing scenarios; supplement with real project tasks reflecting natural-fiber interface load transfer, PALF/PBS three-phase heat transfer and DSC interpretation. Include mixed text editing and recalculation, English matrix substitution with an unlisted polymer, wet-heat cycling, morphology-based failure attribution, stale `current_scope`, valid/expired Theory Context review and bounded language tasks.
3. A scientific domain expert records: was preflight triggered; were critical theories identified; were decisive assumptions checked; did it catch fabricated/unjustified mechanisms; were original sources or exact evidence gaps disclosed; did it disrupt a routine task?
4. For S2, record a compact review receipt: selected cards, card hashes, task assumptions, actual sources opened, applicability status and any unresolved condition. Do not mark a scientific task "passed" merely for a keyword match.
5. Compare scientific quality (theory coverage and misapplication rate) and operating cost (tokens, latency, false triggering). Retain failing cases in the test suite and revise routing/knowledge cards separately.

## Suggested result fields

`case_id`, `pilot_version`, `baseline_or_pilot`, `trigger_expected`, `trigger_observed`, `context_reused_or_invalidated`, `required_theory_ids`, `theory_ids_observed`, `source_passages_actually_checked`, `g2_applicability_correct`, `scientific_overclaim_found`, `unnecessary_preflight`, `latency_seconds`, `reviewer_notes`.

The deterministic 22-prompt `tests/real_task_cases.json` file and the 18-case
multilingual semantic set in `tests/test_semantic_intent.py` are routing fixtures, not a completed field
evaluation. For each actual project task, retain the input scope and evidence
references, the returned tier and reason, all indexed matches or coverage gaps,
the scientific reviewer's applicability judgment, and any false trigger or miss.
Mark source and applicability fields **not checked** until the original material
has been inspected. Do not infer live implicit Skill activation from CLI tests.

## Promotion gates

- Candidate cards can be promoted only with original source passage inspection and human sign-off.
- A synthetic context in a unit test proves the validator's behavior, not a real scientific review.
- S1 may be accepted only when its scoped context was actually reviewed and its selected identities still match. S0 must avoid the library entirely.
- Dynamic skill activation in an independent project is separately tested; the deterministic `theory_preflight.py` CLI cannot prove a Codex agent will read it.
- In the fixed high-risk set, any S0/S1 route is a release blocker. A correct route alone does not prove model applicability or scientific source validity. Outside fixed cases, report uncertainty and obtain scientific review before consequential claims.

## Controlled real-task trial (pending human review)

Select consented, de-identified examples from natural-fiber interface load transfer, PALF/PBS three-phase heat transfer, DSC thermal-transition interpretation, manuscript mechanism claims, Japanese email and ordinary document editing. For each prompt, have a scientific reviewer label requested actions and changed scope **before** viewing the router output. Codex then prepares the structured intent file, and the deterministic script returns S0/S1/S2. Compare expected and observed tier, especially dangerous S0/S1 misses. For S1, inspect the actual current evidence references and selected card hashes; for S2, open original source passages and complete G1–G5. Log false triggers, missed triggers, missing index coverage and latency. A second reviewer adjudicates disagreements. Do not treat these fixture tests as this field trial.

For each prompt, record schema 1.1 instruction/content segments and whether
their boundaries were clear. Include unquoted passages containing scientific
verbs and a paired prompt that asks for scientific judgment after the passage.
Audit the segment labels themselves; a syntactically valid span does not prove
that Codex understood the user's intended actions.

Use 30 actual task prompts, with at least 15 independently labeled as requiring
S2. Include exact paired translation-versus-analysis requests, changed
materials/boundaries/evidence, and a referenced index record whose source or
limitation changed while its Markdown card did not. Require zero S0/S1 routes
among the pre-labeled high-risk prompts. Report ordinary-task false triggers,
latency and knowledge-library reads separately. Verify that Codex itself
generates the structured intent file and invokes the router; CLI fixtures do
not establish that live workflow. Defer automatic activation until the trial
and existing-Skill discovery checks pass.
- If a critical assumption fails, strong scientific inference must not proceed as fact. It remains permissible to discuss hypothetical mechanisms with testable consequences.
