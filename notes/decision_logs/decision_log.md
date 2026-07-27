# Decision Log

This file records important project decisions and the reasoning behind them.

## Format

```markdown
## YYYY-MM-DD - Decision title

Decision:
Describe the decision.

Reason:
Explain the reason.

Impact:
Explain how this affects future work.
```

## 2026-06-29 - Repository-based Codex memory

Decision:
Use this GitHub repository as the persistent memory layer for Codex across multiple computers.

Reason:
Codex does not automatically synchronize local project context, temporary files, and session state across different computers.

Impact:
Important context must be written into version-controlled files such as `AGENTS.md`, `PLANS.md`, and decision logs.

## 2026-06-29 - Initialize Codex research workspace

Decision:
Use a structured folder layout for research context, notes, scripts, templates, data, outputs, and archived materials.

Reason:
A predictable layout makes it easier for Codex and the user to recover context, preserve raw data, and maintain reproducible workflows.

Impact:
Future work should update `PLANS.md`, decision logs, session summaries, and relevant templates instead of relying only on chat history.

### 2026-06-29 - Token-efficient layered rule system

**Decision:**
The repository rule system was changed from a large single `AGENTS.md` into a layered structure: compact root `AGENTS.md`, detailed task-specific files under `docs/rules/`, and an optional global `~/.codex/AGENTS.md` template.

**Reason:**
A large always-read rule file increases fixed context usage. A compact index plus task-specific rule files allows Codex to load only the smallest necessary context.

**Impact:**
Future Codex sessions should begin by reading only `AGENTS.md`, `README.md`, and `PLANS.md`, then selectively load relevant rule files based on the task.

## 2026-07-02 - Research skills system

Decision:
Add a research-oriented skills system under `skills/`, using mostly user-invoked skills to reduce context load.

Reason:
The repository already has layered rules, but recurring tasks such as manuscript review, DSC analysis, Japanese emails, presentation review, and handoff need repeatable workflows with clear completion criteria.

Impact:
Future Codex sessions should use `skills/router/ask-jiang/SKILL.md` to select the smallest relevant workflow, then load only the necessary skill and rule files.

## 2026-07-14 - Parallel V2 Skill pilot

Decision:
Create V2 Skill drafts under `skills_v2/` without replacing V1, and add a compact Skill usage receipt to final responses.

Reason:
The PLA/CF manuscript showed that isolated analysis and manuscript review Skills did not fully cover evidence provenance, full-paper dependency order, cross-artifact consistency, rendered QA, or observable Skill usage frequency.

Impact:
V2 behavior can be compared safely against V1. Future replacement or merging decisions require real-task evidence and explicit user approval.

## 2026-07-14 - Integrate Skills and enable governed automatic invocation

Decision:
Merge the approved V2 workflows into the canonical `skills/` tree, remove `skills_v2/`, enable implicit discovery for all Skills, and add a confirmation gate plus cross-computer installer.

Reason:
The comparison established useful improvements, while parallel versions created duplicate instructions. Repository files also require installation before Codex can discover them automatically.

Impact:
The repository now has one Skill source of truth. Clear matches run automatically; ambiguous, method-sensitive, expensive, or scope-expanding workflows ask once. Final responses report actual Skill use.

## 2026-07-16 - Separate research-brief editing from native Office release

Decision:
Promote the validated project pilot into two canonical Skills: `research-brief-editor` for evidence-led editorial work and `office-native-release` for native Word/PowerPoint export plus Office/PDF pair QA. Keep general artifact verification in `artifact-qa` and remove parallel version naming.

Reason:
The split reduces irrelevant release instructions during editorial work and makes the device-specific Office release gate reusable. Native Office smoke tests preserved critical glyphs and completed structural and full-size visual checks, while LibreOffice has been unreliable on the primary workstation.

Impact:
Future computers install the same two Skills from this repository. Final DOCX/PPTX releases on Windows use Microsoft Office as the authoritative renderer, structural and semantic pair QA as Layer A, and Poppler rendering plus full-size visual inspection as Layer B. Real usage feedback should revise the canonical Skills directly instead of creating another parallel version tree.

## 2026-07-27 - Consolidate presentation workflows into one global Skill

Decision:
Replace the short presentation-review workflow and the project-local presentation pilot with one canonical `presentation-review` Skill. Keep deterministic PPTX validation project-independent, require an exported PPTX snapshot for Google Slides, and reserve native PowerPoint release for Windows release candidates.

Reason:
Parallel project and global copies produced duplicate discovery and risked future drift. Project-specific IFSS filenames and hashes were useful development evidence but do not belong in the reusable Skill.

Impact:
Future presentation work installs `presentation-review` from this repository and keeps project-specific aesthetic ledgers in each workspace. Intermediate PPTX validation uses the lightest sufficient profile; full native Office release remains an explicit final gate.

## 2026-07-27 - Use rolling timestamped default branches

Decision:
Name each upload branch from its first successful PushEvent time in JST using `agent/YYYYMMDD-HHmm-topic`. After validation, make the newest upload branch the GitHub default and retain the previous default as a historical version.

Reason:
The user wants the repository landing state to represent the latest uploaded project while older states remain directly recoverable as timestamped branches.

Impact:
Future publish workflows create and push a new branch, rename it from the recorded PushEvent, validate it, promote it to default, synchronize `origin/HEAD`, and preserve older timestamped branches. Pull requests remain optional review artifacts rather than the promotion mechanism.
