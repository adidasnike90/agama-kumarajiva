#!/usr/bin/env python3
"""Mirror publication corpus to web/public for the Vite reader."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "translated" / "final_translated_data.json"
DST = ROOT / "web" / "public" / "final_translated_data.json"


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"missing corpus: {SRC}")
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, DST)
    print(f"synced {SRC.name} → {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
