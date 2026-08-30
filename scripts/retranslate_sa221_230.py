#!/usr/bin/env python3
"""Retranslate SA 221–230（卷第九末／卷第十首 六入處相應，信>达>雅）→ merge into final_translated_data.json.

本批十经承前批（SA 201–220）而下，仍属六入處相應：取（SA 221）、智识×2（222/223）、
断×2（224/225）、计×2（226/227）、增长（228）、有漏无漏（229）；SA 230 三弥离提
为卷第十之首经（Anālayo 前篇 Fascicle 8 止于 SA 229）。

信：`raw_aligned_data.json` 内备巴利本文、Sujato 英译；SA 221–229 并有 Anālayo 之 SA 英译
    （'On the Six Sense-spheres (1) — A Translation of Saṁyukta-āgama Discourses 188 to 229
    (Fascicle 8)', DDJBS 18, 2016）。凡改求那跋陀罗字面者于 notes 具志所据。
达：白话与罗什风逐段对照，段数严格相同（build 时 assert，merge 时记 paragraph_parallel）。
雅：文言栏与底本之三元组相似度须 < 0.55，否则记 needs_restyle（繁转简闸）。

Confidence 判准（承前批：所量者为「平行可据以厘定本经法义之程度」）：
- high：SC 所列 `full` 平行之巴利本文／英译逐句覆盖本经正文（容汉本省文与语面之异）。
- medium：SC 未列平行（SA 221/228/229），或所列平行之公式与本经实不相当（SA 222/223：
  SC 列 SN35.26／35.27 之四支「证知、遍知、离贪、断舍」，而本经唯「知／识」二支，
  四支之经已用于 SA 190／191）。
- low：本批无。

gold_reconstructed：本批无。SA 228 之「广说乃至」为缘起定型之 peyyāla 省文（中间诸支），
非整篇交叉指示；中间诸支依同卷 SA 218 之缘起式补出以便达，不标 reconstructed。
省文摄记（SA 226／227／228／230 末段）如实保留，不伪作各别全经。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from translate.similarity import similarity_to_source  # noqa: E402
from translate.validate import validate_restyle  # noqa: E402

# ---------------------------------------------------------------------------
# 共用框式
# ---------------------------------------------------------------------------

OPEN_LIT = "如是我闻：一时佛在舍卫国祇树给孤独园。"
OPEN_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

CLOSE_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

AWAKEN_LIT = "「我生已尽，梵行已立，所作已作，自知不受后有。」"
AWAKEN_MOD = "「我的生已尽，梵行已立，该做的已做，自知不再受后有。」"

SIX_LIT = "耳、鼻、舌、身、意亦复如是。"
SIX_MOD = "耳、鼻、舌、身、意也是一样。"

# 六六式受支（内觉＝vedayita）
FEEL_LIT = "内所觉受，若苦、若乐、不苦不乐"
FEEL_MOD = "内心所领受的，无论是苦、是乐、还是不苦不乐"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译，"
    "与 Anālayo 之 SA 英译（DDJBS 18, 2016, Fascicle 8）并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)

PROV_230 = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "Anālayo 前篇（DDJBS 18, Fascicle 8）止于 SA 229，本经无其 SA 英译。"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)

NO_PARALLEL = (
    "SC 于本经未列任何平行（`parallels` 空、巴利本文阙），"
    "故唯以汉本为底，参 Anālayo 之 SA 英译及六入處相應之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」，本经作 medium。"
)

# 眼门六六列：眼、色、眼识、眼触、触缘生受
_EYE_LIST_LIT = f"色、眼识、眼触，及眼触因缘所生受——{FEEL_LIT}"
_EYE_LIST_MOD = f"色、眼识、眼触，以及依眼触为缘而生起的感受——{FEEL_MOD}"


# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}


# --- SA 221 取（SC 无平行；缘起式止于取，同卷 SA 218 之减式）----------------
SUTTAS["SA_221"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：有趣一切取之道。云何为趣一切取之道？"
        "缘眼、色而生眼识，三事和合为触，缘触而受，缘受而爱，缘爱而取。"
        "是故有取及所取。" + SIX_LIT + "取及所取故，是名趣一切取之道。",
        "云何断一切取之道？缘眼、色而生眼识，三事和合为触；"
        "触灭则受灭，受灭则爱灭，爱灭则取灭。" + SIX_LIT + "是名断一切取之道。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：有一条趣向一切「取」的道路。什么是趣向一切取的道路？"
        "缘于眼与色而生起眼识，这三者和合便是触；缘于触而有受，缘于受而有爱，缘于爱而有取。"
        "因此便有取，以及被取的对象。" + SIX_MOD + "因为有取及所取，这叫做趣向一切取的道路。",
        "什么是断除一切取的道路？缘于眼与色而生起眼识，这三者和合便是触；"
        "触止息则受止息，受止息则爱止息，爱止息则取止息。"
        + SIX_MOD + "这叫做断除一切取的道路。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}{NO_PARALLEL}"
        "本经缘起之式与同卷 SA_218（苦集／苦灭之道；SC 列 SN12.43／SN35.106）相同，"
        "唯集边止于「取」（upādāna）而不下开有、生、老死；灭边亦自「触灭」起而止于「取灭」。"
        "此为汉本一系就「取」一门单出之经，非可据 SA_218 之平行径称为 SN35.106——"
        "SC 未列，故不托。信-校正三事："
        "（一）「道跡」同 SA_218：巴利此系作 samudaya／atthaṅgama 或 pahāna，不言 paṭipadā；"
        "汉本加「道跡」一名（趣向之道），今作「趣一切取之道／断一切取之道」。"
        "（二）「取所取故」语面含混，可读作「取于所取」；Anālayo 读作 Therefore there is "
        "clinging and what is clung to（是故有取及所取）——upādāna 与 upādāniya，今从之。"
        "（三）底本灭边末句无「是名断一切取道跡」，Anālayo 以方括补出；今据开首所问补之，不增义。"
        "灭之次第自「触灭」起，同 SA_218 之注：巴利同类经自「爱」无余离贪而灭，"
        "汉本逆观之式存之，不当据此谓阿罗汉无六触。"
    ),
}


# --- SA 222 智识（一）（SC 列 SN 35.26／35.27，公式实为二支非四支）---------
SUTTAS["SA_222"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：当知一切应知之法、一切应识之法。谛听，善思，当为汝说。",
        f"云何一切应知之法、一切应识之法？诸比丘！眼是应知、应识之法；"
        f"{_EYE_LIST_LIT}——彼一切是应知、应识之法。" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：应当了知一切应知之法、一切应识之法。仔细听，好好思量，"
        "我为你们说。",
        f"什么是一切应知之法、一切应识之法？比丘们！眼是应知、应识之法；"
        f"{_EYE_LIST_MOD}——这些都是应知、应识之法。" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium：SC 列 SN35.26／35.27（Aparijānana）为 `full` 平行，"
        "所列「一切」之五支（眼、色、眼识、眼触、触缘生受）与本经相符；"
        "然彼经之公式为四支 `anabhijānaṁ aparijānaṁ avirājayaṁ appajahaṁ abhabbo dukkhakkhayāya`"
        "（不证知、不遍知、不离贪、不断舍则不堪尽苦），已用于 SA_190／191，"
        "而本经唯作「知法、识法」二支之正向列举，无尽苦／不堪之框。"
        "平行既不能定此二支即彼四支之省，依 SA_195／213 之例降为 medium，"
        "不据 SN35.26 增入离贪、断舍二支。"
        "信-校正：「知法、识法」Anālayo 读作 things to be understood / to be discerned"
        "（应知、应识之法），今从之；不强合 SA_190 之「证知／遍知」（abhijānāti／parijānāti）——"
        "彼为能知之行，此为所依之法，位次不同。"
        "「内觉」＝ vedayita（所受）非「觉悟」，沿 SA_195／219 之例作「内所觉受」。"
    ),
}


# --- SA 223 智识（二）（同上，反说：不知不识不得究竟苦边）----------------
SUTTAS["SA_223"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：我不说有一法，于彼不知、不识，而得究竟苦边。"
        f"云何不说？谓不说于眼不知、不识而得究竟苦边；于{_EYE_LIST_LIT}，"
        "亦复不说不知、不识而得究竟苦边。" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：我不说：对任何一法若不知、不识，也能达到苦的究竟边际。"
        f"怎样不这样说呢？就是：我不说对眼不知、不识而能达到苦的究竟边际；对{_EYE_LIST_MOD}，"
        "也一样不说不知、不识而能达到苦的究竟边际。" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium：理由同前经（SA_222）。本经为反说——「不知、不识则不得究竟苦边」，"
        "较前经更近 SN35.26 之 `abhabbo dukkhakkhayāya`，仍唯二支而非四支，故不升作 high。"
        "信-校正二事："
        "（一）底本于眼作「不知、不识」，于色、识、触、受则作「不知不见」；"
        "「见」当为「识」之讹（经题作「智识」，Anālayo 二处皆读 understanding / discerning），"
        "今一律作「不知、不识」。"
        "（二）「究竟苦边」为早期定型（`dukkhassa anta`／accanta-niṭṭhā 一类），"
        "Anālayo: the unsurpassed transcendence of dukkha；沿 SA_109／123 之例存「究竟苦边」。"
        "「内觉」同前经。"
    ),
}


# --- SA 224 断（一）（SN 35.24 Pahāna）--------------------------------------
SUTTAS["SA_224"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：一切欲法应当断。云何一切欲法应当断？"
        f"谓眼是欲法，应当断；{_EYE_LIST_LIT}——彼一切欲法应当断。" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：一切与欲相关的法都应当断除。什么是一切应当断除的欲法？"
        f"就是：眼是欲法，应当断除；{_EYE_LIST_MOD}——这些欲法都应当断除。" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.24（Pahāna）为 `full`、非 resembling 之平行，"
        "眼、色、眼识、眼触、触缘生受五支皆 `pahātabba`（应当断），巴利逐支可对。"
        "信-校正：底本开首作「一切欲法应当断」，巴利作 `sabbappahānāya … dhammaṁ`"
        "（为断「一切」而说法），所断者为 sabba（一切：六处及所生法），不言 kāma／chanda；"
        "Anālayo 读汉本为 all things [related to] desire。汉本加「欲」字与巴利之 sabba 不同，"
        "而所断之列与巴利全同，故存汉本「欲法」之语面而于此志异，不据巴利删「欲」——"
        "「欲法」可读作「所应断之欲贪所系法」，与六入处相应之通义不相违。"
        "「内觉」同 SA_222。"
    ),
}


# --- SA 225 断（二）（SN 35.25 Abhiññāpariññāpahāna）------------------------
SUTTAS["SA_225"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：我不说有一法，于彼不知、不断，而得究竟苦边。"
        f"云何不说？谓不说于眼不知、不断而得究竟苦边；于{_EYE_LIST_LIT}，"
        "亦复不说不知、不断而得究竟苦边。" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：我不说：对任何一法若不知、不断，也能达到苦的究竟边际。"
        f"怎样不这样说呢？就是：我不说对眼不知、不断而能达到苦的究竟边际；对{_EYE_LIST_MOD}，"
        "也一样不说不知、不断而能达到苦的究竟边际。" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.25（Abhiññāpariññāpahāna）为 `full` 平行（SC 标 `resembling`，"
        "盖与 SN35.24 为一组语面近同之经，非疑法义，沿 SA_188／196 之例不因该标降级）。"
        "巴利作 `sabbaṁ abhiññā pariññā pahātabbaṁ`（当以证知、遍知而断一切），"
        "本经汉本为反说「不知、不断则不得究竟苦边」，所对仍是知＋断二门。"
        "信-校正：巴利为三支（abhiññā／pariññā／pahāna），汉本唯「知」「断」二支而省遍知；"
        "今存汉本之二支，不据巴利增入「遍知」——此为汉本一系与 SA_223（知／识）成对之体裁。"
        "「究竟苦边」同前经。"
    ),
}


# --- SA 226 计（一）（SN 35.90／35.91 Ejā：maññati）-------------------------
_226_TAIL_LIT = (
    "（省文）如上所说，于眼等不计；于一切事不计，亦复如是。"
)
_226_TAIL_MOD = (
    "（以下是原典的省文指示）如同上面就不计于眼等所说，把同一格式换成「一切事」"
    "（sabba，一切：六处及所生法）也不计，也按上面那样成一经。"
    "（巴利 SN35.90 正有 `sabbaṁ na maññeyya … sabbaṁ meti na maññeyya` 一句，"
    "与此省文相摄。）"
)

SUTTAS["SA_226"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：我今当说断一切计。谛听，善思，当为汝说。",
        "云何为不计？谓不计见色为我，不计眼为我所，不计眼相属；"
        f"于{_EYE_LIST_LIT}——彼亦不计乐为我、为我所，不计乐为相属。"
        + SIX_LIT,
        "如是不计者，于诸世间都无所取；无所取故无所著；无所著故自觉涅槃："
        + AWAKEN_LIT,
        CLOSE_LIT,
        _226_TAIL_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：我现在要说断除一切「计」（计度、计着）。仔细听，好好思量，"
        "我为你们说。",
        "怎样才是不计呢？就是：不计「见色」为我，不计眼为我所，不计眼与我相属；"
        f"对{_EYE_LIST_MOD}——也不计着、不乐着它们为我、为我所，不计它们与我相属。"
        + SIX_MOD,
        "这样不计的人，对世间都无所取；无所取就无所著；无所著就自己证知涅槃："
        + AWAKEN_MOD,
        CLOSE_MOD,
        _226_TAIL_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.90／35.91（Ejā）为 `full`、非 resembling 之平行，"
        "「不计」＝ `na maññeyya`（不妄计、不计度），末段 `na kiñcipi loke upādiyati；"
        "anupādiyaṁ na paritassati；aparitassaṁ paccattaññeva parinibbāyati` 与"
        "「无所取→无所著→自觉涅槃」相当，巴利本文具足。"
        "信-校正四事："
        "（一）「计」＝ maññati（计度、计着为我），即 MN1 根本法门之语；"
        "巴利经题作 ejā（扰动、动荡，Sujato: turbulence；注释或以渴爱释之），"
        "正文则用 maññati。汉本通篇译作「计」，正得正文之词，今存「计」而于现代栏出「计度」。"
        "（二）底本「不计我见色」句读费解；Anālayo 读作 do not conceive of a self in the "
        "seeing of forms。今厘作「不计见色为我」，并出「我所」「相属」二支——"
        "巴利于每一所缘为四句（不计之为彼、于彼中、从彼、彼是我所有），"
        "汉本约之为我／我所／相属三支，今存汉本之量，不据巴利扩为四句。"
        "（三）「不计乐我、我所」之「乐」＝ nandati／abhinandati（乐着），"
        "Anālayo: conceive of and delight in；非「乐受」之乐。今作「不计乐为我」。"
        "（四）「无所著」于巴利此句作 `na paritassati`（不慌乱、不焦急），"
        "汉本一系以「取→著→涅槃」为定型（沿 SA_43 之例），义近而语面异，存汉本。"
        "末段省文「一切事不计」与巴利 `sabbaṁ na maññeyya` 相摄，如实存为末段，不伪作全文。"
    ),
}


# --- SA 227 计（二）（SN 35.90：ejā 为病、痈、刺）----------------------------
_227_TAIL_LIT = "（省文）如眼等所说，其余一一事——色、识、触、受及余入处——亦复如是。"
_227_TAIL_MOD = (
    "（以下是原典的省文指示）如同就眼等所说，其余每一项"
    "（色、眼识、眼触、触缘生受，以及耳、鼻、舌、身、意）也按同一格式成说。"
)

SUTTAS["SA_227"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：计者是病，计者是痈，计者是刺。"
        "如来以不计而住，故离病、离痈、离刺。",
        "是故，比丘欲求不计而住、离病离痈离刺者，莫计眼为我、为我所，莫计眼相属；"
        f"莫计{_EYE_LIST_LIT}——是我、我所、相在。" + SIX_LIT,
        "比丘！如是不计者，则无所取；无所取故无所著；无所著故自觉涅槃："
        + AWAKEN_LIT,
        CLOSE_LIT,
        _227_TAIL_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：计度是病，计度是痈，计度是刺。"
        "如来因为安住于不计，所以离开了病、离开了痈、离开了刺。",
        "所以，比丘若想安住于不计，离开病、痈、刺，就不要把眼计为我、为我所，"
        "不要计眼与我相属；也不要把"
        f"{_EYE_LIST_MOD}——计为是我、是我所、或彼此相在。" + SIX_MOD,
        "比丘们！这样不计的人，便无所取；无所取就无所著；无所著就自己证知涅槃："
        + AWAKEN_MOD,
        CLOSE_MOD,
        _227_TAIL_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.90 开首 `ejā … rogo, ejā gaṇḍo, ejā sallaṁ；"
        "tathāgato anejo viharati vītasallo`（扰动是病、是痈、是刺；如来住于无扰动、拔刺）"
        "与本经逐句可对，较前经（SA_226）更近巴利之框式。"
        "信-校正二事："
        "（一）「计者是病」之「计」仍＝ maññati，而巴利开首用 ejā；二词在此经中互释"
        "（计度即心之扰动），今于开首存「计」以合汉本通篇，并于 notes 出 ejā。"
        "「痈」＝ gaṇḍa（疮痈），沿 SA_103 之例；「刺」＝ salla（箭刺）。"
        "（二）底本先作「我、我所、相属」，后作「我、我所、相在」——「相属」与「相在」"
        "为同系之第三支（属他／我中有彼、彼中有我），今各存其语面，不强一之。"
        "末段省文如实保留。"
    ),
}


# --- SA 228 增长（SC 无平行；缘起增长／损减 + 六门省文）---------------------
_DO_ARISE_LIT = (
    "缘眼、色而生眼识，三事和合为触，缘触而受，缘受而爱，缘爱而取，"
    "缘取而有，缘有而生，缘生而老、病、死、忧、悲、恼、苦集；如是纯大苦聚集"
)
_DO_ARISE_MOD = (
    "缘于眼与色而生起眼识，这三者和合便是触；缘于触而有受，缘于受而有爱，"
    "缘于爱而有取，缘于取而有有，缘于有而有生，缘于生而有老、病、死、忧、悲、恼、苦的集起；"
    "这样，整个大苦的聚集便生起"
)
_DO_CEASE_LIT = (
    "缘眼、色而生眼识，三事和合为触；触灭则受灭，受灭则爱灭，爱灭则取灭，"
    "取灭则有灭，有灭则生灭，生灭则老、病、死、忧、悲、恼、苦灭；如是纯大苦聚灭"
)
_DO_CEASE_MOD = (
    "缘于眼与色而生起眼识，这三者和合便是触；触止息则受止息，受止息则爱止息，"
    "爱止息则取止息，取止息则有止息，有止息则生止息，"
    "生止息则老、病、死、忧、悲、恼、苦止息；这样，整个大苦的聚集便止息"
)

_228_TAIL_LIT = (
    "（省文）如「增长、损减」二经，如是「起法」「处变易法」「集法」「灭法」，"
    "亦如上说，各成一经。"
)
_228_TAIL_MOD = (
    "（以下是原典的省文指示）如同上面以「增长法、损减法」相对而成二经，"
    "同样换成「起法」（uppādadhamma，会生起的）、「处变易法」"
    "（ṭhitassa aññathatta，住而变易的——「处」＝ ṭhita 驻留，非入处）、"
    "「集法」（samudayadhamma）、「灭法」（nirodhadhamma／vayadhamma），"
    "各按同一缘起格式成一经。"
)

SUTTAS["SA_228"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：我今当说增长法、灭法。云何增长法？"
        f"谓{_DO_ARISE_LIT}。是名增长法。" + SIX_LIT + "是名增长法。",
        f"云何灭法？{_DO_CEASE_LIT}。" + SIX_LIT + "是名损减法。",
        CLOSE_LIT,
        _228_TAIL_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：我现在要说增长之法与灭没之法。什么是增长之法？"
        f"就是{_DO_ARISE_MOD}。这叫做增长之法。" + SIX_MOD + "这叫做增长之法。"
        "（原典此处作「触缘受……广说乃至纯大苦聚集」，中间诸支依同卷 SA_218 之缘起定型补出。）",
        f"什么是灭没之法？{_DO_CEASE_MOD}。" + SIX_MOD + "这叫做损减之法。",
        CLOSE_MOD,
        _228_TAIL_MOD,
    ],
    "notes": (
        f"{PROV}{NO_PARALLEL}"
        "底本集、灭二段皆作「触缘受……广说乃至纯大苦聚（集／灭）」，为缘起定型之 peyyāla，"
        "非法说核心整篇交叉指示（与 SA_207／200 异），故不标 gold_reconstructed；"
        "中间「受缘爱……有、生、老死」诸支依同卷已出之 SA_218 补以便达，不增其量、不补造情节。"
        "信-校正三事："
        "（一）开首作「增长法、灭法」，结句作「是名损减法」——「灭」与「损减」互出；"
        "末段省文则以「增长、损减」为对。今正文结句从底本「损减」，开首存「灭法」而志其不齐。"
        "（二）「处变易法」之「处」非十二处，乃 ṭhita（住、驻留）："
        "有为法三相作 uppāda／vaya／ṭhitassa aññathatta（生、灭、住而变易），"
        "Anālayo: being of a nature to change while remaining。今于省文出其义，以免读作「入处变易」。"
        "（三）六门（增长／损减／起／处变易／集／灭）为同一缘起式之异名系列，"
        "如实存为末段，不伪作六经全文。"
    ),
}


# --- SA 229 有漏无漏（SC 无平行；世俗六处 vs 出世间意门）--------------------
SUTTAS["SA_229"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：我今当说有漏法、无漏法。云何有漏法？"
        f"谓眼、色、眼识、眼触，及眼触因缘所生受——{FEEL_LIT}。"
        f"耳、鼻、舌、身、意，法、意识、意触，及意触因缘所生受——{FEEL_LIT}"
        "——属世俗者，是名有漏法。",
        f"云何无漏法？谓出世间之意，及法、意识、意触，及意触因缘所生受"
        f"——{FEEL_LIT}——属出世间者，是名无漏法。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：我现在要说有漏法与无漏法。什么是有漏法？"
        f"就是眼、色、眼识、眼触，以及依眼触为缘而生起的感受——{FEEL_MOD}。"
        f"耳、鼻、舌、身、意，以及法、意识、意触，依意触为缘而生起的感受——{FEEL_MOD}"
        "——属于世俗（lokiya）的，这叫做有漏法。",
        f"什么是无漏法？就是出世间的意，以及法、意识、意触，依意触为缘而生起的感受"
        f"——{FEEL_MOD}——属于出世间（lokuttara）的，这叫做无漏法。"
        "（无漏只就意门而说，不就眼等五门而说。）",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}{NO_PARALLEL}"
        "「有漏／无漏」＝ sāsava／anāsava（有诸漏、离诸漏）；"
        "「世俗」＝ lokiya，「出世间」＝ lokuttara——皆早期用语，非后来「出世间」之玄谈。"
        "信-校正三事："
        "（一）底本「眼色」当读「眼、色」（内入处与外入处），Anālayo: the eye and forms；今分读之。"
        "（二）有漏法通举六门（眼……意）而标「世俗者」；无漏法唯举「出世间意」及法、意识、"
        "意触、触缘生受——即无漏心只于意门转，不于五色根门转。此为早期教理之通义"
        "（出世间心以涅槃为所缘，不依五尘），汉本此分非臆造；Anālayo 于无漏段以省略号"
        "标底本「谓出世间意」前或有阙文，今不补五门，存汉本唯出意门之量。"
        "（三）卷末「杂阿含经卷第八」为藏经 paratext（卷题；大正藏卷次与 SC 卷第九之异，"
        "同 SA_187／188 之例），不入正文，亦不得据以称罗什译。"
        "「内觉」同前。"
    ),
}


# --- SA 230 三弥离提（SN 35.65–68 Samiddhi；正文问世间＝ SN 35.68）----------
_230_TAIL_LIT = "（省文）如「世间」所说，如是「众生」、如是「魔」，亦如是说。"
_230_TAIL_MOD = (
    "（以下是原典的省文指示）如同这部以「世间」为问的经，把「世间」换成「众生」、"
    "换成「魔」，各按同一格式成一经。"
    "（巴利正为四经：SN35.65 魔、35.66 众生、35.67 苦、35.68 世间；"
    "汉本正文出世间，省文出众生与魔，阙「苦」一经，志之不补。）"
)

SUTTAS["SA_230"] = {
    "lit": [
        OPEN_LIT,
        "时有比丘名三弥离提，往诣佛所，稽首佛足，退坐一面，白佛言："
        "世尊！所谓世间者，云何名世间？",
        "佛告三弥离提：谓眼、色、眼识、眼触，及眼触因缘所生受——"
        f"{FEEL_LIT}；耳、鼻、舌、身、意、法、意识、意触，及意触因缘所生受——"
        f"{FEEL_LIT}，是名世间。所以者何？六入处集则触集，如是乃至纯大苦聚集。",
        "三弥离提！若无彼眼、无色、无眼识、无眼触、无眼触因缘所生受——"
        f"{FEEL_LIT}；无耳、鼻、舌、身、意、法、意识、意触、意触因缘所生受——"
        f"{FEEL_LIT}者，则无世间，亦不设施世间。所以者何？"
        "六入处灭则触灭，如是乃至纯大苦聚灭故。",
        CLOSE_LIT,
        _230_TAIL_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，有一位名叫三弥离提（Samiddhi）的比丘来到佛前，以头面礼佛足，退坐一旁，对佛说："
        "世尊！人们所说的「世间」，怎样才叫做世间？",
        "佛告诉三弥离提：就是眼、色、眼识、眼触，以及依眼触为缘而生起的感受——"
        f"{FEEL_MOD}；耳、鼻、舌、身、意、法、意识、意触，依意触为缘而生起的感受——"
        f"{FEEL_MOD}，这叫做世间。为什么呢？因为六入处集起，触就集起，"
        "这样下去，直到整个大苦的聚集都集起。",
        "三弥离提！假如没有那眼、没有色、没有眼识、没有眼触、没有依眼触为缘所生的感受——"
        f"{FEEL_MOD}；也没有耳、鼻、舌、身、意、法、意识、意触、依意触为缘所生的感受——"
        f"{FEEL_MOD}，便没有世间，也不施设世间（不立世间之名）。为什么呢？"
        "因为六入处止息，触就止息，这样下去，直到整个大苦的聚集都止息。",
        CLOSE_MOD,
        _230_TAIL_MOD,
    ],
    "notes": (
        f"{PROV_230}"
        "confidence=high：SC 列 SN35.65–68（Samiddhi 四问：魔／众生／苦／世间）为 `full` 平行；"
        "本经正文问「世间」，与 SN35.68（Loka）相当；SC 以 35.65 为 primary，盖四经一组而"
        "汉本以省文摄其余，非疑法义。"
        "信-校正四事："
        "（一）「设施世间」＝ lokapaññatti（世间之施设、安立），巴利作 `loko vā lokapaññatti vā`"
        "（世间，或所谓世间者）；今存「设施」而于现代栏出「不立世间之名」。"
        "（二）巴利以「眼、色、眼识、眼识所识之法」（`cakkhuviññāṇaviññātabbā dhammā`）四支"
        "界定世间／魔等；汉本易「所识之法」为「眼触、触缘生受」，并下开「六入处集则触集，"
        "乃至纯大苦聚集」之缘起句。汉本自有其理（以触、受明世间之集），今存其列而志巴利之四支。"
        "（三）地名：巴利设于王舍城竹林（`rājagahe … veḷuvane`），汉本作舍卫国祇树给孤独园，"
        "存汉本而志异。人名三弥离提＝ Samiddhi，与巴利同。"
        "（四）卷首「杂阿含经卷第九」为藏经 paratext（卷题；底本「卷第九」而 SC／经题或作卷第十），"
        "不入正文。省文出「众生」「魔」而阙巴利之「苦」（SN35.67），不补。"
        "经末「诸比丘闻」而问者为三弥离提一人，前后所对之众不一，为汉本常例，存之。"
    ),
}


# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_221": "medium",
    "SA_222": "medium",
    "SA_223": "medium",
    "SA_224": "high",
    "SA_225": "high",
    "SA_226": "high",
    "SA_227": "high",
    "SA_228": "medium",
    "SA_229": "medium",
    "SA_230": "high",
}

# 本批无整篇交叉指示须回填者
RECONSTRUCTED: dict[str, str] = {}

SIM_MAX = 0.55

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

GOLD: dict[str, dict[str, str]] = {}
for _rid, _s in SUTTAS.items():
    _lit_paras: list[str] = list(_s["lit"])
    _mod_paras: list[str] = list(_s["mod"])
    assert len(_lit_paras) == len(_mod_paras), (
        f"{_rid} paragraph mismatch: lit={len(_lit_paras)} mod={len(_mod_paras)}"
    )
    GOLD[_rid] = {
        "kumarajiva_style_text": "\n".join(_lit_paras),
        "modern_psychology_text": "\n".join(_mod_paras),
        "notes": _s["notes"],
    }


def main() -> None:
    assert set(GOLD) == {f"SA_{i}" for i in range(221, 231)}, (
        "GOLD must cover SA_221–SA_230 exactly"
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

            v = validate_restyle(item.get("chinese_text") or "", lit, mod)
            item["validation"] = v
            item["forbidden_hits"] = v.get("forbidden_hits") or []

            sim = round(similarity_to_source(item.get("chinese_text") or "", lit), 3)
            item["similarity_to_source"] = sim

            lit_paras = lit.split("\n")
            mod_paras = mod.split("\n")
            para_ok = len(lit_paras) == len(mod_paras)
            item["paragraph_parallel"] = para_ok

            if v["status"] == "fail" and rid not in RECONSTRUCTED:
                item["review_status"] = "needs_doctrine_check"
            if sim >= SIM_MAX:
                item["review_status"] = "needs_restyle"

            report.append(
                {
                    "id": rid,
                    **v,
                    "sim": sim,
                    "paragraphs": len(lit_paras),
                    "paragraph_parallel": para_ok,
                    "confidence": item["confidence"],
                    "review_status": item["review_status"],
                }
            )
            (gold_dir / f"{rid.lower()}.json").write_text(
                json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        merged.append(item)

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa221-230.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fails = [r for r in report if r["status"] == "fail"]
    warns = [r for r in report if r["status"] == "warn"]
    oks = [r for r in report if r["status"] == "ok"]
    forbidden = [r for r in report if r["forbidden_hits"]]
    too_literal = [r for r in report if r["sim"] >= SIM_MAX]
    para_bad = [r for r in report if not r["paragraph_parallel"]]
    recon = [r for r in report if r["id"] in RECONSTRUCTED]
    max_r = max(report, key=lambda r: r["sim"])
    conf_split = {
        c: sum(1 for r in report if r["confidence"] == c) for c in ("high", "medium", "low")
    }

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_221–230 only)")
    print(f"validation: ok={len(oks)} warn={len(warns)} fail={len(fails)}")
    print(f"forbidden_hits={len(forbidden)}")
    print(
        f"sim>={SIM_MAX} (繁转简嫌疑): {len(too_literal)}  "
        f"max_sim={max_r['sim']} ({max_r['id']})  "
        f"mean_sim={round(sum(r['sim'] for r in report) / len(report), 3)}"
    )
    print(f"paragraph_parallel_violations={len(para_bad)}")
    print(f"gold={len(report) - len(recon)} gold_reconstructed={len(recon)}")
    print(f"confidence: {conf_split}")
    for r in report:
        print(
            r["id"],
            r["status"],
            f"sim={r['sim']}",
            f"paras={r['paragraphs']}",
            r["confidence"],
            r.get("issues"),
            r.get("warnings"),
        )


if __name__ == "__main__":
    main()
