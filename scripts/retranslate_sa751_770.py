#!/usr/bin/env python3
"""Retranslate SA 751–770（圣道分相应 卷二十九末–三十）→ merge.

本批二十经：起 SN45.24；迦摩 SN45.30；阿黎吒 SN45.7；
舍利弗／比丘／畏／受（754–757）；三法 AN3.62；学（三受）SN45.29；
正士 AN10.76；漏尽（学／无学）SN45.13；八正道／修／清净 762–766；
聚 SN47.45；半 SN45.2；婆罗门 SN45.4；邪 SN45.21。

信：有 SN／AN 平行者据巴利／Sujato 厘义；无专经 → medium。
    peyyāla／交叉指示补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_751–770；不触碰 SA_731–750、SA_771+（并行批次）；
      断言 SA_750 不变（若尚未 gold 则断言 SA_730）。
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

OPEN_VAL_LIT = "如是我闻：一时，佛住王舍城山谷精舍。"
OPEN_VAL_MOD = "我是这样听说的：有一次，佛住在王舍城山谷精舍。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_KAMA_LIT = "佛说此经已，迦摩比丘闻佛所说，欢喜奉行。"
CLOSE_KAMA_MOD = "佛说完这部经，迦摩比丘听佛所说，欢喜奉行。"

CLOSE_AN_LIT = "佛说此经已，尊者阿难闻佛所说，欢喜奉行。"
CLOSE_AN_MOD = "佛说完这部经，阿难尊者听佛所说，欢喜奉行。"

EIGHT_LIT = "正见、正志、正语、正业、正命、正方便、正念、正定"
EIGHT_MOD = "正见、正志、正语、正业、正命、正方便、正念、正定"

WRONG_LIT = "邪见、邪志、邪语、邪业、邪命、邪方便、邪念、邪定"
WRONG_MOD = "邪见、邪志、邪语、邪业、邪命、邪方便、邪念、邪定"

SEVEN_PATH_LIT = "正见、正志、正语、正业、正命、正方便、正念"
SEVEN_PATH_MOD = "正见、正志、正语、正业、正命、正方便、正念"

NISSAYA_LIT = "依远离、依离欲、依灭、向于舍"
NISSAYA_MOD = "依于远离、依于离欲、依于灭、而趋向舍"

FIVE_NIV_LIT = "贪欲盖、瞋恚盖、睡眠盖、掉悔盖、疑盖"
FIVE_NIV_MOD = "贪欲盖、瞋恚盖、昏沉睡眠盖、掉举后悔盖、疑盖"

PATH_ASK_LIT = (
    "有道有迹，修习多修习，能断此法不？"
)
PATH_ANS_LIT = f"有。谓八圣道——{EIGHT_LIT}。"
PATH_ASK_MOD = "有没有道路、有没有途径，多修习就能断这些法？"
PATH_ANS_MOD = f"有。就是八圣道——{EIGHT_MOD}。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 751 起（SN45.24）------------------------------------------------------
SUTTAS["SA_751"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「在家、出家而行邪道，我所不赞。所以者何？行邪道者，"
        "于正法、于善法不得成办。何等邪道？谓"
        f"{WRONG_LIT}。」",
        "「在家、出家而行正道，我所称赞。所以者何？行正道者，"
        "于正法、于善法能得成办。何等正道？谓"
        f"{EIGHT_LIT}。」",
        "尔时世尊说偈言：\n"
        "「在家与出家，若行于邪道，\n"
        "　终不乐正法，无上善法味；\n"
        "　在家与出家，若行于正道，\n"
        "　常能心乐法，无上正法味。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「在家、出家而行邪道，我不赞叹。为什么？行邪道的人，"
        "在正法、在善法上不能成办。什么是邪道？就是"
        f"{WRONG_MOD}。」",
        "「在家、出家而行正道，我称赞。为什么？行正道的人，"
        "在正法、在善法上能够成办。什么是正道？就是"
        f"{EIGHT_MOD}。」",
        "那时世尊说偈：\n"
        "「在家与出家，若行于邪道，\n"
        "　终不乐正法，无上善法味；\n"
        "　在家与出家，若行于正道，\n"
        "　常能心乐法，无上正法味。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.24 Dutiyapaṭipadā。"
        "据 SN 校正：「不乐正法」→「于正法／善法不得成办」（nārādhako…ñāyaṁ dhammaṁ kusalaṁ）；"
        "「邪事／正事」→「邪道／正道」（micchā／sammā-paṭipadā）。偈依汉本保留。"
    ),
}

# --- SA 752 迦摩（SN45.30；汉名迦摩／巴利 Uttiya）------------------------------
SUTTAS["SA_752"] = {
    "lit": [
        OPEN_JET_LIT,
        "时，迦摩比丘诣佛所，稽首礼足，退坐一面，白佛言：「世尊！所谓欲者，云何为欲？」",
        "佛告迦摩：「欲者，谓五欲功德：眼识所取色，可爱、可意、可念，长养欲乐；"
        "耳、鼻、舌、身所取声、香、味、触，亦复如是——是名五欲功德。"
        "然色等非即是欲；于彼起贪著者，乃名为欲。」",
        "尔时世尊说偈言：\n"
        "「世间杂众色，彼非即爱欲；\n"
        "　贪著觉想生，是则士夫欲。\n"
        "　众色常住世，行者断心欲。」",
        "迦摩白佛：「宁有道有迹，能断此爱欲不？」"
        f"佛言：「有。谓八正道——{EIGHT_LIT}。」",
        CLOSE_KAMA_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，迦摩比丘来到佛所，叩头礼足，坐在一边，对佛说：「世尊！所谓欲，到底是什么？」",
        "佛告诉迦摩：「欲，是指五欲功德：眼所识的色，可爱、合意、可念，滋长欲乐；"
        "耳、鼻、舌、身所取的声、香、味、触，也是这样——这叫做五欲功德。"
        "然而色等本身并不是欲；对它们生起贪著，才叫做欲。」",
        "那时世尊说偈：\n"
        "「世间杂众色，彼非即爱欲；\n"
        "　贪著觉想生，是则士夫欲。\n"
        "　众色常住世，行者断心欲。」",
        "迦摩对佛说：「可有道路、可有途径，能断这种爱欲吗？」"
        f"佛说：「有。就是八正道——{EIGHT_MOD}。」",
        CLOSE_KAMA_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.30 Uttiya（汉作迦摩）。"
        "义据 SN：五欲功德本身非「欲」，贪著乃欲；修八支道以断。"
        "汉偈「彼非为爱欲」与长行「然彼非欲…贪著者是名欲」同旨，保留。"
    ),
}

# --- SA 753 阿黎吒（SN45.7；甘露＝不死／漏尽界）--------------------------------
SUTTAS["SA_753"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有比丘名阿梨瑟吒，诣佛所，稽首礼足，退坐一面，白佛言："
        "「世尊！所谓甘露者，云何名甘露？」",
        "佛告阿梨瑟吒：「甘露者，是涅槃界之名；我为漏尽者说此名——"
        "谓贪、瞋、痴永尽。」",
        "阿梨瑟吒复问：「有道有迹，修习多修习，得此甘露法不？」"
        f"佛言：「有。谓八圣道——{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有比丘名叫阿梨瑟吒，来到佛所，叩头礼足，坐在一边，对佛说："
        "「世尊！所谓甘露，为什么叫甘露？」",
        "佛告诉阿梨瑟吒：「甘露，是涅槃界的名称；我为漏尽的人说这个名字——"
        "就是贪、瞋、痴永远尽灭。」",
        "阿梨瑟吒又问：「有没有道路、有没有途径，多修习就能得到这甘露法？」"
        f"佛说：「有。就是八圣道——{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.7（amata／rāga-dosa-moha-vinaya＝nibbānadhātu／āsavānaṃ khaya）。"
        "汉「界名说，然我为有漏尽者现说此名」据 SN 点明：甘露＝涅槃界／漏尽之称。"
    ),
}

# --- SA 754 舍利弗（贤圣等三昧根本众具；无专平行）------------------------------
SUTTAS["SA_754"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者舍利弗诣佛所，稽首礼足，退坐一面，白佛言："
        "「世尊！所谓贤圣等三昧根本众具，云何？」",
        "佛告舍利弗：「七支正道，是贤圣等三昧之根本、众具。"
        f"何等七？{SEVEN_PATH_LIT}。"
        "于此七支为基业已，得心一境，是名贤圣等三昧根本众具。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "舍利弗尊者来到佛所，叩头礼足，坐在一边，对佛说："
        "「世尊！所谓贤圣等持的三昧，它的根本与众具是什么？」",
        "佛告诉舍利弗：「七支正道，就是贤圣等持三昧的根本与众具。"
        f"哪七支？{SEVEN_PATH_MOD}。"
        "以这七支为基业之后，心得专一，就叫做贤圣等持三昧的根本众具。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：同 MN117／SN 道支系「正定以余七支为资粮」定型；"
        "汉「得一其心」＝心一境性。"
    ),
}

# --- SA 755 比丘（peyyāla：佛问比丘，同 752 欲义）------------------------------
SUTTAS["SA_755"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「欲者，谓五欲功德；然色等非欲，于彼贪著者是名为欲。"
        f"有道能断，谓八正道——{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「欲，是指五欲功德；然而色等本身不是欲，对它们贪著才叫做欲。"
        f"有道能断，就是八正道——{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "底本「如上三经。如是佛问诸比丘三经亦如是说」；"
        "题名「比丘」，据 SA_752／SN45.30 纲，作佛告比丘之欲义略说。"
    ),
}

# --- SA 756 畏（peyyāla：母子畏纲，详扩见 SA_758／AN3.62）--------------------
SUTTAS["SA_756"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「凡夫所谓无母子畏——兵乱、大火、洪水——实是有母子畏，或可重逢。"
        "我所说真无母子畏，谓老、病、死：母子不能代受。"
        f"断此诸畏，有道有迹，谓八圣道——{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「凡夫所说的无母子畏——兵乱、大火、洪水——其实是有母子畏，或许还能重逢。"
        "我所说真正的无母子畏，是老、病、死：母子不能互相代受。"
        f"要断这些畏，有道路、有途径，就是八圣道——{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：gold_reconstructed——"
        "底本仅「如上三经…」peyyāla；题名「畏」，据 SA_758／AN3.62 母子畏纲略说。"
    ),
}

# --- SA 757 受（peyyāla：三受，详扩见 SA_759／SN45.29）------------------------
SUTTAS["SA_757"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有三受——乐受、苦受、不苦不乐受，皆无常、有为、心所缘生。"
        f"欲断此三受，当修八圣道——{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「有三种受——乐受、苦受、不苦不乐受，都是无常、有为、由心所缘而生。"
        f"想断这三种受，应当修八圣道——{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：gold_reconstructed——"
        "底本仅「如上三经…」peyyāla；题名「受」，据 SA_759／SN45.29 三受＋八支道纲略说。"
    ),
}

# --- SA 758 三法（AN3.62 母子畏）----------------------------------------------
SUTTAS["SA_758"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「无母子畏、有母子畏——愚痴无闻凡夫说之，而不能如实了知。」",
        "「凡夫所谓三种无母子畏：兵乱起而母子相失；大火焚城邑而母子相失；"
        "山洪漂聚落而母子相失。然此实是有母子畏——或时犹得相见；"
        "凡夫误名为无母子畏。」",
        "「我自觉成等正觉所记三种真无母子畏：老——母不能代子不老，子不能代母；"
        "病——亦复如是；死——亦复如是。此则母子不能相代。」",
        "诸比丘白佛：「有道有迹，修习多修习，断前有母子畏、后无母子畏不？」"
        f"佛言：「有。谓八圣道——{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「无母子畏、有母子畏——愚痴无闻的凡夫会说，却不能如实了知。」",
        "「凡夫所说的三种无母子畏：兵乱起来母子失散；大火烧城邑母子失散；"
        "山洪冲聚落母子失散。其实这些是有母子畏——有时还能再见面；"
        "凡夫却误叫做无母子畏。」",
        "「我自己觉悟成等正觉所记的三种真正无母子畏：老——母亲不能代替孩子不老，孩子也不能代替母亲；"
        "病——也是这样；死——也是这样。这才是母子不能互相代替的。」",
        "比丘们对佛说：「有没有道路、有没有途径，多修习就能断前面的有母子畏、后面的无母子畏？」"
        f"佛说：「有。就是八圣道——{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN3.62 Bhaya。"
        "压缩汉本兵／火／水与老病死之对称复述；据 AN 点明："
        "凡夫所称「分离畏」实可重逢（有母子），真不可代者唯老病死。"
    ),
}

# --- SA 759 学（汉题；内容三受＝SN45.29 Vedanā）-------------------------------
SUTTAS["SA_759"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「受有三种，皆无常、有为、由心缘而生起——"
        "乐、苦、不苦不乐。」",
        "比丘问：「修何道迹，能断此三？」"
        f"佛言：「修八圣道——{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「受有三种，都是无常、有为、由心的所缘而生起——"
        "乐、苦、不苦不乐。」",
        "比丘问：「修什么道路，能断这三种？」"
        f"佛说：「修八圣道——{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.29 Vedanā（汉题「学」，正文为三受）。"
        "SN 作「为遍知三受当修八支道」；汉问「断」——义相容，从汉问答形。"
    ),
}

# --- SA 760 正士（AN10.76 老病死缘如来出世；略本）-----------------------------
SUTTAS["SA_760"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「世有三法，不可喜、不可爱、不可念——老、病、死。"
        "若无此三，则如来、应、等正觉不出世间，世间亦不知有如来教诫、教授。"
        "以有此三故，如来出于世间，说教诫、教授。」",
        "诸比丘白佛：「有道有迹，断此三法不？」"
        f"佛言：「有。谓八圣道——{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「世上有三法，不可喜、不可爱、不可念——老、病、死。"
        "如果没有这三样，如来、应、等正觉不会出现在世间，世间也不知道有如来的教诫、教授。"
        "正因为有这三样，如来才出现在世间，说教诫、教授。」",
        "比丘们对佛说：「有没有道路、有没有途径，能断这三法？」"
        f"佛说：「有。就是八圣道——{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.76（SA_346 为同相应之广本）。"
        "本经唯取「老病死→如来出世」＋八支道能断；不展 AN／SA_346 之多层三法链。"
    ),
}

# --- SA 761 漏尽（汉题；内容学／无学＝SN45.13 Sekkha）-------------------------
SUTTAS["SA_761"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「我当说学与无学。谛听，善思。"
        f"云何为学？谓学人成就正见，乃至正定——{EIGHT_LIT}，是名为学。"
        "云何无学？谓无学人成就正见，乃至正定，是名无学。」",
        "「如说学、无学，说正士、说大士，亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「我要说学与无学。仔细听，好好思惟。"
        f"什么是学？就是学人成就正见，乃至正定——{EIGHT_MOD}，这叫做学。"
        "什么是无学？就是无学人成就正见，乃至正定，这叫做无学。」",
        "「像这样说学、无学，说正士、说大士，也是一样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.13 Sekkha（汉题「漏尽」，正文为学／无学）。"
        "peyyāla「正士、大士」依汉末句保留。"
    ),
}

# --- SA 762 八正道分（圣漏尽＝无学八支）--------------------------------------
SUTTAS["SA_762"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「我当说圣漏尽。云何圣漏尽？"
        f"谓无学正见成就，乃至无学正定成就——{EIGHT_LIT}，是名圣漏尽。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「我要说圣漏尽。什么是圣漏尽？"
        f"就是无学正见成就，乃至无学正定成就——{EIGHT_MOD}，这叫做圣漏尽。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：以无学八支成就释「圣漏尽」，"
        "与 SA_761 无学段相续；参 SN 道相应 asekha 定型。"
    ),
}

# --- SA 763 修（列八圣道）-----------------------------------------------------
SUTTAS["SA_763"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当说圣道八支。何等八？"
        "正见、正志、正语、正业、正命、正方便、正念、正定——"
        "是名八圣道。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「要说圣道的八支。哪八支？"
        "正见、正志、正语、正业、正命、正方便、正念、正定——"
        "这叫做八圣道。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：八支道名表；早期定型，无争议。"
    ),
}

# --- SA 764 修（依远离等修八支；≈SN45.15 系＋nissaya）------------------------
SUTTAS["SA_764"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「云何修习八圣道？谛听。"
        f"比丘修习正见，{NISSAYA_LIT}；"
        "正志、正语、正业、正命、正方便、正念、正定，"
        f"皆{NISSAYA_LIT}——是名修八圣道。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「怎样修习八圣道？仔细听。"
        f"比丘修习正见，{NISSAYA_MOD}；"
        "正志、正语、正业、正命、正方便、正念、正定，"
        f"都{NISSAYA_MOD}——这叫做修八圣道。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SC 列 SN45.15（生起）；"
        "汉正文为 viveka-nissita 修习式，据道相应常法保留；"
        "「依無欲」作「依离欲」。"
    ),
}

# --- SA 765 清净（过去／未来修；peyyāla）--------------------------------------
SUTTAS["SA_765"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「过去诸比丘已修八圣道，未来当修八圣道，"
        f"皆修正见乃至正定，{NISSAYA_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「过去的比丘已经修八圣道，未来也应当修八圣道，"
        f"都是修正见乃至正定，{NISSAYA_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉仅「过去已修…未来当修…乃至」；据 SA_764 nissaya 修习式补满。"
    ),
}

# --- SA 766 清净（SN45.16／17）------------------------------------------------
SUTTAS["SA_766"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有八法清净鲜白、无诸过患、离诸烦恼——"
        f"{EIGHT_LIT}。"
        "此八法未起者，非如来、应、等正觉出现于世，则不得生起；"
        "如来出现，乃得生起。」",
        "「如说除佛，说除善逝，亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「有八法清净鲜白、没有过患、离开烦恼——"
        f"{EIGHT_MOD}。"
        "这八法若还未生起，若非如来、应、等正觉出现在世间，就不能生起；"
        "如来出现，才能生起。」",
        "「像说除了佛，说除了善逝，也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.16／45.17 Parisuddha。"
        "据 SN 校正汉「未起不起，唯除佛所调伏／未起能起」："
        "清净八支未起者，唯因如来（及善逝）出现而得生起。"
    ),
}

# --- SA 767 聚（不善聚五盖／善聚八圣道；≈SN47.45 系）--------------------------
SUTTAS["SA_767"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「说不善聚者，谓五盖，是为正说。"
        f"所以者何？纯一不善聚，所谓五盖——{FIVE_NIV_LIT}。」",
        "「说善法聚者，谓八圣道，是为正说。"
        f"所以者何？纯一满净善聚，谓八圣道——{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「说不善聚，就是指五盖，这才是正说。"
        f"为什么？纯粹的不善聚，就是五盖——{FIVE_NIV_MOD}。」",
        "「说善法聚，就是指八圣道，这才是正说。"
        f"为什么？纯粹圆满清净的善聚，就是八圣道——{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：不善聚≈AN5.52／SN47.5（五盖）；"
        "善聚 SN47.45 作四念处，本经在圣道分以八圣道为善聚（与 SA_725 觉支本、SA_611 念处本对观）。"
    ),
}

# --- SA 768 半（SN45.2；圣道分以八支说明）------------------------------------
SUTTAS["SA_768"] = {
    "lit": [
        OPEN_VAL_LIT,
        "时，尊者阿难独一静处，作是念：「半梵行者，谓善知识、善伴党、善随从。」"
        "念已，往白世尊。",
        "佛告阿难：「莫作是言。纯一满净、具足梵行者，即是善知识——"
        "非半，乃全体也。」",
        "「所以者何？我为善知识故，令诸众生修习正见，"
        f"{NISSAYA_LIT}；乃至修正定，{NISSAYA_LIT}。」",
        CLOSE_AN_LIT,
    ],
    "mod": [
        OPEN_VAL_MOD,
        "那时，阿难尊者独自在静处，心想：「梵行的一半，就是善知识、善同伴、善随从。」"
        "想过之后，前去禀告世尊。",
        "佛告诉阿难：「不要这样说。纯粹圆满清净、具足的梵行，就是善知识——"
        "不是一半，而是全体。」",
        "「为什么？因为我是善知识，使众生修习正见，"
        f"{NISSAYA_MOD}；乃至修正定，{NISSAYA_MOD}。」",
        CLOSE_AN_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.2 Upaḍḍha。"
        f"与 SA_726（觉支相应）同经异传：本经以八支道＋{NISSAYA_LIT} 说明。"
        "据 SN 校正：「半」→「全体」。汉「乃至」补为正定。"
    ),
}

# --- SA 769 婆罗门（SN45.4 梵乘）----------------------------------------------
SUTTAS["SA_769"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者阿难晨朝著衣持钵，入舍卫城乞食。"
        "见生闻婆罗门乘白马车，眷属、众具一切皆白；众人唱言：「善乘！善乘！谓婆罗门乘。」"
        "乞食已，还白佛，问：「于正法律，此是世人乘耶？为婆罗门乘耶？」",
        "佛告阿难：「是世人乘，非我法律中婆罗门乘。"
        "我正法律中所谓法乘、天乘、梵乘、大乘——能调伏烦恼军者，即八正道："
        f"{EIGHT_LIT}。」",
        "尔时世尊说偈言：\n"
        "「信慧为法轭，惭愧为长縻，\n"
        "　正念善守护，是为善御者；\n"
        "　舍与定为辕，慧进以为轮，\n"
        "　无著忍为铠，安隐如法行；\n"
        "　直进不退转，至于无忧处，\n"
        "　智士乘此车，摧伏无智怨。」",
        CLOSE_AN_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "阿难尊者早晨穿衣持钵，进入舍卫城乞食。"
        "看见生闻婆罗门乘着白马车，眷属、用具一片全白；众人喊：「好车！好车！这是婆罗门乘。」"
        "乞食回来禀告佛，问：「在正法律里，这算世人的车，还是婆罗门乘？」",
        "佛告诉阿难：「这是世人的车，不是我法律中的婆罗门乘。"
        "我正法律中所谓法乘、天乘、梵乘、大乘——能调伏烦恼军的，就是八正道："
        f"{EIGHT_MOD}。」",
        "那时世尊说偈：\n"
        "「信慧为法轭，惭愧为长縻，\n"
        "　正念善守护，是为善御者；\n"
        "　舍与定为辕，慧进以为轮，\n"
        "　无著忍为铠，安隐如法行；\n"
        "　直进不退转，至于无忧处，\n"
        "　智士乘此车，摧伏无智怨。」",
        CLOSE_AN_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.4 Jāṇussoṇi。"
        "「大乘／梵乘／法乘」＝八支道之异名（brahmayāna／dhammayāna），"
        "非后期大乘宗义。偈据 SN 战车喻略译，删汉冗复。"
    ),
}

# --- SA 770 邪（SN45.21；汉广「应离／应修」式）--------------------------------
SUTTAS["SA_770"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「应离、应断邪见。若邪见不可断，我终不说应离断；"
        "以可断故，说当离断。若不离者，则作非义、不饶益、苦。"
        f"如邪见，{WRONG_LIT}亦如是说。」",
        "「离邪见已，当修正见。若不得修，我终不说当修；"
        "以可得修故，说当修正见——为义、饶益、安乐故。"
        f"如正见，{EIGHT_LIT}亦如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「应当离开、断除邪见。如果邪见不能断，我终不会说应当离断；"
        "正因为可以断，才说应当离断。如果不离开，就会造成无益、无利、苦。"
        f"像邪见这样，{WRONG_MOD}也是这样说。」",
        "「离开邪见之后，应当修正见。如果不能修，我终不会说应当修；"
        "正因为可以修，才说应当修正见——为了有益、有利、安乐。"
        f"像正见这样，{EIGHT_MOD}也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.21 Micchatta（邪性／正性＝八邪／八正）。"
        "汉本「可断故说应离／可得修故说应修」广式保留；SN 唯列邪正二聚，义同。"
    ),
}

# ---------------------------------------------------------------------------
# Confidence / reconstruction
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_751": "high",
    "SA_752": "high",
    "SA_753": "high",
    "SA_754": "medium",
    "SA_755": "medium",
    "SA_756": "medium",
    "SA_757": "medium",
    "SA_758": "high",
    "SA_759": "high",
    "SA_760": "high",
    "SA_761": "high",
    "SA_762": "medium",
    "SA_763": "medium",
    "SA_764": "high",
    "SA_765": "medium",
    "SA_766": "high",
    "SA_767": "high",
    "SA_768": "high",
    "SA_769": "high",
    "SA_770": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_755": "peyyāla「如上三经／佛问比丘」→ SA_752／SN45.30 欲义略说",
    "SA_756": "peyyāla「如上三经」＋题「畏」→ SA_758／AN3.62 母子畏纲",
    "SA_757": "peyyāla「如上三经」＋题「受」→ SA_759／SN45.29 三受纲",
    "SA_765": "「过去已修／未来当修…乃至」→ SA_764 nissaya 修习式",
    "SA_768": "「乃至」→ 八支全＋依远离等（SN45.2）",
}

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
    assert set(GOLD) == {f"SA_{i}" for i in range(751, 771)}, (
        "GOLD must cover SA_751–SA_770 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    # Parallel batches own 731–750 and 771+
    assert not any(f"SA_{i}" in GOLD for i in range(731, 751))
    assert not any(f"SA_{i}" in GOLD for i in range(771, 791))

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

    # Boundary: SA_750 if gold, else SA_730
    _goldish = {"gold", "gold_reconstructed"}
    boundary_id = "SA_750"
    for rec in records:
        if rec["id"] == "SA_750" and rec.get("review_status") not in _goldish:
            boundary_id = "SA_730"
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

    # Snapshot parallel batches to assert untouched
    parallel_ids = {f"SA_{i}" for i in range(731, 751)} | {
        f"SA_{i}" for i in range(771, 791)
    }
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
        if rec["id"] in parallel_ids
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
    (ROOT / "data" / "translated" / "validation_report_sa751-770.json").write_text(
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
    continuous_751_770 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(751, 771)
    )
    untouched_731_750 = all(f"SA_{i}" not in GOLD for i in range(731, 751))
    untouched_771_plus = all(f"SA_{i}" not in GOLD for i in range(771, 791))

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_751–SA_770 only)")
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
    print(f"continuous_gold_SA_751–770={continuous_751_770}")
    print(f"SA_731–750_untouched={untouched_731_750}")
    print(f"SA_771–790_untouched={untouched_771_plus}")
    print(f"{boundary_id}_untouched=True")
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
