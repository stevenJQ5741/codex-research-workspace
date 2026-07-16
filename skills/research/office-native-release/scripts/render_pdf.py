from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from math import ceil, sqrt
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def find_pdftoppm() -> Path:
    candidates: list[Path] = []
    if os.environ.get("PDFTOPPM"):
        candidates.append(Path(os.environ["PDFTOPPM"]))
    for name in ("pdftoppm.exe", "pdftoppm"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    candidates.append(
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "native"
        / "poppler"
        / "Library"
        / "bin"
        / "pdftoppm.exe"
    )
    for candidate in candidates:
        if candidate.is_file() and candidate.suffix.lower() == ".exe":
            return candidate.resolve()
    raise RuntimeError("pdftoppm.exe was not found; run office_preflight.ps1")


def numeric_suffix(path: Path) -> int:
    return int(path.stem.rsplit("-", 1)[1])


def make_montage(paths: list[Path], output: Path) -> None:
    columns = min(4, max(1, ceil(sqrt(len(paths)))))
    thumbnail_width = 420
    thumbnails: list[Image.Image] = []
    try:
        for path in paths:
            image = Image.open(path).convert("RGB")
            height = round(image.height * thumbnail_width / image.width)
            thumbnails.append(image.resize((thumbnail_width, height), Image.Resampling.LANCZOS))
        row_height = max(image.height for image in thumbnails)
        rows = ceil(len(thumbnails) / columns)
        canvas = Image.new("RGB", (columns * thumbnail_width, rows * row_height), "white")
        for index, image in enumerate(thumbnails):
            x = (index % columns) * thumbnail_width
            y = (index // columns) * row_height
            canvas.paste(image, (x, y))
        canvas.save(output, "PNG", optimize=True)
    finally:
        for image in thumbnails:
            image.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render every PDF page with Poppler.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if list(output_dir.glob("page-*.png")) or list(output_dir.glob("render-*.png")):
        raise SystemExit(f"Output directory contains stale page images: {output_dir}")

    pdftoppm = find_pdftoppm()
    prefix = output_dir / "render"
    subprocess.run(
        [str(pdftoppm), "-png", "-r", str(args.dpi), str(pdf_path), str(prefix)],
        check=True,
    )

    raw_paths = sorted(output_dir.glob("render-*.png"), key=numeric_suffix)
    expected_pages = len(PdfReader(str(pdf_path)).pages)
    if len(raw_paths) != expected_pages:
        raise RuntimeError(
            f"Rendered {len(raw_paths)} page(s), expected {expected_pages} from the PDF."
        )

    page_paths: list[Path] = []
    dimensions: list[list[int]] = []
    for number, raw_path in enumerate(raw_paths, start=1):
        page_path = output_dir / f"page-{number}.png"
        raw_path.rename(page_path)
        with Image.open(page_path) as image:
            dimensions.append([image.width, image.height])
        page_paths.append(page_path)

    montage_path = output_dir / "montage.png"
    make_montage(page_paths, montage_path)
    manifest = {
        "pdf": str(pdf_path),
        "pdf_sha256": sha256(pdf_path),
        "renderer": str(pdftoppm),
        "dpi": args.dpi,
        "page_count": len(page_paths),
        "pages": [str(path) for path in page_paths],
        "dimensions": dimensions,
        "montage": str(montage_path),
        "full_size_visual_inspection_required": True,
    }
    manifest_path = output_dir / "render_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
