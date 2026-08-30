#!/usr/bin/env python3
"""Batch-stylize aligned SA records → final_translated_data.json + golden files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.titles import normalize_title  # noqa: E402
from translate.similarity import similarity_to_source  # noqa: E402
from translate.stylize import stylize_record  # noqa: E402
from translate.validate import validate_restyle  # noqa: E402

GOLD_STATUSES = {"gold", "gold_reconstructed"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=51)
    parser.add_argument("--end", type=int, default=1362)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-stylize even if a draft already exists (never overwrite gold)",
    )
    parser.add_argument(
        "--aligned",
        type=Path,
        default=ROOT / "data" / "aligned" / "raw_aligned_data.json",
    )
    args = parser.parse_args()

    out = ROOT / "data" / "translated" / "final_translated_data.json"
    gold_dir = ROOT / "data" / "golden"
    gold_dir.mkdir(parents=True, exist_ok=True)

    if out.exists():
        records = json.loads(out.read_text(encoding="utf-8"))
        by_id = {r["id"]: r for r in records}
    else:
        by_id = {}

    aligned = json.loads(args.aligned.read_text(encoding="utf-8"))
    report: list[dict] = []

    for rec in aligned:
        n = int(rec["id"].split("_")[1])
        if n < args.start or n > args.end:
            continue
        rid = rec["id"]
        item = dict(by_id.get(rid, rec))
        if item.get("review_status") in GOLD_STATUSES and item.get(
            "kumarajiva_style_text"
        ):
            continue
        existing = (item.get("kumarajiva_style_text") or "").strip()
        zh = (rec.get("chinese_text") or item.get("chinese_text") or "").strip()
        # Skip non-empty drafts unless --force or clearly truncated (卷标题误删正文)
        if (
            existing
            and not args.force
            and not (
                len(zh) > 200
                and len(existing) < max(40, int(len(zh) * 0.05))
            )
        ):
            continue
        item.update(
            {
                k: rec[k]
                for k in (
                    "chinese_text",
                    "english_sa_text",
                    "parallels",
                    "primary_sn_uid",
                    "pali_text",
                    "english_sn_text",
                    "errors",
                )
                if k in rec
            }
        )
        n = int(rid.split("_")[1])
        item["title"] = normalize_title(n, rec.get("title") or "")
        styled = stylize_record(item)
        item["kumarajiva_style_text"] = styled["kumarajiva_style_text"]
        item["modern_psychology_text"] = styled["modern_psychology_text"]
        item["notes"] = styled["notes"]
        item["translator"] = "cursor-agent-batch"
        sim = similarity_to_source(item["chinese_text"], item["kumarajiva_style_text"])
        v = validate_restyle(
            item["chinese_text"],
            item["kumarajiva_style_text"],
            item["modern_psychology_text"],
        )
        item["validation"] = v
        item["forbidden_hits"] = v.get("forbidden_hits") or []
        if sim >= 0.72 or v["status"] == "fail":
            item["review_status"] = "needs_revision"
            item["confidence"] = "low"
        elif sim >= 0.55:
            item["review_status"] = "machine_draft"
            item["confidence"] = "medium"
        else:
            item["review_status"] = "machine_draft"
            item["confidence"] = "medium"
        by_id[rid] = item
        (gold_dir / f"{rid.lower()}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        report.append({"id": rid, "sim": round(sim, 2), **v})

    merged = sorted(by_id.values(), key=lambda x: int(x["id"].split("_")[1]))
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_corpus.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fails = sum(1 for r in report if r["status"] == "fail")
    warns = sum(1 for r in report if r["status"] == "warn")
    print(
        f"translated {len(report)} records (SA {args.start}–{args.end}); "
        f"total corpus={len(merged)}; validation fail={fails} warn={warns}"
    )


if __name__ == "__main__":
    main()
