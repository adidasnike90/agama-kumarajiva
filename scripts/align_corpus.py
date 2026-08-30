#!/usr/bin/env python3
"""Align SA corpus in batches and merge into raw_aligned_data.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.align import build_record  # noqa: E402
from pipeline import HttpClient  # noqa: E402
from pipeline.titles import normalize_title  # noqa: E402
from rich.console import Console

console = Console()


def merge_records(master_path: Path, new_records: list[dict]) -> list[dict]:
    by_id: dict[str, dict] = {}
    if master_path.exists():
        for r in json.loads(master_path.read_text(encoding="utf-8")):
            by_id[r["id"]] = r
    for r in new_records:
        n = int(r["id"].split("_")[1])
        r["title"] = normalize_title(n, r.get("title") or "")
        by_id[r["id"]] = r
    return sorted(by_id.values(), key=lambda x: int(x["id"].split("_")[1]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=51)
    parser.add_argument("--end", type=int, default=1362)
    parser.add_argument("--batch", type=int, default=50)
    args = parser.parse_args()

    master = ROOT / "data" / "aligned" / "raw_aligned_data.json"
    cache = ROOT / "data" / "cache"
    aligned_dir = ROOT / "data" / "aligned"
    aligned_dir.mkdir(parents=True, exist_ok=True)

    with HttpClient(cache_dir=cache) as client:
        for lo in range(args.start, args.end + 1, args.batch):
            hi = min(lo + args.batch - 1, args.end)
            batch: list[dict] = []
            for n in range(lo, hi + 1):
                console.print(f"[cyan]Fetching SA {n}…[/cyan]")
                rec = build_record(client, n)
                if rec["errors"]:
                    console.print(f"  [yellow]{rec['errors']}[/yellow]")
                batch.append(rec)
            batch_path = aligned_dir / f"raw_aligned_sa{lo}-{hi}.json"
            batch_path.write_text(
                json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            merged = merge_records(master, batch)
            master.write_text(
                json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            console.print(
                f"[green]SA {lo}–{hi} merged; total={len(merged)}[/green]"
            )


if __name__ == "__main__":
    main()
