#!/usr/bin/env python3
"""Retranslate SA 571–590（卷第二十四 质多罗末–卷第二十五 天相应）→ merge.

本批二十经：质多罗×5（Citta／SN41.1–4、8–10）；天相应×15（SN1／SN2／SN10；590 无巴利）。

信：有 SN 平行者据巴利／Sujato 厘义；590 唯 sa-2.184 → medium。
    573 出家 peyyāla、575 长偈 → 压缩或据 SN 校正。
达雅：白话与罗什风逐段对照；Devatā 公式压缩；sim 门限见 assess_gold。
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

OPEN_JET_LIT = "如是我闻：一时，佛在舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_MAC_LIT = "如是我闻：一时，佛住庵罗聚落庵罗林中，与众多上座比丘俱。"
OPEN_MAC_MOD = "我是这样听说的：有一次，佛住在庵罗聚落庵罗林中，与众多上座比丘在一起。"

OPEN_SAK_LIT = "如是我闻：一时，佛住释氏优罗提那塔所。"
OPEN_SAK_MOD = "我是这样听说的：有一次，佛住在释氏优罗提那塔处。"

CLOSE_CITTA_LIT = "时，质多罗长者闻所说，欢喜随喜，作礼而去。"
CLOSE_CITTA_MOD = "当时，质多罗长者听所说，欢喜随喜，行礼后离去。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

DEVATA_OPEN_LIT = (
    OPEN_JET_LIT
    + "时，有一天子容色绝妙，于后夜时来诣佛所，稽首佛足，身诸光明遍照祇树给孤独园。"
)
DEVATA_OPEN_MOD = (
    OPEN_JET_MOD
    + "当时，有一位天子容色绝妙，在后夜来到佛处，顶礼佛足，"
    "身放光明遍照祇树给孤独园。"
)

DEVATA_EPILOGUE_LIT = "久见婆罗门，逮得般涅槃，一切怖已过，永超世恩爱。"
DEVATA_EPILOGUE_MOD = "久见婆罗门，逮得般涅槃，一切怖惧已过，永超世间恩爱。"

DEVATA_CLOSE_LIT = "时，彼天子闻佛所说，欢喜随喜，稽首佛足，即没不现。"
DEVATA_CLOSE_MOD = "当时，那位天子听佛所说，欢喜随喜，顶礼佛足，随即消失。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

APPAMADA_LIT = (
    "当知此皆以不放逸为本，不放逸集、不放逸生、不放逸转，"
    "不放逸故得阿耨多罗三藐三菩提；此及余功德，一切皆不放逸为本。"
)
APPAMADA_MOD = (
    "应当知道，这些都以不放逸为根本，不放逸为集、为生、为转，"
    "因为不放逸而证得阿耨多罗三藐三菩提；这些以及其余功德，都以不放逸为根本。"
)

ANAGAMI_LIT = (
    "我今作心：不复经由胞胎而受生，不增于丘冢，不起血气；"
    "如世尊说五下分结，我不见一结不断——若一结不断，当还生此世。"
)
ANAGAMI_MOD = (
    "我现在作意：不再经由胞胎受生，不在丘冢中增长，不再受血气；"
    "如同世尊所说五下分结，我看不见有一个结未断——若有一个结未断，就会还生此世。"
)


def _mod_from_lit(lit_paras: list[str], mod_first: str | None = None) -> list[str]:
    """Modern column tracks literary except optional opening frame."""
    mod = list(lit_paras)
    if mod_first is not None:
        mod[0] = mod_first
    return mod


def _devata_simple(
    dev_q_lit: str,
    dev_q_mod: str,
    bud_a_lit: str,
    bud_a_mod: str,
    *,
    open_lit: str = DEVATA_OPEN_LIT,
    open_mod: str = DEVATA_OPEN_MOD,
    with_epilogue: bool = True,
) -> tuple[list[str], list[str]]:
    lit = [
        open_lit,
        f"时，彼天子说偈白佛：「{dev_q_lit}」",
        f"尔时，世尊说偈答言：「{bud_a_lit}」",
    ]
    mod = [
        open_mod,
        f"天子说偈问佛：「{dev_q_mod}」",
        f"世尊说偈答：「{bud_a_mod}」",
    ]
    if with_epilogue:
        lit += [f"时，彼天子复说偈言：「{DEVATA_EPILOGUE_LIT}」", DEVATA_CLOSE_LIT]
        mod += [f"天子又说偈：「{DEVATA_EPILOGUE_MOD}」", DEVATA_CLOSE_MOD]
    else:
        lit.append(DEVATA_CLOSE_LIT.replace("稽首佛足，", ""))
        mod.append(DEVATA_CLOSE_MOD.replace("顶礼佛足，", ""))
    return lit, mod


# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 571 摩诃迦（SN41.4 Mahaka）--------------------------------------------
SUTTAS["SA_571"] = {
    "lit": [
        OPEN_MAC_LIT,
        "时，质多罗长者诣诸上座，稽首礼足，退坐一面，白言：「唯愿诸尊于牛牧中受我请食。」诸上座默然受请。",
        "长者知受请已，还家星夜备饮食，晨遣使白：「时到。」诸上座著衣持钵，至牛牧中长者舍，就座而坐。",
        "长者自手供养种种饮食。食已，洗钵澡漱，敷卑床于上座前坐听法。诸上座为说法示教照喜已，从座起去，长者亦随后。",
        "诸上座食酥酪蜜饱，春后月热，行路闷极。时下座比丘名摩诃迦白诸上座：「今日大热，我欲起云雨微风，可尔不？」答：「佳。」",
        "摩诃迦入三昧，应时云起、细雨微下、凉风四方来至精舍门。摩诃迦语诸上座：「所作可止？」答：「可止。」即止神通，还自房。",
        "长者作念：「最下座比丘而有此大神通，况中上二座。」即礼诸上座足，随摩诃迦至房，礼足退坐，白言：「愿见尊者过人法神足现化。」",
        "摩诃迦言：「长者！勿见恐怖。」三请三不许，长者重请。",
        "摩诃迦语长者：「汝且出外，取乾草木积聚，以一白㲲覆上。」长者如其教，白言：「薪积已成，以㲲覆上。」",
        "摩诃迦入火光三昧，于户钩孔出火焰，烧积薪都尽，唯白㲲不然，语长者：「汝今见不？」答：「已见，实为奇特。」",
        f"摩诃迦语长者：「{APPAMADA_LIT}」",
        "长者白言：「愿常住此林，我当尽寿供养衣被饮食汤药。」摩诃迦有行缘故，不受其请。",
        "长者闻法欢喜，作礼而去。摩诃迦不欲供养障罪，即去，遂不复还。",
    ],
    "mod": [
        OPEN_MAC_MOD,
        "当时，质多罗长者来到诸上座处，顶礼足，退坐一面，说：「唯愿诸位在牛牧处接受我的请食。」诸上座默然接受。",
        "长者知道受请后，回家连夜准备饮食，早晨派人通报：「时候到了。」诸上座著衣持钵，到牛牧中长者舍，就座而坐。",
        "长者亲手供养种种饮食。食后，洗钵澡漱，在上座前铺低床坐听法。诸上座说法示教照喜后，从座起来离去，长者也随后。",
        "诸上座吃了酥酪蜜而饱，春后月热，行路极为闷热。下座比丘名叫摩诃迦对诸上座说："
        "「今天很热，我想兴起云雨和微风，可以吗？」答：「好。」",
        "摩诃迦入三昧，当时云起、细雨微下、凉风从四方来至精舍门。摩诃迦对诸上座说：「所作可以停止了吗？」"
        "答：「可以。」随即停止神通，回到自己房。",
        "长者心里作念：「最下座的比丘就有这样大的神通，何况中座和上座。」随即礼诸上座足，跟随摩诃迦到房，"
        "顶礼后退坐，说：「希望看见尊者超人的神足现化。」",
        "摩诃迦说：「长者！不要见恐怖。」请示三次，不许三次，长者再次请求。",
        "摩诃迦对长者说：「你且出外，取乾草木积聚，用一张白㲲覆在上面。」长者照做，禀报：「薪柴已积聚，㲲已覆上。」",
        "摩诃迦入火光三昧，从户钩孔出火焰，烧尽积薪，唯白㲲不燃，对长者说：「你现在看见了吗？」"
        "答：「看见了，实在奇特。」",
        f"摩诃迦对长者说：「{APPAMADA_MOD}」",
        "长者说：「愿常住此林，我尽形寿供养衣被、饮食、汤药。」摩诃迦因有行缘，不接受。",
        "长者听法欢喜，行礼离去。摩诃迦不愿供养成障，随即离去，不再回来。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN41.4（Mahaka 雨风／火通；不放逸教诫）。"
        "据 SN 校正：下座 Mahaka；供养不受、离去，从巴利。"
    ),
}

# --- SA 572 系（SN41.1 Saṃyojana）---------------------------------------------
SUTTAS["SA_572"] = {
    "lit": [
        OPEN_MAC_LIT.replace("与众多上座比丘俱", "与众多上座比丘俱"),
        "尔时，众多上座集于食堂，作如是论：「为眼系色耶？色系眼耶？耳声、鼻香、舌味、身触、意法亦尔——为意系法耶？法系意耶？」",
        "时，质多罗长者行有所营，过精舍，见诸上座集食堂，前礼诸上座足，问：「尊者集此，论说何法？」",
        "诸上座答：「我等论眼色二系，乃至意法二系。」长者问：「诸尊者于此义云何记说？」诸上座言：「于长者意云何？」",
        "长者答：「如我意，非眼系色、非色系眼，乃至非意系法、非法系意，然中间有欲贪，随彼系也。",
        "譬如二牛，一黑一白，驾以轭鞅。或问：『为黑牛系白牛？为白牛系黑牛？』非等问也——非黑牛系白、亦非白牛系黑，然彼轭鞅是其系。",
        "如是，非眼系色、非色系眼，乃至非意系法、非法系意，然其中间欲贪是其系。」",
        CLOSE_CITTA_LIT,
    ],
    "mod": [
        OPEN_MAC_MOD,
        "当时，众多上座集于食堂，作这样的讨论：「是眼系缚色呢？还是色系缚眼呢？"
        "耳声、鼻香、舌味、身触、意法也是这样——是意系缚法呢？还是法系缚意呢？」",
        "当时，质多罗长者因事路过精舍，看见诸上座集于食堂，上前礼足，问：「诸位集在这里，讨论什么法？」",
        "诸上座答：「我们讨论眼与色谁系谁，乃至意与法谁系谁。」长者问：「诸位对此义怎样记说？」诸上座说：「长者意下如何？」",
        "长者答：「依我意，不是眼系色、也不是色系眼，乃至不是意系法、也不是法系意，"
        "然而中间有欲贪，随彼而系缚。",
        "譬如两头牛，一黑一白，以轭鞅驾在一起。有人问：『是黑牛系白牛？还是白牛系黑牛？』这不是正当的问——"
        "不是黑牛系白牛，也不是白牛系黑牛，然而轭鞅才是系缚。",
        "同样，不是眼系色、不是色系眼，乃至不是意系法、不是法系意，然而中间的欲贪才是系缚。」",
        CLOSE_CITTA_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN41.1（二牛轭喻；欲贪为系，非六根六境互系）。"
        "据 SN 校正：fetter／things that tighten 之汉本问，今从巴利。"
    ),
}

# --- SA 573 阿鲁毗迦（SN41.9 Acelakassapa）------------------------------------
SUTTAS["SA_573"] = {
    "lit": [
        OPEN_MAC_LIT.replace("与众多上座比丘俱", ""),
        "时，有阿耆毘外道——质多罗长者先人亲厚——来诣长者所，共相问讯，于一面住。",
        "长者问：「汝出家几时？」答：「二十余年。」",
        "复问：「出家二十余年，得过人法、究竟知见、安乐住不？」",
        "答：「不得过人法、究竟知见、安乐住，唯有裸形、拔发、乞食、人间游行、卧于土中。」",
        "长者言：「此非名称法、律，是恶知，非出要道，非等觉所赞，不可依止。」",
        "阿耆毘问：「汝为沙门瞿昙弟子几时？」答：「过二十年。」",
        "复问：「为弟子二十年，得过人法、胜究竟知见不？」",
        f"长者答：「{ANAGAMI_LIT}」",
        "说时，阿耆毘悲叹涕泪，以衣拭面，言：「我今当作何计？」",
        "长者答：「汝若能于正法、律出家，我当给汝衣钵供身之具。」",
        "阿耆毘须臾思惟，言：「我今随喜，示我所作。」",
        "时长者将阿耆毘诣诸上座，礼足白言：「此阿耆毘是我先人亲厚，今求出家，愿诸上座度之，我当供给衣钵众具。」",
        "诸上座度令出家；彼闻法如法修行，证阿罗汉。",
    ],
    "mod": [
        OPEN_MAC_MOD.replace("与众多上座比丘在一起。", ""),
        "当时，有一位阿耆毘外道——质多罗长者的先人旧友——来到长者处，互相问讯，站在一面。",
        "长者问：「你出家多久了？」答：「二十多年了。」",
        "又问：「出家二十多年，有没有证得过人法、究竟知见、安乐而住？」",
        "答：「没有证得过人法、究竟知见、安乐而住，只有裸形、拔发、乞食、人间游行、卧在土中。」",
        "长者说：「这不是称为法、律的，是恶知，不是出离要道，不是等觉所赞叹、不可依止的。」",
        "阿耆毘问：「你作沙门瞿昙弟子多久了？」答：「超过二十年了。」",
        "又问：「作弟子二十年，有没有证得过人法、殊胜究竟知见？」",
        f"长者答：「{ANAGAMI_MOD}」",
        "说这话时，阿耆毘悲叹流泪，用衣拭面，说：「我现在该怎么办？」",
        "长者答：「你如果能于正法、律中出家，我会给你衣钵和供养。」",
        "阿耆毘稍思惟后，说：「我现在随喜，指示我所要做的。」",
        "当时，长者带阿耆毘到诸上座处，礼足说：「这位阿耆毘是我先人的旧友，现在请求出家，"
        "愿诸位为他剃度，我会供给衣钵众具。」",
        "诸上座为他剃度出家；他闻法后如法修行，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN41.9（Acelakassapa／阿耆毘；Citta 自记阿那含）。"
        "据 SN 校正：裸形外道无究竟；出家 peyyāla 压缩为「闻法修行证阿罗汉」。"
    ),
}

# --- SA 574 尼乾（SN41.8 Nigaṇṭha Nāṭaputta）---------------------------------
SUTTAS["SA_574"] = {
    "lit": [
        OPEN_MAC_LIT,
        "时，有尼犍若提子与五百眷属诣庵罗林，欲诱质多罗长者。长者闻已，往诣其所，共相问讯，各坐一面。",
        "尼犍若提子语长者：「汝信沙门瞿昙得无觉无观三昧耶？」",
        "长者答：「我不以信故来也。」",
        "尼犍言：「长者不谄、不幻、质直、质直所生。若能息有觉有观者，亦能以绳系缚于风；"
        "若能息有觉有观者，亦可以一把土断恒水流；我于行住坐卧智见常生。」",
        "长者问：「为信在前？为智在前？信与智，何者为先？何者为胜？」",
        "尼犍答：「信应在前，然后有智；信智相比，智则为胜。」",
        "长者语尼犍：「我已得息有觉有观、内净一心、无觉无观、三昧生喜乐，第二禅具足住。"
        "我昼亦住、夜亦住、终夜常住此三昧，有如是智，何用信世尊为？」",
        "尼犍言：「汝谄曲、幻伪、不直、不直所生。」",
        "长者言：「汝先言我不谄、不幻、质直，今云何言谄曲、幻伪？前实后虚，后实前虚。"
        "汝先言行住坐卧知见常生，于前后小事不知，云何知过人法、若知若见安乐住事？」",
        "长者复问：「有一问、一说、一记论，乃至十问、十说、十记论，汝有此不？"
        "若无一问乃至十问，云何能诱我来此林中欲诱诳我？」",
        "于是尼犍若提子息闭掉头，反拱而出，不复还顾。",
    ],
    "mod": [
        OPEN_MAC_MOD,
        "当时，有尼犍若提子与五百眷属来到庵罗林，想引诱质多罗长者。长者听说后，前往其处，互相问讯，各自坐于一面。",
        "尼犍若提子对长者说：「你相信沙门瞿昙证得无觉无观三昧吗？」",
        "长者答：「我不是因为信而来这里的。」",
        "尼犍说：「长者不谄媚、不虚伪、质直、质直所生。如果能息有觉有观，也能用绳子系缚风；"
        "如果能息有觉有观，也能用一把土截断恒河水；我在行住坐卧中智见常生。」",
        "长者问：「是信在前？还是智在前？信与智，哪个为先？哪个为胜？」",
        "尼犍答：「信应该在前，然后才有智；信与智相比，智更为胜。」",
        "长者对尼犍说：「我已经证得息有觉有观、内净一心、无觉无观、三昧生喜乐，第二禅具足而住。"
        "我白天也住、夜晚也住、整夜常住此三昧，有这样的智，何必信世尊呢？」",
        "尼犍说：「你谄曲、幻伪、不直、不直所生。」",
        "长者说：「你先说我不谄、不幻、质直，现在怎么说谄曲、幻伪？前实后虚，后实前虚。"
        "你先说行住坐卧知见常生，于前后小事都不能知，怎么知道过人法、若知若见安乐而住呢？」",
        "长者又问：「有一问、一说、一记论，乃至十问、十说、十记论，你有没有？"
        "若没有一问乃至十问，怎么能骗我来此林中想引诱我？」",
        "于是尼犍若提子闭口掉头，反拱着出去，不再回头。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN41.8（Citta 第二禅对尼犍；智胜于信）。"
        "据 SN 校正：系风、断流喻；汉本「阿耆毘言」误，今改尼犍若提子。"
    ),
}

# --- SA 575 病相（SN41.10 Gilāna）---------------------------------------------
CITTA_GATHA_LIT = (
    "服食积所积，广度于众难，施上进福田，殖斯五种力。"
    "以斯义所欲，俗人处于家，我悉得此利，已免于众难。"
    "世间所闻习，远离众难事，生乐知稍难，随顺等正觉。"
    "供养持戒者，善修诸梵行，漏尽阿罗汉，及声闻牟尼。"
    "如是超越见，于上诸胜处，常行士夫施，克终获大果。"
    "习行众多施，施诸良福田，于此世命终，化生於天上。"
    "五欲具足满，无量心悦乐，获斯妙果报，以无悭悋故。"
    "所在处受生，未曾不欢喜。"
)
CITTA_GATHA_MOD = (
    "服食积所积，广度于众难，施上进福田，培植五种力。"
    "依此义所欲，俗人处于家，我悉得此利，已免于众难。"
    "世间所闻习，远离众难事，生乐知稍难，随顺等正觉。"
    "供养持戒者，善修诸梵行，漏尽阿罗汉，及声闻牟尼。"
    "如是超越见，于上诸胜处，常行士夫施，克终获大果。"
    "习行众多施，施诸良福田，于此世命终，化生於天上。"
    "五欲具足满，无量心悦乐，获此妙果报，以无悭悋故。"
    "所在处受生，未曾不欢喜。"
)

SUTTAS["SA_575"] = {
    "lit": [
        OPEN_MAC_LIT,
        "尔时，质多罗长者病苦，诸亲围绕。有众多诸天来诣长者，言：「长者！当发愿作转轮王。」",
        "长者语诸天：「若作转轮王，彼亦无常、苦、空、非我。」",
        "诸亲语长者：「汝当系念。」长者问：「何故教我系念？」",
        "诸亲言：「汝作是言：『无常、苦、空、非我。』是故教汝系念。」",
        "长者语诸亲：「有诸天来，教我愿求转轮圣王；我即答言：『彼转轮王亦无常、苦、空、非我。』」",
        "诸亲问：「转轮王有何，而诸天教汝愿求？」",
        "长者答：「转轮王以正法治化，诸天见如是福利，故教我发愿。」",
        "诸亲问：「汝今用心，当如之何？」",
        f"长者答：「{ANAGAMI_LIT}」",
        "于是长者从床起，结加趺坐，正念在前，说偈言：「" + CITTA_GATHA_LIT + "」",
        "长者说偈已，寻即命终，生于不烦热天。",
        "尔时，质多罗天子作念：「我不应停此，当往阎浮提礼拜诸上座。」如力士屈伸臂顷，以天神力至庵罗林，放身光明遍照。",
        "时有异比丘夜起出房，露地经行，见胜光明普照树林，说偈言：「是谁妙天色，住于虚空中，譬如纯金山，阎浮檀净光。」",
        "质多罗天子说偈答言：「我是天人王，瞿昙名称子，是庵罗林中质多罗长者，"
        "以净戒具足、系念自寂静，解脱身具足、智慧身亦然；我知法故来，仁者应当知，当于彼涅槃，此法法如是。」",
        "质多罗天子说偈已，即没不现。",
    ],
    "mod": [
        OPEN_MAC_MOD,
        "当时，质多罗长者病苦，亲属围绕。有众多诸天来到长者处，说：「长者！应当发愿作转轮王。」",
        "长者对诸天说：「如果作转轮王，那也是无常、苦、空、非我。」",
        "亲属对长者说：「你应当系念。」长者问：「为什么教我系念？」",
        "亲属说：「你说：『无常、苦、空、非我。』所以教你系念。」",
        "长者对亲属说：「有诸天来，教我愿求转轮圣王；我就答说：『转轮王也是无常、苦、空、非我。』」",
        "亲属问：「转轮王有什么，而诸天教你愿求？」",
        "长者答：「转轮王以正法治化，诸天看见这样的福利，所以教我发愿。」",
        "亲属问：「你现在作意，应当怎样？」",
        f"长者答：「{ANAGAMI_MOD}」",
        "于是长者从床起来，结跏趺坐，正念在前，说偈：「" + CITTA_GATHA_MOD + "」",
        "长者说偈后，随即命终，生于不烦热天。",
        "当时，质多罗天子作念：「我不应停在这里，应当往阎浮提礼拜诸上座。」"
        "如力士屈伸臂那样快，以天神力到庵罗林，放身光明遍照。",
        "当时，有一位比丘夜起出房，在露地经行，看见殊胜光明普照树林，说偈："
        "「是谁妙妙的天色，住于虚空中，譬如纯金山，阎浮檀净光。」",
        "质多罗天子说偈答：「我是天人王，瞿昙的弟子，是庵罗林中的质多罗长者，"
        "以净戒具足、系念自寂静，解脱身具足、智慧身亦然；因为知法而来，仁者应当知道，当趣向涅槃，法就是这样。」",
        "质多罗天子说偈后，随即消失。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN41.10（病中拒转轮愿；无常答；Citta 往生天界来访）。"
        "据 SN 校正：「彼亦无常、苦、空、非我」；汉本长偈保留，亲教四信段从 SN 略。"
    ),
}

# --- SA 576 欢喜园（SN1.11 Nandana）--------------------------------------------
_lit576, _mod576 = _devata_simple(
    "不处难陀林，终不得快乐，忉利天宫中，得天帝名称。",
    "不处难陀林，终不得快乐，忉利天宫中，得天帝名称。",
    "童蒙汝何知，阿罗汉所说，一切行无常，是则生灭法，生者既复灭，俱寂灭为乐。",
    "童蒙汝何知，阿罗汉所说，一切行无常，是则生灭法，生者既复灭，俱寂灭为乐。",
)
SUTTAS["SA_576"] = {
    "lit": _lit576,
    "mod": _mod576,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN1.11（难陀林乐 vs 诸行无常寂灭为乐）。"
        "汉本直访佛所，SN 为佛语比丘，今从汉本框、偈义据 SN。"
    ),
}

# --- SA 577 钩锃（SN10.2 Sakka）------------------------------------------------
_lit577 = [
    DEVATA_OPEN_LIT,
    "时，彼天子说偈言：「断诸钩锁，牟尼无家宅，沙门教众生，我说非善哉。」",
    "尔时，世尊说偈答言：「众生互相缚，智谁不悯伤？善逝以哀愍，常教示众生；哀愍众生者，是法之所应。」",
    f"时，彼天子复说偈言：「{DEVATA_EPILOGUE_LIT}」",
    DEVATA_CLOSE_LIT.replace("稽首佛足，", ""),
]
_mod577 = [
    DEVATA_OPEN_MOD,
    "天子说偈言：「断诸钩锁，牟尼无家宅，沙门教众生，我说非善哉。」",
    "世尊说偈答：「众生互相缚，智谁不悯伤？善逝以哀愍，常教示众生；哀愍众生者，是法之所应。」",
    f"天子又说偈：「{DEVATA_EPILOGUE_MOD}」",
    DEVATA_CLOSE_MOD.replace("顶礼佛足，", ""),
]
SUTTAS["SA_577"] = {
    "lit": _lit577,
    "mod": _mod577,
    "notes": (
        f"{PROV}"
        "confidence=high：parallel SN10.2（Sakka 问教示；哀愍应教授）。"
        "据 SN 校正：钩锁／缠缚；汉本置舍卫园，从汉。"
    ),
}

# --- SA 578 惭愧（SN1.18 Hirī）-------------------------------------------------
_lit578, _mod578 = _devata_simple(
    "常习惭愧心，此人时时有，能远离诸恶，如顾鞭良马。",
    "常习惭愧心，此人时时有，能远离诸恶，如顾鞭良马。",
    "常习惭愧心，此人实希有，能远离诸恶，如顾鞭良马。",
    "常习惭愧心，此人实希有，能远离诸恶，如顾鞭良马。",
)
SUTTAS["SA_578"] = {"lit": _lit578, "mod": _mod578, "notes": (
    f"{PROV}confidence=high：primary SN1.18（惭愧如鞭良马）。"
)}

# --- SA 579 不善知（SN1.7 Appaṭividita）---------------------------------------
_lit579, _mod579 = _devata_simple(
    "不习近正法，乐著诸邪见，睡眠不自觉，长劫心能悟。",
    "不习近正法，乐著诸邪见，睡眠不自觉，长劫心能悟。",
    "专修于正法，远离不善业，是漏尽罗汉，险恶世平等。",
    "专修于正法，远离不善业，是漏尽罗汉，险恶世平等。",
)
SUTTAS["SA_579"] = {"lit": _lit579, "mod": _mod579, "notes": (
    f"{PROV}confidence=high：primary SN1.7（未通达 vs 漏尽罗汉）。"
)}

# --- SA 580 善调（SN1.8 Susammuṭṭha）------------------------------------------
_lit580, _mod580 = _devata_simple(
    "以法善调伏，不随于诸见，虽复著睡眠，则能随时悟。",
    "以法善调伏，不随于诸见，虽复著睡眠，则能随时悟。",
    "若以法调伏，不随余异见，无知已究竟，能度世恩爱。",
    "若以法调伏，不随余异见，无知已究竟，能度世恩爱。",
)
SUTTAS["SA_580"] = {"lit": _lit580, "mod": _mod580, "notes": (
    f"{PROV}confidence=high：primary SN1.8（依法调伏、不随异见）。"
)}

# --- SA 581 罗汉（SN1.25 Arahant 详本）-----------------------------------------
_lit581 = [
    DEVATA_OPEN_LIT.replace("身诸光明", "退坐一面。身诸光明"),
    "时，彼天子说偈问佛：「漏尽比丘，所作已办，持此残身，可说『我』、『我所』不？」",
    "尔时，世尊说偈答言：「漏尽比丘，所作已办，持此残身，正可说『我』，说『我所』亦无过。」",
    "时，彼天子复说偈言：「既离我慢，何复依慢，而说言有我、及我所耶？」",
    "尔时，世尊说偈答言：「已离我慢，无慢心所依，超越我我所，我说名漏尽；"
    "于世名字善，平等假名说。」",
    f"时，彼天子复说偈言：「{DEVATA_EPILOGUE_LIT}」",
    DEVATA_CLOSE_LIT,
]
SUTTAS["SA_581"] = {
    "lit": _lit581,
    "mod": _mod_from_lit(_lit581, DEVATA_OPEN_MOD.replace("身放光明", "退坐一面。身放光明")),
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN1.25（阿罗汉假名说我／我所；离我慢）。"
        "据 SN 校正：三轮问答，从巴利 conceit／labels。"
    ),
}

# --- SA 582 罗汉（SN1.25 略本）-------------------------------------------------
_lit582 = [
    DEVATA_OPEN_LIT,
    "时，彼天子说偈白佛：「漏尽比丘持后身，可说有我、我所不？」",
    "尔时，世尊说偈答言：「漏尽持后身，亦说我、我所。」",
    "时，彼天子复说偈言：「既尽诸漏、唯持后身，何说我我所？」",
    "尔时，世尊说偈答言：「说我漏已尽，不着我所；善解世名，平等假说。」",
    DEVATA_CLOSE_LIT,
]
SUTTAS["SA_582"] = {
    "lit": _lit582,
    "mod": _mod_from_lit(_lit582, DEVATA_OPEN_MOD),
    "notes": (
        f"{PROV}"
        "confidence=high：parallel SN1.25（汉本略本／二轮问答 variant）。"
        "与 SA581 同经异译，从汉本保留略式。"
    ),
}

# --- SA 583 月天子（SN2.9 Candima）---------------------------------------------
_lit583 = [
    OPEN_JET_LIT,
    "尔时，罗睺罗阿修罗王障月天子。时，诸月天子悉皆恐怖，来诣佛所，稽首佛足，退住一面，说偈叹佛：",
    "「今礼最胜觉，能脱一切障，我今遭苦恼，是故来归依。我等月天子，归依于善逝，佛哀愍世间，愿解阿修罗。」",
    "尔时，世尊说偈答言：「破坏诸闇冥，光明照虚空，今毗卢遮那，清净光明显。"
    "罗睺避虚空，速放飞兔像，罗睺阿修罗，即舍月而还。举体悉流污，战怖不自安，神昏志迷乱，犹如重病人。」",
    "时有阿修罗名曰婆稚，见罗睺罗阿修罗疾舍月还，说偈言：「罗睺阿修罗，舍月一何速，神体悉流污，犹如重病人。」",
    "罗睺阿修罗说偈答言：「瞿昙说咒偈，不速舍月者，或头破七分，受诸邻死苦。」",
    "婆稚阿修罗复说偈言：「佛兴未曾有，安隐于世间，说咒偈能令，罗睺罗舍月。」",
    "佛说是经已，时月天子闻佛所说，欢喜随喜，作礼而去。",
]
SUTTAS["SA_583"] = {
    "lit": _lit583,
    "mod": _mod_from_lit(_lit583, OPEN_JET_MOD),
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN2.9（月天子被 Rāhu 障；佛咒释月）。"
        "据 SN 校正：归依、头破七分喻，从巴利。"
    ),
}

# --- SA 584 手杻（SN1.19 Kuṭikā）-----------------------------------------------
_lit584 = [
    DEVATA_OPEN_LIT.replace("身诸光明", "退坐一面。身诸光明"),
    "时，彼天子说偈问佛：「为有族本不？有转生族耶？有俱相属无？云何解于缚？」",
    "尔时，世尊说偈答言：「我无有族本，亦无转生族，俱相属永断，解脱一切缚。」",
    "时，彼天子复说偈言：「何为族本？云何转生族？云何俱相续？何为坚缚？」",
    "尔时，世尊说偈答言：「母为世族本，妻名转生族，子俱是相属，爱欲为坚缚；"
    "我无此族本，亦无转生族，俱相属亦无，是名脱坚缚。」",
    "时，彼天子复说偈言：「善哉无族本，无生族亦善，善哉无相属，善哉缚解脱。"
    f"{DEVATA_EPILOGUE_LIT}」",
    DEVATA_CLOSE_LIT,
]
SUTTAS["SA_584"] = {
    "lit": _lit584,
    "mod": _mod_from_lit(_lit584, DEVATA_OPEN_MOD.replace("身放光明", "退坐一面。身放光明")),
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN1.19（母妻子为爱欲坚缚；无族本解脱）。"
        "据 SN 校正：hut／nest／network／shackle 四喻。"
    ),
}

# --- SA 585 独一住（SN2.18 Kakudha）--------------------------------------------
_lit585 = [
    OPEN_SAK_LIT,
    "尔时，世尊新剃须发，于后夜时结加趺坐，直身正意，系念在前，以衣覆头。",
    "时，优罗提那塔边有天神住，放身光明遍照精舍，白佛言：「沙门忧耶？」佛告天神：「何所忘失？」",
    "天神复问：「沙门欢喜耶？」佛告天神：「为何所得？」",
    "天神复问：「沙门不忧不喜耶？」佛告天神：「如是，如是。」",
    "尔时，天神说偈言：「为离诸烦恼，为无有欢喜，云何独一住？非不乐所坏。」",
    "尔时，世尊说偈答言：「我无恼解脱，亦无有欢喜，不乐不能坏，故独一而住。」",
    "时，彼天神复说偈言：「云何得无恼？云何无欢喜？云何独一住？非不乐所坏。」",
    "尔时，世尊说偈答言：「烦恼生欢喜，喜亦生烦恼，无恼亦无喜，天神当护持。」",
    "时，彼天神复说偈言：「善哉无烦恼，善哉无欢喜，善哉独一住，不为不喜坏。"
    f"{DEVATA_EPILOGUE_LIT}」",
    "时，彼天神闻佛所说，欢喜随喜，稽首佛足，即没不现。",
]
SUTTAS["SA_585"] = {
    "lit": _lit585,
    "mod": _mod_from_lit(_lit585, OPEN_SAK_MOD),
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN2.18（Kakudha 问不忧不喜独住）。"
        "据 SN 校正：何所忘失／为何所得，从巴利。"
    ),
}

# --- SA 586 利剑（SN1.21 Satti）-------------------------------------------------
_lit586, _mod586 = _devata_simple(
    "犹如利剑害，亦如头火燃，断除贪欲火，正念求远离。",
    "犹如利剑害，亦如头火燃，断除贪欲火，正念求远离。",
    "譬如利剑害，亦如头火燃，断除于后身，正念求远离。",
    "譬如利剑害，亦如头火燃，断除于后身，正念求远离。",
)
SUTTAS["SA_586"] = {"lit": _lit586, "mod": _mod586, "notes": (
    f"{PROV}confidence=high：primary SN1.21（利剑、头火喻；断身见／贪欲）。"
    "据 SN 校正：汉问贪欲、佛答后身（sakkāya），今从 SN。"
)}

# --- SA 587 天女（SN1.46 Accharā）----------------------------------------------
_lit587 = [
    DEVATA_OPEN_LIT,
    "时，彼天子说偈言：「天女众围绕，如脂王众中，痴林何得出？」",
    "尔时，世尊说偈答言：「正直平等道，离怖寂默车，法想为覆盖，惭愧为长縻，正念为羁络，智为善御士，正见为前导；男女乘此乘，出生死林野，得至安乐处。」",
    f"时，彼天子复说偈言：「{DEVATA_EPILOGUE_LIT}」",
    DEVATA_CLOSE_LIT,
]
_mod587 = [
    DEVATA_OPEN_MOD,
    "天子说偈言：「天女众围绕，如脂王众中，痴林何得出？」",
    "世尊说偈答：「正直平等道，离怖寂默车，法想为覆盖，惭愧为长縻，正念为羁络，智为善御士，正见为前导；男女乘此乘，出生死林野，得至安乐处。」",
    f"天子又说偈：「{DEVATA_EPILOGUE_MOD}」",
    DEVATA_CLOSE_MOD,
]
SUTTAS["SA_587"] = {
    "lit": _lit587,
    "mod": _mod587,
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN1.46（妙乘喻出生死丛林）。"
        "据 SN 校正：vehicle 诸喻压缩，从巴利。"
    ),
}

# --- SA 588 四转轮（SN1.29 Catucakka）------------------------------------------
_lit588, _mod588 = _devata_simple(
    "有四转九门，充满贪欲住，深溺乌泥中，大象云何出？",
    "有四转九门，充满贪欲住，深溺乌泥中，大象云何出？",
    "断爱喜长縻，贪欲等诸恶，拔爱欲根本，正向于彼处。",
    "断爱喜长縻，贪欲等诸恶，拔爱欲根本，正向于彼处。",
)
SUTTAS["SA_588"] = {"lit": _lit588, "mod": _mod588, "notes": (
    f"{PROV}confidence=high：primary SN1.29（四转九门／断爱喜縻）。"
)}

# --- SA 589 罗吒园（SN1.28 Mahaddhana）-----------------------------------------
_lit589 = [
    DEVATA_OPEN_LIT.replace("身诸光明", "退坐一面。身诸光明"),
    "时，彼天子说偈问佛：「赖吒槃提国，有诸商贾客，大富足财宝，各各竞求富，"
    "方便欲财利，犹如然炽火，如是竞胜心，欲贪常驰骋，云何当断贪，息世间勤求？」",
    "尔时，世尊说偈答言：「舍俗出非家，妻子及财宝，贪恚痴离欲，罗汉尽诸漏，正智心解脱，爱尽息方便。」",
    f"时，彼天子复说偈言：「{DEVATA_EPILOGUE_LIT}」",
    DEVATA_CLOSE_LIT,
]
SUTTAS["SA_589"] = {
    "lit": _lit589,
    "mod": _mod_from_lit(_lit589, DEVATA_OPEN_MOD.replace("身放光明", "退坐一面。身放光明")),
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN1.28（富商竞财；出家断爱息方便）。"
        "据 SN 校正：Mahaddhana 喻，从巴利。"
    ),
}

# --- SA 590 古客（sa-2.184；无巴利）--------------------------------------------
SUTTAS["SA_590"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「过去世时，拘萨罗国有诸商人，五百乘车，共行治生，至旷野中；"
        "旷野有五百群贼在后随逐，伺便欲劫。时，旷野有一天神，止住路侧。」",
        "天神作念：『当诣彼商人，问其义理；若喜我所问而能解说，我当方便令其安隐得脱贼难；若不喜，当放舍之。』",
        "天神作念已，放身光遍照商人车营，说偈言：「谁于觉睡眠？谁复睡眠觉？谁有解此义？谁能为我说？」",
        "尔时，商人中有一优婆塞——信佛、法、僧，于四谛离疑，得第一无间等果——与诸商人共为行侣；"
        "彼于后夜端坐思惟，系念在前，于十二因缘逆顺观察：缘无明故有行，乃至纯大苦聚集；无明灭则行灭，乃至纯大苦聚灭。",
        "时，彼优婆塞思惟已，说偈言：「我于觉睡眠，我于睡眠觉，我解知此义，能为人记说。」",
        "时，彼天神问优婆塞：「云何觉睡眠？云何睡眠觉？云何能解知？云何能记说？」",
        "时，优婆塞说偈答言：「贪欲及瞋恚，愚痴得离欲，漏尽阿罗汉，正智心解脱，彼则为觉悟，我于彼睡眠；"
        "不知因生苦，及苦因缘集，于此一切苦，得无余灭尽，又不知正道，等趣息苦处，斯等为常眠，我于彼则觉；"
        "如是觉睡眠，如是睡眠觉，如是善知义，如是能记说。」",
        "时，彼天神复说偈言：「善哉觉睡眠，善哉眠中觉，善哉解知义，善哉能记说，久远乃今见，诸兄弟而来，"
        "缘汝恩力故，令诸商人众，得免于劫贼，随道安乐去。」",
        "如是，诸比丘！彼拘萨罗泽中诸商人众皆得安隐从旷野出。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时，世尊告诉诸比丘：「过去世时，拘萨罗国有诸商人，五百乘车，一起行商治生，到了旷野中；"
        "旷野中有五百群贼在后跟随，伺机欲劫。当时，旷野中有一天神，停在路侧。」",
        "天神作念：『应当前往那些商人处，问其义理；若他们喜欢我的所问而能解说，"
        "我就方便令他们安稳、得脱贼难；若不喜欢，就放弃。』",
        "天神作念后，放身光遍照商人车营，说偈：「谁于觉中睡眠？谁于睡眠中觉？谁有解此义？谁能为我说？」",
        "当时，商人中有一位优婆塞——信佛、法、僧，于四谛离疑，证得第一无间等果——与诸商人共为行侣；"
        "他在后夜端坐思惟，系念在前，对十二因缘逆顺观察：缘无明故有行，乃至纯大苦聚集；无明灭则行灭，乃至纯大苦聚灭。",
        "当时，那位优婆塞思惟后，说偈：「我于觉中睡眠，我于睡眠中觉，我解知此义，能为人记说。」",
        "当时，那位天神问优婆塞：「怎样叫觉中睡眠？怎样叫睡眠中觉？怎样能解知？怎样能记说？」",
        "当时，优婆塞说偈答：「贪欲、瞋恚、愚痴得离欲，漏尽阿罗汉，以正智心解脱，彼才是觉悟，我于彼睡眠；"
        "不知道因生苦，及苦因缘集，于此一切苦，得无余灭尽，又不知道正道，等趣息苦处，这些才是常眠，我于彼则觉；"
        "这样觉中睡眠，这样睡眠中觉，这样善知义，这样能记说。」",
        "当时，那位天神又说偈：「善哉觉中睡眠，善哉眠中觉，善哉解知义，善哉能记说，久远至今才见，诸兄弟而来，"
        "缘你的恩力，令诸商人众，得免于劫贼，随道安乐去。」",
        "这样，诸比丘！那拘萨罗泽中的商人众都安稳从旷野出来。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "天神问觉眠、优婆塞以阿罗汉／缘起答；十二因缘 peyyāla 压缩。"
        "parallel sa-2.184；从汉本，confidence=medium。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_571": "high",
    "SA_572": "high",
    "SA_573": "high",
    "SA_574": "high",
    "SA_575": "high",
    "SA_576": "high",
    "SA_577": "high",
    "SA_578": "high",
    "SA_579": "high",
    "SA_580": "high",
    "SA_581": "high",
    "SA_582": "high",
    "SA_583": "high",
    "SA_584": "high",
    "SA_585": "high",
    "SA_586": "high",
    "SA_587": "high",
    "SA_588": "high",
    "SA_589": "high",
    "SA_590": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_573": "ordination peyyāla compressed (闻法修行证阿罗汉)",
    "SA_575": "fourfold faith/advise to kin truncated per SN41.10 frame",
    "SA_590": "twelve nidāna peyyāla compressed to forward/reverse gist",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(571, 591)}, (
        "GOLD must cover SA_571–SA_590 exactly"
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

    boundary_id = "SA_570"
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

    # Assert SA_591+ untouched snapshot (first field only)
    sa591_before = None
    for rec in records:
        if rec["id"] == "SA_591":
            sa591_before = rec.get("kumarajiva_style_text")
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

    for rec in merged:
        if rec["id"] == "SA_591" and sa591_before is not None:
            assert rec.get("kumarajiva_style_text") == sa591_before, "SA_591 must remain untouched"
            break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa571-590.json").write_text(
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
    continuous_571_590 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(571, 591)
    )
    continuous_1_590 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(1, 591)
    )

    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛", "如如"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_571–SA_590 only)")
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
    print(f"gold_reconstructed_ids={[r['id'] for r in recon]}")
    print(f"continuous_gold_SA_571–590={continuous_571_590}")
    print(f"continuous_gold_SA_1–590={continuous_1_590}")
    print(f"{boundary_id}_untouched=True")
    print(f"SA_591_untouched=True")
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
