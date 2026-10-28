#!/usr/bin/env python3
"""Safely create or check project-local Codex skill discovery entries."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path


def files_digest(directory: Path) -> dict[str, str]:
    return {str(p.relative_to(directory)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob("*")) if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def sources(root: Path) -> dict[str, Path]:
    skill_root = root / "skills"
    if not skill_root.is_dir() or skill_root.is_symlink():
        raise ValueError("The canonical skills directory is missing or is a symbolic link")
    result = {}
    for entry in sorted(skill_root.rglob("SKILL.md")):
        match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", entry.read_text(encoding="utf-8"))
        if not match:
            raise ValueError(f"Invalid skill name: {entry}")
        name = match.group(1)
        if name in result:
            raise ValueError(f"Duplicate skill name: {name}")
        source = entry.parent.resolve()
        if not source.is_relative_to(skill_root.resolve()):
            raise ValueError(f"Skill source escapes canonical tree: {name}")
        result[name] = source
    if not result:
        raise ValueError("No canonical SKILL.md files found")
    return result


def inspect(root: Path, inventory: dict[str, Path]) -> list[dict]:
    discovery = root / ".agents" / "skills"
    for parent in (root / ".agents", discovery):
        if parent.is_symlink():
            raise ValueError(f"Discovery parent may not be a symlink: {parent}")
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"Discovery parent is not a directory: {parent}")
    rows = []
    for name, source in inventory.items():
        dest = discovery / name
        if dest.is_symlink():
            state = "linked" if dest.resolve() == source else "conflicting_link"
        elif dest.exists():
            state = "copy_matches" if dest.is_dir() and files_digest(dest) == files_digest(source) else "conflicting_or_stale"
        else:
            state = "missing"
        rows.append({"name": name, "source": str(source), "destination": str(dest), "state": state})
    known = set(inventory)
    if discovery.is_dir():
        for extra in sorted(discovery.iterdir()):
            if extra.name not in known:
                rows.append({"name": extra.name, "destination": str(extra), "state": "unmanaged_extra"})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--apply", action="store_true", help="create missing entries; never replace existing entries")
    parser.add_argument("--check", action="store_true", help="return nonzero for missing or conflicting entries")
    parser.add_argument("--mode", choices=("auto", "symlink", "copy"), default="auto")
    args = parser.parse_args()
    if args.apply and args.check:
        parser.error("--apply and --check are mutually exclusive")
    root = args.root.resolve()
    try:
        inventory = sources(root)
        rows = inspect(root, inventory)
        conflicts = [r for r in rows if r["state"] in {"conflicting_link", "conflicting_or_stale"}]
        if args.apply and not conflicts:
            discovery = root / ".agents" / "skills"
            discovery.mkdir(parents=True, exist_ok=True)
            for row in rows:
                if row["state"] != "missing":
                    continue
                dest, source = Path(row["destination"]), Path(row["source"])
                if dest.exists() or dest.is_symlink():
                    raise FileExistsError(f"Destination appeared during setup: {dest}")
                if args.mode == "copy":
                    shutil.copytree(source, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                else:
                    try:
                        dest.symlink_to(os.path.relpath(source, discovery), target_is_directory=True)
                    except OSError:
                        if args.mode != "auto":
                            raise
                        shutil.copytree(source, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            rows = inspect(root, inventory)
        bad = [r for r in rows if r["state"] in {"missing", "conflicting_link", "conflicting_or_stale"}]
        print(json.dumps({"root": str(root), "applied": args.apply and not conflicts,
                          "complete": not bad, "entries": rows,
                          "note": "Unmanaged extras are preserved. Stale copies are never overwritten."},
                         ensure_ascii=False, indent=2))
        return 1 if conflicts or ((args.apply or args.check) and bad) else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc), "complete": False}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
