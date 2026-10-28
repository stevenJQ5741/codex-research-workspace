"""Exercise crop and explicit coverage reporting without Office dependencies."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from test_pptx_invariants import AUDIT, make_pptx


def alter_package(path, transform, remove_media=False, vector_media=False, extra_parts=None):
    with zipfile.ZipFile(path) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    slide = parts["ppt/slides/slide1.xml"].decode("utf-8")
    parts["ppt/slides/slide1.xml"] = transform(slide).encode("utf-8")
    parts.update(extra_parts or {})
    if remove_media:
        parts.pop("ppt/media/image1.png")
    if vector_media:
        rel_path = "ppt/slides/_rels/slide1.xml.rels"
        rels = parts[rel_path].decode("utf-8").replace("</Relationships>",
            '<Relationship Id="rId2" Target="../media/image2.svg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"/></Relationships>')
        parts[rel_path] = rels.encode("utf-8")
        parts["ppt/media/image2.svg"] = b'<svg xmlns="http://www.w3.org/2000/svg"/>'
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in parts.items():
            archive.writestr(name, content)


class CoverageTests(unittest.TestCase):
    def audit(self, transform=lambda text: text, remove_media=False, threshold=150, vector_media=False, extra_parts=None):
        with tempfile.TemporaryDirectory(prefix="pptx-coverage-") as temp:
            folder = Path(temp)
            deck, spec, out = folder / "test.pptx", folder / "spec.json", folder / "out.json"
            make_pptx(deck, "../media/image1.png", 1000, 600)
            alter_package(deck, transform, remove_media, vector_media, extra_parts)
            spec.write_text(json.dumps({"image_quality": {"warn_effective_ppi_below": threshold}}), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(AUDIT), str(deck), "--spec", str(spec), "--output", str(out)],
                                  capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            return json.loads(out.read_text(encoding="utf-8"))

    def test_cropping_reduces_effective_pixels_and_can_trigger_warning(self):
        result = self.audit(lambda x: x.replace("</p:blipFill>", '<a:srcRect l="25000" r="25000"/></p:blipFill>'))
        coverage = result["details"]["image_quality_coverage"]
        self.assertTrue(coverage["complete_within_scope"])
        self.assertEqual(coverage["assessed"][0]["effective_ppi"], 100.0)
        self.assertEqual(result["details"]["image_resolution_warnings"][0]["effective_ppi"], 100.0)
        self.assertTrue(result["all_checks_pass"])

    def test_missing_linked_grouped_tiled_and_bad_crop_are_reported(self):
        cases = (
            (lambda x: x, True, "missing_media"),
            (lambda x: x.replace('r:embed="rId1"', 'r:link="rId1"'), False, "linked_image"),
            (lambda x: x.replace("<p:pic>", "<p:grpSp><p:pic>").replace("</p:pic>", "</p:pic></p:grpSp>"), False, "group_transform"),
            (lambda x: x.replace("</p:blipFill>", "<a:tile/></p:blipFill>"), False, "tiled_fill"),
            (lambda x: x.replace("</p:blipFill>", '<a:srcRect l="80000" r="30000"/></p:blipFill>'), False, "invalid_or_extended_crop"),
            (lambda x: x.replace("</p:blipFill>", '<a:srcRect l="invalid"/></p:blipFill>'), False, "invalid_crop"),
        )
        for transform, missing, reason in cases:
            with self.subTest(reason=reason):
                result = self.audit(transform, missing)
                coverage = result["details"]["image_quality_coverage"]
                self.assertFalse(coverage["complete_within_scope"])
                self.assertEqual(coverage["unassessed"][0]["reason"], reason)
                self.assertTrue(result["warnings"])

    def test_unsupported_raster_and_detected_slide_image_fill_are_reported(self):
        # An invalid image is not silently treated as a sufficiently sharp image.
        with tempfile.TemporaryDirectory(prefix="pptx-coverage-invalid-") as temp:
            folder = Path(temp)
            deck, spec, out = folder / "test.pptx", folder / "spec.json", folder / "out.json"
            make_pptx(deck, "../media/image1.png", 1000, 600)
            with zipfile.ZipFile(deck) as archive:
                parts = {name: archive.read(name) for name in archive.namelist()}
            parts["ppt/media/image1.png"] = b"\x89PNG\r\n\x1a\n"
            with zipfile.ZipFile(deck, "w") as archive:
                for name, content in parts.items(): archive.writestr(name, content)
            spec.write_text('{"image_quality":{"warn_effective_ppi_below":150}}', encoding="utf-8")
            subprocess.run([sys.executable, str(AUDIT), str(deck), "--spec", str(spec), "--output", str(out)], check=True, capture_output=True)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["details"]["image_quality_coverage"]["unassessed"][0]["reason"], "unsupported_or_invalid_raster")
        result = self.audit(lambda x: x.replace("</p:spTree>", '<p:sp><p:nvSpPr><p:cNvPr id="3" name="filled shape"/></p:nvSpPr><p:spPr><a:blipFill><a:blip r:embed="rId1"/></a:blipFill></p:spPr></p:sp></p:spTree>'))
        self.assertEqual(result["details"]["image_quality_coverage"]["unassessed"][0]["reason"], "shape_image_fill")

    def test_disabled_coverage_is_not_claimed_complete(self):
        result = self.audit(threshold=0)
        coverage = result["details"]["image_quality_coverage"]
        self.assertFalse(coverage["enabled"])
        self.assertFalse(coverage["complete_within_scope"])
        self.assertEqual(coverage["assessed"], [])

    def test_layout_master_and_chart_images_are_flagged_as_unassessed(self):
        xml = b'<root xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:blip/></root>'
        parts = {"ppt/slideLayouts/slideLayout1.xml": xml,
                 "ppt/slideMasters/slideMaster1.xml": xml,
                 "ppt/charts/chart1.xml": xml}
        coverage = self.audit(extra_parts=parts)["details"]["image_quality_coverage"]
        self.assertFalse(coverage["complete_within_scope"])
        self.assertEqual({item["object"] for item in coverage["unassessed"]}, set(parts))
        self.assertTrue(all(item["reason"] == "layout_master_or_chart_image" for item in coverage["unassessed"]))

    def test_invalid_non_slide_xml_is_reported(self):
        coverage = self.audit(extra_parts={"ppt/charts/chart1.xml": b"<invalid"})["details"]["image_quality_coverage"]
        self.assertFalse(coverage["complete_within_scope"])
        self.assertEqual(coverage["unassessed"][0]["reason"], "invalid_non_slide_xml")

    def test_missing_svg_extension_is_not_silently_accepted(self):
        result = self.audit(lambda x: x.replace('<a:blip r:embed="rId1"/>',
            '<a:blip r:embed="rId1"><x:svgBlip xmlns:x="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="rId2"/></a:blip>'))
        coverage = result["details"]["image_quality_coverage"]
        self.assertEqual(coverage["unassessed"][0]["reason"], "missing_svg_vector_media")
        self.assertEqual(coverage["assessed"], [])
        self.assertEqual(result["details"]["image_resolution_warnings"], [])

    def test_existing_svg_is_identified_as_vector(self):
        result = self.audit(lambda x: x.replace('<a:blip r:embed="rId1"/>',
            '<a:blip r:embed="rId1"><x:svgBlip xmlns:x="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="rId2"/></a:blip>'), vector_media=True)
        coverage = result["details"]["image_quality_coverage"]
        self.assertEqual(coverage["vector"][0]["reason"], "vector_media")
        self.assertEqual(coverage["vector"][0]["vector_part"], "ppt/media/image2.svg")
        self.assertEqual(coverage["unassessed"], [])


if __name__ == "__main__": unittest.main()
