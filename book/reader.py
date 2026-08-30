"""Reader-facing text for book export (not implementation jargon)."""

from __future__ import annotations

import re

from pipeline.titles import (
    is_t99_insertion,
    juan_label,
    samyukta_label,
    short_title,
    t99_insertion_tag,
    to_cn_num,
)

# Traditional → simplified (single characters for titles / 相应名)
_TRAD_SIMPL = str.maketrans(
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
        "諸": "诸",
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
        "覺": "觉",
        "證": "证",
        "識": "识",
        "陰": "阴",
        "蘊": "蕴",
        "雜": "杂",
        "羅": "罗",
        "緣": "缘",
        "處": "处",
        "諦": "谛",
        "業": "业",
        "報": "报",
        "學": "学",
        "聖": "圣",
        "釋": "释",
        "質": "质",
        "壞": "坏",
        "淨": "净",
        "縛": "缚",
        "繫": "系",
        "著": "着",
        "邊": "边",
        "據": "据",
        "剎": "刹",
        "藥": "药",
        "師": "师",
        "龍": "龙",
        "電": "电",
        "難": "难",
        "動": "动",
        "搖": "摇",
        "輸": "输",
        "屢": "屡",
        "結": "结",
        "閑": "闲",
        "願": "愿",
        "問": "问",
        "見": "见",
        "過": "过",
        "數": "数",
        "憂": "忧",
        "惱": "恼",
        "連": "连",
        "難": "难",
        "難": "难",
    }
)


def simp(s: str) -> str:
    return (s or "").translate(_TRAD_SIMPL)


def reader_short_title(n: int, raw: str | None = None) -> str:
    return simp(short_title(n, raw))


def reader_samyukta(n: int) -> str:
    return simp(samyukta_label(n))


def reader_juan(n: int) -> str:
    return juan_label(n)


def samyukta_sections(lo: int, hi: int) -> list[tuple[int, int, str]]:
    """Split a 卷 id range by 相应 (品目) boundaries."""
    sections: list[tuple[int, int, str]] = []
    cur = samyukta_label(lo)
    start = lo
    for n in range(lo + 1, hi + 2):
        label = samyukta_label(n) if n <= hi else None
        if n > hi or label != cur:
            sections.append((start, n - 1, reader_samyukta(start)))
            if n <= hi:
                start = n
                cur = label or cur
    return sections


def juan_chapter_title(lo: int, hi: int) -> str:
    """卷首标题：整卷同一相应则「卷第一 · 阴相应」，否则仅「卷第七」."""
    sections = samyukta_sections(lo, hi)
    juan = reader_juan(lo)
    if len(sections) == 1:
        return f"卷{juan} · {sections[0][2]}"
    return f"卷{juan}"


def sutta_heading(n: int, rec: dict) -> str:
    """经题：（经号）短题；相应名见卷首或品目分节。"""
    recon = "◇ " if rec.get("review_status") == "gold_reconstructed" else ""
    num = to_cn_num(n)
    title = reader_short_title(n, rec.get("title"))
    return f"{recon}（{num}）{title}"


def sutta_tag(rec: dict) -> str:
    if rec.get("review_status") == "gold_reconstructed":
        return "〔重建经·底本略〕"
    n = int(str(rec.get("id") or "SA_0").split("_")[-1])
    if is_t99_insertion(n):
        return t99_insertion_tag() or "〔T99插入·非相应经〕"
    return ""


def uid_to_reader(uid: str) -> str:
    if not uid:
        return ""
    u = uid.lower()
    m = re.match(r"(sn|an|sa|mn|dn)(\d+)\.(\d+)", u)
    if not m:
        return uid
    corpus, maj, min_ = m.groups()
    names = {"sn": "相应部", "an": "增支部", "mn": "中部", "dn": "长部", "sa": "杂阿含"}
    return f"《{names.get(corpus, corpus.upper())}》{maj}.{min_}"


def normalize_chinese_quotes(text: str) -> str:
    """Replace ASCII '…' with nested Chinese quotes 『…』 in reader-facing prose."""
    if not text:
        return ""
    return re.sub(r"'([^'\n]+)'", r"『\1』", text)


