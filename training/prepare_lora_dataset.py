#!/usr/bin/env python3
"""Convert data/golden/*.json into Alpaca-style JSONL for later LoRA."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data" / "golden"
OUT = ROOT / "data" / "golden" / "lora_sft.jsonl"


def main() -> None:
    files = sorted(GOLD.glob("*.json"))
    files = [f for f in files if f.name != "lora_sft.jsonl"]
    if not files:
        print("No golden JSON files yet.", file=sys.stderr)
        raise SystemExit(1)
    rows = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else [data]
        for rec in items:
            if rec.get("review_status") not in {"reviewed", "gold"}:
                continue
            if not rec.get("kumarajiva_style_text"):
                continue
            rows.append(
                {
                    "instruction": "将下列杂阿含旧译改写为鸠摩罗什风格汉语，并保持原始佛教义理。",
                    "input": rec.get("chinese_text") or "",
                    "output": rec["kumarajiva_style_text"],
                    "id": rec.get("id"),
                }
            )
    OUT.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + ("\n" if rows else ""),
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} examples → {OUT}")


if __name__ == "__main__":
    main()
