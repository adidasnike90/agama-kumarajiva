#!/usr/bin/env python3
"""Retranslate SA 611–630（卷第二十六 念处相应）→ merge.

本批二十经：善聚 SN47.5；弓 MN12（resembling）；不善聚（无平行）；大丈夫 SN47.11；
比丘尼 SN47.10；厨士 SN47.8；鸟 SN47.6；四果（无平行）；私迦陀 SN47.19；猿猴 SN47.7；
年少比丘 SN47.4；菴罗女 SN47.2；世间 SN47.20；郁低迦 SN47.16；婆醯迦 SN47.15；
比丘 peyyāla；阿那律 SN47.26；优陀夷 SN47.21；行 SN47.23；行（无平行）。

信：有 SN 平行者据巴利／Sujato 厘义；612／613／618／630 无可靠专经 → medium；
    625–626 peyyāla／交叉指示 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
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

OPEN_RAJ_BAM_LIT = "如是我闻：一时，佛住王舍城迦兰陀竹园。"
OPEN_RAJ_BAM_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

OPEN_VES_AMB_LIT = "如是我闻：一时，佛在跋祇人间游行，住鞞舍离菴罗园。"
OPEN_VES_AMB_MOD = "我是这样听说的：有一次，佛在跋祇人间游行，住在鞞舍离菴罗园。"

OPEN_BAN_LIT = "如是我闻：一时，佛住波罗奈仙人住处鹿野苑中。"
OPEN_BAN_MOD = "我是这样听说的：有一次，佛住在波罗奈仙人住处鹿野苑中。"

OPEN_SED_LIT = "如是我闻：一时，佛在拘萨罗人间游行，于私伽陀聚落北身恕林中。"
OPEN_SED_MOD = "我是这样听说的：有一次，佛在拘萨罗人间游行，住在私伽陀聚落北身恕林中。"

OPEN_PAT_LIT = "如是我闻：一时，佛住巴连弗邑鸡林精舍。"
OPEN_PAT_MOD = "我是这样听说的：有一次，佛住在巴连弗邑鸡林精舍。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_ONE_LIT = "彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_ONE_MOD = "他听佛所说，欢喜随喜，行礼后离去。"

SATI4_LIT = "身身观念住，受、心、法法观念住"
SATI4_MOD = "身、受、心、法四念处"
SATI_FULL_LIT = (
    "身身观念住，精勤方便，正念正知，调伏世间贪忧；"
    "受、心、法法观念住亦复如是"
)
SATI_FULL_MOD = (
    "于身随观而住，精勤方便，正念正知，调伏世间贪忧；"
    "于受、心、法随观而住也是一样"
)

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)


# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 611 善聚（SN47.5）----------------------------------------------------
SUTTAS["SA_611"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「善法聚者，谓四念处——身、受、心、法，是为正说；"
        "不善法聚者，谓五盖——贪欲、瞋恚、睡眠、掉悔、疑，是为正说。"
        "所以者何？纯一满净之聚，唯四念处；纯一不善之聚，唯五盖。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「善法的聚集，就是四念处——身、受、心、法，这样说才正确；"
        "不善法的聚集，就是五盖——贪欲、瞋恚、昏沉睡眠、掉举后悔、疑，这样说才正确。"
        "为什么？纯粹圆满清净的聚集，只有四念处；纯粹不善的聚集，只有五盖。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.5（kusalarāsi／akusalarāsi）。"
        "据 SN 校正：善聚＝四念处，不善聚＝五盖；汉本「逸满」从 SN kevalo 作纯一。"
    ),
}

# --- SA 612 弓（MN12 resembling）---------------------------------------------
SUTTAS["SA_612"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「如人持四强弓，迅射多罗树影，疾过无阂。"
        "如是如来四种声闻，利根增上，尽百年寿，除食息书写睡眠，"
        "常说常听，尽底受持，不加再问——听法尽寿，如来说法犹不尽。"
        "当知如来名句味身无量无边，所谓四念处：身、受、心、法。」",
        "「是故比丘！于四念处修习，起增上欲，精勤方便，正念正知，应当学。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「好比有人拿着四张强弓，迅速射过多罗树影，快得没有障碍。"
        "同样，如来的四种声闻，利根又精进，尽百年寿命，除去吃饭、休息、书写、睡眠，"
        "常说常听，彻底受持，不再追问——听法到寿命尽，如来的法还是说不完。"
        "应当知道，如来的名、句、味身无量无边，说的就是四念处：身、受、心、法。」",
        "「所以比丘们！应当于四念处修习，起增上欲，精勤方便，正念正知，应当学。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "SC 仅列 MN12／T757 等 resembling（师子吼中「说法不尽」类譬），无 SN47 专经。"
        "confidence=medium：义从汉本四声闻百年听法不尽＋四念处总句；罗什风压缩。"
    ),
}

# --- SA 613 不善聚（无平行）--------------------------------------------------
SUTTAS["SA_613"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「不善聚者，谓三不善根——贪、恚、痴，是为正说；"
        "善聚者，谓四念处——身、受、心、法，是为正说。」",
        "「如三不善根，如是三恶行——身口意；三想——欲、恚、害；"
        "三觉——欲、恚、害；三界——欲、恚、害：皆以四念处为对治善聚。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「不善的聚集，就是三不善根——贪、瞋、痴，这样说才正确；"
        "善的聚集，就是四念处——身、受、心、法，这样说才正确。」",
        "「如同三不善根，三恶行——身、口、意；三想——欲想、恚想、害想；"
        "三觉——欲觉、恚觉、害觉；三界——欲界、恚界、害界：都以四念处为对治的善聚。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "无 SC 巴利专经；与 SA_611／SN47.5 同型而开三不善根及 peyyāla 系列。"
        "confidence=medium：从汉本，压缩重复「佛说此经已」为一条。"
    ),
}

# --- SA 614 大丈夫（SN47.11）-------------------------------------------------
SUTTAS["SA_614"] = {
    "lit": [
        OPEN_JET_LIT,
        "时，有异比丘问佛：「云何大丈夫？云何非大丈夫？」",
        "佛言：「善哉！谛听。若修四念处而心不离贪、不得解脱、不尽有漏，"
        "我不说彼为大丈夫——心未解脱故。"
        "若修四念处，心离贪、得解脱、尽诸有漏，我说彼为大丈夫——心解脱故。」",
        "彼比丘闻已，欢喜随喜，礼足而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时，有一位比丘问佛：「怎样是大丈夫？怎样不是大丈夫？」",
        "佛说：「很好！仔细听。如果修四念处而心不离贪、不得解脱、不尽有漏，"
        "我不说他是大丈夫——因为心还没有解脱。"
        "如果修四念处，心离贪、得解脱、尽诸有漏，我说他是大丈夫——因为心已解脱。」",
        "那位比丘听完，欢喜随喜，顶礼后离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.11（mahāpurisa＝心解脱 vimuttacitta）。"
        "据 SN 校正：判准在心解脱／未解脱；汉「异比丘」问，SN 作舍利弗，问者从汉本。"
        "「离贪」＝virajjati，不作「厌故不乐」。"
    ),
}

# --- SA 615 比丘尼（SN47.10）-------------------------------------------------
SUTTAS["SA_615"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者阿难晨朝入城乞食，先至比丘尼寺。诸尼礼足，白言："
        "「我等修四念处系心住，自知前后升降。」"
        "阿难叹言：「善哉！修四念处善系心者，应如是知前后升降。」"
        "为说法已，乞食还，以事白佛。",
        "佛告阿难：「善哉！应如是学。心外驰求，当制令还；散乱、未解脱，皆如实知。"
        "若身观住时身沈心怠，当取净相，起净信——信已心悦，悦已生喜，"
        "喜已身猗，猗已受乐，乐已心定；定已舍觉观，舍念乐住，如实知。"
        "受、心、法念亦如是。」",
        "阿难闻已，欢喜奉行。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "阿难尊者早晨进城乞食，先到比丘尼寺。比丘尼们顶礼后说："
        "「我们修四念处系心而住，自己知道前后的进退升降。」"
        "阿难赞叹说：「很好！修四念处善系心的人，应当这样知道前后升降。」"
        "为她们说法后，乞食回来，把这件事禀告佛。",
        "佛告诉阿难：「很好！应当这样学。心向外驰求时，要制令回来；"
        "散乱、未解脱，都要如实知道。"
        "如果观身时身体沉滞、心法懈怠，应当取净相，生起净信——"
        "有信则心悦，悦则生喜，喜则身轻安，轻安则受乐，乐则心定；"
        "定后舍离觉观，舍而正念乐住，如实了知。受、心、法念也是一样。」",
        "阿难听完，欢喜奉行。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.10（比丘尼精舍；前后升降＝uttarī nissāraṇa）。"
        "据 SN 校正：系心四念处能得 visesa；身沈心散时以净相调心入定。"
        "罗什风压缩 SN／汉本觉支链。"
    ),
}

# --- SA 616 厨士（SN47.8）----------------------------------------------------
SUTTAS["SA_616"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当取自心相，莫令外散。"
        "愚比丘不取内心而取外相，退减自障——如愚厨士不善谐味、不伺主嗜，"
        "自用调和，主不悦，不得赏念；彼修身观，不能断上烦恼，"
        "不得内心寂静、正念正知，不得四增上心、现法乐住与安隐涅槃。」",
        "「黠慧比丘先取内心，后摄外相，终不退减——如黠厨士善伺主心，"
        "味适主悦，得禄爱念；彼修身观，断上烦恼，内心寂止，正念正知，"
        "得四增心、现法乐住、安隐涅槃。受、心、法观亦如是。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「应当取自己内心的相，不要让心向外散乱。"
        "愚笨的比丘不取内心而取外相，就会退减、自己障碍——好比愚笨厨子"
        "不会调味、不观察主人的嗜好，自作主张，主人不高兴，得不到赏赐；"
        "他修身观，不能断除粗重烦恼，得不到内心寂静、正念正知，"
        "也得不到四增上心、现法乐住与安隐涅槃。」",
        "「聪慧的比丘先取内心，再摄持外相，终不退减——好比聪慧厨子"
        "善于观察主人的心，味道合宜，主人欢喜，得到俸禄宠爱；"
        "他修身观，断除粗重烦恼，内心寂止，正念正知，"
        "得四增上心、现法乐住、安隐涅槃。受、心、法观也是一样。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.8（sūda 厨士譬）。"
        "据 SN 校正：愚者不取内心相（nimitta），不得三摩地、断漏；黠者反是。"
        "「上烦恼」＝upakkilesa；压缩汉本酸咸酢淡枚举。"
    ),
}

# --- SA 617 鸟（SN47.6）------------------------------------------------------
SUTTAS["SA_617"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「昔有罗婆鸟为鹰所捉，空中鸣言：『我舍父母境界游他处，故遭此难。』"
        "鹰问：『何处是汝自境界？』答：『耕垄块下，乃我家境。』"
        "鹰骄放之。罗婆入块下，鹰猛扑，臆冲坚块，碎身而死。"
        "罗婆说偈：『鹰恃力来搏，罗婆依自界；乘瞋猛盛力，致祸碎其身。"
        "我依自境界，智慧胜龙象；观智摧苍鹰。』」",
        "「如是比丘！莫舍自境界游他处。他境界者，五欲——眼色乃至身触，欲心染着；"
        "自境界父母处者，四念处——身、受、心、法。是故当依自界，远离他境，应当学。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「从前有一只鹌鹑被鹰抓住，在空中叫道：『我离开父母的境界到别处去，才遭此难。』"
        "鹰问：『哪里是你自己的境界？』答：『耕地土块下面，才是我家境。』"
        "鹰骄傲地放了它。鹌鹑钻进土块下，鹰猛扑，胸口撞上坚硬土块，粉身碎骨而死。"
        "鹌鹑说偈：『鹰仗着力来搏，鹌鹑依靠自界；趁着瞋怒猛力，反而碎了自身。"
        "我依自己境界，智慧胜过龙象；以智摧破苍鹰。』」",
        "「同样，比丘们！不要离开自己的境界到别处去。别人的境界，就是五欲——"
        "眼所见色乃至身所触，生起欲心染着；自己父母境界，就是四念处——身、受、心、法。"
        "所以应当依止自界，远离他境，应当学。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.6（sakuṇagghi 鹰鹌鹑）。"
        "据 SN 校正：他境＝五欲，自境＝四念处；游他境则魔得便。"
        "汉「罗婆」＝鹌鹑；偈压缩。"
    ),
}

# --- SA 618 四果（无平行）----------------------------------------------------
SUTTAS["SA_618"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「多修四念处，当得四果、四种福利——"
        "须陀洹、斯陀含、阿那含、阿罗汉。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「多多修习四念处，就能得到四果、四种福利——"
        "须陀洹、斯陀含、阿那含、阿罗汉。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "无 SC 巴利专经；义合早期「四念处→四沙门果」通义（cf. SN47 系福利经）。"
        "confidence=medium。"
    ),
}

# --- SA 619 私迦陀（SN47.19）-------------------------------------------------
SUTTAS["SA_619"] = {
    "lit": [
        OPEN_SED_LIT,
        "佛告比丘：「昔有缘幢伎师，肩竖幢，语弟子：『上下互护，嬉戏得利。』"
        "弟子言：『不如各自护——自护则安隐而下。』"
        "师然之：『自护即护他，护他亦护己。"
        "云何自护护他？修习随护作证。云何护他自护？不怖、不违、不害，慈心哀彼。』"
        "是故比丘！自护者修四念处，护他者亦修四念处。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_SED_MOD,
        "佛告诉比丘：「从前有走竹竿的艺人，肩上竖起竹竿，对弟子说：『上下互相护持，表演就能得利。』"
        "弟子说：『不如各自护持——自己护好自己，才能安隐下来。』"
        "师父同意：『保护自己就是保护他人，保护他人也是保护自己。"
        "怎样由自护而护他？修习、随护、作证。怎样由护他而自护？"
        "不令他恐怖、不违背他、不伤害他，以慈心哀愍他。』"
        "所以比丘们！要自护就修四念处，要护他也修四念处。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.19（Sedaka 竹竿譬）。"
        "据 SN 校正：自护＝修习四念处；护他＝安忍不害慈心；自护即护他。"
        "地点从汉本私伽陀／身恕林（SN 作 Sumbha Sedaka）。"
    ),
}

# --- SA 620 猿猴（SN47.7）----------------------------------------------------
SUTTAS["SA_620"] = {
    "lit": [
        OPEN_RAJ_BAM_LIT,
        "佛告比丘：「雪山有处人兽不到；有处唯猿所居；有处人兽共居。"
        "猎师以黐胶涂草，黠猿远避，愚猿以手触——手胶；二手、二足、口求解，五处同胶，"
        "猎师杖贯担去。愚猿舍自境界游他境，故致斯苦。」",
        "「愚比丘依聚落，入村不护根门，于五欲生染，内根外境五缚，随魔所欲。"
        "是故当依自界父母处——四念处：身、受、心、法，莫随他境行。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_BAM_MOD,
        "佛告诉比丘：「大雪山里，有的地方人兽都到不了；有的地方只有猿猴住；有的地方人兽共住。"
        "猎师把黏胶涂在草上，聪明的猿猴远远避开，愚笨的用手提——手粘住；"
        "两手、两脚、嘴去解，五处都粘住，猎师用杖贯穿扛走。"
        "愚猿离开自己境界到别处，才招来这种苦。」",
        "「愚笨比丘依聚落住，进村不护根门，对五欲生染着，内根外境五处被缚，随魔所欲。"
        "所以应当依止自己父母境界——四念处：身、受、心、法，不要随他境而行。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.7（makkaṭa 猕猴黐胶）。"
        "据 SN 校正：五处被缚＝五欲；自境＝四念处；游他境则魔得便。"
    ),
}

# --- SA 621 年少比丘（SN47.4）------------------------------------------------
SUTTAS["SA_621"] = {
    "lit": [
        OPEN_JET_LIT,
        "阿难与诸比丘诣佛，问：「年少比丘当云何教授？」",
        "佛告阿难：「当以四念处教令修习——"
        f"{SATI_FULL_LIT}，乃至知身、知法。"
        "有学未得上进、志求安隐涅槃者，亦当如是修；"
        "阿罗汉漏尽、所作已办者，亦当如是修，于法得远离。」",
        "阿难欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "阿难和比丘们来见佛，问：「年少比丘应当怎样教授？」",
        "佛告诉阿难：「应当用四念处教导他们修习——"
        f"{SATI_FULL_MOD}，乃至了知身、了知法。"
        "有学还没有上进、志求安隐涅槃的人，也应当这样修；"
        "阿罗汉漏尽、该做的已做的人，也应当这样修，于法得远离。」",
        "阿难欢喜随喜，行礼后离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.4（Sāla；教年少修四念处）。"
        "据 SN 校正：有学为知法／满知，阿罗汉亦修四念处以远离；汉问者阿难从汉本。"
    ),
}

# --- SA 622 菴罗女（SN47.2）--------------------------------------------------
SUTTAS["SA_622"] = {
    "lit": [
        OPEN_VES_AMB_LIT,
        "菴罗女庄严乘车来诣。佛遥见，告诸比丘：「勤摄心住，正念正智——菴罗女来，是故诫汝。"
        "云何勤摄心？已生恶断，未生恶不生；未生善令生，已生善令增满——生欲精勤摄心。"
        "云何正智？去来威仪、顾视屈伸、衣钵行住坐卧、眠觉语默，皆随正智。"
        f"云何正念？{SATI_FULL_LIT}。」",
        "菴罗女至，礼足听法。佛为说法示教照喜；女请明日供食，佛默受。"
        "翌日供毕，佛说随喜偈已，从座而去。",
    ],
    "mod": [
        OPEN_VES_AMB_MOD,
        "菴罗女打扮乘车前来。佛远远看见，告诉比丘们：「要勤摄心住，正念正智——"
        "菴罗女来了，所以告诫你们。"
        "什么是勤摄心？已生的恶要断，未生的恶不让生；未生的善让它生，已生的善让它增长圆满——"
        "生起欲乐、精勤摄心。"
        "什么是正智？往来威仪、顾视屈伸、持衣钵、行住坐卧、睡眠觉醒、说话沉默，都随正智。"
        f"什么是正念？{SATI_FULL_MOD}。」",
        "菴罗女到来，顶礼听法。佛为她说法示教照喜；她请明天供食，佛默然接受。"
        "第二天供养完毕，佛说随喜偈后，起座离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.2（sati＋sampajañña）。"
        "据 SN 校正：核心教诫为正念正知而住；汉本增菴罗女请食及随喜偈，压缩保留框架。"
        "「调伏世间贪忧」＝vineyya loke abhijjhādomanassaṁ。"
    ),
}

# --- SA 623 世间（SN47.20）---------------------------------------------------
SUTTAS["SA_623"] = {
    "lit": [
        OPEN_BAN_LIT,
        "佛问比丘：「世间美色，能令多人聚观不？若复歌舞伎乐，众益多不？」"
        "答：「如是。」",
        "「若有士夫乐乐背苦、贪生畏死，令人持满油钵，经美色及大众中过，拔刀者随后——"
        "失一滴油则斩。彼能不顾美色大众，唯念油钵否？」"
        "答：「不也——唯一心系油钵，徐步而过。」",
        "「如是沙门正身自重，一其心念，不顾声色，善摄心法，住身念处者，"
        "则是我弟子。身念处者，精勤正念，调伏世间贪忧；受、心、法亦如是——"
        "油钵譬者，即身念处。」",
        "说偈：「专心护油钵，自心随护持；胜妙微细法，诸佛教如剑。"
        "当一其心护，非彼放逸人，能入不放逸。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_BAN_MOD,
        "佛问比丘：「世间的美色，能让许多人聚集观看吗？如果再加上歌舞伎乐，人会更多吗？」"
        "答：「是的。」",
        "「假如有人喜欢快乐、背离痛苦、贪生怕死，有人叫他端着满满一钵油，从美色和大众中间走过，"
        "后面跟着拔刀的人——洒一滴油就砍头。他还能不看美色大众、只想着油钵吗？」"
        "答：「不能——只会一心系念油钵，慢慢走过。」",
        "「同样，沙门端正自重，一心专注，不顾声色，善摄心法，安住身念处的人，"
        "才是我的弟子。身念处，就是精勤正念，调伏世间贪忧；受、心、法也是一样——"
        "油钵的比喻，指的就是身念处。」",
        "说偈：「专心护持油钵，自己护好心；胜妙微细的法，诸佛教如利剑。"
        "应当一心护持，不是放逸的人，能进入不放逸的教。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.20（janapadakalyāṇī 油钵譬）。"
        "据 SN 校正：油钵＝kāyagatā sati（身念）；地点汉作波罗奈，SN 作 Sedaka，从汉本。"
        "汉广开四念处，SN 重心在身念，今两存而以身念为譬之本。"
    ),
}

# --- SA 624 郁低迦（SN47.16）-------------------------------------------------
SUTTAS["SA_624"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者郁低迦请佛略说法要，愿独静不放逸，乃至不受后有。"
        "佛言：「先净初业，然后修梵行——净戒、直见、具足三业，依戒修四念处："
        f"内身、外身、内外身，{SATI_FULL_LIT}。"
        "如是修者，能越死魔境界。」",
        "郁低迦欢喜而去，独静专精，乃至自知不受后有。"
        "异比丘所问亦如是。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "郁低迦尊者请佛简要说法，希望独自静处不放逸，乃至不受后有。"
        "佛说：「先清净初步的业，然后再修梵行——清净戒、正直见、具足三业，"
        f"依戒修四念处：内身、外身、内外身，{SATI_FULL_MOD}。"
        "这样修习，就能越过死魔的境界。」",
        "郁低迦欢喜离去，独自静处专精，乃至自知不受后有。"
        "其他比丘所问也是一样。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.16（Uttiya）。"
        "据 SN 校正：初业＝净戒＋正见；依戒修四念处则越过 Māra／死境。"
        "汉「如上广说」peyyāla 据 SN 补出越死魔句；异比丘例从汉本。"
    ),
}

# --- SA 625 婆醯迦（SN47.15）-------------------------------------------------
SUTTAS["SA_625"] = {
    "lit": [
        OPEN_JET_LIT,
        "比丘婆醯迦请佛略说法要，如郁低迦所问。"
        "佛言：「先净初业——净戒直见，然后修四念处。"
        "身身观念住者，超越诸魔；受、心、法观念住者，亦超越诸魔。」",
        "婆醯迦欢喜而去，独静专精，乃至不受后有。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "比丘婆醯迦请佛简要说法，如同郁低迦所问。"
        "佛说：「先清净初步的业——净戒与正见，然后再修四念处。"
        "修身念处的人，能超越诸魔；修受、心、法念处的人，也能超越诸魔。」",
        "婆醯迦欢喜离去，独自静处专精，乃至不受后有。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.15（Bāhiya）；汉本明示「如前郁低迦」peyyāla。"
        "差别从汉：「超越诸魔」；SN 作日夜于善法增长不衰退——义近不退堕魔境。"
        "gold_reconstructed：据 SA_624 框补略说。"
    ),
}

# --- SA 626 比丘（peyyāla）---------------------------------------------------
SUTTAS["SA_626"] = {
    "lit": [
        OPEN_JET_LIT,
        "第二经亦如上说。差别者：「如是，比丘！修四念处，超越生死。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "第二经也如上说。差别是：「同样，比丘！修四念处，超越生死。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "底本为交叉指示 peyyāla（「第二经亦如上说」）；"
        "gold_reconstructed：据 SA_624／625 框补开经结，保留「超越生死」差别句。"
        "confidence=medium。"
    ),
}

# --- SA 627 阿那律（SN47.26）-------------------------------------------------
SUTTAS["SA_627"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者阿那律问佛：「有学未得上进安隐涅槃而方便求者，"
        "当云何于正法律多修习，得尽诸漏、自知不受后有？」",
        f"佛言：「当修四念处——{SATI_FULL_LIT}。"
        "多修习已，得尽诸漏，乃至自知不受后有。」",
        "阿那律欢喜随喜，作礼而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "阿那律尊者问佛：「有学还没有上进到安隐涅槃、却在方便求进的人，"
        "应当怎样在正法律中多多修习，才能尽诸漏、自知不受后有？」",
        f"佛说：「应当修四念处——{SATI_FULL_MOD}。"
        "多多修习之后，就能尽诸漏，乃至自知不受后有。」",
        "阿那律欢喜随喜，行礼后离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：parallel SN47.26（padesa／有学部分修四念处），resembling。"
        "汉作阿那律问佛求尽漏；SN 作舍利弗问阿那律「何名有学」——叙事从汉，"
        "义取有学当修四念处以尽漏。"
    ),
}

# --- SA 628 优陀夷（SN47.21）-------------------------------------------------
SUTTAS["SA_628"] = {
    "lit": [
        OPEN_PAT_LIT,
        "尊者优陀夷、尊者阿难亦住彼。优陀夷问阿难："
        "「如来为诸比丘说圣戒，令不断不缺、善究竟、智者所叹——何故说此圣戒？」",
        f"阿难答：「为修四念处故——{SATI4_LIT}。」",
        "二正士论已，各还本处。",
    ],
    "mod": [
        OPEN_PAT_MOD,
        "优陀夷尊者、阿难尊者也住在那里。优陀夷问阿难："
        "「如来为比丘们说圣戒，使它不断不缺、善能究竟、智者称叹——为什么说这样的圣戒？」",
        f"阿难答：「是为了修四念处——{SATI4_MOD}。」",
        "两位正士讨论完毕，各自回住处。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.21（sīla 为修四念处）。"
        "据 SN 校正：说戒目的＝修四念处；汉问者优陀夷，SN 作跋陀罗，人名从汉本。"
    ),
}

# --- SA 629 行（SN47.23）-----------------------------------------------------
SUTTAS["SA_629"] = {
    "lit": [
        OPEN_PAT_LIT,
        "尊者阿难、尊者跋陀罗亦在彼住。跋陀罗问阿难："
        "「有法多修习，能令行者不退转否？」",
        f"阿难答：「有——修四念处则不退转；不修则退减。谓{SATI4_LIT}。」",
        "二正士论已，各还本处。",
    ],
    "mod": [
        OPEN_PAT_MOD,
        "阿难尊者、跋陀罗尊者也住在那里。跋陀罗问阿难："
        "「有没有一种法，多多修习能使修行人不退转？」",
        f"阿难答：「有——修四念处就不退转；不修就会退减。就是{SATI4_MOD}。」",
        "两位正士讨论完毕，各自回住处。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.23（parihāna 正法衰退／不衰退）。"
        "据 SN 校正：不修四念处则衰退，修则不衰退；汉问「不退转」与 SN 不衰退同趣。"
        "人名跋陀罗与 SN Bhadda 合。"
    ),
}

# --- SA 630 行（无平行）------------------------------------------------------
SUTTAS["SA_630"] = {
    "lit": [
        OPEN_PAT_LIT,
        "尊者阿难、尊者跋陀罗亦在彼住。跋陀罗问阿难："
        "「有法多修习，令不净众生得清淨、转增光泽否？」",
        f"阿难答：「有——修四念处，能令不净得净、转增光泽。谓{SATI4_LIT}。」",
        "二正士论已，各还本处。",
    ],
    "mod": [
        OPEN_PAT_MOD,
        "阿难尊者、跋陀罗尊者也住在那里。跋陀罗问阿难："
        "「有没有一种法，多多修习能使不净的众生得到清净、展转增上光泽？」",
        f"阿难答：「有——修四念处，能使不净得净、展转增上光泽。就是{SATI4_MOD}。」",
        "两位正士讨论完毕，各自回住处。",
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "无 SC 巴利专经；与 SA_629 同框而问清淨光泽（cf. SN47 系增长／不退义）。"
        "confidence=medium：从汉本。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_611": "high",
    "SA_612": "medium",
    "SA_613": "medium",
    "SA_614": "high",
    "SA_615": "high",
    "SA_616": "high",
    "SA_617": "high",
    "SA_618": "medium",
    "SA_619": "high",
    "SA_620": "high",
    "SA_621": "high",
    "SA_622": "high",
    "SA_623": "high",
    "SA_624": "high",
    "SA_625": "high",
    "SA_626": "medium",
    "SA_627": "high",
    "SA_628": "high",
    "SA_629": "high",
    "SA_630": "medium",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_625": "peyyāla on SA_624 Uttiya frame; difference 超越诸魔 (cf. SN47.15)",
    "SA_626": "cross-ref peyyāla to prior; difference 超越生死",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(611, 631)}, (
        "GOLD must cover SA_611–SA_630 exactly"
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

    # Boundary: SA_610 must remain untouched
    boundary_id = "SA_610"
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

    # Also snapshot SA_631 if present
    untouched_after = {}
    for i in range(631, 636):
        rid = f"SA_{i}"
        for rec in records:
            if rec["id"] == rid:
                untouched_after[rid] = json.dumps(
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

    for rid, before in untouched_after.items():
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
                assert before == after, f"{rid} must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa611-630.json").write_text(
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
    continuous_611_630 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(611, 631)
    )
    continuous_1_630 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(1, 631)
    )
    untouched_591_610 = all(f"SA_{i}" not in GOLD for i in range(591, 611))

    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛", "如如"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_611–SA_630 only)")
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
    print(f"continuous_gold_SA_611–630={continuous_611_630}")
    print(f"continuous_gold_SA_1–630={continuous_1_630}")
    print(f"SA_591–610_untouched={untouched_591_610}")
    print(f"{boundary_id}_untouched=True")
    print("SA_631+_untouched=True")
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
