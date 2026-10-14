#!/usr/bin/env python3
"""S0 skip, S1 verify a scoped Theory Context, S2 retrieve theory candidates.

Retrieval prepares G1-G5 applicability questions; it does not certify a model.
Only --output writes a file. Python 3.9+ and the standard library suffice.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

RISKY_TASKS = {"new-project", "experiment-design", "model-selection", "mechanism", "novelty"}
HIGH_RISK = ("新项目", "研究方案", "研究计划", "新机理", "建立机理", "提出机理", "机理分析",
             "新理论", "理论框架", "创新性", "研究空白", "实验设计", "模型选择", "从未研究",
             "因果机制", "novel mechanism", "new theory", "novelty", "first time",
             "new project", "experiment design", "model selection", "mechanism claim",
             "メカニズム", "新規性", "研究計画", "実験設計")
THEORY_TERMS = ("理论", "模型", "机理", "机制", "假设", "适用", "rve", "ifss", "dsc",
                "热导率", "载荷传递", "临界长度", "强度", "热性能", "实验方案",
                "验证方案", "解释", "原因", "theory", "model", "mechanism",
                "hypothesis", "conductivity", "strength", "validation plan")
NO_INFERENCE = ("仅重绘", "仅排版", "只翻译", "仅翻译", "重新计算峰面积", "replot only", "format only")
SCOPE_FIELDS = ("project_id", "research_question", "material_system", "model_assumptions", "boundary_conditions", "parameters")
CHANGE_FLAGS = ("material_changed", "model_changed", "boundary_changed", "contradictory_evidence")
SCIENTIFIC_CHANGE = (
    r"(?:替换|换成|改用|更换|改为).{0,24}(?:材料|基体|纤维|模型|PLA|PBS|PALF|热|强度)",
    r"(?:材料|基体|纤维|模型|PLA|PBS|PALF).{0,24}(?:替换|换成|改用|更换|改为)",
    r"(?:新|新的).{0,12}(?:材料|纤维|模型|体系|边界|验证方案)",
    r"(?:湿热老化|湿热循环|湿热处理|界面退化|界面降解|老化前后|处理前后|改性前后|温度变化|速率变化|边界条件变化)",
    r"(?:反例|反证|相反结果|矛盾证据|新证据|与.{0,24}(?:不符|不一致))",
    r"(?:制定|设计|提出).{0,24}(?:验证方案|实验方案|验证路径)",
    r"\breplac(?:e|ed|ing)\b.{0,60}\b(?:matrix|fiber|fibre|material|polymer|model)\b.{0,60}\b(?:with|to|for)\b",
    r"\b(?:hygrothermal cycl(?:e|ing)|interfacial degradation)\b",
    r"(?:根据|基于).{0,30}(?:形貌|断口|显微|观察).{0,30}(?:判定|归因|推断|认定|证明|主导)",
    r"(?:判定|归因|推断).{0,30}(?:纤维断裂|主导破坏|失效机理)",
)
MATERIAL_CODES = ("PLA", "PBS", "PALF", "PCL", "PHA", "PET", "PP", "PE")
SCOPE_REVIEW_MAX_AGE = timedelta(minutes=30)
TRANSFORM_ACTIONS = {"translation", "email", "formatting", "text_edit", "plot_redraw", "bounded_recalculation"}
SCIENCE_ACTIONS = {"bounded_analysis", "bounded_writing", "scientific_calculation", "experiment_design",
                   "model_selection", "model_applicability", "mechanism_attribution", "causal_inference",
                   "evidence_appraisal", "claim_review"}
S2_ACTIONS = SCIENCE_ACTIONS - {"bounded_analysis", "bounded_writing", "scientific_calculation"}
CHANGE_DIMENSIONS = ("material", "model", "process", "boundary", "parameter", "evidence")
DOMAIN_HINTS = {
    "mechanics": ("应力", "力学", "剪切", "强度", "断裂", "破坏", "失效", "ifss", "ilss", "stress", "shear", "fracture", "failure"),
    "thermal": ("热", "导热", "隔热", "conductivity", "fourier", "rve", "熱", "dsc"),
    "dsc": ("dsc", "差示", "熔融", "结晶", "吸热峰", "endotherm", "融解"),
    "natural_fibers": ("天然纤维", "短纤维", "纤维", "palf", "natural fiber", "natural fibre", "fiber", "fibre"),
    "composites": ("复合材料", "composite", "rve", "界面", "interphase"),
}


def present(term, text):
    term, text = term.casefold().strip(), text.casefold()
    if re.fullmatch(r"[a-z0-9 ]+", term):
        return bool(re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", text))
    return term in text


def instant(value):
    """Accept an actual timezone-aware ISO-8601 instant, never a placeholder."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo and parsed.utcoffset() is not None else None


