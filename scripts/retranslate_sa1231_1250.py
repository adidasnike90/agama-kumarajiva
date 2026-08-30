#!/usr/bin/env python3
"""Retranslate SA 1231–1250（刹利相应末＋譬喻相应起）→ merge.

本批二十经：
1231–1240 刹利相应（捕鱼 SN3.7、悭 SN3.19、命终 SN3.20、祠祀 SN3.9、
         繁缚 SN3.10、得胜 SN3.14、毁坏 SN3.15、徒佛教 SN3.18、
         一法 SN3.17、福田／老病死 SN3.3）
1241–1250 譬喻相应（给孤独、上中下者、二净法 AN2、燃烧法、恶行 AN3.17、
         铸金者 AN3.101／AN3.102、牧牛者 MN34／MN33、那提迦 AN8.86）

信：有 SN／AN／MN 平行者据巴利／Sujato 厘义；汉本拙译／异偈据平行校正。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold；virāga 作「厌故离贪」。
边界：只合并 SA_1231–1250；不触碰 SA_1230／SA_1251（邻经）；
      断言邻经关键字段不变。
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

OPEN_GOLD_LIT = "如是我闻：一时，佛住王舍城金师住处。"
OPEN_GOLD_MOD = "我是这样听说的：有一次，佛住在王舍城金师住处。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "佛说此经已，波斯匿王闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY_MOD = "佛说完这部经，波斯匿王听佛所说，欢喜随喜，作礼离去。"

CLOSE_LAY2_LIT = "彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY2_MOD = "他听佛所说，欢喜随喜，作礼离去。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

SUTTAS: dict[str, dict] = {}

# --- SA 1231 捕鱼（SN3.7 Aḍḍakaraṇa）--------------------------------------
SUTTAS["SA_1231"] = {
    "lit": [
        OPEN_JET_LIT,
        "时波斯匿王于正殿断事，见胜刹利、婆罗门、长者大姓因欲故故作妄语，念：「止此断事！"
        "我有贤子，当令断事。何须亲见此等因贪欺妄？」"
        "即往诣佛，稽首退坐，以是事白佛。",
        "佛言：「如是，大王！彼等因欲故妄语，长夜当得不饶益苦。"
        "譬如渔夫截流张网，残杀众生；彼亦如是——贪欲迷醉，不觉已陷，如鱼入网，后必剧苦。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时波斯匿王在正殿断案，看见胜刹利、婆罗门、长者大姓因为欲乐故意说谎，心想：「停止断案吧！"
        "我有贤良的儿子，让他去断。何必亲眼看这些人因贪欺诈说谎？」"
        "便来到佛那里，顶礼后退坐，把这件事告诉佛。",
        "佛说：「正是这样，大王！他们因欲说谎，长夜会得不饶益的苦。"
        "好比渔夫截流张网杀害众生；他们也一样——被贪欲迷醉，不觉已经陷落，如同鱼入网，以后必受剧苦。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.7 Aḍḍakaraṇasutta。"
        "据 SN：富族因欲故作妄语，长夜不利；偈义为贪欲迷醉如鱼入网。"
        "汉「渔夫张网」喻与巴利「鱼迅被网」同轨，压缩罗什风。"
    ),
}

# --- SA 1232 悭（SN3.19 Aputtaka 1）---------------------------------------
SUTTAS["SA_1232"] = {
    "lit": [
        OPEN_JET_LIT,
        "时波斯匿王来诣，稽首退坐，白言：「舍卫有长者摩诃男，巨富积金；"
        "然食粗恶、衣弊屣、乘败车，闭门而食，未尝施与沙门婆罗门及贫穷乞者。」",
        "佛言：「此非善士。得胜财而不自受用，不供父母妻子眷属仆使知识，"
        "不时施沙门婆罗门种胜福田——财不得其用，如旷野池水，无人饮浴，自干消尽。"
        "善男子得胜财，自乐受用，供恤亲眷，时施福田——如聚落边清凉池，人畜皆得受用。」",
        "尔时说偈：「恶士得财，自苦积聚；慧者得财，施受两成，乘理命终，生天受乐。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时波斯匿王到来，顶礼后退坐，说：「舍卫有位长者摩诃男，非常富有；"
        "却吃粗劣的饭、穿破衣、乘破车，关上门吃饭，从不布施给沙门婆罗门和贫穷乞讨的人。」",
        "佛说：「这不是善士。得到大财却不自己享用，不供养父母妻子眷属仆使朋友，"
        "也不适时布施沙门婆罗门种胜福田——财富得不到正当使用，如同旷野池水无人饮用沐浴，自己干涸消尽。"
        "善男子得到大财，自己安乐享用，供养周济亲眷，适时布施福田——如同聚落边清凉的池水，人畜都能受用。」",
        "那时说偈：「恶人得财，自己苦苦积聚；慧者得财，布施与受用都成就，如法命终，生天受乐。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.19 Aputtakasutta。"
        "汉作在世悭吝摩诃男，SN 以无子命终转入王库开端；教学（不善用财／池喻）从 SN。"
        "据 SN 补：财不得用则王贼水火怨嗣夺之——义摄入「不得其用」。"
    ),
}

# --- SA 1233 命终（SN3.20 Aputtaka 2）-------------------------------------
SUTTAS["SA_1233"] = {
    "lit": [
        OPEN_JET_LIT,
        "舍卫长者摩诃男命终无子，财入王家。波斯匿王日中蒙尘来诣，稽首退坐。"
        "佛问：「大王从何所来，似有疲倦？」"
        "「摩诃男无子，财入王家；料理疲极，故来。」",
        "佛言：「彼昔遇多迦罗尸弃辟支佛，使人施食；非净信、不恭敬、不自手与，施已变悔。"
        "由施福七生三十三天，七生舍卫最富；以不净施故，虽富而受用粗弊。"
        "又曾杀异母兄夺财，地狱百千岁；余报七生无子，财没王家。"
        "今旧福尽，未积新福，悭贪放逸，命终已堕地狱。」",
        "王悲泣拭泪。佛说偈：「唯罪福业，是己所有，如影随形。"
        "少粮远行必苦；修德淳厚，善趣长乐。是故当修福，建立他世乐。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "舍卫长者摩诃男去世没有儿子，财产归入王库。波斯匿王大白天满身尘土到来，顶礼后退坐。"
        "佛问：「大王从哪里来，好像很疲倦？」"
        "「摩诃男没有儿子，财产归入王库；我料理得很累，所以来了。」",
        "佛说：「他从前遇到多迦罗尸弃辟支佛，派人布施饮食；却不是净信、不恭敬、不亲手给，给了又后悔。"
        "因为那次布施的福，七次生到三十三天，七次生在舍卫最富的家；因为布施不净，虽然富裕却只用粗劣的衣食。"
        "他又曾杀害异母兄长夺取财产，在地狱受了百千岁苦；残余果报是七生没有儿子，财产没入王库。"
        "现在旧福已尽，没有积新福，又悭贪放逸，死后已经堕入地狱。」",
        "王悲伤哭泣、用衣拭泪。佛说偈：「只有罪福业是自己的，如影随形。"
        "少带干粮远行必苦；修德深厚，在善趣长久安乐。所以应当修福，建立来世的安乐。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.20 Aputtakasutta。"
        "Tagarasikhī 施食／悔施／杀兄夺财／七生无子入王库——据 SN；"
        "汉「不净信、不恭敬、不自手」三过与 SN 悔施相应，保留。"
    ),
}

# --- SA 1234 祠祀（SN3.9 Yañña）-------------------------------------------
SUTTAS["SA_1234"] = {
    "lit": [
        OPEN_JET_LIT,
        "时波斯匿王设大祠，系千牛等，集诸外道。众多比丘入城乞食，闻已还白世尊。",
        "佛即说偈：「马祠人祠、掷轭、王苏摩、无碍大祀——杀生暴恶，果报不大。"
        "正行大仙不赴杀羊牛等之祀；赴不杀生、清净吉祥之祀。"
        "智者如是祠，果大增上，诸天亦喜。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时波斯匿王举办大祭祀，绑起成千的牛等，召集外道。许多比丘进城乞食，听闻后回来告诉世尊。",
        "佛便说偈：「马祭、人祭、掷轭祭、王苏摩祭、无碍大祭——杀害生命、手段暴恶，果报并不大。"
        "正行的大仙不去参加杀羊牛等的祭祀；只参加不杀生、清净吉祥的祭祀。"
        "智者这样祭祀，果报大而且增上，诸天也欢喜。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.9 Yaññasutta。"
        "汉偈「月月大会不及信佛十六分」与 SN 异；"
        "据 SN 校正为马祠人祠等暴恶无大果、不杀生祀乃大果（gold_reconstructed）。"
    ),
}

# --- SA 1235 繁缚（SN3.10 Bandhana）---------------------------------------
SUTTAS["SA_1235"] = {
    "lit": [
        OPEN_JET_LIT,
        "时波斯匿王多所囚执——刹利乃至旃陀罗，持戒犯戒、在家出家，或锁杻、或以绳缚。"
        "众多比丘乞食闻已，还白世尊。",
        "佛说偈：「铁木绳杻，智者不名为坚缚；染念钱财妻子，是缚长固、缓而难脱。"
        "慧者不顾五欲，断此诸缚，出家无忧，永超于世。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时波斯匿王大量关押人——从刹利到旃陀罗，持戒的犯戒的、在家的出家的，有的上锁铐、有的用绳绑。"
        "许多比丘乞食听闻后，回来告诉世尊。",
        "佛说偈：「铁、木、绳、铐，智者说那不算坚固的束缚；染著惦念钱财妻子，才是又长又固、看起来松却难脱的缚。"
        "慧者不顾念五欲，斩断这种束缚，出家无忧，永远超出世间。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.10 Bandhanasutta。"
        "据 SN：铁木绳非坚缚；恋珠宝妻儿乃坚缚，难脱；断已出家舍欲。"
    ),
}

# --- SA 1236 得胜（SN3.14 Saṅgāma 1）--------------------------------------
SUTTAS["SA_1236"] = {
    "lit": [
        OPEN_JET_LIT,
        "摩竭阿阇世起四种军攻拘萨罗；波斯匿亦集四军迎战。阿阇世胜，波斯匿败还舍卫。"
        "众多比丘乞食闻已，还白世尊。",
        "佛言：「阿阇世恶友相得；波斯匿善友相得。然今日败者，当夜卧不安。」"
        "说偈：「战胜增怨，败苦不眠；胜败俱舍，卧觉寂静。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "摩竭陀阿阇世发动四种军攻打拘萨罗；波斯匿也集结四军迎战。阿阇世获胜，波斯匿败退回到舍卫。"
        "许多比丘乞食听闻后，回来告诉世尊。",
        "佛说：「阿阇世交的是恶友；波斯匿交的是善友。可是今天战败的人，夜里会睡不安稳。」"
        "说偈：「打胜了会增添怨敌，战败了苦得睡不着；把胜败都放下，睡醒都寂静安乐。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.14 Paṭhamasaṅgāmasutta。"
        "据 SN 补恶友／善友判语；偈「胜败俱舍」从 SN。"
    ),
}

# --- SA 1237 毁坏（SN3.15 Saṅgāma 2）--------------------------------------
SUTTAS["SA_1237"] = {
    "lit": [
        OPEN_JET_LIT,
        "阿阇世再来攻；波斯匿倍军得胜，生擒阿阇世，载与同车诣佛。"
        "王白：「彼长夜于我无怨而生怨；然是善友之子，当放还国。」"
        "佛言：「善哉！放之，令汝长夜安乐。」",
        "说偈：「人掠人利，利尽还为他所掠。愚以恶未熟自谓安固；恶熟则堕苦。"
        "杀者招杀，胜者招胜——业转相报，掠人者终为人所掠。」",
        "二王闻已，欢喜作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "阿阇世再来进攻；波斯匿加倍出军得胜，活捉阿阇世，同车载到佛那里。"
        "王说：「他长期对我无怨却结怨；可他是好友的儿子，应当放他回国。」"
        "佛说：「很好！放了他，让你长夜安乐。」",
        "说偈：「人靠掠夺得利，利尽了反被别人掠夺。愚人恶业未成熟时自以为安稳；恶业一熟就堕苦。"
        "杀人的招来被杀，征服的招来被征服——业力辗转相报，掠夺别人的终被人掠夺。」",
        "两位国王听完，欢喜作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.15 Dutiyasaṅgāmasutta。"
        "汉偈极略；据 SN 补掠者被掠、恶未熟自安、杀胜相报诸义（gold_reconstructed）。"
        "放甥还国从汉／SN 共同叙事。"
    ),
}

# --- SA 1238 徒佛教（SN3.18 Kalyāṇamitta）---------------------------------
SUTTAS["SA_1238"] = {
    "lit": [
        OPEN_JET_LIT,
        "波斯匿王独静思惟：「世尊正法，现见离炽然、不待时、通达可证——"
        "是则善知识、善伴党，非恶知识。」来白世尊。",
        "佛言：「如是。所以者何？我为众生作善知识：有生老病死忧悲恼苦者，悉令解脱。」",
        "「昔阿难白我：『半梵行者，谓善知识。』我告：『莫作是语！善知识是全梵行。"
        "依善知识，能修八正道——依远离、依离贪、依灭，向于捨。"
        "又依我为善友，有生老死等苦者得解脱——是故善知识是全梵行。"
        "大王当学：我当有善友；有善友已，当依一法——于诸善法不放逸。』」",
        "说偈：「赞叹不放逸，是则佛正教；修禅不放逸，逮证诸漏尽。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "波斯匿王独自静思：「世尊的正法，现前可见、离开烧恼、不等待时节、可以通达亲证——"
        "这就是善知识、善伴侣，不是恶知识。」前来禀告世尊。",
        "佛说：「正是这样。为什么？我为众生作善知识：有生老病死忧悲恼苦的，都让他们得解脱。」",
        "「从前阿难对我说：『梵行的一半，就是善知识。』我告诉他：『不要这么说！善知识是全部的梵行。"
        "依靠善知识，就能修习八正道——依于远离、依于离贪、依于灭，趋向於捨。"
        "又因为依靠我作善友，有生老死等苦的人得到解脱——所以善知识是全部的梵行。"
        "大王应当学：我要有善友；有了善友，还要依止一件事——在各种善法上不放逸。』」",
        "说偈：「赞叹不放逸，这就是佛的正教；修禅而不放逸，就能证得诸漏尽。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.18 Kalyāṇamittasutta。"
        "据 SN 校正：善知识是全梵行（非「半」）；八正道依远离／离贪／灭／捨；"
        "有善友已当依不放逸（gold_reconstructed）。「厌故离贪」义摄入「依离贪」。"
    ),
}

# --- SA 1239 一法（SN3.17 Appamāda；兼 SN45 足迹喻）------------------------
SUTTAS["SA_1239"] = {
    "lit": [
        OPEN_JET_LIT,
        "波斯匿王独静思惟：「颇有一法，修习多修，得现法利、后世利、现法后世利不？」来白佛。",
        "佛言：「有——谓不放逸于善法。譬如诸兽足迹悉入象迹，象迹最大；"
        "不放逸亦复如是，能摄现法后世二利。"
        "大王当住不放逸、依不放逸；夫人、太子、大臣、将士、国人皆当随学。"
        "如是则能自护，仓藏丰实。」",
        "说偈：「称誉不放逸，毁呰放逸；不放逸具足，摄持二义——现法及后世，是名慧者。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "波斯匿王独自静思：「可有一种法，修习得多了，能得现世利益、后世利益、现世后世都利益吗？」前来问佛。",
        "佛说：「有——就是在善法上不放逸。好比一切走兽的足迹都容得进象的足迹，象迹最大；"
        "不放逸也是这样，能统摄现世和后世两种利益。"
        "大王应当安住不放逸、依靠不放逸；夫人、太子、大臣、将士、国人也都应当随学。"
        "这样就能守护自己，库藏丰足。」",
        "说偈：「称赞不放逸，呵责放逸；不放逸圆满，就握住两种义——现世与后世，这才叫有智慧的人。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：义主 SN3.17 Appamādasutta（SC 表亦列 SN45.141–148 足迹群）。"
        "据 SN3.17：一法＝不放逸，摄现法后世利；象迹喻从 SN。"
        "汉「种子、根、陆水」等广喻删省，义已摄于象迹／二利。"
    ),
}

# --- SA 1240 福田／老病死（SN3.3 Jarāmaraṇa）------------------------------
SUTTAS["SA_1240"] = {
    "lit": [
        OPEN_JET_LIT,
        "波斯匿王白佛：「有生者，颇有脱老死不？」"
        "佛言：「大王！有生则无有脱于老死。"
        "胜刹利、婆罗门、长者大姓，多财巨富，生已亦不能免老死。"
        "乃至漏尽阿罗汉，所作已办，身亦当坏散。」",
        "说偈：「王乘宝车，终归朽坏；此身亦然，迁移归老。"
        "如来正法，无有衰老；禀斯法者，永到安隐。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "波斯匿王问佛：「已经受生的人，还有能免于老死的吗？」"
        "佛说：「大王！有生就不能免于老死。"
        "胜刹利、婆罗门、长者大姓，即使多财巨富，生了也不能免老死。"
        "乃至漏尽的阿罗汉，所作已办，身体也终须坏散。」",
        "说偈：「王所乘的宝车，终归会朽坏；这个身体也一样，迁变而归于老。"
        "如来的正法没有衰老之相；禀受这正法的人，永远到达安隐处。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN3.3 Jarāmaraṇasutta。"
        "汉作『老病死世间不爱故佛出兴』与 SN 问答异；"
        "据 SN 校正为：有生则无免老死，富族与阿罗汉身亦然（gold_reconstructed）。"
    ),
}

# --- SA 1241 给孤独（无主平行）--------------------------------------------
SUTTAS["SA_1241"] = {
    "lit": [
        OPEN_JET_LIT,
        "给孤独长者白佛：「凡在我舍者皆得净信；于我舍命终者皆生天上。」"
        "佛言：「善哉深说。谁告汝耶？比丘、比丘尼、诸天、或从我闻？抑自证知？」"
        "答：「皆不也。」",
        "「云何作师子吼？」"
        "「世尊！妊妇生子，我教归佛、法、僧，生已教三归，知法已教持戒；"
        "买奴仆、佣客、弟子、举贷，皆先要三归五戒。"
        "供佛僧时称父母妻子宗亲存亡之名而咒愿；又闻世尊说：因施园田房舍床座、乃至一抟之施，称名咒愿，皆得生天。」",
        "佛言：「善哉！以信能作是说。如来无上知見，审知汝舍命终者皆生天上。」",
        CLOSE_LAY2_LIT.replace("彼", "长者"),
    ],
    "mod": [
        OPEN_JET_MOD,
        "给孤独长者对佛说：「凡是在我家里的人都得到净信；在我家里去世的都生到天上。」"
        "佛说：「说得好，很深刻。谁告诉你的？比丘、比丘尼、诸天、还是从我听来的？或者自己亲证知道？」"
        "答：「都不是。」",
        "「那你凭什么作这样的师子吼？」"
        "「世尊！妇人怀孕生子，我就教她们归依佛、法、僧，生下来教三归，懂事了教持戒；"
        "买奴仆、雇工、收弟子、放贷，都先要求受三归五戒。"
        "供养佛和僧时，称呼父母妻子宗亲在世或已故的名字来祝愿；又听世尊说过：因为布施园田房舍床座、乃至一团食物，称名祝愿，都能生天。」",
        "佛说：「很好！你凭信心能这样说。如来有无上知見，确实知道在你家里去世的都生到天上。」",
        "长者听佛所说，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：给孤独教舍人三归五戒／称名咒愿生天。"
        "删卷首题署；罗什风压缩问答链。"
    ),
}

# --- SA 1242 上中下者（无主平行）------------------------------------------
SUTTAS["SA_1242"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告诸比丘：「当恭敬住，系心畏慎，随顺修梵行上中下座。"
        "若不恭敬、不系心，欲威仪具足——无有是处；威仪不具，欲学法满——无有是处；"
        "学法不满，欲戒定慧解脱解脱知见具足——无有是处；解脱知见不满，欲得无余涅槃——无有是处。"
        "若勤恭敬、系心畏慎，随他德力，则威仪、学法、五分法身次第可具，乃至无余涅槃——斯有是处。"
        "当如是学。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「应当恭敬而住，收摄其心、心怀敬畏，随顺修行梵行的上座、中座、下座。"
        "若不恭敬、不收心，却想威仪具足——没有这回事；威仪不具足，却想学法圆满——没有这回事；"
        "学法不圆满，却想戒定慧解脱解脱知见都具足——没有这回事；解脱知见不满足，却想得无余涅槃——没有这回事。"
        "若勤加恭敬、收心敬畏，随顺他人德行，则威仪、学法、五分法身可以次第具足，一直到无余涅槃——这才有可能。"
        "应当这样学。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：恭敬→威仪→学法→五分法身→无余涅槃连锁。"
        "早期道次第，无大乘语；压缩双重「无有是处／斯有是处」。"
    ),
}

# --- SA 1243 二净法（AN2 hiri/ottappa）------------------------------------
SUTTAS["SA_1243"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告诸比丘：「有二净法能护世间：惭与愧。"
        "若无此二，则不知父母兄弟妻子师长尊卑，浑乱如畜生。"
        "有惭愧故，尊卑有序，不堕畜生趣。」",
        "说偈：「无惭愧则违清净道，向生老病死；有惭愧则增清净道，永闭生死门。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「有两种净法能守护世间：惭和愧。"
        "如果没有这两种，就不知父母兄弟妻子师长的尊卑，混乱如同畜生。"
        "有惭愧，尊卑才有秩序，不会堕入畜生的状态。」",
        "说偈：「没有惭愧就会违背清净之道，趋向生老病死；有惭愧就能增长清净之道，永远关闭生死之门。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：平行 AN2（hiri/ottappa 护世）。"
        "二净法＝惭愧；护世间伦理——与巴利护世法相应。"
    ),
}

# --- SA 1244 燃烧法（无主平行；保早期业报框架）----------------------------
SUTTAS["SA_1244"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告诸比丘：「有烧燃法、不烧燃法。谛听，当说。」",
        "「云何烧燃？男女犯戒行恶，身口意恶成就；疾病困笃时，先恶尽现，如日西山影。"
        "心生追悔：『咄！不修善，当堕恶趣！』悔已不得善心，不善命终，后世续恶——是名烧燃。」",
        "「云何不烧燃？持戒修善，身口意善；苦患临终，攀缘先善：『我作诸善，当生善趣。』"
        "心不变悔，善心命终，后世续善——是名不烧燃。」",
        "说偈：「非法活命，种烧燃业，必生地狱；修善柔和，善心而终。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「有燃烧法、不燃烧法。仔细听，我来说明。」",
        "「什么是燃烧？男女犯戒作恶，身口意恶行成就；病重卧床时，以前的恶业全部现前，如同太阳西沉山影覆盖。"
        "心里追悔：『唉！不修善，要堕恶趣了！』悔恨之后生不起善心，以不善心命终，后世继续不善——这叫燃烧。」",
        "「什么是不燃烧？持戒修善，身口意善行成就；痛苦临终时，攀缘以前的善：『我做了各种善，应当生善趣。』"
        "心不懊悔，以善心命终，后世继续善——这叫不燃烧。」",
        "说偈：「靠非法活命，种下燃烧业，必定生地狱；修善心柔和，以善心而终。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：临终忆恶悔恼／忆善不悔——早期业报定型。"
        "汉广列八大地狱删省，保留烧燃／不烧燃对照核心。"
    ),
}

# --- SA 1245 恶行（AN3.17）------------------------------------------------
SUTTAS["SA_1245"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告诸比丘：「能捨身恶行者，我乃说彼捨身恶行——以彼得身恶行断故。"
        "身恶行无义不利；离身恶行，则义利安乐。口、意恶行亦如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「能够舍离身恶行的人，我才说他舍离了身恶行——因为他真正断除了身恶行。"
        "身恶行没有义利、不能安乐；离开身恶行，才有义利与安乐。口恶行、意恶行也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：平行 AN3.17（舍恶行＝能得彼断）。"
        "三业对称压缩。"
    ),
}

# --- SA 1246 铸金者（AN3.101；SC 亦列 SN46.33）----------------------------
SUTTAS["SA_1246"] = {
    "lit": [
        OPEN_GOLD_LIT,
        "佛告诸比丘：「如铸金者淘沙：先去刚石，次去粗沙，次去细沙黑土，犹有似金微垢；"
        "入炉鼓韛，垢尽而金犹重脆不光；再三陶炼，乃轻软光泽，屈伸不断，可作严具。」",
        "「净心比丘亦尔：先断粗缠恶业邪见；次断欲觉恚觉害觉；次断亲里人众生天等觉；"
        "次除善法觉令心纯净。若三昧为行所持，不得寂静漏尽——如金未调。"
        "若得三昧不为行持，寂静息乐，一心漏尽；离觉观入诸禅，柔软不动，于诸入处悉能作证——"
        "如金调熟，随意所作。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_GOLD_MOD,
        "佛告诉比丘们：「如同炼金的人淘洗沙土：先去掉硬石，再去掉粗沙，再去掉细沙黑土，还留有像金的微垢；"
        "放进炉里鼓风，垢秽虽除，生金仍重脆无光；再三陶炼，才轻软光泽，弯折不断，可以做成饰品。」",
        "「净心修行的比丘也是这样：先断粗重的烦恼缠、恶不善业、邪见；再断欲寻、恚寻、害寻；再断亲里、人众、生天等寻思；"
        "再除去关于善法的寻思，使心纯净。如果三昧还被造作之力把持，不得寂静、不能漏尽——如同金子还未调熟。"
        "如果得到三昧不被造作把持，寂静息乐，一心漏尽；离开觉观进入诸禅，柔软不动，在各种入处都能作证——"
        "如同金子调熟，可以随意制作。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：义主 AN3.101（淘金四阶段）；SC 亦列 SN46.33 五心垢（略本）。"
        "汉『善法觉』当除令心净——从 AN『只剩法寻，仍须再炼』；"
        "禅那柔软可作证从 AN／汉共同收束。"
    ),
}

# --- SA 1247 铸金者（AN3.102）---------------------------------------------
SUTTAS["SA_1247"] = {
    "lit": [
        OPEN_BAM_LIT,
        "佛告诸比丘：「当随时思惟三相：止相、举相、捨相。"
        "一向止则心下劣；一向举则掉乱；一向捨则不得正定尽漏。"
        "若时止、时举、时捨，心则正定，尽诸有漏。」",
        "「如巧金师：时鼓韛、时水洒、时俱捨——一向鼓则焦，一向洒则硬，一向捨则不熟。"
        "三者随时，金得调适，随事所用。比丘于三相亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "佛告诉比丘们：「应当适时修习三相：止相、举相、捨相。"
        "一味只修止，心会沉下；一味只修举，心会掉举；一味只修捨，就不能正定而尽漏。"
        "若有时修止、有时修举、有时修捨，心就能正定，尽诸有漏。」",
        "「如同巧炼金师：有时鼓风、有时洒水、有时只是看顾——一味鼓风会烧焦，一味洒水会变硬，一味不管就不会熟。"
        "三者适时配合，金子才调适，可随用途来用。比丘对三相也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN3.102（定／精勤／捨三基础）。"
        "汉止／举／捨＝samādhi／paggaṇa／upekkhā 三基；金师喻从 AN。"
    ),
}

# --- SA 1248 牧牛者（MN34）------------------------------------------------
SUTTAS["SA_1248"] = {
    "lit": [
        OPEN_BAM_LIT,
        "佛告诸比丘：「昔摩竭有愚牧牛人，夏末不善观恒河此岸彼岸，驱牛峻岸上下，洄澓多难。"
        "有智牧牛人善观两岸，先度领群大牛截流，次度壮牛，次羸小，犊随母，皆安隐度。」",
        "「愚牧牛者——六师富兰那等邪见；不观此世他世，中遭魔难。"
        "智牧牛者——如来；声闻漏尽不生，如大牛截魔贪流，度生死苦岸。"
        "断五下分得阿那含——如次牛；薄贪瞋痴得斯陀含——如羸牛；"
        "断三结得须陀洹——如犊随母：皆截魔流，安度彼岸，究竟苦边。」",
        "说偈：「此世他世，佛智显现；断截魔流，开甘露门，逮得安隐。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "佛告诉比丘们：「从前摩竭陀有个愚笨的牧牛人，夏末不好好观察恒河此岸彼岸，把牛从陡岸赶下又赶上，中流漩涡很多灾难。"
        "有智慧的牧牛人善观两岸，先让领群的大牛截流渡过，再度壮牛，再度瘦弱的，牛犊跟着母亲，都平安得度。」",
        "「愚笨的牧牛人——好比六师富兰那等邪见；不观察此世他世，中途遭受魔难。"
        "有智慧的牧牛人——是如来；漏尽不受后有的声闻，如同大牛截断魔的贪流，度过生死苦的彼岸。"
        "断五下分结得阿那含——如同第二批牛；贪瞋痴淡薄得斯陀含——如同瘦弱的牛；"
        "断三结得须陀洹——如同犊随母：都截断魔流，安稳到达彼岸，究竟苦边。」",
        "说偈：「此世与他世，佛的智慧都显现；斩断魔流，开启甘露门，到达安隐处。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：平行 MN34 Cūḷagopālaka。"
        "四果配牧牛次第从 MN／汉；删冗复，保截魔贪流度岸。"
    ),
}

# --- SA 1249 牧牛者（MN33／AN11.17）---------------------------------------
SUTTAS["SA_1249"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告诸比丘：「牧牛人成就十一法，不能护牛令增安乐："
        "不知色、不知相、不去虫、不覆疮、不起烟、不知路、不知处、不知度处、不知食处、尽取其乳、不料理领群者。」",
        "「比丘成就十一法，亦不能自安安他。何等十一？"
        "不知色——不知四大及造色；不知相——不知愚相慧相；"
        "不去虫——欲恚害觉生而不断；不覆疮——六根取相不守护，漏随生；"
        "不起烟——不能为人分别法；不知道——不知八正道及法律；"
        "不知止处——于如来法不得欢喜出离；不知度处——不知经律论，不及时请问；"
        "不知食处——不知四念处；尽取其乳——受施不知限量；"
        "不称誉上座多闻者——不令众人宗敬奉事。」",
        "「反是十一法成就，则能自安安他——如善牧牛护群增长。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「牧牛人若有十一件事，就不能保护牛群、让它们增长安乐："
        "不知颜色、不知相状、不去虫、不盖疮、不生烟、不知路、不知住处、不知渡口、不知吃草处、把乳挤尽、不善照料领头牛。」",
        "「比丘若有十一法，也不能自安、安他。哪十一？"
        "不知色——不知四大和所造色；不知相——不知愚昧之相与智慧之相；"
        "不去虫——欲寻、恚寻、害寻生起却不断除；不覆疮——六根攀取形相不守护，烦恼漏跟着生；"
        "不起烟——不能为别人分别开示正法；不知道——不知八正道及法律；"
        "不知止处——对如来的法得不到欢喜出离；不知度处——不知经律论，不及时请问；"
        "不知食处——不知四念处；把乳挤尽——接受布施不知限量；"
        "不称誉上座多闻者——不让众人宗敬奉事。」",
        "「反过来成就这十一法，就能自安、安他——如同善牧牛人护持牛群增长。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：平行 MN33／AN11.17 Mahāgopālaka。"
        "十一法对应从 MN；汉『尽乳』字形保留为『尽取其乳』；压缩广说。"
    ),
}

# --- SA 1250 那提迦（AN8.86 Nāgita）---------------------------------------
SUTTAS["SA_1250"] = {
    "lit": [
        "如是我闻：一时，佛在拘萨罗人间游行，至一奢能伽罗聚落，住彼林中。"
        "旧住比丘那提迦为侍者。聚落刹利、婆罗门、长者各办一釜食置门外，高声争先唱言：『我先供世尊！我先供善逝！』",
        "佛闻多人高声，问那提迦：「何故林中多人高声唱说？」"
        "「皆闻世尊住此，欲先供养。愿世尊哀受彼食。」",
        "佛言：「莫以利养称我！我不求利养；莫以名称我！我不求名称。"
        "若人不得出要、远离、寂灭、等觉之乐，乃于供养有味有求。"
        "我于如是出要乐不求而得、无苦而得——于彼利养何味何求？"
        "诸天亦难得此乐；唯我得之。」",
        "那提迦白佛，欲说譬，以天雨水就下，喻信敬随世尊所住而来供养。佛仍拒，并说："
        "见比丘食好食已仰腹喘息偃卧，或饱腹缓行，或从园至园、从众至众——知彼未得出要乐。"
        "「当如是学：于五受阴观生灭，厌故离贪；于六触入处观集灭，厌故离贪；乐远离，精勤远离。」",
        "尊者那提迦闻已，欢喜随喜，作礼而去。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在拘萨罗人间游行，来到一奢能伽罗聚落，住在那里的林中。"
        "旧住比丘那提迦担任侍者。聚落里的刹利、婆罗门、长者各自办好一锅食物放在门外，高声争先喊：『我先供养世尊！我先供养善逝！』",
        "佛听见许多人高声，问那提迦：「为什么林中这么多人高声唱说？」"
        "「都听说世尊住在这里，想争先供养。愿世尊哀愍接受他们的食物。」",
        "佛说：「不要用利养称赞我！我不求利养；不要用名称赞我！我不求名称。"
        "若人得不到出离、远离、寂灭、正觉的快乐，才会对手供养有滋有味、有所希求。"
        "我于这样的出离之乐不求而得、没有辛苦而得——对那些利养还有什么滋味、有什么希求？"
        "诸天也难得这种乐；只有我得到了。」",
        "那提迦向佛请求说比喻，用天雨水往低处流，比喻信敬的人随世尊所住而来供养。佛仍然拒绝，并说："
        "看见比丘吃好食物后仰腹喘息仰卧，或吃饱缓缓行走，或从园到园、从一群人到另一群人——就知道他们还没得到出离之乐。"
        "「应当这样学：对五受阴观察生灭，厌故离贪；对六触入处观察集灭，厌故离贪；乐于远离，精勤远离。」",
        "尊者那提迦听完，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN8.86 Nāgitasutta（汉『那提迦』＝Nāgita）。"
        "据 AN：拒名闻利养；出要／远离／寂灭／觉乐不求而得。"
        "汉五受阴／六触入处『厌离住』据项目规约作「厌故离贪」（virāga）。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {
    "SA_1231": "high",
    "SA_1232": "high",
    "SA_1233": "high",
    "SA_1234": "high",
    "SA_1235": "high",
    "SA_1236": "high",
    "SA_1237": "high",
    "SA_1238": "high",
    "SA_1239": "high",
    "SA_1240": "high",
    "SA_1241": "medium",
    "SA_1242": "medium",
    "SA_1243": "high",
    "SA_1244": "medium",
    "SA_1245": "high",
    "SA_1246": "high",
    "SA_1247": "high",
    "SA_1248": "high",
    "SA_1249": "high",
    "SA_1250": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1234": "汉偈「月月大会不及信佛」与 SN3.9 暴恶大祀无大果／不杀生祀乃大果异；据巴利改正。",
    "SA_1237": "汉偈极略；据 SN3.15 补掠者被掠、恶未熟自安、杀胜相报。",
    "SA_1238": "汉阿难「半梵行」；SN3.18 明善知识是全梵行，并教依不放逸；据巴利改正。",
    "SA_1240": "汉『老病死故佛出兴』框架与 SN3.3『有生则无免老死』问答异；据巴利改正。",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

BATCH_IDS = [f"SA_{i}" for i in range(1231, 1251)]
NEIGHBOR_IDS = {"SA_1230", "SA_1251"} | {f"SA_{i}" for i in list(range(1211, 1231)) + list(range(1251, 1271))}

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
assert NEIGHBOR_IDS.isdisjoint(GOLD), "must not merge neighbor ids"


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
    (ROOT / "data" / "translated" / "validation_report_sa1231-1250.json").write_text(
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1231, 1251)
    )
    untouched_neighbors = all(f"SA_{i}" not in GOLD for i in (1230, 1251))

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1231–SA_1250 only)")
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
    print(f"continuous_1231_1250_goldish={continuous}")
    print(f"SA_1230_SA_1251_untouched={untouched_neighbors}")
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
