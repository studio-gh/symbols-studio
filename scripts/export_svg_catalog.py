#!/usr/bin/env python3
"""Build the page-by-page Symbols Studio vector catalogue for GitHub Pages."""
from __future__ import annotations
import gzip, json, re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets" / "symbols"
DOWNLOADS = ROOT / "assets" / "downloads"
ASSETS.mkdir(parents=True, exist_ok=True)
DOWNLOADS.mkdir(parents=True, exist_ok=True)

def clean_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()[:100] or "symbol"

records = []
seen = set()
for page in range(34, 39):
    source = DATA / f"symbols-page{page}.json.gz"
    items = json.loads(gzip.decompress(source.read_bytes()).decode("utf-8"))
    if not items or any(str(item.get("page")) != str(page) for item in items):
        raise ValueError(f"Source page mismatch: {page}")
    for item in items:
        svg = item.get("svgMarkup", "")
        if not svg.strip().startswith("<svg"):
            raise ValueError(f"Missing SVG markup: {item.get('id')}")
        if 'xmlns=' not in svg[:260]:
            svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        key = clean_id(str(item.get("id") or f"page-{page}-symbol"))
        filename = f"{key}.svg"
        if filename in seen:
            filename = f"{key}-p{page}.svg"
        seen.add(filename)
        (ASSETS / filename).write_text(svg.rstrip() + "\n", encoding="utf-8")
        item["svgFile"] = f"./assets/symbols/{filename}"
        item["svgMarkup"] = svg
        item["kind"] = "visual"
        records.append(item)

if len(records) != 177:
    raise ValueError(f"Expected 177 real sourcebook vector records, found {len(records)}")
(DATA / "symbols-pages-batch01.json").write_text(
    json.dumps(records, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
)
with ZipFile(DOWNLOADS / "symbols-pages-34-38-svg.zip", "w", ZIP_DEFLATED) as archive:
    for path in sorted(ASSETS.glob("*.svg")):
        archive.write(path, path.name)
    archive.writestr("metadata.json", json.dumps(
        [{k:v for k,v in r.items() if k != "svgMarkup"} for r in records],
        ensure_ascii=False, indent=2
    ) + "\n")
print("Published 177 individual SVGs from printed pages 34–38.")
