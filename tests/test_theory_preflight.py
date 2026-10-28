"""Deterministic routing tests; no test proves scientific validity or live Codex activation."""
import copy
import hashlib
import importlib.util
import json
from datetime import datetime, timedelta, timezone
from contextlib import contextmanager
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("theory_preflight", ROOT / "scripts/theory_preflight.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
KNOWLEDGE = ROOT


@contextmanager
def isolated_dir():
    with tempfile.TemporaryDirectory(prefix="theory-routing-test-") as directory:
        yield directory


def valid_context():
    scope = {
        "project_id": "synthetic-short-fiber-test",
        "research_question": "短纤维界面载荷传递的条件性解释",
        "material_system": "synthetic PBS/short fiber",
        "model_assumptions": ["simplified axial load transfer"],
        "boundary_conditions": {"loading": "uniaxial tension"},
        "parameters": {"interface_parameter": "model-defined, not measured IFSS"},
    }
    record = next(r for r in m.read_index(KNOWLEDGE) if r["id"] == "MAT-MECH-001")
    card = m.card_path(KNOWLEDGE, record["path"])
    context = {
        "schema_version": "0.2.2", **copy.deepcopy(scope),
        "theory_cards": [{
            "id": record["id"], "path": record["path"],
            "card_sha256": hashlib.sha256(card.read_bytes()).hexdigest(),
            "index_record_sha256": m.index_record_digest(record),
            "review_status": "candidate", "source_claims_checked": False,
        }],
        "applicability": {"status": "conditional", "scope": "synthetic test scope", "limitations": ["source passage pending"]},
        "conflicts": [], "unresolved_issues": [],
        "generated_at": "2026-10-09T08:00:00+08:00",
        "reviewed_at": "2026-10-09T08:01:00+08:00",
        "reviewed_by": "synthetic-test-fixture; not a scientific reviewer",
        "review_record": {"decision": "scope_reviewed", "basis_refs": ["synthetic fixture only"],
                          "limitations_checked": True, "conflicts_checked": True},
        "reuse_conditions": ["scope and selected hashes unchanged"],
        "invalidation_conditions": ["material, model, boundary, card or evidence changes"],
    }
    return context, scope


def reviewed_scope(scope, query):
    scope = copy.deepcopy(scope)
    scope["scope_review"] = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "checked_by": "synthetic-test-fixture",
        "query_sha256": hashlib.sha256(query.encode("utf-8")).hexdigest(),
        "fields_confirmed_unchanged": list(m.SCOPE_FIELDS),
        "contradictory_evidence_checked": True,
        "evidence_refs": ["synthetic current-task evidence"],
    }
    return scope


def semantic_intent(query, science=None, transform=None, changes=None,
                    relevance="bounded", evidence_checked=True, high_impact=False,
                     uncertainty="none", segments=None, segmentation_status="clear"):
    return {
        "schema_version": "1.1", "task_sha256": hashlib.sha256(query.encode("utf-8")).hexdigest(),
        "task_segments": segments if segments is not None else [{"kind": "instruction", "text": query}],
        "segmentation_status": segmentation_status,
        "transform_actions": transform if transform is not None else [],
        "science_actions": science if science is not None else ["bounded_analysis"],
        "changes": {field: (changes or {}).get(field, "no") for field in m.CHANGE_DIMENSIONS},
        "theory_relevance": relevance, "uncertainty": uncertainty,
        "evidence_checked": evidence_checked, "high_impact_claim": high_impact,
    }