def nonplaceholder(value):
    return (isinstance(value, str) and bool(value.strip()) and
            value.strip().casefold() not in {"unknown", "none", "null", "tbd", "待定", "未指定"})


def schema_error(value, rule, path="context"):
    """Enforce the JSON Schema keywords used by this package without extra dependencies."""
    if "const" in rule and value != rule["const"]:
        return path
    if "enum" in rule and value not in rule["enum"]:
        return path
    kinds = rule.get("type")
    if kinds:
        kinds = kinds if isinstance(kinds, list) else [kinds]
        matches = {"object": lambda v: isinstance(v, dict),
                   "array": lambda v: isinstance(v, list),
                   "string": lambda v: isinstance(v, str),
                   "boolean": lambda v: type(v) is bool,
                   "null": lambda v: v is None}
        if not any(matches[kind](value) for kind in kinds):
            return path
    if isinstance(value, dict):
        for field in rule.get("required", []):
            if field not in value:
                return path + "." + field
        for field, child in rule.get("properties", {}).items():
            if field in value:
                error = schema_error(value[field], child, path + "." + field)
                if error:
                    return error
    elif isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            return path
        for index, item in enumerate(value):
            error = schema_error(item, rule.get("items", {}), f"{path}[{index}]")
            if error:
                return error
    elif isinstance(value, str):
        if len(value) < rule.get("minLength", 0):
            return path
        if "pattern" in rule and re.fullmatch(rule["pattern"], value) is None:
            return path
        if rule.get("format") == "date-time" and instant(value) is None:
            return path
    return None


def noninferential_text_edit(query):
    lowered = query.casefold()
    scientific_action = re.search(r"(?<!不)(?:重新计算|重算|计算|拟合|预测|模拟|求解|判定|归因|推断|评价)", query)
    return (any(term in lowered for term in ("文中", "文本中", "字符串", "术语替换", "in the text", "wording only"))
            and scientific_action is None
            and not any(term in lowered for term in ("原因", "机理", "机制", "性能变化", "验证"))
            and ("解释" not in lowered or "不解释" in lowered))


def task_change_reason(query, context):
    """Task text outranks caller-supplied scope; unclear material identity fails closed."""
    text_edit = noninferential_text_edit(query)
    if not text_edit and any(re.search(pattern, query, re.IGNORECASE) for pattern in SCIENTIFIC_CHANGE):
        return "task_signals_scientific_change"
    if not text_edit and re.search(r"\breplac(?:e|ed|ing)\b.{0,48}\bwith\b", query, re.IGNORECASE):
        recorded_material = context.get("material_system", "") if isinstance(context, dict) else ""
        source_material_named = (isinstance(recorded_material, str) and
                                 any(present(code, query) and present(code, recorded_material)
                                     for code in MATERIAL_CODES))
        if scientific_judgment(query) or source_material_named:
            return "task_signals_scientific_change"
    if isinstance(context, dict) and not text_edit:
        material = context.get("material_system", "")
        if isinstance(material, str):
            named = {code for code in MATERIAL_CODES if present(code, query)}
            recorded = {code for code in MATERIAL_CODES if present(code, material)}
            if named and recorded and not named.issubset(recorded):
                return "task_material_conflicts_with_context"
    return None


def scientific_judgment(query):
    has_domain = any(present(term, query) for terms in DOMAIN_HINTS.values() for term in terms)
    inference = any(present(term, query) for term in ("解释", "原因", "影响", "验证方案", "实验方案",
                                                      "判定", "归因", "推断", "主导", "why", "explain", "cause", "validation plan"))
    return has_domain and inference and not noninferential_text_edit(query)


