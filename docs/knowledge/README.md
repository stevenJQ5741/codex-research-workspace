# Scientific Knowledge Layer — B Final Acceptance Candidate

This directory is **a curated scientific knowledge index**, not a substitute for reading source publications or checking model assumptions. Its canonical copy lives in the Codex Research Workspace repository and is shared across research projects. Project measurements, unpublished results, private identifiers, and project-only parameters remain outside this layer.

## Distinctions

- `docs/rules/`: how scientific work must be conducted (policy).
- `docs/knowledge/`: what scientific theories and models claim, with assumptions, evidence and limitations (knowledge).
- `docs/project_briefs/`: bounded facts and working hypotheses for named projects (context, **not automatically verified**).
- `notes/` and project-level `theory_context.json`: prior decisions or review snapshots (may require re-check).
- `skills/research/theory-grounding/`: procedure for retrieving and auditing a theory (workflow).

## Knowledge admission and verification

1. Add a record to `INDEX.json` with a unique immutable `id`, a relative `path`, multilingual keywords, domains, status, and source links. Never use arbitrary shell commands or untrusted remote paths as metadata.
2. Store a focused Markdown card explaining definition, mathematical model when relevant, assumptions, applicability conditions, measurement-to-model mapping, known counterexamples, competing explanations and exact source pointers.
3. Keep **two independent classifications**: `epistemic_type` (law/theoretical_model/empirical_relation/competing_hypothesis/research_hypothesis) and `review_status` (`candidate`, `reviewed`, `disputed`, `retired`). A bibliographically confirmed DOI does not itself verify the claim or equation in its paper.
4. Automatic extraction can only create **candidate** entries. `reviewed` needs direct inspection of the relevant original passage, exact equation/conditions, and explicit responsible scientific review with a dated log entry. Do not promote an entry by automated self-assertion.
5. Document contradictions rather than silently overwriting old cards. Retire an old card with replacement pointers and retain Git history.
6. For each interpretation, check whether its source addresses the specific material, scale, geometry, loading and regime of the current task. Link a project result only as project evidence, never promote it as a universal law.

## Data format

`INDEX.json` is intentionally JSON, readable by the Python standard library. Each indexed record must have: `id`, `path`, `title`, `domains`, `keywords`, `epistemic_type`, `review_status`, `sources`, `assumptions_checklist`, `known_limitations`. Source objects contain `title`, `url` (or DOI URL), `bibliographic_metadata_checked`, and `claim_in_source_checked`. `claim_in_source_checked=false` means the relevant passage has **not** been directly verified. Index records are discovery metadata: the card's detailed caveats govern.

## S0/S1/S2 research preflight

Codex assesses the user's **requested actions** and six change dimensions before
the deterministic script runs. A translated passage mentioning novelty or a
new model is language content; a request to judge novelty or choose a model is
scientific work. `--intent-file` provides an exact-query-bound structured
assessment. Intent schema 1.1 also segments the exact query into user
instructions and supplied content; the lexical guard scans instructions only.
Unquoted translated text can therefore contain scientific verbs without
triggering a theory search. An uncertain boundary or a new instruction after
content under a pure-transform assessment routes to S2 for review. Missing,
contradictory or uncertain scientific intent routes to S2 unless the task is a
clearly bounded text transformation. The lexical guard is supplementary and
cannot guarantee semantic understanding.

- **S0:** no scientific inference is requested. The router returns without reading this directory.
- **S1:** reuse a dated, scoped Theory Context only after its review record is
  complete and a fresh `current_scope.scope_review` binds the exact task query
  to checked project/question, material, model assumptions, boundaries,
  parameters and contrary evidence. Selected card hashes and source-review
  states and the complete canonical index-record hashes must still match.
  This performs no candidate-card search. Task text
  indicating change, mixed editing and recalculation, wet-heat cycling,
  morphology-based attribution or counterevidence overrides stale scope data.
  The current task's actual evidence must be inspected before setting
  `evidence_checked=true`; a fresh timestamp is only a validity limit. A
  candidate card remains a candidate during reuse. High-impact claims with
  unchecked decisive sources require S2.
- **S2:** new or changed scientific inference, an explicit theory request, or
  a theory-dependent task without a valid context retrieves candidates. The
  acting reviewer must then perform G1–G5 source and applicability checks.
  No indexed match is a **coverage gap**, not a novelty finding.

The small index offers a card only for a keyword hit, an explicitly requested
matching domain, or two inferred domain matches. This reduces unrelated
candidate cards; it can also leave a genuine theory undiscovered. Broaden the
source search when coverage is incomplete.

`THEORY_CONTEXT.schema.json` defines the compact handoff record. The package's
`examples/theory_context_short_fiber_candidate.json` is intentionally pending
and cannot pass S1. A candidate card may be used conditionally for scoped
reasoning after an explicit applicability review, but remains unverified source
evidence until its original claim and conditions are checked.

`current_scope` repeats the six scope fields from the Context and adds
`scope_review`: `checked_at` (timezone-aware ISO-8601), `checked_by`,
`query_sha256` (SHA-256 of the exact UTF-8 query),
`fields_confirmed_unchanged` (all six scope field names),
`contradictory_evidence_checked: true`, and nonempty `evidence_refs`. These
fields are a traceable attestation, not proof that an external document was
actually inspected. In v0.2.2, `checked_at` must be no older than 30 minutes
at preflight. The responsible reviewer must inspect current evidence and its
references before asserting that nothing consequential changed. A v0.2
Context cannot be reused without a fresh v0.2.2-format review. Each selected
record stores `index_record_sha256`, the SHA-256 of UTF-8 JSON for the entire
index record with sorted keys, `ensure_ascii=False`, compact separators and
no NaN. Source URL, applicability checklist, limitation or source status
changes therefore invalidate S1 even when the Markdown card is unchanged.
The new hash does not certify the underlying scientific claim.

From the repository root:

```powershell
python scripts/theory_preflight.py --task-type new-project --query "短天然纤维增强 PBS 复合材料的载荷传递"
python scripts/theory_preflight.py --task-type model-selection --query "PALF/PBS 三相模型导热率" --domain thermal
python scripts/theory_preflight.py --task-type routine --query "润色日语邮件"
python scripts/theory_preflight.py --task-type analysis --query "沿用既有 RVE 参数计算热导率" --intent-file intent.json --theory-context context.json --scope-file current_scope.json
```

Output is a candidate list plus instructions for human/agent scientific judgment. This script does **not** mechanically certify applicability. A strong scientific conclusion requires review of the card, actual source, current project facts and relevant experiments.

## Cache and staleness

Snapshots may record `knowledge_base_commit` (Git commit SHA) and selected cards with `card_sha256` and `index_record_sha256`. A snapshot is invalidated when a consequential material/model assumption changes, either selected hash changes, or new contradictory evidence appears. A new chat alone is **not** an invalidation event. If repository version or source verification is unavailable, explicitly report the gap and avoid claiming an audited result.
