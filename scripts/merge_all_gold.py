#!/usr/bin/env python3
"""Merge all scripts/retranslate_sa*.py GOLD dicts into final corpus (safe, gold-only overwrite)."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from translate.similarity import similarity_to_source  # noqa: E402
from translate.validate import validate_restyle  # noqa: E402

GOLD_STATUSES = {"gold", "gold_reconstructed"}


def load_gold_from_script(path: Path) -> dict[str, dict]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if not spec or not spec.loader:
        return {}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(getattr(mod, "GOLD", {}) or {})


def main() -> None:
    scripts = sorted(
        (ROOT / "scripts").glob("retranslate_sa*.py"),
        key=lambda p: p.name,
    )
    gold: dict[str, dict] = {}
    for p in scripts:
        g = load_gold_from_script(p)
        if not g:
            continue
        gold.update(g)
        print(f"loaded {len(g):4d} from {p.name}")

    out = ROOT / "data" / "translated" / "final_translated_data.json"
    aligned = ROOT / "data" / "aligned" / "raw_aligned_data.json"
    gold_dir = ROOT / "data" / "golden"
    gold_dir.mkdir(parents=True, exist_ok=True)

    by_id: dict[str, dict] = {}
    if out.exists():
        for r in json.loads(out.read_text(encoding="utf-8")):
            by_id[r["id"]] = r
    for r in json.loads(aligned.read_text(encoding="utf-8")):
        by_id.setdefault(r["id"], r)

    report = []
    for rid, g in sorted(gold.items(), key=lambda x: int(x[0].split("_")[1])):
        item = dict(by_id.get(rid) or {"id": rid})
        item["kumarajiva_style_text"] = g["kumarajiva_style_text"]
        item["modern_psychology_text"] = g["modern_psychology_text"]
        item["notes"] = g.get("notes") or ""
        item["translator"] = "cursor-agent"
        # reconstructed heuristic
        if "gold_reconstructed" in (g.get("notes") or "") or rid in getattr(
            sys.modules.get(rid, object()), "RECONSTRUCTED", set()
        ):
            pass
        status = "gold"
        conf = "high"
        if "gold_reconstructed" in item["notes"] or "不作臆造" in item["notes"] or "仅作交叉" in item["notes"]:
            status = "gold_reconstructed"
            conf = "low"
        elif "confidence=medium" in item["notes"] or "无可靠" in item["notes"]:
            conf = "medium"
        item["review_status"] = status
        item["confidence"] = conf
        v = validate_restyle(
            item.get("chinese_text") or "",
            item["kumarajiva_style_text"],
            item["modern_psychology_text"],
        )
        item["validation"] = v
        item["forbidden_hits"] = v.get("forbidden_hits") or []
        sim = similarity_to_source(item.get("chinese_text") or "", item["kumarajiva_style_text"])
        item["similarity_to_source"] = round(sim, 3)
        by_id[rid] = item
        (gold_dir / f"{rid.lower()}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        report.append({"id": rid, "status": v["status"], "sim": round(sim, 3)})

    merged = sorted(by_id.values(), key=lambda x: int(x["id"].split("_")[1]))
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "web" / "public" / "final_translated_data.json").write_text(
        out.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (ROOT / "data" / "translated" / "gold_merge_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    statuses = {}
    for r in merged:
        statuses[r.get("review_status")] = statuses.get(r.get("review_status"), 0) + 1
    print(f"corpus={len(merged)} gold_entries={len(gold)} statuses={statuses}")
    high_sim = [r for r in report if r["sim"] >= 0.55]
    print(f"sim>=0.55: {len(high_sim)}")


if __name__ == "__main__":
    main()
