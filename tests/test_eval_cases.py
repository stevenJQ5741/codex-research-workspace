import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("theory_preflight", ROOT / "scripts/theory_preflight.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RouterCases(unittest.TestCase):
    def test_research_and_non_inference_cases(self):
        cases = json.loads((ROOT / "tests/real_task_cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 22)
        for case in cases:
            with self.subTest(case=case["id"]):
                result = m.run(case["prompt"], case["task_type"], knowledge_root=str(ROOT))
                self.assertEqual(result["tier"], case["expected_tier"])
                if case.get("expected_card"):
                    self.assertIn(case["expected_card"], [c["id"] for c in result["selected_theories"]])
                if case["expected_tier"] == "S0":
                    self.assertEqual(result["selected_theories"], [])


if __name__ == "__main__":
    unittest.main()
