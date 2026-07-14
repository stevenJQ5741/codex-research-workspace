# 0001 - Research Skills System

## Status

Accepted. The original user-invoked policy is superseded by ADR 0002.

## Context

The repository already uses a token-efficient layered rule system with:

- compact root `AGENTS.md`
- detailed rules in `docs/rules/`
- persistent task state in `PLANS.md`
- durable decisions in `notes/decision_logs/decision_log.md`

The next improvement is to add reusable skills for common research workflows.

## Decision

Create a research-oriented skills system under:

```text
skills/
```

At adoption time, most skills were user-invoked to avoid unnecessary context load. ADR 0002 later superseded this invocation policy.

A router skill, `ask-jiang`, will help choose the correct workflow.

## Reason

Research tasks often fail because Codex:

- starts writing before clarifying assumptions
- overclaims scientific conclusions
- loads too much context
- forgets project-specific terminology
- treats model estimates as measured values
- produces polished but scientifically unsafe text

Skills provide repeatable workflows with clear completion criteria and feedback loops.

## Consequences

Future work should use skills for recurring workflows such as:

- research clarification
- manuscript review
- DSC analysis
- heat-transfer analysis
- presentation review
- Japanese emails
- handoff between sessions

Detailed scientific rules remain in `docs/rules/`, not inside every skill.