class RoutingTests(unittest.TestCase):
    def test_new_mechanism_analysis_is_s2(self):
        out = m.run("分析短纤维复合材料的新机理", "analysis", knowledge_root=str(KNOWLEDGE))
        self.assertEqual(out["tier"], "S2")

    def test_new_theory_manuscript_is_s2(self):
        out = m.run("撰写新理论的论文并判断创新性", "manuscript", knowledge_root=str(KNOWLEDGE))
        self.assertEqual(out["tier"], "S2")

    def test_routine_label_cannot_suppress_risk(self):
        out = m.run("建立短纤维载荷传递新机理", "routine", knowledge_root=str(KNOWLEDGE))
        self.assertEqual(out["tier"], "S2")
        self.assertIn("MAT-MECH-001", [c["id"] for c in out["selected_theories"]])

    def test_s0_does_not_read_library(self):
        with mock.patch.object(m, "read_index", side_effect=AssertionError("library was opened")):
            for query in ("请帮我修改日语邮件", "仅调整图片排版", "翻译这段日文行政说明"):
                with self.subTest(query=query):
                    out = m.run(query, "auto", knowledge_root="Z:/missing-library")
                    self.assertEqual(out["tier"], "S0")
                    self.assertEqual(out["overall_status"], "not_required")

    def test_valid_context_is_s1_without_candidate_search(self):
        context, scope = valid_context()
        query = "沿用现有短纤维模型解释结果"
        with mock.patch.object(m, "select", side_effect=AssertionError("full candidate search")):
            out = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                        theory_context=context, current_scope=reviewed_scope(scope, query),
                        intent=semantic_intent(query))
        self.assertEqual(out["tier"], "S1")
        self.assertEqual(out["selected_theories"], [])
        self.assertEqual(out["reused_context"]["theory_card_ids"], ["MAT-MECH-001"])
        self.assertEqual(out["reused_context"]["theory_cards"][0]["review_status"], "candidate")
        self.assertFalse(out["reused_context"]["theory_cards"][0]["source_claims_checked"])
        self.assertFalse(out["scientific_applicability_evaluated"])

    def test_missing_or_changed_context_upgrades_to_s2(self):
        context, scope = valid_context()
        query = "沿用短纤维模型解释强度"
        missing = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE), current_scope=scope,
                        intent=semantic_intent(query))
        self.assertEqual(missing["tier"], "S2")
        changed = copy.deepcopy(scope)
        changed["material_system"] = "changed fiber/matrix"
        out = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                    theory_context=context, current_scope=changed, intent=semantic_intent(query))
        self.assertEqual(out["tier"], "S2")
        self.assertIn("scope_changed", out["route_reason"])

    def test_new_conflicting_evidence_upgrades_to_s2(self):
        context, scope = valid_context()
        scope["contradictory_evidence"] = True
        out = m.run("沿用短纤维模型解释强度", "analysis", knowledge_root=str(KNOWLEDGE),
                    theory_context=context, current_scope=scope)
        self.assertEqual(out["tier"], "S2")

    def test_card_hash_or_status_change_invalidates_context(self):
        context, scope = valid_context()
        query = "沿用短纤维模型解释强度"
        context["theory_cards"][0]["card_sha256"] = "0" * 64
        out = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                    theory_context=context, current_scope=reviewed_scope(scope, query),
                    intent=semantic_intent(query))
        self.assertEqual(out["tier"], "S2")
        self.assertIn("card_hash_changed", out["route_reason"])

    def test_pending_example_cannot_pass_s1(self):
        example = json.loads((ROOT / "examples/theory_context_short_fiber_candidate.json").read_text(encoding="utf-8"))
        scope = {key: example[key] for key in m.SCOPE_FIELDS}
        out = m.run("沿用短纤维模型", "analysis", knowledge_root=str(KNOWLEDGE),
                    theory_context=example, current_scope=scope,
                    intent=semantic_intent("沿用短纤维模型"))
        self.assertEqual(out["tier"], "S2")
        self.assertEqual(out["route_reason"], "example_context_not_reusable")

    def test_five_reported_misroutes_are_s2(self):
        for query in (
            "用 PLA 替换 PBS 并解释复合材料热性能变化",
            "比较湿热老化前后强度变化及其原因",
            "为新的天然纤维材料制定验证方案",
        ):
            with self.subTest(query=query):
                self.assertEqual(m.run(query, knowledge_root=str(KNOWLEDGE))["tier"], "S2")
        context, scope = valid_context()
        for query in (
            "将 PBS 换成 PLA，继续沿用旧短纤维模型",
            "出现新的反例证据，但继续沿用旧模型",
        ):
            with self.subTest(query=query):
                out = m.run(query, "routine", knowledge_root=str(KNOWLEDGE),
                            theory_context=context, current_scope=reviewed_scope(scope, query))
                self.assertEqual(out["tier"], "S2")
                self.assertNotEqual(out["route_reason"], "valid_context_reused")

    def test_mixed_text_edit_and_scientific_recalculation_is_s2(self):
        query = "把文中的 PBS 换成 PLA，同时重新计算热导率"
        for required in (None, False):
            with self.subTest(requires_theory=required):
                out = m.run(query, "routine", knowledge_root=str(KNOWLEDGE),
                            requires_theory=required)
                self.assertEqual(out["tier"], "S2")

    def test_english_matrix_change_overrides_stale_scope(self):
        context, scope = valid_context()
        for query in ("Replace the PBS matrix with TPU and explain the short-fiber strength",
                      "Replace PBS with TPU and explain short-fiber strength"):
            with self.subTest(query=query):
                out = m.run(query, "routine", knowledge_root=str(KNOWLEDGE),
                            theory_context=context, current_scope=reviewed_scope(scope, query))
                self.assertEqual(out["tier"], "S2")
                self.assertNotEqual(out["route_reason"], "valid_context_reused")

    def test_hygrothermal_interface_degradation_overrides_stale_scope(self):
        context, scope = valid_context()
        query = "针对湿热循环导致的界面退化沿用旧模型"
        out = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                    theory_context=context, current_scope=reviewed_scope(scope, query))
        self.assertEqual(out["tier"], "S2")
        self.assertNotEqual(out["route_reason"], "valid_context_reused")

    def test_morphology_based_failure_attribution_is_s2(self):
        query = "根据形貌观察判定纤维断裂主导破坏"
        out = m.run(query, "auto", knowledge_root=str(KNOWLEDGE))
        self.assertEqual(out["tier"], "S2")

    def test_old_task_scope_review_cannot_pass_s1(self):
        context, scope = valid_context()
        query = "沿用现有短纤维模型解释结果"
        stale = reviewed_scope(scope, query)
        stale["scope_review"]["checked_at"] = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        out = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                    theory_context=context, current_scope=stale, intent=semantic_intent(query))
        self.assertEqual(out["tier"], "S2")
        self.assertEqual(out["route_reason"], "current_task_scope_review_expired")

    def test_caller_cannot_mark_scientific_change_as_no_theory(self):
        out = m.run("用 PLA 替换 PBS 并解释复合材料热性能变化", "routine",
                    knowledge_root=str(KNOWLEDGE), requires_theory=False)
        self.assertEqual(out["tier"], "S2")

    def test_broad_domain_hint_does_not_add_unrelated_cards(self):
        thermal = m.run("用 PLA 替换 PBS 并解释复合材料热性能变化",
                        knowledge_root=str(KNOWLEDGE))
        self.assertEqual([c["id"] for c in thermal["selected_theories"]], ["MAT-THERM-001"])
        aging = m.run("比较湿热老化前后强度变化及其原因", knowledge_root=str(KNOWLEDGE))
        self.assertEqual(aging["tier"], "S2")
        self.assertEqual(aging["overall_status"], "coverage_gap")
        self.assertEqual(aging["selected_theories"], [])

    def test_stale_scope_review_does_not_pass_s1(self):
        context, scope = valid_context()
        query = "沿用现有短纤维模型解释结果"
        self.assertEqual(m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                               theory_context=context, current_scope=scope)["tier"], "S2")
        review = reviewed_scope(scope, "另一项任务")
        out = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                    theory_context=context, current_scope=review, intent=semantic_intent(query))
        self.assertEqual(out["route_reason"], "current_task_scope_review_invalid")

    def test_invalid_context_review_metadata_is_rejected(self):
        query = "沿用现有短纤维模型解释结果"
        for field, value in (("generated_at", "nonsense"), ("reviewed_at", "not-a-date"),
                             ("reviewed_by", "unknown"), ("review_record", None)):
            with self.subTest(field=field):
                context, scope = valid_context()
                context[field] = value
                out = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                            theory_context=context, current_scope=reviewed_scope(scope, query),
                            intent=semantic_intent(query))
                self.assertEqual(out["tier"], "S2")

    def test_schema_checks_nested_types_and_hash(self):
        query = "沿用现有短纤维模型解释结果"
        for field, value in (("model_assumptions", "not-an-array"),
                             ("theory_cards", [{"id": "MAT-MECH-001"}])):
            with self.subTest(field=field):
                context, scope = valid_context()
                context[field] = value
                out = m.run(query, "analysis", knowledge_root=str(KNOWLEDGE),
                            theory_context=context, current_scope=reviewed_scope(scope, query),
                            intent=semantic_intent(query))
                self.assertEqual(out["tier"], "S2")
                self.assertIn("context_schema_invalid", out["route_reason"])

    def test_text_substitution_without_scientific_judgment_is_s0(self):
        out = m.run("仅把文中 PBS 替换为 PLA，不解释性能", "routine", knowledge_root="Z:/missing-library")
        self.assertEqual(out["tier"], "S0")
        english = m.run("In the text, replace the PBS matrix with TPU; wording only", "routine",
                        knowledge_root="Z:/missing-library")
        self.assertEqual(english["tier"], "S0")

    def test_schema_and_pending_example_agree(self):
        schema = json.loads((KNOWLEDGE / "docs/knowledge/THEORY_CONTEXT.schema.json").read_text(encoding="utf-8"))
        example = json.loads((ROOT / "examples/theory_context_short_fiber_candidate.json").read_text(encoding="utf-8"))
        self.assertTrue(set(schema["required"]).issubset(example))
        self.assertEqual(example["theory_cards"][0]["review_status"], "candidate")
        self.assertFalse(example["theory_cards"][0]["source_claims_checked"])
        actual = hashlib.sha256(m.card_path(KNOWLEDGE, example["theory_cards"][0]["path"]).read_bytes()).hexdigest()
        self.assertEqual(example["theory_cards"][0]["card_sha256"], actual)
        record = next(r for r in m.read_index(KNOWLEDGE) if r["id"] == example["theory_cards"][0]["id"])
        self.assertEqual(example["theory_cards"][0]["index_record_sha256"], m.index_record_digest(record))

    def test_manual_request_is_s2(self):
        out = m.run("请检查现有热导率模型的理论条件", "routine", knowledge_root=str(KNOWLEDGE),
                    manual_trigger=True)
        self.assertEqual(out["tier"], "S2")
        self.assertEqual(out["route_reason"], "manual_theory_request")

    def test_no_match_is_coverage_gap(self):
        out = m.run("新项目：天体中微子振荡理论", "new-project", knowledge_root=str(KNOWLEDGE))
        self.assertEqual(out["overall_status"], "coverage_gap")
        self.assertTrue(out["knowledge_coverage_gap"])
        self.assertIn("do not infer theory absence or novelty", out["required_next_step"])

    def test_bad_index_fails_closed(self):
        with isolated_dir() as temp:
            path = Path(temp) / "docs/knowledge/INDEX.json"
            path.parent.mkdir(parents=True)
            path.write_text("{bad json", encoding="utf-8")
            out = m.run("新项目：短纤维载荷传递", "new-project", knowledge_root=temp)
            self.assertEqual(out["overall_status"], "knowledge_unavailable")
            self.assertFalse(out["scientific_applicability_evaluated"])

    def test_candidate_status_is_not_promoted(self):
        out = m.run("新项目：短纤维载荷传递", "new-project", knowledge_root=str(KNOWLEDGE))
        card = next(c for c in out["selected_theories"] if c["id"] == "MAT-MECH-001")
        self.assertEqual(card["review_status"], "candidate")
        record = next(r for r in m.read_index(KNOWLEDGE) if r["id"] == "MAT-MECH-001")
        self.assertEqual(card["index_record_sha256"], m.index_record_digest(record))
        self.assertFalse(card["sources"][0]["claim_in_source_checked"])
        self.assertTrue(all(item["status"] == "unreviewed" for item in card["applicability_checklist"]))


if __name__ == "__main__":
    unittest.main()
