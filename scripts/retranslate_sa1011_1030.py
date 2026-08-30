#!/usr/bin/env python3
"""Retranslate SA 1011–1030（诸天相应续 + 业报相应起）→ merge.

本批二十经：
1011–1022 诸天相应续（覆、无明、信、第二、持戒至老、生世间×3、非道、最上胜、偈者、别车）
1023–1030 业报相应起（叵求那 AN6.56、阿湿波誓 SN22.88、疾病 SN35.74–75、病比丘、
        疾病 SN36.7–8、给孤独）

信：有 SN／AN 平行者据巴利／Sujato 厘义；1012、1027、1030 无 SC 巴利专经 → medium。
    1011 据 SN1.68 校正汉偈（死掩／苦依／爱罗／老围，非衰／死／爱／法）；
    1018 据 SN1.55 校正「苦甚可畏」（汉作「业」）；
    1021 据 SN1.60：chanda＝韵律、kavi＝诗人。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_1011–1030；不触碰邻经 SA_1010、SA_1031；
      若邻经已为 gold／gold_reconstructed 则断言不变。
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

batch_range = range(1011, 1031)

# ---------------------------------------------------------------------------
# 共用框式
# ---------------------------------------------------------------------------

OPEN_JET_LIT = "如是我闻：一时，佛住舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_AN_LIT = "佛说此经已，尊者阿难闻佛所说，欢喜随喜，作礼而去。"
CLOSE_AN_MOD = "佛说完这部经，尊者阿难听佛所说，欢喜随喜，作礼离去。"

DEVA_NIGHT_LIT = (
    "后夜分，有天子来诣佛所，容色绝妙，稽首礼足，退坐一面；身诸光明遍照祇园。"
)
DEVA_NIGHT_MOD = (
    "后夜分，有一位天子，容色绝妙，来到佛前，顶礼佛足，退坐一面；"
    "身上的光明遍照祇树给孤独园。"
)

DEVA_CLOSE_LIT = (
    "天子说偈：「久见婆罗门，逮得般涅槃，一切怖已过，永超世恩爱。」"
    "闻已欢喜，礼足即没。"
)
DEVA_CLOSE_MOD = (
    "天子又说偈：「久见婆罗门，逮得般涅槃，一切怖已过，永超世恩爱。」"
    "听完欢喜随喜，顶礼佛足，随即隐没不见。"
)

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

FIVE_LOWER_LIT = "五下分结（身见、戒取、疑、欲贪、瞋恚）"
FIVE_LOWER_MOD = "五下分结（身见、戒取、疑、欲贪、瞋恚）"

THREE_VED_ASK_LIT = (
    "「云何？苦患可忍不？为增为损？」"
    "白言：「甚苦，难可堪忍；苦受但增不损。」"
)
THREE_VED_ASK_MOD = (
    "「怎么样？苦痛还能忍受吗？是在加重还是减轻？」"
    "答：「很苦，难以忍受；苦受只增不减。」"
)


def _deva_exchange(
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

# --- SA 1011 覆（SN1.68 Pihita）---------------------------------------------
_lit, _mod = _deva_exchange(
    "谁掩于世间？何处世间住？谁罗于世间？谁围覆世间？",
    "什么把世间掩闭？世间安住在什么上？什么罗网世间？什么围覆世间？",
    "死掩于世间，苦为世间住，爱罗于世间，老围覆世间。",
    "死把世间掩闭，世间安住在苦上，爱把世间罗住，老把世间围覆。",
)
SUTTAS["SA_1011"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}confidence=high：primary SN1.68；"
        "据巴利校正汉偈：maccu 掩、dukkha 住、taṇhā 罗、jarā 围"
        "（汉「衰老／死／爱／法」与平行错位，已改）。"
    ),
}

# --- SA 1012 无明（无巴利专经；sa-2.239）------------------------------------
SUTTAS["SA_1012"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "天子说偈问：「谁隐覆世间？谁系缚世间？谁忆念众生？谁建众生幢？」",
        "世尊说偈答：「无明覆世间，爱结缚众生，隐覆忆众生，我慢为生幢。」",
        "天子复问：「谁无有覆盖？谁复无爱结？谁出离隐覆？谁不建慢幢？」",
        "世尊说偈答：「如来等正觉，正智心解脱，不为无明覆，亦无爱结系，"
        "超出诸隐覆，摧灭我慢幢。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "天子说偈问：「谁把世间隐覆？谁系缚世间？谁忆持众生？谁竖起众生的幢？」",
        "世尊说偈答：「无明覆盖世间，爱结系缚众生，隐覆令众生被忆持，我慢是众生幢。」",
        "天子又问：「谁没有覆盖？谁没有爱结？谁出离隐覆？谁不竖我慢幢？」",
        "世尊说偈答：「如来等正觉，以正智心得解脱，不被无明覆，也不被爱结系，"
        "超出一切隐覆，摧灭我慢幢。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：parallel sa-2.239，无巴利专经；无明覆／爱结／我慢幢，从汉本。"
    ),
}

# --- SA 1013 信（SN1.73 Vitta）-----------------------------------------------
_lit, _mod = _deva_exchange(
    "何者士夫最上财？何法善修招安乐？众味之中何最胜？云何寿命说第一？",
    "人的最上财富是什么？什么善修习能招来安乐？众味之中什么最甜？怎样活命才算第一？",
    "净信为士夫胜财，正法善修招安乐，真谛说为味中上，慧命乃为寿中最。",
    "清净的信是人的胜财，正法善修习能招安乐，真谛是味道中最上的，以慧活命才是寿中第一。",
)
SUTTAS["SA_1013"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": f"{PROV}confidence=high：primary SN1.73；信财、法乐、谛味、慧命。",
}

# --- SA 1014 第二（SN1.59 Dutya）---------------------------------------------
_lit, _mod = _deva_exchange(
    "比丘同己第二谁？谁为随顺教授者？何处游心自娱乐，娱乐已能断诸结？",
    "比丘以谁为同伴第二？谁是随顺教授他的？心在何处自娱，娱已能断诸结？",
    "信为同己之第二，智慧为彼教授者，涅槃喜乐处游心，比丘于是断结缚。",
    "信是同伴第二，智慧是教授者，心游于涅槃喜乐处，比丘因此断结缚。",
)
SUTTAS["SA_1014"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": f"{PROV}confidence=high：primary SN1.59；信为伴、慧为教、乐涅槃断苦。",
}

# --- SA 1015 持戒至老（SN1.51 Jarā）-----------------------------------------
_lit, _mod = _deva_exchange(
    "云何善法至年老？云何善法得建立？云何名为人之宝？云何盗贼不能夺？",
    "什么到老仍善好？什么善好地安立？什么是人的宝藏？什么盗贼夺不走？",
    "持戒善好至年老，净信善好得建立，智慧名为人之宝，功德贼不能夺。",
    "持戒到老仍善好，净信善好地安立，智慧是人的宝藏，功德盗贼夺不走。",
)
SUTTAS["SA_1015"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": f"{PROV}confidence=high：primary SN1.51；戒、信、慧、福德。",
}

# --- SA 1016 生世间（SN1.56 Jana）--------------------------------------------
_lit, _mod = _deva_exchange(
    "何法能生诸众生？何等在前而驰驱？云何轮转于生死？何者令彼不解脱？",
    "什么能生起众生？什么在前奔驰？怎样轮转生死？什么使他不得解脱？",
    "爱欲能生诸众生，其心在前而驰驱，有情轮转于生死，苦法令彼不解脱。",
    "爱欲能生起众生，心在前奔驰，有情轮转生死，苦使他不得解脱。",
)
SUTTAS["SA_1016"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}confidence=high：primary SN1.56；"
        "taṇhā 生、citta 驰、satta 入轮回、dukkha 不解脱。"
    ),
}

# --- SA 1017 生世间（SN1.57）-------------------------------------------------
_lit, _mod = _deva_exchange(
    "何法能生诸众生？何等在前而驰驱？云何轮转于生死？何法可为所依怙？",
    "什么能生起众生？什么在前奔驰？怎样轮转生死？什么可作为归依？",
    "爱欲能生诸众生，其心在前而驰驱，有情轮转于生死，业为可依怙。",
    "爱欲能生起众生，心在前奔驰，有情轮转生死，业是可依怙的。",
)
SUTTAS["SA_1017"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": f"{PROV}confidence=high：primary SN1.57；末句 kamma 为归趣（parāyana）。",
}

# --- SA 1018 生世间（SN1.55）-------------------------------------------------
_lit, _mod = _deva_exchange(
    "何法能生诸众生？何等在前而驰驱？云何轮转于生死？何法甚为可怖畏？",
    "什么能生起众生？什么在前奔驰？怎样轮转生死？什么最为可怖畏？",
    "爱欲能生诸众生，其心在前而驰驱，有情轮转于生死，苦为甚可畏。",
    "爱欲能生起众生，心在前奔驰，有情轮转生死，苦是最为可怖畏的。",
)
SUTTAS["SA_1018"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}confidence=high：primary SN1.55；"
        "据巴利校正：dukkha 为 mahabbhaya（汉作「业」误，已改）。"
    ),
}

# --- SA 1019 非道（SN1.58 Uppatha）-------------------------------------------
_lit, _mod = _deva_exchange(
    "何名说为非道迹？云何日夜迁谢尽？云何垢秽于梵行？何者无水能澡浴？",
    "什么叫做非道？什么日夜在消尽？什么是梵行的垢秽？什么是无水之浴？",
    "贪欲说名非道迹，寿命日夜迁谢尽，女人为梵行之垢，世人所染著于彼；"
    "炽然与修于梵行，是则无水之澡浴。",
    "贪欲叫做非道，寿命日夜消尽，女人为梵行的垢秽，众生染著于此；"
    "热诚与修梵行，便是无水的澡浴。",
)
SUTTAS["SA_1019"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}confidence=high：primary SN1.58；"
        "rāga 非道、vaya 日夜尽、itthī 梵行垢、tapo+brahmacariya 无水浴。"
    ),
}

# --- SA 1020 最上胜（SN1.61 Nāma）--------------------------------------------
_lit, _mod = _deva_exchange(
    "何法映蔽于世间？何法更无有其上？何为一法普制御，令诸众生皆随顺？",
    "什么映蔽一切世间？什么没有比它更高的？哪一法能普遍制御，令众生都随顺？",
    "名者映蔽于世间，名者更无有其上，唯有一名之一法，能制御诸世间。",
    "名映蔽一切世间，没有比名更高的，单单「名」这一法，就能制御一切世间。",
)
SUTTAS["SA_1020"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": f"{PROV}confidence=high：primary SN1.61；nāma 映一切、无有过其上。",
}

# --- SA 1021 偈者（SN1.60 Gāthā）---------------------------------------------
_lit, _mod = _deva_exchange(
    "何法为诸偈之因？以何庄严于诸偈？诸偈何所依而住？何者名为偈之体？",
    "什么是偈颂的因？用什么庄严偈颂？偈颂依止什么？什么是偈颂的主体？",
    "韵律为诸偈之因，文字庄严于诸偈，名者偈之所依住，诗人名为偈之体。",
    "韵律是偈颂的因，文字庄严偈颂，名是偈颂所依，诗人是偈颂的主体。",
)
SUTTAS["SA_1021"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": (
        f"{PROV}confidence=high：primary SN1.60；"
        "据巴利：chanda＝韵律（非「欲」）、akkharā＝文字、nāma＝名、kavi＝诗人"
        "（汉「欲／造作」已校正）。"
    ),
}

# --- SA 1022 别车（SN1.72 Ratha）---------------------------------------------
_lit, _mod = _deva_exchange(
    "云何得知于车乘？云何复知于火起？云何得知于国土？云何得知于妻妇？",
    "凭什么认得车乘？凭什么认得有火？凭什么认得国土？凭什么认得妻妇？",
    "见幢盖故知有车，见烟故知有火起，见王故知有国土，见夫故知其为妻。",
    "看见幢盖就知道有车，看见烟就知道有火，看见王就知道有国土，看见丈夫就知道她是妻。",
)
SUTTAS["SA_1022"] = {
    "lit": _lit,
    "mod": _mod,
    "notes": f"{PROV}confidence=high：primary SN1.72；幢／烟／王／夫为征知。",
}

# --- SA 1023 叵求那（AN6.56 Phagguna）---------------------------------------
SUTTAS["SA_1023"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者叵求那住东园鹿母讲堂，疾病困笃。尊者阿难白佛："
        "「叵求那病笃，病比丘多有死者。愿世尊往视，以哀愍故！」世尊默许。",
        "日晡从禅觉，往彼房敷座而坐，为说种种法，示教照喜已，从坐起去。"
        "世尊去后，叵求那寻命终；临终诸根喜悦，颜貌清净，肤色鲜白。",
        "阿难供养舍利已，白佛：「彼临终诸根喜悦、肤色鲜泽，当生何趣？后世云何？」",
        "佛告阿难：「闻法及时，有六种福利。何等为六？",
        f"「若比丘先未病时未断{FIVE_LOWER_LIT}，病起苦患、生分微弱，得闻大师说法，闻已断五下分结——"
        "是名大师说法福利。",
        "「若不蒙大师，而得余多闻梵行者说法，闻已断五下分结——是名教授听法福利。",
        "「若两俱不闻，而先所闻法独静思惟观察，得断五下分结——是名思惟先闻法福利。",
        "「复次，若先已断五下分结，而不得无上爱尽、不起诸漏、心善解脱；"
        "病时得闻大师说法，便得无上爱尽解脱——是名大师说法福利。",
        "「若不得大师，而得余梵行者说法，亦得无上爱尽解脱——是名教授闻法福利。",
        "「若两俱不闻，而思惟先闻法，得无上爱尽解脱——是名思惟先闻法福利。",
        "「叵求那先未断五下分结，亲从大师闻法，即断五下分结；"
        "是故诸根喜悦。我记彼得阿那含。」",
        CLOSE_AN_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时尊者叵求那住在东园鹿母讲堂，病重危急。尊者阿难对佛说："
        "「叵求那病得很重，病比丘常有死去的。愿世尊去看他，出于哀愍！」世尊默然答应。",
        "傍晚从禅定起来，到他房中敷座坐下，为他种种说法，开示劝勉令欢喜后离去。"
        "世尊走后，叵求那不久命终；临终时诸根喜悦，面容清净，肤色鲜白。",
        "阿难供养舍利后问佛：「他临终诸根喜悦、肤色光泽，会生到哪里？后世怎样？」",
        "佛告诉阿难：「在适当的时候闻法，有六种利益。哪六种？",
        f"「若比丘病前还未断{FIVE_LOWER_MOD}，病起受苦、生命微弱，得听大师说法，听后断五下分结——"
        "这叫大师说法的利益。",
        "「若没得到大师，却得到其他多闻梵行者说法，听后断五下分结——这叫教授听法的利益。",
        "「若两样都听不到，却对以前听过的法独自静思观察，因而断五下分结——这叫思惟先闻法的利益。",
        "「其次，若病前已断五下分结，但还没得到无上爱尽、诸漏不起、心善解脱；"
        "病时听大师说法，便得无上爱尽解脱——这叫大师说法的利益。",
        "「若得不到大师，却得到其他梵行者说法，同样得无上爱尽解脱——这叫教授闻法的利益。",
        "「若两样都听不到，却思惟先闻之法，得无上爱尽解脱——这叫思惟先闻法的利益。",
        "「叵求那原先未断五下分结，亲自从大师闻法，便断了五下分结；"
        "所以诸根喜悦。我记别他得阿那含。」",
        CLOSE_AN_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN6.56；"
        "临终闻法六益：未断五下分结者三路（佛／弟子／自思）得阿那含；"
        "已断五下分结未漏尽者三路得阿罗汉；记叵求那阿那含。"
    ),
}

# --- SA 1024 阿湿波誓（SN22.88 Assaji）--------------------------------------
SUTTAS["SA_1024"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者阿湿波誓住东园鹿母讲堂，身遭重病，极生苦患。佛往问讯，说三受，乃至「转增无损」。",
        "佛告：「汝莫变悔！」白言：「我实有变悔。」"
        "「汝得无破戒耶？」白言：「不破戒。」「若不破戒，何为变悔？」",
        "白言：「我先未病时，多修身息乐正受；今日不得入彼三昧，恐退失三昧。」",
        "佛告：「我问汝：汝见色是我、异我、相在不？受、想、行、识是我、异我、相在不？」"
        "白言：「不也，世尊。」",
        "「汝既不见五阴是我、异我、相在，何故变悔？」白言：「不正思惟故。」",
        "佛告：「若沙门、婆罗门三昧坚固平等，不得入彼三昧，不应念『我于三昧退减』。"
        "圣弟子不见色受想行识是我、异我、相在，但当觉知：贪瞋痴永尽无余；"
        "尽已，一切漏尽，无漏心解脱、慧解脱，现法自知作证："
        "『我生已尽，梵行已立，所作已作，自知不受后有。』」",
        "说是法时，阿湿波誓不起诸漏，心得解脱；欢喜踊悦，身病即除。"
        "佛令彼欢喜随喜已，从坐起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时尊者阿湿波誓住在东园鹿母讲堂，身患重病，苦痛很重。佛前去问讯，说三种受，乃至「只增不减」。",
        "佛说：「你不要变悔！」答：「我确实有变悔。」"
        "「你该不会破戒了吧？」答：「没有破戒。」「既不破戒，为什么变悔？」",
        "答：「我病前常常修习身息安乐的正受；今天不能再入那种三昧，怕是退失了三昧。」",
        "佛说：「我问你：你看见色是我、异于我、或相在吗？受、想、行、识是我、异于我、或相在吗？」"
        "答：「不是的，世尊。」",
        "「你既不见五阴是我、异我、相在，为什么还变悔？」答：「因为不正思惟。」",
        "佛说：「若沙门、婆罗门三昧坚固平等，一时不能入那三昧，也不应想『我从三昧退减』。"
        "圣弟子不见色受想行识是我、异我、相在，只需觉知：贪瞋痴永久灭尽无余；"
        "灭尽之后，一切漏尽，无漏心解脱、慧解脱，现法自知作证："
        "『我生已尽，梵行已立，所作已作，自知不受后有。』」",
        "说这法时，阿湿波誓诸漏不起，心得解脱；欢喜踊跃，身病随即除去。"
        "佛让他欢喜随喜后，从座起离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN22.88；"
        "变悔非破戒，乃恐失三昧；以五阴非我正观，不应以不得定谓退；"
        "贪瞋痴尽则漏尽；说已解脱，病除。汉处祇园／东园，巴利作王舍／迦叶精舍——从汉框、取巴利义。"
    ),
}

# --- SA 1025 疾病（SN35.74）-------------------------------------------------
SUTTAS["SA_1025"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有年少新学比丘，出家未久，少知识，独住边聚落客僧房，疾病困笃。"
        "众比丘白佛，请往哀愍。世尊默许，日晡往视。",
        "病比丘遥见，扶床欲起。佛告：「息卧勿起。」问苦患，乃至「但增不损」。",
        "「汝得无变悔耶？」白言：「实有。」「得无犯戒耶？」白言：「不犯。」"
        "「若不犯戒，何为变悔？」"
        "白言：「我年幼出家未久，过人法胜妙知見未得；念命终当生何处，故变悔。」",
        "佛告：「有眼故有眼识；有眼识故有眼触；眼触缘生内受——苦、乐、不苦不乐。"
        "耳鼻舌身意亦如是。若无眼则无眼识、无眼触、无彼受；余根亦尔。"
        "是故当善思惟如是法，得善命终，后世亦善。」",
        "佛为种种说法，示教照喜已去。彼寻命终；临终诸根喜悦，颜貌清净，肤色鲜白。",
        "众比丘问生处。佛告：「彼是真宝物，闻法解了，于法无畏，得般涅槃；当供养舍利。」"
        "即为受第一记。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位年少新学比丘，出家不久，认识的人少，独自住在边远聚落的客僧房，病重危急。"
        "众比丘禀告佛，请佛前去哀愍。世尊默然答应，傍晚前去看他。",
        "病比丘远远看见，扶着床想起来。佛说：「躺着别起。」问苦痛，乃至「只增不减」。",
        "「你该不会变悔吧？」答：「确实有。」「该不会犯戒吧？」答：「没有犯。」"
        "「既不犯戒，为什么变悔？」"
        "答：「我年纪轻、出家不久，过人的胜妙知見还没有；想到命终会生到哪里，所以变悔。」",
        "佛说：「有眼才有眼识；有眼识才有眼触；眼触为缘生起内受——苦、乐、不苦不乐。"
        "耳鼻舌身意也是这样。若没有眼，就没有眼识、眼触和那些受；其余诸根也一样。"
        "所以应当好好思惟这样的法，才能善命终，后世也善。」",
        "佛为他种种说法，开示劝勉令欢喜后离去。他不久命终；临终诸根喜悦，面容清净，肤色鲜白。",
        "众比丘问他生到何处。佛说：「他是真正的宝物，听法清楚了解，于法无畏，已得般涅槃；应当供养舍利。」"
        "随即为他授第一记。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN35.74；"
        "新学病比丘恐不知生处；以六根触受缘起开示；命终诸根净，记般涅槃。"
    ),
}

# --- SA 1026 疾病（SN35.75）-------------------------------------------------
SUTTAS["SA_1026"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有年少新学病比丘，因缘如上。佛往问讯已，告言：",
        "「谛听，善思，当为汝说。若比丘作是念：『我此识身及外境界一切相，"
        "无有我、我所见、我慢系着使；心解脱、慧解脱，现法自知作证具足住。』"
        "于此识身及外境界一切相，亦复如是无我、我所、我慢系着使，"
        "及彼心解脱、慧解脱，现法自知作证具足住——",
        "是名比丘断爱欲，转诸结，止慢无间等，究竟苦边。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位年少新学的病比丘，因缘如上。佛前去问讯后告诉他：",
        "「仔细听，好好想，我为你说。若比丘这样念：『我这个有识之身以及外境一切相，"
        "都没有我、我所见、我慢系着的烦恼；心解脱、慧解脱，现法自知作证，具足而住。』"
        "对这个有识之身以及外境一切相，也同样没有我、我所、我慢系着，"
        "并且心解脱、慧解脱，现法自知作证，具足而住——",
        "这就叫做比丘断除爱欲，转开诸结，止息慢的无间等，究竟苦边。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN35.75；"
        "汉本 peyyāla，据平行补：识身与外相无我我所我慢，心慧二解脱，究竟苦边。"
    ),
}

# --- SA 1027 病比丘（无巴利专经）---------------------------------------------
SUTTAS["SA_1027"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有病比丘，因缘如上。佛问：「汝不自犯戒耶？」",
        "白言：「我不以持净戒故，于世尊所修梵行。」",
        "「汝以何法于我所修梵行？」"
        "白言：「为离贪欲、瞋恚、愚癡故，于世尊所修梵行。」",
        "佛告：「如是。比丘！贪欲缠故不得离欲；无明缠故慧不清净。"
        "是故于欲离欲得心解脱，离无明故得慧解脱。"
        "若比丘于欲离欲心解脱身作证，离无明慧解脱——"
        "是名断诸爱欲，转结缚，止慢无间等，究竟苦边。"
        "于此法当善思惟。」如上广说，乃至受第一记。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位病比丘，因缘如上。佛问：「你该不会自己犯戒了吧？」",
        "答：「我并不是为了持净戒，才在世尊处修梵行。」",
        "「那你为了什么法在我这里修梵行？」"
        "答：「为了离贪欲、瞋恚、愚癡，才在世尊处修梵行。」",
        "佛说：「正是如此。比丘！被贪欲缠住就不能离欲；被无明缠住慧就不清净。"
        "所以要在欲上离欲而得心解脱，离开无明而得慧解脱。"
        "若比丘在欲上离欲、心解脱并亲自作证，又离无明而慧解脱——"
        "这就叫做断诸爱欲，转开结缚，止息慢的无间等，究竟苦边。"
        "应当好好思惟这样的法。」如上广说，乃至授第一记。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：无 SC 巴利专经；近病比丘闻法系列。"
        "梵行目的为离贪瞋痴；离欲心解脱、离无明慧解脱，究竟苦边。"
    ),
}

# --- SA 1028 疾病（SN36.7）-------------------------------------------------
SUTTAS["SA_1028"] = {
    "lit": [
        OPEN_JET_LIT,
        "时众多比丘集伽梨隶讲堂，多有疾病。世尊晡时从禅觉，往彼敷座，告诸比丘：",
        "「当正念正智以待时，是则随顺我教。",
        "云何正念？内身身观念处，精勤正念正智，调伏世间贪忧；"
        "外身、内外身，受、心、法——内、外、内外——亦复如是，是名正念。",
        "云何正智？来去、瞻视、屈伸、持衣钵、行住坐卧眠觉、语默，皆正知而住，是名正智。",
        "正念正智住者，若起乐受，当知有因缘——缘身："
        "『此身无常、有为、心缘生；乐受亦无常、有为、心缘生。』"
        "观身及乐受无常、生灭、离欲、灭尽、舍；观已，于彼贪使永不复使。",
        "若起苦受，缘身亦如是观；观已，于彼瞋使永不复使。",
        "若起不苦不乐受，缘身亦如是观；观已，于彼无明使永不复使。",
        "多闻圣弟子如是观，于色受想行识厌离，离欲，解脱，解脱知見："
        "『我生已尽，梵行已立，所作已作，自知不受后有。』」",
        "世尊说偈：「乐觉时不知，贪使之所使，不见于出离；"
        "苦受时不知，瞋使之所使，不见出离道；"
        "舍受亦不知，终不度彼岸。"
        "比丘勤正智，于一切受悉知；知受已漏尽，依慧而命终，涅槃不堕数。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时许多比丘聚集在伽梨隶讲堂，很多人生病。世尊傍晚从禅定起来，到那里敷座，告诉比丘们：",
        "「应当正念正智地等待时节，这才是随顺我的教导。",
        "什么是正念？在内身观察身，精勤、正念正智，调伏世间的贪与忧；"
        "外身、内外身，以及受、心、法——内、外、内外——也是这样，这叫正念。",
        "什么是正智？往来、看视、屈伸、持衣钵、行住坐卧眠醒、说话沉默，都正知而住，这叫正智。",
        "正念正智而住的人，若生起乐受，应当知道有因缘——缘于身："
        "『这个身无常、有为、由心为缘而生；乐受也无常、有为、由心为缘而生。』"
        "观察身与乐受的无常、生灭、离欲、灭尽、舍离；观察之后，对它们的贪使永远不再驱使。",
        "若生起苦受，也缘身这样观察；观察之后，瞋使永远不再驱使。",
        "若生起不苦不乐受，也缘身这样观察；观察之后，无明使永远不再驱使。",
        "多闻圣弟子这样观察，对色受想行识厌离，离欲，解脱，有解脱的知見："
        "『我生已尽，梵行已立，所作已作，自知不受后有。』」",
        "世尊说偈：「觉知乐受时若不知，就被贪使驱使，看不见出离；"
        "觉知苦受时若不知，就被瞋使驱使，看不见出离道；"
        "舍受若也不知，终究不能度彼岸。"
        "比丘精勤正智，对一切受都能了知；了知诸受后漏尽，依慧命终，涅槃不堕于数。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN36.7；"
        "病堂教正念正智待时；三受缘身而观无常等，断贪瞋无明使；"
        "厌五阴得解脱。汉在祇园／伽梨隶，巴利作毗舍离／重阁讲堂——从汉框。"
    ),
}

# --- SA 1029 疾病（SN36.8）-------------------------------------------------
SUTTAS["SA_1029"] = {
    "lit": [
        OPEN_JET_LIT,
        "时众多比丘集伽梨隶讲堂，多有疾病。世尊往教正念正智待时，观三受，如上说。",
        "差别者：乐、苦、不苦不乐受缘于触而生；观触及受无常乃至舍，"
        "则贪、瞋、无明使永不复使。"
        "圣弟子如是观者，于色解脱，于受想行识解脱；我说彼解脱生老病死。",
        "世尊说偈：「多闻有慧者，非不觉诸受；苦乐分别了，当知凡夫有升沉。"
        "于乐不染著，于苦不倾动；知受不再生，依于贪恚觉；断已心解脱。"
        "系念正向待终时，比丘精勤正智不动；知一切受已，现法尽诸漏；"
        "依慧而命终，涅槃不堕数。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时许多比丘聚集在伽梨隶讲堂，很多人生病。世尊前去教他们正念正智等待时节，观察三受，如上所说。",
        "不同的是：乐、苦、不苦不乐受都是缘于触而生；观察触与受的无常乃至舍离，"
        "贪、瞋、无明使就永远不再驱使。"
        "圣弟子这样观察，于色得解脱，于受想行识得解脱；我说他们解脱了生老病死。",
        "世尊说偈：「多闻有智慧的人，并非不觉知诸受；对苦乐分辨明了，当知凡夫有升有沉。"
        "于乐不染着，于苦不动摇；知道受不再生起，那是依于贪恚的觉；断除之后心善解脱。"
        "系念端正向往、等待终时，比丘精勤正智不动摇；了知一切受，现法尽诸漏；"
        "依慧命终，涅槃不堕于数。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN36.8；"
        "与 1028 同型，条件作触（phassa）非身；观成则解脱生老病死。"
        "汉本删省，据平行补触缘与解脱句。"
    ),
}

# --- SA 1030 给孤独（无巴利专经）---------------------------------------------
SUTTAS["SA_1030"] = {
    "lit": [
        OPEN_JET_LIT,
        "时给孤独长者得病，身极苦痛。世尊晨朝着衣持钵，入城次第乞食，至其舍。",
        "长者遥见，冯床欲起。佛告：「勿起，增其苦患。」即坐，"
        + THREE_VED_ASK_LIT,
        "佛告：「当如是学：于佛不坏净，于法、僧不坏净，圣戒成就。」",
        "长者白言：「如世尊说四不坏净，我已有之：我于佛、法、僧不坏净，圣戒成就。」",
        "佛言：「善哉！」即记长者得阿那含果。",
        "长者请佛食，世尊默许。即办种种净美饮食供养。世尊食已，为说种种法，示教照喜，从坐起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时给孤独长者生病，身体极度苦痛。世尊早晨着衣持钵，进城依次乞食，来到他的家。",
        "长者远远看见，扶着床想起来。佛说：「别起来，免得加重苦痛。」随即坐下，"
        + THREE_VED_ASK_MOD,
        "佛说：「应当这样学：对佛成就不坏净，对法、僧成就不坏净，成就圣戒。」",
        "长者说：「正如世尊说的四不坏净，我已经有了：我对佛、法、僧有不坏净，也成就圣戒。」",
        "佛说：「很好！」随即记别长者得阿那含果。",
        "长者请佛用餐，世尊默然答应。随即备办种种清净美味饮食供养。世尊吃完，为他种种说法，开示劝勉令欢喜，从座起离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：无 SC 巴利专经；近给孤独病中问讯系列。"
        "四不坏净（佛法人戒）已具，记阿那含——从汉本，不臆改成果位。"
    ),
}

# ---------------------------------------------------------------------------
# Confidence / reconstruction / build GOLD
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_1011": "high",
    "SA_1012": "medium",
    "SA_1013": "high",
    "SA_1014": "high",
    "SA_1015": "high",
    "SA_1016": "high",
    "SA_1017": "high",
    "SA_1018": "high",
    "SA_1019": "high",
    "SA_1020": "high",
    "SA_1021": "high",
    "SA_1022": "high",
    "SA_1023": "high",
    "SA_1024": "high",
    "SA_1025": "high",
    "SA_1026": "high",
    "SA_1027": "medium",
    "SA_1028": "high",
    "SA_1029": "high",
    "SA_1030": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1011": "汉偈死／苦／爱／老与 SN1.68 错位（衰／死／爱／法）；据巴利重排。",
    "SA_1018": "汉末句『业甚可畏』；据 SN1.55 作 dukkha 校正为苦。",
    "SA_1021": "汉『欲／造作』；据 SN1.60 chanda＝韵律、kavi＝诗人校正。",
    "SA_1026": "汉 peyyāla『如上说』；据 SN35.75 补识身外相无我及二解脱句。",
    "SA_1029": "汉删省；据 SN36.8 补触缘三受及解脱生老病死。",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

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

assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
assert set(RECONSTRUCTED) <= set(GOLD)
assert set(GOLD) == {f"SA_{i}" for i in batch_range}


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

    _goldish = {"gold", "gold_reconstructed"}
    by_lookup = {r["id"]: r for r in records}

    # Neighbors: assert untouched
    guard_ids = {"SA_1010", "SA_1031"}
    # Also guard any already-gold outside batch that parallel agents might touch
    for i in list(range(991, 1011)) + list(range(1031, 1051)):
        guard_ids.add(f"SA_{i}")

    boundary_before = {
        gid: _snap(by_lookup[gid]) for gid in guard_ids if gid in by_lookup
    }

    report: list[dict] = []
    merged: list[dict] = []
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

    by_merged = {r["id"]: r for r in merged}
    for gid, before in boundary_before.items():
        after = _snap(by_merged[gid])
        assert before == after, f"{gid} must remain untouched"

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1011-1030.json").write_text(
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

    continuous = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in _goldish for i in batch_range
    )
    untouched_neighbors = all(
        f"SA_{i}" not in GOLD for i in list(range(991, 1011)) + list(range(1031, 1051))
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1011–SA_1030 only)")
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
    print(f"continuous_gold_SA_1011–1030={continuous}")
    print(f"neighbors_untouched={untouched_neighbors}")
    print(f"SA_1010_untouched={('SA_1010' in boundary_before)}")
    print(f"SA_1031_untouched={('SA_1031' in boundary_before)}")
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
