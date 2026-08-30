#!/usr/bin/env python3
"""Retranslate SA 1331–1350（卷第五十 林相应：不乐～波吒利）→ merge.

本批二十经（林相应 Vanasaṁyutta）：
1331–1335 不乐 SN9.4、睡眠 SN9.2、远离 SN9.1、倒净 SN9.11、安住 SN1.15／SN9.12
1336–1340 阇利那 SN9.6、诵习 SN9.10、花 SN9.14、迦叶 SN9.3、跋耆子 SN9.9
1341–1344 非比丘法 SN9.5、龙与 SN9.7、众多比丘 SN2.25／SN9.13、嬉戏 SN9.8
1345–1350 见多、睡眠、味、离林、优楼鸟、波吒利（SC 无可靠专经）

信：有 SN 平行者据巴利／Sujato 厘义；无平行者降 medium。
达雅：白话与罗什风逐段对照；林天劝发公式压缩；sim 门限见 assess_gold。
禁「厌故不乐」→「厌故离贪」（本批多林天偈，无定型厌离句则不强插）。
边界：只合并 SA_1331–1350；不触碰 SA_1330、SA_1351（邻经）。
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

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

SUTTAS: dict[str, dict] = {}

# --- SA 1331 不乐（SN9.4 Sambahula）---------------------------------------
SUTTAS["SA_1331"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有众多比丘于拘萨罗人间，住一林中夏安居。彼林中天神知十五日诸比丘受岁，深生忧戚。"
        "余天神语之曰：「汝何卒生愁忧？当喜比丘持戒清净，今日受岁。」"
        "林神答言：「我知今日受岁，不同无惭外道。然精进比丘受岁已，持衣钵，明日当去，此林当空。」",
        "比丘去后，林神说偈：「今我心不乐，但见空林树；清辩多闻众，瞿昙诸弟子，今悉何处去？」"
        "异天子说偈：「或至摩伽陀，或至拘萨罗，或在跋耆地，处处修远离；犹如野禽兽，随乐而无家。」",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有许多比丘在拘萨罗人间，住在一座林中过夏安居。林中的天神知道十五日比丘们要受岁，心里非常忧愁。"
        "别的天神对他说：「你为什么忽然这么愁苦？应当欢喜——比丘们持戒清净，今天受岁。」"
        "林神回答：「我知道今天受岁，和那些无惭的外道受岁不同。可是精进的比丘受岁之后，会拿着衣钵，明天就到别处去，这座林子就要空了。」",
        "比丘们离开后，林神说偈：「今天我心里不乐，只看见空空的林木；那些心净善说法、多闻的比丘，瞿昙的弟子们，如今都到哪里去了？」"
        "另一位天子说偈：「有的到了摩伽陀，有的到了拘萨罗，有的在跋耆地，处处修习远离；就像野兽一样，随所乐而无家。」",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.4。"
        "信-校正：汉「金刚地」据巴利 vajjibhūmiyā 作「跋耆地」；"
        "「不乐」＝arati（不乐／不满），非 virāga，偈中存「不乐」不改「离贪」。"
        "汉有受岁问答为汉本增广，巴利直叙安居竟即遊行，叙事情节存汉而义据 SN。"
    ),
}

# --- SA 1332 睡眠（SN9.2 Upaghāna／Niddā）---------------------------------
SUTTAS["SA_1332"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住一林中，昼入正受，身极疲怠，夜则睡眠。"
        "林中天神念：「此非比丘法——空林正受而夜著睡眠，我当往觉悟之。」即说偈言：",
        "「比丘宜速起，何以著睡眠？病箭刺身时，睡眠复何益？"
        "汝本信出家，当增彼信乐；莫为睡眠伏，令心不自在。"
        "欲乐无常住，愚夫迷醉之；余人犹被缚，汝已得解脱——正信而出家，何得著睡眠？"
        "已伏贪欲心，慧净超无明；漏尽无忧恼，出家何故眠？"
        "精进常坚固，专求于涅槃；起明断无明，调此最后身——云何著睡眠？」",
        "比丘闻已，专精思惟，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗人间，住在一座林中，白天入定，身体非常疲倦，夜里就睡着了。"
        "林中的天神心想：「这不是比丘该做的——在空林里入定却夜里贪睡，我应当去唤醒他。」便说偈：",
        "「比丘，快起来！为什么贪睡？被病箭射中时，睡眠有什么好处？"
        "你本因信而出家，应当增长那份信乐；不要被睡眠制服，让心不得自在。"
        "欲乐无常不定，愚夫仍迷醉其中；别人还被绑着，你已经解脱——正信出家，怎么还贪睡？"
        "已调伏贪欲，以智超越无明；漏尽无忧，出家为什么睡？"
        "精进、坚定，一心求涅槃；生起明慧断无明，调御这最后之身——怎么还贪睡？」",
        "比丘听了，专精思惟，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.2。"
        "巴利后半「何以烦扰出家者」诸偈，汉本统归天神劝进且结以得罗汉；"
        "义据 SN（无常欲、离贪、断无明、精进求涅槃），叙次存汉。"
        "「正受」＝昼禅／入定（divāvihāra）。"
    ),
}

# --- SA 1333 远离（SN9.1 Viveka）------------------------------------------
SUTTAS["SA_1333"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗林中，昼入正受，心起不善觉，依于恶贪。"
        "林中天神念：「非比丘法——住林正受而起不善觉、依恶贪，我当往开悟。」即说偈言：",
        "「汝欲修远离，乃住空闲林；而心随外缘，乱想驰不息。"
        "当伏乐世心，常乐心解脱；舍彼不乐想，安住寂静乐。"
        "正念莫散乱，勿著我我所；欲尘深难渡，莫令欲所漂。"
        "如鸟振尘土，精进正念者，亦当振欲尘——尘谓贪瞋痴，非世间土尘；"
        "于如来法律，持心莫放逸。」",
        "比丘闻已，专精思惟，断诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗的林中，白天入定，心里生起不善的寻思，依着恶贪。"
        "林中的天神心想：「这不是比丘该做的——住在林中入定，却生不善寻思、依着恶贪，我应当去开导他。」便说偈：",
        "「你想修远离，才住进空闲林；可心却随外境，乱想奔驰不停。"
        "应当调伏乐著世间的心，常乐于心解脱；舍掉不乐的想法，安住在寂静之乐。"
        "保持正念，不要散乱，不要执著我、我所；欲的尘垢深而难渡，不要被欲漂走。"
        "就像鸟抖落尘土，精进而正念的人，也应当抖落欲尘——所谓尘，是贪、瞋、痴，不是世间的土尘；"
        "在如来的法律中，把持其心，不要放逸。」",
        "比丘听了，专精思惟，断除烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.1。"
        "巴利偈较短（舍人欲、舍不乐、欲尘、振尘）；汉广开贪瞋痴三尘，义不违，存汉广说而压缩罗什风。"
        "「不善觉／恶贪」据 SN pāpake akusale vitakke … gehanissite（依家居之不善寻）。"
    ),
}

# --- SA 1334 倒净（SN9.11 Ayoniso）----------------------------------------
SUTTAS["SA_1334"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住一林中，昼入正受，起非理作意。"
        "林中天神念：「此非比丘法，我当方便觉悟之。」即说偈言：",
        "「以非理作意，故为觉观食；当舍非理念，修习如理观。"
        "念佛、法、僧宝，及自所持戒；则生欢喜心，喜乐转增胜；"
        "喜心充满故，速得尽苦边。」",
        "比丘闻已，专精思惟，尽诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗人间，住在一座林中，白天入定，却作非理作意。"
        "林中的天神心想：「这不是比丘该做的，我应当方便唤醒他。」便说偈：",
        "「因为非理作意，你被寻伺所吞噬；应当舍非理之念，修习如理的思惟。"
        "忆念佛、法、僧，以及自己所受持的戒；就会生起欢喜，喜乐愈来愈增胜；"
        "喜心充满，就能迅速到达苦的尽头。」",
        "比丘听了，专精思惟，尽诸烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.11。"
        "信-校正：汉「不正思惟／不正念」据巴利 ayoniso manasikāra 作「非理作意／非理念」；"
        "「如理观」＝yoniso anucintaya。SN 明示欲、恚、害寻，汉略，义据 SN 补于 notes。"
        "「倒净」题名存卷目；正文不用后出「净倒」玄学义。"
    ),
}

# --- SA 1335 安住（SN1.15／近 SN9.12）-------------------------------------
SUTTAS["SA_1335"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘于拘萨罗人间，住一林中，昼入正受。日中时，不乐心生，说偈言："
        "「日中鸟声寂，空林忽作响，令我心生怖。」",
        "林中天神说偈答：「日中鸟声寂，空林自作响——此响令我悦。"
        "汝当舍不乐，专修于正受。」",
        "比丘闻已，专精思惟，舍诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗人间，住在一座林中，白天入定。到了正午，心里生起不乐，说偈："
        "「正午众鸟静默，空林忽然响起声音，使我心里害怕。」",
        "林中的天神用偈回答：「正午众鸟静默，空林自己响起声音——这声音使我感到喜悦。"
        "你应当舍掉不乐，专心修习正定。」",
        "比丘听了，专精思惟，舍离烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.15（及林相应近经 SN9.12）。"
        "信-校正：汉「应汝不乐心」据巴利 sā rati paṭibhāti maṁ"
        "（空林之响于我为可喜）改作天神自陈「此响令我悦」；"
        "劝舍 arati（不乐）而修定，与 SN 一致。"
    ),
}

# --- SA 1336 阇利那（SN9.6 Anuruddha）------------------------------------
SUTTAS["SA_1336"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时尊者阿那律陀在拘萨罗人间，住一林中。"
        "有天神名阇邻尼，是尊者本善知识，来诣其所，说偈言："
        "「当愿生本处，三十三天上；五欲悉具足，天女常围绕。」",
        "尊者说偈答：「天女大苦聚，著有身见故；求生彼趣者，亦复是大苦。"
        "阇邻尼当知：我不乐生彼。生死已永尽，不受于后有。」",
        "阇邻尼闻已，欢喜随喜，即没不现。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者阿那律陀在拘萨罗人间，住在一座林中。"
        "有一位天神名叫阇邻尼，是尊者从前的善知识，来到他那里，说偈："
        "「你应当发愿回到本处，生在三十三天；五欲都具足，天女常常围绕。」",
        "尊者用偈回答：「天女其实是大苦聚，因为执著有身见；那些想生到那里的人，同样是大苦。"
        "阇邻尼你应当知道：我不愿生到那里。我的生死已经永尽，不再受后有。」",
        "阇邻尼听了，欢喜随喜，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.6。"
        "巴利尚有欢喜园往复及「诸行无常」偈，汉本较略；核心拒天欲、尽后有与 SN 合，不臆补欢喜园段。"
        "「阇邻尼」＝Jālinī；「有身见」＝sakkāyadiṭṭhi。"
    ),
}

# --- SA 1337 诵习（SN9.10 Sajjhāya）---------------------------------------
SUTTAS["SA_1337"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有比丘在拘萨罗林中，先勤诵经、讲说；精勤思惟，得阿罗汉已，不复勤于诵说。",
        "林中天神说偈：「比丘汝先时，昼夜勤诵习，常与诸比丘，共论决定义；"
        "今于诸法句，寂然无所说。」",
        "比丘说偈答：「本未离欲时，心乐于法句；既与离欲会，诵说事已毕。"
        "所见所闻思，已知而放舍——圣说为尽舍。」",
        "天神闻已，欢喜随喜，即没不现。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗的林中，原先勤于诵经、讲说；精勤思惟，证得阿罗汉之后，不再勤于诵说。",
        "林中的天神说偈：「比丘，你从前昼夜勤诵，常和比丘们一起讨论决定的法义；"
        "现在对于法句，却沉默什么也不说。」",
        "比丘用偈回答：「我还没有离欲的时候，心里喜爱法句；一旦与离欲相应，诵说的事便已完毕。"
        "凡所见、所闻、所思，已经了知而放下——圣者说这叫做尽舍。」",
        "天神听了，欢喜随喜，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.10。"
        "信-校正：结句据巴利 yaṁ kiñci diṭṭhaṁva sutaṁ mutaṁ vā; aññāya nikkhepanamāhu santo"
        "作「所见所闻思，已知而放舍」；汉「无知悉放捨」易误读，据 SN 校正。"
    ),
}

# --- SA 1338 花（SN9.14 Gandhatthena）------------------------------------
SUTTAS["SA_1338"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗林中，患眼病，师教令嗅莲花香。比丘至莲池岸，迎风坐，随风嗅香。"
        "主池天神语之曰：「汝不与而取香，是则盗香贼！」",
        "比丘说偈：「不坏亦不夺，远住但嗅香；云何名为贼？」"
        "天神曰：「人不与而取，世说以为贼；嗅香亦如是，名为盗香贼。」",
        "时有人掘藕、折花负去。比丘曰：「彼毁花取根，汝何不责之？」"
        "天神曰：「粗恶毁法人，如垢衣难语；无染求净者，纤恶如大云——宜责于汝。」",
        "比丘曰：「善哉善安慰！愿数数为我说。」"
        "天神曰：「我非汝仆使；汝当自了知，趣向于善道。」",
        "比丘闻已，欢喜随喜，独静思惟，断诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗的林中，患了眼病，老师教他嗅莲花香。比丘来到莲池岸边，迎风而坐，随风嗅香。"
        "主管水池的天神对他说：「你没有被给予却取用香气，这就是盗香的贼！」",
        "比丘说偈：「我不毁坏也不抢夺，只是远远地嗅香；怎么能叫做贼？」"
        "天神说：「别人不给而自己取，世间就称为贼；嗅香也是这样，叫做盗香贼。」",
        "这时有人掘藕、折花背走。比丘说：「那人毁花取根，你为什么不责备他？」"
        "天神说：「对粗暴作恶的人，就像对脏衣服，不值得多说；对无染而求清净的人，细小的过恶也像大云那样显眼——所以该提醒的是你。」",
        "比丘说：「说得好，谢谢你的安慰！愿你常常这样提醒我。」"
        "天神说：「我不是你的仆役；你自己应当了知，什么是趋向善道。」",
        "比丘听了，欢喜随喜，独自静思，断除烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.14。"
        "汉有眼患／师教因缘，巴利为食后入池嗅花；因缘存汉，对答义据 SN"
        "（不与取香、不问粗恶者、毛端之恶如云、自知善道）。"
    ),
}

# --- SA 1339 迦叶（SN9.3 Kassapagotta）-----------------------------------
SUTTAS["SA_1339"] = {
    "lit": [
        OPEN_BAM_LIT,
        "尔时尊者十力迦叶住王舍城仙人窟中。去之不远，猎师尺只张网捕鹿。"
        "尊者为哀愍故而为说法，猎师不解；即以神力，指端出火，彼犹不悟。",
        "窟中天神说偈：「深山中猎师，少智盲无目；非时而为说，如愚不入心。"
        "闻而不解义，视而不见法；正使十指燃，彼终不见谛。」",
        "尊者十力迦叶即默然住。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "那时尊者十力迦叶住在王舍城仙人窟中。不远处，猎师尺只张网捕鹿。"
        "尊者出于哀愍而为他说法，猎师却听不懂；尊者便以神通让指端出火，他仍然不觉悟。",
        "窟中的天神说偈：「深山里的猎师，少智如同盲人；不在适当的时候说法，他愚昧听不进去。"
        "听了也不懂意思，看了也不见法；即使十指都燃起火，他也终究见不到真理。」",
        "尊者十力迦叶于是默然安住。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.3。"
        "巴利场景在拘萨罗林、劝猎师（cheta）；汉在仙人窟／尺只捕鹿，存汉地名人物。"
        "「非时说」＝akāle ovadaṁ；结以尊者默然，与 SN 生起紧迫感同向。"
    ),
}

# --- SA 1340 跋耆子（SN9.9 Vajjiputta）-----------------------------------
SUTTAS["SA_1340"] = {
    "lit": [
        OPEN_BAM_LIT,
        "时尊者金刚子住巴连弗邑林中。邑人夏四月过，作憍牟尼大会。"
        "尊者闻世间大会，生不乐心，说偈：「独住空林中，犹如弃枯木；"
        "夏满世欢会，观苦无过我。」",
        "林中天神说偈：「独住空林中，犹如弃枯木——三十三天众，常所愿乐处；"
        "如地狱仰望，得生人道中。」",
        "尊者闻已，专精思惟，断诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "那时尊者金刚子住在巴连弗邑的林中。城里人过了夏四月，举办憍牟尼大会。"
        "尊者听见世间的大会，心里生起不乐，说偈：「独自住在空林，像被丢弃的枯木；"
        "夏天满了，世人欢会，我看世上的苦，没有比我更苦的。」",
        "林中的天神说偈：「独自住在空林，像被丢弃的枯木——这正是三十三天众常常向往的地方；"
        "就像地狱里的众生仰望，希望能生到人道。」",
        "尊者听了，专精思惟，断除烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.9。"
        "巴利为跋耆比丘住毗舍离、跋耆人彻夜节会；汉作金刚子／巴连弗／憍牟尼会，存汉专名。"
        "义据 SN：空林独处为天所羡慕，非真苦。"
    ),
}

# --- SA 1341 非比丘法（SN9.5 Ānanda；汉异）--------------------------------
SUTTAS["SA_1341"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者阿难在拘萨罗人间，住一林中，多与白衣从事说法，往返繁密。"
        "林中天神哀愍，欲令觉悟，说偈言：",
        "「入林依树根，涅槃置心首；禅思莫放逸，勿多与俗交。"
        "扬尘之欲染，能坏禅定心；硬土不生树，欲染不生禅。」",
        "尊者阿难为天神所劝，专精思惟，远离散乱。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者阿难在拘萨罗人间，住在一座林中，常常为在家人说法，来往很密。"
        "林中的天神出于哀愍，想使他警觉，便说偈：",
        "「进入树林，依止树根，把涅槃放在心上最前；修禅不要放逸，不要过多与俗人交往。"
        "扬起尘土的欲染，会破坏禅定；坚硬的土长不出树，欲染之中生不出禅定。」",
        "尊者阿难被天神劝勉后，专精思惟，远离散乱。",
    ],
    "notes": (
        f"{PROV}confidence=medium：SC 列 SN9.5（Ānanda），巴利呵阿难过多劝化白衣、妨禅；"
        "汉本作「唯乐持戒、不增上进」，叙事异。依项目「巴利优先」，正文据 SN9.5 重构，"
        "汉「偏持戒」异叙事不采用。gold_reconstructed。"
    ),
}

# --- SA 1342 龙与（SN9.7 Nāgadatta）--------------------------------------
SUTTAS["SA_1342"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者那迦达多在拘萨罗林中，晨入聚落过早，暮还过晚，与在家、出家周旋亲昵。",
        "林中天神念：「此非比丘法。」即说偈：「晨出暮乃归，道俗相习近；"
        "苦乐与之同，恐随家放逸，而堕魔所摄。」",
        "尊者如是觉悟已，专精思惟，断诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "尊者那迦达多在拘萨罗的林中，早晨进村太早，傍晚回来太晚，与在家人、出家人交往过密。",
        "林中的天神心想：「这不是比丘该做的。」便说偈：「清早出去，很晚才回林，和道俗过分亲近；"
        "苦乐都跟他们同一条心，恐怕会随着居家放逸，而落入魔的掌控。」",
        "尊者这样被唤醒之后，专精思惟，断除烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.7。"
        "「那迦达多」＝Nāgadatta；早出晚归、亲近居家与 SN 合。"
    ),
}

# --- SA 1343 众多比丘（SN2.25／SN9.13）------------------------------------
SUTTAS["SA_1343"] = {
    "lit": [
        OPEN_JET_LIT,
        "时众多比丘在拘萨罗林中，言语嬉戏，终日散乱，不摄诸根。"
        "林中天神不喜，说偈：「昔瞿昙弟子，无常想乞食，无常想坐卧；"
        "观世无常故，得究竟苦边。今此难养众，驰求于诸家；"
        "披衣如老牛，徒曳尾而行。」",
        "比丘问：「汝欲厌我耶？」天神曰：「不举名姓，不责一人；"
        "总说众中过，令漏者自省；精进修行者，我则归命礼。」",
        "诸比丘闻已，专精思惟，断诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有许多比丘在拘萨罗的林中，说说笑笑，整天散乱，不收摄根门。"
        "林中的天神不高兴，说偈：「从前瞿昙的弟子，以无常想去乞食，以无常想受用床卧；"
        "因为观察世间无常，得至于苦的尽头。现在这些难养的人，到处向人家奔走求食；"
        "披着袈裟像老牛，只是拖着尾巴走。」",
        "比丘们问：「你是要厌弃我们吗？」天神说：「我不点名道姓，也不单责某一个人；"
        "只是总说大众中的过失，让有漏失的自己反省；对精进修行的人，我仍然归命礼敬。」",
        "比丘们听了，专精思惟，断除烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.25（及 SN9.13 同主题）。"
        "汉「垂著僧伽梨，如老牛曳尾」与 SN 散乱比丘之呵责同向；存汉譬。"
    ),
}

# --- SA 1344 嬉戏（SN9.8 Kulagharaṇī）------------------------------------
SUTTAS["SA_1344"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗林中，与长者妇过从，恶名流布。比丘念：「我不类，宁自杀。」",
        "林中天神念：「此比丘实无破戒大过，而欲自害，我当方便开悟。」"
        "化作长者女，语比丘言：「里巷已为我与汝作恶名，可还俗共相娱乐。」"
        "比丘曰：「既有恶名，我当自杀！」",
        "天神复天身，说偈：「多闻恶名者，苦行当堪忍；不应自逼恼。"
        "闻声即怖者，如林中野兽，不成出家法。心坚住忍者，乃名真出家。"
        "他语不能使汝成盗，亦不能使他语令汝成罗汉；如汝自知，诸天亦知。」",
        "比丘闻已，专精思惟，断诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗的林中，与长者的妇女来往过密，恶名传开。比丘心想：「我不像话，宁可自杀。」",
        "林中的天神心想：「这位比丘其实没有破戒的大过，却想自杀，我应当方便开导。」"
        "便化作长者女，对比丘说：「街坊已经给我们编了恶名，不如还俗一起享乐。」"
        "比丘说：「既然已有恶名，我应当自杀！」",
        "天神恢复天身，说偈：「听到许多恶名，修行人应当忍耐；不该自己折磨自己。"
        "一听见声音就害怕，像林中的野兽，那不成出家法。内心坚定能忍耐的，才是真正的出家。"
        "别人的话不能把你变成盗贼，也不能单靠别人的话使你成为阿罗汉；你自己怎样知道，诸天也怎样知道。」",
        "比丘听了，专精思惟，断除烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN9.8。"
        "巴利天神化作家主妇激将；汉有自杀情节为汉本增，义据 SN「忍恶名、莫自害」。"
        "禁将「不乐」与 virāga 定型混读；本经「恶名」非厌离道次第。"
    ),
}

# --- SA 1345 见多（无专经）-----------------------------------------------
SUTTAS["SA_1345"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者见多在拘萨罗林中，著粪扫衣。梵天王与七百梵天乘宫殿，来诣其所，恭敬礼事。",
        "林中天神说偈：「观彼诸根寂，能感胜供养；三明已具足，得不动之法。"
        "少事粪扫衣，七百梵天子，乘宫来奉敬；已见有边际，稽首度有岸。」",
        "说是偈已，即没不现。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者见多在拘萨罗的林中，穿着粪扫衣。梵天王与七百梵天乘着宫殿，来到他那里恭敬礼拜。",
        "林中的天神说偈：「看他诸根寂静，能感得殊胜的供养；三明已经具足，证得不动之法。"
        "事务很少，穿着粪扫衣，七百梵天子乘宫殿前来礼敬；他已见到有的边际，我顶礼这位度到有岸的人。」",
        "说完这偈，随即隐没不见。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；粪扫衣／三明／梵天来诣与早期罗汉德赞同轨，不臆造平行编号。"
    ),
}

# --- SA 1346 睡眠（无专经；近 SN9.2 主题）---------------------------------
SUTTAS["SA_1346"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗林中，身疲夜眠。林中天神觉悟之，说偈：「起起，比丘！睡眠何义？修禅莫眠。」",
        "比丘曰：「懈怠少方便，四体既羸瘦，夜则著睡眠。」"
        "天神曰：「当自守护，莫大声呼；已得闲静，莫令退失。」"
        "比丘曰：「我当用汝语，精勤不随眠。」",
        "如是屡劝，比丘专精，断诸烦恼，得阿罗汉。即说偈言：「七夜常端坐，身生喜充满；"
        "初夜观宿命，中夜天眼净，后夜破无明，见众生苦乐。」"
        "天神复记：先有十四须陀洹当来此林证果，以一懈怠故方便觉悟。比丘随喜；"
        "天神誓于疾病时与药，说已没不现。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗的林中，身体疲倦，夜里贪睡。林中的天神唤醒他，说偈：「起来，起来，比丘！睡眠有什么意义？修禅不要睡。」",
        "比丘说：「我懈怠、方法少，四肢又瘦弱，夜里就贪睡。」"
        "天神说：「应当自己守护，不要大喊大叫；已经得到闲静，不要让它退失。」"
        "比丘说：「我听从你的话，精勤不跟着睡眠转。」",
        "这样多次劝勉后，比丘专精努力，断除烦恼，证得阿罗汉。便说偈：「七夜常常端坐，身上充满喜乐；"
        "初夜观察宿命，中夜天眼清净，后夜破除无明，得见众生的苦与乐。」"
        "天神又说：从前有十四位须陀洹会到这座林中证果，因为看到他一个人懈怠，才方便唤醒。比丘随喜；"
        "天神又说若他生病会给良药。说完便隐没不见。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；主题近 SN9.2 劝离睡眠，而有十四须陀洹／与药等汉本独有细节，保守存汉。"
    ),
}

# --- SA 1347 味（无专经）-------------------------------------------------
SUTTAS["SA_1347"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者舍利弗在拘萨罗人间，依聚落田侧而住。晨著衣持钵入村乞食。",
        "有尼揵子酒醉，持酒瓶出，见尊者说偈：「米膏熏我身，持瓶而行；山河草木，视作金色。」",
        "尊者念：「恶邪作此声，我岂不能答？」即说偈：「无想定所熏，持空三昧瓶；"
        "山河草木，视之如涕唾。」",
    ],
    "mod": [
        OPEN_JET_MOD,
        "尊者舍利弗在拘萨罗人间，依着一处聚落的田边住。清晨穿衣持钵进村乞食。",
        "有一个尼揵子喝醉了，拿着酒瓶出来，看见尊者说偈：「米酒的气味熏着我的身体，我拿着酒瓶走；山河草木，看起来一片金色。」",
        "尊者心想：「这种恶邪发出这样的声音，我难道不能回答吗？」便说偈：「无想定熏习我，我持着空三昧之瓶；"
        "山河草木，在我看来如同涕唾。」",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；醉酒外道与空三昧对举，早期禅喻可解，不臆造 SN 编号。"
        "「无想／空三昧」按汉本禅定语境理解，不作后有部专名发挥。"
    ),
}

# --- SA 1348 离林（无专经）-----------------------------------------------
SUTTAS["SA_1348"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗林中，得他心智，而烦恼有余。林边有井，野干为汲水罐钩颈，求脱不得，"
        "念：「天欲明，田夫将出，此罐怖我久矣，愿得脱！」",
        "比丘知其心，说偈：「如来慧日出，离林说空法；久怖今可放。」"
        "自说是教已，一切结尽，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位比丘在拘萨罗的林中，已得他心智，但烦恼还有剩余。林边有井，一只野干被汲水罐钩住脖子，怎么也脱不开，"
        "心想：「天快亮了，农夫就要出来，这水罐惊吓我很久了，但愿能脱身！」",
        "比丘知道它的心，说偈：「如来的智慧如日升起，出离树林说空法；长久的恐怖，现在可以放开了。」"
        "他对自己说了这番教诫之后，一切结使尽除，证得阿罗汉。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；野干钩颈喻自心系缚，比丘以「离林说空」自教而证果，保守依汉。"
    ),
}

# --- SA 1349 优楼鸟（无专经）---------------------------------------------
SUTTAS["SA_1349"] = {
    "lit": [
        "如是我闻：一时，佛在拘萨罗人间遊行，住一林中。",
        "林中天神见佛行迹，低头谛观，修念佛。时有鸺鹠欲蹈佛足迹。"
        "天神说偈：「鸺鹠团目鸟，栖止在树间；莫乱如来迹，坏我念佛境。」"
        "说是偈已，默然念佛。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在拘萨罗人间遊行，住在一座林中。",
        "林中的天神看见佛的足迹，低头仔细观看，修习念佛。这时有一只鸺鹠想踏佛的足迹。"
        "天神说偈：「团眼的鸺鹠鸟，栖息在树间；不要扰乱如来的足迹，破坏我念佛的境界。」"
        "说完这偈，默默地念佛。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；「念佛」＝早期 buddhānussati（念佛功德），非净土称名。"
        "「优楼」＝鸺鹠一类。"
    ),
}

# --- SA 1350 波吒利（无专经）---------------------------------------------
SUTTAS["SA_1350"] = {
    "lit": [
        "如是我闻：一时，佛在拘萨罗人间，住一林中，依波吒利树下。",
        "林中天神说偈：「今日风卒起，吹波吒利树；花落以缤纷，供养于如来。」"
        "说是偈已，默然而住。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在拘萨罗人间，住在一座林中，依止波吒利树下。",
        "林中的天神说偈：「今天风忽然刮起，吹动波吒利树；花纷纷落下，供养如来。」"
        "说完这偈，默然而住。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经；波吒利＝pāṭali（紫矿／喇叭花树），存音译。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE: dict[str, str] = {
    "SA_1331": "high",
    "SA_1332": "high",
    "SA_1333": "high",
    "SA_1334": "high",
    "SA_1335": "high",
    "SA_1336": "high",
    "SA_1337": "high",
    "SA_1338": "high",
    "SA_1339": "high",
    "SA_1340": "high",
    "SA_1341": "medium",
    "SA_1342": "high",
    "SA_1343": "high",
    "SA_1344": "high",
    "SA_1345": "medium",
    "SA_1346": "medium",
    "SA_1347": "medium",
    "SA_1348": "medium",
    "SA_1349": "medium",
    "SA_1350": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1341": "汉本「唯乐持戒」与 SN9.5 阿难多化白衣异；据 SN9.5 重构林天劝禅、勿多俗交。",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

BATCH_IDS = [f"SA_{i}" for i in range(1331, 1351)]
PARALLEL_BATCH_IDS = {f"SA_{i}" for i in range(1311, 1331)} | {
    f"SA_{i}" for i in range(1351, 1371)
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
    # Hard neighbors called out by the task
    hard_neighbors = {"SA_1330", "SA_1351"}
    hard_before = {
        rec["id"]: _snap(rec) for rec in records if rec["id"] in hard_neighbors
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
    for rid, before in hard_before.items():
        for rec in merged:
            if rec["id"] == rid:
                assert before == _snap(rec), f"{rid} (hard neighbor) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1331-1350.json").write_text(
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1331, 1351)
    )
    untouched_neighbors = all(
        f"SA_{i}" not in GOLD for i in list(range(1311, 1331)) + list(range(1351, 1371))
    )
    hard_ok = (
        by_merged["SA_1330"]["review_status"] == hard_before["SA_1330"]
        or _snap(by_merged["SA_1330"]) == hard_before["SA_1330"]
    ) and (
        _snap(by_merged["SA_1351"]) == hard_before["SA_1351"]
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1331–SA_1350 only)")
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
    print(f"continuous_1331_1350_goldish={continuous}")
    print(f"neighbors_1311-1330_and_1351-1370_untouched={untouched_neighbors}")
    print(f"SA_1330_SA_1351_untouched={hard_ok}")
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
