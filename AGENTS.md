# AGENTS.md

## Purpose

This repository is the persistent working memory for Codex-assisted research.

Use this file as a compact operating guide.
Do not treat it as a full knowledge base.

Detailed rules are stored in `docs/rules/` and should be read only when relevant to the current task.

## User context

The user is Quan Jiang / 姜 泉.

Main work areas:

- Composite materials.
- Fiber-reinforced polymers.
- Interface evaluation.
- DSC and thermal analysis.
- Heat-transfer modeling.
- 3D-printed composites.
- Natural fiber composites.
- Academic writing.
- Japanese academic and administrative emails.
- Presentation preparation.
- International research proposals.

## Core rules

Always follow these rules:

1. Be precise.
2. Avoid overclaiming.
3. Do not invent data, citations, parameters, file names, or experimental conditions.
4. Clearly separate:
   - experimental observations
   - calculated results
   - model assumptions
   - literature-supported interpretation
   - speculation
5. Do not treat model results as measured values.
6. Do not overwrite raw data.
7. Do not delete files without explicit user approval.
8. Do not commit sensitive personal files or credentials.
9. Prefer reproducible workflows over one-time manual edits.
10. Preserve the user's intended scientific logic unless explicitly asked to restructure.

## Language policy

- Use Chinese for discussion, planning, and explanations.
- Use academic English for manuscripts, abstracts, reports, figure captions, and conference materials.
- Use concise and polite Japanese for emails to professors, companies, and university staff.
- Avoid excessive keigo unless specifically required.
- For Japanese emails, keep sentences short and purpose-first.

## Token-efficiency policy

Do not read every rule file by default.

At the start of a task:

1. Read this `AGENTS.md`.
2. Read `README.md`.
3. Read `PLANS.md`.
4. Identify which specific rule files are relevant.
5. Ask or state which additional files will be read before reading them, unless the task clearly requires them.

Do not automatically read:

- all files under `docs/rules/`
- all session summaries
- all project briefs
- all decision logs

Prefer reading:

- the smallest relevant rule file
- the latest relevant decision log entry
- the current task file
- the exact data file needed for analysis

## Rule-file map

Read the following detailed rule files only when relevant.

| Task type | Rule file |
| --- | --- |
| Token-efficient workflow | `docs/rules/token_efficiency_rules.md` |
| Manuscripts, abstracts, captions, academic English | `docs/rules/manuscript_writing_rules.md` |
| DSC curves, Tg/Tc/Tm, broad endotherms | `docs/rules/dsc_analysis_rules.md` |
| Moving heat-source model, reheating, ILSS thermal discussion | `docs/rules/heat_transfer_rules.md` |
| IFSS, interface evaluation, microstructure-property links | `docs/rules/ifss_interface_rules.md` |
| Natural fibers, e-ASIA, PALF/PBS/PLA, agricultural validation | `docs/rules/natural_fiber_project_rules.md` |
| Data files, Python analysis, figures, tables, reports | `docs/rules/data_management_rules.md` |
| Japanese professor, company, and university emails | `docs/rules/japanese_email_rules.md` |
| PPT structure, slide narrative, visual consistency | `docs/rules/presentation_rules.md` |
| Project-specific background | `docs/rules/current_research_context.md` |

Read `docs/rules/current_research_context.md` only when project background is needed.

## Skills map

Reusable workflows live under `skills/`.
Install them with `scripts/install_skills.ps1` so Codex can discover them.

Use the router automatically when the workflow is unclear:

- `skills/router/ask-jiang/SKILL.md`

Task-specific skills:

| Task | Skill |
| --- | --- |
| clarify a complex research task | `skills/research/research-grill/SKILL.md` |
| update shared terminology | `skills/research/shared-language/SKILL.md` |
| reproducible data analysis | `skills/research/analysis-feedback-loop/SKILL.md` |
| manuscript review or revision | `skills/research/manuscript-review/SKILL.md` |
| full manuscript production | `skills/research/manuscript-pipeline/SKILL.md` |
| scientific claim audit | `skills/research/claim-evidence-audit/SKILL.md` |
| DSC analysis | `skills/research/dsc-analysis/SKILL.md` |
| heat-transfer or ILSS reheating analysis | `skills/research/heat-transfer-analysis/SKILL.md` |
| presentation review | `skills/research/presentation-review/SKILL.md` |
| Japanese email | `skills/research/japanese-email/SKILL.md` |
| artifact verification | `skills/research/artifact-qa/SKILL.md` |
| cross-session handoff | `skills/research/handoff/SKILL.md` |
| final Skill receipt | `skills/governance/skill-usage-report/SKILL.md` |

Skills are workflows.
Detailed scientific rules remain in `docs/rules/`.

### Invocation policy

1. Select relevant installed Skills automatically.
2. Use at most one primary and two supporting Skills.
3. Proceed when the match is clear and the request already authorizes the work.
4. Ask once when the workflow is ambiguous, method-sensitive, expensive, or expands scope.
5. Keep destructive, external, sensitive, commit, and push actions separately authorized.
6. End every final response with actual Skill usage or explicit non-use.

## Session workflow

### Start of session

Default start:

1. Read `AGENTS.md`.
2. Read `README.md`.
3. Read `PLANS.md`.
4. Do not read all detailed rules automatically.
5. Decide which detailed rule files are relevant.
6. Summarize the current state briefly.
7. Apply the invocation policy before major work.

### End of session

At the end of a major session:

1. List modified files.
2. Summarize key changes.
3. Summarize important decisions.
4. Summarize unresolved issues.
5. Update `PLANS.md` only if the task state changed.
6. Update `notes/decision_logs/decision_log.md` only for durable decisions.
7. Add a session summary only when the session produced meaningful changes.
8. Keep summaries short.
9. Run `git status`.
10. Do not push unless the user explicitly approves.

## Output style

Prefer concise structured responses:

1. What was done.
2. Key result.
3. Files changed.
4. Risks or unresolved issues.
5. Next step.

Avoid:

- long generic explanations
- repeated background
- unnecessary alternatives
- decorative language
- rewriting stable rules without reason