def validate_intent(intent, query):
    """Validate Codex's task-action assessment; this does not perform semantic analysis."""
    if intent is None:
        return "semantic_intent_missing"
    if not isinstance(intent, dict) or intent.get("schema_version") != "1.1":
        return "semantic_intent_invalid"
    if intent.get("task_sha256") != hashlib.sha256(query.encode("utf-8")).hexdigest():
        return "semantic_intent_task_mismatch"
    transforms, science = intent.get("transform_actions"), intent.get("science_actions")
    if (not isinstance(transforms, list) or not isinstance(science, list) or
            not transforms and not science or
            any(not isinstance(x, str) for x in transforms + science) or
            len(set(transforms)) != len(transforms) or len(set(science)) != len(science) or
            not set(transforms).issubset(TRANSFORM_ACTIONS) or
            not set(science).issubset(SCIENCE_ACTIONS)):
        return "semantic_intent_invalid"
    changes = intent.get("changes")
    if (not isinstance(changes, dict) or set(changes) != set(CHANGE_DIMENSIONS) or
            any(changes[key] not in {"yes", "no", "unknown"} for key in CHANGE_DIMENSIONS) or
            intent.get("theory_relevance") not in {"none", "bounded", "new_or_changed", "uncertain"} or
            intent.get("uncertainty") not in {"none", "intent", "scope", "evidence"} or
            type(intent.get("evidence_checked")) is not bool or
            type(intent.get("high_impact_claim")) is not bool):
        return "semantic_intent_invalid"
    segments = intent.get("task_segments")
    if (not isinstance(segments, list) or not segments or
            any(not isinstance(segment, dict) or set(segment) != {"kind", "text"} or
                segment["kind"] not in {"instruction", "content"} or
                not isinstance(segment["text"], str) or not segment["text"]
                for segment in segments) or
            segments[0]["kind"] != "instruction" or
            "".join(segment["text"] for segment in segments) != query or
            intent.get("segmentation_status") not in {"clear", "uncertain"}):
        return "semantic_intent_segments_invalid"
    return None


def instruction_surface(query, segments=None):
    """Inspect only requested actions; quoted material is a fallback mask."""
    if segments is not None:
        query = " ".join(segment["text"] for segment in segments
                         if segment["kind"] == "instruction")
    return re.sub(r'“[^”]*”|「[^」]*」|『[^』]*』|‘[^’]*’|"[^\"]*"|\'[^\']*\'',
                  ' ', query)


def explicit_scientific_request(query, pure_transform=False, segments=None):
    """Guard independent user-requested actions, not words in quoted material."""
    surface = instruction_surface(query, segments)
    compound = re.search(
        r"(?:并|同时|还要|然后|再|以及|\band\b|\bthen\b|\balso\b).{0,64}"
        r"(?:重新计算|计算|分析|讨论|解释|判断|评价|比较|选择|设计|验证|归因|推断|"
        r"recalculat\w*|analy[sz]\w*|discuss|explain|evaluat\w*|compar\w*|design|select)",
        surface, re.IGNORECASE)
    if compound:
        return True
    if re.match(r"^\s*(?:请)?(?:仅|只)?(?:翻译|重绘|排版|润色|修改邮件|把文中|将文中|translate|replot|format|in the text)", surface, re.IGNORECASE):
        return False
    if re.match(r"^\s*(?:请)?(?:比较|判断|评价|选择|重新设计|设计|分析|解释|验证|"
                r"(?:根据|基于).{0,64}(?:判定|归因|分析|讨论|解释|评价)|"
                r"compare|evaluate|choose|determine|explain|design)", surface, re.IGNORECASE):
        return True
    if pure_transform:
        return False  # Domain words in the material being translated are content, not task actions.
    return "是否导致" in surface or "是否支持" in surface or task_change_reason(surface, None) is not None


def clear_bounded_transform(query):
    if explicit_scientific_request(query):
        return False
    return bool(re.match(r"^\s*(?:请)?(?:仅|只)?(?:翻译|translate|重绘|排版|润色邮件|修改日语邮件|"
                         r"帮我修改日语邮件|调整图片排版|把文中|将文中|in the text)", query, re.IGNORECASE)
                or "重新计算峰面积" in query and "并" not in query and "同时" not in query)


def root_of(explicit=None):
    return Path(explicit).expanduser().resolve() if explicit else Path(__file__).resolve().parent.parent


def revision(root):
    try:
        p = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=4, check=False)
        value = p.stdout.strip()
        return value if p.returncode == 0 and re.fullmatch(r"[a-f0-9]{40}", value) else None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def read_index(root):
    records = json.loads((root / "docs/knowledge/INDEX.json").read_text(encoding="utf-8"))["records"]
    if not isinstance(records, list):
        raise ValueError("INDEX.json records must be an array")
    return records


