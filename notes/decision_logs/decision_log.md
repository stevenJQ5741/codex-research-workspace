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
