#!/usr/bin/env python3
"""Retranslate SA 1291–1310（卷第五十 杂相应续：火不烧～照明）→ merge.

本批二十经：
1291–1299 天子问答（火不烧／粮／甚能／所为／车乘／锯陀女／算数／何重／十善）
1300 因陀罗（SN10.1 胚胎；汉作释提桓因）
1301–1305 长胜／尸毘／月自在／毗纽／般闍罗（SN2.21、2.11、2.12、2.7 等）
1306–1308 须深摩／边际／外道诸见（SN2.29、2.26、2.30）
1309–1310 摩佉／照明（SN2.3、SN1.26）

信：有 SN 平行者据巴利／Sujato 厘义；无平行者降 medium。
达雅：白话与罗什风逐段对照；Devatā 公式压缩；sim 门限见 assess_gold。
禁「厌故不乐」→「厌故离贪」；本批「厌离」作 nibbidā／离贪义，不取后期术语。
边界：只合并 SA_1291–1310；断言 SA_1290 及 SA_1311+ 不变。
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

OPEN_VEP_LIT = "如是我闻：一时，佛住王舍城毘富罗山侧。"
OPEN_VEP_MOD = "我是这样听说的：有一次，佛住在王舍城毘富罗山侧。"

EPI_LIT = "久见婆罗门，逮得般涅槃，一切怖已过，永超世恩爱。"
EPI_MOD = "久见婆罗门，逮得般涅槃，一切怖惧已过，永超世间恩爱。"

DEVA_NIGHT_LIT = (
    "后夜分，有天子容色绝妙，来诣佛所，稽首礼足，退坐一面；"
    "身诸光明遍照祇树给孤独园。"
)
DEVA_NIGHT_MOD = (
    "后夜分，有一位天子容色绝妙，来到佛前，顶礼佛足，退坐一面；"
    "身上的光明遍照祇树给孤独园。"
)

DEVA_CLOSE_LIT = f"天子复说偈：「{EPI_LIT}」闻已欢喜，礼足即没。"
DEVA_CLOSE_MOD = f"天子又说偈：「{EPI_MOD}」听完欢喜随喜，顶礼佛足，随即隐没不见。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)


def _deva(
    q_lit: str,
    q_mod: str,
    a_lit: str,
    a_mod: str,
) -> tuple[list[str], list[str]]:
    lit = [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        f"天子说偈问：「{q_lit}」",
        f"世尊说偈答：「{a_lit}」",
        DEVA_CLOSE_LIT,
    ]
    mod = [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        f"天子说偈问：「{q_mod}」",
        f"世尊说偈答：「{a_mod}」",
        DEVA_CLOSE_MOD,
    ]
    return lit, mod


def _named_short(
    name_lit: str,
    name_mod: str,
    say_lit: str,
    say_mod: str,
    ans_lit: str,
    ans_mod: str,
    *,
    ask: bool = False,
) -> tuple[list[str], list[str]]:
    night_lit = (
        f"后夜分，有{name_lit}天子容色绝妙，来诣佛所，稽首礼足，退坐一面；"
        "身诸光明遍照祇树给孤独园。"
    )
    night_mod = (
        f"后夜分，有{name_mod}天子容色绝妙，来到佛前，顶礼佛足，退坐一面；"
        "身上的光明遍照祇树给孤独园。"
    )
    if ask:
        q_lit = f"{name_lit}天子说偈问：「{say_lit}」"
        q_mod = f"{name_mod}天子说偈问：「{say_mod}」"
    else:
        q_lit = f"{name_lit}天子说偈：「{say_lit}」"
        q_mod = f"{name_mod}天子说偈：「{say_mod}」"
    lit = [
        OPEN_JET_LIT,
        night_lit,
        q_lit,
        f"世尊说偈答：「{ans_lit}」",
        f"{name_lit}天子闻已欢喜，礼足即没。",
    ]
    mod = [
        OPEN_JET_MOD,
        night_mod,
        q_mod,
        f"世尊说偈答：「{ans_mod}」",
        f"{name_mod}天子听完欢喜随喜，顶礼佛足，随即隐没不见。",
    ]
    return lit, mod


# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 1291 火不烧（近 SN1.52；汉火／风／水／盗问，答以福）----------------
_lit1291, _mod1291 = _deva(
    "何物火不烧？何风不能吹？水灾坏大地，何物不流散？"
    "恶王及盗贼强劫人财物，何男子女人不为其所夺？云何珍宝藏，终竟不亡失？",
    "什么东西火烧不了？什么风吹不动？洪水坏大地，什么不会冲散？"
    "恶王和盗贼强夺人的财物，什么样的男女不被他们夺走？怎样的珍宝藏，终究不会丧失？",
    "福德火不烧，福德风不吹；水灾坏大地，福德水不散。"
    "恶王及盗贼虽夺人财宝，若男子女人有福则不被劫；乐报之宝藏，终竟不亡失。",
    "福德，火烧不了，风也吹不动；洪水坏大地，福德不会被冲散。"
    "恶王和盗贼虽然夺走财物，男女若有福德就不会被劫走；能感乐报的宝藏，终究不会丧失。",
)
SUTTAS["SA_1291"] = {
    "lit": _lit1291,
    "mod": _mod1291,
    "notes": (
        f"{PROV}confidence=high：SC 列 resembling SN1.52（Ajarasā）；"
        "巴利以戒／信／慧／福为「不老／安住／宝／盗不能取」，汉以火风水盗问而专答「福」。"
        "框从汉，核心「福不可夺」据 SN puññaṃ corehyahāriyaṃ；不改写成全四问 SN 文。"
    ),
}

# --- SA 1292 粮（SN1.77／1.79 合影）-----------------------------------------
_lit1292, _mod1292 = _deva(
    "谁当持资粮？何物贼不劫？何人劫而遮？何人劫不遮？何人常来诣，智慧者喜乐？",
    "谁该带上路的资粮？什么东西贼抢不走？抢了谁会被拦阻？抢了谁反受人爱？"
    "谁常常来访，智慧的人会欢喜？",
    "信者持资粮，福德劫不夺；贼劫夺则遮，沙门夺则喜；沙门常来诣，智慧者欣乐。",
    "有信心的人带着资粮，福德抢不走；盗贼抢了会被拦，沙门受供养则受人爱；"
    "沙门常来访，智慧的人会欢喜。",
)
SUTTAS["SA_1292"] = {
    "lit": _lit1292,
    "mod": _mod1292,
    "notes": (
        f"{PROV}confidence=high：primary 近 SN1.77（Issariya）盗贼／沙门「劫」对句，"
        "及 SN1.79（Pātheyya）以信为资粮。汉合写；「沙门夺欢喜」据 SN haranto samaṇo piyo"
        "作沙门受供／乞食而人喜，非盗贼义。"
    ),
}

# --- SA 1293 甚能／最难（四难；无专经）--------------------------------------
_lit1293, _mod1293 = _deva(
    "一切相映障，知一切世间，乐安慰一切——唯愿世尊说：云何是世间最为难得者？",
    "能映障一切相，了知一切世间，乐于安慰一切——愿世尊说：世间什么最为难得？",
    "为主而行忍，无财而欲施，遭难而行法，富贵修远离——如是四法，是则为最难。",
    "身居上位还能忍耐，自己没有财物却想布施，遭遇危难仍按法而行，身处富贵却修远离——"
    "这四种，才是世间最难得的。",
)
SUTTAS["SA_1293"] = {
    "lit": _lit1293,
    "mod": _mod1293,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；四难（主而忍、贫而施、难而法、富而离）"
        "与早期「难得」定型相应。题名汉录或与下经互易，文以「最难得」为准。"
    ),
}

# --- SA 1294 所为／自在乐（无专经）------------------------------------------
_lit1294, _mod1294 = _deva(
    "大力自在乐，所求无不得——何复胜于彼，一切所欲备？",
    "有大力、得自在、所求皆得——还有什么比这更胜，能备足一切所欲？",
    "大力自在乐，彼则无所求；若有求欲者，是苦非为乐；于求已过去，是则乐于彼。",
    "真有大力自在之乐的人，其实已经无所求；还有欲求的，那是苦而不是乐；"
    "欲求已经过去的，才是真正的乐。",
)
SUTTAS["SA_1294"] = {
    "lit": _lit1294,
    "mod": _mod1294,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；对破「所欲备足即乐」，"
        "结归无求乃乐，义近早期离欲／少欲。不取后期「真空妙有」等。"
    ),
}

# --- SA 1295 车乘（无专经）-------------------------------------------------
_lit1295, _mod1295 = _deva(
    "车从何处起？谁能转于车？车转至何所？何故坏磨灭？",
    "车从哪里生起？谁能转动这车？车转到哪里？为什么会坏灭？",
    "车从诸业起，心识能转车；随因而转至，因坏车则亡。",
    "车从诸业生起，心识能转动这车；随因而转到某处，因坏了车也就灭了。",
)
SUTTAS["SA_1295"] = {
    "lit": _lit1295,
    "mod": _mod1295,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；以业／心识／因缘说「车」，"
        "义近早期缘起，不作唯识／如来藏读。"
    ),
}

# --- SA 1296 锯陀女（无专经）-----------------------------------------------
SUTTAS["SA_1296"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "天子白佛：「世尊！拘屡陀王女修波罗提沙今日生子。」"
        "佛言：「此则不善，非是善。」",
        "天子说偈：「人生子为乐，世间有子欢；父母年老衰，子则能奉养。"
        "瞿昙何故说，生子为不善？」",
        "世尊说偈答：「当知恒无常，纯空诸阴非子；生子常得苦，愚者说言乐。"
        "是故我说言，生子非为善；非善为善像，念像不可念；实苦貌似乐，放逸所践蹈。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "天子对佛说：「世尊！拘屡陀王的女儿修波罗提沙今天生了儿子。」"
        "佛说：「这并非善事，不是善。」",
        "天子说偈：「人生子是乐，世间有子就欢喜；父母年老体衰，儿子能奉养。"
        "瞿昙为什么说生子不善？」",
        "世尊说偈答：「应当知道一切恒是无常，纯是空的诸阴，并没有一个『子』实体；"
        "生子常得苦，愚人才说是乐。所以我说生子并非善；把不善当成善的样子，"
        "把不可念的当成可念；其实是苦，只是外表像乐，正是放逸所踩踏的。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；以无常、空、诸阴破「生子为乐」。"
        "汉「纯空阴非子」保留早期阴／空用语；不引入佛性／真心。"
    ),
}

# --- SA 1297 算数（无专经）-------------------------------------------------
_lit1297, _mod1297 = _deva(
    "云何数所数？云何数不隐？云何数中数？云何说言说？",
    "什么是被数的？什么数不会隐没？什么是数中之数？怎样才叫「说」？",
    "佛法难测量；二流不显现。若彼名及色，灭尽悉无余——"
    "是名数所数，彼数不隐藏；是彼数中数，是则说名数。",
    "佛法难以测量；两种流转也不会再显现。若名与色灭尽无余——"
    "那才叫被数到的，那数也不会隐藏；那是数中之数，也才叫真正的「说」。",
)
SUTTAS["SA_1297"] = {
    "lit": _lit1297,
    "mod": _mod1297,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；以名色灭尽释「数」，"
        "义近早期名色／灭尽，文句拙处略顺读，不强作阿毗达磨计量。"
    ),
}

# --- SA 1298 何重（无专经）-------------------------------------------------
_lit1298, _mod1298 = _deva(
    "何物重于地？何物高于空？何物疾于风？何物多于草？",
    "什么比地还重？什么比虚空还高？什么比风还快？什么比草还多？",
    "戒德重于地，慢高于虚空，忆念疾于风，思想多于草。",
    "戒德比地还重，憍慢比虚空还高，忆念比风还快，思想比草还多。",
)
SUTTAS["SA_1298"] = {
    "lit": _lit1298,
    "mod": _mod1298,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；戒／慢／念／想四喻，"
        "与天子偈对破定型相应。"
    ),
}

# --- SA 1299 十善（无专经；十善业迹）---------------------------------------
SUTTAS["SA_1299"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "天子说偈问：「何戒何威仪？何得何为业？慧者云何住？云何往生天？」",
        "世尊说偈答：「远离杀生，持戒自防，害心不加于生，是则生天路。"
        "远离不与取，于施与心欣乐，断除盗心，是则生天路。"
        "不行于他所受，远离邪淫，自知止足，是则生天路。"
        "不为财利戏笑而妄语，是则生天路。"
        "断除两舌，不离他亲友，常念和合彼此，是则生天路。"
        "远离不爱语，软语不伤人，常说淳美言，是则生天路。"
        "不为无义不饶益之绮语，常顺法言，是则生天路。"
        "于聚落空地见利不起『我有』贪想，是则生天路。"
        "慈心无害想，不害众生，心无怨结，是则生天路。"
        "于苦业及果报生净信，受持正见，是则生天路。"
        "如是十种净业迹，等受坚固持，是则生天路。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "天子说偈问：「什么戒、什么威仪？有什么成就、做什么业？"
        "有智慧的人怎样安住？怎样才能往生天上？」",
        "世尊说偈答：「远离杀生，持戒护持自己，害心不加于众生，这就是生天之路。"
        "远离不与取，对布施心生欢喜，断除盗心，这就是生天之路。"
        "不侵犯别人所守护的，远离邪淫，自己知道满足，这就是生天之路。"
        "不为财利或戏笑而说妄语，这就是生天之路。"
        "断除两舌，不拆散别人的亲友，常想着让彼此和合，这就是生天之路。"
        "远离难听的话，柔和的话不伤人，常说淳美的言语，这就是生天之路。"
        "不说无义、无益的绮语，常随顺法而说，这就是生天之路。"
        "在聚落或空地见到利益，不起『这是我的』贪想，这就是生天之路。"
        "怀着慈心、没有伤害的想法，不伤害众生，心里没有怨结，这就是生天之路。"
        "对苦的业及其果报生起清净的信心，受持正见，这就是生天之路。"
        "像这样十种清净的业迹，平等受持、牢固守住，这就是生天之路。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；十善业迹（身三、口四、意三）"
        "与早期业道定型一致。删汉「自为己及他」等冗复，义从十善。"
    ),
}

# --- SA 1300 因陀罗（SN10.1；汉作释提桓因）--------------------------------
SUTTAS["SA_1300"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，释提桓因来诣佛所，稽首礼足，退坐一面；身诸光明遍照祇树给孤独园。",
        "释提桓因说偈问：「何法命不知？何法命不觉？何法锁于命？何法为命缚？」",
        "世尊说偈答：「色者命不知，诸行命不觉；身锁于其命，受缚于命者。」",
        "释提桓因复问：「色者非为命，诸佛之所说。云何而得熟？云何段肉住？"
        "云何知命身？」",
        "世尊说偈答：「迦罗逻为初，迦罗逻生胞，胞生肉段，肉段生坚厚；"
        "坚厚生肢节及诸毛发等，色等诸情根渐次成形体；"
        "因母饮食等，长养彼胎身。」",
        "释提桓因闻已欢喜，礼足即没。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，释提桓因来到佛前，顶礼佛足，退坐一面；身上的光明遍照祇树给孤独园。",
        "释提桓因说偈问：「什么是命所不知的？什么是命所不觉的？"
        "什么锁住命？什么把命绑住？」",
        "世尊说偈答：「色，是命所不知的；诸行，是命所不觉的；"
        "身体锁住那命；受，把命绑住。」",
        "释提桓因又问：「诸佛说色并不是命。那身体怎样成熟？怎样成为肉团而住？"
        "怎样知道这命身？」",
        "世尊说偈答：「最初是迦罗逻，由迦罗逻生胞，由胞生肉段，由肉段生坚厚；"
        "由坚厚生出肢节和毛发等，色等诸根渐渐形成身体；"
        "靠着母亲的饮食等，长养那在胎中的身。」",
        "释提桓因听完欢喜随喜，顶礼佛足，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN10.1（Indaka）；巴利在王舍城因陀罗山、夜叉因陀罗，"
        "汉作祇园／释提桓因——框从汉，胚胎次第据巴利 kalala→abbuda→pesi→ghana→pasākhā。"
        "汉前半「命不知／不觉」无 SN 对应，保守保留；义从早期非命／色受行。"
    ),
}

# --- SA 1301 说善称／长胜（无专经）-----------------------------------------
_lit1301, _mod1301 = _named_short(
    "长胜",
    "长胜",
    "善学微妙说，习近诸沙门，独一无等侣，正思惟静默。",
    "好好学习微妙的说法，亲近诸位沙门，独自一人没有同伴，正思惟而静默。",
    "善学微妙说，习近诸沙门，独一无等侣，寂默静诸根。",
    "好好学习微妙的说法，亲近诸位沙门，独自一人没有同伴，寂静调伏诸根。",
)
SUTTAS["SA_1301"] = {
    "lit": _lit1301,
    "mod": _mod1301,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；佛以「寂默静诸根」印可／校正"
        "天子「正思惟静默」。"
    ),
}

# --- SA 1302 尸毘（SN2.21）-------------------------------------------------
_lit1302, _mod1302 = _named_short(
    "尸毘",
    "尸毘",
    "何人应同止？何等人共事？应知何等法，是转胜非恶？",
    "应当和什么人同住？应当和什么人共事？应当了知什么法，才会转向殊胜而不是恶劣？",
    "与正士同止，与正士共事；应知正士法，是转胜非恶。",
    "和正直的人同住，和正直的人共事；应当了知正直人的法，才会转向殊胜而不是恶劣。",
    ask=True,
)
SUTTAS["SA_1302"] = {
    "lit": _lit1302,
    "mod": _mod1302,
    "notes": (
        f"{PROV}confidence=high：primary SN2.21（Siva）；汉略为一问一答，"
        "巴利天子广说亲近善人诸益、佛答「解脱一切苦」。框从汉略本，"
        "「正士／正士法」据 SN sabbhi／sataṃ saddhamma。"
    ),
}

# --- SA 1303 月自在（SN2.11）-----------------------------------------------
_lit1303, _mod1303 = _named_short(
    "月自在",
    "月自在",
    "彼当至究竟，如鹿依无蚊之草泽；若得正系念，一心善正受。",
    "他们将到达安稳处，如同鹿依止没有蚊子的草泽；若得正念系念，一心善入正受。",
    "彼当到彼岸，如鱼决其网；禅定具足住，不放逸、舍战诤，心常致喜乐。",
    "他们将到彼岸，如同鱼挣破了网；具足安住禅定，不放逸、舍离战诤，心里常得喜乐。",
)
SUTTAS["SA_1303"] = {
    "lit": _lit1303,
    "mod": _mod1303,
    "notes": (
        f"{PROV}confidence=high：primary SN2.11（Candimasa）。"
        "据 SN：天子以无蚊泽中鹿喻禅定正念；佛以破网之鱼喻到彼岸，"
        "并强调不放逸、舍战诤（appamattā raṇañjahā）。汉「如蚊依从草」据 SN 校正为鹿依无蚊草泽。"
    ),
}

# --- SA 1304 毗纽（SN2.12）-------------------------------------------------
_lit1304, _mod1304 = _named_short(
    "毘瘦纽",
    "毘瘦纽",
    "供养于如来，欢喜常增长；欣乐正法律，不放逸随学。",
    "供养如来，欢喜常常增长；欣乐正法律，不放逸地随学。",
    "若如是随学我所宣说之教，防护不放逸；以不放逸故，不随死魔自在。",
    "若这样随学我所宣说的教法，防护而不放逸；因为不放逸，就不会落入死魔的掌控。",
)
SUTTAS["SA_1304"] = {
    "lit": _lit1304,
    "mod": _mod1304,
    "notes": (
        f"{PROV}confidence=high：primary SN2.12（Veṇḍu／Vishnu）。"
        "据 SN：不放逸随学则不随死魔（maccu）自在；汉「不随魔自在」据巴利作死魔。"
    ),
}

# --- SA 1305 般闍罗（SN2.7）-----------------------------------------------
_lit1305, _mod1305 = _named_short(
    "般闍罗健",
    "般闍罗健",
    "憒乱之处所，黠慧者能觉；禅思觉所觉，牟尼思惟力。",
    "在逼窄憒乱之处，广慧者能发现出路；以禅而觉所应觉，那是牟尼的思惟力。",
    "了知憒乱法，亦得知涅槃；若得正系念，一心善正受。",
    "即使在逼窄憒乱中，也能了知趣向涅槃的法；若得正念，便能一心善入正定。",
)
SUTTAS["SA_1305"] = {
    "lit": _lit1305,
    "mod": _mod1305,
    "notes": (
        f"{PROV}confidence=high：primary SN2.7（Pañcālacaṇḍa）。"
        "据 SN：sambādhe okāsa——逼窄中得空隙；佛答即使逼窄中亦得知趣涅槃之法，"
        "正念者正定。汉「正觉得涅槃」作「得知涅槃／趣灭之法」，避后期「正觉」歧读。"
    ),
}

# --- SA 1306 须深摩（SN2.29）-----------------------------------------------
SUTTAS["SA_1306"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，须深天子与五百眷属容色绝妙，来诣佛所，稽首礼足，退坐一面；"
        "身诸光明遍照祇树给孤独园。",
        "世尊问尊者阿难：「汝于尊者舍利弗善说法，心喜乐不？」"
        "阿难白佛：「如是，世尊！若不愚、不癡、有智慧，闻尊者舍利弗善说，心无不欣乐。"
        "所以者何？舍利弗持戒多闻，少欲知足，精勤远离，正念坚住，智慧正受；"
        "捷疾慧、利慧、出离慧、决定慧、大慧、广慧、深慧、无等慧，智宝成就；"
        "善能教化，示教照喜，常为四众说法不倦。」",
        "佛言：「如是，如汝所说。谁若不愚、不癡、有智慧，闻舍利弗善说而不欢喜？」"
        "并如是称叹舍利弗。须深天子眷属内心欢喜，身光倍增明净。",
        "须深天子说偈：「舍利弗多闻，明智平等慧，持戒善调伏，得不起涅槃；"
        "持此最后身，降伏于魔军。」",
        "须深天子及五百眷属闻已欢喜，礼足即没。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，须深天子与五百眷属容色绝妙，来到佛前，顶礼佛足，退坐一面；"
        "身上的光明遍照祇树给孤独园。",
        "世尊问尊者阿难：「你对于尊者舍利弗善于说法，心里欢喜吗？」"
        "阿难回答：「是的，世尊！若不愚、不癡、有智慧，听尊者舍利弗善说，没有不欢喜的。"
        "为什么呢？舍利弗持戒、多闻，少欲知足，精勤远离，正念坚固，智慧正定；"
        "有捷疾的智慧、锐利的智慧、出离的智慧、决定的智慧、大智慧、广智慧、深智慧、无等的智慧，成就智宝；"
        "又善于教化，开示、教导、照亮、使人生喜，常为四众说法而不厌倦。」",
        "佛说：「正是这样，正如你所说。有谁若不愚、不癡、有智慧，听了舍利弗善说却不欢喜呢？」"
        "并这样称叹舍利弗。须深天子的眷属内心欢喜，身上的光明更加明净。",
        "须深天子说偈：「舍利弗多闻，明智而慧平等，持戒善于调伏，证得无余涅槃；"
        "持此最后之身，降伏魔军。」",
        "须深天子及五百眷属听完欢喜随喜，顶礼佛足，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.29（Susīma）。"
        "巴利先阿难赞舍利弗，佛印可，须深及天众来随喜；汉则天众已在而佛问阿难——"
        "框从汉，赞辞据 SN 压缩罗什风（删叠床架屋之智名而不失多慧义）。"
        "「不起涅槃」＝无余依涅槃，不作如来藏读。"
    ),
}

# --- SA 1307 边际／赤马（SN2.26）-------------------------------------------
SUTTAS["SA_1307"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，赤马天子容色绝妙，来诣佛所，稽首礼足，退坐一面；"
        "身诸光明遍照祇树给孤独园。",
        "赤马白佛：「世尊！颇有能行过世界边，至不生、不老、不死处不？」"
        "佛言：「无有能由游行过世界边，至不生、不老、不死处者。」",
        "赤马白佛：「奇哉！世尊善说斯义。所以者何？我自忆宿命，名曰赤马，作外道仙人，"
        "得神通，离诸爱欲。我念：『我神足捷疾，如健士以利箭横射过多罗树影之顷，"
        "能登一须弥至一须弥，足蹑东海超至西海。宁可求世界边。』"
        "即便发行，唯除食息便利、减节睡眠，常行百岁，于彼命终，"
        "竟不能过世界边，至不生、不老、不死处。」",
        "佛告赤马：「我今但以一寻之身，说于世界、世界集、世界灭、世界灭道迹。"
        "何等为世间？谓五受阴：色、受、想、行、识，是名世间。"
        "何等为世间集？谓当来有爱，喜贪俱，于彼彼染着，是名世间集。"
        "云何世间灭？若彼当来有爱，喜贪俱、彼彼染着，无余断、舍、离贪、尽、灭、息、没，"
        "是名世间灭。"
        "何等为世间灭道迹？谓八圣道——正见、正志、正语、正业、正命、正方便、正念、正定。"
        "赤马！了知世间则断世间，了知集则断集，了知灭则证灭，了知道迹则修道迹。"
        "若比丘于世间苦若知若断，于集若知若断，于灭若知若证，于道若知若修——"
        "是名得世界边，度世间爱。」",
        "世尊复说偈：「未曾远游行而得世界边；不得世界边，终不尽苦边。"
        "是故牟尼能知世界边，善解世界边，诸梵行已立；"
        "于彼世界边平等觉知者，是名贤圣行，度世间彼岸。」",
        "赤马天子闻已欢喜，礼足即没。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，赤马天子容色绝妙，来到佛前，顶礼佛足，退坐一面；"
        "身上的光明遍照祇树给孤独园。",
        "赤马对佛说：「世尊！有没有人能靠行走越过世界的边际，到达不生、不老、不死的地方？」"
        "佛说：「没有人能靠游行越过世界的边际，到达不生、不老、不死的地方。」",
        "赤马说：「奇哉！世尊说得太好了。为什么呢？我自己记得宿命，那时名叫赤马，"
        "是外道仙人，有神通，已离诸爱欲。我心想：『我的神足这样快，就像健壮的人用利箭"
        "横着射过多罗树影那么短的时间里，就能从一座须弥跨到另一座，脚踩东海就超到西海。"
        "今天不如去求世界的边际。』于是就出发了，只除了吃饭、休息、便利，并减少睡眠，"
        "一直走了一百年，在那一生结束时，终究不能越过世界边际，到达不生、不老、不死处。」",
        "佛告诉赤马：「我现在只就这一寻高的身体，来说世界、世界的集、世界的灭、世界灭的道迹。"
        "什么是世间？就是五受阴：色、受、想、行、识，这叫做世间。"
        "什么是世间集？就是能招来有的爱，与喜贪一起，在各处染着，这叫做世间集。"
        "什么是世间灭？若那能招来有的爱——与喜贪一起、在各处的染着——无余地断除、舍离、离贪、灭尽、止息、沉没，"
        "这叫做世间灭。"
        "什么是世间灭的道迹？就是八圣道——正见、正志、正语、正业、正命、正精进、正念、正定。"
        "赤马！了知世间就断世间，了知集就断集，了知灭就证灭，了知道迹就修道迹。"
        "若比丘对世间苦能知、能断，对集能知、能断，对灭能知、能证，对道能知、能修——"
        "这才叫做得到世界的边际，度脱世间的爱。」",
        "世尊又说偈：「从没有靠远行就得到世界边际的；得不到世界边际，终究不能尽苦边。"
        "所以牟尼能知世界边际，善解世界边际，梵行已经确立；"
        "对那世界边际能平等觉知的人，才叫做贤圣之行，度到世间的彼岸。」",
        "赤马天子听完欢喜随喜，顶礼佛足，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.26（Rohitassa）。"
        "据 SN：不可以游行至世界边；于一寻身说世界四谛——五阴为世间，爱为集，"
        "爱无余灭为灭，八支为道。汉「离、尽、无欲」据 virāga 作「离贪」（厌故离贪）；"
        "不用「厌故不乐」。"
    ),
}

# --- SA 1308 外道诸见（SN2.30）---------------------------------------------
SUTTAS["SA_1308"] = {
    "lit": [
        OPEN_VEP_LIT,
        "有六天子，本为外道出家——一名阿毘浮、二名增上阿毘浮、三名能求、"
        "四名毘蓝婆、五名阿俱吒、六名迦蓝——来诣佛所。",
        "阿毘浮说偈：「比丘专至心，常修习生厌离贪，初夜后夜善自摄；"
        "见闻如来所说，不堕于地狱。」",
        "增上阿毘浮说偈：「厌离于黑闇，心常自摄护，永离世间言语诤论；"
        "从如来大师禀受沙门法，善摄护世间，不令造众恶。」",
        "能求说偈：「于斩截椎打杀害，及供养布施，迦叶皆不见为恶，亦不见为福。」",
        "毘蓝婆说偈：「我谓彼尼乾若提子，出家学道，长夜修难行；"
        "于大师徒众远离妄语——如是人去阿罗汉不远。」",
        "世尊说偈答：「死瘦野狐虽常共师子游，终日羸劣，不能为师子。"
        "尼乾大师之众虚妄自赞，恶心妄语，去阿罗汉甚远。」",
        "时天魔波旬加力于阿俱吒天子，令说偈：「精勤弃闇冥，常守护远离；"
        "深着微妙色，贪乐于梵世——我教化斯等，令得生梵天。」",
        "世尊知是魔力，非彼天子自心，说偈：「若诸所有色，于此及与彼，或复虚空中，"
        "各别光照耀——当知彼一切不离魔与魔缚，犹如垂钩饵，钩钓于游鱼。」",
        "诸天子心念：「何故瞿昙言是魔说？」世尊告言：「今阿俱吒所诵，非自心说，是魔波旬加力。」"
        "并复说前偈以明魔缚。",
        "诸天子叹言：「奇哉！沙门瞿昙能见天魔，而我等不见。」各说偈赞：「断除一切有身爱贪想，"
        "令善护者除一切妄语；欲断欲爱、三有爱、见贪，应供养大师。"
        "王舍城中毘富罗山第一，雪山诸山最，金翅鸟中尊；"
        "八方上下一切众生界，于诸天人中，等正觉最上。」",
        "诸天子说偈赞已，闻佛所说，欢喜礼足，即没不现。",
    ],
    "mod": [
        OPEN_VEP_MOD,
        "有六位天子，从前是外道出家人——名叫阿毘浮、增上阿毘浮、能求、"
        "毘蓝婆、阿俱吒、迦蓝——来到佛前。",
        "阿毘浮说偈：「比丘专心一意，常修习生厌、离贪，初夜后夜善于收摄自己；"
        "见闻如来所说，就不会堕落地狱。」",
        "增上阿毘浮说偈：「厌离黑闇，心里常常自己守护，永离世间的言语诤论；"
        "从如来大师领受沙门法，善于守护世间，不让人造种种恶。」",
        "能求说偈：「对于斩截、捶打、杀害，以及供养布施，迦叶都看不见有恶，也看不见有福。」",
        "毘蓝婆说偈：「我认为那位尼乾若提子，出家学道，长夜修难行；"
        "在大师与徒众中远离妄语——这样的人离阿罗汉不远。」",
        "世尊说偈回答：「瘦死的野狐虽然常和狮子一起游走，整天还是羸弱，成不了狮子。"
        "尼乾大师的徒众虚妄地自我称赞，怀着恶心说妄语，离阿罗汉非常远。」",
        "那时天魔波旬用力加在阿俱吒天子身上，让他说偈：「精勤抛弃闇冥，常常守护远离；"
        "深深贪着微妙的色，贪乐梵世——我教化这些人，让他们生到梵天。」",
        "世尊知道这是魔力，不是那位天子自己的心，便说偈：「凡是所有的色，在这里或那里，"
        "或在虚空中，各自放光显耀——要知道那一切都不离魔与魔的系缚，"
        "就像垂下带饵的钩，去钓游动的鱼。」",
        "天子们心想：「为什么瞿昙说这是魔说的？」世尊告诉他们：「现在阿俱吒所念的，"
        "不是他自己心里说的，是魔波旬加力。」并又说前面的偈，说明魔的系缚。",
        "天子们赞叹：「奇哉！沙门瞿昙能看见天魔，我们却看不见。」各自说偈称赞："
        "「断除一切有身的爱贪之想，使善加守护的人除去一切妄语；"
        "若要断欲爱、三有爱、见贪，应当供养大师。"
        "王舍城中毘富罗山第一，雪山在众山中最高，金翅鸟在鸟中最尊；"
        "八方上下一切众生界里，在诸天与人中，等正觉最为最上。」",
        "天子们说偈赞叹之后，听佛所说，欢喜顶礼佛足，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.30（nānātitthiyasāvakā）。"
        "汉六天子名与巴利 Asama 等不尽同，且赞颂对象分配有异；"
        "义据 SN：破尼乾近罗汉之赞，揭魔劝生梵世，明诸色不离魔缚。"
        "「常修行厌离」据 nibbidā／virāga 作「生厌离贪」（厌故离贪）；不用「厌故不乐」。"
        "框从汉，不作全经按 SN 重排（v1 不自动重排）。"
    ),
}

# --- SA 1309 摩佉（SN2.3）--------------------------------------------------
_lit1309, _mod1309 = _named_short(
    "摩伽",
    "摩伽",
    "杀何得安眠？杀何得善乐？为杀何等人，瞿昙所赞叹？",
    "杀了什么才能安稳睡眠？杀了什么才能得到善乐？杀什么样的人，是瞿昙所赞叹的？",
    "若杀于瞋恚，而得安隐眠；杀于瞋恚者，令人得欢喜。"
    "瞋恚为毒本，杀者我所叹；杀彼瞋恚已，长夜无忧患。",
    "若杀掉瞋恚，就能安稳睡眠；杀掉瞋恚的人，能使人得欢喜。"
    "瞋恚是毒的根源，杀掉它是我所赞叹的；杀掉那瞋恚之后，长夜没有忧患。",
    ask=True,
)
SUTTAS["SA_1309"] = {
    "lit": _lit1309,
    "mod": _mod1309,
    "notes": (
        f"{PROV}confidence=high：primary SN2.3（Māgha）。"
        "据 SN：杀瞋则安眠、无忧；瞋有毒根。汉略「甘尖」喻，义从杀瞋。"
    ),
}

# --- SA 1310 照明（SN1.26）-------------------------------------------------
_lit1310, _mod1310 = _named_short(
    "弥耆迦",
    "弥耆迦",
    "明照有几种，能照明世间？唯愿世尊说，何等明最上？",
    "能照明世间的光有几种？愿世尊说，哪种光明最为最上？",
    "世间有四种光明，更无第五：昼以日为照，夜以月为照；"
    "灯火昼夜照，照彼彼色像；人天诸光明中，佛光明为上。",
    "世间有四种光明，找不到第五种：白天以太阳照耀，夜晚以月亮照耀；"
    "灯火白天夜晚都照，照见种种色像；在人天一切光明之中，佛的光明最为最上。",
    ask=True,
)
SUTTAS["SA_1310"] = {
    "lit": _lit1310,
    "mod": _mod1310,
    "notes": (
        f"{PROV}confidence=high：primary SN1.26（Pajjota）。"
        "据 SN：世间四光明——日、月、火、佛；汉「三种」据巴利校正为四种。"
        "结句「佛光明为上」＝ sambuddho tapataṃ seṭṭho。"
    ),
}

# ---------------------------------------------------------------------------
# confidence / reconstructed
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_1291": "high",
    "SA_1292": "high",
    "SA_1293": "medium",
    "SA_1294": "medium",
    "SA_1295": "medium",
    "SA_1296": "medium",
    "SA_1297": "medium",
    "SA_1298": "medium",
    "SA_1299": "medium",
    "SA_1300": "high",
    "SA_1301": "medium",
    "SA_1302": "high",
    "SA_1303": "high",
    "SA_1304": "high",
    "SA_1305": "high",
    "SA_1306": "high",
    "SA_1307": "high",
    "SA_1308": "high",
    "SA_1309": "high",
    "SA_1310": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1303": "汉「如蚊依从草」据 SN2.11 校正为鹿依无蚊草泽；佛答补不放逸、舍战诤。",
    "SA_1310": "汉「三种光明」据 SN1.26 校正为四种（日、月、火、佛）。",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

BATCH_IDS = [f"SA_{i}" for i in range(1291, 1311)]
# 邻批：前一路含 SA_1290（1271–1290）、后一路 SA_1311+
PARALLEL_BATCH_IDS = {f"SA_{i}" for i in range(1271, 1291)} | {
    f"SA_{i}" for i in range(1311, 1331)
}

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

assert set(GOLD) == set(BATCH_IDS), f"GOLD keys mismatch: {set(GOLD) ^ set(BATCH_IDS)}"
assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
assert set(RECONSTRUCTED) <= set(GOLD)
assert PARALLEL_BATCH_IDS.isdisjoint(GOLD), "must not merge neighbor batches"


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
    aligned = ROOT / "data" / "aligned" / "raw_aligned_data.json"
    out = ROOT / "data" / "translated" / "final_translated_data.json"
    gold_dir = ROOT / "data" / "golden"
    gold_dir.mkdir(parents=True, exist_ok=True)

    if out.exists():
        records = json.loads(out.read_text(encoding="utf-8"))
    else:
        records = json.loads(aligned.read_text(encoding="utf-8"))

    parallel_before = {
        rec["id"]: _snap(rec) for rec in records if rec["id"] in PARALLEL_BATCH_IDS
    }
    sa1290_before = next(_snap(rec) for rec in records if rec["id"] == "SA_1290")

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

    for rid, before in parallel_before.items():
        for rec in merged:
            if rec["id"] == rid:
                assert before == _snap(rec), f"{rid} (neighbor) must remain untouched"
                break

    sa1290_after = next(_snap(rec) for rec in merged if rec["id"] == "SA_1290")
    assert sa1290_before == sa1290_after, "SA_1290 must remain unchanged"

    for i in range(1311, 1331):
        rid = f"SA_{i}"
        if rid in parallel_before:
            continue  # already asserted via parallel_before
        before = next(( _snap(r) for r in records if r["id"] == rid), None)
        after = next(( _snap(r) for r in merged if r["id"] == rid), None)
        if before is not None and after is not None:
            assert before == after, f"{rid} must remain untouched"

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1291-1310.json").write_text(
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
    continuous = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1291, 1311)
    )
    untouched_neighbors = all(
        f"SA_{i}" not in GOLD for i in list(range(1271, 1291)) + list(range(1311, 1331))
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

    yan_ok = (
        "离贪" in (by_merged["SA_1307"].get("kumarajiva_style_text") or "")
        and "生厌" in (by_merged["SA_1308"].get("kumarajiva_style_text") or "")
        and "厌故不乐" not in (by_merged["SA_1307"].get("kumarajiva_style_text") or "")
        and "厌故不乐" not in (by_merged["SA_1308"].get("kumarajiva_style_text") or "")
    )

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1291–SA_1310 only)")
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
    print(f"continuous_1291_1310_goldish={continuous}")
    print(f"neighbors_1271-1290_and_1311-1330_untouched={untouched_neighbors}")
    print(f"SA_1290_unchanged=True")
    print(f"SA_1307_1308_厌故离贪={yan_ok}")
    if needs_restyle:
        print("needs_restyle_detail:")
        for r in needs_restyle:
            print(f"  {r['id']} sim={r['sim']} reasons={r.get('gate_reasons')}")
    if fails:
        print("fail_detail:")
        for r in fails:
            print(f"  {r['id']} issues={r.get('issues')}")
    for r in sorted(report, key=lambda x: int(x["id"].split("_")[1])):
        print(
            f"  {r['id']}: status={r['review_status']} conf={r['confidence']} "
            f"val={r['status']} sim={r['sim']} paras={r['paragraphs']}"
        )


if __name__ == "__main__":
    main()
