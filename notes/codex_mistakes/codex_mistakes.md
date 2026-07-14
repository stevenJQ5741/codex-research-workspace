# Codex Mistakes

This file records recurring Codex mistakes so they can be avoided in future sessions.

## Format

```markdown
## Mistake title

Problem:
Describe the mistake.

Correction:
Describe the correct behavior.

Example:
Give a concrete example if useful.
```

## Overclaiming Scientific Results

Problem:
Codex may sometimes describe weak or indirect evidence as a confirmed conclusion.

Correction:
Use cautious academic language and clearly separate experimental results, assumptions, and interpretation.

Example:
Do not write: "The material melted at 220°C."

Prefer:
"The DSC curve suggests broad endothermic behavior around 200-220°C, which may correspond to high softening or partial melting."

## Assuming Repository Skills Are Automatically Installed

Problem:
Keeping SKILL.md files in a Git repository does not by itself make them discoverable in every Codex task.

Correction:
Treat the repository as the source of truth, run scripts/install_skills.ps1 after clone or pull, and restart Codex. Never overwrite an unmarked personal Skill during installation.
