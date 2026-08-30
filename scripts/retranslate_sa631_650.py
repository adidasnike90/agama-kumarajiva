#!/usr/bin/env python3
"""Retranslate SA 631–650（念处相应末 + 根力相应起）→ merge.

本批二十经：行／行／一切法（念处，或无专 SN）；贤圣 SN47.17；光泽；比丘；
波罗提木叉 SN47.46；纯陀 SN47.13；布萨 SN47.14；Aśokavadāna×2（无巴利，压缩）；
学 SN48.23；净 SN48.1；须陀洹 SN48.2；阿罗汉 SN48.4；当知 SN48.8；
广说 SN48.10；略说 SN48.12；漏尽 SN48.20；沙门婆罗门 SN48.6。

信：有 SN 平行者据巴利／Sujato 厘义；631–633、635–636、640–641 无专经 → medium/low。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：不触碰 SA_611–630（并行批次）；断言 SA_610 不变（SA_630 尚未 gold）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts._sa640_gold import SA_640_LIT, SA_640_MOD  # noqa: E402
from scripts._sa641_gold import SA_641_LIT, SA_641_MOD  # noqa: E402
from translate.quality_gate import assess_gold  # noqa: E402
from translate.similarity import similarity_to_source  # noqa: E402
from translate.validate import validate_restyle  # noqa: E402

# ---------------------------------------------------------------------------
# 共用框式
# ---------------------------------------------------------------------------

OPEN_JET_LIT = "如是我闻：一时，佛住舍卫国祇树给孤独园。"
OPEN_JET_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

OPEN_PAT_LIT = "如是我闻：一时，佛住巴连弗邑鸡林精舍。"
OPEN_PAT_MOD = "我是这样听说的：有一次，佛住在巴连弗邑鸡林精舍。"

OPEN_RAJ_BAM_LIT = "如是我闻：一时，佛住王舍城迦兰陀竹园。"
OPEN_RAJ_BAM_MOD = "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。"

OPEN_MATH_LIT = "如是我闻：一时，佛住摩偷罗国跋陀罗河侧伞盖菴罗林中。"
OPEN_MATH_MOD = "我是这样听说的：有一次，佛住在摩偷罗国跋陀罗河侧伞盖菴罗林中。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

FOUR_SATI_LIT = "身、受、心、法四念处"
FOUR_SATI_MOD = "身、受、心、法四念处"

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

# --- SA 631 行（无专 SN）------------------------------------------------------
SUTTAS["SA_631"] = {
    "lit": [
        OPEN_PAT_LIT,
        "时尊者阿难、尊者跋陀罗亦住彼。跋陀罗问阿难："
        "「颇有法，修习多修习，能使未度彼岸者得度？」",
        "阿难答：「有，谓四念处——身、受、心、法。」",
        "二正士共论已，各还本处。",
    ],
    "mod": [
        OPEN_PAT_MOD,
        "那时尊者阿难、尊者跋陀罗也住在那里。跋陀罗问阿难："
        "「可有一法，多修习能使未度彼岸的人得度？」",
        "阿难答：「有，就是四念处——身、受、心、法。」",
        "两位正士共论完毕，各自回去。",
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：念处相应弟子问答；无 SN 专经，义同四念处度彼岸定型。"
    ),
}

# --- SA 632 行（无专 SN）------------------------------------------------------
SUTTAS["SA_632"] = {
    "lit": [
        OPEN_PAT_LIT,
        "时尊者阿难、尊者跋陀罗亦住彼。跋陀罗问阿难："
        "「颇有法，修习多修习，而得阿罗汉？」",
        "阿难答：「有，谓四念处——身、受、心、法。」",
        "二正士共论已，各还本处。",
    ],
    "mod": [
        OPEN_PAT_MOD,
        "那时尊者阿难、尊者跋陀罗也住在那里。跋陀罗问阿难："
        "「可有一法，多修习能得阿罗汉？」",
        "阿难答：「有，就是四念处——身、受、心、法。」",
        "两位正士共论完毕，各自回去。",
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：同上系，果位作阿罗汉；无 SN 专经。"
    ),
}

# --- SA 633 一切法（无专 SN）--------------------------------------------------
SUTTAS["SA_633"] = {
    "lit": [
        OPEN_PAT_LIT,
        "佛告比丘：「说一切法，正说者——谓四念处：身、受、心、法。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_PAT_MOD,
        "佛告比丘：「说一切法，正说者——就是四念处：身、受、心、法。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：「一切法＝四念处」名目经；无 SN 专经。"
    ),
}

# --- SA 634 贤圣（SN47.17）----------------------------------------------------
SUTTAS["SA_634"] = {
    "lit": [
        OPEN_PAT_LIT,
        "佛告比丘：「四念处修习多修习，是贤圣、能出离，趣苦边尽。"
        "何等为四？身、受、心、法念处——热诚、正知、正念，调伏世间贪忧。」",
        "「如出离，正尽苦、究竟苦边、得大果、大福利、甘露法、究竟甘露、甘露作证，亦如是说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_PAT_MOD,
        "佛告比丘：「四念处多修习，是贤圣、能出离，趣向苦的尽头。"
        "哪四种？身、受、心、法念处——热诚、正知、正念，调伏世间贪忧。」",
        "「如出离，正尽苦、究竟苦边、得大果、大福利、甘露法、究竟甘露、甘露作证，也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.17 Ariya（贤圣出离、尽苦）。"
        "汉本 peyyāla「如上广说」诸果名，压缩保留；地点从汉本巴连弗。"
    ),
}

# --- SA 635 光泽（无专 SN）----------------------------------------------------
SUTTAS["SA_635"] = {
    "lit": [
        OPEN_PAT_LIT,
        "佛告比丘：「四念处修习多修习：未净众生令净，已净众生令增光泽。"
        "何等为四？身、受、心、法念处。」",
        "「如净众生，未度令度、得阿罗汉、得辟支佛、得无上正觉，亦如上说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_PAT_MOD,
        "佛告比丘：「四念处多修习：未净的众生令得清净，已净的令增光泽。"
        "哪四种？身、受、心、法念处。」",
        "「如净众生，未度令度、得阿罗汉、得辟支佛、得无上正觉，也是这样说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：净／光泽及诸果 peyyāla；无 SN 专经，参 SN47 定型。"
    ),
}

# --- SA 636 比丘（无专 SN；出家道次第＋念处）---------------------------------
SUTTAS["SA_636"] = {
    "lit": [
        OPEN_PAT_LIT,
        "佛告比丘：「当说修四念处。如来出兴，说正法，善说满净梵行。"
        "族姓子闻法生信，见在家欲乐过患，舍家出家，持戒清净，守护根门，"
        "正知而行。」",
        "「住阿兰若、树下、空闲，正身正念。断五盖——贪、瞋、睡眠、掉悔、疑——"
        "内身身观念住，精勤正知正念，调伏世间贪忧；外身、内外身，受、心、法亦如是。"
        "是名比丘修四念处。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_PAT_MOD,
        "佛告比丘：「当说修四念处。如来出世，说正法，善说满净梵行。"
        "族姓子闻法生信，见在家欲乐的过患，舍家出家，持戒清净，守护根门，"
        "正知而行。」",
        "「住阿兰若、树下、空闲，正身正念。断五盖——贪、瞋、睡眠、掉悔、疑——"
        "内身身观念住，精勤正知正念，调伏世间贪忧；外身、内外身，受、心、法也是这样。"
        "这叫比丘修四念处。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=medium：出家道次第＋四念处，近 SN47 系广说而无专经平行；压缩汉本冗复。"
    ),
}

# --- SA 637 波罗提木叉（SN47.46）----------------------------------------------
SUTTAS["SA_637"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「当先净诸善法根本——于波罗提木叉善自防护，轨则具足，"
        "于微细罪见大怖畏，受持学处。依戒、住戒，修四念处：身、受、心、法——"
        "热诚、正知、正念，调伏世间贪忧。如是依戒修四念处。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「当先清净诸善法的根本——于波罗提木叉善自防护，轨则具足，"
        "于微细罪见大怖畏，受持学处。依戒、住戒，修四念处：身、受、心、法——"
        "热诚、正知、正念，调伏世间贪忧。这样依戒修四念处。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.46 Pātimokkha（戒为善法初、依戒修念处）。"
        "据 SN 校正：汉本「如上广说」压缩为戒＋四念处定型；地点舍卫从汉／SN。"
    ),
}

# --- SA 638 纯陀（SN47.13）----------------------------------------------------
SUTTAS["SA_638"] = {
    "lit": [
        OPEN_RAJ_BAM_LIT,
        "时尊者舍利弗住摩竭提那罗聚落，病重；纯陀沙弥瞻视。舍利弗因病般涅槃。"
        "纯陀持其余舍利及衣鉢，至王舍城，诣阿难所，白言：「我和上舍利弗已涅槃，"
        "舍利衣鉢在此。」",
        "阿难闻已，与纯陀俱诣佛所，白佛：「我今举体解体，心志迷闷，法不现前——"
        "纯陀言舍利弗已涅槃。」",
        "佛问：「阿难！舍利弗持汝戒身、定身、慧身、解脱身、解脱知见身而去耶？」"
        "「不也，世尊。」「我自证所说道品——四念处乃至八支圣道——彼持而去耶？」"
        "「不也，世尊。然舍利弗能示、能教、能照、能喜，为众说法；我为法故愁忧。」",
        "佛告阿难：「莫愁忧。生者、作者、有为败坏之法，欲令不坏，无有是处。"
        "我先已说：所爱念事皆是乖离。譬如大树，大枝先折；大宝山，大巖先崩。"
        "如来大众中，大声闻先般涅槃。我所在方，有舍利弗则不空；然彼亦有为法。」",
        "「阿难！当作自洲自依、法洲法依，莫异洲异依。云何？身受心法念处，"
        "精勤正知正念，调伏世间贪忧——是名自洲自依、法洲法依。修如是者，能尽众苦。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_RAJ_BAM_MOD,
        "那时尊者舍利弗住在摩竭提那罗聚落，病重；纯陀沙弥照料。舍利弗因病般涅槃。"
        "纯陀带着其余舍利和衣鉢，到王舍城，见阿难，说：「我和上舍利弗已经涅槃，"
        "舍利衣鉢在此。」",
        "阿难听了，和纯陀一起见佛，白佛：「我现在全身像散了，心志迷闷，法想不起来——"
        "纯陀说舍利弗已经涅槃。」",
        "佛问：「阿难！舍利弗把你的戒、定、慧、解脱、解脱知见带走了吗？」"
        "「没有，世尊。」「我自证所说的道品——四念处乃至八支圣道——他带走了吗？」"
        "「没有，世尊。可是舍利弗能开示、教导、照明、令喜，为众说法；我为法而愁忧。」",
        "佛告诉阿难：「不要愁忧。凡是生的、造作的、有为败坏之法，想要不坏，没有这回事。"
        "我先前已说：所爱念的事都是会乖离的。好比大树，大枝先折；大宝山，大巖先崩。"
        "如来大众中，大声闻先般涅槃。我所在的地方，有舍利弗就不空；可那也是有为法。」",
        "「阿难！应当作自洲自依、法洲法依，不要异洲异依。怎样？身受心法念处，"
        "精勤正知正念，调伏世间贪忧——这叫自洲自依、法洲法依。这样修习，能尽众苦。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.13 Cunda（舍利弗涅槃、自洲法洲）。"
        "据 SN 校正：五分法身／道品未失；大枝先折譬；四念处为自依。汉作王舍城，SN 作舍卫，地点从汉。"
    ),
}

# --- SA 639 布萨（SN47.14）----------------------------------------------------
SUTTAS["SA_639"] = {
    "lit": [
        OPEN_MATH_LIT,
        "时舍利弗、目揵连涅槃未久。月十五日布萨，世尊于大众前敷座而坐，"
        "观察众会已，告诸比丘：「我观大众，见已虚空——以二大声闻般涅槃故。"
        "我声闻中，唯此二人善能说法教诫。有钱财、法财：钱财从世人求，法财从彼二人求；"
        "如来已离二种财。」",
        "「汝等莫以彼涅槃故愁忧。生法、起法、作法，欲令不坏，无有是处。"
        "譬如大树大枝先折，宝山大巖先崩。如来不久亦当过去。"
        "当作自洲自依、法洲法依，莫异洲异依——谓身受心法念处，"
        "精勤正知正念，调伏世间贪忧；如是修者，能尽众苦。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_MATH_MOD,
        "那时舍利弗、目揵连涅槃未久。月十五日布萨，世尊在大众前敷座而坐，"
        "观察众会后，告诉比丘们：「我看大众，觉得空了——因为两位大声闻般涅槃。"
        "我的声闻中，只有这两人最能说法教诫。有钱财、法财：钱财向世人求，法财向他们求；"
        "如来已经远离这两种财。」",
        "「你们不要因为他们涅槃而愁忧。生法、起法、作法，想要不坏，没有这回事。"
        "好比大树大枝先折，宝山大巖先崩。如来不久也要过去。"
        "应当作自洲自依、法洲法依，不要异洲异依——就是身受心法念处，"
        "精勤正知正念，调伏世间贪忧；这样修习，能尽众苦。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN47.14 Ukkacelā（二大声闻涅槃后自洲）。"
        "据 SN 校正：众会空、大枝先折、自洲法洲＝四念处。汉作摩偷罗布萨，SN 作恒河岸 Ukkacelā，地点从汉。"
    ),
}

# --- SA 640 Aśokavadāna（法灭）------------------------------------------------
SUTTAS["SA_640"] = {
    "lit": SA_640_LIT,
    "mod": SA_640_MOD,
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=low：Aśokavadāna 法灭授记插入，无巴利平行；唯压缩汉本，不增传说细节。"
    ),
}

# --- SA 641 Aśokavadāna（半阿摩勒）--------------------------------------------
SUTTAS["SA_641"] = {
    "lit": SA_641_LIT,
    "mod": SA_641_MOD,
    "notes": (
        f"{NO_PARALLEL}"
        "confidence=low：半阿摩勒因缘，无巴利平行；唯压缩汉本，不增阿育传说细节。"
    ),
}

# --- SA 642 学（SN48.23）------------------------------------------------------
SUTTAS["SA_642"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有三根——未知当知根、已知根、具知根。」",
        "即说偈：「觉知学地时，随顺直道进，精进勤方便，善自护其心。"
        "自知生已尽，无碍道已知，以知得解脱，最后得具知。"
        "不动意解脱，一切有能尽，诸根悉具足，乐于根寂静，"
        "持于最后身，降伏众魔怨。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有三根——未知当知根、已知根、具知根。」",
        "就说偈：「觉知学地时，随顺直道进，精进勤方便，善自护其心。"
        "自知生已尽，无碍道已知，以知得解脱，最后得具知。"
        "不动意解脱，一切有能尽，诸根悉具足，乐于根寂静，"
        "持于最后身，降伏众魔怨。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.23（aññātaññassāmī／aññā／aññātāvī 三根）。"
        "据 SN 校正：「无知根」→「具知根」（已究竟知）；偈从汉本罗什化。"
    ),
}

# --- SA 643 净（SN48.1）-------------------------------------------------------
SUTTAS["SA_643"] = {
    "lit": [
        OPEN_JET_LIT,
        "世尊告诸比丘：「五根者，信、精进、念、定、慧——是名五根。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "世尊告诉比丘们：「所谓五根，就是信、精进、念、定、慧——这叫五根。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.1（五根名目）。"
    ),
}

# --- SA 644 须陀洹（SN48.2）---------------------------------------------------
SUTTAS["SA_644"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "圣弟子于此五根如实知味、知患、知离，是名须陀洹，不堕恶趣，"
        "决定正向正觉，七有天人往生，究竟苦边。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "圣弟子对这五根如实知味、知患、知离，叫做须陀洹，不堕恶趣，"
        "决定正向正觉，最多七次往来天人，究竟苦边。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.2。"
        "据 SN 校正：汉「三结断知」→知五根之味／患／离（assāda／ādīnava／nissaraṇa）；果位须陀洹从两边同。"
    ),
}

# --- SA 645 阿罗汉（SN48.4）---------------------------------------------------
SUTTAS["SA_645"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "圣弟子于此五根如实知味、知患、知离，以不取著而得解脱，是名阿罗汉——"
        "诸漏已尽，所作已作，弃重担，逮己利，尽有结，正智心善解脱。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "圣弟子对这五根如实知味、知患、知离，以不取著而得解脱，叫做阿罗汉——"
        "诸漏已尽，所作已作，放下重担，得自己的利益，尽诸有结，正智心善解脱。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.4。"
        "据 SN 校正：知味患离已，以不取著解脱；阿罗汉定型句从汉／SN 合。"
    ),
}

# --- SA 646 当知（SN48.8）-----------------------------------------------------
SUTTAS["SA_646"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "信根当知在四不坏净；精进根当知在四正勤；念根当知在四念处；"
        "定根当知在四禅；慧根当知在四圣谛。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "信根当知在四不坏净；精进根当知在四正勤；念根当知在四念处；"
        "定根当知在四禅；慧根当知在四圣谛。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.8 Daṭṭhabba（五根所见处）。"
        "汉「四不坏净」≈ SN 须陀洹支（sotāpattiyaṅga）；从汉术语，义从 SN。"
    ),
}

# --- SA 647 广说（SN48.10）----------------------------------------------------
SUTTAS["SA_647"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「何等信根？圣弟子于如来正觉起净信，坚固不可沮坏，是名信根。」",
        "「何等精进根？已生恶不善法令断，未生恶法令不生，未生善法令生，"
        "已生善法令住不忘、修习增广——生欲、精进、摄心、增上，是名精进根。」",
        "「何等念根？身受心法念处，精勤正知正念，调伏世间贪忧，是名念根。」",
        "「何等定根？离欲恶不善法，有觉有观，离生喜乐，初禅具足住，"
        "乃至第四禅具足住，是名定根。」",
        "「何等慧根？苦、集、灭、道四圣谛如实知，是名慧根。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「什么是信根？圣弟子对如来正觉起净信，坚固不可沮坏，这叫信根。」",
        "「什么是精进根？已生恶不善法令断，未生恶法令不生，未生善法令生，"
        "已生善法令住不忘、修习增广——生欲、精进、摄心、增上，这叫精进根。」",
        "「什么是念根？身受心法念处，精勤正知正念，调伏世间贪忧，这叫念根。」",
        "「什么是定根？离欲恶不善法，有觉有观，离生喜乐，初禅具足住，"
        "乃至第四禅具足住，这叫定根。」",
        "「什么是慧根？苦、集、灭、道四圣谛如实知，这叫慧根。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.10 Vibhaṅga（五根广分别）。"
        "信根从 SN 信如来正觉；精进＝四正勤；念＝四念处；定＝四禅；慧＝四谛／生灭慧。"
    ),
}

# --- SA 648 略说（SN48.12）----------------------------------------------------
SUTTAS["SA_648"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "于此五根圆满具足者，是阿罗汉，尽诸苦边；弱于此者，是阿那含；"
        "又弱者，是斯陀含；又弱者，是须陀洹；"
        "又弱者，是随法行；又弱者，是随信行。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "这五根圆满具足的，是阿罗汉，尽诸苦边；比这弱的，是阿那含；"
        "再弱的，是斯陀含；再弱的，是须陀洹；"
        "再弱的，是随法行；再弱的，是随信行。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.12 Saṁkhitta（五根强弱分果位）。"
        "据 SN 校正：汉本略说作须陀洹三结，改为 SN 六阶（阿罗汉→随信行）。"
    ),
}

# --- SA 649 漏尽（SN48.20）----------------------------------------------------
SUTTAS["SA_649"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "修习多修习此五根故，漏尽已，无漏心解脱、慧解脱，"
        "于现法自知作证：我生已尽，梵行已立，所作已作。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。"
        "因为修习多修习这五根，漏尽以后，无漏心解脱、慧解脱，"
        "在现法中自己证知：我生已尽，梵行已立，所作已作。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.20 Āsavakkhaya（修五根得漏尽二解脱）。"
        "据 SN 校正：汉阿罗汉定型 → SN 现法自证漏尽心解脱／慧解脱。"
    ),
}

# --- SA 650 沙门婆罗门（SN48.6）-----------------------------------------------
SUTTAS["SA_650"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「若沙门、婆罗门于此五根不如实知味、知患、知离，我不说彼是真沙门、真婆罗门；"
        "彼于沙门义、婆罗门义，现法未能自知作证。」",
        "「若如实知此五根之集、灭、味、患、离，我说彼是真沙门、真婆罗门；"
        "于沙门义、婆罗门义，现法自知作证。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告比丘：「有五根——信、精进、念、定、慧。」",
        "「若沙门、婆罗门对这五根不能如实知味、知患、知离，我不说他们是真沙门、真婆罗门；"
        "他们在现法中不能自己证知沙门义、婆罗门义。」",
        "「若如实知这五根的集、灭、味、患、离，我说他们是真沙门、真婆罗门；"
        "在现法中自己证知沙门义、婆罗门义。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN48.6。"
        "据 SN 校正：汉作佛自证五根集灭道成正觉 → SN 真／非真沙门婆罗门知五根味患离。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_631": "medium",
    "SA_632": "medium",
    "SA_633": "medium",
    "SA_634": "high",
    "SA_635": "medium",
    "SA_636": "medium",
    "SA_637": "high",
    "SA_638": "high",
    "SA_639": "high",
    "SA_640": "low",
    "SA_641": "low",
    "SA_642": "high",
    "SA_643": "high",
    "SA_644": "high",
    "SA_645": "high",
    "SA_646": "high",
    "SA_647": "high",
    "SA_648": "high",
    "SA_649": "high",
    "SA_650": "high",
}

RECONSTRUCTED: dict[str, str] = {}

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
    assert set(GOLD) == {f"SA_{i}" for i in range(631, 651)}, (
        "GOLD must cover SA_631–SA_650 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    # Parallel batch owns 611–630
    assert not any(f"SA_{i}" in GOLD for i in range(611, 631))

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

    # Boundary: SA_630 if gold, else SA_610
    _goldish = {"gold", "gold_reconstructed"}
    boundary_id = "SA_630"
    for rec in records:
        if rec["id"] == "SA_630" and rec.get("review_status") not in _goldish:
            boundary_id = "SA_610"
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

    # Snapshot 611–630 to assert untouched
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
        if rec["id"] in {f"SA_{i}" for i in range(611, 631)}
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
    (ROOT / "data" / "translated" / "validation_report_sa631-650.json").write_text(
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
    continuous_631_650 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(631, 651)
    )
    untouched_611_630 = all(f"SA_{i}" not in GOLD for i in range(611, 631))

    ban_terms = ["厌故不乐", "如来藏", "佛性", "常乐我净", "真心", "妄心", "本来面目", "即心即佛", "如如"]
    ban_hits = []
    for rid in GOLD:
        lit = by_merged[rid].get("kumarajiva_style_text") or ""
        mod = by_merged[rid].get("modern_psychology_text") or ""
        for t in ban_terms:
            if t in lit or t in mod:
                ban_hits.append((rid, t))

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_631–SA_650 only)")
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
    print(f"continuous_gold_SA_631–650={continuous_631_650}")
    print(f"SA_611–630_untouched={untouched_611_630}")
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
