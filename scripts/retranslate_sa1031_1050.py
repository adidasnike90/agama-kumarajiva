#!/usr/bin/env python3
"""Retranslate SA 1031–1050（业报相应 卷四十三末–四十）→ merge.

本批二十经：
1031–1038 业报（给孤独 SN55.27／MN143·SN55.26；达摩提离 SN55.53；
         长寿 SN55.3；婆薮；沙罗 SN55.39；耶输；摩那提那 SN47.30）
1039–1050 业报卷四十（淳陀 AN10.176、舍行 AN10.167／119、生闻 AN10.177、
         鞞闻摩 MN41×2、鞞纽多罗 SN55.7、随类 AN10.199–210、蛇行 AN10.216、
         圆珠 AN3.118／无平行、徒生 AN10.174、出不出 AN10.175）

信：有 SN／AN／MN 平行者据巴利／Sujato 厘义；peyyāla／「如上说」据平行或邻经补纲；
    1032 SC 主平行标 sn2.20，然汉叙事同 MN143／SN55.26（舍利弗视疾），据彼厘义；
    1034 六明分想／果位据 SN55.3 校正。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_1031–1050；不触碰 SA_1011–1030（并行批次）；
      若 SA_1030 已为 gold／gold_reconstructed，则断言其不变。
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

OPEN_BAM_LIT = "如是我闻：一时，佛住王舍城迦兰陀竹园。"
OPEN_BAM_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

OPEN_KAP_LIT = "如是我闻：一时，佛住迦毗罗卫国尼拘律园中。"
OPEN_KAP_MOD = "我是这样听说的：有一次，佛住在迦毗罗卫国尼拘律园中。"

OPEN_VAR_LIT = "如是我闻：一时，佛住波罗奈国仙人住处鹿野苑中。"
OPEN_VAR_MOD = "我是这样听说的：有一次，佛住在波罗奈国仙人住处鹿野苑中。"

OPEN_NAT_LIT = "如是我闻：一时，佛住那梨聚落曲谷精舍。"
OPEN_NAT_MOD = "我是这样听说的：有一次，佛住在那梨聚落曲谷精舍。"

OPEN_CHA_LIT = "如是我闻：一时，佛住瞻婆国竭伽池侧。"
OPEN_CHA_MOD = "我是这样听说的：有一次，佛住在瞻婆国竭伽池侧。"

OPEN_GOL_LIT = "如是我闻：一时，佛住王舍城金师精舍。"
OPEN_GOL_MOD = "我是这样听说的：有一次，佛住在王舍城金师精舍。"

OPEN_KOS_LIT = "如是我闻：一时，佛在拘萨罗国人间游行，住鞞罗磨聚落北身恕林中。"
OPEN_KOS_MOD = "我是这样听说的：有一次，佛在拘萨罗国人间游行，住在鞞罗磨聚落北身恕林中。"

OPEN_VEL_LIT = "如是我闻：一时，佛在拘萨罗人间游行，至鞞纽多罗聚落北身恕林中住。"
OPEN_VEL_MOD = "我是这样听说的：有一次，佛在拘萨罗人间游行，到鞞纽多罗聚落北身恕林中住下。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_LAY_MOD = "他们听佛所说，欢喜随喜，作礼离去。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

FOUR_CONF_LIT = "于佛不坏净、于法不坏净、于僧不坏净、圣戒成就"
FOUR_CONF_MOD = "对佛不坏净、对法不坏净、对僧不坏净，以及圣戒成就"

TEN_BAD_LIT = "杀生、不与取、邪淫、妄语、两舌、恶口、绮语、贪、瞋、邪见"
TEN_BAD_MOD = TEN_BAD_LIT
TEN_GOOD_LIT = "不杀生、不与取、不邪淫、不妄语、不两舌、不恶口、不绮语、无贪、无瞋、正见"
TEN_GOOD_MOD = TEN_GOOD_LIT

SIX_MIND_LIT = "念佛、念法、念僧、念戒、念施、念天"
SIX_MIND_MOD = SIX_MIND_LIT

SIX_REAL_LIT = (
    "一切行无常想、于无常作苦想、于苦作无我想、舍想、离欲想、灭想"
)
SIX_REAL_MOD = (
    "观一切行为无常、于无常中观苦、于苦中观无我、观舍离、观离欲、观灭"
)

ILL_ASK_LIT = (
    "问言：「长者！苦患可安忍不？为减为增？」"
    "答言：「尊者！苦受增剧，但增不减。」"
)
ILL_ASK_MOD = (
    "问道：「长者！痛苦还能忍受吗？是在减轻还是加重？」"
    "答道：「尊者！苦受很重，只增不减。」"
)

AWAKEN_LIT = "我生已尽，梵行已立，所作已作，自知不受后有。"
AWAKEN_MOD = AWAKEN_LIT

SOTAPANNA_SELF_LIT = (
    "我地狱尽，畜生、饿鬼尽，一切恶趣尽；得须陀洹，不堕恶趣，"
    "决定正向三菩提，七有天人往生，究竟苦边。"
)
SOTAPANNA_SELF_MOD = (
    "我已尽地狱、畜生、饿鬼，一切恶趣尽；得须陀洹，不堕恶趣，"
    "决定趋向正觉，最多七次往返人天，究竟苦边。"
)

# 十不善／十善略释（淳陀系）
BLACK_DETAIL_LIT = (
    f"谓{TEN_BAD_LIT}："
    "手常血腥，心乐杀害，乃至昆虫不离杀；于他财物聚落空地不离盗；"
    "于有护妇女以力侵逼不离邪淫；"
    "于王庭众会知而妄语；传此破彼两舌；刚强恶口；不时、无义绮语；"
    "于他财起「愿为我有」之贪；欲缚打杀害之瞋；"
    f"及邪见言无施无报、无善恶业果、无此世他世父母、无世阿罗汉能自知作证「{AWAKEN_LIT}」。"
)
BLACK_DETAIL_MOD = (
    f"就是{TEN_BAD_MOD}："
    "手常血腥，心里喜欢杀害，连昆虫也不离杀；在村落空地偷取他财；"
    "对有人守护的妇女用强力侵逼；"
    "在王庭集会里明知故犯地说假话；搬弄是非两舌；说刚强恶口；说不合时、无义的绮语；"
    "对他的财物起「但愿归我」的贪；想捆绑鞭打杀害的瞋；"
    f"以及邪见，说没有布施没有果报、没有善恶业果、没有此世他世和父母、"
    f"没有世间阿罗汉能自己现证「{AWAKEN_MOD}」。"
)

WHITE_DETAIL_LIT = (
    f"谓{TEN_GOOD_LIT}："
    "舍刀杖，惭愧悲念一切众生；与者取、不与不取；"
    "于有护者乃至一花鬘，不强干邪淫；审谛实说；"
    "离者令和、和者随喜；柔软令人乐闻；谛说、时说、实说、义说、法说；"
    "于他财不起己有想；不作打缚杀害之念；"
    f"正见有施有报有福、有善恶业果、有此世他世父母、有世阿罗汉能现证「{AWAKEN_LIT}」。"
)
WHITE_DETAIL_MOD = (
    f"就是{TEN_GOOD_MOD}："
    "放下刀杖，怀着惭愧悲念一切众生；给人的才取、不给的不取；"
    "对有人守护的人，乃至一串花鬘，也不强行邪淫；如实审慎地说；"
    "离散的促令和合、和合的随喜；话说得柔软让人乐听；"
    "说真实、合时、有义、合法的话；"
    "对他的财物不起「归我所有」之想；不起打绑杀害的念头；"
    f"正见：有布施有果报有福德、有善恶业果、有此世他世和父母、"
    f"有世间阿罗汉能现证「{AWAKEN_MOD}」。"
)

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 1031 给孤独（SN55.27）-----------------------------------------------
SUTTAS["SA_1031"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者阿难闻给孤独长者身遭苦患，往诣其舍。"
        "长者遥见，扶床欲起。阿难止之，为问三受——"
        "乐受、苦受、不苦不乐受——乃至「苦患但增不减。」",
        "阿难告言：「勿怖！无闻凡夫不信佛、法、僧，圣戒不具，"
        "是故怖畏命终及后世苦。"
        f"汝已断不信，{FOUR_CONF_LIT}，何畏之有？」",
        "长者白言：「我何所怖？昔于王舍城寒林丘冢间见世尊，"
        f"即得{FOUR_CONF_LIT}。"
        "自尔以来，家财悉与佛及四众共。」",
        "阿难言：「善哉！汝自记说须陀洹果。」"
        "长者请食，阿难默受。设供已，更为说法示教照喜，从坐起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时尊者阿难听说给孤独长者身患重病，就到他家里去。"
        "长者远远看见，扶着床想起来。阿难阻止他，并问起三种受——"
        "乐受、苦受、不苦不乐受——一直说到「病苦只增不减。」",
        "阿难告诉他：「不要怕！没听闻的凡夫不信佛、法、僧，圣戒不具足，"
        "所以害怕命终和后世的苦。"
        f"你已经断除不信，{FOUR_CONF_MOD}，有什么可怕的呢？」",
        "长者说：「我怕什么？从前在王舍城寒林坟间见到世尊，"
        f"就得到了{FOUR_CONF_MOD}。"
        "从那时起，家里的财物都与佛和四众共享。」",
        "阿难说：「很好！你自己记说了须陀洹果。」"
        "长者请他用餐，阿难默然接受。供养完毕，又为他说法开示鼓励，然后起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.27；"
        "据巴利补凡夫四怖（不信三宝＋破戒）／圣弟子四不坏净无怖；"
        "汉「叉摩修多罗」三受问安 peeyāla 略补。reconstruction：三受问安纲。"
    ),
}

# --- SA 1032 给孤独（汉同 MN143／SN55.26；SC 亦列 sn2.20）-------------------
SUTTAS["SA_1032"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时尊者舍利弗闻给孤独长者苦患，语阿难：「当共往看。」阿难默许。"
        "二人共诣其舍。长者遥见舍利弗，扶床欲起……问三受，乃至「苦患转增。」",
        "舍利弗告言：「当如是学：眼等六根不著，不依六界生贪识；"
        "色等六尘不著，不依法界生贪识；"
        "地水火风空识界不著；色受想行识阴不著，不依五阴生贪识。」",
        "长者悲泣。阿难问：「怯劣耶？」"
        "答言：「不也。我奉佛二十余年，未闻如是深法。」"
        "舍利弗言：「我亦久未为诸白衣说如是法。」",
        "长者白言：「居家有胜信胜念，不闻深法或生退没。"
        "愿常为白衣说深妙法，哀愍故！请受此食。」默然受请。"
        "设供已，说法示教照喜，从坐起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者舍利弗听说给孤独长者病苦，对阿难说：「我们一起去探望。」阿难默许。"
        "二人一起到他家。长者远远看见舍利弗，扶床想起来……问起三受，一直到「病苦加重。」",
        "舍利弗告诉他：「应当这样学：对眼等六根不执着，不依六界生起贪识；"
        "对色等六尘不执着，不依法界生起贪识；"
        "对地水火风空识界不执着；对色受想行识五蕴不执着，不依五蕴生起贪识。」",
        "长者流泪。阿难问：「是胆怯退缩吗？」"
        "答道：「不是。我归依佛二十多年，还没听过这样深的法。」"
        "舍利弗说：「我也好久没有对在家人说这样的法。」",
        "长者说：「在家人虽有好的信与念，不听深法有时会退堕。"
        "请常为白衣说深妙法，出于哀愍！请接受这餐供养。」他们默然接受。"
        "供养后，又为他说法开示鼓励，然后起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：汉叙事同 MN143 Anāthapiṇḍikovāda／SN55.26（舍利弗视疾、六处界阴不著）；"
        "SC 表亦列 sn2.20（死后化生说偈），义属另经，不以彼改写本经；"
        "三受问安 peeyāla 略补。reconstruction：三受问安纲。"
    ),
}

# --- SA 1033 达摩提离（SN55.53；汉作 peeyāla＋六念→阿那含）------------------
SUTTAS["SA_1033"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时达摩提离长者身遭苦患。世尊往看，问安三受，乃至苦增不减。"
        f"佛告言：「当依{FOUR_CONF_LIT}；于上更修六念——{SIX_MIND_LIT}。」",
        f"长者白言：「{FOUR_CONF_LIT}及六念，我今悉成就，常修不离。」",
        "佛言：「善哉！汝自记阿那含果。」"
        "请佛受食，默然许之。设供已，说法示教照喜，从坐起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时达摩提离长者身患重病。世尊前去探望，问起三受，一直到病苦加重不减。"
        f"佛告诉他：「应当依止{FOUR_CONF_MOD}；再往上修习六念——{SIX_MIND_MOD}。」",
        f"长者说：「{FOUR_CONF_MOD}和六念，我现在都成就了，常常修习不离。」",
        "佛说：「很好！你自己记说了阿那含果。」"
        "他请佛用餐，佛默然答应。供养后，又为他说法开示鼓励，然后起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=medium：gold_reconstructed——"
        "汉「如给孤独初经／第二经广说」peeyāla，差别为四不坏净上修六念、记阿那含；"
        "SN55.53 Dhammadinna 在鹿野苑劝修甚深空相应说，后以四预流支记须陀洹，叙事异；"
        "本经依汉位次补视疾＋六念纲，果位从汉。reconstruction：peeyāla 视疾＋六念。"
    ),
}

# --- SA 1034 长寿（SN55.3 Dīghāvu）------------------------------------------
SUTTAS["SA_1034"] = {
    "lit": [
        OPEN_BAM_LIT,
        "时有长寿童子——树提长者之孙——身婴重病。"
        "世尊闻已，晨朝入城乞食，次至其舍。"
        f"{ILL_ASK_LIT}"
        f"佛告童子：「当如是学：{FOUR_CONF_LIT}。」",
        f"童子白言：「此四不坏净，我今悉有。」"
        f"佛言：「当依此四，于上修六明分想：{SIX_REAL_LIT}。」",
        f"童子白言：「六想我亦常现前。然念命终后，祖父树提当云何？」"
        "树提语之曰：「勿以我为念。且听世尊法，思惟忆持，长夜得利。」"
        f"童子言：「我当于一切行修{SIX_REAL_LIT}，常现在前。」",
        "佛告童子：「汝今自记阿那含果。」"
        "请佛受食，默许。设供说法已，从坐起去。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "当时有长寿童子——树提长者的孙子——身患重病。"
        "世尊听说后，清晨进城乞食，依次到他家。"
        f"{ILL_ASK_MOD}"
        f"佛告诉童子：「应当这样学：{FOUR_CONF_MOD}。」",
        f"童子说：「这四不坏净，我现在都有。」"
        f"佛说：「应当依这四法，再修六种通向证智的想：{SIX_REAL_MOD}。」",
        f"童子说：「这六想我也常常现前。可是想到命终以后，祖父树提会怎样？」"
        "树提对他说：「不要惦记我。先听世尊说法，思惟忆持，长夜得安乐利益。」"
        f"童子说：「我会对一切行修习{SIX_REAL_MOD}，让它们常常现前。」",
        "佛告诉童子：「你现在自己记说了阿那含果。」"
        "他请佛用餐，佛默然答应。供养说法后，佛起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.3；"
        "据巴利校正六明分想为无常／苦／无我／舍／离欲／灭（汉作观食、不可乐、死想）；"
        "果位据 SN55.3 记阿那含（汉作斯陀含）。reconstruction：六想＋果位。"
    ),
}

# --- SA 1035 婆薮（无平行；如达摩提离 peeyāla）------------------------------
SUTTAS["SA_1035"] = {
    "lit": [
        OPEN_VAR_LIT,
        "时婆薮长者身遭苦患。世尊往看，"
        f"如达摩提离经广说——依{FOUR_CONF_LIT}修{SIX_MIND_LIT}，自记阿那含果；"
        "受请设供，说法示教照喜已，从坐起去。",
    ],
    "mod": [
        OPEN_VAR_MOD,
        "当时婆薮长者身患重病。世尊前去探望，"
        f"如同达摩提离经中广说——依{FOUR_CONF_MOD}修{SIX_MIND_MOD}，自己记说阿那含果；"
        "接受供养，说法开示鼓励后，起身离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉「如前达摩提那广说」peeyāla；据 SA_1033 纲补。住鹿野苑。"
    ),
}

# --- SA 1036 沙罗（SN55.39 Godhā 女近；汉作释氏沙罗＋五喜处）--------------
SUTTAS["SA_1036"] = {
    "lit": [
        OPEN_KAP_LIT,
        "时释氏沙罗疾病委笃。世尊晨朝乞食，次到其舍。"
        f"{ILL_ASK_LIT}"
        f"佛告言：「当如是学：{FOUR_CONF_LIT}。」"
        f"沙罗白言：「此四法我悉有之。」",
        f"佛言：「当依四不坏净，于上修五喜处——念如来乃至念自所施。」"
        "沙罗白言：「五喜处我亦常修。」",
        "佛言：「善哉！汝自记斯陀含果。」"
        "请佛受食，默许。设供说法已，从坐起去。",
    ],
    "mod": [
        OPEN_KAP_MOD,
        "当时释迦族的沙罗病得很重。世尊清晨乞食，依次到他家。"
        f"{ILL_ASK_MOD}"
        f"佛告诉他：「应当这样学：{FOUR_CONF_MOD}。」"
        f"沙罗说：「这四法我都有。」",
        f"佛说：「应当依四不坏净，再修五喜之处——念如来乃至念自己的布施。」"
        "沙罗说：「五喜之处我也常常修。」",
        "佛说：「很好！你自己记说了斯陀含果。」"
        "他请佛用餐，佛默然答应。供养说法后，佛起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=medium：平行 SN55.39 Kāḷigodhā（释女、四预流支含无悭施，记须陀洹）；"
        "汉作释氏沙罗男众、五喜处（念佛等）、记斯陀含——保留汉叙事位次，"
        "法义以四不坏净＋喜施／念处为共核。"
    ),
}

# --- SA 1037 耶输（无平行；peeyāla）-----------------------------------------
SUTTAS["SA_1037"] = {
    "lit": [
        OPEN_NAT_LIT,
        "尔时耶输长者疾病困笃。"
        f"世尊往看，如达摩提离经广说，得阿那含果记——"
        f"依{FOUR_CONF_LIT}修{SIX_MIND_LIT}；受请说法已，从坐起去。",
    ],
    "mod": [
        OPEN_NAT_MOD,
        "那时耶输长者病势沉重。"
        f"世尊前去探望，如同达摩提离经中广说，得到阿那含果的记说——"
        f"依{FOUR_CONF_MOD}修{SIX_MIND_MOD}；接受供养说法后，起身离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：gold_reconstructed——"
        "汉「如达摩提那广说」peeyāla；据 SA_1033 纲补。住那梨曲谷。"
    ),
}

# --- SA 1038 摩那提那（SN47.30）---------------------------------------------
SUTTAS["SA_1038"] = {
    "lit": [
        OPEN_CHA_LIT,
        "时摩那提那长者疾病新差，遣人诣尊者阿那律所，"
        "稽首问讯，请明日通身四人受食；自言俗事繁，不能躬迎，愿哀愍赴请。"
        "阿那律默受，告来使：「且安，我自知时。」",
        "夜办净食。晨朝复告时到。阿那律著衣持钵，通身四人诣其舍。"
        "长者眷属迎礼问讯，退坐一面。",
        "阿那律问：「堪忍安乐住不？」"
        "答言：「先病委笃，今已蒙差。」"
        "问：「汝住何法，苦患得息？」",
        "长者白言：「我住四念处，专修系念，故苦患得息。"
        "谓内身、外身、内外身；受、心、法——各内外俱，"
        "精勤正念正智，调伏世间贪忧。"
        "于世尊所说五下分结，我都不见有未断者。」",
        "阿那律言：「善哉！汝自记阿那含果。」"
        "长者手自供食；食已听法，示教照喜已，尊者从坐起去。",
    ],
    "mod": [
        OPEN_CHA_MOD,
        "当时摩那提那长者病刚好，派人到尊者阿那律那里，"
        "顶礼问讯，请明天连他一共四人来受食；说自己俗事多，不能亲自迎接，请慈悲赴请。"
        "阿那律默然接受，告诉来人：「你安心，我自己会知道时间。」",
        "夜里备好清净饮食。清晨再通报时间到了。阿那律穿衣持钵，连同三人到他家。"
        "长者眷属迎接礼拜问讯，退坐一面。",
        "阿那律问：「还能忍受、安住吗？」"
        "答道：「先前病很重，现在已经好些了。」"
        "又问：「你安住什么法，病苦才得以平息？」",
        "长者说：「我安住四念处，专心系念，所以病苦得以休息。"
        "就是内身、外身、内外身；受、心、法——各分内外，"
        "精勤、正念、正智，调伏世间的贪与忧。"
        "对于世尊所说的五下分结，我看不见还有哪一样没断。」",
        "阿那律说：「很好！你自己记说了阿那含果。」"
        "长者亲手供食；吃完听法，开示鼓励后，尊者起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.30；"
        "据巴利补「五下分结已断」自记阿那含（汉唯举四念处得息）；"
        "汉作阿那律受请、病已差；巴利作阿难视疾、病中说——保留汉人物／情节。"
        "reconstruction：五下分结自记。"
    ),
}

# --- SA 1039 淳陀（AN10.176）------------------------------------------------
SUTTAS["SA_1039"] = {
    "lit": [
        OPEN_GOL_LIT,
        "时淳陀长者来诣佛所，稽首退坐。"
        "佛问：「汝爱乐何等沙门、婆罗门净行？」"
        "淳陀白言：「有事水、事毘湿波天，执杖澡罐、常净其手者，教人望日澡发持斋，"
        "著新白㲲，卧牛粪地；晨朝触地、执粪草，唱『此地净，我如是净』——"
        "如是乃净。我所宗仰。」",
        "佛告淳陀：「有黑法黑报，不净不净果，负重向下。"
        "成就此恶者，触地执草唱净，亦不清净；不触不执，亦不清净。",
        f"「何等黑法？{BLACK_DETAIL_LIT}"
        "是名黑报不净，触与不触皆不净。",
        "「有白法白报，净有净果，轻举上升。"
        "成就此善者，触地执草，亦得清净；不触不执，亦得清净。",
        f"「何等白法？{WHITE_DETAIL_LIT}"
        "是名白报清净，触与不触皆净。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_GOL_MOD,
        "当时淳陀长者来到佛处，顶礼后退坐一面。"
        "佛问：「你喜欢哪一类沙门、婆罗门的净行？」"
        "淳陀说：「有事奉水、事奉毘湿波天，拿着杖和澡罐、常常洗手的人，"
        "教人在月圆日洗头持斋，穿新白衣，睡在涂牛粪的地上；"
        "清晨摸地、拿牛粪和草，喊『这里清净，我也这样清净』——"
        "这样才算清净。我所宗仰的就是这类。」",
        "佛告诉淳陀：「有黑法得黑报，不净得不净果，像负重向下坠。"
        "成就这些恶法的人，即使摸地拿草喊清净，也不清净；不摸不拿，也不清净。",
        f"「什么是黑法？{BLACK_DETAIL_MOD}"
        "这叫做黑报不净，摸与不摸都不清净。",
        "「有白法得白报，净有净果，像轻举向上升。"
        "成就这些善法的人，摸地拿草，也得清净；不摸不拿，也得清净。",
        f"「什么是白法？{WHITE_DETAIL_MOD}"
        "这叫做白报清净，摸与不摸都清净。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.176 Cunda；"
        "据巴利：净秽不在触地澡浴，而在十不善／十善业道；"
        "汉「恶心」作恶口；「坏语」作绮语。压缩仪轨描写。"
    ),
}

# --- SA 1040 舍行（AN10.167／AN10.119）--------------------------------------
SUTTAS["SA_1040"] = {
    "lit": [
        OPEN_GOL_LIT,
        "时有异婆罗门于十五日洗头受斋，著新白㲲，手执生草，来诣佛所，问讯退坐。"
        "佛问：「洗头著新衣，是谁家法？」"
        "答言：「瞿昙！是学舍法——望日洗头持斋，随力布施作福，名婆罗门舍行。」",
        "佛告言：「贤圣法律之舍行异于此。」"
        "「云何？」"
        f"「谓依不杀而舍杀生，依不盗而舍不与取，依不邪淫而舍非梵行，"
        "依实语而舍妄语，依和合而舍两舌，依软语而舍恶口，依义语而舍绮语，"
        "依无贪而舍苦贪爱著，依无瞋而舍忿恨，依正见而舍邪见。"
        f"是名贤圣法律所行舍行——即舍{TEN_BAD_LIT}。」",
        "婆罗门言：「善哉！贤圣舍行。」欢喜随喜，从坐起去。",
    ],
    "mod": [
        OPEN_GOL_MOD,
        "当时有一位婆罗门在月圆日洗头持斋，穿新白衣，手里拿着鲜草，来到佛处，问讯后退坐。"
        "佛问：「洗头穿新衣，是哪一家的法？」"
        "答道：「瞿昙！这是修习舍行——月圆日洗头持斋，随力布施作福，叫做婆罗门的舍行。」",
        "佛告诉他：「贤圣法律中的舍行跟这不一样。」"
        "「怎样呢？」"
        f"「就是依不杀而舍弃杀生，依不盗而舍弃偷盗，依不邪淫而舍弃非梵行，"
        "依实语而舍弃妄语，依和合而舍弃两舌，依软语而舍弃恶口，依有义之语而舍弃绮语，"
        "依无贪而舍弃苦贪与爱著，依无瞋而舍弃忿恨，依正见而舍弃邪见。"
        f"这叫做贤圣法律中的舍行——也就是舍弃{TEN_BAD_MOD}。」",
        "婆罗门说：「很好！贤圣的舍行。」欢喜随喜，起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.167／AN10.119 Paccorohaṇī；"
        "汉「如前清淨分广说」peeyāla，据 AN／SA_1039 十业道补舍行之义。"
        "reconstruction：十善舍十恶纲。"
    ),
}

# --- SA 1041 生闻（AN10.177）------------------------------------------------
SUTTAS["SA_1041"] = {
    "lit": [
        OPEN_BAM_LIT,
        "时生闻梵志来诣佛所，问讯退坐，白言："
        "「瞿昙！我有亲爱命终，我为彼信心布施。彼得受不？」",
        "佛告言：「非一向得。"
        "若生地狱、畜生、人中，则受彼趣之食，不得汝施；"
        "若生入处饿鬼，乃得汝所施食。」",
        "「若不生彼趣，谁当食之？」"
        "「必有余亲知识生入处饿鬼者，得食之。」"
        "「若都无者？」"
        "「施者自得其福，达嚫不失。」",
        "「云何施者自受达嚫？」"
        f"「若人行{TEN_BAD_LIT}，而能施沙门婆罗门衣食钱财灯明——"
        "纵生象马牛驴等畜生，以施故仍得受用诸具；"
        f"若持{TEN_GOOD_LIT}而行施，生人中得衣食众具，生天上得天福庄严。"
        "是名施者行施，果报不失。」",
        "生闻闻已，欢喜随喜，从坐起去。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "当时生闻梵志来到佛处，问讯后退坐，说道："
        "「瞿昙！我有极亲爱的人忽然命终，我为他怀着信心布施。他能得到吗？」",
        "佛告诉他：「不是一律都能得到。"
        "如果生在地狱、畜生、人中，就受用那一趣的食物，得不到你的施食；"
        "如果生在名叫入处的饿鬼中，才能得到你所施的食物。」",
        "「如果不生到那里，谁来吃呢？」"
        "「一定还有别的亲戚朋友生在入处饿鬼中，会得到吃的。」"
        "「如果全都没有呢？」"
        "「布施的人自己仍得福德，供养的果报不会失掉。」",
        "「怎样施者自己受达嚫？」"
        f"「如果有人做{TEN_BAD_MOD}，却还能布施沙门婆罗门衣食钱财灯明——"
        "即使生为象马牛驴等畜生，因为布施仍能得到相应的受用；"
        f"如果持守{TEN_GOOD_MOD}又布施，生在人中得衣食用具，生在天上得天福庄严。"
        "这叫做施者行施，果报不失。」",
        "生闻听完，欢喜随喜，起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.177 Jāṇussoṇi；"
        "据巴利：唯「入处饿鬼」能受荐亡施食；余趣不得；施福施者不失；"
        "汉「如淳陀广说」十业 peeyāla 压缩。reconstruction：十业与畜生／人天报纲。"
    ),
}

# --- SA 1042 鞞闻摩（MN41）--------------------------------------------------
SUTTAS["SA_1042"] = {
    "lit": [
        OPEN_KOS_LIT,
        "鞞罗聚落婆罗门、长者闻佛住林中，共诣稽首，退坐一面，白言："
        "「何因命终生地狱？」"
        f"佛告：「行非法、行险行——具足{TEN_BAD_LIT}，故生地狱。」",
        "「何因得生天上？」"
        f"「行法行、正行——具足{TEN_GOOD_LIT}，故生天上。」",
        "「若行此正行，欲求生剎利、婆罗门、居士大姓，悉得；"
        "欲求四王天乃至他化自在天，悉得；欲求梵世、光音、遍净、阿伽尼吒，悉得——"
        "以持戒清净、心离爱欲，所愿必成。"
        "欲求初禅乃至第四禅，慈悲喜舍，空处、识处、无所有处、非想非非想处，悉得；"
        "欲求须陀洹、斯陀含、阿那含，及天耳、他心、宿命、生死、漏尽诸智，悉得——"
        "以法行正行、持戒离欲故。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_KOS_MOD,
        "鞞罗聚落的婆罗门和长者听说佛住在林中，一起前来顶礼，退坐一面，问道："
        "「什么因缘命终生地狱？」"
        f"佛告诉他们：「做非法、做险恶之行——具足{TEN_BAD_MOD}，所以生地狱。」",
        "「什么因缘能生天上？」"
        f"「做法行、做正行——具足{TEN_GOOD_MOD}，所以生天上。」",
        "「如果修这样的正行，想生到剎利、婆罗门、居士大家族，都能如愿；"
        "想生四王天乃至他化自在天，都能如愿；想生梵世、光音、遍净、色究竟天，都能如愿——"
        "因为持戒清净、心离爱欲，所愿自然成就。"
        "想修初禅到第四禅，慈悲喜舍，空无边处、识无边处、无所有处、非想非非想处，都能成就；"
        "想证须陀洹、斯陀含、阿那含，以及天耳、他心、宿命、生死、漏尽等智，都能得到——"
        "因为法行正行、持戒离欲的缘故。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary MN41 Sāleyyaka（及 MN42）；"
        "十不善→地狱，十善→人天及禅、梵、果智所愿；压缩汉本层叠愿望。"
    ),
}

# --- SA 1043 鞞闻摩（MN41／42 peeyāla）--------------------------------------
SUTTAS["SA_1043"] = {
    "lit": [
        OPEN_KOS_LIT,
        "时鞞罗磨聚落婆罗门、长者乘白马车，持金斗伞盖澡瓶，出村诣林；"
        "至道口下车步入，问讯退坐。",
        f"白言：「瞿昙！何因命终生地狱，乃至生天？」"
        f"佛即为说：行{TEN_BAD_LIT}生地狱；行{TEN_GOOD_LIT}生天上，"
        "及大姓、诸天、禅定、梵世、沙门果所愿皆得——如上鞞闻摩经广说。",
        "闻已欢喜随喜，从坐起去。",
    ],
    "mod": [
        OPEN_KOS_MOD,
        "当时鞞罗磨聚落的婆罗门和长者乘坐白马车，带着金斗、伞盖、澡瓶，出村到林中；"
        "到路口下车步行进入，问讯后退坐。",
        f"问道：「瞿昙！什么因缘命终生地狱，乃至生天？」"
        f"佛就为他们说：做{TEN_BAD_MOD}生地狱；做{TEN_GOOD_MOD}生天上，"
        "以及大家族、诸天、禅定、梵世、沙门果等所愿都能得到——如同前面鞞闻摩经中广说。",
        "听完欢喜随喜，起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：gold_reconstructed——"
        "汉「如上修多罗广说」；人物迎佛仪式异于 SA_1042，法义同 MN41／42。"
        "reconstruction：十业生趣纲。"
    ),
}

# --- SA 1044 鞞纽多罗（SN55.7）----------------------------------------------
SUTTAS["SA_1044"] = {
    "lit": [
        OPEN_VEL_LIT,
        "鞞纽多罗聚落婆罗门、长者共诣林中，问讯退坐。"
        "世尊告言：「我当说自通之法。谛听。"
        "圣弟子作是念：『我不喜他杀我，他亦不喜；云何杀彼？』觉已受不杀戒。"
        "『我不喜他盗我、侵我妻、欺我、离我亲、恶口、绮语；他亦如是——我云何加之？』"
        "是故持不盗、不邪淫、不妄语、不两舌、不恶口、不绮语。"
        "如是七支，名圣戒。",
        f"「又成就{FOUR_CONF_LIT}，是名四不坏净。"
        f"圣弟子观察自身，能自记说：『{SOTAPANNA_SELF_LIT}』」",
        "闻已欢喜随喜，从坐起去。",
    ],
    "mod": [
        OPEN_VEL_MOD,
        "鞞纽多罗聚落的婆罗门和长者一起到林中，问讯后退坐。"
        "世尊告诉他们：「我要说自通之法。仔细听。"
        "圣弟子这样想：『我不喜欢别人杀我，别人也不喜欢；怎么能去杀他？』觉悟后受持不杀戒。"
        "『我不喜欢别人偷我、侵我妻、骗我、离间我的亲友、恶口、绮语；别人也一样——我怎么能对别人这样做？』"
        "所以持不盗、不邪淫、不妄语、不两舌、不恶口、不绮语。"
        "这七支，叫做圣戒。",
        f"「又成就{FOUR_CONF_MOD}，叫做四不坏净。"
        f"圣弟子观察自己，能自己记说：『{SOTAPANNA_SELF_MOD}』」",
        "听完欢喜随喜，起身离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN55.7 Veḷudvāreyya；"
        "自通法＝推己及人成七支圣戒，加四不坏净自记须陀洹；"
        "汉「如上说」peeyāla 压缩为七戒纲。"
    ),
}

# --- SA 1045 随类（AN10.199–210）--------------------------------------------
SUTTAS["SA_1045"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有相习近法。谛听。"
        f"杀生者与杀生者相习近，乃至邪见与邪见相习近——"
        "如不净物自相和合。"
        f"不杀与不杀相习近，乃至正见与正见相习近——"
        "如净物和合：乳生酪，酪生酥，酥生醍醐。"
        "是名相习近法。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有彼此习近同类的法。仔细听。"
        f"杀生的人与杀生的人彼此习近，乃至邪见与邪见彼此习近——"
        "如同不净的东西自己和合在一起。"
        f"不杀的与不杀的彼此习近，乃至正见与正见彼此习近——"
        "如同净物和合：乳生酪，酪生酥，酥生醍醐。"
        "这叫做相习近法。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.199–210（类聚习近）；"
        "十不善自相习近／十善自相习近；醍醐喻从汉。"
    ),
}

# --- SA 1046 蛇行（AN10.216）------------------------------------------------
SUTTAS["SA_1046"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有蛇行法。谛听。"
        f"行{TEN_BAD_LIT}者，身口意皆蛇行，趣向地狱或畜生——"
        "腹行类如蛇鼠猫狸，是名蛇行法。"
        f"行{TEN_GOOD_LIT}者，身口意非蛇行，趣向天上或人中，是名非蛇行法。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有蛇行法。仔细听。"
        f"做{TEN_BAD_MOD}的人，身口意都像蛇一样弯曲而行，趋向地狱或畜生——"
        "腹行之类如蛇、鼠、猫、狸，这叫做蛇行法。"
        f"做{TEN_GOOD_MOD}的人，身口意不是蛇行，趋向天上或人中，这叫做非蛇行法。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.216；"
        "汉「如前淳陀广说」peeyāla，据十业道补。reconstruction：十业蛇行纲。"
    ),
}

# --- SA 1047 圆珠（AN3.118）-------------------------------------------------
SUTTAS["SA_1047"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有恶业因、恶心因、恶见因，身坏命终必堕泥犁。"
        "譬如圆珠掷空，落地流转，不住一处。"
        f"恶业谓杀生乃至绮语；恶心谓贪与瞋；恶见谓邪颠倒——"
        "具此三因，必堕地狱。",
        f"「有善业因、善心因、善见因，身坏命终必生善趣。"
        f"善业谓{TEN_GOOD_LIT}中身口七支；善心谓无贪无瞋；善见谓正见乃至知不受后有。"
        "譬如四方摩尼珠掷空，随堕则安；三善因所生亦尔。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有恶业因、恶心因、恶见因，身体坏灭命终后一定堕落地狱。"
        "就像圆球抛向空中，落地滚动，停不住在一处。"
        f"恶业是杀生乃至绮语；恶心是贪与瞋；恶见是邪倒的见——"
        "具足这三因，一定堕地狱。",
        f"「有善业因、善心因、善见因，身体坏灭命终后一定生到善趣。"
        f"善业是{TEN_GOOD_MOD}里的身口七支；善心是无贪无瞋；善见是正见，乃至知道不受后有。"
        "就像四方平整的摩尼珠抛向空中，落下就安住；三善因所受生也是这样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN3.118；"
        "恶三因如圆球不安，善三因如方珠安住；汉末误呼「婆罗门」改为告比丘。"
        "reconstruction：善恶三因纲（汉「如上广说」）。"
    ),
}

# --- SA 1048 圆珠（无 SC 平行；十业人天报）----------------------------------
SUTTAS["SA_1048"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「杀生多习，生地狱；若生人中，命短。"
        "不与取多习，生地狱；若生人中，财难。"
        "邪淫多习，生地狱；若生人中，妻为他侵。"
        "妄语多习，生地狱；若生人中，多遭讥毁。"
        "两舌多习，生地狱；若生人中，亲友乖离。"
        "恶口多习，生地狱；若生人中，常闻恶声。"
        "绮语多习，生地狱；若生人中，言不见信。"
        "贪、瞋、邪见多习，生地狱；若生人中，增贪、增瞋、增痴。",
        "「离杀多修，生天上；若生人中，长寿。"
        "乃至正见多修，生天上；若生人中，不增愚痴——余九善亦各得人天对治之报。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「杀生常常做，会生地狱；若生为人，寿命短。"
        "偷盗常常做，会生地狱；若生为人，财物艰难。"
        "邪淫常常做，会生地狱；若生为人，妻子被人侵夺。"
        "妄语常常做，会生地狱；若生为人，多被讥讽。"
        "两舌常常做，会生地狱；若生为人，亲友离散。"
        "恶口常常做，会生地狱；若生为人，常听到难听的话。"
        "绮语常常做，会生地狱；若生为人，说话不被信任。"
        "贪、瞋、邪见常常做，会生地狱；若生为人，更增贪、瞋、痴。",
        "「远离杀生常常修，会生天上；若生为人，长寿。"
        "乃至正见常常修，会生天上；若生为人，不增愚痴——其余九种善也各有相应的人天果报。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：十不善／十善人中别报，义近 AN8.40 等业报定型；"
        "无专 SC 平行，压缩汉本对举以免过度贴字。"
    ),
}

# --- SA 1049 徒生（AN10.174）------------------------------------------------
SUTTAS["SA_1049"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘："
        f"「{TEN_BAD_LIT}各有三种——从贪生、从瞋生、从痴生。"
        f"{TEN_GOOD_LIT}各有三种——从不贪生、从不瞋生、从不痴生。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们："
        f"「{TEN_BAD_MOD}各有三种——从贪生、从瞋生、从痴生。"
        f"{TEN_GOOD_MOD}各有三种——从不贪生、从不瞋生、从不痴生。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.174；"
        "十不善／十善皆可从贪瞋痴或其反面生起。"
    ),
}

# --- SA 1050 出不出（AN10.175）----------------------------------------------
SUTTAS["SA_1050"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有出法，有不出法。"
        f"不杀生于杀生为出，乃至正见于邪见为出——"
        f"以{TEN_GOOD_LIT}出于{TEN_BAD_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有出离的法，有不出离的法。"
        f"不杀生是从杀生中出离，乃至正见是从邪见中出离——"
        f"用{TEN_GOOD_MOD}从{TEN_BAD_MOD}中出离。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary AN10.175；"
        "十善为「出」，对治十不善之「不出」。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {
    "SA_1031": "high",
    "SA_1032": "high",
    "SA_1033": "medium",
    "SA_1034": "high",
    "SA_1035": "medium",
    "SA_1036": "medium",
    "SA_1037": "medium",
    "SA_1038": "high",
    "SA_1039": "high",
    "SA_1040": "high",
    "SA_1041": "high",
    "SA_1042": "high",
    "SA_1043": "high",
    "SA_1044": "high",
    "SA_1045": "high",
    "SA_1046": "high",
    "SA_1047": "high",
    "SA_1048": "medium",
    "SA_1049": "high",
    "SA_1050": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1031": "叉摩三受问安 peeyāla → 据 SN55.27／差摩问安纲略补",
    "SA_1032": "三受问安 peeyāla → 据 MN143／差摩问安纲略补",
    "SA_1033": "「如给孤独经广说」peeyāla → 视疾＋四不坏净＋六念＋阿那含",
    "SA_1034": "六明分想／果位据 SN55.3 校正（舍离欲灭；阿那含）",
    "SA_1035": "「如前达摩提那广说」→ SA_1033 纲",
    "SA_1037": "「如达摩提那广说」→ SA_1033 纲",
    "SA_1038": "据 SN47.30 补五下分结已断自记",
    "SA_1040": "「如前清淨分」→ AN10.167 十善舍十恶纲",
    "SA_1041": "「如淳陀广说」十业＋畜生／人天施报纲",
    "SA_1043": "「如上广说」→ SA_1042／MN41 十业生趣纲",
    "SA_1046": "「如前淳陀」→ 十业蛇行纲",
    "SA_1047": "「如上广说」→ AN3.118 善恶三因纲",
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
assert set(GOLD) == {f"SA_{i}" for i in range(1031, 1051)}


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
    by_status = {r["id"]: r.get("review_status") for r in records}
    if by_status.get("SA_1030") in _goldish:
        boundary_id = "SA_1030"
    else:
        boundary_id = None

    boundary_before = None
    if boundary_id:
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

    # Snapshot 1011–1030 to assert untouched (parallel batch)
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
        if rec["id"] in {f"SA_{i}" for i in range(1011, 1031)}
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
    (ROOT / "data" / "translated" / "validation_report_sa1031-1050.json").write_text(
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
    continuous_1031_1050 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1031, 1051)
    )
    untouched_1011_1030 = all(f"SA_{i}" not in GOLD for i in range(1011, 1031))

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1031–SA_1050 only)")
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
    print(f"continuous_gold_SA_1031–1050={continuous_1031_1050}")
    print(f"SA_1011–1030_untouched={untouched_1011_1030}")
    if boundary_id:
        print(f"{boundary_id}_untouched=True")
    else:
        print("SA_1030_boundary_skipped (not yet gold)")
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
