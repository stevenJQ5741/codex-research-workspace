# Shared Language Context

## Purpose

This file defines the shared language used by Quan Jiang and Codex.

It is a glossary, not a manuscript, not a scratchpad, and not a full research plan.

Use this file to reduce ambiguity, shorten future prompts, and prevent terminology drift.

## Rules

1. Record only terms that matter repeatedly.
2. Keep definitions short.
3. Do not include long experimental discussion.
4. Do not include implementation details unless they clarify a term.
5. If a term is unresolved, mark it as `Unresolved`.
6. If a term changes meaning, update the entry and record the reason in the decision log if durable.

## Core terms

### Codex workspace

The GitHub repository used as persistent project memory across computers.

### Token-efficient layered rule system

The rule structure where `AGENTS.md` is a compact index, detailed rules live in `docs/rules/`, and task-specific background is loaded only when needed.

### Durable decision

A decision that affects future interpretation, writing, analysis, file structure, or workflow.

### Raw data

Original experimental or measurement data. Raw data must not be overwritten.

### Processed data

Data generated from raw data through cleaning, smoothing, baseline correction, fitting, calculation, or conversion.

### Overclaiming

Stating a conclusion more strongly than the evidence supports.

### Model estimate

A value calculated from assumptions and equations. It must not be described as a direct measurement.

### High-softening or partial-melting range

A cautious thermal interpretation used when DSC or model results suggest softening or melting-related behavior but do not justify a sharp melting point.

### Apparent thermal conductivity

An estimated thermal conductivity affected by sensor position, boundary conditions, and model assumptions. It should not be treated as an intrinsic material constant without validation.

### IFSS

Interfacial shear strength. It can support interpretation of interface-related behavior, but should not be used alone to explain all macroscopic properties.

### ILSS

Interlaminar shear strength. For reheating studies, ILSS changes should be connected cautiously to surface temperature, pressure, contact time, and polymer flow.

### Shared language

The controlled vocabulary used by the user and Codex to reduce verbosity and ambiguity.

### Evidence ledger

A compact mapping from a scientific claim or derived value to its source, evidence class, assumptions, limitations, and permitted wording.

### Release candidate

The exact manuscript, figure, table, workbook, or PDF version currently being checked for delivery. It must be identified explicitly before QA.

### Skill usage receipt

A compact final-response record naming the Skills that materially affected the task, their roles, and any evidence-based revision signal.

### Invocation gate

The rule that allows a clearly matched Skill to proceed automatically but requires one confirmation when the workflow is ambiguous, method-sensitive, expensive, or materially expands scope.

### Managed Skill copy

A local Skill installed from this repository and marked as replaceable by scripts/install_skills.ps1. Unmarked personal Skills must not be overwritten.

## Unresolved terms

Add unresolved terms here when needed.
