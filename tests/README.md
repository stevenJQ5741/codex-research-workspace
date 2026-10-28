# Deterministic regression tests

Run from the repository root with Python 3.9 or later:

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
```

These tests use the Python standard library. They restore the original B Final
BoundaryFix routing fixtures and adapt their paths to the canonical repository
layout. `real_task_cases.json` retains the 22 original cases;
`test_semantic_intent.py` retains the 18-case multilingual acceptance set.
`test_pptx_invariants.py` exercises relative and absolute image relationships,
effective PPI warnings and high-resolution/disabled-threshold controls.
`test_image_quality_coverage.py` checks crop-aware PPI and explicit unassessed
objects; `test_project_skill_discovery.py` checks non-overwriting discovery setup.

The example Theory Context is deliberately pending and not valid for S1 reuse.
Fixture success does not establish scientific correctness, source review,
automatic Codex activation, native Office rendering or the independent 30-task
field trial described in `docs/knowledge/EVAL_PROTOCOL.md`.

The example card's SHA-256 covers actual file bytes. `.gitattributes` causes
future fresh checkouts to materialize Markdown knowledge cards with LF line
endings. Existing checkouts are not rewritten automatically; inspect
`git ls-files --eol` and preserve local changes before deciding whether any
checkout needs to be refreshed. A line-ending change can invalidate a cached
Theory Context even when its scientific text has not changed.

On restricted Windows runners where the system temporary directory is
unwritable, set `TEMP` and `TMP` to an existing writable scratch directory
before running the tests. Do not change tracked research inputs to make tests pass.
