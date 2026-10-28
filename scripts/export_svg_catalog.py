#!/usr/bin/env python3
"""Build the visual SVG catalogue only from validated source records."""
from __future__ import annotations
import json, re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets" / "symbols"
DOWNLOADS = ROOT / "assets" / "downloads"
ASSETS.mkdir(parents=True, exist_ok=True)
DOWNLOADS.mkdir(parents=True, exist_ok=True)

# The compressed source payloads currently in the repo fail gzip validation.
# Do not let optional exports block the Pages deployment. If a validated visual
# batch is already present, export that data; otherwise keep deployment intact.
def clean_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()[:100] or "symbol"

batch_file = DATA / "symbols-pages-batch01.json"
if not batch_file.exists():
    print("No validated visual batch available; keeping static site deployable.")
    raise SystemExit(0)

records = json.loads(batch_file.read_text(encoding="utf-8"))
if not isinstance(records, list):
    raise ValueError("Visual batch must be a JSON list.")
seen = set()
for item in records:
    svg = item.get("svgMarkup", "")
    if not isinstance(svg, str) or not svg.strip().startswith("<svg"):
        raise ValueError(f"Missing SVG markup: {item.get('id')}")
    page = str(item.get("page", ""))
    if not page:
        raise ValueError(f"Missing source page: {item.get('id')}")
    key = clean_id(str(item.get("id") or f"page-{page}-symbol"))
    filename = f"{key}.svg"
    if filename in seen:
        filename = f"{key}-p{page}.svg"
    seen.add(filename)
    if 'xmlns=' not in svg[:260]:
        svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    (ASSETS / filename).write_text(svg.rstrip() + "\n", encoding="utf-8")
    item["svgFile"] = f"./assets/symbols/{filename}"
    item["svgMarkup"] = svg
    item["kind"] = "visual"

with (DATA / "symbols-pages-batch01.json").open("w", encoding="utf-8") as stream:
    json.dump(records, stream, ensure_ascii=False, separators=(",", ":"))
    stream.write("\n")

with ZipFile(DOWNLOADS / "symbols-pages-svg.zip", "w", ZIP_DEFLATED) as archive:
    for path in sorted(ASSETS.glob("*.svg")):
        archive.write(path, path.name)
    archive.writestr("metadata.json", json.dumps(
        [{k:v for k,v in item.items() if k != "svgMarkup"} for item in records],
        ensure_ascii=False, indent=2
    ) + "\n")
print(f"Published {len(records)} SVG records from the validated visual batch.")
