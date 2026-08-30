#!/usr/bin/env python3
"""Normalize sutra titles across aligned/translated/golden JSON files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.titles import normalize_title  # noqa: E402


def patch_file(path: Path) -> int:
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    if isinstance(data, list):
        items = data
        wrapper = "list"
    elif isinstance(data, dict) and "id" in data:
        items = [data]
        wrapper = "dict"
    else:
        return 0
    for rec in items:
        rid = rec.get("id") or ""
        m = re.match(r"SA_(\d+)$", rid)
        if not m:
            continue
        n = int(m.group(1))
        new = normalize_title(n, rec.get("title") or "")
        if rec.get("title") != new:
            rec["title"] = new
            changed += 1
    if changed:
        out = items if wrapper == "list" else items[0]
        path.write_text(
            json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return changed


def main() -> None:
    paths = [
        ROOT / "data" / "aligned" / "raw_aligned_data.json",
        ROOT / "data" / "aligned" / "raw_aligned_sa31-50.json",
        ROOT / "data" / "translated" / "final_translated_data.json",
        ROOT / "web" / "public" / "final_translated_data.json",
        ROOT / "data" / "golden" / "sa1-10_bundle.json",
    ]
    paths.extend(sorted((ROOT / "data" / "golden").glob("sa_*.json")))
    total = 0
    for p in paths:
        c = patch_file(p)
        if c:
            print(f"{p.relative_to(ROOT)}: {c} titles")
            total += c
    d = json.loads(
        (ROOT / "data" / "translated" / "final_translated_data.json").read_text(
            encoding="utf-8"
        )
    )
    for r in d:
        n = int(r["id"].split("_")[1])
        if n in (1, 14, 32, 33, 34, 36, 37, 50):
            print(r["id"], "→", r["title"])
    print(f"done, patches={total}")


if __name__ == "__main__":
    main()
