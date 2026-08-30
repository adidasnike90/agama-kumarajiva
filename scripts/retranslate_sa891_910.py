#!/usr/bin/env python3
"""Retranslate SA 891–910（湖池／入界阴／不坏净／聚落主）→ merge.

本批二十经：
891 湖池 SN13.2（SC 栏或标 SN13.1；汉湖池＝莲池量喻族）
892–901 入界阴相应：六内处、种子、如实知、三爱、三有漏、罗睺罗 SN18.1、
        眼已断、眼生 SN26.1、眼著 SN27.1、善法
902–904 不坏净 AN4.34（第一信：如来／离贪法／声闻众）
905–910 聚落主：外道 SN16.12、法减灭 SN16.13、动摇 SN42.2、争斗 SN42.3、
        调马 SN42.5、恶性 SN42.1

信：有平行者以 SN／AN／Pāli／Sujato 厘义；无平行者 medium。
    peyyāla／删省（903–904、895–896 等）→ gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_891–910；不触碰邻经；
      若 SA_890 已为 gold／gold_reconstructed 则断言不变，并断言 SA_911 不变。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

batch_range = range(891, 911)

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

OPEN_RAJ_LIT = "如是我闻：一时，佛住王舍城迦兰陀竹园。"
OPEN_RAJ_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "彼聚落主闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY_MOD = "那位聚落主听佛所说，欢喜随喜，作礼离去。"

SIX_IN_LIT = "眼、耳、鼻、舌、身、意"
SIX_IN_MOD = "眼、耳、鼻、舌、身、意"

ARHAT_LIT = (
    "是名阿罗汉：诸漏已尽，所作已作，舍诸重担，逮得己利，尽诸有结，正智心善解脱。"
)
ARHAT_MOD = (
    "这叫做阿罗汉：诸漏已尽，该做的已做，放下重担，得到自己的利益，"
    "有结尽了，以正智心善解脱。"
)

PEYYALA_AYAT_LIT = "如内六入处，外六入处、六识、六触、六受、六想、六思、六爱、六界、五阴，亦如是说。"
PEYYALA_AYAT_MOD = (
    "如同内六入处，外六入处、六识、六触、六受、六想、六思、六爱、六界、五阴，也是这样说。"
)

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

REFUGE_LIT = "归佛、归法、归比丘僧。"
REFUGE_MOD = "归依佛、归依法、归依比丘僧。"

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 891 湖池（SN13.2 Pokkharaṇī；SC 或标 SN13.1）-----------------------
SUTTAS["SA_891"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「譬如湖池，纵横五十由旬，深亦如是，水满欲溢。"
        "有人以一毛端渧取其水。云何——毛端一渧为多？湖水为多？」"
        "比丘白佛：「毛端一渧甚少；湖水无量，不可为比。」"
        "佛言：「见具足、正见具足之圣弟子，于法现观已，所断众苦无量，如大湖水；"
        "所余之苦，如毛端一渧——最多七有，当究竟苦边。"
        "见法、得法眼，其利如是。」",
        "如毛端，草筹端渧水亦尔；如湖池，萨罗、恒河、耶符那、及大海，其譬亦尔。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「好比一座湖池，长宽各五十由旬，深也一样，水满得快溢出来。"
        "有人用一根毛尖蘸那湖水。怎么样——毛尖蘸的一滴多，还是湖水多？」"
        "比丘们禀告：「毛尖一滴很少；湖水多得无法相比。」"
        "佛说：「见具足、正见具足的圣弟子，于法现观之后，已经断除的苦无量，像大湖的水；"
        "剩下的苦，像毛尖一滴——最多还有七次生死，就会到苦的尽头。"
        "见法、得法眼，利益就是这样大。」",
        "像毛尖一样，草茎尖蘸水也可以这样说；像湖池一样，萨罗池、恒河、耶符那河、以及大海，也可以同样说。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：汉湖池量喻＝SN13.2 Pokkharaṇī（莲池）；"
        "SC 栏或标 SN13.1 Nakhasikhā（爪甲尘），今据正文取 SN13.2。"
        "「最多七有」据 SN 补明须陀洹余苦上际；末河海异门略存。"
    ),
}

# --- SA 892 六内处等（无专 SN；入流／漏尽定型）-----------------------------
SUTTAS["SA_892"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有内六入处——眼内入处，耳、鼻、舌、身、意内入处。"
        "于此六法观察忍，名信行：超升离生，离凡夫地；虽未得须陀洹，命终前必得。"
        "若增上观察忍，名法行：亦超升离生，离凡夫地；命终前必得须陀洹。"
        "若如实正智观察，三结已尽——身见、戒取、疑——是名须陀洹："
        "不堕恶趣，定趣正觉，七有天人往生，究竟苦边。"
        "若正智观察，不起诸漏，离欲解脱，名阿罗汉；" + ARHAT_LIT + "」",
        PEYYALA_AYAT_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有内六入处——眼内入处，以及耳、鼻、舌、身、意内入处。"
        "对这些法以观察而忍可，叫做信行：超升离生，离开凡夫地；虽然还没证须陀洹，命终前一定能得。"
        "如果以更增上的观察而忍可，叫做法行：同样超升离生，离开凡夫地；命终前一定能得须陀洹。"
        "如果以如实正智观察，三结已经尽了——身见、戒取、疑——就叫须陀洹："
        "不堕恶趣，必定趋向正觉，最多七次在人天往来，究竟苦边。"
        "如果正智观察，不再起诸漏，离欲解脱，就叫阿罗汉；" + ARHAT_MOD + "」",
        PEYYALA_AYAT_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：信行／法行／须陀洹三结／阿罗汉漏尽为早期定型；"
        "末「外六入乃至五阴」peyyāla 略存。近 SN25／SN26 观门族，不妄改。"
    ),
}

# --- SA 893 五种种子（近 SN22.54；无 SC 专标）------------------------------
SUTTAS["SA_893"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有五种子——根种、茎种、节种、枝种、种子。"
        "若种不断、不坏、不腐、不穿，得地不得水，不得生长；得水不得地，亦不得生长；"
        "地水俱得，乃得生长增广。"
        "如是：有业，而烦恼、爱、见、慢、无明未断，则行得生；"
        "若有业而无烦恼、爱、见、无明，行则灭。」",
        "如行，识、名色、六入处、触、受、爱、取、有、生、老死，亦如是说。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有五种种子——根种、茎种、节种、枝种、种子。"
        "如果种子不断、不坏、不腐、不破，有地没有水，不能生长；有水没有地，也不能生长；"
        "地和水都有，才能生长增广。"
        "同样：有业，而烦恼、爱、见、慢、无明还没断，诸行就会生起；"
        "如果有业却没有烦恼、爱、见、无明，诸行就会灭。」",
        "像行一样，识、名色、六入处、触、受、爱、取、有、生、老死，也可以这样说。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：喻近 SN22.54 Bīja（五种子＋地水）；"
        "汉以业／烦恼等生「行」而贯十二支，从汉框架，不整经改作「识住」。"
    ),
}

# --- SA 894 如实知（世间集等异门；无专 SN）---------------------------------
SUTTAS["SA_894"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「我于世间、世间集不如实知时，"
        "终不得于天、魔、梵、沙门、婆罗门及诸众生中，为解脱、为出离，心离颠倒，"
        "亦不名等正觉。"
        "以我于世间及世间集如实知故，乃得解脱、出离，心离颠倒，成等正觉。」",
        "如世间、世间集，世间灭、世间出，乃至世间集、灭、味、患、出，"
        "及集灭道迹、味患出等异门，亦如是说。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「我若对世间、世间的集起不能如实了知，"
        "终究不能在天、魔、梵、沙门、婆罗门以及众生之中，得到解脱、出离，心离颠倒，"
        "也不叫做等正觉。"
        "因为我对世间及世间的集起如实了知，才得到解脱、出离，心离颠倒，成等正觉。」",
        "如同世间、世间集，世间灭、世间出，一直到世间的集、灭、味、患、出，"
        "以及集灭道迹、味患出等不同说法，也可以这样说。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：觉者「如实知世间」定型；末异门 peyyāla 压缩列举，不逐门展开。"
    ),
}

# --- SA 895 三爱（无专 SN；peyyāla 求师等）---------------------------------
SUTTAS["SA_895"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有三爱——欲爱、色爱、无色爱。"
        "为断此三爱故，当求大师。」",
        "如求大师，次师、教师、善知识、梵行者，乃至念处、正勤、根、力、觉、道、止观、正思惟，亦如是说。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有三种爱——欲爱、色爱、无色爱。"
        "为了断这三种爱，应当求大师。」",
        "如同求大师，求次师、教师、善知识、梵行者，一直到念处、正勤、根、力、觉支、道、止观、正思惟，也可以这样说。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：三爱为早期定型；汉末长串「求××」peyyāla 压缩为纲。"
    ),
}

# --- SA 896 三有漏（无专 SN；同上 peyyāla）---------------------------------
SUTTAS["SA_896"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有三有漏——欲有漏、有有漏、无明有漏。"
        "为断此三有漏故，当求大师。」",
        "如求大师，乃至求正思惟，亦如是说。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有三种有漏——欲有漏、有有漏、无明有漏。"
        "为了断这三种有漏，应当求大师。」",
        "如同求大师，一直到求正思惟，也可以这样说。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：三有漏定型；「乃至正思惟」交叉指示 SA_895 求师链，gold_reconstructed。"
    ),
}

# --- SA 897 罗睺罗（SN18.1 Cakkhu；据巴利校正汉「内六入尽漏」本）-----------
SUTTAS["SA_897"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者罗睺罗来诣佛所，稽首礼足，退坐一面，白佛言："
        "「善哉世尊！愿略说法。我闻已，当独一静处，精勤修习。」"
        "佛告罗睺罗：「于意云何——眼是常耶？无常耶？」"
        "「无常，世尊。」"
        "「无常者，是苦耶？乐耶？」"
        "「苦，世尊。」"
        "「若无常、苦、变易之法，可观为『此是我的、我是彼、彼是我的我』不？」"
        "「不也，世尊。」"
        "「耳、鼻、舌、身、意，亦复如是——无常、苦，不可计我。」"
        "「如是观已，多闻圣弟子于眼乃至意厌；厌故离贪；离贪故解脱；"
        "解脱已，自知解脱：『我生已尽，梵行已立，所作已作，自知不受后有。』」",
        "如眼，色、识、触，乃至五阴，亦如是说。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时罗睺罗尊者来到佛那里，顶礼后坐在一边，对佛说："
        "「愿世尊为我略说法。我听了以后，要独自在静处精勤修习。」"
        "佛问罗睺罗：「你怎么看——眼是常，还是无常？」"
        "「无常，世尊。」"
        "「无常的，是苦，还是乐？」"
        "「是苦，世尊。」"
        "「若是无常、苦、会变坏的法，还能看成『这是我的、我就是它、它是我的我』吗？」"
        "「不能，世尊。」"
        "「耳、鼻、舌、身、意也是一样——无常、苦，不可计为我。」"
        "「这样观察以后，多闻圣弟子对眼直到意都会厌离；厌离所以离贪；离贪所以解脱；"
        "解脱以后，自己知道解脱：『我生已尽，梵行已立，所作已作，自知不受后有。』」",
        "像眼一样，色、识、触，一直到五阴，也可以这样说。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN18.1 Cakkhu。"
        "汉本作「正观内六入尽有漏」框，与 SN 无常／苦／非我现观不合，"
        "今据 SN 校正；住处从 SN 作祇园。末「乃至五阴」从汉 peyyāla。"
    ),
}

# --- SA 898 眼已断（无专 SN）-----------------------------------------------
SUTTAS["SA_898"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时世尊告诸比丘：「若比丘于眼欲贪断，是名眼已断——"
        "已知、断其根本，如截多罗树头，于未来世成不生法。"
        "耳、鼻、舌、身、意，亦复如是。」",
        PEYYALA_AYAT_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时世尊告诉比丘们：「如果比丘对眼的欲贪断除了，就叫眼已断——"
        "已经了知、断了根本，像截断多罗树头，在未来世成为不再生起的法。"
        "耳、鼻、舌、身、意也是这样。」",
        PEYYALA_AYAT_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：欲贪断＝「已断」定型；近 SN35 断贪族，无专经不抬高置信。"
    ),
}

# --- SA 899 眼生（SN26.1 Uppāda）------------------------------------------
SUTTAS["SA_899"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时世尊告诸比丘：「若眼生、住、成就、显现，则苦生、病住、老死显现；"
        "耳、鼻、舌、身、意亦如是。"
        "若眼灭、息、没，则苦灭、病息、老死没；乃至意亦如是。」",
        PEYYALA_AYAT_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时世尊告诉比丘们：「如果眼生起、住留、成就、显现，那么苦就生起、病就住留、老死就显现；"
        "耳、鼻、舌、身、意也是这样。"
        "如果眼灭尽、止息、消失，那么苦就灭、病就息、老死就没；一直到意也是这样。」",
        PEYYALA_AYAT_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN26.1 Uppāda。"
        "汉「苦生、病住、老死显现」与巴利 dukkha／roga／jarāmaraṇa 对应，从 SN。"
    ),
}

# --- SA 900 眼著（SN27.1 Cakkhu；据巴利补「心向出离」）---------------------
SUTTAS["SA_900"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时世尊告诸比丘：「于眼欲贪，是心之烦恼；耳、鼻、舌、身、意欲贪，亦心之烦恼。"
        "比丘于此六处心烦恼已断者，其心倾向出离；"
        "心为出离所修习，则于胜智所应证法，堪任能作。」",
        PEYYALA_AYAT_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时世尊告诉比丘们：「对眼的欲贪，是心的烦恼；对耳、鼻、舌、身、意的欲贪，也是心的烦恼。"
        "比丘在这六处上心的烦恼已经断除的，他的心就倾向出离；"
        "心被出离所修习，对于应当以胜智证得的法，就堪能担当。」",
        PEYYALA_AYAT_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN27.1 Cakkhu。"
        "汉「味著生上烦恼、障不得断」义近；今据 SN 补「心向出离／堪任胜智」，"
        "据 SN 校正。"
    ),
}

# --- SA 901 善法建立（无专 SN）---------------------------------------------
SUTTAS["SA_901"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "佛告比丘：「善法所依，在于内六处——犹造作所依，在于大地。"
        "外六处乃至五阴，为善法依，亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "佛告诉比丘们：「善法的依止，在内六处——就像造作的依止，在大地。"
        "外六处一直到五阴，作为善法的依止，也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：依处建立善法定型；末异门略提不演。"
    ),
}

# --- SA 902 如來第一（AN4.34 Aggappasāda 之一）-----------------------------
SUTTAS["SA_902"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时世尊告诸比丘：「若诸众生——无足、二足、四足、多足，有色、无色，"
        "有想、无想、非想非非想——于彼如来、应、等正觉最第一。"
        "若于佛得不坏净，是信于第一；信于第一者，得第一果。"
        "如是于法、于僧、于圣戒得不坏净，亦第一信、得第一果。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时世尊告诉比丘们：「无论哪些众生——没有脚的、两脚的、四脚的、多脚的，有色的、无色的，"
        "有想的、无想的、非想非非想的——在他们之中，如来、应、等正觉是最第一。"
        "如果对佛成就不坏净，就是信于第一；信于第一的人，得到第一的果报。"
        "同样，对法、对僧、对圣戒成就不坏净，也是第一的信、得第一的果。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：平行 AN4.34／AN5.32／Iti90。"
        "汉「乃至圣戒」peyyāla 据 AN 四／五第一信补佛／法／僧／戒不坏净果。"
        "本经专举如来第一。"
    ),
}

# --- SA 903 离贪法第一（AN4.34 virāga；汉删省）-----------------------------
SUTTAS["SA_903"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时世尊告诸比丘：「譬如世间所作，皆依于地而得建立；"
        "如是一切法——有为、无为——离贪之法最第一，"
        "谓骄慢尽、渴爱灭、依处拔、轮回断、爱尽、离贪、灭、涅槃。"
        "若于离贪法得不坏净，是信于第一；信于第一者，得第一果。"
        "于佛、僧、圣戒亦如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时世尊告诉比丘们：「好比世间所做的事，都依止大地才能建立；"
        "同样，一切法——有为的、无为的——离贪之法是最第一，"
        "也就是骄慢尽、渴爱灭、依处拔除、轮回切断、爱尽、离贪、灭、涅槃。"
        "如果对离贪法成就不坏净，就是信于第一；信于第一的人，得到第一的果报。"
        "对佛、僧、圣戒也可以这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：AN4.34 第三分 virāgo…nibbānaṁ。"
        "汉「如是广说乃至圣戒」删省，据 AN 补离贪法释义及不坏净果；"
        "汉地依之喻保留为起句。gold_reconstructed。"
    ),
}

# --- SA 904 声闻第一（AN4.34 saṅgha；汉删省）------------------------------
SUTTAS["SA_904"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "尔时世尊告诸比丘：「若诸世间众会，如来声闻众最第一——"
        "所谓四双八士，应请、应待、应供、应合掌，世间无上福田。"
        "若于僧得不坏净，是信于第一；信于第一者，得第一果。"
        "于佛、法、圣戒亦如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时世尊告诉比丘们：「在世间各种众会之中，如来的声闻众是最第一——"
        "也就是四双八辈，应请、应待、应供、应合掌，是世间无上福田。"
        "如果对僧成就不坏净，就是信于第一；信于第一的人，得到第一的果报。"
        "对佛、法、圣戒也可以这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：AN4.34 第四分 sāvakasaṅgha。"
        "汉「如是广说乃至圣戒」删省，据 AN 补僧德及不坏净果。gold_reconstructed。"
    ),
}

# --- SA 905 外道（SN16.12 Paraṁmaraṇa；据巴利校正）-------------------------
SUTTAS["SA_905"] = {
    "lit": [
        "如是我闻：一时，尊者摩诃迦叶、尊者舍利弗住波罗奈仙人住处鹿野苑。",
        "晡时，舍利弗从禅觉，诣摩诃迦叶所，共相问讯，退坐一面，问言："
        "「迦叶！如来死后有耶？」"
        "「此，世尊不记说。」"
        "「死后无耶？亦有亦无耶？非有非无耶？」"
        "「皆不记说。」"
        "「以何因缘不记说？」"
        "「此事不引义、不引法、不资梵行，不趣厌、离贪、灭、静、通、觉、涅槃，是故不记。」"
        "「何所记说？」"
        "「苦、苦集、苦灭、苦灭道迹——此是世尊所记。"
        "以能引义、引法、资梵行，趣厌、离贪、灭、静、通、觉、涅槃故。」",
        "时二正士共论已，各还本处。",
    ],
    "mod": [
        "我是这样听说的：有一次，摩诃迦叶尊者、舍利弗尊者住在波罗奈仙人住处鹿野苑。",
        "下午，舍利弗从禅定起来，到摩诃迦叶那里，互相问讯后坐在一边，问道："
        "「迦叶！如来死后还有吗？」"
        "「这件事，世尊不记说。」"
        "「死后没有吗？也有也没有吗？既非有也非没有吗？」"
        "「都不记说。」"
        "「因为什么因缘不记说？」"
        "「这件事不引义、不引法、无益于梵行，不导向厌离、离贪、灭、平静、通达、觉醒、涅槃，所以不记。」"
        "「那么记说的是什么？」"
        "「苦、苦集、苦灭、苦灭道迹——这是世尊所记说的。"
        "因为能引义、引法、有益于梵行，导向厌离、离贪、灭、平静、通达、觉醒、涅槃。」",
        "两位正士讨论完，各自回去。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN16.12 Paraṁmaraṇa。"
        "汉作外道四句诘舍利弗，迦叶以五蕴尽／涅槃释不记；"
        "今据 SN 校正为：不记因不资梵行，所记者四谛。住处从 SN 作鹿野苑。"
    ),
}

# --- SA 906 法减灭（SN16.13 Saddhammapatirūpaka）---------------------------
SUTTAS["SA_906"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时尊者摩诃迦叶住东园鹿子母讲堂，晡时从禅觉，诣佛所，稽首退坐，白佛言："
        "「何因何缘，昔少制戒而多比丘得证；今多制戒而少乐习学？」"
        "佛告迦叶：「众生减、正法欲灭时，制戒则多，得证则少。"
        "相似像法未出，正法不灭；相似像法出，正法乃灭——"
        "如真金未有伪金则不没，伪金出则真金没。"
        "正法非为地水火风所坏，乃因恶人于中非法说法、法说非法、非律说律、律说非律，"
        "以相似法炽然故灭；亦不顿没如海船沉，唯渐次灭。」",
        "「有五因缘令正法沉没：于大师、法、学、随顺教、所赞梵行，不恭敬、不下意供养而依住。"
        "有五因缘令法、律不没、不忘、不退：于此五者恭敬尊重、下意供养、依止而住。"
        "是故当学：于大师乃至所赞梵行，恭敬供养，依止而住。」",
        "尊者摩诃迦叶闻已，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时摩诃迦叶尊者住在东园鹿子母讲堂，下午从禅定起来，到佛那里，顶礼后退坐，问道："
        "「什么因缘，从前戒条少而证果的比丘多；如今戒条多而乐于修学的少？」"
        "佛告诉迦叶：「众生衰退、正法将灭时，制定的戒就多，证得的就少。"
        "相似像法还没出现，正法不会灭；相似像法一出现，正法才会灭——"
        "好比还没有伪金时真金不消失，伪金出现了真金就消失。"
        "正法不是被地水火风所坏，而是因为恶人在里面把非法说成法、法说成非法、非律说成律、律说成非律，"
        "用相似的法旺起来才灭；也不会像海船那样一下子沉没，只是渐渐灭。」",
        "「有五种因缘使正法沉没：对大师、法、学处、随顺教、以及大师所赞的梵行，不恭敬、不下意供养却还依止而住。"
        "有五种因缘使法、律不沉没、不遗忘、不衰退：对这五者恭敬尊重、下意供养、依止而住。"
        "所以应当学：对大师一直到所赞的梵行，都恭敬供养，依止而住。」",
        "摩诃迦叶尊者听完，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN16.13 Saddhammapatirūpaka。"
        "汉五浊／五不敬与 SN 像法、五不恭敬相应；伪宝喻据 SN 真金／伪金，从 SN。"
    ),
}

# --- SA 907 动摇（SN42.2 Tālapuṭa 伎儿）------------------------------------
SUTTAS["SA_907"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时遮罗周罗那罗聚落主来诣佛所，问讯退坐，白言："
        "「瞿昙！我闻古昔伎儿耆宿言：『若于大众中歌舞伎戏，令人喜笑，身坏命终生欢喜天。』"
        "瞿昙法中义云何？」"
        "佛言：「且止，莫问。」如是再三，犹请不已。",
        "佛言：「古昔众生不离贪、恚、痴缚。伎儿令其喜笑，岂不增彼三缚？"
        "如人反缚，恶人以水数浇其绳，缚岂不急？」"
        "「如是，瞿昙！」"
        "「若言伎儿以喜笑业生欢喜天，是则邪见；邪见者当生地狱或畜生。」",
        "聚落主悲泣。佛言：「是故我先止汝莫问。」"
        "白言：「非因瞿昙语悲，乃自伤久为愚伎所欺。"
        "我今舍此恶业，" + REFUGE_LIT + "」"
        "佛言：「善哉！此真实要。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时遮罗周罗那罗聚落主来到佛那里，问讯后退坐，说道："
        "「瞿昙！我听从前老一辈伎儿说：『若在大众里歌舞伎戏，使人欢喜笑乐，死后生到欢喜天。』"
        "在瞿昙的法里，意思怎么样？」"
        "佛说：「先别问这个。」这样三次，他还是不停地请。",
        "佛说：「从前的众生离不开贪、瞋、痴的束缚。伎儿让他们喜笑，岂不是加重这三种束缚？"
        "好比有人被绳子反绑着，恶人夜里一次次用水浇那绳子，绑得岂不是更紧？」"
        "「是的，瞿昙！」"
        "「若说伎儿凭逗人喜笑的业能生欢喜天，那就是邪见；邪见的人应当生到地狱或畜生。」",
        "聚落主哭了。佛说：「所以我起先不让你问。」"
        "他说：「不是因为您这话才哭，是伤心自己长久被那些愚昧伎儿所骗。"
        "我从今天起舍这种恶业，" + REFUGE_MOD + "」"
        "佛说：「很好！这才是真实切要。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN42.2 Tālapuṭa。"
        "汉「欢喜天」≈ pahāsa；三缚／浇绳喻／邪见二趣与 SN 合。"
    ),
}

# --- SA 908 争斗（SN42.3 Yodhājīva）----------------------------------------
SUTTAS["SA_908"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时战斗活聚落主来诣佛所，问讯退坐，白言："
        "「瞿昙！我闻古昔战斗活耆宿言：『若被甲执兵，先登摧敌，身坏命终生箭降伏天。』"
        "义云何？」"
        "佛言：「且止，莫问。」再三犹请。",
        "佛言：「彼先起伤害心，欲缚、斫、杀于敌；身口意三种恶邪，"
        "而谓生箭降伏天者，无有是处。"
        "若作是见，是则邪见；邪见当生地狱或畜生。」",
        "聚落主悲泣，白言：「自伤久为愚说所欺。我今舍恶业，" + REFUGE_LIT + "」"
        "佛言：「此真实要。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时以战斗为生的聚落主来到佛那里，问讯后退坐，说道："
        "「瞿昙！我听从前老一辈战士说：『若披甲执兵器，冲在前摧破敌人，死后生到箭降伏天。』"
        "意思怎么样？」"
        "佛说：「先别问这个。」三次他还是请。",
        "佛说：「他先起了伤害心，想要捆绑、砍杀敌人；身口意三种恶邪，"
        "却说能生箭降伏天——没有这回事。"
        "如果这样见，就是邪见；邪见应当生到地狱或畜生。」",
        "聚落主哭了，说：「伤心自己长久被愚昧的话所骗。我从今天起舍恶业，" + REFUGE_MOD + "」"
        "佛说：「这才是真实切要。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN42.3 Yodhājīva。"
        "汉「箭降伏天」≈ parajita；三种恶邪／邪见二趣从 SN。"
    ),
}

# --- SA 909 调马（SN42.5 Assāroha；据巴利校正汉「三法调马」本）-------------
SUTTAS["SA_909"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时调马聚落主来诣佛所，问讯退坐，白言："
        "「瞿昙！我闻古昔马乘战士耆宿言：『若于阵上勤勇驰杀，为敌所害，"
        "身坏命终生箭降伏天。』义云何？」"
        "佛言：「且止，莫问。」再三犹请。",
        "佛言：「彼于阵上勤勇时，先起伤害心，欲杀于敌；身口意恶邪，"
        "而谓生箭降伏天者，无有是处。"
        "若作是见，是则邪见；邪见当生地狱或畜生。」",
        "聚落主悲泣，白言：「自伤久为愚说所欺。我今舍恶业，" + REFUGE_LIT + "」"
        "佛言：「此真实要。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时调马（马乘）聚落主来到佛那里，问讯后退坐，说道："
        "「瞿昙！我听从前老一辈马乘战士说：『若在阵上奋勇驰杀，被敌人所害，"
        "死后生到箭降伏天。』意思怎么样？」"
        "佛说：「先别问这个。」三次他还是请。",
        "佛说：「他在阵上奋勇时，先起了伤害心，想杀敌人；身口意恶邪，"
        "却说能生箭降伏天——没有这回事。"
        "如果这样见，就是邪见；邪见应当生到地狱或畜生。」",
        "聚落主哭了，说：「伤心自己长久被愚昧的话所骗。我从今天起舍恶业，" + REFUGE_MOD + "」"
        "佛说：「这才是真实切要。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN42.5 Assāroha（马乘／骑兵长）。"
        "汉误作三法调马（柔软／刚强／「杀」＝不教授，近 AN4.111 Kesi）；"
        "今据 SN 校正为与战斗活同型之阵上业报问答。据 SN 校正。"
    ),
}

# --- SA 910 恶性（SN42.1 Caṇḍa；据巴利校正汉「八正道」本）------------------
SUTTAS["SA_910"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时凶恶聚落主来诣佛所，稽首退坐，白言："
        "「何因何缘，有人称恶性？有人称贤善？」"
        "佛言：「若贪未断，为他所恼，即现瞋忿，故称恶性；瞋、痴未断，亦复如是。"
        "若贪已断，不为他所恼，不现瞋忿，故称贤善；瞋、痴已断，亦复如是。」",
        "聚落主白言：「奇哉！我以贪、瞋、痴故，人称恶性。我今当舍瞋恚粗犷，"
        + REFUGE_LIT
        + "」"
        "佛言：「此真实要。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "那时性情凶恶的聚落主来到佛那里，顶礼后退坐，问道："
        "「什么因缘，有人被称为恶性？有人被称为贤善？」"
        "佛说：「如果贪还没断，被别人触恼就表现出瞋忿，所以被称为恶性；瞋、痴还没断，也是这样。"
        "如果贪已经断了，不被别人触恼，不表现瞋忿，所以被称为贤善；瞋、痴已经断了，也是这样。」",
        "聚落主说：「奇哉！我正因为贪、瞋、痴，才被人叫做恶性。我从今天起要舍弃瞋恚粗暴，"
        + REFUGE_MOD
        + "」"
        "佛说：「这才是真实切要。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN42.1 Caṇḍa。"
        "汉以不修八正道释恶性，与 SN 贪瞋痴未断不合，今据 SN 校正。"
    ),
}

CONFIDENCE: dict[str, str] = {
    "SA_891": "high",
    "SA_892": "medium",
    "SA_893": "medium",
    "SA_894": "medium",
    "SA_895": "medium",
    "SA_896": "medium",
    "SA_897": "high",
    "SA_898": "medium",
    "SA_899": "high",
    "SA_900": "high",
    "SA_901": "medium",
    "SA_902": "high",
    "SA_903": "high",
    "SA_904": "high",
    "SA_905": "high",
    "SA_906": "high",
    "SA_907": "high",
    "SA_908": "high",
    "SA_909": "high",
    "SA_910": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_896": "底本『如求大师，乃至求正思惟』交叉指示 SA_895 求师链；压缩保留",
    "SA_903": "汉『如是广说乃至圣戒』删省；据 AN4.34 virāga／不坏净果重建",
    "SA_904": "汉『如是广说乃至圣戒』删省；据 AN4.34 sāvakasaṅgha／不坏净果重建",
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
        "GOLD must cover SA_891–SA_910 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    assert not any(f"SA_{i}" in GOLD for i in list(range(871, 891)) + list(range(911, 931)))

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

    # Assert SA_890 unchanged if already gold; always guard SA_911
    boundary_ids: list[str] = []
    if by_lookup.get("SA_890", {}).get("review_status") in _goldish:
        boundary_ids.append("SA_890")
    boundary_ids.append("SA_911")

    boundary_before = {bid: None for bid in boundary_ids}
    for rec in records:
        if rec["id"] in boundary_before:
            boundary_before[rec["id"]] = _snap(rec)

    # Neighbors outside batch must remain untouched
    guard_ids = {f"SA_{i}" for i in list(range(871, 891)) + list(range(911, 931))}
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
    (ROOT / "data" / "translated" / "validation_report_sa891-910.json").write_text(
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
    sa890_status = by_merged.get("SA_890", {}).get("review_status")
    sa890_note = (
        f"SA_890_untouched=True (was {sa890_status})"
        if "SA_890" in boundary_before and boundary_before["SA_890"] is not None
        else f"SA_890_not_gold (status={sa890_status}); skip assert"
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_891–SA_910 only)")
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
    print(f"continuous_gold_SA_891–910={continuous}")
    print(sa890_note)
    print("SA_911_untouched=True")
    print("neighbors_871–890_and_911–930_untouched=True")
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
