#!/usr/bin/env python3
"""Retranslate SA 991–1010（鹿住／延清＋诸天相应）→ merge.

本批二十经：
991–992 杂相应末（鹿住 AN6.44；延清 AN2.35 学无学福田）
993–1010 诸天相应起（赞大声闻、婆耆娑灭尽无专经；
    阿练 SN1.10、憍慢 SN1.9、修福 SN1.47、云何大得 SN1.42、
    生欢喜 SN2.23、远去 SN1.53、强亲 SN1.3、思惟 SN1.5、睡寤 SN1.6、
    生欢喜 SN1.12、义利 SN1.54、所爱 SN1.13、刹利 SN1.14、种子 SN1.74、
    意 SN1.62、缚 SN1.64）

信：有 SN／AN 平行者据巴利／Sujato 厘义；993–994 无 SC 巴利 → medium。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_991–1010；不触碰 SA_990、SA_1011；
      注：SA_999 之后 ID 续为 SA_1000+。
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

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_LAY_LIT = "佛说此经已，给孤独长者闻佛所说，欢喜奉行。"
CLOSE_LAY_MOD = "佛说完这部经，给孤独长者听佛所说，欢喜奉行。"

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

# --- SA 991 鹿住（AN6.44／AN10.75 变本）------------------------------------
SUTTAS["SA_991"] = {
    "lit": [
        "如是我闻：一时，佛住释氏弥城留利邑夏安居；"
        "有余比丘于舍卫国祇树给孤独园夏安居。",
        "彼比丘晨朝著衣持钵，入舍卫城乞食，次至鹿住优婆夷舍。"
        "鹿住遥见，疾敷座请坐——事同阿难所问修多罗。",
        "比丘语曰：「姊妹且止！汝安能知众生诸根优劣？"
        "唯有如来能知。」说已，从座起去。",
        "三月安居竟，作衣已，持衣钵往诣弥城留利，礼佛足，退坐一面，"
        "以与鹿住所论广白世尊。",
        "佛告比丘：「鹿住安能知世间诸根优劣？唯如来能知。"
        "或有人未离瞋慢，时起贪法，又不听法、不多闻、不调见，"
        "不能时时得心解脱——我说此人下劣。"
        "或有人虽未离瞋慢、时起贪法，然乐闻法、多闻、善调见，"
        "时时能得心解脱——我说此人胜妙。"
        "若等量二人，谓『此有是法、彼有是法，当同一趣、同一受生、同一后世』，"
        "如是筹量，长夜非义、不饶益苦。"
        "彼二有间，非如来谁能别知？是故莫量人人；量人人者，自招其患。"
        "唯有如来能知人耳。」",
        "「复次：或有人未离瞋慢，时起口恶行；或贤善同止、乐梵行侣，"
        "而不乐闻法、不得时时心解脱——住贤善地（人天），不能转进。"
        "或同其贤善，而乐闻法、多闻、调见、得时时心解脱——"
        "于贤善地能转胜进，于正法流有所堪能。"
        "此二有间，非如来谁能别知？莫量人人。」",
        "「鹿住愚癡少智……」余如上阿难修多罗广说。",
        CLOSE_BH_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛在释氏弥城留利邑结夏安居；"
        "另有比丘在舍卫国祇树给孤独园结夏安居。",
        "那位比丘早晨著衣持钵，进城乞食，依次到鹿住优婆夷家。"
        "鹿住远远看见，赶紧敷座请坐——情形如同阿难那部经所说。",
        "比丘说：「姊妹且停！你怎么能知道众生诸根的优劣？"
        "只有如来才能知道。」说完便起身离去。",
        "三个月安居结束，作衣完毕，他持衣钵前往弥城留利，顶礼佛足，退坐一面，"
        "把与鹿住所谈的事详细告诉世尊。",
        "佛告诉比丘：「鹿住怎么能知道世间诸根优劣？只有如来能知。"
        "有的人还没离开瞋与慢，时常起贪，又不听法、不多闻、不调伏见解，"
        "也不能时时得到心解脱——我说这种人下劣。"
        "有的人虽然也未离瞋慢、时常起贪，却乐于闻法、多闻、善调见解，"
        "时时能得心解脱——我说这种人胜妙。"
        "若把两人等量齐观，说『彼此有同样的法，就该同一趣、同一受生、同一后世』，"
        "这样衡量，会长夜不得利益、遭受痛苦。"
        "这两类人之间的差别，除了如来谁能分辨？所以不要衡量人；衡量人会自找祸患。"
        "只有如来能知人。」",
        "「再者：有人未离瞋慢而时起口恶行；或性情贤善、乐与梵行者同住，"
        "却不乐闻法、不能时时心解脱——只住人天贤善之地，不能向上转进。"
        "另有同样贤善的人，却乐闻法、多闻、调见、得时时心解脱——"
        "能从贤善之地转进更胜，于正法之流有所堪能。"
        "这两类之间的差别，除了如来谁能分辨？不要衡量人。」",
        "「鹿住愚癡少智……」其余如同阿难那部经里广说的那样。",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：parallel AN6.44／AN10.75（Migasālā 勿量人）。"
        "汉本为阿难修多罗之变本（匿名比丘、弥城留利安居），义同六类人："
        "外相相似而闻法／调见／暂时心解脱有无不同；据 AN 厘「正法流」胜进义。"
        "「如上阿难修多罗」指 SA_990，不复录富兰那／梨师达多长段。"
    ),
}

# --- SA 992 延清（AN2.35 学／无学福田）--------------------------------------
SUTTAS["SA_992"] = {
    "lit": [
        OPEN_JET_LIT,
        "给孤独长者来诣佛所，礼足却坐，白言：「世尊！世间有几福田？」",
        "佛告长者：「世间有二种福田——学与无学。」即说偈："
        "「世有学无学，大会常延请；正直心真实，身口亦复然；"
        "是则良福田，施者获大果。」",
        CLOSE_LAY_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "给孤独长者来到佛前，顶礼佛足，退坐一面，问：「世尊！世间有几种福田？」",
        "佛告诉长者：「世间有两种福田——有学与无学。」即说偈："
        "「世间有学与无学，大众常延请；内心正直真实，身口亦然；"
        "这就是良福田，布施者得大果。」",
        CLOSE_LAY_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：parallel AN2.35（sekha／asekha 二福田；SC 表作 an2.32-41 组）。"
        "据巴利：福田为有学、无学；汉「延清」≈大会延请供养。"
    ),
}

# --- SA 993 赞大声闻（无巴利专经；婆耆舍赞上座）-----------------------------
SUTTAS["SA_993"] = {
    "lit": [
        OPEN_JET_LIT,
        "时诸上座比丘依佛左右而住："
        "阿若憍陈如、摩诃迦叶、舍利弗、大目揵连、阿那律、二十亿耳、"
        "陀罗骠摩罗子、婆那迦婆娑、耶舍、富留那、分陀檀尼迦等。",
        "尊者婆耆舍住东园鹿子母讲堂，念言：「世尊与诸上座在祇园，"
        "我当往以偈各叹。」即诣佛所，礼足一面，说偈赞上座及佛：",
        "「上座断贪欲，超世诸积聚，深智少言说，勇猛勤方便，道净我稽首。"
        "已伏诸魔怨，远离于群聚，不为五欲缚，闲林修寡欲，是故我稽首。"
        "禅思不放逸，内心乐正受，辩慧显深义，神通众自在，天眼见五趣，"
        "精勤坏死网，知足度疑惑，断结出见处，心坚魔能伏——"
        "如是诸上座，我今稽首礼。」",
        "「大人离闇冥，寂灭牟尼尊；正法离垢秽，光明照世间，是故名为佛。"
        "地神虚空天，三十三天子，光明悉映障；度有越群众，正觉第一觉；"
        "断结伏异道，降魔得无上，离尘灭诸垢，是故稽首礼。」",
        "婆耆舍偈赞时，诸比丘闻已，皆大欢喜。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时诸位上座比丘依止佛左右而住："
        "阿若憍陈如、摩诃迦叶、舍利弗、大目揵连、阿那律、二十亿耳、"
        "陀罗骠摩罗子、婆那迦婆娑、耶舍、富留那、分陀檀尼迦等。",
        "尊者婆耆舍住在东园鹿子母讲堂，心想：「世尊与诸上座在祇园，"
        "我应当前往，用偈一一赞叹。」便到佛前，顶礼后退立一面，说偈赞上座及佛：",
        "「上座已断贪欲，超越世间积聚，深智少言，勇猛精进，道德清净——我稽首。"
        "已降伏魔怨，远离群聚，不为五欲所缚，闲林少欲——故我稽首。"
        "禅思不放逸，内心乐于正受，辩才显深义，神通自在无畏，天眼见五趣，"
        "精勤坏生死网，知足度疑惑，断结超出见处，心坚能伏魔——"
        "如是诸上座，我今稽首礼。」",
        "「大人离闇冥，寂灭的牟尼；正法离垢，光明照世间，所以名为佛。"
        "地神、虚空天、三十三天，光明都被映障；度生死、越群众，正觉第一；"
        "断结、伏异道、降魔得无上，离尘灭垢——故我稽首礼。」",
        "婆耆舍说偈赞叹时，比丘们听了都大欢喜。",
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：无 SC 巴利专经；义近 Thag 婆耆舍赞上座／赞佛偈群。"
        "罗什风压缩十一上座逐赞为总赞＋赞佛，保留名号列叙。"
    ),
}

# --- SA 994 婆耆娑灭尽（无巴利专经；临终偈）--------------------------------
SUTTAS["SA_994"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者婆耆舍住东园鹿子母讲堂，疾病困笃；尊者富邻尼为看病人。",
        "婆耆舍语富邻尼：「往白世尊：婆耆舍稽首问讯少病少恼、起居轻利。"
        "我病笃无力往见，愿世尊哀愍，来此讲堂。」",
        "富邻尼往白，世尊默许。晡时从禅起，往诣婆耆舍。"
        "婆耆舍遥见，凭床欲起；佛止之：「莫自轻动！」即坐，问苦增损。"
        "答如焰摩迦修多罗：「苦患转增，不觉其损。」",
        "佛问：「汝心得不染、不著、不污、解脱、离颠倒不？」"
        "白言：「得。」「云何得？」"
        "「过去眼识于色，心不顾念；未来不欣；现在不著。"
        "三世色中贪爱念尽，灭、息、离、解脱，故心不染著、离颠倒，正受而住。"
        "耳鼻舌身意于法，亦复如是。愿听我说最后偈。」"
        "佛言：「宜知是时。」",
        "婆耆舍正身端坐，系念在前，说偈："
        "「我今住佛前，稽首恭敬礼，于一切诸法，悉皆得解脱。"
        "世尊等正觉，降魔大牟尼，世间无有等，稽首大精进。"
        "我今是最后，得见于世尊；正智系正念，暮当般涅槃。"
        "苦乐不苦乐，触缘今永断；内外诸受中，正智无所著。"
        "明见真实者，九十一劫中，三劫不空过，有大仙出世；"
        "安慰诸天人，开眼离尘冥，说苦集灭道，安隐趣涅槃。"
        "人身正法现，专修勿空过；我今众庆集，轮回悉已断。"
        "爱识河已竭，阴本已拔除；所作已作竟，重担有流断。"
        "如野龙象脱，正念待时至；生者悉归灭，诸行无有常。"
        "是故强其志，观察有恐怖，速尽此苦阴，勿复增轮转。」",
        "叹说已，长辞大众，入无余涅槃。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "尊者婆耆舍住在东园鹿子母讲堂，病势沉重；尊者富邻尼照料他。",
        "婆耆舍对富邻尼说：「去禀告世尊：婆耆舍稽首问讯少病少恼、起居轻安。"
        "我病重无力前往，愿世尊哀愍，到这讲堂来。」",
        "富邻尼转告后，世尊默然应许。下午从禅定起来，前往婆耆舍处。"
        "婆耆舍远远看见，扶床想起来；佛制止说：「不要勉强动！」便坐下，询问苦痛增减。"
        "他如同焰摩迦经中所说：「苦痛只觉加重，不觉减轻。」",
        "佛问：「你的心是否已不染、不著、不污、解脱、离开颠倒？」"
        "答：「是。」「怎样得到的？」"
        "「对过去眼识所见之色，心不再顾念；对未来不欣求；对现在不执著。"
        "三世色中的贪爱忆念已尽，灭尽、止息、远离、解脱，所以心不染著、离颠倒，安住正受。"
        "耳、鼻、舌、身、意对法也是如此。请听我说最后的偈。」"
        "佛说：「现在正是时候。」",
        "婆耆舍端身正坐，系念眼前，说偈："
        "「我今住在佛前，稽首敬礼，于一切法都已解脱。"
        "世尊是等正觉，降魔的大牟尼，世间无人可比，稽首大精进。"
        "这是我最后一次得见世尊；以正智正念，今夜将入涅槃。"
        "苦受、乐受、不苦不乐受，都从触生，如今永断；内外诸受，正智都无所著。"
        "明见真实者说：九十一劫中，三劫不空过，有大仙出世；"
        "安慰天人，开眼离闇，说苦集灭道，安隐趋向涅槃。"
        "得人身又闻正法，应专修勿空过；我今众善圆满，轮回已断。"
        "爱与识的河流已枯，五阴根本已拔；所作已办，重担与有流已断。"
        "如林中龙象脱去枷锁，正念等待时至；生者必灭，诸行无常。"
        "所以要坚定志愿，观察恐怖，速尽苦阴，勿再增加轮转。」",
        "赞叹说完，辞别大众，入无余涅槃。",
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：无 SC 巴利专经；临终六入不著、最后偈近 Thag 婆耆舍涅槃偈群。"
        "「焰摩迦修多罗」问病定型从汉本；罗什风删梵式复沓，保留四谛／无常／所作已作。"
    ),
}

# --- SA 995 阿练（SN1.10）----------------------------------------------------
_lit995, _mod995 = _deva_exchange(
    "阿练若比丘，住空闲寂静，修梵行一食，何故颜色鲜？",
    "阿练若比丘住空闲处，寂静修梵行，一日一食，为什么脸色还那么鲜明？",
    "过去不追忧，未来不欣求，现在随所得，正念持而食；"
    "以是颜色鲜。驰想未来、追悔过去，愚火自煎，如雹断青草。",
    "他们不为过去忧悔，不为未来企求，只依当日所得，正念而食；"
    "所以脸色鲜明。若驰想未来、追悔过去，愚痴之火自煎，如冰雹打断青草。",
)
SUTTAS["SA_995"] = {
    "lit": _lit995,
    "mod": _mod995,
    "notes": (
        f"{PROV}confidence=high：primary SN1.10 Arañña。"
        "据 SN：不忧过去、不求未来、依现得而活，故颜色鲜；愚者反是如折芦。"
    ),
}

# --- SA 996 憍慢（SN1.9）-----------------------------------------------------
_lit996, _mod996 = _deva_exchange(
    "乐慢者难调，未定无寂默；独在林放逸，不度死彼岸。",
    "爱著我慢的人难以调伏，心未得定就谈不上牟尼寂默；"
    "独自在林中却放逸，不能度越死魔的彼岸。",
    "已舍慢善定，善心遍解脱；独在林不逸，能度死彼岸。",
    "舍弃我慢、内心善定，善心于一切处解脱；"
    "独自在林中不放逸，就能度越死魔的彼岸。",
)
SUTTAS["SA_996"] = {
    "lit": _lit996,
    "mod": _mod996,
    "notes": (
        f"{PROV}confidence=high：primary SN1.9 Mānakāma。"
        "据 SN 校正汉问偈：乐慢难调／无定无牟尼／林中放逸不度死；"
        "汉「不欲起憍慢」义倒，今从巴利。"
    ),
}

# --- SA 997 修福增（SN1.47）--------------------------------------------------
_lit997, _mod997 = _deva_exchange(
    "云何得昼夜，功德常增长？何人戒具足，当得往生天？",
    "怎样才能昼夜功德常增长？什么人住法具戒，能往生天？",
    "种园植林树，造桥及井泉，施僧坊客舍，功德日夜增；"
    "如法戒具足，如是得生天。",
    "种植园林、树木，造桥、井泉，布施僧坊客舍，功德日夜增长；"
    "住法具戒的人，因此得生天。",
)
SUTTAS["SA_997"] = {
    "lit": _lit997,
    "mod": _mod997,
    "notes": (
        f"{PROV}confidence=high：primary SN1.47 Vanaropa。"
        "据 SN：园／林／桥／井泉／僧坊；法住具戒者生天。"
    ),
}

# --- SA 998 云何大得（SN1.42）------------------------------------------------
_lit998, _mod998 = _deva_exchange(
    "施何得大力？施何得妙色？施何得安乐？施何得明目？"
    "谁名一切施？愿佛为分别。",
    "布施什么得大力？什么得妙色？什么得安乐？什么得明目？"
    "谁称为一切施？请佛分别说明。",
    "施食得大力，施衣得妙色，施乘得安乐，施灯得明目；"
    "施僧坊一切，说法施甘露。",
    "施食物得大力，施衣服得妙色，施车乘得安乐，施灯明得明目；"
    "施僧坊名为一切施，说法则是施甘露。",
)
SUTTAS["SA_998"] = {
    "lit": _lit998,
    "mod": _mod998,
    "notes": (
        f"{PROV}confidence=high：primary SN1.42 Kiṁdada。"
        "据 SN：食／衣／乘／灯；僧坊＝一切施；说法＝施甘露（amata）。"
    ),
}

# --- SA 999 生欢喜（SN2.23 Serī）---------------------------------------------
SUTTAS["SA_999"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，天子悉鞞梨来诣佛所，容色绝妙，稽首礼足，退坐一面；"
        "身诸光明遍照祇园。",
        "天子说偈问：「诸天及世人，皆于食欣乐；谁名彼夜叉，于食不欣乐？」",
        "世尊说偈答：「净信以惠施，此世及后世，随其所至处，福报常影随。"
        "是故当舍悭，行无垢惠施，施已心欢喜，此世他世受。」",
        "悉鞞梨白佛：「奇哉！善说。」复诵佛偈，自白："
        "「我昔为人王，名悉鞞梨，于四城门普施。"
        "夫人、王子、大臣、将士、庶民次第求分福，我以东、南、西、北门"
        "及城内四交道施处分属之，王施遂断。"
        "使者来白，我勅：边国岁入半分入库，半分即于彼处惠施。"
        "我长夜行施，得可爱可意福报，无有穷极；"
        "如五大河合流入海，功德聚不可称量。」",
        "天子闻已欢喜，礼足即没。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，名叫悉鞞梨的天子来到佛前，容色绝妙，顶礼佛足，退坐一面；"
        "身上光明遍照祇园。",
        "天子说偈问：「诸天和世人都喜爱饮食；那个不喜爱饮食的夜叉，名叫什么？」",
        "世尊说偈答：「以清净信心布施，此世与后世，福报如影随形。"
        "所以应当舍悭吝，行无垢布施；施后心欢喜，此世他世都受用。」",
        "悉鞞梨对佛说：「奇哉！说得好。」又诵一遍佛偈，并自述："
        "「我过去曾是国王，名叫悉鞞梨，在四城门普施。"
        "夫人、王子、大臣、将士、平民先后请求也有份作福，我便把东、南、西、北门"
        "和城内十字路口的施处分给他们，自己的布施因而中断。"
        "使者来报，我下令：边地岁入一半入库，一半就地布施。"
        "我长夜行施，得到可爱可意的福报，没有穷尽；"
        "如同五大河汇流入海，功德聚不可计量。」",
        "天子听完欢喜，顶礼佛足，随即隐没。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN2.23 Serī。"
        "据 SN 校正问偈：谁于食不喜（夜叉／yakkha）；答为净信惠施、舍悭。"
        "汉问「福乐自随逐」义偏，从巴利；四门分施叙事从汉本压缩。"
    ),
}

# --- SA 1000 远去（SN1.53）---------------------------------------------------
_lit1000, _mod1000 = _deva_exchange(
    "远行谁为友？居家谁为友？有事谁为友？后世谁为友？",
    "远行时谁是善知识？居家时谁是善知识？有事急需时谁是善知识？后世谁是善知识？",
    "商旅远行友，母亲居家友，盟友有事友，自修福后世友。",
    "商队是远行的朋友，母亲是居家的朋友，盟友是有事时的朋友，"
    "自己所修的福德是后世的朋友。",
)
SUTTAS["SA_1000"] = {
    "lit": _lit1000,
    "mod": _mod1000,
    "notes": (
        f"{PROV}confidence=high：primary SN1.53 Mitta。"
        "据 SN 校正：远行友＝商旅（sattha）；居家友＝母（mātā）；"
        "有事友＝盟友；后世友＝自作福。汉「贤良妻」「宗亲通财」从巴利改。"
    ),
}

# --- SA 1001 强亲回（SN1.3）--------------------------------------------------
_lit1001, _mod1001 = _deva_exchange(
    "寿命迁谢促，老逼无救护；观死大恐怖，当修福至乐。",
    "寿命被带走而短暂，为老所逼而无救护；看见死亡的大恐怖，应当修福趣向安乐。",
    "寿命迁谢促，老逼无救护；观死大恐怖，当舍世贪饵，趣无余涅槃。",
    "寿命被带走而短暂，为老所逼而无救护；看见死亡的大恐怖，"
    "应当舍弃世间饵食，趣向无余涅槃。",
)
SUTTAS["SA_1001"] = {
    "lit": _lit1001,
    "mod": _mod1001,
    "notes": (
        f"{PROV}confidence=high：primary SN1.3 Upanīya（亦近 SN2.19）。"
        "据 SN：观死怖后，求寂者应舍世间饵（lokāmisa），非仅「作诸功德」。"
    ),
}

# --- SA 1002 思惟（SN1.5）----------------------------------------------------
_lit1002, _mod1002 = _deva_exchange(
    "几法应当断？几法应当舍？几法应增修？越几得度流？",
    "应当断除几法？舍弃几法？增修几法？超越几法才算度越急流？",
    "断五复舍五，增修于五根，超越五和合，比丘度流渊。",
    "断五、舍五，再增修五法；超越五结缚，比丘便度越急流。",
)
SUTTAS["SA_1002"] = {
    "lit": _lit1002,
    "mod": _mod1002,
    "notes": (
        f"{PROV}confidence=high：primary SN1.5 Katichinda。"
        "据 SN：断五／舍五／修五／越五结则度流；汉「五根」作增修所缘，义从五上分。"
    ),
}

# --- SA 1003 睡寤（SN1.6）----------------------------------------------------
_lit1003, _mod1003 = _deva_exchange(
    "几人觉中眠？几人眠中觉？几人取尘垢？几人得清净？",
    "多少人在觉者中沉睡？多少人在睡者中清醒？多少人取尘垢？多少人得清净？",
    "五人觉中眠，五人眠中觉，五人取于垢，五人得清净。",
    "五人在觉者中沉睡，五人在睡者中清醒，五人取尘垢，五人得清净。",
)
SUTTAS["SA_1003"] = {
    "lit": _lit1003,
    "mod": _mod1003,
    "notes": (
        f"{PROV}confidence=high：primary SN1.6 Jāgara。"
        "据 SN：五盖眠于觉、五根觉于眠；五取垢、五净。"
    ),
}

# --- SA 1004 生欢喜（SN1.12）-------------------------------------------------
_lit1004, _mod1004 = _deva_exchange(
    "有子乐其子，有牛乐其牛；众生乐有余，无余则无乐。",
    "有子女的人以子女为乐，有牛的人以牛为乐；众生以有余依为乐，无余依便无乐。",
    "有子忧其子，有牛忧其牛；众生忧有余，无余则无忧。",
    "有子女的人因子女而忧，有牛的人因牛而忧；众生因有余依而忧，无余依便无忧。",
)
SUTTAS["SA_1004"] = {
    "lit": _lit1004,
    "mod": _mod1004,
    "notes": (
        f"{PROV}confidence=high：primary SN1.12 Nandati。"
        "据 SN：喜／忧皆由 upādhi（有余／执取）；无余依则无喜亦无忧。"
        "汉「母子」从 putta 作子女；义同。"
    ),
}

# --- SA 1005 义利（SN1.54）---------------------------------------------------
_lit1005, _mod1005 = _deva_exchange(
    "何为人依处？何为最上友？依何而活命，依地诸有情？",
    "什么是人的依处？什么是最上伴侣？依地而活的有情，靠什么活命？",
    "子为人依处，妻为最上友，依雨而活命，依地诸有情。",
    "子女是人的依处，妻子是最上伴侣；依地而活的有情，靠雨水活命。",
)
SUTTAS["SA_1005"] = {
    "lit": _lit1005,
    "mod": _mod1005,
    "notes": (
        f"{PROV}confidence=high：primary SN1.54 Vatthu。"
        "据 SN 校正：vatthu＝子；paramo sakhā＝妻；upajīvanti＝雨（vuṭṭhi）。"
        "汉「田宅／饮食／业」与巴利不合，今从 SN。"
    ),
}

# --- SA 1006 所爱无过子（SN1.13）---------------------------------------------
_lit1006, _mod1006 = _deva_exchange(
    "所爱无过子，财无贵于牛，光明无过日，水流无过海。",
    "爱著没有超过子女的，财富没有贵过牛的，光明没有超过太阳的，水流没有超过海的。",
    "爱无过于己，财无过于谷，光明无过慧，水流无过雨。",
    "爱著没有超过自己的，财富没有超过谷物的，光明没有超过智慧的，水流没有超过雨的。",
)
SUTTAS["SA_1006"] = {
    "lit": _lit1006,
    "mod": _mod1006,
    "notes": (
        f"{PROV}confidence=high：primary SN1.13 Natthiputtasama。"
        "据 SN 校正答偈：己／谷／慧／雨（vuṭṭhi）；汉「见」误，从巴利。"
    ),
}

# --- SA 1007 刹利（SN1.14）---------------------------------------------------
_lit1007, _mod1007 = _deva_exchange(
    "刹利两足尊，特牛四足胜，童女为上妻，长子为上子。",
    "刹利是两足中最上的，壮牛是四足中最上的，童女是妻子中最上的，长子是儿子中最上的。",
    "正觉两足尊，龙马四足胜，善听为贤妻，孝顺子之上。",
    "正等觉是两足中最上的，良马是四足中最上的，善于听从的是贤妻，孝顺的是儿子中最上的。",
)
SUTTAS["SA_1007"] = {
    "lit": _lit1007,
    "mod": _mod1007,
    "notes": (
        f"{PROV}confidence=high：primary SN1.14 Khattiya。"
        "据 SN：佛／ājānīya／sussūsā（善听）／assava（顺教子）；"
        "汉答「漏尽子」义偏，从巴利。"
    ),
}

# --- SA 1008 种子（SN1.74）---------------------------------------------------
SUTTAS["SA_1008"] = {
    "lit": [
        OPEN_JET_LIT,
        "后夜分，有天子来诣佛所，容色绝妙，稽首礼足；身光遍照祇园。",
        "天子问偈：「从地起者何最胜？于空堕落何为上？何所依止最为胜？诸说之中谁上辩？」",
        "有天子本为田家，以宿习答：「五谷从地起最胜，种子于空落为上，特牛依止最为胜，爱子所说为上辩。」",
        "问者斥曰：「我不问汝。」复以偈问佛。",
        "世尊答：「明从下踊出最胜，无明于空落为上，僧为依止最为胜，佛说诸说之上辩。」",
        "天子复问：「世间几法起？几法相随顺？几法取于爱？几法当损减？」",
        "佛答：「世六法等起，世六法随顺，世六法取爱，世六法损减。」",
        DEVA_CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "后夜分，有一位天子来到佛前，容色绝妙，顶礼佛足；身光遍照祇园。",
        "天子问偈：「从地涌起的什么最上？从空中落下的什么最上？"
        "什么依止最上？什么说法最上？」",
        "有位前世务农的天子凭旧习回答：「五谷从地起最上，种子从空落下最上，"
        "壮牛是依止中最上，爱子的话是言语中最上。」",
        "发问的天子斥责说：「我不是问你。」再以偈问佛。",
        "世尊答：「明从下涌起最上，无明从空落下最上，僧伽是依止最上，佛说是最上辩才。」",
        "天子又问：「世间几法俱起？几法相随顺？几法取著为爱？几法应当减损？」",
        "佛答：「世间六法俱起，六法随顺，六法取爱，六法损减。」",
        DEVA_CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.74 Bīja。"
        "据 SN：田家答种子／雨／牛／子；佛答 vijjā／avijjā／saṅgha／buddha。"
        "汉「三明」作踊出／落下，今作明／无明；末段六法问答为汉本所有，SN1.74 无，保留并志异。"
    ),
}

# --- SA 1009 意（SN1.62）-----------------------------------------------------
_lit1009, _mod1009 = _deva_exchange(
    "谁牵世间转？谁复拘世间？何法为唯一，令一切随转？",
    "什么牵动世间运转？什么拖曳世间？哪一法使一切都受其控制？",
    "心牵世间转，心复拘世间，心法为唯一，令一切随转。",
    "心牵动世间运转，心拖曳世间；心这一法，使一切都受其控制。",
)
SUTTAS["SA_1009"] = {
    "lit": _lit1009,
    "mod": _mod1009,
    "notes": (
        f"{PROV}confidence=high：primary SN1.62 Citta（汉题「意」）。"
        "据 SN：citta 牵／拘世间，为唯一能制御者；汉「心／意」互通。"
    ),
}

# --- SA 1010 缚（SN1.64）-----------------------------------------------------
_lit1010, _mod1010 = _deva_exchange(
    "何法缚世间？何法令流转？断除于何法，说名得涅槃？",
    "什么系缚世间？什么使它四处转想？断除什么才叫做涅槃？",
    "喜能缚世间，寻伺令流转，断除于爱欲，说名得涅槃。",
    "欢喜系缚世间，寻伺使它流转；断除渴爱，才叫做涅槃。",
)
SUTTAS["SA_1010"] = {
    "lit": _lit1010,
    "mod": _mod1010,
    "notes": (
        f"{PROV}confidence=high：primary SN1.64 Saṁyojana。"
        "据 SN 校正：nandī 缚世间；vitakka 为流转；断 taṇhā 名涅槃。"
        "汉「欲能缚／调伏欲」义偏，从巴利喜／寻伺／爱。"
    ),
}

# ---------------------------------------------------------------------------
# confidence / reconstructed
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_991": "high",
    "SA_992": "high",
    "SA_993": "medium",
    "SA_994": "medium",
    "SA_995": "high",
    "SA_996": "high",
    "SA_997": "high",
    "SA_998": "high",
    "SA_999": "high",
    "SA_1000": "high",
    "SA_1001": "high",
    "SA_1002": "high",
    "SA_1003": "high",
    "SA_1004": "high",
    "SA_1005": "high",
    "SA_1006": "high",
    "SA_1007": "high",
    "SA_1008": "high",
    "SA_1009": "high",
    "SA_1010": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_996": "汉问偈「不欲起憍慢」与 SN1.9 乐慢难调义倒；据巴利改正。",
    "SA_999": "汉问偈偏「福乐自随」；据 SN2.23 校正为谁于食不喜。",
    "SA_1000": "汉居家友作贤妻、通财作宗亲；据 SN1.53 校正为母／盟友。",
    "SA_1005": "汉答田宅／饮食／业；据 SN1.54 校正为子／妻／雨。",
    "SA_1006": "汉答「见」；据 SN1.13 校正为雨（vuṭṭhi）。",
    "SA_1007": "汉答「漏尽子」；据 SN1.14 校正为顺教／孝顺子。",
    "SA_1010": "汉「欲缚／调欲」；据 SN1.64 校正为喜缚、寻伺流转、断爱。",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

BATCH_IDS = [f"SA_{i}" for i in range(991, 1011)]
NEIGHBOR_IDS = {"SA_990", "SA_1011"}

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


def main() -> None:
    aligned = ROOT / "data" / "aligned" / "raw_aligned_data.json"
    out = ROOT / "data" / "translated" / "final_translated_data.json"
    gold_dir = ROOT / "data" / "golden"
    gold_dir.mkdir(parents=True, exist_ok=True)

    if out.exists():
        records = json.loads(out.read_text(encoding="utf-8"))
    else:
        records = json.loads(aligned.read_text(encoding="utf-8"))

    # Snapshot neighbors SA_990 / SA_1011
    neighbor_before = {
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
        if rec["id"] in NEIGHBOR_IDS
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

    for rid, before in neighbor_before.items():
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
                assert before == after, f"{rid} (neighbor) must remain untouched"
                break

    # Ensure we did not accidentally put neighbors in GOLD
    assert NEIGHBOR_IDS.isdisjoint(GOLD), "neighbors must not be in GOLD"

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa991-1010.json").write_text(
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
    continuous_991_1010 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(991, 1011)
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_991–SA_1010 only)")
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
    print(f"continuous_gold_SA_991–1010={continuous_991_1010}")
    print(f"SA_990_untouched={ 'SA_990' in neighbor_before }")
    print(f"SA_1011_untouched={ 'SA_1011' in neighbor_before }")
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
