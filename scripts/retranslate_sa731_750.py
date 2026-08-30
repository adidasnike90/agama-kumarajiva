#!/usr/bin/env python3
"""Retranslate SA 731–750（觉支相应末–圣道分相应起）→ merge.

本批二十经：支节／起 SN46.10；七道品×2 SN46.5；果报 variants（二／四／七果）；
不净观 SN46.67；死念 SN46.68；慈 SN46.54／62；灭（空等至，无专平行）；
安那般那念 SN46.66；无常想 SN46.71 系；日出 SN45.55；无明×2 SN45.1。

信：有 SN 平行者据巴利／Sujato 厘义；无专经 → medium。
    peyyāla／交叉指示补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_731–750；断言 SA_730 不变；不触碰 SA_751+。
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

SEVEN_LIT = "念觉支、择法觉支、精进觉支、喜觉支、轻安觉支、定觉支、舍觉支"
SEVEN_MOD = "念觉支、择法觉支、精进觉支、喜觉支、轻安觉支、定觉支、舍觉支"

NISSAYA_LIT = "依远离、依离欲、依灭、向于舍"
NISSAYA_MOD = "依于远离、依于离欲、依于灭、而趋向舍"

EIGHT_LIT = "正见、正思惟、正语、正业、正命、正精进、正念、正定"
EIGHT_MOD = "正见、正思惟、正语、正业、正命、正精进、正念、正定"

WRONG_LIT = "邪见、邪思惟、邪语、邪业、邪命、邪精进、邪念、邪定"
WRONG_MOD = "邪见、邪思惟、邪语、邪业、邪命、邪精进、邪念、邪定"

LIB_LIT = (
    "圣弟子心正解脱贪欲、瞋恚、愚癡；得正知見："
    "『我生已尽，梵行已立，所作已作，自知不受后有。』"
)
LIB_MOD = (
    "圣弟子的心正解脱贪欲、瞋恚、愚痴；得正知見："
    "『我生已尽，梵行已立，所作已作，自己知道不再受后有。』"
)

# 某想／观俱修七觉支
def _saññā_body_lit(topic: str) -> str:
    return (
        f"「云何修习？心与{topic}俱，修念觉支，{NISSAYA_LIT}；"
        f"择法、精进、喜、轻安、定、舍觉支，亦{NISSAYA_LIT}。」"
    )


def _saññā_body_mod(topic: str) -> str:
    return (
        f"「怎样修习？心与{topic}一起，修念觉支，{NISSAYA_MOD}；"
        f"择法、精进、喜、轻安、定、舍觉支，也{NISSAYA_MOD}。」"
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

# --- SA 731 支节（SN46.10）----------------------------------------------------
SUTTAS["SA_731"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有七觉支——{SEVEN_LIT}。"
        "此七觉支清净鲜白，无有支节，离诸烦恼；"
        "未生者，除佛调伏教授则不生；若生，唯佛调伏教授，非余。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告诉比丘：「有七觉支——{SEVEN_MOD}。"
        "这七觉支清净鲜白，没有支节残缺，离开一切烦恼；"
        "还没生起的，除了佛的调伏教授就不会生；若生起，也只靠佛的调伏教授，不是别的。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.10 Dutiyauppanna"
        "（七觉支未生而起，唯在善逝调伏／sugatavinaya）。"
        "据 SN 校正汉本交错「未起不起／未起而起」句；觉分→觉支；"
        "保留汉题「支节」与「清净鲜白、无有支节」传统用语。"
    ),
}

# --- SA 732 起（peyyāla；善逝）------------------------------------------------
SUTTAS["SA_732"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有七觉支——{SEVEN_LIT}。"
        "未生者，除善逝调伏教授则不生；若生，是善逝调伏教授，非余。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告诉比丘：「有七觉支——{SEVEN_MOD}。"
        "还没生起的，除了善逝的调伏教授就不会生；若生起，就是善逝的调伏教授，不是别的。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：与 SA_731 同本 SN46.10；差别在「佛／善逝」。"
        "gold_reconstructed：汉「如上说。差别者」peyyāla → 补七觉支名＋善逝句。"
    ),
}

# --- SA 733 七道品（异比丘问；SN46.5 系／汉本渐次起）--------------------------
SUTTAS["SA_733"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘来诣佛所，稽首礼足，退坐一面，白佛言："
        "「世尊说觉支。云何为觉支？」",
        "佛告比丘：「趣向于觉，故名觉支。所谓七道品法——七觉支。"
        f"修{SEVEN_LIT}，{NISSAYA_LIT}，能渐次起、修习满足。」",
        "比丘复问：「云何渐次起、修习满足？」",
        "佛言：「若比丘内身循身观，摄心系念不忘，尔时方便修念觉支，念满足；"
        "于法简择分别，修择法觉支；乃至精进、喜、轻安、定、舍，次第满足。"
        "外身、内外身，受、心、法循法观，亦复如是。"
        "如是住者，七觉支渐次起，起已修习满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘来到佛所，叩头礼足，坐在一边，对佛说："
        "「世尊说觉支。什么是觉支？」",
        "佛告诉比丘：「因为趣向于觉，所以叫觉支。也就是七道品法——七觉支。"
        f"修{SEVEN_MOD}，{NISSAYA_MOD}，能渐渐生起、修习满足。」",
        "比丘又问：「怎样渐渐生起、修习满足？」",
        "佛说：「如果比丘对内身循身观察，把心收摄、系念不忘，这时方便修念觉支，念满足；"
        "对法简择分别，修择法觉支；一直到精进、喜、轻安、定、舍，按次第满足。"
        "外身、内外身，以及受、心、法循法观察，也是一样。"
        "这样安住，七觉支就渐渐生起，生起后修习满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SC primary SN46.5 Bhikkhu（趣向觉故名觉支＋{NISSAYA_LIT}）；"
        "汉本更广，以四念处起七觉支渐次链——早期定型，予保留。"
        "据 SN 补「趣向于觉」定义；觉分→觉支；猗→轻安。"
    ),
}

# --- SA 734 果报（二果；对异比丘）---------------------------------------------
SUTTAS["SA_734"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘来问觉支。佛为说七觉支渐次满足已，告言：",
        f"「若修习七觉支——{SEVEN_LIT}——多修习已，当期二果："
        "或现法得智、漏尽；或有余依而得阿那含果。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘来问觉支。佛为他说了七觉支渐渐满足之后，告诉他：",
        f"「若修习七觉支——{SEVEN_MOD}——多多修习，可以期望两种果："
        "或者现法得智、漏尽；或者还有余依而证得阿那含果。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：果报结构合 SN48.65 系二果"
        "（diṭṭheva dhamme aññā／upādisese anāgāmitā），所修为七觉支（本相应）。"
        "据 SN 校正汉「无余涅槃／阿那含」交错；"
        "gold_reconstructed：汉「如上。差别者」→补问答框与七支。"
    ),
}

# --- SA 735 果报（四果；异比丘）-----------------------------------------------
SUTTAS["SA_735"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘问修七觉支之果。佛告言：",
        f"「修习七觉支——{SEVEN_LIT}——多修习已，得四果、四福利："
        "须陀洹果、斯陀含果、阿那含果、阿罗汉果。」",
        "异比丘闻已，欢喜奉行。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘问修七觉支的果报。佛告诉他：",
        f"「修习七觉支——{SEVEN_MOD}——多多修习，得四种果、四种福利："
        "须陀洹果、斯陀含果、阿那含果、阿罗汉果。」",
        "那位比丘听完，欢喜奉行。",
    ],
    "notes": (
        f"{PROV}confidence=high：四沙门果合 SN48.12 系略说；所修为七觉支。"
        "gold_reconstructed：汉「如上说。差别者」→补开场与七支名。"
    ),
}

# --- SA 736 七种果（异比丘）---------------------------------------------------
SUTTAS["SA_736"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘问修七觉支之果。佛告言：",
        f"「修习七觉支——{SEVEN_LIT}——多修习已，当得七种果、七种福利。"
        "何等为七？现法得智证乐；若命终时得；"
        "若不得者，五下分结尽，得中般涅槃；"
        "若不得中般，得生般涅槃；"
        "若不得生般，得无行般涅槃；"
        "若不得无行般，得有行般涅槃；"
        "若不得有行般，得上流般涅槃。」",
        "异比丘闻已，欢喜奉行。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘问修七觉支的果报。佛告诉他：",
        f"「修习七觉支——{SEVEN_MOD}——多多修习，当得七种果、七种福利。"
        "哪七种？现法得智证之乐；或者在命终时得到；"
        "若还得不到，断尽五下分结，得中般涅槃；"
        "若不得中般，得生般涅槃；"
        "若不得生般，得无行般涅槃；"
        "若不得无行般，得有行般涅槃；"
        "若不得有行般，得上流般涅槃。」",
        "那位比丘听完，欢喜奉行。",
    ],
    "notes": (
        f"{PROV}confidence=high：七果合 SN46.3 末（anāgāmin 五类＋现法／命终智）；"
        "SC resembling SN46.3。gold_reconstructed：汉「如上说。差别者」→补开场与七支；"
        "理顺汉「现法／命终」交错句。"
    ),
}

# --- SA 737 七道品（告诸比丘）-------------------------------------------------
SUTTAS["SA_737"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「所谓觉支——何等为觉支？」"
        "诸比丘白佛：「世尊是法根、法眼、法依，唯愿演说，我等闻已当受奉行。」",
        f"佛言：「七觉支者，谓七道品法——{SEVEN_LIT}。"
        f"修此七支，{NISSAYA_LIT}，渐次起，起已修习满足。」",
        "「云何渐次起？若比丘身循身观，专心系念不忘，方便修念觉支，念满足；"
        "于法简择，修择法觉支；精进、喜、轻安、定、舍，亦如是。"
        "内身、外身、内外身，受、心、法循法观，亦复如是。"
        "是名七觉支渐次起，起已修习满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「所谓觉支——什么是觉支？」"
        "比丘们对佛说：「世尊是法根、法眼、法依，请为我们说，我们听了会受持奉行。」",
        f"佛说：「七觉支，就是七道品法——{SEVEN_MOD}。"
        f"修这七支，{NISSAYA_MOD}，渐渐生起，生起后修习满足。」",
        "「怎样渐渐生起？如果比丘对身循身观察，专心系念不忘，方便修念觉支，念满足；"
        "对法简择，修择法觉支；精进、喜、轻安、定、舍，也是一样。"
        "内身、外身、内外身，以及受、心、法循法观察，也是一样。"
        "这叫七觉支渐渐生起，生起后修习满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：与 SA_733 同系（SN46.5 resembling）；"
        "本经佛自问自答告大众，有「法根法眼法依」请法套语。"
        "猗→轻安；觉分→觉支。"
    ),
}

# --- SA 738 果报（二果；告诸比丘）---------------------------------------------
SUTTAS["SA_738"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「修习七觉支——{SEVEN_LIT}——多修习已，当期二果："
        "或现法得智；或有余依而得阿那含果。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告诉比丘：「修习七觉支——{SEVEN_MOD}——多多修习，可以期望两种果："
        "或者现法得智；或者还有余依而证得阿那含果。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：与 SA_734 同二果义（SN48.65 系），告大众。"
        "据 SN 校正汉「现法智有余涅槃及阿那含」含混句；"
        "gold_reconstructed：peyyāla「如上说」→列七支＋二果。"
    ),
}

# --- SA 739 果报（四果；告诸比丘）---------------------------------------------
SUTTAS["SA_739"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「修习七觉支——{SEVEN_LIT}——多修习已，当得四果："
        "须陀洹果、斯陀含果、阿那含果、阿罗汉果。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告诉比丘：「修习七觉支——{SEVEN_MOD}——多多修习，当得四果："
        "须陀洹果、斯陀含果、阿那含果、阿罗汉果。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：与 SA_735 同四果；告大众。"
        "gold_reconstructed：peyyāla「如上说」→列七支＋四果。"
    ),
}

# --- SA 740 果报（七果；告诸比丘）---------------------------------------------
SUTTAS["SA_740"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「修习七觉支——{SEVEN_LIT}——多修习已，当得七果。"
        "何等为七？现法得智；或命终时得；"
        "若不得者，五下分结尽，得中般涅槃；"
        "若不得中般，得生般涅槃；"
        "若不得生般，得无行般涅槃；"
        "若不得无行般，得有行般涅槃；"
        "若不得有行般，得上流般涅槃。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告诉比丘：「修习七觉支——{SEVEN_MOD}——多多修习，当得七果。"
        "哪七种？现法得智；或者在命终时得到；"
        "若还得不到，断尽五下分结，得中般涅槃；"
        "若不得中般，得生般涅槃；"
        "若不得生般，得无行般涅槃；"
        "若不得无行般，得有行般涅槃；"
        "若不得有行般，得上流般涅槃。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：与 SA_736 同七果（SN46.3 末）；告大众。"
        "gold_reconstructed：汉「如上说。差别者」→补七支名；理顺果次。"
    ),
}

# --- SA 741 不净观（SN46.67）--------------------------------------------------
SUTTAS["SA_741"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当修不净观，多修习已，得大果大福利。」",
        _saññā_body_lit("不净观"),
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「应当修不净观，多多修习，能得大果大福利。」",
        _saññā_body_mod("不净观"),
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.67 Asubha"
        "（asubhasaññā＋七觉支＋{NISSAYA_LIT}）。猗→轻安；觉分→觉支。"
    ),
}

# --- SA 742 死念（SN46.68）----------------------------------------------------
SUTTAS["SA_742"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当修死想，多修习已，得大果大福利。」",
        _saññā_body_lit("死想"),
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「应当修死想，多多修习，能得大果大福利。」",
        _saññā_body_mod("死想"),
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.68 Maraṇa（maraṇasaññā）。"
        "汉「随死念」据 SN 作「死想」；gold_reconstructed：乃至舍觉分→七支全列。"
    ),
}

# --- SA 743 慈（外道对扬；SN46.54）--------------------------------------------
SUTTAS["SA_743"] = {
    "lit": [
        "如是我闻：一时，佛住释氏黄枕邑。",
        "时众多比丘晨朝着衣持钵，入邑乞食。以时尚早，过外道精舍，共相问讯，于一面坐。",
        "外道言：「瞿昙教弟子断五盖、住四念处，修慈、悲、喜、舍，遍满十方；我等亦尔。有何异？」"
        "诸比丘不喜，默然乞食已，还白世尊。",
        "佛告比丘：「彼若作是说，当问：修慈心，何所最胜？修悲、喜、舍，何所最胜？"
        "如是问者，彼则骇散，不能善答。除如来及声闻众，我不见余众闻此能随喜。」",
        "「诸比丘！心与慈俱多修习，于净最胜；"
        "悲心多修习，空无边处最胜；"
        "喜心多修习，识无边处最胜；"
        "舍心多修习，无所有处最胜。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在释氏黄枕邑。",
        "那时许多比丘清晨穿衣持钵，进城乞食。因为时间还早，就经过外道精舍，互相问候，坐在一边。",
        "外道说：「瞿昙教弟子断五盖、住四念处，修慈、悲、喜、舍，遍满十方；我们也是这样。有什么不同？」"
        "比丘们心里不高兴，默默乞食回来后，把这话告诉世尊。",
        "佛告诉比丘：「他们若这样说，你们应当问：修慈心，以什么为最胜？修悲、喜、舍，以什么为最胜？"
        "这样一问，他们就会慌乱，答不好。除了如来和声闻众，我没看见别人听了这个能随喜。」",
        "「诸比丘！心与慈一起多多修习，以净为最胜；"
        "悲心多多修习，以空无边处为最胜；"
        "喜心多多修习，以识无边处为最胜；"
        "舍心多多修习，以无所有处为最胜。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.54 Mettāsahagata"
        "（慈→净／subha；悲→空无边；喜→识无边；舍→无所有）。"
        "罗什风压缩外道对扬与四无量遍满套语；汉「空／识／无所有入处」据 SN 作「处」。"
        "SN 广说解脱自在及与觉支俱修，本经从汉略本要点。"
    ),
}

# --- SA 744 慈（想俱觉支；SN46.62）--------------------------------------------
SUTTAS["SA_744"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当修慈心，多修习已，得大果大福利。」",
        _saññā_body_lit("慈"),
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「应当修慈心，多多修习，能得大果大福利。」",
        _saññā_body_mod("慈"),
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.62 Mettā"
        "（mettā＋七觉支＋{NISSAYA_LIT}）。"
        "gold_reconstructed：乃至舍觉分→七支全列。"
    ),
}

# --- SA 745 灭（空等至；无专平行）---------------------------------------------
SUTTAS["SA_745"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当修空无边处，多修习已，得大果大福利。」",
        _saññā_body_lit("空无边处"),
        CLOSE_BH_LIT,
        "如空无边处，识无边处、无所有处、非想非非想处——三经亦如上说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「应当修空无边处，多多修习，能得大果大福利。」",
        _saññā_body_mod("空无边处"),
        CLOSE_BH_MOD,
        "像空无边处这样，识无边处、无所有处、非想非非想处——三部经也如同上面所说。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：题作「灭」，正文为空等至与觉支俱修；"
        "参 SN46 想品定型（saññā／āyatana＋bojjhaṅga）。"
        "gold_reconstructed：汉「入处」统一为「处」；peyyāla 三经注记保留。"
    ),
}

# --- SA 746 安那般那念（SN46.66）----------------------------------------------
SUTTAS["SA_746"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当修安那般那念，多修习已，得大果大福利。」",
        _saññā_body_lit("安那般那念"),
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「应当修安那般那念（出入息念），多多修习，能得大果大福利。」",
        _saññā_body_mod("安那般那念"),
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.66 Ānāpāna。"
        "gold_reconstructed：乃至舍觉分→七支全列。"
    ),
}

# --- SA 747 无常（SN46.71 系；peyyāla 诸想）-----------------------------------
SUTTAS["SA_747"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当修无常想，多修习已，得大果大福利。」",
        _saññā_body_lit("无常想"),
        CLOSE_BH_LIT,
        "如无常想，如是无常苦想、苦无我想、食厌想、一切世间不可乐想、"
        "尽想、断想、离贪想、灭想、患想、不净想，"
        "青瘀想、脓烂想、膨胀想、坏想、啖残想、血涂想、离散想、骨想、空想——"
        "一一经亦如上说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「应当修无常想，多多修习，能得大果大福利。」",
        _saññā_body_mod("无常想"),
        CLOSE_BH_MOD,
        "像无常想这样，还有无常苦想、苦无我想、对食物的厌想、一切世间不可乐想、"
        "尽想、断想、离贪想、灭想、患想、不净想，"
        "以及青瘀想、脓烂想、膨胀想、坏想、啖残想、血涂想、离散想、骨想、空想——"
        "每一部经也如同上面所说。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary 近 SN46.71 Anicca（及想品 SN46.57–76 同轨）；"
        "汉「心口与无常想俱」据 SN 作「心与…俱」。"
        "「厌故离贪」：尽／断／离贪／灭诸想从 SN virāga／nirodha 系，不用「厌故不乐」。"
        "gold_reconstructed：peyyāla 诸想名目据汉列＋SN 想品校理（食厌、离贪等）。"
    ),
}

# --- SA 748 日出（SN45.55；圣道分起）------------------------------------------
SUTTAS["SA_748"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「如日出前相，谓明相初光。"
        "如是正尽苦边、究竟苦边之前相，所谓如理作意。"
        "成就如理作意者，当修习多修习八支圣道——"
        f"{EIGHT_LIT}，各{NISSAYA_LIT}。」",
        f"「正定起已，{LIB_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「好比太阳升起之前的预兆，就是黎明的初光。"
        "同样，正尽苦边、究竟苦边的前相，就是如理作意。"
        "成就如理作意的人，应当修习、多多修习八支圣道——"
        f"{EIGHT_MOD}，每一支都{NISSAYA_MOD}。」",
        f"「正定生起之后，{LIB_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.55 Yonisomanasikārasampadā"
        "（如理作意＝八道前相，如明相之于日出）。"
        "据 SN 校正汉以「正见」为前相——本作如理作意；保留汉「正尽苦边」框架。"
        "正志→正思惟、正方便→正精进；结以解脱智见为 SA 常套。"
    ),
}

# --- SA 749 无明（SN45.1）-----------------------------------------------------
SUTTAS["SA_749"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「无明为前相，生诸恶不善法，无惭无愧随生；"
        f"无惭无愧生已，起邪见；邪见起已，能起{WRONG_LIT}。」",
        "「明为前相，生诸善法，惭愧随生；"
        f"惭愧生已，能生正见；正见生已，起{EIGHT_LIT}，次第而起。」",
        f"「正定起已，{LIB_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「无明作为前相，生起各种恶不善法，无惭无愧跟着生起；"
        f"无惭无愧生起后，生起邪见；邪见生起后，就能生起{WRONG_MOD}。」",
        "「明作为前相，生起各种善法，惭愧跟着生起；"
        f"惭愧生起后，能生正见；正见生起后，就生起{EIGHT_MOD}，按次第生起。」",
        f"「正定生起之后，{LIB_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.1 Avijjā"
        "（无明→无惭无愧→邪道；明→惭愧→正道）。"
        "正志／正方便据罗什常译作正思惟／正精进；"
        "汉有解脱智见收束，SN 止于正定——从汉相应结。"
    ),
}

# --- SA 750 无明（广释；无专平行）---------------------------------------------
SUTTAS["SA_750"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「诸恶不善法，皆以无明为根本——无明集、无明生、无明起。"
        "所以者何？无明者，无知：于善、不善，有罪、无罪，下法、上法，"
        "染污、不染污，有分别、无分别，缘起、非缘起，不如实知；"
        f"不如实知故起邪见，邪见起已，能起{WRONG_LIT}。」",
        "「诸善法生，皆以明为根本——明集、明生、明起。"
        "明者，于善、不善，罪、无罪，亲近、不亲近，卑法、胜法，"
        "秽污、白净，有分别、无分别，缘起、非缘起，悉如实知；"
        f"如实知故是正见，正见能起{EIGHT_LIT}。」",
        f"「正定起已，圣弟子正解脱贪、恚、痴；{LIB_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「各种恶不善法，都以无明为根本——由无明集、无明生、无明起。"
        "为什么？无明就是无知：对善与不善，有罪与无罪，下法与上法，"
        "染污与不染污，有分别与无分别，缘起与非缘起，不能如实知；"
        f"因为不如实知而起邪见，邪见生起后，就能生起{WRONG_MOD}。」",
        "「各种善法生起，都以明为根本——由明集、明生、明起。"
        "明，就是对善与不善，罪与无罪，该亲近与不该亲近，卑法与胜法，"
        "秽污与白净，有分别与无分别，缘起与非缘起，都能如实知；"
        f"如实知就是正见，正见能生起{EIGHT_MOD}。」",
        f"「正定生起之后，圣弟子正解脱贪、瞋、痴；{LIB_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；广释无明＝不如实知诸法，"
        "明＝如实知→正见→八道，与 SA_749／SN45.1 同轨而加分别。"
        "罗什风删汉「若比丘」赘呼；正志→正思惟。"
    ),
}

# ---------------------------------------------------------------------------
# Confidence / reconstruction
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_731": "high",
    "SA_732": "high",
    "SA_733": "high",
    "SA_734": "high",
    "SA_735": "high",
    "SA_736": "high",
    "SA_737": "high",
    "SA_738": "high",
    "SA_739": "high",
    "SA_740": "high",
    "SA_741": "high",
    "SA_742": "high",
    "SA_743": "high",
    "SA_744": "high",
    "SA_745": "medium",
    "SA_746": "high",
    "SA_747": "high",
    "SA_748": "high",
    "SA_749": "high",
    "SA_750": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_732": "peyyāla「如上说」→ 七觉支＋善逝调伏教授句（SN46.10）",
    "SA_734": "peyyāla「如上」→ 异比丘问＋七支＋二果（据 SN 校）",
    "SA_735": "peyyāla「如上说」→ 异比丘问＋七支＋四果",
    "SA_736": "peyyāla「如上说」→ 异比丘问＋七支＋七果理顺",
    "SA_738": "peyyāla「如上说」→ 七支＋二果（据 SN 校）",
    "SA_739": "peyyāla「如上说」→ 七支＋四果",
    "SA_740": "peyyāla「如上说」→ 七支＋七果理顺",
    "SA_742": "乃至舍觉分 → 七觉支全列＋nissaya",
    "SA_744": "乃至舍觉分 → 七觉支全列＋nissaya",
    "SA_745": "空等至＋peyyāla 三处注记；无专平行",
    "SA_746": "乃至舍觉分 → 七觉支全列＋nissaya",
    "SA_747": "无常想正文＋peyyāla 诸想名目校理",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(731, 751)}, (
        "GOLD must cover SA_731–SA_750 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    assert not any(f"SA_{i}" in GOLD for i in range(751, 800))
    assert "SA_730" not in GOLD

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

    # Boundary: SA_730 must remain untouched
    boundary_id = "SA_730"
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

    # Snapshot SA_751+ to assert untouched
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
        if rec["id"].startswith("SA_")
        and int(rec["id"].split("_")[1]) >= 751
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
                assert before == after, f"{rid} (SA_751+) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa731-750.json").write_text(
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
    continuous_731_750 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(731, 751)
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_731–SA_750 only)")
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
    print(f"continuous_gold_SA_731–750={continuous_731_750}")
    print(f"SA_730_untouched=True")
    print(f"SA_751+_untouched=True")
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
