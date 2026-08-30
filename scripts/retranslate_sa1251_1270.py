#!/usr/bin/env python3
"""Retranslate SA 1251–1270（譬喻相应末＋杂相应起）→ merge.

本批二十经：
1251–1264 譬喻相应：那提迦 AN6.42、枕木 SN20.8、釜 SN20.4、人家 SN20.3、
         七手剑 SN20.5、爪上 SN20.2、弓手 SN20.6、鼓 SN20.7、铁丸（无平行）、
         猫 SN20.10、木杵（无平行）、野狐 SN20.11、尿粪／野狐（resembling SN17.5／17.8）
1265–1266 跋迦黎 SN22.87、阐陀 SN35.87／MN144
1267–1270 杂相应起：济度 SN1.1、解陀 SN1.2、流（≈SN2.15）、拘迦尼（无巴利）

信：full 平行据巴利／Sujato；resembling 保守依汉＋注异；无平行 medium/low。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
厌故离贪：1257「厌离、不乐、解脱」→「生厌、离贪、解脱」。
边界：只合并 SA_1251–1270；断言邻经 SA_1250／SA_1271 不变。
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

OPEN_BAM_LIT = "如是我闻：一时，佛住王舍城迦兰陀竹园。"
OPEN_BAM_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

OPEN_VES_LIT = "如是我闻：一时，佛住毗舍离猕猴池侧重阁讲堂。"
OPEN_VES_MOD = "我是这样听说的：有一次，佛住在毗舍离猕猴池侧重阁讲堂。"

OPEN_VAR_LIT = "如是我闻：一时，佛住波罗奈仙人住处鹿野苑中。"
OPEN_VAR_MOD = "我是这样听说的：有一次，佛住在波罗奈仙人住处鹿野苑中。"

OPEN_VAL_LIT = "如是我闻：一时，佛住王舍城山谷精舍。"
OPEN_VAL_MOD = "我是这样听说的：有一次，佛住在王舍城山谷精舍。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY_MOD = "他听佛所说，欢喜随喜，作礼离去。"

CLOSE_DEV_LIT = "时彼天子闻佛所说，欢喜随喜，稽首佛足，即没不现。"
CLOSE_DEV_MOD = "那时天子听佛所说，欢喜随喜，稽首佛足，随即隐没不见。"

DEV_OPEN_LIT = (
    "时有一天子，容色绝妙，于后夜来诣佛所，稽首佛足，退坐一面；"
    "身诸光明遍照祇树给孤独园。"
)
DEV_OPEN_MOD = (
    "那时有一位天子，容色绝妙，后夜来到佛前，稽首佛足，退坐一面；"
    "身上的光明照遍祇树给孤独园。"
)

MILK_LIT = "挤牛乳顷"
MILK_MOD = "挤一下牛乳那么短的时间"

METTA_TRAIN_LIT = (
    f"当如是学：『乃至{MILK_LIT}，于一切众生修习慈心；"
    "慈心解脱当修习、多修习，以为车乘、以为所依。』"
)
METTA_TRAIN_MOD = (
    f"应当这样学：『哪怕只{MILK_MOD}，也要对一切众生修习慈心；"
    "慈心解脱应当修习、多修习，当作车乘、当作所依。』"
)

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

SUTTAS: dict[str, dict] = {}

# --- SA 1251 那提迦（AN6.42 Nāgita；汉「如上广说」）-------------------------
SUTTAS["SA_1251"] = {
    "lit": [
        "如是我闻：一时，佛在拘萨罗人间游行，至一奢能伽罗聚落，住彼林中。"
        "时尊者那提迦为佛侍者。聚落婆罗门居士多持饮食，门外喧闹求施。"
        "佛告那提迦：「我不乐名称；有人不得出离、远离、寂静、觉支之乐，"
        "且取利养恭敬污浊之乐。我能无艰难得彼胜乐。」",
        "「那提迦！我见比丘住聚落精舍，正受而坐，念言：『沙弥、净人往来作声，"
        "或令彼退失正受。』是故我不喜比丘住聚落。"
        "我见比丘住空闲处，坐而瞌睡，念言：『彼当除睡，专念空闲一想。』我喜其住空闲。"
        "我见比丘住空闲处，心未得定，念言：『未定者令得定，已定者令护持。』我喜其住空闲。"
        "我见比丘住空闲处，已得正受，念言：『未解脱者令速解脱，已解脱者令不退失。』我喜其住空闲。",
        "「复次，那提迦！我见比丘住聚落，多获衣食汤药，耽著利养，弃捨空闲；"
        "我不喜如是住聚落。我见比丘住空闲，虽有利养而不废远离；我喜如是住空闲。"
        "比丘当如是学。」",
        "佛说此经已，那提迦比丘欢喜随喜，作礼而去。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在拘萨罗人间游行，到了一奢能伽罗聚落，住在附近林中。"
        "那时那提迦尊者作佛的侍者。聚落里的婆罗门居士带着许多饮食，在门外喧闹，想要供养。"
        "佛对那提迦说：「我不乐求名声；有些人得不到出离、远离、寂静、觉悟的乐，"
        "只好取用利养恭敬那种污浊的乐。我能不难得到那些殊胜的乐。」",
        "「那提迦！我看见比丘住在聚落精舍里正受而坐，心想：『沙弥、净人来往作声，"
        "也许会让他退失正受。』所以我不喜欢比丘住聚落。"
        "我看见比丘住空闲处却坐着打瞌睡，心想：『他会除掉睡意，专念空闲的一想。』我喜欢他住空闲。"
        "我看见比丘住空闲处，心还没得定，心想：『未得定的让他得定，已得定的让他护持。』我喜欢他住空闲。"
        "我看见比丘住空闲处已经正受，心想：『未解脱的让他快解脱，已解脱的让他不退失。』我喜欢他住空闲。",
        "「还有，那提迦！我看见比丘住聚落，多得衣食汤药，耽著利养，丢掉空闲；"
        "我不喜欢这样住聚落。我看见比丘住空闲，虽有利养却不废远离；我喜欢这样住空闲。"
        "比丘应当这样学。」",
        "佛说完这部经，那提迦比丘欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN6.42 Nāgitasutta。"
        "汉「至那楞伽罗……如上广说」peeyāla → 据 AN 补聚落喧闹、不乐名称／利养框架；"
        "住聚落／空闲好恶据巴利校正（汉以仰卧吁咄、摇身坐睡为不喜，巴利以空闲瞌睡亦可喜）。"
    ),
}

# --- SA 1252 枕木（SN20.8 Kaliṅgara）---------------------------------------
SUTTAS["SA_1252"] = {
    "lit": [
        OPEN_VES_LIT,
        "尔时世尊告诸比丘：「今诸离车子以木为枕，精勤不放逸而住；"
        "是故摩竭陀王阿阇世毘提希子不得其便。"
        "当来之世，离车子手足柔软，繒纊为枕，安卧至日出，放逸而住；"
        "以放逸故，王阿阇世乃得其便。",
        "「如是，今诸比丘以木为枕，于精进事精勤不放逸；魔波旬不得其便。"
        "当来比丘手足柔软，繒纊为枕，安卧至日出，放逸而住；魔波旬乃得其便。"
        "是故比丘当如是学：『我等以木为枕，精勤不放逸，修习精进。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "那时世尊告诉比丘们：「现在离车子们用木头当枕头，精勤不放逸地住；"
        "所以摩竭陀王阿阇世——毘提希之子——得不到可乘之机。"
        "将来离车子手足柔软，用丝绵当枕头，一直睡到日出，放逸而住；"
        "因为放逸，阿阇世王才会得到可乘之机。",
        "「同样，现在比丘们用木头当枕头，在精进事上精勤不放逸；魔波旬得不到可乘之机。"
        "将来比丘手足柔软，用丝绵当枕头，一直睡到日出，放逸而住；魔波旬才会得到可乘之机。"
        "所以比丘应当这样学：『我们用木头当枕头，精勤不放逸，修习精进。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.8 Kaliṅgarasutta。"
        "据 SN 收束：木枕／不放逸→王与魔不得便；未来软枕放逸→得其便；删汉肌肤筋骨冗叙。"
    ),
}

# --- SA 1253 釜（SN20.4 Okkhā）---------------------------------------------
SUTTAS["SA_1253"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「譬如有人晨朝以百釜饭食惠施，日中、日暮亦复如是。"
        f"若复有人乃至{MILK_LIT}修习慈心，此慈功德胜彼惠施，算数譬类所不能及。"
        f"{METTA_TRAIN_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「好比有人早晨用一百锅饭食布施，中午、傍晚也是这样。"
        f"如果另有人哪怕只{MILK_MOD}修习慈心，这慈心的功德胜过那布施，用算数譬喻都比不上。"
        f"{METTA_TRAIN_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.4 Okkhāsutta。"
        "据 SN：okkhāsataṁ→百釜（汉「三百釜」不从）；"
        f"gadduhanamatta→{MILK_LIT}；结劝慈心解脱多修习。"
    ),
}

# --- SA 1254 人家（SN20.3 Kula）---------------------------------------------
SUTTAS["SA_1254"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「譬如人家多女少男，易为盗贼所劫。"
        "如是比丘若不修习慈心解脱，易为非人所得其便。"
        "譬如人家多男少女，盗贼难劫；如是比丘修习慈心解脱，非人不得其便。"
        f"{METTA_TRAIN_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「好比人家女人多、男人少，容易被盗贼劫夺。"
        "同样，比丘若不修习慈心解脱，容易被非人趁虚而入。"
        "好比人家男人多、女人少，盗贼难劫；同样，比丘修习慈心解脱，非人就不得其便。"
        f"{METTA_TRAIN_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.3 Kulasutta。"
        "据 SN：主体为比丘慈心解脱 vs 非人（汉「善男子善女人／恶鬼神」收束为比丘／非人）。"
    ),
}

# --- SA 1255 七手剑／利矛（SN20.5 Satti）------------------------------------
SUTTAS["SA_1255"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「譬如利矛，锋刃广利。有人言：『我能以手以拳折屈此矛。』"
        "于意云何？彼人能折屈不？」"
        "比丘白佛：「不能。世尊！彼矛锋利，非手拳所能折；适足自困。」",
        "「如是，比丘！若修习慈心解脱，多修习，以为车乘、所依；"
        "有非人欲坏其心，终不能得，适自疲苦。"
        f"{METTA_TRAIN_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「好比一支锋利的矛。有人说：『我能用手用拳把它折弯。』"
        "你们怎么想？那人折得了吗？」"
        "比丘回答：「折不了。世尊！那矛太利，不是手拳折得了的；只会自找苦吃。」",
        "「同样，比丘！若修习慈心解脱，多修习，当作车乘、所依；"
        "有非人想扰乱他的心，终究做不到，只会自己疲苦。"
        f"{METTA_TRAIN_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.5 Sattisutta。"
        "satti tiṇhaphalā→利矛（汉「七手剑／匕手剑」据义改）；"
        "非人欲坏心→自取疲苦。"
    ),
}

# --- SA 1256 爪上（SN20.2 Nakhasikhā；汉误植慈心）---------------------------
SUTTAS["SA_1256"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊以爪抄少许土，告诸比丘：「于意云何？我爪上土多，为大地土多？」"
        "比丘白佛：「世尊！爪上土甚少，大地土无量，不可为比。」",
        "佛告诸比丘：「如是，得生人间者少，如爪上土；不得生人间者多，如大地土。"
        "是故比丘当如是学：『我等当不放逸而住。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊用指甲挑起一点土，告诉比丘们：「你们怎么想？我指甲上的土多，还是大地的土多？」"
        "比丘回答：「世尊！指甲上的土极少，大地的土无量，没法比。」",
        "佛告诉比丘们：「同样，能生到人间的少，像指甲上的土；不能生到人间的多，像大地的土。"
        "所以比丘应当这样学：『我们应当不放逸而住。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.2 Nakhasikhāsutta。"
        "据 SN 校正：爪土喻＝人间受生少／非人趣多，结劝不放逸；"
        "汉误植「修习慈心」多少之较，不从（慈心爪喻见他经串）。"
    ),
}

# --- SA 1257 弓手（SN20.6 Dhanuggaha）---------------------------------------
SUTTAS["SA_1257"] = {
    "lit": [
        OPEN_VES_LIT,
        "尔时世尊告诸比丘：「诸行无常，不恒、不安，是变易法。"
        "当观察诸行，生厌、离贪、解脱。」",
        "时有异比丘从座起，偏袒右肩，合掌白佛：「世尊！寿命迁灭，迟速如何？」"
        "佛言：「我能说，然汝欲知者难。」比丘白佛：「可说譬不？」佛言：「可说。」",
        "「譬如四健弓手立于四方，俱时放箭；有人于箭未落，尽接四箭。"
        "比丘！如是人为捷疾不？」白佛：「捷疾。世尊！」"
        "「彼虽捷疾，日与月更疾；日与月及导日月诸天更疾；命行迁灭复倍疾于彼。"
        "是故比丘当如是学：『我等当不放逸而住。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "那时世尊告诉比丘们：「诸行无常，不恒、不安，是变易法。"
        "应当观察诸行，生厌、离贪、解脱。」",
        "这时有一位比丘从座起，偏袒右肩，合掌对佛说：「世尊！寿命迁灭，快慢怎么样？」"
        "佛说：「我能说，但你要想完全了知却难。」比丘说：「可以说个譬喻吗？」佛说：「可以。」",
        "「好比四位强弓手站在四方，同时放箭；有人在箭还没落地前，把四支箭都接住。"
        "比丘！这样的人算不算迅疾？」回答：「迅疾。世尊！」"
        "「他虽然迅疾，日与月更快；日与月以及在日月前奔走的诸天更快；命行迁灭比那还要快得多。"
        "所以比丘应当这样学：『我们应当不放逸而住。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.6 Dhanuggahasutta。"
        "汉「厌离、不乐、解脱」据 nibbindati／virajjati／vimuccati 作「生厌、离贪、解脱」（厌故离贪）；"
        "接箭→日月→导日月天→命行更快，据 SN 收束（汉地神／四王层层略并）。"
    ),
}

# --- SA 1258 鼓（SN20.7 Āṇi）------------------------------------------------
SUTTAS["SA_1258"] = {
    "lit": [
        OPEN_VAR_LIT,
        "尔时世尊告诸比丘：「过去世时，陀舍罗诃人有鼓名阿能诃，声好深远。"
        "鼓久裂坏，裁皮补钉，展转增钉；后时木壳尽坏，唯余钉聚。」",
        "「如是，当来比丘闻如来所说甚深、出世间、空相应修多罗，不肯谛听受持；"
        "而于文辞绮饰、外道弟子所造杂论，专心顶受。"
        "由是如来甚深空相应法便当隐没，如彼鼓坏，唯余钉聚。"
        "是故当如是学：『于如来所说甚深空相应法，谛听受持，欢喜崇习。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VAR_MOD,
        "那时世尊告诉比丘们：「过去世时，陀舍罗诃人有一面鼓名叫阿能诃，声音好听又传得远。"
        "鼓用久了裂坏，就裁皮打钉修补，钉子越补越多；后来木壳都坏尽了，只剩下一堆钉子。」",
        "「同样，将来比丘听到如来所说甚深、出世间、与空相应的经典，不肯好好听受持；"
        "却对外道弟子所作、文辞华丽的杂论，专心奉持。"
        "这样一来，如来甚深空相应的法就会隐没，像那面鼓坏了，只剩钉堆。"
        "所以应当这样学：『对如来所说甚深空相应法，要谛听受持，欢喜崇习。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.7 Āṇisutta。"
        "āṇi→钉／补钉；suññatappaṭisaṁyutta→空相应；"
        "外道诗偈文辞 vs 如来甚深空法隐没——据 SN；住处汉波罗奈，义从巴利。"
    ),
}

# --- SA 1259 铁丸（无平行）--------------------------------------------------
SUTTAS["SA_1259"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「譬如热铁丸投著劫贝绵中，当速燃不？」"
        "白佛：「如是，世尊！」",
        "「愚人依聚落住，入村乞食，不护身、不守根、不系念；见少壮女人，取相起贪，"
        "欲火烧心烧身，遂捨戒退转，长夜得非义。"
        "是故当如是学：『善护其身，守护根门，系念乞食。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「好比烧热的铁丸丢进劫贝绵里，会不会很快烧起来？」"
        "回答：「会的，世尊！」",
        "「愚人依聚落住，进村乞食，不护身、不守根、不系念；看见年轻女人，取相起贪，"
        "欲火烧心烧身，于是捨戒退转，长夜得到无益的苦果。"
        "所以应当这样学：『好好护身，守护根门，系念乞食。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：铁丸投绵喻欲火；与 SN20.10 猫喻同主题而异喻。"
    ),
}

# --- SA 1260 猫（SN20.10 Biḷāra）---------------------------------------------
SUTTAS["SA_1260"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「过去世时，有猫羸瘦，于孔穴伺鼠。鼠出，猫急吞之；"
        "鼠在腹中啮其内藏，猫迷闷狂走，遂至于死。」",
        "「如是，愚比丘入村乞食，不护身口意，不守根门，不立正念；"
        "见女人衣不整齐，贪欲侵心，于圣律中是为死——谓捨戒还俗；"
        "或近于死——谓犯可悔重罪。内法被啮，捨戒退减，长夜得不饶益。"
        "是故当如是学：『善护身口意，守根立念，入村乞食。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「过去世时，有只猫又饿又瘦，在洞穴边等老鼠。老鼠出来，猫急忙吞下；"
        "老鼠在肚子里咬它的内脏，猫昏乱狂奔，终于死了。」",
        "「同样，愚笨的比丘进村乞食，不护身口意，不守根门，不立正念；"
        "看见女人衣着不整齐，贪欲侵心，在圣律中这就叫做死——指捨戒还俗；"
        "或近于死——指犯了可以悔除的重罪。内心被啮食，捨戒退减，长夜得到无益的苦。"
        "所以应当这样学：『善护身口意，守根立念，进村乞食。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.10 Biḷārasutta。"
        "据 SN：死＝捨戒还俗，近死＝可悔重罪；汉略框架，义从巴利补。"
    ),
}

# --- SA 1261 木杵（无平行）--------------------------------------------------
SUTTAS["SA_1261"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「譬如木杵，日夜春用不已则消减。"
        "如是沙门、婆罗门不闭根门，食不知量，初夜后夜不勤觉寤，善法日减，如彼木杵。」",
        "「譬如优钵罗、钵昙摩、拘牟头、分陀利生于水中，随水增长。"
        "如是善闭根门，饮食知量，初夜后夜精勤觉寤，善法日增。"
        "当如是学：『善闭根门，饮食知量，初夜后夜精勤觉寤。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「好比木杵，日夜不停地舂就会渐渐磨损。"
        "同样，沙门、婆罗门若不闭根门，饮食不知量，初夜后夜不勤觉寤，善法天天减损，就像那木杵。」",
        "「好比优钵罗、钵昙摩、拘牟头、分陀利长在水里，随水增长。"
        "同样，善闭根门，饮食知量，初夜后夜精勤觉寤，善法天天增长。"
        "应当这样学：『善闭根门，饮食知量，初夜后夜精勤觉寤。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：木杵消减 vs 莲华增长；根门／知量／觉寤定型。"
    ),
}

# --- SA 1262 野狐（SN20.11 Siṅgāla；汉义相反）-------------------------------
SUTTAS["SA_1262"] = {
    "lit": [
        OPEN_BAM_LIT + "尔时世尊后夜闻野狐鸣。",
        "夜过天明，于众前坐，告诸比丘：「汝等后夜闻野狐鸣不？」"
        "白佛：「如是，世尊！」",
        "「彼老野狐为疥疮所苦，然所欲往则往，所欲住则住，寒风亦吹其身。"
        "若有自称释子者，能得如是身类，犹为幸事。"
        "是故当如是学：『我等当不放逸而住。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD + "那时世尊后夜听见野狐叫。",
        "夜过天亮，在大众前坐下，告诉比丘们：「你们后夜听见野狐叫了吗？」"
        "回答：「听见了，世尊！」",
        "「那只老野狐正受疥疮之苦，可它仍能想去就去、想住就住，寒风也还吹在它身上。"
        "若有人自称是释子，能得到这样的身类，都还算幸运。"
        "所以应当这样学：『我们应当不放逸而住。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN20.11 Siṅgālasutta。"
        "据 SN 校正：疥狐虽苦犹得自在；自称释子得此身犹幸——汉「愚人欲求如是形类」义相反，不从。"
    ),
}

# --- SA 1263 尿粪（resembling SN17.5；汉主题＝有如粪）-----------------------
SUTTAS["SA_1263"] = {
    "lit": [
        OPEN_BAM_LIT,
        "尔时世尊告诸比丘：「我不赞叹受少有身，何况多受？所以者何？受有则苦。"
        "譬如粪秽，少亦臭恶，何况于多？诸有亦尔，少亦不赞，乃至刹那，何况于多？"
        "是故当如是学：『断除诸有，莫增长有。』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "那时世尊告诉比丘们：「我连稍微受有都不称赞，何况多受？为什么？受有就是苦。"
        "好比粪便，少也臭秽，何况多？一切有也是这样，少也不赞叹，哪怕一刹那，何况多？"
        "所以应当这样学：『断除诸有，不要增长有。』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：SC resembling SN17.5 Mīḷhaka（粪甲虫／利养憍慢），主题不同；"
        "本经汉义为 bhava 如粪、少有亦不赞——保守依汉，不改写为利养相应。"
    ),
}

# --- SA 1264 野狐（resembling SN17.8；汉＝知恩）-----------------------------
SUTTAS["SA_1264"] = {
    "lit": [
        OPEN_BAM_LIT + "尔时世尊夜后分闻野狐鸣。",
        "夜过，于众前坐，告诸比丘：「汝等夜后分闻野狐鸣不？」"
        "白佛：「如是，世尊！」",
        "「彼野狐为疥疮所困，是故鸣唤。若有人为治其疮，彼必知恩报恩。"
        "今有愚人，不知恩报恩。是故当如是学：『知恩报恩；小恩尚报，况复大恩？』」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD + "那时世尊后夜听见野狐叫。",
        "夜过，在大众前坐下，告诉比丘们：「你们后夜听见野狐叫了吗？」"
        "回答：「听见了，世尊！」",
        "「那野狐被疥疮所困，所以叫唤。如果有人给它治疮，它一定会知恩报恩。"
        "可现在有愚人，不知恩报恩。所以应当这样学：『知恩报恩；小恩尚且要报，何况大恩？』」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：SC resembling SN17.8（疥狐／利养不安），主题不同；"
        "本经汉义为知恩报恩——保守依汉，不改写为利养相应。"
    ),
}

# --- SA 1265 跋迦黎（SN22.87 Vakkali）---------------------------------------
SUTTAS["SA_1265"] = {
    "lit": [
        OPEN_BAM_LIT + "时尊者跋迦梨住金师精舍，疾病困笃，遣人请佛哀愍来看。",
        "世尊晡时往诣。跋迦梨欲起，佛止之，问病可忍不。答言苦痛转增，欲求刀自杀。",
        "佛言：「止！何用见此臭秽之身？见法者则见我，见我者则见法。"
        "跋迦梨！色是常耶？非常耶？」答：「无常。」「若无常，是苦耶？」答：「是苦。」"
        "「无常、苦、变易法，宁有可贪可欲不？」答：「不也。」受、想、行、识亦如是。"
        "「于五受阴无取著，是则善终。」说已，佛去。",
        "后夜二天来白佛：「跋迦梨欲自杀。」第二天言：「彼已善解脱。」"
        "晨朝佛遣比丘往告：「天记汝善解脱；佛记汝善终，勿怖。」",
        "跋迦梨下床受教，白言：「我于五阴无常、苦、无可贪欲，决定无疑；"
        "然苦痛逼身，欲刀自杀。」即执刀自杀。",
        "佛率众至尸所，见烟闇周匝，告言：「此是恶魔求跋迦梨识神所生处。"
        "跋迦梨识不住著，已般涅槃。」为说第一记。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD + "那时跋迦梨尊者住在金师精舍，病重困苦，派人请佛哀愍来看。",
        "世尊傍晚前往。跋迦梨想起身，佛拦住他，问病是否可忍。他答苦痛加重，想用刀自杀。",
        "佛说：「罢了！何必看这臭秽的身体？见法就是见我，见我就是见法。"
        "跋迦梨！色是常还是无常？」答：「无常。」「若无常，是苦吗？」答：「是苦。」"
        "「无常、苦、变易之法，还有可贪可欲吗？」答：「没有。」受、想、行、识也是这样。"
        "「对五受阴没有取著，就是善终。」说完，佛离去。",
        "后夜两位天子来告诉佛：「跋迦梨想自杀。」第二位说：「他已经善解脱。」"
        "清晨佛派比丘去转告：「天记你善解脱；佛记你善终，不要怕。」",
        "跋迦梨下床受教，说：「我对五阴无常、苦、无可贪欲，决定无疑；"
        "可苦痛逼身，仍想用刀自杀。」便执刀自杀。",
        "佛带领大众到遗体处，看见烟闇环绕，说：「这是恶魔在寻找跋迦梨识神投生何处。"
        "跋迦梨的识不再住著，已经涅槃。」于是为他作第一记别。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN22.87 Vakkalisutta。"
        "据 SN 补「见法即见我／何用见臭身」（汉略）；"
        "五阴无常苦无取→善终；魔求识、识不住＝涅槃；peeyāla 病问安／广问答收束。"
    ),
}

# --- SA 1266 阐陀（SN35.87／MN144 Channa）----------------------------------
SUTTAS["SA_1266"] = {
    "lit": [
        OPEN_BAM_LIT + "时尊者阐陀在那罗聚落菴罗林中，疾病困笃。"
        "尊者舍利弗与尊者摩诃拘絺罗往问病。",
        "阐陀言：「苦痛转增，唯欲执刀自杀。」"
        "舍利弗劝勿自害，当供衣药瞻病。阐陀言：「供养无乏；我久敬事大师，当无罪自杀。」",
        "舍利弗问：「眼色识乃至意法，汝见是我、异我、相在不？」答：「不也。非我、不异我、不相在。"
        "我于彼见灭、知灭故，作如是观。」"
        "摩诃拘絺罗说依止动摇乃至纯苦聚集；无依则止息，纯大苦聚灭。",
        "阐陀言：「供养大师事毕，适意非不适意。」遂以刀自杀。",
        "舍利弗白佛问趣。佛言：「彼已自记无罪。若捨此身而余身相续，我说有过；"
        "捨此身已余身不相续，我说无大过。阐陀无罪而自杀。」为说第一记。",
        "尊者舍利弗闻已，欢喜作礼而去。",
    ],
    "mod": [
        OPEN_BAM_MOD + "那时阐陀尊者在那罗聚落菴罗林中，病重困苦。"
        "舍利弗尊者与摩诃拘絺罗尊者前去探病。",
        "阐陀说：「苦痛加重，只想用刀自杀。」"
        "舍利弗劝他不要自害，愿意供衣药、照顾病人。阐陀说：「供养并不缺；我长久敬事大师，将会无罪自杀。」",
        "舍利弗问：「眼、色、识一直到意与法，你看作是我、异我、相在吗？」答：「不是。非我、不异我、不相在。"
        "我在那些法上见灭、知灭，所以这样观察。」"
        "摩诃拘絺罗说：有依止就动摇，一直到纯苦聚集；无依止就止息，纯大苦聚灭。",
        "阐陀说：「供养大师的事已经做完，心中适意。」于是用刀自杀。",
        "舍利弗问佛他生往何处。佛说：「他已亲自声明无罪。若捨此身还有余身相续，我说有过；"
        "捨此身后余身不再相续，我说没有大过。阐陀是无罪而自杀。」于是为他作第一记别。",
        "舍利弗尊者听完，欢喜作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN35.87／MN144 Channasutta。"
        "无罪自杀＝捨身已无后有相续；汉伴友摩诃拘絺罗（巴利多作 Mahācunda），名从汉；"
        "六入处非我＋依止／无依止链据平行收束。"
    ),
}

# --- SA 1267 济度（SN1.1 Oghataraṇa）---------------------------------------
SUTTAS["SA_1267"] = {
    "lit": [
        OPEN_JET_LIT,
        DEV_OPEN_LIT,
        "天子白佛：「比丘！云何度驶流耶？」佛言：「无所住立，亦无所求进，我度驶流。」"
        "「云何无所住立、无所求进而度？」"
        "「天子！我若住立则沈；若求进则漂。是故无所住立、无所求进，而度驶流。」",
        "天子说偈：「久见婆罗门，逮得般涅槃；一切怖已过，永超世恩爱。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEV_OPEN_MOD,
        "天子问佛：「比丘！您是怎么度过急流的？」佛说：「不站住，也不用力游，我度过了急流。」"
        "「怎样才能不站住、不用力游而度过呢？」"
        "「天子！我一站住就下沉；一用力游就被冲走。所以不站住、不用力游，而度过急流。」",
        "天子说偈：「久见婆罗门，逮得般涅槃；一切怖已过，永超世恩爱。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.1 Oghataraṇasutta。"
        "据 SN：appatiṭṭhaṁ anāyūhaṁ——不住不进（汉「抱／直进」拙译，据义改）；"
        "住则沈、进则漂。"
    ),
}

# --- SA 1268 解陀（SN1.2 Nimokkha）-----------------------------------------
SUTTAS["SA_1268"] = {
    "lit": [
        OPEN_JET_LIT,
        DEV_OPEN_LIT,
        "天子白佛：「比丘知众生解脱、遍解脱、远离不？」"
        "佛言：「知。」「云何知？」"
        "「爱喜有尽，想与识尽，诸受灭息，我如是知众生解脱、遍解脱、远离。」",
        "天子说偈：「久见婆罗门，逮得般涅槃；一切怖已过，永超世恩爱。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEV_OPEN_MOD,
        "天子问佛：「比丘知道众生的解脱、遍解脱、远离吗？」"
        "佛说：「知道。」「怎样知道？」"
        "「爱喜于有尽了，想与识尽了，诸受灭息，我这样知道众生的解脱、遍解脱、远离。」",
        "天子说偈：「久见婆罗门，逮得般涅槃；一切怖已过，永超世恩爱。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.2 Nimokkhasutta。"
        "据 SN：nandībhavaparikkhaya／saññāviññāṇasaṅkhaya／vedanānirodha；"
        "汉「爱喜灭尽，我心解脱」收束为有爱尽＋想识尽＋受灭。"
    ),
}

# --- SA 1269 流（≈SN2.15 Candana；resembling）------------------------------
SUTTAS["SA_1269"] = {
    "lit": [
        OPEN_JET_LIT,
        DEV_OPEN_LIT,
        "天子说偈问：「谁度于诸流，昼夜勤精进？不攀亦不住，何染而不著？」",
        "世尊说偈答：「一切戒具足，智慧善正受，精勤心决定，度难度诸流。"
        "不乐于欲想，超越于色结，爱贪已永尽，深渊而不沈。」",
        "天子说偈：「久见婆罗门，逮得般涅槃；一切怖已过，永超世恩爱。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEV_OPEN_MOD,
        "天子用偈问：「谁能度过诸流，昼夜精勤不懈？不攀缘也不住立，怎样染著却不沾？」",
        "世尊用偈答：「始终持戒具足，有智慧又善入定，精勤而心决定，能度过难度的诸流。"
        "远离欲想，超越色结，爱贪已经永尽，在深渊里也不下沉。」",
        "天子说偈：「久见婆罗门，逮得般涅槃；一切怖已过，永超世恩爱。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：SC resembling SN2.15 Candanasutta（偈近）；"
        "据平行：戒／慧／定／精进度流；离欲想、超色结、爱贪尽则不沈深渊。"
    ),
}

# --- SA 1270 拘迦尼（无巴利；SA2 平行）-------------------------------------
SUTTAS["SA_1270"] = {
    "lit": [
        OPEN_VAL_LIT,
        "时有拘迦尼光明天女，容色绝妙，于后夜来诣佛所，稽首佛足；"
        "身诸光明遍照山谷。即说偈言："
        "「心不作诸恶，身口亦复然；五欲观如空，正智善系念。"
        "不习近众苦，不与非义合。」",
        "佛言：「如是，如是。」即述其偈而印可之。"
        "天女闻已，欢喜随喜，稽首佛足，即没不现。",
        "夜过晨朝，佛入僧中，告诸比丘，具说昨夜天女来偈及己所印可。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VAL_MOD,
        "那时有位拘迦尼光明天女，容色绝妙，后夜来到佛前，稽首佛足；"
        "身上的光明照遍山谷。她说偈道："
        "「心不作恶，身口也不作恶；五欲看作空虚，正智而善系念。"
        "不亲近招来众苦的事，不与无益的事和合。」",
        "佛说：「正是这样。」便复述她的偈，表示印可。"
        "天女听完，欢喜随喜，稽首佛足，随即隐没不见。",
        "夜过清晨，佛进入僧众中，告诉比丘们，把昨夜天女来偈和自己所印可的事都说了。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：SC 仅 SA2 平行，无可靠巴利；"
        "依汉本雅化：心口身不作恶、五欲如空、正智系念。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {
    "SA_1251": "high",
    "SA_1252": "high",
    "SA_1253": "high",
    "SA_1254": "high",
    "SA_1255": "high",
    "SA_1256": "high",
    "SA_1257": "high",
    "SA_1258": "high",
    "SA_1259": "medium",
    "SA_1260": "high",
    "SA_1261": "medium",
    "SA_1262": "high",
    "SA_1263": "medium",
    "SA_1264": "medium",
    "SA_1265": "high",
    "SA_1266": "high",
    "SA_1267": "high",
    "SA_1268": "high",
    "SA_1269": "medium",
    "SA_1270": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1251": "汉「如上广说」peeyāla → 据 AN6.42 补喧闹求施／不乐名称框架，并校正空闲好恶",
    "SA_1256": "汉误植慈心多少 → 据 SN20.2 改正为人间受生少／不放逸",
    "SA_1262": "汉「欲求野狐形类」与 SN20.11 相反 → 据巴利改正为得此身犹幸",
    "SA_1265": "汉略「见法即见我」→ 据 SN22.87 补；病问安／五阴问答 peeyāla 收束",
    "SA_1267": "汉「抱／直进」拙译 → 据 SN1.1 appatiṭṭha／anāyūha 改正",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

BATCH_IDS = [f"SA_{i}" for i in range(1251, 1271)]
NEIGHBOR_IDS = {"SA_1250", "SA_1271"}

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

assert set(GOLD) == set(BATCH_IDS), f"GOLD keys mismatch: {set(GOLD) ^ set(BATCH_IDS)}"
assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
assert set(RECONSTRUCTED) <= set(GOLD)
assert NEIGHBOR_IDS.isdisjoint(GOLD), "must not merge neighbors SA_1250／SA_1271"


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

    neighbor_before = {
        rec["id"]: _snap(rec) for rec in records if rec["id"] in NEIGHBOR_IDS
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

    for rid, before in neighbor_before.items():
        for rec in merged:
            if rec["id"] == rid:
                assert before == _snap(rec), f"{rid} (neighbor) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1251-1270.json").write_text(
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1251, 1271)
    )
    neighbors_untouched = all(rid not in GOLD for rid in NEIGHBOR_IDS)

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

    yan_ok = "生厌、离贪、解脱" in (by_merged["SA_1257"].get("kumarajiva_style_text") or "")

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1251–SA_1270 only)")
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
    print(f"continuous_1251_1270_goldish={continuous}")
    print(f"SA_1250_SA_1271_untouched={neighbors_untouched}")
    print(f"SA_1257_厌故离贪={yan_ok}")
    if needs_restyle:
        print("needs_restyle_detail:")
        for r in needs_restyle:
            print(f"  {r['id']} sim={r['sim']} reasons={r.get('gate_reasons')}")
    if fails:
        print("fail_detail:")
        for r in fails:
            print(f"  {r['id']} issues={r.get('issues')}")
    for r in sorted(report, key=lambda x: x["id"]):
        print(
            f"  {r['id']}: status={r['review_status']} conf={r['confidence']} "
            f"val={r['status']} sim={r['sim']} paras={r['paragraphs']}"
        )


if __name__ == "__main__":
    main()
