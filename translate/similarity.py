"""Detect '繁转简' style failures: literary too close to Guṇabhadra source."""

from __future__ import annotations

import re
import unicodedata


def _to_simplified_approx(s: str) -> str:
    # Normalize punctuation / whitespace; leave chars (most gold already simplified).
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", "", s)
    s = s.replace("：", ":").replace("；", ";").replace("，", ",").replace("。", ".")
    s = s.replace("「", "").replace("」", "").replace("『", "").replace("』", "")
    s = s.replace("（", "(").replace("）", ")")
    # traditional→simplified common Buddhist chars
    table = str.maketrans(
        {
            "無": "无",
            "觀": "观",
            "斷": "断",
            "離": "离",
            "愛": "爱",
            "爾": "尔",
            "時": "时",
            "為": "为",
            "於": "于",
            "諸": "诸",
            "國": "国",
            "樹": "树",
            "給": "给",
            "獨": "独",
            "園": "园",
            "衛": "卫",
            "說": "说",
            "經": "经",
            "樂": "乐",
            "實": "实",
            "當": "当",
            "應": "应",
            "滅": "灭",
            "盡": "尽",
            "後": "后",
            "證": "证",
            "識": "识",
            "陰": "阴",
            "與": "与",
            "從": "从",
            "來": "来",
            "對": "对",
            "開": "开",
            "聞": "闻",
            "處": "处",
            "眾": "众",
            "惱": "恼",
            "憂": "忧",
            "變": "变",
            "易": "易",
            "報": "报",
            "達": "达",
            "獲": "获",
            "種": "种",
            "類": "类",
            "會": "会",
            "義": "义",
            "見": "见",
            "覺": "觉",
            "觀": "观",
        }
    )
    return s.translate(table)


def _trigrams(s: str) -> set[str]:
    if len(s) < 3:
        return {s} if s else set()
    return {s[i : i + 3] for i in range(len(s) - 2)}


def similarity_to_source(chinese: str, literary: str) -> float:
    a = _to_simplified_approx(chinese)
    b = _to_simplified_approx(literary)
    if not a or not b:
        return 0.0
    ta, tb = _trigrams(a), _trigrams(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def is_too_literal(chinese: str, literary: str, threshold: float = 0.72) -> bool:
    """True if Kumarajiva column is suspiciously close to source (繁转简嫌疑)."""
    return similarity_to_source(chinese, literary) >= threshold
