#!/usr/bin/env python3
"""Plan and audit a PPTX revision with the Python standard library.

The script inventories a candidate deck, optionally compares it with a baseline
at the raw OOXML-package level, enforces a validation profile, identifies the
affected slides and evidence that became stale, and recommends only the next
checks required by the mutation lane. Native PowerPoint export and full visual
release QA remain separate release-candidate steps.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}

PROFILES = (
    "custom",
    "inventory",
    "aesthetic-round",
    "controlled-revision",
    "notes-only",
    "release-candidate",
)
SLIDE_RE = re.compile(r"^ppt/slides/slide(\d+)\.xml$")
SLIDE_OR_RELS_RE = re.compile(
    r"^ppt/slides/(?:_rels/)?slide(\d+)\.xml(?:\.rels)?$"
)
NOTES_OR_RELS_RE = re.compile(
    r"^ppt/notesSlides/(?:_rels/)?notesSlide(\d+)\.xml(?:\.rels)?$"
)
WORD_RE = re.compile(r"[^\W_]+(?:[-'][^\W_]+)*", re.UNICODE)
SENTENCE_RE = re.compile(r"[^.!?]+(?:[.!?]+|$)", re.UNICODE)

VOLATILE_METADATA_PARTS = {
    "docProps/app.xml",
    "docProps/core.xml",
    "ppt/viewProps.xml",
}
GLOBAL_VISUAL_PREFIXES = (
    "ppt/theme/",
    "ppt/slideLayouts/",
    "ppt/slideMasters/",
)
GLOBAL_VISUAL_PARTS = {
    "ppt/presentation.xml",
    "ppt/presProps.xml",
    "ppt/tableStyles.xml",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_slide_set(spec: str | None) -> list[int]:
    if not spec:
        return []
    slides: set[int] = set()
    for raw_item in spec.split(","):
        item = raw_item.strip()
        if not item:
            continue
        if "-" in item:
            start_text, end_text = item.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start <= 0 or end < start:
                raise ValueError(f"Invalid slide range: {item}")
            slides.update(range(start, end + 1))
        else:
            number = int(item)
            if number <= 0:
                raise ValueError(f"Invalid slide number: {item}")
            slides.add(number)
    return sorted(slides)


def xml_root(package: zipfile.ZipFile, part: str) -> ET.Element:
    return ET.fromstring(package.read(part))


def text_runs(root: ET.Element) -> list[str]:
    return [node.text or "" for node in root.findall(".//a:t", NS) if node.text]


def slide_parts(package: zipfile.ZipFile) -> list[tuple[int, str]]:
    parts: list[tuple[int, str]] = []
    for name in package.namelist():
        match = SLIDE_RE.match(name)
        if match:
            parts.append((int(match.group(1)), name))
    return sorted(parts)


def relationship_targets(
    package: zipfile.ZipFile, source_part: str, rels_part: str
) -> list[str]:
    if rels_part not in package.namelist():
        return []
    root = xml_root(package, rels_part)
    targets: list[str] = []
    for relation in root.findall("pr:Relationship", NS):
        if relation.attrib.get("TargetMode", "").casefold() == "external":
            continue
        target = relation.attrib.get("Target", "")
        if not target:
            continue
        targets.append(
            posixpath.normpath(
                posixpath.join(posixpath.dirname(source_part), target)
            )
        )
    return sorted(set(targets))


def notes_part_for_slide(
    package: zipfile.ZipFile, slide_number: int, slide_part: str
) -> str | None:
    rels_part = f"ppt/slides/_rels/slide{slide_number}.xml.rels"
    for target in relationship_targets(package, slide_part, rels_part):
        if target.startswith("ppt/notesSlides/notesSlide"):
            return target if target in package.namelist() else None
    return None


def note_text(package: zipfile.ZipFile, note_part: str | None) -> str:
    if not note_part:
        return ""
    root = xml_root(package, note_part)
    kept: list[str] = []
    for shape in root.findall(".//p:sp", NS):
        placeholder = shape.find("./p:nvSpPr/p:nvPr/p:ph", NS)
        placeholder_type = (
            placeholder.attrib.get("type", "") if placeholder is not None else ""
        )
        if placeholder_type in {"dt", "ftr", "hdr", "sldNum"}:
            continue
        kept.extend(text_runs(shape))
    return " ".join(part.strip() for part in kept if part.strip()).strip()


def sentence_word_counts(texts: Iterable[str]) -> list[int]:
    counts: list[int] = []
    for text in texts:
        for match in SENTENCE_RE.finditer(text):
            sentence = match.group(0).strip()
            if sentence:
                counts.append(len(WORD_RE.findall(sentence)))
    return [count for count in counts if count > 0]


def presentation_size(package: zipfile.ZipFile) -> dict[str, float | int | None]:
    part = "ppt/presentation.xml"
    if part not in package.namelist():
        return {"cx": None, "cy": None, "width_inches": None, "height_inches": None}
    root = xml_root(package, part)
    size = root.find("p:sldSz", NS)
    if size is None:
        return {"cx": None, "cy": None, "width_inches": None, "height_inches": None}
    cx = int(size.attrib.get("cx", 0))
    cy = int(size.attrib.get("cy", 0))
    return {
        "cx": cx,
        "cy": cy,
        "width_inches": cx / 914400 if cx else None,
        "height_inches": cy / 914400 if cy else None,
    }


def inventory(path: Path) -> dict:
    with zipfile.ZipFile(path) as package:
        slides = slide_parts(package)
        visible_by_slide: dict[str, str] = {}
        notes_by_slide: dict[str, str] = {}
        note_parts_by_slide: dict[str, str | None] = {}
        relationships_by_slide: dict[str, list[str]] = {}
        shape_count = 0
        picture_count = 0
        chart_count = 0
        table_count = 0

        shape_tags = {
            f"{{{NS['p']}}}sp",
            f"{{{NS['p']}}}pic",
            f"{{{NS['p']}}}graphicFrame",
            f"{{{NS['p']}}}grpSp",
            f"{{{NS['p']}}}cxnSp",
        }

        for slide_number, slide_part in slides:
            root = xml_root(package, slide_part)
            visible_by_slide[str(slide_number)] = " ".join(text_runs(root)).strip()
            shape_count += sum(1 for node in root.iter() if node.tag in shape_tags)
            picture_count += len(root.findall(".//p:pic", NS))
            chart_count += len(root.findall(".//c:chart", NS))
            table_count += len(root.findall(".//a:tbl", NS))

            rels_part = f"ppt/slides/_rels/slide{slide_number}.xml.rels"
            relationships_by_slide[str(slide_number)] = relationship_targets(
                package, slide_part, rels_part
            )
            note_part = notes_part_for_slide(package, slide_number, slide_part)
            note_parts_by_slide[str(slide_number)] = note_part
            notes_by_slide[str(slide_number)] = note_text(package, note_part)

        names = set(package.namelist())
        media_parts = sorted(name for name in names if name.startswith("ppt/media/"))
        chart_parts = sorted(
            name
            for name in names
            if re.match(r"^ppt/charts/chart\d+\.xml$", name)
        )

        return {
            "path": str(path.resolve()),
            "sha256": sha256_file(path),
            "package_parts": sorted(names),
            "structure": {
                "slides": len(slides),
                "slide_size": presentation_size(package),
                "shapes": shape_count,
                "pictures": picture_count,
                "chart_instances": chart_count,
                "chart_parts": len(chart_parts),
                "tables": table_count,
                "media_parts": len(media_parts),
            },
            "visible_text_by_slide": visible_by_slide,
            "notes_by_slide": notes_by_slide,
            "note_parts_by_slide": note_parts_by_slide,
            "relationships_by_slide": relationships_by_slide,
            "all_visible_text": "\n".join(visible_by_slide.values()),
            "all_notes_text": "\n".join(notes_by_slide.values()),
        }


def package_diff(baseline: Path, candidate: Path) -> dict:
    with zipfile.ZipFile(baseline) as base_zip, zipfile.ZipFile(candidate) as candidate_zip:
        base_names = set(base_zip.namelist())
        candidate_names = set(candidate_zip.namelist())
        common = sorted(base_names & candidate_names)
        changed = [
            name for name in common if base_zip.read(name) != candidate_zip.read(name)
        ]
        return {
            "changed_parts": changed,
            "added_parts": sorted(candidate_names - base_names),
            "removed_parts": sorted(base_names - candidate_names),
        }


def all_diff_parts(diff: dict | None) -> list[str]:
    if not diff:
        return []
    return sorted(
        set(diff["changed_parts"]) | set(diff["added_parts"]) | set(diff["removed_parts"])
    )


def same_structure(left: dict, right: dict) -> bool:
    keys = (
        "slides",
        "slide_size",
        "shapes",
        "pictures",
        "chart_instances",
        "chart_parts",
        "tables",
        "media_parts",
    )
    return all(left.get(key) == right.get(key) for key in keys)


def find_terms(text: str, terms: Iterable[str]) -> list[str]:
    lowered = text.casefold()
    return [term for term in terms if term.casefold() in lowered]


def slide_number_from_part(part: str) -> int | None:
    match = SLIDE_OR_RELS_RE.match(part)
    return int(match.group(1)) if match else None


def is_global_visual_part(part: str) -> bool:
    return part in GLOBAL_VISUAL_PARTS or part.startswith(GLOBAL_VISUAL_PREFIXES)


def changed_text_slides(baseline: dict, candidate: dict, field: str) -> list[int]:
    baseline_text = baseline[field]
    candidate_text = candidate[field]
    slide_numbers = {int(key) for key in baseline_text} | {
        int(key) for key in candidate_text
    }
    return sorted(
        number
        for number in slide_numbers
        if baseline_text.get(str(number), "") != candidate_text.get(str(number), "")
    )


def classify_changes(
    diff: dict | None, baseline: dict | None, candidate: dict
) -> dict:
    parts = all_diff_parts(diff)
    direct_slide_changes: set[int] = set()
    note_part_changes: set[int] = set()
    chart_parts: list[str] = []
    media_parts: list[str] = []
    embedding_parts: list[str] = []
    metadata_parts: list[str] = []
    global_visual_parts: list[str] = []
    other_parts: list[str] = []

    for part in parts:
        slide_number = slide_number_from_part(part)
        notes_match = NOTES_OR_RELS_RE.match(part)
        if slide_number is not None:
            direct_slide_changes.add(slide_number)
        elif notes_match:
            note_part_changes.add(int(notes_match.group(1)))
        elif part.startswith("ppt/charts/"):
            chart_parts.append(part)
        elif part.startswith("ppt/media/"):
            media_parts.append(part)
        elif part.startswith("ppt/embeddings/"):
            embedding_parts.append(part)
        elif part in VOLATILE_METADATA_PARTS or part.startswith("docProps/"):
            metadata_parts.append(part)
        elif is_global_visual_part(part):
            global_visual_parts.append(part)
        else:
            other_parts.append(part)

    text_changes = (
        changed_text_slides(baseline, candidate, "visible_text_by_slide")
        if baseline
        else []
    )
    note_text_changes = (
        changed_text_slides(baseline, candidate, "notes_by_slide")
        if baseline
        else []
    )

    dependent_object_slides: set[int] = set()
    chart_slides: set[int] = set()
    relationship_maps = [candidate["relationships_by_slide"]]
    if baseline:
        relationship_maps.append(baseline["relationships_by_slide"])
    changed_set = set(parts)
    for relation_map in relationship_maps:
        for slide_text, targets in relation_map.items():
            slide_number = int(slide_text)
            if any(target.startswith("ppt/charts/") for target in targets):
                chart_slides.add(slide_number)
            visible_targets = [
                target
                for target in targets
                if not target.startswith("ppt/notesSlides/")
            ]
            if changed_set.intersection(visible_targets):
                dependent_object_slides.add(slide_number)
    if embedding_parts:
        dependent_object_slides.update(chart_slides)

    all_slides = set(range(1, candidate["structure"]["slides"] + 1))
    if global_visual_parts:
        visual_impacted = all_slides
    else:
        visual_impacted = direct_slide_changes | dependent_object_slides

    return {
        "direct_slide_changes": sorted(direct_slide_changes),
        "visible_text_changed_slides": text_changes,
        "notes_changed_slides": note_text_changes,
        "notes_package_changes": sorted(note_part_changes),
        "dependent_object_slides": sorted(dependent_object_slides),
        "visual_impacted_slides": sorted(visual_impacted),
        "chart_parts": chart_parts,
        "media_parts": media_parts,
        "embedding_parts": embedding_parts,
        "global_visual_parts": global_visual_parts,
        "volatile_metadata_parts": metadata_parts,
        "other_parts": other_parts,
        "structure_changed": (
            not same_structure(baseline["structure"], candidate["structure"])
            if baseline
            else False
        ),
    }


def part_allowed(
    part: str,
    profile: str,
    allowed_slides: set[int],
    allowed_prefixes: list[str],
    strict_metadata: bool,
) -> bool:
    if any(part.startswith(prefix) for prefix in allowed_prefixes):
        return True
    if (
        profile in {"aesthetic-round", "controlled-revision"}
        and not strict_metadata
        and part in VOLATILE_METADATA_PARTS
    ):
        return True
    slide_number = slide_number_from_part(part)
    return (
        profile in {"aesthetic-round", "controlled-revision"}
        and slide_number in allowed_slides
    )


def unexpected_scope_changes(
    diff: dict,
    profile: str,
    allowed_slides: set[int],
    allowed_prefixes: list[str],
    strict_metadata: bool,
) -> dict:
    unexpected: dict[str, list[str]] = {}
    for key in ("changed_parts", "added_parts", "removed_parts"):
        unexpected[key] = [
            part
            for part in diff[key]
            if not part_allowed(
                part,
                profile,
                allowed_slides,
                allowed_prefixes,
                strict_metadata,
            )
        ]
    return unexpected


def derive_validation_reuse(change_summary: dict, has_diff: bool) -> dict:
    if not has_diff:
        return {
            "reusable": [],
            "invalidated": [],
            "note": "No baseline comparison was performed.",
        }

    reusable: list[str] = []
    invalidated: list[str] = ["protected candidate hash and prior release identity"]

    text_changed = bool(change_summary["visible_text_changed_slides"])
    notes_changed = bool(change_summary["notes_changed_slides"])
    charts_changed = bool(
        change_summary["chart_parts"] or change_summary["embedding_parts"]
    )
    media_changed = bool(change_summary["media_parts"])
    global_visual = bool(change_summary["global_visual_parts"])
    visual_changed = bool(change_summary["visual_impacted_slides"])
    unexplained = bool(change_summary["other_parts"])

    if text_changed:
        invalidated.extend(
            [
                "scientific and semantic review for changed visible text",
                "speaker-note alignment for slides with changed visible text",
            ]
        )
    else:
        reusable.append("visible-text semantic review")
    if notes_changed:
        invalidated.append("speaker-note language, alignment, and timing review")
    else:
        reusable.append("speaker-note review")
    if charts_changed:
        invalidated.append("chart data, editability, and chart-slide visual review")
    else:
        reusable.append("chart review")
    if media_changed:
        invalidated.append("image provenance, crop, resolution, and visual review")
    else:
        reusable.append("media provenance review")
    if global_visual:
        invalidated.append("full-deck visual review")
    elif visual_changed:
        invalidated.append(
            "visual review only for the reported visual-impacted slides"
        )
    else:
        reusable.append("visual review of unchanged slide content")
    if unexplained:
        invalidated.append("all evidence affected by unexplained package changes")

    return {
        "reusable": sorted(set(reusable)),
        "invalidated": sorted(set(invalidated)),
        "note": (
            "Reusable evidence remains conditional on the exact baseline and "
            "candidate hashes recorded in this report."
        ),
    }


def validation_plan(profile: str, change_summary: dict, slide_count: int) -> dict:
    impacted = change_summary["visual_impacted_slides"]
    if profile == "inventory":
        return {
            "render_slides": [],
            "native_office_release_required_now": False,
            "next_steps": [
                "Choose the mutation lane and validation profile before editing."
            ],
        }
    if profile == "aesthetic-round":
        return {
            "render_slides": impacted,
            "native_office_release_required_now": False,
            "next_steps": [
                "Render only the impacted slides under the same conditions as the baseline.",
                "Show a before/after comparison and request user aesthetic judgment.",
                "Do not run full native Office release until a release candidate is declared.",
            ],
        }
    if profile == "controlled-revision":
        return {
            "render_slides": impacted,
            "native_office_release_required_now": False,
            "next_steps": [
                "Re-run only the semantic, chart, media, note, or visual checks listed as invalidated.",
                "Render only the visual-impacted slides unless a global visual part changed.",
                "Promote to release-candidate only after revision scope is accepted.",
            ],
        }
    if profile == "notes-only":
        return {
            "render_slides": [],
            "native_office_release_required_now": False,
            "next_steps": [
                "Review note language, slide alignment, pronunciation burden, and timing.",
                "Skip slide rendering because all visible slide parts must remain exact.",
                "Run release-candidate validation only when preparing the final deliverable.",
            ],
        }
    if profile == "release-candidate":
        return {
            "render_slides": list(range(1, slide_count + 1)),
            "native_office_release_required_now": True,
            "next_steps": [
                "Run $office-native-release with a fresh spec and render directory.",
                "Inspect every native-rendered slide at full size.",
                "Require explicit user aesthetic approval or mark aesthetic review pending.",
            ],
        }
    return {
        "render_slides": impacted,
        "native_office_release_required_now": False,
        "next_steps": [
            "Apply the explicit checks requested by the custom invocation.",
            "Do not infer release readiness from this custom audit alone.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="Candidate PPTX to audit")
    parser.add_argument("--baseline", type=Path, help="Baseline PPTX for comparison")
    parser.add_argument("--output", type=Path, required=True, help="UTF-8 JSON report path")
    parser.add_argument("--profile", choices=PROFILES, default="custom")
    parser.add_argument(
        "--allowed-slide-changes",
        help="Authorized visible slide changes, for example 2-4,11",
    )
    parser.add_argument(
        "--strict-metadata",
        action="store_true",
        help="Do not ignore normal PowerPoint metadata drift in scoped profiles",
    )
    parser.add_argument("--expected-slides", type=int)
    parser.add_argument("--require-same-structure", action="store_true")
    parser.add_argument(
        "--allow-changed-prefix",
        action="append",
        default=[],
        help="Authorized OOXML part prefix; applies to changed, added, and removed parts",
    )
    parser.add_argument(
        "--notes-required",
        help="Slides requiring notes, for example 1-14,16-23",
    )
    parser.add_argument("--max-note-average", type=float)
    parser.add_argument("--max-note-sentence", type=int)
    parser.add_argument("--require-text", action="append", default=[])
    parser.add_argument("--forbid-text", action="append", default=[])
    parser.add_argument("--forbid-notes", action="append", default=[])
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.candidate.is_file():
        parser.error(f"Candidate does not exist: {args.candidate}")
    if args.candidate.suffix.lower() != ".pptx":
        parser.error("Candidate must be a .pptx file")
    if args.baseline and not args.baseline.is_file():
        parser.error(f"Baseline does not exist: {args.baseline}")

    baseline_required = args.profile in {
        "aesthetic-round",
        "controlled-revision",
        "notes-only",
    }
    if baseline_required and not args.baseline:
        parser.error(f"Profile {args.profile} requires --baseline")
    if (args.require_same_structure or args.allow_changed_prefix) and not args.baseline:
        parser.error("A baseline is required for structure or changed-part checks")
    if args.profile == "release-candidate" and args.expected_slides is None:
        parser.error("Profile release-candidate requires --expected-slides")
    if args.profile == "notes-only" and any(
        not prefix.startswith("ppt/notesSlides/") for prefix in args.allow_changed_prefix
    ):
        parser.error("Profile notes-only cannot authorize non-note package prefixes")

    try:
        required_note_slides = parse_slide_set(args.notes_required)
        allowed_slide_changes = parse_slide_set(args.allowed_slide_changes)
    except ValueError as exc:
        parser.error(str(exc))
    if (
        args.profile in {"aesthetic-round", "controlled-revision"}
        and not allowed_slide_changes
    ):
        parser.error(f"Profile {args.profile} requires --allowed-slide-changes")

    candidate = inventory(args.candidate)
    baseline = inventory(args.baseline) if args.baseline else None
    diff = package_diff(args.baseline, args.candidate) if args.baseline else None
    change_summary = classify_changes(diff, baseline, candidate)

    invalid_allowed_slides = [
        number
        for number in allowed_slide_changes
        if number > candidate["structure"]["slides"]
    ]
    if invalid_allowed_slides:
        parser.error(
            "Allowed slide numbers exceed candidate slide count: "
            + ",".join(map(str, invalid_allowed_slides))
        )

    checks: dict[str, bool] = {"candidate_is_readable_pptx": True}
    details: dict[str, object] = {}

    if args.expected_slides is not None:
        checks["expected_slide_count"] = (
            candidate["structure"]["slides"] == args.expected_slides
        )

    require_same_structure = args.require_same_structure or args.profile == "notes-only"
    if require_same_structure and baseline:
        checks["same_structure_as_baseline"] = same_structure(
            baseline["structure"], candidate["structure"]
        )

    effective_prefixes = list(args.allow_changed_prefix)
    if args.profile == "notes-only" and "ppt/notesSlides/" not in effective_prefixes:
        effective_prefixes.append("ppt/notesSlides/")

    scope_profiles = {"aesthetic-round", "controlled-revision", "notes-only"}
    if args.profile in scope_profiles and diff:
        unexpected = unexpected_scope_changes(
            diff,
            args.profile,
            set(allowed_slide_changes),
            effective_prefixes,
            args.strict_metadata,
        )
        details["unexpected_scope_changes"] = unexpected
        checks["changes_within_authorized_scope"] = not any(unexpected.values())
    elif args.allow_changed_prefix and diff:
        unexpected = unexpected_scope_changes(
            diff,
            args.profile,
            set(),
            effective_prefixes,
            True,
        )
        details["unexpected_scope_changes"] = unexpected
        checks["only_allowed_parts_changed"] = not any(unexpected.values())

    if args.profile == "notes-only" and baseline:
        checks["visible_text_unchanged"] = not change_summary[
            "visible_text_changed_slides"
        ]
        checks["no_visual_slide_impact"] = not change_summary[
            "visual_impacted_slides"
        ]

    if required_note_slides:
        missing_notes = [
            number
            for number in required_note_slides
            if not candidate["notes_by_slide"].get(str(number), "").strip()
        ]
        out_of_range = [
            number
            for number in required_note_slides
            if number > candidate["structure"]["slides"]
        ]
        details["missing_required_notes"] = missing_notes
        details["required_note_slides_out_of_range"] = out_of_range
        checks["notes_present_on_required_slides"] = not missing_notes and not out_of_range
        note_texts = [
            candidate["notes_by_slide"].get(str(number), "")
            for number in required_note_slides
            if candidate["notes_by_slide"].get(str(number), "").strip()
        ]
    else:
        note_texts = [
            text for text in candidate["notes_by_slide"].values() if text.strip()
        ]

    sentence_counts = sentence_word_counts(note_texts)
    note_stats = {
        "sentences": len(sentence_counts),
        "words": sum(sentence_counts),
        "average_words_per_sentence": (
            round(sum(sentence_counts) / len(sentence_counts), 2)
            if sentence_counts
            else 0.0
        ),
        "maximum_words_per_sentence": max(sentence_counts, default=0),
    }
    if args.max_note_average is not None:
        checks["note_average_within_limit"] = (
            bool(sentence_counts)
            and note_stats["average_words_per_sentence"] <= args.max_note_average
        )
    if args.max_note_sentence is not None:
        checks["note_sentence_max_within_limit"] = (
            bool(sentence_counts)
            and note_stats["maximum_words_per_sentence"] <= args.max_note_sentence
        )

    required_missing = [
        term
        for term in args.require_text
        if term.casefold() not in candidate["all_visible_text"].casefold()
    ]
    forbidden_visible = find_terms(candidate["all_visible_text"], args.forbid_text)
    forbidden_notes = find_terms(candidate["all_notes_text"], args.forbid_notes)
    details["missing_required_text"] = required_missing
    details["forbidden_visible_text_found"] = forbidden_visible
    details["forbidden_notes_text_found"] = forbidden_notes
    if args.require_text:
        checks["all_required_text_present"] = not required_missing
    if args.forbid_text:
        checks["forbidden_visible_text_absent"] = not forbidden_visible
    if args.forbid_notes:
        checks["forbidden_notes_text_absent"] = not forbidden_notes

    reuse = derive_validation_reuse(change_summary, diff is not None)
    plan = validation_plan(
        args.profile, change_summary, candidate["structure"]["slides"]
    )
    visual_required = args.profile in {
        "custom",
        "aesthetic-round",
        "controlled-revision",
        "release-candidate",
    }

    report = {
        "profile": args.profile,
        "candidate": {
            "path": candidate["path"],
            "sha256": candidate["sha256"],
            "structure": candidate["structure"],
        },
        "baseline": (
            {
                "path": baseline["path"],
                "sha256": baseline["sha256"],
                "structure": baseline["structure"],
            }
            if baseline
            else None
        ),
        "authorized_scope": {
            "allowed_slide_changes": allowed_slide_changes,
            "allowed_package_prefixes": effective_prefixes,
            "strict_metadata": args.strict_metadata,
        },
        "package_diff": diff,
        "change_summary": change_summary,
        "validation_reuse": reuse,
        "validation_plan": plan,
        "notes": {
            "required_slides": required_note_slides,
            "stats_scope": required_note_slides or "all nonempty notes",
            "stats": note_stats,
        },
        "details": details,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "visual_inspection_required": visual_required,
        "visual_inspection_scope": plan["render_slides"],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["all_checks_pass"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except zipfile.BadZipFile as exc:
        print(f"Invalid PPTX ZIP package: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except ET.ParseError as exc:
        print(f"Invalid OOXML XML: {exc}", file=sys.stderr)
        raise SystemExit(2)
