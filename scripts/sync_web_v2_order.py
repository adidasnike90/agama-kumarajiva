#!/usr/bin/env python3
"""Copy v2 academic-order index into web/public for the Vite reader."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "metadata" / "v2" / "academic_order_index.json"
DST = ROOT / "web" / "public" / "academic_order_index.json"


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"missing {SRC}; run: make v2-order")
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, DST)
    print(f"synced {SRC.name} → {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
