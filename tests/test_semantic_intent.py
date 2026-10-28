"""Fixed multilingual task-action acceptance set; the intent labels are human fixtures."""
import copy
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from test_theory_preflight import (KNOWLEDGE, ROOT, isolated_dir, m, reviewed_scope,
                                   semantic_intent, valid_context)


CASES = (
    ("仅翻译一段讨论创新性的英文，不评价主张", "S0", [], ["translation"], "none", {}),
    ("仅翻译“新的短纤维模型”这句话", "S0", [], ["translation"], "none", {}),
    ("Translate the phrase 'a novel fiber model' only", "S0", [], ["translation"], "none", {}),
    ("新しい複合材料モデルという文を日本語に翻訳するだけ", "S0", [], ["translation"], "none", {}),
    ("请修改日语邮件措辞并排版附件", "S0", [], ["email", "formatting"], "none", {}),
    ("把文中的 PBS 换成 PLA，同时重新计算热导率", "S2", ["scientific_calculation"], ["text_edit"], "new_or_changed", {"material": "yes"}),
    ("仅重绘 DSC 曲线，并解释异常放热峰产生的原因", "S2", ["mechanism_attribution"], ["plot_redraw"], "new_or_changed", {}),
    ("比较 Halpin–Tsai 与 Mori–Tanaka 哪个更合适", "S2", ["model_selection"], [], "new_or_changed", {}),
    ("判断 Maxwell–Garnett 公式是否适合高填充率复合材料", "S2", ["model_applicability"], [], "new_or_changed", {}),
    ("判断界面热阻是否导致热导率降低", "S2", ["causal_inference"], [], "new_or_changed", {}),
    ("评价 SEM 断口是否支持界面脱粘结论", "S2", ["evidence_appraisal"], [], "new_or_changed", {}),
    ("重新设计变量验证实验", "S2", ["experiment_design"], [], "new_or_changed", {}),
    ("评价英文描述中的界面黏附机理证据", "S2", ["claim_review"], [], "new_or_changed", {}),
    ("Replace the PBS matrix with TPU and explain strength", "S2", ["causal_inference"], [], "new_or_changed", {"material": "yes"}),
    ("针对湿热循环导致的界面退化沿用旧模型", "S2", ["model_applicability"], [], "new_or_changed", {"process": "yes", "evidence": "unknown"}),
    ("PALF/PBS 三相导热模型的边界条件改变后重新预测", "S2", ["scientific_calculation"], [], "new_or_changed", {"boundary": "yes"}),
    ("DSC の異常発熱ピークの原因を説明して", "S2", ["mechanism_attribution"], [], "new_or_changed", {}),
    ("SEM 破面は界面剥離を支持するか判断して", "S2", ["evidence_appraisal"], [], "new_or_changed", {}),
)


