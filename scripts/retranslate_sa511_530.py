#!/usr/bin/env python3
"""Retranslate SA 511–530（卷第二十一 弟子所说相应·业报喻）→ merge.

本批二十经：屠羊弟子、堕胎、调象、好战、猎师、杀猪、断人头、锻铜、
捕鱼、卜占女／师、好他淫、卖色、瞋恚灯油、憎嫉婆罗门、知事不分油、
盗七果、盗石蜜、盗二饼、比丘（及尼等）。

信：有 SN19 平行者据巴利／Sujato 厘义；汉本详于 SN 者从汉（如 523 卖色）；
    529 无可靠平行 → low。达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
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

OPEN_RAJ_LIT = "如是我闻：一时，佛在王舍城迦兰陀竹园。"
OPEN_RAJ_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

OPEN_VAR_LIT = "如是我闻：一时，佛在波罗奈国仙人住处鹿野苑。"
OPEN_VAR_MOD = "我是这样听说的：有一次，佛住在波罗奈国仙人处鹿野苑。"

OPEN_JET_LIT = "如是我闻：一时，佛在舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_JET_BRIEF_LIT = "如是我闻：一时，佛住舍卫国。"
OPEN_JET_BRIEF_MOD = "我是这样听说的：有一次，佛住在舍卫国。"

CLOSE_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_SHI_LIT = "佛说是经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_SHI_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

WITNESS_LIT = "诸比丘！如大目犍连所见，真实不虚，应当受持。"
WITNESS_MOD = "诸比丘！如同大目犍连所见的，真实不虚，你们应当受持。"

KARMA_TAIL_LIT = "缘斯罪故，堕地狱受无量苦；地狱余报，今得此身，续受其苦。"
KARMA_TAIL_MOD = "因为那个罪业的缘故，堕入地狱受无量苦；地狱的剩余果报，现在得到这样的身，继续承受那些苦。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」，本经作 medium。"
)


def _raj_vignette(
    vision_lit: str,
    vision_mod: str,
    place_lit: str,
    place_mod: str,
    crime_lit: str,
    crime_mod: str,
    *,
    extra_lit: str | None = None,
    extra_mod: str | None = None,
) -> tuple[list[str], list[str]]:
    """Abbreviated Rājagaha karma vignette (目连路见 → 佛释业)."""
    lit = [
        OPEN_RAJ_LIT,
        f"尊者大目犍连于路中见一大身众生，{vision_lit}，乘虚而行。",
        f"佛告诸比丘：「此众生者，过去于此{place_lit}为{crime_lit}，{KARMA_TAIL_LIT}{WITNESS_LIT}。」",
        CLOSE_LIT,
    ]
    mod = [
        OPEN_RAJ_MOD,
        f"大目犍连尊者在路中看见一个身躯巨大的众生，{vision_mod}，在空中飞行。",
        f"佛告诉比丘们：「这个众生，过去在此{place_mod}做{crime_mod}，"
        f"{KARMA_TAIL_MOD}{WITNESS_MOD}。」",
        CLOSE_MOD,
    ]
    if extra_lit:
        lit.insert(-1, extra_lit)
        mod.insert(-1, extra_mod or extra_lit)
    return lit, mod


def _mogg_report(
    open_lit: str,
    open_mod: str,
    vision_lit: str,
    vision_mod: str,
    place_lit: str,
    place_mod: str,
    crime_lit: str,
    crime_mod: str,
    *,
    close_lit: str = CLOSE_LIT,
    close_mod: str = CLOSE_MOD,
    extra_lit: str | None = None,
    extra_mod: str | None = None,
) -> tuple[list[str], list[str]]:
    """Moggallāna reports vision to Buddha (舍卫／鹿野 abbreviated)."""
    lit = [
        open_lit,
        f"尊者大目犍连言：「我于路中见一大身众生，{vision_lit}，乘虚而行，啼哭号呼。」",
        f"佛告诸比丘：「此众生者，过去于此{place_lit}为{crime_lit}，{KARMA_TAIL_LIT}{WITNESS_LIT}。」",
        close_lit,
    ]
    mod = [
        open_mod,
        f"大目犍连尊者说：「我在路中看见一个身躯巨大的众生，{vision_mod}，"
        f"在空中飞行，啼哭号呼。」",
        f"佛告诉比丘们：「这个众生，过去在此{place_mod}做{crime_mod}，"
        f"{KARMA_TAIL_MOD}{WITNESS_MOD}。」",
        close_mod,
    ]
    if extra_lit:
        lit.insert(-1, extra_lit)
        mod.insert(-1, extra_mod or extra_lit)
    return lit, mod


# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 511 屠羊弟子（SN 19.4 Nicchavi）------------------------------------
_lit, _mod = _raj_vignette(
    "举体无皮，形如脯腊",
    "全身没有皮，形状像干肉",
    "王舍城",
    "王舍城",
    "屠羊弟子",
    "屠羊的徒弟",
)
SUTTAS["SA_511"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.4 Nicchavi（剥皮／无皮身）。"
        "汉作屠羊弟子，巴利 orabbhiko 为屠羊；保留汉职业，删广本标题。"
    ),
}

# --- SA 512 堕胎（SN 19.3 Piṇḍa）--------------------------------------------
_lit, _mod = _raj_vignette(
    "举体无皮，形如肉段",
    "全身没有皮，只是一块肉",
    "王舍城",
    "王舍城",
    "自堕其胎",
    "自行堕胎的人",
)
SUTTAS["SA_512"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=medium：SN19.3 作肉块身，汉明确自堕其胎；"
        "义同为杀胎之业报，从汉本。"
    ),
}

# --- SA 513 调象士（SN 19.8 Sūciloma）---------------------------------------
_lit, _mod = _raj_vignette(
    "遍身生毛，毛如大针，针皆火然，还烧其体，痛彻骨髓",
    "遍身长毛，毛像大针，针都着火，反过来烧它的身体，痛彻骨髓",
    "王舍城",
    "王舍城",
    "调象士",
    "调象的人",
    extra_lit="如调象士，调马士、调牛士、好谗人及诸苦切人者，亦复如是。",
    extra_mod="如同调象的人，调马、调牛的人，好进谗言的人，以及种种苛刻折磨人的人，也是这样。",
)
SUTTAS["SA_513"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.8 Sūciloma（针毛烧身）；"
        "汉列调象／马／牛及谗人、苦切人，据汉保留并摄。"
    ),
}

# --- SA 514 好战（SN 19.9 Dutiyasūciloma）-----------------------------------
_lit, _mod = _raj_vignette(
    "举身生毛，毛利如刀，其毛火然，还割其体，痛彻骨髓",
    "全身长毛，毛尖像刀，毛着火，反过来割它的身体，痛彻骨髓",
    "王舍城",
    "王舍城",
    "好乐战诤、刀剑伤人者",
    "好斗战、以刀剑伤人的人",
)
SUTTAS["SA_514"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.9（针穿周身）；"
        "汉作好战刀剑，巴利作进谗，从汉本职业。"
    ),
}

# --- SA 515 猎师（SN 19.6 Satti）--------------------------------------------
_lit, _mod = _raj_vignette(
    "遍身生毛，其毛似箭，皆悉火然，还烧其身，痛彻骨髓",
    "遍身长毛，毛像箭，全都着火，反过来烧它的身体，痛彻骨髓",
    "王舍城",
    "王舍城",
    "猎师，射杀禽兽",
    "猎师，射杀飞禽走兽",
)
SUTTAS["SA_515"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.6 Satti（矛／箭毛烧身）；"
        "汉猎师射禽兽，与 SN 猎鹿义同。"
    ),
}

# --- SA 516 杀猪（SN 19.5 Asiloma）------------------------------------------
_lit, _mod = _raj_vignette(
    "举体生毛，毛如䂎矛，毛悉火然，还烧其身，痛彻骨髓",
    "全身长毛，毛像铁矛，毛都着火，反过来烧它的身体，痛彻骨髓",
    "王舍城",
    "王舍城",
    "屠猪人，䂎杀群猪",
    "屠猪的人，用矛刺杀群猪",
)
SUTTAS["SA_516"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.5 Asiloma（剑毛烧身）；"
        "汉屠猪，巴利杀猪，职业相应。"
    ),
}

# --- SA 517 断人头（SN 19.16 Asīsaka）--------------------------------------
_lit, _mod = _raj_vignette(
    "无头而身，两眼生胸，口在胸前，身常流血，诸虫唼食，痛彻骨髓",
    "没有头只有身，两只眼睛长在胸前，口也在胸前，身体常流血，各种虫来咬食，痛彻骨髓",
    "王舍城",
    "王舍城",
    "好断人首者",
    "喜欢砍人脑袋的人",
    extra_lit="如断人首，捉头者亦如是。",
    extra_mod="如同砍人首，捉人首的人也是这样。",
)
SUTTAS["SA_517"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.16 Asīsaka（无头身）；"
        "汉并摄捉头，据汉。"
    ),
}

# --- SA 518 锻铜师（SN 19.10 Kumbhaṇḍa）------------------------------------
_lit, _mod = _raj_vignette(
    "阴卵如瓮，坐则踞上，行则肩担",
    "阴部像瓮那么大，坐就坐在上面，走就用肩扛着",
    "王舍城",
    "王舍城",
    "锻铜师，以伪器欺人",
    "锻铜的工匠，用假器具欺骗人",
    extra_lit="如锻铜师，斗秤欺人、村主、市监，亦如是。",
    extra_mod="如同锻铜师，用斗秤欺骗人、村长、市监的人，也是这样。",
)
SUTTAS["SA_518"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.10 Kumbhaṇḍa（巨卵身）；"
        "汉锻铜伪器，并摄斗秤、村主、市监。"
    ),
}

# --- SA 519 捕鱼师（SN 19.7 Usuloma）----------------------------------------
_lit, _mod = _raj_vignette(
    "以铜铁罗网自缠其身，火常炽然，还烧其体，痛彻骨髓",
    "用铜铁罗网缠住自己，火常猛烈燃烧，反过来烧它的身体，痛彻骨髓",
    "王舍城",
    "王舍城",
    "捕鱼师",
    "捕鱼的人",
    extra_lit="如捕鱼师，捕鸟、网兔，亦如是。",
    extra_mod="如同捕鱼的人，捕鸟、网兔的人，也是这样。",
)
SUTTAS["SA_519"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.7 Usuloma（铁网烧身）；"
        "汉捕鱼，并摄捕鸟、网兔。"
    ),
}

# --- SA 520 卜占女（SN 19.14 Maṅgulitthi）----------------------------------
_lit, _mod = _raj_vignette(
    "顶有铁磨，盛火炽然，转磨其顶",
    "头顶有铁磨，盛满烈火，转动磨它的头顶",
    "王舍城",
    "王舍城",
    "卜占女人，转式惑人取财",
    "占卜的女人，转动式盘迷惑人骗取财物",
)
SUTTAS["SA_520"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.14 Maṅgulitthi（顶磨）；"
        "汉转式卜占，与 SN 女巫相应。"
    ),
}

# --- SA 521 卜占师（SN 19.2 Pesi）------------------------------------------
_lit, _mod = _raj_vignette(
    "其身独转，犹若旋风",
    "它的身体独自旋转，好像旋风",
    "王舍城",
    "王舍城",
    "卜占师，误惑多人取财",
    "占卜的人，误导许多人骗取财物",
)
SUTTAS["SA_521"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.2 Pesi（旋身如轮）；"
        "汉卜占师误惑取财。"
    ),
}

# --- SA 522 好他淫（SN 19.11）------------------------------------------------
_lit, _mod = _raj_vignette(
    "傴身藏行，举体被服悉皆火然，还烧其身",
    "弯身隐藏而行，全身所披所盖全都着火，反过来烧它的身体",
    "王舍城",
    "王舍城",
    "好行他淫者",
    "好与人通奸的人",
)
SUTTAS["SA_522"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.11（粪坑／火身）；"
        "汉作他淫火身，据汉。"
    ),
}

# --- SA 523 卖色（SN 19.13；汉详于 SN）--------------------------------------
SUTTAS["SA_523"] = {
    "lit": [
        OPEN_VAR_LIT,
        "时，尊者大目犍连与尊者勒叉那晨朝共入波罗奈城乞食。"
        "路中，大目犍连顾念微笑。勒叉那问：「尊者微笑，必有因缘？」"
        "大目犍连言：「非时问，且乞食，还诣世尊当问。」",
        "俱乞食已，洗足持钵，诣佛稽首，退坐一面。"
        "勒叉那复问：「晨朝路中，何缘微笑？」",
        "大目犍连言：「我见一大身众生，举体脓坏，臭秽不净，乘虚而行；"
        "乌、鵄、鵰、鷲、野干、饿狗随逐擭食，啼哭号呼。"
        "念众生得如是身、受如是苦，一何痛哉！」",
        "佛告诸比丘：「我亦见此众生而不说者，恐人不信；"
        "不信如来所说，愚痴长夜受苦。"
        "此众生者，过去于此波罗奈城，女人卖色自活。"
        "时有比丘于迦叶佛所出家；彼女以不清净心请之，比丘直心受请不解其意。"
        "女人瞋恚，以不净水洒比丘身。"
        "缘斯罪故，堕地狱受无量苦；地狱余报，今得此身，续受其苦。"
        + WITNESS_LIT
        + "」",
        CLOSE_SHI_LIT,
    ],
    "mod": [
        OPEN_VAR_MOD,
        "当时，大目犍连尊者与勒叉那尊者早晨一起入波罗奈城乞食。"
        "在路上，大目犍连尊者顾念而微笑。勒叉那尊者问：「尊者微笑，一定有因缘吧？」"
        "大目犍连尊者说：「现在不是问的时候，先去乞食，回到世尊面前再问。」",
        "一起乞食完毕，洗足拿着钵，到佛处顶礼，退坐一面。"
        "勒叉那尊者又问：「早晨在路上，为什么微笑？」",
        "大目犍连尊者说：「我看见一个身躯巨大的众生，全身脓烂，臭秽不净，在空中飞行；"
        "乌鸦、鸱鸮、雕、鹫、野干、饿狗追着啄食，啼哭号呼。"
        "想到众生得到这样的身、承受这样的苦，多么痛啊！」",
        "佛告诉比丘们：「我也看见这个众生却没有说，怕人不相信；"
        "不相信如来所说，愚痴的人长夜受苦。"
        "这个众生，过去在此波罗奈城，是一个卖色活命的女人。"
        "当时有一位比丘在迦叶佛时代出家；那女人以不清净的心邀请他，比丘心地正直接受了邀请，却不明白她的意思。"
        "女人瞋恚，用不净水洒在那位比丘身上。"
        "因为那个罪业的缘故，堕入地狱受无量苦；地狱的剩余果报，现在得到这样的身，继续承受那些苦。"
        + WITNESS_MOD
        + "」",
        CLOSE_SHI_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium：SN19.13 仅列通奸女剥皮，"
        "汉本详述迦叶时比丘、不清净请、洒水等，从汉；业报义不违。"
    ),
}

# --- SA 524 瞋恚灯油（SN 19.15 Okilinī）------------------------------------
_lit, _mod = _mogg_report(
    OPEN_VAR_LIT,
    OPEN_VAR_MOD,
    "举体火然，乘虚而行，啼哭号呼，受诸苦痛",
    "全身着火，在空中飞行，啼哭号呼，承受种种苦痛",
    "波罗奈城",
    "波罗奈城",
    "自在王第一夫人，起瞋恚心以然灯油洒王身",
    "自在王的第一夫人，起瞋恚心把燃着的灯油洒在王身上",
    close_lit=CLOSE_SHI_LIT,
    close_mod=CLOSE_SHI_MOD,
)
SUTTAS["SA_524"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.15 Okilinī（妒妇烧身）；"
        "汉作灯油洒王，SN 作热炭洒妾，妒害义同，从汉细节。"
    ),
}

# --- SA 525 憎嫉婆罗门（SN 19.12 Gūthakhāda）--------------------------------
_lit, _mod = _mogg_report(
    OPEN_VAR_LIT,
    OPEN_VAR_MOD,
    "举体粪秽，以涂其身，亦食粪秽，臭秽苦恼，啼哭号呼",
    "全身粪秽，用粪涂身，也吃粪秽，臭秽苦恼，啼哭号呼",
    "波罗奈城",
    "波罗奈城",
    "自在王师婆罗门，以憎嫉心请迦叶佛声闻僧，以粪著饭下试恼众僧",
    "自在王的师婆罗门，以憎嫉心请迦叶佛时代的声闻僧，把粪放在饭下面想恼乱众僧",
)
SUTTAS["SA_525"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.12 Gūthakhāda（食粪）；"
        "汉迦叶时以粪试僧，与 SN 请僧食粪相应。"
    ),
}

# --- SA 526 知事不分油（汉；近 SN 19 系）------------------------------------
_lit, _mod = _mogg_report(
    OPEN_JET_LIT,
    OPEN_JET_MOD,
    "头上有大铜鑊，炽然满中，群铜流灌身体，啼哭号呼",
    "头上有大铜锅，里面满盛烈火，滚铜流灌身体，啼哭号呼",
    "舍卫国",
    "舍卫国",
    "迦叶佛法中出家知事比丘，檀越送油不按时分待客比丘",
    "在迦叶佛时代出家做知事比丘，施主送油却不按时分给来访的比丘",
)
SUTTAS["SA_526"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{NO_PARALLEL}"
        "知事不分油、顶铜鑊灌身；SC 泛列 SN19 平行，无专经，从汉 medium。"
    ),
}

# --- SA 527 盗取七果（SN 19.19 系）------------------------------------------
_lit, _mod = _mogg_report(
    OPEN_JET_LIT,
    OPEN_JET_MOD,
    "有炽热铁丸从身出入，苦痛切迫，啼哭号呼",
    "有炽热的铁丸从身体进进出出，苦痛迫切，啼哭号呼",
    "舍卫国",
    "舍卫国",
    "迦叶佛法中出家沙弥，守众僧果园，盗取七果持奉和上",
    "在迦叶佛时代出家做沙弥，看守众僧的果园，偷取七枚果子上供给他的和尚",
)
SUTTAS["SA_527"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=medium：近 SN19.19 Pāpasikkhamāna（恶沙弥）系；"
        "汉盗七果、铁丸出入，据汉。"
    ),
}

# --- SA 528 盗食石蜜（SN 19.20 系）------------------------------------------
_lit, _mod = _mogg_report(
    OPEN_JET_BRIEF_LIT,
    OPEN_JET_BRIEF_MOD,
    "其舌广长，见有利釿，炎火炽然，以釿其舌，啼哭号呼",
    "它的舌头又宽又长，有利刃在，烈火炽燃，用刃割它的舌头，啼哭号呼",
    "舍卫国",
    "舍卫国",
    "迦叶佛法中出家沙弥，破石蜜供僧，著斧刃者盗取食之",
    "在迦叶佛时代出家做沙弥，破石蜜供养众僧，沾在斧刃上的偷取出来吃",
)
SUTTAS["SA_528"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=medium：近 SN19.20 Pāpasāmaṇera 系；"
        "汉盗食石蜜、舌受釿，据汉。"
    ),
}

# --- SA 529 盗取二饼（无平行）------------------------------------------------
_lit, _mod = _mogg_report(
    OPEN_JET_BRIEF_LIT,
    OPEN_JET_BRIEF_MOD,
    "有双铁轮在两胁下，炽然旋转，还烧其身，啼哭号呼",
    "有两个铁轮在两边胁下，猛烈旋转，反过来烧它的身体，啼哭号呼",
    "舍卫国",
    "舍卫国",
    "迦叶佛法中出家沙弥，持石蜜饼供僧，盗取二饼藏于掖下",
    "在迦叶佛时代出家做沙弥，拿石蜜饼供养众僧，偷取两个饼藏在腋下",
)
SUTTAS["SA_529"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{NO_PARALLEL}"
        "SC 未列专经；汉盗二饼、胁下铁轮，保守依汉，confidence 作 low。"
    ),
}

# --- SA 530 比丘（SN 19.17 Pāpabhikkhu）------------------------------------
_lit, _mod = _mogg_report(
    OPEN_JET_BRIEF_LIT,
    OPEN_JET_BRIEF_MOD,
    "以炽然铁叶缠其身，衣被床卧悉皆热铁，炎火炽然，食热铁丸，啼哭号呼",
    "用炽燃的铁叶缠住它的身，衣服、被褥、床席全是热铁，烈火炽燃，吃热的铁丸，啼哭号呼",
    "舍卫国",
    "舍卫国",
    "迦叶佛法中出家比丘，为众僧乞衣食，供僧之余辄自受用",
    "在迦叶佛时代出家做比丘，为众僧乞衣食，供养众僧之余就自己受用",
    extra_lit="如比丘，比丘尼、式叉摩那、沙弥、沙弥尼、优婆塞、优婆夷，亦如是。",
    extra_mod="如同比丘，比丘尼、式叉摩那、沙弥、沙弥尼、优婆塞、优婆夷，也是这样。",
)
SUTTAS["SA_530"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN19.17 Pāpabhikkhu（恶比丘火身）；"
        "汉为众乞衣食而自受用，并摄诸众。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_511": "high",
    "SA_512": "medium",
    "SA_513": "high",
    "SA_514": "high",
    "SA_515": "high",
    "SA_516": "high",
    "SA_517": "high",
    "SA_518": "high",
    "SA_519": "high",
    "SA_520": "high",
    "SA_521": "high",
    "SA_522": "high",
    "SA_523": "medium",
    "SA_524": "high",
    "SA_525": "high",
    "SA_526": "medium",
    "SA_527": "medium",
    "SA_528": "medium",
    "SA_529": "low",
    "SA_530": "high",
}

RECONSTRUCTED: dict[str, str] = {}

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
    assert set(GOLD) == {f"SA_{i}" for i in range(511, 531)}, (
        "GOLD must cover SA_511–SA_530 exactly"
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

    sa510_before = None
    for rec in records:
        if rec["id"] == "SA_510":
            sa510_before = json.dumps(
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

    for rec in merged:
        if rec["id"] == "SA_510" and sa510_before is not None:
            sa510_after = json.dumps(
                {
                    "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                    "modern_psychology_text": rec.get("modern_psychology_text"),
                    "notes": rec.get("notes"),
                    "review_status": rec.get("review_status"),
                    "confidence": rec.get("confidence"),
                },
                ensure_ascii=False,
            )
            assert sa510_before == sa510_after, "SA_510 must remain untouched"
            break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa511-530.json").write_text(
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
    continuous_530 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(1, 531)
    )
    continuous_511_530 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(511, 531)
    )

    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛", "如如"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_511–SA_530 only)")
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
    print(f"continuous_gold_SA_1–530={continuous_530}")
    print(f"continuous_gold_SA_511–530={continuous_511_530}")
    print(f"SA_510_untouched=True")
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
