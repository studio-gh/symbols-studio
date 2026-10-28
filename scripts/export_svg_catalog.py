#!/usr/bin/env python3
"""Validate uploaded page-level SVG metadata and export standalone symbols."""
from __future__ import annotations
import gzip, json, sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SVG_ROOT = ROOT / "assets" / "symbols"
DOWNLOAD_ROOT = ROOT / "assets" / "downloads"
BUNDLE = DOWNLOAD_ROOT / "symbols-pages-34-36-svg.zip"
pages = [34, 35, 36]
entries = []
for page in pages:
    path = DATA_DIR / f"symbols-page{page}.json.gz"
    try:
        items = json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
    except Exception as exc:
        print(f"Invalid compressed catalogue {path}: {exc}", file=sys.stderr)
        raise
    if not isinstance(items, list) or not items:
        raise ValueError(f"Empty catalogue for page {page}")
    if any(str(item.get("page")) != str(page) for item in items):
        raise ValueError(f"Wrong source page metadata in {path}")
    entries.extend(items)

SVG_ROOT.mkdir(parents=True, exist_ok=True)
DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
written = []
for entry in entries:
    markup = entry.get("svgMarkup")
    filename = entry.get("svgFile", "")
    relative = str(filename).removeprefix("./")
    if not markup or not markup.lstrip().startswith("<svg"):
        raise ValueError(f"Missing SVG markup for {entry.get('id')}")
    if not relative.startswith("assets/symbols/") or not relative.endswith(".svg"):
        raise ValueError(f"Unexpected SVG output path: {relative}")
    if "xmlns=" not in markup[:250]:
        markup = markup.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markup + "\n", encoding="utf-8")
    written.append(target)

metadata = [{k:v for k,v in item.items() if k != "svgMarkup"} for item in entries]
metadata_path = DOWNLOAD_ROOT / "metadata-pages-34-36.json"
metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
readme_path = DOWNLOAD_ROOT / "README.txt"
readme_path.write_text(
    "Symbols Studio — SVG batch, printed pages 34–36\n"
    f"{len(written)} individual SVG files, vectorized from scanned sourcebook pages 34–36.\n"
    "First-pass contour traces: review shapes manually before production use.\n"
    "Source: Henry Dreyfuss, Symbol Sourcebook, McGraw-Hill, 1972, printed pages 34–36.\n",
    encoding="utf-8",
)
with ZipFile(BUNDLE, "w", ZIP_DEFLATED) as archive:
    for path in written:
        archive.write(path, path.relative_to(SVG_ROOT))
    archive.write(metadata_path, "metadata.json")
    archive.write(readme_path, "README.txt")
print(f"Exported {len(written)} standalone SVGs to {SVG_ROOT}")
print(f"Created {BUNDLE}")
