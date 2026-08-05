# Codex Research Workspace

This repository stores durable research context, reusable workflows, professional
rules, decisions, scripts, and templates so Codex work can continue reliably
across computers.

## Architecture

| Layer | Purpose |
| --- | --- |
| `AGENTS.md` | compact operating entrypoint |
| `PLANS.md` | current objectives and unresolved work |
| `docs/rules/` | reusable professional and workflow rules |
| `docs/project_briefs/` | project-specific facts, parameters, and boundaries |
| `docs/shared_language/CONTEXT.md` | canonical terminology |
| `docs/adr/` | durable architecture and policy decisions |
| `skills/` | reusable operational workflows |
| `notes/` | historical decisions, mistakes, sessions, and maintenance logs |
| `scripts/` | reproducible utilities |
| `templates/` | reusable artifact and prompt templates |
| `data/`, `outputs/`, `archive/` | protected inputs, generated artifacts, and inactive history |

This separation is intentional: universal Skills must not contain project file
names, experimental parameters, private identifiers, or project-specific history.

## Start a session

```powershell
git pull
powershell -ExecutionPolicy Bypass -File scripts/install_skills.ps1
codex
```

Read `AGENTS.md`, `README.md`, and `PLANS.md`, then load only the files needed for
the task. Push only after explicit approval.

## Skill responsibility matrix

| Skill | Primary responsibility | Boundary |
| --- | --- | --- |
| `ask-jiang` | select the smallest workflow | routes; does not resolve research assumptions |
| `research-grill` | resolve consequential ambiguity | clarifies; does not choose the Skill stack |
| `shared-language` | control durable terms and symbols | terminology, not full artifact editing |
| `analysis-feedback-loop` | reproducible calculations and figures | analysis, not manuscript orchestration |
| `manuscript-pipeline` | orchestrate full-paper production | coordinates; delegates review and claim audit |
| `manuscript-review` | review an existing draft | broad manuscript quality, not full production |
| `claim-evidence-audit` | test claim support and wording strength | claim ledger, not prose or release review |
| `dsc-analysis` | analyze DSC data | DSC only |
| `heat-transfer-analysis` | analyze thermal models and interpretation | thermal scope only |
| `presentation-review` | review/revise slides and audit PPTX changes | delegates final native release |
| `research-brief-editor` | produce evidence-grounded short Office sources | brief content, not Office export |
| `artifact-qa` | generic structural, numerical, and visual QA | excludes final native Office pairs |
| `office-native-release` | native Word/PowerPoint export and pair QA | final declared Office releases only |
| `japanese-email` | concise Japanese email drafting | email only |
| `handoff` | continuation record | records state; does not redo the task |
| `skill-usage-report` | disclose actual Skill use | reporting only |

Use at most one primary and two supporting Skills. Precise triggers live in each
`SKILL.md` frontmatter.

## Rules and project briefs

Load reusable rules from `docs/rules/`. Load named project facts from
`docs/project_briefs/INDEX.md`. If a value, filename, sample, event, or model
setting belongs to one project, keep it in a project brief rather than a universal
Skill or professional rule.

## Terms and decisions

Use `docs/shared_language/CONTEXT.md` for canonical terms such as authoritative
source, baseline, release candidate, validation profile, snapshot, and archive.
Use `docs/adr/` for hard-to-reverse policy. Historical logs explain how the
current state developed but are not active policy unless an ADR says so.

## Installation and validation

The repository `skills/` tree is authoritative. Install managed copies with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_skills.ps1
```

The installer refuses to replace an unmarked personal Skill. After Skill changes:

1. validate every Skill and `agents/openai.yaml`
2. check completion criteria and unresolved placeholders
3. install to an isolated destination and compare hashes
4. run script syntax checks and relevant smoke tests
5. use real tasks to evaluate routing precision

## Branch maintenance

Validated uploads continue to use rolling timestamped default branches. Branch
retention, half-year snapshot tags, deletion eligibility, and post-delete checks
are governed by
`docs/adr/0004-maintenance-boundaries-and-branch-retention.md`. Every pruning
cycle begins with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/branch_pruning_dry_run.ps1 `
  -PreviousDefault agent/YYYYMMDD-HHmm-topic `
  -SnapshotTag snapshot/YYYY-H1 `
  -InactiveBranch branch-confirmed-inactive
```

Omit `-InactiveBranch` when inactivity has not been confirmed; the script will
protect that branch. It never deletes a remote branch. Remote deletion always
requires a separate approval and post-delete reachability checks.
