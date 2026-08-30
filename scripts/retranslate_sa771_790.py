#!/usr/bin/env python3
"""Retranslate SA 771–790（圣道分相应 卷三十：彼岸／一法／非法／断贪／邪正）→ merge.

本批二十经：
  771–774 彼岸 SN45.34（772–774 peyyāla 异问者）
  775–781 一法 SN45.76／77（内不正思惟／外恶知识；781 省文）
  782 非法是法（对举 peyyāla）
  783 断贪 SN45.5（阿难；末段 peyyāla）
  784–785 邪正 SN45.21／MN117（785 世／出世间二种）
  786–788 向邪 AN10.103／AN1.306
  789 生闻（正见二种；末段 peyyāla）
  790 邪正（趣／道）

信：有 SN／AN 平行者据巴利／Sujato 厘义；求那跋陀罗汉本定位。
    peyyāla／交叉指示补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_771–790；不触碰 SA_751–770、SA_791+（并行批次）；
      断言 SA_770 不变（若尚未 gold 则断言最近前序 gold）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from translate.quality_gate import assess_gold  # noqa: E402
from translate.similarity import similarity_to_source  # noqa: E402
from translate.validate import validate_restyle  # noqa: E402

# ---------------------------------------------------------------------------
# 共用框式
# ---------------------------------------------------------------------------

OPEN_JET_LIT = "如是我闻：一时，佛住舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_KOS_LIT = "如是我闻：一时，佛住拘睒弥国瞿师罗园。"
OPEN_KOS_MOD = "我是这样听说的：有一次，佛住在拘睒弥国瞿师罗园。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

EIGHT_WRONG_LIT = "邪见、邪志、邪语、邪业、邪命、邪方便、邪念、邪定"
EIGHT_WRONG_MOD = "邪见、邪志、邪语、邪业、邪命、邪方便、邪念、邪定"
EIGHT_RIGHT_LIT = "正见、正志、正语、正业、正命、正方便、正念、正定"
EIGHT_RIGHT_MOD = "正见、正志、正语、正业、正命、正方便、正念、正定"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

VERSE_PARA_LIT = (
    "尔时世尊说偈言：「希有诸人民，能度于彼岸；"
    "一切诸世间，徘徊游此岸。"
    "于此正法律，能善随顺者，"
    "斯等能度彼，生死难度岸。」"
)
VERSE_PARA_MOD = (
    "那时世尊说偈：「人间能到彼岸的很少；"
    "其余世间人，只在此岸徘徊。"
    "能善随顺这正法律的人，"
    "才能度过那难渡的生死岸。」"
)

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 771 彼岸（生闻；SN45.34）--------------------------------------------
SUTTAS["SA_771"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有生闻婆罗门来诣佛所，问讯已，退坐一面，白佛言："
        "「瞿昙！云何非彼岸？云何彼岸？」",
        f"佛告婆罗门：「{EIGHT_WRONG_LIT}，是非彼岸；"
        f"{EIGHT_RIGHT_LIT}，是彼岸。」",
        VERSE_PARA_LIT,
        "生闻婆罗门闻已，欢喜随喜，从座起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有生闻婆罗门来到佛所，问讯后坐在一边，对佛说："
        "「瞿昙！什么是非彼岸？什么是彼岸？」",
        f"佛告诉婆罗门：「{EIGHT_WRONG_MOD}，是非彼岸；"
        f"{EIGHT_RIGHT_MOD}，是彼岸。」",
        VERSE_PARA_MOD,
        "生闻婆罗门听完，欢喜随喜，从座位起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.34 Pāraṅgama；"
        "汉作生闻问答，SN 直告比丘「八法能从此岸至彼岸」——保留汉问讯框，法义据八支。"
        "偈据汉本四颂，不补 SN 后半暗／明等颂。"
    ),
}

# --- SA 772–774 彼岸 peyyāla（异问者）---------------------------------------
_PARA_ASKERS = [
    (
        "SA_772",
        "异比丘问尊者阿难",
        "有异比丘来诣尊者阿难所，问讯已，白言：「云何非彼岸？云何彼岸？」"
        f"阿难答言：「{EIGHT_WRONG_LIT}，非彼岸；{EIGHT_RIGHT_LIT}，是彼岸。」"
        "并说彼岸偈，如上。彼比丘闻已，欢喜随喜而去。",
        "有一位比丘来到尊者阿难那里，问讯后说：「什么是非彼岸？什么是彼岸？」"
        f"阿难回答：「{EIGHT_WRONG_MOD}，是非彼岸；{EIGHT_RIGHT_MOD}，是彼岸。」"
        "并说彼岸偈，如前。那比丘听完，欢喜随喜离去。",
        "异比丘问阿难 → 据 SA771／SN45.34 彼岸八支＋偈纲",
    ),
    (
        "SA_773",
        "异比丘问佛",
        "有异比丘来诣佛所，白佛言：「世尊！云何非彼岸？云何彼岸？」"
        f"佛告比丘：「{EIGHT_WRONG_LIT}，非彼岸；{EIGHT_RIGHT_LIT}，是彼岸。」"
        "并说彼岸偈，如上。彼比丘闻已，欢喜奉行。",
        "有一位比丘来到佛所，对佛说：「世尊！什么是非彼岸？什么是彼岸？」"
        f"佛告诉比丘：「{EIGHT_WRONG_MOD}，是非彼岸；{EIGHT_RIGHT_MOD}，是彼岸。」"
        "并说彼岸偈，如前。那比丘听完，欢喜奉行。",
        "异比丘问佛 → 据 SA771／SN45.34 彼岸八支＋偈纲",
    ),
    (
        "SA_774",
        "问诸比丘",
        "尔时世尊告诸比丘：「云何非彼岸？云何彼岸？"
        f"{EIGHT_WRONG_LIT}，非彼岸；{EIGHT_RIGHT_LIT}，是彼岸。」"
        "并说彼岸偈。诸比丘闻佛所说，欢喜奉行。",
        "那时世尊告诉诸比丘：「什么是非彼岸？什么是彼岸？"
        f"{EIGHT_WRONG_MOD}，是非彼岸；{EIGHT_RIGHT_MOD}，是彼岸。」"
        "并说彼岸偈。比丘们听佛所说，都欢喜奉行。",
        "问诸比丘 → 据 SA771／SN45.34 彼岸八支＋偈纲",
    ),
]
for _rid, _label, _lit_body, _mod_body, _basis in _PARA_ASKERS:
    SUTTAS[_rid] = {
        "lit": [OPEN_JET_LIT, _lit_body],
        "mod": [OPEN_JET_MOD, _mod_body],
        "notes": (
            f"{PROV}confidence=medium：底本仅「{_label}等三经亦如上说」peyyāla；"
            f"据 SA771／SN45.34 补彼岸八支纲。reconstruction={_basis}。"
        ),
        "_recon": _basis,
    }

# --- SA 775 一法：不正思惟令邪道生（内）------------------------------------
SUTTAS["SA_775"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「于内法中，我不见一法能令未生恶不善法生、已生者增广，"
        "如不正思惟。不正思惟者，未起邪见令起，已起令增；"
        f"余邪支——邪志乃至邪定——亦复如是。」",
        "「于内法中，我不见一法能令未生恶不善法不生、已生者灭，如正思惟。"
        "正思惟者，未生邪见令不生，已生令灭；余邪支亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「在内心的法里，我不见有哪一法更能让未生的恶不善法生起、"
        "已生的再增广，像不正思惟这样。不正思惟会让未起的邪见生起，已起的再增广；"
        "其余邪志乃至邪定，也是这样。」",
        "「在内心的法里，我不见有哪一法更能让未生的恶不善法不生、已生的灭尽，像正思惟这样。"
        "正思惟会让未生的邪见不生，已生的灭尽；其余邪支也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling SN45.76／83（正思惟成就八正道）；"
        "汉本以「不正／正思惟」对邪道生灭立说，与 AN1 一法门近；"
        "保留汉构，八邪支压缩为邪见例＋余支例。"
    ),
}

# --- SA 776 一法：不正思惟令正道退（内）------------------------------------
SUTTAS["SA_776"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「于内法中，我不见一法能令未生善法不生、已生善法退减，"
        "如不正思惟。不正思惟者，未生正见令不生，已生令退；"
        "余正支——正志乃至正定——亦复如是。」",
        "「于内法中，我不见一法能令未生善法生、已生者增广，如正思惟。"
        "正思惟者，未生正见令生，已生令增；余正支亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「在内心的法里，我不见有哪一法更能让未生的善法不生、"
        "已生的善法退减，像不正思惟这样。不正思惟会让未生的正见不生，已生的退减；"
        "其余正志乃至正定，也是这样。」",
        "「在内心的法里，我不见有哪一法更能让未生的善法生起、已生的再增广，像正思惟这样。"
        "正思惟会让未生的正见生起，已生的再增广；其余正支也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling SN45.76；"
        "与 775 对举——不正思惟损正道、正思惟长正道；八支压缩。"
    ),
}

# --- SA 777 一法：合说（内）------------------------------------------------
SUTTAS["SA_777"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「于内法中，我不见一法能令恶不善法生而增、善法不生而退，"
        "如不正思惟。不正思惟者，令邪见乃至邪定生而增，"
        "令正见乃至正定不生而退。」",
        "「于内法中，我不见一法能令恶不善法不生而灭、善法生而增，如正思惟。"
        "正思惟者，令邪见乃至邪定不生而灭，令正见乃至正定生而增。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「在内心的法里，我不见有哪一法更能让恶不善法生起增广、"
        "善法不生退减，像不正思惟这样。不正思惟会让邪见乃至邪定生起增广，"
        "让正见乃至正定不生退减。」",
        "「在内心的法里，我不见有哪一法更能让恶不善法不生灭尽、善法生起增广，像正思惟这样。"
        "正思惟会让邪见乃至邪定不生灭尽，让正见乃至正定生起增广。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：775＋776 合说；"
        "压缩重复八支枚举为「乃至」式。"
    ),
}

# --- SA 778 一法：恶／善知识令邪道（外）------------------------------------
SUTTAS["SA_778"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「于外法中，我不见一法能令未生恶不善法生、已生者增广，"
        "如恶知识、恶伴党、恶随从。彼能令邪见乃至邪定生而增。」",
        "「于外法中，我不见一法能令未生恶不善法不生、已生者灭，"
        "如善知识、善伴党、善随从。彼能令邪见乃至邪定不生而灭。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「在外缘的法里，我不见有哪一法更能让未生的恶不善法生起、"
        "已生的再增广，像恶知识、恶同伴、恶随从这样。他们会让邪见乃至邪定生起增广。」",
        "「在外缘的法里，我不见有哪一法更能让未生的恶不善法不生、已生的灭尽，"
        "像善知识、善同伴、善随从这样。他们会让邪见乃至邪定不生灭尽。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.77／84（善知识成就八正道）；"
        "汉本兼说恶知识生邪道、善知识灭邪道；保留汉对举，义与 SN 善友门相摄。"
    ),
}

# --- SA 779 一法：善知识令正道（外）----------------------------------------
SUTTAS["SA_779"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「于外法中，我不见一法能令未生善法生、已生者增广，"
        "如善知识、善伴党、善随从。彼能令正见乃至正定生而增。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「在外缘的法里，我不见有哪一法更能让未生的善法生起、"
        "已生的再增广，像善知识、善同伴、善随从这样。他们会让正见乃至正定生起增广。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.77；"
        "专说善知识长养八正道；汉本略，不补恶知识退正道段。"
    ),
}

# --- SA 780 一法：外法合说--------------------------------------------------
SUTTAS["SA_780"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「于外法中，我不见一法能令恶不善法生而增、善法不生而退，"
        "如恶知识、恶伴党、恶随从。彼令邪见乃至邪定生而增，"
        "令正见乃至正定不生而退。」",
        "「于外法中，我不见一法能令恶不善法不生而灭、善法生而增，"
        "如善知识、善伴党、善随从。彼令邪见乃至邪定不生而灭，"
        "令正见乃至正定生而增。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「在外缘的法里，我不见有哪一法更能让恶不善法生起增广、"
        "善法不生退减，像恶知识、恶同伴、恶随从这样。他们让邪见乃至邪定生起增广，"
        "让正见乃至正定不生退减。」",
        "「在外缘的法里，我不见有哪一法更能让恶不善法不生灭尽、善法生起增广，"
        "像善知识、善同伴、善随从这样。他们让邪见乃至邪定不生灭尽，"
        "让正见乃至正定生起增广。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：778＋779 合说；八支压缩为「乃至」。"
        "据 SN45.77 善友门校正达意。"
    ),
}

# --- SA 781 一法：内法略＋peyyāla-------------------------------------------
SUTTAS["SA_781"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「于内法中，不正思惟能令邪见生而增、正见不生而退；"
        "正思惟能令邪见不生而灭、正见生而增。」",
        "「如说邪见、正见，余七支——邪志／正志乃至邪定／正定——亦复如是，如上。」",
        "「如内法八经，外法八经——以恶／善知识为缘——亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「在内心的法里，不正思惟会让邪见生起增广、正见不生退减；"
        "正思惟会让邪见不生灭尽、正见生起增广。」",
        "「就像邪见与正见这样说，其余七支——邪志与正志，乃至邪定与正定——也都一样，如前。」",
        "「就像内法这八经，外法八经——以恶知识、善知识为缘——也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：底本末「七经如上说／外法八经亦如是说」peyyāla；"
        "据 775–780 纲压缩。reconstruction=内八＋外八 peyyāla 摄记。"
    ),
    "_recon": "内法余七支＋外法八经 peyyāla 摄记（据 775–780）",
}

# --- SA 782 非法是法（对举 peyyāla）----------------------------------------
SUTTAS["SA_782"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有非法、是法。谛听，善思，当为汝说。"
        f"何等非法、是法？谓{EIGHT_WRONG_LIT}为非法，"
        f"{EIGHT_RIGHT_LIT}为是法。」",
        "「如非法／是法，非律／正律，非圣／是圣，不善／善，非习／习，"
        "非善哉／善哉，黑／白，非义／正义，卑／胜，有罪／无罪，应去／不去——"
        "一一经皆如上说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「有非法，也有正法。仔细听，好好想，我为你们说。"
        f"什么是非法、什么是正法？就是{EIGHT_WRONG_MOD}是非法，"
        f"{EIGHT_RIGHT_MOD}是正法。」",
        "「就像非法与正法这样，非律与正律、非圣与是圣、不善与善、非习与习、"
        "非善哉与善哉、黑与白、非义与正义、卑与胜、有罪与无罪、应舍与不应舍——"
        "每一经都如上说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium："
        "首经举八邪／八正；其余对举皆「如上说」peyyāla，摄记不展开。"
        "reconstruction=非法是法等十一对 peyyāla 压缩。"
    ),
    "_recon": "非法／是法以下十一对举 peyyāla 压缩",
}

# --- SA 783 断贪（阿难；SN45.5；末段 peyyāla）------------------------------
SUTTAS["SA_783"] = {
    "lit": [
        OPEN_KOS_LIT + "尊者阿难亦在彼住。",
        "有异婆罗门来诣阿难所，问讯已，退坐一面，白言："
        "「欲有所问，宁有闲暇为记说不？」"
        "阿难曰：「随问，知者当答。」",
        "婆罗门问：「何故于沙门瞿昙所出家修梵行？」"
        "答言：「为断故。」「断何等？」"
        "「断贪欲、瞋恚、愚癡。」",
        "「有道有迹，能断贪、瞋、癡耶？」"
        f"「有，谓八圣道——{EIGHT_RIGHT_LIT}。」",
        "婆罗门言：「贤哉之道！修习多修习，能断贪、瞋、癡。」"
        "闻已欢喜随喜，从座起去。",
        "「如断贪瞋癡，调伏、得涅槃、厌离、沙门义、婆罗门义、解脱、"
        "苦断、究竟苦边、正尽苦——一一经皆如上说。」",
    ],
    "mod": [
        OPEN_KOS_MOD + "尊者阿难也住在那里。",
        "有一位婆罗门来到阿难那里，问讯后坐在一边，说："
        "「想请教一个问题，可有空为我解说吗？」"
        "阿难说：「你问吧，知道的我会答。」",
        "婆罗门问：「为什么在沙门瞿昙那里出家修梵行？」"
        "答：「为了断除。」「断除什么？」"
        "「断除贪欲、瞋恚、愚癡。」",
        "「有没有道路、轨迹，能断贪、瞋、癡？」"
        f"「有，就是八圣道——{EIGHT_RIGHT_MOD}。」",
        "婆罗门说：「真是好道！修习、多修习，就能断贪、瞋、癡。」"
        "听完欢喜随喜，从座位起身离去。",
        "「就像断贪瞋癡这样，调伏、得涅槃、厌离、沙门义、婆罗门义、解脱、"
        "苦断、究竟苦边、正尽苦——每一经都如上说。」",
    ],
    "notes": (
        f"{PROV}confidence=high：resembling SN45.5（梵行目的／八正道）；"
        "汉作阿难答婆罗门「为断贪瞋癡」，SN 作比丘答外道「为遍知苦」——"
        "保留汉问答框，道迹据八支。末段目的 peyyāla 摄记。"
        "reconstruction=断贪等目的系列 peyyāla。"
    ),
    "_recon": "断贪瞋癡等目的系列 peyyāla 摄记",
}

# --- SA 784 邪正（定义；SN45.21／分析近 SN45.8）----------------------------
SUTTAS["SA_784"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有邪有正。谛听，善思，当为汝说。"
        f"何等为邪？谓{EIGHT_WRONG_LIT}。"
        f"何等为正？谓{EIGHT_RIGHT_LIT}。」",
        "「何等正见？谓知有施、有说、有斋，有善恶业及果报，有此世他世，"
        "有父母、有众生生，有阿罗汉善到善向，于此世他世自知作证："
        "我生已尽，梵行已立，所作已作，自知不受后有。」",
        "「何等正志？谓出要志、无恚志、不害志。"
        "何等正语？谓离妄语、两舌、恶口、绮语。"
        "何等正业？谓离杀、盗、淫。"
        "何等正命？谓如法求衣食卧具汤药，非不如法。"
        "何等正方便？谓欲精进、方便出离、勤竞堪能、常行不退。"
        "何等正念？谓念随顺，不妄不虚。"
        "何等正定？谓心住不乱，坚固摄持，寂止三昧，系念一心。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「有邪，也有正。仔细听，好好想，我为你们说。"
        f"什么是邪？就是{EIGHT_WRONG_MOD}。"
        f"什么是正？就是{EIGHT_RIGHT_MOD}。」",
        "「什么是正见？就是知道有布施、有教说、有斋戒，有善恶业及果报，有此世他世，"
        "有父母、有众生生，有阿罗汉善到善向，在此世他世自己证知："
        "我生已尽，梵行已立，所作已作，自己知道不受后有。」",
        "「什么是正志？就是出离之志、无瞋之志、不害之志。"
        "什么是正语？就是远离妄语、两舌、恶口、绮语。"
        "什么是正业？就是远离杀、盗、淫。"
        "什么是正命？就是如法求衣服饮食卧具汤药，而不是不如法。"
        "什么是正方便？就是有欲精进、方便出离、勤奋胜任、常行不退。"
        "什么是正念？就是念能随顺，不虚妄。"
        "什么是正定？就是心安住不乱，坚固摄持，寂止三昧，一心。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.21 Micchatta（邪／正道列名）；"
        "汉具各支释义，近 SN45.8／世间正见定型；据巴利厘「邪／正」总纲，释义从汉＋早期定型。"
        "正志＝sammāsaṅkappa；正方便＝sammāvāyāma。"
    ),
}

# --- SA 785 邪正二种（MN117）-----------------------------------------------
_WORLD_LIT = "世俗、有漏、有取，转向善趣"
_WORLD_MOD = "世俗、有漏、有取，转向善趣"
_NOBLE_LIT = "圣、出世间、无漏、不取，正尽苦，转向苦边"
_NOBLE_MOD = "圣、出世间、无漏、不取，正尽苦，转向苦边"
_NOBLE_THINK_LIT = "圣弟子于苦、集、灭、道如理思惟，无漏思惟相应"
_NOBLE_THINK_MOD = "圣弟子对苦、集、灭、道如理思惟，与无漏思惟相应"

SUTTAS["SA_785"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「如上说。差别者：正见有二种——"
        f"有正见{_WORLD_LIT}；有正见是{_NOBLE_LIT}。」",
        f"「世间正见者，谓知有施有说乃至阿罗汉不受后有，是名{_WORLD_LIT}之正见。"
        f"出世间正见者，谓{_NOBLE_THINK_LIT}，于法简择、分别、推求、觉知观察，"
        f"是名{_NOBLE_LIT}之正见。」",
        f"「正志亦二种。世间者，出要、无恚、不害之觉，是{_WORLD_LIT}。"
        f"出世间者，{_NOBLE_THINK_LIT}，心法分别、决意、立意，是{_NOBLE_LIT}。」",
        f"「正语、正业、正命亦各二种。世间者，离口四恶、身三恶、如法求活命；"
        f"出世间者，{_NOBLE_THINK_LIT}，于邪命及余恶行无漏远离、固守不犯。」",
        f"「正方便、正念、正定亦各二种。世间者，欲精进不休息、念随顺不虚、心住三昧；"
        f"出世间者，皆与{_NOBLE_THINK_LIT}，精进、正念、心住不乱。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「如上所说。不同的是：正见有两种——"
        f"有一种正见是{_WORLD_MOD}；有一种正见是{_NOBLE_MOD}。」",
        f"「世间正见，就是知道有布施、有教说，乃至知道有阿罗汉不受后有，这叫{_WORLD_MOD}的正见。"
        f"出世间正见，就是{_NOBLE_THINK_MOD}，对法简择、分别、推求、觉察，"
        f"这叫{_NOBLE_MOD}的正见。」",
        f"「正志也有两种。世间的，是出离、无瞋、不害的意向，属{_WORLD_MOD}。"
        f"出世间的，是{_NOBLE_THINK_MOD}，心法上分别、决意、确立，属{_NOBLE_MOD}。」",
        f"「正语、正业、正命也各有两种。世间的，是远离口四恶、身三恶、如法求活命；"
        f"出世间的，是{_NOBLE_THINK_MOD}，对邪命和其他恶行无漏地远离、守持不犯。」",
        f"「正方便、正念、正定也各有两种。世间的，是欲精进不休息、念随顺不虚、心住三昧；"
        f"出世间的，都与{_NOBLE_THINK_MOD}，精进、正念、心安住不乱。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling MN117 Mahācattārīsaka（世／出世间道支）；"
        "汉「如上说」承 784；压缩八支各二种之重复「苦苦思惟…」定型为统一无漏思惟句。"
        "不引入大乘术语。"
    ),
}

# --- SA 786 向邪（AN10.103）------------------------------------------------
SUTTAS["SA_786"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「心趣邪道，则违法、不乐法；"
        "心趣正道，则乐法、不违法。"
        f"邪者，{EIGHT_WRONG_LIT}；"
        f"正者，{EIGHT_RIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「心若走向邪道，就违背法、不喜欢法；"
        "心若走向正道，就喜欢法、不违背法。"
        f"所谓邪，就是{EIGHT_WRONG_MOD}；"
        f"所谓正，就是{EIGHT_RIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.103（邪→损减；正→增益之链）；"
        "汉略标向邪／向正与八支，不展开果报链（见 787／788）。"
    ),
}

# --- SA 787 向邪果报（AN1.306／AN10.104）-----------------------------------
SUTTAS["SA_787"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「向邪者违于法、不乐于法；向正者乐于法、不违于法。」",
        "「何等向邪？谓邪见人，身口业随其所见，若思、若欲、若愿、若为，皆随顺之，"
        "得不爱、不可意果。所以者何？见恶故。邪见起已，邪志乃至邪定随之。"
        "是名向邪者违于法、不乐于法。」",
        "「何等向正？谓正见人，身口业随其所见，若思、若欲、若愿、若为，皆随顺之，"
        "得可爱、可意果。所以者何？见正故。正见起已，正志乃至正定随之。"
        "是名向正者乐于法、不违于法。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「趋向邪的人违背法、不乐于法；趋向正的人乐于法、不违背法。」",
        "「怎样是向邪？就是邪见的人，身业口业都随他的见，思、欲、愿、造作也都随顺，"
        "得到不可爱、不可意的果报。为什么？因为见是恶的。邪见一生起，邪志乃至邪定就跟着来。"
        "这叫向邪者违背法、不乐于法。」",
        "「怎样是向正？就是正见的人，身业口业都随他的见，思、欲、愿、造作也都随顺，"
        "得到可爱、可意的果报。为什么？因为见是正的。正见一生起，正志乃至正定就跟着来。"
        "这叫向正者乐于法、不违背法。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN1.306–315／AN10.104（见为导首，业随见转）；"
        "汉「以见恶故／以见正故」句读据义校正；压缩八支枚举。"
    ),
}

# --- SA 788 向邪譬喻＋世出世间偈-------------------------------------------
SUTTAS["SA_788"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「向邪者违于法、不乐于法；向正者乐于法、不违于法。」",
        "「邪见人，身口意业随见而转，得不爱果。譬如苦种着地，溉以四味，所成皆苦——"
        "以种苦故。邪见起已，邪志乃至邪定随之。」",
        "「正见人，身口意业随见而转，得可爱果。譬如甘蔗、稻麦、葡萄着地，溉以四味，所成皆甜——"
        "以种甜故。正见起已，正志乃至正定随之。」",
        "「世间、出世间向邪向正，亦如上说。」",
        "「并说偈言：「鄙法不应近，放逸不应行；不应习邪见，增长于世间。"
        "假使有世间，正见增上者；虽复百千生，终不堕恶趣。」」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「趋向邪的人违背法、不乐于法；趋向正的人乐于法、不违背法。」",
        "「邪见的人，身口意业都随见而转，得到不可爱的果报。好比苦种埋进地里，用水火风地味浇灌，"
        "长出来的都苦——因为种子是苦的。邪见一生起，邪志乃至邪定就跟着来。」",
        "「正见的人，身口意业都随见而转，得到可爱的果报。好比甘蔗、稻麦、葡萄埋进地里，用四味浇灌，"
        "长出来的都甜——因为种子是甜的。正见一生起，正志乃至正定就跟着来。」",
        "「世间、出世间的向邪向正，也如上说。」",
        "「并说偈：「卑劣的法不该亲近，放逸不该去做；不该习邪见，让世间增长。"
        "若有世间人正见增上；哪怕百千生，终不堕恶趣。」」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN1.306 系＋种喻；"
        "「世间出世间亦如是说」peyyāla 摄记，不另展；偈从汉本。"
        "reconstruction=世间／出世间向邪向正 peyyāla 摄记。"
    ),
    "_recon": "世间／出世间向邪向正 peyyāla 摄记",
}

# --- SA 789 生闻正见二种（末段 peyyāla）------------------------------------
SUTTAS["SA_789"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有生闻婆罗门来诣佛所，稽首问讯已，退坐一面，白佛言："
        "「瞿昙！何等为正见？」",
        f"佛告婆罗门：「正见有二种。有正见{_WORLD_LIT}；"
        f"有正见是{_NOBLE_LIT}。」",
        f"「世间正见者，谓知有施、有说、有斋，乃至自知不受后有，是{_WORLD_LIT}。"
        f"出世间正见者，谓{_NOBLE_THINK_LIT}，于法简择、分别、求觉、巧慧观察，"
        f"是{_NOBLE_LIT}。」",
        "生闻婆罗门闻已，欢喜随喜，从座起去。",
        "「如正见，正志、正语、正业、正命、正方便、正念、正定——一一经如上说。」",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有生闻婆罗门来到佛所，叩头问讯后坐在一边，对佛说："
        "「瞿昙！什么是正见？」",
        f"佛告诉婆罗门：「正见有两种。有一种正见是{_WORLD_MOD}；"
        f"有一种正见是{_NOBLE_MOD}。」",
        f"「世间正见，就是知道有布施、有教说、有斋戒，乃至自己知道不受后有，这属{_WORLD_MOD}。"
        f"出世间正见，就是{_NOBLE_THINK_MOD}，对法简择、分别、求觉、善巧观察，"
        f"这属{_NOBLE_MOD}。」",
        "生闻婆罗门听完，欢喜随喜，从座位起身离去。",
        "「就像正见这样，正志、正语、正业、正命、正方便、正念、正定——每一经都如上说。」",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：承 MN117／SA785 二种正见；"
        "问者作生闻婆罗门。余七支「如上说」peyyāla。"
        "reconstruction=正志乃至正定 peyyāla。"
    ),
    "_recon": "正志乃至正定二种定义 peyyāla",
}

# --- SA 790 邪正（趣／道）--------------------------------------------------
SUTTAS["SA_790"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有邪及邪道，有正及正道。谛听，善思，当为汝说。"
        "何等为邪？谓地狱、畜生、饿鬼。"
        f"何等邪道？谓{EIGHT_WRONG_LIT}。"
        "何等为正？谓人、天、涅槃。"
        f"何等正道？谓{EIGHT_RIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉诸比丘：「有邪和邪道，也有正和正道。仔细听，好好想，我为你们说。"
        "什么是邪？就是地狱、畜生、饿鬼。"
        f"什么是邪道？就是{EIGHT_WRONG_MOD}。"
        "什么是正？就是人、天、涅槃。"
        f"什么是正道？就是{EIGHT_RIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium："
        "以三恶趣为邪果、人天涅槃为正果，八邪／八正为道；早期道果对举，无大乘义。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_771": "high",
    "SA_772": "medium",
    "SA_773": "medium",
    "SA_774": "medium",
    "SA_775": "high",
    "SA_776": "high",
    "SA_777": "high",
    "SA_778": "high",
    "SA_779": "high",
    "SA_780": "high",
    "SA_781": "medium",
    "SA_782": "medium",
    "SA_783": "high",
    "SA_784": "high",
    "SA_785": "high",
    "SA_786": "high",
    "SA_787": "high",
    "SA_788": "high",
    "SA_789": "medium",
    "SA_790": "medium",
}

RECONSTRUCTED: dict[str, str] = {}
for _rid, _s in SUTTAS.items():
    if "_recon" in _s:
        RECONSTRUCTED[_rid] = _s["_recon"]

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

GOLD: dict[str, dict[str, str]] = {}
for _rid, _s in SUTTAS.items():
    _lit_paras: list[str] = list(_s["lit"])
    _mod_paras: list[str] = list(_s["mod"])
    if len(_lit_paras) != len(_mod_paras):
        raise AssertionError(
            f"{_rid} paragraph mismatch: lit={len(_lit_paras)} mod={len(_mod_paras)}"
        )
    GOLD[_rid] = {
        "kumarajiva_style_text": "\n".join(_lit_paras),
        "modern_psychology_text": "\n".join(_mod_paras),
        "notes": _s["notes"],
    }


def main() -> None:
    assert set(GOLD) == {f"SA_{i}" for i in range(771, 791)}, (
        "GOLD must cover SA_771–SA_790 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    assert not any(f"SA_{i}" in GOLD for i in range(751, 771))
    assert not any(f"SA_{i}" in GOLD for i in range(791, 811))

    aligned = ROOT / "data" / "aligned" / "raw_aligned_data.json"
    out = ROOT / "data" / "translated" / "final_translated_data.json"
    gold_dir = ROOT / "data" / "golden"
    gold_dir.mkdir(parents=True, exist_ok=True)

    if out.exists():
        by_id = {r["id"]: r for r in json.loads(out.read_text(encoding="utf-8"))}
        for r in json.loads(aligned.read_text(encoding="utf-8")):
            by_id.setdefault(r["id"], r)
        records = sorted(by_id.values(), key=lambda x: int(x["id"].split("_")[1]))
    else:
        records = json.loads(aligned.read_text(encoding="utf-8"))

    _goldish = {"gold", "gold_reconstructed"}
    by_lookup = {r["id"]: r for r in records}
    boundary_id = "SA_770"
    if by_lookup.get("SA_770", {}).get("review_status") not in _goldish:
        for i in range(769, 0, -1):
            rid = f"SA_{i}"
            if by_lookup.get(rid, {}).get("review_status") in _goldish:
                boundary_id = rid
                break

    boundary_before = None
    for rec in records:
        if rec["id"] == boundary_id:
            boundary_before = json.dumps(
                {
                    "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                    "modern_psychology_text": rec.get("modern_psychology_text"),
                    "notes": rec.get("notes"),
                    "review_status": rec.get("review_status"),
                    "confidence": rec.get("confidence"),
                },
                ensure_ascii=False,
            )
            break

    # Snapshot parallel batches: SA_751–770 and SA_791–810
    guard_ids = {f"SA_{i}" for i in range(751, 771)} | {f"SA_{i}" for i in range(791, 811)}
    mid_before = {
        rec["id"]: json.dumps(
            {
                "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                "modern_psychology_text": rec.get("modern_psychology_text"),
                "notes": rec.get("notes"),
                "review_status": rec.get("review_status"),
                "confidence": rec.get("confidence"),
            },
            ensure_ascii=False,
        )
        for rec in records
        if rec["id"] in guard_ids
    }

    report = []
    merged = []
    for rec in records:
        rid = rec["id"]
        item = dict(rec)
        if rid in GOLD:
            g = GOLD[rid]
            lit = g["kumarajiva_style_text"]
            mod = g["modern_psychology_text"]
            item["kumarajiva_style_text"] = lit
            item["modern_psychology_text"] = mod
            item["notes"] = g["notes"]
            item["translator"] = "cursor-agent"

            prior = rec.get("prior_review_status") or rec.get("review_status")
            item["prior_review_status"] = "needs_revision" if prior in OWN_STATUSES else prior

            item["confidence"] = CONFIDENCE[rid]
            if rid in RECONSTRUCTED:
                item["review_status"] = "gold_reconstructed"
                item["reconstruction_basis"] = RECONSTRUCTED[rid]
            else:
                item["review_status"] = "gold"
                item.pop("reconstruction_basis", None)

            v = validate_restyle(item.get("chinese_text") or "", lit, mod)
            item["validation"] = v
            item["forbidden_hits"] = v.get("forbidden_hits") or []

            sim = round(similarity_to_source(item.get("chinese_text") or "", lit), 3)
            sim_mod = round(similarity_to_source(item.get("chinese_text") or "", mod), 3)
            item["similarity_to_source"] = sim

            lit_paras = lit.split("\n")
            mod_paras = mod.split("\n")
            para_ok = len(lit_paras) == len(mod_paras)
            item["paragraph_parallel"] = para_ok

            if v["status"] == "fail" and rid not in RECONSTRUCTED:
                item["review_status"] = "needs_doctrine_check"
            gate_status, gate_reasons = assess_gold(
                sim, len(lit.replace("\n", "")), round(sim - sim_mod, 3)
            )
            if gate_status and rid not in RECONSTRUCTED:
                item["review_status"] = gate_status
                item["quality_gate_reasons"] = gate_reasons

            report.append(
                {
                    "id": rid,
                    **v,
                    "sim": sim,
                    "paragraphs": len(lit_paras),
                    "paragraph_parallel": para_ok,
                    "confidence": item["confidence"],
                    "review_status": item["review_status"],
                    "gate_reasons": gate_reasons if gate_status else [],
                }
            )
            (gold_dir / f"{rid.lower()}.json").write_text(
                json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        merged.append(item)

    for rec in merged:
        if rec["id"] == boundary_id and boundary_before is not None:
            boundary_after = json.dumps(
                {
                    "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                    "modern_psychology_text": rec.get("modern_psychology_text"),
                    "notes": rec.get("notes"),
                    "review_status": rec.get("review_status"),
                    "confidence": rec.get("confidence"),
                },
                ensure_ascii=False,
            )
            assert boundary_before == boundary_after, f"{boundary_id} must remain untouched"
            break

    for rid, before in mid_before.items():
        for rec in merged:
            if rec["id"] == rid:
                after = json.dumps(
                    {
                        "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                        "modern_psychology_text": rec.get("modern_psychology_text"),
                        "notes": rec.get("notes"),
                        "review_status": rec.get("review_status"),
                        "confidence": rec.get("confidence"),
                    },
                    ensure_ascii=False,
                )
                assert before == after, f"{rid} (parallel batch) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa771-790.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fails = [r for r in report if r["status"] == "fail"]
    warns = [r for r in report if r["status"] == "warn"]
    oks = [r for r in report if r["status"] == "ok"]
    forbidden = [r for r in report if r.get("forbidden_hits")]
    needs_restyle = [r for r in report if r["review_status"] == "needs_restyle"]
    para_bad = [r for r in report if not r["paragraph_parallel"]]
    recon = [r for r in report if r["id"] in RECONSTRUCTED]
    max_r = max(report, key=lambda r: r["sim"])
    conf_split = {
        c: sum(1 for r in report if r["confidence"] == c) for c in ("high", "medium", "low")
    }

    by_merged = {r["id"]: r for r in merged}
    goldish = {"gold", "gold_reconstructed"}
    continuous_771_790 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(771, 791)
    )
    untouched_751_770 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") not in goldish
        or f"SA_{i}" not in GOLD
        for i in range(751, 771)
    )
    # stronger: none of 751-770 were in this merge
    untouched_751_770 = all(f"SA_{i}" not in GOLD for i in range(751, 771))
    untouched_791_810 = all(f"SA_{i}" not in GOLD for i in range(791, 811))

    ban_terms = [
        "厌故不乐",
        "如来藏",
        "佛性",
        "常乐我净",
        "真心",
        "妄心",
        "本来面目",
        "即心即佛",
        "如如",
        "发菩提心",
    ]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_771–SA_790 only)")
    print(f"validation: ok={len(oks)} warn={len(warns)} fail={len(fails)}")
    print(f"forbidden_hits={len(forbidden)} ban_term_hits={ban_hits}")
    print(
        f"needs_restyle (assess_gold): {len(needs_restyle)}  "
        f"max_sim={max_r['sim']} ({max_r['id']})  "
        f"mean_sim={round(sum(r['sim'] for r in report) / len(report), 3)}"
    )
    print(f"paragraph_parallel_violations={len(para_bad)}")
    print(f"gold={len(report) - len(recon)} gold_reconstructed={len(recon)}")
    print(f"gold_reconstructed_ids={[r['id'] for r in recon]}")
    print(f"confidence: {conf_split}")
    print(f"continuous_gold_SA_771–790={continuous_771_790}")
    print(f"SA_751–770_untouched={untouched_751_770}")
    print(f"SA_791–810_untouched={untouched_791_810}")
    print(f"boundary={boundary_id}_untouched=True")
    for r in report:
        print(
            r["id"],
            r["status"],
            f"sim={r['sim']}",
            f"paras={r['paragraphs']}",
            r["confidence"],
            r["review_status"],
            r.get("gate_reasons") or "",
            r.get("issues"),
            r.get("warnings"),
        )


if __name__ == "__main__":
    main()
