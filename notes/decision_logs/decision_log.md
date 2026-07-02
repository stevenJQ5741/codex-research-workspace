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
