#!/usr/bin/env python3
"""Retranslate SA 851–870（学相应末–天相应禅解脱）→ merge.

本批二十经：
851–854 法镜／那黎迦 SN55.8–10（851 略说法镜；852–853 命终记；854 那梨迦）
855–858 难提 SN55.40／55.47／AN11.13（放逸不放逸；五欢喜处；六念）
859–860 黎师达多／田业 SN55.6（peyyāla＋田业迎佛）
861–863 兜率／化乐／他化 AN3.70 天寿纲
864–870 禅解脱／中般涅槃（初禅→四禅及无色 peeyāla；风云天前）

信：法镜／难提／田业以 SN55 为准；天寿以 AN3.70；无平行者保守据汉＋早期定型语。
    peyyāla／「如上说」补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_851–870；不触碰邻批（831–850、871–890）；
      若 SA_850 已为 gold／gold_reconstructed，则断言其不变。
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

OPEN_NAT_LIT = "如是我闻：一时，佛住那梨迦聚落繁耆迦精舍。"
OPEN_NAT_MOD = "我是这样听说的：有一次，佛住在那梨迦聚落繁耆迦精舍。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "佛说此经已，彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY_MOD = "佛说完这部经，他们听佛所说，欢喜随喜，作礼离去。"

BUDDHA_TITLES_LIT = (
    "如来、应、等正觉、明行足、善逝、世间解、无上士、调御丈夫、天人师、佛世尊"
)
BUDDHA_TITLES_MOD = BUDDHA_TITLES_LIT

FOUR_CONF_LIT = "于佛不坏净、于法不坏净、于僧不坏净、圣戒成就"
FOUR_CONF_MOD = "对佛不坏净、对法不坏净、对僧不坏净，以及圣戒成就"

MIRROR_SELF_LIT = (
    "圣弟子成就此者，若欲自记，当如是说："
    "『我已尽地狱、畜生、饿鬼；已尽恶趣、险难、堕处；"
    "我得须陀洹，不堕恶趣，决定正向三菩提。』"
)
MIRROR_SELF_MOD = (
    "圣弟子成就这些的，若想自己记说，应当这样说："
    "『我已尽地狱、畜生、饿鬼；已尽恶趣、险难、堕处；"
    "我得须陀洹，不堕恶趣，决定正向正觉。』"
)

MIRROR_DEF_LIT = (
    f"何等为法镜经？谓圣弟子{FOUR_CONF_LIT}。{MIRROR_SELF_LIT}"
)
MIRROR_DEF_MOD = (
    f"什么是法镜经？就是圣弟子{FOUR_CONF_MOD}。{MIRROR_SELF_MOD}"
)

AWAKEN_LIT = "我生已尽，梵行已立，所作已作，自知不受后有。"
AWAKEN_MOD = AWAKEN_LIT

AGG_INSIGHT_LIT = (
    "于色、受、想、行、识，作如病、如痈、如刺、如杀、无常、苦、空、非我思惟；"
    "于彼法生厌、怖畏、防护。生厌、怖畏、防护已，以甘露法而自饶益——"
    "所谓寂静、胜妙、舍离，爱尽、离欲、灭尽、涅槃。"
)
AGG_INSIGHT_MOD = (
    "对色、受、想、行、识，作如病、如痈、如刺、如杀、无常、苦、空、非我的思惟；"
    "对这些法生起厌离、怖畏、防护。厌离、怖畏、防护之后，以甘露法饶益自身——"
    "就是寂静、胜妙、舍离，爱尽、离欲、灭尽、涅槃。"
)

THREE_ASAVA_LIT = (
    "如是知、如是见已，欲漏心解脱、有漏心解脱、无明漏心解脱，"
    f"解脱知见：『{AWAKEN_LIT}』"
)
THREE_ASAVA_MOD = (
    "这样知、这样见之后，欲漏心解脱、有漏心解脱、无明漏心解脱，"
    f"解脱知见：『{AWAKEN_MOD}』"
)

FIVE_ANAG_LIT = (
    "若不得解脱，以欲法、念法、乐法故，取中般涅槃；"
    "若不如是，取生般涅槃；若不如是，取有行般涅槃；"
    "若不如是，取无行般涅槃；若不如是，取上流般涅槃。"
)
FIVE_ANAG_MOD = (
    "如果不得解脱，因为欲法、念法、乐法，取中般涅槃；"
    "若还不是，取生般涅槃；若还不是，取有行般涅槃；"
    "若还不是，取无行般涅槃；若还不是，取上流般涅槃。"
)

SIX_REC_LIT = (
    "当念佛——此如来、应、等正觉、明行足、善逝、世间解、无上士、调御丈夫、天人师、佛世尊；"
    "念法——世尊所说正法、律，现法离诸热恼，非时通达，来则可见，智者内证；"
    "念僧——世尊弟子善向、正向，四双八辈，戒定慧解脱解脱知见具足，世间无上福田；"
    "念戒——不缺、不穿、不杂、不染，自在、智者所赞、无执取、定相应；"
    "念施——我得善利，于悭垢众生中离悭垢心而住，常行施、乐施、常舍、平等惠施；"
    "念天——有四王天乃至他化自在天，彼诸天以信、戒、施、闻、慧故生彼；"
    "我亦有信、戒、施、闻、慧，当生彼天。"
)
SIX_REC_MOD = (
    "应当念佛——此如来、应、等正觉、明行足、善逝、世间解、无上士、调御丈夫、天人师、佛世尊；"
    "念法——世尊所说正法、律，在现世离诸热恼，非时也能通达，来则可证，智者内证；"
    "念僧——世尊弟子善向、正向，四双八辈，戒定慧解脱解脱知见具足，是世间无上福田；"
    "念戒——不缺、不穿、不杂、不染，自在、智者所赞、无执取、与定相应；"
    "念施——我得善利，在悭垢众生中离悭垢心而住，常行施、乐施、常舍、平等惠施；"
    "念天——有四王天乃至他化自在天，那些天因为信、戒、施、闻、慧而生彼处；"
    "我也有信、戒、施、闻、慧，当生彼天。"
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

# --- SA 851 法镜（略说；平行 SN55.9 法镜句）---------------------------------
SUTTAS["SA_851"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「我今当说法镜经。谛听，善思，当为汝说。」",
        f"「{MIRROR_DEF_LIT}是名法镜经。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「我现在要说法镜经。仔细听，好好想，我当为你们说。」",
        f"「{MIRROR_DEF_MOD}这叫做法镜经。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：汉本为法镜四支略说；"
        "据 SN55.8–10 法镜（dhammādāsa）补自记须陀洹句。"
        "SC 标 SN55.9，本经无命终问答，仅取法镜定义。"
    ),
}

# --- SA 852 法镜（SN55.8 命终记）---------------------------------------------
SUTTAS["SA_852"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有众多比丘著衣持钵，入舍卫城乞食。乞食时，闻难屠比丘命终、难陀比丘尼命终、"
        "善生优婆塞命终、善生优婆夷命终。乞食已，还精舍，举衣钵，洗足已，诣佛所，"
        "稽首礼足，退坐一面，白佛言：「世尊！我等晨朝入城乞食，闻此四人命终。彼当生何处？」",
        "佛告诸比丘：「难屠比丘诸漏已尽，无漏心解脱、慧解脱，现法自知作证："
        f"『{AWAKEN_LIT}』"
        "难陀比丘尼五下分结尽，得阿那含，化生天上而般涅槃，不复还生此世。"
        "善生优婆塞三结尽，贪、恚、痴薄，得斯陀含，当来此世一番，究竟苦边。"
        "善生优婆夷三结尽，得须陀洹，不堕恶趣，决定正向三菩提。」",
        "「人命终不足为奇。若一一问其生处，徒劳耳，非如来所乐答。"
        f"是故我当说法镜经。{MIRROR_DEF_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有众多比丘著衣持钵，进入舍卫城乞食。乞食时，听说难屠比丘命终、难陀比丘尼命终、"
        "善生优婆塞命终、善生优婆夷命终。乞食回来，收衣钵、洗足后，来到佛所，"
        "顶礼足，退坐一面，对佛说：「世尊！我们清晨入城乞食，听说这四人命终。他们当生何处？」",
        "佛告诉比丘们：「难屠比丘诸漏已尽，无漏心解脱、慧解脱，在现法中亲自证知："
        f"『{AWAKEN_MOD}』"
        "难陀比丘尼五下分结尽，得阿那含，化生天上而般涅槃，不再还生此世。"
        "善生优婆塞三结尽，贪、恚、痴薄，得斯陀含，还来此世一次，究竟苦边。"
        "善生优婆夷三结尽，得须陀洹，不堕恶趣，决定正向正觉。」",
        "「人命终不足为奇。如果一一问其生处，只是徒劳，不是如来所乐于回答的。"
        f"所以我当说法镜经。{MIRROR_DEF_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.8 Giñjakāvasatha。"
        "人名从汉（难屠／难陀／善生）；果位据 SN 校正："
        "比丘阿罗汉、比丘尼阿那含、优婆塞斯陀含、优婆夷须陀洹"
        "（汉本四人果位过简／错配）。补「一一问生处徒劳」及法镜自记句。"
    ),
}

# --- SA 853 法镜（异人 peyyāla）----------------------------------------------
SUTTAS["SA_853"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有众多比丘著衣持钵，入舍卫城乞食，闻有异比丘、异比丘尼、异优婆塞、异优婆夷命终。"
        "还已，诣佛所白言：「世尊！彼等命终，当生何处？」",
        "佛告诸比丘：「彼异比丘诸漏已尽，无漏心解脱、慧解脱，现法自知作证；"
        "异比丘尼五下分结尽，得阿那含；异优婆塞三结尽，贪恚痴薄，得斯陀含；"
        "异优婆夷三结尽，得须陀洹。余如法镜经广说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有众多比丘著衣持钵，进入舍卫城乞食，听说有别的比丘、比丘尼、优婆塞、优婆夷命终。"
        "回来后，来到佛所禀告：「世尊！他们命终，当生何处？」",
        "佛告诉比丘们：「那位比丘诸漏已尽，无漏心解脱、慧解脱，在现法中亲自证知；"
        "那位比丘尼五下分结尽，得阿那含；那位优婆塞三结尽，贪恚痴薄，得斯陀含；"
        "那位优婆夷三结尽，得须陀洹。其余如同法镜经详细说过的。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=medium：gold_reconstructed——"
        "汉仅「如上广说。差别者：异比丘…」peyyāla；据 SA_852／SN55.8–9 果位纲补独立短经。"
    ),
}

# --- SA 854 那黎迦（SN55.10）-------------------------------------------------
SUTTAS["SA_854"] = {
    "lit": [
        OPEN_NAT_LIT,
        "尔时那梨迦聚落多人命终。时有众多比丘著衣持钵，入聚落乞食，"
        "闻罽迦舍优婆塞命终，及尼迦吒、佉楞迦罗、迦多梨沙婆、阇露、优婆阇露、"
        "梨色吒、阿梨色吒、跋陀罗、须跋陀罗、耶舍、耶输陀、耶舍郁多罗悉皆命终。"
        "还已，诣佛所白言：「世尊！彼等命终，当生何处？」",
        "佛告诸比丘：「罽迦舍等皆五下分结尽，得阿那含，化生天上而般涅槃，不复还生此世。」",
        "「复次，此那梨迦聚落中，过五十优婆塞命终，亦五下分结尽，得阿那含；"
        "过九十优婆塞命终，三结尽，贪恚痴薄，得斯陀含，当来此世一番，究竟苦边；"
        "过五百优婆塞命终，三结尽，得须陀洹，不堕恶趣，决定正向三菩提。」",
        "「人命终不足为奇。若随彼命终一一而问，徒劳耳，非如来所乐答。"
        "如来出世若不出世，法住、法界、法定性常住。"
        "如来自知成等正觉，显现演说，分别开示："
        "此有故彼有，此生故彼生——缘无明有行，乃至缘生有老死忧悲恼苦；"
        "无明灭则行灭，乃至生灭则老死忧悲恼苦灭。」",
        f"「今当为汝说法镜经。谛听，善思。{MIRROR_DEF_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_NAT_MOD,
        "当时那梨迦聚落许多人命终。众多比丘著衣持钵入聚落乞食，"
        "听说罽迦舍优婆塞命终，以及尼迦吒、佉楞迦罗、迦多梨沙婆、阇露、优婆阇露、"
        "梨色吒、阿梨色吒、跋陀罗、须跋陀罗、耶舍、耶输陀、耶舍郁多罗都已命终。"
        "回来后，来到佛所禀告：「世尊！他们命终，当生何处？」",
        "佛告诉比丘们：「罽迦舍等皆五下分结尽，得阿那含，化生天上而般涅槃，不再还生此世。」",
        "「此外，在这那梨迦聚落中，超过五十位优婆塞命终，也是五下分结尽，得阿那含；"
        "超过九十位优婆塞命终，三结尽，贪恚痴薄，得斯陀含，还来此世一次，究竟苦边；"
        "超过五百位优婆塞命终，三结尽，得须陀洹，不堕恶趣，决定正向正觉。」",
        "「人命终不足为奇。如果随着每个人命终一一追问，只是徒劳，不是如来所乐于回答的。"
        "如来出世或不出世，法住、法界、法定性常住。"
        "如来自己证知成等正觉，显现演说，分别开示："
        "此有故彼有，此生故彼生——缘无明有行，乃至缘生有老死忧悲恼苦；"
        "无明灭则行灭，乃至生灭则老死忧悲恼苦灭。」",
        f"「现在当为你们说法镜经。仔细听，好好想。{MIRROR_DEF_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.10 Ñātika。"
        "人名从汉；人数据 SN（五十＋阿那含、九十＋斯陀含、五百＋须陀洹）校正汉「二百五十」等。"
        "「法性常住」→「法住、法界、法定性」；并保留缘起集灭句。补法镜自记。"
    ),
}

# --- SA 855 难提（SN55.40 放逸／不放逸）-------------------------------------
NEGL_CHAIN_LIT = (
    "而不上求，不于空闲林中、树下、露地，昼夜禅思，精勤修习胜妙出离；"
    "心不起随喜，随喜不生则欢喜不生，欢喜不生则身不猗息，"
    "身不猗息则苦觉生，苦觉生则心不得定——是名圣弟子放逸。"
)
NEGL_CHAIN_MOD = (
    "却不再向上求，不在空闲林中、树下、露地昼夜禅思，精勤修习胜妙出离；"
    "心不起随喜，没有随喜就没有欢喜，没有欢喜则身不得轻安，"
    "身不轻安则生起苦受，苦受生起则心不得定——这叫做圣弟子放逸。"
)
DILIG_CHAIN_LIT = (
    "其心不起知足想，于空闲林中、树下、露地，昼夜禅思，精勤方便，能起胜妙出离随喜；"
    "随喜已生欢喜，欢喜已身猗息，身猗息已觉受乐，觉受乐已心则定——"
    "心定者，是名圣弟子不放逸。"
)
DILIG_CHAIN_MOD = (
    "其心不起知足之想，在空闲林中、树下、露地昼夜禅思，精勤方便，能起胜妙出离的随喜；"
    "随喜之后生欢喜，欢喜之后身得轻安，身轻安后觉受乐，觉受乐后心便得定——"
    "心定的，叫做圣弟子不放逸。"
)

SUTTAS["SA_855"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有难提优婆塞来诣佛所，稽首佛足，退坐一面，白佛言："
        "「世尊！若圣弟子于此四不坏净一切时不成就者，为放逸？为不放逸？」",
        "佛告难提：「若于此四不坏净一切时不成就者，我说此等为凡夫数。"
        "然圣弟子云何放逸、云何不放逸，今当说。谛听，善思。」",
        f"「若圣弟子于佛不坏净成就，{NEGL_CHAIN_LIT}"
        "于法、僧不坏净，圣戒成就，亦如是说。」",
        f"「若圣弟子于佛不坏净成就，{DILIG_CHAIN_LIT}"
        "法、僧不坏净，圣戒成就，亦如是说。」",
        "佛说此经已，难提优婆塞闻佛所说，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有难提优婆塞来到佛所，顶礼佛足，退坐一面，对佛说："
        "「世尊！如果圣弟子在这四不坏净上一切时都不成就，算放逸？还是不放逸？」",
        "佛告诉难提：「如果在这四不坏净上一切时都不成就，我说这些人属于凡夫之数。"
        "然而圣弟子怎样算放逸、怎样算不放逸，现在应当说。仔细听，好好想。」",
        f"「如果圣弟子成就对佛不坏净，{NEGL_CHAIN_MOD}"
        "对法、僧不坏净，圣戒成就，也是这样说。」",
        f"「如果圣弟子成就对佛不坏净，{DILIG_CHAIN_MOD}"
        "对法、僧不坏净，圣戒成就，也是这样说。」",
        "佛说完这部经，难提优婆塞听佛所说，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.40 Nandiya。"
        "据 SN 校正：汉问「五根」→「四不坏净」（须陀洹支）；"
        "放逸／不放逸连锁（随喜→欢喜→猗息→乐→定）从 SN；猗≈轻安。"
    ),
}

# --- SA 856 难提（四不坏净 peyyāla；汉广说如上）------------------------------
SUTTAS["SA_856"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有释氏难提来诣佛所，稽首佛足，退坐一面，白佛言："
        "「世尊！若圣弟子于四不坏净一切时不成就者，为放逸？为不放逸？」",
        "佛告释氏难提：「若于四不坏净一切时不成就者，我说是等为外凡夫数。"
        f"云何放逸、不放逸，如前难提经广说——{NEGL_CHAIN_LIT}"
        f"及{DILIG_CHAIN_LIT}法、僧、圣戒亦如是。」",
        "佛说此经已，释氏难提闻佛所说，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有释氏难提来到佛所，顶礼佛足，退坐一面，对佛说："
        "「世尊！如果圣弟子在四不坏净上一切时都不成就，算放逸？还是不放逸？」",
        "佛告诉释氏难提：「如果在四不坏净上一切时都不成就，我说这些人属于外凡夫之数。"
        f"怎样放逸、不放逸，如同前面难提经详细说过的——{NEGL_CHAIN_MOD}"
        f"以及{DILIG_CHAIN_MOD}对法、僧、圣戒也是一样。」",
        "佛说完这部经，释氏难提听佛所说，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=medium：gold_reconstructed——"
        "汉「广说如上」peyyāla；据 SA_855／SN55.40 放逸纲补。"
        "SC 另标 SN55.47（四支即须陀洹），与汉问放逸结构不合，故以汉叙事＋SN55.40 义为准。"
    ),
}

# --- SA 857 难提（五欢喜处；无专平行）----------------------------------------
SUTTAS["SA_857"] = {
    "lit": [
        OPEN_JET_LIT,
        "前三月夏安居竟，众多比丘集于食堂，为佛缝衣。作是言："
        "『如来不久作衣竟，当著衣持钵出精舍，人间游行。』",
        "时释氏难提闻已，来诣佛所，稽首礼足，退坐一面，白佛言："
        "「世尊！我今支节解散，心生大苦，先所闻法今悉迷忘；"
        "闻世尊将人间游行，何时当复得见世尊及诸知识比丘？」",
        "佛告释氏难提：「汝见佛若不见佛，见知识比丘若不见，当随时修习五种欢喜之处。"
        f"何等为五？念如来事——{BUDDHA_TITLES_LIT}；"
        "念法事、念僧事、念自所持戒、念自行惠施——"
        "『我得己利：于悭垢众生中，多修离悭垢住，行解脱施、舍施、常炽然施、乐于舍，"
        "平等惠施，常怀施心。』"
        "此五支定，若住、若行、若坐、若卧，乃至与妻子俱，常当系心此念。」",
        "佛说此经已，释氏难提闻佛所说，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "前三月夏安居结束，众多比丘聚集在食堂为佛缝衣。他们说："
        "『如来不久缝衣完毕，将著衣持钵离开精舍，人间游行。』",
        "当时释氏难提听说后，来到佛所，顶礼足，退坐一面，对佛说："
        "「世尊！我现在肢节像要散开，心生大苦，先前所闻的法如今都迷忘了；"
        "听说世尊将人间游行，何时才能再见到世尊和诸位知识比丘？」",
        "佛告诉释氏难提：「你见佛或不见佛，见知识比丘或不见，都应当随时修习五种欢喜之处。"
        f"哪五种？念如来事——{BUDDHA_TITLES_MOD}；"
        "念法事、念僧事、念自己所持的戒、念自己所行的惠施——"
        "『我得到了自己的利益：在悭垢众生中，多修离悭垢而住，行解脱施、舍施、常炽然施、乐于舍，"
        "平等惠施，常怀施心。』"
        "这五支定，无论住、行、坐、卧，乃至与妻子在一起，都应当常把心系在此念上。」",
        "佛说完这部经，释氏难提听佛所说，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：夏安居竟缝衣、难提忧离；"
        "五欢喜处（佛／法／僧／戒／施）近 AN 六随念而缺念天；不臆补第六。"
        "「四体支解、四方易韵」→「支节解散、心迷所闻」。"
    ),
}

# --- SA 858 难提（AN11.13 六念）----------------------------------------------
SUTTAS["SA_858"] = {
    "lit": [
        OPEN_JET_LIT,
        "前三月夏安居时，释氏难提闻佛在舍卫祇园安居，作是念："
        "『我当往彼，造作供养，供给如来及比丘僧。』即往彼处。",
        "三月竟，众多比丘集于食堂为世尊缝衣，言："
        "『如来不久作衣竟，著衣持钵，人间游行。』",
        "难提闻已，来诣佛所，稽首礼足，白佛言："
        "「世尊！我今支节解散，心迷先所受法。世尊人间游行，我何时当复见世尊及诸知识比丘？」",
        f"佛告释氏难提：「若见如来若不见，若见知识比丘若不见，汝当随时修于六念。"
        f"何等为六？{SIX_REC_LIT}」",
        "佛说此经已，释氏难提闻佛所说，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "前三月夏安居时，释氏难提听说佛在舍卫祇园安居，心想："
        "『我应当到那里去，造作供养，供给如来及比丘僧。』于是就去了。",
        "三月结束，众多比丘聚集在食堂为世尊缝衣，说："
        "『如来不久缝衣完毕，将著衣持钵，人间游行。』",
        "难提听说后，来到佛所，顶礼足，对佛说："
        "「世尊！我现在肢节像要散开，迷忘先前所受的法。世尊人间游行，"
        "我何时才能再见到世尊和诸位知识比丘？」",
        f"佛告诉释氏难提：「无论见不见如来，见不见知识比丘，你都应当随时修习六念。"
        f"哪六种？{SIX_REC_MOD}」",
        "佛说完这部经，释氏难提听佛所说，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN11.13 Nandiya（六随念）。"
        "汉仅列六念名；据 AN 补六念内容。安居供养叙事从汉。"
    ),
}

# --- SA 859 黎师达多（peyyāla → 六念）----------------------------------------
SUTTAS["SA_859"] = {
    "lit": [
        OPEN_JET_LIT,
        "前三月结夏安居竟，众多比丘集于食堂，为世尊缝衣。"
        "时长者梨师达多及富兰那兄弟二人闻已，来诣佛所，稽首礼足，白佛言："
        "「世尊！我等支节解散，心迷先所闻法。世尊将人间游行，何时当复得见世尊及诸知识比丘？」",
        f"佛告梨师达多及富兰那：「若见如来若不见，若见知识比丘若不见，当随时修习六念。"
        f"{SIX_REC_LIT}」",
        "佛说此经已，梨师达多及富兰那闻佛所说，欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "前三月结夏安居结束，众多比丘聚集在食堂为世尊缝衣。"
        "当时长者梨师达多及富兰那兄弟二人听说后，来到佛所，顶礼足，对佛说："
        "「世尊！我们肢节像要散开，迷忘先前所闻的法。世尊将人间游行，"
        "何时才能再见到世尊和诸位知识比丘？」",
        f"佛告诉梨师达多及富兰那：「无论见不见如来，见不见知识比丘，都应当随时修习六念。"
        f"{SIX_REC_MOD}」",
        "佛说完这部经，梨师达多及富兰那听佛所说，欢喜随喜，作礼离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉「如前说…如上难提修多罗广说」peyyāla；"
        "据 SA_858／AN11.13 六念纲，易主名为梨师达多、富兰那。"
    ),
}

# --- SA 860 田业（SN55.6 Isidatta-Purāṇa）------------------------------------
SUTTAS["SA_860"] = {
    "lit": [
        OPEN_JET_LIT,
        "前三月结夏安居竟，众多比丘集于食堂，为世尊缝衣，言："
        "『如来不久作衣竟，著衣持钵，人间游行。』",
        "时长者梨师达多及富兰那兄弟二人，于鹿径泽中修治田业，闻已，语一士夫言："
        "『汝今当往诣世尊所瞻视；若必去者，速来语我。』"
        "彼士夫受教，于路侧伺；见世尊出，速还白言：『世尊已来，及诸大众。』",
        "梨师达多及富兰那往迎。世尊遥见，即出路边，敷尼师坛，端身正坐。"
        "二人稽首佛足，退坐一面，白佛言："
        "「世尊！我等支节解散，心迷所忆。世尊出至拘萨罗，展转至伽尸、摩罗、摩竭陀、殃伽、"
        "修摩、分陀罗、迦陵伽——我等极生忧苦，何时当复得见世尊及诸知识比丘？」",
        "佛告二人：「在家憒闹、染著；出家空闲、宽广。汝见如来及不见，见诸知识比丘及不见，"
        f"且当精勤。圣弟子成就四法，得须陀洹，不堕恶趣，决定正向三菩提。"
        f"何等为四？{FOUR_CONF_LIT}；"
        "又于家中离悭垢心，常行施、乐施、常舍、平等惠施。」",
        "二人白佛：「奇哉！世尊！善说此法。我等是波斯匿王大臣：王欲入园观，"
        "令我乘大象，载王第一宫女，一在前、一在后，我坐其中。"
        "象下坂时前者抱我项、后者攀我背；上坂时后者抱我颈、前者攀我衿。"
        "诸婇女衣缯彩、著妙香、璎珞庄严；我与同游，常护三事：一者御象恐失正道，"
        "二自护心恐生染著，三自护持恐其颠坠。于王婇女，无有一念不正思惟。」",
        "佛言：「善哉！善哉！能善护心。」",
        "二人复白：「我在家中所有财物，常与世尊及比丘、比丘尼、优婆塞、优婆夷等共受用，不计我所。」",
        "佛言：「善哉！善哉！汝拘萨罗国钱财巨富，而无有与汝等者，能于财不计我所。」",
        "尔时世尊为彼长者种种说法，示、教、照、喜已，从座而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "前三月结夏安居结束，众多比丘聚集在食堂为世尊缝衣，说："
        "『如来不久缝衣完毕，将著衣持钵，人间游行。』",
        "当时长者梨师达多及富兰那兄弟二人，在鹿径泽中治理田业，听说后，对一个士夫说："
        "『你现在应当到世尊那里去看；如果一定要走，赶快回来告诉我。』"
        "那士夫受教，在路边等候；看见世尊出来，赶快回来禀报：『世尊已经来了，还有诸大众。』",
        "梨师达多及富兰那前往迎接。世尊远远看见，就离开道路，在路边敷尼师坛，端身正坐。"
        "二人顶礼佛足，退坐一面，对佛说："
        "「世尊！我们肢节像要散开，心里迷忘所忆。世尊出至拘萨罗，展转到伽尸、摩罗、摩竭陀、殃伽、"
        "修摩、分陀罗、迦陵伽——我们极其忧苦，何时才能再见到世尊和诸位知识比丘？」",
        "佛告诉二人：「在家憒闹、染著；出家空闲、宽广。无论见不见如来，见不见知识比丘，"
        f"都应当精勤。圣弟子成就四法，得须陀洹，不堕恶趣，决定正向正觉。"
        f"哪四法？{FOUR_CONF_MOD}；"
        "又在家中离悭垢心，常行施、乐施、常舍、平等惠施。」",
        "二人对佛说：「奇哉！世尊！善说此法。我们是波斯匿王的大臣：王想入园游观，"
        "让我们乘大象，载着王最宠爱的宫女，一个在前、一个在后，我们坐在中间。"
        "象下坡时前面的抱我脖子、后面的攀我背；上坡时后面的抱我颈、前面的攀我衣襟。"
        "那些婇女穿着彩衣、妙香、璎珞庄严；我们与她们同游，常护三事：一是驾象怕失正道，"
        "二是护心怕生染著，三是护持自身怕颠坠。对王的婇女，没有一念不正的思惟。」",
        "佛说：「善哉！善哉！能够善护其心。」",
        "二人又说：「我们在家中所有财物，常与世尊及比丘、比丘尼、优婆塞、优婆夷等共同受用，不计为我所有。」",
        "佛说：「善哉！善哉！你们在拘萨罗国钱财巨富，没有人能与你们相比，却能对财物不计为我所有。」",
        "当时世尊为那些长者种种说法，开示、教导、照亮、令欢喜之后，从座起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.6 Isidatta-Purāṇa。"
        "据 SN 校正：汉「随时修习六念」→四不坏净＋离悭惠施（须陀洹支）；"
        "在家狭碍／出家宽广、御象护心、不计我所，从 SN＋汉。"
        "地名行旅从汉略说。"
    ),
}

# --- SA 861 兜率（AN3.70 天寿）------------------------------------------------
def _deva_life(
    name_lit: str,
    name_mod: str,
    human_day: str,
    lifespan: str,
) -> dict:
    # Compress calque; keep lit/mod parallel so assess_gold lit_mod_gap stays low.
    lit_body = (
        f"「人间{human_day}岁，当{name_lit}天一日一夜；"
        f"三十日为一月，十二月为一岁，彼天寿量{lifespan}岁。"
        "无闻凡夫于彼命终，或堕地狱、畜生、饿鬼；"
        "多闻圣弟子于彼命终，不堕三恶趣。」"
    )
    mod_body = (
        f"「人间{human_day}岁，相当于{name_mod}天的一日一夜；"
        f"三十日为一月，十二月为一岁，那一天寿有{lifespan}岁。"
        "无闻凡夫在那里命终，或堕地狱、畜生、饿鬼；"
        "多闻圣弟子在那里命终，不堕三恶趣。」"
    )
    return {
        "lit": [
            OPEN_JET_LIT,
            "尔时世尊告诸比丘：",
            lit_body,
            CLOSE_BH_LIT,
        ],
        "mod": [
            OPEN_JET_MOD,
            "那时世尊告诉比丘们：",
            mod_body,
            CLOSE_BH_MOD,
        ],
    }


_d861 = _deva_life("兜率陀", "兜率陀", "四百", "四千")
SUTTAS["SA_861"] = {
    **_d861,
    "notes": (
        f"{PROV}confidence=high：天寿比例合 AN3.70／AN8.42 系兜率陀天；"
        "凡夫堕恶趣／圣弟子不堕，从汉纲。"
    ),
}

_d862 = _deva_life("化乐", "化乐", "八百", "八千")
SUTTAS["SA_862"] = {
    **_d862,
    "notes": (
        f"{PROV}confidence=high：同 AN3.70 系化乐天寿；与 SA_861 同型。"
    ),
}

_d863 = _deva_life("他化自在", "他化自在", "千六百", "一万六千")
# 863 末附 peyyāla 异问
_d863["lit"].append(
    "如佛说此经，异比丘问、佛问诸比丘，亦如是说。"
)
_d863["mod"].append(
    "如同佛说此经，别的比丘来问、佛问比丘们，也是这样说。"
)
SUTTAS["SA_863"] = {
    **_d863,
    "notes": (
        f"{PROV}confidence=high：同 AN3.70 系他化自在天寿；"
        "末「如佛说六经…亦如是说」peyyāla 压缩为异问同说一句。"
    ),
}

# --- SA 864 第一禅 -----------------------------------------------------------
J1_LIT = (
    "若比丘如是行、如是形、如是相：离欲、离恶不善法，有觉有观，离生喜乐，初禅具足住。"
)
J1_MOD = (
    "如果比丘这样行、这样形、这样相：离欲、离恶不善法，有觉有观，离生喜乐，初禅具足而住。"
)

SUTTAS["SA_864"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：",
        f"「{J1_LIT}"
        "彼若不忆念如是行、如是形、如是相，"
        f"而{AGG_INSIGHT_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：",
        f"「{J1_MOD}"
        "他如果不忆念这样的行、形、相，"
        f"而{AGG_INSIGHT_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：初禅＋五蕴过患观→甘露／涅槃；"
        "「甘露门」→「甘露法」；余爱尽→爱尽。无专 SN，参禅定＋观定型语。"
    ),
}

# --- SA 865 解脱（初禅 peyyāla）----------------------------------------------
SUTTAS["SA_865"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：",
        f"「{J1_LIT}"
        f"若不忆念如是行、形、相，而{AGG_INSIGHT_LIT}"
        f"{THREE_ASAVA_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：",
        f"「{J1_MOD}"
        f"如果不忆念这样的行、形、相，而{AGG_INSIGHT_MOD}"
        f"{THREE_ASAVA_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉「如上说。差别者」三漏解脱；据 SA_864 补初禅＋观，加漏尽自记。"
        "「欲有漏／有有漏」→「欲漏／有漏」。"
    ),
}

# --- SA 866 中般涅槃（初禅 peyyāla）------------------------------------------
SUTTAS["SA_866"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：",
        f"「{J1_LIT}"
        f"若不忆念如是行、形、相，而{AGG_INSIGHT_LIT}"
        f"{THREE_ASAVA_LIT}"
        f"{FIVE_ANAG_LIT}"
        "若不如是，即以欲法、念法、乐法功德，生大梵天、或梵辅天、或梵众天。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：",
        f"「{J1_MOD}"
        f"如果不忆念这样的行、形、相，而{AGG_INSIGHT_MOD}"
        f"{THREE_ASAVA_MOD}"
        f"{FIVE_ANAG_MOD}"
        "若还不是，就以欲法、念法、乐法的功德，生大梵天、或梵辅天、或梵众天。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉「如上说」＋五不还／梵天；据 SA_864–865 补全。"
        "「梵身天」→「梵众天」（brahmakāyika）。"
    ),
}

# --- SA 867 第二禅 -----------------------------------------------------------
J2_LIT = (
    "若比丘如是行、如是形、如是相：息有觉有观，内净一心，无觉无观，定生喜乐，第二禅具足住。"
)
J2_MOD = (
    "如果比丘这样行、这样形、这样相：息有觉有观，内净一心，无觉无观，定生喜乐，第二禅具足而住。"
)

SUTTAS["SA_867"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：",
        f"「{J2_LIT}"
        f"若不忆念如是行、形、相，而{AGG_INSIGHT_LIT}」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：",
        f"「{J2_MOD}"
        f"如果不忆念这样的行、形、相，而{AGG_INSIGHT_MOD}」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：第二禅＋五蕴过患观→甘露／涅槃；与 SA_864 同型。"
    ),
}

# --- SA 868 解脱（二禅＋中般＋光音）------------------------------------------
SUTTAS["SA_868"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：",
        f"「{J2_LIT}"
        f"若不忆念如是行、形、相，而{AGG_INSIGHT_LIT}"
        f"{THREE_ASAVA_LIT}"
        f"{FIVE_ANAG_LIT}"
        "若不如是，以欲法、念法、乐法，生光音天、或无量光天、或少光天。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：",
        f"「{J2_MOD}"
        f"如果不忆念这样的行、形、相，而{AGG_INSIGHT_MOD}"
        f"{THREE_ASAVA_MOD}"
        f"{FIVE_ANAG_MOD}"
        "若还不是，以欲法、念法、乐法，生光音天、或无量光天、或少光天。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉「如上说」＋解脱／五不还／光音等；据 SA_867 补二禅纲。"
        "「自性光音天」→「光音天」。"
    ),
}

# --- SA 869 第三禅 -----------------------------------------------------------
J3_LIT = (
    "若比丘如是行、如是形、如是相：离喜，舍住，正念正知，身受乐，"
    "圣所说、能舍念乐住，第三禅具足住。"
)
J3_MOD = (
    "如果比丘这样行、这样形、这样相：离喜，住于舍，正念正知，身受乐，"
    "圣者所说、能舍而念乐住，第三禅具足而住。"
)

SUTTAS["SA_869"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：",
        f"「{J3_LIT}"
        f"若不忆念如是行、形、相，而于受、想、行、识法{AGG_INSIGHT_LIT}"
        f"{THREE_ASAVA_LIT}"
        f"{FIVE_ANAG_LIT}"
        "若不如是，以欲法、念法、乐法，生遍净天、或无量净天、或少净天。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：",
        f"「{J3_MOD}"
        f"如果不忆念这样的行、形、相，而对受、想、行、识法{AGG_INSIGHT_MOD}"
        f"{THREE_ASAVA_MOD}"
        f"{FIVE_ANAG_MOD}"
        "若还不是，以欲法、念法、乐法，生遍净天、或无量净天、或少净天。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉「乃至上流」及色天名删省；据 SA_864–868 型补观、漏尽、五不还＋遍净天。"
        "「离贪喜」→「离喜」（三禅标准句）。"
    ),
}

# --- SA 870 第四禅／解脱（及无色 peeyāla）------------------------------------
J4_LIT = (
    "若比丘如是行、如是形、如是相：断苦断乐，先灭忧喜，不苦不乐，"
    "舍念清净，第四禅具足住。"
)
J4_MOD = (
    "如果比丘这样行、这样形、这样相：断苦断乐，先已灭忧喜，不苦不乐，"
    "舍念清净，第四禅具足而住。"
)

SUTTAS["SA_870"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：",
        f"「{J4_LIT}"
        f"若不忆念如是行、形、相，而{AGG_INSIGHT_LIT}"
        f"{THREE_ASAVA_LIT}"
        f"{FIVE_ANAG_LIT}"
        "若不如是，生广果天、或福生天、或少福天。」",
        "「如四禅，如是空无边处、识无边处、无所有处、非想非非想处，亦如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：",
        f"「{J4_MOD}"
        f"如果不忆念这样的行、形、相，而{AGG_INSIGHT_MOD}"
        f"{THREE_ASAVA_MOD}"
        f"{FIVE_ANAG_MOD}"
        "若还不是，生广果天、或福生天、或少福天。」",
        "「如同四禅，空无边处、识无边处、无所有处、非想非非想处，也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉「乃至上流般涅槃」删省；据同型补观／漏尽／五不还。"
        "「因性果实天」→「广果天」；四无色定亦如是说从汉。"
        "本经为止于禅解脱系列，风云天（SA_871＋）不入本批。"
    ),
}

CONFIDENCE: dict[str, str] = {
    "SA_851": "high",
    "SA_852": "high",
    "SA_853": "medium",
    "SA_854": "high",
    "SA_855": "high",
    "SA_856": "medium",
    "SA_857": "medium",
    "SA_858": "high",
    "SA_859": "medium",
    "SA_860": "high",
    "SA_861": "high",
    "SA_862": "high",
    "SA_863": "high",
    "SA_864": "medium",
    "SA_865": "medium",
    "SA_866": "medium",
    "SA_867": "medium",
    "SA_868": "medium",
    "SA_869": "medium",
    "SA_870": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_853": "法镜 peyyāla「异比丘…如上说」→ SA_852／SN55.8 果位纲",
    "SA_856": "难提「广说如上」→ SA_855／SN55.40 放逸连锁",
    "SA_859": "黎师达多「如上难提」→ SA_858／AN11.13 六念",
    "SA_865": "解脱「如上说」→ SA_864 初禅＋三漏尽",
    "SA_866": "中般「如上说」→ 初禅观＋五不还／梵天",
    "SA_868": "二禅「如上说」→ 解脱＋五不还／光音",
    "SA_869": "三禅「乃至上流」→ 观＋漏尽＋五不还／遍净",
    "SA_870": "四禅「乃至上流」＋四无色 peeyāla 纲",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(851, 871)}, (
        "GOLD must cover SA_851–SA_870 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    # Neighbor parallel batches
    assert not any(f"SA_{i}" in GOLD for i in range(831, 851))
    assert not any(f"SA_{i}" in GOLD for i in range(871, 891))

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
    by_status = {r["id"]: r.get("review_status") for r in records}

    # Assert SA_850 unchanged only if already gold
    boundary_id = "SA_850" if by_status.get("SA_850") in _goldish else None
    boundary_before = None
    if boundary_id:
        for rec in records:
            if rec["id"] == boundary_id:
                boundary_before = _snap(rec)
                break

    neighbor_ids = {f"SA_{i}" for i in list(range(831, 851)) + list(range(871, 891))}
    neighbors_before = {
        rec["id"]: _snap(rec) for rec in records if rec["id"] in neighbor_ids
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

    if boundary_id and boundary_before is not None:
        for rec in merged:
            if rec["id"] == boundary_id:
                assert boundary_before == _snap(rec), f"{boundary_id} must remain untouched"
                break

    for rid, before in neighbors_before.items():
        for rec in merged:
            if rec["id"] == rid:
                assert before == _snap(rec), f"{rid} (neighbor batch) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa851-870.json").write_text(
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
    continuous_851_870 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(851, 871)
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

    sa850_status = by_merged.get("SA_850", {}).get("review_status")
    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_851–SA_870 only)")
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
    print(f"continuous_gold_SA_851–870={continuous_851_870}")
    print(f"neighbors_831–850_871–890_untouched=True")
    if boundary_id:
        print(f"{boundary_id}_untouched=True (was gold)")
    else:
        print(f"SA_850_assert_skipped (status={sa850_status}, not gold)")
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
