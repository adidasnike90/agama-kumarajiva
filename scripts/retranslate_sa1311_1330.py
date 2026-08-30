#!/usr/bin/env python3
"""Retranslate SA 1311–1330（杂相应末＋夜叉相应：昙摩～害及无害）→ merge.

本批二十经：
1311–1318 杂相应末（天子偈）：昙摩 SN2.5、所断 SN1.5、实智 SN2.6、度流≈SN10.3偈、
         栴檀 SN1.75／SN2.15、迦叶 SN2.1／SN2.2
1319–1330 夜叉相应：崛摩 SN10.4、白山（无）、宾伽罗 SN10.6、富那婆薮 SN10.7、
         曼尼遮闻（无）、箭毛 SN10.3、受斋 SN10.5、矌野 SN10.12、净／雄 SN10.9–11、
         七岳雪山 Snp1.9、害及无害 Ud4.4

信：有 SN／Snp／Ud 平行者据巴利／Sujato 厘义；无平行者降 medium。
达雅：白话与罗什风逐段对照；Devatā／夜叉冗复压缩；sim 门限见 assess_gold。
禁「厌故不乐」→「厌故离贪」（本批多偈颂／夜叉，无定型厌离句则不强插）。
边界：只合并 SA_1311–1330；不触碰 SA_1291–1310、SA_1331–1350。
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

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_DEV_LIT = "时彼天子闻佛所说，欢喜随喜，稽首佛足，即没不现。"
CLOSE_DEV_MOD = "那时天子听佛所说，欢喜随喜，顶礼佛足，随即隐没不见。"

CLOSE_YAK_LIT = "时彼夜叉闻佛所说，欢喜随喜，作礼而去。"
CLOSE_YAK_MOD = "那时夜叉听佛所说，欢喜随喜，作礼离去。"

DEVA_NIGHT_LIT = (
    "后夜分，有天子容色绝妙，来诣佛所，稽首礼足，退坐一面；"
    "身诸光明遍照祇树给孤独园。"
)
DEVA_NIGHT_MOD = (
    "后夜分，有一位天子容色绝妙，来到佛前，顶礼佛足，退坐一面；"
    "身上的光明遍照祇树给孤独园。"
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

# --- SA 1311 昙摩（SN2.5 Dāmali）-------------------------------------------
SUTTAS["SA_1311"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，昙摩尼天子容色绝妙，来诣佛所，稽首礼足，退坐一面；"
        "身诸光明遍照祇园。",
        "天子说偈：「婆罗门所应为：精进勿疲倦；舍离诸爱欲，不望受后有。」",
        "世尊说偈答：「婆罗门事已办，所作已成办。人未得河中立足处，则肢节用力泅；"
        "既得立足立于干地，已到彼岸，则不复泅。"
        "昙摩尼！漏尽禅思之婆罗门亦复如是：已至生老死尽边，不复用力，已到彼岸。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫昙摩尼的天子容色绝妙，来到佛前，顶礼佛足，退坐一面；"
        "身上光明遍照祇园。",
        "天子说偈：「婆罗门该做的是：精进不要疲倦；舍离爱欲，不指望再受后有。」",
        "世尊说偈答：「婆罗门的事已经办完，该做的都做成了。人若还没在河里站稳脚跟，"
        "就会手脚并用拼命游；一旦站稳、立在干地上，已经到了彼岸，就不必再游。"
        "昙摩尼！漏尽而禅思的婆罗门也是这样：已到生老死的尽头，不必再用力，已经到了彼岸。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.5 Dāmalisutta。"
        "汉「勤跪」＝āyūhati（用力泅），据巴利改「用力泅／不复泅」；"
        "未得 gādha（立足）则泅，得立足立干地则不泅——喻漏尽者已到彼岸。"
    ),
}

# --- SA 1312 所断（SN1.5 Katichinda）---------------------------------------
SUTTAS["SA_1312"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，多罗揵陀天子容色绝妙，来诣佛所，稽首礼足；身诸光明遍照祇园。",
        "天子说偈问：「断几捨几法？几法上增修？超越几积聚，名比丘度流？」",
        "世尊说偈答：「断五捨于五，五法上增修；超五种积聚，名比丘度流。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫多罗揵陀的天子容色绝妙，来到佛前，顶礼佛足；身上光明遍照祇园。",
        "天子说偈问：「要断几、捨几？还要增修几法？超越几种系缚，才叫比丘度过流？」",
        "世尊说偈答：「断五、捨五，再增修五法；超越五种系缚，才叫比丘度过流。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.5 Katichindasutta。"
        "五断／五捨／五增修／五积聚（saṅga）＝传统五下分结等义，汉本与巴利同轨。"
    ),
}

# --- SA 1313 实智（SN2.6 Kāmada）-------------------------------------------
SUTTAS["SA_1313"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，迦摩天子容色绝妙，来诣佛所，稽首礼足；身诸光明遍照祇园。",
        "天子白佛：「甚难！世尊！甚难！」"
        "佛说偈：「虽难，有学具戒定者犹能作；已入非家、心安住者，知足能生乐。」",
        "天子言：「知足甚难得！」"
        "佛说偈：「虽难得，乐于心寂者犹能得；昼夜意乐于修习。」",
        "天子言：「心难令正受！」"
        "佛说偈：「虽难定，乐于诸根寂者犹能定；已断死罗网，圣者随所欲行。」",
        "天子言：「险道甚难行！」"
        "佛说偈：「险而不平之道，圣者犹能行；非圣于险道头足倒置而堕。"
        "圣者之道路平，以圣者于不平处能平。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫迦摩的天子容色绝妙，来到佛前，顶礼佛足；身上光明遍照祇园。",
        "天子对佛说：「太难了！世尊！太难了！」"
        "佛说偈：「虽然难，具戒定的有学者还是能做到；已出家、心安住的人，知足能带来乐。」",
        "天子说：「知足很难得！」"
        "佛说偈：「虽然难得，乐于让心寂静的人还是能得到；昼夜心意都乐于修习。」",
        "天子说：「心很难入定！」"
        "佛说偈：「虽然难定，乐于诸根寂静的人还是能定；斩断了死神的网，圣者便随愿而行。」",
        "天子说：「这条险路很难走！」"
        "佛说偈：「路虽险不平，圣者还是走得通；非圣在险路上头朝下栽下去。"
        "圣者的路是平的，因为圣者在不平处也能走平。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.6 Kāmadasutta。"
        "据 SN 校正：tuṭṭhi＝知足（汉「静默」偏）；cittavūpasama／indriyūpasama；"
        "死网＝maccuno jāla；圣者于 visama 而 samo。"
    ),
}

# --- SA 1314 度流（偈＝SN10.3／Snp2.5；汉作天子问答）-----------------------
SUTTAS["SA_1314"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，迦摩天子容色绝妙，来诣佛所，稽首礼足，退坐一面；身诸光明遍照祇园。",
        "天子说偈问：「贪恚何所因？不乐、喜、身毛竖从何生？"
        "意中诸觉想从何起？如童子纵乌鸦，任其所之。」",
        "世尊说偈答：「贪恚从此因；不乐、喜、身毛竖从此生；意中觉想从此起，"
        "如童子纵乌鸦。爱润所生、自所起，如尼拘律从干生根；"
        "处处著于诸欲，如藤蔓遍林。若知彼因，则能遣除——夜叉当听！"
        "能度此难度流，未曾度者，不复受有。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫迦摩的天子容色绝妙，来到佛前，顶礼佛足，退坐一面；身上光明遍照祇园。",
        "天子说偈问：「贪和瞋从哪里来？不乐、喜乐、汗毛竖立从哪里生？"
        "心里的种种寻思从哪里起？好像孩子放走乌鸦，由它飞去。」",
        "世尊说偈答：「贪瞋从这里来；不乐、喜乐、汗毛竖立从这里生；心里的寻思从这里起，"
        "好像孩子放走乌鸦。它们由爱润而生、由自身而起，像尼拘律树从树干生出气根；"
        "处处黏着于欲，像藤蔓爬满树林。若知道它们从哪里来，就能遣除——夜叉啊，听着！"
        "能渡过这道难度的流，这是从前没渡过的，从此不再受后有。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：偈 primary SN10.3／Snp2.5 Sūciloma（叙事见 SA_1324）；"
        "汉框为天子问，存之。据巴利校正：kumārakā dhaṅkamivossajanti＝童子纵乌鸦"
        "（汉「依倚乳母」误）；snehajā attasambhūtā／nigrodha 气根／māluvā 藤。"
    ),
}

# --- SA 1315 栴檀（SN1.75 Bhīta）-------------------------------------------
SUTTAS["SA_1315"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，栴檀天子容色绝妙，来诣佛所，稽首礼足，退坐一面；身诸光明遍照祇园。",
        "天子说偈问：「瞿昙大智无碍！众人多怖，道亦多门；住何法、学何法，不惧他世？」",
        "世尊说偈答：「正摄口与意，身不作诸恶；居家丰饮食，而能信、柔和、好施、知分与。"
        "住此四法，住于法者，则不惧他世。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫栴檀的天子容色绝妙，来到佛前，顶礼佛足，退坐一面；身上光明遍照祇园。",
        "天子说偈问：「瞿昙大智无碍！这里许多人害怕，道路也有许多门径；"
        "安住什么、修学什么，才不怕来世？」",
        "世尊说偈答：「口与意安放得正，身不作恶；虽在家丰足饮食，却有信、柔和、好布施、知分与人。"
        "安住这四法、安住于法的人，就不怕来世。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.75 Bhītāsutta。"
        "据 SN 四法：vācaṁ manañca paṇidhāya sammā、身不作恶、saddho mudū saṁvibhāgī vadaññū；"
        "汉「广集群宾／财法施」收束为信、柔、施、知分与。"
    ),
}

# --- SA 1316 栴檀（SN2.15 Candana）-----------------------------------------
SUTTAS["SA_1316"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，栴檀天子容色绝妙，来诣佛所，稽首礼足，退坐一面；身诸光明遍照祇园。",
        "天子说偈问：「谁度于诸流，昼夜勤不懈？无立足、无所攀，云何不没于深？」",
        "世尊说偈答：「常具戒，有慧善正受，精进心决定，能度难度流。"
        "离于欲想，超越色结，喜贪已尽，则不没于深。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫栴檀的天子容色绝妙，来到佛前，顶礼佛足，退坐一面；身上光明遍照祇园。",
        "天子说偈问：「谁能度过诸流，昼夜精勤不懈？没有立足处、也无所攀缘，怎样才不沉没在深处？」",
        "世尊说偈答：「始终持戒具足，有智慧又善入定，精进而心决定，能度过难度的流。"
        "远离欲想，超越色的结缚，喜与贪已经尽了，就不会沉没在深处。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.15 Candanasutta。"
        "据 SN：sīla／paññā／samādhi／āraddhavīriya 度流；"
        "virato kāmasaññāya、rūpasaṁyojanātigo、nandīrāgaparikkhīṇa 则不沈 gambhīre。"
    ),
}

# --- SA 1317 迦叶（SN2.1 Paṭhamakassapa）-----------------------------------
SUTTAS["SA_1317"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，迦叶天子容色绝妙，来诣佛所，稽首礼足，退坐一面；身诸光明遍照祇园。",
        "天子白佛：「世尊已说比丘相，而未说比丘之教诫。」佛言：「迦叶！汝当自说。」",
        "天子说偈：「当学善说之语，亲近沙门；独坐于静处，令心寂定。」",
        "世尊印可。天子知佛印可，欢喜礼足，右绕而没。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫迦叶的天子容色绝妙，来到佛前，顶礼佛足，退坐一面；身上光明遍照祇园。",
        "天子对佛说：「世尊已经开示了比丘的相状，却还没说对比丘的教诫。」"
        "佛说：「迦叶！那就由你来说。」",
        "天子说偈：「应当学善于言说，亲近沙门；独自坐在静处，让心寂定。」",
        "世尊表示印可。天子知道佛已印可，欢喜顶礼，右绕佛后隐没。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.1 Paṭhamakassapasutta。"
        "汉偈（正念解脱、坏有等）与巴利异；据 SN 校正为四事教诫："
        "subhāsita／samaṇūpāsana／ekāsana raho／cittavūpasama。gold_reconstructed。"
    ),
}

# --- SA 1318 迦叶（SN2.2 Dutiyakassapa）------------------------------------
SUTTAS["SA_1318"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，迦叶天子容色绝妙，来诣佛所，稽首礼足，退坐一面；身诸光明遍照祇园。",
        "天子说偈：「比丘若禅思、心解脱，欲求心愿成满——已知世间生灭，"
        "善心无依著，是则其果报。」",
        "世尊印可。天子闻已，欢喜礼足，即没不现。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫迦叶的天子容色绝妙，来到佛前，顶礼佛足，退坐一面；身上光明遍照祇园。",
        "天子说偈：「比丘若禅思、心已解脱，又想让心愿圆满——已经了知世间的生灭，"
        "内心善好、无所依著，那就是他的果报。」",
        "世尊表示印可。天子听完，欢喜顶礼，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.2 Dutiyakassapasutta。"
        "汉偈近前经扩写；据 SN 校正：jhāyī vimuttacitta、hadayassānupatti、"
        "lokassa udayabbaya、sucetaso anissito。gold_reconstructed。"
    ),
}

# --- SA 1319 崛摩（SN10.4 Maṇibhadda；汉有供宿叙事）-------------------------
SUTTAS["SA_1319"] = {
    "lit": [
        "如是我闻：一时，佛在摩竭提国人间游行，日暮与五百比丘止屈摩夜叉住处。"
        "屈摩夜叉请佛及众宿，世尊默然受请。夜叉化作五百重阁、床褥、灯明，延请入舍。",
        "夜叉说偈：「有正念者常吉祥，有正念者安乐增；正念者日日转胜，解脱于怨憎。」",
        "佛告夜叉：「有正念者常吉祥，有正念者安乐增；正念者日日转胜，然未免于怨憎。"
        "若昼夜乐于不害，慈心及一切有情，则于一切无所怨。」",
        "夜叉欢喜随喜，礼足还住。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在摩竭提国一带游行，傍晚与五百比丘住在屈摩夜叉的住处。"
        "屈摩夜叉请佛和大众过夜，世尊默然接受。夜叉化出五百座重阁、床褥和灯火，请来入舍。",
        "夜叉说偈：「有正念的人总是吉祥，有正念的人安乐增长；正念的人一天比一天更好，能解脱怨憎。」",
        "佛告诉夜叉：「有正念的人总是吉祥，有正念的人安乐增长；正念的人一天比一天更好，"
        "却还不能免于怨憎。若昼夜都乐于不伤害，对一切有情怀着慈心，那就对任何人都没有怨恨。」",
        "夜叉欢喜随喜，顶礼后回到自己的住处。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.4 Maṇibhaddasutta。"
        "汉供宿化阁为 SA 叙事，压缩保留；偈据 SN 校正：satimā 吉祥≠已免 vera；"
        "须 ahiṃsā＋metta 于一切有情，乃 veraṁ na kenaci。gold_reconstructed（偈义）。"
    ),
}

# --- SA 1320 白山（无巴利平行）---------------------------------------------
SUTTAS["SA_1320"] = {
    "lit": [
        "如是我闻：一时，佛住摩鸠罗山，尊者那伽波罗为侍者。",
        "夜暗微雨，电光闪现，世尊出房露地经行。帝释化作毗琉璃重阁，持阁随佛经行。",
        "侍者法：待师禅觉然后眠。那伽波罗嫌经行久，反被毛衣作摩鸠罗鬼形，"
        "立于经行道头呼：「摩鸠罗鬼来！」",
        "佛告：「愚痴人！欲以鬼形怖佛耶？不能动如来一毛；如来久离恐怖。」",
        "帝释问：「正法律中亦有如此人耶？」佛言：「憍尸迦！瞿昙家广大，"
        "如是等人未来亦当得清净法。」",
        "世尊说偈：「若婆罗门于自所得法已到彼岸，则毘舍遮与摩鸠罗皆悉超过；"
        "观察诸受已灭，因缘已尽，人我已尽，生老病死皆已超过。」",
        "帝释闻已欢喜，礼足即没。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在摩鸠罗山，那伽波罗尊者做侍者。",
        "夜里昏暗又下小雨，电光闪动，世尊走出房门在露天经行。"
        "帝释化作一座毗琉璃重阁，举着随佛经行。",
        "做侍者的规矩是：等师父从禅定出来再睡。那伽波罗嫌经行太久，把毛衣翻过来毛朝外，"
        "装成摩鸠罗鬼的样子，站在经行道头喊：「摩鸠罗鬼来了！」",
        "佛说：「愚痴人！想用鬼形来吓佛吗？动不了如来一根毫毛；如来早已远离恐怖。」",
        "帝释问：「正法律里也有这样的人吗？」佛说：「憍尸迦！瞿昙家很广大，"
        "这样的人将来也会得到清净之法。」",
        "世尊说偈：「若婆罗门在自己所得的法上已经到了彼岸，毘舍遮和摩鸠罗就都超过去了；"
        "观察诸受已经灭尽，因缘已尽，人我已尽，生老病死都已超过。」",
        "帝释听完欢喜，顶礼后随即隐没。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 巴利专经；依汉本雅化压缩侍者作鬼怖佛、"
        "帝释随行及「已到彼岸则超鬼怖」之偈。"
    ),
}

# --- SA 1321 宾伽罗（SN10.6 Piyaṅkara）-------------------------------------
SUTTAS["SA_1321"] = {
    "lit": [
        OPEN_BAM_LIT,
        "尊者阿那律于摩竭提人间游行，止毕陵伽鬼母住处。后夜端坐，广诵法句诸偈。",
        "毕陵伽鬼子夜啼，鬼母说偈止之：「毕陵伽！莫啼。当听比丘诵法句。"
        "若解法句，当护戒、离杀、不妄语，自修善戒，冀脱鬼神趣。」",
        "说是偈时，鬼子啼声即止。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "阿那律尊者在摩竭提一带游行，住在毕陵伽鬼母的住处。后夜端身正坐，广诵种种法句偈。",
        "毕陵伽鬼子夜里哭闹，鬼母说偈哄他：「毕陵伽！别哭。听听比丘诵的法句。"
        "若懂得法句，就应当护戒、不杀生、不妄语，好好学自己的戒行，但愿能脱出鬼神道。」",
        "说完这偈，鬼子的哭声就停了。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.6 Piyaṅkarasutta。"
        "据 SN：听法句、护生、不妄语、学善戒，冀 muccema pisācayoni；"
        "汉「忧陀那、波罗延…」等诵目压缩为「法句诸偈」。"
    ),
}

# --- SA 1322 富那婆薮（SN10.7 Punabbasu）-----------------------------------
SUTTAS["SA_1322"] = {
    "lit": [
        "如是我闻：一时，佛在摩竭提人间游行，止富那婆薮鬼母住处，为诸比丘说四圣谛。",
        "鬼子富那婆薮与女欝多罗夜啼。鬼母说偈：「富那婆薮、欝多罗莫啼！"
        "令我得闻如来法。父母不能令子脱苦，闻正法则能脱苦。"
        "世人著欲为苦所迫；我欲闻佛所说解脱老死之法，汝等当默。」",
        "二子答：「母！我等默然。但当专听；未解正法故长夜受苦。"
        "佛为天人明灯，最后身而说法。」",
        "母喜说偈：「奇哉慧子！已见圣谛；富那婆薮且安乐，欝多罗亦当听。」",
        "二子随喜默然。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在摩竭提一带游行，住在富那婆薮鬼母的住处，对比丘们讲四圣谛。",
        "鬼子富那婆薮和女儿欝多罗夜里哭闹。鬼母说偈：「富那婆薮、欝多罗，别哭！"
        "让我好听如来的法。父母不能让孩子脱离苦，听正法才能脱离苦。"
        "世人贪著爱欲被众苦逼迫；我想听佛所觉悟的解脱老死之法，你们安静。」",
        "两个孩子答：「妈妈！我们不说话了。您只管专心听；正是因为还不懂正法，才长久受苦。"
        "佛是天人的明灯，以最后之身而说法。」",
        "母亲欢喜说偈：「好聪明的孩子！我已得见圣谛；富那婆薮，愿你安乐，欝多罗也来听。」",
        "两个孩子随喜，安静下来。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.7 Punabbasusutta。"
        "据 SN：爱法胜过爱子／夫；听 saddhamma 能脱苦；子默听、母见 ariyasaccāni；"
        "汉「四圣谛」开场与巴利 nibbāna 相应法并存。"
    ),
}

# --- SA 1323 曼尼遮闻（无巴利平行）-----------------------------------------
SUTTAS["SA_1323"] = {
    "lit": [
        "如是我闻：一时，佛在摩竭提人间游行，止摩尼遮罗鬼住处。",
        "有女人持香花饮食来祠鬼，遥见世尊坐彼处，以为即摩尼遮罗，说偈求现世安乐、后世生天。",
        "佛说偈：「莫放逸、莫恃鬼；自修所作，乃得生天乐。」",
        "女人悟是沙门瞿昙，即以香花供养，礼足问：「何道现世安隐、后世生天？」",
        "佛说偈：「布施、调心、护根，正见修贤行，亲近沙门，以正命自活，他世得生天乐。"
        "何用三十三天苦网？当一其心，断除爱欲；我当说离垢甘露，汝当善听。」",
        "如常法次第说施戒生天、欲味欲患出要。女人于座上见四谛，得法眼净，尽寿归三宝。",
        "闻已欢喜，礼佛而去。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在摩竭提一带游行，住在摩尼遮罗鬼的住处。",
        "有个女人带着香花饮食来祭鬼，远远看见世尊坐在那里，以为就是摩尼遮罗，"
        "说偈祈求现世安乐、来世生天。",
        "佛说偈：「不要放逸，也不要仗着鬼神；自己修该做的事，才能得到生天的乐。」",
        "女人明白这是沙门瞿昙，便用香花供养，顶礼后问：「怎样现世安稳、来世生天？」",
        "佛说偈：「布施、调心、守护根门，持正见、修贤行，亲近沙门，以正当职业维生，"
        "来世就能生天。何必贪三十三天那张苦网？应当专心，断除爱欲；我要说离垢甘露，你好好听。」",
        "佛又按常法依次讲布施持戒生天、欲的滋味与过患、出离。女人当场见到四谛，法眼清净，"
        "尽形寿归依佛法僧。",
        "听完欢喜，礼佛离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 巴利专经；依汉本压缩：勿恃鬼神、自修；"
        "施戒护根正命生天，进而劝断欲、闻甘露，证四谛归三宝。"
    ),
}

# --- SA 1324 箭毛（SN10.3 Sūciloma）----------------------------------------
SUTTAS["SA_1324"] = {
    "lit": [
        "如是我闻：一时，佛在摩竭提人间游行，止针毛鬼住处。时针毛与粗毛夜叉路过，"
        "粗毛曰：「彼是沙门。」针毛曰：「且试之为真沙门否。」",
        "针毛以身逼佛，世尊却身。针毛问：「沙门怖耶？」佛言：「我不怖，但汝触恶。」",
        "针毛曰：「若不问答令我喜，当坏汝心、裂汝胸、掷汝恒水彼岸。」"
        "佛言：「我不见天魔梵世人能如是害如来者。汝但问。」",
        "针毛说偈问：「贪恚何所因？不乐、喜、身毛竖从何生？意中觉想从何起？"
        "如童子纵乌鸦。」",
        "佛说偈答：「贪恚从此因；不乐、喜、身毛竖从此生；觉想从此起，如童子纵乌鸦。"
        "爱润所生、自所起，如尼拘律干生根；著欲如藤遍林。若知彼因则能遣除——夜叉当听！"
        "能度难度流，未曾度者，不复受有。」",
        "针毛悔过，受三归。闻已欢喜奉行。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在摩竭提一带游行，住在针毛鬼的住处。当时针毛与粗毛夜叉路过，"
        "粗毛说：「那是沙门。」针毛说：「先试试他是不是真沙门。」",
        "针毛用身体去挤佛，世尊侧身避开。针毛问：「沙门，你怕了吗？」佛说：「我不怕，只是你的触碰很恶。」",
        "针毛说：「若回答不能让我高兴，我就搅乱你的心、裂开你的胸、把你扔到恒河对岸。」"
        "佛说：「我不见天、魔、梵、世人能这样害如来。你尽管问。」",
        "针毛说偈问：「贪和瞋从哪里来？不乐、喜乐、汗毛竖立从哪里生？心里寻思从哪里起？"
        "好像孩子放走乌鸦。」",
        "佛说偈答：「贪瞋从这里来；不乐、喜、汗毛竖从这里生；寻思从这里起，好像孩子放走乌鸦。"
        "由爱润而生、由自身而起，像尼拘律从树干生根；黏着于欲像藤蔓爬满林。知道来处就能遣除——"
        "夜叉啊，听着！能渡过这道难度的流，这是从前没渡过的，从此不再受后有。」",
        "针毛悔过，受三归。听完欢喜奉行。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.3／Snp2.5 Sūcilomasutta。"
        "据 SN：Kharo／Sūcilomo；触恶非怖；童子纵乌鸦譬；snehajā／nigrodha／māluvā；"
        "知因则 vinodeti，度 duttara ogha 至 apunabbhava。汉「炎鬼」并入粗毛试探。"
    ),
}

# --- SA 1325 受斋（SN10.5 Sānu）--------------------------------------------
SUTTAS["SA_1325"] = {
    "lit": [
        OPEN_BAM_LIT,
        "有优婆夷子名娑努，受八支斋而犯戒，为鬼神所持。母泣说偈："
        "「十四、十五及月八日，神变月分，具足八支守斋修梵行者，鬼不得戏——我从阿罗汉闻。"
        "今乃见鬼弄娑努！」",
        "鬼说偈：「汝所闻是。娑努醒时当告以鬼语：勿作恶业，公开或隐密皆勿作；"
        "若作恶业，虽逃遁亦不得脱苦。」即放其子。",
        "子醒问母何哭。母说偈：「死人乃哭，失踪乃哭；捨欲出家而还入欲者，虽生犹死，是故亦哭。"
        "已出炭火而欲复投，已出深坑而欲复堕；财宝出火又欲自焚——汝欲何为？」",
        "母如是发悟，子还空闲精勤，断结得阿罗汉。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "有优婆夷的儿子名叫娑努，受了八支斋却犯了戒，被鬼神捉住。母亲哭着说偈："
        "「十四、十五和每月八日，以及神变的那段日子，完整受持八支斋、修梵行的人，"
        "鬼不能戏弄——我是从阿罗汉那里听来的。可今天竟看见鬼在戏弄娑努！」",
        "鬼说偈：「你听的不错。娑努醒来时，把鬼的话告诉他：不要作恶业，公开或私下都不要作；"
        "若作了恶业，就算逃跑也脱不了苦。」说完就放了她的儿子。",
        "儿子醒来问母亲为什么哭。母亲说偈：「死了才哭，失踪了才哭；捨了欲出家又回到欲里的人，"
        "虽然活着却像死了，所以也要哭。已经离开炭火却想再跳进去，已经离开深坑却想再掉下去；"
        "财宝从火里抢出又想自己烧掉——你到底要怎样？」",
        "母亲这样警醒他，儿子回到空闲处精勤修行，断尽结缚，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.5 Sānusutta。"
        "据 SN 校正：鬼诫「勿作恶」为主（汉「拔菅缓急」譬为异传，今从巴利）；"
        "母哭出家还俗如复投炭火／深坑；汉结得阿罗汉为 SA 所增，存之并志。"
        "gold_reconstructed（鬼诫与母哭据巴利）。"
    ),
}

# --- SA 1326 矌野（SN10.12 Āḷavaka）----------------------------------------
SUTTAS["SA_1326"] = {
    "lit": [
        "如是我闻：一时，佛在阿臈鬼住处宿。阿臈三呼「出去／进来」，佛皆从之；"
        "第四呼「出去」，佛言：「已三见命，今不复出。汝欲何为便为之。」",
        "阿臈威胁坏心裂胸掷恒水。佛言：「不见有能如是害我者。汝但问。」",
        "问：「人何财最胜？何善行致乐？何味最甜？云何活命最胜？」"
        "答：「信为最胜财；如法而行致乐；谛为味中上；慧命为活命最胜。」",
        "问：「云何度流？云何度海？云何逾苦？云何得清净？」"
        "答：「以信度流，不放逸度海，精进逾苦，以慧清净。」",
        "问：「云何得慧、得财、得名、得友？云何从此世至他世而不忧？」"
        "答：「信诸阿罗汉及趣涅槃之法，好学、不放逸、有简择则得慧；"
        "善业精勤则得财；以谛得名；以施结友。在家有信而具谛、法、坚忍、捨，"
        "则他世不忧。汝可更问诸沙门婆罗门：有过此谛、法、施、忍否？」",
        "阿臈言：「何须更问？今日已知后世义。佛来住此，实为我利。"
        "我当村村城城礼敬正觉及正法。」",
        CLOSE_YAK_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在阿臈鬼的住处。阿臈三次喊「出去／进来」，佛都听从；"
        "第四次喊「出去」，佛说：「已经听你三次了，现在不再出去。你要怎样就怎样。」",
        "阿臈威胁要搅乱心、裂开胸、扔到恒河对岸。佛说：「我不见有谁能这样害我。你尽管问。」",
        "问：「人什么财最胜？怎样好好实行能得乐？什么味道最甜？怎样活命最好？」"
        "答：「信是最胜的财；如法实行能得乐；真实是味道中最上的；以智慧活命才是最好的活命。」",
        "问：「怎样度流？怎样度海？怎样越过苦？怎样得清净？」"
        "答：「以信度流，以不放逸度海，以精进越过苦，以智慧得清净。」",
        "问：「怎样得智慧、得财富、得好名声、交到朋友？怎样从此世到他世而不忧愁？」"
        "答：「信阿罗汉和导向涅槃的法，好学、不放逸、有简择，就得到智慧；"
        "做事得宜又勤劳就得到财富；以真实得到名声；以布施结交朋友。"
        "在家有信而又具备真实、正法、坚忍、惠施，到他世就不会忧愁。"
        "你也可以再去问别的沙门婆罗门：还有比真实、正法、布施、安忍更好的吗？」",
        "阿臈说：「何必再问？今天我已明白对来世有益的事。佛来住在这里，实在是为我好。"
        "我要一村一村、一城一城地礼敬正觉和正法。」",
        CLOSE_YAK_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.12／Snp1.10 Āḷavakasutta。"
        "据 SN 收束问答：信财／法行／谛味／慧命；信度流四句；得慧财名友与四法"
        "（sacca dhamma dhiti cāga）；汉「几法起世间」等为 Hemavata 串入，今据 Āḷavaka 删并。"
        "gold_reconstructed（问答序据巴利）。"
    ),
}

# --- SA 1327 净（SN10.9–10 Sukkā；汉叔迦罗）--------------------------------
SUTTAS["SA_1327"] = {
    "lit": [
        OPEN_BAM_LIT,
        "叔迦罗比丘尼住王园比丘尼众中，王舍城人素恭敬如阿罗汉。"
        "一日城中吉星大会，阙其供养。有夜叉敬重彼尼，街巷说偈催请："
        "「王舍人醉眠，不供叔迦罗；善修诸根、善说离垢涅槃法，听者终日无厌，"
        "乘法慧度生死流。」",
        "有优婆塞施衣、有优婆塞施食。夜叉复说偈：「智慧优婆塞获大福：施食／衣与叔迦罗——"
        "彼已解脱一切结缚。」说已即没。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "叔迦罗比丘尼住在王园比丘尼众中，王舍城人一向恭敬她如同阿罗汉。"
        "有一天城里过吉星节集会，没有人供养她。有夜叉敬重这位比丘尼，在街巷里说偈催请："
        "「王舍城人醉酒睡着，不供养叔迦罗；她善修诸根，善说离垢的涅槃法，听的人整天不厌，"
        "靠听法的智慧度过生死流。」",
        "有优婆塞布施衣服，又有优婆塞布施饮食。夜叉又说偈：「有智慧的优婆塞得大福：把食／衣施给叔迦罗——"
        "她已经解脱一切结缚。」说完就隐没了。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.9–10 Sukkāsutta。"
        "据 SN：夜叉赞优婆塞施食与已解脱一切 gantha 之 Sukkā；"
        "汉「叔迦罗」＝Sukkā；催供叙事压缩保留。"
    ),
}

# --- SA 1328 雄（SN10.11 Cīrā；汉毘罗）------------------------------------
SUTTAS["SA_1328"] = {
    "lit": [
        OPEN_BAM_LIT,
        "毘罗比丘尼住王园比丘尼众中。吉星大会日，无人供养。"
        "有夜叉敬重彼尼，里巷衢头说偈：「王舍人醉眠，毘罗无人供；勇猛修根，善说离垢涅槃法，"
        "听者终日无厌，乘法慧度生死流。」",
        "有优婆塞施衣、有优婆塞施食。夜叉说偈：「智慧优婆塞获大福：以衣／食施毘罗——"
        "彼已解脱一切轭。」说已即没。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "毘罗比丘尼住在王园比丘尼众中。吉星节集会那天，没有人供养她。"
        "有夜叉敬重这位比丘尼，在里巷路口说偈：「王舍城人醉酒昏睡，毘罗无人供养；"
        "她勇猛修根，善说离垢的涅槃法，听的人整天不厌，靠听法的智慧度过生死流。」",
        "有优婆塞布施衣服，又有优婆塞布施饮食。夜叉说偈：「有智慧的优婆塞得大福：把衣／食施给毘罗——"
        "她已经解脱一切轭。」说完就隐没了。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.11 Cīrāsutta。"
        "据 SN：施 cīvara 与已解脱一切 yoga 之 Cīrā；汉「毘罗」对 Cīrā；"
        "结缚／轭分属 Sukkā／Cīrā 二经用语。"
    ),
}

# --- SA 1329 七岳雪山（Snp1.9 Hemavata）------------------------------------
SUTTAS["SA_1329"] = {
    "lit": [
        OPEN_BAM_LIT,
        "娑多耆利与醯魔波低夜叉共誓：宫中出宝必相告。醯魔宫生千葉金色波昙摩，大如车轮，遣使来报。"
        "娑多耆利答：「何用百千莲华！我宫有大宝——如来、应、等正觉、明行足、善逝、世间解、"
        "无上士、调御丈夫、天人师、佛世尊，可来奉事。」",
        "醯魔率五百眷属至，说偈次第问：彼愿乐慈济众生不？于受不受心想平等不？"
        "明达行成、诸漏永尽、不受后有不？牟尼意与身口业满、明行具足不？"
        "不害生、不与不取、远离放荡、日夜乐禅不？不乐五欲、心不浊、法眼净、愚痴尽不？"
        "不妄语、无粗恶、不离间、说如法不？净戒、正念寂、等解脱、如来大智具足不？"
        "娑多耆利一一答：「如是，彼牟尼悉已具足。」",
        "二夜叉曰：「伊泥延鹿蹲相，少食离贪，牟尼乐林禅——当共往礼瞿昙。」"
        "遂与百千鬼神诣竹园，礼足问：「云何出苦？云何苦解脱？苦于何灭尽？」",
        "佛说偈：「世五欲功德，及说第六意；于彼欲无贪，解脱一切苦。如是出苦、解脱苦，苦从此灭。」",
        "复问：「泉从何转还？恶道何不转？世间苦乐于何灭尽？」"
        "佛言：「眼耳鼻舌身意——于彼名色永灭无余，则泉转还、道不转、苦乐尽。」",
        "问：「几法起世间？几法和合？几法取？几法灭？」答：「六法起、六法和合、六法取、六法灭。」",
        "问谁度流。答：「一切戒具足，智慧善正受，精进内正念，能度难度流；"
        "不乐欲想，超越色结，无攀无住，不溺深渊。以信度流，不放逸度海，精进除苦，慧得清净。」",
        "二夜叉及五百眷属归依礼敬，欢喜随喜而去。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "娑多耆利与醯魔波低两位夜叉互相约定：宫里出现宝物一定告诉对方。"
        "醯魔宫里长出千葉金色莲花，大如车轮，派人来报。"
        "娑多耆利答：「要百千朵莲花做什么！我宫里有大宝——如来、应、等正觉、明行足、善逝、"
        "世间解、无上士、调御丈夫、天人师、佛世尊，你们该来奉事。」",
        "醯魔带着五百眷属前来，用偈依次问：那位愿意慈济众生吗？对受与不受心是否平等？"
        "明达与修行是否成就、诸漏是否永尽、不再受后有？"
        "牟尼的意与身口业是否圆满、明行是否具足？"
        "是否不杀害、不偷取、远离放荡、日夜乐于禅修？"
        "是否不乐五欲、心不浑浊、法眼清净、愚痴尽除？"
        "是否不妄语、无粗恶语、不离间、说如法的话？"
        "净戒、正念寂静、等解脱、如来大智是否都具足？"
        "娑多耆利一一回答：「是的，那位牟尼都已经具足。」",
        "两位夜叉说：「有伊泥延鹿蹲的瑞相，少食离贪，牟尼乐于林中禅——我们该一起去礼敬瞿昙。」"
        "于是与百千鬼神来到竹园，顶礼后问：「怎样出离苦？怎样解脱苦？苦在哪里灭尽？」",
        "佛说偈：「世间五种欲的功德，再加上第六意；若对这些欲没有贪，就解脱一切苦。"
        "这样出苦、这样解脱苦，苦从这里灭。」",
        "又问：「水流从哪里折回？恶道为什么不转？世间苦乐在哪里灭尽？」"
        "佛说：「眼耳鼻舌身意——在那里名色灭尽无余，水流就折回，道不再转，苦乐就尽了。」",
        "问：「几法生起世间？几法和合？几法执取？几法灭尽？」"
        "答：「六法生起、六法和合、六法执取、六法灭尽。」",
        "问谁能度流。答：「持戒具足，智慧善入定，精进而内怀正念，能度过难度的流；"
        "不乐欲想，超越色结，无所攀缘、无所住立，就不沉没在深渊。"
        "以信度流，以不放逸度海，以精进除苦，以智慧得清净。」",
        "两位夜叉和五百眷属归依礼敬，欢喜随喜离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary Snp1.9 Hemavatasutta（Sātāgira／Hemavata）。"
        "汉问答极繁，据 Snp 义压缩重复印可句，保留：互报宝物→问德印可→鹿蹲相共诣→"
        "苦灭／六处名色／六法／度流；厌贪义见于「于欲无贪则解脱一切苦」。"
        "aligned 缺巴利全文，据 SC 平行及汉本对读。"
    ),
}

# --- SA 1330 害及无害（Ud4.4 Yakkhapahāra）---------------------------------
SUTTAS["SA_1330"] = {
    "lit": [
        OPEN_BAM_LIT,
        "尊者舍利弗、大目揵连住耆闍崛山。舍利弗新剃发，露地入定。"
        "优波伽吒鬼欲击其头，伽吒鬼再三谏：「莫击！此沙门大德大力，长夜当得大苦。」不听。",
        "优波伽吒以手击舍利弗头，力可摧七寻象或裂山峰；击已自呼「烧我、煮我」，陷入地，堕无间狱。",
        "目连以天眼见，往问：「苦痛可忍不？」舍利弗言：「可忍，头稍有苦。」"
        "目连叹其大德大力。二人共相慰劳。",
        "世尊以天耳闻，说偈：「心如刚石，安住不倾；染著已离，瞋不返报；"
        "若如是修心，何有苦痛忧？」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "舍利弗尊者和大目揵连尊者住在耆闍崛山。舍利弗刚剃过头发，在露天入定。"
        "优波伽吒鬼想打他的头，伽吒鬼再三劝：「别打！这位沙门德大、力大，你会长时间受大苦。」他不听。",
        "优波伽吒用手打舍利弗的头，那一击的力量能打倒七寻高的象，或劈开山峰；"
        "打完自己喊「烧我、煮我」，坠入地中，堕入无间地狱。",
        "目连用天眼看见，前来问：「苦痛还能忍受吗？」舍利弗说：「能忍受，头稍微有点苦。」"
        "目连赞叹他德大、力大。两人互相安慰。",
        "世尊用天耳听见，说偈：「心像坚石，安住不动摇；已经离开染著，对瞋怒也不反击；"
        "若这样修心，哪里还有苦痛忧愁？」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：parallel Ud4.4 Yakkhapahārasutta。"
        "据 Ud：月光夜新剃发露地入定；一击可倒大象／裂山峰；舍利弗唯「头稍苦」；"
        "优陀那偈＝心坚如石、离染、不报瞋。汉鬼名伽吒／优波伽吒从汉。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {
    "SA_1311": "high",
    "SA_1312": "high",
    "SA_1313": "high",
    "SA_1314": "high",
    "SA_1315": "high",
    "SA_1316": "high",
    "SA_1317": "high",
    "SA_1318": "high",
    "SA_1319": "high",
    "SA_1320": "medium",
    "SA_1321": "high",
    "SA_1322": "high",
    "SA_1323": "medium",
    "SA_1324": "high",
    "SA_1325": "high",
    "SA_1326": "high",
    "SA_1327": "high",
    "SA_1328": "high",
    "SA_1329": "high",
    "SA_1330": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1317": "汉偈与 SN2.1 异，据巴利四事教诫（善说／亲近沙门／独坐静处／心寂）改写。",
    "SA_1318": "汉偈扩写与 SN2.2 异，据巴利禅思心解脱／知世间生灭／善心无依改写。",
    "SA_1319": "汉正念安眠偈缺「未免怨憎」之驳，据 SN10.4 补正念≠免怨、须不害＋慈。",
    "SA_1325": "鬼诫与母哭据 SN10.5（勿作恶；出家还俗如复投炭火），替换汉菅草异传。",
    "SA_1326": "问答序据 SN10.12 收束；删 Hemavata 串入之「几法起世间」等。",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

BATCH_IDS = [f"SA_{i}" for i in range(1311, 1331)]
PARALLEL_BATCH_IDS = {f"SA_{i}" for i in range(1291, 1311)} | {
    f"SA_{i}" for i in range(1331, 1351)
}

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
assert PARALLEL_BATCH_IDS.isdisjoint(GOLD), "must not merge neighbor batches"


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

    parallel_before = {
        rec["id"]: _snap(rec) for rec in records if rec["id"] in PARALLEL_BATCH_IDS
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

    for rid, before in parallel_before.items():
        for rec in merged:
            if rec["id"] == rid:
                assert before == _snap(rec), f"{rid} (neighbor) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1311-1330.json").write_text(
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1311, 1331)
    )
    untouched_neighbors = all(
        f"SA_{i}" not in GOLD for i in list(range(1291, 1311)) + list(range(1331, 1351))
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1311–SA_1330 only)")
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
    print(f"continuous_1311_1330_goldish={continuous}")
    print(f"neighbors_1291-1310_and_1331-1350_untouched={untouched_neighbors}")
    if needs_restyle:
        print("needs_restyle_detail:")
        for r in needs_restyle:
            print(f"  {r['id']} sim={r['sim']} reasons={r.get('gate_reasons')}")
    if fails:
        print("fail_detail:")
        for r in fails:
            print(f"  {r['id']} issues={r.get('issues')}")
    for r in sorted(report, key=lambda x: int(x["id"].split("_")[1])):
        print(
            f"  {r['id']}: status={r['review_status']} conf={r['confidence']} "
            f"val={r['status']} sim={r['sim']} paras={r['paragraphs']}"
        )


if __name__ == "__main__":
    main()
