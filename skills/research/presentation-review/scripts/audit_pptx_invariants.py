#!/usr/bin/env python3
"""Audit task-declared PPTX invariants without rendering or Office automation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import struct
import sys
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree as ET


PML = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
MATH = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"p": PML, "a": A, "r": R, "rel": REL, "m": MATH}
EMU_PER_POINT = 12700.0
EMU_PER_INCH = 914400.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def xml(package: zipfile.ZipFile, part: str) -> ET.Element:
    return ET.fromstring(package.read(part))


def rels(package: zipfile.ZipFile, part: str) -> dict[str, str]:
    root = xml(package, part)
    return {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in root.findall("rel:Relationship", NS)
    }


def normalize_target(source_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return str(PurePosixPath(source_part).parent.joinpath(target))


def slide_parts(package: zipfile.ZipFile) -> list[str]:
    presentation = xml(package, "ppt/presentation.xml")
    relationships = rels(package, "ppt/_rels/presentation.xml.rels")
    parts = []
    for slide_id in presentation.findall("p:sldIdLst/p:sldId", NS):
        rel_id = slide_id.attrib[f"{{{R}}}id"]
        parts.append(normalize_target("ppt/presentation.xml", relationships[rel_id]))
    return parts


def rels_part(part: str) -> str:
    path = PurePosixPath(part)
    return str(path.parent / "_rels" / f"{path.name}.rels")


def text_of(node: ET.Element) -> str:
    return "".join(item.text or "" for item in node.findall(".//a:t", NS)).strip()


def geometry(node: ET.Element) -> dict[str, float] | None:
    transform = node.find("p:spPr/a:xfrm", NS)
    if transform is None:
        return None
    offset = transform.find("a:off", NS)
    extent = transform.find("a:ext", NS)
    if offset is None or extent is None:
        return None
    values = {
        "left": int(offset.attrib.get("x", "0")) / EMU_PER_POINT,
        "top": int(offset.attrib.get("y", "0")) / EMU_PER_POINT,
        "width": int(extent.attrib.get("cx", "0")) / EMU_PER_POINT,
        "height": int(extent.attrib.get("cy", "0")) / EMU_PER_POINT,
    }
    values["right"] = values["left"] + values["width"]
    values["bottom"] = values["top"] + values["height"]
    values["aspect_ratio"] = (
        values["width"] / values["height"] if values["height"] else math.inf
    )
    return values


def shape_records(package: zipfile.ZipFile, part: str) -> list[dict[str, Any]]:
    root = xml(package, part)
    relationships = {}
    relation_part = rels_part(part)
    if relation_part in package.namelist():
        relationships = rels(package, relation_part)
    records = []
    for kind, xpath, nv_path in (
        ("shape", ".//p:sp", "p:nvSpPr/p:cNvPr"),
        ("picture", ".//p:pic", "p:nvPicPr/p:cNvPr"),
    ):
        for node in root.findall(xpath, NS):
            nonvisual = node.find(nv_path, NS)
            record: dict[str, Any] = {
                "kind": kind,
                "name": nonvisual.attrib.get("name", "") if nonvisual is not None else "",
                "description": nonvisual.attrib.get("descr", "") if nonvisual is not None else "",
                "text": text_of(node),
                "geometry": geometry(node),
            }
            if kind == "picture":
                blip = node.find("p:blipFill/a:blip", NS)
                rel_id = blip.attrib.get(f"{{{R}}}embed") if blip is not None else None
                target = relationships.get(rel_id, "") if rel_id else ""
                record["media_part"] = (
                    normalize_target(part, target) if target else ""
                )
            records.append(record)
    return records


def matches(record: dict[str, Any], selector: dict[str, Any]) -> bool:
    if selector.get("kind") and record["kind"] != selector["kind"]:
        return False
    for key, field in (
        ("name_regex", "name"),
        ("description_regex", "description"),
        ("text_regex", "text"),
    ):
        if key in selector and not re.search(selector[key], record.get(field, "")):
            return False
    geom = record.get("geometry")
    numeric_filters = {
        "left_min_points": ("left", lambda value, threshold: value >= threshold),
        "left_max_points": ("left", lambda value, threshold: value <= threshold),
        "top_min_points": ("top", lambda value, threshold: value >= threshold),
        "top_max_points": ("top", lambda value, threshold: value <= threshold),
        "right_min_points": ("right", lambda value, threshold: value >= threshold),
        "right_max_points": ("right", lambda value, threshold: value <= threshold),
        "aspect_ratio_min": ("aspect_ratio", lambda value, threshold: value >= threshold),
        "aspect_ratio_max": ("aspect_ratio", lambda value, threshold: value <= threshold),
    }
    for key, (field, predicate) in numeric_filters.items():
        if key in selector:
            if geom is None or not predicate(geom[field], float(selector[key])):
                return False
    return True


def same_geometry(
    rows: list[dict[str, Any]], fields: list[str], tolerance: float
) -> tuple[bool, list[dict[str, Any]]]:
    comparable = [row for row in rows if row.get("geometry")]
    if not comparable:
        return False, []
    reference = comparable[0]["geometry"]
    differences = []
    for row in comparable[1:]:
        delta = {
            field: round(row["geometry"][field] - reference[field], 4)
            for field in fields
        }
        if any(abs(value) > tolerance for value in delta.values()):
            differences.append({"slide": row["slide"], "delta_points": delta})
    return not differences, differences


def image_dimensions(data: bytes, suffix: str) -> tuple[int, int] | None:
    suffix = suffix.lower()
    if suffix == ".png" and data.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", data[16:24])
    if suffix == ".gif" and data[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", data[6:10])
    if suffix == ".bmp" and data.startswith(b"BM") and len(data) >= 26:
        return struct.unpack("<ii", data[18:26])
    if suffix in (".jpg", ".jpeg") and data.startswith(b"\xff\xd8"):
        index = 2
        while index + 9 < len(data):
            if data[index] != 0xFF:
                index += 1
                continue
            marker = data[index + 1]
            index += 2
            if marker in (0xD8, 0xD9):
                continue
            if index + 2 > len(data):
                break
            length = struct.unpack(">H", data[index : index + 2])[0]
            if marker in range(0xC0, 0xC4) and index + 7 < len(data):
                height, width = struct.unpack(">HH", data[index + 3 : index + 7])
                return width, height
            index += length
    return None


def visible_text(records: list[dict[str, Any]]) -> str:
    return "\n".join(record["text"] for record in records if record["text"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    failures: list[str] = []
    warnings: list[str] = []
    details: dict[str, Any] = {}

    with zipfile.ZipFile(args.candidate) as package:
        parts = slide_parts(package)
        slides = []
        for number, part in enumerate(parts, 1):
            records = shape_records(package, part)
            root = xml(package, part)
            slides.append(
                {
                    "number": number,
                    "part": part,
                    "records": records,
                    "text": visible_text(records),
                    "office_math": len(root.findall(".//m:oMath", NS)),
                }
            )

        expected_slides = int(spec.get("expected_slides", len(slides)))
        checks["expected_slide_count"] = len(slides) == expected_slides
        if not checks["expected_slide_count"]:
            failures.append(
                f"Expected {expected_slides} slides, found {len(slides)}"
            )

        page_spec = spec.get("page_numbers", {})
        if page_spec.get("enabled"):
            pattern = re.compile(page_spec.get("text_regex", r"^(\d+)\s*/\s*(\d+)$"))
            expected_start = int(page_spec.get("expected_start", 1))
            expected_total = int(page_spec.get("expected_total", len(slides)))
            expected_per_slide = int(page_spec.get("expected_per_slide", 1))
            page_rows = []
            page_errors = []
            for slide in slides:
                found = []
                for record in slide["records"]:
                    match = pattern.fullmatch(record["text"].strip())
                    if match:
                        found.append((record, match))
                if len(found) != expected_per_slide:
                    page_errors.append(
                        {"slide": slide["number"], "found": len(found)}
                    )
                for record, match in found:
                    numerator, denominator = int(match.group(1)), int(match.group(2))
                    expected_numerator = expected_start + slide["number"] - 1
                    if numerator != expected_numerator or denominator != expected_total:
                        page_errors.append(
                            {
                                "slide": slide["number"],
                                "text": record["text"],
                                "expected": f"{expected_numerator}/{expected_total}",
                            }
                        )
                    page_rows.append(
                        {
                            "slide": slide["number"],
                            "text": record["text"],
                            "geometry": record["geometry"],
                        }
                    )
            checks["page_numbers_complete_and_sequential"] = not page_errors
            details["page_numbers"] = {"errors": page_errors, "rows": page_rows}
            if page_errors:
                failures.append("Page numbers are missing, duplicated, or out of sequence")
            if page_spec.get("same_geometry"):
                ok, differences = same_geometry(
                    page_rows,
                    ["left", "top", "width", "height"],
                    float(page_spec.get("tolerance_points", 0.5)),
                )
                checks["page_number_geometry_consistent"] = ok
                details["page_numbers"]["geometry_differences"] = differences
                if not ok:
                    failures.append("Page-number geometry is not consistent")

        repeat_details = {}
        for invariant in spec.get("repeat_objects", []):
            identifier = invariant["id"]
            selector = invariant.get("selector", {})
            expected = int(invariant.get("expected_per_slide", 1))
            rows = []
            count_errors = []
            for slide in slides:
                found = [r for r in slide["records"] if matches(r, selector)]
                if len(found) != expected:
                    count_errors.append(
                        {"slide": slide["number"], "found": len(found)}
                    )
                for record in found:
                    rows.append(
                        {
                            "slide": slide["number"],
                            "name": record["name"],
                            "description": record["description"],
                            "media_part": record.get("media_part", ""),
                            "geometry": record["geometry"],
                        }
                    )
            count_key = f"repeat_object_{identifier}_count"
            checks[count_key] = not count_errors
            if count_errors:
                failures.append(f"Repeated object {identifier} is missing or duplicated")
            item_details: dict[str, Any] = {
                "count_errors": count_errors,
                "rows": rows,
            }
            fields = invariant.get("same_geometry_fields", [])
            if fields:
                ok, differences = same_geometry(
                    rows,
                    fields,
                    float(invariant.get("tolerance_points", 0.5)),
                )
                checks[f"repeat_object_{identifier}_geometry"] = ok
                item_details["geometry_differences"] = differences
                if not ok:
                    failures.append(f"Repeated object {identifier} geometry differs")
            if invariant.get("same_media"):
                media = {row["media_part"] for row in rows if row["media_part"]}
                checks[f"repeat_object_{identifier}_media"] = len(media) == 1
                item_details["unique_media_parts"] = sorted(media)
                if len(media) != 1:
                    failures.append(f"Repeated object {identifier} media differs")
            repeat_details[identifier] = item_details
        if repeat_details:
            details["repeat_objects"] = repeat_details

        math_spec = spec.get("office_math", {})
        total_math = sum(slide["office_math"] for slide in slides)
        minimum_total = int(math_spec.get("minimum_total", 0))
        checks["office_math_minimum_total"] = total_math >= minimum_total
        math_errors = []
        by_slide = {str(slide["number"]): slide["office_math"] for slide in slides}
        for slide_number, minimum in math_spec.get("minimum_by_slide", {}).items():
            found = by_slide.get(str(slide_number), 0)
            if found < int(minimum):
                math_errors.append(
                    {"slide": int(slide_number), "minimum": int(minimum), "found": found}
                )
        checks["office_math_minimum_by_slide"] = not math_errors
        details["office_math"] = {
            "total": total_math,
            "minimum_total": minimum_total,
            "by_slide": by_slide,
            "errors": math_errors,
        }
        if not checks["office_math_minimum_total"] or math_errors:
            failures.append("Office Math count is below the declared minimum")

        forbidden_hits = []
        for expression in spec.get("forbidden_visible_regex", []):
            pattern = re.compile(expression)
            for slide in slides:
                matches_found = sorted(set(pattern.findall(slide["text"])))
                if matches_found:
                    forbidden_hits.append(
                        {
                            "slide": slide["number"],
                            "pattern": expression,
                            "matches": matches_found[:20],
                        }
                    )
        checks["forbidden_visible_text_absent"] = not forbidden_hits
        details["forbidden_visible_text"] = forbidden_hits
        if forbidden_hits:
            failures.append("Forbidden visible-text patterns were found")

        duplicate_spec = spec.get("duplicate_text_overlap", {})
        duplicate_hits = []
        if duplicate_spec.get("warn"):
            tolerance = float(duplicate_spec.get("geometry_tolerance_points", 0.5))
            for slide in slides:
                groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
                for record in slide["records"]:
                    normalized = " ".join(record["text"].split())
                    if normalized and record["geometry"]:
                        groups[normalized].append(record)
                for text, records in groups.items():
                    for index, first in enumerate(records):
                        for second in records[index + 1 :]:
                            if all(
                                abs(first["geometry"][field] - second["geometry"][field])
                                <= tolerance
                                for field in ("left", "top", "width", "height")
                            ):
                                duplicate_hits.append(
                                    {
                                        "slide": slide["number"],
                                        "text": text[:120],
                                        "objects": [first["name"], second["name"]],
                                    }
                                )
            if duplicate_hits:
                warnings.append("Near-identical overlapping text objects were found")
        details["duplicate_text_overlap_warnings"] = duplicate_hits

        image_spec = spec.get("image_quality", {})
        threshold = float(image_spec.get("warn_effective_ppi_below", 0))
        low_resolution = []
        if threshold > 0:
            for slide in slides:
                for record in slide["records"]:
                    media_part = record.get("media_part")
                    geom = record.get("geometry")
                    if not media_part or not geom or media_part not in package.namelist():
                        continue
                    dimensions = image_dimensions(
                        package.read(media_part), PurePosixPath(media_part).suffix
                    )
                    if not dimensions or geom["width"] <= 0 or geom["height"] <= 0:
                        continue
                    width_inches = geom["width"] * EMU_PER_POINT / EMU_PER_INCH
                    height_inches = geom["height"] * EMU_PER_POINT / EMU_PER_INCH
                    effective_ppi = min(
                        dimensions[0] / width_inches,
                        dimensions[1] / height_inches,
                    )
                    if effective_ppi < threshold:
                        low_resolution.append(
                            {
                                "slide": slide["number"],
                                "object": record["name"],
                                "media_part": media_part,
                                "pixels": list(dimensions),
                                "effective_ppi": round(effective_ppi, 1),
                            }
                        )
            if low_resolution:
                warnings.append(
                    f"Images below the declared {threshold:g} effective PPI warning threshold were found"
                )
        details["image_resolution_warnings"] = low_resolution

        allowed_roi_types = {
            "school_logo",
            "equation_region",
            "chart_axes_ticks_legend",
        }
        requested_roi_types = set(
            spec.get("visual_review", {}).get(
                "allowed_roi_types", sorted(allowed_roi_types)
            )
        )
        unsupported_roi_types = sorted(requested_roi_types - allowed_roi_types)
        checks["roi_policy_uses_allowed_types_only"] = not unsupported_roi_types
        details["roi_policy"] = {
            "allowed_types": sorted(allowed_roi_types),
            "requested_types": sorted(requested_roi_types),
            "unsupported_types": unsupported_roi_types,
        }
        if unsupported_roi_types:
            failures.append(
                "Unsupported ROI types were requested: "
                + ", ".join(unsupported_roi_types)
            )

    all_checks_pass = all(checks.values())
    report = {
        "candidate": {
            "path": str(args.candidate.resolve()),
            "sha256": sha256(args.candidate),
            "slides": len(slides),
        },
        "spec": str(args.spec.resolve()),
        "checks": checks,
        "all_checks_pass": all_checks_pass,
        "failures": failures,
        "warnings": warnings,
        "details": details,
        "visual_review": {
            "overview_purpose": "narrative_only",
            "full_size_scope": spec.get("visual_review", {}).get(
                "full_size_slides", "changed_or_dependent"
            ),
            "allowed_roi_types": [
                "school_logo",
                "equation_region",
                "chart_axes_ticks_legend",
            ],
            "roi_trigger": "changed_failed_or_uncertain_only",
            "semantic_crop_review_is_manual": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"all_checks_pass": all_checks_pass, "failures": failures, "warnings": warnings}, ensure_ascii=False, indent=2))
    return 0 if all_checks_pass else 1


if __name__ == "__main__":
    sys.exit(main())
