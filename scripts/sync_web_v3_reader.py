#!/usr/bin/env python3
"""Sync V3 reader JSON into web/public/."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [
    (
        ROOT / "data" / "translated" / "v3_reader_units.json",
        ROOT / "web" / "public" / "v3_reader_units.json",
    ),
    (
        ROOT / "data" / "metadata" / "v3" / "reader_index.json",
        ROOT / "web" / "public" / "v3_reader_index.json",
    ),
]


def main() -> None:
    for src, dst in PAIRS:
        if not src.is_file():
            raise SystemExit(f"missing {src}; run: make v3-reader")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"synced {src.name} → {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
