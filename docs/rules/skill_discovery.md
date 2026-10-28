# Project-local skill discovery

`skills/` is the only authoritative tree. `.agents/skills/` is a generated local
discovery surface and is ignored by Git; do not put an authoritative new Skill
there. User-level managed installation remains available through
`scripts/install_skills.ps1`; installing global and project-local copies with the
same names may cause duplicate selector entries. Restart or open a new session
if a changed skill is not discovered.

From the repository root:

```powershell
python scripts/sync_project_skills.py
python scripts/sync_project_skills.py --apply
python scripts/sync_project_skills.py --check
```

Use a working Python 3.9+ interpreter; replace `python` with its absolute path
when the Windows `python.exe` alias is unavailable. The helper uses only the
standard library and does not install packages or contact a network service.

The first command is a read-only preview. The second creates only missing entries,
preferring relative symbolic links and falling back to copies if link creation is
unavailable. `--mode symlink` or `--mode copy` chooses a specific method. Existing
correct links and byte-identical copies are retained. A conflicting link or stale
copy blocks creation; the script never replaces or deletes it. Inspect the returned
JSON and preserve any user changes before separately deciding how to resolve a
conflict. Extra local entries are listed and left unchanged.
`--check` returns a nonzero exit code for missing or conflicting canonical entries;
the ordinary preview can show planned missing entries without treating them as an error.

Copied entries do not update automatically: rerun the preview after changing
`skills/`; a stale copy is reported. The generated discovery directory is ignored,
including any manually added entries, so personal content there is not a Git backup.
The script can be tested with `--root` against an isolated checkout. A successful
local check or installation does not prove discovery on another physical computer,
nor does it prove implicit invocation in a live Codex task.
