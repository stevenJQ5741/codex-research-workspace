# End Session Prompt

Use this prompt at the end of a Codex session.

```text
Please summarize this session and update the repository context.

Required actions:

1. List all files modified in this session.
2. Summarize the main changes.
3. Summarize any decisions made.
4. Summarize unresolved issues.
5. Update PLANS.md if the task state changed.
6. Add a new entry to notes/decision_logs/decision_log.md if important decisions were made.
7. Add a new session summary under notes/session_summaries/ using the format YYYY-MM-DD-session-summary.md.
8. If you made or noticed a recurring mistake, update notes/codex_mistakes/codex_mistakes.md.
9. Run git status and show me the result.
10. Do not push until I explicitly approve.
```
