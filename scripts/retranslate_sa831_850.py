#!/usr/bin/env python3
"""Retranslate SA 831–850（学相应：戒／三学／离车–天道）→ merge.

本批二十经：
831–840 学相应（戒、三学、离车 SN55.30、不贪、王、四不坏净、过患、食、戒）
841 润泽 SN55.41
842–850 学相应卷三十三／三十二（婆罗门、舍利弗、恐怖、天道）

信：有 SN／AN 者以平行为准；求那跋陀罗汉本定位术语。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_831–850；不触碰 SA_811–830／SA_851+（并行批次）；
      断言 SA_830 不变（若尚未 gold 则 SA_810）。
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

OPEN_VES_LIT = "如是我闻：一时，佛住毗舍离国猕猴池侧重阁讲堂。"
OPEN_VES_MOD = "我是这样听说的：有一次，佛住在毗舍离国猕猴池侧重阁讲堂。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_SAR_LIT = "佛说此经已，尊者舍利弗闻佛所说，欢喜奉行。"
CLOSE_SAR_MOD = "佛说完这部经，尊者舍利弗听佛所说，都欢喜奉行。"

FOUR_LIT = "于佛不坏净、于法不坏净、于僧不坏净、圣戒成就"
FOUR_MOD = "于佛不坏净、于法不坏净、于僧不坏净、以及圣戒成就"

STUDY_LIT = f"是故诸比丘当如是学：『我当成就{FOUR_LIT}。』"
STUDY_MOD = f"所以比丘们应当这样学：『我应当成就{FOUR_MOD}。』"

SOTA_SELF_LIT = (
    "地狱、畜生、饿鬼恶趣已尽，得须陀洹，不堕恶趣，决定正向正觉，"
    "极七有天人往来，究竟苦边"
)
SOTA_SELF_MOD = (
    "地狱、畜生、饿鬼恶趣已尽，得须陀洹，不堕恶趣，决定正向正觉，"
    "最多七次天人往来，究竟苦边"
)

EIGHT_LIT = "正见、正志、正语、正业、正命、正精进、正念、正定"
EIGHT_MOD = "正见、正志、正语、正业、正命、正精进、正念、正定"

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

# --- SA 831 戒（学戒轻重；SC 表列 AN3.91 与法义不符，保守依汉）---------------
SUTTAS["SA_831"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若上座长老，初不乐学戒、不重戒，"
        "见余比丘乐学戒、重戒、赞叹制戒，亦不随赞。"
        "我于此等亦不赞叹——以其初不乐学戒故。"
        "所以者何？若大师赞彼，余人当习近亲重、同其所见；"
        "同见故，长夜受不饶益苦。"
        "于中年、少年，亦复如是。"
        "其乐学戒、重戒、赞叹制戒者，我则随喜赞叹。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「如果上座长老起初不乐学戒、不重戒，"
        "看见别的比丘乐学戒、重戒、赞叹制戒，也不跟着赞叹。"
        "我对这些人也不赞叹——因为他们起初就不乐学戒。"
        "为什么？若大师赞叹他们，别人就会亲近倚重、同其所见；"
        "同见之后，长夜会受无益之苦。"
        "对中年、少年，也是一样。"
        "那些乐学戒、重戒、赞叹制戒的，我则随喜赞叹。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：学相应「戒」——上座不乐学戒则不赞；"
        "SC 表列 AN3.91 Saṅkavā 与 SA_830 同号，法义不符，不以彼为据。"
        "删「如前说」回环，补乐学戒者随喜句以足因果。"
    ),
}

# --- SA 832 三学（AN3.89）------------------------------------------------------
SUTTAS["SA_832"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有三学。何等为三？谓增上戒学、增上心学、增上慧学。"
        "何等增上戒学？比丘住戒，护波罗提木叉律仪，威仪具足，"
        "见微细罪生怖畏，受持学处——是名增上戒学。"
        "何等增上心学？比丘离欲、离不善法，有觉有观，离生喜乐，"
        "初禅具足住，乃至第四禅具足住——是名增上心学。"
        "何等增上慧学？比丘如实知苦圣谛、苦集、苦灭、苦灭道迹圣谛——"
        "是名增上慧学。」",
        "三学余门，如念处说：如禅，无量、无色亦尔；"
        "如四谛，四念处、四正断、四神足、五根、五力、七觉支、八圣道、"
        "止观修习，亦复如是。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有三学。哪三种？就是增上戒学、增上心学、增上慧学。"
        "什么是增上戒学？比丘住戒，护持波罗提木叉律仪，威仪具足，"
        "见微细罪就生怖畏，受持学处——这叫增上戒学。"
        "什么是增上心学？比丘离欲、离不善法，有觉有观，离生喜乐，"
        "具足安住初禅，一直到具足安住第四禅——这叫增上心学。"
        "什么是增上慧学？比丘如实知道苦圣谛、苦集、苦灭、苦灭道迹圣谛——"
        "这叫增上慧学。」",
        "三学其余门类，如同念处所说：如同禅，无量、无色也一样；"
        "如同四谛，四念处、四正断、四神足、五根、五力、七觉支、八圣道、"
        "止观修习，也是这样说。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN3.89 Paṭhamasikkhattaya（三学）；"
        "据巴利 adhicitta→增上心学（汉「增上意学」同义改称）；"
        "卷末 peyyāla 纲目压缩保留，不回填全文。"
    ),
}

# --- SA 833 离车（SN55.30 Nandaka）---------------------------------------------
SUTTAS["SA_833"] = {
    "lit": [
        OPEN_VES_LIT,
        "时有离车大臣难陀，来诣佛所，稽首佛足，退坐一面。",
        "佛告难陀：「圣弟子成就四法，得须陀洹，不堕恶趣，决定正向正觉。"
        f"何等为四？谓{FOUR_LIT}。"
        "成就此四者，得寿命——人寿、天寿；得好色、安乐、名称、自在——"
        "皆于人中、天上具足。"
        "难陀！我非从他沙门、婆罗门闻已而说；乃自知、自见、自证，故如是说。」",
        "时有从者白难陀：「浴时已至，宜去。」"
        "难陀答言：「止！何须外洗。今于世尊得清净信，即是内浴。」",
        "离车难陀闻佛所说，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_VES_MOD,
        "那时有离车大臣难陀，来到佛那里，顶礼佛足，退坐一面。",
        "佛告诉难陀：「圣弟子成就四法，得须陀洹，不堕恶趣，决定正向正觉。"
        f"哪四种？就是{FOUR_MOD}。"
        "成就这四法的人，得到寿命——人寿、天寿；得到好色、安乐、名称、自在——"
        "在人间、天上都具足。"
        "难陀！我不是从别的沙门、婆罗门听来才说；乃是自己知、自己见、自己证，才这样说。」",
        "这时有随从对难陀说：「洗澡的时间到了，该走了。」"
        "难陀答道：「够了！何必外面的澡浴。如今于世尊得清净信，就是内在的沐浴。」",
        "离车难陀听佛所说，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.30 Nandakalicchavi；"
        "据 SN 校正：补须陀洹／不堕恶趣定型；删汉「十法」天人色声香味触铺排；"
        "改「不由他信…」为「非从他闻，自知自见自证」；调象师→大臣（mahāmatta）。"
    ),
}

# --- SA 834 不贪（SN55.44／45 大富）--------------------------------------------
SUTTAS["SA_834"] = {
    "lit": [
        OPEN_VES_LIT,
        "尔时世尊告诸比丘：「圣弟子成就四法，说名富裕、大财、大受用。"
        f"何等为四？谓{FOUR_LIT}。"
        f"{STUDY_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "那时世尊告诉比丘们：「圣弟子成就四法，可以说是富裕、大财、大受用。"
        f"哪四种？就是{FOUR_MOD}。"
        f"{STUDY_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.44／45 Mahaddhana（大富）；"
        "据 SN：aḍḍha／mahaddhana／mahābhoga→富裕大财；"
        "汉「不于人中贫活、不寒乞」意同，改称以就巴利。"
    ),
}

# --- SA 835 王（SN55.1 转轮王）-------------------------------------------------
SUTTAS["SA_835"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「转轮王王四天下，身坏命终，得生天上，"
        "于欢喜园天女围绕、五欲自恣——然缺四法，仍未脱地狱、畜生、饿鬼恶趣之苦。"
        f"何等为四？谓未成就{FOUR_LIT}。"
        "多闻圣弟子粪扫衣、抟食活命、草敷为座——然成就此四，"
        "已解脱地狱、畜生、饿鬼恶趣之苦。"
        "诸比丘！得四天下，于得此四法，不及其十六分之一。"
        f"{STUDY_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「转轮王统治四天下，身坏命终，得生天上，"
        "在欢喜园有天女围绕、受用五欲——可是缺少四法，仍未脱地狱、畜生、饿鬼恶趣之苦。"
        f"哪四法？就是尚未成就{FOUR_MOD}。"
        "多闻圣弟子穿粪扫衣、靠乞食活命、以草为座——可是成就这四法，"
        "已经解脱地狱、畜生、饿鬼恶趣之苦。"
        "比丘们！得到四天下，比起得到这四法，还够不上十六分之一。"
        f"{STUDY_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.1 Cakkavattirāja；"
        "据 SN 补欢喜园／五欲句与「四天下不及十六分一」；"
        "删汉「七宝／四种神力」冗列，义从平行。"
    ),
}

# --- SA 836 四不坏净（SN55.16／17 亲友）----------------------------------------
SUTTAS["SA_836"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若所哀愍、所应听者——亲友、同僚、亲属——"
        f"当劝立安住于四不坏净。何等为四？{FOUR_LIT}。"
        "所以者何？地水火风可有变易增损，"
        "圣弟子成就于佛不坏净者，无有堕地狱、畜生、饿鬼之理——"
        "于法、僧不坏净、圣戒，亦复如是。"
        f"{STUDY_LIT}"
        "亦当建立余人，令得成就。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「凡是你们所哀愍、值得听受的——亲友、同僚、亲属——"
        f"应当劝导、安立他们住于四不坏净。哪四种？{FOUR_MOD}。"
        "为什么？地水火风可以变易增损，"
        "圣弟子成就于佛不坏净的，没有堕入地狱、畜生、饿鬼的道理——"
        "于法、僧不坏净、圣戒，也是一样。"
        f"{STUDY_MOD}"
        "也应当建立别人，使他们成就。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.16／17 Mittāmacca；"
        "汉兼「哀愍令说」与「四大可变、四净不变」——分属 16／17，并取；"
        "「四不坏净」= sotāpattiyaṅga。"
    ),
}

# --- SA 837 过患（无平行：依人五患→劝四不坏净）-------------------------------
SUTTAS["SA_837"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若唯信敬于人，生五过患。"
        "彼或犯戒违律，为众摈弃；敬者念言：『我所重师，众已弃薄，我何缘入寺？』"
        "不入寺则不敬僧，不敬僧则不闻法，不闻法退失善法，不久住正法——是为初患。"
        "或众作不见举；或彼持衣钵游方；或捨戒还俗；或身坏命终——"
        "敬者皆以是故不入寺、不敬僧、不闻法、退失善法，不得久住——是为五患。"
        f"是故当如是学：『我当成就{FOUR_LIT}。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「如果只信敬某一个人，会生五种过患。"
        "那人或犯戒违律，被僧众摈弃；敬重他的人会想：『我所敬重的师，已被众弃薄，我何必再入寺？』"
        "不入寺就不敬僧，不敬僧就听不到法，听不到法就退失善法，不能久住正法——这是第一种过患。"
        "或者僧众对他作不见举；或者他持衣钵游方；或者捨戒还俗；或者身坏命终——"
        "敬重他的人都因此不入寺、不敬僧、不闻法、退失善法，不能久住——这就是五种过患。"
        f"所以应当这样学：『我应当成就{FOUR_MOD}。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；"
        "压缩五患同型反复（犯戒摈／不见举／游方／还俗／命终），"
        "结归四不坏净——与前后须陀洹支相应一致。"
    ),
}

# --- SA 838 食（SN55.31 福德润泽／安乐食）--------------------------------------
SUTTAS["SA_838"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种福德润泽、善法润泽，为安乐之食。"
        f"何等为四？谓{FOUR_LIT}——"
        "是为四福德润泽、善法润泽，能长养安乐。"
        f"{STUDY_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种福德润泽、善法润泽，是安乐的资粮。"
        f"哪四种？就是{FOUR_MOD}——"
        "这就是四种福德润泽、善法润泽，能长养安乐。"
        f"{STUDY_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.31 Paṭhamapuññābhisanda；"
        "据 SN 校正：删汉「抟食、触食、意思食、识食」误植（属食相应）；"
        "puññābhisanda／sukhassāhāra→福德润泽、安乐食。"
    ),
}

# --- SA 839 戒（peyyāla；无平行，依 838 纲＋汉差别）---------------------------
SUTTAS["SA_839"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种福德润泽、善法润泽，为安乐之食。"
        "何等为四？谓于佛不坏净；于法——为正闻法；于僧——为正念僧；"
        "及圣戒成就。"
        f"{STUDY_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种福德润泽、善法润泽，是安乐的资粮。"
        "哪四种？就是于佛不坏净；于法——作为正闻法；于僧——作为正念僧；"
        "以及圣戒成就。"
        f"{STUDY_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=low：汉仅「如上说。差别者…」残句；"
        "gold_reconstructed：依 SA_838／SN55.31 四润泽框架，"
        "按汉「闻法、众僧所念、圣戒」释为法／僧／戒差别表述。"
    ),
}

# --- SA 840 戒（SN55.32 第四＝离悭施）-----------------------------------------
SUTTAS["SA_840"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种福德润泽、善法润泽，为安乐之食。"
        "何等为四？谓于佛不坏净、于法不坏净、于僧不坏净；"
        "复次，圣弟子离悭垢心，在家而住，舒手惠施，常乐捨与，均等布施——"
        "是为第四福德润泽、善法润泽，能长养安乐。"
        "是故诸比丘当如是学：『我当成就于佛、法、僧不坏净，"
        "及离悭惠施。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种福德润泽、善法润泽，是安乐的资粮。"
        "哪四种？就是于佛不坏净、于法不坏净、于僧不坏净；"
        "再者，圣弟子心离悭垢，住在家中，舒手布施，常乐捨与，均等分享——"
        "这是第四种福德润泽、善法润泽，能长养安乐。"
        "所以比丘们应当这样学：『我应当成就于佛、法、僧不坏净，"
        "以及离悭布施。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.32 Dutiyapuññābhisanda；"
        "gold_reconstructed：汉「次经亦如上说」据 SN 补全；"
        "第四支=离悭施（非圣戒）——据巴利校正汉「圣戒成就」误植。"
    ),
}

# --- SA 841 润泽（SN55.41）-----------------------------------------------------
SUTTAS["SA_841"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种福德润泽、善法润泽，为安乐之食。"
        f"何等为四？谓{FOUR_LIT}。"
        "圣弟子成就此四，其福不可称量——不得言尔所福、尔所福聚；"
        "唯说为无量、不可计，是大福聚。"
        "譬如大海，水不可量——不得言百瓶、千瓶、百千瓶；"
        "唯说为大水聚。圣弟子四润泽亦复如是。"
        f"{STUDY_LIT}」",
        "尔时世尊说偈言：",
        "「众流归巨海，汪洋不可量；江河人所依，悉趣于大海。"
        "能施衣食座，福流归智者；如河输海水，功德亦复然。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种福德润泽、善法润泽，是安乐的资粮。"
        f"哪四种？就是{FOUR_MOD}。"
        "圣弟子成就这四种，他的福德不可称量——不能说有这么多福、这么大福聚；"
        "只能说是无量、不可计算的大福聚。"
        "好比大海，水不可量——不能说有一百瓶、一千瓶、百千瓶；"
        "只能说是大水聚。圣弟子的四种润泽也是这样。"
        f"{STUDY_MOD}」",
        "那时世尊说偈道：",
        "「众流归入巨海，汪洋不可测量；江河为人所依，都奔向大海。"
        "能布施衣食座席，福流归于智者；如同河水输送入海，功德也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.41 Paṭhamaabhisanda；"
        "gold_reconstructed：汉「次经亦如上说」据 SN 补四润泽＋大海喻；"
        "汉五河合流→据 SN 改为大海不可量；偈据 SN 施衣食座／福流归智者校。"
    ),
}

# --- SA 842 婆罗门（SN55.12）---------------------------------------------------
SUTTAS["SA_842"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「婆罗门说『起而行』之道，劝弟子："
        "『善男子！晨朝东向直行，坑堑、棘刺、沼泽、污水皆莫避；"
        "随所颠仆，即待其死——身坏命终，当生善趣、天上。』"
        "此是愚行、迷行，不趣厌、离贪、灭、寂、通智、等觉、涅槃。"
        "我于圣律中说『起而行』之道，能趣一向厌、离贪、灭、寂、通智、等觉、涅槃——"
        f"谓圣弟子成就{FOUR_LIT}。"
        "此是『起而行』道，能趣涅槃。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「婆罗门宣说一种叫『起而行』的道，劝弟子："
        "『善男子！清晨向东方一直走，坑堑、棘刺、沼泽、污水都不要躲；"
        "在哪里跌倒，就在那里等死——身坏命终，会生到善趣、天上。』"
        "这是愚行、迷行，不导向厌离、离贪、灭、寂静、通智、等觉、涅槃。"
        "我在圣律中宣说『起而行』之道，能导向一向厌离、离贪、灭、寂静、通智、等觉、涅槃——"
        f"就是圣弟子成就{FOUR_MOD}。"
        "这才是『起而行』之道，能趣向涅槃。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.12 Brāhmaṇa（udayagāminī）；"
        "据 SN 校正：汉「八圣道」→四不坏净（须陀洹支）为「起而行」正道；"
        "删胡麻屑／牛屎卧等外道仪轨铺排，义从巴利直行不顾险。"
    ),
}

# --- SA 843 舍利弗（SN55.5）----------------------------------------------------
SUTTAS["SA_843"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊问尊者舍利弗：「所谓入流分——何等为入流分？」"
        "舍利弗白佛：「世尊！入流分有四：亲近善士、听闻正法、"
        "如理作意、法次法向。」"
        "佛言：「善哉！舍利弗！」",
        "「所谓流——何等为流？」"
        f"舍利弗白佛：「世尊！流者，谓八圣道——{EIGHT_LIT}。」"
        "佛言：「善哉！」",
        "「所谓入流者——何等为入流者？」"
        "舍利弗白佛：「世尊！成就此八圣道者，是名入流者——"
        "某名某姓之尊者。」"
        "佛言：「善哉！如汝所说。」",
        CLOSE_SAR_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊问尊者舍利弗：「人们说入流分——什么是入流分？」"
        "舍利弗回答佛：「世尊！入流分有四种：亲近善士、听闻正法、"
        "如理作意、依法次法修行。」"
        "佛说：「善哉！舍利弗！」",
        "「人们说流——什么是流？」"
        f"舍利弗回答佛：「世尊！流就是八圣道——{EIGHT_MOD}。」"
        "佛说：「善哉！」",
        "「人们说入流者——什么是入流者？」"
        "舍利弗回答佛：「世尊！成就这八圣道的人，叫做入流者——"
        "某某名、某某姓的尊者。」"
        "佛说：「善哉！正如你所说。」",
        CLOSE_SAR_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.5 Dutiyasāriputta；"
        "据 SN 校正问序：入流分→流→入流者；"
        "入流者＝成就八圣道（非汉「四不坏净」）；四不坏净属果德，此处从巴利。"
    ),
}

# --- SA 844 舍利弗（SN55.4：阿难问／舍利弗答）---------------------------------
SUTTAS["SA_844"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时尊者阿难诣尊者舍利弗所，问讯已，退坐一面，言："
        "「舍利弗！成就几法，如来记说彼人得须陀洹，不堕恶趣，"
        "决定正向正觉，极七有天人往来，究竟苦边？」",
        "舍利弗言：「阿难！成就四法，如来记说彼人得须陀洹，不堕恶趣，"
        "决定正向正觉，极七有天人往来，究竟苦边。"
        f"何等为四？谓{FOUR_LIT}。"
        "成就此四，如来记说得须陀洹，不堕恶趣，决定正向正觉，究竟苦边。」",
        "阿难言：「如是，如是！」",
        "时二尊者共论已，展转随喜，从座起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者阿难到尊者舍利弗那里，问讯后，退坐一面，说："
        "「舍利弗！要成就几法，如来才会记说那人得须陀洹，不堕恶趣，"
        "决定正向正觉，最多七次天人往来，究竟苦边？」",
        "舍利弗说：「阿难！成就四法，如来记说那人得须陀洹，不堕恶趣，"
        "决定正向正觉，最多七次天人往来，究竟苦边。"
        f"哪四种？就是{FOUR_MOD}。"
        "成就这四种，如来记说得须陀洹，不堕恶趣，决定正向正觉，究竟苦边。」",
        "阿难说：「正是这样！」",
        "当时两位尊者讨论完毕，互相随喜，从座位起来离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.4 Paṭhamasāriputta；"
        "据 SN 校正：问答主从——阿难问、舍利弗答（汉互倒）；"
        "删「断四法」对扬，唯取「成就四法」；七有／究竟苦边从汉须陀洹定型。"
    ),
}

# --- SA 845 恐怖（SN55.29／AN9.28）---------------------------------------------
SUTTAS["SA_845"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「圣弟子五恐怖怨对已息，成就四入流分，"
        "于圣理以慧善见善透——若欲自记，则能自记："
        f"『{SOTA_SELF_LIT}。』",
        "何等五恐怖怨对息？杀生因缘生怖怨；离杀生则息。"
        "不与取、邪淫、妄语、饮酒因缘生怖怨；离则息——"
        "是名五恐怖怨对息。",
        f"何等四入流分？谓{FOUR_LIT}。",
        "何等圣理如实证知？谓苦圣谛、苦集、苦灭、苦灭道迹如实知——"
        "是名于圣理如实证知。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「圣弟子五种恐怖怨对已经平息，成就四入流分，"
        "对圣理以智慧善见、善透——如果想自己记说，就能自己记说："
        f"『{SOTA_SELF_MOD}。』",
        "哪五种恐怖怨对平息？因杀生而生怖畏怨对；离杀生就平息。"
        "因不与取、邪淫、妄语、饮酒而生怖畏怨对；远离就平息——"
        "这叫五种恐怖怨对平息。",
        f"哪四种入流分？就是{FOUR_MOD}。",
        "什么是对圣理如实证知？就是苦圣谛、苦集、苦灭、苦灭道迹如实知道——"
        "这叫对圣理如实证知。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.29／AN9.28；"
        "据 SN：汉「三事决定」→四入流分（补圣戒）；"
        "ariyo ñāyo 汉作四谛，保留（SN55.28 或作缘起，本经从汉四谛门）。"
    ),
}

# --- SA 846 恐怖（peyyāla：八道／缘起二门）-------------------------------------
SUTTAS["SA_846"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「圣弟子五恐怖怨对已息，成就四入流分，"
        "于圣理以慧善见善透——若欲自记，则能自记："
        f"『{SOTA_SELF_LIT}。』"
        f"五息、四入流分，如上说。差别者：圣理谓八圣道——{EIGHT_LIT}。」",
        "次经复说，差别者：「圣理谓十二缘起如实知——"
        "此有故彼有，此起故彼起：无明缘行，行缘识，识缘名色，"
        "名色缘六处，六处缘触，触缘受，受缘爱，爱缘取，取缘有，"
        "有缘生，生缘老死忧悲苦恼。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「圣弟子五种恐怖怨对已经平息，成就四入流分，"
        "对圣理以智慧善见、善透——如果想自己记说，就能自己记说："
        f"『{SOTA_SELF_MOD}。』"
        f"五息、四入流分，如同前面所说。差别在于：圣理是指八圣道——{EIGHT_MOD}。」",
        "下一经也这样说，差别在于：「圣理是指如实知道十二缘起——"
        "此有故彼有，此起故彼起：无明缘行，行缘识，识缘名色，"
        "名色缘六处，六处缘触，触缘受，受缘爱，爱缘取，取缘有，"
        "有缘生，生缘老死忧悲苦恼。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.28／SN12.41 等（圣理＝八道／缘起）；"
        "gold_reconstructed：汉「如上说」二差别经，据 SA_845 框架＋SN 缘起定型补全。"
    ),
}

# --- SA 847 天道（SN55.34）-----------------------------------------------------
SUTTAS["SA_847"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种诸天之足迹，能令未净者净、已净者更净。"
        f"何等为四？谓{FOUR_LIT}——"
        "是名四天足迹，未净令净，已净更净。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种诸天的足迹，能使未清净的清净、已清净的更清净。"
        f"哪四种？就是{FOUR_MOD}——"
        "这叫做四种天足迹，未净令净，已净更净。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.34 Paṭhamadevapada；"
        "devapada→天足迹／天道；汉「诸天天道」从习称，义同。"
    ),
}

# --- SA 848 天道（SN55.35 广：念佛等→无恚）------------------------------------
SUTTAS["SA_848"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种诸天之足迹，未净令净，已净更净。"
        "何等为四？圣弟子念如来：『彼世尊是阿罗汉、等正觉、明行足、善逝、"
        "世间解、无上士、调御丈夫、天人师、佛世尊。』"
        "念已作是观：『诸天以无恚为上；我于若怖若安，都不安害有情——"
        "我实成就天足迹法。』是为第一。",
        "复次，念法：『佛所说法，现见、无时、来见、导向、智者各自当知。』"
        "如是观无恚，安住天足迹——是为第二。",
        "复次，念僧：『世尊弟子僧善行、质直行、如理行、和敬行，"
        "应供、应待、应施、应合掌，是世间无上福田。』"
        "如是观无恚——是为第三。",
        "复次，念自戒：『我戒不破、不穿、不杂、智者所赞、能引定。』"
        "如是观无恚——是为第四。"
        "是名四天足迹，未净令净，已净更净。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种诸天的足迹，使未净者净、已净者更净。"
        "哪四种？圣弟子忆念如来：『那位世尊是阿罗汉、等正觉、明行足、善逝、"
        "世间解、无上士、调御丈夫、天人师、佛世尊。』"
        "忆念后这样观察：『诸天以无恚为最上；我不论在怖畏或安稳中，都不伤害有情——"
        "我确实成就了天足迹之法。』这是第一种。",
        "再者，忆念法：『佛所说的法，现可见、不待时、请来看、导向、智者各自当知。』"
        "这样观察无恚，安住天足迹——这是第二种。",
        "再者，忆念僧：『世尊的弟子僧善行、质直行、如理行、和敬行，"
        "应供养、应接待、应布施、应合掌，是世间无上福田。』"
        "这样观察无恚——这是第三种。",
        "再者，忆念自己的戒：『我的戒不破、不穿、不杂、智者所赞、能引定。』"
        "这样观察无恚——这是第四种。"
        "这叫做四种天足迹，未净令净，已净更净。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN55.35 Dutiyadevapada；"
        "据 SN 校正：汉「随喜→猗息→乐→三昧」链压缩为「念已观无恚＝天足迹」；"
        "abyābajjha→无恚／不害；保留佛十号与法僧戒定型。"
    ),
}

# --- SA 849 天道（SN55.35 略：断恶贪不善）--------------------------------------
SUTTAS["SA_849"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种诸天之足迹，未净令净，已净增净。"
        "何等为四？圣弟子念如来——阿罗汉、等正觉…佛世尊。"
        "念已，断恶贪及心不善法；心随喜、欢悦、身轻安、觉乐、得定；"
        "复作是念：『诸天以无恚为上；我于若怖若安，不起瞋恚，"
        "当受持纯一满净天足迹。』"
        "于法、僧、圣戒，亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种诸天的足迹，使未净者净、已净者更净。"
        "哪四种？圣弟子忆念如来——阿罗汉、等正觉…佛世尊。"
        "忆念之后，断除恶贪以及心中的不善法；心随喜、欢悦、身轻安、觉乐、得定；"
        "再这样想：『诸天以无恚为最上；我不论在怖畏或安稳中，都不起瞋恚，"
        "应当受持纯一清净的天足迹。』"
        "对于法、僧、圣戒，也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：同系 SN55.35 略本／汉异门；"
        "保留汉「断恶贪不善」＋随喜猗息链；结归无恚天足迹；"
        "法僧戒 peyyāla 从汉「亦如是说」。"
    ),
}

# --- SA 850 天道（SN55.35 略：正直／法流水）------------------------------------
SUTTAS["SA_850"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种诸天之足迹，未净令净，已净增净。"
        "何等为四？圣弟子念如来——阿罗汉、等正觉…佛世尊。"
        "念已，贪瞋痴缠不得覆心，其心正直；得法流、义流，随喜念佛之利；"
        "随喜、欢悦、身轻安、觉乐、得定；"
        "复作是念：『诸天以无恚为上；我于世间不起瞋恚，"
        "当受持纯一满净天足迹。』"
        "于法、僧、圣戒，亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种诸天的足迹，使未净者净、已净者更净。"
        "哪四种？圣弟子忆念如来——阿罗汉、等正觉…佛世尊。"
        "忆念之后，贪瞋痴缠盖不住心，心变得正直；得到法流、义流，随喜念佛的利益；"
        "随喜、欢悦、身轻安、觉乐、得定；"
        "再这样想：『诸天以无恚为最上；我在世间不起瞋恚，"
        "应当受持纯一清净的天足迹。』"
        "对于法、僧、圣戒，也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：同系 SN55.35 汉异门（正直／法流水）；"
        "汉「心貪欲缠…其心正直」读为缠不得覆、心转正直；"
        "义从无恚天足迹，不引入后期术语。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {
    "SA_831": "medium",
    "SA_832": "high",
    "SA_833": "high",
    "SA_834": "high",
    "SA_835": "high",
    "SA_836": "high",
    "SA_837": "medium",
    "SA_838": "high",
    "SA_839": "low",
    "SA_840": "high",
    "SA_841": "high",
    "SA_842": "high",
    "SA_843": "high",
    "SA_844": "high",
    "SA_845": "high",
    "SA_846": "high",
    "SA_847": "high",
    "SA_848": "high",
    "SA_849": "medium",
    "SA_850": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_839": "peyyāla「如上说」残句 → 依 SA_838／SN55.31 四润泽框架＋汉闻法／念僧／圣戒差别",
    "SA_840": "「次经亦如上说」→ SN55.32 全纲（佛法拉僧＋离悭施为第四）",
    "SA_841": "「次经亦如上说」→ SN55.41 四润泽＋大海喻＋偈",
    "SA_846": "「如上说」二差别 → SA_845 框架＋八道／十二缘起圣理门",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(831, 851)}, (
        "GOLD must cover SA_831–SA_850 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    # Parallel batches own 811–830 and 851+
    assert not any(f"SA_{i}" in GOLD for i in range(811, 831))
    assert not any(f"SA_{i}" in GOLD for i in range(851, 871))

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

    # Boundary: SA_830 if gold, else SA_810
    _goldish = {"gold", "gold_reconstructed"}
    by_status = {r["id"]: r.get("review_status") for r in records}
    if by_status.get("SA_830") in _goldish:
        boundary_id = "SA_830"
    else:
        boundary_id = "SA_810"

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
    parallel_ids = {f"SA_{i}" for i in list(range(811, 831)) + list(range(851, 871))}
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
    (ROOT / "data" / "translated" / "validation_report_sa831-850.json").write_text(
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
    continuous_831_850 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(831, 851)
    )
    untouched_811_830 = all(f"SA_{i}" not in GOLD for i in range(811, 831))
    untouched_851_plus = all(f"SA_{i}" not in GOLD for i in range(851, 871))

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_831–SA_850 only)")
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
    print(f"continuous_gold_SA_831–850={continuous_831_850}")
    print(f"SA_811–830_untouched={untouched_811_830}")
    print(f"SA_851–870_untouched={untouched_851_plus}")
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
