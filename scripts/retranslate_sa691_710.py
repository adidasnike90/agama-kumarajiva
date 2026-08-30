#!/usr/bin/env python3
"""Retranslate SA 691–710（根力相应末–觉支相应初）→ merge.

本批二十经：七力 AN7.4；八力 AN8.27／AN8.28；九力（弱平行）；王力（无专平行）；
如来力 AN10.21；不正思惟 SN46.24；不退 SN46.36；盖 SN46.40；障盖 SN46.37；
木封 SN46.39；七觉支 SN46.38；听法（无专平行，近 SN46.38）。

信：有 AN／SN 平行者据巴利／Sujato 厘义；无专经 → medium。
    peyyāla／交叉指示补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_691–710；断言 SA_690 不变；不触碰 SA_711+。
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

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_SAR_LIT = "佛说此经已，尊者舍利弗闻佛所说，欢喜奉行。"
CLOSE_SAR_MOD = "佛说完这部经，尊者舍利弗听佛所说，欢喜奉行。"

FOUR_PADHANA_LIT = (
    "已生恶不善法令断，未生恶法令不生，未生善法令生，"
    "已生善法令住不忘、修习增广"
)
FOUR_PADHANA_MOD = (
    "已生的恶不善法要断除，未生的恶法使不生，未生的善法使生起，"
    "已生的善法使安住不忘、修习增长"
)

SEVEN_LIT = "信力、精进力、惭力、愧力、念力、定力、慧力"
SEVEN_MOD = "信力、精进力、惭力、愧力、念力、定力、慧力"

NINE_LIT = "信力、精进力、惭力、愧力、念力、定力、慧力、数力、修力"
NINE_MOD = "信力、精进力、惭力、愧力、念力、定力、慧力、数力、修力"

# 觉支次第据 SN：念→择法→精进→喜→猗（轻安）→定→舍
BOJJ_LIT = "念、择法、精进、喜、猗、定、舍"
BOJJ_MOD = "念、择法、精进、喜、猗、定、舍"
BOJJ_FULL_LIT = "念觉支、择法觉支、精进觉支、喜觉支、猗觉支、定觉支、舍觉支"
BOJJ_FULL_MOD = "念觉支、择法觉支、精进觉支、喜觉支、猗觉支、定觉支、舍觉支"

NIV_LIT = "贪欲、瞋恚、睡眠、掉悔、疑"
NIV_MOD = "贪欲、瞋恚、昏沉睡眠、掉举后悔、疑"
NIV_GAI_LIT = "贪欲盖、瞋恚盖、睡眠盖、掉悔盖、疑盖"
NIV_GAI_MOD = "贪欲盖、瞋恚盖、昏沉睡眠盖、掉举后悔盖、疑盖"

TEN_TATH_LIT = (
    "一、处非处如实知。二、过去未来现在业及受因事报如实知。"
    "三、禅、解脱、三昧、正受之杂染与清净如实知。四、众生诸根差别如实知。"
    "五、众生种种意解如实知。六、世间种种界如实知。七、一切至处道如实知。"
    "八、种种宿命如实忆念。九、天眼净见众生死此生彼、随业受报。"
    "十、诸漏已尽，无漏心解脱、慧解脱，现法自知作证："
    "我生已尽，梵行已立，所作已作，不受后有。"
)
TEN_TATH_MOD = (
    "一、如实知处与非处。二、如实知过去未来现在的业及受的因缘果报。"
    "三、如实知禅、解脱、三昧、正受的杂染与清净。四、如实知众生诸根的差别。"
    "五、如实知众生种种意向。六、如实知世间种种界。七、如实知一切能到某处的道。"
    "八、如实忆念种种宿命。九、以清净天眼见众生死此生彼、随业受报。"
    "十、诸漏已尽，无漏心解脱、慧解脱，在现法中自己证知："
    "我生已尽，梵行已立，所作已作，不再受后有。"
)

ROAR_LIT = "得先佛最胜处智，能转梵轮，于大众中作师子吼"
ROAR_MOD = "得先佛最胜处的智慧，能转梵轮，在大众中作师子吼"

EIGHT_WORLD_LIT = (
    "自在王者力、断事大臣力、结恨女人力、啼泣婴儿力、"
    "毁呰愚人力、审谛黠慧力、忍辱出家力、计数多闻力"
)
EIGHT_WORLD_MOD = (
    "自在王者力、断事大臣力、结恨女人力、啼泣婴儿力、"
    "毁呰愚人力、审谛黠慧力、忍辱出家力、计数多闻力"
)

TEN_WORLD_LIT = (
    "自在王者力、断事大臣力、机关工巧力、刀剑贼盗力、怨恨女人力、"
    "啼泣婴儿力、毁呰愚人力、审谛黠慧力、忍辱出家力、计数多闻力"
)
TEN_WORLD_MOD = (
    "自在王者力、断事大臣力、机关工巧力、刀剑贼盗力、怨恨女人力、"
    "啼泣婴儿力、毁呰愚人力、审谛黠慧力、忍辱出家力、计数多闻力"
)

# 漏尽八力（AN8.28）——据巴利校正汉本撮略
KHINA_EIGHT_LIT = (
    "一、以正慧如实善见一切诸行无常。"
    "二、以正慧如实善见诸欲如火坑。"
    "三、心顺趣远离、流注远离、浚输远离，乐出离，于一切漏处之法已永尽。"
    "四、四念处善修习。"
    "五、四神足善修习。"
    "六、五根善修习。"
    "七、七觉支善修习。"
    "八、八圣道善修习。"
)
KHINA_EIGHT_MOD = (
    "一、以正慧如实善见一切诸行无常。"
    "二、以正慧如实善见诸欲如同火坑。"
    "三、心顺向远离、流注远离、倾注远离，乐于出离，对一切能生漏的法已经永尽。"
    "四、四念处善加修习。"
    "五、四神足善加修习。"
    "六、五根善加修习。"
    "七、七觉支善加修习。"
    "八、八圣道善加修习。"
)

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

# --- SA 691 七力（AN7.4 广分别）-----------------------------------------------
SUTTAS["SA_691"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有七力——{SEVEN_LIT}。」",
        "「何等信力？于如来所起信心，深入坚固，"
        "诸天、魔、梵、沙门、婆罗门及余同法所不能坏，是名信力。」",
        f"「何等精进力？谓四正断——{FOUR_PADHANA_LIT}，是名精进力。」",
        "「何等惭力？耻于身口意恶行，耻起恶不善法，是名惭力。」",
        "「何等愧力？于可愧事而愧，愧起恶不善法，是名愧力。」",
        "「何等念力？谓四念处，是名念力。」",
        "「何等定力？谓四禅，是名定力。」",
        "「何等慧力？谓四圣谛，是名慧力。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有七种力——{SEVEN_MOD}。」",
        "「什么是信力？对如来生起信心，深入坚固，"
        "诸天、魔、梵、沙门、婆罗门以及其他同修都不能破坏，叫做信力。」",
        f"「什么是精进力？就是四正断——{FOUR_PADHANA_MOD}，叫做精进力。」",
        "「什么是惭力？耻于身口意恶行，耻于生起恶不善法，叫做惭力。」",
        "「什么是愧力？对可愧的事感到愧疚，愧于生起恶不善法，叫做愧力。」",
        "「什么是念力？就是四念处，叫做念力。」",
        "「什么是定力？就是四禅，叫做定力。」",
        "「什么是慧力？就是四圣谛，叫做慧力。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN7.4 Vitthatabala（七力广说）。"
        "gold_reconstructed：汉「如上广说／如上说」peyyāla → 据 AN7.4＋本卷学力定型补七力分别；"
        "精进取四正断（与卷内力相应一致）；惭愧从 AN 身口意恶行义压缩。"
    ),
}

# --- SA 692 八力（AN8.27 世间八力略）------------------------------------------
SUTTAS["SA_692"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当知八力：王者自在、大臣断事、女人结恨、婴儿啼泣、"
        "愚人毁呰、黠慧审谛、出家忍辱、多闻计数。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「应当知道八种力：王者的自在、大臣的断事、女人的结恨、婴儿的啼泣、"
        "愚人的毁谤指责、黠慧者的审慎谛观、出家人的忍辱、多闻者的思惟计数。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN8.27 Paṭhamabala（世间八力）。"
        "汉列王／大臣／女／婴儿／愚／慧／出家／多闻；"
        "AN 作啼泣／瞋／刀兵／王权／毁訾／审思／计数／忍辱——名次有异而义同世间力。"
        "罗什风压缩「何等为八」套语，直列八名。"
    ),
}

# --- SA 693 八力（分别）-------------------------------------------------------
SUTTAS["SA_693"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有八力——{EIGHT_WORLD_LIT}。」",
        "「自在王力者，王现自在威势；断事大臣力者，大臣现断事之功；"
        "结恨女人力者，女人现结恨；啼泣婴儿力者，婴儿现啼泣；"
        "毁呰愚人力者，愚人触事毁呰；审谛黠慧力者，黠慧常现审谛；"
        "忍辱出家力者，出家常现忍辱；计数多闻力者，多闻常现思惟计数。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有八种力——{EIGHT_WORLD_MOD}。」",
        "「自在王力，是王显现自在威势；断事大臣力，是大臣显现断事的功力；"
        "结恨女人力，是女人显现结恨；啼泣婴儿力，是婴儿显现啼泣；"
        "毁呰愚人力，是愚人遇事就毁谤指责；审谛黠慧力，是黠慧的人常现审慎谛观；"
        "忍辱出家力，是出家人常现忍辱；计数多闻力，是多闻的人常现思惟计数。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN8.27 分别差别。"
        "gold_reconstructed：peyyāla「如上说」补八力名目＋各一句释义。"
    ),
}

# --- SA 694 八力（漏尽；AN8.28）-----------------------------------------------
SUTTAS["SA_694"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时尊者舍利弗诣佛所，稽首礼足，退坐一面。"
        "佛告舍利弗：「漏尽比丘有几力，而能记说：我诸漏已尽？」",
        "舍利弗白佛：「漏尽比丘有八力，依此而记说：我诸漏已尽。」",
        f"「何等为八？{KHINA_EIGHT_LIT}」",
        "「成就此八力，漏尽比丘得记说：我诸漏已尽。」",
        CLOSE_SAR_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者舍利弗来到佛那里，稽首礼足，退坐一面。"
        "佛告诉舍利弗：「漏尽的比丘有几种力，才能记说：我的诸漏已经尽了？」",
        "舍利弗对佛说：「漏尽的比丘有八种力，依此而记说：我的诸漏已经尽了。」",
        f"「哪八种？{KHINA_EIGHT_MOD}」",
        "「成就这八种力，漏尽比丘就能记说：我的诸漏已经尽了。」",
        CLOSE_SAR_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN8.28 Dutiyabala（漏尽八力）；"
        "AN10.90 为十力扩本（多四正断／五力），本经汉作八力故从 AN8.28。"
        "据 AN 校正：（1）问答主客——佛问、舍利弗答（汉作舍利弗问佛）；"
        "（2）八力纲——诸行无常、欲如火坑、心向远离、四念处／四神足／五根／七觉／八正道"
        "（汉撮「顺趣离／出／涅槃」＋道品略举）。"
    ),
}

# --- SA 695 八力（异比丘问）---------------------------------------------------
SUTTAS["SA_695"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时有异比丘诣佛所，稽首礼足，退坐一面，白佛言："
        "「世尊！漏尽比丘有几力，而能记说：我诸漏已尽？」",
        f"佛告比丘：「漏尽比丘有八力——{KHINA_EIGHT_LIT}"
        "成就此八力，得记说：我诸漏已尽。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘来到佛那里，稽首礼足，退坐一面，对佛说："
        "「世尊！漏尽的比丘有几种力，才能记说：我的诸漏已经尽了？」",
        f"佛告诉比丘：「漏尽比丘有八种力——{KHINA_EIGHT_MOD}"
        "成就这八种力，就能记说：我的诸漏已经尽了。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN8.28 系 peyyāla 差别（异比丘问）。"
        "gold_reconstructed：汉仅「如舍利弗问经。如是异比丘问佛」→ 据 SA_694／AN8.28 补全问答＋八力纲；"
        "本经作比丘问、佛答。"
    ),
}

# --- SA 696 八力（告诸比丘）---------------------------------------------------
SUTTAS["SA_696"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「漏尽比丘有八力——{KHINA_EIGHT_LIT}"
        "成就此八力，漏尽比丘得记说：我诸漏已尽。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「漏尽的比丘有八种力——{KHINA_EIGHT_MOD}"
        "成就这八种力，漏尽比丘就能记说：我的诸漏已经尽了。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN8.28 系；告诸比丘略说。"
        "gold_reconstructed：汉「问诸比丘经亦如上说」→ 据 AN8.28 八力纲直告大众。"
    ),
}

# --- SA 697 九力（略）---------------------------------------------------------
SUTTAS["SA_697"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「比丘当知九力——信、精进、惭、愧、念、定、慧，及数力、修力。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「比丘应当知道九种力——信、精进、惭、愧、念、定、慧，以及数力、修力。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：SC 挂 AN8.28／AN10.90，然彼为漏尽力，"
        "与本经九力（七力＋数力＋修力）名目不符，故降 medium；"
        "依汉本略列，参七力定型。"
    ),
}

# --- SA 698 九力（分别）-------------------------------------------------------
SUTTAS["SA_698"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有九力——{NINE_LIT}。」",
        "「何等信力？于如来所起正信心，深入坚固，"
        "诸天、魔、梵、沙门、婆罗门及余同法所不能坏，是名信力。」",
        f"「何等精进力？谓四正断——{FOUR_PADHANA_LIT}，是名精进力。」",
        "「何等惭力？耻起恶不善法，是名惭力。何等愧力？于可愧事而愧，是名愧力。」",
        "「何等念力？谓内身身观住等四念处，是名念力。"
        "何等定力？谓四禅。何等慧力？谓四圣谛。」",
        "「何等数力？圣弟子于闲房、树下作如是数思："
        "『身口恶行者，现法后世当受恶报』——如是思惟计数，是名数力。」",
        "「何等修力？谓修四念处，是名修力。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有九种力——{NINE_MOD}。」",
        "「什么是信力？对如来生起正信，深入坚固，"
        "诸天、魔、梵、沙门、婆罗门以及其他同修都不能破坏，叫做信力。」",
        f"「什么是精进力？就是四正断——{FOUR_PADHANA_MOD}，叫做精进力。」",
        "「什么是惭力？耻于生起恶不善法，叫做惭力。什么是愧力？对可愧的事感到愧疚，叫做愧力。」",
        "「什么是念力？就是内身观身等四念处，叫做念力。"
        "什么是定力？就是四禅。什么是慧力？就是四圣谛。」",
        "「什么是数力？圣弟子在闲房、树下这样计数思惟："
        "『身口恶行的人，现法与后世当受恶报』——这样思惟计数，叫做数力。」",
        "「什么是修力？就是修习四念处，叫做修力。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：同 697，SC 平行与名目不合；"
        "gold_reconstructed：汉「如上说／如前说」→ 据七力定型＋汉残句补数力／修力。"
    ),
}

# --- SA 699 王力（十世间力略；无平行）-----------------------------------------
SUTTAS["SA_699"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当知十力：王者自在、大臣断事、机关工巧、刀剑贼盗、女人怨恨、"
        "婴儿啼泣、愚人毁呰、黠慧审谛、出家忍辱、多闻计数。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「应当知道十种力：王者的自在、大臣的断事、机关的工巧、盗贼的刀剑、女人的怨恨、"
        "婴儿的啼泣、愚人的毁谤指责、黠慧者的审慎谛观、出家人的忍辱、多闻者的思惟计数。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：十世间力（八力加机关工巧、刀剑贼盗）；"
        "无 SC 专经，依汉本略列。"
    ),
}

# --- SA 700 王力（分别）-------------------------------------------------------
SUTTAS["SA_700"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有十力——{TEN_WORLD_LIT}。」",
        "「自在王力者，王现自在威势；断事大臣力者，大臣现断事之功；"
        "机关工巧力者，造机关者现其工巧；刀剑贼盗力者，盗贼现刀剑之势；"
        "怨恨女人力者，女人现怨恨；啼泣婴儿力者，婴儿现啼泣；"
        "毁呰愚人力者，愚人触事毁呰；审谛黠慧力者，黠慧常现审谛；"
        "忍辱出家力者，出家常现忍辱；计数多闻力者，多闻常现思惟计数。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有十种力——{TEN_WORLD_MOD}。」",
        "「自在王力，是王显现自在威势；断事大臣力，是大臣显现断事的功力；"
        "机关工巧力，是造机关的人显现工巧；刀剑贼盗力，是盗贼显现刀剑之势；"
        "怨恨女人力，是女人显现怨恨；啼泣婴儿力，是婴儿显现啼泣；"
        "毁呰愚人力，是愚人遇事就毁谤指责；审谛黠慧力，是黠慧的人常现审慎谛观；"
        "忍辱出家力，是出家人常现忍辱；计数多闻力，是多闻的人常现思惟计数。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：同 699。"
        "gold_reconstructed：汉仅释五力、余「如上说」→ 据 693／699 补足十力各一句。"
    ),
}

# --- SA 701 如来力（十力略；AN10.21）------------------------------------------
SUTTAS["SA_701"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有十种如来力。成就此力，如来、应、等正觉{ROAR_LIT}。」",
        f"「何等为十？{TEN_TATH_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有十种如来力。成就这些力，如来、应、等正觉就{ROAR_MOD}。」",
        f"「哪十种？{TEN_TATH_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.21 Sīhanāda（十如来力）。"
        "gold_reconstructed：汉「初力……乃至漏尽如上说」→ 据 SA_684／AN10.21 压缩十力各一句；"
        "转梵轮／师子吼套语并为一处。"
    ),
}

# --- SA 702 如来力（答问记说）-------------------------------------------------
SUTTAS["SA_702"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「如来有十力。成就此力，如来、应、等正觉{ROAR_LIT}。」",
        "「若有来问处非处智力，如来如其所知见觉，成等正觉，为彼记说。"
        "问业报智力、禅解脱三昧正受智力、诸根差别智力、种种意解智力、"
        "种种界智力、至处道智力、宿命智力、天眼智力、漏尽智力，亦复如是——"
        "皆如所知见觉，为彼记说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「如来有十种力。成就这些力，如来、应、等正觉就{ROAR_MOD}。」",
        "「如果有人来问处非处智力，如来就按自己所知所见所觉、成等正觉的内容，为他记说。"
        "问业报智力、禅解脱三昧正受智力、诸根差别智力、种种意解智力、"
        "种种界智力、至处道智力、宿命智力、天眼智力、漏尽智力，也是一样——"
        "都按所知所见所觉，为他记说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN10.21／SA_687 系答问记说差别。"
        "gold_reconstructed：peyyāla「如上说／广说如上」→ 十力问答纲；"
        "无专 SN，义从 AN 十力。"
    ),
}

# --- SA 703 如来力（教诫＋学力／十力）-----------------------------------------
SUTTAS["SA_703"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「凡所有法，彼彼意解作证，皆由如来无畏智所生。"
        "若比丘为我声闻，不谄不伪，质直心生，我则为彼教诫、教授说法——"
        "晨朝说法，至日中得胜进；日暮说法，至晨朝得胜进。"
        "彼生正直心，实知实、不实知不实，上知上、无上知无上；"
        "当知、当见、当得、当觉者，皆悉了知，斯有是处。」",
        "「所谓五学力、十种如来力。何等五学力？信力、精进力、念力、定力、慧力。」",
        f"「何等十如来力？{TEN_TATH_LIT}」",
        "「若有来问处非处智力，如来如所知见觉，为彼记说；乃至漏尽智力，亦复如是。"
        "诸比丘！处非处智力，我说是定、非不定；乃至漏尽智，我说是定、非不定——"
        "定者正道，非定者邪道。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「凡是各种法，随各自意向而证知的，都由如来无畏智所生。"
        "如果比丘做我的声闻，不谄曲、不虚伪，生起质直心，我就为他教诫、教授说法——"
        "早晨说法，到中午得到胜进；傍晚说法，到早晨得到胜进。"
        "他生起正直心，实的知道是实、不实的知道是不实，上的知道是上、无上的知道是无上；"
        "应当知、见、得、觉的，都能了知，这是有这个道理的。」",
        "「也就是五学力、十种如来力。哪五种学力？信力、精进力、念力、定力、慧力。」",
        f"「哪十种如来力？{TEN_TATH_MOD}」",
        "「如果有人来问处非处智力，如来就按所知所见所觉为他记说；乃至漏尽智力，也是一样。"
        "比丘们！处非处智力，我说是确定的、不是不确定的；乃至漏尽智，我说是确定的、不是不确定的——"
        "确定的是正道，不确定的是邪道。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN10.21 系扩说（教诫胜进＋五学力＋十力＋定／非定）。"
        "gold_reconstructed：十力「如上广说」→ 据 SA_684／AN 压缩；"
        "保留汉「晨朝／日暮胜进」与「定者正道」义。"
    ),
}

# --- SA 704 不正思惟（SN46.24）------------------------------------------------
SUTTAS["SA_704"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「若不正思惟，未起{NIV_LIT}盖则起，已起则增广；"
        f"未起{BOJJ_LIT}觉支则不起，已起则退失。」",
        f"「若正思惟，未起{NIV_LIT}盖则不起，已起则断；"
        f"未起{BOJJ_LIT}觉支则起，已起则增广。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「如果不正思惟，未生起的{NIV_MOD}盖就会生起，已生起的就会增广；"
        f"未生起的{BOJJ_MOD}觉支就不会生起，已生起的就会退失。」",
        f"「如果正思惟，未生起的{NIV_MOD}盖就不会生起，已生起的就会断除；"
        f"未生起的{BOJJ_MOD}觉支就会生起，已生起的就会增广。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.24 Ayonisomanasikāra。"
        "据 SN 校正觉支次第：喜先于猗（passaddhi）；压缩五盖／七觉各别重复。"
    ),
}

# --- SA 705 不退（SN46.36）----------------------------------------------------
SUTTAS["SA_705"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五退法——{NIV_LIT}盖，是名退法。」",
        f"「若修习七觉支——{BOJJ_FULL_LIT}——多修令增广，是名不退法。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种退堕之法——{NIV_MOD}盖，叫做退法。」",
        f"「如果修习七觉支——{BOJJ_FULL_MOD}——多多修习使它增广，叫做不退法。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.36 Aparihāniya（七觉支→不退减）。"
        "汉有五退法对举，义与邻经五盖／七觉配对相合，故保留；"
        "SN 正文唯强调七觉不退。觉支次第据 SN。"
    ),
}

# --- SA 706 盖（SN46.40）------------------------------------------------------
SUTTAS["SA_706"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五法能为黑暗、能盲无目、能作无智、能羸智慧，"
        f"非明、非等觉，不转趣涅槃——谓{NIV_LIT}。」",
        f"「有七觉支能作大明、能为目、增长智慧，为明、为正觉，转趣涅槃——"
        f"谓{BOJJ_FULL_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种法能造成黑暗、能使人盲目、能造成无智、能削弱智慧，"
        f"不是明、不是等觉，不导向涅槃——就是{NIV_MOD}。」",
        f"「有七觉支能造成大光明、能成为眼睛、增长智慧，是明、是正觉，导向涅槃——"
        f"就是{BOJJ_FULL_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.40 Nīvaraṇa（五盖黑暗／七觉明）。"
        "据 SN：盖→障慧、不趣涅槃；觉支→生明见、趣涅槃。压缩汉重复套语。"
    ),
}

# --- SA 707 障盖（SN46.37）----------------------------------------------------
SUTTAS["SA_707"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五障、五盖，染恼于心，能羸智慧，为障阂分，"
        f"非明、非等觉，不转趣涅槃——谓{NIV_GAI_LIT}。」",
        f"「七觉支非障非盖，不恼于心，增长智慧，为明、为正觉，转趣涅槃——"
        f"谓{BOJJ_FULL_LIT}。」",
        "尔时世尊说偈言：「贪瞋与睡眠，　掉悔及与疑，　五盖覆世间，　令不见正道；"
        "若得七觉支，　则为大照明；　念择法精进，　喜猗定与舍，　随顺牟尼道，　脱生死怖畏。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种障、五种盖，染恼于心，能削弱智慧，属于障阂一类，"
        f"不是明、不是等觉，不导向涅槃——就是{NIV_GAI_MOD}。」",
        f"「七觉支不是障、不是盖，不恼乱于心，增长智慧，是明、是正觉，导向涅槃——"
        f"就是{BOJJ_FULL_MOD}。」",
        "那时世尊说偈：「贪瞋与睡眠，　掉悔以及疑，　五盖覆世间，　使人不见正道；"
        "若得七觉支，　就成为大照明；　念择法精进，　喜猗定与舍，　随顺牟尼道，　脱离生死怖畏。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.37 Āvaraṇa（障盖羸慧／觉支非障）。"
        "汉偈保留而罗什风压缩；觉支次第据 SN。SN 无偈处不增宗，唯压缩汉偈。"
    ),
}

# --- SA 708 木封（SN46.39）----------------------------------------------------
SUTTAS["SA_708"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「若族姓子舍世务，剃发着袈裟，正信非家、出家学道；"
        "而有愚人依聚落，入村乞食，不护身、不守根、不摄念，"
        "取女人少壮之相而生染着，欲火烧心，返俗退戒——"
        "本求出离，反增罪业而自破坏。」",
        "「譬如大树，种子至微，长大乃能缠障余树，令其摧折仆倒。"
        f"如是五心树——{NIV_GAI_LIT}——种子虽微，增长则荫覆善心，令其堕卧。」",
        f"「若修七觉支——{BOJJ_FULL_LIT}——多修习已，转成不退。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「如果族姓子舍弃世务，剃发穿着袈裟，正信而从非家出去学道；"
        "却有愚人依住聚落，进村乞食，不护身、不守根门、不摄念，"
        "执取女人少壮的相貌而生染着，欲火烧心，返俗退戒——"
        "本来求出离，反而增罪业而自己破坏。」",
        "「好比大树，种子极小，长大后却能缠障其他的树，使它摧折仆倒。"
        f"同样，五种心树——{NIV_GAI_MOD}——种子虽小，增长就会荫覆善心，使它倒下。」",
        f"「如果修习七觉支——{BOJJ_FULL_MOD}——多多修习之后，就成为不退转。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.39 Rukkha（寄生大树喻五盖）。"
        "据 SN：出家后更陷欲而摧折；五盖为心之寄生树；七觉非障、趣智解脱。"
        "汉树名略去专名，取喻义；觉支次第据 SN。"
    ),
}

# --- SA 709 七觉支（SN46.38 听法）---------------------------------------------
SUTTAS["SA_709"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「若比丘专一其心，侧耳听法，能断五法，修习七法，令得满足。」",
        f"「何等断五？谓{NIV_GAI_LIT}。」",
        f"「何等修七？谓{BOJJ_FULL_LIT}——修此七法，转进满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「如果比丘专一其心，侧耳听法，就能断除五种法，修习七种法，使它们满足。」",
        f"「断除哪五种？就是{NIV_GAI_MOD}。」",
        f"「修习哪七种？就是{BOJJ_FULL_MOD}——修这七法，展转增进而满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.38 Aparihāniya／听法（圣弟子专心听法时五盖灭、七觉满）。"
        "汉缺「尔时告比丘」开场，补佛告；觉支次第据 SN。"
    ),
}

# --- SA 710 听法（无专平行；近 709＋心／慧解脱）--------------------------------
SUTTAS["SA_710"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「圣弟子以清净信心专精听法，能断五法，修习七法，令得满足。」",
        f"「何等五？谓{NIV_GAI_LIT}，此则断。」",
        f"「何等七？谓{BOJJ_FULL_LIT}——修令满足。」",
        "「净信者得心解脱，具智者得慧解脱。"
        "贪欲染心者不得厌离，无明染心者慧不清净。"
        "是故离贪者心解脱，离无明者慧解脱。"
        "若比丘离贪得心解脱、身作证，离无明得慧解脱——"
        "是名断爱缚结，慢无间等，究竟苦边。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「圣弟子以清净信心专心听法，就能断除五种法，修习七种法，使它们满足。」",
        f"「哪五种？就是{NIV_GAI_MOD}，这些就会断除。」",
        f"「哪七种？就是{BOJJ_FULL_MOD}——修习使它们满足。」",
        "「有净信的人得心解脱，具智慧的人得慧解脱。"
        "被贪欲染污的心得不到厌离，被无明染污的心智慧不清净。"
        "所以离贪的人心解脱，离无明的人慧解脱。"
        "如果比丘离贪而得心解脱、以身作证，离无明而得慧解脱——"
        "这就叫做断除爱的系缚与慢等无间，究竟到达苦的尽头。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；近 SN46.38／SA_709，"
        "而结以心解脱／慧解脱与断爱缚究竟苦边。"
        "据项目规约：汉「不得不乐」→作「不得厌离」，结句用「离贪／离无明」"
        "（厌故离贪），不取「厌故不乐」。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_691": "high",
    "SA_692": "high",
    "SA_693": "high",
    "SA_694": "high",
    "SA_695": "high",
    "SA_696": "high",
    "SA_697": "medium",
    "SA_698": "medium",
    "SA_699": "medium",
    "SA_700": "medium",
    "SA_701": "high",
    "SA_702": "high",
    "SA_703": "high",
    "SA_704": "high",
    "SA_705": "high",
    "SA_706": "high",
    "SA_707": "high",
    "SA_708": "high",
    "SA_709": "high",
    "SA_710": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_691": "七力如上广说 → AN7.4＋学力定型补分别",
    "SA_693": "如上说 → 八力名目＋各一句释义",
    "SA_695": "如舍利弗问经／异比丘问 → AN8.28 八力纲＋异问者",
    "SA_696": "问诸比丘经亦如上说 → AN8.28 八力直告",
    "SA_698": "如上说／如前说 → 七力定型＋数力／修力",
    "SA_700": "如上说残释 → 据 693／699 补足十力释义",
    "SA_701": "初力乃至漏尽如上说 → SA_684／AN10.21 十力压缩",
    "SA_702": "如上说／广说如上 → 十力答问记说纲",
    "SA_703": "十力如上广说 → SA_684／AN 十力压缩",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(691, 711)}, (
        "GOLD must cover SA_691–SA_710 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    assert not any(f"SA_{i}" in GOLD for i in range(671, 691))
    assert not any(f"SA_{i}" in GOLD for i in range(711, 721))

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

    boundary_id = "SA_690"
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

    # Snapshot SA_711+ (sample) and SA_671–690 to assert untouched
    guard_ids = {f"SA_{i}" for i in range(671, 691)} | {f"SA_{i}" for i in range(711, 721)}
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
            else:
                item.pop("quality_gate_reasons", None)

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
                assert before == after, f"{rid} must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa691-710.json").write_text(
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
    continuous_1_710 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1, 711)
    )
    continuous_691_710 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(691, 711)
    )
    untouched_711 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") not in goldish
        or f"SA_{i}" not in GOLD
        for i in range(711, 721)
    )

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_691–SA_710 only)")
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
    print(f"continuous_gold_SA_691–710={continuous_691_710}")
    print(f"continuous_gold_SA_1–710={continuous_1_710}")
    print(f"SA_711–720_not_in_GOLD={untouched_711}")
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
