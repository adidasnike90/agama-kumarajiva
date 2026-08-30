#!/usr/bin/env python3
"""Retranslate SA 791–810（圣道分末–安那般那念相应）→ merge.

本批二十经：
791–793 邪正／顺流逆流（十不善／八邪正；无专 SN 或弱平行）
794–800 沙门／婆罗门／梵行 SN45.35–40（卷标自 797 或作安那般那，法义仍属道品）
801 饶益 AN5.98（五法饶益安那般那念）
802–803 一明 SN54.1（略／广十六行）
804 断觉想 SN54.2（及果利 peyyāla）
805 阿黎瑟吒 SN54.6｜806 罽宾那 SN54.7
807 一奢能伽罗 SN54.11｜808 迦摩 SN54.12
809 福利等 SN54.9｜810 金刚 SN54.13

信：794–800 以 SN45 为准；801+ 以 SN54／AN 为准；卷标错置不改法义归属。
    peyyāla／交叉指示补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_791–810；不触碰 SA_771–790（并行批次）；
      断言 SA_790 不变（若尚未 gold 则 SA_770，再否则 SA_730）。
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

CLOSE_AN_LIT = "佛说此经已，尊者阿难闻佛所说，欢喜奉行。"
CLOSE_AN_MOD = "佛说完这部经，尊者阿难听佛所说，欢喜奉行。"

EIGHT_LIT = "正见、正志、正语、正业、正命、正精进、正念、正定"
EIGHT_MOD = "正见、正志、正语、正业、正命、正精进、正念、正定"
EIGHT_WRONG_LIT = "邪见、邪志、邪语、邪业、邪命、邪精进、邪念、邪定"
EIGHT_WRONG_MOD = "邪见、邪志、邪语、邪业、邪命、邪精进、邪念、邪定"

FOUR_FRUIT_LIT = "须陀洹果、斯陀含果、阿那含果、阿罗汉果"
FOUR_FRUIT_MOD = "须陀洹果、斯陀含果、阿那含果、阿罗汉果"

SEVEN_BOJ_LIT = "念觉支、择法觉支、精进觉支、喜觉支、轻安觉支、定觉支、舍觉支"
SEVEN_BOJ_MOD = "念觉支、择法觉支、精进觉支、喜觉支、轻安觉支、定觉支、舍觉支"

NISSAYA_LIT = "依远离、依离欲、依灭、向于舍"
NISSAYA_MOD = "依于远离、依于离欲、依于灭、而趋向舍"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

# 坐前方便（汉传常有；SN54 多直入林树空静）
SIT_PREP_LIT = (
    "若比丘依止聚落、城邑，晨朝著衣持钵入村乞食，善护其身，守诸根门，善系心住。"
    "乞食已还，举衣钵、洗足已，入林中闲房树下，或空露地，端身正坐，系念在前。"
    "断世贪爱，离欲清净；瞋恚、昏沉睡眠、掉举后悔、疑皆断，度诸疑惑，于善法心得决定。"
    "远离五盖——于心令慧力羸、为障碍分、不趣涅槃者。"
)
SIT_PREP_MOD = (
    "如果比丘依止聚落、城邑，清晨著衣持钵入村乞食，善护自身，守住根门，善系其心。"
    "乞食回来，收衣钵、洗足后，入林中闲房树下，或空露地，端身正坐，把念安住在前。"
    "断除世间贪爱，离欲清净；瞋恚、昏沉睡眠、掉举后悔、疑都断除，度过疑惑，于善法心得决定。"
    "远离五盖——那些使心中慧力衰弱、成障碍分、不趋向涅槃的。"
)

# SN54 十六行（末四：无常／离贪／灭／舍遣；据巴利校正汉「断、無欲、灭」）
SIXTEEN_LIT = (
    "正念而入息，正念而出息。"
    "入息长，如实知『入息长』；出息长，如实知『出息长』。"
    "入息短，如实知『入息短』；出息短，如实知『出息短』。"
    "学『觉知一切身而入息』，学『觉知一切身而出息』；"
    "学『止息身行而入息』，学『止息身行而出息』。"
    "学『觉知喜而入息』，学『觉知喜而出息』；"
    "学『觉知乐而入息』，学『觉知乐而出息』；"
    "学『觉知心行而入息』，学『觉知心行而出息』；"
    "学『止息心行而入息』，学『止息心行而出息』。"
    "学『觉知心而入息』，学『觉知心而出息』；"
    "学『悦心而入息』，学『悦心而出息』；"
    "学『定心而入息』，学『定心而出息』；"
    "学『解脱心而入息』，学『解脱心而出息』。"
    "学『观察无常而入息』，学『观察无常而出息』；"
    "学『观察离贪而入息』，学『观察离贪而出息』；"
    "学『观察灭而入息』，学『观察灭而出息』；"
    "学『观察舍遣而入息』，学『观察舍遣而出息』。"
)
SIXTEEN_MOD = (
    "正念地入息，正念地出息。"
    "入息长，如实知道『入息长』；出息长，如实知道『出息长』。"
    "入息短，如实知道『入息短』；出息短，如实知道『出息短』。"
    "学着『觉知整个身体而入息』，学着『觉知整个身体而出息』；"
    "学着『让身行止息而入息』，学着『让身行止息而出息』。"
    "学着『觉知喜而入息』，学着『觉知喜而出息』；"
    "学着『觉知乐而入息』，学着『觉知乐而出息』；"
    "学着『觉知心行而入息』，学着『觉知心行而出息』；"
    "学着『让心行止息而入息』，学着『让心行止息而出息』。"
    "学着『觉知心而入息』，学着『觉知心而出息』；"
    "学着『使心喜悦而入息』，学着『使心喜悦而出息』；"
    "学着『使心入定而入息』，学着『使心入定而出息』；"
    "学着『使心解脱而入息』，学着『使心解脱而出息』。"
    "学着『观察无常而入息』，学着『观察无常而出息』；"
    "学着『观察离贪而入息』，学着『观察离贪而出息』；"
    "学着『观察灭而入息』，学着『观察灭而出息』；"
    "学着『观察舍遣而入息』，学着『观察舍遣而出息』。"
)

SIXTEEN_SHORT_LIT = f"如前广说，乃至{SIXTEEN_LIT}"
SIXTEEN_SHORT_MOD = f"如同前面详细说过的，一直到{SIXTEEN_MOD}"

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 791 邪正（十不善／十善趣道）------------------------------------------
SUTTAS["SA_791"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有邪、有邪道，有正、有正道。谛听，善思，当为汝说。"
        "何等为邪？谓地狱、畜生、饿鬼。"
        "何等为邪道？谓杀生、不与取、邪淫、妄语、两舌、恶口、绮语、贪、瞋、邪见。"
        "何等为正？谓人、天、涅槃。"
        "何等为正道？谓不杀生、不与取、不邪淫、不妄语、不两舌、不恶口、不绮语、无贪、无瞋、正见。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有邪、有邪道，有正、有正道。仔细听，好好想，我当为你们说。"
        "什么是邪？就是地狱、畜生、饿鬼。"
        "什么是邪道？就是杀生、不与取、邪淫、妄语、两舌、恶口、绮语、贪、瞋、邪见。"
        "什么是正？就是人、天、涅槃。"
        "什么是正道？就是不杀生、不与取、不邪淫、不妄语、不两舌、不恶口、不绮语、无贪、无瞋、正见。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：近 SN45.21 Micchatta／十业道框架；"
        "汉以三恶趣／人天涅槃配十不善／十善，非八支道本经；不杀等作「不与取」以合早期术语。"
    ),
}

# --- SA 792 邪正（五无间为恶趣道；peyyāla）----------------------------------
SUTTAS["SA_792"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有邪、有邪道，有正、有正道。谛听，善思，当为汝说。"
        "何等为邪？谓地狱、畜生、饿鬼。"
        "何等为恶趣道？谓杀父、杀母、杀阿罗汉、破和合僧、恶意出佛身血。"
        "何等为正？谓人、天、涅槃。"
        "何等为正道？谓不杀生、不与取、不邪淫、不妄语、不两舌、不恶口、不绮语、无贪、无瞋、正见。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有邪、有邪道，有正、有正道。仔细听，好好想，我当为你们说。"
        "什么是邪？就是地狱、畜生、饿鬼。"
        "什么是恶趣道？就是杀父、杀母、杀阿罗汉、破和合僧、恶意出佛身血。"
        "什么是正？就是人、天、涅槃。"
        "什么是正道？就是不杀生、不与取、不邪淫、不妄语、不两舌、不恶口、不绮语、无贪、无瞋、正见。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：peyyāla 据 SA_791 补全；"
        "差别在「恶趣道」举五无间业。reconstruction。"
    ),
}

# --- SA 793 顺流逆流 ---------------------------------------------------------
SUTTAS["SA_793"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有顺流道，有逆流道。谛听，善思，当为汝说。"
        f"何等为顺流道？谓{EIGHT_WRONG_LIT}。"
        f"何等为逆流道？谓{EIGHT_LIT}。」",
        CLOSE_BH_LIT,
        "如顺流、逆流，如是退道与胜道、下道与上道，及余道迹名目，亦如上说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有顺流道，有逆流道。仔细听，好好想，我当为你们说。"
        f"什么是顺流道？就是{EIGHT_WRONG_MOD}。"
        f"什么是逆流道？就是{EIGHT_MOD}。」",
        CLOSE_BH_MOD,
        "如同顺流、逆流，退道与胜道、下道与上道，以及其他道迹的名称，也都如上所说。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：八邪／八正配顺流（随生死）／逆流（逆生死）；"
        "末句 peyyāla 压缩诸异名。reconstruction：末段道迹异名。"
    ),
}

# --- SA 794 沙门及沙门法（SN45.36 系）----------------------------------------
SUTTAS["SA_794"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「我当说沙门与沙门法。谛听。"
        f"沙门法者，八圣道支——{EIGHT_LIT}。"
        "成就此道者，是名沙门。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「我要说沙门和沙门法。仔细听。"
        f"沙门法，就是八圣道支——{EIGHT_MOD}。"
        "成就这条道的人，叫做沙门。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.36 Sāmañña（沙门法／沙门义之姊妹；"
        "本经举「沙门」为成就道者，义近 SN 之 sāmañña 实践面）。"
        "卷属圣道分；与后「安那般那」卷标错置无涉。"
    ),
}

# --- SA 795 沙门法沙门义（SN45.36）-------------------------------------------
SUTTAS["SA_795"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有沙门法、沙门义。"
        f"何等为沙门法？谓八圣道——{EIGHT_LIT}。"
        "何等为沙门义？谓贪欲永尽，瞋恚、愚痴永尽，一切烦恼永尽，是名沙门义。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有沙门法、沙门义。"
        f"什么是沙门法？就是八圣道——{EIGHT_MOD}。"
        "什么是沙门义？就是贪欲永尽，瞋恚、愚痴永尽，一切烦恼永尽，这叫做沙门义。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.36；"
        "sāmañña＝八支道，sāmaññattha＝贪瞋痴尽（沙门义／沙门义利）。"
    ),
}

# --- SA 796 沙门法沙门果（SN45.35）-------------------------------------------
SUTTAS["SA_796"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有沙门法及沙门果。谛听，善思，当为汝说。"
        f"何等为沙门法？谓八圣道——{EIGHT_LIT}。"
        f"何等为沙门果？谓{FOUR_FRUIT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有沙门法以及沙门果。仔细听，好好想，我当为你们说。"
        f"什么是沙门法？就是八圣道——{EIGHT_MOD}。"
        f"什么是沙门果？就是{FOUR_FRUIT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.35 Sāmaññaphala；"
        "法＝八支，果＝四沙门果。"
    ),
}

# --- SA 797 沙门法沙门果（广；仍 SN45，非 SN54）-------------------------------
SUTTAS["SA_797"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有沙门法及沙门果。谛听，善思，当为汝说。"
        f"何等为沙门法？谓八圣道——{EIGHT_LIT}。"
        f"何等为沙门果？谓{FOUR_FRUIT_LIT}。"
        "何等为须陀洹果？谓三结断。"
        "何等为斯陀含果？谓三结断，贪、瞋、痴薄。"
        "何等为阿那含果？谓五下分结尽。"
        "何等为阿罗汉果？谓贪、瞋、痴永尽，一切烦恼永尽。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有沙门法以及沙门果。仔细听，好好想，我当为你们说。"
        f"什么是沙门法？就是八圣道——{EIGHT_MOD}。"
        f"什么是沙门果？就是{FOUR_FRUIT_MOD}。"
        "什么是须陀洹果？就是三结已断。"
        "什么是斯陀含果？就是三结已断，贪、瞋、痴已薄。"
        "什么是阿那含果？就是五下分结已尽。"
        "什么是阿罗汉果？就是贪、瞋、痴永尽，一切烦恼永尽。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.35 扩说四果内涵；"
        "大正卷标入「安那般那念相应」，法义仍属圣道／沙门果，不以 SN54 强配。"
        "恚→瞋以合三毒定型。"
    ),
}

# --- SA 798 沙门法、沙门、沙门义（SN45.36 合）--------------------------------
SUTTAS["SA_798"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有沙门法、沙门、沙门义。谛听，善思，当为汝说。"
        f"何等为沙门法？谓八圣道——{EIGHT_LIT}。"
        "何等为沙门？谓成就此法者。"
        "何等为沙门义？谓贪欲永断，瞋恚、痴永断，一切烦恼永断。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有沙门法、沙门、沙门义。仔细听，好好想，我当为你们说。"
        f"什么是沙门法？就是八圣道——{EIGHT_MOD}。"
        "什么是沙门？就是成就此法的人。"
        "什么是沙门义？就是贪欲永断，瞋恚、痴永断，一切烦恼永断。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.36；"
        "合「法／人／义」三句，与 794–795 互文。"
    ),
}

# --- SA 799 沙门果（peyyāla）-------------------------------------------------
SUTTAS["SA_799"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有沙门果。"
        f"何等为沙门果？谓{FOUR_FRUIT_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有沙门果。"
        f"什么是沙门果？就是{FOUR_FRUIT_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.35 果句；"
        "汉「如上说」peyyāla，据 796／SN 补独立短经。reconstruction。"
    ),
}

# --- SA 800 婆罗门／梵行（SN45.37–40 peyyāla）--------------------------------
SUTTAS["SA_800"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「如说沙门法、沙门、沙门义、沙门果，如是婆罗门法、婆罗门、婆罗门义、婆罗门果亦如是说。"
        f"何等为婆罗门法？谓八圣道——{EIGHT_LIT}。"
        "何等为婆罗门？谓成就此法者。"
        "何等为婆罗门义？谓贪欲永尽，瞋恚、愚痴永尽，一切烦恼永尽。"
        f"何等为婆罗门果？谓{FOUR_FRUIT_LIT}。"
        "梵行法、梵行者、梵行义、梵行果，亦如上说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「如同所说的沙门法、沙门、沙门义、沙门果，婆罗门法、婆罗门、婆罗门义、婆罗门果也这样说。"
        f"什么是婆罗门法？就是八圣道——{EIGHT_MOD}。"
        "什么是婆罗门？就是成就此法的人。"
        "什么是婆罗门义？就是贪欲永尽，瞋恚、愚痴永尽，一切烦恼永尽。"
        f"什么是婆罗门果？就是{FOUR_FRUIT_MOD}。"
        "梵行法、梵行者、梵行义、梵行果，也如上所说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.37–40 Brahmañña／Brahmacariya 系列；"
        "汉仅交叉指示，据 SN／前沙门诸经补纲。reconstruction。"
    ),
}

# --- SA 801 饶益（AN5.98）----------------------------------------------------
SUTTAS["SA_801"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「修安那般那念，有五法能大饶益。何等五？"
        "一者戒净：住波罗提木叉，威仪具足，微罪生畏，受持学处。"
        "二者少欲：事少、务少。"
        "三者食知量：多少得中，不因食起贪求，精勤思惟。"
        "四者初夜后夜，不眠著，精勤思惟。"
        "五者闲林静处，离诸愦闹。"
        "比丘！此五法，于修入出息念，多所饶益。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「修习入出息念，有五种法能大大饶益。哪五种？"
        "第一，戒清净：安住波罗提木叉，威仪具足，对微细罪也生怖畏，受持学处。"
        "第二，少欲：事情少、事务少。"
        "第三，饮食知量：多少适中，不因饮食起贪求，精勤思惟。"
        "第四，初夜后夜不贪睡，精勤思惟。"
        "第五，在空闲林野静处，远离愦闹。"
        "比丘们！这五种法，对修习入出息念，很有饶益。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN5.98 Ānāpānāsati（五法饶益）；"
        "兼参 AN5.96–97。安那般那念＝入出息念；学戒→学处。"
        "自此真正进入安那般那法义（前 797–800 虽卷标误入，法义属道品）。"
    ),
}

# --- SA 802 一明（略；SN54.1）------------------------------------------------
SUTTAS["SA_802"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「汝等当修入出息念。"
        "修习既久，身息、心息；有觉有观，其心寂静纯一，明了之想亦得满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「你们应当修习入出息念。"
        "长久修习之后，身体止息、内心止息；有觉有观，心寂静而纯一，明了之想也能满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：略说，义承 SN54.1 Ekadhamma／汉「一明」；"
        "广说见 SA_803。觉观＝vitakka／vicāra；明分想＝明了观想分。"
    ),
}

# --- SA 803 一明（广十六行；SN54.1）------------------------------------------
SUTTAS["SA_803"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「当修安那般那念。"
        "若比丘修习安那般那念，多修习者，得身心止息，有觉有观，寂灭纯一，明分之想修习满足。"
        "云何修习安那般那念，多修习已，身心止息，有觉有观，寂灭纯一，明分之想修习满足？」",
        f"{SIT_PREP_LIT}{SIXTEEN_LIT}"
        "是名修安那般那念：身止息、心止息，有觉有观，寂灭纯一，明分之想修习满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「应当修习入出息念。"
        "如果比丘修习入出息念，多多修习，便得身心止息，有觉有观，寂灭而纯一，明了之想修习满足。"
        "怎样修习入出息念，多多修习之后，身心止息，有觉有观，寂灭纯一，明了之想修习满足呢？」",
        f"{SIT_PREP_MOD}{SIXTEEN_MOD}"
        "这叫做修习入出息念：身止息、心止息，有觉有观，寂灭纯一，明了之想修习满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN54.1；兼 MN118 十六行。"
        "据巴利校正末四：无常、离贪（virāga）、灭、舍遣（paṭinissagga）；"
        "汉「观察断／無欲／灭」及「内息／外息」之生硬对译已改。"
        "坐前五盖为汉传叙事框架，SN 直入林树空静；并存而十六行以 SN 为准。"
    ),
}

# --- SA 804 断觉想（SN54.2 + 果利 peyyāla）-----------------------------------
SUTTAS["SA_804"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「当修安那般那念。安那般那念修习多修习者，能断诸觉想。"
        f"云何修习多修习能断诸觉想？{SIT_PREP_LIT}{SIXTEEN_LIT}"
        "是名安那般那念修习多修习，能断诸觉想。」",
        CLOSE_BH_LIT,
        "如断觉想，如是心不倾动，得大果大福利，得甘露、究竟甘露，"
        "得二果、四果、七果——一一经亦如上十六行说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「应当修习入出息念。入出息念修习多多修习，就能断除各种觉想。"
        f"怎样修习多多修习就能断除各种觉想？{SIT_PREP_MOD}{SIXTEEN_MOD}"
        "这叫做入出息念修习多多修习，能断除各种觉想。」",
        CLOSE_BH_MOD,
        "如同断除觉想，心不倾动、得大果大福利、得甘露与究竟甘露、"
        "得二果、四果、七果——每一部经也都按上面的十六行来说明。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN54.2；觉想≈vitakka（寻）。"
        "末段果利异名 peyyāla，据 SN54.3–5 等纲补。reconstruction：果利异名段。"
    ),
}

# --- SA 805 阿黎瑟吒（SN54.6）------------------------------------------------
SUTTAS["SA_805"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「如我所说安那般那念，汝等修习否？」",
        "时有比丘名阿梨瑟吒，于众中坐，即从座起，整衣服，为佛作礼，右膝著地，合掌白佛言："
        "「世尊！世尊所说安那般那念，我已修习。」",
        "佛告阿梨瑟吒：「汝云何修习我所说安那般那念？」",
        "比丘白佛：「世尊！于过去诸欲，我已断欲贪；于未来诸欲，不生欣乐；"
        "于内外诸法违逆之想，善能除灭。我正念入息，正念出息——我如是修世尊所说安那般那念。」",
        "佛告阿梨瑟吒：「汝实修我所说安那般那念，非不修。"
        "然更有胜妙，过汝所修。何等胜妙？"
        f"{SIT_PREP_LIT}{SIXTEEN_LIT}"
        "阿梨瑟吒！此则胜妙，过汝所修安那般那念。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「像我所说的入出息念，你们修习了吗？」",
        "当时有位比丘名叫阿梨瑟吒，在大众中坐着，就从座位起来，整理衣服，向佛作礼，右膝著地，合掌对佛说："
        "「世尊！世尊所说的入出息念，我已经修习了。」",
        "佛告诉阿梨瑟吒：「你怎样修习我所说的入出息念？」",
        "比丘对佛说：「世尊！对过去的各种欲，我已断除欲贪；对未来的各种欲，不生欣乐；"
        "对内外诸法的违逆之想，也能妥善除灭。我正念入息，正念出息——我这样修世尊所说的入出息念。」",
        "佛告诉阿梨瑟吒：「你确实在修我所说的入出息念，并不是不修。"
        "然而还有更殊胜巧妙的，超过你所修的。什么更殊胜？"
        f"{SIT_PREP_MOD}{SIXTEEN_MOD}"
        "阿梨瑟吒！这才更殊胜，超过你所修的入出息念。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN54.6 Ariṭṭha；"
        "据巴利校正自述：弃过去欲贪、除未来欲贪、灭内外违逆想，再正念出入息；"
        "汉「过去诸行不顾念」等过宽，已收束为欲贪／违逆想。十六行满相为「胜妙过其上」。"
    ),
}

# --- SA 806 罽宾那（SN54.7）--------------------------------------------------
SUTTAS["SA_806"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊晨朝著衣持钵，入舍卫城乞食。食已还精舍，举衣钵、洗足已，"
        "持尼师檀入安陀林，坐一树下，昼日禅思。",
        "时尊者罽宾那亦晨朝乞食已，入安陀林，于树下坐禅，去佛不远，"
        "正身不动，身心正直，住胜妙住。",
        "尔时众多比丘晡时从禅觉，往诣佛所，稽首礼足，退坐一面。",
        "佛告诸比丘：「汝等见尊者罽宾那不？去我不远，正身端坐，身心不动，住胜妙住。」",
        "诸比丘白佛：「世尊！我等数见彼尊者正身端坐，善摄其身，不倾不动，专心胜妙。」",
        "佛告诸比丘：「若比丘修习三昧，身心安住，不倾不动，住胜妙住，"
        "得此三昧，不待勤苦方便，随欲即得。」",
        "诸比丘白佛：「何等三昧，令比丘身心不动，住胜妙住？」",
        "佛告诸比丘：「若比丘依止聚落，晨朝乞食已，还坐林中闲房或露地，"
        f"思惟系念，{SIXTEEN_LIT}"
        "是名三昧。比丘如是端坐思惟，身心不动，住胜妙住。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊清晨著衣持钵，入舍卫城乞食。吃完回到精舍，收衣钵、洗足后，"
        "拿着坐具进入安陀林，坐在一棵树下，白天禅思。",
        "当时尊者罽宾那也清晨乞食完毕，进入安陀林，在树下坐禅，离佛不远，"
        "身体端正不动，身心正直，安住在殊胜微妙的住中。",
        "那时许多比丘傍晚从禅修中出来，来到佛所，叩头礼足，坐在一边。",
        "佛告诉比丘们：「你们看见尊者罽宾那了吗？离我不远，端身正坐，身心不动，安住胜妙。」",
        "比丘们对佛说：「世尊！我们多次看见那位尊者端身正坐，善摄身体，不倾斜不动摇，专心在胜妙中。」",
        "佛告诉比丘们：「如果比丘修习三昧，身心安住，不倾斜不动摇，安住胜妙，"
        "得到这种三昧，不必苦苦用功，随欲就能得到。」",
        "比丘们对佛说：「是什么三昧，能使比丘身心不动，安住胜妙？」",
        "佛告诉比丘们：「如果比丘依止聚落，清晨乞食回来，坐在林中闲房或露地，"
        f"系念思惟，{SIXTEEN_MOD}"
        "这叫做那种三昧。比丘这样端坐思惟，身心不动，安住胜妙。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN54.7 Kappina；"
        "不动胜住＝安那般那三昧；十六行据 SN 补「乃至」。"
    ),
}

# --- SA 807 一奢能伽罗（SN54.11）---------------------------------------------
SUTTAS["SA_807"] = {
    "lit": [
        "如是我闻：一时，佛住一奢能伽罗林中。",
        "尔时世尊告诸比丘：「我欲三月坐禅，诸比丘勿复往来，唯除送食比丘及布萨时。」"
        "作是语已，即三月坐禅，无一比丘敢往来者，唯除送食及布萨时。",
        "三月过已，世尊从禅觉，于比丘僧前坐，告诸比丘："
        "「若诸外道出家来问：『沙门瞿昙于三月中云何坐禅？』"
        "汝应答言：『如来三月以安那般那念坐禅而住。』"
        "所以者何？我于此三月多住安那般那念："
        f"{SIXTEEN_LIT}"
        "我悉知已，作是念：『此犹是粗住；我今于此止息已，当入更微细之住。』"
        "息粗住已，即入微细思惟，多住而住。」",
        "「时有三天子，色相殊妙，过夜来至我所。"
        "一天子言：『沙门瞿昙，时已至。』"
        "一天子言：『非时至，是时将至。』"
        "第三天子言：『非为时至，亦非时将至；此则修住，是阿罗汉寂灭耳。』」",
        "佛告诸比丘：「若有正说——圣住、天住、梵住、学住、无学住、如来住；"
        "学人未得当得、未到当到、未证当证；无学人现法乐住——"
        "谓安那般那念，此则正说。"
        "所以者何？安那般那念者，是圣住、天住、梵住，乃至无学现法乐住。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在一奢能伽罗林中。",
        "那时世尊告诉比丘们：「我想要三月坐禅，比丘们不要再往来，只除送食的比丘和布萨的时候。」"
        "说完这话，就三月坐禅，没有一个比丘敢来往，只除送食和布萨时。",
        "三月过后，世尊从禅修中出来，在比丘僧前坐下，告诉比丘们："
        "「如果有外道出家人来问：『沙门瞿昙在这三个月里怎样坐禅？』"
        "你们应当回答：『如来三个月以入出息念坐禅而住。』"
        "为什么？我在这三个月里多多安住入出息念："
        f"{SIXTEEN_MOD}"
        "我都知道了，心中想：『这还是粗的安住；我现在把这止息后，应当进入更微细的安住。』"
        "止息粗住之后，就进入微细思惟，多多安住。」",
        "「当时有三位天子，色相非常殊妙，过了夜来到我这里。"
        "一位天子说：『沙门瞿昙，时候到了。』"
        "一位天子说：『不是时候到了，是时候将到。』"
        "第三位天子说：『既不是时候到了，也不是时候将到；这就是修住，是阿罗汉的寂灭啊。』」",
        "佛告诉比丘们：「如果有人正确地说——圣住、天住、梵住、学住、无学住、如来住；"
        "学人未得的当得、未到的当到、未证的当证；无学人现法乐住——"
        "那就是入出息念，这样说才正确。"
        "为什么？入出息念就是圣住、天住、梵住，乃至无学的现法乐住。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN54.11 Icchānaṅgala；"
        "汉「二月」据 SN 作雨安居三月校正。三天子问答为汉本特有叙事，保留；"
        "圣／天／梵／如来住与学无学现法乐住据 SN 厘义。"
    ),
}

# --- SA 808 迦摩（SN54.12）---------------------------------------------------
SUTTAS["SA_808"] = {
    "lit": [
        "如是我闻：一时，佛住迦毗罗卫尼拘律树园中。",
        "尔时释氏摩诃男诣尊者迦磨比丘所，礼足已，退坐一面，问言："
        "「云何？尊者迦磨！学住者即是如来住耶？为学住异、如来住异？」",
        "迦磨答言：「摩诃男！学住异、如来住异。"
        "学住者，断五盖而多住；"
        "如来住者，于五盖已断已知，断其根本，如截多罗树头，更不复生，于未来世成不生法。」",
        "「一时世尊住一奢能伽罗林中，告诸比丘：『我欲三月坐禅……』广说如前，"
        "乃至『安那般那念是圣住、天住、梵住，学无学现法乐住。』"
        "以是故知，摩诃男！学住异、如来住异。」",
        "释氏摩诃男闻已欢喜，从座起去。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在迦毗罗卫尼拘律树园中。",
        "那时释迦族的摩诃男来到尊者迦磨比丘那里，礼足后坐在一边，问道："
        "「怎么样？尊者迦磨！学人的住就是如来的住吗？还是学住不同、如来住不同？」",
        "迦磨回答：「摩诃男！学住不同，如来住也不同。"
        "学住，是断除五盖而多多安住；"
        "如来住，是对五盖已经断尽、已经了知，断其根本，如同截断多罗树头，不再生长，于未来世成为不生之法。」",
        "「有一次世尊住在一奢能伽罗林中，告诉比丘们：『我想要三月坐禅……』详细如同前面所说，"
        "一直到『入出息念是圣住、天住、梵住，以及学人与无学人的现法乐住。』"
        "因为这个缘故知道，摩诃男！学住不同，如来住也不同。」",
        "释迦族的摩诃男听完欢喜，从座位起来离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN54.12；"
        "学住＝断五盖而住；如来住＝五盖根本永断。交叉引用 SA_807／SN54.11。"
        "迦毗罗越→迦毗罗卫。"
    ),
}

# --- SA 809 福利等（SN54.9 不净→安那般那）-----------------------------------
SUTTAS["SA_809"] = {
    "lit": [
        "如是我闻：一时，佛住金刚聚落跋求摩河侧萨罗梨林中。",
        "尔时世尊为诸比丘说不净观，赞叹不净观言："
        "「诸比丘修不净观，多修习者，得大果大福利。」",
        "时诸比丘修不净观已，极厌患身，或以刀自杀，或服毒药，或绳自绞、投岩，或令余比丘杀。",
        "有一比丘极生厌患，至鹿林梵志子所，语言：「贤首！汝能杀我者，衣钵属汝。」"
        "鹿林梵志子即杀彼比丘。持刀至跋求摩河边洗刀时，有魔天住于空中赞言："
        "「善哉！善哉！贤首！汝得无量功德，能令沙门释子持戒有德——"
        "未度者度，未脱者脱，未苏息者令得苏息，未涅槃者令得涅槃；衣钵杂物悉属汝。」",
        "鹿林梵志子闻已，增恶邪见，手执利刀，循诸房舍、经行处、禅房，见比丘便言："
        "「何等沙门持戒有德，未度者我能令度，未脱者令脱……？」"
        "时有厌患身者出房，求彼令度；梵志子即以利刀杀害，次第乃至杀六十人。",
        "尔时世尊至十五日说戒时，于众僧前坐，问尊者阿难："
        "「何因何缘，诸比丘转少、转减、转尽？」",
        "阿难白佛：「世尊为诸比丘说修不净观并赞叹之；诸比丘修已极厌患身……」"
        "广说乃至「杀六十比丘。以是因缘，僧众转少。"
        "唯愿世尊更说余法，令诸比丘闻已勤修智慧，乐受正法，乐住正法。」",
        "佛告阿难：「是故我今说微细住：随顺开觉，已起、未起恶不善法速令休息——"
        "如天大雨，能令已起、未起尘垢休息。"
        "何等为微细住多修习，能令已起、未起恶不善法休息？谓安那般那念住。」",
        "阿难白佛：「云何修习安那般那念住，能如是休息恶不善法？」",
        f"佛告阿难：「{SIT_PREP_LIT}{SIXTEEN_LIT}」",
        CLOSE_AN_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在金刚聚落跋求摩河侧的萨罗梨林中。",
        "那时世尊为比丘们说不净观，并赞叹不净观说："
        "「比丘们修不净观，多多修习，能得大果大福利。」",
        "当时比丘们修不净观后，对身体极其厌患，有的用刀自杀，有的服毒药，有的用绳子自绞、投岩，有的让别的比丘杀害。",
        "有一位比丘极度厌患，来到鹿林梵志子那里，说：「贤首！你若能杀我，衣钵归你。」"
        "鹿林梵志子就杀了那位比丘。拿着刀到跋求摩河边洗刀时，有魔天在空中称赞说："
        "「好啊！好啊！贤首！你得到无量功德，能让沙门释子中持戒有德的——"
        "未度的得度，未脱的得脱，未得苏息的得到苏息，未得涅槃的得到涅槃；衣钵杂物都归你。」",
        "鹿林梵志子听了，增长邪见，手拿利刀，走遍房舍、经行处、禅房，见到比丘就说："
        "「哪些沙门持戒有德，未度的我能使他得度，未脱的使他得脱……？」"
        "当时有厌患身体的人走出房来，求他令自己得度；梵志子就用利刀杀害，接连乃至杀了六十人。",
        "那时世尊到了十五日说戒的时候，在僧众前坐下，问尊者阿难："
        "「是什么因缘，比丘们变得越来越少、减损、殆尽？」",
        "阿难对佛说：「世尊为比丘们说修不净观并加以赞叹；比丘们修了之后对身体极其厌患……」"
        "详细说一直到「杀了六十位比丘。因为这个因缘，僧众变少。"
        "唯愿世尊再说别的法，让比丘们听了勤修智慧，乐于受持正法，乐于安住正法。」",
        "佛告诉阿难：「因此我现在说明微细的安住：随顺开觉，已生起、尚未生起的恶不善法迅速休息——"
        "就像天降大雨，能使已扬起、未扬起的尘垢休息。"
        "什么是多多修习的微细安住，能使已起、未起的恶不善法休息？就是入出息念的安住。」",
        "阿难对佛说：「怎样修习入出息念的安住，能这样使恶不善法休息？」",
        f"佛告诉阿难：「{SIT_PREP_MOD}{SIXTEEN_MOD}」",
        CLOSE_AN_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN54.9；"
        "SN 作毗舍离大林重阁，汉作金刚跋求摩河侧——地名从汉，法义从 SN："
        "不净观赞叹后僧众自害，改示安那般那为微细、能息恶不善法之住。"
        "魔赞／鹿林梵志子杀六十人为汉广叙事，保留。"
    ),
}

# --- SA 810 金刚（SN54.13 一法满四／七／二）----------------------------------
SUTTAS["SA_810"] = {
    "lit": [
        "如是我闻：一时，佛住金刚跋求摩河侧萨罗梨林中。",
        "尔时尊者阿难独一静处，禅思作是念：「颇有一法，修习多修习，"
        "令四法满足；四法满足已，七法满足；七法满足已，二法满足？」"
        "从禅觉已，往诣佛所，稽首礼足，退坐一面，以是念白佛。",
        "佛告阿难：「有一法，多修习已，能令二法满足。何等一法？谓安那般那念。"
        "多修习已，能令四念处满足；四念处满足已，七觉支满足；七觉支满足已，明与解脱满足。」",
        "「云何修安那般那念，令四念处满足？"
        f"{SIT_PREP_LIT}"
        "阿难！圣弟子入息时如入息而学，出息时如出息而学；"
        "若长若短，觉知一切身，止息身行——如是学。"
        "尔时圣弟子于身循身观住；若有余身法，亦随比思惟。是名身念处。"
        "若时觉知喜、觉知乐、觉知心行、止息心行——如是学。"
        "尔时于受循受观住；若有余受，亦随比思惟。是名受念处。"
        "若时觉知心、悦心、定心、解脱心——如是学。"
        "尔时于心循心观住；若有余心，亦随比思惟。是名心念处。"
        "若时观察无常、离贪、灭、舍遣——如是学。"
        "尔时于法循法观住；若有余法，亦随比思惟。是名法念处。"
        "是名修安那般那念，满足四念处。」",
        "阿难白佛：「云何修四念处，令七觉支满足？」",
        "佛告阿难：「若比丘于身循身观，念住不忘，尔时方便修念觉支，念觉支满足；"
        "念满足已，于法简择思量，修择法觉支，择法觉支满足；"
        "简择已得精勤，修精进觉支，精进觉支满足；"
        "精勤已心欢喜，修喜觉支，喜觉支满足；"
        "欢喜已身心轻安，修轻安觉支，轻安觉支满足；"
        "身心乐已得定，修定觉支，定觉支满足；"
        "定满足已，贪忧灭，得平等舍，修舍觉支，舍觉支满足。"
        "受、心、法念处，亦如是说。"
        f"是名修四念处，满足七觉支——{SEVEN_BOJ_LIT}。」",
        "阿难白佛：「云何修七觉支，满足明与解脱？」",
        f"佛告阿难：「若比丘修念觉支，{NISSAYA_LIT}，乃至修舍觉支，{NISSAYA_LIT}——"
        "如是修习，明与解脱满足。"
        "阿难！是名法法相类、法法相润：十三法中，一法为增上，一法为门，次第增进，修习满足。」",
        CLOSE_AN_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在金刚跋求摩河侧的萨罗梨林中。",
        "那时尊者阿难独自在静处禅思，心中想：「可有一种法，修习多多修习，"
        "能使四种法满足；四种法满足后，七种法满足；七种法满足后，两种法满足？」"
        "从禅修中出来后，来到佛所，叩头礼足，坐在一边，把这个想法禀告佛。",
        "佛告诉阿难：「有一种法，多多修习后，能使两种法满足。哪一种法？就是入出息念。"
        "多多修习后，能使四念处满足；四念处满足后，七觉支满足；七觉支满足后，明与解脱满足。」",
        "「怎样修习入出息念，使四念处满足？"
        f"{SIT_PREP_MOD}"
        "阿难！圣弟子入息时依入息而学，出息时依出息而学；"
        "或长或短，觉知整个身体，止息身行——这样学。"
        "那时圣弟子在身上循身观察而住；若还有其他身法，也随顺比类思惟。这叫做身念处。"
        "若有时觉知喜、觉知乐、觉知心行、止息心行——这样学。"
        "那时在受上循受观察而住；若还有其他受，也随顺比类思惟。这叫做受念处。"
        "若有时觉知心、使心喜悦、使心入定、使心解脱——这样学。"
        "那时在心上循心观察而住；若还有其他心，也随顺比类思惟。这叫做心念处。"
        "若有时观察无常、离贪、灭、舍遣——这样学。"
        "那时在法上循法观察而住；若还有其他法，也随顺比类思惟。这叫做法念处。"
        "这叫做修习入出息念，满足四念处。」",
        "阿难对佛说：「怎样修四念处，使七觉支满足？」",
        "佛告诉阿难：「如果比丘在身上循身观察，念住不忘，那时便方便修念觉支，念觉支满足；"
        "念满足后，对法简择思量，修择法觉支，择法觉支满足；"
        "简择之后精勤用功，修精进觉支，精进觉支满足；"
        "精勤之后心生欢喜，修喜觉支，喜觉支满足；"
        "欢喜之后身心轻安，修轻安觉支，轻安觉支满足；"
        "身心安乐之后得定，修定觉支，定觉支满足；"
        "定满足后，贪与忧灭，得平等舍，修舍觉支，舍觉支满足。"
        "受、心、法念处，也这样说。"
        f"这叫做修四念处，满足七觉支——{SEVEN_BOJ_MOD}。」",
        "阿难对佛说：「怎样修七觉支，满足明与解脱？」",
        f"佛告诉阿难：「如果比丘修念觉支，{NISSAYA_MOD}，一直到修舍觉支，{NISSAYA_MOD}——"
        "这样修习，明与解脱就满足。"
        "阿难！这叫做法与法相类、法与法相润：在这十三法中，一法为增上，一法为门，次第增进，修习满足。」",
        CLOSE_AN_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN54.13 Ānanda；"
        "一法＝安那般那念 → 四念处 → 七觉支 → 明解脱（vijjā-vimutti）。"
        "觉分→觉支；猗→轻安；明解脱＝明与解脱。地名从汉（金刚），结构从 SN。"
    ),
}

CONFIDENCE: dict[str, str] = {
    "SA_791": "medium",
    "SA_792": "medium",
    "SA_793": "medium",
    "SA_794": "high",
    "SA_795": "high",
    "SA_796": "high",
    "SA_797": "high",
    "SA_798": "high",
    "SA_799": "high",
    "SA_800": "high",
    "SA_801": "high",
    "SA_802": "high",
    "SA_803": "high",
    "SA_804": "high",
    "SA_805": "high",
    "SA_806": "high",
    "SA_807": "high",
    "SA_808": "high",
    "SA_809": "high",
    "SA_810": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_792": "邪正 peyyāla：恶趣道五无间；正道十善据 SA_791 补",
    "SA_793": "顺流逆流末：退／胜／下／上道迹异名 peyyāla 压缩",
    "SA_799": "沙门果 peyyāla「如上说」→ SN45.35 四果句",
    "SA_800": "婆罗门／梵行交叉指示 → SN45.37–40 全纲",
    "SA_804": "断觉想末：不动／大果／甘露／二四五七果 peyyāla",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(791, 811)}, (
        "GOLD must cover SA_791–SA_810 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    # Parallel batch owns 771–790
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

    # Boundary: SA_790 if gold, else SA_770, else SA_730
    _goldish = {"gold", "gold_reconstructed"}
    by_status = {r["id"]: r.get("review_status") for r in records}
    if by_status.get("SA_790") in _goldish:
        boundary_id = "SA_790"
    elif by_status.get("SA_770") in _goldish:
        boundary_id = "SA_770"
    else:
        boundary_id = "SA_730"

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

    # Snapshot 771–790 to assert untouched
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
        if rec["id"] in {f"SA_{i}" for i in range(771, 791)}
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
    (ROOT / "data" / "translated" / "validation_report_sa791-810.json").write_text(
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
    continuous_791_810 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(791, 811)
    )
    untouched_771_790 = all(f"SA_{i}" not in GOLD for i in range(771, 791))

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_791–SA_810 only)")
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
    print(f"continuous_gold_SA_791–810={continuous_791_810}")
    print(f"SA_771–790_untouched={untouched_771_790}")
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
