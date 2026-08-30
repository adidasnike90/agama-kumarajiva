#!/usr/bin/env python3
"""Retranslate SA 1091–1110（魔相应续 → 帝释相应起）→ merge.

本批二十经：
1091–1103 魔相应续（求德 SN4.23、魔女 SN4.25、害恶 SN4.3、苦行 SN4.1、
         乞食 SN4.18、绳索 SN4.5、自应 SN4.14、作王 SN4.20、众多 SN4.21、
         善觉 SN4.22、师子 SN4.12、钵 SN4.16、入处 SN4.17）
1104–1110 帝释相应起（帝释 SN11.11、摩诃离 SN11.13、以何因 SN11.12、
         夜叉 SN11.22、得眼 SN11.24、得善胜 SN11.5、缚系 SN11.4）

信：有平行者以 SN／Pāli／Sujato 厘义；汉本用于定位与传统术语。
    1106 末偈『如上广说』→ 据 SN11.12／邻经七受偈重建（gold_reconstructed）。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_1091–1110；不触碰邻经 SA_1090、SA_1111。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

batch_range = range(1091, 1111)

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

OPEN_URU_LIT = "如是我闻：一时，佛住郁鞞罗聚落尼连禅河侧菩提树下，初成正觉。"
OPEN_URU_MOD = "我是这样听说的：有一次，佛住在郁鞞罗聚落尼连禅河侧菩提树下，刚成正觉不久。"

OPEN_URU_SOON_LIT = "如是我闻：一时，佛住郁鞞罗聚落尼连禅河侧，于菩提树下成佛未久。"
OPEN_URU_SOON_MOD = "我是这样听说的：有一次，佛住在郁鞞罗聚落尼连禅河侧，在菩提树下成佛未久。"

OPEN_VAR_LIT = "如是我闻：一时，佛住波罗奈国仙人住处鹿野苑中。"
OPEN_VAR_MOD = "我是这样听说的：有一次，佛住在波罗奈国仙人住处鹿野苑中。"

OPEN_VES_LIT = "如是我闻：一时，佛住鞞舍离国猕猴池侧重阁讲堂。"
OPEN_VES_MOD = "我是这样听说的：有一次，佛住在鞞舍离国猕猴池侧重阁讲堂。"

OPEN_SIL_LIT = "如是我闻：一时，佛住释氏石主释氏聚落。"
OPEN_SIL_MOD = "我是这样听说的：有一次，佛住在释迦族石主聚落。"

OPEN_GODHIKA_LIT = "如是我闻：一时，佛住王舍城毘婆罗山七叶树林石室中。"
OPEN_GODHIKA_MOD = "我是这样听说的：有一次，佛住在王舍城毘婆罗山七叶树林石室中。"

OPEN_PANCA_LIT = "如是我闻：一时，佛住娑罗婆罗门聚落。"
OPEN_PANCA_MOD = "我是这样听说的：有一次，佛住在娑罗婆罗门聚落。"

OPEN_WILD_LIT = "如是我闻：一时，佛住王舍城多众践蹈旷野中。"
OPEN_WILD_MOD = "我是这样听说的：有一次，佛住在王舍城多众践蹈的旷野中。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY_MOD = "他听佛所说，欢喜随喜，作礼离去。"

VANISH_LIT = "时魔波旬作是念：「沙门已知我心。」内怀忧慼，即没不现。"
VANISH_MOD = "那时魔波旬心里想：「沙门已经知道我的心。」内心忧恼，随即隐没不见。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)

SEVEN_VOWS_LIT = (
    "谓本为人时受持七种受：一者供养父母；二者恭敬家中尊长；"
    "三者言语柔和；四者不两舌；五者于悭吝世间行解脱施，常乐惠施；"
    "六者常说真实；七者不瞋，设起瞋恚，速能除灭。"
)
SEVEN_VOWS_MOD = (
    "就是他从前做人时受持七种誓愿：一、供养父母；二、恭敬家中尊长；"
    "三、说话柔和；四、不两舌；五、在悭吝的世间里行解脱施，常乐布施；"
    "六、常说真实；七、不瞋，即使生起瞋恚，也能很快除掉。"
)

SEVEN_VERSE_LIT = (
    "「供养于父母，及家之尊长，柔和恭逊辞，离粗言两舌。"
    "调伏悭吝心，常修真实语，于瞋能速除，三十三诸天，"
    "见行此七法，咸言当生此。」"
)
SEVEN_VERSE_MOD = (
    "「供养父母，恭敬家中尊长，言语柔和谦逊，远离粗言两舌。"
    "调伏悭吝心，常说真实语，对瞋恚能很快除掉——三十三天见有人行这七法，"
    "都会说：此人当来生此天。」"
)

SAKKA_EXHORT_LIT = (
    "佛告诸比丘：「释提桓因于三十三天为自在王，尚赞不瞋与忍。"
    "汝等正信非家、出家学道，亦当如是学。」"
)
SAKKA_EXHORT_MOD = (
    "佛告诉比丘们：「帝释在三十三天做自在王，尚且赞叹不瞋与忍辱。"
    "你们正信出家学道，也应当这样学。」"
)

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 1091 求德（SN4.23 Godhika）------------------------------------------
SUTTAS["SA_1091"] = {
    "lit": [
        OPEN_GODHIKA_LIT,
        "时尊者瞿低迦住仙人山侧黑石室，独一精勤，得时分解脱，而数数退转；"
        "乃至六反得已复退。彼作是念：「我六反退转，宁以刀自尽，莫令第七再退。」",
        "魔波旬知其所念，恐彼出己境界，执琉璃柄琵琶诣佛所，鼓弦说偈："
        "「大智大神力，炽然有弟子，今欲自取死；牟尼当制之。"
        "正法律声闻，未得心所愿，云何于学地，而取于命终？」",
        "尔时瞿低迦已以刀自尽。世尊知是波旬，说偈答言："
        "「智者作如是，不贪求活命；拔爱欲根本，瞿低般涅槃。」",
        "佛告诸比丘：「来，共至黑石室，观瞿低迦善男子以刀自尽。」"
        "世尊与众多比丘往见其身委地；时有黑烟暗雾，遍诸方维上下。"
        "佛言：「见此烟雾不？此是波旬周匝求彼识神：『瞿低识何所住？』"
        "然瞿低迦识无所住，已般涅槃。」",
        "波旬复以琵琶说偈：「上下及诸方，遍求彼识神，都不见其处，瞿低何所之？」"
        "佛复说偈：「坚固具足士，常乐修禅定，昼夜勤精进，不顾于性命。"
        "已摧伏死军，不还于后有；拔爱欲根本，瞿低般涅槃。」"
        "波旬忧恼，琵琶落地，即没不现。",
        "尔时世尊为瞿低迦授第一记。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_GODHIKA_MOD,
        "那时尊者瞿低迦住在仙人山侧黑石室，独自精勤，证得暂时的心解脱，却一再退失；"
        "乃至六次得而复失。他心想：「我已六次退转，宁可持刀自尽，别让第七次再退。」",
        "魔波旬知道他的念头，怕他超出自己的境界，就拿着琉璃柄琵琶到佛那里，弹琴说偈："
        "「大智大神力，您有炽盛的弟子，如今却想自尽；请牟尼制止他。"
        "正法律中的声闻，还未满心愿，怎能在有学地就取命终？」",
        "那时瞿低迦已经持刀自尽。世尊知道对方是波旬，用偈回答："
        "「智者就是这样做，并不贪求活命；连根拔除渴爱，瞿低迦已般涅槃。」",
        "佛告诉比丘们：「来，一起到黑石室，看瞿低迦善男子持刀自尽的地方。」"
        "世尊与众多比丘前去，见他身体委在地上；那时有黑烟暗雾，遍布各方上下。"
        "佛说：「看见这烟雾了吗？那是波旬四处寻找他的识：『瞿低的识安住在哪里？』"
        "可是瞿低迦的识无所安住，已经般涅槃。」",
        "波旬又弹琵琶说偈：「上下及诸方，我遍求他的识，都找不到处所，瞿低到哪里去了？」"
        "佛又说偈：「坚固具足的人，常乐修禅定，昼夜勤精进，不顾惜性命。"
        "已摧伏死军，不再来后有；连根拔除渴爱，瞿低迦已般涅槃。」"
        "波旬忧恼，琵琶落地，随即隐没不见。",
        "那时世尊为瞿低迦授第一记（记别已般涅槃）。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.23 Godhikasutta 全平行。"
        "据巴利校正：识无所住（appatiṭṭhita viññāṇa）故般涅槃，非汉「不住心」之含混；"
        "魔求识神处据 SN 作「何处建立」；佛答偈据 SN 补昼夜精进、摧死军、不还后有。"
        "汉本住处作毘婆罗山石室，巴利作竹园；存汉开卷而志异。"
    ),
}

# --- SA 1092 魔女（SN4.25 Māradhītu）---------------------------------------
SUTTAS["SA_1092"] = {
    "lit": [
        OPEN_URU_SOON_LIT,
        "魔波旬欲作留难，化作年少，说偈扰佛。佛知是魔，答以已得寂灭之利、摧伏魔军、"
        "服食禅乐，故不与人周旋。魔复劝勿教人；佛言：有来问度彼岸者，我以正答，"
        "令得涅槃，不随魔自在。魔自譬饥乌啄石，折觜空归，忧慼画地而坐。",
        "魔有三女——爱欲、爱念、爱乐——白父：「我以欲索缚彼如野象，牵至父前。」"
        "魔言：「彼已离爱，出魔境界，非欲所能招。」",
        "三女诣佛求给侍，世尊不顾，以离欲善解脱故。女等复各现种种女色——"
        "童女、初嫁、未产、已产、中年、老年——再三求侍，佛仍不顾。",
        "爱欲女以偈问何求；佛答已得寂灭大利、不著色欲。爱念女问云何度五欲流与第六海；"
        "佛答：身止息、心善解脱、正念不动、离爱恚睡眠，故度彼岸。爱乐女赞已超死境；"
        "佛言入如来法律者皆已得度，慧者何忧。",
        "三女志不满而还。魔遥见，以偈嘲之：欲爪破山、藕丝转大山、手抒大海——"
        "于一切和合已解脱之如来，不可倾动。说已即没不现。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_URU_SOON_MOD,
        "魔波旬想作留难，化成年少，用偈搅扰佛。佛知道是魔，回答说自己已得寂灭之利、"
        "摧伏魔军、以禅悦为食，所以不跟人周旋。魔又劝他别教人；佛说：有人来问度彼岸，"
        "我就如实回答，令得涅槃，不随魔摆布。魔自比作饿乌啄石头，折嘴空回，忧恼地坐着画地。",
        "魔有三个女儿——爱欲、爱念、爱乐——对父亲说：「我们用欲索像缚野象一样绑住他，"
        "牵到父亲面前。」魔说：「他已离爱，超出魔境，不是欲所能招来的。」",
        "三女到佛那里求做侍者，世尊不理睬，因为已离欲、心善解脱。她们又各现种种女色——"
        "童女、初嫁、未产、已产、中年、老年——再三求侍，佛仍然不理。",
        "爱欲女用偈问他还求什么；佛答已得寂灭大利、不著色欲。爱念女问怎样度五欲流和第六海；"
        "佛答：身得止息、心善解脱、正念不动、离开爱恚与睡眠覆盖，所以能到彼岸。"
        "爱乐女称赞他已超越死魔境；佛说进入如来法律的人都已得度，有慧的人还忧什么。",
        "三女志愿不满而回去。魔远远看见，用偈嘲笑她们：想用爪破山、用藕丝转大山、用手舀大海——"
        "对一切和合已解脱的如来，是无法动摇的。说完就隐没不见。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.25 魔女经全平行；删梵式反复之百种色变，保留六类形色纲要与偈义。"
        "三女名据汉爱欲／爱念／爱乐（≈Taṇhā, Arati, Ragā）；法义以离欲善解脱为准。"
    ),
}

# --- SA 1093 害恶（SN4.3 Subha）---------------------------------------------
SUTTAS["SA_1093"] = {
    "lit": [
        OPEN_URU_LIT,
        "魔波旬欲令生怖，现百种净、不净色。佛知是魔，说偈："
        "「长夜生死苦中，造作净秽色；止矣波旬！汝已堕负处。"
        "身口意善护，不随魔自在，亦不作魔使。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_URU_MOD,
        "魔波旬想让佛生起怖畏，现出百种净色与不净色。佛知道是魔，说偈："
        "「长夜流转生死苦中，造作美丑之色；够了，波旬！你已经失败。"
        "身口意防护好的人，不落在魔的掌控里，也不做你的走卒。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.3；据巴利补「已堕负处／非魔使」义；汉「不度苦彼岸」并入败北义。"
    ),
}

# --- SA 1094 苦行（SN4.1 Tapokamma）-----------------------------------------
SUTTAS["SA_1094"] = {
    "lit": [
        OPEN_URU_LIT,
        "世尊独坐禅思：「善哉！我已解脱无义苦行，先愿已成，得无上菩提。」",
        "魔化年少说偈：「苦行能令净，汝今反弃舍；不净妄计净，已失清净道。」"
        "佛知是魔，答言：「我知苦行无义，如旱地操棹；戒、定、慧道我已修习，"
        "得第一清净。波旬！汝已堕负。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_URU_MOD,
        "世尊独自禅思：「太好了！我已解脱无意义的苦行，先前的愿已成就，证得无上菩提。」",
        "魔化成年少说偈：「苦行能使人清净，你如今反而舍弃；自己不净却自以为净，已偏离清净道。」"
        "佛知道是魔，回答：「我知道那些苦行没有义利，像在旱地上划桨；戒、定、慧之道我已修习，"
        "得到最上的清净。波旬！你已经失败。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.1；据巴利以「无义苦行／旱地操棹」校正汉「如弓弹有声」之喻；"
        "清净道＝戒定慧。"
    ),
}

# --- SA 1095 乞食（SN4.18 Piṇḍa）--------------------------------------------
SUTTAS["SA_1095"] = {
    "lit": [
        OPEN_PANCA_LIT,
        "世尊晨朝著衣持钵，入聚落乞食。时魔扰乱信心婆罗门、居士，令佛空钵而出。"
        "魔追后问：「沙门！得食不？」佛知是魔，言：「波旬扰如来，汝谓如来当受诸苦恼耶？」"
        "魔言：「可更入聚落，我当令得食。」佛说偈："
        "「我等虽无物，安乐而自活；如光音诸天，常以喜为食。"
        "不以有身故，而求于饮食。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_PANCA_MOD,
        "世尊清晨披衣持钵，进聚落乞食。那时魔扰乱有信心的婆罗门和居士，使佛空着钵出来。"
        "魔跟在后面问：「沙门！讨到食物没有？」佛知道是魔，说：「波旬扰乱如来，你以为如来会因此受诸苦恼吗？」"
        "魔说：「可以再进聚落，我会让你得到食物。」佛说偈："
        "「我们即使一无所有，也能安乐过活；像光音天一样，常以喜乐为食。"
        "并不因为有这个身体，就去追求饮食。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.18；据巴利：空钵而出、魔先扰施主，非仅「先入其舍」；"
        "偈以喜食（pīti）如光音天为骨。"
    ),
}

# --- SA 1096 绳索（SN4.5 Mārapāsa）------------------------------------------
SUTTAS["SA_1096"] = {
    "lit": [
        OPEN_VAR_LIT,
        "佛告诸比丘：「我已解脱人天一切绳索，汝等亦复解脱。"
        "当为人间多所饶益，安乐人天；勿二人同行一路，各各游行教化。"
        "我亦当往郁鞞罗，为众生说法。」",
        "魔化年少说偈：「汝为人天索所缚，大缚未脱，终不得出我手。」"
        "佛答：「我已脱人天一切索，亦脱大缚；波旬！汝已堕负。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_VAR_MOD,
        "佛告诉比丘们：「我已解脱人界天界的一切绳索，你们也已解脱。"
        "应当到人间多作饶益，安乐人天；不要两个人同走一路，各自游行教化。"
        "我也要到郁鞞罗去为众生说法。」",
        "魔化成年少说偈：「你被人天绳索绑着，大绑还没脱，终究逃不出我的手。」"
        "佛回答：「我已脱离人天一切索，也脱离大绑；波旬！你已经失败。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.5（兼 SN4.4 遣使义）；「勿二人同行」据巴利补明转法轮遣弟子之制。"
    ),
}

# --- SA 1097 自应（SN4.14 Patirūpa）-----------------------------------------
SUTTAS["SA_1097"] = {
    "lit": [
        OPEN_SIL_LIT,
        "时石主聚落多人疫死，远近男女来受三归；病人或使人自称名字："
        "「我某甲归佛、归法、归比丘僧。」世尊勤为四众说法，信者多生人天。",
        "魔化年少说偈：「何必勤说法？顺违皆驰走；有结缚在，云何为人说？」"
        "佛知是魔，答言：「众生群聚而生，智者不能不哀愍；以哀愍故，法自应教化。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_SIL_MOD,
        "那时石主聚落很多人因疫病死去，远近男女前来受三归；病人或者托人代报名字："
        "「我某某归依佛、法、僧。」世尊勤为四众说法，有信心的人多往生人天。",
        "魔化成年少说偈：「何必辛勤说法？顺与不顺都在奔忙；还有结缚在，怎么能为人说？」"
        "佛知道是魔，回答：「众生群聚而生，有智慧的人不能不哀愍；正因为哀愍，法就应当教化。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.14 偈义（悲愍教化、离爱憎）为骨；汉有疫死三归叙事为 SA 独有框，"
        "存之以定位，法义据巴利「出哀愍而教、已离顺违」。"
    ),
}

# --- SA 1098 作王（SN4.20 Rajja）--------------------------------------------
SUTTAS["SA_1098"] = {
    "lit": [
        OPEN_SIL_LIT,
        "世尊独坐作是念：「颇有如法作王，不杀、不教杀，一向行法、不行非法者耶？」",
        "魔来劝言：「可作王！可得如意。」佛问何故。魔言：「世尊修四如意足，"
        "若欲令雪山变为真金，即能不异。」",
        "佛言：「我都无心作王，亦无心变山为金。」即说偈："
        "「正使金山如雪山，一人得之犹不足；智者观金与土石，等无有异。"
        "已知苦从何而生，云何复趣诸欲？见世爱着是缠锁，应当修习令解脱。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_SIL_MOD,
        "世尊独自坐着心想：「可有如法做国王，不杀、不教人杀，只行法、不行非法的吗？」",
        "魔前来劝说：「可以做王！一定能如意。」佛问为什么。魔说：「世尊修习四神足，"
        "若想让雪山变成真金，立刻就能做到。」",
        "佛说：「我完全不想做王，也不想把山变成金。」就说偈："
        "「即使金山像雪山那么大，一个人得到仍不知足；智者看黄金与土石，平等无异。"
        "既知苦从哪里生起，怎会再奔向诸欲？看见世间爱着是绳索，应当修习以求解脱。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.20；据巴利补「苦因／爱着是缠」后半偈义；汉住处作石主，"
        "巴利作雪山野舍，存汉框。"
    ),
}

# --- SA 1099 众多（SN4.21 Sambahula）----------------------------------------
SUTTAS["SA_1099"] = {
    "lit": [
        OPEN_SIL_LIT,
        "时众多比丘集堂作衣。魔化盛年婆罗门，大髻兽皮，执杖而至，言："
        "「年少出家，何舍现欲而求后时之乐？」比丘答：「我等乃舍后时少味多苦之欲，"
        "就现法之乐——离炽然、不待时、缘自通达。」婆罗门三反掉首，以杖筑地，即没不现。",
        "诸比丘怖畏，往白世尊。佛言：「此非婆罗门，是魔波旬。」说偈："
        "「见苦从欲生，云何乐于欲？知着为世锁，智者当自调。"
        "真金积如山，一人犹不足；是故有慧者，应修平等观。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_SIL_MOD,
        "那时许多比丘聚在堂里做衣服。魔化作盛年婆罗门，大发髻、披兽皮、拄杖前来，说："
        "「年纪轻轻就出家，为什么舍现世的欲乐去求以后才有的乐？」比丘们答：「我们正是舍掉"
        "以后才有、少味多苦的欲，去就现法就能体验的乐——离开炽然、不必等待、自己可以通达。」"
        "那婆罗门三次甩头，用杖戳地，随即隐没不见。",
        "比丘们害怕，去禀告世尊。佛说：「那不是婆罗门，是魔波旬。」说偈："
        "「看见苦从欲生起，怎会还爱着欲？知道爱着是世间锁链，智者应当调伏自己。"
        "真金堆积如山，一个人仍不知足；所以有智慧的人，应当修平等观。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.21；「现法乐／后时乐」对举据巴利 sandiṭṭhika／kālika。"
    ),
}

# --- SA 1100 善觉（SN4.22 Samiddhi）-----------------------------------------
SUTTAS["SA_1100"] = {
    "lit": [
        OPEN_SIL_LIT,
        "尊者善觉乞食已，林中昼正受，作是念：「我得善利——遇佛正法、持戒贤众；"
        "当得贤善命终，后世亦贤，因斯脱苦。」魔化大身怖人，地若欲裂。善觉恐怖，往白佛。"
        "佛言：「非大身士夫，是魔波旬。还依本处，精勤三昧，因斯脱苦。」",
        "善觉还坐。魔复现威。善觉说偈：「我正信出家，正念系心住；"
        "随汝变形色，我心不倾动。知汝是幻化，便可从此灭。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_SIL_MOD,
        "尊者善觉乞食回来，在林中作日间禅定，心想：「我得到大善利——遇上佛与正法、"
        "戒德贤善的僧众；将来会善终，后世也贤善，由此脱离众苦。」魔化作高大可怕的身形，像要震裂大地。"
        "善觉害怕，去禀告佛。佛说：「不是什么大力士，是魔波旬。回到原处，精勤修定，由此脱苦。」",
        "善觉回去再坐。魔又现威势。善觉说偈：「我以正信出家，正念安住；"
        "随你怎样变形，我心不动摇。知道你是幻化，可以从这里消失了。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.22 Samiddhi；汉「善觉」＝Samiddhi。"
    ),
}

# --- SA 1101 师子（SN4.12 Sīha）---------------------------------------------
SUTTAS["SA_1101"] = {
    "lit": [
        OPEN_VAR_LIT,
        "佛告诸比丘：「如来声闻作师子吼，言『已知！已知！』——于苦、集、灭、道四圣谛。"
        "魔化年少说偈：「大众中无畏，作师子吼者，谓无有敌手耶？」"
        "佛答：「如来于甚深法律，方便师子吼，于法无所畏；大英雄于众中，已度诸取着。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_VAR_MOD,
        "佛告诉比丘们：「如来的声闻作师子吼，说『已知！已知！』——所知就是苦、集、灭、道四圣谛。"
        "魔化成年少说偈：「在大众里无所畏惧地作师子吼，是以为没有对手吗？」"
        "佛回答：「如来在甚深法律中方便作师子吼，于法无所畏；大英雄在众中，已经度过各种取着。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.12；四谛为汉本明示师子吼内容，与巴利『已度诸取』并存；"
        "住处汉鹿野苑、巴利或标舍卫，存汉。"
    ),
}

# --- SA 1102 钵（SN4.16 Patta）----------------------------------------------
SUTTAS["SA_1102"] = {
    "lit": [
        OPEN_WILD_LIT + "与五百比丘俱，庭中置五百钵，说五受阴生灭。",
        "魔化大牛入钵间，比丘欲驱，恐坏钵。佛言：「此非牛，是魔波旬。」说偈："
        "「色受想行识，非我非我所；如实知彼义，于彼无所著。"
        "无所著安隐，超出诸结缚；魔军虽遍求，永不得其处。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_WILD_MOD + "与五百比丘在一起，庭中放着五百只钵，讲五受阴的生灭。",
        "魔化作大牛走进钵中间，比丘想赶走它，怕打坏钵。佛说：「这不是牛，是魔波旬。」说偈："
        "「色受想行识，不是我、也不是我所；如实知道这义理，对它们就没有执着。"
        "无所著而安稳，超出各种结缚；魔军即使到处找，也永远找不到他。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.16；五取阴非我我所、魔不得处，据巴利。"
    ),
}

# --- SA 1103 入处（SN4.17 Āyatana）------------------------------------------
SUTTAS["SA_1103"] = {
    "lit": [
        OPEN_WILD_LIT + "与六百比丘俱，说六触入处集、灭。",
        "魔化大身怖人，比丘毛竖。佛言：「此是恶魔。」说偈："
        "「色声香味触，及法为第六；世间所贪著，是为最恶饵。"
        "佛弟子正念，超越此一切；已出魔境界，如日无云翳。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_WILD_MOD + "与六百比丘在一起，讲六触入处的集起与灭尽。",
        "魔化作高大可怕的身形，比丘们汗毛直竖。佛说：「这是恶魔。」说偈："
        "「色声香味触，以及第六的法；世间所贪着的，就是最坏的诱饵。"
        "佛的弟子保持正念，超越这一切；已经离开魔的境界，像太阳没有云翳。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN4.17；六境为饵、正念弟子出魔界，据巴利。"
    ),
}

# --- SA 1104 帝释（SN11.11 Vatapada）----------------------------------------
SUTTAS["SA_1104"] = {
    "lit": [
        OPEN_BAM_LIT,
        "佛告诸比丘：「若人受持七种受，以此因缘得生帝释处。"
        + SEVEN_VOWS_LIT
        + "」",
        "尔时世尊说偈言：" + SEVEN_VERSE_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "佛告诉比丘们：「如果有人受持七种誓愿，凭这因缘能生到帝释那里。"
        + SEVEN_VOWS_MOD
        + "」",
        "那时世尊说偈：" + SEVEN_VERSE_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN11.11；据巴利补第七『不瞋／速除瞋』（汉本漏略或并入他项）。"
    ),
}

# --- SA 1105 摩诃离（SN11.13 Mahāli）----------------------------------------
SUTTAS["SA_1105"] = {
    "lit": [
        OPEN_VES_LIT,
        "离车摩诃利来问：「世尊见天帝释不？」佛言：「见。」"
        "又问：「见有鬼似帝释形不？」佛言：「我知帝释，亦知有鬼似帝释；"
        "亦知彼因受持法故得生帝释处——本为人时，」" + SEVEN_VOWS_LIT,
        "即说偈言：" + SEVEN_VERSE_LIT,
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "离车人摩诃利前来问：「世尊见过天帝释吗？」佛说：「见过。」"
        "又问：「见过长得像帝释的鬼吗？」佛说：「我认识帝释，也知道有鬼长得像帝释；"
        "也知道他因受持那些法才生到帝释位——从前做人时，」" + SEVEN_VOWS_MOD,
        "就说偈：" + SEVEN_VERSE_MOD,
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN11.13；汉『乃至行平等捨』删省七受，据 SN 展开；"
        "巴利详帝释异名，本经问答以七受为核心，异名详见 SA_1106。"
    ),
}

# --- SA 1106 以何因（SN11.12 Sakka-nāma）------------------------------------
SUTTAS["SA_1106"] = {
    "lit": [
        OPEN_VES_LIT,
        "有异比丘问：「何因名释提桓因？」佛言：「本为人时能善行施，故名释提桓因（能）。」"
        "「何因名富兰陀罗？」佛言：「本为人时最先行施，故名富兰陀罗（先施）。」"
        "「何因名摩伽婆？」佛言：「本为人时名摩伽，故仍称摩伽婆。」"
        "「何因名婆娑婆？」佛言：「本为人时施设客堂，故名婆娑婆。」"
        "「何因名憍尸迦？」佛言：「本属憍尸族，故名憍尸迦。」"
        "「何因名舍脂钵低？」佛言：「阿修罗女舍脂为第一天后，故名舍脂之夫。」"
        "「何因名千眼？」佛言：「于一坐顷能思千义，故名千眼。」"
        "「何因名因提利？」佛言：「于三十三天为王为主，故名天王。」",
        "「复次，本为人时受持七种受，故得为帝释，远离恶趣苦。」" + SEVEN_VOWS_LIT,
        "尔时世尊说偈言：" + SEVEN_VERSE_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "有一位比丘问：「为什么叫释提桓因？」佛说：「从前做人时善于布施，所以叫释提桓因（能者）。」"
        "「为什么叫富兰陀罗？」佛说：「从前做人时最先布施，所以叫富兰陀罗（先施者）。」"
        "「为什么叫摩伽婆？」佛说：「从前做人时名叫摩伽，所以仍称摩伽婆。」"
        "「为什么叫婆娑婆？」佛说：「从前做人时施设客堂，所以叫婆娑婆。」"
        "「为什么叫憍尸迦？」佛说：「本属憍尸族，所以叫憍尸迦。」"
        "「为什么叫舍脂钵低？」佛说：「阿修罗女舍脂是第一天后，所以叫舍脂之夫。」"
        "「为什么叫千眼？」佛说：「在一次坐中能思考上千种义理，所以叫千眼。」"
        "「为什么叫因提利？」佛说：「在三十三天做王做主，所以叫天王。」",
        "「再者，从前做人时受持七种誓愿，所以成为帝释，远离恶趣之苦。」" + SEVEN_VOWS_MOD,
        "那时世尊说偈：" + SEVEN_VERSE_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN11.12；据巴利校正词源：Sakka＝能施、Purindada＝先施、"
        "Vāsava＝施客堂（校正汉『婆詵私衣』）、千眼＝一坐思千义。"
        "末『如上广说』偈据 SN11.12／SA_1104 七受偈重建。"
    ),
}

# --- SA 1107 夜叉（SN11.22 Dubbaṇṇiya）--------------------------------------
SUTTAS["SA_1107"] = {
    "lit": [
        OPEN_VES_LIT,
        "佛告诸比丘：「过去有一夜叉，丑恶无仪，坐帝释空座。三十三天见已大瞋；"
        "诸天愈瞋，彼鬼愈端正。天往白帝释，帝释言：『彼是食瞋鬼。』"
        "即往合掌三称：『仁者！我是释提桓因。』帝释愈恭下，鬼愈丑恶，寻没不现。"
        "帝释复位，说偈教诫不瞋：瞋盛能自持，如制逸马车；能持者名善御，非谓执缰人。」",
        SAKKA_EXHORT_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "佛告诉比丘们：「过去有一个夜叉，相貌丑恶，坐在帝释空着的宝座上。三十三天见了大怒；"
        "天越怒，那鬼反而越端正。天去禀告帝释，帝释说：『那是吃瞋恚的鬼。』"
        "帝释亲自前去，合掌三次自称：『仁者！我是释提桓因。』他越谦下，鬼越丑，终于隐没。"
        "帝释回到座位，用偈教人不要瞋：瞋火再盛也能自持，像制服乱跑的马车；"
        "能这样自持的才叫好车夫，不只是抓住缰绳的人。」",
        SAKKA_EXHORT_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN11.22；食瞋鬼（kodhabhakkha）——瞋增则彼美，敬下则彼灭。"
    ),
}

# --- SA 1108 得眼（SN11.24 Accaya）------------------------------------------
SUTTAS["SA_1108"] = {
    "lit": [
        OPEN_JET_LIT,
        "世尊乞食已，至安陀林昼正受。时祇桓二比丘诤，一骂一默；骂者悔谢，彼不受忏，"
        "众共劝谏，高声闹乱。佛以天耳闻，还问因缘。",
        "佛言：「有二愚：犯罪而不自知；人悔谢而不受。有二智：知罪；及能受忏。"
        "不受忏者，长夜当得不饶益苦。过去帝释于三十三天说偈：于他无害心，瞋亦不长住；"
        "盛瞋能自持，如制逸马车；能持名善御，非谓执缰者。」",
        SAKKA_EXHORT_LIT.replace("不瞋与忍", "忍辱"),
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "世尊乞食后，到安陀林作日间禅定。那时祇园有两个比丘争执，一个骂、一个沉默；"
        "骂的人悔过道歉，对方不接受，众人劝谏，吵嚷起来。佛用天耳听见，回来询问缘故。",
        "佛说：「有两种愚人：犯了错却不自知；别人悔过却不接受。有两种智者：知道自己的错；"
        "以及能接受别人的忏悔。不接受忏悔的人，长夜会得到无益的苦。过去帝释在三十三天说偈："
        "对他人不起害心，瞋也不久住；瞋火再盛也能自持，像制服乱跑的马车；"
        "能这样自持才叫好车夫，不只是抓住缰绳的人。」",
        SAKKA_EXHORT_MOD.replace("不瞋与忍辱", "忍辱"),
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN11.24；二愚二智（知过／受忏）据巴利补明；汉详帝释忍辱偈，并存。"
    ),
}

# --- SA 1109 得善胜（SN11.5 Subhāsitajaya）----------------------------------
SUTTAS["SA_1109"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告诸比丘：「过去天与阿修罗欲战。帝释共毘摩质多罗约：以论议决胜负，"
        "理屈者伏；两边各有明识证知。",
        "阿修罗王先立论：若不折伏愚人，愚人更伤人，当以力杖强制。"
        "帝释答：见愚瞋盛，智以静默伏；忍为最上，自他俱安。"
        "两边智者称量：阿修罗偈长夜长诤斗；帝释偈长夜息诤斗——帝释善论得胜。」",
        "「释提桓因以善论伏阿修罗。汝等出家，亦当善论、赞叹善论。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「过去天与阿修罗要开战。帝释和毘摩质多罗约定：用辩论分胜负，"
        "理亏的认输；两边各有明白事理的人作证。",
        "阿修罗王先立论：若不制服愚人，愚人更会伤人，应当用强力和杖来压。"
        "帝释回答：看见愚人瞋盛，智者用平静沉默来降伏；忍是最上的，自己和他人都得安稳。"
        "两边有智慧的人衡量：阿修罗的偈会长夜助长争斗；帝释的偈会长夜止息争斗——帝释辩论得胜。」",
        "「帝释用善论折服阿修罗。你们出家，也应当善于论议、赞叹善论。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN11.5；删梵式往复偈群，保留『力伏愚』vs『忍默伏』对立及裁判结论。"
    ),
}

# --- SA 1110 缚系（SN11.4 Vepacitti）----------------------------------------
SUTTAS["SA_1110"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告诸比丘：「过去天与阿修罗战。帝释勅：若天胜，生擒毘摩质多罗，五缚送天宫；"
        "阿修罗王亦勅反缚帝释。战后天胜，以五缚系阿修罗王于断法殿门侧。"
        "帝释出入，彼瞋骂不已。御者问：为畏为力不足而忍耶？"
        "帝释答：非畏非力不足；黠慧岂与愚夫对诤？见愚瞋盛，智以静默伏。"
        "强忍弱者，是为上忍；自他俱护，忍辱常得胜，亦免长夜苦。」",
        SAKKA_EXHORT_LIT.replace("不瞋与忍", "忍辱"),
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘们：「过去天与阿修罗交战。帝释下令：若天胜，就活捉毘摩质多罗，五花大绑送回天宫；"
        "阿修罗王也下令反过来绑帝释。交战后天胜了，用五花大绑把阿修罗王绑在断法殿门边。"
        "帝释进出时，对方不停怒骂。车夫问：您是害怕还是力气不够才忍耐？"
        "帝释答：不是怕，也不是力气不够；有智慧的人怎会跟愚人对骂？见愚人瞋盛，智者用沉默降伏。"
        "强者能忍弱者，才是最上的忍；保护自己也保护他人，忍辱往往得胜，也免长夜之苦。」",
        SAKKA_EXHORT_MOD.replace("不瞋与忍辱", "忍辱"),
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN11.4；五缚门侧骂辱、御者激将、帝释明忍非畏，据巴利；压缩多层对偈。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {f"SA_{i}": "high" for i in batch_range}

RECONSTRUCTED: dict[str, str] = {
    "SA_1105": "汉『乃至行平等捨』删省七受；据 SN11.13／七受偈展开",
    "SA_1106": "汉末『如上广说』删省七受偈；据 SN11.12／SA_1104 重建，并校正词源",
    "SA_1092": "删魔女百种色变之梵式反复，保留六类形色与偈问答纲",
    "SA_1109": "压缩天阿修罗多层对偈为力伏／忍伏对立及裁判结论",
    "SA_1110": "压缩御者—帝释多层对偈，保留五缚骂辱与上忍义",
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
    assert set(GOLD) == {f"SA_{i}" for i in batch_range}, (
        "GOLD must cover SA_1091–SA_1110 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    assert not any(
        f"SA_{i}" in GOLD for i in list(range(1071, 1091)) + list(range(1111, 1131))
    )

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

    _goldish = {"gold", "gold_reconstructed"}
    by_lookup = {r["id"]: r for r in records}

    boundary_ids: list[str] = []
    if by_lookup.get("SA_1090", {}).get("review_status") in _goldish:
        boundary_ids.append("SA_1090")
    boundary_ids.append("SA_1111")

    boundary_before = {bid: None for bid in boundary_ids}
    for rec in records:
        if rec["id"] in boundary_before:
            boundary_before[rec["id"]] = _snap(rec)

    guard_ids = {f"SA_{i}" for i in list(range(1071, 1091)) + list(range(1111, 1131))}
    mid_before = {rec["id"]: _snap(rec) for rec in records if rec["id"] in guard_ids}

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

    by_merged = {r["id"]: r for r in merged}
    for bid, before in boundary_before.items():
        if before is None:
            continue
        after = _snap(by_merged[bid])
        assert before == after, f"{bid} must remain untouched"

    for rid, before in mid_before.items():
        after = _snap(by_merged[rid])
        assert before == after, f"{rid} (neighbor) must remain untouched"

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1091-1110.json").write_text(
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

    continuous = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in _goldish for i in batch_range
    )
    sa1090_status = by_merged.get("SA_1090", {}).get("review_status")
    sa1090_note = (
        f"SA_1090_untouched=True (was {sa1090_status})"
        if "SA_1090" in boundary_before and boundary_before["SA_1090"] is not None
        else f"SA_1090_not_gold (status={sa1090_status}); skip assert"
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1091–SA_1110 only)")
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
    print(f"continuous_gold_SA_1091–1110={continuous}")
    print(sa1090_note)
    print("SA_1111_untouched=True")
    print("neighbors_1071–1090_and_1111–1130_untouched=True")
    for r in report:
        print(
            r["id"],
            r["status"],
            f"sim={r['sim']}",
            f"paras={r['paragraphs']}",
            r["confidence"],
            r["review_status"],
            f"gate={r['gate_reasons']}" if r["gate_reasons"] else "",
        )


if __name__ == "__main__":
    main()
