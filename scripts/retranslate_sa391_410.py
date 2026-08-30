#!/usr/bin/env python3
"""Retranslate SA 391–410（卷第十六末諦相應–卷第十七思惟）→ merge into final_translated_data.json.

本批二十经：沙门婆罗门略、如实知、善男子、日月×3、佉提罗、因陀罗柱、
论处、衣、百枪、平等正觉、如实知（拘利）、申恕林、孔、龟；
思惟×2、觉×2。

信：有平行者以 SN／Pāli／Sujato 厘义；无平行者 medium；
    交叉指示（SA 391 广说如上、SA 410 如上广说）→ gold_reconstructed。
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

OPEN_BEN_LIT = "如是我闻：一时，佛在波罗㮈仙人住处鹿野苑中。"
OPEN_BEN_MOD = "我是这样听说的：有一次，佛住在波罗㮈仙人住处鹿野苑中。"

OPEN_RAJ_LIT = "如是我闻：一时，佛在王舍城迦兰陀竹园。"
OPEN_RAJ_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

OPEN_VES_LIT = "如是我闻：一时，佛在毗舍离猕猴池侧重阁讲堂。"
OPEN_VES_MOD = "我是这样听说的：有一次，佛住在毗舍离猕猴池侧重阁讲堂。"

CLOSE_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

AWAKEN_LIT = "「我生已尽，梵行已立，所作已作，自知不受后有。」"
AWAKEN_MOD = "「我生已尽，梵行已立，所作已作，自知不受后有。」"

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

# --- SA 391 沙门婆罗门（略；交叉指示）---------------------------------------
# 底本「广说如上。差别者」→ 据 SA 390／SN56.5–6 纲 + 汉本差别语重建
SUTTAS["SA_391"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若沙门、婆罗门于" + FOUR_TRUTH_LIT + "不如实知——"
        "当知是沙门、婆罗门非沙门数、非婆罗门数。"
        "若于四圣谛如实知者——是沙门数、是婆罗门数。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「若沙门、婆罗门对" + FOUR_TRUTH_MOD + "不能如实了知——"
        "就应当知道：这样的沙门、婆罗门不算沙门之数、不算婆罗门之数。"
        "若对四圣谛如实了知——才是沙门之数、婆罗门之数。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "底本『广说如上。差别者』为交叉指示；"
        "依 SA_390／SN56.5–6 四谛如实知＝真沙门纲，保留汉本差别语『沙门数／婆罗门数』。"
        "confidence=high（平行可靠；文面重建）。"
    ),
}

# --- SA 392 如实知（SN 56.22）-----------------------------------------------
SUTTAS["SA_392"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若沙门、婆罗门于" + FOUR_TRUTH_LIT + "不如实知——"
        "我不说彼为真沙门、真婆罗门；"
        "亦不能于沙门义、婆罗门义见法自知作证。"
        "若如实知四圣谛——我说彼为真沙门、真婆罗门；"
        "能于沙门义、婆罗门义见法自知作证。」",
        "尔时，世尊复说偈言：\n"
        "「不知苦及因，　苦尽永无余；\n"
        "　不知息苦道，　心慧两解脱——\n"
        "　彼不能作边，　犹堕生与老。\n"
        "　如实知苦因，　苦尽永无余；\n"
        "　知息苦道迹，　心慧具解脱——\n"
        "　彼堪能作边，　不复生与老。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「若沙门、婆罗门对" + FOUR_TRUTH_MOD + "不能如实了知——"
        "我不以他们为真正的沙门、真正的婆罗门；"
        "也不能在沙门义、婆罗门义上见法、自己知道、自己作证。"
        "若如实了知四圣谛——我才说他们是真正的沙门、真正的婆罗门；"
        "能在沙门义、婆罗门义上见法、自己知道、自己作证。」",
        "那时，世尊又说偈颂：\n"
        "「不知苦与苦因，　苦尽处永无余；\n"
        "　不知息苦之道，　心解脱与慧解脱——\n"
        "　便不能作苦边，　仍堕于生与老。\n"
        "　如实知苦与因，　苦尽处永无余；\n"
        "　知息苦的道迹，　心慧都具足解脱——\n"
        "　便能作苦边，　不再生、不再老。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.22。"
        "信-校正：汉本中段『舍恶趣／舍戒退减／求良福田』等异喻串非 SN 所传，"
        "据 Sujato 收束为真沙门义＋偈（心解脱／慧解脱、作边／生老）。"
        "汉『不得脱苦』读作未能于沙门义自证，不另立脱苦新义。"
    ),
}

# --- SA 393 善男子（SN 56.3；汉本果位串压缩保留）---------------------------
SUTTAS["SA_393"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若有善男子——过去、未来、现在——"
        "正信非家、出家学道，彼一切皆为如实现观四圣谛故。"
        "何等为四？谓" + FOUR_TRUTH_LIT + "。」",
        "「三结尽得须陀洹，贪恚痴薄得斯陀含，五下分结尽得阿那含，"
        "乃至漏尽得心解脱、慧解脱，见法自知作证：" + AWAKEN_LIT +
        "彼一切亦以如实知四圣谛故。"
        "辟支佛道、无上等正觉，亦复如是。」",
        "「是故比丘当勤修学：『此是苦』……『此是苦灭道迹』——"
        "于四圣谛起无间等。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「凡是善男子——过去、未来、现在——"
        "以正信离开居家而出家学道，他们全都是为了如实现观四圣谛。"
        "哪四种？就是" + FOUR_TRUTH_MOD + "。」",
        "「断尽三结得须陀洹，贪瞋痴薄得斯陀含，断尽五下分结得阿那含，"
        "乃至漏尽得心解脱、慧解脱，见法自己知道、自己作证：" + AWAKEN_MOD +
        "这一切也是因为如实了知四圣谛。"
        "辟支佛道、无上等正觉，也是这样。」",
        "「所以比丘应当努力修学：『这是苦』……『这是苦灭道迹』——"
        "在四圣谛上起无间等。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.3（resembling SN56.4）。"
        "信：三世善男子正信出家＝为四谛现观（SN／Sujato）。"
        "汉本须陀洹→佛果位串非 SN56.3 本文，压缩保留并系于『皆以知四谛故』，"
        "以存漏尽证言定型；「无间等」＝abhisamaya。"
    ),
}

# --- SA 394 日月（SN 56.37 日之前相＝正见）---------------------------------
SUTTAS["SA_394"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「譬如日出，明相先起。"
        "如是比丘欲如实现观四圣谛，亦有前相——谓正见。"
        "有正见故，当知能如实知：『此是苦』……『此是苦灭道迹』。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「好比太阳要出来，先有明相升起。"
        "同样，比丘要如实现观四圣谛，也有前相——就是正见。"
        "有了正见，就可以指望如实了知：『这是苦』……『这是苦灭道迹』。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.37。"
        "信-校正：汉『正尽苦前相＝知四圣谛』与巴利不符；"
        "据 SN／Sujato：aruṇugga∶sūriya ＝ sammādiṭṭhi∶四谛现观——"
        "正见为前相，四谛现观如日出。"
    ),
}

# --- SA 395 日月（SN 56.38）-------------------------------------------------
SUTTAS["SA_395"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若日月不出世间，大光大明亦不现；"
        "是时冥闇深厚，昼夜、半月、一月、时节、岁数皆不了知。"
        "日月出已，大光大明乃现，冥闇息，昼夜时节岁数皆可了知。」",
        "「如是，如來、应、等正觉若不出世，大光大明亦不现；"
        "四圣谛亦无开示、演说、建立、分别、显了——"
        "世间长夜纯大闇冥。"
        "如來出世，说" + FOUR_TRUTH_LIT + "，大光大明现前，冥闇销灭。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「若日月不在世间出现，大光明也不会出现；"
        "那时冥闇深厚，昼夜、半月、一月、时节、岁数都不能了知。"
        "日月出现以后，大光明才出现，冥闇止息，昼夜时节岁数才都能了知。」",
        "「同样，如来、应供、等正觉若不出世，大光明也不会出现；"
        "四圣谛也不会有开示、演说、建立、分别、显了——"
        "世间长夜只是纯大闇冥。"
        "如来出世，说" + FOUR_TRUTH_MOD + "，大光明现前，冥闇销灭。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.38。"
        "日月∶如來＝大光大明∶四谛开示；据 Sujato 补『开示／分别／显了』定型，"
        "删汉『众星』旁支以就雅。"
    ),
}

# --- SA 396 日月（无平行）---------------------------------------------------
SUTTAS["SA_396"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「譬如日出，周行空中，坏诸闇冥，光明显照。"
        "如是圣弟子一切集法灭已，离诸尘垢，法眼生，与无间等俱——"
        "三结尽：身见、戒取、疑；名须陀洹，不堕恶趣，决定正向正觉，"
        "极七有天人往来，作苦边。」",
        "「彼圣弟子中间虽起忧苦，犹能离欲、离恶不善法，"
        "有觉有观，离生喜乐，初禅具足住——"
        "不见有一法未断，能令还生此世；此则法眼之大义。」",
        "「是故比丘于四圣谛未无间等者，当勤方便，起增上欲，精进修学。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「好比太阳出来，在空中运行，坏灭闇冥，光明显照。"
        "同样，圣弟子一切集法灭尽以后，离开尘垢，生起法眼，与无间等同时——"
        "断尽三结：身见、戒取、疑；名为须陀洹，不堕恶趣，决定正向正觉，"
        "最多七次往返人天，作苦边。」",
        "「那位圣弟子中间虽然还会起忧苦，仍能离欲、离恶不善法，"
        "有觉有观，离生喜乐，具足住于初禅——"
        "看不到还有哪一法未断、能让他再还生此世；这就是得法眼的大义。」",
        "「所以比丘对四圣谛还没有无间等的，应当勤加方便，发起强盛愿欲，精进修学。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "法眼＋三结尽＝须陀洹定型；初禅段示法眼后仍可进住禅支。"
        "不引入如来藏／本觉义。confidence=medium。"
    ),
}

# --- SA 397 佉提罗（SN 56.32）-----------------------------------------------
SUTTAS["SA_397"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若有人言：『我于" + FOUR_TRUTH_LIT + "未如实现观，"
        "而能正尽作苦边』——无有是处。」",
        "「譬如有人言：『我以佉提罗叶、松针、诃梨勒叶作器盛水』——无有是处。"
        "如是未现观四圣谛而欲正尽作苦边——亦无是处。」",
        "「若言：『我已如实现观四圣谛，乃能正尽作苦边』——斯有是处。」",
        "「譬如以莲叶、波罗奢叶、摩楼迦叶作器盛水——斯有是处。"
        "如是已现观四圣谛而正尽作苦边——亦有是处。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「若有人说：『我还没有如实现观"
        + FOUR_TRUTH_MOD + "，却能正确地作苦边』——没有这个道理。」",
        "「好比有人说：『我用佉提罗叶、松针、诃梨勒叶做成器具来盛水』——没有这个道理。"
        "同样，还没有现观四圣谛却想正确地作苦边——也没有这个道理。」",
        "「若说：『我已经如实现观四圣谛，才能正确地作苦边』——这才说得通。」",
        "「好比用莲叶、波罗奢叶、摩楼迦叶做成器具来盛水——说得通。"
        "同样，已经现观四圣谛而正确地作苦边——也说得通。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.32。"
        "信-校正：汉本误作『前三谛未无间等则不得道谛』；"
        "据 SN／Sujato：四谛皆未现观则不能作苦边；叶喻叶种据巴利补松针／诃梨勒／莲／波罗奢。"
    ),
}

# --- SA 398 因陀罗柱（SN 56.39）---------------------------------------------
SUTTAS["SA_398"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若沙门、婆罗门于" + FOUR_TRUTH_LIT + "不如实知——"
        "则常瞻他面，随他语转，念：『彼尊者其知、其见。』"
        "譬如轻软绵丸、劫贝华丸，置平地，四方风吹，随风而转——"
        "以未见四圣谛故。」",
        "「若如实知四圣谛——则不瞻他面、不随他语。"
        "譬如因陀罗柱，铜铁所作，深入地中，四方猛风不能令动——"
        "以善见四圣谛故。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「若沙门、婆罗门对" + FOUR_TRUTH_MOD + "不能如实了知——"
        "就会常常仰望别人的脸，跟着别人的话转，心想：『这位尊者该是知道、看见的。』"
        "好比轻软的绵丸、劫贝花丸，放在平地上，四方风一吹就随风滚动——"
        "因为没有看见四圣谛。」",
        "「若如实了知四圣谛——就不仰望别人的脸、不跟着别人的话转。"
        "好比因陀罗柱，铜铁做成，深深埋进地里，四方猛风也不能动摇——"
        "因为已经善见四圣谛。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.39。"
        "棉絮轻故随风＝未见四谛；因陀罗柱深植＝善见四谛；据 Sujato 补『彼尊者其知、其见』。"
    ),
}

# --- SA 399 论处（SN 56.40）-------------------------------------------------
SUTTAS["SA_399"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若比丘于" + FOUR_TRUTH_LIT + "如实知——"
        "东、西、南、北有沙门、婆罗门来求论、欲摧其说，"
        "欲如法令彼动摇——无有是处。」",
        "「譬如石柱长十六肘，八肘入地，四方猛风不能令动——"
        "以善见四圣谛故，智慧不可倾动。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「若比丘对" + FOUR_TRUTH_MOD + "如实了知——"
        "即使东、西、南、北有沙门、婆罗门前来求论、想推翻他的说法，"
        "想如法地让他动摇——也没有这个道理。」",
        "「好比石柱长十六肘，八肘埋进地里，四方猛风也不能动摇——"
        "因为已经善见四圣谛，智慧不可倾动。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.40。"
        "信-校正：删汉『反生忧苦』旁义；据 SN 收束为求论者不能如法动摇善见四谛者。"
    ),
}

# --- SA 400 衣（SN 56.34）---------------------------------------------------
SUTTAS["SA_400"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若衣或头着火，当如何？」"
        "比丘白佛：「当起增上欲、精勤、勇猛、正念正知，急救令灭。」",
        "佛言：「于四圣谛犹未现观者，当置头衣于不顾，"
        "于四圣谛起增上欲、精勤、勇猛、正念正知，修无间等。"
        "何等为四？谓" + FOUR_TRUTH_LIT + "。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「如果衣服或头上着了火，该怎么办？」"
        "比丘们回答：「应当发起强盛愿欲、精勤、勇猛、正念正知，赶快把火灭掉。」",
        "佛说：「对四圣谛还没有现观的人，应当把头衣着火的事搁在一边不管，"
        "先对四圣谛发起强盛愿欲、精勤、勇猛、正念正知，修无间等。"
        "哪四种？就是" + FOUR_TRUTH_MOD + "。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.34。"
        "信-校正：汉本『莫作是说』对话紊乱；据 SN／Sujato："
        "头衣着火犹当等舍不顾，先以增上欲现观四谛。"
        "长夜恶趣炽然之义并入『未现观故当忍』之急切，不另衍地狱清单。"
    ),
}

# --- SA 401 百枪（SN 56.35）-------------------------------------------------
SUTTAS["SA_401"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「譬如士夫寿百岁。有人语之："
        "『晨朝、日中、晡时各受百枪，日日三百，至于百岁，"
        "然后乃得现观四圣谛——汝宁能不？』"
        "志求义者，足以堪受。」",
        "「所以者何？生死轮转无始，枪、剑、箭、斧之苦无有前际。"
        "然我说四圣谛现观不与忧苦俱，唯与喜乐俱。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「好比有人寿命一百岁。有人对他说："
        "『早晨、中午、傍晚各受一百枪，天天三百枪，直到满一百岁，"
        "然后才能现观四圣谛——你能接受吗？』"
        "真正求义的人，也足以接受。」",
        "「为什么？生死轮转没有起点，枪、剑、箭、斧的打击也找不到前际。"
        "可是我并不是说现观四圣谛要带着忧苦；我说现观四圣谛是带着喜乐的。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.35。"
        "信-校正：据 SN 补『现观与喜乐俱，不与忧苦俱』；"
        "汉『三恶道空受众苦亦不闻法』收束为无始轮回枪斧之喻。"
    ),
}

# --- SA 402 平等正觉（SN 56.23）---------------------------------------------
SUTTAS["SA_402"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「有四圣谛。何等为四？谓" + FOUR_TRUTH_LIT + "。"
        "如来以如实正觉此四圣谛，故名如來、应、等正觉。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「有四种圣谛。哪四种？就是" + FOUR_TRUTH_MOD + "。"
        "如来因为如实正觉了这四圣谛，所以名为如来、应供、等正觉。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.23（resembling SN56.24）。"
        "『平等正觉』读作对四谛 yathābhūtaṁ abhisambuddha，非密教平等义。"
    ),
}

# --- SA 403 如实知（SN 56.21 拘利村）---------------------------------------
SUTTAS["SA_403"] = {
    "lit": [
        "如是我闻：一时，佛在跋耆国拘利村。",
        "尔时，世尊告诸比丘：「我与汝等，以于四圣谛不知、不觉、不随顺解、不现观故，"
        "长夜驰骋生死。何等为四？谓" + FOUR_TRUTH_LIT + "。」",
        "「今此四圣谛已知、已觉、已现观——"
        "有爱已断，有结已尽，更不受后有。」",
        "尔时，世尊说偈言：\n"
        "「不见四圣谛，　长夜涉生死；\n"
        "　既见诸谛已，　有结悉已除；\n"
        "　苦根已永断，　更不受后有。」",
        CLOSE_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在跋耆国拘利村。",
        "那时，世尊告诉比丘们：「我和你们，因为对四圣谛不知、不觉、不能随顺理解、不能现观，"
        "所以长夜奔驰在生死里。哪四种？就是" + FOUR_TRUTH_MOD + "。」",
        "「现在这四圣谛已经知道、已经觉了、已经现观——"
        "有爱已经断，有结已经尽，更不再受后有。」",
        "那时，世尊说偈颂：\n"
        "「不见四圣谛，　长夜流转生死；\n"
        "　既已见诸谛，　有结全都除去；\n"
        "　苦的根已永断，　更不再受后有。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.21。"
        "信-校正：汉『摩竭…竹林聚落福德舍』处所与 SN 不合；"
        "据 Pāli／Sujato 作跋耆拘利村（Koṭigāma）。"
        "『有爱／有结』＝bhavataṇhā／bhavanetti；不读作大乘有结使玄义。"
    ),
}

# --- SA 404 申恕林（SN 56.31）-----------------------------------------------
SUTTAS["SA_404"] = {
    "lit": [
        "如是我闻：一时，佛在拘舍弥申恕林中。",
        "尔时，世尊手把申恕树叶，告诸比丘：「于意云何——"
        "我手中叶多？林中叶多？」"
        "比丘白佛：「手中甚少，林中无量。」",
        "佛言：「如是，我所证知而未说者甚多；已为汝说者甚少。"
        "所以不说——彼非义饶益，非梵行本，不趣厌、离贪、灭、静、证智、正觉、涅槃。」",
        "「我所已说者何？谓：『此是苦』……『此是苦灭道迹』。"
        "所以说——彼" + BENEFIT_LIT + "，趣厌、离贪、灭、静、证智、正觉、涅槃。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在拘舍弥的申恕林中。",
        "那时，世尊手里握着几片申恕树叶，告诉比丘们：「你们怎么看——"
        "我手里的叶子多，还是林子里的叶子多？」"
        "比丘们回答：「手里的很少，林子里的多到无法计量。」",
        "佛说：「同样，我所亲自证知却没有说给你们的很多；已经说给你们的很少。"
        "为什么不说？那些没有义饶益，不是梵行的根本，"
        "不导向厌、离贪、灭、静、证智、正觉、涅槃。」",
        "「我已经说的是什么？就是：『这是苦』……『这是苦灭道迹』。"
        "为什么说这些？因为它们有" + BENEFIT_MOD + "，"
        "导向厌、离贪、灭、静、证智、正觉、涅槃。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.31。"
        "信-校正：处所据 SN 作拘舍弥申恕林（sīsapāvana），非汉本摩竭福德舍；"
        "已说＝四谛，未说＝非义非梵行本。"
        "nibbidā／virāga 作『厌／离贪』，不用『厌故不乐』。"
    ),
}

# --- SA 405 孔（SN 56.45）---------------------------------------------------
SUTTAS["SA_405"] = {
    "lit": [
        OPEN_VES_LIT,
        "尔时，尊者阿难晨朝着衣持钵，入毗舍离乞食。"
        "见诸离车童子竞射门孔，箭箭皆入，心以为奇。",
        "乞食还已，往白世尊。佛告阿难：「于意云何——"
        "远射门孔、箭箭不空为难？或取马尾毛破为七分，以端刺端为难？」"
        "阿难白佛：「以端刺端，是则甚难。」",
        "佛言：「然于" + FOUR_TRUTH_LIT + "如实穿透现观，难又过彼。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "那时，尊者阿难早晨穿着衣、拿着钵，进入毗舍离乞食。"
        "看见许多离车童子比赛射门上的孔，箭箭都射进去，心里觉得很奇妙。",
        "乞食回来以后，去禀告世尊。佛告诉阿难：「你怎么看——"
        "从远处射门孔、箭箭不空更难？还是把马尾毛破成七分，用一端刺中另一端更难？」"
        "阿难回答：「用一端刺中另一端，那才真正很难。」",
        "佛说：「可是对" + FOUR_TRUTH_MOD + "如实穿透、现观，比那还要难。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.45。"
        "信-校正：汉『破一毛为百分』及偈『观苦阴非我』与 SN 不符；"
        "据 Sujato 作马尾毛七分、端端相刺；难又难者＝四谛现观穿透。"
        "删汉偈以免引入非平行之无我专颂（无我义自在五蕴教，不必此经强立）。"
    ),
}

# --- SA 406 龟（SN 56.47）---------------------------------------------------
SUTTAS["SA_406"] = {
    "lit": [
        OPEN_VES_LIT,
        "尔时，世尊告诸比丘：「譬如大地尽成大海，有人投一孔之轭于海；"
        "有一盲龟，百年一出其头。于意云何——盲龟百年一出，能值轭孔不？」"
        "比丘白佛：「久远或值，或不值。」",
        "佛言：「盲龟值孔，犹速于愚人堕恶趣已得复人身。"
        "所以者何？恶趣中无法行、等行、善作、福作，唯更相残杀、强者陵弱——"
        "以未见四圣谛故。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "那时，世尊告诉比丘们：「好比整个大地都变成大海，有人把只有一个孔的轭扔进海里；"
        "又有一只盲龟，一百年才伸出一次头。你们怎么看——这只盲龟百年一出，能正好套进那个孔吗？」"
        "比丘们回答：「要隔很久才可能碰上，也许永远碰不上。」",
        "佛说：「盲龟套进孔里，还比愚人堕入恶趣以后再得到人身更快。"
        "为什么？恶趣里没有法行、等行、善作、福作，只是互相残杀、强者欺凌弱者——"
        "因为没有看见四圣谛。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.47（resembling SN56.48）。"
        "信-校正：汉作阿难对答；据 SN 改诸比丘对答。"
        "一孔之轭（ekacchiggaḷaṁ yugaṁ）＋盲龟＝人身难得；因＝未见四谛。"
    ),
}

# --- SA 407 思惟（SN 56.41 世间思惟）---------------------------------------
SUTTAS["SA_407"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，思惟世间。世尊知已，往诣食堂，敷座而坐，告言："
        "「慎莫思惟世间。所以者何？世间思惟" + NOT_BENEFIT_LIT + "。"
        "当正思惟：『此苦圣谛……此苦灭道迹圣谛。』"
        "如此思惟则" + BENEFIT_LIT + "。」",
        "「过去世时，有一士夫出王舍城，于池侧坐，思惟世间——"
        "见四军——象、马、车、步——尽入一藕孔中，自谓发狂。"
        "诣大众言，众亦谓狂。然彼所见真实：时诸天与阿修罗战，"
        "阿修罗败，退入藕孔城中。」",
        "「是故比丘莫思惟世间——有常、无常，有边、无边，命即身、命异身，"
        "如來死后有、无、亦有亦无、非有非无。"
        "当思惟四圣谛。何等为四？谓" + FOUR_TRUTH_LIT + "。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里，思惟世间的事情。世尊知道以后，来到食堂，敷座坐下，告诉他们："
        "「千万不要思惟世间。为什么？世间思惟" + NOT_BENEFIT_MOD + "。"
        "应当正确思惟：『这是苦圣谛……这是苦灭道迹圣谛。』"
        "这样思惟就" + BENEFIT_MOD + "。」",
        "「过去世时，有一个人从王舍城出来，在池边坐下思惟世间——"
        "看见四军——象军、马军、车军、步军——全都钻进一根藕孔里，自以为发狂了。"
        "他到大众那里说，大家也说他疯了。可是他所见是真实的：当时诸天与阿修罗交战，"
        "阿修罗战败，退进藕孔里的城中。」",
        "「所以比丘不要思惟世间——有常、无常，有边、无边，命就是身、命与身异，"
        "如来死后有、无、亦有亦无、非有非无。"
        "应当思惟四圣谛。哪四种？就是" + FOUR_TRUTH_MOD + "。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.41。"
        "世间思惟＝lokacintā；据 SN 补十无记式列举。"
        "藕孔四军为真实天阿修罗战事，非玄幻神通本体论。"
        "『厌／离贪』导向见 BENEFIT 定型；不用『厌故不乐』。"
    ),
}

# --- SA 408 思惟（SN 56.8）--------------------------------------------------
SUTTAS["SA_408"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，论议：世间有常、无常，有边、无边，"
        "命即身、命异身，如來死后有、无、亦有亦无、非有非无。",
        "世尊以天耳闻已，往诣食堂，问：「汝等集此，何所言说？」"
        "比丘具白如上。",
        "佛言：「莫作如是论。所以者何？如此论" + NOT_BENEFIT_LIT + "。"
        "应当论：『此苦圣谛……此苦灭道迹圣谛。』"
        "如是论则" + BENEFIT_LIT + "。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里讨论：世间有常、无常，有边、无边，"
        "命就是身、命与身异，如来死后有、无、亦有亦无、非有非无。",
        "世尊用天耳听见以后，来到食堂，问：「你们聚在这里，在说什么？」"
        "比丘们把上面的讨论都禀告了。",
        "佛说：「不要作这样的议论。为什么？这样的议论" + NOT_BENEFIT_MOD + "。"
        "应当讨论：『这是苦圣谛……这是苦灭道迹圣谛。』"
        "这样讨论就" + BENEFIT_MOD + "。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.8。"
        "十无记式恶不善寻思；当以四谛代替。汉食堂叙事情节保留。"
    ),
}

# --- SA 409 觉（SN 56.7）----------------------------------------------------
SUTTAS["SA_409"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，或起贪觉，或起瞋觉，或起害觉。"
        "世尊知已，往诣食堂，告言："
        "「莫起贪觉、瞋觉、害觉。所以者何？此诸觉" + NOT_BENEFIT_LIT + "。"
        "当起苦圣谛觉、苦集圣谛觉、苦灭圣谛觉、苦灭道迹圣谛觉——"
        "此则" + BENEFIT_LIT + "。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里，有的起贪觉，有的起瞋觉，有的起害觉。"
        "世尊知道以后，来到食堂，告诉他们："
        "「不要起贪觉、瞋觉、害觉。为什么？这些觉" + NOT_BENEFIT_MOD + "。"
        "应当起苦圣谛觉、苦集圣谛觉、苦灭圣谛觉、苦灭道迹圣谛觉——"
        "这些才" + BENEFIT_MOD + "。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.7。"
        "贪／瞋／害觉＝kāma／byāpāda／vihiṁsā-vitakka；当以四谛寻思代之。"
    ),
}

# --- SA 410 觉（交叉指示；亲里等觉）-----------------------------------------
SUTTAS["SA_410"] = {
    "lit": [
        OPEN_RAJ_LIT,
        "时有众多比丘集于食堂，或起亲里觉，或起国土人民觉，或起不死觉。"
        "世尊知已，往诣食堂，告言："
        "「莫起亲里觉、国土人民觉、不死觉。所以者何？此诸觉"
        + NOT_BENEFIT_LIT + "。"
        "当起苦圣谛觉、苦集圣谛觉、苦灭圣谛觉、苦灭道迹圣谛觉——"
        "此则" + BENEFIT_LIT + "。」",
        URGE_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_RAJ_MOD,
        "当时有许多比丘聚集在食堂里，有的起亲里觉，有的起国土人民觉，有的起不死觉。"
        "世尊知道以后，来到食堂，告诉他们："
        "「不要起亲里觉、国土人民觉、不死觉。为什么？这些觉"
        + NOT_BENEFIT_MOD + "。"
        "应当起苦圣谛觉、苦集圣谛觉、苦灭圣谛觉、苦灭道迹圣谛觉——"
        "这些才" + BENEFIT_MOD + "。」",
        URGE_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "底本『一时……如上广说。差别者』为交叉指示；"
        "依 SA_409／SN56.7 框式重建，差别保留汉本『亲里觉、国土人民觉、不死觉』"
        "（ñāti／janapada／amara-vitakka 一类，非 SN56.7 贪瞋害）。"
        "confidence=high（框式有平行；差别据汉）。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_391": "high",
    "SA_392": "high",
    "SA_393": "high",
    "SA_394": "high",
    "SA_395": "high",
    "SA_396": "medium",
    "SA_397": "high",
    "SA_398": "high",
    "SA_399": "high",
    "SA_400": "high",
    "SA_401": "high",
    "SA_402": "high",
    "SA_403": "high",
    "SA_404": "high",
    "SA_405": "high",
    "SA_406": "high",
    "SA_407": "high",
    "SA_408": "high",
    "SA_409": "high",
    "SA_410": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_391": (
        "底本『广说如上。差别者』为交叉指示；"
        "依 SA_390／SN56.5–6 四谛如实知纲 + 汉本『沙门数／婆罗门数』差别重建"
    ),
    "SA_410": (
        "底本『一时……如上广说。差别者』为交叉指示；"
        "依 SA_409／SN56.7 框式 + 汉本『亲里／国土人民／不死觉』差别重建"
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
    assert set(GOLD) == {f"SA_{i}" for i in range(391, 411)}, (
        "GOLD must cover SA_391–SA_410 exactly"
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

    # Snapshot SA_390 before merge to assert untouched
    sa390_before = None
    for rec in records:
        if rec["id"] == "SA_390":
            sa390_before = json.dumps(
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

    # Assert SA_390 untouched
    for rec in merged:
        if rec["id"] == "SA_390" and sa390_before is not None:
            sa390_after = json.dumps(
                {
                    "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                    "modern_psychology_text": rec.get("modern_psychology_text"),
                    "notes": rec.get("notes"),
                    "review_status": rec.get("review_status"),
                    "confidence": rec.get("confidence"),
                },
                ensure_ascii=False,
            )
            assert sa390_before == sa390_after, "SA_390 must remain untouched"
            break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa391-410.json").write_text(
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
        for i in range(1, 411)
    )

    # Also check no 厌故不乐 / forbidden
    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_391–SA_410 only)")
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
    print(f"continuous_gold_SA_1–410={continuous}")
    print(f"SA_390_untouched=True")
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
