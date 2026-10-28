#!/usr/bin/env python3
"""Publish the current committed branch and make it GitHub's default branch.

Without --apply, validate and print a plan only. This tool never commits, force
pushes, deletes branches, changes credentials, or changes global proxy settings.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def proxy_environment():
    env = os.environ.copy()
    if sys.platform != "win32" or env.get("HTTPS_PROXY") or env.get("https_proxy"):
        return env
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings") as key:
            enabled = winreg.QueryValueEx(key, "ProxyEnable")[0]
            server = winreg.QueryValueEx(key, "ProxyServer")[0]
        if enabled and re.fullmatch(r"(?:127\.0\.0\.1|localhost):[0-9]{1,5}", server):
            env["HTTPS_PROXY"] = "http://" + server
            env.setdefault("HTTP_PROXY", "http://" + server)
    except (OSError, ImportError):
        pass
    return env


def run(command, root, env, check=True):
    result = subprocess.run(command, cwd=root, env=env, text=True,
                            encoding="utf-8", errors="replace",
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and result.returncode:
        raise RuntimeError(f"{command[0]} failed (exit {result.returncode}): {result.stderr.strip()}")
    return result.stdout.strip() if check else result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="push and set the published branch as default")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root, normally inferred from script location")
    args = parser.parse_args()
    root = args.root.resolve()
    env = proxy_environment()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GH_PROMPT_DISABLED"] = "1"
    git = lambda *a: run(["git", *a], root, env)
    gh = lambda *a: run(["gh", *a], root, env)
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise RuntimeError("Worktree or index is not clean. Review and commit intended changes first.")
    branch = git("symbolic-ref", "--quiet", "--short", "HEAD")
    head = git("rev-parse", "--verify", "HEAD")
    url = git("remote", "get-url", "origin")
    if not re.match(r"(?i)^https://github\.com/", url) and not re.match(r"(?i)^git@github\.com:", url):
        raise RuntimeError("origin must point to github.com.")
    repo = json.loads(gh("repo", "view", url, "--json", "nameWithOwner"))["nameWithOwner"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise RuntimeError("GitHub repository name is invalid.")
    info = json.loads(gh("api", f"repos/{repo}"))
    previous = info["default_branch"]
    if not previous:
        raise RuntimeError("Cannot determine the current GitHub default branch.")

    def remote_sha(name):
        value = git("ls-remote", "--heads", "origin", "refs/heads/" + name)
        return value.split()[0] if value else None

    previous_sha = remote_sha(previous)
    if not previous_sha:
        raise RuntimeError("Cannot determine the default branch tip.")
    ancestor = run(["git", "merge-base", "--is-ancestor", previous_sha, head], root, env, check=False)
    if ancestor.returncode:
        raise RuntimeError("The current commit does not contain the remote default, or its history is unavailable locally. Fetch and review before publishing.")
    target_before = remote_sha(branch)
    print(json.dumps({"repository": repo, "branch": branch, "commit": head,
                      "current_default": previous, "current_default_commit": previous_sha,
                      "remote_branch_commit": target_before, "apply": args.apply}, indent=2))
    if not args.apply:
        print("Preview only; use --apply after review to push and update the default.")
        return
    if remote_sha(previous) != previous_sha or remote_sha(branch) != target_before:
        raise RuntimeError("Remote branch changed during preflight; review and retry.")
    git("push", "origin", f"HEAD:refs/heads/{branch}")
    if remote_sha(branch) != head:
        raise RuntimeError("Push completed, but the remote branch tip differs from the intended commit.")
    current = json.loads(gh("api", f"repos/{repo}"))["default_branch"]
    if current != previous:
        raise RuntimeError("GitHub default changed during publication; inspect it before promotion.")
    if previous != branch:
        if remote_sha(previous) != previous_sha:
            raise RuntimeError("Previous default advanced during publication; inspect it before promotion.")
        gh("api", "--method", "PATCH", f"repos/{repo}", "-f", "default_branch=" + branch)
    if json.loads(gh("api", f"repos/{repo}"))["default_branch"] != branch or remote_sha(branch) != head:
        raise RuntimeError("Post-publication verification failed; inspect GitHub before retrying.")
    git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/" + branch)
    print("Published and verified GitHub default:", branch, head)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as exc:
        print("Publication stopped:", exc, file=sys.stderr)
        sys.exit(1)
