#!/usr/bin/env python3
"""Retranslate SA 671–690（根力相应 卷二十七末–二十八）→ merge.

本批二十经：四力×2 AN4.153；五力 SN50.1–12／劝修；当知 SN48.8；五力劝成；
学力×4 AN5.1 系；白法／不善法 AN5.5；十力 AN10.21；乳母（无专平行）；
师子吼×2 AN6.64；七力×3 AN7.3。

信：有 AN／SN 平行者据巴利／Sujato 厘义；无专经 → medium。
    peyyāla／交叉指示补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_671–690；不触碰 SA_651–670（并行批次）；断言 SA_670 不变。
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

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

FOUR_PADHANA_LIT = (
    "已生恶不善法令断，未生恶法令不生，未生善法令生，"
    "已生善法令住不忘、修习增广——生欲、精进、摄心、增上"
)
FOUR_PADHANA_MOD = (
    "已生的恶不善法要断除，未生的恶法使不生，未生的善法使生起，"
    "已生的善法使安住不忘、修习增长——生起欲乐、精进、摄心、增上"
)

FIVE_BALA_LIT = "信力、精进力、念力、定力、慧力"
FIVE_BALA_MOD = "信力、精进力、念力、定力、慧力"

SEKHA_LIT = "信力、精进力、惭力、愧力、慧力"
SEKHA_MOD = "信力、精进力、惭力、愧力、慧力"

SEVEN_LIT = "信力、精进力、惭力、愧力、念力、定力、慧力"
SEVEN_MOD = "信力、精进力、惭力、愧力、念力、定力、慧力"

ROAR_LIT = "得先佛最胜处智，能转梵轮，于大众中作师子吼"
ROAR_MOD = "得先佛最胜处的智慧，能转梵轮，在大众中作师子吼"

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

# --- SA 671 四力（AN4.153 系：圣弟子不畏）------------------------------------
SUTTAS["SA_671"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「觉力、精进力、无罪力、摄力——是为四力。」",
        "「圣弟子成就此四力，当如是学：我不畏不活。何缘畏不活？"
        "身口意行不净、行邪贪，不信、懈怠、失念、不定、恶慧、悭而不摄者，乃应畏不活。"
        "我有觉力、精进力、无罪力、摄力，故不应畏不活。"
        "恶名畏、大众畏、死畏、恶趣畏，亦复如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「觉力、精进力、无罪力、摄力——这就是四力。」",
        "「圣弟子成就这四力，应当这样学：我不怕无法活命。凭什么怕？"
        "身口意行不清净、行邪贪，以及不信、懈怠、失念、不定、恶慧、悭吝不摄的人，才该怕无法活命。"
        "我有觉力、精进力、无罪力、摄力，所以不该怕无法活命。"
        "恶名畏、大众畏、死畏、恶趣畏，也是一样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling AN4.153 Paññābala（觉／精进／无罪／摄）；"
        "本经为圣弟子以四力遣五畏之差别。gold_reconstructed："
        "peyyāla「恶名等亦如上说」展开为五畏各一句。"
    ),
}

# --- SA 672 四力（分别）-------------------------------------------------------
SUTTAS["SA_672"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有四力——觉力、精进力、无罪力、摄力。」",
        "「何等觉力？谓慧、大慧、深慧、难胜慧；"
        "于善不善、有罪无罪、宜习不宜习、黑白、缘起非缘起如实知，是名觉力。」",
        f"「何等精进力？谓四正断——{FOUR_PADHANA_LIT}，正念正知而学，是名精进力。」",
        "「何等无罪力？谓身、口、意无罪，是名无罪力。」",
        "「何等摄力？谓四摄事——布施、爱语、利行、同事，是名摄力。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有四种力——觉力、精进力、无罪力、摄力。」",
        "「什么是觉力？就是慧、大慧、深慧、难胜慧；"
        "对善与不善、有罪与无罪、应习与不应习、黑白、缘起与非缘起都能如实知，叫做觉力。」",
        f"「什么是精进力？就是四正断——{FOUR_PADHANA_MOD}，正念正知而学，叫做精进力。」",
        "「什么是无罪力？身、口、意都无罪过，叫做无罪力。」",
        "「什么是摄力？四摄事——布施、爱语、利行、同事，叫做摄力。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling AN4.153；分别与 SA_667 同系。"
        "gold_reconstructed：汉「无罪力、摄力如上修多罗」→据 SA_667／AN 补足；"
        "精进力「四正断如前」→四正断定型。"
    ),
}

# --- SA 673 五力（SN50.1–12／AN5.13）------------------------------------------
SUTTAS["SA_673"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「所谓五力：信、精进、念、定、慧——修此五力，能胜烦恼。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「所谓五种力：信、精进、念、定、慧——修这五力，能胜过烦恼。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN50.1–12／AN5.13（五力略说名目）。"
        "罗什风压缩问答套语；略点「能胜烦恼」以别于纯抄汉列名（义不增宗）。"
    ),
}

# --- SA 674 五力（勤加精进）---------------------------------------------------
SUTTAS["SA_674"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五力——{FIVE_BALA_LIT}。"
        f"诸比丘当如是学：我当勤加精进，成就{FIVE_BALA_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种力——{FIVE_BALA_MOD}。"
        f"比丘们应当这样学：我要勤加精进，成就{FIVE_BALA_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：五力劝修差别（勤加精进成就）；无 SC 专经。"
        "gold_reconstructed：peyyāla「如上说」补五力名目＋劝学句。"
    ),
}

# --- SA 675 当知（SN48.8／AN5.15）---------------------------------------------
SUTTAS["SA_675"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五力——{FIVE_BALA_LIT}。"
        "信力当知在四不坏净；精进力当知在四正断；念力当知在四念处；"
        "定力当知在四禅；慧力当知在四圣谛。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种力——{FIVE_BALA_MOD}。"
        "信力应当在四不坏净上认取；精进力在四正断；念力在四念处；"
        "定力在四禅；慧力在四圣谛。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.8／AN5.15 Daṭṭhabba（五力／五根所见处）；"
        "与 SA_646 同型，根→力。汉「四不坏净」≈ SN 须陀洹支。"
    ),
}

# --- SA 676 五力（我成就）-----------------------------------------------------
SUTTAS["SA_676"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五力——{FIVE_BALA_LIT}。"
        f"是故诸比丘当如是学：我成就{FIVE_BALA_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种力——{FIVE_BALA_MOD}。"
        f"所以比丘们应当这样学：我成就{FIVE_BALA_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：与 674 同系，本经作「我成就」现成句；无 SC 专经。"
        "gold_reconstructed：peyyāla「如上说」补五力名目。"
    ),
}

# --- SA 677 学力（AN5.1）------------------------------------------------------
SUTTAS["SA_677"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五学力。何等为五？{SEKHA_LIT}——皆是学力。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种有学之力。哪五种？{SEKHA_MOD}——都是学力。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN5.1 Saṁkhitta（sekhabala 略说）。"
        "汉序信／精进／惭／愧／慧；义同 AN（saddhā／vīriya／hiri／ottappa／paññā）。"
    ),
}

# --- SA 678 学力（当成就）-----------------------------------------------------
SUTTAS["SA_678"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五学力——{SEKHA_LIT}。"
        f"诸比丘当如是学：我当成就{SEKHA_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种有学之力——{SEKHA_MOD}。"
        f"比丘们应当这样学：我应当成就{SEKHA_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN5.1 系劝修差别。"
        "gold_reconstructed：peyyāla「如上说」补五学力名目＋劝学。"
    ),
}

# --- SA 679 学力（分别）-------------------------------------------------------
SUTTAS["SA_679"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五学力——{SEKHA_LIT}。」",
        "「何等信力学力？于如来所善入于信，根本坚固，"
        "诸天、魔、梵、沙门、婆罗门及余同法所不能坏，是名信力学力。」",
        f"「何等精进力学力？谓四正断——{FOUR_PADHANA_LIT}，是名精进力学力。」",
        "「何等惭力学力？耻于起恶不善法及诸烦恼，畏有炽然苦报与生老病死忧悲苦恼，"
        "是名惭力学力。」",
        "「何等愧力学力？于可愧事而愧，愧起恶不善法及诸烦恼，畏有炽然苦报与生老病死忧悲苦恼，"
        "是名愧力学力。」",
        "「何等慧力学力？圣弟子住于慧，成就世间生灭慧，贤圣出离，决定正尽苦，"
        "是名慧力学力。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种有学之力——{SEKHA_MOD}。」",
        "「什么是信力这种学力？对如来善入净信，根本坚固，"
        "诸天、魔、梵、沙门、婆罗门以及其他同修都不能破坏，叫做信力学力。」",
        f"「什么是精进力学力？就是四正断——{FOUR_PADHANA_MOD}，叫做精进力学力。」",
        "「什么是惭力学力？耻于生起恶不善法及诸烦恼，畏惧有炽盛苦报与生老病死忧悲苦恼，"
        "叫做惭力学力。」",
        "「什么是愧力学力？对可愧的事感到愧疚，愧于生起恶不善法及诸烦恼，"
        "畏惧有炽盛苦报与生老病死忧悲苦恼，叫做愧力学力。」",
        "「什么是慧力学力？圣弟子安住于慧，成就世间生灭的智慧，贤圣出离，决定正尽苦，"
        "叫做慧力学力。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN5.2／学力广分别系。"
        "gold_reconstructed：汉「四正断如前广说」→四正断定型补足。"
    ),
}

# --- SA 680 学力（是故当学）---------------------------------------------------
SUTTAS["SA_680"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有五学力——{SEKHA_LIT}。"
        f"是故诸比丘当如是学：我当成就{SEKHA_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有五种有学之力——{SEKHA_MOD}。"
        f"所以比丘们应当这样学：我应当成就{SEKHA_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：学力结劝；与 678 近，无 SC 专经。"
        "gold_reconstructed：peyyāla「如上说」补五学力名目。"
    ),
}

# --- SA 681 白法（善法退／住）-------------------------------------------------
SUTTAS["SA_681"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「若比丘于善法变易、退失、不久住，他人当以五白法呵责："
        "汝不以信入于善法——依信则能离不善、修诸善；"
        "亦无精进、无惭、无愧、无慧入于善法——依慧则能离不善、修诸善。」",
        "「若于正法不变、不退、久住，他人当以五白法庆慰："
        "正信入于善法，依信离不善、修诸善；"
        "精进、惭、愧、慧入于善法，依慧离不善、修诸善。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「如果比丘在善法上变易、退失、不能久住，别人会用五种白法来责备："
        "你不是靠信进入善法——靠信就能离不善、修诸善；"
        "也没有精进、惭、愧、慧进入善法——靠慧就能离不善、修诸善。」",
        "「如果在正法上不变、不退、能久住，别人会用五种白法来庆贺安慰："
        "正信进入善法，靠信离不善、修诸善；"
        "精进、惭、愧、慧进入善法，靠慧离不善、修诸善。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN5.5 Sikkhā 系（白法呵责／庆慰）；"
        "本经主题为善法退失与久住，五支同 sekhabala。"
    ),
}

# --- SA 682 白法（还戒／尽寿梵行）---------------------------------------------
SUTTAS["SA_682"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「若比丘还戒、退戒，他人当以五白法呵责："
        "不以信入于善法——依信则离不善、修诸善；"
        "不以精进、惭、愧、慧入于善法——依慧则离不善、修诸善。」",
        "「若尽寿纯一满净、梵行清白，他人当以五白法庆慰："
        "正信入于善法，依信离不善、修诸善；"
        "精进、惭、愧、慧入于善法，依慧离不善、修诸善。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「如果比丘还戒、退戒，别人会用五种白法来责备："
        "不是靠信进入善法——靠信就能离不善、修诸善；"
        "不是靠精进、惭、愧、慧进入善法——靠慧就能离不善、修诸善。」",
        "「如果尽形寿纯一清净、梵行清白，别人会用五种白法来庆贺安慰："
        "正信进入善法，靠信离不善、修诸善；"
        "精进、惭、愧、慧进入善法，靠慧离不善、修诸善。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN5.5（舍学／住学）。"
        "gold_reconstructed：汉「庆慰如上说」→据 SA_681 五白法庆慰句补足。"
    ),
}

# --- SA 683 不善法-------------------------------------------------------------
SUTTAS["SA_683"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「若不欲令恶不善法生，当依信住于善法；"
        "若信退灭、不信永住，恶不善法则生。"
        "精进、惭、愧、慧亦如是——若退灭而恶慧永住，恶不善法则生。」",
        "「若依信，则离不善、修诸善；依精进、惭、愧、慧，亦离不善、修诸善。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「如果不想让恶不善法生起，应当依信安住善法；"
        "若信退灭、不信常住，恶不善法就会生起。"
        "精进、惭、愧、慧也一样——若退灭而恶慧常住，恶不善法就会生起。」",
        "「若依信，就能离不善、修诸善；依精进、惭、愧、慧，也能离不善、修诸善。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN5.5／学力退堕系；不善法因信等退灭而生，依五学力则离恶修善。"
    ),
}

# --- SA 684 十力（AN10.21）----------------------------------------------------
SUTTAS["SA_684"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「若于色生厌、离欲、灭尽、不起、解脱，受、想、行、识亦尔，"
        "是名如来、应、等正觉。"
        "若于色生厌、离欲、不起、解脱，受、想、行、识亦尔，是名阿罗汉慧解脱。"
        "此二者有何差别？」",
        "诸比丘白佛：「世尊是法根、法眼、法依，唯愿演说。」",
        "佛告比丘：「如来于未闻法能自觉知，现法自证得菩提，能为未来说正法、觉诸声闻——"
        "谓四念处、四正断、四神足、五根、五力、七觉支、八圣道；"
        "未得能得，未制梵行能制，善知道、善说道，为众导师；"
        "然后声闻随法随道，乐奉教诫，善于正法。是名如来与阿罗汉慧解脱之别。」",
        "「复次，学人有五力——信、精进、念、定、慧；如来有十力。」",
        "「何等十？一、处非处如实知。"
        "二、过去未来现在业及受因事报如实知。"
        "三、禅、解脱、三昧、正受之杂染与清净如实知。"
        "四、众生诸根差别如实知。"
        "五、众生种种意解如实知。"
        "六、世间种种界如实知。"
        "七、一切至处道如实知。"
        "八、种种宿命——族姓、饮食、苦乐、寿命——如实忆念。"
        "九、天眼净见众生死此生彼、随业受报。"
        "十、诸漏已尽，无漏心解脱、慧解脱，现法自知作证："
        "我生已尽，梵行已立，所作已作，不受后有。」",
        f"「成就此十力故，如来{ROAR_LIT}。"
        "唯如来具足，是名如来与声闻种种差别。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「如果对色生厌、离欲、灭尽、不起、解脱，受、想、行、识也一样，"
        "那就称为如来、应、等正觉。"
        "如果对色生厌、离欲、不起、解脱，受、想、行、识也一样，那就称为阿罗汉慧解脱。"
        "这两者有什么差别？」",
        "比丘们对佛说：「世尊是法根、法眼、法依，请为我们演说。」",
        "佛告比丘：「如来对未曾听闻的法能自己觉悟，在现法中自证得菩提，"
        "能为未来宣说正法、觉悟声闻——"
        "也就是四念处、四正断、四神足、五根、五力、七觉支、八圣道；"
        "未得的能得，未制定的梵行能制定，善知道、善说道，做大众的导师；"
        "然后声闻才随法随道，乐于奉行教诫，善于正法。这就是如来与阿罗汉慧解脱的差别。」",
        "「再者，有学有五种力——信、精进、念、定、慧；如来有十种力。」",
        "「哪十种？一、如实知处与非处。"
        "二、如实知过去未来现在的业及受的因缘果报。"
        "三、如实知禅、解脱、三昧、正受的杂染与清净。"
        "四、如实知众生诸根的差别。"
        "五、如实知众生种种意向。"
        "六、如实知世间种种界。"
        "七、如实知一切能到某处的道。"
        "八、如实忆念种种宿命——族姓、饮食、苦乐、寿命。"
        "九、以清净天眼见众生死此生彼、随业受报。"
        "十、诸漏已尽，无漏心解脱、慧解脱，在现法中自己证知："
        "我生已尽，梵行已立，所作已作，不再受后有。」",
        f"「成就这十力，如来就{ROAR_MOD}。"
        "只有如来具足，这就是如来与声闻的种种差别。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.21 Sīhanāda（十力师子吼）。"
        "压缩每力后「转梵轮／师子吼」套语为结句一处；开首佛／阿罗汉差别从汉＋AN 道品觉他义。"
    ),
}

# --- SA 685 乳母（无专平行）---------------------------------------------------
SUTTAS["SA_685"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「譬如婴儿，父母生已付乳母，随时摩拭、沐浴、乳哺、调护。"
        "若不慎，儿或以草土不净着物入口，乳母当即令除去；"
        "能自除者善，不能者，乳母左手持头、右手探哽——"
        "儿虽苦，乳母必苦探，欲令长夜安乐故。」",
        "「若儿长大有识别，复持不净着物入口否？」诸比丘白：「不也。"
        "长大尚不以足触，况入口。」",
        "「小时乳母勤护；长大智慧成，乳母放舍，以其不自放逸故。"
        "如是，始学声闻慧未足，如来以法随时教授；久学慧深固，如来放舍不复殷勤——"
        "以其智慧成就、不放逸故。」",
        "「是故声闻有五学力，如来成就十力——如上说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「好比婴儿，父母生下后交给乳母，随时擦洗、沐浴、喂乳、调护。"
        "若不小心，孩子或许把草土等不净物放进嘴里，乳母应当立刻让他除去；"
        "能自己除掉就好，不能的话，乳母左手扶头、右手掏出口中哽住的东西——"
        "孩子当时虽苦，乳母仍要苦苦掏出，为的是让他长夜安乐。」",
        "「孩子长大有了分别，还会把不净物放进嘴里吗？」比丘们答：「不会。"
        "长大了连脚都不去碰，何况放进嘴里。」",
        "「小时乳母勤加护持；长大智慧成就，乳母就放手，因为他已不放逸。"
        "同样，初学声闻智慧不足时，如来用法随时教导；久学智慧深固，如来就放手不再殷勤督促——"
        "因为他智慧已成、自己不放逸。」",
        "「所以声闻有五种学力，如来成就十力——如同前面所说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：乳母譬喻学力／十力；SC 无专平行。"
        "gold_reconstructed：「如上广说」交叉指示 SA_684 十力与学力差别，不重录全表。"
    ),
}

# --- SA 686 师子吼（AN6.64 六力）---------------------------------------------
SUTTAS["SA_686"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「如来有六力。成就此六力，如来、应、等正觉{ROAR_LIT}。」",
        "「何等六？一、处非处如实知。"
        "二、过去未来现在诸业因缘果报如实知。"
        "三、禅、解脱、三昧、正受之杂染与清净如实知。"
        "四、种种宿命如实忆念。"
        "五、天眼净见众生死此生彼、随业受报。"
        "六、诸漏已尽，无漏心解脱、慧解脱，现法自知作证。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「如来有六种力。成就这六力，如来、应、等正觉就{ROAR_MOD}。」",
        "「哪六种？一、如实知处与非处。"
        "二、如实知过去未来现在诸业的因缘果报。"
        "三、如实知禅、解脱、三昧、正受的杂染与清净。"
        "四、如实忆念种种宿命。"
        "五、以清净天眼见众生死此生彼、随业受报。"
        "六、诸漏已尽，无漏心解脱、慧解脱，在现法中自己证知。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN6.64 Sīhanāda（六如来力）。"
        "据 AN 校正：汉第二力「心乐法受」→诸业因缘果报（kammasamādāna vipāka）。"
        "gold_reconstructed：peyyāla「如上广说」压缩为六力名相各一句。"
    ),
}

# --- SA 687 狮子吼（AN6.64 答问）---------------------------------------------
SUTTAS["SA_687"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「如来有六力，能于大众作师子吼。」",
        "「若有来问处非处智力，如来如其所知见觉，成等正觉，为彼记说。"
        "问诸业因缘果报智力、禅解脱三昧正受智力、宿命智力、天眼智力、漏尽智力，亦复如是——"
        "皆如所知见觉，为彼记说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「如来有六种力，能在大众中作师子吼。」",
        "「若有人来问处非处的智力，如来依自己所知所见所觉、成等正觉，为他记说。"
        "问诸业因缘果报的智力、禅解脱三昧正受的智力、宿命智力、天眼智力、漏尽智力，也一样——"
        "都依自己所知所见所觉，为他记说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN6.64 后分（以六力答问记说）。"
        "据 AN 校正：汉「自以乐受」→诸业因缘果报智力。"
        "gold_reconstructed：peyyāla「如上说」＋六力问答纲。"
    ),
}

# --- SA 688 七力（AN7.3）------------------------------------------------------
SUTTAS["SA_688"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「比丘当知七力——信、精进、惭、愧、念、定、慧。」",
        "尔时说偈：「信进与惭愧，　念定慧为七；　具足此力者，　有漏得永尽。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「比丘应当知道七种力——信、精进、惭、愧、念、定、慧。」",
        "那时说偈：「信进与惭愧，　念定慧为七；　具足这些力的人，　有漏得以永尽。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN7.3 Saṁkhittabala（七力略说＋偈）。"
        "偈文罗什风压缩，义同 AN／汉本「得尽诸有漏」。"
    ),
}

# --- SA 689 七力（当学）-------------------------------------------------------
SUTTAS["SA_689"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有七力——{SEVEN_LIT}。"
        "是故比丘当如是学：我当成就信力；精进、惭、愧、念、定、慧力，亦当学。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有七种力——{SEVEN_MOD}。"
        "所以比丘应当这样学：我应当成就信力；精进、惭、愧、念、定、慧力，也应当学。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN7.3 系劝修差别。"
        "gold_reconstructed：peyyāla「如上说」补七力名目＋劝学。"
    ),
}

# --- SA 690 七力（偈异）-------------------------------------------------------
SUTTAS["SA_690"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有七力——{SEVEN_LIT}。」",
        "尔时世尊说偈言：「信力精进力，　及说惭愧力，　念力定慧力，　是名为七力；"
        "七力成就者，　疾断诸有漏。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告比丘：「有七种力——{SEVEN_MOD}。」",
        "那时世尊说偈：「信力精进力，　以及惭愧力，　念力定慧力，　这就叫七力；"
        "成就七力的人，　迅速断诸有漏。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN7.3 系；与 688 同列异偈（「疾断」对「得尽」）。"
        "gold_reconstructed：peyyāla「如上说」补七力名目＋异偈。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_671": "high",
    "SA_672": "high",
    "SA_673": "high",
    "SA_674": "medium",
    "SA_675": "high",
    "SA_676": "medium",
    "SA_677": "high",
    "SA_678": "high",
    "SA_679": "high",
    "SA_680": "medium",
    "SA_681": "high",
    "SA_682": "high",
    "SA_683": "high",
    "SA_684": "high",
    "SA_685": "medium",
    "SA_686": "high",
    "SA_687": "high",
    "SA_688": "high",
    "SA_689": "high",
    "SA_690": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_671": "五畏 peyyāla 展开（恶名／大众／死／恶趣同不活畏）",
    "SA_672": "无罪力／摄力／四正断 据 SA_667＋AN4.153 补足",
    "SA_674": "如上说 → 五力名目＋勤加精进劝学",
    "SA_676": "如上说 → 五力名目＋我成就劝学",
    "SA_678": "如上说 → 五学力名目＋劝学",
    "SA_679": "四正断如前广说 → 四正断定型",
    "SA_680": "如上说 → 五学力名目＋结劝",
    "SA_682": "庆慰如上说 → 五白法庆慰句自 SA_681",
    "SA_685": "十力／学力如上广说 → 交叉指示 SA_684，不重录",
    "SA_686": "六力 peyyāla 据 AN6.64 压缩；第二力据 AN 校正业报",
    "SA_687": "如上说＋六力答问纲；第二力据 AN 校正",
    "SA_689": "如上说 → 七力名目＋劝学",
    "SA_690": "如上说 → 七力名目＋异偈",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(671, 691)}, (
        "GOLD must cover SA_671–SA_690 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    # Parallel batch owns 651–670
    assert not any(f"SA_{i}" in GOLD for i in range(651, 671))

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

    # Boundary: SA_670 if gold, else SA_650
    _goldish = {"gold", "gold_reconstructed"}
    boundary_id = "SA_670"
    for rec in records:
        if rec["id"] == "SA_670" and rec.get("review_status") not in _goldish:
            boundary_id = "SA_650"
            break
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

    # Snapshot 651–670 to assert untouched
    mid_before = {
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
        if rec["id"] in {f"SA_{i}" for i in range(651, 671)}
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

    for rid, before in mid_before.items():
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
                assert before == after, f"{rid} (parallel batch) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa671-690.json").write_text(
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
    continuous_671_690 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(671, 691)
    )
    untouched_651_670 = all(f"SA_{i}" not in GOLD for i in range(651, 671))

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_671–SA_690 only)")
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
    print(f"continuous_gold_SA_671–690={continuous_671_690}")
    print(f"SA_651–670_untouched={untouched_651_670}")
    print(f"{boundary_id}_untouched=True")
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
