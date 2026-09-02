#!/usr/bin/env python3
"""Copy built research-edition PDFs into web/public/books/ for the reader downloads."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "public" / "books"

COPIES = [
    (ROOT / "book" / "build" / "main.pdf", "v1-taisho.pdf"),
    (ROOT / "book_v2" / "build" / "main.pdf", "v2-reorder.pdf"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ok = 0
    for src, name in COPIES:
        dst = OUT / name
        if not src.is_file():
            print(f"skip (missing): {src.relative_to(ROOT)}")
            continue
        shutil.copy2(src, dst)
        mb = dst.stat().st_size / (1024 * 1024)
        print(f"synced {src.relative_to(ROOT)} → {dst.relative_to(ROOT)} ({mb:.1f} MiB)")
        ok += 1
    if ok == 0:
        raise SystemExit(
            "no PDFs copied; run `make book` / `make book-v2` first, or keep existing web/public/books/"
        )


if __name__ == "__main__":
    main()
