---
name: theory-grounding
description: Check theory applicability for scientific explanations, material or model changes, experiment plans, mechanisms, novelty claims and explicit theory requests. Reuse a reviewed Theory Context only after checking the current task. Skip bounded language and formatting work.
---

# Theory Grounding — B Final Acceptance Candidate

## Scope

This Skill performs the **theory stage** before consequential scientific inference. It retrieves candidates and checks their original sources, assumptions, applicability, alternatives and limitations. It is not a literature survey, data-analysis engine or final manuscript claim audit. A `candidate` card is never verified scientific evidence merely because it matched a query.

## Route before loading knowledge

1. **Codex first reads the entire user request as actions.** Separate the user's requested actions from scientific terms inside material being translated or edited. Identify all language transformations, scientific calculations, model choice/applicability, mechanism or causal explanation, experiment design, evidence appraisal and claim review. Assess material, model, process, boundary, parameter and evidence changes as `yes`, `no` or `unknown`. If any consequential action or change is unclear, record uncertainty; do not guess it is routine. Produce the structured intent contract below before calling the deterministic router.
2. The router checks the exact query hash and the structured assessment, then applies conservative action-level guards only to **instruction segments**, not the supplied text being translated or edited. Quotation marks are not required to identify supplied content. A broad `routine`, `analysis` or `manuscript` tag, or `--requires-theory no`, cannot suppress detected scientific risk. Mixed editing and recalculation are scientific tasks. If an intent is missing or invalid, only a clearly bounded transformation may fall back to S0; other tasks go to S2 with uncertainty reported. A pure-transform assessment with a new instruction after supplied content goes to S2 for review. The guard still cannot understand every language expression or correct every wrong agent assessment.
3. **S0:** routine email, translation, formatting, or clearly bounded non-inferential operations need no theory preflight. Do not open `docs/knowledge/`.
4. **S1:** reuse only after a documented Context review and a fresh comparison of this exact task with project/question, material, model assumptions, boundary conditions, parameters and contrary evidence. Record the current task's query hash, checker, time and evidence references in `current_scope.scope_review`; its check must be no older than 30 minutes at preflight. Set `evidence_checked=true` only after actually inspecting current evidence; the timestamp alone is insufficient. Check each selected card hash, its complete canonical `INDEX.json` record hash, and source-review state without a full candidate search. A missing, changed, conflicted or unreviewed context, or an unsubstantiated or expired scope check, routes a theory-dependent task to S2. A `candidate` may support a limited working hypothesis, never verified scientific authority. A high-impact claim with unchecked decisive source claims goes to S2.
5. **S2:** locate `docs/knowledge/INDEX.json` in the canonical checkout. `scripts/theory_preflight.py` provides deterministic candidates and an unreviewed applicability checklist. When checking original-source availability or review status, consult `docs/knowledge/evidence/README.md` for relevant review receipts; a receipt does not promote a candidate. The acting scientific reviewer completes G1-G5 below. No match means a coverage gap, never proof of novelty or absence of theory.

The CLI supports `--intent-file`, `--manual-trigger`, `--theory-context` and `--scope-file`. Use `--output` only when an output file was explicitly requested. If the canonical knowledge checkout is unavailable, report `knowledge_unavailable` and do not claim a completed audit.

## Structured intent contract (agent judgment, then deterministic validation)

Pass JSON with `schema_version: "1.1"` and `task_sha256` equal to SHA-256 of the exact UTF-8 `--query`. `task_segments` is a nonempty ordered list of `{ "kind": "instruction" | "content", "text": "..." }`. The texts must concatenate byte-for-byte to the exact query, the first segment must be an instruction, and no segment may be empty. Mark the user's requested operations as `instruction` and supplied passages to translate or edit as `content`, even without quotation marks. Include later requested operations as additional instruction segments. Set `segmentation_status` to `clear` only when those boundaries are clear; use `uncertain` otherwise, which routes to S2. Version 1.0 intent files lack this boundary and are rejected for safe reclassification. For example, `只翻译这段话：研究人员比较模型并解释实验结果` has instruction `只翻译这段话：` and content `研究人员比较模型并解释实验结果`.

