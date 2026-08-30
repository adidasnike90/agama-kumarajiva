#!/usr/bin/env python3
"""Retranslate SA 1051–1070（业报相应末 + 比丘相应起）→ merge.

本批二十经：
1051–1061 业报末（岸 AN10.170、真实法、恶法、善男子、十～四十法、法非法）
1062–1070 比丘相应起（善生 SN21.5、恶色、提婆、象首、难陀 AN8.9/SN21.8、
         窒师、般阇闻、年少）

信：有 AN／SN 平行者据巴利／Sujato 厘义；peyyāla／「如上说」据平行或邻经补纲；
    1060–1061 SC 标 AN10.198，汉文为非法／正律对举，义近 AN10.171 系，据十业道厘义；
    1065 汉叙事「手比丘」命终，法义同 SN3.2／SN3.23 贪瞋痴；
    1066 「如手比丘」peeyāla → 据 SA_1065 纲；SC 亦列 AN8.9（根门难陀）与汉略异。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_1051–1070；断言 SA_1050 不变；不触碰 SA_1071+。
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

BATCH = range(1051, 1071)

# ---------------------------------------------------------------------------
# 共用框式
# ---------------------------------------------------------------------------

OPEN_JET_LIT = "如是我闻：一时，佛住舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_BAM_LIT = "如是我闻：一时，佛住王舍城迦兰陀竹园。"
OPEN_BAM_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY_MOD = "他听佛所说，欢喜随喜，作礼离去。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)

TEN_BAD_LIT = "杀生、不与取、邪淫、妄语、两舌、恶口、绮语、贪、瞋、邪见"
TEN_BAD_MOD = TEN_BAD_LIT
TEN_GOOD_LIT = "不杀生、不与取、不邪淫、不妄语、不两舌、不恶口、不绮语、无贪、无瞋、正见"
TEN_GOOD_MOD = TEN_GOOD_LIT

AWAKEN_LIT = "我生已尽，梵行已立，所作已作，自知不受后有。"
AWAKEN_MOD = AWAKEN_LIT

SPEAR_BAD_LIT = "如铁矛投水，直沉不浮"
SPEAR_BAD_MOD = "像铁矛投进水里，直沉下去浮不起来"
SPEAR_GOOD_LIT = "如铁矛仰投虚空，轻扬而上"
SPEAR_GOOD_MOD = "像铁矛向上投向虚空，轻扬而起"

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 1051 岸（AN10.170 Orima）--------------------------------------------
SUTTAS["SA_1051"] = {
    "lit": [
        OPEN_BAM_LIT,
        "时有生闻婆罗门来诣佛所，稽首退坐，白言：「瞿昙！所说此岸、彼岸——云何此岸？云何彼岸？」",
        "佛告婆罗门："
        f"「{TEN_BAD_LIT}——是名此岸；"
        f"{TEN_GOOD_LIT}——是名彼岸。」"
        "即说偈言：「少有修善人，能度于彼岸；一切众生类，驰走于此岸。"
        "于此正法律，观察诸法相；如是度彼岸，摧伏死魔军。」",
        "生闻婆罗门闻已，欢喜随喜，从坐起去。"
        "异比丘所问、尊者阿难所问、佛问诸比丘——三经亦如上说。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "那时有生闻婆罗门来见佛，顶礼后退坐一旁，问道："
        "「瞿昙！您所说的此岸、彼岸——什么是此岸？什么是彼岸？」",
        "佛告诉婆罗门："
        f"「{TEN_BAD_MOD}——这叫做此岸；"
        f"{TEN_GOOD_MOD}——这叫做彼岸。」"
        "接着说偈：「少有人修善，能度到彼岸；其余一切众生，只在此岸奔走。"
        "在这正法律中，观察诸法之相；这样就能度到彼岸，摧伏死魔之军。」",
        "生闻婆罗门听完，欢喜随喜，起身离去。"
        "另有异比丘所问、尊者阿难所问、佛问诸比丘——三经也如上所说。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.170；"
        "十不善为此岸、十善为彼岸；偈据 AN／汉合写；"
        "末「三经亦如上说」peeyāla 保留纲目。"
    ),
}

# --- SA 1052 真实法（AN10.191 Saddhamma）------------------------------------
SUTTAS["SA_1052"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有恶法，有真实法。谛听。"
        f"云何恶法？谓{TEN_BAD_LIT}，是名恶法。"
        f"云何真实法？谓{TEN_GOOD_LIT}，是名真实法。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有恶法，有真实法。仔细听。"
        f"什么是恶法？就是{TEN_BAD_MOD}，这叫做恶法。"
        f"什么是真实法？就是{TEN_GOOD_MOD}，这叫做真实法。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.191；"
        "恶法＝十不善，真实法＝十善。"
    ),
}

# --- SA 1053 恶法（AN4.207–210 pāpadhamma 系）-------------------------------
SUTTAS["SA_1053"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有恶法、恶恶法；有真实法、真实真实法。谛听。"
        f"云何恶法？谓{TEN_BAD_LIT}。"
        "云何恶恶法？谓自作杀生，复教人杀，乃至自起邪见，复以邪见教人。"
        f"云何真实法？谓{TEN_GOOD_LIT}。"
        "云何真实真实法？谓自不杀生，复教人不杀，乃至自行正见，复以正见教人。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有恶法、加倍的恶法；有真实法、加倍的真实法。仔细听。"
        f"什么是恶法？就是{TEN_BAD_MOD}。"
        "什么是加倍的恶法？就是自己杀生，又教人杀，乃至自己起邪见，又拿邪见教人。"
        f"什么是真实法？就是{TEN_GOOD_MOD}。"
        "什么是加倍的真实法？就是自己不杀生，又教人不杀，乃至自己行正见，又拿正见教人。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：parallels AN4.207–210；"
        "自作＋教作＝「恶恶／真实真实」；十支据 AN／汉补全。"
    ),
}

# --- SA 1054 善男子（AN10.192 Sappurisadhamma）------------------------------
SUTTAS["SA_1054"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有不善男子，有善男子。谛听。"
        f"云何不善男子？谓行{TEN_BAD_LIT}者。"
        f"云何善男子？谓行{TEN_GOOD_LIT}者。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有不善男子，有善男子。仔细听。"
        f"什么是不善男子？就是行{TEN_BAD_MOD}的人。"
        f"什么是善男子？就是行{TEN_GOOD_MOD}的人。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.192；"
        "不善／善男子以十不善、十善分判。"
    ),
}

# --- SA 1055 善男子善男子（AN4.201 系）--------------------------------------
SUTTAS["SA_1055"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有不善男子、不善男子之不善男子；"
        "有善男子、善男子之善男子。谛听。"
        f"云何不善男子？谓行{TEN_BAD_LIT}者。"
        "云何不善男子之不善男子？谓手自杀生，复教人杀，乃至自行邪见，复教人行邪见。"
        f"云何善男子？谓行{TEN_GOOD_LIT}者。"
        "云何善男子之善男子？谓自不杀生，复教人不杀，乃至自行正见，复以正见教人。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有不善男子、加倍的不善男子；"
        "有善男子、加倍的善男子。仔细听。"
        f"什么是不善男子？就是行{TEN_BAD_MOD}的人。"
        "什么是加倍的不善男子？就是亲手杀生，又教人杀，乃至自己行邪见，又教人行邪见。"
        f"什么是善男子？就是行{TEN_GOOD_MOD}的人。"
        "什么是加倍的善男子？就是自己不杀生，又教人不杀，乃至自己行正见，又拿正见教人。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN4.201 系；"
        "自作＋教作层层加深不善／善。"
    ),
}

# --- SA 1056 十法（AN10.221）------------------------------------------------
SUTTAS["SA_1056"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若成就十法，"
        f"{SPEAR_BAD_LIT}，身坏命终，下生恶趣泥犁。"
        f"何等为十？谓{TEN_BAD_LIT}。"
        "「若成就十法，"
        f"{SPEAR_GOOD_LIT}，身坏命终，上生天上。"
        f"何等为十？谓{TEN_GOOD_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「若成就十法，"
        f"{SPEAR_BAD_MOD}，身体坏灭命终后，下生恶趣地狱。"
        f"哪十种？就是{TEN_BAD_MOD}。"
        "「若成就十法，"
        f"{SPEAR_GOOD_MOD}，身体坏灭命终后，上生天上。"
        f"哪十种？就是{TEN_GOOD_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.221（resembling）；"
        "十不善沉堕／十善上生；铁矛喻从汉，义同巴利投水／上扬。"
    ),
}

# --- SA 1057 二十法（AN10.222）----------------------------------------------
SUTTAS["SA_1057"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若成就二十法，"
        f"{SPEAR_BAD_LIT}，身坏命终，下生恶趣泥犁。"
        "何等二十？谓自手杀生，复教人杀；乃至自行邪见，复以邪见教人——"
        "自作、教作各十，合为二十。"
        "「若成就二十法，"
        f"{SPEAR_GOOD_LIT}，身坏命终，上生天上。"
        "何等二十？谓自不杀生，复教人不杀；乃至自行正见，复以正见教人。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「若成就二十法，"
        f"{SPEAR_BAD_MOD}，身体坏灭命终后，下生恶趣地狱。"
        "哪二十种？就是自己亲手杀生，又教人杀；乃至自己行邪见，又拿邪见教人——"
        "自作、教作各十，合为二十。"
        "「若成就二十法，"
        f"{SPEAR_GOOD_MOD}，身体坏灭命终后，上生天上。"
        "哪二十种？就是自己不杀生，又教人不杀；乃至自己行正见，又拿正见教人。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.222；"
        "二十＝十不善／十善之自作＋教作。"
    ),
}

# --- SA 1058 三十法（AN10.223）----------------------------------------------
SUTTAS["SA_1058"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若成就三十法，"
        f"{SPEAR_BAD_LIT}，身坏命终，下生恶趣泥犁。"
        "何等三十？谓自手杀生，教人令杀，赞叹杀生；"
        "乃至自行邪见，教人令行，常赞行邪见者——"
        "自作、教作、赞叹各十，合为三十。"
        "「若成就三十法，"
        f"{SPEAR_GOOD_LIT}，身坏命终，上生天上。"
        "何等三十？谓自不杀生，教人不杀，常赞不杀功德；"
        "乃至自行正见，教人令行，常赞正见功德。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「若成就三十法，"
        f"{SPEAR_BAD_MOD}，身体坏灭命终后，下生恶趣地狱。"
        "哪三十种？就是自己亲手杀生，教人杀，又称赞杀生；"
        "乃至自己行邪见，教人行，又常常称赞行邪见的人——"
        "自作、教作、赞叹各十，合为三十。"
        "「若成就三十法，"
        f"{SPEAR_GOOD_MOD}，身体坏灭命终后，上生天上。"
        "哪三十种？就是自己不杀生，教人不杀，又常常称赞不杀的功德；"
        "乃至自己行正见，教人行，又常常称赞正见的功德。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.223；"
        "三十＝自作＋教作＋赞叹。"
    ),
}

# --- SA 1059 四十法（AN10.224）----------------------------------------------
SUTTAS["SA_1059"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若成就四十法，"
        f"{SPEAR_BAD_LIT}，身坏命终，下生恶趣泥犁。"
        "何等四十？谓手自杀生，教人令杀，赞叹杀生，见他杀生心随欢喜；"
        "乃至自行邪见，教人令行，赞叹邪见，见行邪见心随欢喜——"
        "自作、教作、赞叹、随喜各十，合为四十。"
        "「若成就四十法，"
        f"{SPEAR_GOOD_LIT}，身坏命终，上生天上。"
        "何等四十？谓不杀生，教人不杀，口赞不杀，见不杀者心随欢喜；"
        "乃至自行正见，教人令行，赞叹正见，见行正见心随欢喜。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「若成就四十法，"
        f"{SPEAR_BAD_MOD}，身体坏灭命终后，下生恶趣地狱。"
        "哪四十种？就是亲手杀生，教人杀，称赞杀生，看见别人杀生心里跟着欢喜；"
        "乃至自己行邪见，教人行，称赞邪见，看见别人行邪见心里跟着欢喜——"
        "自作、教作、赞叹、随喜各十，合为四十。"
        "「若成就四十法，"
        f"{SPEAR_GOOD_MOD}，身体坏灭命终后，上生天上。"
        "哪四十种？就是不杀生，教人不杀，口称赞不杀，看见不杀的人心里跟着欢喜；"
        "乃至自己行正见，教人行，称赞正见，看见别人行正见心里跟着欢喜。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.224；"
        "四十＝自作＋教作＋赞叹＋随喜。"
    ),
}

# --- SA 1060 法非法（SC 标 AN10.198；义近 AN10.171 Adhamma）----------------
SUTTAS["SA_1060"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有非法，有正法。谛听。"
        f"何等非法？谓{TEN_BAD_LIT}，是名非法。"
        f"何等正法？谓{TEN_GOOD_LIT}，是名正法。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有非法，有正法。仔细听。"
        f"什么是非法？就是{TEN_BAD_MOD}，这叫做非法。"
        f"什么是正法？就是{TEN_GOOD_MOD}，这叫做正法。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：SC 标 AN10.198 Sacchikātabba，"
        "然汉文为非法／正法对举，义近 AN10.171 Adhamma；据十业道厘义。"
        "据 SN／AN 校正：法义取十不善／十善，不取「应实证法」纲。"
    ),
}

# --- SA 1061 非律正律＋peeyāla（SC 同标 AN10.198）---------------------------
SUTTAS["SA_1061"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有非律，有正律。谛听。"
        f"何等非律？谓{TEN_BAD_LIT}。"
        f"何等正律？谓{TEN_GOOD_LIT}。」",
        "如非律、正律——非圣与圣、不善与善、非亲近与亲近、非善哉与善哉、"
        "黑法与白法、非义与正义、卑法与胜法、有罪与无罪、弃法与不弃法——"
        "一一经皆如上说，以十不善、十善分判。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有非律，有正律。仔细听。"
        f"什么是非律？就是{TEN_BAD_MOD}。"
        f"什么是正律？就是{TEN_GOOD_MOD}。」",
        "像非律与正律这样——非圣与圣、不善与善、不该亲近与该亲近、不善哉与善哉、"
        "黑法与白法、非义与正义、卑下法与殊胜法、有罪与无罪、应弃与不应弃——"
        "每一经都如上所说，都以十不善、十善来分判。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：SC 标 AN10.198；汉 peeyāla 系列对举，"
        "据十业道补纲。reconstruction：非法对举 peeyāla 纲。"
    ),
}

# --- SA 1062 善生（SN21.5 Sujāta）-------------------------------------------
SUTTAS["SA_1062"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者善生新剃须发，着袈裟衣，正信非家而出家，来诣佛所，稽首退坐。",
        "世尊告诸比丘：「当知此善生善男子二处端严："
        "一者剃除须发，着袈裟衣，正信非家出家；"
        f"二者尽诸有漏，无漏心解脱、慧解脱，现法自知作证：『{AWAKEN_LIT}』」"
        "即说偈言：「寂静尽诸漏，比丘庄严好；离欲断诸结，涅槃不复生；"
        "持此最后身，摧伏魔怨敌。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者善生刚剃去须发，穿着袈裟，以正信从有家入于非家而出家，"
        "来到佛前，顶礼后退坐一旁。",
        "世尊告诉比丘们：「应当知道，这位善生善男子有两处端严："
        "一是剃除须发，穿着袈裟，以正信出家；"
        f"二是已尽诸有漏，得无漏心解脱、慧解脱，在现法中自己现证：『{AWAKEN_MOD}』」"
        "接着说偈：「寂静而尽诸漏，比丘这样才真正庄严；离欲断结，涅槃不再受生；"
        "持此最后之身，摧伏魔怨。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN21.5；"
        "二处端严＝出家相好＋漏尽作证（巴利兼美色与梵行究竟；汉重出家相与漏尽）。"
    ),
}

# --- SA 1063 恶色（SN21.6 Lakuṇḍakabhaddiya）--------------------------------
SUTTAS["SA_1063"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘形色丑陋，难可瞻视，为诸比丘所轻慢，来诣佛所。"
        "四众见之，皆起轻想，相谓：「彼何比丘？形貌丑陋，为人轻慢。」",
        "世尊知诸比丘心念，告言：「汝等见彼比丘形貌丑陋、令人起慢不？」"
        "答言：「唯然，已见。」"
        "佛言：「莫于彼起轻想。所以者何？彼已尽诸漏，所作已作，离诸重担，"
        "断诸有结，正智，心善解脱。莫妄量人，唯如来能量人。」",
        "彼比丘稽首退坐。世尊复告：「莫于是比丘起轻想；莫量于人，唯如来能知人。」"
        "即说偈言：「飞鸟及走兽，莫不畏师子；唯师子兽王，无有与等者。"
        "如是智慧人，虽小则为大；莫取其身相，而生轻慢心。"
        "何用巨大身，多肉而无慧；此贤胜智慧，则为上士夫。"
        "离欲断诸结，涅槃永不生；持此最后身，摧伏众魔军。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘形貌丑陋，难看，被比丘们轻慢，来到佛前。"
        "四众看见他，都起轻慢想，彼此说：「那是什么比丘？形貌丑陋，被人轻慢。」",
        "世尊知道比丘们心里想什么，问：「你们看见那位比丘形貌丑陋、让人起慢心吗？」"
        "答：「是的，已经看见了。」"
        "佛说：「不要对他起轻慢想。为什么？他已经尽诸漏，所作已作，卸下重担，"
        "断除有结，有正智，心善解脱。不要妄自衡量人，只有如来能衡量人。」",
        "那位比丘顶礼后退坐。世尊又说：「不要对这位比丘起轻慢；不要衡量人，只有如来能知人。」"
        "接着说偈：「飞鸟走兽，无不畏惧狮子；唯有狮子王，没有匹敌。"
        "有智慧的人也是这样，身虽小而为大；不要看外表，就生轻慢。"
        "巨大的身躯有什么用？多肉而无慧；这位贤者智慧殊胜，才是上士。"
        "离欲断结，涅槃不再受生；持此最后之身，摧伏众魔军。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN21.6；"
        "莫以貌取；漏尽大力，唯如来能量人。"
    ),
}

# --- SA 1064 提婆（SN17.35／AN4.68）-----------------------------------------
SUTTAS["SA_1064"] = {
    "lit": [
        OPEN_BAM_LIT,
        "尔时提婆达多利养大起：摩竭陀王阿阇世韦提希子日日五百乘车来诣，"
        "日日持五百釜食供养；提婆达多将五百人别众而受。",
        "众多比丘入城乞食，闻已，还诣佛所白言。"
        "佛告诸比丘：「莫称叹提婆达多所得利养。所以者何？"
        "彼以利养自坏，他世亦坏——"
        "如芭蕉、竹、芦，结果即枯；如骡受胎，母子俱丧。"
        "愚人提婆达多受此利养，长夜得不饶益苦。"
        "是故应当学：设有利养起，莫生染着。」"
        "即说偈言：「芭蕉生果死，竹芦实亦然；骡以妊故丧，士以贪自丧。"
        "常行非义行，多知不免愚；善法日损减，茎枯根亦伤。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "那时提婆达多得到很大的利养：摩竭陀王阿阇世——韦提希之子——每天带着五百辆车来，"
        "每天送来五百釜食物供养；提婆达多带着五百人另立一众来接受。",
        "许多比丘进城乞食，听说以后，回到佛那里禀告。"
        "佛告诉比丘们：「不要称叹提婆达多所得的利养。为什么？"
        "他因利养而自毁，来世也毁——"
        "就像芭蕉、竹子、芦苇，一结果就枯死；就像骡子受孕，母子都丧命。"
        "愚人提婆达多受这些利养，长夜得到不利益的苦。"
        "所以应当这样学：即使有利养生起，也不要染着。」"
        "接着说偈：「芭蕉结果就死，竹芦结实也一样；骡因怀孕丧命，人因贪而自丧。"
        "常做不合义的事，知道再多也免不了愚；善法天天减损，茎枯了根也伤。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN17.35（亦近 AN4.68／SN17.36）；"
        "利养名闻为自害；芭蕉竹芦骡喻据巴利。"
    ),
}

# --- SA 1065 象首／手比丘（法义 SN3.2／SN3.23；汉叙事异）-------------------
SUTTAS["SA_1065"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时舍卫国有手比丘——释氏子——于舍卫命终。"
        "众多比丘乞食闻已，还诣佛所，白言：「手比丘命终，当生何处？云何受生？」",
        "佛告诸比丘：「是手比丘成就三不善法，命终当生恶趣泥犁。"
        "何等为三？谓贪欲、瞋恚、愚痴。此三不善结缚其心，故堕恶趣。」"
        "即说偈言：「贪瞋与愚痴，结缚士夫心；内发还自伤，犹如竹芦实。"
        "无贪无瞋痴，是说为黠慧；内发不自伤，是名为胜出。"
        "是故当离贪，及瞋痴冥心；比丘智慧明，苦尽般涅槃。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时舍卫国有位手比丘——释迦族子弟——在舍卫命终。"
        "许多比丘乞食时听说了，回到佛那里问：「手比丘命终后，会生到哪里？怎样受生？」",
        "佛告诉比丘们：「这位手比丘成就了三种不善法，命终后会生到恶趣地狱。"
        "哪三种？就是贪欲、瞋恚、愚痴。这三种不善结缚他的心，所以堕恶趣。」"
        "接着说偈：「贪、瞋与愚痴，结缚人的心；从内生起反而自伤，就像竹芦结果自毁。"
        "没有贪瞋痴，才叫做聪慧；从内生起却不自伤，才叫做胜过而出离。"
        "所以应当离贪，以及瞋与痴暗；比丘智慧明了，苦尽而般涅槃。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SC 列 SN3.2／SN3.23（resembling）——贪瞋痴自害；"
        "汉叙事为释子手比丘命终堕恶趣（SA-2.4 作象首）；法义据巴利三不善根。"
    ),
}

# --- SA 1066 难陀（peeyāla；SC 列 AN8.9）------------------------------------
SUTTAS["SA_1066"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时舍卫国有难陀比丘命终。"
        "众多比丘乞食闻已，还诣佛所，问其往生。"
        "佛告诸比丘：「是难陀比丘成就贪欲、瞋恚、愚痴三不善法，"
        "结缚于心，命终当生恶趣泥犁。」"
        "即说偈言：「贪瞋与愚痴，结缚士夫心；内发还自伤，犹如竹芦实。"
        "是故当离贪，及瞋痴冥心；比丘智慧明，苦尽般涅槃。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时舍卫国有位难陀比丘命终。"
        "许多比丘乞食时听说了，回到佛那里问起他的往生。"
        "佛告诉比丘们：「这位难陀比丘成就了贪欲、瞋恚、愚痴三种不善法，"
        "结缚于心，命终后会生到恶趣地狱。」"
        "接着说偈：「贪、瞋与愚痴，结缚人的心；从内生起反而自伤，就像竹芦结果自毁。"
        "所以应当离贪，以及瞋与痴暗；比丘智慧明了，苦尽而般涅槃。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：汉唯「如手比丘，难陀修多罗亦如是说」peeyāla；"
        "据 SA_1065 纲补。SC 亦列 AN8.9（根门守护之难陀），与此汉略异——"
        "本批从汉 peeyāla，不改写成 AN8.9。"
        "reconstruction：手比丘三不善／泥犁纲移难陀。"
    ),
}

# --- SA 1067 难陀（SN21.8 Nanda）--------------------------------------------
SUTTAS["SA_1067"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时尊者难陀——佛姨母子——好着好衣，擣治光泽，执持好钵，嬉戏调笑而行。"
        "众多比丘白佛。世尊遣一比丘召之。难陀来，稽首退住。",
        "佛问：「汝实好着好衣、嬉戏调笑而行不？」答言：「实尔。」"
        "佛告难陀：「汝贵姓出家，不应如是。"
        "当念：应作阿练若、乞食、着粪扫衣，常赞粪扫衣，乐处山泽，不顾五欲。」",
        "难陀受教，修阿兰若、乞食、粪扫衣，乐处山泽，不顾爱欲。"
        "世尊即说偈言：「难陀何见汝，修习阿兰若；家家行乞食，身着粪扫衣；"
        "乐处于山泽，不顾于五欲。」",
        "尊者难陀闻佛所说，欢喜奉行。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者难陀——佛的姨母之子——喜欢穿好衣服，擣打得光鲜，拿着好钵，嬉戏调笑地走。"
        "许多比丘禀告佛。世尊派一位比丘去召他。难陀来了，顶礼后站在一旁。",
        "佛问：「你真的喜欢穿好衣服、嬉戏调笑地走吗？」答：「确实如此。」"
        "佛告诉难陀：「你以贵姓出家，不应当这样。"
        "应当想：该住阿兰若、乞食、穿粪扫衣，常称赞粪扫衣，乐于住在山林，不顾五欲。」",
        "难陀受教后，修习阿兰若、乞食、粪扫衣，乐住山林，不顾爱欲。"
        "世尊接着说偈：「难陀，怎么见到你修习阿兰若；挨家挨户乞食，身穿粪扫衣；"
        "乐住于山林，不顾五欲。」",
        "尊者难陀听佛所说，欢喜奉行。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN21.8；"
        "责难陀好衣调笑，教以头陀行（阿兰若、乞食、粪扫衣）。"
    ),
}

# --- SA 1068 窒师／低沙（SN21.9 Tissa）--------------------------------------
SUTTAS["SA_1068"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时尊者低沙自念：「我是世尊姑子兄弟」，故不修恭敬，无所顾录，"
        "亦不畏惧，不堪谏止。"
        "众多比丘白佛。世尊召之。低沙来，稽首退住。",
        "佛问：「汝实作是念，不修恭敬、不堪忍谏不？」答言：「实尔。」"
        "佛告低沙：「汝不应尔。当念：我是世尊姑子兄弟，应修恭敬畏惧，堪忍谏止。」"
        "即说偈言：「善哉汝低沙，离瞋恚为善；莫生瞋恚心，瞋恚者非善。"
        "若能离瞋慢，修行柔软心；然后于我所，修行于梵行。」",
        "低沙比丘闻已，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者低沙自己想：「我是世尊姑姑家的兄弟」，因此不修恭敬，无所顾忌，"
        "也不畏惧，受不了劝谏。"
        "许多比丘禀告佛。世尊召他来。低沙来了，顶礼后站在一旁。",
        "佛问：「你真的这样想，不修恭敬、受不了劝谏吗？」答：「确实如此。」"
        "佛告诉低沙：「你不应当这样。应当想：我是世尊姑姑家的兄弟，更应修恭敬畏惧，能受劝谏。」"
        "接着说偈：「很好啊低沙，离瞋才是善；不要生瞋心，有瞋就不是善。"
        "若能离瞋与慢，修柔软心；然后在我这里，才能修习梵行。」",
        "低沙比丘听完，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN21.9；"
        "汉重「恃亲不恭、不堪谏」；巴利兼「怒责他人反被讥」——以汉叙事为主，"
        "偈据巴利／汉合写：离瞋慢、柔软心、堪谏。"
    ),
}

# --- SA 1069 般阇闻／毘舍佉（SN21.7 Visākha）--------------------------------
SUTTAS["SA_1069"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者毘舍佉般阇梨子于供养堂为众多比丘说法："
        "言辞满足，妙音清彻，句味辩正，随智慧说，听者乐闻，无所依说，显深义，"
        "令诸比丘一心专听。",
        "世尊昼日入定，以天耳闻其说法声，从三昧起，往诣讲堂，于大众前坐，"
        "赞言：「善哉！毘舍佉！汝能为诸比丘如是说法。"
        "当数数如是说，令诸比丘专精敬重、一心乐听，长夜以义饶益，安隐乐住。」"
        "即说偈言：「若不说法者，愚智杂难分；此愚此智慧，无由自显现。"
        "善说清凉法，因说智乃彰；说法为明照，光显大仙幢；"
        "善说为仙幢，法为罗汉幢。」",
        "尊者毘舍佉般阇梨子闻已，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者毘舍佉——般阇梨之子——在供养堂为许多比丘说法："
        "言辞圆满，音声清彻，文句义味正确，随智慧而说，听的人乐意听，不依他而说，显示深义，"
        "使比丘们一心专注地听。",
        "世尊白天入定，用天耳听见说法的声音，从三昧起来，到讲堂大众前坐下，"
        "称赞说：「很好！毘舍佉！你能这样为比丘们说法。"
        "应当常常这样说，使比丘们专精敬重、一心乐听，长夜得到法义的利益，安隐乐住。」"
        "接着说偈：「若不说法，愚与智混杂难分；谁愚谁智，无从自己显现。"
        "善说清凉法，智慧因说而彰显；说法是明灯，光显大仙之幢；"
        "善说是仙幢，法是罗汉之幢。」",
        "尊者毘舍佉般阇梨子听完，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN21.7（亦 AN4.48）；"
        "汉住舍卫，巴利多作毗舍离——处所从汉；赞善说法显愚智。"
    ),
}

# --- SA 1070 年少（SN21.4 Nava）---------------------------------------------
SUTTAS["SA_1070"] = {
    "lit": [
        OPEN_JET_LIT,
        "时诸比丘于供养堂共作衣。一年少者出家未久，不欲相助。"
        "白佛已，世尊问：「汝实不欲助作衣耶？」答：「随力当助。」",
        "佛知彼意，告诸比丘：「莫轻是年少。所以者何？彼已得四禅，现法乐住，不勤而得；"
        f"本所出家，精勤修习，现法作证：『{AWAKEN_LIT}』」"
        "即说偈言：「非劣薄德者，能正向涅槃；此贤虽年少，已得上士处。"
        "离欲心解脱，涅槃不复生；持此最后身，摧伏众魔军。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时比丘们在供养堂一起作衣。有位年少比丘出家不久，不想帮忙。"
        "禀告佛后，世尊问：「你真的不想帮忙作衣吗？」答：「我会尽力量帮忙。」",
        "佛知道他的心意，告诉比丘们：「不要轻视这位年少的。为什么？他已经证得四禅，"
        "能在现法中安乐而住，不费力就得到；"
        f"他出家所求的，精勤修习后，已在现法中作证：『{AWAKEN_MOD}』」"
        "接着说偈：「不是下劣薄德的人，就能正向涅槃；这位贤者虽然年少，已得上士之位。"
        "离欲而心解脱，涅槃不再受生；持此最后之身，摧伏众魔军。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN21.4；"
        "年少不营作衣，实已得四禅现法乐住／漏尽；莫妄轻量。"
        "汉「四增心法」据巴利作四禅（jhāna）。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {
    "SA_1051": "high",
    "SA_1052": "high",
    "SA_1053": "high",
    "SA_1054": "high",
    "SA_1055": "high",
    "SA_1056": "high",
    "SA_1057": "high",
    "SA_1058": "high",
    "SA_1059": "high",
    "SA_1060": "medium",
    "SA_1061": "medium",
    "SA_1062": "high",
    "SA_1063": "high",
    "SA_1064": "high",
    "SA_1065": "high",
    "SA_1066": "medium",
    "SA_1067": "high",
    "SA_1068": "high",
    "SA_1069": "high",
    "SA_1070": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1061": "非法对举 peeyāla → 十不善／十善系列纲",
    "SA_1066": "「如手比丘」→ SA_1065 三不善／泥犁纲移难陀",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

GOLD: dict[str, dict[str, str]] = {}
for _rid, _s in SUTTAS.items():
    lit_paras = _s["lit"]
    mod_paras = _s["mod"]
    assert len(lit_paras) == len(mod_paras), f"{_rid} lit/mod paragraph mismatch"
    GOLD[_rid] = {
        "kumarajiva_style_text": "\n".join(lit_paras),
        "modern_psychology_text": "\n".join(mod_paras),
        "notes": _s["notes"],
    }

assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
assert set(RECONSTRUCTED) <= set(GOLD)
assert set(GOLD) == {f"SA_{i}" for i in BATCH}


def _snapshot(rec: dict) -> str:
    return json.dumps(
        {
            "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
            "modern_psychology_text": rec.get("modern_psychology_text"),
            "notes": rec.get("notes"),
            "review_status": rec.get("review_status"),
            "confidence": rec.get("confidence"),
        },
        ensure_ascii=False,
    )


def main() -> None:
    aligned = ROOT / "data" / "aligned" / "raw_aligned_data.json"
    out = ROOT / "data" / "translated" / "final_translated_data.json"
    gold_dir = ROOT / "data" / "golden"
    gold_dir.mkdir(parents=True, exist_ok=True)

    if out.exists():
        records = json.loads(out.read_text(encoding="utf-8"))
    else:
        records = json.loads(aligned.read_text(encoding="utf-8"))

    # Boundary: SA_1050 must remain untouched
    boundary_id = "SA_1050"
    boundary_before = None
    for rec in records:
        if rec["id"] == boundary_id:
            boundary_before = _snapshot(rec)
            break
    assert boundary_before is not None, f"{boundary_id} missing from records"

    # Snapshot SA_1071+ to assert untouched
    after_before = {
        rec["id"]: _snapshot(rec)
        for rec in records
        if rec["id"].startswith("SA_")
        and rec["id"][3:].isdigit()
        and int(rec["id"][3:]) >= 1071
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

    # Assert SA_1050 unchanged
    for rec in merged:
        if rec["id"] == boundary_id:
            assert boundary_before == _snapshot(rec), f"{boundary_id} must remain untouched"
            break

    # Assert SA_1071+ unchanged
    for rid, before in after_before.items():
        for rec in merged:
            if rec["id"] == rid:
                assert before == _snapshot(rec), f"{rid} (SA_1071+) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1051-1070.json").write_text(
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
    continuous = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in BATCH
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
        # 厌故离贪 positive check not required here (no 厌离 formula in this batch)

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1051–SA_1070 only)")
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
    print(f"continuous_gold_SA_1051–1070={continuous}")
    print(f"SA_1050_untouched=True")
    print(f"SA_1071+_untouched=True (n={len(after_before)})")
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
