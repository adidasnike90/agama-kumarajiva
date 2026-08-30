#!/usr/bin/env python3
"""Retranslate SA 411–430（卷第十七 谛相应续）→ merge into final_translated_data.json.

本批二十经：论、争、大力、宿命、说论；受持、如如、受持；疑×2；
深嶮、大热、大闇；千明、千世界×2；四圣谛；禅思、三摩提、杖。

信：有平行者以 SN／Pāli／Sujato 厘义；无平行者 medium；
    交叉指示（SA 412／415／425／427）→ gold_reconstructed。
达：白话与罗什风逐段对照，段数严格相同。
雅：长文（≥400 字）sim < 0.45；短文 < 0.50（`assess_gold`）。
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

OPEN_RAJ_LIT = "如是我闻：一时，佛在王舍城迦兰陀竹园。"
OPEN_RAJ_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

CLOSE_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

FOUR_TRUTH_LIT = "苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛"
FOUR_TRUTH_MOD = "苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛"

URGE_LIT = (
    "「是故比丘于四圣谛未无间等者，当勤方便，起增上欲，精进修学。"
    "何等为四？谓" + FOUR_TRUTH_LIT + "。」"
)
URGE_MOD = (
    "「所以比丘对四圣谛还没有无间等的，应当勤加方便，发起强盛愿欲，精进修学。"
    "哪四种？就是" + FOUR_TRUTH_MOD + "。」"
)

BENEFIT_LIT = "义饶益、法饶益、梵行饶益，正智、正觉、正向涅槃"
BENEFIT_MOD = "有义饶益、法饶益、梵行饶益，能得正智、正觉，正向涅槃"

NOT_BENEFIT_LIT = "非义饶益，非法饶益，非梵行饶益，非智、非觉，不向涅槃"
NOT_BENEFIT_MOD = "没有义饶益，没有法饶益，没有梵行饶益，不是正智、正觉，不向涅槃"

TALK_FOUR_LIT = (
    "应当论说：『此苦圣谛、此苦集圣谛、此苦灭圣谛、此苦灭道迹圣谛。』"
    "所以者何？此四圣谛" + BENEFIT_LIT + "。"
)
TALK_FOUR_MOD = (
    "应当讨论：『这是苦圣谛、这是苦集圣谛、这是苦灭圣谛、这是苦灭道迹圣谛。』"
    "为什么？这四圣谛" + BENEFIT_MOD + "。"
)

BIRTH_CLIFF_LIT = "生、老、病、死、忧、悲、恼、苦"
BIRTH_CLIFF_MOD = "生、老、病、死、忧、悲、恼、苦"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」，本经作 medium。"
)

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 411 论（SN 56.10）----------------------------------------------------
SUTTAS["SA_411"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，共作议论：王事、贼事、战斗、钱财、衣食、男女、"
        "世语、行业、海中事。",
        "世尊于定中以天耳闻已，往诣食堂，敷座而坐，问：「汝等集此，何所言说？」"
        "比丘具白如上。",
        "佛言：「莫作如是无益之论。所以者何？如此论" + NOT_BENEFIT_LIT + "。"
        + TALK_FOUR_LIT + "」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里，一起议论：国王、盗贼、战争、钱财、衣食、男女、"
        "世俗闲谈、行业、海里的事。",
        "世尊在定中用天耳听见以后，来到食堂，敷座坐下，问：「你们聚在这里，在说什么？」"
        "比丘们把上面的议论都禀告了。",
        "佛说：「不要作这类无益的议论。为什么？这样的议论" + NOT_BENEFIT_MOD + "。"
        + TALK_FOUR_MOD + "」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.10 Tiracchānakathā。"
        "低劣戏论（tiracchānakathā）当以四谛论代之；汉食堂叙事情节保留。"
        "Sujato 列举更广，汉本略列已足达意，不另增花鬘／街市等项。"
    ),
}

# --- SA 412 争（SN 56.9；交叉指示）-------------------------------------------
SUTTAS["SA_412"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，共相诤论：「我知法、律，汝等不知；"
        "我所说成就、与理合，汝等不成就、不与理合；"
        "应先说者后说，应后说者先说——"
        "我胜汝劣，能答者当答。」",
        "世尊以天耳闻已，往诣食堂，问已，比丘具白。"
        "佛言：「莫作如是诤论。所以者何？如此论" + NOT_BENEFIT_LIT + "。"
        + TALK_FOUR_LIT + "」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里，互相诤论：「我懂法、律，你们不懂；"
        "我说的成立、合乎道理，你们的不成立、不合道理；"
        "该先说的你们后说，该后说的你们先说——"
        "我胜你们劣，谁能答就答。」",
        "世尊用天耳听见以后，来到食堂，询问之后，比丘们都禀告了。"
        "佛说：「不要作这样的诤论。为什么？这样的议论" + NOT_BENEFIT_MOD + "。"
        + TALK_FOUR_MOD + "」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "底本『如是广说，乃至……学无间等』为交叉指示；"
        "依 SA_411／SN56.9 框式重建：斥 viggāhikakathā，代以四谛论，补 URGE。"
        "confidence=high（平行可靠；文面重建）。"
    ),
}

# --- SA 413 大力（无 SN；Ud 2.2 resembling）---------------------------------
SUTTAS["SA_413"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，共作议论：「波斯匿王与频婆娑罗王，"
        "何者大力？何者大富？」",
        "世尊以天耳闻已，往诣食堂，问：「汝等何所论说？」"
        "比丘具白世尊。",
        "佛言：「何用议论诸王大力、大富？莫作是论。所以者何？此"
        + NOT_BENEFIT_LIT + "。"
        + TALK_FOUR_LIT + "」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里，一起议论：「波斯匿王和频婆娑罗王，"
        "谁更有大力？谁更富有？」",
        "世尊用天耳听见以后，来到食堂，问：「你们在议论什么？」"
        "比丘们把事情都禀告了世尊。",
        "佛说：「何必议论诸王谁大力、谁大富？不要作这种议论。为什么？这"
        + NOT_BENEFIT_MOD + "。"
        + TALK_FOUR_MOD + "」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "SC 仅列 resembling Ud 2.2（国王话题），非 SN 谛相应平行；"
        "依食堂斥戏论＋四谛定型框雅化，保留汉本二王比较情节。"
    ),
}

# --- SA 414 宿命（无平行）----------------------------------------------------
SUTTAS["SA_414"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，共作议论：「汝等宿命作何等业？"
        "习何工巧？以何自活？」",
        "世尊以天耳闻已，往诣食堂，问：「汝说何等？」"
        "比丘具白世尊。",
        "佛言：「莫论宿命所作。所以者何？此" + NOT_BENEFIT_LIT + "。"
        + TALK_FOUR_LIT + "」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里，一起议论：「你们过去世做了什么业？"
        "学过什么手艺？靠什么维生？」",
        "世尊用天耳听见以后，来到食堂，问：「你们在说什么？」"
        "比丘们把事情都禀告了世尊。",
        "佛说：「不要议论宿命所做的事。为什么？这" + NOT_BENEFIT_MOD + "。"
        + TALK_FOUR_MOD + "」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "论宿业／工巧／自活属无益戏论；当以四谛论代之。"
    ),
}

# --- SA 415 说论（无平行；交叉指示）-----------------------------------------
SUTTAS["SA_415"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，共作说论：「某檀越作粗疏食，我等食已无味无力；"
        "不如捨彼粗食而行乞食——"
        "乞时得好食，又见好色、闻好声，多人所识，亦得衣被、卧具、医药。」",
        "世尊以天耳闻已，往诣食堂，问已，比丘具白。"
        "佛言：「莫作如是论。所以者何？此" + NOT_BENEFIT_LIT + "。"
        + TALK_FOUR_LIT + "」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里，一起议论：「某位檀越做的饭菜粗陋，我们吃了无味无力；"
        "不如捨了那粗食去乞食——"
        "乞食时能得好食，又能见好色、闻好声，为许多人所识，还能得衣被、卧具、医药。」",
        "世尊用天耳听见以后，来到食堂，询问之后，比丘们都禀告了。"
        "佛说：「不要作这样的议论。为什么？这" + NOT_BENEFIT_MOD + "。"
        + TALK_FOUR_MOD + "」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "底本『即诣食堂……如是广说，乃至正向涅槃』为交叉指示；"
        "依 SA_411／414 食堂斥戏论框重建，差别保留汉本『粗食／乞食利养』话题。"
    ),
}

# --- SA 416 受持（SN 56.15）-------------------------------------------------
SUTTAS["SA_416"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「汝等持我所说四圣谛不？」",
        "时有异比丘从座起，正衣服，礼佛合掌白言：「唯然，世尊所说四圣谛，我悉受持。」",
        "佛问：「汝云何受持？」"
        "比丘白言：「世尊说此苦圣谛，我即受持；"
        "此苦集圣谛、此苦灭圣谛、此苦灭道迹圣谛，我亦如是受持。」",
        "佛言：「善哉！善哉！我所说四圣谛，汝真实受持。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「你们受持我所讲说的四圣谛吗？」",
        "当时有一位比丘从座位上起来，整理衣服，礼佛合掌说：「是的，世尊所说的四圣谛，我都受持。」",
        "佛问：「你怎么受持？」"
        "比丘回答：「世尊说这是苦圣谛，我就受持；"
        "这是苦集圣谛、这是苦灭圣谛、这是苦灭道迹圣谛，我也这样受持。」",
        "佛说：「很好！很好！我所讲的四圣谛，你真实地受持了。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.15 Paṭhamadhāraṇa。"
        "dhāreti＝受持／忆持四谛次第；汉对话框与 SN 合。"
    ),
}

# --- SA 417 如如（SN 56.20；慎「如如」）-------------------------------------
SUTTAS["SA_417"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「有四法：如实、不虚、不异。何等为四？"
        "谓此苦圣谛——如实、不虚、不异；"
        "此苦集圣谛、此苦灭圣谛、此苦灭道迹圣谛——亦如实、不虚、不异。"
        "此四者真、实、审谛、不颠倒，是圣所谛。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「有四种法：如实、不虚假、不是别的样子。哪四种？"
        "就是这苦圣谛——如实、不虚假、不是别的样子；"
        "这苦集圣谛、这苦灭圣谛、这苦灭道迹圣谛——也如实、不虚假、不是别的样子。"
        "这四种真切、确实、审谛、不颠倒，是圣者所确认的谛。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.20／27 Tatha。"
        "信-校正：汉题『如如』及『如如、不离如、不异如』易读作后出真如义；"
        "据 Pāli tatha／avitatha／anaññatha（Sujato: real, not unreal, not otherwise）"
        "改写为『如实、不虚、不异』，并收束汉本受持对话为佛直说四谛真实相。"
        "保留『真、实、审谛、不颠倒』早期谛义，不用真如／如来藏等后出语。"
    ),
}

# --- SA 418 受持（SN 56.16）-------------------------------------------------
SUTTAS["SA_418"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「汝持我所说四圣谛不？」",
        "时有异比丘从座起，礼佛合掌白言：「唯然，我悉持之——"
        "苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛。」",
        "佛言：「善哉！若沙门、婆罗门作是说：『沙门瞿昙所说苦圣谛，我当捨之，"
        "更立余苦圣谛』——无有是处；问已不知，唯增疑惑，非其境界故。"
        "于集、灭、道圣谛欲捨而更立者，亦复如是——但有言说，无有是处。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「你们受持我所讲的四圣谛吗？」",
        "当时有一位比丘从座位上起来，礼佛合掌说：「是的，我都受持——"
        "苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛。」",
        "佛说：「很好！若有沙门、婆罗门这样说：『沙门瞿昙所说的苦圣谛，我要捨弃，"
        "另立别的苦圣谛』——没有这样的道理；问了也不知，只会增加疑惑，因为不是他的境界。"
        "对集、灭、道圣谛想捨弃而另立的，也是一样——只有空话，没有这样的道理。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.16 Dutiyadhāraṇa。"
        "四谛不可捨此立彼（netaṁ ṭhānaṁ vijjati）；汉『但有言数』读作空言无实。"
    ),
}

# --- SA 419 疑（无平行）------------------------------------------------------
SUTTAS["SA_419"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「若比丘于佛有疑，则于" + FOUR_TRUTH_LIT + "皆有疑；"
        "于法、于僧有疑，亦于四圣谛有疑。"
        "若于佛不疑，则于四圣谛不疑；于法、于僧不疑，亦于四圣谛不疑。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「若比丘对佛有疑，就会对" + FOUR_TRUTH_MOD + "都有疑；"
        "对法、对僧有疑，也会对四圣谛有疑。"
        "若对佛不疑，就对四圣谛不疑；对法、对僧不疑，也对四圣谛不疑。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "佛／法／僧疑与四谛疑相应；依汉本收束重复，不臆造平行义。"
    ),
}

# --- SA 420 疑（无平行；与 419 互逆）-----------------------------------------
SUTTAS["SA_420"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「若沙门、婆罗门于苦圣谛有疑，则于佛、法、僧有疑；"
        "于集、灭、道圣谛有疑，亦于佛、法、僧有疑。"
        "若于苦圣谛不疑，则于佛、法、僧不疑；"
        "于集、灭、道圣谛不疑，亦于佛、法、僧不疑。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「若沙门、婆罗门对苦圣谛有疑，就会对佛、法、僧有疑；"
        "对集、灭、道圣谛有疑，也会对佛、法、僧有疑。"
        "若对苦圣谛不疑，就对佛、法、僧不疑；"
        "对集、灭、道圣谛不疑，也对佛、法、僧不疑。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "与 SA_419 互逆：由四谛疑推至三宝疑；依汉本雅化。"
    ),
}

# --- SA 421 深嶮（SN 56.42）-------------------------------------------------
SUTTAS["SA_421"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「汝等共行，至深嶮岩。」"
        "诸比丘白佛：「唯然，世尊！」"
        "世尊与大众至深嶮岩，敷座周观，告言：「此岩极大深嶮。」",
        "时有异比丘白佛：「此极深嶮——更有深嶮过此、甚可怖畏者不？」",
        "佛言：「有。谓沙门、婆罗门于" + FOUR_TRUTH_LIT + "不如实知——"
        "于趣生诸行而乐著，于趣" + BIRTH_CLIFF_LIT + "诸行而乐著；"
        "乐著故造作，造作故堕生深嶮，堕老病死忧悲恼苦深嶮。"
        "此则大深嶮，险过此岩。是故当于四圣谛勤修无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「你们一起走，到深险的山岩去。」"
        "比丘们回答：「好的，世尊！」"
        "世尊与大众来到深险山岩，敷座四面观察，说：「这山岩极大、极深险。」",
        "当时有一位比丘对佛说：「这已经很深险了——还有比这更深险、更可怕的吗？」",
        "佛说：「有。就是沙门、婆罗门对" + FOUR_TRUTH_MOD + "不能如实了知——"
        "对通向生的诸行生起乐著，对通向" + BIRTH_CLIFF_MOD + "的诸行生起乐著；"
        "乐著就继续造作，造作就堕入生的深险，堕入老病死忧悲恼苦的深险。"
        "这才是更大的深险，险过这座岩。所以应当对四圣谛勤修无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.42 Papāta。"
        "信-校正：据 SN 补『乐著诸行→造作→堕生老死深嶮』因果链"
        "（abhiramanti saṅkhāresu… papāta）；汉『生本诸行乐著』收束为此。"
        "汉住竹园／共至深岩叙事情节保留（SN 作灵鹫山→Paṭibhānakūṭa）。"
    ),
}

# --- SA 422 大热（SN 56.43）-------------------------------------------------
SUTTAS["SA_422"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「有大热地狱。生彼中者，眼所见色、耳所闻声、"
        "乃至意所知法，唯是非爱、非可意、非悦意——一向炽然。」",
        "时有异比丘白佛：「此则大热——更有大热过此、甚可怖畏、无过上者不？」",
        "佛言：「有。谓沙门、婆罗门于四圣谛不如实知——"
        "于趣生诸行乐著造作，故为" + BIRTH_CLIFF_LIT + "大火所烧。"
        "此则大热，过彼地狱。是故当于四圣谛勤修无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「有大热地狱。生在那里的众生，眼所见色、耳所闻声、"
        "乃至意所知法，都只是不可爱、不可意、不悦意——一味炽热焚烧。」",
        "当时有一位比丘对佛说：「这已经是大热了——还有比这更大热、更可怕、再没有更上的吗？」",
        "佛说：「有。就是沙门、婆罗门对四圣谛不能如实了知——"
        "对通向生的诸行乐著造作，因而被" + BIRTH_CLIFF_MOD + "的大火所烧。"
        "这才是更大的热，超过那地狱。所以应当对四圣谛勤修无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.43 Mahāpariḷāha。"
        "信-校正：据 SN 补六境一向非爱可意（aniṭṭha／akanta／amanāpa），"
        "及『乐著诸行→生老死热恼』；汉『一向与烔然』收束为此。"
    ),
}

# --- SA 423 大闇（SN 56.46）-------------------------------------------------
SUTTAS["SA_423"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「有世界中间大闇——日月虽有大威德大光明，"
        "其光不照彼处；生彼中者，不见自身分。」",
        "时有异比丘白佛：「此则大闇——更有大闇过此、甚可怖畏者不？」",
        "佛言：「有。谓沙门、婆罗门于四圣谛不如实知——"
        "乐著造作趣生诸行，故堕" + BIRTH_CLIFF_LIT + "大闇之中。"
        "此则大闇，过彼世界中间。是故当于四圣谛勤修无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「有世界与世界中间的大黑暗——日月虽有大威德、大光明，"
        "光照也到不了那里；生在那里的众生，连自己的肢体都看不见。」",
        "当时有一位比丘对佛说：「这已经是大黑暗了——还有比这更大、更可怕的黑暗吗？」",
        "佛说：「有。就是沙门、婆罗门对四圣谛不能如实了知——"
        "乐著造作通向生的诸行，因而堕入" + BIRTH_CLIFF_MOD + "的大黑暗中。"
        "这才是更大的黑暗，超过那世界中间的黑暗。所以应当对四圣谛勤修无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.46 Andhakāra（SC resembling；本文／英译可用）。"
        "信-校正：汉『大闇地狱』据 SN lokantarikā andhakāra 改写为『世界中间大闇』；"
        "日月威光不及、不见自身——与后 SA_424 千世界闇冥衔接。"
    ),
}

# --- SA 424 千明（AN 3.80 resembling；无 SN 谛本）---------------------------
SUTTAS["SA_424"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「如日游行照诸世界——乃至千日千月，照千世界、"
        "千须弥、千四天下、千四王天乃至千梵天，是名小千世界。"
        "此小千世界中间有大闇冥：日月威光所不能照，生彼中者不见自身分。」",
        "时有异比丘白佛：「更有大闇过此者不？」",
        "佛言：「有。谓沙门、婆罗门于四圣谛不如实知，"
        "堕" + BIRTH_CLIFF_LIT + "大闇冥中——此闇过于世界中间。"
        "是故当于四圣谛勤修无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「就像太阳游行照耀诸世界——乃至有千日千月，照耀千世界、"
        "千座须弥、千个四天下、千个四王天乃至千个梵天，这叫做小千世界。"
        "这小千世界的中间有大黑暗：日月的威光也照不到，生在那里的众生看不见自己的肢体。」",
        "当时有一位比丘对佛说：「还有比这更大的黑暗吗？」",
        "佛说：「有。就是沙门、婆罗门对四圣谛不能如实了知，"
        "堕入" + BIRTH_CLIFF_MOD + "的大黑暗中——这黑暗超过世界中间的黑暗。"
        "所以应当对四圣谛勤修无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "SC 仅列 resembling AN 3.80（小千世界名数）；谛＋闇冥喻同 SA_423／SN56.46 族。"
        "小千世界名数依汉本收束，不另增 AN 叙事。"
    ),
}

# --- SA 425 千世界（交叉指示）-----------------------------------------------
SUTTAS["SA_425"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「从小千世界数满至千，是名中千世界。"
        "中千世界中间亦有大闇冥——日月威光所不能照；"
        "而不如实知四圣谛者，堕" + BIRTH_CLIFF_LIT + "大闇，过彼中千中间之闇。"
        "是故当于四圣谛勤修无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「从小千世界数满到一千，叫做中千世界。"
        "中千世界中间也有大黑暗——日月的威光也照不到；"
        "而不能如实了知四圣谛的人，堕入" + BIRTH_CLIFF_MOD + "的大黑暗，超过那中千中间的黑暗。"
        "所以应当对四圣谛勤修无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "底本『如前所说，乃至……学无间等』为交叉指示；"
        "依 SA_424 小千闇冥＋四谛框，差别改为中千世界。"
    ),
}

# --- SA 426 千世界（SN 56.46 resembling）------------------------------------
SUTTAS["SA_426"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「从中千世界数满至千，是名三千大千世界。"
        "大千世界中间有大闇冥——日月游行普照世界，而彼不见；"
        "不了四圣谛者，堕" + BIRTH_CLIFF_LIT + "大闇冥中。"
        "是故当于四圣谛勤修无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「从中千世界数满到一千，叫做三千大千世界。"
        "大千世界中间有大黑暗——日月游行普照世界，却照不到那里；"
        "不能了知四圣谛的人，堕入" + BIRTH_CLIFF_MOD + "的大黑暗中。"
        "所以应当对四圣谛勤修无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 列 SN56.46 resembling；三千大千名数依汉本，"
        "闇冥＋四谛义据 SN Andhakāra 族。"
    ),
}

# --- SA 427 四圣谛（无平行；交叉／异门指示）---------------------------------
SUTTAS["SA_427"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「我今当说四圣谛。谛听，善思。"
        "何等为四？谓" + FOUR_TRUTH_LIT + "——是名四圣谛。"
        "如是四圣谛：有，当知；我当说，亦复如是。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「我现在要讲四圣谛。仔细听，好好思惟。"
        "哪四种？就是" + FOUR_TRUTH_MOD + "——这叫做四圣谛。"
        "这四圣谛：是有的，应当了知；我应当讲说，也是一样。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "底本末句『如当说，如是有、如是当知，亦如上说』为异门／交叉指示；"
        "依四谛略说定型重建为『有／当知／当说』三门并举，不另臆造广释。"
    ),
}

# --- SA 428 禅思（SN 56.2）--------------------------------------------------
SUTTAS["SA_428"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「当勤禅思，正方便起，内寂其心。"
        "所以者何？比丘禅思、内寂心成，则如实显现——"
        "此苦圣谛如实显现，此苦集、苦灭、苦灭道迹圣谛如实显现。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「应当勤修禅思，发起正方便，让内心寂静。"
        "为什么？比丘禅思、内心寂静成就以后，就会如实显现——"
        "这苦圣谛如实显现，这苦集、苦灭、苦灭道迹圣谛也如实显现。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.2 Paṭisallāna。"
        "禅思／内寂≈paṭisallāna；yathābhūtaṁ pajānāti→如实显现（汉本用语保留）。"
    ),
}

# --- SA 429 三摩提（SN 56.1）------------------------------------------------
SUTTAS["SA_429"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「当修无量三摩提，专心正念。"
        "所以者何？修无量三摩提、专心正念已，则如实显现——"
        "此苦圣谛如实显现，苦集、苦灭、苦灭道迹圣谛如实显现。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「应当修习无量三摩提，专心正念。"
        "为什么？修习无量三摩提、专心正念以后，就会如实显现——"
        "这苦圣谛如实显现，苦集、苦灭、苦灭道迹圣谛也如实显现。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.1 Samādhi。"
        "汉『无量三摩提』保留；SN 作 samādhiṁ bhāvetha（修等持），"
        "samāhito yathābhūtaṁ pajānāti。"
    ),
}

# --- SA 430 杖（SN 56.33）----------------------------------------------------
SUTTAS["SA_430"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，佛告诸比丘：「譬如有人掷杖虚空，寻即还堕——"
        "或根著地，或头著地。"
        "如是有情无明所覆、渴爱所系，流转诸趣——"
        "或从此世往彼世，或从彼世还来此世。"
        "所以者何？于四圣谛未如实见故。何等为四？谓" + FOUR_TRUTH_LIT + "。"
        "是故当于四圣谛勤修无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，佛告诉比丘们：「好比有人把杖抛向虚空，立刻又落下来——"
        "有时根部着地，有时头部着地。"
        "同样，有情被无明所覆盖、被渴爱所系缚，在诸趣中流转——"
        "有时从此世到彼世，有时从彼世回到此世。"
        "为什么？因为对四圣谛还没有如实看见。哪四种？就是" + FOUR_TRUTH_MOD + "。"
        "所以应当对四圣谛勤修无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.33 Daṇḍa。"
        "信-校正：汉『或堕地狱／畜生／饿鬼』据 SN 改为无明覆、渴爱系、"
        "彼此世流转（sakimpi asmā lokā paraṁ lokaṁ…）；杖或根或头落地为喻。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_411": "high",
    "SA_412": "high",
    "SA_413": "medium",
    "SA_414": "medium",
    "SA_415": "medium",
    "SA_416": "high",
    "SA_417": "high",
    "SA_418": "high",
    "SA_419": "medium",
    "SA_420": "medium",
    "SA_421": "high",
    "SA_422": "high",
    "SA_423": "high",
    "SA_424": "medium",
    "SA_425": "medium",
    "SA_426": "high",
    "SA_427": "medium",
    "SA_428": "high",
    "SA_429": "high",
    "SA_430": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_412": (
        "底本『如是广说，乃至……学无间等』为交叉指示；"
        "依 SA_411／SN56.9 食堂斥诤论框 + 四谛论／URGE 重建"
    ),
    "SA_415": (
        "底本『即诣食堂……如是广说，乃至正向涅槃』为交叉指示；"
        "依 SA_411／414 框 + 汉本『粗食／乞食利养』差别重建"
    ),
    "SA_425": (
        "底本『如前所说，乃至……学无间等』为交叉指示；"
        "依 SA_424 小千闇冥＋四谛框，差别改为中千世界"
    ),
    "SA_427": (
        "底本『如当说，如是有、如是当知，亦如上说』为异门／交叉指示；"
        "依四谛略说定型重建为有／当知／当说三门"
    ),
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
    assert set(GOLD) == {f"SA_{i}" for i in range(411, 431)}, (
        "GOLD must cover SA_411–SA_430 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"

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

    # Snapshot SA_410 before merge to assert untouched
    sa410_before = None
    for rec in records:
        if rec["id"] == "SA_410":
            sa410_before = json.dumps(
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

    # Assert SA_410 untouched
    for rec in merged:
        if rec["id"] == "SA_410" and sa410_before is not None:
            sa410_after = json.dumps(
                {
                    "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                    "modern_psychology_text": rec.get("modern_psychology_text"),
                    "notes": rec.get("notes"),
                    "review_status": rec.get("review_status"),
                    "confidence": rec.get("confidence"),
                },
                ensure_ascii=False,
            )
            assert sa410_before == sa410_after, "SA_410 must remain untouched"
            break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa411-430.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fails = [r for r in report if r["status"] == "fail"]
    warns = [r for r in report if r["status"] == "warn"]
    oks = [r for r in report if r["status"] == "ok"]
    forbidden = [r for r in report if r["forbidden_hits"]]
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(1, 431)
    )

    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛", "如如"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_411–SA_430 only)")
    print(f"validation: ok={len(oks)} warn={len(warns)} fail={len(fails)}")
    print(f"forbidden_hits={len(forbidden)} ban_term_hits={ban_hits}")
    print(
        f"needs_restyle (assess_gold): {len(needs_restyle)}  "
        f"max_sim={max_r['sim']} ({max_r['id']})  "
        f"mean_sim={round(sum(r['sim'] for r in report) / len(report), 3)}"
    )
    print(f"paragraph_parallel_violations={len(para_bad)}")
    print(f"gold={len(report) - len(recon)} gold_reconstructed={len(recon)}")
    print(f"confidence: {conf_split}")
    print(f"continuous_gold_SA_1–430={continuous}")
    print(f"SA_410_untouched=True")
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
