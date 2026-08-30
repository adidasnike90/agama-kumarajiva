#!/usr/bin/env python3
"""Retranslate SA 172–187（卷第七／第八 斷知相應，信>达>雅）→ merge into final_translated_data.json.

斷知相應为「省文经」（peyyāla）之极致：每经正文仅出一式，末段以「一一八经」「三十二经」
等指示读者自行衍展。今于正文全出问答，于末段将省文指示译为可读之衍展说明，
并标出各组经数，使可通读而不失其结构。

信：SuttaCentral 平行表于 SA 172–187 十六经全未列巴利平行（parallels 皆空），
故不得伪托 SN 某经；今以汉本为底，参 Anālayo 英译（'On Views and Penetrative Knowledge —
A Translation of Saṁyukta-āgama Discourses 139 to 187 (Fascicle 7)', DDJBS 17, 2015）
及三十七道品之巴利定型语厘定法义，凡改求那跋陀罗字面者皆于 notes 具志。
因全相应无平行可据，依项目规约全批 confidence 上限为 medium（不作 high）。

达：白话与罗什风逐段对照，段数严格相同（build 时 assert，merge 时记 paragraph_parallel）。
雅：文言栏与底本之三元组相似度须 < 0.55，否则记 needs_restyle（繁转简闸）。
底本术语已讹、须依经内经数回填法数者（SA_184 四通行、SA_185 三法句）标 gold_reconstructed。
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

# 救头然譬（SA 175、177–186）
FIRE_Q_LIT = "尔时世尊告诸比丘：如人头衣被火所烧，当云何救？"
FIRE_Q_MOD = "那时，世尊告诉比丘们：譬如有人头上的巾衣被火烧着了，该怎么救？"
FIRE_A_LIT = "诸比丘白佛：世尊！当起增上欲，慇懃方便，急救令灭。"
FIRE_A_MOD = "比丘们对佛说：世尊！应当生起最猛利的意愿，殷勤设法，赶紧把火扑灭。"

ELL_LIT = "（如上广说，乃至……）"
ELL_MOD = "（此处原典省文，余者如上广说，乃至经末。）"

# 三世八经（凡末段「如无常，如是过去无常……」皆同此式）
EIGHT_LIT = (
    "（省文）如「无常」，如是过去无常、未来无常、现在无常、过去未来无常、"
    "过去现在无常、未来现在无常、过去未来现在无常，一一如上广说，成八经。"
)
EIGHT_MOD = (
    "（以下是原典的省文指示）把上面的「无常」依次换成过去无常、未来无常、现在无常、"
    "过去与未来无常、过去与现在无常、未来与现在无常、过去未来现在无常，"
    "各按同一格式成一部经，共八部。"
)


def senses_tail(count_lit: str, count_mod: str) -> tuple[str, str]:
    """末段「如当断N经，如是当知、当吐……一一N经」之八义衍展。"""
    lit = (
        f"如「当断」{count_lit}经，如是「当知」、「当吐」、「当尽」、「当止」、"
        f"「当舍」、「当灭」、「当没」，一一亦{count_lit}经，皆如上说。"
    )
    mod = (
        f"以「应当断除」为纲有{count_mod}部经；同样以「应当了知」、「应当吐弃」、"
        f"「应当灭尽」、「应当止息」、「应当舍离」、「应当灭除」、「应当令其隐没」为纲，"
        f"每一项也各有{count_mod}部经。"
    )
    return lit, mod


def fire_body(
    prac_lit: str,
    prac_mod: str,
    urge_lit: str = "当尽断灭",
    urge_mod: str = "却应当断尽",
    ellipsis: bool = True,
) -> tuple[str, str]:
    """救头然譬之佛答段：为断无常火故，当修某法。"""
    lit = (
        f"佛告比丘：头衣烧然，尚可暂忘；无常盛火，{urge_lit}。"
        f"为断无常火故，当{prac_lit}。断何等无常故当{prac_lit}？"
        f"谓断色无常故当{prac_lit}，断受、想、行、识无常故当{prac_lit}。"
    )
    mod = (
        f"佛告诉比丘们：头巾着火，还可以暂时忘却；无常这场大火，{urge_mod}。"
        f"为了断除无常之火，应当{prac_mod}。为断除什么样的无常，才应当{prac_mod}呢？"
        f"就是说：为断除色的无常，应当{prac_mod}；为断除受、想、行、识的无常，应当{prac_mod}。"
    )
    if ellipsis:
        lit += ELL_LIT
        mod += ELL_MOD
    return lit, mod


# notes 共用前言：诚实交代平行阙如与所依
PROV = (
    "SuttaCentral 平行表于断知相应（SA 172–187）未列任何巴利平行，故不托 SN 某经；"
    "今以汉本为底，参 Anālayo 英译（DDJBS 17, 2015）及道品巴利定型语厘定法义。"
)

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}


# --- SA 172 无常法当断 -------------------------------------------------------
SUTTAS["SA_172"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：诸法无常者，一切当断。断彼法已，则得义利，长夜安乐。"
        "何法无常？色是无常，受、想、行、识是无常。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：凡是无常的法，都应当断除。断除了它，便得到真实的利益，"
        "长久安乐。什么是无常的？色是无常的，受、想、行、识是无常的。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "「以义饶益，长夜安乐」为巴利 atthāya hitāya sukhāya 一类定型语（Anālayo："
        "for your benefit and welfare, for your peace and happiness for a long time），"
        "今作「则得义利，长夜安乐」，取其义而去其calque。"
        "「若法无常者当断」之「断」（pahāna）所断非色法自身，乃于无常法之欲贪，"
        "此意由次经（SA_173）「过去色是无常法，过去欲是无常法」显之，故本经存其略而不增字。"
    ),
}


# --- SA 173 过去无常法当断 ---------------------------------------------------
SUTTAS["SA_173"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：过去无常之法，一切当断。断彼法已，则得义利，长夜安乐。"
        "云何过去无常法？过去色是无常法，于过去色之欲亦是无常法，是法当断；"
        "断彼法已，则得义利，长夜安乐。受、想、行、识亦复如是。",
        CLOSE_LIT,
        "（省文）如「过去」，如是未来、现在、过去现在、未来现在、过去未来、"
        "过去未来现在，一一如上说，各成一经。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：凡属过去而无常的法，都应当断除。断除了它，便得到真实的利益，"
        "长久安乐。什么是过去而无常的法？过去的色是无常之法，对过去之色所起的欲也是无常之法，"
        "这些都应当断除；断除了它，便得到真实的利益，长久安乐。受、想、行、识也是一样。",
        CLOSE_MOD,
        "（以下是原典的省文指示）把「过去」依次换成未来、现在、过去与现在、未来与现在、"
        "过去与未来、过去未来现在，各按同一格式成一部经。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium。「过去欲是无常法」之「欲」，Anālayo 读作 past desire [for it]，"
        "即缘过去色所起之欲（chanda／rāga），非另立一「欲」法；今译作「于过去色之欲」以显其所缘，"
        "并因此可知前经（SA_172）「无常法当断」之所断实在欲贪。"
        "汉本末段列世相仅七项而缺「过去未来」之一序，今依三世八经通例补足语序，不增法义。"
    ),
}


# --- SA 174 求大师 -----------------------------------------------------------
_TEACHER_EPITHETS_LIT = (
    "种种教、随顺教、安、广安、周普安、导、广导、究竟导、说、广说、随顺说、"
    "第二伴、真知识、同意、愍、悲、崇义、崇安慰、乐、崇触、崇安隐、"
    "欲、精进、方便、广方便、堪能方便、坚固、强健、勇猛身心、勇猛难伏、"
    "摄受常学、不放逸修、思惟、念、觉、知、明、慧、辩、思量、梵行、如意、"
    "念处、正勤、根、力、觉、道、止、观、念身、正忆念"
)
SUTTAS["SA_174"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：为断无常法故，当求大师。云何无常法？谓色是无常法；"
        "为断彼法，当求大师。受、想、行、识亦复如是。",
        CLOSE_LIT,
        "（省文）如是过去、未来、现在、过去未来现在无常，皆当求大师，成八种经。",
        f"如「求大师」，如是{_TEACHER_EPITHETS_LIT}，一一亦成八经，皆如上说。",
        "如「当断」义，如是「当知」义、「当尽」义、「当吐」义、「当止」义、「当舍」义亦如是。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：为了断除无常之法，应当寻求大师。什么是无常之法？"
        "就是说：色是无常之法；为断除它，应当寻求大师。受、想、行、识也是一样。",
        CLOSE_MOD,
        "（以下是原典的省文指示）把「无常」换成过去、未来、现在乃至过去未来现在无常，"
        "都说「应当寻求大师」，共成八部经。",
        "「大师」（导师）一名之外，原典又列约五十个称谓，可一一替换成经；今按义类略举："
        "就其教导说——种种教、随顺教、说、广说、随顺说、导、广导、究竟导；"
        "就其与人安隐说——安、广安、周普安、崇安慰、崇安隐、乐、崇触；"
        "就其为友说——第二伴（同行之友）、真知识（善友）、同意、愍、悲、崇义；"
        "就其精勤说——欲、精进、方便、广方便、堪能方便、坚固、强健、勇猛身心、勇猛难伏、"
        "摄受常学、不放逸修；"
        "就其智慧说——思惟、念、觉、知、明、慧、辩、思量、梵行、如意；"
        "就其道品说——念处、正勤、根、力、觉支、道支、止、观、念身、正忆念。"
        "以上每一项，也各按三世成八部经。",
        "以「应当断除」为纲既如上说，以「应当了知」、「应当灭尽」、「应当吐弃」、"
        "「应当止息」、「应当舍离」为纲的，也是一样。",
    ],
    "notes": (
        f"{PROV}"
        "「大师」即 satthā（导师），非后世「大师」之尊称；末段所列诸名皆善师善友之异称，"
        "至「念处、正勤、根、力、觉、道、止、观」则已转为所修道品之名（Anālayo 同此读）。"
        "「第二伴」即同行之伴（dutiya），「真知识」即善友（kalyāṇamitta），"
        "「崇安隐」「崇安慰」之「崇」为「尚、务」，今于现代栏显其义。"
        "汉本此段名相冗长而无句读之别，今于文言栏存其全列以志底本，于现代栏按义类分组以便通读。"
    ),
}


# --- SA 175 烧头衣（求大师）--------------------------------------------------
_f175_lit, _f175_mod = fire_body(
    "勤求大师",
    "殷勤寻求大师",
    urge_lit="应尽除断灭",
    urge_mod="却须彻底除断、灭尽",
    ellipsis=False,
)
SUTTAS["SA_175"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f175_lit,
        CLOSE_LIT,
        EIGHT_LIT + "是名八种救头然譬经。",
        "如「求大师」，如是求种种教、随顺教等，亦如上广说。",
        "如「断」义，如是「知」义、「尽」义、「吐」义、「止」义、「舍」义、"
        "「灭」义、「没」义，亦复如是。",
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f175_mod,
        CLOSE_MOD,
        EIGHT_MOD + "这就是以「救头上之火」为譬的八部经。",
        "如同「寻求大师」，同样寻求种种教导者、随顺教导者等等，也照上面详说。",
        "如同以「断除」为纲，同样以「了知」、「灭尽」、「吐弃」、「止息」、「舍离」、"
        "「灭除」、「隐没」为纲的，也是一样。",
    ],
    "notes": (
        f"{PROV}"
        "「火烧头衣」即巴利 ādittacela／ādittasīsa（头衣着火、头颅着火）之譬，"
        "巴利同譬见 SN56.34（Cela），彼以四圣谛为所急，此以无常为所急；"
        "此係教理上之同式，非 SuttaCentral 平行表所列，故仅作参照，不入平行。"
        "「当起增上欲，慇懃方便」即 adhimattaṁ chandañca vāyāmañca ussāhañca（增上之欲、精勤、努力），"
        "今作「当起增上欲，慇懃方便，急救令灭」，取其急切之势。"
        "「头衣烧然尚可暂忘」一句为汉译之妙笔：非谓头火可忘，乃谓无常之火更急于头火，故存之。"
    ),
}


# --- SA 176 内身身观住（四念处）---------------------------------------------
_MINDFULNESS_12_LIT = (
    "外身观身而住、内外身观身而住、内受观受而住、外受观受而住、内外受观受而住、"
    "内心观心而住、外心观心而住、内外心观心而住、内法观法而住、外法观法而住、"
    "内外法观法而住"
)
SUTTAS["SA_176"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：为断无常故，当随修内身观身而住。何等法无常？谓色无常；"
        "为断彼故，当随修内身观身而住。如是受、想、行、识无常；为断彼故，"
        "当随修内身观身而住。",
        CLOSE_LIT,
        "（省文）如「色无常」，如是过去色、未来色、现在色、过去未来色、过去现在色、"
        "未来现在色、过去未来现在色无常，为断彼故，当随修内身观身而住；"
        "受、想、行、识亦复如是，成八经。",
        f"如「内身观身而住」八经，如是{_MINDFULNESS_12_LIT}，一一亦八经，皆如上说。",
        "如为断无常义而修四念处，如是为「知」义、「尽」义、「吐」义、「止」义、"
        "「舍」义、「灭」义、「没」义而随修四念处，亦如上说。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：为了断除无常，应当依内身而观身安住。什么法是无常的？"
        "就是说：色是无常的；为断除它，应当依内身而观身安住。受、想、行、识同样是无常的；"
        "为断除它们，应当依内身而观身安住。",
        CLOSE_MOD,
        "（以下是原典的省文指示）把「色无常」依次换成过去之色、未来之色、现在之色、"
        "过去与未来之色、过去与现在之色、未来与现在之色、过去未来现在之色无常，"
        "都说「为断除它，应当依内身而观身安住」；受、想、行、识也照此办，共成八部经。",
        "如同「依内身而观身安住」有八部经，同样依外身观身、依内外身观身，"
        "依内受观受、依外受观受、依内外受观受，依内心观心、依外心观心、依内外心观心，"
        "依内法观法、依外法观法、依内外法观法而安住，每一项也各有八部经（合十二门九十六经）。",
        "如同为断除无常而修四念处，同样为「了知」、「灭尽」、「吐弃」、「止息」、"
        "「舍离」、「灭除」、「隐没」而修四念处，也照上面说。",
    ],
    "notes": (
        f"{PROV}"
        "「随修内身身观住」即巴利 ajjhattaṁ kāye kāyānupassī viharati（于内身循身观而住），"
        "求那跋陀罗「身身观住」为逐字对译，汉语读之不顺；今作「随修内身观身而住」，"
        "存「观身如身」之义而顺汉语（Anālayo：be established in contemplating the internal body as a body）。"
        "内、外、内外三门配身、受、心、法四念处成十二门，各依三世八相，故成九十六经，"
        "与次经（SA_177）末段「九十六经」之数相合。"
    ),
}


# --- SA 177 烧头衣（四念处）--------------------------------------------------
_f177_lit, _f177_mod = fire_body(
    "随修内身观身而住",
    "依内身而观身安住",
    urge_lit="应尽断灭",
    urge_mod="却应当断尽",
)
SUTTAS["SA_177"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f177_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如「内身观身而住」八经，如是「外身观身而住」八经、「内外身观身而住」八经，"
        "皆如上说。",
        "如身念处二十四经，如是受念处、心念处、法念处，一一亦二十四经，如上说。",
        senses_tail("九十六", "九十六")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f177_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同「依内身而观身安住」有八部经，同样「依外身而观身安住」八部、"
        "「依内外身而观身安住」八部，都照上面说。",
        "如同身念处共二十四部经（内、外、内外三门各八），同样受念处、心念处、法念处，"
        "每一项也各有二十四部经，合为九十六部。",
        senses_tail("九十六", "九十六")[1],
    ],
    "notes": (
        f"{PROV}"
        "本经即 SA_176 之救头然譬本；「身身观住」之译语问题同前经。"
        "末段之数可校：三门（内、外、内外）×八相（三世七合并一总）＝二十四，"
        "四念处×二十四＝九十六，故「当断无常九十六经」，「当知」以下七义亦各九十六经。"
        "「广说乃至」之省文，今于文言栏以括注存之，不伪作全文。"
    ),
}


# --- SA 178 四正断 -----------------------------------------------------------
_178_LIT = (
    "佛告比丘：头衣烧然，尚可暂忘；无常盛火，应尽断灭。为断无常火故，"
    "已生恶不善法当断，起欲、发勤、精进、摄心、持心，令其增长。"
    "断何等无常法故，为断已生恶不善法而起欲、方便、摄心增进？"
    "谓色无常，受、想、行、识无常，为断彼故，令已生恶不善法断，"
    "起欲、方便、摄心增进。" + ELL_LIT
)
_178_MOD = (
    "佛告诉比丘们：头巾着火，还可以暂时忘却；无常这场大火，却应当断尽。"
    "为了断除无常之火，对已经生起的恶不善法应当断除——生起意愿、发起勤勇、精进不懈、"
    "摄持自心，使这断除之力增长。为断除什么样的无常，才为断除已生的恶不善法而"
    "生起意愿、设法、摄心增进呢？就是说：色是无常的，受、想、行、识是无常的，"
    "为断除它们，便使已生的恶不善法断除，生起意愿、设法、摄心增进。" + ELL_MOD
)
SUTTAS["SA_178"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _178_LIT,
        CLOSE_LIT,
        EIGHT_LIT,
        "如「已生恶不善法当断」，如是「未生恶不善法令不生」、「未生善法令生」、"
        "「已生善法令增广」，各起欲、方便、摄心增进，一一亦八经，皆如上说。",
        senses_tail("三十二", "三十二")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _178_MOD,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同「已生的恶不善法应当断除」，同样「未生的恶不善法使它不生」、"
        "「未生的善法使它生起」、「已生的善法使它增广」，各自都生起意愿、设法、摄心增进，"
        "每一项也各有八部经（四正断合三十二经）。",
        senses_tail("三十二", "三十二")[1],
    ],
    "notes": (
        f"{PROV}"
        "本经所修为四正断（cattāro sammappadhānā，汉旧译四正勤）：断已生恶、防未生恶、"
        "生未生善、增已生善。「起欲、精勤、摄心令增长」即巴利定型语 chandaṁ janeti vāyamati "
        "vīriyaṁ ārabhati cittaṁ paggaṇhāti padahati（起欲、精勤、发勤、摄心、持心），"
        "求那跋陀罗略作「起欲、方便、摄心增进」，「方便」即 vāyāma（精勤）之意译，非「便宜」；"
        "今于首出处补足五支，后仍存汉本略语以见其省文之迹。"
    ),
}


# --- SA 179 四神足 -----------------------------------------------------------
_f179_lit, _f179_mod = fire_body(
    "修欲三昧勤行成就神足",
    "修习「由欲而得的三昧、以精勤之行成就」的神足",
)
SUTTAS["SA_179"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f179_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如修「欲三昧」，如是「精进三昧」、「心三昧」、「思惟三昧」，"
        "一一亦八经，皆如上说。",
        senses_tail("三十二", "三十二")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f179_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同修习「由欲而得的三昧」，同样修习「由精进而得的三昧」、「由心而得的三昧」、"
        "「由观察思惟而得的三昧」，每一项也各有八部经（四神足合三十二经）。",
        senses_tail("三十二", "三十二")[1],
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium。「欲定断行成就如意足」为巴利 chanda-samādhi-padhāna-saṅkhāra-"
        "samannāgata-iddhipāda 之逐字对译，其中「断行」实译 padhāna-saṅkhāra（勤行、精勤之造作），"
        "非「断除之行」；求那跋陀罗以「断」译 padhāna，与本相应通篇之「断」（pahāna）同字异义，"
        "极易致误。今据巴利改写为「欲三昧勤行成就神足」，并于现代栏显作「由欲而得的三昧、"
        "以精勤之行成就」（Anālayo：the base for supernormal power endowed with concentration "
        "due to desire and formations of striving）。"
        "「如意足」即 iddhipāda，今作「神足」以从通译。四足之第三、第四，汉本作「意定」「思惟定」，"
        "即 citta-samādhi 与 vīmaṁsā-samādhi，今作「心三昧」「思惟三昧」。"
    ),
}


# --- SA 180 五根 -------------------------------------------------------------
_f180_lit, _f180_mod = fire_body("修信根", "修习信根")
SUTTAS["SA_180"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f180_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如「信根」八经，如是修精进根、念根、定根、慧根，一一亦八经，皆如上说。",
        senses_tail("四十", "四十")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f180_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同「信根」有八部经，同样修习精进根、念根、定根、慧根，"
        "每一项也各有八部经（五根合四十经）。",
        senses_tail("四十", "四十")[1],
    ],
    "notes": (
        f"{PROV}"
        "五根即 pañcindriya：信（saddhā）、精进（vīriya）、念（sati）、定（samādhi）、慧（paññā）。"
        "「信根」之信为 saddhā（信赖、确信），非盲信；Anālayo 作 the faculty of confidence，"
        "今存旧译「信根」而于注显其义。"
    ),
}


# --- SA 181 五力 -------------------------------------------------------------
_f181_lit, _f181_mod = fire_body("修信力", "修习信力")
SUTTAS["SA_181"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f181_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如「信力」，如是精进力、念力、定力、慧力，一一亦八经，皆如上说。",
        senses_tail("四十", "四十")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f181_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同「信力」，同样精进力、念力、定力、慧力，"
        "每一项也各有八部经（五力合四十经）。",
        senses_tail("四十", "四十")[1],
    ],
    "notes": (
        f"{PROV}"
        "五力即 pañca balāni，名目与五根同（信、精进、念、定、慧），"
        "所异者在「根」为能生之机，「力」为不可屈之势，故别立一相应之经群。"
    ),
}


# --- SA 182 七觉支 -----------------------------------------------------------
_f182_lit, _f182_mod = fire_body("修念觉支", "修习念觉支")
SUTTAS["SA_182"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f182_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如「念觉支」八经，如是择法觉支、精进觉支、喜觉支、轻安觉支、舍觉支、定觉支，"
        "一一亦八经，皆如上说。",
        senses_tail("五十六", "五十六")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f182_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同「念觉支」有八部经，同样择法觉支、精进觉支、喜觉支、轻安觉支、舍觉支、定觉支，"
        "每一项也各有八部经（七觉支合五十六经）。",
        senses_tail("五十六", "五十六")[1],
    ],
    "notes": (
        f"{PROV}"
        "七觉支即 satta bojjhaṅgā：念（sati）、择法（dhammavicaya）、精进（vīriya）、"
        "喜（pīti）、轻安（passaddhi）、定（samādhi）、舍（upekkhā）。"
        "汉本作「觉分」，今作「觉支」以从通译；「除觉分」即 passaddhi-sambojjhaṅga，"
        "「除」谓身心之猗息，今据巴利作「轻安觉支」，不作「除去」解。"
    ),
}


# --- SA 183 八正道 -----------------------------------------------------------
_f183_lit, _f183_mod = fire_body("修正见", "修习正见")
SUTTAS["SA_183"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f183_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如「正见」八经，如是正志、正语、正业、正命、正方便、正念、正定，"
        "一一亦八经，皆如上说。",
        senses_tail("六十四", "六十四")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f183_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同「正见」有八部经，同样正志（正思惟）、正语、正业、正命、"
        "正方便（正精进）、正念、正定，每一项也各有八部经（八正道合六十四经）。",
        senses_tail("六十四", "六十四")[1],
    ],
    "notes": (
        f"{PROV}"
        "八正道即 ariyo aṭṭhaṅgiko maggo。汉本「正志」即 sammāsaṅkappa（正思惟），"
        "「正方便」即 sammāvāyāma（正精进）；「方便」为 vāyāma 之意译，同 SA_178 之例。"
        "今文言栏存旧译名目以合汉传八正道之称，现代栏括注其巴利本义。"
    ),
}


# --- SA 184 四通行 -----------------------------------------------------------
_f184_lit, _f184_mod = fire_body(
    "修苦迟通行",
    "修习「苦而迟得通达」之行迹",
    urge_lit="当尽断灭无余",
    urge_mod="却应当断尽无余",
)
SUTTAS["SA_184"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f184_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如「苦迟通行」八经，如是苦速通行、乐迟通行、乐速通行，"
        "一一亦八经，皆如上说。",
        senses_tail("三十二", "三十二")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f184_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同「苦而迟得通达」之行有八部经，同样「苦而速得通达」、「乐而迟得通达」、"
        "「乐而速得通达」，每一项也各有八部经（四种行迹合三十二经）。",
        senses_tail("三十二", "三十二")[1],
    ],
    "notes": (
        f"{PROV}"
        "review_status=gold_reconstructed，confidence=low：四道之名非底本语面之直译，"
        "乃依经内「三十二经」之数回填之法数。"
        "汉本作「苦习尽道」，末段并列「苦尽道、乐非尽道、乐尽道」，"
        "合四项而各成八经，总三十二经，与末段「三十二经」之数正合。"
        "据此四项之数与其「苦／乐」「习尽（迟）／尽（速）」之对，当即巴利四通行"
        "（catasso paṭipadā，AN4.162 一类）：dukkhā paṭipadā dandhābhiññā（苦迟通行）、"
        "dukkhā paṭipadā khippābhiññā（苦速通行）、sukhā paṭipadā dandhābhiññā（乐迟通行）、"
        "sukhā paṭipadā khippābhiññā（乐速通行）；Anālayo 末段亦如此读"
        "（the painful not immediate path 等）。"
        "另一读法以「苦、习、尽、道」为四圣谛（Anālayo 正文如此译），然若作四谛则不得四项八经之数，"
        "故本篇从四通行之读，而志此异说，降置信度为 medium。"
    ),
}


# --- SA 185 法句 -------------------------------------------------------------
_f185_lit, _f185_mod = fire_body(
    "修无贪法句",
    "修习「无贪」这一法句",
    urge_lit="当尽断灭无余",
    urge_mod="却应当断尽无余",
)
SUTTAS["SA_185"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f185_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如「当修无贪法句」八经，如是「无恚」、「无痴」诸句、正句、法句，"
        "一一亦八经，皆如上说。",
        senses_tail("二十四", "二十四")[0],
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f185_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同「应当修习无贪法句」有八部经，同样「无瞋」、「无痴」这些法句、正句，"
        "每一项也各有八部经（三法句合二十四经）。",
        senses_tail("二十四", "二十四")[1],
    ],
    "notes": (
        f"{PROV}"
        "review_status=gold_reconstructed，confidence=low：法句之数依经内「二十四经」之数"
        "定为三法句，非底本明言。"
        "「法句」即 dhammapada（法之句、法之足处）。"
        "巴利四法句（AN4.29）为 anabhijjhā（无贪）、abyāpāda（无恚）、sammāsati（正念）、"
        "sammāsamādhi（正定）；汉本此处只三项——无贪、无恚、无痴，"
        "以「无痴」代巴利之正念、正定，且总数二十四经（三×八）与巴利之四句不合。"
        "今存汉本之三句而志其与巴利之异，不强改为四句，故降置信度。"
        "「无恚」之恚为 byāpāda（瞋害之意），非仅怒气。"
    ),
}


# --- SA 186 止观 -------------------------------------------------------------
_f186_lit, _f186_mod = fire_body("修止", "修习止（心的安定）")

_186_NOT_SELF_LIT = (
    "尔时世尊复告诸比丘：诸所有色，若过去、若未来、若现在，若内、若外，"
    "若粗、若细，若好、若丑，若远、若近，彼一切非我、非异我、不相在，如实知之；"
    "受、想、行、识亦复如是。多闻圣弟子如是正观者，于色生厌，于受、想、行、识生厌；"
    "厌故离贪，离贪故解脱，解脱知见：「我生已尽，梵行已立，所作已作，"
    "自知不受后有。」"
)
_186_NOT_SELF_MOD = (
    "那时，世尊又告诉比丘们：凡所有色——无论过去、未来、现在，内、外，粗、细，"
    "好、丑，远、近——这一切都非我、非异我、不相在，应当如实了知；"
    "受、想、行、识也是一样。多闻圣弟子这样正观的人，对色生起厌离，"
    "对受、想、行、识生起厌离；厌离了便不再贪乐，不贪乐便得解脱，"
    "解脱而知见：「我的生已尽，梵行已立，该做的已做，自知不再受后有。」"
)

_186_SYNONYMS_LIT = (
    "（省文）如「无常」，如是动摇、旋转、尫瘵、破坏、飘疾、朽败、危顿、不恒、不安、"
    "变易、恼苦、灾患、魔邪、魔势、魔器，如沫、如泡、如芭蕉、如幻，微劣、贪嗜、"
    "杀摽、刀剑、疾妒、相残、损减、衰耗、系缚、搥打、恶疮、痈疽、利刺、烦恼、"
    "谪罚、阴盖、过患、处愁、戚、恶知识，苦、空、非我、非我所，怨家连锁，"
    "非义、非安慰，热恼、无荫、无洲、无覆、无依、无护，生法、老法、病法、死法、"
    "忧悲法、恼苦法、无力法、羸劣法、不可欲法、诱引法、将养法、有苦法、有杀法、"
    "有恼法、有热法、有相法、有吹法、有取法、深崄法、难涩法、不正法、凶暴法、"
    "有贪法、有恚法、有痴法、不住法、烧然法、罣阂法、灾法、集法、灭法、骨聚法、"
    "肉段法、执炬法、火坑法，如毒蛇、如梦价借、如树果、如屠牛者、如杀人者、"
    "如触露、如淹水、如驶流、如织缕、如轮沙水、如跳杖、如毒瓶、如毒身、如毒华、"
    "如毒果、烦恼动，一一皆如「无常」例说。"
)
_186_SYNONYMS_MOD = (
    "（以下是原典的省文指示）除「无常」之外，原典又列约一百一十个同类异名，"
    "可一一替换而各成一经；今按义类略分如下："
    "一、动转不停之名——动摇、旋转、飘疾、不恒、不安、变易、不住；"
    "二、病坏危亡之名——尫瘵（羸病）、破坏、朽败、危顿、损减、衰耗、恶疮、痈疽、利刺、"
    "生法、老法、病法、死法、羸劣法、无力法；"
    "三、苦恼灾患之名——恼苦、灾患、烦恼、谪罚（责罚）、过患、处愁、戚（忧戚）、忧悲法、"
    "热恼、有苦法、有恼法、有热法、灾法、烦恼动；"
    "四、魔所摄之名——魔邪、魔势、魔器；"
    "五、虚伪不实之譬——如沫、如泡、如芭蕉、如幻、如梦价借（如梦中借来之物）、微劣；"
    "六、杀害之譬——杀摽（击杀）、刀剑、相残、有杀法、如毒蛇、如屠牛者、如杀人者、"
    "执炬法（如逆风持火炬）、火坑法、如毒瓶、如毒身、如毒华、如毒果、骨聚法、肉段法；"
    "七、贪染系缚之名——贪嗜、疾妒、有贪法、有恚法、有痴法、诱引法、有取法、系缚、搥打、"
    "怨家连锁（如仇家之锁链）、阴盖（为五阴所覆）、罣阂法（障碍）、恶知识；"
    "八、无依无救之名——非义、非安慰、无荫、无洲（无洲渚可依）、无覆、无依、无护、"
    "不可欲法、将养法（须时时调养）、深崄法、难涩法、不正法、凶暴法、烧然法；"
    "九、流迁不住之譬——如树果、如触露、如淹水、如驶流（急流）、如织缕、如轮沙水、如跳杖；"
    "十、直显法义之名——苦、空、非我、非我所，以及集法、灭法、有相法、有吹法。"
    "凡此诸名，都照「无常」的格式各成一经。"
)

_186_SAMATHA2_LIT = (
    "佛复告诸比丘：如是，比丘！乃至为断过去、未来、现在无常，乃至令其灭、没，"
    "当修止观。断何等法过去、未来、现在无常，乃至灭没，而修止观？"
    "谓为断色过去、未来、现在无常，乃至灭没故，修止观；受、想、行、识亦复如是。"
)
_186_SAMATHA2_MOD = (
    "佛又告诉比丘们：就是这样，比丘们！乃至为了断除过去、未来、现在的无常，"
    "乃至使它灭除、隐没，应当修习止与观。为断除什么法的过去、未来、现在之无常，"
    "乃至令其灭没，而修止观呢？就是说：为断除色的过去、未来、现在之无常，"
    "乃至令其灭没，而修止观；受、想、行、识也是一样。"
)

SUTTAS["SA_186"] = {
    "lit": [
        OPEN_LIT,
        FIRE_Q_LIT,
        FIRE_A_LIT,
        _f186_lit,
        CLOSE_LIT,
        EIGHT_LIT,
        "如修「止」八经，如是修「观」亦八经，皆如上说。",
        senses_tail("十六", "十六")[0],
        _186_NOT_SELF_LIT,
        CLOSE_LIT,
        _186_SYNONYMS_LIT,
        _186_SAMATHA2_LIT,
        "是故诸所有色，若过去、若未来、若现在，若内、若外，若粗、若细，若好、若丑，"
        "若远、若近，彼一切非我、非异我、不相在，如实知之。受、想、行、识亦复如是。",
        "多闻圣弟子如是观者，于色生厌，于受、想、行、识生厌；厌故离贪，离贪故解脱，"
        "解脱知见：「我生已尽，梵行已立，所作已作，自知不受后有。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        FIRE_Q_MOD,
        FIRE_A_MOD,
        _f186_mod,
        CLOSE_MOD,
        EIGHT_MOD,
        "如同修「止」有八部经，同样修「观」也有八部经。",
        senses_tail("十六", "十六")[1],
        _186_NOT_SELF_MOD,
        CLOSE_MOD,
        _186_SYNONYMS_MOD,
        _186_SAMATHA2_MOD,
        "因此，凡所有色——无论过去、未来、现在，内、外，粗、细，好、丑，远、近——"
        "这一切都非我、非异我、不相在，应当如实了知。受、想、行、识也是一样。",
        "多闻圣弟子这样观察的人，对色生起厌离，对受、想、行、识生起厌离；"
        "厌离便不再贪乐，不贪乐便得解脱，解脱而知见："
        "「我的生已尽，梵行已立，该做的已做，自知不再受后有。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "「止」「观」即 samatha 与 vipassanā（Anālayo：tranquillity／insight）。"
        "本经底本实合三段：救头然譬之止观八经、五阴非我而生厌解脱之全经、"
        "及无常百余异名之省文列并再出止观。今于文言栏依底本次第分段，不并合、不删经末重出，"
        "以存断知相应「一式衍多经」之体裁。"
        "「非我、非异我、不相在」即 na attā, na aññatra attā, na aññamaññassa（非我、非我所、不相在）"
        "一类否定式，为阴相应通语，此处存之。"
        "无常异名列中「苦、空、非我、非我所」为直显法义之语，「集法、灭法」为缘起生灭之语，"
        "皆非徒然之修辞，故于现代栏别为一类。"
        "「如梦价借」谓如梦中借得之物，梦醒即无；「执炬法」谓如逆风持炬，反自烧手；"
        "「轮沙水」「跳杖」皆言旋转不住之势。此诸僻譬今于现代栏加括注，文言栏存底本语面。"
    ),
}


# --- SA 187 一法 -------------------------------------------------------------
_187_DEFILEMENTS_LIT = (
    "如「贪」，如是恚、痴、瞋、恨、呰、执、嫉、悭、幻、谄、无惭、无愧、"
    "慢、慢慢、增慢、我慢、增上慢、邪慢、卑慢、憍慢、放逸、矜高、曲为相规、"
    "利诱、利恶、欲多、欲常、欲不敬、恶口、恶知识、不忍、贪嗜、不贪、恶贪，"
    "身见、边见、邪见、见取、戒取、欲爱、瞋恚、睡眠、掉悔、疑、惛悴、蹁蹮、"
    "赑屃、懒、乱想、不正忆、身浊、不直、不软、不异，欲觉、恚觉、害觉、亲觉、"
    "国土觉、轻易觉、爱他家觉、愁忧恼苦——于此等一一法，乃至为其映翳故，"
    "不堪任于色灭尽作证。"
)
_187_DEFILEMENTS_MOD = (
    "如同「贪」，同样还有约六十个烦恼之名可以替换；今按义类略分如下："
    "一、三毒及其眷属——瞋、痴、忿、恨、呰（讥毁）、执（固执己见）、嫉、悭、"
    "幻（诈伪）、谄、无惭、无愧；"
    "二、慢之诸相——慢、慢慢、增慢、我慢、增上慢、邪慢、卑慢、憍慢、放逸、矜高；"
    "三、贪利之相——曲为相规（曲意迎合以图人）、利诱、利恶、欲多、欲常、欲不敬、"
    "恶口、恶知识、不忍、贪嗜、（卑）不贪、恶贪；"
    "四、见与结之相——身见（我见）、边见、邪见、见取、戒取、欲爱、瞋恚、"
    "睡眠（昏沉睡意）、掉悔（掉举与追悔）、疑；"
    "五、心之滞钝——惛悴、蹁蹮（跛行不正）、赑屃（偏私固滞）、懒、乱想、不正忆（不正忆念）、"
    "身浊、不直、不软、不异（不出众）；"
    "六、恶寻思——欲觉、恚觉、害觉、亲觉（念亲属）、国土觉（念乡土）、轻易觉（轻慢他人）、"
    "爱他家觉（贪他家之供养）、愁忧恼苦。"
    "对这些法，乃至被它们遮蔽的缘故，都不堪能证得色的灭尽。"
)

SUTTAS["SA_187"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：以成就一法故，不复堪任知色无常，知受、想、行、识无常。"
        "何等一法成就？谓贪欲一法成就，则不堪能知色无常，知受、想、行、识无常。"
        "复以何等一法成就故堪能？谓成就无贪欲；成就无贪欲法者，则堪能知色无常，"
        "堪能知受、想、行、识无常。",
        CLOSE_LIT,
        "（省文）如「成就、不成就」，如是「知、不知」、「亲、不亲」、「明、不明」、"
        "「识、不识」、「察、不察」、「量、不量」、「覆、不覆」、「种、不种」、"
        "「掩、不掩」、「映翳、不翳」亦如是。",
        "如「知」，如是「识解」、「受」、「求」、「辩」、「触证」，亦复如是。",
        _187_DEFILEMENTS_LIT,
        "何等为一法？所谓恼苦。以恼苦映翳故，不堪任于色灭尽作证，"
        "不堪任于受、想、行、识灭尽作证。一法不映翳故，则堪任于色灭尽作证，"
        "堪任于受、想、行、识灭尽作证。",
        "何等一法？谓恼苦。此一法不映翳故，堪任于色灭尽作证，"
        "堪任于受、想、行、识灭尽作证。",
        CLOSE_LIT,
        "（底本于此题「杂阿含经卷第七」，断知相应竟。）",
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：由于具备了一法，就不再堪能了知色是无常，"
        "了知受、想、行、识是无常。是具备了哪一法呢？就是具备了贪欲这一法，"
        "便不堪能了知色是无常，了知受、想、行、识是无常。"
        "又由于成就哪一法才堪能呢？就是成就无贪欲；成就了无贪欲之法的人，"
        "便堪能了知色是无常，堪能了知受、想、行、识是无常。",
        CLOSE_MOD,
        "（以下是原典的省文指示）如同「具备、不具备」，同样「了知、不了知」、"
        "「亲近、不亲近」、「明了、不明了」、「认识、不认识」、「省察、不省察」、"
        "「量度、不量度」、「被覆、不被覆」、「滋长、不滋长」、「被掩、不被掩」、"
        "「被遮蔽、不被遮蔽」，也照此说。",
        "如同「了知」，同样「识解」、「领受」、「寻求」、「辨别」、「触证」，也是一样。",
        _187_DEFILEMENTS_MOD,
        "是哪一法呢？就是恼苦。由于被恼苦遮蔽的缘故，不堪能证得色的灭尽，"
        "不堪能证得受、想、行、识的灭尽。反之，不被这一法遮蔽的缘故，"
        "便堪能证得色的灭尽，堪能证得受、想、行、识的灭尽。",
        "是哪一法呢？就是恼苦。不被这一法遮蔽的缘故，便堪能证得色的灭尽，"
        "堪能证得受、想、行、识的灭尽。",
        CLOSE_MOD,
        "（底本在此处题「杂阿含经卷第七」，断知相应到此结束。）",
    ],
    "notes": (
        f"{PROV}"
        "「以成就一法故，不复堪任知色无常」：一法即贪欲（abhijjhā／rāga），"
        "谓贪欲在则不能如实知无常，无贪则能知；与「贪欲盖心，不见如实」之早期教理一贯。"
        "「映翳」谓遮蔽（Anālayo：being screened by），非「映照」；"
        "末段之一法作「恼苦」，与首段之「贪欲」不同，乃省文列举之末项自成一段，非前后矛盾。"
        "「独证」当作「触证」（Anālayo：to touch, to realize），今据改。"
        "「不忍贪、嗜不贪、恶贪」句读不明，Anālayo 读为不忍、贪嗜、（卑）不贪、恶贪四项，今从之而志其疑。"
        "「掉悔」即 uddhacca-kukkucca（掉举恶作），「睡眠」即 thīnamiddha（昏沉睡眠），"
        "「戒取」即 sīlabbata-parāmāsa 一类之戒禁取，皆五盖／结之名。"
        "底本经末题「杂阿含经卷第七」，而卷题作卷第八，此为大正藏卷次与相应分卷之异，今志之不改。"
    ),
}


# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

# 本相应 SC 平行表全空（见 PROV），依项目规约「无可靠平行时 confidence 降为 medium/low」，
# 故全批以 medium 为上限；不因道品定型语可考而升作 high。
DEFAULT_CONFIDENCE = "medium"

# 底本术语已讹、须依经内经数回填法数者：正文非底本语面之直译，标 gold_reconstructed / low。
RECONSTRUCTED: dict[str, str] = {
    "SA_184": "四道之名依「三十二经」之数回填为四通行（底本作「苦习尽道」等，已讹）",
    "SA_185": "法句之数依「二十四经」之数定为三法句（与巴利 AN4.29 之四法句不合）",
}

SIM_MAX = 0.55  # 繁转简嫌疑阈值（文言栏与求那跋陀罗底本之三元组相似度上限）

# 本脚本自身产出之状态；不可记为 pre-gold 状态，否则重跑会覆盖启发式草稿之来历。
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
    assert set(GOLD) == {f"SA_{i}" for i in range(172, 188)}, "GOLD must cover SA_172–SA_187 exactly"

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

            if rid in RECONSTRUCTED:
                item["review_status"] = "gold_reconstructed"
                item["confidence"] = "low"
                item["reconstruction_basis"] = RECONSTRUCTED[rid]
            else:
                item["review_status"] = "gold"
                item["confidence"] = DEFAULT_CONFIDENCE

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
    (ROOT / "data" / "translated" / "validation_report_sa172-187.json").write_text(
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_172–187 only)")
    print(f"validation: ok={len(oks)} warn={len(warns)} fail={len(fails)}")
    print(f"forbidden_hits={len(forbidden)}")
    print(
        f"sim>={SIM_MAX} (繁转简嫌疑): {len(too_literal)}  "
        f"max_sim={max_r['sim']} ({max_r['id']})"
    )
    print(f"paragraph_parallel_violations={len(para_bad)}")
    print(f"gold={len(report) - len(recon)} gold_reconstructed={len(recon)}")
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
