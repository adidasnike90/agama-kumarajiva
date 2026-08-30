#!/usr/bin/env python3
"""Fetch SuttaCentral original_title for all SA sutras (title metadata)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline import HttpClient, SC_API  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1362)
    parser.add_argument("--sleep", type=float, default=0.05)
    args = parser.parse_args()

    out_path = ROOT / "data" / "metadata" / "sc_original_titles.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    titles: dict[str, str] = {}
    if out_path.exists():
        titles = json.loads(out_path.read_text(encoding="utf-8"))

    cache = ROOT / "data" / "cache"
    with HttpClient(cache_dir=cache) as client:
        for n in range(args.start, args.end + 1):
            key = str(n)
            if key in titles and titles[key].strip():
                continue
            try:
                data = client.get_json(f"{SC_API}/suttaplex/sa{n}")
                if isinstance(data, list):
                    data = data[0]
                ot = (data.get("original_title") or "").strip()
                ot = re.sub(r"\s+", "", ot)
                if ot:
                    titles[key] = ot
                    print(f"SA_{n} → {ot}")
            except Exception as e:  # noqa: BLE001
                print(f"SA_{n} WARN {e}")
            time.sleep(args.sleep)

    out_path.write_text(
        json.dumps(
            dict(sorted(titles.items(), key=lambda x: int(x[0]))),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"wrote {len(titles)} titles → {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
