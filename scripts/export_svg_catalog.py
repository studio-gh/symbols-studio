#!/usr/bin/env python3
"""Export each embedded SVG in the page-34 catalogue as a standalone file."""
from __future__ import annotations

import gzip
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
CATALOGS = sorted((ROOT / "data").glob("symbols-page*.json.gz"))
SVG_ROOT = ROOT / "assets" / "symbols"
DOWNLOAD_ROOT = ROOT / "assets" / "downloads"
BUNDLE = DOWNLOAD_ROOT / "symbols-pages-34-36-svg.zip"

entries = []
for catalog_path in CATALOGS:
    entries.extend(json.loads(gzip.decompress(catalog_path.read_bytes()).decode("utf-8")))
if not entries:
    raise FileNotFoundError("No compressed SVG catalogues found in data/")
SVG_ROOT.mkdir(parents=True, exist_ok=True)
DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
written: list[Path] = []

for entry in entries:
    markup = entry.get("svgMarkup")
    relative = str(entry.get("svgFile", "")).removeprefix("./")
    if not markup or not markup.lstrip().startswith("<svg"):
        raise ValueError(f"Missing SVG markup for {entry.get('id')}")
    if not relative.startswith("assets/symbols/") or not relative.endswith(".svg"):
        raise ValueError(f"Unexpected SVG output path: {relative}")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markup + "\n", encoding="utf-8")
    written.append(target)

metadata = [{key: value for key, value in entry.items() if key != "svgMarkup"} for entry in entries]
metadata_path = DOWNLOAD_ROOT / "metadata-pages-34-36.json"
metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
readme_path = DOWNLOAD_ROOT / "README.txt"
readme_path.write_text(
    "Symbols Studio — SVG batch, printed pages 34–36\n"
    f"{len(written)} individual SVG files, vectorized from the supplied scanned page.\n"
    "First-pass contour traces: review shapes manually before production use.\n"
    "Source: Henry Dreyfuss, Symbol Sourcebook, McGraw-Hill, 1972, p. 34.\n",
    encoding="utf-8",
)

with ZipFile(BUNDLE, "w", ZIP_DEFLATED) as archive:
    for path in written:
        archive.write(path, path.relative_to(ROOT / "assets" / "symbols"))
    archive.write(metadata_path, "metadata.json")
    archive.write(readme_path, "README.txt")

print(f"Exported {len(written)} standalone SVG files to {SVG_ROOT}")
print(f"Created {BUNDLE}")
