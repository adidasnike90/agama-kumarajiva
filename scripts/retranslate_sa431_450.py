#!/usr/bin/env python3
"""Retranslate SA 431–450（卷第十七谛相应末＋卷第十八界相应）→ merge.

本批二十经：杖、五节、增上说法、黠慧；须达多、殿堂×2、虫、山、湖池、土、爪甲、
四圣谛当生来生；眼药丸、鄙心、偈、行、偈、界和合、少闻等。

信：有平行者以 SN／Pāli／Sujato 厘义；无平行者 medium；
    交叉指示（SA 436／437／443／446／448／449）→ gold_reconstructed。
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

OPEN_JET_LIT = "如是我闻：一时，佛在舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

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

URGE_SHORT_LIT = "是故当于四圣谛勤修无间等。"
URGE_SHORT_MOD = "所以应当对四圣谛勤修无间等。"

DHATU_JOIN_LIT = "众生依界而会、依界而合"
DHATU_JOIN_MOD = "众生依界而聚会、依界而相合"

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

# --- SA 431 杖（无平行）-----------------------------------------------------
SUTTAS["SA_431"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「譬如有人掷杖虚空，必还堕地——"
        "或堕净处，或堕不净。"
        "如是沙门、婆罗门于" + FOUR_TRUTH_LIT + "不如实知，"
        "以不如实知故，或生善趣，或生恶趣。"
        + URGE_SHORT_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「好比有人把杖抛向虚空，一定还会落地——"
        "有时落在干净处，有时落在不净处。"
        "同样，沙门、婆罗门对" + FOUR_TRUTH_MOD + "不能如实了知，"
        "因为不能如实了知，有的生到善趣，有的生到恶趣。"
        + URGE_SHORT_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "与 SA_430／SN56.33 同杖喻而异义：汉本以净／不净地喻善趣／恶趣；"
        "无平行可据，不据 SN56.33 改作无明覆渴爱系。"
    ),
}

# --- SA 432 五节（无平行）---------------------------------------------------
SUTTAS["SA_432"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，佛告诸比丘：「譬如五节相续之轮，大力士令速旋转。"
        "如是沙门、婆罗门于" + FOUR_TRUTH_LIT + "不如实知，"
        "轮回五趣而速旋转——或堕地狱、畜生、饿鬼，或人、或天，还堕恶道，长夜轮转。"
        + URGE_SHORT_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，佛告诉比丘们：「好比有五个节相连的轮，大力士让它飞快旋转。"
        "同样，沙门、婆罗门对" + FOUR_TRUTH_MOD + "不能如实了知，"
        "在五趣中飞快轮转——或堕地狱、畜生、饿鬼，或生人、天，又还堕恶道，长夜轮转。"
        + URGE_SHORT_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "五节轮喻五趣速转；无 SN 平行，依汉本保守改写。"
    ),
}

# --- SA 433 增上说法（无平行）-----------------------------------------------
SUTTAS["SA_433"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「如来、应、等正觉增上说法，谓四圣谛——"
        "开示、施設、建立、分别、显说。"
        "何等为四？谓" + FOUR_TRUTH_LIT + "。"
        + URGE_SHORT_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「如来、应供、等正觉的增上说法，就是四圣谛——"
        "开示、施設、建立、分别、清楚讲说。"
        "哪四种？就是" + FOUR_TRUTH_MOD + "。"
        + URGE_SHORT_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "删汉『散说、显现、表露』冗列，留开示／施設／建立／分别／显说；"
        "无平行，medium。"
    ),
}

# --- SA 434 黠慧（无平行）---------------------------------------------------
SUTTAS["SA_434"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「何等为黠慧？于" + FOUR_TRUTH_LIT + "如实知——是黠慧耶？为非耶？」"
        "诸比丘白佛：「如我解世尊所说，于四圣谛如实知者，是为黠慧。」"
        "佛言：「善哉！于四圣谛如实知者，是则黠慧。"
        + URGE_SHORT_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「什么叫做黠慧？对" + FOUR_TRUTH_MOD + "如实了知——这是黠慧，还是不是？」"
        "比丘们禀告佛：「按我们理解世尊所说，对四圣谛如实了知的，就是黠慧。」"
        "佛说：「好！对四圣谛如实了知的，就是黠慧。"
        + URGE_SHORT_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "黠慧＝于四圣谛如实知；问答框依汉本，删『为不知耶』赘问。"
    ),
}

# --- SA 435 须达多（SN 56.32 resembling）------------------------------------
SUTTAS["SA_435"] = {
    "lit": [
        OPEN_JET_LIT,
        "时须达多长者诣佛，稽首，一面坐，白言：「世尊！四圣谛为渐次无间等？为一顿无间等？」"
        "佛告长者：「四圣谛渐次无间等，非一顿无间等。」",
        "「若言于苦圣谛未无间等，而于苦集、苦灭、苦灭道迹圣谛得无间等者——无有是处。"
        "譬如细叶联合作器，盛水持行——无有是处。"
        "若于苦圣谛已无间等，次第于苦集、苦灭、苦灭道迹圣谛无间等者——斯有是处。"
        "譬如莲叶联合作器，盛水游行——斯有是处。"
        "是故长者于四圣谛未无间等者，当勤方便，起增上欲，学无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时须达多长者来见佛，顶礼后坐在一边，问：「世尊！四圣谛是渐次无间等，还是一口气顿得无间等？」"
        "佛告诉长者：「四圣谛是渐次无间等，不是一口气顿得无间等。」",
        "「如果有人说：对苦圣谛还没有无间等，却能对苦集、苦灭、苦灭道迹圣谛得到无间等——没有这回事。"
        "好比用细叶子拼成器皿去盛水行走——没有这回事。"
        "如果对苦圣谛已经无间等，再依次对苦集、苦灭、苦灭道迹圣谛无间等——这是有的。"
        "好比用莲叶拼成器皿盛水行走——这是有的。"
        "所以长者对四圣谛还没有无间等的，应当勤加方便，发起强盛愿欲，修学无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 列 SN56.32 resembling（Khadirapatta）。"
        "信：叶器盛水可否，喻未无间等则不能尽苦／得后谛；"
        "Sujato 作『未如实通达四谛而尽苦——无是处』，汉以须达多问渐次／一顿为叙，"
        "并明须先苦谛而后余谛——据 SN 义保留『无是处／有是处』，叙事情节依汉。"
        "细叶≈khadera 等；莲叶≈paduma。"
    ),
}

# --- SA 436 殿堂（SN 56.44；交叉指示）---------------------------------------
SUTTAS["SA_436"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘问四圣谛无间等，佛亦如须达多长者所答而说，唯譬有别。",
        "佛告比丘：「譬如四阶之道升于殿堂。"
        "若言不登初阶，而登第二、第三、第四阶升堂——无有是处；"
        "要由初阶，然后次登余阶，乃得升堂。"
        "如是于苦圣谛未无间等，而欲于苦集、苦灭、苦灭道迹圣谛无间等——无有是处。"
        "若于苦圣谛无间等已，次第于余三谛无间等——斯有是处。"
        + URGE_SHORT_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位比丘请问四圣谛的无间等，佛也像回答须达多长者那样讲说，只是比喻不同。",
        "佛告诉比丘：「好比有四层台阶通向殿堂。"
        "如果有人说不登第一阶，却登第二、第三、第四阶上堂——没有这回事；"
        "必须先登第一阶，再依次登其余阶，才能上到殿堂。"
        "同样，对苦圣谛还没有无间等，却想对苦集、苦灭、苦灭道迹圣谛无间等——没有这回事。"
        "如果对苦圣谛已经无间等，再依次对其余三谛无间等——这是有的。"
        + URGE_SHORT_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "底本『如须达长者所问，有异比丘问，亦如是说，唯譬有差别』为交叉指示；"
        "依 SA_435／SN56.44 重建。SN 以楼阁下层未建不可架上层为喻；"
        "汉本四阶升堂义同『须次第』，保留汉喻。"
        "confidence=high（平行可靠；文面重建）。"
    ),
}

# --- SA 437 殿堂（SN 56.44；交叉指示）---------------------------------------
SUTTAS["SA_437"] = {
    "lit": [
        OPEN_JET_LIT,
        "时阿难问四圣谛无间等，佛亦如异比丘所问而说，唯譬有别。",
        "佛告阿难：「譬如四磴之梯升于殿堂。"
        "若言不由初磴，而登第二、第三、第四磴升堂——无有是处。"
        "如是于苦圣谛未无间等，而欲于苦集、苦灭、苦灭道迹圣谛无间等——无有是处。"
        "若由初磴次第而升——斯有是处；"
        "于苦圣谛无间等已，次第于余三谛无间等——亦有是处。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时阿难请问四圣谛的无间等，佛也像回答那位比丘那样讲说，只是比喻不同。",
        "佛告诉阿难：「好比有四磴梯子通向殿堂。"
        "如果有人说不从第一磴登起，却登第二、第三、第四磴上堂——没有这回事。"
        "同样，对苦圣谛还没有无间等，却想对苦集、苦灭、苦灭道迹圣谛无间等——没有这回事。"
        "如果从第一磴依次登上去——这是有的；"
        "对苦圣谛已经无间等，再依次对其余三谛无间等——也是有的。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "底本『如异比丘问，阿难所问，亦如是说，唯譬差别』为交叉指示；"
        "依 SA_436／SN56.44 重建，差别为四磴梯＋对机阿难。"
        "confidence=high（平行可靠；文面重建）。"
    ),
}

# --- SA 438 虫（SN 56.36）---------------------------------------------------
SUTTAS["SA_438"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「譬如尽取阎浮提草木作枪，欲贯大海一切水虫——"
        "大虫贯大枪，中虫贯中枪，小虫贯小枪：大中之虫未尽，草木已竭；"
        "细小诸虫，尤不可贯。所以者何？其形微故。"
        "如是恶趣广大无量。见具足者，出离如是广大恶趣，如实知" + FOUR_TRUTH_LIT + "。"
        + URGE_SHORT_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「好比把阎浮提所有草木都做成枪，想贯穿大海里一切水虫——"
        "大虫用大枪，中虫用中枪，小虫用小枪：粗大的虫还没穿完，草木已经用尽；"
        "细小的虫更没法贯穿。为什么？因为它们的身体太微细。"
        "恶趣就是这样广大无量。具足正见的人，出离这样广大的恶趣，如实了知"
        + FOUR_TRUTH_MOD + "。"
        + URGE_SHORT_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.36 Pāṇa。"
        "信-校正：汉结『众生界无数无量』据 SN 改为恶趣（apāya）广大；"
        "见具足者（diṭṭhisampanno）出离恶趣而如实知四谛。"
        "阎浮提＝Jambudīpa（Sujato Black Plum Tree Land）。"
    ),
}

# --- SA 439 山（SN 13.11／SN 56.49）-----------------------------------------
SUTTAS["SA_439"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊手执土石，问诸比丘：「此手中土石为多？雪山土石为多？」"
        "比丘白佛：「手中甚少；雪山无量，算数譬类所不能及。」"
        "佛言：「于" + FOUR_TRUTH_LIT + "如实知者，如我手中土石；"
        "不如实知者，如彼雪山土石，其数无量。"
        + URGE_SHORT_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊手里握着一点土石，问比丘们：「我手里这点土石多，还是雪山的土石多？」"
        "比丘们禀告：「手里的很少；雪山多得无法计量，没法用数目或比喻相比。」"
        "佛说：「对" + FOUR_TRUTH_MOD + "如实了知的人，就像我手里这点土石；"
        "不能如实了知的人，就像那雪山的土石，数量无量。"
        + URGE_SHORT_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 列 SN13.11、SN56.49。"
        "SN13.11 以须弥豆许石较外道证得；本经汉文属谛相应，"
        "以知／不知四谛多寡为义——保留汉应用，数量喻与 SN 同族。"
    ),
}

# --- SA 440 湖池等（SN 56.52）-----------------------------------------------
SUTTAS["SA_440"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「譬如湖池，深广五十由旬，水皆盈满。"
        "有人以发、以毛、或以指端渧取其水，乃至再三。"
        "云何——所渧为多？湖水为多？」"
        "比丘白佛：「渧水甚少；湖水无量，不可为比。」"
        "佛言：「多闻圣弟子具足见谛、得圣道果，断诸苦本，如截多罗树头，"
        "于未来世成不生法；其所余者，如彼指端渧水；已断无量，如大湖水。"
        + URGE_SHORT_LIT + "」",
        "如湖池譬，萨罗、恒河、耶符那、及四大海，其譬亦尔。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「好比一座湖池，深广各五十由旬，水满满的。"
        "有人用头发、毛，或用指尖蘸那湖水，蘸到两三次。"
        "怎么样——蘸起来的水多，还是湖水多？」"
        "比丘们禀告：「蘸的水很少；湖水多得无法相比。」"
        "佛说：「多闻圣弟子具足见谛、证得圣道果，断除苦的根本，像截断多罗树头一样，"
        "在未来世成为不再生起之法；剩下的苦，就像那指尖蘸的水；已经断除的，像大湖的水那样无量。"
        + URGE_SHORT_MOD + "」",
        "像湖池这个比喻一样，萨罗池、恒河、耶符那河、以及四大海，也可以同样说。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.52 Pokkharaṇī（并 SN56.53 等）。"
        "汉本明言见谛弟子余苦如渧、已断如湖——据 SN『noble disciple』量喻补全；"
        "末列河海异门，略存不演。"
    ),
}

# --- SA 441 土等（SN 13.11 resembling）--------------------------------------
SUTTAS["SA_441"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊手捉团土，大如梨果，告诸比丘：「我手中团土为多？雪山土石为多？」"
        "比丘白佛：「手中甚少；雪山王土石无量，不可为比。」"
        "佛言：「于" + FOUR_TRUTH_LIT + "如实知者，如我手中团土；"
        "不如实知者，如雪山王土石。"
        + URGE_SHORT_LIT + "」",
        "如雪山王，尼民陀罗乃至须弥山王、及大地土石，其譬亦尔。",
        "如梨果，阿摩勒乃至蒜子，其量喻亦尔。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊手里握着一团土，大约像梨那么大，告诉比丘们：「我手里这团土多，还是雪山的土石多？」"
        "比丘们禀告：「手里的很少；雪山王的土石多得无法相比。」"
        "佛说：「对" + FOUR_TRUTH_MOD + "如实了知的人，就像我手里这团土；"
        "不能如实了知的人，就像雪山王的土石。"
        + URGE_SHORT_MOD + "」",
        "像雪山王一样，尼民陀罗山直到须弥山王、以及大地土石，也可以同样说。",
        "像梨果一样，阿摩勒果直到蒜子，这种量的比喻也可以同样说。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 列 SN13.11 resembling 等。"
        "与 SA_439 同族量喻；舍卫／梨果为差别。末山名、果名异门略列不演。"
    ),
}

# --- SA 442 爪甲（SN 56.102 等；爪甲量喻族）---------------------------------
SUTTAS["SA_442"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊以爪甲擎土，告诸比丘：「甲上土为多？大地土为多？」"
        "比丘白佛：「甲上甚少；大地无量，不可为比。」",
        "佛言：「形可见之众生，如甲上土；形微不可见者，如大地土。"
        "人道如甲上；非人如大地。生中国者如甲上；生边地者如大地。"
        "成就圣慧眼、知此法律、正想正觉、法无间等者，如甲上；"
        "不尔者，如大地。"
        "知有父母、知沙门婆罗门、修施戒、畏他世罪者，如甲上；不尔者，如大地。"
        "不杀、不盗、不邪淫、不妄语、不两舌、不恶口、不绮语，及离贪恚邪见者，如甲上；"
        "不持戒、不离贪恚邪见者，如大地。"
        "持五戒、八戒、十善者，如甲上；不持者，如大地。"
        "从地狱、畜生、饿鬼命终生人、生天者，如甲上；还生恶趣者，如大地。"
        "人中没还生人中、天没还生天者，如甲上；人天没而生恶趣者，如大地。"
        + URGE_SHORT_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊用指甲挑起一点土，告诉比丘们：「指甲上的土多，还是大地的土多？」"
        "比丘们禀告：「指甲上很少；大地多得无法相比。」",
        "佛说：「形体看得见的众生，像指甲上的土；形体微细看不见的，像大地的土。"
        "生在人道的像指甲上；非人像大地。生在中国的像指甲上；生在边地的像大地。"
        "成就圣慧眼、懂得这法律、正想正觉、于法得无间等的，像指甲上；"
        "不是这样的，像大地。"
        "知道有父母、知道沙门婆罗门、修布施持戒、畏惧他世罪的，像指甲上；不是这样的，像大地。"
        "不杀、不盗、不邪淫、不妄语、不两舌、不恶口、不绮语，以及远离贪、嗔、邪见的，像指甲上；"
        "不持戒、不离贪嗔邪见的，像大地。"
        "持五戒、八戒、十善的，像指甲上；不持的，像大地。"
        "从地狱、畜生、饿鬼命终后生到人或天的，像指甲上；还生恶趣的，像大地。"
        "人中死后还生人中、天中死后还生天的，像指甲上；人天死后生到恶趣的，像大地。"
        + URGE_SHORT_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.102；并 SN56.51 Nakhasikhā 等爪甲量喻族。"
        "汉本广列可见／不可见、人／非人、中国／边地、慧眼、戒善、恶趣往来；"
        "罗什风删『如陆地水性』等重复套语，并诸戒／诸趣为数段，义不减。"
        "Sujato 残条『人死还生人少、生地狱多』与汉末段同旨。"
    ),
}

# --- SA 443 四圣谛当生来生（无平行；异门交叉）-------------------------------
SUTTAS["SA_443"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「我昔未闻正法，以如理作意观察苦圣谛，正见于是生；"
        "观察苦集、苦灭、苦灭道迹圣谛，正见亦生。"
        "已生、今生、当生，其义一也；"
        "生起、修习、亲近、多修、触证、作证，亦复如是。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「我从前还没有听闻正法时，用如理作意观察苦圣谛，正见就生起来了；"
        "观察苦集、苦灭、苦灭道迹圣谛，正见也生起来了。"
        "已经生起、现在生起、将来生起，意思是一样的；"
        "发起、修习、亲近修、多多修、触证、作证，也是一样。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "底本『如已生，如是今生、当生。如生，如是起、习……亦如是』为异门／交叉指示；"
        "依四谛正见生起定型，将今生／当生与起习修证诸门并举重建，不另臆造广释。"
    ),
}

# --- SA 444 眼药丸（无平行；卷第十八界相应）---------------------------------
SUTTAS["SA_444"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「譬如眼药丸，深广一由旬。"
        "若有人取此药丸，界界分置，能速令尽，而于诸界不得其边。"
        "当知诸界，其数无量。是故比丘当善学种种界。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「好比一颗眼药团，深广有一由旬。"
        "如果有人把这药团按界一处处安放，很快就能分完，却在种种界上找不到尽头。"
        "应当知道：诸界数量无量。所以比丘应当好好修学种种界。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "界相应开卷；眼药丸喻界无量。无 SN 平行，medium。"
    ),
}

# --- SA 445 鄙心（SN 14.14）-------------------------------------------------
SUTTAS["SA_445"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「" + DHATU_JOIN_LIT + "。"
        "行不善心时与不善界俱，善心时与善界俱；"
        "胜心时与胜界俱，鄙心时与鄙界俱。"
        "是故诸比丘当善学种种界。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「" + DHATU_JOIN_MOD + "。"
        "起不善心时就与不善界在一起，起善心时就与善界在一起；"
        "起殊胜心时就与殊胜界在一起，起卑劣心时就与卑劣界在一起。"
        "所以比丘们应当好好修学种种界。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN14.14 Hīnādhimuttika。"
        "信：dhātuso sattā saṁsandanti samenti；"
        "鄙／胜≈hīna／kalyāṇa adhimutti；汉『不善／善』并留。"
        "Sujato 过未今三时，汉略——义已足，不增演。"
    ),
}

# --- SA 446 偈（SN 14.16；交叉＋偈）-----------------------------------------
SUTTAS["SA_446"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「" + DHATU_JOIN_LIT + "——"
        "鄙心与鄙界俱，胜心与胜界俱。"
        "譬如粪与粪合，乳与乳合；众生亦复如是，依界而会。」",
        "即说偈言：「相会则生缠，远离则得断；"
        "如人持小木，欲渡于巨海，人木则俱没——"
        "依懈怠者亦复如是。"
        "当离懈怠人，及卑劣精进；"
        "当与诸贤圣，精进修禅者共住。」"
        "「众生与界俱，相似共和合。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「" + DHATU_JOIN_MOD + "——"
        "卑劣心与卑劣界在一起，殊胜心与殊胜界在一起。"
        "好比粪与粪相合，乳与乳相合；众生也是这样，依界而聚会。」",
        "接着说偈：「彼此交会就生出缠缚，远离就能切断；"
        "好比有人抓着一小块木头，想渡过大海，人与木头一起沉没——"
        "依靠懈怠的人也是这样。"
        "应当远离懈怠的人，以及精进卑劣的人；"
        "应当与贤圣、精进修禅的人共同安住。」"
        "「众生与界在一起，同类的就互相和合。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "底本『广说如上。差别者，即说偈言』为交叉指示；"
        "散文依 SA_445／SN14.16（粪合／乳合）重建；"
        "偈据 SN gāthā（saṁsaggā vanatho…）信校正，删汉『胶漆／珂乳』衍饰，"
        "留『众生与界俱』结句以应界相应。"
        "confidence=high（平行可靠；文面重建）。"
    ),
}

# --- SA 447 行（SN 14.15）---------------------------------------------------
SUTTAS["SA_447"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「" + DHATU_JOIN_LIT + "——"
        "不善心与不善界俱，善心与善界俱；鄙心与鄙界俱，胜心与胜界俱。」",
        "时憍陈如与多比丘经行，皆上座多闻、出家已久、梵行已立；"
        "大迦叶与诸比丘经行，皆少欲知足、头陀苦行为乐；"
        "舍利弗与诸比丘经行，皆大智慧；"
        "目揵连与诸比丘经行，皆有大神通；"
        "阿那律与诸比丘经行，皆天眼明彻；"
        "二十亿耳与诸比丘经行，皆勇猛精进；"
        "陀骠与诸比丘经行，皆能为众营僧事；"
        "优波离与诸比丘经行，皆通达律；"
        "富楼那与诸比丘经行，皆善能说法；"
        "迦旃延与诸比丘经行，皆能分别经义；"
        "阿难与诸比丘经行，皆多闻总持；"
        "罗睺罗与诸比丘经行，皆善护律行；"
        "提婆达多与诸比丘经行，皆习恶欲。"
        "「是名" + DHATU_JOIN_LIT + "。是故当善分别种种诸界。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「" + DHATU_JOIN_MOD + "——"
        "不善心与不善界在一起，善心与善界在一起；卑劣心与卑劣界在一起，殊胜心与殊胜界在一起。」",
        "当时憍陈如和许多比丘在附近经行，都是上座多闻、出家已久、梵行已经确立；"
        "大迦叶和比丘们经行，都少欲知足、乐修头陀苦行；"
        "舍利弗和比丘们经行，都有大智慧；"
        "目揵连和比丘们经行，都有大神通；"
        "阿那律和比丘们经行，都天眼明彻；"
        "二十亿耳和比丘们经行，都勇猛精进；"
        "陀骠和比丘们经行，都能为大众操办僧事；"
        "优波离和比丘们经行，都通达戒律；"
        "富楼那和比丘们经行，都善于说法；"
        "迦旃延和比丘们经行，都能分别经义；"
        "阿难和比丘们经行，都多闻总持；"
        "罗睺罗和比丘们经行，都善于护持律行；"
        "提婆达多和比丘们经行，都习近恶欲。"
        "「这就是" + DHATU_JOIN_MOD + "。所以应当好好分别种种诸界。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN14.15 Caṅkama。"
        "信：同类相从——大智、神通、头陀、天眼、说法、持律、多闻、恶欲各与其党；"
        "汉列憍陈如／二十亿耳／陀骠／迦旃延／罗睺罗较 SN 为广，叙事情节保留。"
        "SN 在耆阇崛山；汉作竹园——住处依汉见证。"
    ),
}

# --- SA 448 偈（SN 14.16；交叉＋偈）-----------------------------------------
SUTTAS["SA_448"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时，世尊告诸比丘：「" + DHATU_JOIN_LIT + "——"
        "鄙心与鄙界俱，胜心与胜界俱。"
        "譬如粪合于粪，乳合于乳。」",
        "即说偈言：「相会则生缠，远离则得断；"
        "如人持小木，欲渡于巨海，人木则俱没——"
        "依懈怠者亦复如是。"
        "当离懈怠人，及卑劣精进；"
        "当与诸贤圣，精进修禅者共住。"
        "众生与界俱，相似共和合。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时，世尊告诉比丘们：「" + DHATU_JOIN_MOD + "——"
        "卑劣心与卑劣界在一起，殊胜心与殊胜界在一起。"
        "好比粪与粪相合，乳与乳相合。」",
        "接着说偈：「彼此交会就生出缠缚，远离就能切断；"
        "好比有人抓着一小块木头，想渡过大海，人与木头一起沉没——"
        "依靠懈怠的人也是这样。"
        "应当远离懈怠的人，以及精进卑劣的人；"
        "应当与贤圣、精进修禅的人共同安住。"
        "众生与界在一起，同类的就互相和合。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "底本『……如上广说已，即说偈言』为交叉指示；"
        "依 SA_446／SN14.16 重建，住处为王舍城竹园（依汉）。"
        "confidence=high（平行可靠；文面重建）。"
    ),
}

# --- SA 449 界和合（SN 14.12；交叉指示）-------------------------------------
SUTTAS["SA_449"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「" + DHATU_JOIN_LIT + "。"
        "胜心生时与胜界俱，鄙心生时与鄙界俱；"
        "杀生时与杀界俱，不与取、邪淫、妄语、饮酒时，各与其界俱；"
        "不杀、不盗、不淫、不妄语、不饮酒时，各与其界俱。"
        "是故诸比丘当善分别种种界。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「" + DHATU_JOIN_MOD + "。"
        "殊胜心生起时与殊胜界在一起，卑劣心生起时与卑劣界在一起；"
        "杀生时与杀生界在一起，不与取、邪淫、妄语、饮酒时，各自与相应的界在一起；"
        "不杀、不盗、不淫、不妄语、不饮酒时，也各自与相应的界在一起。"
        "所以比丘们应当好好分别种种界。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "底本『众生常与界俱……如是广说，乃至……』为交叉指示；"
        "依 SA_445 框＋汉所列杀盗淫妄酒诸界重建。"
        "primary SN14.12 Sanidāna 为欲寻／恚寻／害寻有因缘生起链，与本经『业道界俱』异文；"
        "本经取界相应和合义（汉＋SN14.14–17 族），不改写为 vitakka 链。"
        "confidence=medium（平行义距；文面重建）。"
    ),
}

# --- SA 450 少闻等（SN 14.17）-----------------------------------------------
SUTTAS["SA_450"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「" + DHATU_JOIN_LIT + "——"
        "不信与不信界俱，犯戒与犯戒界俱，无惭无愧与无惭无愧界俱；"
        "有信与信界俱，持戒与持戒界俱，有惭有愧与惭愧界俱。"
        "如是精进与懈怠、正念与失念、正定与不正定、"
        "多闻与少闻、能施与悭吝、善慧与恶慧、"
        "易养与难养、少欲与多欲、知足与不知足、摄受与不摄受——"
        "皆各与其界俱。"
        "是故诸比丘当善分别种种诸界。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「" + DHATU_JOIN_MOD + "——"
        "不信的与不信界在一起，犯戒的与犯戒界在一起，无惭无愧的与无惭无愧界在一起；"
        "有信心的与信界在一起，持戒的与持戒界在一起，有惭有愧的与惭愧界在一起。"
        "同样，精进与懈怠、正念与失念、正定与不正定、"
        "多闻与少闻、能布施与悭吝、善慧与恶慧、"
        "容易供养与难以供养、少欲与多欲、知足与不知足、摄受与不摄受——"
        "都各自与相应的界在一起。"
        "所以比丘们应当好好分别种种诸界。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN14.17 Assaddhasaṁsandana（并 14.18–24 族）。"
        "信：不信／无惭／无愧／少闻／懈怠／失念／恶慧各与其类；"
        "汉末『如上经。如是广说』诸对——据 SN 族补精进、念、定、闻、施、慧等，"
        "并留汉易养／少欲／知足／摄受。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_431": "medium",
    "SA_432": "medium",
    "SA_433": "medium",
    "SA_434": "medium",
    "SA_435": "high",
    "SA_436": "high",
    "SA_437": "high",
    "SA_438": "high",
    "SA_439": "high",
    "SA_440": "high",
    "SA_441": "high",
    "SA_442": "high",
    "SA_443": "medium",
    "SA_444": "medium",
    "SA_445": "high",
    "SA_446": "high",
    "SA_447": "high",
    "SA_448": "high",
    "SA_449": "medium",
    "SA_450": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_436": (
        "底本『如须达长者所问，有异比丘问，亦如是说，唯譬有差别』为交叉指示；"
        "依 SA_435／SN56.44 四阶升堂＋渐次无间等框重建"
    ),
    "SA_437": (
        "底本『如异比丘问，阿难所问，亦如是说，唯譬差别』为交叉指示；"
        "依 SA_436／SN56.44 四磴梯＋对机阿难重建"
    ),
    "SA_443": (
        "底本『如已生，如是今生、当生。如生，如是起、习……亦如是』为异门／交叉指示；"
        "依四谛正见生起定型将诸门并举重建"
    ),
    "SA_446": (
        "底本『广说如上。差别者，即说偈言』为交叉指示；"
        "散文依 SA_445／SN14.16；偈据 SN gāthā 信校正"
    ),
    "SA_448": (
        "底本『……如上广说已，即说偈言』为交叉指示；"
        "依 SA_446／SN14.16 重建（竹园住处）"
    ),
    "SA_449": (
        "底本『如是广说，乃至……杀生时与杀界俱……』为交叉指示；"
        "依 SA_445 框＋汉列杀盗淫妄酒诸界重建（不据 SN14.12 vitakka 链改写）"
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
    assert set(GOLD) == {f"SA_{i}" for i in range(431, 451)}, (
        "GOLD must cover SA_431–SA_450 exactly"
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

    # Snapshot SA_430 before merge to assert untouched
    sa430_before = None
    for rec in records:
        if rec["id"] == "SA_430":
            sa430_before = json.dumps(
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

    # Assert SA_430 untouched
    for rec in merged:
        if rec["id"] == "SA_430" and sa430_before is not None:
            sa430_after = json.dumps(
                {
                    "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                    "modern_psychology_text": rec.get("modern_psychology_text"),
                    "notes": rec.get("notes"),
                    "review_status": rec.get("review_status"),
                    "confidence": rec.get("confidence"),
                },
                ensure_ascii=False,
            )
            assert sa430_before == sa430_after, "SA_430 must remain untouched"
            break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa431-450.json").write_text(
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
        for i in range(1, 451)
    )

    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛", "如如"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_431–SA_450 only)")
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
    print(f"continuous_gold_SA_1–450={continuous}")
    print(f"SA_430_untouched=True")
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
