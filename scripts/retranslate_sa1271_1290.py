#!/usr/bin/env python3
"""Retranslate SA 1271–1290（卷第五十 杂相应：四句法经～大地）→ merge.

本批二十经：
1271–1274 拘迦那／波纯提女系（四句法、拘迦那沙、波纯提女×2；SN1.39–40）
1275–1277 天子问答（触 SN1.22、愚痴人 SN2.22、嫌责 SN1.35）
1278 瞿迦黎（SN6.10／AN10.89）
1279–1284 负处／垂下／遮止／名称／技能／弹琴（1281＝SN1.24；余无专经或异）
1285–1290 乘捨 SN1.71、種別 SN1.36、善丈夫 SN1.31、慳贪 SN1.32、八天 SN1.38、大地

信：有 SN／AN 平行者据巴利／Sujato 厘义；无平行者降 medium。
达雅：白话与罗什风逐段对照；Devatā 公式压缩；sim 门限见 assess_gold。
禁「厌故不乐」→「厌故离贪」（本批多天子偈，无定型厌离句则不强插）。
边界：只合并 SA_1271–1290；不触碰 SA_1251–1270、SA_1291–1310。
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

OPEN_VAL_LIT = "如是我闻：一时，佛住王舍城山谷精舍。"
OPEN_VAL_MOD = "我是这样听说的：有一次，佛住在王舍城山谷精舍。"

OPEN_VES_LIT = "如是我闻：一时，佛住毗舍离猕猴池侧重阁讲堂。"
OPEN_VES_MOD = "我是这样听说的：有一次，佛住在毗舍离猕猴池侧重阁讲堂。"

OPEN_BAM_LIT = "如是我闻：一时，佛住王舍城迦兰陀竹园。"
OPEN_BAM_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

OPEN_GOLD_LIT = "如是我闻：一时，佛住王舍城金婆罗山、金婆罗鬼神住处石室中。"
OPEN_GOLD_MOD = "我是这样听说的：有一次，佛住在王舍城金婆罗山、金婆罗鬼神住处的石室中。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "彼婆罗门闻佛所说，欢喜随喜，礼足而去。"
CLOSE_LAY_MOD = "那位婆罗门听佛所说，欢喜随喜，顶礼佛足后离去。"

DEVA_NIGHT_LIT = (
    "后夜分，有天子容色绝妙，来诣佛所，稽首礼足，退坐一面；"
    "身诸光明遍照祇树给孤独园。"
)
DEVA_NIGHT_MOD = (
    "后夜分，有一位天子容色绝妙，来到佛前，顶礼佛足，退坐一面；"
    "身上的光明遍照祇树给孤独园。"
)

EPI_LIT = "久见婆罗门，逮得般涅槃，一切怖已过，永超世恩爱。"
EPI_MOD = "久见婆罗门，逮得般涅槃，一切怖惧已过，永超世间恩爱。"

DEVA_CLOSE_LIT = f"天子复说偈：「{EPI_LIT}」闻已欢喜，礼足即没。"
DEVA_CLOSE_MOD = f"天子又说偈：「{EPI_MOD}」听完欢喜随喜，顶礼佛足，随即隐没不见。"

# SN1.39–40 四句法（身口意不作恶；舍欲、正念正知、不习无益苦）
FOUR_LIT = (
    "于一切世间，身口意莫作恶；舍诸欲，正念正知，勿习近无益之苦。"
)
FOUR_MOD = (
    "在一切世间，身、口、意都不要作恶；舍离诸欲，保持正念正知，"
    "不要习近那无益的苦。"
)

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


# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 1271 四句法经（近 SN1.39–40 偈；无专经）------------------------------
SUTTAS["SA_1271"] = {
    "lit": [
        OPEN_VAL_LIT,
        "尊者阿难告诸比丘：「我当说四句法。谛听，善思。」即说偈："
        f"「{FOUR_LIT}」"
        "「比丘！是名四句法。」",
        "时有异婆罗门在侧为年少受诵，作念：「阿难此偈，于我所诵，乃是非人语。」"
        "即诣佛所，问讯已白言：「瞿昙！阿难所说，是非人语，非人说。」",
        "佛言：「如是，婆罗门！此是非人语。昔有拘迦尼天女来诣我所，礼足说此偈；"
        f"我亦印可：『{FOUR_LIT}』"
        "是故当知：此偈非人所说，非人所说。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_VAL_MOD,
        "尊者阿难对比丘们说：「我要说四句法。仔细听，好好想。」便说偈："
        f"「{FOUR_MOD}」"
        "「比丘们！这叫做四句法。」",
        "当时有位婆罗门在旁边教少年诵经，心想：「阿难这偈，对照我教的经，竟是非人说的话。」"
        "便到佛前，问讯后说：「瞿昙！阿难所说，是非人的话，不是人说的。」",
        "佛说：「是的，婆罗门！这是非人说的。从前拘迦尼天女来到我这里，顶礼后说了这偈；"
        f"我也印可：『{FOUR_MOD}』"
        "所以应当知道：这偈是非人说的，不是人说的。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；偈与 SN1.39–40 Kokanadā／"
        "Pajjunna 女所说同轨（身口意不作恶、舍欲正念、不习无益苦）。"
        "汉「其心不为恶／五欲悉虚空」据 SN 作身口意莫作恶、舍诸欲。"
        "「非人语」＝非人（天）所说，非「鬼话」义。"
    ),
}

# --- SA 1272 拘迦那沙（近 SN1.40；无专列）------------------------------------
SUTTAS["SA_1272"] = {
    "lit": [
        OPEN_VAL_LIT,
        "时拘迦那娑天女——光明天女，电光炽然——归佛法僧，来诣佛所，礼足退坐，"
        f"身光普照山谷，说偈：「{FOUR_LIT}」",
        f"佛告天女：「如是，如汝所言：『{FOUR_LIT}』」"
        "天女闻已欢喜，礼足即没。",
        "夜过晨朝，佛入僧中敷座，告诸比丘：「昨后夜拘迦那娑天女来，说此饶益偈；"
        "我亦印可。拘迦那天女，电光炎炽，敬礼三宝，说偈义饶益。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VAL_MOD,
        "当时拘迦那娑天女——光明天女，电光炽盛——归依佛法僧，来到佛前，顶礼后退坐，"
        f"身光普照山谷，说偈：「{FOUR_MOD}」",
        f"佛对天女说：「是的，正如你所说：『{FOUR_MOD}』」"
        "天女听完欢喜，顶礼后随即隐没。",
        "夜过天明，佛进入僧众中敷座，对比丘们说：「昨天后夜拘迦那娑天女来，"
        "说了这有益的偈；我也印可。拘迦那天女，电光炽盛，敬礼三宝，说偈饶益。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；内容近 SN1.40（幼拘迦那／波纯提女）"
        "之来访、说四句法、佛印可、晨朝告众。偈据 SN 校正。"
    ),
}

# --- SA 1273 波纯提女（SN1.40 Kokanadā 幼）----------------------------------
SUTTAS["SA_1273"] = {
    "lit": [
        OPEN_VAL_LIT,
        "后夜，拘迦那娑天女——波纯提之女、光明天女——放电炎炽，来诣佛所，礼足退坐，"
        "身光普照山谷，说偈：「我能广分别如来正法律；今且略说，以表其心。"
        f"{FOUR_LIT}」",
        f"佛言：「如是，天女！如汝所言：『{FOUR_LIT}』」"
        "天女欢喜礼足，即没不现。",
        "晨朝佛告诸比丘：「昨后夜拘迦那娑来，先自能广说正法而略表其心，"
        f"次说四句；我印可之。彼闻已欢喜，礼足即没。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VAL_MOD,
        "后夜，拘迦那娑天女——波纯提的女儿、光明天女——放电光炽盛，来到佛前，顶礼后退坐，"
        "身光普照山谷，说偈：「我能广分别如来的正法律；现在只略说，以表达心意。"
        f"{FOUR_MOD}」",
        f"佛说：「是的，天女！正如你所说：『{FOUR_MOD}』」"
        "天女欢喜顶礼，随即隐没。",
        "天明佛对比丘们说：「昨天后夜拘迦那娑来，先说自己能广讲正法而只略表心意，"
        f"再说四句；我印可了。她听完欢喜，顶礼后隐没。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.40（Kokanadā the Younger）。"
        "据 SN：能广分别而略说；身口意不作恶；舍欲、正念正知、不习无益苦。"
        "汉住山谷精舍，巴利近毗舍离大木；框从汉，义从 SN。"
    ),
}

# --- SA 1274 波纯提女（SN1.39 Kokanadā）-------------------------------------
SUTTAS["SA_1274"] = {
    "lit": [
        OPEN_VES_LIT,
        "后夜，拘迦那娑天女与朱卢陀天女来诣佛所，礼足退坐，身光遍照猕猴池侧。",
        "朱卢陀说偈：「大师等正觉，住毗舍离；我朱卢陀与拘迦那，稽首敬礼。"
        "昔唯传闻牟尼正法，今乃现见圣者说法。"
        "于圣法律以恶慧厌毁者，必堕恶道，长夜受苦；"
        "于圣法律正念律仪具足者，生善趣天，长夜安乐。」",
        f"拘迦那复说：「{FOUR_LIT}」",
        f"佛印可：「如汝所言：『{FOUR_LIT}』」二天女欢喜，即没不现。",
        "晨朝佛告诸比丘，具述二天女所赞及四句法，并己所印可。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_VES_MOD,
        "后夜，拘迦那娑天女与朱卢陀天女来到佛前，顶礼后退坐，身光遍照猕猴池侧。",
        "朱卢陀说偈：「大师等正觉住在毗舍离；我朱卢陀与拘迦那，顶礼敬礼。"
        "从前只听闻牟尼正法，现在才亲眼看见圣者说法。"
        "对圣法律以恶慧厌毁的人，必堕恶道，长夜受苦；"
        "对圣法律正念、律仪具足的人，生到善趣天上，长夜安乐。」",
        f"拘迦那又说：「{FOUR_MOD}」",
        f"佛印可：「正如你们所说：『{FOUR_MOD}』」二位天女欢喜，随即隐没。",
        "天明佛对比丘们详细讲述二天女的赞叹和四句法，以及自己的印可。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.39。"
        "据 SN：厌毁圣法者堕恶趣；信受具戒者生天。汉「朱卢陀」并存（巴利或以拘迦那一人出）；"
        "四句法据 SN1.39–40。不用「厌故不乐」。"
    ),
}

# --- SA 1275 触（SN1.22）-----------------------------------------------------
_lit1275, _mod1275 = _deva(
    "不侵人者，侵不能及；侵人者，侵乃及之。侵无过者，侵还自受。",
    "不侵犯别人的人，侵犯伤不到他；去侵犯别人的，侵犯才会落到自己头上。"
    "侵犯没有过错的人，那侵犯还是回到自己身上。",
    "若于无过、清净无垢之士起瞋加害，恶还自中——如逆风扬尘，还坌己身。",
    "若对没有过错、清净无垢的人起瞋加害，恶果还回到自己身上——"
    "就像逆风扬尘，尘土还是扑到自己身上。",
)
SUTTAS["SA_1275"] = {
    "lit": _lit1275,
    "mod": _mod1275,
    "notes": (
        f"{PROV}confidence=high：primary SN1.22。"
        "据 SN 校正：汉「无触不报触」语拙，义为不侵者不受侵、侵无过者恶自还；"
        "佛答以逆风扬尘喻。"
    ),
}

# --- SA 1276 愚痴人（SN2.22 Khema）------------------------------------------
_lit1276, _mod1276 = _deva(
    "愚人所行，不合黠慧；自作恶行，即自恶友；所造众恶，终获苦报。",
    "愚人的所作所为，不合智慧；自己作恶，就是自己的恶知识；所作众恶，终得苦报。",
    "作不善业，后必热恼——造时虽喜，啼泣受报。作诸善业，后不热恼——"
    "欢喜而作，安乐受报。",
    "作了不善业，后来必定热恼——造作时虽然欢喜，却要啼泣受报。"
    "作了诸善业，后来不会热恼——欢喜而作，安乐受报。",
)
SUTTAS["SA_1276"] = {
    "lit": _lit1276,
    "mod": _mod1276,
    "notes": (
        f"{PROV}confidence=high：primary SN2.22（Khema）。"
        "据 SN：恶业后苦、善业后乐；汉略车轴喻，存汉简幅而义从 SN。"
    ),
}

# --- SA 1277 嫌责（SN1.35）---------------------------------------------------
SUTTAS["SA_1277"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "天子说偈：「非唯言说、非唯听闻，便能行此难行之道；"
        "唯正念静虑者，乃解脱魔缚。"
        "应说所行、行其所说；空言不行，智者知其非——如同窃取。」",
        "佛问：「汝今嫌责于我耶？」天子白：「悔过，世尊！悔过，善逝！」"
        "世尊熙怡微笑。",
        "天子复言：「我已悔过，世尊若不纳受，内怀瞋恨，则结怨不舍。」",
        "佛答：「言悔而内心不息，云何息怨？何名修善？"
        "谁无过失？谁无迷谬？谁能常坚固正念？"
        "如来悲悯一切——无过、无谬、正念坚固。"
        "我不取结怨，是故纳汝悔过。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "天子说偈：「不是只靠说话、也不是只靠听闻，就能走上这条难行的道；"
        "只有正念静虑的人，才能解脱魔的系缚。"
        "应当说自己做得到的、也做到自己所说的；空口说而不做，智者知道那不对——如同偷窃。」",
        "佛问：「你们现在是在嫌责我吗？」天子说：「悔过，世尊！悔过，善逝！」"
        "世尊和颜微笑。",
        "天子又说：「我已经悔过，若世尊不接受，心里怀着瞋恨，就会结怨不放。」",
        "佛答：「口头悔过而内心不息灭，怎么能息怨？哪能叫修善？"
        "谁没有过失？谁没有迷谬？谁能常常正念坚固？"
        "如来悲悯一切——没有过错、没有迷谬、正念坚固。"
        "我不取结怨，所以接受你们的悔过。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.35（Ujjhānasaññino）。"
        "据 SN 校正：汉略「纳悔／如来无过」答偈，今据巴利补全；"
        "佛微笑后天子更生嫌责，佛明不结怨而纳悔。"
        "gold_reconstructed：汉本嫌责经缺佛最终纳悔偈，据 SN1.35 补。"
    ),
}

# --- SA 1278 瞿迦黎（SN6.10／AN10.89）---------------------------------------
SUTTAS["SA_1278"] = {
    "lit": [
        OPEN_BAM_LIT,
        "瞿迦梨比丘——提婆达多伴党——来诣佛所，礼足退坐。"
        "佛告：「瞿迦梨！莫于舍利弗、目犍连清净梵行者起不净心；长夜当得大苦。」",
        "彼白佛：「我信世尊语；然舍利弗、大目犍连心有恶欲。」如是再三，不受教，"
        "从座起去。去已，身生疱疮，渐大如桃李，脓血流出，身坏命终，生摩诃钵昙摩地狱。",
        "后夜三天子来：一天子白「瞿迦梨已命终」；第二天子言「已堕地狱」；"
        "第三说偈：「士夫生世，斧生口中，恶言自斩。"
        "应毁而誉、应誉而毁，罪从口生，死堕恶道。"
        "博弈失财，过犹为小；毁佛及声闻，乃为大过。」说已即没。",
        "晨朝佛告众，问欲闻阿浮陀等地狱寿量不。比丘请说。"
        "佛言：「如拘萨罗满仓芥子，百年取一，芥尽而阿浮陀寿犹不尽；"
        "二十阿浮陀等一尼罗浮陀，展转二十倍至摩诃钵昙摩。"
        "瞿迦梨以诽谤舍利弗、目犍连故，堕摩诃钵昙摩。"
        "是故当学：于烧焦炷尚不欲毁，何况有识众生？」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "瞿迦梨比丘——提婆达多的同伴——来到佛前，顶礼后退坐。"
        "佛说：「瞿迦梨！不要对舍利弗、目犍连这些清净梵行者起不净心；长夜会受大苦。」",
        "他说：「我信世尊的话；可是舍利弗、大目犍连心里有恶欲。」这样说了三次，不听劝，"
        "从座起身离去。离去后，全身生出疱疮，渐渐大如桃李，脓血流出，身坏命终，"
        "生到摩诃钵昙摩地狱。",
        "后夜三位天子来：一位说「瞿迦梨已经命终」；第二位说「已经堕地狱」；"
        "第三位说偈：「人出生在世间，斧头就生在口中，恶言会斩断自己。"
        "该贬却夸、该夸却贬，罪从口生，死后堕恶道。"
        "赌博输钱，过错还算小；毁谤佛与声闻，才是大过。」说完就隐没。",
        "天明佛告诉大众，问是否想听阿浮陀等地狱的寿命。比丘们请说。"
        "佛说：「好比拘萨罗国满仓芥子，一百年取一粒，芥子取尽而阿浮陀的寿命还没尽；"
        "二十个阿浮陀等于一个尼罗浮陀，这样二十倍展转到摩诃钵昙摩。"
        "瞿迦梨因为诽谤舍利弗、目犍连，堕入摩诃钵昙摩。"
        "所以应当学：连烧焦的灯炷都不想毁坏，何况有情识的众生？」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN6.10（并 AN10.89）。"
        "据 SN：三劝不听；疮溃命终；堕粉红莲地狱；芥子仓喻寿量。"
        "汉三天子分报，巴利多作梵天沙婆主；义同，框从汉。"
    ),
}

# --- SA 1279 轻贱（无专经；负处门）-------------------------------------------
SUTTAS["SA_1279"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "天子问：「云何知堕负处？负处之门为何？」",
        "佛答：「乐法为胜处，毁法为负处。亲恶友、疏善友、与善结怨；"
        "斗秤欺人、博弈嗜酒、耽女色耗财；夫妇放荡不守；老少匹配而嫉；"
        "贪睡、戏游、懈怠瞋恨；多财奢费；少财而起王者之贪；"
        "庄严自悭、食人不报；请沙门而不时施、呵责乞者；"
        "有财不养父母、殴骂尊长；毁佛及弟子；非罗汉而自称——"
        "此皆世间负处，如险道，慧者当远避。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "天子问：「怎样知道堕入失败之处？失败之门是什么？」",
        "佛答：「乐法是胜处，毁法是负处。亲近恶友、疏远善友、与善人结怨；"
        "用秤斗骗人、赌博嗜酒、耽于女色耗财；夫妇放荡不守；老少匹配而生嫉妒；"
        "贪睡、嬉戏、懈怠瞋恨；多财却奢侈浪费；少财却起称王的贪心；"
        "妆饰自己却悭吝、吃人的却不回报；请沙门却不及时布施、呵责乞食者；"
        "有财却不奉养父母、殴打辱骂尊长；毁谤佛与弟子；不是阿罗汉却自称——"
        "这些都是世间的失败之处，像险路，有智慧的人应当远避。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；近诸天相应「败处／衰损」类教"
        "（cf. DN31 Sigālovāda 部分条目）。压缩汉长偈为义类，不臆造平行。"
    ),
}

# --- SA 1280 垂下-------------------------------------------------------------
_lit1280, _mod1280 = _deva(
    "谁屈下而随屈？谁高举而随举？云何如童戏，以土块相掷？",
    "谁低下就跟着低下？谁高举就跟着高举？怎么会像孩童戏耍，拿土块互相投掷？",
    "爱下则随下，爱举则随举；爱戏于愚夫，如童以块相掷。",
    "爱著低下就跟着低下，爱著高举就跟着高举；爱戏耍在愚人身上，就像孩童拿土块互掷。",
)
SUTTAS["SA_1280"] = {
    "lit": _lit1280,
    "mod": _mod1280,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；义为随爱高下、如童戏掷块。"
        "参 Devatā 问答定型。"
    ),
}

# --- SA 1281 遮止（SN1.24）---------------------------------------------------
_lit1281, _mod1281 = _deva(
    "若心有所遮，侵逼不能及；若遮一切境，则免一切苦。",
    "若心有所防护，侵逼就伤不到；若防护一切境界，就能免于一切苦。",
    "不必一切遮；心未全自在。但遮恶法所从来处，则不令逼迫。",
    "不必防护一切；心也还没有完全自在。只要防护恶法所从来的地方，就不会被逼迫。",
)
SUTTAS["SA_1281"] = {
    "lit": _lit1281,
    "mod": _mod1281,
    "notes": (
        f"{PROV}confidence=high：primary SN1.24。"
        "据 SN：非一切皆遮，但遮恶法所从生处。"
    ),
}

# --- SA 1282 名称-------------------------------------------------------------
_lit1282, _mod1282 = _deva(
    "云何得名称？云何得大财？云何德流闻？云何得善友？",
    "怎样得到好名声？怎样得到大财富？怎样德行流布远闻？怎样得到善友？",
    "持戒得名称，布施得大财，真实德流闻，恩惠得善友。",
    "持戒得到名声，布施得到大财，真实使德行流闻，恩惠得到善友。",
)
SUTTAS["SA_1282"] = {
    "lit": _lit1282,
    "mod": _mod1282,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；戒／施／真实／恩惠四答，"
        "义与诸天相应福德问答同轨。"
    ),
}

# --- SA 1283 技能-------------------------------------------------------------
SUTTAS["SA_1283"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "天子问：「人智以求财，当如何等摄？胜劣如何分？」",
        "佛答：「先学功巧，方便集财；得已分作四：一分自用，二分营生，"
        "一分密藏以备匮乏。营生则田种、商贾、牧畜、邸舍求利。"
        "善修如蜂集味、蚁积土，财日夜增。"
        "不付老耄、不寄边民、不信奸悭；亲成事者，远不成事。"
        "于亲族中如牛王分财饮食；寿尽生天受乐。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "天子问：「人用智慧求财，应当怎样妥善管理？好坏怎样区分？」",
        "佛答：「先学技艺，用方法集财；得到以后分成四份：一份自己用，两份经营生计，"
        "一份密藏以防匮乏。经营则种田、经商、畜牧、开邸舍求利。"
        "好好经营，就像蜜蜂采蜜、蚂蚁积土，财物日夜增长。"
        "不要托付给老迈的人、不要寄放在边地之民、不要信任奸诈悭吝的人；"
        "亲近能成事的，远离不能成事的。"
        "在亲族中像牛王一样分配财物饮食；寿命尽了生天受乐。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；四分财法近 AN8.54／DN31 居士理财教。"
        "压缩汉长偈，不臆造专经平行。"
    ),
}

# --- SA 1284 弹琴-------------------------------------------------------------
SUTTAS["SA_1284"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告诸比丘：「过去拘萨罗有弹琴人，名麤牛，游行止野中。"
        "六天宫天女来请：『阿舅！为我弹琴，我当歌舞。』"
        "麤牛曰：『我为汝弹；汝当自说生此因缘。』天女曰：『且弹，歌中自说。』"
        "彼即弹琴，六天女歌舞。",
        "一天女：「胜妙衣施，故生殊胜，随欲游空，天身如金，天女百中胜。」"
        "二：「胜妙香施，亦复如是。」"
        "三：「以食惠施，亦复如是。」"
        "四：「昔为人婢，不盗不贪，勤而不懈，量腹分食济贫，故得天报。」"
        "五：「昔为子妇，嫜姑暴恶，我执礼卑逊奉顺，故得天报。」"
        "六：「昔从比丘、比丘尼闻法，一宿受斋，故得天报。」",
        "麤牛自庆：「我今善来此林，见闻天女；当增修善，亦当生天。」"
        "说已，天女即没。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛对比丘们说：「过去拘萨罗国有个弹琴人，名叫麤牛，游行停在野外。"
        "六位天宫的天女来请：『阿舅！为我们弹琴，我们来歌舞。』"
        "麤牛说：『我为你们弹；你们要自己说出往生这里的因缘。』"
        "天女说：『先弹吧，歌里自己会说。』他就弹琴，六位天女歌舞。",
        "第一位：「因为布施胜妙衣服，所以生得殊胜，随欲在空中游行，天身如金，在天女中超百人。」"
        "第二位：「因为布施胜妙香，也是这样。」"
        "第三位：「因为布施食物，也是这样。」"
        "第四位：「从前做人的婢女，不偷不贪，勤劳不懈怠，量腹节食分给穷人，所以得天报。」"
        "第五位：「从前做人家的儿媳，公婆暴恶，我守礼卑逊奉顺，所以得天报。」"
        "第六位：「从前从比丘、比丘尼听闻正法，一宿受持斋戒，所以得天报。」",
        "麤牛自己庆幸：「我今天来到这林中真好，看见并听闻天女；应当更修善业，也会生天。」"
        "说完，天女随即隐没。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；六天女因施衣／香／食、婢女节食、"
        "子妇忍顺、一宿斋戒而生天——早期福德教，不引入大乘术语。"
    ),
}

# --- SA 1285 乘捨（SN1.71 Chetvā；汉问式异）---------------------------------
_lit1285, _mod1285 = _deva(
    "何法灭则安寝？何法灭则无忧？杀何法为圣所许？",
    "什么法灭了就能安睡？什么法灭了就没有忧愁？杀掉什么是圣者所赞许的？",
    "瞋恚灭则安寝，瞋恚灭则无忧。瞋根有毒而端甜；圣赞灭瞋——灭已无忧。"
    "欲生诸烦恼，欲为苦本；调伏烦恼则调伏众苦，调伏众苦则烦恼亦调。",
    "瞋恚灭了就能安睡，瞋恚灭了就没有忧愁。瞋的根有毒而尖端甜蜜；"
    "圣者赞许灭除瞋——灭了就没有忧愁。"
    "欲生起诸烦恼，欲是苦的根本；调伏烦恼就调伏众苦，调伏众苦烦恼也跟着调伏。",
)
SUTTAS["SA_1285"] = {
    "lit": _lit1285,
    "mod": _mod1285,
    "notes": (
        f"{PROV}confidence=high：primary SN1.71。"
        "据 SN 校正：汉「何起应灭／贪生防护／无明应离」问式与巴利「灭瞋则安」不完全同文；"
        "今以灭瞋无忧为正，兼存汉「欲为苦本」收束。"
        "gold_reconstructed：问句据 SN1.71 改写。"
    ),
}

# --- SA 1286 種別（SN1.36）---------------------------------------------------
SUTTAS["SA_1286"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "天子说偈：「愚耽放逸；智护不放逸，如护最上财。"
        "勿乐放逸、勿耽欲乐；不放逸而静虑，疾尽诸漏。」",
        "佛答：「世间众事非即是欲；心驰觉想，乃名士夫欲。"
        "信为良伴，不信则不度；舍瞋离慢、超诸结缚；"
        "不著名色，远离积聚；能断杂相，超生死流——是名比丘。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "天子说偈：「愚人耽于放逸；智者防护不放逸，如同守护最上的财宝。"
        "不要乐于放逸、不要耽于欲乐；不放逸而静虑，很快就能尽诸漏。」",
        "佛答：「世间种种事物本身不是欲；心驰骋于觉想，才叫做人的欲。"
        "信是好伴侣，不信就不能度；舍瞋离慢、超越结缚；"
        "不著名色，远离积聚；能断除杂相，超出生死流——这才叫做比丘。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.36（Nānātitthiyā／Satullapakāyikā 类）。"
        "据 SN：不放逸为宝；欲在心不在事；信为伴；不著名色。"
        "汉单天子框，巴利多天子迭颂；压缩从汉，义从 SN。"
    ),
}

# --- SA 1287 善丈夫（SN1.31）-------------------------------------------------
_lit1287, _mod1287 = _deva(
    "与何人同处？与谁共事？知何人法，名为胜非恶？",
    "和什么人相处？和谁共事？了知什么人的法，才叫做殊胜而非恶？",
    "与正士同游，与正士共事，解知正士法——则解脱众苦，是胜非恶。",
    "和正士一起交游，和正士一起做事，了知正士的法——就能解脱众苦，这才是殊胜而非恶。",
)
SUTTAS["SA_1287"] = {
    "lit": _lit1287,
    "mod": _mod1287,
    "notes": (
        f"{PROV}confidence=high：primary SN1.31。"
        "据 SN：佛总结「亲近善士，解善说法，则解脱一切苦」；"
        "汉「胜非恶」据此作解脱众苦。巴利多天子各颂，汉压缩为一问答。"
    ),
}

# --- SA 1288 慳贪（SN1.32）---------------------------------------------------
SUTTAS["SA_1288"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "天子说：「悭吝心生，不能行施；明智求福，乃能惠施。」",
        "佛答：「因怖而不施，所怖还自至——饥渴之畏，今世后世恼愚人。"
        "少财能施，多财或悭；难舍而能舍，是名难施。"
        "百千盛会之福，不及如法少施十六分之一。"
        "打缚恼生而取财以施，是有罪施，不及如法平等施。"
        "难施能施，应贤圣行；所往获福，寿终生天。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "天子说：「悭吝心生起，就不能布施；明智求福的人，才能惠施。」",
        "佛答：「因为害怕而不布施，所怕的反而会来到——饥渴的怖畏，在今世后世恼害愚人。"
        "财物少而能施，财物多有时反而悭吝；难舍而能舍，才叫难能的布施。"
        "百千盛大祭祀的福，比不上如法少施的十六分之一。"
        "靠打绑恼害众生得来的财去布施，是有罪的施，比不上如法平等的施。"
        "难施而能施，才是贤圣所应行；所到之处得福，寿终生天。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.32。"
        "据 SN：悭怖还自至；少施倍胜大祀；有罪施不及如法施。"
        "汉「耶盛会」＝盛大祭祀；压缩多天子迭颂。"
    ),
}

# --- SA 1289 八天（SN1.38）---------------------------------------------------
SUTTAS["SA_1289"] = {
    "lit": [
        OPEN_GOLD_LIT,
        "尔时世尊为木枪所刺，身痛剧烈；然以正念正知，堪忍安住，心无退减。",
        "山神天子八人念：「世尊身苦而能舍心安忍，我等当往赞叹。」"
        "即诣佛所，礼足退住。",
        "一天子赞：「沙门瞿昙，人中师子，身遭苦痛，正念堪忍，无所退减。」"
        "二赞为大龙、牛王、良马、上首、最胜。"
        "三赞为分陀利华：身苦而行舍，正念安住。"
        "四言：「若于瞿昙分陀利所起嫌毁，长夜当得不饶益——除不知真实者。」"
        "五赞其定善住，解脱离尘，不踊不没，心得解脱。"
        "六–八言：诵吠陀、修苦行百年，为欲与戒取所缚，心不解脱——卑下不度彼岸；"
        "憍慢放逸独居山林，亦不得度死魔军。",
        "八天子各赞已，礼足即没。",
    ],
    "mod": [
        OPEN_GOLD_MOD,
        "那时世尊被木枪刺伤，身体剧痛；然而以正念正知，堪忍安住，心没有退减。",
        "八位山神天子心想：「世尊身体受苦却能舍心安忍，我们应当前去赞叹。」"
        "便来到佛前，顶礼后退住。",
        "一位天子赞：「沙门瞿昙，人中的狮子，身体遭受苦痛，正念堪忍，没有退减。」"
        "第二位赞为大龙、牛王、良马、上首、最胜。"
        "第三位赞为白莲花：身体受苦却行舍，正念安住。"
        "第四位说：「若对瞿昙这朵白莲起嫌毁，长夜会得不利益——除非是不知真实的人。」"
        "第五位赞他的定善住，解脱离尘，不向前倾也不后退沉没，心得解脱。"
        "第六至第八位说：诵吠陀、修苦行一百年，被欲与戒取所缚，心不解脱——"
        "是卑下一类，不能度到彼岸；憍慢放逸独自住在山林，也不能度过死魔的军队。",
        "八位天子各自赞叹完毕，顶礼后随即隐没。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.38（Sakalika）。"
        "据 SN：木枪刺足；正念正知安忍；诸天赞象／狮／龙／调御；"
        "定不前倾后仰；吠陀苦行者心不解脱。汉「金鎗」＝木枪／裂片；八天从汉数。"
    ),
}

# --- SA 1290 大地-------------------------------------------------------------
_lit1290, _mod1290 = _deva(
    "广无过于地，深无踰于海，高无过须弥，大士无毘纽。",
    "广阔没有超过大地的，深没有超过大海的，高没有超过须弥的，大士没有超过毘纽的。",
    "广无过于爱，深无踰于腹，高莫过憍慢，大士无胜佛。",
    "广阔没有超过爱的，深没有超过肚腹的，高没有超过憍慢的，大士没有胜过佛的。",
)
SUTTAS["SA_1290"] = {
    "lit": _lit1290,
    "mod": _mod1290,
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；以爱／腹／慢对破地／海／山／毘纽，"
        "结归佛为最上士。毘纽＝Viṣṇu，存名而义从早期对破。"
    ),
}

# ---------------------------------------------------------------------------
# confidence / reconstructed
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_1271": "medium",
    "SA_1272": "medium",
    "SA_1273": "high",
    "SA_1274": "high",
    "SA_1275": "high",
    "SA_1276": "high",
    "SA_1277": "high",
    "SA_1278": "high",
    "SA_1279": "medium",
    "SA_1280": "medium",
    "SA_1281": "high",
    "SA_1282": "medium",
    "SA_1283": "medium",
    "SA_1284": "medium",
    "SA_1285": "high",
    "SA_1286": "high",
    "SA_1287": "high",
    "SA_1288": "high",
    "SA_1289": "high",
    "SA_1290": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1277": "汉本缺佛最终纳悔／如来无过偈，据 SN1.35 补。",
    "SA_1285": "汉问式与 SN1.71「灭瞋则安」不完全同文，问句据巴利改写。",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

BATCH_IDS = [f"SA_{i}" for i in range(1271, 1291)]
# 邻批：前一路 1251–1270、后一路起点 1291+（并行中亦不可覆写）
PARALLEL_BATCH_IDS = {f"SA_{i}" for i in range(1251, 1271)} | {
    f"SA_{i}" for i in range(1291, 1311)
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

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1271-1290.json").write_text(
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1271, 1291)
    )
    untouched_neighbors = all(
        f"SA_{i}" not in GOLD for i in list(range(1251, 1271)) + list(range(1291, 1311))
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1271–SA_1290 only)")
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
    print(f"continuous_1271_1290_goldish={continuous}")
    print(f"neighbors_1251-1270_and_1291-1310_untouched={untouched_neighbors}")
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
