"""V2 academic reading order (Anesaki/Yinshun fascicle reconstruction)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2_META = ROOT / "data" / "metadata" / "v2"


@lru_cache(maxsize=1)
def _load_index() -> dict:
    path = V2_META / "academic_order_index.json"
    if not path.exists():
        raise FileNotFoundError(
            f"missing {path}; run: python scripts/build_v2_academic_order.py"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def reading_order_sa_t99() -> list[int]:
    """T99 SA ids in academic main-text order (insertions excluded)."""
    return list(_load_index()["reading_order_sa_t99"])


def appendix_sa_t99() -> list[int]:
    return list(_load_index()["appendix_sa_t99"])


def lookup(sa_t99: int) -> dict | None:
    return _load_index()["by_sa_t99"].get(str(sa_t99))


def academic_seq(sa_t99: int) -> int | None:
    """1-based seq in main stream, or None if appendix / unknown."""
    info = lookup(sa_t99)
    if not info or info.get("role") != "main":
        return None
    return int(info["seq"])


def is_appendix(sa_t99: int) -> bool:
    info = lookup(sa_t99)
    return bool(info and info.get("role") == "appendix")
