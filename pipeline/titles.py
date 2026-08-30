"""Canonical SA display titles."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data" / "metadata"

# Legacy manual overrides (short titles where SC/Bilara metadata is wrong).
SHORT_TITLES: dict[int, str] = {
    604: "阿育王傳（施沙）",
    640: "法滅授記",
    641: "半阿摩勒",
    1: "無常",
    33: "非我",
    34: "無我",
    35: "三正士",
    36: "自洲",
    37: "我",
    38: "卑下",
    39: "種子",
    40: "封滯",
    41: "五轉",
    42: "七處",
    43: "取著",
    44: "繫著",
    45: "覺",
    46: "三世陰世食",
    47: "信",
    48: "信",
    49: "阿難",
    50: "阿難",
}

CN_NUM = "〇一二三四五六七八九"


@lru_cache(maxsize=1)
def _load_juan_ends() -> list[tuple[int, str]]:
    path = META / "juan_ends.json"
    if path.exists():
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [(int(a), str(b)) for a, b in raw]
    return [
        (32, "第一"),
        (58, "第二"),
        (87, "第三"),
        (102, "第四"),
        (110, "第五"),
    ]


@lru_cache(maxsize=1)
def _load_samyukta_ranges() -> list[tuple[int, int, str]]:
    path = META / "samyukta_taisho.json"
    if not path.exists():
        return [(1, 110, "陰相應")]
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [(int(r["start"]), int(r["end"]), r["label"]) for r in raw]


@lru_cache(maxsize=1)
def _load_t99_insertions() -> tuple[frozenset[int], str]:
    path = META / "t99_insertions.json"
    if not path.exists():
        return frozenset(), ""
    raw = json.loads(path.read_text(encoding="utf-8"))
    ids = frozenset(int(n) for n in raw.get("sutta_ids") or [])
    tag = str(raw.get("reader_tag") or "").strip()
    return ids, tag


def is_t99_insertion(n: int) -> bool:
    return n in _load_t99_insertions()[0]


def t99_insertion_tag() -> str:
    return _load_t99_insertions()[1]


@lru_cache(maxsize=1)
def _load_sc_short_titles() -> dict[int, str]:
    path = META / "sc_original_titles.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {int(k): v for k, v in raw.items()}


def to_cn_num(n: int) -> str:
    """T99-style sutta numeral for headings (一…一〇…一〇二…)."""
    if n <= 0:
        return str(n)
    if n == 10:
        return "一〇"
    if 1 <= n <= 9:
        return CN_NUM[n]
    if 11 <= n <= 19:
        return "一" + CN_NUM[n - 10]
    if 20 <= n <= 99:
        tens, ones = divmod(n, 10)
        if ones == 0:
            return CN_NUM[tens] + "〇"
        return CN_NUM[tens] + CN_NUM[ones]
    if n == 100:
        return "一〇〇"
    # 101–1362: per-digit with 〇 (T99 经号)
    return "".join(CN_NUM[int(c)] for c in str(n))


def juan_label(n: int) -> str:
    ends = _load_juan_ends()
    for end, label in ends:
        if n <= end:
            return label
    # T99 has 50 fascicles; IDs past the last mapped end stay in 卷第五十
    if ends:
        return ends[-1][1]
    return "？"


def samyukta_label(n: int) -> str:
    for start, end, label in _load_samyukta_ranges():
        if start <= n <= end:
            return label
    return "（待標定相应）"


def extract_short_from_good_title(raw: str, n: int) -> str | None:
    cn = to_cn_num(n)
    m = re.search(rf"[（(]{re.escape(cn)}[）)]\s*([^\s（(/]+)", raw)
    if m:
        name = re.sub(r"\(SA.*$", "", m.group(1)).strip()
        if name and name not in {"陰相應", "杂阿含经", "雜阿含經"}:
            return name
    m2 = re.search(rf"[（(]{n}[）)]\s*([^\s（(/]+)", raw)
    if m2:
        return m2.group(1).strip()
    return None


def short_title(n: int, raw: str | None = None) -> str:
    if n in SHORT_TITLES:
        return SHORT_TITLES[n]
    sc = _load_sc_short_titles()
    if n in sc and sc[n].strip():
        return sc[n].strip()
    if raw:
        found = extract_short_from_good_title(raw, n)
        if found:
            return found
    return f"第{to_cn_num(n)}经"


def normalize_title(n: int, raw: str | None = None) -> str:
    """Format: 雜阿含經  卷第一  陰相應  （N）  短題."""
    return (
        f"雜阿含經  卷{juan_label(n)}  {samyukta_label(n)}  "
        f"（{to_cn_num(n)}）  {short_title(n, raw)}"
    )