def index_record_digest(record):
    """Hash the complete normalized record, including sources and limitations."""
    canonical = json.dumps(record, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def card_path(root, relative):
    base = (root / "docs/knowledge").resolve()
    path = (base / relative).resolve()
    if not path.is_relative_to(base) or not path.is_file():
        raise ValueError("Card path missing or outside knowledge root: " + str(relative))
    return path


def validate_context(context, scope, root, query):
    """Read only index metadata and recorded cards; perform no candidate search."""
    if not isinstance(context, dict):
        return False, "context_missing"
    if not isinstance(scope, dict):
        return False, "current_scope_missing"
    if context.get("schema_version") != "0.2.2":
        return False, "context_schema_mismatch"
    if context.get("example_only"):
        return False, "example_context_not_reusable"
    try:
        schema = json.loads((root / "docs/knowledge/THEORY_CONTEXT.schema.json").read_text(encoding="utf-8"))
        error = schema_error(context, schema)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return False, "context_schema_unavailable:" + type(exc).__name__
    if error:
        return False, "context_schema_invalid:" + error
    now = datetime.now(timezone.utc)
    generated, reviewed = instant(context["generated_at"]), instant(context["reviewed_at"])
    if (reviewed is None or generated is None or generated > reviewed or
            reviewed > now + timedelta(minutes=5) or not nonplaceholder(context["reviewed_by"])):
        return False, "context_review_metadata_invalid"
    receipt = context["review_record"]
    if (not isinstance(receipt, dict) or receipt.get("decision") != "scope_reviewed" or
            receipt.get("limitations_checked") is not True or
            receipt.get("conflicts_checked") is not True or
            not isinstance(receipt.get("basis_refs"), list) or
            not receipt["basis_refs"] or not all(nonplaceholder(x) for x in receipt["basis_refs"])):
        return False, "context_review_record_invalid"
    if any(scope.get(flag) for flag in CHANGE_FLAGS) or scope.get("new_conflicting_evidence"):
        return False, "material_model_boundary_or_evidence_changed"
    if context.get("conflicts"):
        return False, "context_has_unresolved_conflict"
    for field in ("conflicts", "unresolved_issues"):
        if field not in context or not isinstance(context[field], list):
            return False, "context_field_missing:" + field
    if any(item.get("blocking") for item in context.get("unresolved_issues", []) if isinstance(item, dict)):
        return False, "context_has_blocking_issue"
    for field in SCOPE_FIELDS:
        if field not in scope or field not in context:
            return False, "scope_field_missing:" + field
        if scope[field] != context[field]:
            return False, "scope_changed:" + field
    if not isinstance(context["applicability"], dict) or context["applicability"].get("status") not in {"applicable", "conditional"}:
        return False, "applicability_not_reusable"
    review = scope.get("scope_review")
    if not isinstance(review, dict):
        return False, "current_task_scope_review_missing"
    checked = instant(review.get("checked_at"))
    if (checked is None or checked < reviewed or checked > now + timedelta(minutes=5) or
            not nonplaceholder(review.get("checked_by")) or
            review.get("query_sha256") != hashlib.sha256(query.encode("utf-8")).hexdigest() or
            not isinstance(review.get("fields_confirmed_unchanged"), list) or
            not all(isinstance(x, str) for x in review["fields_confirmed_unchanged"]) or
            set(review["fields_confirmed_unchanged"]) != set(SCOPE_FIELDS) or
            len(review["fields_confirmed_unchanged"]) != len(SCOPE_FIELDS) or
            review.get("contradictory_evidence_checked") is not True or
            not isinstance(review.get("evidence_refs"), list) or not review["evidence_refs"] or
            not all(nonplaceholder(x) for x in review["evidence_refs"])):
        return False, "current_task_scope_review_invalid"
    if checked < now - SCOPE_REVIEW_MAX_AGE:
        return False, "current_task_scope_review_expired"
    cards = context.get("theory_cards")
    if not isinstance(cards, list) or not cards:
        return False, "context_cards_missing"
    if len({selected["id"] for selected in cards}) != len(cards):
        return False, "context_card_ids_duplicated"
    try:
        records = {r["id"]: r for r in read_index(root)}
        for selected in cards:
            record = records.get(selected["id"])
            if record is None:
                return False, "card_missing:" + selected["id"]
            if record["review_status"] in {"disputed", "retired"}:
                return False, "card_not_reusable:" + selected["id"]
            if selected["index_record_sha256"] != index_record_digest(record):
                return False, "index_record_changed:" + selected["id"]
            if selected["path"] != record["path"] or selected["review_status"] != record["review_status"]:
                return False, "card_identity_changed:" + selected["id"]
            if not record["sources"]:
                return False, "card_sources_missing:" + selected["id"]
            checked = all(s.get("claim_in_source_checked") is True for s in record["sources"])
            if selected.get("source_claims_checked") is not checked:
                return False, "source_review_changed:" + selected["id"]
            digest = hashlib.sha256(card_path(root, record["path"]).read_bytes()).hexdigest()
            if selected["card_sha256"] != digest:
                return False, "card_hash_changed:" + selected["id"]
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return False, "context_identity_unavailable:" + type(exc).__name__
    return True, "context_valid"


def select(records, query, domain, limit, root):
    found = []
    inferred = {d for d, terms in DOMAIN_HINTS.items() if any(present(t, query) for t in terms)}
    for record in records:
        domains = set(record.get("domains", []))
        matches = [t for t in record.get("keywords", []) if present(t, query)]
        score = min(6, len(matches) * 2) + len(inferred & domains)
        if domain in domains:
            score += 4
        if domain and domain not in domains and not matches:
            score = 0
        if not matches and domain not in domains and len(inferred & domains) < 2:
            continue  # a single broad domain hint is not enough to offer a card
        if score < 1:
            continue
        path = card_path(root, record["path"])
        found.append({
            "id": record["id"], "title": record["title"], "file": str(path.relative_to(root)),
            "review_status": record["review_status"], "epistemic_type": record["epistemic_type"],
            "matching_keywords": matches, "score": score,
            "assumptions_to_check": record["assumptions_checklist"],
            "limitations": record["known_limitations"], "sources": record["sources"],
            "card_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "index_record_sha256": index_record_digest(record),
            "applicability_checklist": [{"condition": c, "status": "unreviewed"}
                                        for c in record["assumptions_checklist"]],
        })
    return sorted(found, key=lambda x: (-x["score"], x["id"]))[:limit]


def run(query, task_type="auto", domain=None, knowledge_root=None, limit=5,
        theory_context=None, current_scope=None, manual_trigger=False, requires_theory=None,
        intent=None):
    if not 1 <= limit <= 25:
        raise ValueError("limit must be 1..25")
    intent_error = validate_intent(intent, query)
    guard = explicit_scientific_request(query, pure_transform=(not intent_error and
        bool(intent["transform_actions"]) and not intent["science_actions"] and
        intent["theory_relevance"] == "none"),
        segments=intent["task_segments"] if not intent_error else None)
    post_content_instruction = (not intent_error and bool(intent["transform_actions"]) and
        not intent["science_actions"] and intent["theory_relevance"] == "none" and
        any(segment["kind"] == "instruction" and
            any(previous["kind"] == "content" for previous in intent["task_segments"][:index])
            for index, segment in enumerate(intent["task_segments"])))
    context_status, root = "not_checked", None
    if manual_trigger:
        tier, reason = "S2", "manual_theory_request"
    elif task_type in RISKY_TASKS or requires_theory is True:
        tier, reason = "S2", "explicit_theory_risk"
    elif post_content_instruction:
        tier, reason = "S2", "post_content_instruction_requires_review"
    elif guard:
        tier, reason = "S2", "explicit_scientific_action_guard"
    elif intent_error:
        if intent_error == "semantic_intent_missing" and clear_bounded_transform(query):
            tier, reason = "S0", "bounded_transform_fallback"
        else:
            tier, reason = "S2", intent_error
    else:
        science = set(intent["science_actions"])
        changes = intent["changes"]
        relevance = intent["theory_relevance"]
        if intent["segmentation_status"] == "uncertain":
            tier, reason = "S2", "instruction_content_boundary_uncertain"
        elif intent["uncertainty"] != "none":
            tier, reason = "S2", "semantic_intent_uncertain"
        elif any(value != "no" for value in changes.values()):
            tier, reason = "S2", "semantic_scope_or_evidence_change"
        elif science & S2_ACTIONS or relevance == "new_or_changed":
            tier, reason = "S2", "semantic_scientific_review_required"
        elif relevance == "uncertain":
            tier, reason = "S2", "semantic_theory_relevance_uncertain"
        elif not science and relevance == "none" and not intent["high_impact_claim"]:
            tier, reason = "S0", "semantic_transform_only"
        elif science and relevance == "bounded":
            if not intent["evidence_checked"]:
                tier, reason = "S2", "current_evidence_not_reviewed"
            else:
                root = root_of(knowledge_root)
                valid, context_status = validate_context(theory_context, current_scope, root, query)
                if valid and intent["high_impact_claim"] and any(
                        card["review_status"] != "reviewed" or not card["source_claims_checked"]
                        for card in theory_context["theory_cards"]):
                    valid, context_status = False, "high_impact_source_review_required"
                tier, reason = ("S1", "valid_context_reused") if valid else ("S2", context_status)
        else:
            tier, reason = "S2", "semantic_intent_inconsistent"

    out = {
        "schema_version": "0.2.2", "router_version": "B-Final-boundary-fix",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task": query, "task_type": task_type, "tier": tier, "route_reason": reason,
        "intent_status": "validated" if not intent_error else "missing" if intent is None else "invalid",
        "routing_uncertain": bool(intent_error) or reason in {
            "semantic_intent_uncertain", "semantic_theory_relevance_uncertain", "semantic_intent_inconsistent",
            "instruction_content_boundary_uncertain", "post_content_instruction_requires_review"},
        "context_status": context_status, "scientific_applicability_evaluated": False,
        "overall_status": "not_required" if tier == "S0" else "context_reused" if tier == "S1" else "unresolved",
        "selected_theories": [], "reused_context": None, "knowledge_base_commit": None,
        "knowledge_coverage_gap": False, "required_next_step": "No theory preflight required" if tier == "S0" else "",
    }
    if tier == "S0":
        return out
    root = root or root_of(knowledge_root)
    if tier == "S1":
        out["reused_context"] = {
            "project_id": theory_context["project_id"], "research_question": theory_context["research_question"],
            "theory_card_ids": [c["id"] for c in theory_context["theory_cards"]],
            "theory_cards": [{"id": c["id"], "review_status": c["review_status"],
                              "source_claims_checked": c["source_claims_checked"],
                              "card_sha256": c["card_sha256"],
                              "index_record_sha256": c["index_record_sha256"]}
                             for c in theory_context["theory_cards"]],
            "reviewed_at": theory_context["reviewed_at"], "applicability": theory_context["applicability"],
        }
        out["required_next_step"] = ("Use only within the reviewed scope; preserve each card's source-review status. "
                                     "Recheck when material, model, boundaries, parameters or evidence change.")
        return out
    try:
        out["selected_theories"] = select(read_index(root), query, domain, limit, root)
        out["knowledge_base_commit"] = revision(root)
        if not out["selected_theories"]:
            out["overall_status"] = "coverage_gap"
            out["knowledge_coverage_gap"] = True
            out["required_next_step"] = "No indexed match. Broaden source search; do not infer theory absence or novelty."
        else:
            out["required_next_step"] = (
                "Review exact sources and G1-G5 applicability against project facts. "
                "Checklist conditions remain unreviewed until scientific review."
            )
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        out["overall_status"] = "knowledge_unavailable"
        out["required_next_step"] = f"Knowledge layer unavailable/invalid: {type(exc).__name__}: {exc}; no completed theory audit."
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", required=True)
    p.add_argument("--task-type", choices=["auto", "routine", "analysis", "manuscript", *sorted(RISKY_TASKS)], default="auto")
    p.add_argument("--domain")
    p.add_argument("--knowledge-root")
    p.add_argument("--theory-context", type=Path)
    p.add_argument("--scope-file", type=Path)
    p.add_argument("--intent-file", type=Path, help="Codex-assessed task intent JSON bound to exact --query")
    p.add_argument("--manual-trigger", action="store_true")
    p.add_argument("--requires-theory", choices=["auto", "yes", "no"], default="auto")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--output", type=Path, help="Explicit JSON output path; otherwise stdout only")
    a = p.parse_args()
    try:
        context = json.loads(a.theory_context.read_text(encoding="utf-8")) if a.theory_context else None
        scope = json.loads(a.scope_file.read_text(encoding="utf-8")) if a.scope_file else None
        intent = json.loads(a.intent_file.read_text(encoding="utf-8")) if a.intent_file else None
        required = None if a.requires_theory == "auto" else a.requires_theory == "yes"
        out = run(a.query, a.task_type, a.domain, a.knowledge_root, a.limit,
                  context, scope, a.manual_trigger, required, intent)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        p.error(str(exc))
    content = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if a.output:
        if not a.output.parent.is_dir():
            p.error("--output parent directory does not exist")
        a.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 2 if out["overall_status"] == "knowledge_unavailable" else 0


if __name__ == "__main__":
    raise SystemExit(main())
