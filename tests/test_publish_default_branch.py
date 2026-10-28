"""Guard publication against divergence, dirty state, and missed promotion."""
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/publish_default_branch.py"
spec = importlib.util.spec_from_file_location("publisher", SCRIPT)
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class PublicationTests(unittest.TestCase):
    def simulate(self, *, apply=True, dirty=False, ancestor=True, moving_default=False):
        state = {"default": "old", "old": "a" * 40, "new": None,
                 "head": "b" * 40, "mutations": []}
        def invoke(command, root, env, check=True):
            name, *args = command
            if name == "git":
                if args[:2] == ["status", "--porcelain"]: return " M file" if dirty else ""
                if args[0] == "symbolic-ref" and "--short" in args: return "new"
                if args[:2] == ["rev-parse", "--verify"]: return state["head"]
                if args[:2] == ["remote", "get-url"]: return "https://github.com/example/repo.git"
                if args[:2] == ["ls-remote", "--heads"]:
                    branch = args[-1].removeprefix("refs/heads/")
                    sha = state[branch]
                    return f"{sha}\trefs/heads/{branch}" if sha else ""
                if args[:2] == ["merge-base", "--is-ancestor"]:
                    return subprocess.CompletedProcess(command, 0 if ancestor else 1)
                if args[0] == "push":
                    state["mutations"].append("push")
                    state["new"] = state["head"]
                    if moving_default: state["old"] = "c" * 40
                    return ""
                if args[0] == "symbolic-ref":
                    state["mutations"].append("local_head")
                    return ""
            if name == "gh":
                if args[:2] == ["repo", "view"]: return json.dumps({"nameWithOwner": "example/repo"})
                if args[0] == "api" and "--method" in args:
                    state["mutations"].append("promote")
                    state["default"] = "new"
                    return "{}"
                if args[0] == "api": return json.dumps({"default_branch": state["default"]})
            raise AssertionError(command)
        argv = ["publisher"] + (["--apply"] if apply else [])
        with patch.object(sys, "argv", argv), patch.object(publisher, "run", side_effect=invoke), \
             patch.object(publisher, "proxy_environment", return_value={}), contextlib.redirect_stdout(io.StringIO()):
            try:
                publisher.main()
                error = None
            except RuntimeError as exc:
                error = str(exc)
        return state, error

    def test_preview_does_not_change_remote(self):
        state, error = self.simulate(apply=False)
        self.assertIsNone(error)
        self.assertEqual(state["mutations"], [])

    def test_new_branch_is_pushed_and_promoted(self):
        state, error = self.simulate()
        self.assertIsNone(error)
        self.assertEqual(state["default"], "new")
        self.assertEqual(state["mutations"], ["push", "promote", "local_head"])

    def test_dirty_and_unrelated_histories_stop_before_push(self):
        for kwargs in ({"dirty": True}, {"ancestor": False}):
            with self.subTest(kwargs=kwargs):
                state, error = self.simulate(**kwargs)
                self.assertIsNotNone(error)
                self.assertEqual(state["mutations"], [])

    def test_default_advancing_after_push_prevents_promotion(self):
        state, error = self.simulate(moving_default=True)
        self.assertIn("advanced", error)
        self.assertEqual(state["mutations"], ["push"])
        self.assertEqual(state["default"], "old")


if __name__ == "__main__":
    unittest.main()
