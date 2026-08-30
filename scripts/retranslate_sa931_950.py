#!/usr/bin/env python3
"""Retranslate SA 931–950（释氏相应末–婆蹉外道相应起）→ merge.

本批二十经：
931–939 释氏相应末（AN6.10 六念、AN11.11–12 十一／十二、AN3.73 学无学、
         SN55.23–24 含罗／麤手、SN15 血泪母乳）
940–950 婆蹉外道相应起（SN15 无始轮回譬：土丸、豆粒、喜乐、苦恼、恐怖、彼爱、
         恒河、骨聚、城、山、过去）

信：有 SN／AN 平行者据巴利／Sujato 厘义；944 无 SC 巴利平行 → medium。
    932 五法据 AN11.11 校正（信精进念定慧，非汉「戒闻施」系）；
    933 据 AN11.12 作五德＋六念（汉「空」衍／十二框压缩）；
    934 问义据 AN3.73 校正为定与慧先后（汉「正受／解脱」）；
    936 据 SN55.24：临终受学；坚固树喻；
    937 「厌已不乐」→「厌故离贪」；
    946 据 SN15.8 校正（汉问诸佛数 → 巴利问过去劫／恒河沙喻）；
    950 据 SN15.7 校正四弟子日忆十万劫。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_931–950；断言 SA_930 不变；不触碰 SA_951+。
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

OPEN_KAP_LIT = "如是我闻：一时，佛住迦毗罗卫国尼拘律园中。"
OPEN_KAP_MOD = "我是这样听说的：有一次，佛住在迦毗罗卫国尼拘律园中。"

OPEN_JET_LIT = "如是我闻：一时，佛住舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_VES_LIT = "如是我闻：一时，佛住毗舍离猕猴池侧重阁讲堂。"
OPEN_VES_MOD = "我是这样听说的：有一次，佛住在毗舍离猕猴池边重阁讲堂。"

OPEN_RAJ_BAM_LIT = "如是我闻：一时，佛住王舍城竹园。"
OPEN_RAJ_BAM_MOD = "我是这样听说的：有一次，佛住在王舍城竹园。"

OPEN_VEP_LIT = "如是我闻：一时，佛住王舍城毗富罗山。"
OPEN_VEP_MOD = "我是这样听说的：有一次，佛住在王舍城毗富罗山。"

CLOSE_MH_LIT = "摩诃男欢喜随喜，作礼而去。"
CLOSE_MH_MOD = "摩诃男欢喜随喜，行礼离去。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

BEGINLESS_LIT = (
    "众生无始生死，无明所盖，爱系其颈，长夜轮转，不知苦之本际。"
)
BEGINLESS_MOD = (
    "众生无始以来生死，被无明覆盖、爱结系住脖子，长夜轮转，不知苦的本际。"
)

CUT_HAVE_LIT = "当勤精进，断除诸有，莫令增长。"
CUT_HAVE_MOD = "应当勤加精进，断除诸有，不要让它增长。"

ALAM_LIT = "是故于一切行，当生厌离；厌故离贪；离贪故解脱。"
ALAM_MOD = "所以对一切行，应当生起厌离；厌离所以离贪；离贪所以解脱。"

TATHAGATA_LIT = "如来、应、等正觉、明行足、善逝、世间解、无上士、调御丈夫、天人师、佛世尊"
TATHAGATA_MOD = "如来、应供、等正觉、明行足、善逝、世间解、无上士、调御丈夫、天人师、佛世尊"

AWAKEN_LIT = "我生已尽，梵行已立，所作已作，自知不受后有。"
AWAKEN_MOD = "我生已尽，梵行已立，所作已作，自知不受后有。"

FOUR_TRUTH_LIT = (
    "此苦圣谛如实知，此苦集圣谛如实知，此苦灭圣谛如实知，此苦灭道迹圣谛如实知"
)
FOUR_TRUTH_MOD = (
    "如实知苦圣谛，如实知苦集圣谛，如实知苦灭圣谛，如实知苦灭道迹圣谛"
)

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

# --- SA 931 住处（AN6.10 Mahānāma 六念）------------------------------------
SUTTAS["SA_931"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时释氏摩诃男来诣佛所，稽首礼足，退坐一面，白佛言："
        "「世尊！圣弟子已得果、解了教法，当常修何等念住？」",
        "佛告摩诃男：「圣弟子已得果、解了教法，当修六随念。"
        "譬如饥人羸瘦，得美食则身肥泽；如是修六随念，疾趣安隐涅槃。"
        "「何等为六？念佛：'"
        + TATHAGATA_LIT
        + "。'念时不起贪瞋痴，心正直，得义得法，随喜欢悦，身猗息，觉受乐，心得定；"
        "于凶险众生中无罣碍，入法流水，乃至涅槃。"
        "念法：世尊法律，现法离炽然，不待时节，通达现观，缘自觉知——亦复如是。"
        "念僧：世尊弟子善向、正向，四双八辈，戒定慧解脱解脱知见具足，应供良福田——亦复如是。"
        "念戒：不坏不缺、智者所赞——亦复如是。"
        "念施：于悭垢众生中得离悭处，自手施、乐捨、等施——亦复如是。"
        "念天：有四大王天乃至他化自在天；有正信、戒、施、闻、慧者命终生彼，我亦当行——亦复如是。"
        "摩诃男！圣弟子已得果者，如是多修六念，于正法律速尽诸漏，"
        "无漏心解脱、慧解脱，现法自知作证：'"
        + AWAKEN_LIT
        + "'」",
        CLOSE_MH_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时释迦族的摩诃男来到佛处，顶礼佛足，退坐一面，对佛说："
        "「世尊！圣弟子已经得果、理解了教法，应当常常修习怎样的念住？」",
        "佛告诉摩诃男：「圣弟子已经得果、理解了教法，应当修六种随念。"
        "好比饥饿消瘦的人，得到美食身体就丰润；这样修六随念，很快趋向安隐涅槃。"
        "「哪六种？念佛：'"
        + TATHAGATA_MOD
        + "。'这样念时不起贪瞋痴，心端正，得义得法，随喜欢悦，身体轻安，觉受快乐，心得到定；"
        "在凶险的众生中没有障碍，进入法的流水，直至涅槃。"
        "念法：世尊的法律，现法就能离开炽然，不等时节，现前通达，自己缘而觉知——也是这样。"
        "念僧：世尊的弟子善向、正向，四双八辈，戒定慧解脱解脱知见具足，值得供养的良福田——也是这样。"
        "念戒：不坏不缺、智者所称赞——也是这样。"
        "念施：在悭吝垢秽的众生中得到远离悭垢之处，亲手施、乐于捨、平等施——也是这样。"
        "念天：有四大王天直到他化自在天；有正信、戒、施、闻、慧的人命终生到那里，我也应当这样行——也是这样。"
        "摩诃男！圣弟子已得果的人，这样多修六念，在正法律中很快尽诸漏，"
        "无漏的心解脱、慧解脱，现法自己知道、自己作证：'"
        + AWAKEN_MOD
        + "'」",
        CLOSE_MH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN6.10；"
        "据巴利：已得果圣弟子常修六念（汉「学地求漏尽」框校正）；"
        "六念连锁随喜→猗息→乐→定；饥人得食喻从汉。"
    ),
}

# --- SA 932 十一（AN11.11）-------------------------------------------------
SUTTAS["SA_932"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时众多比丘集食堂为世尊缝衣。摩诃男闻已，念言："
        "「安居讫、作衣竟，世尊当人间游行，何时复得见世尊及诸知识比丘？」"
        "来诣佛所，白言：「我四体不摄，迷于四方，闻法悉忘。」",
        "佛告摩诃男：「见与不见世尊及知识比丘，皆当依五法，修六念。"
        "何等五？有信则成，非无信；有精进则成，非懈怠；有念则成，非失念；"
        "有定则成，非散乱；有慧则成，非无慧。"
        "依此五法，修六念处：念佛、法、僧、戒、施、天。"
        "成就此十一法，住于学迹，终不腐败，堪任知見，近于甘露；"
        "然不能一切疾得甘露涅槃。"
        "譬如伏鸡伏卵，或五或十，随时爱护；纵中间放逸，犹能啄卵生子——"
        "以初善护故。圣弟子成就十一法，亦复如是。」",
        CLOSE_MH_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时许多比丘聚集在食堂为世尊缝衣。摩诃男听说后想："
        "「安居结束、衣服做成，世尊就要人间游行，什么时候才能再见到世尊和知识比丘？」"
        "他来到佛处说：「我四肢不听使唤，辨不清方向，听过的法都忘了。」",
        "佛告诉摩诃男：「无论见不见世尊和知识比丘，都应当依五种法，修六种念。"
        "哪五种？有信才能成就，不是无信；有精进才能成就，不是懈怠；有念才能成就，不是失念；"
        "有定才能成就，不是散乱；有慧才能成就，不是无慧。"
        "依这五法，修六念处：念佛、法、僧、戒、施、天。"
        "成就这十一法，住在有学的道路上，终不会腐败，能够知見，接近甘露；"
        "但不能说一切人很快就得到甘露涅槃。"
        "好比母鸡孵蛋，或五或十，时时爱护；即使中间有些放逸，还能啄破蛋壳让小鸡出生——"
        "因为起初好好护持的缘故。圣弟子成就十一法，也是这样。」",
        CLOSE_MH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN11.11；"
        "据巴利五法＝信、精进、念、定、慧（汉「戒闻施」系校正）；"
        "五＋六念＝十一；伏鸡喻从汉／巴利。"
    ),
}

# --- SA 933 十二（AN11.12）-------------------------------------------------
SUTTAS["SA_933"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时众多比丘集食堂为世尊缝衣。摩诃男闻已，来白佛言："
        "「我四体不摄，先所闻法今悉忘失。何时复得见世尊及诸知识比丘？」",
        "佛告摩诃男：「见与不见，常当依五法，增修六随念。"
        "信、精进、念、定、慧为根本；于上修念佛乃至念天。"
        "如是十一法成就，行住坐卧、作务居家，皆应修习。"
        "彼圣弟子诸恶减退不增长，离尘不取；不取故不著，缘自涅槃：'"
        + AWAKEN_LIT
        + "'」",
        CLOSE_MH_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时许多比丘聚集在食堂为世尊缝衣。摩诃男听说后来对佛说："
        "「我四肢不听使唤，以前听过的法现在都忘了。什么时候才能再见到世尊和知识比丘？」",
        "佛告诉摩诃男：「无论见不见，都应当常常依五种法，再增修六种随念。"
        "以信、精进、念、定、慧为根本；在上面再修念佛直到念天。"
        "这样十一法成就以后，行走、站立、坐着、躺着、做事、在家，都应当修习。"
        "那样的圣弟子，种种恶会减退不增长，离尘垢、不执取；不取所以不著，自己缘于涅槃：'"
        + AWAKEN_MOD
        + "'」",
        CLOSE_MH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN11.12；"
        "据巴利：五德＋六念（汉「空」及「十二」框压缩／校正）；"
        "行住坐卧皆修从 AN；收束涅槃句从汉。"
    ),
}

# --- SA 934 解脱（AN3.73）--------------------------------------------------
SUTTAS["SA_934"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时摩诃男来白佛言：「如我解佛所说，有定故有慧，非无定。"
        "为先定而后慧耶？先慧而后定耶？为定慧一时俱生耶？」"
        "世尊默然。如是第二、第三问，佛亦默然。",
        "尊者阿难执扇侍后，念言：「摩诃男以深义问，世尊病差未久，我当余事引之。」"
        "语摩诃男：「学人亦有戒、定、慧、解脱；无学人亦有戒、定、慧、解脱。」",
        "摩诃男问其相。阿难言：「圣弟子住戒波罗提木叉，威仪具足；"
        "离欲恶不善法，乃至第四禅具足住——是学定。"
        f"如是定具足已，{FOUR_TRUTH_LIT}；"
        "如是知见已，五下分结断，得阿那含，不还此世——"
        "尔时成就学戒、学定、学慧、学解脱。"
        "复于余时尽诸有漏，无漏心解脱、慧解脱，自知作证：'"
        + AWAKEN_LIT
        + "'——尔时成就无学戒、定、慧、解脱。"
        "是名世尊所说学与无学。」",
        "摩诃男欢喜，礼佛而去。世尊知其去已，告阿难："
        "「迦毗罗卫诸释，乃能共论深义，快得善利，于甚深法贤圣慧眼而得深入。」",
        "阿难闻已，欢喜奉行。",
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时摩诃男来对佛说：「如我理解佛所说，有定才有慧，不是没有定。"
        "是先有定然后有慧呢？先有慧然后有定呢？还是定和慧同时生起呢？」"
        "世尊默然。这样问了第二、第三次，佛也默然。",
        "阿难尊者在后面拿扇子侍候，心想：「摩诃男拿很深的义理来问，世尊病刚好不久，我该用别的事把话引开。」"
        "就对摩诃男说：「有学的人也有戒、定、慧、解脱；无学的人也有戒、定、慧、解脱。」",
        "摩诃男问它们的差别。阿难说：「圣弟子安住戒波罗提木叉，威仪具足；"
        "离开欲和恶不善法，直到具足安住第四禅——这是有学的定。"
        f"这样定具足以后，{FOUR_TRUTH_MOD}；"
        "这样知见以后，五下分结断除，得到阿那含，不再还生此世——"
        "那时成就有学的戒、定、慧、解脱。"
        "又在其余时候尽诸有漏，无漏的心解脱、慧解脱，自己知道、自己作证：'"
        + AWAKEN_MOD
        + "'——那时成就无学的戒、定、慧、解脱。"
        "这就是世尊所说的有学与无学。」",
        "摩诃男欢喜，礼佛离去。世尊知道他走了，告诉阿难："
        "「迦毗罗卫的释迦族人，竟能一起讨论深义，得到很好的利益，对甚深法的贤圣慧眼能够深入。」",
        "阿难听了，欢喜奉行。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN3.73；"
        "据巴利问义＝定与慧先后（汉「正受故解脱」校正）；"
        "阿难答学／无学戒定慧解脱链从汉＋AN；佛病差未久、默然、事后赞释种从汉。"
    ),
}

# --- SA 935 含罗（SN55.23 Godhā）-------------------------------------------
SUTTAS["SA_935"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时释氏沙陀语摩诃男：「世尊说须陀洹成就几法？」"
        "答：「四法：佛、法、僧不坏净，圣戒成就。」"
        "沙陀言：「莫作是说！但三法：佛、法、僧不坏净。」再三各不相受，共诣佛所。",
        "摩诃男具白其事。沙陀从坐起，合掌白佛："
        "「若有诤论，一者世尊，一者僧众乃至天人世人——我宁随世尊，不随余众。」",
        "佛问摩诃男：「沙陀作如是论，汝当云何？」"
        "答：「我唯言善、言真实。」"
        "佛告摩诃男：「当知四法成就须陀洹：于佛、法、僧不坏净，圣戒成就。如是受持。」",
        CLOSE_MH_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时释迦族的沙陀对摩诃男说：「世尊说须陀洹成就几种法？」"
        "回答：「四种法：对佛、法、僧的不坏净，以及圣戒成就。」"
        "沙陀说：「不要这样说！只有三种：对佛、法、僧的不坏净。」再三各不相让，一起到佛那里。",
        "摩诃男把事情详细禀告。沙陀从座位起来，合掌对佛说："
        "「如果有争论，一边是世尊，一边是僧众乃至天人世人——我宁愿跟随世尊，不跟随其余众人。」",
        "佛问摩诃男：「沙陀这样议论，你怎么看？」"
        "回答：「我只说善的、真实的。」"
        "佛告诉摩诃男：「应当知道四种法成就须陀洹：对佛、法、僧的不坏净，以及圣戒成就。这样受持。」",
        CLOSE_MH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.23 Godhā；"
        "巴利 Godhā 为女众，汉作沙陀；四法须陀洹（三不坏净＋圣戒）佛所印定。"
    ),
}

# --- SA 936 麤手（SN55.24 Sarakāni）---------------------------------------
SUTTAS["SA_936"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时迦毗罗卫诸释集堂论：「世尊记百手释氏命终得须陀洹，不堕恶趣，决定正向三菩提；"
        "然彼犯戒饮酒——当往问佛。」摩诃男往白佛。",
        "佛告摩诃男：「若圣弟子长夜归依佛、法、僧，岂堕恶趣？"
        "百手释氏长夜归依三宝，云何堕恶趣？"
        "复次：于佛、法、僧有不坏净，戒具足，八解脱身证，以慧见漏尽——俱解脱，不堕恶趣。"
        "有不坏净，漏尽而不得八解脱——慧解脱。"
        "有不坏净，八解脱身证而未漏尽——身证。"
        "有不坏净，于正法律如实知見——见到。"
        "有不坏净，信解深固——信解脱。"
        "信于佛法语，于五根审谛堪忍——随法行；五根少慧堪忍——随信行。"
        "此诸人皆不堕恶趣。"
        "若此坚固树能知义与非义，我犹记说须陀洹，况百手释氏？"
        "彼临命终受持净戒，捨离饮酒，我记彼得须陀洹，究竟苦边。」",
        CLOSE_MH_LIT,
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时迦毗罗卫的释迦族人聚集议论：「世尊记说百手释氏命终得须陀洹，不堕恶趣，决定正向正觉；"
        "可是他犯戒饮酒——应当去问佛。」摩诃男前去禀告佛。",
        "佛告诉摩诃男：「如果圣弟子长夜归依佛、法、僧，怎么会堕恶趣？"
        "百手释氏长夜归依三宝，怎么会堕恶趣？"
        "再者：对佛、法、僧有不坏净，戒具足，八解脱身证，以慧见漏尽——是俱解脱，不堕恶趣。"
        "有不坏净，漏尽但不得八解脱——是慧解脱。"
        "有不坏净，八解脱身证但还未漏尽——是身证。"
        "有不坏净，对正法律如实知見——是见到。"
        "有不坏净，信解坚固——是信解脱。"
        "信佛的法语，对五根仔细忍受——是随法行；五根慧力较少也能忍受——是随信行。"
        "这些人都不会堕恶趣。"
        "假如这些坚固的大树能懂得义与非义，我还要记说它们得须陀洹，何况百手释氏？"
        "他临命终时受持净戒，捨离饮酒，我记说他得须陀洹，究竟苦边。」",
        CLOSE_MH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.24 Sarakāni；"
        "据巴利：长夜归依＋临终受学；坚固树喻；"
        "汉列俱解脱／慧解脱／身证／见到／信解脱／随法随信行阶次保留。"
    ),
}

# --- SA 937 血（SN15.13）---------------------------------------------------
SUTTAS["SA_937"] = {
    "lit": [
        OPEN_VES_LIT,
        "时有四十比丘住波梨耶聚落，皆修阿练若、粪扫衣、乞食，学人未离欲，来诣佛所。"
        "世尊念：「我当为说法，令于此生不起诸漏，心得解脱。」",
        "告诸比丘：「"
        + BEGINLESS_LIT
        + "于意云何？恒水及四大海水为多？汝等长夜轮转，身体破坏所出之血为多？」"
        "比丘白佛：「流血甚多，过于恒水及四大海。」"
        "佛言：「善哉！长夜或生象马驼驴牛犬，截耳鼻头足，血无量；"
        "或为盗贼所害，分离肢体；或弃冢间脓坏；或堕地狱、畜生、饿鬼——血出无量。」",
        "「色为常、无常？」「无常。」「无常者苦耶？」「苦。」"
        "「无常、苦、变易法，可计我、异我、相在不？」「不也。」受想行识亦如是。"
        "「一切色受想行识，非我、不异我、不相在。如是观者，于五受阴厌；"
        "厌故离贪；离贪故解脱；解脱知見：'"
        + AWAKEN_LIT
        + "'」"
        "说是法时，四十比丘不起诸漏，心得解脱。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "当时有四十位比丘住在波梨耶聚落，都修阿练若、穿粪扫衣、乞食，还是有学、未离欲，来到佛处。"
        "世尊心想：「我应当为他们说法，让他们就在这一生不起诸漏，内心解脱。」",
        "告诉比丘们：「"
        + BEGINLESS_MOD
        + "你们怎么看？恒河水和四大海水多，还是你们长夜轮转、身体破坏流出来的血多？」"
        "比丘们对佛说：「流血非常多，超过恒河水和四大海。」"
        "佛说：「很好！长夜中你们或者生为象马驼驴牛狗，耳朵鼻子头脚被砍断，血无量；"
        "或者被盗贼杀害，肢体分离；或者丢在坟间脓烂；或者堕落地狱、畜生、饿鬼——流出的血也无量。」",
        "「色是常还是无常？」「无常。」「无常的是苦吗？」「是苦。」"
        "「无常、苦、会变坏的法，还能计为我、异我、彼此相在吗？」「不能。」受想行识也是这样。"
        "「一切色受想行识，不是我、不异于我、不相在。这样观察的人，对五受阴厌离；"
        "厌离所以离贪；离贪所以解脱；解脱而有知見：'"
        + AWAKEN_MOD
        + "'」"
        "说这部法的时候，四十位比丘不起诸漏，内心解脱。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.13；"
        "汉四十比丘／毗舍离框保留（巴利三十／王舍城）；"
        "「厌已不乐」→「厌故离贪」；血多于四大海。"
    ),
}

# --- SA 938 泪（SN15.3）----------------------------------------------------
SUTTAS["SA_938"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "于意云何？恒水及四大海水为多？汝等长夜轮转，悲泣流泪为多？」"
        "比丘白佛：「流泪甚多，过于恒水及四大海。」"
        "佛言：「善哉！长夜丧失父母兄弟姊妹宗亲知识，丧失钱财，为之流泪无量；"
        "弃冢间脓血，及生地狱、畜生、饿鬼——亦复如是。」",
        "「色无常、苦、变易，不可计我。受想行识亦如是。"
        "圣弟子如是知见，于五受阴厌；厌故离贪；离贪故解脱；"
        "解脱生老病死忧悲恼苦。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "你们怎么看？恒河水和四大海水多，还是你们长夜轮转、悲伤哭泣流下的泪多？」"
        "比丘们对佛说：「流泪非常多，超过恒河水和四大海。」"
        "佛说：「很好！长夜中丧失父母兄弟姊妹宗亲朋友，丧失钱财，为此流泪无量；"
        "丢在坟间的脓血，以及生到地狱、畜生、饿鬼——也是这样。」",
        "「色是无常、苦、会变坏，不可计为我。受想行识也是这样。"
        "圣弟子这样知见，对五受阴厌离；厌离所以离贪；离贪所以解脱；"
        "解脱生老病死忧悲恼苦。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.3 Assu；"
        "泪多于四大海；与不可爱合、与可爱离；收束用厌故离贪。"
    ),
}

# --- SA 939 母乳（SN15.4）--------------------------------------------------
SUTTAS["SA_939"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "于意云何？恒水及四大海水为多？汝等长夜轮转，所饮母乳为多？」"
        "比丘白佛：「饮母乳甚多，过于恒水及四大海。」"
        "佛言：「善哉！长夜或生象驼马牛驴诸禽兽，饮母乳无量；"
        "弃冢间脓血，堕三恶趣髓血流出——亦复无量。」",
        "「色无常乃至五受阴非我、非我所；于诸世间无所取；"
        "不取故不著；厌故离贪；离贪故解脱；自知：'"
        + AWAKEN_LIT
        + "'」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "你们怎么看？恒河水和四大海水多，还是你们长夜轮转、所喝的母乳多？」"
        "比丘们对佛说：「喝的母乳非常多，超过恒河水和四大海。」"
        "佛说：「很好！长夜中或者生为象驼马牛驴等禽兽，喝母乳无量；"
        "丢在坟间的脓血，堕三恶趣髓血流出——也无量。」",
        "「色无常，一直到五受阴不是我、不是我所；对世间没有所取；"
        "不取所以不著；厌离所以离贪；离贪所以解脱；自己知道：'"
        + AWAKEN_MOD
        + "'」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.4 Khīra；"
        "母乳多于四大海；收束厌故离贪。"
    ),
}

# --- SA 940 土丸（SN15.1 草木筹数母）---------------------------------------
SUTTAS["SA_940"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "若此阎浮提一切草木，斩为四指筹，以数长夜所经之母及母之母；"
        "筹尽而母数犹不尽。"
        "如是无始生死。是故比丘当如是学：'"
        + CUT_HAVE_LIT
        + "'」"
        + ALAM_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "假如把这阎浮提一切草木，砍成四指长的筹，用来数长夜以来所经历的母亲和母亲的母亲；"
        "筹数完了，母亲的数目还数不尽。"
        "无始生死就是这样。所以比丘应当这样学：'"
        + CUT_HAVE_MOD
        + "'」"
        + ALAM_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.1 Tiṇakaṭṭha；"
        "据巴利数母／祖母（汉「父母」校正为母系）；四指筹。"
    ),
}

# --- SA 941 如豆粒（SN15.2 土丸数父）-------------------------------------
SUTTAS["SA_941"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "若此大地泥土，悉以为丸如枣核，以数长夜所经之父及父之父；"
        "土丸尽而父数犹不尽。"
        "如是无始生死。是故当勤方便：'"
        + CUT_HAVE_LIT
        + "'」"
        + ALAM_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "假如把这大地的泥土，都搓成像枣核那么大的丸，用来数长夜以来所经历的父亲和父亲的父亲；"
        "土丸尽了，父亲的数目还数不尽。"
        "无始生死就是这样。所以应当勤加方便：'"
        + CUT_HAVE_MOD
        + "'」"
        + ALAM_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.2 Pathavī；"
        "据巴利数父／祖父（汉「父母／婆罗果」作枣核丸以从 SN kolaṭṭhi）。"
    ),
}

# --- SA 942 喜乐（SN15.12）-------------------------------------------------
SUTTAS["SA_942"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "若见众生安隐喜乐，当作是念："
        "『我等长夜轮转，亦曾受如是乐，其数无量。』"
        "是故当如是学：'"
        + CUT_HAVE_LIT
        + "'」"
        + ALAM_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "如果看见众生安隐喜乐，应当这样想："
        "『我们长夜轮转，也曾受过这样的乐，次数无量。』"
        "所以应当这样学：'"
        + CUT_HAVE_MOD
        + "'」"
        + ALAM_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.12 Sukhita；"
        "见喜乐众生则念：『我亦曾尔』。"
    ),
}

# --- SA 943 苦恼（SN15.11）-------------------------------------------------
SUTTAS["SA_943"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "若见众生受诸苦恼，当作是念："
        "『我长夜轮转，亦曾更受如是之苦，其数无量。』"
        "是故当勤方便：'"
        + CUT_HAVE_LIT
        + "'」"
        + ALAM_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "如果看见众生受种种苦恼，应当这样想："
        "『我长夜轮转，也曾受过这样的苦，次数无量。』"
        "所以应当勤加方便：'"
        + CUT_HAVE_MOD
        + "'」"
        + ALAM_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.11 Duggata；"
        "见苦恼众生则念：『我亦曾尔』。"
    ),
}

# --- SA 944 恐怖（无专 SN；近 SN15 无始定型）-------------------------------
SUTTAS["SA_944"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "若见众生而生恐怖，衣毛为竖，当作是念："
        "『我等过去必曾杀生，为伤害者、为恶知识；"
        "于无始生死长夜轮转，不知苦之本际。』"
        "是故当如是学：'"
        + CUT_HAVE_LIT
        + "'」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "如果看见众生就生起恐怖，汗毛竖起，应当这样想："
        "『我们过去一定曾经杀生，做过伤害者、恶知识；"
        "在无始生死中长夜轮转，不知苦的本际。』"
        "所以应当这样学：'"
        + CUT_HAVE_MOD
        + "'」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：无专 SC 巴利平行；无始＋见生恐怖定型，参 SN15 族。"
    ),
}

# --- SA 945 彼爱（SN15.14–19 合）-------------------------------------------
SUTTAS["SA_945"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "若见众生爱念欢喜，当作是念："
        "『如是众生过去世时，必曾为我父母、兄弟、妻子、亲属、师友、知识。"
        "长夜无明所盖、爱系其颈，故轮转不知苦之本际。』"
        "是故当精勤方便：'"
        + CUT_HAVE_LIT
        + "'」"
        + ALAM_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "如果看见众生令人爱念欢喜，应当这样想："
        "『这样的众生在过去世，一定曾经是我的父母、兄弟、妻子、亲属、师友、知识。"
        "长夜被无明覆盖、爱结系住脖子，所以轮转不知苦的本际。』"
        "所以应当精勤方便：'"
        + CUT_HAVE_MOD
        + "'」"
        + ALAM_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：parallels SN15.14–19（母父兄弟姊妹子女分经）；"
        "汉合为一经『必为我等亲友』；义从巴利『不易得未曾为母等者』。"
    ),
}

# --- SA 946 恒河（SN15.8；据巴利校正汉问诸佛数）---------------------------
SUTTAS["SA_946"] = {
    "lit": [
        OPEN_RAJ_BAM_LIT,
        "时有异婆罗门来诣佛所，问讯已，退坐一面，白言："
        "「瞿昙！过去世有几劫已过？」"
        "佛告婆罗门：「过去劫甚多，不可以数计——百、千、十万劫皆难算。」"
        "婆罗门言：「可说譬不？」"
        "佛言：「可说。譬如恒河，从源至入海，中间沙粒不可数；"
        "过去已过之劫，多于彼沙，亦难可数。"
        + BEGINLESS_LIT
        + "长夜受苦，坟垄增长。是故于一切行，当生厌离；厌故离贪；离贪故解脱。」",
        "婆罗门言：「善哉瞿昙！我从今日尽寿归依佛、法、僧，为优婆塞。」",
    ],
    "mod": [
        OPEN_RAJ_BAM_MOD,
        "当时有一位婆罗门来到佛处，问讯后坐在一边，说："
        "「瞿昙！过去世有多少劫已经过去了？」"
        "佛告诉婆罗门：「过去的劫非常多，没法用数目计算——百、千、十万劫都难算。」"
        "婆罗门说：「可以打个比方吗？」"
        "佛说：「可以。好比恒河，从源头到入海，中间的沙粒数不清；"
        "过去已经过去的劫，比那些沙还多，也难计算。"
        + BEGINLESS_MOD
        + "长夜受苦，坟垄增长。所以对一切行应当厌离；厌离所以离贪；离贪所以解脱。」",
        "婆罗门说：「很好，瞿昙！我从今天起尽形寿归依佛、法、僧，做优婆塞。」",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.8 Gaṅgā；gold_reconstructed："
        "汉问未来／过去佛如恒河沙并出家得阿罗汉；"
        "据 SN15.8 校正为问过去劫数＋恒河沙喻＋归依为优婆塞。"
    ),
}

# --- SA 947 骨聚（SN15.10）-------------------------------------------------
SUTTAS["SA_947"] = {
    "lit": [
        OPEN_VEP_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "有一人于一劫中轮转生死，若骨不腐坏而积聚者，如毗富罗山。"
        f"若圣弟子{FOUR_TRUTH_LIT}，如是知见，断三结——身见、戒取、疑——"
        "得须陀洹，不堕恶趣，决定正向三菩提，七有天人往生，究竟苦边。」",
        "尔时世尊说偈："
        "「一人一劫中，积骨如山丘；\n"
        "　正智见真谛，苦集灭道迹；\n"
        "　至多经七有，究竟于苦边。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VEP_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "有一个人在一劫中轮转生死，如果骨头不腐烂而堆积起来，会像毗富罗山那样高。"
        f"如果圣弟子{FOUR_TRUTH_MOD}，这样知见，断除三结——身见、戒取、疑——"
        "得到须陀洹，不堕恶趣，决定正向正觉，最多七次往来天人，究竟苦边。」",
        "那时世尊说偈："
        "「一人一劫中，积骨如山丘；\n"
        "　正智见真谛，苦集灭道迹；\n"
        "　至多经七有，究竟于苦边。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.10；"
        "一劫骨聚如毗富罗；见四谛断三结得须陀洹；偈从汉／SN 压缩。"
    ),
}

# --- SA 948 城（SN15.6）----------------------------------------------------
SUTTAS["SA_948"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "」"
        "时有异比丘问：「劫长久如？」"
        "佛言：「我能说，汝难知。」「可说譬不？」「可说。"
        "譬如铁城，方一由旬，高亦尔，满中芥子；有人百年取一芥子，芥子尽而劫犹不竟。"
        "如是长劫，百千万亿苦相续，白骨成丘，脓血成流，三恶趣满。"
        "是故当如是学：'"
        + CUT_HAVE_LIT
        + "'」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "」"
        "当时有一位比丘问：「一劫有多久？」"
        "佛说：「我能说，你很难了知。」「可以打个比方吗？」「可以。"
        "好比一座铁城，长宽高各一由旬，里面装满芥子；有人每一百年取出一粒芥子，芥子取尽了，劫还没有结束。"
        "这样长的劫里，百千万亿的苦连续不断，白骨成丘，脓血成流，三恶趣充满。"
        "所以应当这样学：'"
        + CUT_HAVE_MOD
        + "'」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.6 Sāsapa；"
        "铁城满芥、百年一粒；劫犹不尽。"
    ),
}

# --- SA 949 山（SN15.5）----------------------------------------------------
SUTTAS["SA_949"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "」"
        "时有异比丘问：「劫长久如？」"
        "佛言：「我能说，汝难知。」「可说譬不？」「可说。"
        "如大石山，方一由旬，无缺无孔，坚固一体；"
        "有人百年以迦尸细布一拂，拂之不已，山尽而劫犹不竟。"
        "如是长劫，受诸苦恼无量。是故当如是学：'"
        + CUT_HAVE_LIT
        + "'」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "」"
        "当时有一位比丘问：「一劫有多久？」"
        "佛说：「我能说，你很难了知。」「可以打个比方吗？」「可以。"
        "好比一座大石山，长宽高各一由旬，没有缺口、没有孔洞，坚固成一块；"
        "有人每一百年用迦尸国的细布拂拭一次，不停地拂，山磨尽了，劫还没有结束。"
        "这样长的劫里，所受苦恼无量。所以应当这样学：'"
        + CUT_HAVE_MOD
        + "'」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.5 Pabbata；"
        "大石山＋迦尸细布百年一拂；劫犹不尽。"
    ),
}

# --- SA 950 过去（SN15.7）--------------------------------------------------
SUTTAS["SA_950"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「"
        + BEGINLESS_LIT
        + "」"
        "时有异比丘问：「过去有几劫？」"
        "佛言：「甚多难知。」「可说譬不？」「可说。"
        "譬如有四弟子，寿命百岁；日日各忆念十万劫。"
        "如是百年命终，所忆犹不尽过去劫数边际。"
        "过去无量劫中，长夜受苦，积骨成山，髓血成流，及堕三恶趣。"
        "是故当如是学：'"
        + CUT_HAVE_LIT
        + "'」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「"
        + BEGINLESS_MOD
        + "」"
        "当时有一位比丘问：「过去有多少劫？」"
        "佛说：「非常多，很难了知。」「可以打个比方吗？」「可以。"
        "好比有四位弟子，寿命一百岁；每天各自忆念十万劫。"
        "这样到百年命终，所忆念的还不能穷尽过去劫数的边际。"
        "在过去无量劫中，长夜受苦，积骨成山，髓血成流，以及堕三恶趣。"
        "所以应当这样学：'"
        + CUT_HAVE_MOD
        + "'」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN15.7；"
        "据巴利四弟子日日各忆十万劫（汉「一人晨午暮各三十万」校正）。"
    ),
}

# ---------------------------------------------------------------------------
# Confidence / reconstruction / build GOLD
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_931": "high",
    "SA_932": "high",
    "SA_933": "high",
    "SA_934": "high",
    "SA_935": "high",
    "SA_936": "high",
    "SA_937": "high",
    "SA_938": "high",
    "SA_939": "high",
    "SA_940": "high",
    "SA_941": "high",
    "SA_942": "high",
    "SA_943": "high",
    "SA_944": "medium",
    "SA_945": "high",
    "SA_946": "high",
    "SA_947": "high",
    "SA_948": "high",
    "SA_949": "high",
    "SA_950": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_946": (
        "汉问未来／过去佛如恒河沙并出家证阿罗汉；"
        "据 SN15.8 校正为问过去劫数、恒河沙喻、归依为优婆塞。"
    ),
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

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

assert set(GOLD) == {f"SA_{i}" for i in range(931, 951)}, (
    "GOLD must cover SA_931–SA_950 exactly"
)
assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
assert set(RECONSTRUCTED) <= set(GOLD)
assert "SA_930" not in GOLD and not any(f"SA_{i}" in GOLD for i in range(951, 971))


def main() -> None:
    aligned = ROOT / "data" / "aligned" / "raw_aligned_data.json"
    out = ROOT / "data" / "translated" / "final_translated_data.json"
    gold_dir = ROOT / "data" / "golden"
    gold_dir.mkdir(parents=True, exist_ok=True)

    if out.exists():
        records = json.loads(out.read_text(encoding="utf-8"))
    else:
        records = json.loads(aligned.read_text(encoding="utf-8"))

    # Boundary: SA_930 must remain untouched
    boundary_id = "SA_930"
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
    assert boundary_before is not None, "SA_930 must exist for boundary assert"

    # Snapshot SA_951+ in range that might be adjacent
    after_before = {
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
        if rec["id"] in {f"SA_{i}" for i in range(951, 971)}
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
        if rec["id"] == boundary_id:
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

    for rid, before in after_before.items():
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
                assert before == after, f"{rid} (SA_951+) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa931-950.json").write_text(
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
    continuous_931_950 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(931, 951)
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_931–SA_950 only)")
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
    print(f"continuous_gold_SA_931–950={continuous_931_950}")
    print("SA_930_untouched=True")
    print("SA_951+_untouched=True")
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
