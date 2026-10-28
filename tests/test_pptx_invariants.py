"""Regression tests for image relationships in PowerPoint invariant audits."""
import json
import os
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = Path(os.environ.get("PPTX_AUDIT_SCRIPT", ROOT / "skills/research/presentation-review/scripts/audit_pptx_invariants.py"))


def png(width, height):
    def chunk(tag, payload):
        return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", zlib.crc32(tag + payload) & 0xffffffff)
    rows = (b"\x00" + b"\xff\xff\xff" * width) * height
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def make_pptx(path, target, width, height):
    p = "http://schemas.openxmlformats.org/presentationml/2006/main"
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    r = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    rel = "http://schemas.openxmlformats.org/package/2006/relationships"
    presentation = f'<p:presentation xmlns:p="{p}" xmlns:r="{r}"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst></p:presentation>'
    presentation_rels = f'<Relationships xmlns="{rel}"><Relationship Id="rId1" Target="slides/slide1.xml" Type="{r}/slide"/></Relationships>'
    slide = f'''<p:sld xmlns:p="{p}" xmlns:a="{a}" xmlns:r="{r}"><p:cSld><p:spTree>
      <p:pic><p:nvPicPr><p:cNvPr id="2" name="Image"/></p:nvPicPr>
      <p:blipFill><a:blip r:embed="rId1"/></p:blipFill>
      <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="4572000" cy="2743200"/></a:xfrm></p:spPr></p:pic>
      </p:spTree></p:cSld></p:sld>'''
    slide_rels = f'<Relationships xmlns="{rel}"><Relationship Id="rId1" Target="{target}" Type="{r}/image"/></Relationships>'
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("ppt/presentation.xml", presentation)
        archive.writestr("ppt/_rels/presentation.xml.rels", presentation_rels)
        archive.writestr("ppt/slides/slide1.xml", slide)
        archive.writestr("ppt/slides/_rels/slide1.xml.rels", slide_rels)
        archive.writestr("ppt/media/image1.png", png(width, height))


class ImageResolutionRegressionTests(unittest.TestCase):
    def audit(self, target, width, height, threshold=150):
        with tempfile.TemporaryDirectory(prefix="pptx-invariant-test-") as temp:
            folder = Path(temp)
            make_pptx(folder / "candidate.pptx", target, width, height)
            (folder / "spec.json").write_text(json.dumps({"image_quality": {"warn_effective_ppi_below": threshold}}), encoding="utf-8")
            result = subprocess.run([sys.executable, str(AUDIT), str(folder / "candidate.pptx"),
                                     "--spec", str(folder / "spec.json"), "--output", str(folder / "result.json")],
                                    capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            return json.loads((folder / "result.json").read_text(encoding="utf-8"))

    def test_low_resolution_is_reported_for_normal_and_equivalent_paths(self):
        for target in ("../media/image1.png", "./../media/image1.png", "/ppt/media/image1.png", "../../ppt/media/image1.png"):
            with self.subTest(target=target):
                result = self.audit(target, 36, 24)
                self.assertTrue(result["all_checks_pass"])  # image quality is a warning
                warnings = result["details"]["image_resolution_warnings"]
                self.assertEqual(len(warnings), 1, result)
                self.assertEqual(warnings[0]["media_part"], "ppt/media/image1.png")
                self.assertEqual(warnings[0]["pixels"], [36, 24])
                self.assertEqual(warnings[0]["effective_ppi"], 7.2)
                self.assertTrue(result["warnings"])

    def test_high_resolution_and_disabled_threshold_do_not_warn(self):
        result = self.audit("../media/image1.png", 900, 600)
        self.assertEqual(result["details"]["image_resolution_warnings"], [])
        result = self.audit("../media/image1.png", 36, 24, threshold=0)
        self.assertEqual(result["details"]["image_resolution_warnings"], [])


if __name__ == "__main__":
    unittest.main()