class SemanticAcceptanceTests(unittest.TestCase):
    def test_unquoted_translation_content_is_not_an_instruction(self):
        prompts = (
            ("只翻译这段话：", "研究人员比较模型并解释实验结果"),
            ("Translate the following: ", "Researchers compare models and explain results."),
            ("仅翻译下列句子：", "作者设计实验并验证模型"),
        )
        with mock.patch.object(m, "read_index", side_effect=AssertionError("S0 opened knowledge")):
            for instruction, content in prompts:
                with self.subTest(content=content):
                    query = instruction + content
                    segments = [{"kind": "instruction", "text": instruction},
                                {"kind": "content", "text": content}]
                    intent = semantic_intent(query, science=[], transform=["translation"],
                                             relevance="none", segments=segments)
                    out = m.run(query, knowledge_root="Z:/missing-library", intent=intent)
                    self.assertEqual(out["tier"], "S0", out)
                    self.assertEqual(out["router_version"], "B-Final-boundary-fix")

    def test_scientific_action_after_unquoted_content_is_s2(self):
        instruction = "先翻译这段话："
        content = "研究人员比较模型并解释结果。"
        followup = "随后判断 DSC 异常峰产生的原因"
        query = instruction + content + followup
        segments = [{"kind": "instruction", "text": instruction},
                    {"kind": "content", "text": content},
                    {"kind": "instruction", "text": followup}]
        wrong = semantic_intent(query, science=[], transform=["translation"],
                                relevance="none", segments=segments)
        result = m.run(query, knowledge_root=str(KNOWLEDGE), intent=wrong)
        self.assertEqual(result["tier"], "S2", result)
        self.assertEqual(result["route_reason"], "post_content_instruction_requires_review")
        self.assertTrue(result["routing_uncertain"])

    def test_scientific_recalculation_and_translation_are_s2(self):
        instruction = "把文中的 PBS 换成 PLA，同时重新计算热导率："
        content = "PBS composite conductivity results"
        query = instruction + content
        intent = semantic_intent(query, science=["scientific_calculation"],
                                 transform=["text_edit"], relevance="new_or_changed",
                                 changes={"material": "yes"},
                                 segments=[{"kind": "instruction", "text": instruction},
                                           {"kind": "content", "text": content}])
        self.assertEqual(m.run(query, knowledge_root=str(KNOWLEDGE), intent=intent)["tier"], "S2")

    def test_incomplete_or_uncertain_segmentation_fails_closed(self):
        query = "只翻译这段话：研究人员比较模型并解释实验结果"
        instruction, content = query.split("：", 1)
        segments = [{"kind": "instruction", "text": instruction + "："},
                    {"kind": "content", "text": content}]
        base = semantic_intent(query, science=[], transform=["translation"],
                               relevance="none", segments=segments)
        uncertain = copy.deepcopy(base)
        uncertain["segmentation_status"] = "uncertain"
        out = m.run(query, knowledge_root=str(KNOWLEDGE), intent=uncertain)
        self.assertEqual(out["tier"], "S2")
        self.assertEqual(out["route_reason"], "instruction_content_boundary_uncertain")
        incomplete = copy.deepcopy(base)
        incomplete["task_segments"][1]["text"] = content[:-1]
        out = m.run(query, knowledge_root=str(KNOWLEDGE), intent=incomplete)
        self.assertEqual(out["tier"], "S2")
        self.assertEqual(out["intent_status"], "invalid")
        self.assertTrue(out["routing_uncertain"])
        legacy = copy.deepcopy(base)
        legacy["schema_version"] = "1.0"
        out = m.run(query, knowledge_root=str(KNOWLEDGE), intent=legacy)
        self.assertEqual(out["tier"], "S2")
        self.assertTrue(out["routing_uncertain"])

    def test_quoted_science_is_translation_content_not_action(self):
        prompts = (
            '只翻译 “The researchers compare models and explain their results.”',
            '只翻译含有“对比模型并解释结果”的研究题目',
            '仅翻译包含“设计实验并验证模型”的邮件',
        )
        with mock.patch.object(m, "read_index", side_effect=AssertionError("S0 opened knowledge")):
            for query in prompts:
                with self.subTest(query=query):
                    intent = semantic_intent(query, science=[], transform=["translation"], relevance="none")
                    out = m.run(query, knowledge_root="Z:/missing-library", intent=intent)
                    self.assertEqual(out["tier"], "S0", out)

    def test_independent_scientific_action_overrides_wrong_pure_edit_intent(self):
        prompts = (
            ("先翻译文字，再根据 SEM 图分析失效机理", "translation"),
            ("根据热导率数据讨论界面热阻", "text_edit"),
        )
        for query, transform in prompts:
            with self.subTest(query=query):
                wrong = semantic_intent(query, science=[], transform=[transform], relevance="none")
                out = m.run(query, knowledge_root=str(KNOWLEDGE), intent=wrong)
                self.assertEqual(out["tier"], "S2", out)
                self.assertEqual(out["route_reason"], "explicit_scientific_action_guard")

    def test_index_source_scope_or_limit_change_invalidates_s1(self):
        context, scope = valid_context()
        query = "沿用现有短纤维模型解释结果"
        intent = semantic_intent(query)
        original = m.run(query, knowledge_root=str(KNOWLEDGE), theory_context=context,
                         current_scope=reviewed_scope(scope, query), intent=intent)
        self.assertEqual(original["tier"], "S1")
        mutations = (
            lambda record: record["sources"][0].update(url="https://example.invalid/changed"),
            lambda record: record["known_limitations"].append("new scoped limitation"),
            lambda record: record["assumptions_checklist"].append("new applicability condition"),
        )
        for mutate in mutations:
            with self.subTest(change=mutate.__code__.co_firstlineno), isolated_dir() as temporary:
                root = Path(temporary)
                dest = root / "docs/knowledge"
                shutil.copytree(KNOWLEDGE / "docs/knowledge", dest)
                index_path = dest / "INDEX.json"
                index = json.loads(index_path.read_text(encoding="utf-8"))
                mutate(next(r for r in index["records"] if r["id"] == "MAT-MECH-001"))
                index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
                out = m.run(query, knowledge_root=str(root), theory_context=context,
                            current_scope=reviewed_scope(scope, query), intent=intent)
                self.assertEqual(out["tier"], "S2")
                self.assertEqual(out["route_reason"], "index_record_changed:MAT-MECH-001")

    def test_old_context_without_index_identity_is_not_reusable(self):
        context, scope = valid_context()
        context["theory_cards"][0].pop("index_record_sha256")
        query = "沿用现有短纤维模型解释结果"
        out = m.run(query, knowledge_root=str(KNOWLEDGE), theory_context=context,
                    current_scope=reviewed_scope(scope, query), intent=semantic_intent(query))
        self.assertEqual(out["tier"], "S2")
        self.assertIn("context_schema_invalid", out["route_reason"])

    def test_cli_consumes_exact_query_intent_file(self):
        query = "仅翻译“新的短纤维模型”这句话"
        with isolated_dir() as directory:
            path = Path(directory) / "intent.json"
            path.write_text(json.dumps(semantic_intent(query, science=[], transform=["translation"],
                                                       relevance="none"), ensure_ascii=False), encoding="utf-8")
            call = subprocess.run([sys.executable, str(ROOT / "scripts/theory_preflight.py"),
                                   "--query", query, "--intent-file", str(path),
                                   "--knowledge-root", "Z:/missing-library"],
                                  capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(call.returncode, 0, call.stderr)
            self.assertEqual(json.loads(call.stdout)["tier"], "S0")

    def test_fixed_multilingual_routes_and_s0_zero_reads(self):
        with mock.patch.object(m, "read_index", wraps=m.read_index) as index:
            for query, expected, science, transform, relevance, changes in CASES:
                with self.subTest(query=query):
                    before = index.call_count
                    intent = semantic_intent(query, science=science, transform=transform,
                                             changes=changes, relevance=relevance)
                    out = m.run(query, "routine", knowledge_root=str(KNOWLEDGE), intent=intent)
                    self.assertEqual(out["tier"], expected, out)
                    if expected == "S0":
                        self.assertEqual(index.call_count, before)

    def test_misleading_low_risk_claim_cannot_downgrade_explicit_science(self):
        query = "仅重绘 DSC 曲线，并解释异常放热峰产生的原因"
        intent = semantic_intent(query, science=[], transform=["plot_redraw"], relevance="none")
        self.assertEqual(m.run(query, "routine", knowledge_root=str(KNOWLEDGE),
                               intent=intent)["tier"], "S2")

    def test_unknown_or_stale_intent_is_uncertain_s2(self):
        query = "对这组结果做下一步处理"
        missing = m.run(query, knowledge_root=str(KNOWLEDGE))
        self.assertEqual(missing["tier"], "S2")
        self.assertTrue(missing["routing_uncertain"])
        wrong = semantic_intent("another task")
        stale = m.run(query, knowledge_root=str(KNOWLEDGE), intent=wrong)
        self.assertEqual(stale["route_reason"], "semantic_intent_task_mismatch")
        self.assertTrue(stale["routing_uncertain"])

    def test_s1_requires_current_evidence_and_candidate_remains_candidate(self):
        context, scope = valid_context()
        query = "沿用现有短纤维模型解释结果"
        current = reviewed_scope(scope, query)
        intent = semantic_intent(query)
        reused = m.run(query, knowledge_root=str(KNOWLEDGE), theory_context=context,
                       current_scope=current, intent=intent)
        self.assertEqual(reused["tier"], "S1")
        self.assertEqual(reused["reused_context"]["theory_cards"][0]["review_status"], "candidate")
        self.assertFalse(reused["scientific_applicability_evaluated"])
        unchecked = copy.deepcopy(intent)
        unchecked["evidence_checked"] = False
        self.assertEqual(m.run(query, knowledge_root=str(KNOWLEDGE), theory_context=context,
                               current_scope=current, intent=unchecked)["tier"], "S2")
        high_impact = copy.deepcopy(intent)
        high_impact["high_impact_claim"] = True
        result = m.run(query, knowledge_root=str(KNOWLEDGE), theory_context=context,
                       current_scope=current, intent=high_impact)
        self.assertEqual(result["tier"], "S2")
        self.assertEqual(result["route_reason"], "high_impact_source_review_required")

    def test_changed_scope_even_with_old_current_scope_record_is_s2(self):
        context, scope = valid_context()
        query = "沿用旧模型解释新热史后的结果"
        intent = semantic_intent(query, changes={"process": "yes"})
        out = m.run(query, knowledge_root=str(KNOWLEDGE), theory_context=context,
                    current_scope=reviewed_scope(scope, query), intent=intent)
        self.assertEqual(out["tier"], "S2")


if __name__ == "__main__":
    unittest.main()
