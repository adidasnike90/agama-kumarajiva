"""Heuristic Kumarajiva-style restyle + modern plain (batch corpus)."""

from __future__ import annotations

import re
from typing import Any

TRAD_SIMPL = str.maketrans(
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
        "聞": "闻",
        "處": "处",
        "眾": "众",
        "惱": "恼",
        "憂": "忧",
        "變": "变",
        "報": "报",
        "獲": "获",
        "種": "种",
        "類": "类",
        "會": "会",
        "義": "义",
        "見": "见",
        "覺": "觉",
        "麁": "粗",
        "醜": "丑",
        "繫": "系",
        "攝": "摄",
        "陽": "阳",
        "門": "门",
        "問": "问",
        "歡": "欢",
        "踊": "踊",
        "躍": "跃",
        "頭": "头",
        "禮": "礼",
        "邊": "边",
        "聖": "圣",
        "聽": "听",
        "壞": "坏",
        "不": "不",
        "壞": "坏",
        "諸": "诸",
        "餘": "余",
        "難": "难",
        "提": "提",
        "邏": "逻",
        "睺": "睺",
        "羅": "罗",
        "頻": "频",
        "婆": "婆",
        "娑": "娑",
        "門": "门",
        "閻": "阎",
        "羅": "罗",
        "王": "王",
        "舍": "舍",
        "城": "城",
        "竹": "竹",
        "園": "园",
        "精": "精",
        "舍": "舍",
        "祇": "祇",
        "樹": "树",
        "給": "给",
        "孤": "孤",
        "獨": "独",
        "園": "园",
    }
)

PHRASE_FIXES: list[tuple[str, str]] = [
    (r"欲令如是、不令如是", "得大自在；不得自在"),
    (r"亦得于色欲令如是、不令如是", "亦应得大自在"),
    (r"舍衛國", "舍卫国"),
    (r"如是我聞：?", "如是我闻："),
    (r"爾時，?", "尔时，"),
    (r"比丘！", "比丘："),
    (r"諸比丘！", "诸比丘："),
    (r"沙門、婆羅門", "沙门、婆罗门"),
    (r"五受陰", "五受阴"),
    (r"五取蘊", "五取蕴"),
    (r"([色受想行識])⋯", r"\1、"),
    (r"⋯+", "……"),
    (r"……([，。；])", r"\1"),
    (r"  +", ""),
]


def clean_source(text: str) -> str:
    # Strip SC HTML chrome / Taishō front matter (do NOT delete body after mid-text 卷 markers).
    text = re.sub(r"Sa[ṁm]yuktāgama雜阿含經", "", text)
    text = re.sub(r"Sa[ṁm]yuktāgama杂阿含经", "", text)
    text = re.sub(r"Sa[ṁm]yuktāgama", "", text)
    text = re.sub(r"(?s)^.*?(?=如是我聞|如是我闻|爾時|尔时)", "", text, count=1)
    text = re.sub(
        r"雜阿含經卷第?[一二三四五六七八九十百〇]+",
        "",
        text,
    )
    text = re.sub(
        r"杂阿含经卷第?[一二三四五六七八九十百〇]+",
        "",
        text,
    )
    text = re.sub(r"宋天竺三藏求那跋陀羅譯", "", text)
    text = re.sub(r"宋天竺三藏求那跋陀罗译", "", text)
    text = re.sub(r"第[一二三四五六七八九十]+誦[^\n。]*", "", text)
    text = re.sub(r"T\s*\d{4}[a-c]\d{2}", "", text)
    text = re.sub(r"\s+", "", text)
    return text.strip()


def stylize_literary(source: str) -> str:
    t = clean_source(source)
    t = t.translate(TRAD_SIMPL)
    t = t.replace("祇樹給孤獨園", "祇树给孤独园")
    for pat, repl in PHRASE_FIXES:
        t = re.sub(pat, repl, t)
    t = re.sub(
        r"([色受想行识])、([色受想行识])、([色受想行识])、([色受想行识])、([色受想行识])",
        "色、受、想、行、识",
        t,
    )
    t = re.sub(
        r"([色受想行识])、([色受想行识])、([色受想行识])、([色受想行识])",
        "受、想、行、识",
        t,
    )
    t = re.sub(r"(如是我闻：)", r"\1\n", t)
    t = re.sub(r"(一时[^。]+。)", r"\1\n", t, count=1)
    t = re.sub(r"(佛说此经已[^。]+。)", r"\n\1", t)
    t = re.sub(r"\n{2,}", "\n", t)
    return t.strip()


def to_modern_plain(literary: str) -> str:
    lines = [ln.strip() for ln in literary.split("\n") if ln.strip()]
    out: list[str] = []
    for ln in lines:
        m = ln
        if m.startswith("如是我闻"):
            m = "我是这样听说的：" + m[len("如是我闻：") :]
        elif m.startswith("尔时"):
            m = "那时，" + m[2:]
            m = m.replace("告诸比丘：", "世尊告诉比丘们：")
        elif "佛说此经已" in m:
            m = m.replace(
                "佛说此经已，诸比丘闻佛所说，欢喜奉行。",
                "佛说完这部经，比丘们听佛所说，都欢喜奉行。",
            )
            m = m.replace("佛说此经已，", "佛说完这部经，")
            m = m.replace("欢喜奉行。", "都欢喜奉行。")
        out.append(m)
    return "\n".join(out) if out else literary


def build_notes(record: dict[str, Any]) -> str:
    sn = record.get("primary_sn_uid") or ""
    if sn:
        return f"据 {sn.upper()} 平行；批量初译，待人工复核。"
    return "无可靠 SC 主平行；依汉本雅化。批量初译，待人工复核。confidence=medium。"


def stylize_record(record: dict[str, Any]) -> dict[str, str]:
    src = record.get("chinese_text") or ""
    if not src.strip():
        return {
            "kumarajiva_style_text": "",
            "modern_psychology_text": "",
            "notes": "源文本缺失。",
        }
    lit = stylize_literary(src)
    modern = to_modern_plain(lit)
    if "如是我闻" in src and "如是我闻" not in lit:
        lit = "如是我闻：\n" + lit
        modern = "我是这样听说的：\n" + modern
    if "欢喜奉行" in src and "欢喜奉行" not in lit:
        lit += "\n佛说此经已，诸比丘闻佛所说，欢喜奉行。"
        modern += "\n佛说完这部经，比丘们听佛所说，都欢喜奉行。"
    return {
        "kumarajiva_style_text": lit,
        "modern_psychology_text": modern,
        "notes": build_notes(record),
    }
