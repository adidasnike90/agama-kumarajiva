"""Post-edit validation for 信达雅 restyles."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Early markers that should usually survive in literary restyle of 阴相应
EARLY_MARKERS = [
    "无常",
    "苦",
    "空",
    "非我",
    "厌",
    "解脱",
]

STOCK_AWAKENING = ["我生已尽", "梵行已立", "所作已作"]

FRAME = ["如是我闻", "欢喜奉行"]


def load_forbidden_terms() -> list[str]:
    path = ROOT / "glossary" / "forbidden_mahayana.txt"
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def find_forbidden_hits(text: str) -> list[str]:
    return [t for t in load_forbidden_terms() if t in text]


def _norm(s: str) -> str:
    # unify common variants for checks
    table = str.maketrans(
        {
            "無": "无",
            "觀": "观",
            "斷": "断",
            "離": "离",
            "愛": "爱",
            "顯": "显",
            "爾": "尔",
            "時": "时",
            "為": "为",
            "與": "与",
            "於": "于",
            "從": "从",
            "來": "来",
            "對": "对",
            "開": "开",
            "關": "关",
            "門": "门",
            "聞": "闻",
            "國": "国",
            "樹": "树",
            "給": "给",
            "獨": "独",
            "園": "园",
            "爾": "尔",
            "諸": "诸",
            "衛": "卫",
            "祇": "祇",
            "說": "说",
            "經": "经",
            "樂": "乐",
            "實": "实",
            "當": "当",
            "應": "应",
            "滅": "灭",
            "盡": "尽",
            "後": "后",
            "覺": "觉",
            "證": "证",
            "識": "识",
            "陰": "阴",
            "蘊": "蕴",
        }
    )
    return s.translate(table)


def validate_restyle(source_zh: str, literary: str, modern: str) -> dict:
    """Return machine checks; does not replace human review."""
    src = _norm(source_zh)
    lit = _norm(literary)
    mod = _norm(modern)
    combined = lit + "\n" + mod

    issues: list[str] = []
    warnings: list[str] = []

    hits = find_forbidden_hits(combined)
    if hits:
        issues.append(f"forbidden:{','.join(hits)}")

    for frame in FRAME:
        nframe = _norm(frame)
        if nframe in src and nframe not in lit:
            warnings.append(f"missing_frame:{frame}")
        # Modern column must keep the same narrative frame as literary
        if nframe in lit and nframe not in mod and frame == "如是我闻":
            # modern may paraphrase as「我是这样听说的」
            if "我是这样听说" not in mod and "如是我闻" not in mod:
                issues.append("modern_missing_opening_frame")
        if frame == "欢喜奉行" and nframe in lit and nframe not in mod:
            issues.append("modern_missing_closing_frame")

    # If source has awakening stock, literary should keep it
    if all(_norm(p) in src for p in STOCK_AWAKENING):
        for p in STOCK_AWAKENING:
            if _norm(p) not in lit:
                issues.append(f"missing_stock:{p}")

    # Aggregate coverage: only when source is clearly about the five aggregates,
    # not incidental 色/识 in compounds like 善知识、色泽.
    agg_context = any(
        k in src
        for k in ("五受阴", "五阴", "五蕴", "色受阴", "色阴", "受阴", "想阴", "行阴", "识阴")
    )
    if agg_context and "色" in src and "识" in src:
        for sk in ("色", "受", "想", "行", "识"):
            if sk not in lit:
                if "五阴" in lit or "五蕴" in lit or "五受阴" in lit:
                    warnings.append(f"condensed_aggregate:{sk}")
                else:
                    issues.append(f"missing_aggregate:{sk}")

    # Core marks: only check the sutta body (before 欢喜奉行), ignoring uddāna tails
    src_body = src
    for end in ("欢喜奉行", "歡喜奉行"):
        if end in src_body:
            src_body = src_body.split(end)[0]
            break
    for mark in ("无常", "苦", "空", "非我"):
        if mark in src_body and mark not in lit and mark not in mod:
            warnings.append(f"mark_not_in_output:{mark}")

    if len(lit) < max(40, int(len(re.sub(r"\s+", "", src)) * 0.25)):
        warnings.append("literary_suspiciously_short")

    status = "ok"
    if issues:
        status = "fail"
    elif warnings:
        status = "warn"

    return {
        "status": status,
        "issues": issues,
        "warnings": warnings,
        "forbidden_hits": hits,
    }
