# 2026-08-04 Deep Cleanup Audit

## Scope and safety

The audit covered repository structure, Skills, rules, ADRs, shared language,
decision and mistake logs, session summaries, scripts, templates, local and
remote branches, tags, the default branch, and open pull requests. No commit,
push, remote branch deletion, or remote tag creation was authorized.

## Before-state metrics

| Metric | Before |
| --- | ---: |
| Skills | 16 |
| active `docs/rules/*.md` files | 10 |
| remote branches | 3 |
| remote tags | 0 |

All 16 Skills had `SKILL.md`, `agents/openai.yaml`, an explicit completion
criterion, and implicit-invocation metadata. Repository and installed managed
copies initially matched by SHA-256. PowerShell and Python sources parsed.

## Principal findings

1. `presentation-review` duplicated final native release steps owned by
   `office-native-release`.
2. `manuscript-pipeline` carried a project-named PLA/CF reference.
3. `docs/rules/` mixed reusable rules with project temperatures, feed rates,
   conference identity fields, and tri-country project detail.
4. Skill invocation and token policies were repeated across `AGENTS.md`,
   `README.md`, `PLANS.md`, rules, templates, and Skills.
5. Historical pilot policy remained readable without consistent superseded
   labels.
6. `authoritative source`, `baseline`, `release candidate`, `validation profile`,
   `snapshot`, and `archive` lacked one canonical definition set.
7. Empty documentation trees suggested obsolete homes.
8. The repository had no half-year branch pruning record or snapshot tag.

## Disposition matrix

| Item | Disposition | Reason | Impact and risk |
| --- | --- | --- | --- |
| 16 canonical Skills | retain and simplify | responsibilities remain useful | routing must be tested on real tasks |
| project-named manuscript reference | delete after folding generic controls into workflow | violates universal Skill boundary | Git history preserves provenance |
| presentation final-release instructions | merge boundary into `office-native-release` | remove duplicated release authority | presentation handoff must remain explicit |
| token and Skill design rules | merge into `workflow_governance_rules.md` | one active governance source | all indexes must change together |
| presentation rule file | merge reusable content into presentation references | duplicated Skill/reference content | presentation tasks now load the Skill |
| current and natural-fiber project rules | move into project briefs | separate project knowledge | old paths become invalid and are removed from indexes |
| project DSC/thermal values | move into `ilss-reheating.md` | retain context without polluting general rules | values remain working context, not validated data |
| private conference control ID | remove from active tree | repository policy forbids private IDs | recoverable in Git history; external tracking required |
| duplicate manuscript rules template | delete | it was a second policy copy, not an artifact template | manuscript rule remains authoritative |
| empty duplicate docs trees | delete | no active content and misleading destinations | none |
| ADR and decision/session history | retain; mark superseded items | historical evidence remains necessary | readers must prefer accepted ADRs |
| Office and PPTX scripts | retain | deterministic validated capability | runtime smoke tests remain environment-dependent |
| rolling default branches | retain | current publication mechanism | requires half-year review |

## Skill boundary matrix

| Pair | Boundary |
| --- | --- |
| `manuscript-pipeline` / `manuscript-review` | full production orchestration / review of an existing draft |
| `claim-evidence-audit` / `manuscript-review` | claim support and permitted wording / broader argument, language, consistency, readiness |
| `artifact-qa` / `office-native-release` | generic artifact QA / final native Office export and pair release |
| `research-grill` / `ask-jiang` | assumption resolution inside work / workflow routing |
| `presentation-review` / `office-native-release` | slide content, design, bounded revision audit / final native PowerPoint release |

## Mechanical versus real-task evidence

Mechanical checks can establish structure, syntax, links, validator compliance,
installation parity, and Git reachability. They cannot establish that automatic
Skill routing is precise, that prompts are economical on real manuscripts, or
that Office rendering remains stable after environment changes. Those remain
forward-validation tasks.

## After-state metrics

| Metric | Before | After |
| --- | ---: | ---: |
| Skills | 16 | 16 |
| active `docs/rules/*.md` files | 10 | 7 |
| total `SKILL.md` lines | 630 | 512 |
| root `AGENTS.md` lines | 150 | 57 |
| remote branches | 3 | 3 |
| local tags | 0 | 1 |
| remote tags | 0 | 0 |

The local annotated `snapshot/2026-H1` points to the final H1 commit
`0555b5a223cc84f697b6f3fc8d70e669a205f734`. It was not pushed.

## Validation results

- 16/16 Skills passed the official validator.
- 16/16 `openai.yaml` files parsed and retained implicit invocation.
- 16/16 Skills contain explicit stop conditions and completion criteria.
- Isolated installation copied 16/16 managed Skills with zero marker or SHA-256
  mismatch.
- Four PowerShell and three Python scripts passed syntax parsing.
- The three Python command-line tools passed `--help` smoke tests.
- Native Office preflight found Word, PowerPoint, their COM registrations, and
  Poppler; no release artifact was available for pair or visual QA.
- Explicit Markdown links, active legacy-path references, universal-Skill project
  leakage, Skill placeholders, metadata length, and `git diff --check` all
  reported zero failures.

## Forward tests

Three independent read-only prompts selected the intended smallest workflow:

1. existing manuscript plus mechanism claims:
   `manuscript-review` with targeted `claim-evidence-audit`, not
   `manuscript-pipeline`
2. working-draft spreadsheet and DOCX QA: `artifact-qa`, not
   `office-native-release`
3. bounded review-copy slide revision: `presentation-review`, not
   `office-native-release`

These tests support the revised boundaries but do not replace real artifact work.
