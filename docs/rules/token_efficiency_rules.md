# Token Efficiency Rules

## Purpose

Reduce unnecessary context consumption while preserving research reliability.

## Core rules

1. Do not read all rule files by default.
2. Read only the smallest set of files needed for the task.
3. Prefer current task files over historical summaries.
4. Prefer compact decision logs over full conversation history.
5. Do not output long summaries unless requested.
6. Do not repeat full rules in every response.
7. Do not load all data files before knowing which one is needed.
8. Do not open large files unless the task requires it.
9. Ask before reading broad folders.
10. Use file maps and targeted search when possible.

## Start-session default

Read only:

- `AGENTS.md`
- `README.md`
- `PLANS.md`

Then decide which detailed rules are relevant.

## End-session default

Keep the summary short:

- files modified
- key decision
- unresolved issue
- next step

Only update logs if the information will matter in future sessions.

## When to update decision logs

Update decision logs only when:

- scientific interpretation changes
- a model assumption is fixed
- a terminology rule is established
- a project direction changes
- a recurring mistake is identified
- an important writing convention is confirmed

Do not log trivial edits.
