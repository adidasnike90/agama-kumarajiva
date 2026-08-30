#!/usr/bin/env python3
"""Retranslate SA 1111–1130（帝释相应末–不坏净相应）→ merge.

本批二十经：
1111–1120 帝释相应（敬佛／法／僧 SN11.19–20／18、须毘罗 SN11.1、仙人 SN11.10／9、
         灭瞋 SN11.21、月八日 AN3.37–38、病 SN11.23、婆稚 SN11.8、持一戒 SN11.7）
1121–1130 不坏净相应（释氏 AN10.46、疾病 SN55.54、菩提 SN55.48、往生 SN55.36、
         须陀恒×2 SN55.50／46、四法 SN55.2、四果×2、行住坐卧）

信：有 SN／AN 平行者据巴利／Sujato 厘义；1122 汉「三种穌息」据 SN55.54 校正为四不坏净；
    1112／1127／1130 peyyāla 据邻经／平行补纲。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_1111–1130；不触碰 SA_1091–1110／SA_1131+（并行批次）。
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

batch_range = range(1111, 1131)

# ---------------------------------------------------------------------------
# 共用框式
# ---------------------------------------------------------------------------

OPEN_JET_LIT = "如是我闻：一时，佛住舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_KAP_LIT = "如是我闻：一时，佛住迦毗罗卫国尼拘律园中。"
OPEN_KAP_MOD = "我是这样听说的：有一次，佛住在迦毗罗卫国尼拘律园中。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY_MOD = "他们听佛所说，欢喜随喜，作礼离去。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

FOUR_CONF_LIT = "于佛不坏净、于法不坏净、于僧不坏净、圣戒成就"
FOUR_CONF_MOD = "对佛不坏净、对法不坏净、对僧不坏净，以及圣戒成就"

SAKKA_EXHORT_LIT = (
    "彼天帝释于三十三天为自在王，尚能如是；"
    "汝等正信非家、出家学道，亦当如是学。"
)
SAKKA_EXHORT_MOD = (
    "那位天帝释在三十三天已是自在之王，尚且如此；"
    "你们正信舍家、出家学道，也应当这样学。"
)

SUTTAS: dict[str, dict] = {}

# --- SA 1111 敬佛（SN11.19）-------------------------------------------------
SUTTAS["SA_1111"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「过去世时，释提桓因欲入园观，勅御者严驾千马之车。"
        "御者白言：『俱尸迦！驾已办，唯王知时。』"
        "帝释下常胜殿，东向合掌礼佛。御者见已，心惊毛竖，马鞭落地。」",
        "「帝释问：『汝见何忧怖，乃落马鞭？』"
        "御者白：『大王为舍脂之夫，人天大小王、四护世、三十三天众皆礼于王；"
        "何处更有尊于帝释者，而今东向合掌？故我怖畏。』」",
        "「帝释答：『我于世间大小王及三十三天实为尊主，故彼来敬；"
        "然复有世间等正觉、名号满天师，是故我稽首礼。』"
        "御者言：『是必世间胜，故天王合掌东向；我今亦当礼天王所礼者。』"
        "帝释礼佛已，乘千马车往诣园观。」",
        "「诸比丘！帝释尚恭敬佛、赞叹敬佛；汝等亦应恭敬于佛，赞叹恭敬佛者。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「过去世时，天帝释想去园中游览，吩咐御者备好千马之车。"
        "御者回报：『俱尸迦！车已备好，请大王看着时辰。』"
        "帝释走下常胜殿，面向东方合掌礼佛。御者看见，吓得汗毛直竖，马鞭掉落。」",
        "「帝释问：『你看见什么可怕的事，才把马鞭掉了？』"
        "御者说：『大王是舍脂的丈夫，人间天上大小王、四大天王、三十三天众都向您敬礼；"
        "哪里还有比帝释更尊贵的，您却向东合掌？所以我害怕。』」",
        "「帝释答：『我对世间大小王和三十三天确实是尊主，所以他们来敬；"
        "但世间还有等正觉、名号圆满的天人师，因此我向他稽首。』"
        "御者说：『那一定是世间最胜，所以天王合掌向东；我也应当礼天王所礼的那位。』"
        "帝释礼佛后，乘千马车去园中游览。」",
        "「比丘们！帝释尚且恭敬佛、赞叹敬佛；你们也应当恭敬佛，赞叹恭敬佛的人。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN11.19 Satthāravandanā；"
        "帝释东向礼佛，御者惊怖，偈问答后同礼；结劝出家众亦应敬佛。"
        "巴利另含礼阿罗汉／有学，汉题「敬佛」以佛为主，从汉略。"
    ),
}

# --- SA 1112 敬法（SN11.18；汉 peyyāla＋偈）---------------------------------
SUTTAS["SA_1112"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「过去世时，释提桓因欲入园观，勅御者严驾千马之车。"
        "御者白：『驾已办，唯王知时。』帝释下常胜殿，东向合掌敬礼尊法。"
        "御者心惊，问何故有尊过于天王者。」",
        "「帝释说偈：『人天大小王、四护世、三十三众皆礼于我；"
        "然复有持净戒、长夜入正受、正信出家究竟梵行者，我于彼恭敬；"
        "调伏贪恚、超越愚痴、修学不放逸者，亦礼之；"
        "贪瞋痴尽、漏尽阿罗汉，复应敬礼；"
        "若在家奉持净戒、如法布萨，亦应敬礼。』」",
        "「御者言：『是必世间胜，故天王敬礼；我亦随天王恭敬。』"
        "帝释敬礼法已，乘车往园观。」",
        "「诸比丘！帝释尚敬礼法、赞叹礼法；汝等亦当敬礼法，赞叹礼法者。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「过去世时，天帝释想去园中游览，吩咐御者备好千马之车。"
        "御者回报车已备好。帝释走下常胜殿，向东合掌敬礼尊法。"
        "御者吃惊，问为什么还有比天王更当敬礼的。」",
        "「帝释说偈：『人天大小王、四大天王、三十三天众都礼我；"
        "但还有持净戒、长夜修定、正信出家究竟梵行的人，我对他们恭敬；"
        "能调伏贪瞋、超越愚痴、不放逸修学的，我也礼敬；"
        "贪瞋痴尽的漏尽阿罗汉，更应当敬礼；"
        "若在家持净戒、如法布萨，也应当敬礼。』」",
        "「御者说：『那一定是世间最胜，所以天王敬礼；我也跟随天王恭敬。』"
        "帝释敬礼法后，乘车去园中游览。」",
        "「比丘们！帝释尚且敬礼法、赞叹礼法；你们也应当敬礼法，赞叹礼法的人。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN11.18 Sakka-namassana；"
        "汉「广说如上」peyyāla 据 1111 叙事框＋汉偈／SN 礼戒德、阿罗汉、在家持戒者重建；"
        "结劝从题「敬法」（汉末兼及僧者，以 1113 专经敬僧，此处从法）。"
        "据 SN／汉校正。"
    ),
}

# --- SA 1113 敬僧（SN11.20）-------------------------------------------------
SUTTAS["SA_1113"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「过去世时，帝释欲入园观，勅御者严驾。"
        "御者白：『驾已办，唯王知时。』帝释下殿，周向诸方合掌恭敬众僧。"
        "御者见已惊怖，马鞭落地，说偈：『诸方唯有人，胞胎臭秽、饥渴所烧；"
        "何故憍尸迦，敬重于非家？』」",
        "「帝释答：『我敬出家者：游行诸方不计行止，城邑色不能累心；"
        "不畜资具，一往无欲；往无所求，唯乐无为；言则善定，不言则寂。"
        "诸天阿修罗相诤，人间亦尔；唯出家者于诤无诤，于众生放舍刀杖；"
        "于财色不醉不荒，远离诸恶——是故敬礼。』」",
        "「御者言：『天王所敬必是世间胜，我从今日当礼出家人。』"
        "帝释敬礼僧已，昇车游园。」",
        "「诸比丘！帝释尚恭敬众僧、赞叹敬僧；汝等亦当恭敬众僧，赞叹敬僧功德。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「过去世时，帝释想去园中游览，吩咐御者备车。"
        "车备好后，帝释下殿，向各方合掌恭敬僧众。"
        "御者看见吓得马鞭落地，说偈：『各方只有人，生自臭秽胞胎、被饥渴烧灼；"
        "为什么憍尸迦，反而敬重舍家的人？』」",
        "「帝释答：『我敬出家人：四方游行不计行止，城邑美色动不了他的心；"
        "不囤积资具，一向少欲；去无所求，只乐无为；说话善定，不说则寂静。"
        "诸天与阿修罗相争，人间也一样；只有出家人在诤中无诤，对众生放下刀杖；"
        "对财色不醉不荒，远离诸恶——所以我敬礼。』」",
        "「御者说：『天王所敬的一定是世间最胜，我从今天起也礼出家人。』"
        "帝释敬礼僧后，上车游园。」",
        "「比丘们！帝释尚且恭敬僧众、赞叹敬僧；你们也应当恭敬僧众，赞叹敬僧的功德。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN11.20 Saṅghavandanā；"
        "帝释礼僧，御者问何以敬『臭秽人身』之出家者；答以无诤、少欲、放舍刀杖。"
    ),
}

# --- SA 1114 须毘罗（SN11.1 Suvīra）-----------------------------------------
SUTTAS["SA_1114"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「过去世时，阿修罗兴象马车步四兵，欲与三十三天战。"
        "帝释三度勅宿毘梨天子集四兵应战；宿毘梨受教已，还宫懈怠宽纵，不勤方便。」",
        "「宿毘梨说偈求『不起无为、无作无忧』之安隐处，请帝释与之。"
        "帝释答：『若有如是处，汝得已亦应携我同往。』"
        "如是再三，以『无方便』『不放逸』『懒惰无所起』『无事得乐』为请，帝释皆同答。"
        "末后帝释言：『若畏有为、不念造作，但当速净涅槃径路。』」",
        "「于是宿毘梨严四兵，与阿修罗战，摧敌得胜，还归天宫。」",
        "「诸比丘！帝释以精勤得胜，亦常赞叹精勤；汝等出家，当勤精进，赞叹精勤。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「过去世时，阿修罗发动象、马、车、步四兵，要与三十三天交战。"
        "帝释三次吩咐宿毘梨天子集结四兵应战；宿毘梨答应后，回宫却懈怠放纵，不肯精进。」",
        "「宿毘梨用偈求一个『什么都不用做、无为安隐、无作无忧』的地方，请帝释给他。"
        "帝释答：『若有那样的地方，你得到了也该带我一起去。』"
        "这样反复几次，用『不用努力』『不放逸处』『懒惰无事』『没事也得乐』来求，帝释都同样回答。"
        "最后帝释说：『你若怕造作、不想有为，就该赶快清净走向涅槃的路。』」",
        "「于是宿毘梨备好四兵，与阿修罗作战，击败敌军，得胜回宫。」",
        "「比丘们！帝释靠精勤得胜，也常赞叹精勤；你们出家，应当精进，赞叹精勤。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN11.1 Suvīra；"
        "懒惰天子三度违勅，求『无作安乐』；帝释反讽并归于涅槃道，终以精勤破阿修罗。"
        "罗什风压缩五番对偈为再三总叙。"
    ),
}

# --- SA 1115 仙人（SN11.10／11.9）-------------------------------------------
SUTTAS["SA_1115"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「过去世时，诸仙人住聚落边空闲处；不远则天、阿修罗对阵。」",
        "「毘摩质多罗除去五饰，入仙人园，高视不顾、不问讯而出。"
        "仙人议：『此人无调伏色，非威仪法——乃阿修罗王。以是知天众当增、阿修罗当减。』」",
        "「帝释亦除五饰入园，周遍问讯慰劳乃出。"
        "仙人议：『此人有调伏、有威仪，似族姓子——乃天帝释。以是知天众增、阿修罗减。』」",
        "「毘摩质多罗闻仙人赞天，瞋恚炽盛。仙人往乞无畏，彼答：『无有无畏与汝，当遗以恐怖。』"
        "仙人呪曰：『随行种果；乞无畏而施以怖，当获无尽畏。』凌虚而去。"
        "是夜阿修罗王心惊三起，闻战鼓恶声，惧败退还。」",
        "「帝释得胜，诣仙人处礼足，坐于下风。东风起，有仙人嫌腋臭，请千眼移坐；"
        "帝释答：『众香华鬘不及此香，宁久闻之，未曾厌患。』」",
        "「诸比丘！帝释恭敬出家人，亦赞叹恭敬之德；汝等当恭敬诸梵行者。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「过去世时，仙人们住在聚落边的空闲处；不远处天众与阿修罗摆开阵势。」",
        "「毘摩质多罗去掉五种装饰，走进仙人园，昂头四望、不问讯就离开。"
        "仙人议论：『这人没有调伏之相，也不合威仪——是阿修罗王。由此可知天众将增、阿修罗将减。』」",
        "「帝释也去掉五饰进园，一一问讯慰劳才离开。"
        "仙人议论：『这人有调伏、有威仪，像族姓子——是天帝释。由此可知天众增、阿修罗减。』」",
        "「毘摩质多罗听说仙人赞天，怒火中烧。仙人前来求无畏，他却说：『没有无畏给你们，只给恐怖。』"
        "仙人咒道：『怎样播种怎样收；求无畏却给恐怖，将得无尽的怖畏。』说完凌空离去。"
        "当夜阿修罗王三次惊醒，听见要开战的恶声，怕战败，逃回本宫。」",
        "「帝释得胜后，到仙人处顶礼，坐在下风处。东风吹来，有仙人嫌腋下臭，请千眼天王挪座；"
        "帝释答：『各种香花结成的华鬘，都不如这气味；我宁愿长久闻它，从不厌患。』」",
        "「比丘们！帝释恭敬出家人，也赞叹恭敬的功德；你们应当恭敬同行梵行的人。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：parallels SN11.10／SN11.9；"
        "汉含仙人观二王威仪、乞无畏、呪退阿修罗、帝释甘坐下风——据汉叙事罗什化；"
        "巴利 SN11.10 以仙人呪 Sambara 为主，义同『施怖获怖』。"
    ),
}

# --- SA 1116 灭瞋（SN11.21）-------------------------------------------------
SUTTAS["SA_1116"] = {
    "lit": [
        OPEN_JET_LIT,
        "时天帝释晨朝来诣，稽首佛足，身光遍照祇树，说偈问："
        "「杀何而得安隐眠？杀何而无忧畏？杀何等法，为瞿昙所赞？」",
        "世尊说偈答："
        "「害凶恶瞋恚，得安隐眠；害凶恶瞋恚，心无忧畏。"
        "瞋为毒根，灭彼苦种，则无忧畏——贤圣所赞。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那天帝释清晨前来，顶礼佛足，身光遍照祇园，用偈问道："
        "「杀了什么才能安稳睡眠？杀了什么才没有忧惧？杀哪种法，是瞿昙所赞叹的？」",
        "世尊用偈回答："
        "「灭除凶恶的瞋恚，就能安稳睡眠；灭除凶恶的瞋恚，心就没有忧惧。"
        "瞋是毒根，灭了这苦的种子，便无忧畏——这是贤圣所赞叹的。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN11.21 Chetvā；"
        "所当『杀』者唯瞋；巴利言瞋根毒而端甜，汉作苦种子——义同灭瞋无忧。"
    ),
}

# --- SA 1117 月八日（AN3.37–38）---------------------------------------------
SUTTAS["SA_1117"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「月八日，四大天王遣大臣案行世间，察人是否供养父母、沙门婆罗门，"
        "宗亲尊重，作福畏罪，于八日、十四、十五及神变月受戒布萨；"
        "十四日遣太子下观；十五日四王自下观察。」",
        "「若世间少有如是行者，四王白天帝释，三十三天不喜，言：『世人不善，天众减、阿修罗增。』"
        "若多人如法斋戒，则天众喜，言：『天众增、阿修罗减。』」",
        "「帝释欢喜，说偈：『若人月八日、十四十五日及神变月，受持八支斋，"
        "如我所修行，彼亦如是修。』」",
        "「诸比丘！此偈非善说——帝释自有贪瞋痴，未脱生老病死忧悲恼苦。"
        "若漏尽阿罗汉说此偈，乃为善说——彼已离贪瞋痴，已脱生老病死。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「每月八日，四大天王派大臣巡查人间，看人们是否供养父母、沙门婆罗门，"
        "尊重宗亲，修福畏罪，在八日、十四、十五和神变月受持斋戒布萨；"
        "十四日派太子下来看；十五日四大天王亲自下界观察。」",
        "「若世间很少有人这样做，四王禀报天帝释，三十三天就不高兴，说：『世人不善，天众减少、阿修罗增多。』"
        "若很多人如法斋戒，天众就欢喜，说：『天众增多、阿修罗减少。』」",
        "「帝释欢喜，说偈：『若有人在月八日、十四、十五和神变月受持八支斋，"
        "像我这样修行，那人也是这样修。』」",
        "「比丘们！这偈说得不好——帝释自己还有贪瞋痴，没能脱离生老病死忧悲苦恼。"
        "若是漏尽阿罗汉说这偈，才算善说——因为他已离贪瞋痴，已脱生老病死。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：parallels AN3.37–38 Catumahārāja／Rājapūjita；"
        "四王案行→天众增减；帝释八支斋偈；佛判唯阿罗汉可自称『如我修』。"
        "SC 未挂 SN，以 AN 为据。"
    ),
}

# --- SA 1118 病（SN11.23）---------------------------------------------------
SUTTAS["SA_1118"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「过去世时，毘摩质多罗阿修罗王病笃，诣帝释所求治。"
        "帝释言：『汝授我幻法，我当疗汝。』阿修罗王还问众，有诈伪者教曰："
        "『帝释质直好信；但告彼：学此幻法者堕地狱，受苦无量百千岁——彼必息意。』」",
        "「毘摩质多罗以偈白：『千眼天王！阿修罗幻术皆虚诳法，令人堕地狱，长夜受苦。』"
        "帝释言：『止！止！非我所须。汝且还去，令病得差、身力安隐。』」",
        "「诸比丘！帝释长夜真实，不幻不伪，贤善质直；汝等亦应如是学。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「过去世时，毘摩质多罗阿修罗王病重，到帝释那里求治。"
        "帝释说：『你把幻术教我，我就给你治病。』阿修罗王回去问部众，有个诡诈的教他说："
        "『帝释为人质直诚信；只要告诉他：学这幻术会堕地狱，受苦无量百千年——他一定打消念头。』」",
        "「毘摩质多罗用偈说：『千眼天王！阿修罗幻术都是虚诳法，会令人堕地狱，长夜受苦。』"
        "帝释说：『罢了！罢了！这不是我需要的。你回去吧，愿你病愈、身体安稳。』」",
        "「比丘们！帝释一向真实，不弄虚作假，贤善质直；你们也应当这样学。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN11.23；"
        "巴利为帝释往问疾、求 Sambari 幻法；汉作病者往求、诈伪教以地狱劝退——叙事异而『不学虚幻、质直』义同。"
        "从汉完整对话罗什化，结劝不幻不伪。"
    ),
}

# --- SA 1119 婆稚（SN11.8）-------------------------------------------------
SUTTAS["SA_1119"] = {
    "lit": [
        OPEN_JET_LIT,
        "时天帝释与鞞卢阇那子婆稚阿修罗王，晨朝俱诣佛所，身光普照祇园，退坐一面。",
        "婆稚说偈：「人当勤方便，必令利满足；利满足已，何须复方便。」"
        "帝释说偈：「若人勤方便，必令利满足；利满足已，修忍无过上。」"
        "俱问：「何者善说？」佛言：「二说俱善。且复听我：」",
        "「一切众生各求己利。世间和合与第一义——当知世和合是无常法。"
        "若人勤方便令利满足，利满足已，修忍无过上。」",
        "二人欢喜作礼而去。佛告比丘：「帝释修行于忍、赞叹于忍；汝等亦应修忍、赞叹忍。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那天帝释与鞞卢阇那之子婆稚阿修罗王清晨一同来到佛前，身光普照祇园，退坐一面。",
        "婆稚说偈：「人应当努力，一定要使利益圆满；利益圆满了，何必再努力。」"
        "帝释说偈：「人若努力使利益圆满；利益圆满之后，修忍才是最上。」"
        "两人问：「谁说得更好？」佛说：「两种都好。再听我说：」",
        "「一切众生各自求自己的利益。世间的和合与第一义——要知道世间和合是无常法。"
        "人若努力使利益圆满，圆满之后，修忍才是最上。」",
        "两人欢喜作礼离去。佛告诉比丘们：「帝释修行忍、赞叹忍；你们也应当修忍、赞叹忍。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN11.8 Verocana／Vepacitti-or-Veroca；"
        "阿修罗主勤方便，帝释以忍为上；佛双印并归于无常与忍。"
    ),
}

# --- SA 1120 持一戒（SN11.7）-----------------------------------------------
SUTTAS["SA_1120"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「过去世时，帝释于佛前受戒：『乃至佛法住世，尽形寿，"
        "有恼我者，我不反报。』毘摩质多罗闻已，持剑逆来。"
        "帝释遥告：『住！缚汝勿动！』彼不得动，责以受戒；帝释言：『我实受戒，且汝息住受缚。』」",
        "「阿修罗求放，帝释令先约誓不复嬈乱。彼说偈誓："
        "『贪瞋妄语、谤毁贤圣所趣之处——我若嬈乱，趣同彼趣。』"
        "帝释乃放，往白佛；佛赞：『善哉！汝要彼约誓如法，彼不复敢嬈乱。』」",
        "「诸比丘！帝释行不嬈乱，亦赞叹不扰乱法；汝等亦应如是学。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「过去世时，帝释在佛前受戒：『只要佛法住世，尽我形寿，"
        "即使有人恼害我，我也不反击。』毘摩质多罗听说后，提着利剑迎面而来。"
        "帝释远远喝道：『站住！绑住你，不许动！』对方动不了，便责问他是否受过戒；"
        "帝释说：『我确实受了戒，但你先停住受绑。』」",
        "「阿修罗求释放，帝释要他先发誓不再扰乱。他用偈发誓："
        "『贪、瞋、妄语、诽谤贤圣所去的恶趣——我若再扰乱，就堕同一趣。』"
        "帝释这才放他，去禀告佛；佛称赞：『很好！你要他发誓如法，他不敢再扰乱了。』」",
        "「比丘们！帝释实行不扰乱，也赞叹不扰乱之法；你们也应当这样学。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN11.7 Nadubbhiya；"
        "巴利为帝释独念『不欺仇敌』；汉作佛前受戒并缚阿修罗令誓——不报复／不嬈乱义同。"
        "从汉完整叙事罗什化。"
    ),
}

# --- SA 1121 释氏（AN10.46）-------------------------------------------------
SUTTAS["SA_1121"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时众多释氏来诣，礼足一面。佛问：「汝等于法斋日及神足月受持斋戒、修功德不？」"
        "答：「有时得，有时不得。」"
        "佛言：「瞿昙！汝等不获善利——憍慢、烦恼、忧悲之人，乃于斋日或得或不得。」",
        "「譬人求利，日日倍增，乃至一月钱财广耶？」答：「如是。」"
        "「如是增财，能令十年一向喜乐、多住禅定，远离忧苦不？」"
        "乃至一年、一月、一日一夜——皆答「不也。」",
        "「我声闻中有直心不谄不幻者，我教化十年，能使百千万岁一向喜乐、多住禅定；"
        "乃至一日一夜教化，明旦亦能令胜进，得斯陀含、阿那含——以彼先得须陀洹故。」",
        "释氏白：「我从今日于诸斋日当修八支斋，神足月受持斋戒，随力惠施，修诸功德。」"
        "佛言：「善哉！为真实要。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时许多释迦族人前来，顶礼后退坐一面。佛问：「你们在法斋日和神足月有没有受持斋戒、修功德？」"
        "答：「有时候有，有时候没有。」"
        "佛说：「瞿昙们！你们没有得到真正的利益——带着憍慢、烦恼、忧悲，才会对斋日或持或不持。」",
        "「好比人求财，天天成倍增加，到一个月是否钱财很广？」答：「是。」"
        "「这样增财，能让人十年一直喜乐、多住禅定，远离忧苦吗？」"
        "一直问到一年、一月、一日一夜——都答「不能。」",
        "「我的声闻里若有直心、不谄不幻的人，我教化十年，能使他百千万年一向喜乐、多住禅定；"
        "甚至一日一夜的教化，到第二天也能使他胜进，证得斯陀含、阿那含——因为他先前已得须陀洹。」",
        "释氏说：「我们从今天起，在斋日一定修八支斋，神足月受持斋戒，随力布施，修诸功德。」"
        "佛说：「很好！这才是真实紧要的事。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.46 Sakka；"
        "释氏斋戒不定；佛以倍增钱财不能换禅乐，对显直心弟子短期可进二果（先须陀洹）。"
        "汉「神足月」＝神变月／pavāraṇā 季。"
    ),
}

# --- SA 1122 疾病（SN55.54；据巴利校正四穌息）-------------------------------
SUTTAS["SA_1122"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时众多释氏集论议堂，语难提：「我等或得见佛、知识比丘，或不得；"
        "若有智慧优婆塞、优婆夷疾病困苦，当云何教化说法？当共问世尊。」"
        "难提与诸释俱诣佛所，具白斯义。",
        "佛告难提：「智慧优婆塞当诣病者，以四穌息处教授："
        f"『仁者！当成就{FOUR_CONF_LIT}。』」",
        "「问：『汝顾恋父母不？』若顾恋，教舍：『不由顾恋得活，用顾恋为？』"
        "若已舍，叹喜；次问妻子奴仆钱财——如舍父母法。」",
        "「次问人间五欲。若顾念，教曰：『人间五欲不净败坏，不如天上胜妙五欲。』"
        "令舍人间、志天上。若已舍人间而顾天欲，叹喜，复曰："
        "『天欲无常、苦、空、变坏；当更舍有身之欲。』"
        "若顾有身胜欲，教舍，乐涅槃寂灭为上。若已乐涅槃，叹善随喜。」",
        "「如是先后次第教诫，令得不起涅槃，与漏尽比丘等无有异。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时许多释迦族人在议事堂商议，对难提说：「我们有时能见佛和相熟的比丘，有时不能；"
        "若有智慧的男女居士病重痛苦，该怎样教导说法？应当一起去问世尊。」"
        "难提与众释氏一起到佛前，把这事详细禀告。",
        "佛告诉难提：「有智慧的优婆塞应当到病者那里，用四种安慰处来教导："
        f"『仁者！应当成就{FOUR_CONF_MOD}。』」",
        "「问：『你还挂念父母吗？』若挂念，就教他放下：『挂念也不能因此活命，何必挂念？』"
        "若已放下，就随喜赞叹；再问妻子、奴仆、钱财——用同样的方法教他放下。」",
        "「再问人间五欲。若还挂念，就说：『人间五欲污秽败坏，不如天上的胜妙五欲。』"
        "让他放下人间、志向天上。若已放下人间却还顾念天欲，就赞叹，再说："
        "『天欲也是无常、苦、空、会变坏的；应当进一步放下对有身之欲的顾念。』"
        "若还顾念有身胜欲，就教他放下，以涅槃寂灭之乐为最上。若已乐于涅槃，就随喜赞叹。」",
        "「就这样依次教导，使他得到不再起的涅槃，与漏尽比丘没有差别。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.54 Gilāna（Mahānāma）；"
        "汉「三种穌息」（缺戒）据 SN 校正为四不坏净；逐舍父母→亲属财物→人欲→天欲→有身→涅槃。"
        "汉难提／巴利摩诃男为同相应病教类型。据 SN 校正。"
    ),
}

# --- SA 1123 菩提（SN55.48）-------------------------------------------------
SUTTAS["SA_1123"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时释氏名菩提来诣，礼足白言：「善哉！我等快得善利，得为世尊亲属。」",
        "佛告：「莫作是语。所谓善利者，"
        f"{FOUR_CONF_LIT}。当作是学。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时有位名叫菩提的释迦族人前来，顶礼后说：「太好了！我们真是得到善利，能做世尊的亲属。」",
        "佛告诉他：「不要这样说。所谓善利，是"
        f"{FOUR_CONF_MOD}。应当这样学。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：~SN55.48 Bhaddiya；"
        "亲族之利不如四不坏净；巴利以四法明须陀洹，汉对治『以亲为利』慢。"
    ),
}

# --- SA 1124 往生（SN55.36）-------------------------------------------------
SUTTAS["SA_1124"] = {
    "lit": [
        OPEN_KAP_LIT,
        "尔时世尊告诸比丘：「若圣弟子于佛不坏净成就，"
        "先以佛不坏净往生善趣诸天皆大欢喜，叹言："
        "『我以是因缘来生此天；彼圣弟子今亦成就，亦当来生。』"
        f"于法、僧不坏净及圣戒成就，亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "那时世尊告诉比丘们：「若圣弟子成就对佛的不坏净，"
        "那些先前因对佛不坏净而生到善趣的天神都会大欢喜，赞叹说："
        "『我因这因缘来生此天；那位圣弟子现在也成就了，也将来生这里。』"
        "对法、对僧的不坏净以及圣戒成就，也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.36 Sabhāgata；"
        "四不坏净与先往生诸天『同分』欢喜；汉题「往生」。"
    ),
}

# --- SA 1125 须陀恒（SN55.50 道分）------------------------------------------
SUTTAS["SA_1125"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「趣须陀洹有四支——亲善知识、闻如法说、"
        "如理思惟、依教修行。具此四支，名为须陀洹道分。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「趋向须陀洹有四个支分——亲近善知识、听闻正法、"
        "如理思惟、依照教法去修行。具备这四支，就叫须陀洹道分。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：~SN55.50／55.55 aṅga；"
        "四预流支：善友、闻法、如理作意、法次法向。"
    ),
}

# --- SA 1126 须陀恒（SN55.46 果分）------------------------------------------
SUTTAS["SA_1126"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「须陀洹所依有四："
        "信佛不坏、信法不坏、信僧不坏，并成圣戒。"
        "成就此四，是名须陀洹分。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「须陀洹所依止的有四项："
        "对佛的信心不坏、对法的信心不坏、对僧的信心不坏，并且成就圣戒。"
        "成就这四项，就叫须陀洹分。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.46 Sandiṭṭhika；"
        "四不坏净＝须陀洹分（果德）；与 1125 道分相对。"
    ),
}

# --- SA 1127 四法（SN55.2）--------------------------------------------------
SUTTAS["SA_1127"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若成就四法，当知是须陀洹。"
        f"何等为四？{FOUR_CONF_LIT}。」",
        "「如是不分别说；若分别，则比丘、比丘尼、式叉摩那、沙弥、沙弥尼、"
        "优婆塞、优婆夷成就四法者，皆当知是须陀洹。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「若成就四种法，就应当知道是须陀洹。"
        f"哪四种？{FOUR_CONF_MOD}。」",
        "「这样是总说；若分别说，则比丘、比丘尼、式叉摩那、沙弥、沙弥尼、"
        "优婆塞、优婆夷成就这四法的，都应当知道是须陀洹。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.2 Ariyasāvaka；"
        "四法成就即须陀洹；汉 peyyāla 七众据邻经略补。"
    ),
}

# --- SA 1128 四果（略列；~SN55.55–58 仅相似）-------------------------------
SUTTAS["SA_1128"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「沙门之果凡有四种——"
        "预流、一来、不还、无生；是名四沙门果。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「沙门的果位一共有四种——"
        "预流（须陀洹）、一来（斯陀含）、不还（阿那含）、无生（阿罗汉）；这叫四沙门果。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：SC 标 ~SN55.55–58，然彼明四预流支趣果；"
        "本经唯列四沙门果名，从汉略说，不据 SN 扩写预流支。"
        "文言用预流／一来／不还／无生，白话括注传统音译。"
    ),
}

# --- SA 1129 四果（定义）----------------------------------------------------
SUTTAS["SA_1129"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四沙门果：须陀洹、斯陀含、阿那含、阿罗汉。"
        "须陀洹果者，三结断；斯陀含果者，三结断而贪恚痴薄；"
        "阿那含果者，五下分结断；阿罗汉果者，贪瞋痴永尽，一切烦恼永尽。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种沙门果：须陀洹、斯陀含、阿那含、阿罗汉。"
        "须陀洹果是断了三结；斯陀含果是断了三结，并且贪、瞋、痴变薄；"
        "阿那含果是断了五下分结；阿罗汉果是贪瞋痴永远尽了，一切烦恼永远尽了。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：SC 同挂 ~SN55.55–58，然本经为四果结使定义，"
        "义近 SN22.109／AN 果位定型；从汉，不据预流支平行改写。"
    ),
}

# --- SA 1130 行住坐卧（无平行；peyyāla）-------------------------------------
SUTTAS["SA_1130"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「若有比丘于某处经行，而于四沙门果中得一一果，"
        "彼尽形寿当念彼处。如经行，如是住处、坐处、卧处亦然。」",
        "「如是比丘；比丘尼、式叉摩那、沙弥、沙弥尼、优婆塞、优婆夷，亦各于行住坐卧如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「如果有比丘在某处经行，而在四沙门果中证得任何一果，"
        "他尽形寿都应当忆念那个地方。经行如此，住处、坐处、卧处也是如此。」",
        "「比丘是这样；比丘尼、式叉摩那、沙弥、沙弥尼、优婆塞、优婆夷，"
        "各自在行、住、坐、卧上也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 巴利专经；"
        "证果处当尽寿忆念；peyyāla 住坐卧及七众据汉略补。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {
    "SA_1111": "high",
    "SA_1112": "high",
    "SA_1113": "high",
    "SA_1114": "high",
    "SA_1115": "high",
    "SA_1116": "high",
    "SA_1117": "high",
    "SA_1118": "high",
    "SA_1119": "high",
    "SA_1120": "high",
    "SA_1121": "high",
    "SA_1122": "high",
    "SA_1123": "high",
    "SA_1124": "high",
    "SA_1125": "high",
    "SA_1126": "high",
    "SA_1127": "high",
    "SA_1128": "medium",
    "SA_1129": "medium",
    "SA_1130": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1112": "「广说如上」peyyāla → 据 SA_1111 叙事框＋汉偈／SN11.18 礼戒德重建",
    "SA_1122": "汉「三种穌息」缺戒 → 据 SN55.54 校正为四不坏净",
    "SA_1127": "七众「一一经如上」peyyāla → 略补七众同得须陀洹",
    "SA_1130": "住坐卧／七众 peyyāla → 据汉略补",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

GOLD: dict[str, dict[str, str]] = {}
for _rid, _s in SUTTAS.items():
    lit_paras = list(_s["lit"])
    mod_paras = list(_s["mod"])
    assert len(lit_paras) == len(mod_paras), f"{_rid} lit/mod paragraph mismatch"
    GOLD[_rid] = {
        "kumarajiva_style_text": "\n".join(lit_paras),
        "modern_psychology_text": "\n".join(mod_paras),
        "notes": _s["notes"],
    }

assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
assert set(RECONSTRUCTED) <= set(GOLD)
assert set(GOLD) == {f"SA_{i}" for i in batch_range}


def _snap(rec: dict) -> str:
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

    _goldish = {"gold", "gold_reconstructed"}
    by_status = {r["id"]: r.get("review_status") for r in records}
    if by_status.get("SA_1110") in _goldish:
        boundary_lo = "SA_1110"
    else:
        boundary_lo = None
    if by_status.get("SA_1131") in _goldish:
        boundary_hi = "SA_1131"
    else:
        boundary_hi = None

    boundary_before: dict[str, str] = {}
    for bid in (boundary_lo, boundary_hi):
        if not bid:
            continue
        for rec in records:
            if rec["id"] == bid:
                boundary_before[bid] = _snap(rec)
                break

    # Snapshot neighbors outside batch (parallel batches)
    neighbor_ids = {f"SA_{i}" for i in list(range(1091, 1111)) + list(range(1131, 1151))}
    neighbor_before = {
        rec["id"]: _snap(rec) for rec in records if rec["id"] in neighbor_ids
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

    for bid, before in boundary_before.items():
        for rec in merged:
            if rec["id"] == bid:
                assert before == _snap(rec), f"{bid} must remain untouched"
                break

    for rid, before in neighbor_before.items():
        for rec in merged:
            if rec["id"] == rid:
                assert before == _snap(rec), f"{rid} (neighbor) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1111-1130.json").write_text(
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
    continuous = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in _goldish for i in batch_range
    )
    untouched_neighbors = all(f"SA_{i}" not in GOLD for i in list(range(1091, 1111)) + list(range(1131, 1151)))

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1111–SA_1130 only)")
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
    print(f"continuous_gold_SA_1111–1130={continuous}")
    print(f"neighbors_untouched={untouched_neighbors}")
    if boundary_lo:
        print(f"{boundary_lo}_untouched=True")
    else:
        print("SA_1110_boundary_skipped (not yet gold)")
    if boundary_hi:
        print(f"{boundary_hi}_untouched=True")
    else:
        print("SA_1131_boundary_skipped (not yet gold)")
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
