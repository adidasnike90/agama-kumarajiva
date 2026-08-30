#!/usr/bin/env python3
"""Retranslate SA 371–390（卷第十六 食相應末–諦相應初）→ merge into final_translated_data.json.

本批二十经：食、颇求那、子肉、有贪×5；转法轮、四圣谛×2、当知、已知、
漏尽、边际、无有关键×2、五支六分、大医王、沙门婆罗门。

信：有平行者以 SN／Pāli／Sujato 厘义；无平行者 medium；
    交叉指示（SA 373 须深矛喻、SA 376 如前广说）→ gold_reconstructed。
达：白话与罗什风逐段对照，段数严格相同。
雅：长文（≥400 字）sim < 0.45；短文 < 0.50（`assess_gold`）。
    374–378 各保留异喻，勿繁转简五通克隆。
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

OPEN_JET_LIT = "如是我闻：一时，佛在舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_BEN_LIT = "如是我闻：一时，佛在波罗㮈仙人住处鹿野苑中。"
OPEN_BEN_MOD = "我是这样听说的：有一次，佛住在波罗㮈仙人住处鹿野苑中。"

CLOSE_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

AWAKEN_LIT = "「我生已尽，梵行已立，所作已作，自知不受后有。」"
AWAKEN_MOD = "「我生已尽，梵行已立，所作已作，自知不受后有。」"

FOUR_FOOD_LIT = "抟食、触食、意思食、识食"
FOUR_FOOD_MOD = "抟食、触食、意思食、识食"

FOUR_TRUTH_LIT = "苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛"
FOUR_TRUTH_MOD = "苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛"

# 四食有贪 → 识住 → 名色 → 行 → 当来有 → 纯大苦聚（据 SN12.64 纲要）
GREED_CHAIN_LIT = (
    "识住增长；识住增长故入于名色；入名色故诸行增长；"
    "行增长故当来有增长；当来有增长故生、老、病、死、忧、悲、恼、苦集——"
    "如是纯大苦聚集。"
)
GREED_CHAIN_MOD = (
    "识便住着增长；识住增长，便入于名色；入名色，诸行便增长；"
    "行增长，当来的有便增长；当来有增长，生、老、病、死、忧、悲、恼、苦便集起——"
    "这样纯大苦聚集。"
)
NO_GREED_CHAIN_LIT = (
    "识不住、不增长；故不入名色；行不增长；当来有不生不长；"
    "未来世生、老、病、死、忧、悲、恼、苦不起——如是纯大苦聚灭。"
)
NO_GREED_CHAIN_MOD = (
    "识便不住、不增长；因而不入名色；行不增长；当来有不生不长；"
    "未来世生、老、病、死、忧、悲、恼、苦不起——这样纯大苦聚灭。"
)

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

# --- SA 371 食（SN 12.11 Āhāra）----------------------------------------------
SUTTAS["SA_371"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有四食，资益众生，令得住世、摄受长养。"
        "何等为四？谓抟食——或粗或细、触食、意思食、识食。」",
        "「此四食何因、何集、何生、何起？谓爱为因、为集、为生、为起。"
        "爱何因、何集、何生、何起？谓受。"
        "受何因？谓触。触何因？谓六入处。"
        "六入处何因？谓名色。名色何因？谓识。识何因？谓行。行何因？谓无明。」",
        "「如是无明缘行，行缘识，乃至爱缘四食；"
        "食集故未来世生、老、病、死、忧、悲、恼、苦集——如是纯大苦聚集。」",
        "「无明灭则行灭，乃至六入处灭则触灭，触灭则受灭，受灭则爱灭，爱灭则食灭；"
        "食灭故未来世生、老、病、死、忧、悲、恼、苦灭——如是纯大苦聚灭。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有四种食，资益众生，使他们能住在世间、摄受长养。"
        "哪四种？抟食——或粗或细、触食、意思食、识食。」",
        "「这四食以什么为因、为集、为生、为起？以爱为因、为集、为生、为起。"
        "爱以什么为因？以受。受以什么为因？以触。触以什么为因？以六入处。"
        "六入处以什么为因？以名色。名色以什么为因？以识。识以什么为因？以行。"
        "行以什么为因？以无明。」",
        "「这样，无明缘行，行缘识，乃至爱缘四食；"
        "食集起，所以未来世生、老、病、死、忧、悲、恼、苦集起——"
        "这样纯大苦聚集。」",
        "「无明灭则行灭，乃至六入处灭则触灭，触灭则受灭，受灭则爱灭，爱灭则食灭；"
        "食灭尽，所以未来世生、老、病、死、忧、悲、恼、苦灭尽——"
        "这样纯大苦聚灭。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.11（Āhāra）。"
        "信-校正：汉本溯因止于六入处，据 Pāli／Sujato 补名色←识←行←无明；"
        "四食＝kabaliṅkāra／phassa／manosañcetanā／viññāṇa；"
        "「何触」读作「何起」（pabhava），不作「触」字义。"
    ),
}

# --- SA 372 颇求那（SN 12.12 Moḷiyaphagguna）--------------------------------
SUTTAS["SA_372"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有四食，资益众生，令得住世、摄受长养。"
        "何等为四？抟食——或粗或细、触食、意思食、识食。」",
        "时有比丘名颇求那，在佛后扇佛，白言：「世尊！谁食此识？」",
        "佛告颇求那：「我不说有食识者。若我说有食识者，汝问『谁食』乃成。"
        "今应问：『识食何所缘？』我则答：『识食能招未来有，令相续生；"
        "有有故有六入处，六入处缘触。』」",
        "颇求那复问：「为谁触？」"
        "佛言：「我不说有触者。应问：『何缘故有触？』"
        "答：『六入处缘触，触缘受。』」",
        "复问：「为谁受？」"
        "佛言：「我不说有受者。应问：『何缘故有受？』"
        "答：『触缘受，受缘爱。』」",
        "复问：「为谁爱？」"
        "佛言：「我不说有爱者。应问：『何缘故有爱？』"
        "答：『受缘爱，爱缘取。』」",
        "复问：「为谁取？」"
        "佛言：「我不说有取者。应问：『何缘故有取？』"
        "答：『爱缘取，取缘有。』」",
        "复问：「为谁有？」"
        "佛言：「我不说有有者。应问：『何缘故有有？』"
        "答：『取缘有；有缘生，生缘老、病、死、忧、悲、恼、苦——"
        "如是纯大苦聚集。"
        "六入处灭则触灭，乃至生灭则老、病、死、忧、悲、恼、苦灭——"
        "如是纯大苦聚灭。』」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有四种食，资益众生，使他们能住在世间、摄受长养。"
        "哪四种？抟食——或粗或细、触食、意思食、识食。」",
        "当时有位比丘名叫颇求那，在佛身后给佛扇风，问道："
        "「世尊！是谁在吃这识食？」",
        "佛告诉颇求那：「我不说有一个在吃识的人。若我说有，你问『谁吃』才说得通。"
        "现在该问：『识食以什么为缘？』我就答：『识食能招引未来的有，使生命相续；"
        "有了有，才有六入处；六入处缘触。』」",
        "颇求那又问：「是谁在触？」"
        "佛说：「我不说有一个在触的人。该问：『以什么为缘而有触？』"
        "答：『六入处缘触，触缘受。』」",
        "又问：「是谁在受？」"
        "佛说：「我不说有一个在受的人。该问：『以什么为缘而有受？』"
        "答：『触缘受，受缘爱。』」",
        "又问：「是谁在爱？」"
        "佛说：「我不说有一个在爱的人。该问：『以什么为缘而有爱？』"
        "答：『受缘爱，爱缘取。』」",
        "又问：「是谁在取？」"
        "佛说：「我不说有一个在取的人。该问：『以什么为缘而有取？』"
        "答：『爱缘取，取缘有。』」",
        "又问：「是谁在有？」"
        "佛说：「我不说有一个在有的人。该问：『以什么为缘而有有？』"
        "答：『取缘有；有缘生，生缘老、病、死、忧、悲、恼、苦——"
        "这样纯大苦聚集。"
        "六入处灭则触灭，乃至生灭则老、病、死、忧、悲、恼、苦灭——"
        "这样纯大苦聚灭。』」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.12（Moḷiyaphagguna）。"
        "信-校正：破『谁食／谁触』之作者见；正问条件缘起（na koci / kiṃpaccayā）；"
        "汉『我不言有食识者』＝Sujato “I don’t speak of one who consumes”。"
    ),
}

# --- SA 373 子肉（SN 12.63 Puttamaṁsa）— 矛喻交叉指示 → reconstructed ------
SUTTAS["SA_373"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有四食，资益众生，令得住世、摄受长养。"
        "何等为四？抟食——或粗或细、触食、意思食、识食。」",
        "「云何观察抟食？譬如夫妇唯有一子，爱念将养，欲度旷野险道；"
        "粮食乏尽，饥困无计，议曰：『宁杀此极爱之子，食肉得度，莫令三人俱死。』"
        "既杀其子，含悲垂泪，强食其肉，乃得度野。"
        "彼食子肉，宁取其味、贪嗜美乐否？」"
        "答曰：「不也，世尊！」"
        "「彼强食其肉，但为度险与否？」"
        "答言：「如是，世尊！」",
        "「凡食抟食，当如是观。如是观者，抟食断知；"
        "抟食断知已，于五欲功德贪爱则断；"
        "五欲贪爱断者，多闻圣弟子于五欲上无有一结能牵还生此世。」",
        "「云何观察触食？譬如牛生剥其皮，处处诸虫唼食，沙土坌尘、草木针刺；"
        "依地则地虫食，依水则水虫食，依空则飞虫食——卧起常有苦毒。"
        "于触食当如是观。如是观者，触食断知；触食断知则三受断；"
        "三受断者，多闻圣弟子于上更无所应作。」",
        "「云何观察意思食？譬如城邑边有火坑，无烟无焰，深过人顶；"
        "有人乐生厌死、背苦向乐，二人强拽欲投其中——"
        "其人唯愿远避：『若堕此坑，必死无疑。』"
        "观意思食亦复如是。如是观者，意思食断知；意思食断则三爱断；"
        "三爱断者，多闻圣弟子于上更无所应作。」",
        "「云何观察识食？（底本『如前须深经广说』：依 SN12.63 三矛喻补纲。）"
        "譬如王命捕盗，缚送王所。王敕：『晨以百矛刺之。』午问犹活，"
        "复敕日中、日晡各以百矛刺之。一日三百矛，身无完处，苦痛极剧——"
        "观识食亦复如是。如是观者，识食断知；识食断知则名色断知；"
        "名色断知者，多闻圣弟子于上更无所应作。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有四种食，资益众生，使他们能住在世间、摄受长养。"
        "哪四种？抟食——或粗或细、触食、意思食、识食。」",
        "「怎样观察抟食？好比夫妇只有一个儿子，十分疼爱，要过旷野险道；"
        "粮食吃完，饿得没办法，商量：『宁可杀了这极疼爱的儿子，吃肉好过险，"
        "别让三个人一起死。』于是杀了儿子，含着眼泪勉强吃肉，才走出旷野。"
        "他们吃儿子的肉，还会贪那滋味、贪图美味之乐吗？」"
        "答：「不会的，世尊！」"
        "「他们勉强吃肉，只是为了过险，对不对？」"
        "答：「是的，世尊！」",
        "「凡吃抟食，应当这样看。这样看，就能完全了知抟食；"
        "完全了知抟食，对五种欲功德的贪爱就断；"
        "五欲贪爱断了，多闻圣弟子在五欲上就没有一条结能使他再回到这个世界。」",
        "「怎样观察触食？好比一头牛被活活剥皮，到处虫子叮咬，沙土尘土、草木针刺；"
        "靠地有地虫咬，靠水有水虫咬，在空中有飞虫咬——起卧都带着苦毒。"
        "对触食应当这样看。这样看，就能完全了知触食；完全了知触食，三受就断；"
        "三受断了，多闻圣弟子在上面再也没有该做的了。」",
        "「怎样观察意思食？好比城边有火坑，无烟无焰，深过人高；"
        "有人爱生厌死、背苦向乐，两个壮汉硬拖他往坑里拽——"
        "他一心只想远远躲开：『若掉进这坑，必死无疑。』"
        "观察意思食也应当这样。这样看，就能完全了知意思食；"
        "完全了知意思食，三爱就断；三爱断了，多闻圣弟子在上面再也没有该做的了。」",
        "「怎样观察识食？（底本只写『如前须深经广说』：按 SN12.63 三矛喻补出纲要。）"
        "好比国王命人捉到盗贼，绑到王前。王下令：『早晨用一百支矛刺他。』"
        "中午问还活着，又下令中午、傍晚各用一百支矛刺。一天三百支矛，"
        "身上没有完好之处，苦痛极重——观察识食也应当这样。"
        "这样看，就能完全了知识食；完全了知识食，就能完全了知名色；"
        "完全了知名色，多闻圣弟子在上面再也没有该做的了。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.63（Puttamaṁsa）。"
        "gold_reconstructed：识食段底本『如前须深经广说』为交叉指示；"
        "依 SN12.63 晨／午／晡各百矛（一日三百）补纲，不用须深盗法之矛喻语境。"
        "信-校正：意思食火坑据 Pāli 作『二人强拽投坑』，汉『自行避火』从 SN；"
        "断知＝pariññā（完全了知）。"
    ),
}

# --- SA 374 有贪（SN 12.64 纲：有喜有贪→苦聚）-------------------------------
SUTTAS["SA_374"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有四食，资益众生，令得住世、摄受长养。"
        "何等为四？" + FOUR_FOOD_LIT + "。」",
        "「若于此四食有喜有贪，则" + GREED_CHAIN_LIT + "」",
        "「若于四食无贪无喜，则" + NO_GREED_CHAIN_LIT + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有四种食，资益众生，使他们能住在世间、摄受长养。"
        "哪四种？" + FOUR_FOOD_MOD + "。」",
        "「若对这四食有喜有贪，则" + GREED_CHAIN_MOD + "」",
        "「若对四食无贪无喜，则" + NO_GREED_CHAIN_MOD + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.64（Atthirāga）。"
        "本经为『有贪』系列之无喻本；链据 Pāli："
        "rāga／nandi／taṇhā → viññāṇa 住增长 → nāmarūpa → saṅkhārā → 当来有。"
        "画家／日光线喻见后经分说，此处不回填。"
    ),
}

# --- SA 375 有贪（忧悲尘垢略本）---------------------------------------------
SUTTAS["SA_375"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有四食，资益众生，令得住世、摄受长养。"
        "何等为四？" + FOUR_FOOD_LIT + "。」",
        "「于此四食有贪有喜，则有忧悲、有尘垢；"
        "若于四食无贪无喜，则无忧悲，亦无尘垢。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有四种食，资益众生，使他们能住在世间、摄受长养。"
        "哪四种？" + FOUR_FOOD_MOD + "。」",
        "「对这四食有贪有喜，就有忧悲、有尘垢；"
        "若对四食无贪无喜，就没有忧悲，也没有尘垢。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 列 SN12.64，汉本为极略异传——"
        "有贪→忧悲尘垢／无贪→无忧无垢；不演识住全链。"
        "与 374／376–378 分喻分说，勿繁转简克隆。"
    ),
}

# --- SA 376 有贪（日光线喻；如前广说 → reconstructed）----------------------
SUTTAS["SA_376"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有四食，资益众生，令得住世、摄受长养。"
        "何等为四？" + FOUR_FOOD_LIT + "。」",
        "「于此四食有贪有喜，则识住增长，乃至纯大苦聚集。"
        "（底本『如前广说』：链依 SA_374／SN12.64 纲，不逐支演。）」",
        "「若于四食无贪无喜，则识不住，乃至纯大苦聚灭。」",
        "「譬如楼阁宫殿，东西开牖；日出东方，应照何所？」"
        "比丘白佛：「应照西壁。」"
        "「若无西壁，应何所照？」"
        "「应照虚空，无所攀缘。」",
        "「如是，于四食无贪无喜，识无所住——如是纯大苦聚灭。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有四种食，资益众生，使他们能住在世间、摄受长养。"
        "哪四种？" + FOUR_FOOD_MOD + "。」",
        "「对这四食有贪有喜，识便住着增长，乃至纯大苦聚集。"
        "（底本只写『如前广说』：链条按 SA_374／SN12.64 纲要，不逐支展开。）」",
        "「若对四食无贪无喜，识便不住，乃至纯大苦聚灭。」",
        "「好比楼阁宫殿，东西开窗；太阳从东方升起，光应照到哪里？」"
        "比丘答：「应照西壁。」"
        "「若没有西壁，应照哪里？」"
        "「应照虚空，没有攀缘之处。」",
        "「同样，对四食无贪无喜，识便无所住——这样纯大苦聚灭。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium：SC 列 SN12.64；本经以日光线／无攀缘为别喻。"
        "gold_reconstructed：有贪／无贪两段『如前广说』为交叉指示，"
        "依 SA_374／SN12.64 识住链纲压缩提示，不回填画家喻全文。"
        "信：无西壁→照虚空无所住＝Sujato “It wouldn’t land”。"
    ),
}

# --- SA 377 有贪（画虚空喻）-------------------------------------------------
SUTTAS["SA_377"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有四食，资益众生，令得住世、摄受长养。"
        "何等为四？" + FOUR_FOOD_LIT + "。」",
        "「于此四食有贪有喜，识住增长，乃至纯大苦聚集。」",
        "「譬如楼阁东西开牖，日出东方，应照何所？」"
        "答言：「应照西壁。」"
        "「如是有贪有喜，识住增长，乃至大苦聚集。」",
        "「若于四食无贪无喜，亦无识住增长，乃至纯大苦聚灭。」",
        "「譬如画师集众彩，欲妆画虚空——宁能画否？」"
        "答言：「不能。世尊！虚空非色、无对、不可见故。」",
        "「如是无贪无喜，亦无识住——乃至纯大苦聚灭。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有四种食，资益众生，使他们能住在世间、摄受长养。"
        "哪四种？" + FOUR_FOOD_MOD + "。」",
        "「对这四食有贪有喜，识便住着增长，乃至纯大苦聚集。」",
        "「好比楼阁东西开窗，太阳从东方升起，光应照到哪里？」"
        "答：「应照西壁。」"
        "「同样，有贪有喜，识住增长，乃至大苦聚集。」",
        "「若对四食无贪无喜，也就没有识住增长，乃至纯大苦聚灭。」",
        "「好比画师调齐各种颜料，想在虚空上作画——画得成吗？」"
        "答：「画不成，世尊！虚空不是色、没有对碍、看不见。」",
        "「同样，无贪无喜，也就没有识住——乃至纯大苦聚灭。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 列 SN12.64；本经特出『画虚空不能成』之喻，"
        "与巴利『画家画板壁』形成对观——有所攀缘则可画，无所住则不可。"
        "识住链作 peyyāla 压缩，不逐食分说。"
    ),
}

# --- SA 378 有贪（画色／离色喻）---------------------------------------------
SUTTAS["SA_378"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有四食，资益众生，令得住世、摄受长养。"
        "何等为四？" + FOUR_FOOD_LIT + "。」",
        "「于此四食有贪有喜，识住增长，乃至纯大苦聚集。」",
        "「譬如画师集众彩，欲就色而妆画种种像——宁能成否？」"
        "答言：「能。世尊！」"
        "「如是有贪有喜，识住增长，乃至纯大苦聚集。」",
        "「若于四食无贪无喜，无有识住，乃至纯大苦聚灭。」",
        "「譬如画师欲离于色而妆画作像——宁能成否？」"
        "答言：「不能。世尊！」",
        "「如是无贪无喜，无有识住——乃至纯大苦聚灭。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有四种食，资益众生，使他们能住在世间、摄受长养。"
        "哪四种？" + FOUR_FOOD_MOD + "。」",
        "「对这四食有贪有喜，识便住着增长，乃至纯大苦聚集。」",
        "「好比画师调齐颜料，要在有色处画种种像——画得成吗？」"
        "答：「画得成，世尊！」"
        "「同样，有贪有喜，识住增长，乃至纯大苦聚集。」",
        "「若对四食无贪无喜，没有识住，乃至纯大苦聚灭。」",
        "「好比画师想离开色法去作画成像——画得成吗？」"
        "答：「画不成，世尊！」",
        "「同样，无贪无喜，没有识住——乃至纯大苦聚灭。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 列 SN12.64；本经以『就色可画／离色不可』对应"
        "有贪识住／无贪无住；近巴利画家喻而汉本分经独说。"
        "与 374–377 各留异喻，不互为繁转简克隆。"
    ),
}

# --- SA 379 转法轮（SN 56.12／近 56.11）-------------------------------------
SUTTAS["SA_379"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告五比丘：「此苦圣谛，本所未闻；当正思惟，生眼、智、明、觉。"
        "此苦集圣谛、此苦灭圣谛、此苦灭道迹圣谛，亦复如是——本所未闻，"
        "当正思惟，生眼、智、明、觉。」",
        "「复次：苦圣谛已知当知；苦集圣谛已知当断；"
        "苦灭圣谛已知当证；苦灭道迹圣谛已知当修——"
        "皆本所未闻，正思惟时，生眼、智、明、觉。」",
        "「复次：苦圣谛已知、知已出；苦集已知、已断出；"
        "苦灭已知、已证出；道迹已知、已修出——"
        "皆本所未闻，正思惟时，生眼、智、明、觉。」",
        "「诸比丘！我于此四圣谛三转十二行，若不生眼、智、明、觉，"
        "则终不得于诸天、魔、梵、沙门、婆罗门及闻法众中，"
        "为解脱、为出、为离，亦不自证得阿耨多罗三藐三菩提。"
        "我已三转十二行，生眼、智、明、觉故，于彼众中得出、得脱，"
        "自证得成阿耨多罗三藐三菩提。」",
        "说是法时，尊者憍陈如及八万诸天，远尘离垢，得法眼净。",
        "世尊问憍陈如：「知法未？」答：「已知，世尊！」"
        "再问：「知法未？」答：「已知，善逝！」"
        "以已知法故，名阿若拘邻。",
        "地神唱言：「世尊于波罗㮈仙人住处鹿野苑中，三转十二行法轮——"
        "诸沙门、婆罗门、天、魔、梵所未曾转，多所饶益，利安人天。」"
        "虚空神乃至梵身天展转传唱。是故此经名《转法轮》。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉五比丘：「这苦圣谛，是我从前未听过的法；"
        "应当正思惟，便生起眼、智、明、觉。"
        "这苦集圣谛、苦灭圣谛、苦灭道迹圣谛，也是一样——"
        "从前未听过，正思惟时，生起眼、智、明、觉。」",
        "「再者：苦圣谛已经了知，还应当完全了知；苦集已经了知，还应当断；"
        "苦灭已经了知，还应当证；道迹已经了知，还应当修——"
        "都是从前未听过的法，正思惟时，生起眼、智、明、觉。」",
        "「再者：苦圣谛已经了知、了知已完成；苦集已经了知、已经断尽；"
        "苦灭已经了知、已经证得；道迹已经了知、已经修习完成——"
        "都是从前未听过的法，正思惟时，生起眼、智、明、觉。」",
        "「比丘们！我若对这四圣谛三转十二行，不生起眼、智、明、觉，"
        "就终究不能在诸天、魔、梵、沙门、婆罗门及闻法众中，"
        "得到解脱、出离，也不能自己证得无上正等正觉。"
        "正因为我已三转十二行，生起眼、智、明、觉，才在那些众中得出、得脱，"
        "自己证成无上正等正觉。」",
        "说此法时，尊者憍陈如以及八万诸天，远离尘垢，得到法眼清净。",
        "世尊问憍陈如：「知道法了吗？」答：「已经知道，世尊！」"
        "再问：「知道法了吗？」答：「已经知道，善逝！」"
        "因为他已知法，所以名叫阿若拘邻。",
        "地神高声唱：「世尊在波罗㮈仙人住处鹿野苑中，三转十二行法轮——"
        "沙门、婆罗门、天、魔、梵都不曾转过，多所饶益，利安人天。」"
        "虚空神乃至梵身天展转传唱。所以这部经名叫《转法轮》。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.12（三转十二行纲）；叙事近 SN56.11。"
        "三转＝示相／劝修／已办；十二行＝四谛×三。"
        "「阿耨多罗三藐三菩提」早期译词，白话「无上正等正觉」。"
        "天众传唱压缩 peyyāla，不逐层复述。"
    ),
}

# --- SA 380 四圣谛（无平行）-------------------------------------------------
SUTTAS["SA_380"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「圣谛有四。何等为四？"
        "谓" + FOUR_TRUTH_LIT + "。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「圣谛有四种。哪四种？"
        "就是" + FOUR_TRUTH_MOD + "。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "仅标四谛名数；定型开合。confidence=medium。"
    ),
}

# --- SA 381 四圣谛（当修无间等）---------------------------------------------
SUTTAS["SA_381"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「圣谛凡四：苦、集、灭、与道迹。」",
        "「于此四谛犹未现观透彻者，当勤修无间等——"
        "发胜愿欲，精进堪能，系念正知，务令觉了。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「圣谛一共有四种：苦、集、灭、以及道迹。」",
        "「对这四谛还没有现观透彻的人，应当努力修无间等——"
        "发起殊胜的愿欲，精进而能担当，系念正知，务必觉了。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "「无间等」＝abhisamaya（现观／透彻了知），非大乘无间道术语。"
        "confidence=medium。"
    ),
}

# --- SA 382 当知（SN 56.29 Pariññeyya）--------------------------------------
SUTTAS["SA_382"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「有四圣谛。何等为四？"
        "谓" + FOUR_TRUTH_LIT + "。」",
        "「苦圣谛当知、当解；集圣谛当知、当断；"
        "灭圣谛当知、当证；道迹圣谛当知、当修。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「有四种圣谛。哪四种？"
        "就是" + FOUR_TRUTH_MOD + "。」",
        "「苦圣谛应当了知、应当解了；集圣谛应当了知、应当断除；"
        "灭圣谛应当了知、应当证得；道迹圣谛应当了知、应当修习。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.29（Pariññeyya）。"
        "四谛作业：pariññeyya／pahātabba／sacchikātabba／bhāvetabba。"
    ),
}

# --- SA 383 已知（无平行）---------------------------------------------------
SUTTAS["SA_383"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「有四圣谛。何等为四？"
        "谓" + FOUR_TRUTH_LIT + "。」",
        "「若比丘于苦圣谛已知、已解，于集已知、已断，"
        "于灭已知、已证，于道迹已知、已修——"
        "如是则断爱欲，转去诸结，于慢、无明等，究竟苦边。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「有四种圣谛。哪四种？"
        "就是" + FOUR_TRUTH_MOD + "。」",
        "「若比丘对苦圣谛已经了知、已经解了，对集已经了知、已经断除，"
        "对灭已经了知、已经证得，对道迹已经了知、已经修习——"
        "这样就能断除爱欲，转去各种结缚，在慢、无明等方面，到达苦的尽头。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "已办四谛→断爱、去结、尽慢无明、究竟苦边。confidence=medium。"
    ),
}

# --- SA 384 漏尽（无平行）---------------------------------------------------
SUTTAS["SA_384"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「圣谛有四——" + FOUR_TRUTH_LIT + "。」",
        "「比丘若已解苦、已断集、已证灭、已修道迹——"
        "是则漏尽阿罗汉：所作已办，卸重担，获己利，"
        "有结永尽，正智而善解脱。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「圣谛有四种——" + FOUR_TRUTH_MOD + "。」",
        "「比丘若已经解了苦、已经断了集、已经证了灭、已经修了道迹——"
        "那就是漏尽阿罗汉：该做的已办，卸下重担，得到自己的利益，"
        "有的结缚永远尽了，以正智而善得解脱。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "四谛已办＝漏尽阿罗汉定型（khīṇāsava 等）。confidence=medium。"
    ),
}

# --- SA 385 边际（无平行）---------------------------------------------------
SUTTAS["SA_385"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「有四圣谛。何等为四？"
        "谓" + FOUR_TRUTH_LIT + "。」",
        "「若比丘于苦已知、已解，于集已知、已断，"
        "于灭已知、已证，于道迹已知、已修——"
        "是名边际、究竟边际、离垢边际；梵行已终，纯一清白，名为上士。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「有四种圣谛。哪四种？"
        "就是" + FOUR_TRUTH_MOD + "。」",
        "「若比丘对苦已经了知、已经解了，对集已经了知、已经断除，"
        "对灭已经了知、已经证得，对道迹已经了知、已经修习——"
        "这就叫边际、究竟边际、离垢边际；梵行已经完成，纯一清白，名叫上士。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "边际／离垢边际＝梵行究竟之誉。confidence=medium。"
    ),
}

# --- SA 386 无有关键（略；无平行）---------------------------------------------
SUTTAS["SA_386"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「有四圣谛。何等为四？"
        "谓" + FOUR_TRUTH_LIT + "。」",
        "「若比丘于苦已知、已解，于集已知、已断，"
        "于灭已知、已证，于道迹已知、已修——"
        "如是无有关键，平治城堑，度诸险难，解脱结缚，"
        "名为贤圣，建立圣幢。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「有四种圣谛。哪四种？"
        "就是" + FOUR_TRUTH_MOD + "。」",
        "「若比丘对苦已经了知、已经解了，对集已经了知、已经断除，"
        "对灭已经了知、已经证得，对道迹已经了知、已经修习——"
        "这样便没有门闩关键，填平城堑，度过险难，解脱结缚，"
        "名叫贤圣，竖起圣幢。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "城喻略本；详释见 SA_387。confidence=medium。"
    ),
}

# --- SA 387 无有关键（详释；无平行）-----------------------------------------
SUTTAS["SA_387"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「有四圣谛。何等为四？"
        "谓" + FOUR_TRUTH_LIT + "。」",
        "「若比丘于苦已知、已解，于集已知、已断，"
        "于灭已知、已证，于道迹已知、已修——"
        "如是无有关键，平治城堑，度诸险难，名为贤圣，建立圣幢。」",
        "「云何无有关键？谓五下分结已断、已知，是名离关键。"
        "云何平治城堑？无明谓之深堑，彼得断知，是名平治城堑。"
        "云何度诸险难？谓无际生死，究竟苦边，是名度诸险难。"
        "云何解脱结缚？谓爱已断、已知。"
        "云何建立圣幢？谓我慢已断、已知，是名建立圣幢。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「有四种圣谛。哪四种？"
        "就是" + FOUR_TRUTH_MOD + "。」",
        "「若比丘对苦已经了知、已经解了，对集已经了知、已经断除，"
        "对灭已经了知、已经证得，对道迹已经了知、已经修习——"
        "这样便没有门闩关键，填平城堑，度过险难，名叫贤圣，竖起圣幢。」",
        "「什么叫没有关键？五下分结已经断除、已经了知，就叫离开关键。"
        "什么叫填平城堑？无明就是深堑，对它得到断知，就叫填平城堑。"
        "什么叫度过险难？无边的生死到达苦的尽头，就叫度过险难。"
        "什么叫解脱结缚？爱已经断除、已经了知。"
        "什么叫竖起圣幢？我慢已经断除、已经了知，就叫竖起圣幢。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "关键＝五下分结；堑＝无明；险难＝无际生死；缚＝爱；幢＝我慢。"
        "早期结使语，非密教／禅宗术语。confidence=medium。"
    ),
}

# --- SA 388 五支六分（无平行）-----------------------------------------------
SUTTAS["SA_388"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「圣谛凡四——" + FOUR_TRUTH_LIT + "。」",
        "「比丘于苦已解、于集已断、于灭已证、于道已修者——"
        "乃断五支、具六分，守其一、依其四；"
        "弃诸谛执，远离四衢，觉想已证，所作已办；"
        "心慧二俱善解脱，纯一清白，号曰上士。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「圣谛一共四种——" + FOUR_TRUTH_MOD + "。」",
        "「比丘对苦已经解了、对集已经断了、对灭已经证了、对道已经修了——"
        "那就是断了五支、具足六分，守护那一、依倚那四；"
        "舍弃种种谛执，远离四衢歧路，觉想已经证得，该做的已经办完；"
        "心与慧都善得解脱，纯一清白，称为上士。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "「断五支、成六分……」为阿罗汉德号定型（亦见于 AN 等）；"
        "此处系于四谛已办。不臆解五支六分细目。confidence=medium。"
    ),
}

# --- SA 389 大医王（无巴利；T219 汉平行）------------------------------------
SUTTAS["SA_389"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「成就四法，名曰大医王，具王者之所应、王者之分。"
        "何等为四？一、善知病；二、善知病源；三、善知对治；"
        "四、善知治已，当来更不动发。」",
        "「云何善知病？谓如实知如是种种病。"
        "云何善知病源？谓知因风、痰阴、涎唾、众冷，及现事、时节等而起。"
        "云何善知对治？谓应涂、应吐、应下、应灌鼻、应熏、应取汗——如是比。"
        "云何治已当来不动？谓究竟除愈，未来永不起。」",
        "「如來、应、等正觉为大医王，成就四德，疗众生病，亦复如是——"
        "如实知苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛。」",
        "「世间良医于生、老、病、死、忧、悲、恼、苦之根本对治不如实知；"
        "如來于生根本及老、病、死、忧、悲、恼、苦根本对治皆如实知——"
        "是故名为大医王。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「成就四种法，就叫大医王，具备为王者所应有的资格与职分。"
        "哪四种？一、善于了知病；二、善于了知病的根源；三、善于了知对治；"
        "四、善于了知治好以后，将来不会再发作。」",
        "「什么叫善于了知病？就是如实知道各种病。"
        "什么叫善于了知病源？知道因风、痰、涎唾、众冷，以及眼前的事、时节等而起。"
        "什么叫善于对治？该涂的涂、该吐的吐、该下的下、该灌鼻、该熏、该发汗——这一类。"
        "什么叫治好后将来不动发？就是彻底治好，未来永远不再起。」",
        "「如来、应供、等正觉是大医王，成就这四种德，治疗众生的病，也是这样——"
        "如实知道苦圣谛、苦集圣谛、苦灭圣谛、苦灭道迹圣谛。」",
        "「世间的良医对生、老、病、死、忧、悲、恼、苦的根本对治不能如实了知；"
        "如来对生的根本，以及对老、病、死、忧、悲、恼、苦的根本对治都能如实了知——"
        "所以名叫大医王。」",
        CLOSE_MOD,
    ],
    "notes": (
        "SC 未列巴利平行，唯有汉译 T219《医喻》等；"
        "四谛配四医德为早期譬喻，非法身／如来藏医王义。"
        "confidence=medium。"
    ),
}

# --- SA 390 沙门婆罗门（SN 56.5／56.6 resembling）---------------------------
SUTTAS["SA_390"] = {
    "lit": [
        OPEN_BEN_LIT,
        "尔时，世尊告诸比丘：「若诸沙门、婆罗门于" + FOUR_TRUTH_LIT + "不如实知——"
        "此非沙门之沙门，非婆罗门之婆罗门；"
        "亦不能于沙门义、婆罗门义见法自知作证：" + AWAKEN_LIT,
        "「若沙门、婆罗门于此四圣谛如实知——"
        "当知是沙门之沙门、婆罗门之婆罗门；"
        "于沙门义、婆罗门义见法自知作证：" + AWAKEN_LIT,
        "「是故比丘于四圣谛无间等，当起增上欲，精勤堪能，方便修学。"
        "何等为四？谓" + FOUR_TRUTH_LIT + "。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_BEN_MOD,
        "那时，世尊告诉比丘们：「若沙门、婆罗门对" + FOUR_TRUTH_MOD + "不能如实了知——"
        "这就不是真正的沙门、真正的婆罗门；"
        "也不能在沙门义、婆罗门义上见法、自己知道、自己作证：" + AWAKEN_MOD,
        "「若沙门、婆罗门对这四圣谛如实了知——"
        "就应当知道：这才是沙门中的沙门、婆罗门中的婆罗门；"
        "能在沙门义、婆罗门义上见法、自己知道、自己作证：" + AWAKEN_MOD,
        "「所以比丘对四圣谛的无间等，应当发起强盛的愿欲，精勤堪能，方便修学。"
        "哪四种？就是" + FOUR_TRUTH_MOD + "。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN56.5（resembling SN56.6）。"
        "汉本以『非沙门之沙门』正反双说，近 SN56 沙门婆罗门系列；"
        "巴利 56.5 偏『觉四谛』略文，法义从四谛如实知＝真沙门。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_371": "high",
    "SA_372": "high",
    "SA_373": "high",
    "SA_374": "high",
    "SA_375": "high",
    "SA_376": "medium",
    "SA_377": "high",
    "SA_378": "high",
    "SA_379": "high",
    "SA_380": "medium",
    "SA_381": "medium",
    "SA_382": "high",
    "SA_383": "medium",
    "SA_384": "medium",
    "SA_385": "medium",
    "SA_386": "medium",
    "SA_387": "medium",
    "SA_388": "medium",
    "SA_389": "medium",
    "SA_390": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_373": (
        "底本识食段『如前须深经广说』为交叉指示；"
        "依 SN12.63 晨／午／晡各百矛（一日三百）补纲，不用须深盗法语境"
    ),
    "SA_376": (
        "底本有贪／无贪两段『如前广说』为交叉指示；"
        "依 SA_374／SN12.64 识住链纲压缩提示，日光线喻保留"
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
    assert set(GOLD) == {f"SA_{i}" for i in range(371, 391)}, (
        "GOLD must cover SA_371–SA_390 exactly"
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

    # Snapshot SA_370 before merge to assert untouched
    sa370_before = None
    for rec in records:
        if rec["id"] == "SA_370":
            sa370_before = json.dumps(
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

    # Assert SA_370 untouched
    for rec in merged:
        if rec["id"] == "SA_370" and sa370_before is not None:
            sa370_after = json.dumps(
                {
                    "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                    "modern_psychology_text": rec.get("modern_psychology_text"),
                    "notes": rec.get("notes"),
                    "review_status": rec.get("review_status"),
                    "confidence": rec.get("confidence"),
                },
                ensure_ascii=False,
            )
            assert sa370_before == sa370_after, "SA_370 must remain untouched"
            break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa371-390.json").write_text(
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
        for i in range(1, 391)
    )

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_371–SA_390 only)")
    print(f"validation: ok={len(oks)} warn={len(warns)} fail={len(fails)}")
    print(f"forbidden_hits={len(forbidden)}")
    print(
        f"needs_restyle (assess_gold): {len(needs_restyle)}  "
        f"max_sim={max_r['sim']} ({max_r['id']})  "
        f"mean_sim={round(sum(r['sim'] for r in report) / len(report), 3)}"
    )
    print(f"paragraph_parallel_violations={len(para_bad)}")
    print(f"gold={len(report) - len(recon)} gold_reconstructed={len(recon)}")
    print(f"confidence: {conf_split}")
    print(f"continuous_gold_SA_1–390={continuous}")
    print(f"SA_370_untouched=True")
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