`transform_actions` is a list from `translation`, `email`, `formatting`, `text_edit`, `plot_redraw`, `bounded_recalculation`. `science_actions` is a list from `bounded_analysis`, `bounded_writing`, `scientific_calculation`, `experiment_design`, `model_selection`, `model_applicability`, `mechanism_attribution`, `causal_inference`, `evidence_appraisal`, `claim_review`. Include both lists for mixed tasks. `changes` must specify all six dimensions `material`, `model`, `process`, `boundary`, `parameter`, `evidence` as `yes`, `no` or `unknown`. Set `theory_relevance` to `none`, `bounded`, `new_or_changed` or `uncertain`; `uncertainty` to `none`, `intent`, `scope` or `evidence`; `evidence_checked` and `high_impact_claim` are booleans. An attestation is not itself proof that evidence was inspected. Keep evidence references in `current_scope.scope_review` and the task record. Missing or contradictory facts mean `unknown`/uncertainty and S2. Do not fabricate a low-risk intent to avoid retrieval.

## S2 scientific check: G1-G5

1. **G1 Coverage:** identify baseline theories and plausible missing alternatives; broaden source search when the small index is insufficient.
2. **G2 Applicability:** compare material system, geometry, scale, loading, temperature/rate regime, boundaries, parameter definitions and failure modes with each candidate. Label each condition confirmed, assumed, missing, contradicted or not applicable.
3. **G3 Quantities:** distinguish measured, fitted, literature-derived and model-estimated parameters; check units, signs and definitions. Defer detailed numerical audit to `analysis-feedback-loop`.
4. **G4 Evidence:** inspect decisive original passages, equations and limitations; separate bibliographic checks from claim checks. Record competing explanations and contradictions. Do not promote a card by automated self-assertion.
5. **G5 Novelty/falsification:** a priority or mechanism claim needs a scoped literature search and plausible test that could refute it.

## Theory Context handoff

Use `docs/knowledge/THEORY_CONTEXT.schema.json` v0.2.2. Record only selected IDs, card hashes, canonical index-record hashes, source-review states, scoped assumptions, applicability decision, review basis and unresolved conditions; do not copy complete cards. Compute an index hash as SHA-256 over UTF-8 JSON of the entire selected record with sorted keys, `ensure_ascii=False`, compact separators and no NaN. `examples/theory_context_short_fiber_candidate.json` illustrates a **pending**, non-reusable case. Older Context records require fresh review before migration; adding a hash alone is not a scientific review. The script checks structure and identity; a human or responsible scientific process must verify the truth of review references and scientific applicability. Preserve candidate source status even if a task-level model review concludes `conditional`.

Invalidate a context when material/model/boundary conditions or parameter definitions change, a selected card or index-record hash or review state changes, or contradictory evidence appears. A new chat alone does not invalidate it.

## Staged Skill coordination

Keep at most one primary and two supporting Skills **in each stage**. `ask-jiang` routes the task; this preflight produces a compact Theory Context and then releases its working context. `research-grill` resolves consequential missing inputs. `analysis-feedback-loop`, `heat-transfer-analysis` and `dsc-analysis` execute quantitative or experimental analysis in the next stage. `claim-evidence-audit` checks actual final claims, and `handoff` records scoped state. Do not keep all these Skills resident together.

Return task/scope, selected IDs and statuses, sources actually checked, G1-G5 applicability matrix, alternatives, missing parameters, limitations and a status of `applicable`, `conditional`, `unresolved` or `blocked`. Never infer `applicable` from keyword retrieval. Label hypothetical brainstorming and its test plan distinctly from a validated conclusion.

## Stop conditions

Do not present a consequential scientific conclusion as verified when the
knowledge library, decisive source passages, applicable assumptions or required
scope review are unavailable. Report the missing evidence and an `unresolved` or
`blocked` status; hypothetical alternatives and their validation plans may still
be discussed as such. Do not promote a candidate without the original source
review and responsible human sign-off required by the knowledge admission rules.

## Completion criterion

The theory stage is complete when the requested actions and scope are classified,
the applicable S0/S1/S2 route and its reason are recorded, and the results do not
exceed the reviewed evidence. For S1, the context identity and current scope must
be checked. For S2, document G1–G5, the sources actually inspected, limitations,
alternatives and unresolved conditions. A candidate remains a candidate until its
separate promotion requirements are met. Record missing coverage instead of
claiming a completed scientific review; fixture success is not a field trial.
