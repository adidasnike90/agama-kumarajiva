#!/usr/bin/env python3
"""Retranslate SA 651–670（卷第二十七 根力相应续）→ merge.

本批二十经：沙门婆罗门 SN48.6/7；成 SN48.14；成 SN48.13；堂阁 SN48.52；
信 SN48.10；堂阁变体 SN48.52/50/10；信（无平行）；二力 AN2.11–20；
二力／三力 peyyāla；四力 AN4.152；四力变体；摄 AN4.32；四力 AN4.153。

信：有 SN／AN 平行者据巴利厘义；无专经 → medium/low。
    交叉指示／peyyāla 补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：断言 SA_650 不变；不触碰 SA_671+。
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

OPEN_MALLA_LIT = "如是我闻：一时，佛在末罗人间，住郁鞞罗迦波聚落。"
OPEN_MALLA_MOD = "我是这样听说的：有一次，佛在末罗人间，住在郁鞞罗迦波聚落。"

OPEN_APANA_LIT = "如是我闻：一时，佛在央伽人间，住阿婆那聚落。"
OPEN_APANA_MOD = "我是这样听说的：有一次，佛在央伽人间，住在阿婆那聚落。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

FIVE_IND_LIT = "信、精进、念、定、慧"
FIVE_IND_MOD = "信、精进、念、定、慧"

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

# --- SA 651 沙门婆罗门（SN48.6／7）--------------------------------------------
SUTTAS["SA_651"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「若沙门、婆罗门于此五根之味、患、离不如实知，我不说彼是真沙门、真婆罗门；"
        "彼于沙门义、婆罗门义，现法未能自知作证。」",
        "「若如实知此五根之集、没、味、患、离，我说彼是真沙门、真婆罗门；"
        "于沙门义、婆罗门义，现法自知作证。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「若沙门、婆罗门对这五根的味、患、离不能如实知，我不说他们是真沙门、真婆罗门；"
        "他们在现法中不能自己证知沙门义、婆罗门义。」",
        "「若如实知这五根的集、没、味、患、离，我说他们是真沙门、真婆罗门；"
        "在现法中自己证知沙门义、婆罗门义。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.7／48.6（沙门婆罗门知五根味患离）。"
        "据 SN 校正：汉作佛自证五根成正觉 → SN 真／非真沙门婆罗门；"
        "用语从汉「集、没、味、患、离」（≈ samudaya／atthaṅgama／assāda／ādīnava／nissaraṇa）。"
        "与 SA_650 同系，略变句式以别卷次。"
    ),
}

# --- SA 652 成（SN48.14）------------------------------------------------------
SUTTAS["SA_652"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "于此五根圆满具足者，得阿罗汉；弱于此者，得阿那含；"
        "又弱者，得斯陀含；又弱者，得须陀洹；"
        "又弱者，是随法行；又弱者，是随信行。」",
        "「满足者成满足事，减缺者成减缺事；此五根终不空无果。"
        "若于此五根一切无有，我说彼在凡夫之数。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "这五根圆满具足的，得阿罗汉；比这弱的，得阿那含；"
        "再弱的，得斯陀含；再弱的，得须陀洹；"
        "再弱的，是随法行；再弱的，是随信行。」",
        "「满足的成就满足之事，减缺的成就减缺之事；这五根终不空无果。"
        "如果对这些五根一无所有，我说他算在凡夫之列。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.14 Saṁkhitta（五根强弱六阶＋不空无果）。"
        "据 SN 校正：汉仅四果 → 补随法行／随信行；保留汉「无诸根＝凡夫」。"
    ),
}

# --- SA 653 成（SN48.13）------------------------------------------------------
SUTTAS["SA_653"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "于此五根增上明利满足者，得阿罗汉；弱于此者，得阿那含；"
        "又弱者，得斯陀含；又弱者，得须陀洹；"
        "又弱者，是随法行；又弱者，是随信行。」",
        "「如是根有差别，故果有差别；果有差别，故人有差别。"
        "满足者作满足事，减少者作减少事；诸根不空无果。"
        "若无此诸根，我说彼作凡夫之数。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "这五根增上明利满足的，得阿罗汉；比这弱的，得阿那含；"
        "再弱的，得斯陀含；再弱的，得须陀洹；"
        "再弱的，是随法行；再弱的，是随信行。」",
        "「这样，根有差别，所以果有差别；果有差别，所以人有差别。"
        "满足的作满足之事，减少的作减少之事；诸根不空无果。"
        "如果没有这些根，我说他算在凡夫之列。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.13（六阶＋indriyavemattatā→phalavemattatā→puggalavemattatā）。"
        "据 SN 压缩：汉本俱分解脱／身证／见到…长列 → 从 SN 六阶＋根异果异人异；"
        "汉「根波罗蜜知人」义并入差别句。"
    ),
}

# --- SA 654 堂阁（SN48.52）----------------------------------------------------
SUTTAS["SA_654"] = {
    "lit": [
        OPEN_MALLA_LIT,
        "佛告比丘：「圣弟子若未生圣慧，则信、精进、念、定四根不得安住；"
        "圣慧一生，此四根随之安住。」",
        "「譬如堂阁，栋梁未立，众椽不得安住；栋梁既立，众椽皆得安住。"
        "如是圣弟子有慧，则信、精进、念、定随慧而立——"
        "五根之中，慧为其首，以摄持故。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_MALLA_MOD,
        "佛告比丘：「圣弟子如果还没有生起圣慧，信、精进、念、定这四根就不能安住；"
        "圣慧一生起，这四根就随之安住。」",
        "「好比堂阁，栋梁还没立起，众椽就不能安住；栋梁一立，众椽都能安住。"
        "同样，圣弟子有了慧，信、精进、念、定就随慧而立——"
        "五根之中，慧是首要，用来摄持。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.52 Mallika（kūṭāgāra 栋喻；慧立则四根安住）。"
        "据 SN 校正：地点末罗郁鞞罗迦波（非祇园）；"
        "汉略「慧摄五根」→ 补 SN「未生圣慧则四根不安」义。"
    ),
}

# --- SA 655 信（SN48.10 resembling）-------------------------------------------
SUTTAS["SA_655"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "信根者，当知四不坏净；精进根者，当知四正断；"
        "念根者，当知四念处；定根者，当知四禅；慧根者，当知四圣谛。」",
        "「此诸功德，一切以慧为首，以摄持故。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "信根，应当知道是四不坏净；精进根，应当知道是四正断；"
        "念根，应当知道是四念处；定根，应当知道是四禅；慧根，应当知道是四圣谛。」",
        "「这些功德，一切都以慧为先，用来摄持。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling SN48.10 Vibhaṅga（五根所摄法类）。"
        "汉「乃至……」peyyāla 删省；保留四不坏净／四正断／四念处／四禅／四谛对应＋慧为首。"
    ),
}

# --- SA 656 堂阁（SN48.52 resembling）-----------------------------------------
SUTTAS["SA_656"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "若圣弟子成就慧根，能修信根——依离、依无欲、依灭、向于舍，"
        "是名信根成就；信根成就，即与慧根相应。」",
        "「如信根，精进、念、定、慧根修习亦复如是。"
        "是故五根，慧为其首，以摄持故。"
        "譬如堂阁，栋为其首，众材所依，以摄持故。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "若圣弟子成就慧根，就能修信根——依于远离、依于无欲、依于灭、趋向于舍，"
        "这叫信根成就；信根成就，就与慧根相应。」",
        "「如同信根，精进、念、定、慧根的修习也是这样。"
        "所以五根以慧为首，用来摄持。"
        "好比堂阁，栋是首要，众材所依，用来摄持。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling SN48.52（慧具则余根随成；栋喻）。"
        "「依离、依无欲、依灭、向于舍」＝ viveka／virāga／nirodha／vossagga 定型；"
        "与 SA_654 同喻而补「随慧修余根」义。"
    ),
}

# --- SA 657 堂阁（SN48.52／50 resembling）-------------------------------------
SUTTAS["SA_657"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "若圣弟子成就信根，当作是观：众生无始生死，无明所覆，爱结所系，"
        "长夜往来，不知本际；有因故有生死，因永尽则无生死。」",
        "「无明大暗聚为障——谁般涅槃？唯苦灭、苦息、清凉、永没。」",
        "「如信根，精进、念、定、慧根亦如是说。"
        "此五根，慧为首，慧所摄持；譬如堂阁，栋为首，栋所摄持。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "若圣弟子成就信根，应当这样观察：众生无始以来生死，被无明覆盖、爱结系缚，"
        "长夜往来，不知本际；有因才有生死，因永远尽了就没有生死。」",
        "「无明这大黑暗聚是障碍——谁在般涅槃？只有苦灭、苦息、清凉、永没。」",
        "「如同信根，精进、念、定、慧根也是这样说。"
        "这五根以慧为首、为慧所摄持；好比堂阁以栋为首、为栋所摄持。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：resembling SN48.52／SN48.50 末（无始生死＋涅槃唯苦灭）。"
        "汉「谁般涅槃」从 SN anamataggo／sabbasaṅkhārasamatho 义压缩；堂阁喻同系。"
    ),
}

# --- SA 658 堂阁（SN48.10 resembling）-----------------------------------------
SUTTAS["SA_658"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「何等信根？圣弟子于如来所起净信，根本坚固，"
        "天、魔、梵、沙门、婆罗门及诸世间法所不能坏，是名信根。」",
        "「何等精进根？谓四正断。何等念根？谓四念处。"
        "何等定根？谓四禅。何等慧根？谓四圣谛。」",
        "「此诸功德，皆以慧为首；譬如堂阁，栋为其首。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「什么是信根？圣弟子对如来生起净信，根本坚固，"
        "天、魔、梵、沙门、婆罗门以及世间诸法都不能破坏，这叫信根。」",
        "「什么是精进根？就是四正断。什么是念根？就是四念处。"
        "什么是定根？就是四禅。什么是慧根？就是四圣谛。」",
        "「这些功德都以慧为先；好比堂阁，栋是首要。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling SN48.10（信不可坏＋四正断／念处／禅／谛）；"
        "收束以堂阁栋喻（与 SA_654–657 同卷母题）。"
    ),
}

# --- SA 659 堂阁（SN48.50）----------------------------------------------------
SUTTAS["SA_659"] = {
    "lit": [
        OPEN_APANA_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「何等信根？圣弟子于如来起一向净信，不疑不惑，是名信根。」",
        "「何等精进根？既有净信，则起精进——断不善、满善法，是名精进根。」",
        "「何等念根？精进已立，则正念现前，是名念根。"
        "何等定根？正念现前，则得定、得心一境，是名定根。」",
        "「何等慧根？心定之后，如实知：生死无始，本际不可得；"
        "无明永尽，则苦灭、清凉——是名慧根。」",
        "「此五根，慧为首，以摄持故；譬如堂阁，栋为其首。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_APANA_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「什么是信根？圣弟子对如来起一向净信，不疑不惑，这叫信根。」",
        "「什么是精进根？有了净信，就发起精进——断除不善、圆满善法，这叫精进根。」",
        "「什么是念根？精进立了，正念就现前，这叫念根。"
        "什么是定根？正念现前，就得定、得心一境，这叫定根。」",
        "「什么是慧根？心定之后，如实知道：生死无始，本际不可得；"
        "无明永远尽了，苦就灭尽、清凉——这叫慧根。」",
        "「这五根以慧为首，用来摄持；好比堂阁，栋是首要。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.50 Āpaṇa（信→精进→念→定→慧连锁；无始生死）。"
        "据 SN 校正：汉「于如来发菩提心」→ 于如来一向净信（ekantagata abhippasanna）；"
        "地点从 SN 央伽阿婆那；「所余堂阁如上」据同卷栋喻补一句。"
        "gold_reconstructed：底本堂阁段为交叉指示。"
    ),
}

# --- SA 660 信（无平行）-------------------------------------------------------
SUTTAS["SA_660"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "于此五根修习多修习，能断过去、未来、现在一切苦。」",
        "「如苦断，究竟苦边、苦尽、苦息、苦没，度苦流，于缚得解，"
        "害诸有，一切漏尽，亦如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "对这些五根修习多修习，能断过去、未来、现在一切苦。」",
        "「如同苦断，究竟苦边、苦尽、苦息、苦没，度苦流，于束缚得解脱，"
        "灭诸有，一切漏尽，也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：五根修习断三世苦＋果德 peyyāla 压缩；无 SN 专经。"
        "「害诸色」从早期「害有／尽有」义作「害诸有」，避色身误读。"
    ),
}

# --- SA 661 二力（AN2.11–20）--------------------------------------------------
SUTTAS["SA_661"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有二种力——思择力、修习力。」",
        "「何等思择力？圣弟子于空闲林树下作是思惟："
        "『身恶行，现法、后世受恶报。我若行身恶行，则自悔、他人亦悔我，"
        "大师、梵行者皆当责我，恶名流布，身坏命终，堕恶趣泥犁。』"
        "如是思择已，断身恶行，修身善行；口、意恶行亦如是断、修——是名思择力。」",
        "「何等修习力？圣弟子思择力成就已，随得修习力；得已，修习力满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有二种力——思择力、修习力。」",
        "「什么是思择力？圣弟子在空闲林树下这样思惟："
        "『身恶行，现法、后世会受恶报。我若行身恶行，自己后悔，他人也因我后悔，"
        "大师、梵行者都会责备我，恶名流传，身坏命终，堕入恶趣地狱。』"
        "这样思择之后，断身恶行，修身善行；口、意恶行也这样断、修——这叫思择力。」",
        "「什么是修习力？圣弟子思择力成就之后，随之得到修习力；得到以后，修习力满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN2.11–20 系（paṭisaṅkhānabala／bhāvanābala）。"
        "「数力」据巴利作「思择力」（计数／思择）；修力＝修习力。"
    ),
}

# --- SA 662 二力（peyyāla）----------------------------------------------------
SUTTAS["SA_662"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有二种力——思择力、修习力。」",
        "「圣弟子思择力成就已，贪、恚、痴或节或尽。"
        "依于思择力，安立思择力，随得修习力；得已，修习力满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有二种力——思择力、修习力。」",
        "「圣弟子思择力成就之后，贪、瞋、痴或减弱或尽除。"
        "依于思择力，安立思择力，随之得到修习力；得到以后，修习力满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：SA_661 差别句 peyyāla；补开经名目。"
        "gold_reconstructed：底本「如上说」交叉指示，据 SA_661 框补。"
    ),
}

# --- SA 663 二力（peyyāla）----------------------------------------------------
SUTTAS["SA_663"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有二种力——思择力、修习力。"
        "何等修习力？谓修四念处。」",
        "「如四念处，修四正断、四如意足、五根、五力、七觉分、八圣道分，"
        "乃至止观，亦如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有二种力——思择力、修习力。"
        "什么是修习力？就是修四念处。」",
        "「如同四念处，修四正断、四如意足、五根、五力、七觉分、八圣道分，"
        "乃至止观，也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：修力＝四念处及道品 peyyāla；补开经。"
        "gold_reconstructed：底本「如上说」＋道品串列交叉指示。"
    ),
}

# --- SA 664 三力（无平行）-----------------------------------------------------
SUTTAS["SA_664"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「力有三聚：一者信、精进、慧；二者信、念、慧；三者信、定、慧。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「力有三组：第一是信、精进、慧；第二是信、念、慧；第三是信、定、慧。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：三组三力名目经；无 AN／SN 专经对应。罗什风并三复次为一句。"
    ),
}

# --- SA 665 三力（peyyāla）----------------------------------------------------
SUTTAS["SA_665"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当学三力：信、精进、慧——我当具足。」",
        "「若以念代精进，或以定代精进，配成三力，所学亦尔。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「应当修学三力：信、精进、慧——我应当具足。」",
        "「如果用念代替精进，或用定代替精进，配成三力，所学也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：SA_664 学句变体；peyyāla 压缩。"
        "gold_reconstructed：底本「如精进力，念力、定力亦如是说」交叉指示。"
    ),
}

# --- SA 666 三力（定义＋交叉）-------------------------------------------------
SUTTAS["SA_666"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有三力——信力、精进力、慧力。」",
        "「何等信力？圣弟子于如来所入净信，根本坚固，"
        "天、魔、梵、沙门、婆罗门及诸同法所不能坏，是名信力。」",
        "「何等精进力？谓修四正断。何等慧力？谓知四圣谛。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有三力——信力、精进力、慧力。」",
        "「什么是信力？圣弟子对如来进入净信，根本坚固，"
        "天、魔、梵、沙门、婆罗门以及同法者都不能破坏，这叫信力。」",
        "「什么是精进力？就是修四正断。什么是慧力？就是知四圣谛。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：三力分别（信不可坏／四正断／四谛）；"
        "汉开题「信、念、慧」与正文「精进」不合，从正文作信、精进、慧。"
        "gold_reconstructed：底本「余二力如上说」不回填 SA_664 另两组全文。"
    ),
}

# --- SA 667 四力（AN4.152 resembling）-----------------------------------------
SUTTAS["SA_667"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有四力——信力、精进力、念力、慧力。"
        "复有四力——信力、念力、定力、慧力。"
        "复有四力——觉力、精进力、无罪力、摄力。」",
        "「何等觉力？于善不善、有罪无罪、宜习不宜习、劣胜、黑白、"
        "有分别无分别、缘起非缘起，皆如实知，是名觉力。」",
        "「何等精进力？谓四正断。何等无罪力？谓身、口、意无罪。"
        "何等摄力？谓四摄事——布施、爱语、利行、同事。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有四力——信力、精进力、念力、慧力。"
        "又有四力——信力、念力、定力、慧力。"
        "又有四力——觉力、精进力、无罪力、摄力。」",
        "「什么是觉力？对善与不善、有罪与无罪、宜习与不宜习、劣与胜、黑与白、"
        "有分别与无分别、缘起与非缘起，都能如实知，这叫觉力。」",
        "「什么是精进力？就是四正断。什么是无罪力？就是身、口、意无罪。"
        "什么是摄力？就是四摄事——布施、爱语、利行、同事。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling AN4.152（四力名目）；"
        "觉／无罪／摄三力从汉本分别，义属早期（四正断、三业清净、四摄）。"
        "gold_reconstructed：底本「如上三力说／如前广说」交叉指示，据名目补纲。"
    ),
}

# --- SA 668 四力（四摄最胜）---------------------------------------------------
SUTTAS["SA_668"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有四摄事——布施、爱语、利行、同事。」",
        "「最胜布施者，谓法施。"
        "最胜爱语者，谓应时为乐闻善男子说法。」",
        "「最胜利行者：令不信者入信、立信；持戒者以净戒，悭者以施，"
        "恶慧者以正智，令入、令立。」",
        "「最胜同事者：阿罗汉与阿罗汉，阿那含与阿那含，"
        "斯陀含与斯陀含，须陀洹与须陀洹，净戒者与净戒者——各以同德授彼。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有四摄事——布施、爱语、利行、同事。」",
        "「最殊胜的布施，是法施。"
        "最殊胜的爱语，是应时为乐于听法的善男子说法。」",
        "「最殊胜的利行：让不信的人进入信仰、安立于信；对持戒的人以净戒，"
        "对悭吝的人以布施，对恶慧的人以正智，使他们进入、安立。」",
        "「最殊胜的同事：阿罗汉与阿罗汉，阿那含与阿那含，"
        "斯陀含与斯陀含，须陀洹与须陀洹，净戒者与净戒者——各以相同的德行授予对方。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：四摄最胜分别；承 SA_667 摄力。"
        "gold_reconstructed：底本「如上说」交叉指示，补四摄开题。"
    ),
}

# --- SA 669 摄（AN4.32）-------------------------------------------------------
SUTTAS["SA_669"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「若有所取于众者，一切皆是四摄事——"
        "或取布施，或取爱语，或取利行，或取同事。」",
        "「过去世众之所取，未来世众之所取，亦皆四摄事。」",
        "尔时世尊说偈：「布施及爱语，　或有行利者，　同事诸行生，　各随其所应。"
        "以此摄世间，　犹车因釭运。　世无四摄事，　母不念其子，"
        "父尊亦无敬。　以有四摄故，　大士德被世。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「凡是大众所取用的，一切都是四摄事——"
        "或者取布施，或者取爱语，或者取利行，或者取同事。」",
        "「过去世大众所取的，未来世大众所取的，也都是四摄事。」",
        "那时世尊说偈：「布施以及爱语，　或者有利行，　同事各种行为生起，　各随其所相应。"
        "用这些摄持世间，　如同车子靠车釭运转。　世上若无四摄事，　母亲也不顾念子女，"
        "对父亲尊长也无恭敬。　因为有四摄，　大士的德行遍及世间。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN4.32 Saṅgaha（四摄持世，如车釭；偈义同）。"
        "据 AN 校正压缩汉偈；「如上说」开经从四摄事径说。"
    ),
}

# --- SA 670 四力（AN4.153）----------------------------------------------------
SUTTAS["SA_670"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「觉力、精进力、无罪力、摄力——是为四力。」",
        "「比丘具此四力，远离五畏：畏不活、畏恶名、畏大众、畏死、畏恶趣。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「觉力、精进力、无罪力、摄力——这就是四力。」",
        "「比丘具备这四力，就远离五种畏惧：怕活不下去、怕恶名、怕在大众中、怕死、怕恶趣。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling AN4.153（四力；离五怖畏）。"
        "gold_reconstructed：底本「……如上说」指 SA_667 四力分别，此处只取名目＋五恐怖果。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_651": "high",
    "SA_652": "high",
    "SA_653": "high",
    "SA_654": "high",
    "SA_655": "high",
    "SA_656": "high",
    "SA_657": "medium",
    "SA_658": "high",
    "SA_659": "high",
    "SA_660": "medium",
    "SA_661": "high",
    "SA_662": "medium",
    "SA_663": "medium",
    "SA_664": "medium",
    "SA_665": "medium",
    "SA_666": "medium",
    "SA_667": "high",
    "SA_668": "medium",
    "SA_669": "high",
    "SA_670": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_659": "cross-ref 所余堂阁如上说 → hall peak line from SA_654–658",
    "SA_662": "peyyāla 如上说 → frame from SA_661 + greed/hate/delusion difference",
    "SA_663": "peyyāla 如上说 → 修力＝四念处 + path-factor list",
    "SA_665": "peyyāla 念力定力亦如是说 → learn-formula variants",
    "SA_666": "余二力如上说 → omit backfill of other triads",
    "SA_667": "如上三力说／如前广说 → named tetrads + brief definitions",
    "SA_668": "如上说 → 四摄最胜 from prior 摄力",
    "SA_670": "如上说 → 四力 names + five fears",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(651, 671)}, (
        "GOLD must cover SA_651–SA_670 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    assert not any(f"SA_{i}" in GOLD for i in range(671, 700))
    assert "SA_650" not in GOLD

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

    # Boundary: SA_650 must remain untouched
    boundary_id = "SA_650"
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

    # Snapshot SA_671+ in range we care about (671–690) to assert untouched
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
        if rec["id"] in {f"SA_{i}" for i in range(671, 691)}
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
        if rec["id"] == boundary_id and boundary_before is not None:
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
                assert before == after, f"{rid} must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa651-670.json").write_text(
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
    continuous_651_670 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(651, 671)
    )
    continuous_1_670 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(1, 671)
    )

    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛", "如如", "发菩提心"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_651–SA_670 only)")
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
    print(f"continuous_gold_SA_651–670={continuous_651_670}")
    print(f"continuous_gold_SA_1–670={continuous_1_670}")
    print(f"SA_650_untouched=True")
    print(f"SA_671+_untouched=True")
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