def clean_chinese_text(text: str) -> str:
    """Strip SC headers and T99 fascicle titles (错简卷题) from 底本."""
    if not text:
        return ""
    s = text.strip()
    s = re.sub(r"^Saṁyuktāgama(?:雜阿含經|杂阿含经)?\s*", "", s)
    s = re.sub(
        r"^(?:\u3000\s*\n+)?(?:雜阿含經|杂阿含经)卷[^\n]+\n+\s*宋天竺三藏求那跋陀(?:罗|羅)譯\s*\n+",
        "",
        s,
    )
    # Standalone fascicle title lines anywhere (卷界／错简卷题，非经正文)
    s = re.sub(
        r"^[ \u3000\t]*(?:雜阿含經|杂阿含经)\s*卷第[^\n]*\n+",
        "",
        s,
        flags=re.MULTILINE,
    )
    s = re.sub(
        r"\n+[ \u3000\t]*(?:雜阿含經|杂阿含经)\s*卷第[^\n]*\s*$",
        "",
        s,
    )
    s = re.sub(r"(?:雜阿含經|杂阿含经)\s*卷第[^\n]*\s*$", "", s, flags=re.MULTILINE)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def clean_notes(notes: str) -> str:
    if not notes:
        return ""
    s = notes
    s = re.sub(r"本经 SC 平行表所列平行及.*?传统术语。", "", s)
    s = re.sub(
        r"SC 于本经未列可靠巴利平行.*?medium/low」。",
        "无可靠巴利平行，依汉本并参同类型经厘定。",
        s,
    )
    # No trailing colon: mid-sentence "confidence=medium。" must not become "平行较弱：。"
    s = re.sub(r"confidence\s*=\s*high[：:]?", "据平行经", s)
    s = re.sub(r"confidence\s*=\s*medium[：:]?", "平行较弱", s)
    s = re.sub(r"confidence\s*=\s*low[：:]?", "无强平行", s)
    s = re.sub(r"review_status\s*=\s*gold_reconstructed[，,]?", "", s)
    s = re.sub(r"gold_reconstructed[，,]?", "", s)
    s = re.sub(r"`raw_aligned_data\.json`", "语料", s)
    s = re.sub(r"\s+", " ", s).strip(" ；，。")
    s = re.sub(r"[：:](?=[。．.])", "", s)
    # Drop empty confidence leftovers
    s = re.sub(r"^(平行较弱|无强平行|据平行经)\s*$", "", s)
    s = re.sub(r"(平行较弱|无强平行|据平行经)\s*$", "", s)
    return simp(s).strip(" ；，。")


def _english_source_label(rec: dict) -> tuple[str, str]:
    """Return (english text, attribution) for parallel excerpt."""
    sn = (rec.get("english_sn_text") or "").strip()
    sa = (rec.get("english_sa_text") or "").strip()
    if sn:
        return sn, "Bhikkhu Sujato（CC0）"
    if not sa:
        return "", ""
    if sa.startswith("Thus I have heard") or "Bhagavān" in sa[:200]:
        return sa, "Charles Patton（CC0）"
    return sa, "Bhikkhu Anālayo（原刊《法鼓佛学学报》等；SC 经译者授权在其平台刊载；本书仅短摘录）"


def format_parallels_reader(rec: dict) -> list[str]:
    lines: list[str] = []
    primary = rec.get("primary_sn_uid")
    if primary:
        lines.append(f"所据巴利经：{uid_to_reader(str(primary))}")

    seen = {primary} if primary else set()
    for p in rec.get("parallels") or []:
        uid = p.get("uid") or ""
        if not uid or uid in seen:
            continue
        if (p.get("root_lang") or "").lower() != "pli":
            continue
        seen.add(uid)
        otitle = simp(p.get("original_title") or "")
        ttitle = p.get("translated_title") or ""
        label = uid_to_reader(str(uid))
        extra = f"《{otitle}》" if otitle else ""
        if ttitle:
            extra += f"（{ttitle}）"
        lines.append(f"相关平行：{label}{extra}")

    if not lines:
        lines.append("（本条无巴利专经平行；义理据底本及同类型经）")

    pali = (rec.get("pali_text") or "").strip()
    if pali:
        excerpt = pali[:600] + ("…" if len(pali) > 600 else "")
        lines.append("巴利原文（摘；Mahāsaṅgīti 数字本）：" + excerpt)

    en, en_attr = _english_source_label(rec)
    if en:
        excerpt = en[:600] + ("…" if len(en) > 600 else "")
        lines.append(f"英译（摘；{en_attr}）：" + excerpt)

    return lines


def label_source() -> str:
    return "【底本·求那跋陀罗译】"


def label_modern() -> str:
    return "【今译意】"


def label_literary() -> str:
    return "【正文·仿罗什风】"


def label_critical() -> str:
    return "【校勘与说明】"


def label_parallels() -> str:
    return "【巴利平行与参考译文】"
