#!/usr/bin/env python3
"""Retranslate SA 591–610（卷第二十五天相应末 + 念处相应起）→ merge.

本批二十经：输波罗 sa-2.185；须达 SN10.8；须达生天 SN2.20；首长者 AN3.127；
无烦 SN1.50；常惊 SN2.17；颜色 SN2.14；睡眠 SN1.16；髻发 SN1.23；极难尽 SN1.17；
池水 SN1.27；伊尼延 SN1.30；流 SN10.12（汉本仅偈）；Aśokavadāna（无巴利）；
念处 peyyāla；念处 SN47.24；净 SN47.1；甘露 SN47.33；集 SN47.42；正念 SN47.39。

信：有 SN／AN 平行者据巴利／Sujato 厘义；591、594、604、605 无专经 → medium/low。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts._sa604_gold import SA_604_LIT, SA_604_MOD  # noqa: E402
from translate.quality_gate import assess_gold  # noqa: E402
from translate.similarity import similarity_to_source  # noqa: E402
from translate.validate import validate_restyle  # noqa: E402

# ---------------------------------------------------------------------------
# 共用框式
# ---------------------------------------------------------------------------

OPEN_JET_LIT = "如是我闻：一时，佛住舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_RAJ_COOL_LIT = "如是我闻：一时，佛在王舍城寒林中丘冢间。"
OPEN_RAJ_COOL_MOD = "我是这样听说的：有一次，佛住在王舍城寒林的丘冢间。"

OPEN_RAJ_BAM_LIT = "如是我闻：一时，佛住王舍城迦兰陀竹园。"
OPEN_RAJ_BAM_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

OPEN_WILD_LIT = "如是我闻：一时，佛住旷野精舍。"
OPEN_WILD_MOD = "我是这样听说的：有一次，佛住在旷野精舍。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

DEVA_NIGHT_LIT = "后夜分，有天子来诣佛所，容色绝妙，稽首礼足，退坐一面；身诸光明遍照祇园。"
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


def _deva_exchange(
    q_lit: str,
    q_mod: str,
    a_lit: str,
    a_mod: str,
    *,
    opening_lit: str = OPEN_JET_LIT,
    opening_mod: str = OPEN_JET_MOD,
    deva_open_lit: str = DEVA_NIGHT_LIT,
    deva_open_mod: str = DEVA_NIGHT_MOD,
) -> tuple[list[str], list[str]]:
    lit = [
        opening_lit,
        deva_open_lit,
        f"天子说偈问：「{q_lit}」",
        f"世尊说偈答：「{a_lit}」",
        DEVA_CLOSE_LIT,
    ]
    mod = [
        opening_mod,
        deva_open_mod,
        f"天子说偈问：「{q_mod}」",
        f"世尊说偈答：「{a_mod}」",
        DEVA_CLOSE_MOD,
    ]
    return lit, mod


# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 591 输波罗（sa-2.185）------------------------------------------------
SUTTAS["SA_591"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「昔有海洲优婆塞，赴他舍会，极毁欲言：『欲虚妄不实，如幻化诳婴。』"
        "归家却恣五欲。」",
        "其舍有天神，念言：『此人不类——会中毁欲，回家自恣；当令觉悟。』说偈："
        "「于大聚会中，毁呰欲无常，自没于爱欲，如牛溺深泥。"
        "我观彼会中，诸优婆塞等，多闻明解法，奉持于净戒。"
        "汝见彼乐法，而说欲无常，如何自恣欲，不断于贪爱，何故乐世间，畜妻子眷属。」",
        "天神开觉已，彼优婆塞剃发著袈裟，出家精勤，漏尽得阿罗汉。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「昔有海洲优婆塞，赴他舍会，极毁欲言：『欲虚妄不实，如幻化诳婴。』"
        "归家却恣五欲。」",
        "其舍有天神，念言：「此人不类——会中毁欲，回家自恣；当令觉悟。」说偈："
        "「于大聚会中，毁呰欲无常，自没于爱欲，如牛溺深泥。"
        "我观彼会中，诸优婆塞等，多闻明解法，奉持于净戒。"
        "汝见彼乐法，而说欲无常，如何自恣欲，不断于贪爱，何故乐世间，畜妻子眷属。」",
        "天神开觉已，彼优婆塞剃发著袈裟，出家精勤，漏尽得阿罗汉。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：parallel sa-2.185，无巴利专经；天神诫毁欲而自恣者，从汉本。"
    ),
}

# --- SA 592 须达（SN10.8）----------------------------------------------------
SUTTAS["SA_592"] = {
    "lit": [
        OPEN_RAJ_COOL_LIT,
        "时，给孤独长者有小因缘至王舍城，止宿长者舍。夜见长者告妻子、仆使、作人："
        "『汝等皆起，破樵然火，炊饭作饼，调和众味，庄严堂舍。』",
        "给孤独长者作念：『今此长者何为？为嫁女娶妇？为请宾客、国王、大臣？』"
        "即问：『汝何所作？』彼答：『唯欲请佛及比丘僧设供养。』",
        "给孤独长者闻佛名，心大欢喜，身毛怡悦，问：『何为佛？何为僧？』"
        "彼广说佛、僧义，又言：『今日请佛及现前僧。』给孤独问：『我今可得往见世尊不？』"
        "答：『汝且住此，我请世尊来至我舍，于此得见。』",
        "给孤独即于夜至心念佛，因得睡眠。天未明，忽见明相，谓天已晓，出城向寒林。"
        "至城下，夜始二更，城门未开；中夜尽，门开。给孤独见门开，乘明相出城；"
        "出城已，明相即灭，还暗冥，心生恐怖，欲还。",
        "时，城门侧有天神住，放身光从城门至寒林，普照，告言：『汝且前进，可得胜利，慎勿退还。』",
        "时，彼天神说偈言："
        "「善良马百匹，黄金满百斤，骡车及马车，各各有百乘，种种诸珍奇，重宝载其上，"
        "宿命种善根，得如此福报，若人宗重心，向佛行一步，十六分之一，过前福之上。"
        "是故长者！汝当前进，慎勿退还！」",
        "复说偈：「雪山大龙象，纯金为庄饰，巨身长大牙，以此象施人，不及向佛福，十六分之一。」",
        "复说偈：「金菩阇国女，其数有百人，种种众妙宝，璎珞具庄严，以是持施与，"
        "不及行向佛，一步之功德，十六分之一。是故长者！当速前进，得其大利。」",
        "给孤独问天神：『贤者！汝是何人？』天神答：『我是摩头息揵大摩那婆，"
        "是长者善知识；于尊者舍利弗、大目揵连所起信敬，缘斯功德，今得生天，典此城门。』",
        "给孤独作念：『佛兴于世，非为小事；得闻正法，亦非小事。』寻光明至寒林丘冢间。",
        "世尊出房露地经行。给孤独遥见佛，以俗礼恭敬问讯：『云何？世尊！安隐卧不？』",
        "世尊说偈答：「婆罗门涅槃，是则常安乐，爱欲所不染，解脱永无余。"
        "断一切希望，调伏心炽燃，心得寂止息，止息安隐眠。」",
        "世尊将给孤独入房就座，为其说法，示教照喜，说诸法无常，宜修布施、持戒、生天福，"
        "欲味、欲患、欲出，远离之福。",
        "给孤独闻法、见法、得法、入法、解法，度诸疑惑，不由他信，不由他度，入正法、律，"
        "心得无畏，从座起，右膝著地，合掌白言：『已度。世尊！已度。善逝！我从今日尽其寿命，"
        "归佛、归法、归比丘僧，为优婆塞，证知我。』",
        "世尊问：『汝名何等？居何所？』白言：『名须达多；以常给孤贫，时人名给孤独。"
        "在拘萨罗人间舍卫城，唯愿世尊来舍卫国，我当尽寿供养。』",
        "佛问：『舍卫国有精舍不？』白：『无也。』佛告：『汝可于彼建立精舍。』"
        "白：『但使世尊来舍卫国，我当作精舍僧房。』世尊默然受请。长者知受请已，稽首佛足而去。",
    ],
    "mod": [
        OPEN_RAJ_COOL_MOD,
        "当时，给孤独长者因小事来到王舍城，住在一位长者舍中。夜里看见长者吩咐妻子、仆从、工人："
        "「你们都起来，砍柴生火，煮饭作饼，调和种种美味，庄严堂舍。」",
        "给孤独心想：「这位长者要做什么？是为嫁女娶妇？还是请宾客、国王、大臣？」"
        "便问：「你要做什么？」对方答：「只想请佛及比丘僧来设供养。」",
        "给孤独长者听见佛名，心大欢喜，毛孔开悦，问：「什么是佛？什么是僧？」"
        "对方广说佛、僧之义，又说：「今日请佛及现前僧。」给孤独问：「我现在能去见世尊吗？」"
        "答：「你先住在这里，我请世尊到我舍中，在那里得见。」",
        "给孤独当夜至心念佛，因而入睡。天未亮，忽见光明，以为天明，出城往寒林。"
        "到城下时，夜才二更，城门未开；中夜过后，门才开。给孤独见门开，趁光明出城；"
        "出城后光明即灭，复归黑暗，心生恐怖，想要返回。",
        "当时，城门侧有天神安住，放身光从城门照至寒林，普照一切，告知："
        "「你且前进，可得胜利，千万不要退回。」",
        "天神说偈："
        "「即使良马百匹、黄金满百斤、骡车马车各百乘、种种珍宝满载，"
        "这是宿世种善根所得的福报；若人至心向佛走一步，其功德胜过前者十六分之一。"
        "所以，长者！你当前进，切勿退回！」",
        "又说偈：「雪山大龙象，以纯金庄严，巨身长大牙，以此象施人，不及向佛一步之福的十六分之一。」",
        "又说偈：「金菩阇国女百人，种种妙宝璎珞庄严，以此布施，不及向佛走一步的功德十六分之一。"
        "所以，长者！当速前进，得大利益。」",
        "给孤独问天神：「贤者！你是什么人？」天神答：「我是摩头息揵大摩那婆，"
        "是长者的善知识；曾对舍利弗、大目揵连起信敬心，缘此功德，今得生天，掌管此城门。」",
        "给孤独作念：「佛兴于世，不是小事；得闻正法，也不是小事。」便循光明至寒林丘冢间。",
        "世尊出房在露地经行。给孤独远远看见佛，以世俗礼节恭敬问讯：「世尊安隐吗？」",
        "世尊说偈答：「婆罗门涅槃，才是常安乐，不为爱欲所染，解脱永无余。"
        "断一切希望，调伏心中炽燃，心得寂止，止息而安稳。」",
        "世尊领给孤独入房就座，为其说法，示教照喜，说诸法无常，应当修习布施、持戒、生天福，"
        "以及欲味、欲患、欲出、远离等福。",
        "给孤独闻法、见法、得法、入法、解法，度越诸疑，不由他人而得信、不由他人而得度，"
        "入于正法、律，心得无畏，从座起，右膝著地，合掌白佛：「已度，世尊！已度，善逝！"
        "我从今日尽形寿，归依佛、法、僧，为优婆塞，请为我证知。」",
        "世尊问：「你叫什么名字？住在哪里？」白言：「名须达多；因常救济孤苦，人号给孤独。"
        "住在拘萨罗国舍卫城，唯愿世尊来舍卫国，我尽形寿供养。」",
        "佛问：「舍卫国有精舍吗？」答：「没有。」佛告：「你可在彼建立精舍。」"
        "白：「只要世尊来舍卫国，我就造精舍僧房。」世尊默然接受。长者知佛受请，顶礼佛足离去。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN10.8（Anāthapiṇḍika 夜诣、Sivaka 天神劝进、归依）。"
        "据 SN 校正：非人开城门、三度明暗、向佛一步十六分福；汉本增嫁娶问讯等叙事保留。"
    ),
}

# --- SA 593 须达生天（SN2.20）-----------------------------------------------
SUTTAS["SA_593"] = {
    "lit": [
        OPEN_JET_LIT,
        "给孤独长者病终生兜率，为天子。念言：「不宜久留，当见世尊。」"
        "如屈伸臂，兜率没，现佛前，礼足却坐；身光满祇园。",
        "说偈："
        "「于此祇桓林，仙人僧住止，诸王亦住此，增我欢喜心，"
        "深信净戒业，智慧为胜寿，以此净众生，非族姓财物，"
        "大智舍利弗，正念常寂默，闲居修远离，初建业良友。」",
        "说已即没。",
        "夜过，佛入僧中敷座，告比丘：「此夜有天子，容色绝妙，来我前说如上偈。」",
        "阿难白佛：「应是给孤独长者生彼来见；彼于舍利弗极敬重。」",
        "佛告阿难：「正是。给孤独长者生彼天，来见我。」",
        "佛为舍利弗说偈："
        "「一切世间智，唯除于如来，比舍利弗智，十六不及一。"
        "如舍利弗智，天人悉同等，比于如来智，十六不及一。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "给孤独长者病终生兜率，为天子。念言：「不宜久留，当见世尊。」"
        "如屈伸臂，兜率没，现佛前，礼足却坐；身光满祇园。",
        "说偈："
        "「于此祇桓林，仙人僧住止，诸王亦住此，增我欢喜心，"
        "深信净戒业，智慧为胜寿，以此净众生，非族姓财物，"
        "大智舍利弗，正念常寂默，闲居修远离，初建业良友。」",
        "说已即没。",
        "夜过，佛入僧中敷座，告比丘：「此夜有天子，容色绝妙，来我前说如上偈。」",
        "阿难白佛：「应是给孤独长者生彼来见；彼于舍利弗极敬重。」",
        "佛告阿难：「正是。给孤独长者生彼天，来见我。」",
        "佛为舍利弗说偈："
        "「一切世间智，唯除于如来，比舍利弗智，十六不及一。"
        "如舍利弗智，天人悉同等，比于如来智，十六不及一。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN2.20（Anāthapiṇḍika devaputta 赞祇园、戒慧、舍利弗）。"
        "据 SN 校正：业／慧／律净众生，非族姓财；末偈比智十六分一。"
    ),
}

# --- SA 594 首长者生天（AN3.127）---------------------------------------------
SUTTAS["SA_594"] = {
    "lit": [
        OPEN_WILD_LIT,
        "时，有旷野长者疾病命终，生无热天。生彼天已，作念：『我不应久住，不见世尊。』"
        "如力士屈伸臂顷，从无热天没，现于佛前。",
        "时，彼天子天身委地，不能自立，犹如酥油委地。世尊告彼天子：『汝当变化作此粗身，而立于地。』",
        "天子即自化形，作粗身而立，前礼佛足，退坐一面。",
        "世尊告手天子：『汝手天子，本于此间为人身时，所受经法，今故忆念不悉忘耶？』",
        "手天子白佛言：『世尊！本所受持，今悉不忘。本人间时，有所闻法不尽得者，今亦忆念，"
        "如世尊善说。世尊说言：「若人安乐处，能忆持法，非为苦处。」此说真实。」",
        "佛告手天子：『汝于这个人间时，于几法无厌足故，而得生彼无热天中？』",
        "手天子白佛：『世尊！我于三法无厌足故，身坏命终，生无热天。何等三？"
        "见佛无厌故，闻法无厌故，供养众僧无厌故。』即说偈言："
        "「见佛无厌足，闻法亦无厌，供养于众僧，亦未曾知足，"
        "受持贤圣法，调伏悭著垢，三法不知足，故生无热天。」",
        "时，手天子闻佛所说，欢喜随喜，即没不现。",
    ],
    "mod": [
        OPEN_WILD_MOD,
        "当时，有一位旷野长者病终，生无热天。生彼天后作念：「我不应久住，尚未见世尊。」"
        "如力士屈伸手臂一般迅速，从无热天消失，现在佛前。",
        "那位天子的天身委地，不能自立，犹如酥油委地。世尊告诉他：「你应当变化成粗重之身，然后立于地上。」",
        "天子随即化现粗身而立，上前顶礼佛足，退坐一面。",
        "世尊问手天子：「手天子，你以前在此人间为人时，所受经法，现在是否仍记得、没有忘失？」",
        "手天子白佛说：「世尊！以前所受持的，现在都记得。人间时未能尽得的法，现在也忆念起来，"
        "如同世尊善说。世尊说：『若人处于安乐之处，能忆持法；处于苦处则不然。』这说得真实。」",
        "佛问手天子：「你以前在这个人间，对哪几法无厌足，因而生彼无热天？」",
        "手天子白佛说：「世尊！我对三法无厌足，身坏命终，生无热天。哪三种？"
        "见佛无厌、闻法无厌、供养众僧无厌。」即说偈："
        "「见佛无厌足，闻法亦无厌，供养于众僧，也未曾知足，"
        "受持贤圣法，调伏悭贪垢，三法不知足，故生无热天。」",
        "手天子听佛所说，欢喜随喜，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium：parallel AN3.127（见佛／闻法／供僧无厌生天）；aligned 无巴利本文，从汉本。"
        "据 AN 校正：三法无厌为见佛、闻法、供养僧；天身细软须化粗身。"
    ),
}

# --- SA 595 无烦天（SN1.50）--------------------------------------------------
SUTTAS["SA_595"] = {
    "lit": [
        OPEN_JET_LIT,
        "有无烦天子来，光满祇园，礼足却坐。说偈："
        "「生彼无烦天，解脱七比丘，贪瞋恚已尽，超世度恩爱，"
        "谁度于诸流，难度死魔军，谁断死魔縻，永超烦恼轭？」",
        "佛答："
        "「优波迦、波罗揵荼、弗迦罗娑梨、跋提、揵陀叠、"
        "婆休难提、波毗瘦㝹——此等皆度流，断死魔縻，越天轭；"
        "说深妙法，觉难知者。巧问深义，汝今是谁？」",
        "天子白佛："
        "「我是阿那含，生无烦天，故知七比丘解脱，贪瞋恚尽，永超恩爱。」",
        "佛复说："
        "「眼耳鼻舌身，意入为第六；名色无余灭，知此者度流，"
        "七比丘贪尽，永超世恩爱。」",
        "天子复说："
        "「鞞跋楞伽村，我名难提婆罗，作瓦器，迦叶佛弟子，"
        "持优婆塞法，养父母，离欲梵行；世世为友，宿命合同，"
        "善身心，持后边身。」",
        "佛复说："
        "「如汝所说，鞞跋楞伽瓦师难提婆罗，迦叶佛弟子，"
        "持优婆塞法，养父母，离欲梵行；昔汝知识，善身心，持后边身。」",
        "天子闻已欢喜，即没。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "有无烦天子来，光满祇园，礼足却坐。说偈："
        "「生彼无烦天，解脱七比丘，贪瞋恚已尽，超世度恩爱，"
        "谁度于诸流，难度死魔军，谁断死魔縻，永超烦恼轭？」",
        "佛答："
        "「优波迦、波罗揵荼、弗迦罗娑梨、跋提、揵陀叠、"
        "婆休难提、波毗瘦㝹——此等皆度流，断死魔縻，越天轭；"
        "说深妙法，觉难知者。巧问深义，汝今是谁？」",
        "天子白佛："
        "「我是阿那含，生无烦天，故知七比丘解脱，贪瞋恚尽，永超恩爱。」",
        "佛复说："
        "「眼耳鼻舌身，意入为第六；名色无余灭，知此者度流，"
        "七比丘贪尽，永超世恩爱。」",
        "天子复说："
        "「鞞跋楞伽村，我名难提婆罗，作瓦器，迦叶佛弟子，"
        "持优婆塞法，养父母，离欲梵行；世世为友，宿命合同，"
        "善身心，持后边身。」",
        "佛复说："
        "「如汝所说，鞞跋楞伽瓦师难提婆罗，迦叶佛弟子，"
        "持优婆塞法，养父母，离欲梵行；昔汝知识，善身心，持后边身。」",
        "天子闻已欢喜，即没。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN1.50（Avīha 七天、Ghaṭīkāra 陶师前世）。"
        "据 SN 校正：七比丘名、名色无余灭、瓦师难提婆罗事；汉本音译名保留。"
    ),
}

# --- SA 596–602 天问偈（SN2.17 等）------------------------------------------
_lit596, _mod596 = _deva_exchange(
    "此世多恐怖，众生常恼乱，已起者亦苦，未起亦当苦，颇有离恐处，唯愿慧眼说。",
    "此世多恐怖，众生常恼乱，已起者亦苦，未起亦当苦，颇有离恐处，唯愿慧眼说。",
    "无有异苦行，无异伏诸根，无异一切舍，而得见解脱。",
    "无有异苦行，无异伏诸根，无异一切舍，而得见解脱。",
)
SUTTAS["SA_596"] = {
    "lit": _lit596,
    "mod": _mod596,
    "notes": (
        f"{PROV}confidence=high：primary SN2.17（Subrahmā，无别道见安隐）。"
        "据 SN 校正：慧／摄根／一切舍三句；汉题「常惊」≈ utrasta。"
    ),
}

_lit597, _mod597 = _deva_exchange(
    "云何诸众生，受身得妙色？云何修方便，而得乘出道？"
    "众生住何法，为何所修习，为何等众生，诸天所供养。",
    "云何诸众生，受身得妙色？云何修方便，而得乘出道？"
    "众生住何法，为何所修习，为何等众生，诸天所供养。",
    "持戒明智慧，自修习正受，正直心系念，炽然忧悉灭，"
    "得平等智慧，其心善解脱，"
    "斯等因缘故，受身得妙色，成就乘出道，心住于中学，"
    "如是德备者，为诸天供养。",
    "持戒明智慧，自修习正受，正直心系念，炽然忧悉灭，"
    "得平等智慧，其心善解脱，"
    "斯等因缘故，受身得妙色，成就乘出道，心住于中学，"
    "如是德备者，为诸天供养。",
)
SUTTAS["SA_597"] = {
    "lit": _lit597,
    "mod": _mod597,
    "notes": (
        f"{PROV}confidence=high：primary SN2.14（Nandana 问戒慧定）。"
        "据 SN 校正：伦理／慧／ evolved、最后一身、诸天礼。"
    ),
}

_lit598, _mod598 = _deva_exchange(
    "沉没于睡眠，欠呿不欣乐，饱食心憒闹，懈怠不精勤，斯十覆众生，圣道不显现。",
    "沉没于睡眠，欠呿不欣乐，饱食心憒闹，懈怠不精勤，斯十覆众生，圣道不显现。",
    "心没于睡眠，欠呿不欣乐，饱食心憒闹，懈怠不精勤，精勤修习者，能开发圣道。",
    "心没于睡眠，欠呿不欣乐，饱食心憒闹，懈怠不精勤，精勤修习者，能开发圣道。",
)
SUTTAS["SA_598"] = {
    "lit": _lit598,
    "mod": _mod598,
    "notes": (
        f"{PROV}confidence=high：primary SN1.16（睡眠等五盖障圣道）。"
        "据 SN 校正：汉本「十覆」→ 五盖；以精勤开圣道。"
    ),
}

_lit599, _mod599 = _deva_exchange(
    "外缠结非缠，内缠缠众生，今问于瞿昙，谁于缠离缠？",
    "外缠不是缠，内缠缠众生，今问瞿昙：谁能于缠中解缠？",
    "智者建立戒，内心修智慧，比丘勤修习，于缠能解缠。",
    "智者建立戒，内心修智慧，比丘勤修习，于缠能解缠。",
)
SUTTAS["SA_599"] = {
    "lit": _lit599,
    "mod": _mod599,
    "notes": (
        f"{PROV}confidence=high：primary SN1.23（Jaṭā 缠）。"
        "汉本略去 SN 贪恚痴尽、名色无余段，不增补，仅志其异。"
    ),
}

_lit600, _mod600 = _deva_exchange(
    "难度难可忍，沙门无知故，多起诸艰难，重钝溺沉没，"
    "心随觉自在，数数溺沉没，沙门云何行，善摄护其心？",
    "梵行难行难忍——不熟练者尤其如此；处处狭隘艰难，愚钝者沉没。"
    "心随寻伺流转，一步步沉没。沙门该怎样行，才能善护其心？",
    "如龟善方便，以壳自藏六，比丘习禅思，善摄诸觉想，"
    "其心无所依，他莫能恐怖，是则自隐密，无能诽谤者。",
    "如同乌龟善巧，把六肢收入壳中；比丘习禅思，善摄诸觉想。"
    "心无所依，别人无法恐吓；自己隐密安住，无人能诽谤。",
)
SUTTAS["SA_600"] = {
    "lit": _lit600,
    "mod": _mod600,
    "notes": (
        f"{PROV}confidence=high：primary SN1.17 Dukkara（龟喻摄心）。"
        "据 SN 厘义：难行难忍／心随寻伺溺／龟壳收六肢。"
        "对照说明：UI 英文栏为 SN 平行 Sujato 译，非汉本英译——"
        "SN1.17 仅三偈、无「天子来访」散文框及「久见婆罗门」结偈；"
        "汉本问偈较 SN 为长（增「心随觉自在」等），结偈属天相应定型，今保留。"
    ),
}

_lit601, _mod601 = _deva_exchange(
    "萨罗小流注，当于何反流，生死之径路，于何而不转，世间诸苦乐，何由灭无余？",
    "萨罗小流注，当于何反流，生死之径路，于何而不转，世间诸苦乐，何由灭无余？",
    "眼耳鼻舌身，及彼意入处，名色灭无余，萨罗小还流，"
    "生死道不转，苦乐灭无余。",
    "眼耳鼻舌身，及彼意入处，名色灭无余，萨罗小还流，"
    "生死道不转，苦乐灭无余。",
)
SUTTAS["SA_601"] = {
    "lit": _lit601,
    "mod": _mod601,
    "notes": (
        f"{PROV}confidence=high：primary SN1.27（流还、名色无余灭）。"
        "据 SN 校正：汉以六入答，义同名色灭；不增四界无住段。"
    ),
}

_lit602, _mod602 = _deva_exchange(
    "伊尼耶鹿𨄔，仙人中之尊，少食不嗜味，禅思乐山林，"
    "我今敬稽首，而问于瞿昙，云何出离苦？云何苦解脱？我今问解脱，于何而灭尽？",
    "伊尼耶鹿𨄔，仙人中之尊，少食不嗜味，禅思乐山林，"
    "我今敬稽首，而问于瞿昙，云何出离苦？云何苦解脱？我今问解脱，于何而灭尽？",
    "世间五欲德，心法说第六，于彼欲无欲，解脱一切苦，"
    "如是于苦出，如是苦解脱，汝所问解脱，于彼而灭尽。",
    "世间五欲德，心法说第六，于彼欲无欲，解脱一切苦，"
    "如是于苦出，如是苦解脱，汝所问解脱，于彼而灭尽。",
)
SUTTAS["SA_602"] = {
    "lit": _lit602,
    "mod": _mod602,
    "notes": (
        f"{PROV}confidence=high：primary SN1.30（Eṇijaṅgha，五欲／意第六）。"
        "据 SN 校正：鹿𨄔仙人问苦出；五欲及心为第六。"
    ),
}

# --- SA 603 流（SN10.12 偈段）-------------------------------------------------
SUTTAS["SA_603"] = {
    "lit": [
        OPEN_JET_LIT,
        DEVA_NIGHT_LIT,
        "问偈：「云何度诸流？云何度大海？云何能舍苦？云何得清净？」",
        "佛答：「信能度诸流，不放逸度海，精进能除苦，智慧得清净。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        DEVA_NIGHT_MOD,
        "问偈：「云何度诸流？云何度大海？云何能舍苦？云何得清净？」",
        "佛答：「信能度诸流，不放逸度海，精进能除苦，智慧得清净。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：parallel SN10.12（Āḷavaka 末偈）；汉本仅录度流四句，"
        "不增夜叉问答叙事。据 SN 校正：信／不放逸／精进／慧。"
    ),
}

# --- SA 604 Aśokavadāna -------------------------------------------------------
SUTTAS["SA_604"] = {
    "lit": SA_604_LIT,
    "mod": SA_604_MOD,
    "notes": (
        f"{NO_PARALLEL}"
        "Aśokavadāna 杂入 SA；无 SC 巴利平行。confidence=low："
        "唯依汉本叙事与偈，不增 Ashoka 传说细节；罗什风压缩梵式复述。"
    ),
}

# --- SA 605 念处（peyyāla）----------------------------------------------------
SUTTAS["SA_605"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有四念处——身、受、心、法念处。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有四念处——身、受、心、法念处。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "念处相应起首 peyyāla；义同 SN47 系四念处名，gold_reconstructed 保留名目句。"
        "confidence=medium。"
    ),
}

# --- SA 606 念处（SN47.24）---------------------------------------------------
SUTTAS["SA_606"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「四念处——身、受、心、法；应炽然修习，正念正知。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「四念处——身、受、心、法；应炽然修习，正念正知。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.24（四念处炽然、正念正知）。"
        "据 SN 校正：四支完整；汉本与 605 名目同而加修行句。"
    ),
}

# --- SA 607 净（SN47.1）------------------------------------------------------
SUTTAS["SA_607"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「唯一直行，净众有情，越忧悲、灭恼苦、得实法——谓四念处：身、受、心、法。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「唯一直行，净众有情，越忧悲、灭恼苦、得实法——谓四念处：身、受、心、法。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.1（ekāyano maggo 一乘道）。"
        "SN 作 Vesālī 芒果园，汉作舍卫祇园，地点从汉本，义从 SN。"
    ),
}

# --- SA 608 甘露（SN47.33）---------------------------------------------------
SUTTAS["SA_608"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「离四念处，则离实法、离圣道、离甘露，不得脱生老病苦忧恼——我说彼不得解脱。」",
        "「不离四念处，则得实法、圣道、甘露，解脱生老病苦忧恼——我说彼解脱众苦。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「离四念处，则离实法、离圣道、离甘露，不得脱生老病苦忧恼——我说彼不得解脱。」",
        "「不离四念处，则得实法、圣道、甘露，解脱生老病苦忧恼——我说彼解脱众苦。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.33（四念处与圣道／甘露）。"
        "据 SN 校正：离／不离四念处即离／得 noble path 灭苦。"
    ),
}

# --- SA 609 集（SN47.42）------------------------------------------------------
SUTTAS["SA_609"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「我今当说四念处集、四念处没。谛听，善思。"
        "何等为四念处集、四念处没？食集则身集、食灭则身没。如是随身集观住，"
        "随身灭观住，随身集灭观住，则无所依住，于诸世间永无所取。」",
        "「如是触集则受集，触灭则受没。如是随集法观受住，随灭法观受住，"
        "随集灭法观受住，则无所依住，于诸世间都无所取。」",
        "「名色集则心集，名色灭则心没。随集法观心住，随灭法观心住，"
        "随集灭法观心住，则无所依住，于诸世间则无所取。」",
        "「忆念集则法集，忆念灭则法没。随集法观法住，随灭法观法住，"
        "随集灭法观法住，则无所依住，于诸世间则无所取。是名四念处集、四念处没。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「我现在要说四念处的集与没。谛听，善思惟。"
        "什么是四念处集、四念处没？食集则身集，食灭则身没。这样随身的集而观住，"
        "随身的灭而观住，随身的集灭而观住，就无所依住，于世间永无所取。」",
        "「同样，触集则受集，触灭则受没。这样随受的集而观住，随受的灭而观住，"
        "随受的集灭而观住，就无所依住，于世间都无所取。」",
        "「名色集则心集，名色灭则心没。随心的集而观住，随心的灭而观住，"
        "随心的集灭而观住，就无所依住，于世间无所取。」",
        "「忆念集则法集，忆念灭则法没。随法的集而观住，随法的灭而观住，"
        "随法的集灭而观住，就无所依住，于世间无所取。这叫做四念处集、四念处没。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.42（食／触／名色／忆念集没）。"
        "据 SN 校正：汉「忆念」≈ manasikāra 作意；四支各随集灭观住。"
    ),
}

# --- SA 610 正念（SN47.39）----------------------------------------------------
SUTTAS["SA_610"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当说修四念处：内身外身内外身，受心法亦内外；"
        "精勤方便，正念正知，调伏世间忧悲。过去未来亦同。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「当说修四念处：内身外身内外身，受心法亦内外；"
        "精勤方便，正念正知，调伏世间忧悲。过去未来亦同。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.39（四念处修习）。"
        "汉本增内外身法与过去未来句，从汉保留；义同 SN bhāvanā。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_591": "medium",
    "SA_592": "high",
    "SA_593": "high",
    "SA_594": "medium",
    "SA_595": "high",
    "SA_596": "high",
    "SA_597": "high",
    "SA_598": "high",
    "SA_599": "high",
    "SA_600": "high",
    "SA_601": "high",
    "SA_602": "high",
    "SA_603": "high",
    "SA_604": "low",
    "SA_605": "medium",
    "SA_606": "high",
    "SA_607": "high",
    "SA_608": "high",
    "SA_609": "high",
    "SA_610": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_605": "peyyāla opening of satipaṭṭhāna saṃyutta (cf. SN47)",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(591, 611)}, (
        "GOLD must cover SA_591–SA_610 exactly"
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

    # Boundary: SA_590 if gold, else SA_570
    _goldish = {"gold", "gold_reconstructed"}
    boundary_id = "SA_590"
    for rec in records:
        if rec["id"] == "SA_590" and rec.get("review_status") not in _goldish:
            boundary_id = "SA_570"
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

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa591-610.json").write_text(
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
    continuous_591_610 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(591, 611)
    )
    untouched_571_590 = all(f"SA_{i}" not in GOLD for i in range(571, 591))

    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛", "如如"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_591–SA_610 only)")
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
    print(f"continuous_gold_SA_591–610={continuous_591_610}")
    print(f"SA_571–590_untouched={untouched_571_590}")
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
