#!/usr/bin/env python3
"""Build V3 法义读本 as a continuous Kumarajiva-style reader.

Editorial stance (docs/V3_DHARMA_READER.md):
  If 罗什 were to re-translate the Āgamas for reading — not for catalog —
  he would NOT keep T99 short titles like「如来第一」「离贪法第一」in sequence.
  He would open with doctrine, collapse peyyāla variants, and write continuous
  chapters with new pedagogical titles.

This builder:
  - Uses hand-authored chapter/section titles (通读新拟)
  - Melts multiple SA sources into one literary + one modern passage
  - Strips repeated 如是我闻 / 欢喜奉行 frames inside a section
  - Emits edition_map for audit (信 at unit/cluster level)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.titles import to_cn_num  # noqa: E402

CORPUS = ROOT / "data" / "translated" / "final_translated_data.json"
OUT_DIR = ROOT / "data" / "metadata" / "v3"
UNITS_OUT = ROOT / "data" / "translated" / "v3_reader_units.json"

# ---------------------------------------------------------------------------
# Continuous outline: titles are NEW; sources are pools to melt (not reprint).
# Order ≈ 罗什若译阿含之教学序：先安信，次观法，次缘起，次修道，次证果，末对机。
# ---------------------------------------------------------------------------

CHAPTERS: list[dict] = [
    {
        "id": 1,
        "title": "开经·正信",
        "blurb": "先明听法因缘与不坏净信，使心有所归，然后可观法。",
        "sections": [
            {
                "title": "听法因缘",
                "sources": [902, 903, 904],
                "lead_lit": "若欲入佛法海，当先立信。信不坏者，于佛、法、僧及圣戒，心无异向。",
                "lead_mod": "想真正学佛，先要把信心立稳。信心不坏，就是对佛、法、僧和清净戒，心里不再摇摆。",
            },
            {
                "title": "不坏净与四果之基",
                "sources": [1121, 1122, 1123, 1125, 1127, 1129],
                "lead_lit": "世尊教诸弟子：成就不坏净，则趣向诸道果，如病得药、如闇遇明。",
                "lead_mod": "佛陀教导：成就不动摇的清净信，就能趣向各阶道果——像病得药、暗中见光。",
            },
            {
                "title": "学处总说",
                "sources": [816, 820, 830, 840, 850, 860],
                "lead_lit": "既有正信，当知所应学。学有增上，戒定慧展转相依，不可偏废。",
                "lead_mod": "有了正信，还要知道该学什么。戒、定、慧互相增上，缺一不可。",
            },
        ],
    },
    {
        "id": 2,
        "title": "观五蕴",
        "blurb": "色受想行识，皆无常、苦、空、非我。此为阿含观行之枢要。",
        "sections": [
            {
                "title": "五阴无常",
                "sources": [1, 2, 8, 9, 10],
                "lead_lit": "一时佛在舍卫国祇树给孤独园。尔时世尊告诸比丘：当观五阴。",
                "lead_mod": "有一次佛在舍卫国祇园。他对比丘们说：应当观察五蕴。",
            },
            {
                "title": "五阴是苦",
                "sources": [11, 12, 13, 14, 15],
                "lead_lit": "复次，当观五阴是苦。无常故苦，苦故非我所应贪着。",
                "lead_mod": "再进一步：五蕴是苦。因为无常，所以是苦；既是苦，就不该贪着。",
            },
            {
                "title": "空与非我",
                "sources": [16, 17, 18, 19, 20, 21, 22],
                "lead_lit": "复次，五阴空、非我、非我所。若于五阴生我我所想，则长夜轮转。",
                "lead_mod": "再观：五蕴是空，不是我，也不属于我。若在五蕴上执着我、我所，就会长期流转。",
            },
            {
                "title": "厌离与解脱",
                "sources": [30, 31, 32, 33, 34, 50, 51],
                "lead_lit": "观已正知，则生厌离；厌离故贪尽；贪尽故心解脱。心解脱者，所作已办。",
                "lead_mod": "如理观察之后，就会厌离；厌离则贪尽；贪尽则心解脱。心解脱了，该做的就做成了。",
            },
            {
                "title": "炽然与出要",
                "sources": [70, 80, 90, 100, 108],
                "lead_lit": "世尊以种种方便，示五阴如炽然、如重担，劝令速求灭度，出离火宅。",
                "lead_mod": "佛又用种种比喻，说五蕴像烈火、像重担，劝人赶快求出离。",
            },
        ],
    },
    {
        "id": 3,
        "title": "观六入",
        "blurb": "眼色、耳声乃至意法，触生受，受生爱。知处、护根，则苦边可尽。",
        "sections": [
            {
                "title": "六入处总观",
                "sources": [188, 189, 190, 195, 200],
                "lead_lit": "尔时世尊告诸比丘：眼、耳、鼻、舌、身、意，是谓内六入处；色、声、香、味、触、法，是谓外六入处。",
                "lead_mod": "佛告诉比丘：眼耳鼻舌身意是内六处；色声香味触法是外六处。",
            },
            {
                "title": "触受与系缚",
                "sources": [210, 220, 230, 240, 250],
                "lead_lit": "根境相对则有识，三事和合名触；触缘受，受缘爱。爱取有生，苦蕴集起。",
                "lead_mod": "根与境相对就有识，三者会合叫触；由触有受，由受有爱。爱取推动有与生，苦蕴就聚起来。",
            },
            {
                "title": "护根与离染",
                "sources": [255, 273, 274, 280, 1164, 1170],
                "lead_lit": "是故比丘当护根门：见色不取相、不取好，耳声乃至意法，亦复如是。护根故不漏，不漏故心定，心定故如实知。",
                "lead_mod": "所以要守住根门：看见色不要抓取相貌好坏，听声乃至对意法也一样。护根就不漏失，不漏则心定，心定才能如实了知。",
            },
        ],
    },
    {
        "id": 4,
        "title": "观缘起",
        "blurb": "此有故彼有，此灭故彼灭。十二支还灭，是大沙门所说中道。",
        "sections": [
            {
                "title": "缘起法住",
                "sources": [283, 284, 285, 286, 287],
                "lead_lit": "世尊说缘起：此有故彼有，此生故彼生；此无故彼无，此灭故彼灭。若佛出世、若不出世，此法常住。",
                "lead_mod": "佛说缘起：有此故有彼，生此故生彼；无此则无彼，灭此则灭彼。不论佛出不出世，这个法则都在。",
            },
            {
                "title": "十二支流转",
                "sources": [290, 295, 300, 310, 320],
                "lead_lit": "所谓无明缘行，行缘识，识缘名色，名色缘六入，六入缘触，触缘受，受缘爱，爱缘取，取缘有，有缘生，生缘老死忧悲苦恼。如是纯大苦聚集。",
                "lead_mod": "也就是：无明缘行，行缘识……一直到生缘老死忧悲苦恼。整个大苦堆就这样聚起来。",
            },
            {
                "title": "还灭与中道",
                "sources": [330, 340, 350, 360, 370],
                "lead_lit": "无明灭则行灭，乃至生灭则老死灭，纯大苦聚灭。离有无二边，是名中道，大沙门所说。",
                "lead_mod": "无明灭则行灭，一直到生灭则老死灭，大苦堆也就灭了。离开有无两边，这叫中道，是大沙门所说。",
            },
        ],
    },
    {
        "id": 5,
        "title": "食受谛见",
        "blurb": "明四食、诸受、四谛，并简邪见，令知苦集灭道。",
        "sections": [
            {
                "title": "四食",
                "sources": [371, 372, 373, 374, 375],
                "lead_lit": "有四食，长养众生：抟食、触食、意思食、识食。当观其集、灭、味、患、离。",
                "lead_mod": "有四种食养众生：段食、触食、意思食、识食。要观察它们的集起、灭尽、滋味、过患与出离。",
            },
            {
                "title": "诸受",
                "sources": [455, 456, 460, 470, 480],
                "lead_lit": "受有三种：乐受、苦受、不苦不乐受。于乐受生染，于苦受生恚，于舍受生痴，是为结缚。若如实知受，则不受后有。",
                "lead_mod": "受有三种：乐、苦、不苦不乐。对乐起贪、对苦起瞋、对舍起痴，就是结缚。若如实知受，就不再受后有。",
            },
            {
                "title": "四圣谛",
                "sources": [379, 380, 385, 390, 400, 406],
                "lead_lit": "此苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛。若如实证知，则生眼、智、明、觉。",
                "lead_mod": "这就是苦、集、灭、道四圣谛。真正证知，就会生起法眼与智慧光明。",
            },
            {
                "title": "断知与离见",
                "sources": [130, 131, 133, 140, 150, 160, 170],
                "lead_lit": "种种见：有见、无见、我见、断常，皆依五阴而起。当断、当知、当离，勿随见网。",
                "lead_mod": "种种邪见——有、无、我、断、常——都依五蕴而起。要断、要知、要离，别陷进见网。",
            },
        ],
    },
    {
        "id": 6,
        "title": "修道",
        "blurb": "念处、根力、觉支、八正道、安那般那——道品一贯，如众流归海。",
        "sections": [
            {
                "title": "四念处",
                "sources": [605, 606, 610, 620, 630, 639],
                "lead_lit": "有一乘道，净众生、度忧悲、灭苦恼、得如实法，谓四念处：身、受、心、法，循身观乃至循法观，精勤觉知，除世间贪忧。",
                "lead_mod": "有一条一乘之道，能清净众生、度脱忧悲、灭除苦恼，就是四念处：观身、受、心、法，精勤觉知，去掉世间贪忧。",
            },
            {
                "title": "五根五力",
                "sources": [642, 650, 660, 670, 680, 690, 700],
                "lead_lit": "信根、精进根、念根、定根、慧根；修之满，则成信力乃至慧力，能摧未伏烦恼。",
                "lead_mod": "信、精进、念、定、慧五根；修到充满，就成为五力，能摧破还没降伏的烦恼。",
            },
            {
                "title": "七觉支",
                "sources": [704, 710, 720, 730, 740, 747],
                "lead_lit": "念觉支、择法、精进、喜、轻安、定、舍——七觉分，顺向涅槃。",
                "lead_mod": "念、择法、精进、喜、轻安、定、舍——七觉支，通向涅槃。",
            },
            {
                "title": "八正道",
                "sources": [748, 750, 760, 770, 780, 790, 796],
                "lead_lit": "正见、正志、正语、正业、正命、正方便、正念、正定，是名八圣道分，苦灭之道。",
                "lead_mod": "正见、正志、正语、正业、正命、正精进、正念、正定，就是八圣道，灭苦之路。",
            },
            {
                "title": "安那般那念",
                "sources": [797, 800, 805, 810, 815],
                "lead_lit": "修安那般那念，系心出入息，能满四念处，满七觉支，顺趣涅槃。",
                "lead_mod": "修入出息念，心系在呼吸上，能圆满四念处与七觉支，趣向涅槃。",
            },
        ],
    },
    {
        "id": 7,
        "title": "修证",
        "blurb": "由信而修，由修而证。入流乃至无生，皆不离先所说观与道。",
        "sections": [
            {
                "title": "向果与证果",
                "sources": [873, 875, 880, 885, 890, 891],
                "lead_lit": "须陀洹、斯陀含、阿那含、阿罗汉——有向有果。断三结入流，乃至漏尽无生。",
                "lead_mod": "须陀洹到阿罗汉，有「向」有「果」。断三结就入流，直到漏尽、不再受生。",
            },
            {
                "title": "解脱知見",
                "sources": [1124, 1130, 1131, 1135, 1136],
                "lead_lit": "心解脱已，自知自证：我生已尽，梵行已立，所作已作，不受后有。",
                "lead_mod": "心解脱之后，自己清楚：生死已尽，梵行已立，该做的已做，不再受后有。",
            },
        ],
    },
    {
        "id": 8,
        "title": "善说与对机",
        "blurb": "弟子所演、对机问答，取其开决心疑者，以助通读，不求备载诸众。",
        "sections": [
            {
                "title": "舍利弗与目连之说",
                "sources": [490, 491, 495, 500, 501, 502, 503],
                "lead_lit": "大弟子承佛神力，为众说法，与世尊所说无异，皆令向厌、离欲、灭尽。",
                "lead_mod": "大弟子秉承佛的力量为大家说法，和佛说的一致，都是引导厌离、离欲、趋向灭尽。",
            },
            {
                "title": "阿难与质多之问",
                "sources": [537, 540, 556, 560, 566, 570, 575],
                "lead_lit": "阿难多闻，质多居士善问。一问一答，法义朗然，如净水现月。",
                "lead_mod": "阿难博学多闻，质多居士善于提问。一问一答，法义清楚，像净水映月。",
            },
            {
                "title": "譬喻与决外道",
                "sources": [940, 950, 960, 1023, 1030, 1241, 1250, 1260],
                "lead_lit": "或以譬喻破执，或对外道显示正法：业报不亡，中道离边，勿随邪论。",
                "lead_mod": "有时用比喻破执着，有时对外道开示：业报不失，中道离边，不要跟着邪论走。",
            },
        ],
    },
]


_OPEN_RE = re.compile(
    r"^如是我闻[：:，,\s]*一时[^。]*[。．]\s*",
)
_OPEN_MOD_RE = re.compile(
    r"^(?:我是这样听说的[：:]\s*)?(?:有一次[，,]?)?[^。\n]*(?:住在|在)[^。\n]*[。．]\s*",
)
_CLOSE_ANY_RE = re.compile(
    r"(?:时)?诸比丘闻(?:佛|世尊)所说[，,]?欢喜奉行[。．]?",
)
_CLOSE_MOD_RE = re.compile(
    r"(?:比丘们|大家)听(?:了|佛所说)[^。]*欢喜奉行[。．]?",
)
_END_FORMULA_RE = re.compile(
    r"(?:佛说此经已|佛说完这部经)[，,]?\s*",
)
_MID_OPEN_LIT_RE = re.compile(
    r"(?:尔时)?世尊告诸比丘[：:]",
)


def _sa_num(rec: dict) -> int:
    return int(str(rec["id"]).split("_")[1])


def _strip_frame(text: str, *, modern: bool) -> str:
    t = (text or "").strip()
    if not t:
        return ""
    # Global cleanup of nidāna / closing formulas (any position)
    t = re.sub(r"如是我闻[：:，,\s]*[^。…\n]*[。．…]+", "", t)
    t = re.sub(r"我是这样听说的[：:][^\n]*\n?", "", t)
    t = re.sub(r"有一次[，,]?(?:佛|世尊)[^。\n]*(?:住在|在)[^。\n]*[。．]\s*", "", t)
    t = _CLOSE_ANY_RE.sub("", t)
    t = _CLOSE_MOD_RE.sub("", t)
    t = _END_FORMULA_RE.sub("", t)
    t = re.sub(r"欢喜奉行[。．]?", "", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def _pick_sources(by_id: dict[int, dict], ids: list[int]) -> list[dict]:
    out: list[dict] = []
    for n in ids:
        rec = by_id.get(n)
        if not rec:
            continue
        if not (rec.get("kumarajiva_style_text") or "").strip():
            continue
        out.append(rec)
    return out


def _compose_field(
    recs: list[dict],
    field: str,
    *,
    lead: str,
    modern: bool,
) -> str:
    parts: list[str] = []
    if lead:
        parts.append(lead.strip())
    for i, rec in enumerate(recs):
        body = _strip_frame(rec.get(field) or "", modern=modern)
        if not body:
            continue
        if not modern and i > 0:
            body = _MID_OPEN_LIT_RE.sub("又告诸比丘：", body, count=1)
            parts.append(body if body.startswith("又告") else "又告诸比丘：" + body)
        elif modern and i > 0:
            body = re.sub(
                r"^那时世尊告诉比丘们[：:]",
                "佛又告诉比丘们：",
                body,
                count=1,
            )
            if not body.startswith("佛又"):
                body = "佛又告诉比丘们：" + body
            parts.append(body)
        else:
            if lead and not modern:
                body = _MID_OPEN_LIT_RE.sub("世尊告诸比丘：", body, count=1)
            parts.append(body)

    closing = (
        "时诸比丘闻佛所说，欢喜奉行。"
        if not modern
        else "比丘们听了，都欢喜奉行。"
    )
    text = "\n".join(p for p in parts if p)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"欢喜奉行[。．]?", "", text)
    text = text.strip() + "\n" + closing
    return text.strip()


def _note(section_title: str, chapter_title: str, sources: list[int], used: list[int]) -> str:
    ids = "、".join(str(x) for x in used)
    return (
        f"本段「{section_title}」属通读新拟篇题，编入「{chapter_title}」。"
        f"熔铸大正第{ids}经等罗什风译文，去其重复开经结经，连贯成文；"
        f"非逐经照录，亦非大正原题。"
    )


def main() -> None:
    recs = json.loads(CORPUS.read_text(encoding="utf-8"))
    by_id = {_sa_num(r): r for r in recs}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    UNITS_OUT.parent.mkdir(parents=True, exist_ok=True)

    edition_map: list[dict] = []
    units_out: list[dict] = []
    seq = 0

    for ch in CHAPTERS:
        for sec in ch["sections"]:
            seq += 1
            sources = list(sec["sources"])
            picked = _pick_sources(by_id, sources)
            if not picked:
                raise SystemExit(f"no sources for {ch['title']} / {sec['title']}: {sources}")

            lit = _compose_field(
                picked,
                "kumarajiva_style_text",
                lead=sec.get("lead_lit") or "",
                modern=False,
            )
            mod = _compose_field(
                picked,
                "modern_psychology_text",
                lead=sec.get("lead_mod") or "",
                modern=True,
            )
            used = [_sa_num(r) for r in picked]
            unit_id = f"V3-{ch['id']:02d}-{seq:04d}"
            title = sec["title"]
            note = _note(title, ch["title"], sources, used)

            edition_map.append(
                {
                    "v3_unit_id": unit_id,
                    "seq": seq,
                    "chapter_id": ch["id"],
                    "chapter_title": ch["title"],
                    "title_zh": title,
                    "title_kind": "pedagogical_new",
                    "source_sa_t99": used,
                    "requested_sa_t99": sources,
                    "edit_ops": "melt_continuous",
                    "rationale": "罗什风通读：新拟篇题，多经熔文，去重复程式",
                }
            )
            units_out.append(
                {
                    "id": unit_id,
                    "seq": seq,
                    "chapter_id": ch["id"],
                    "chapter_title": ch["title"],
                    "title": title,
                    "source_sa": used[0],
                    "source_sas": used,
                    "source_id": picked[0]["id"],
                    "primary_sn_uid": picked[0].get("primary_sn_uid") or "",
                    "review_status": "v3_composed",
                    "kumarajiva_style_text": lit,
                    "modern_psychology_text": mod,
                    "note": note,
                }
            )

    catalog = {
        "schema_version": 2,
        "title_zh": "法义读本（罗什风通读）",
        "editorial": (
            "篇题为通读新拟，不沿用大正短题；"
            "正文由多经罗什风译文熔铸，去重复开经结经。"
            "假定：若鸠摩罗什为通读而译阿含，当如是重编，而非逐经照录经目。"
        ),
        "policy": "docs/V3_DHARMA_READER.md",
        "chapters": [
            {
                "id": c["id"],
                "title": c["title"],
                "blurb": c["blurb"],
                "sections": [s["title"] for s in c["sections"]],
            }
            for c in CHAPTERS
        ],
        "stats": {
            "units": len(units_out),
            "chapters": len(CHAPTERS),
            "source_sa_used": len({s for u in units_out for s in u["source_sas"]}),
        },
    }

    (OUT_DIR / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "edition_map.json").write_text(
        json.dumps(edition_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    UNITS_OUT.write_text(
        json.dumps(units_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "reader_index.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "title_zh": catalog["title_zh"],
                "editorial": catalog["editorial"],
                "chapters": catalog["chapters"],
                "units": [
                    {
                        "id": u["id"],
                        "seq": u["seq"],
                        "chapter_id": u["chapter_id"],
                        "chapter_title": u["chapter_title"],
                        "title": u["title"],
                        "source_sas": u["source_sas"],
                    }
                    for u in units_out
                ],
                "stats": catalog["stats"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"wrote {len(units_out)} continuous sections / {len(CHAPTERS)} chapters")
    print(f"stats: {catalog['stats']}")
    for u in units_out[:8]:
        print(f"  {u['seq']:02d} {u['chapter_title']} · {u['title']} ← SA{u['source_sas']}")


if __name__ == "__main__":
    main()
