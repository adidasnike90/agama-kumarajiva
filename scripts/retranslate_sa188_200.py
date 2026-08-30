#!/usr/bin/env python3
"""Retranslate SA 188–200（卷第九 六入處相應 首段，信>达>雅）→ merge into final_translated_data.json.

六入處相應始于此。本批十三经皆短中篇，以六内入处（眼耳鼻舌身意）为纲，
反复以「无常—厌—离贪—解脱」「不识不知不断不离欲—不堪任尽苦」等定型式说法。

信：本批与前批（断知相应 SA 172–187，SC 平行表全空）不同——SC 于十三经全列巴利平行，
且 `raw_aligned_data.json` 内已备巴利本文、Sujato 英译，及 Anālayo 之 SA 英译
（'On the Six Sense-spheres (1) — A Translation of Saṁyukta-āgama Discourses 188 to 229
(Fascicle 8)', DDJBS 18, 2016）。故本批以巴利平行厘定法义，凡改求那跋陀罗字面者于 notes 具志。
达：白话与罗什风逐段对照，段数严格相同（build 时 assert，merge 时记 paragraph_parallel）。
雅：文言栏与底本之三元组相似度须 < 0.55，否则记 needs_restyle（繁转简闸）。

Confidence 判准（逐经列于 CONFIDENCE）：
- high：SC 所列 `full` 平行之巴利本文／英译逐句覆盖本经正文（SA 188–191、194、196–199）。
- medium：SC 所列平行与本经内容实不相符，须另行认定或无单一经可覆盖（SA 192、193、195）。
- low：底本正文核心仅作交叉指示，须依所指之经回填者（SA 200，并标 gold_reconstructed）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from translate.similarity import similarity_to_source  # noqa: E402
from translate.validate import validate_restyle  # noqa: E402

# ---------------------------------------------------------------------------
# 共用框式
# ---------------------------------------------------------------------------

OPEN_LIT = "如是我闻：一时佛在舍卫国祇树给孤独园。"
OPEN_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

CLOSE_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_RAHULA_LIT = "佛说此经已，尊者罗睺罗闻佛所说，欢喜奉行。"
CLOSE_RAHULA_MOD = "佛说完这部经，罗睺罗尊者听佛所说，欢喜奉行。"

AWAKEN_LIT = "「我生已尽，梵行已立，所作已作，自知不受后有。」"
AWAKEN_MOD = "「我的生已尽，梵行已立，该做的已做，自知不再受后有。」"

# 六入处之省略：底本每经皆「耳、鼻、舌、身、意亦复如是」，罗什风正宜存此简式
SIX_LIT = "耳、鼻、舌、身、意亦复如是。"
SIX_MOD = "耳、鼻、舌、身、意也是一样。"

# notes 共用前言：交代所依
PROV = (
    "本经 SC 平行表所列巴利平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译，"
    "与 Anālayo 之 SA 英译（DDJBS 18, 2016, Fascicle 8）并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)

# 「一切无常」之六六式正文（SA 195／196／200 共用之纲要；SA 197 易「无常」为「烧然」）
def all_impermanent(word_lit: str, word_mod: str) -> tuple[str, str]:
    lit = (
        f"一切{word_lit}。云何一切{word_lit}？谓眼{word_lit}；色、眼识、眼触，"
        f"及眼触因缘所生受——若苦、若乐、不苦不乐——彼亦{word_lit}。"
        f"耳、鼻、舌、身、意，声、香、味、触、法，乃至意触因缘所生受，亦复如是。"
    )
    mod = (
        f"一切都是{word_mod}的。哪些是「一切」呢？就是说：眼是{word_mod}的；"
        f"色（所见之境）、眼识、眼触，以及依眼触为缘而生起的感受——无论是苦、是乐、"
        f"还是不苦不乐——也都是{word_mod}的。"
        f"耳、鼻、舌、身、意，以及声、香、味、触、法，乃至依意触为缘而生起的感受，"
        f"也都是一样。"
    )
    return lit, mod


# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}


# --- SA 188 离喜贪（SN 35.156 Ajjhattanandikkhaya）---------------------------
SUTTAS["SA_188"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：眼实无常。观眼无常，是名正见；正见故生厌，生厌故喜尽，"
        "喜尽则贪尽，贪尽则喜尽。喜、贪俱尽，我说是心善解脱。" + SIX_LIT,
        "比丘！心善解脱者，能自记说：" + AWAKEN_LIT,
        CLOSE_LIT,
        "（省文）如「无常」，如是「苦」、「空」、「非我」，亦如上说，各成一经。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：眼本来就是无常的。观见眼是无常，这就叫正见；"
        "有了正见便生起厌离，生起厌离便使爱乐止息，爱乐止息则贪欲止息，"
        "贪欲止息则爱乐止息。爱乐与贪欲都止息了，我说这样的心是真正解脱的。" + SIX_MOD,
        "比丘们！心真正解脱的人，能够自己宣说：" + AWAKEN_MOD,
        CLOSE_MOD,
        "（以下是原典的省文指示）把「无常」依次换成「苦」、「空」、「非我」，"
        "各按同一格式成一部经。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high。SC 标 SN35.156 为 resembling，然其所标之犹疑在于 SN35.153–158 一系"
        "诸经语面几同、难定与本经相当者为何经，非疑其法义；所据之句巴利逐字可对，故不因此降级。"
        "信-校正二事："
        "（一）底本「当正观察眼无常」为劝令式，巴利作直陈 `aniccaṁyeva, bhikkhave, cakkhuṁ`"
        "（眼实是无常），继以 `aniccanti passati, sāssa hoti sammādiṭṭhi`（见其无常，即是正见）；"
        "巴利之意在「所见与实相相符故名正见」，非「应当去观」，今改作「眼实无常，观眼无常，是名正见」。"
        "（二）底本「离喜、离贪」平列二事，巴利作互摄式 `nandikkhayā rāgakkhayo; rāgakkhayā "
        "nandikkhayo. nandirāgakkhayā cittaṁ suvimuttaṁ`（喜尽则贪尽，贪尽则喜尽；喜贪俱尽，"
        "说心善解脱），今复其互摄之势。"
        "「喜」即 nandī（爱乐、耽喜），非世俗之欢喜；「心正解脱」即 suvimutta（善解脱），"
        "今作「心善解脱」以合巴利之 su-。"
        "末段「如无常，如是苦、空、非我」为省文指示，如实存为末段，不伪作各别全经。"
    ),
}


# --- SA 189 正思惟（SN 35.158 Ajjhattaaniccanandikkhaya）---------------------
SUTTAS["SA_189"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：于眼当如理作意，如实观其无常。何以故？"
        "于眼如理作意、观其无常故，则于眼生厌；厌故欲贪断，欲贪断故，我说是心善解脱。"
        + SIX_LIT,
        "如是，比丘！心善解脱者，能自记说：" + AWAKEN_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：对于眼，应当如理用心，如实观见它的无常。为什么呢？"
        "因为对眼如理用心、观见它的无常，便对眼生起厌离；厌离便断除了欲贪，"
        "欲贪断除了，我说这样的心是真正解脱的。" + SIX_MOD,
        "就是这样，比丘们！心真正解脱的人，能够自己宣说：" + AWAKEN_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high（SC 标 SN35.158 为 resembling，其故同 SA_188：SN35.153–158 一系语面几同，"
        "非疑法义；所据之句巴利逐字可对）。"
        "信-校正二事："
        "（一）底本「正思惟」易与八正道之「正志」（sammāsaṅkappa）相混，巴利实作 "
        "`cakkhuṁ yoniso manasi karotha`——yoniso manasikāra，谓「如理作意、循其根源而用心」"
        "（Sujato: rationally apply the mind；Anālayo: give right attention），"
        "与「正志」之思惟内容无关，今改作「如理作意」而于此志之。"
        "（二）底本自「正思惟观察无常」直跳「欲贪断」，脱去中间一支；巴利作 "
        "`…samanupassanto cakkhusmimpi nibbindati. nandikkhayā rāgakkhayo…`"
        "（观之则于眼生厌，厌故喜尽贪尽），今据补「则于眼生厌」一支，使因果链完足。"
        "「欲贪」即 nandirāga（喜贪）之意译，存底本语面。"
    ),
}


# --- SA 190 眼（一）（SN 35.26 Paṭhamaaparijānana）--------------------------
_KNOW_FOUR_LIT = "不证知、不遍知、不离贪、不断舍"
_KNOW_FOUR_POS_LIT = "证知、遍知、离贪、断舍"
_KNOW_FOUR_MOD = "不亲证、不遍知、不离贪、不断舍"
_KNOW_FOUR_POS_MOD = "亲证、遍知、离贪、断舍"

SUTTAS["SA_190"] = {
    "lit": [
        OPEN_LIT,
        f"尔时世尊告诸比丘：于眼若{_KNOW_FOUR_LIT}者，不堪任正尽诸苦。" + SIX_LIT,
        f"诸比丘！于眼若{_KNOW_FOUR_POS_LIT}者，则堪任正尽诸苦；"
        f"于耳、鼻、舌、身、意{_KNOW_FOUR_POS_LIT}者，亦堪任正尽诸苦。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        f"那时，世尊告诉比丘们：对于眼，若是{_KNOW_FOUR_MOD}，便不堪能真正灭尽众苦。"
        + SIX_MOD,
        f"比丘们！对于眼，若能{_KNOW_FOUR_POS_MOD}，便堪能真正灭尽众苦；"
        f"对耳、鼻、舌、身、意能{_KNOW_FOUR_POS_MOD}的人，也堪能真正灭尽众苦。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.26 之巴利定型语逐支可对，正可校底本四支之术语。"
        "信-校正：底本「不识、不知、不断、不离欲」四支语面含混（「识」「知」同为知义，"
        "「离欲」又似「断」之复），巴利作 `anabhijānaṁ aparijānaṁ avirājayaṁ appajahaṁ "
        "abhabbo dukkhakkhayāya`——四支各有所当："
        "abhijānāti＝证知（现前而知，Sujato: directly know）、parijānāti＝遍知（周遍而知，"
        "completely understand）、virājeti＝离贪（离染，have dispassion）、pajahati＝断舍（舍弃，"
        "give up）；今依巴利正作「证知、遍知、离贪、断舍」，并从巴利之次第（离贪先于断舍），"
        "底本作「断」先「离欲」后，语序之异不涉法义。"
        "「不堪任正尽苦」即 `abhabbo dukkhakkhayāya`（不堪能尽苦）。"
        "又巴利于「一切」下并列眼、色、眼识、眼触及触缘生受五支，汉本此经唯举六内入处，"
        "为汉本此系之体裁（次经 SA_191 同），今存汉本之量，不据巴利增广。"
    ),
}


# --- SA 191 眼（二）（SN 35.27 Dutiyaaparijānana）---------------------------
_BEYOND_LIT = "超越生、老、病、死之苦"
_BEYOND_MOD = "超越生、老、病、死之苦"

SUTTAS["SA_191"] = {
    "lit": [
        OPEN_LIT,
        f"尔时世尊告诸比丘：于眼若{_KNOW_FOUR_LIT}者，不堪任{_BEYOND_LIT}；"
        f"于耳、鼻、舌、身、意{_KNOW_FOUR_LIT}者，亦不堪任{_BEYOND_LIT}。",
        f"诸比丘！于眼若{_KNOW_FOUR_POS_LIT}者，则堪任{_BEYOND_LIT}；"
        f"于耳、鼻、舌、身、意{_KNOW_FOUR_POS_LIT}者，亦堪任{_BEYOND_LIT}。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        f"那时，世尊告诉比丘们：对于眼，若是{_KNOW_FOUR_MOD}，便不堪能{_BEYOND_MOD}；"
        f"对耳、鼻、舌、身、意{_KNOW_FOUR_MOD}的人，也不堪能{_BEYOND_MOD}。",
        f"比丘们！对于眼，若能{_KNOW_FOUR_POS_MOD}，便堪能{_BEYOND_MOD}；"
        f"对耳、鼻、舌、身、意能{_KNOW_FOUR_POS_MOD}的人，也堪能{_BEYOND_MOD}。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：四支术语之校正同前经（SA_190），巴利定型语逐支可对。"
        "本经与前经唯异于所越之境：前经作「正尽苦」（dukkhakkhaya），本经作「越生、老、病、死苦」。"
        "巴利 SN35.26／35.27 二经皆作 dukkhakkhaya，所异者在所列之支（35.27 增眼触缘生受一支），"
        "故汉本此对之「正尽苦／越生老病死苦」之别不见于巴利，当为汉本一系自有之衍分；"
        "「越生老病死苦」为早期定型语（`jātijarāmaraṇaṁ samatikkamati` 一类），非增造，故仍作 high。"
    ),
}


# --- SA 192 不离欲（一）（SC 列 SN 35.21，实不相当）------------------------
_DESIRE_PROV = (
    "SC 于本经列 SN35.21／35.22（Dukkhuppāda，苦之生起）为 resembling 平行，"
    "然彼二经所说为「眼之生、住、现起即苦之生、病之住、老死之现起」，"
    "与本经「于眼不离欲、心不解脱则不堪任尽苦」之式实不相当，无单一巴利经可覆盖本经正文，"
    "故 confidence 降为 medium。"
)

SUTTAS["SA_192"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：于眼不离欲，心不解脱者，不堪任正尽诸苦；"
        "于耳、鼻、舌、身、意不离欲，心不解脱者，亦不堪任正尽诸苦。",
        "诸比丘！于眼离欲，心得解脱者，则堪任正尽诸苦；"
        "于耳、鼻、舌、身、意离欲，心得解脱者，亦堪任正尽诸苦。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：对于眼不能离欲，心便不得解脱，也就不堪能真正灭尽众苦；"
        "对耳、鼻、舌、身、意不能离欲，心不得解脱的人，也不堪能真正灭尽众苦。",
        "比丘们！对于眼能够离欲，心便得解脱，也就堪能真正灭尽众苦；"
        "对耳、鼻、舌、身、意能够离欲，心得解脱的人，也堪能真正灭尽众苦。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}{_DESIRE_PROV}"
        "校勘：底本正说作「若于眼、色离欲」而反说唯作「于眼不离欲」，前后不齐；"
        "「色」一字当为涉次经（SA_193 通篇作「眼、色」）而衍，Anālayo 亦仅读作 the eye，今删之，"
        "使本经专说六内入处，次经乃兼说内外，二经之别乃明。"
        "「不堪任正尽苦」即「不堪能真正灭尽众苦」（`abhabbo dukkhakkhayāya`），同 SA_190。"
    ),
}


# --- SA 193 不离欲（二）------------------------------------------------------
SUTTAS["SA_193"] = {
    "lit": [
        OPEN_LIT,
        f"尔时世尊告诸比丘：于眼、于色不离欲，心不解脱者，不堪任{_BEYOND_LIT}；"
        f"于耳、鼻、舌、身、意不离欲，心不解脱者，亦不堪任{_BEYOND_LIT}。",
        f"诸比丘！于眼、于色离欲，心得解脱者，则堪任{_BEYOND_LIT}；"
        f"于耳、鼻、舌、身、意离欲，心得解脱者，亦堪任{_BEYOND_LIT}。",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        f"那时，世尊告诉比丘们：对于眼、对于色不能离欲，心便不得解脱，也就不堪能{_BEYOND_MOD}；"
        f"对耳、鼻、舌、身、意不能离欲，心不得解脱的人，也不堪能{_BEYOND_MOD}。",
        f"比丘们！对于眼、对于色能够离欲，心便得解脱，也就堪能{_BEYOND_MOD}；"
        f"对耳、鼻、舌、身、意能够离欲，心得解脱的人，也堪能{_BEYOND_MOD}。",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}{_DESIRE_PROV}"
        "本经与前经之别有二：一在所越之境（前经「正尽苦」，本经「越生老病死苦」），"
        "二在所对之境（本经兼举内入处与外入处之「色」，前经唯举内入处）；"
        "底本于后举六根处仍仅列「耳、鼻、舌、身、意」而不列声、香、味、触、法，"
        "为省文之常例，今存其略而不增字。"
    ),
}


# --- SA 194 生喜（SN 35.19／35.20 Abhinanda）--------------------------------
SUTTAS["SA_194"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：于眼生喜，则于苦生喜；喜于苦者，我说于苦不得解脱。"
        + SIX_LIT,
        "诸比丘，于眼不生喜，则不喜于苦；不喜于苦者，我说于苦得解脱。" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：对眼生起爱乐耽著，就是对苦生起爱乐；"
        "对苦生起爱乐的人，我说他不能从苦中解脱。" + SIX_MOD,
        "比丘们，对眼不生爱乐耽著，就不对苦生爱乐；"
        "不对苦生爱乐的人，我说他能从苦中解脱。" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.19／35.20（Abhinanda）为 `full`、非 resembling 之平行，"
        "巴利之式与本经逐句相符（Sujato: if you take pleasure in the eye, you take pleasure in "
        "suffering… you're not free from suffering, I say）。"
        "「生喜」即 abhinandati——耽著爱乐而非泛言欢喜；正与经末「欢喜奉行」之「欢喜」"
        "（`attamanā`，心悦）异义，故文言栏存「生喜」之简，而现代栏作「生起爱乐耽著」以别之。"
        "雅：改「若于眼生喜者……不解脫於苦」之求那体为「于眼生喜，则于苦生喜」四字节奏。"
    ),
}


# --- SA 195 无常（一）（SC 列 SN 35.1–12，实相当者为 SN 35.43–51 一系）------
_195_LIT, _195_MOD = all_impermanent("无常", "无常")
SUTTAS["SA_195"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：" + _195_LIT,
        "多闻圣弟子如是观者，于眼生厌，于色、眼识、眼触及眼触因缘所生受生厌；"
        "于耳、鼻、舌、身、意，声、香、味、触、法，乃至意触因缘所生受，亦皆生厌。"
        "厌故离贪，离贪故解脱，解脱故自知解脱：" + AWAKEN_LIT,
        CLOSE_LIT,
        "（省文）如「无常」经，如是「苦」、「空」、「无我」，亦如上说，各成一经。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：" + _195_MOD,
        "多闻圣弟子这样观察的人，对眼生起厌离，对色、眼识、眼触以及依眼触为缘所生的感受，"
        "也生起厌离；对耳、鼻、舌、身、意，声、香、味、触、法，乃至依意触为缘所生的感受，"
        "同样都生起厌离。厌离便离贪，离贪便得解脱，解脱便自知已解脱：" + AWAKEN_MOD,
        CLOSE_MOD,
        "（以下是原典的省文指示）如同这部「无常」经，把「无常」换成「苦」、「空」、「无我」，"
        "各按同一格式成一部经。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium：SC 于本经所列 SN35.1–12 为内外六处之无常／苦／非我三组，"
        "其正文唯举六处而无「色、识、触、触缘生受」之六六列，与本经「一切无常」之量不合；"
        "本经实与 SN35.43–51（Aniccādi，`sabbaṁ aniccaṁ` 下开眼、色、眼识、眼触、触缘生受五支）"
        "同式，而彼系 SC 系于次经（SA_196）名下。因所据之平行係本篇另行认定，非 SC 所列，"
        "依项目规约降为 medium。"
        "信-校正：底本「厌故不乐，不乐故解脱」之「不乐」非「不喜欢」，乃 virāga（离贪）；"
        "巴利定型语作 `nibbidā virāgo, virāgā vimutti`（厌→离贪→解脱），"
        "今作「厌故离贪，离贪故解脱」，沿用本项目 SA_124／127 之例。"
        "「解脱知见」即 `vimuttasmiṁ vimuttamiti ñāṇaṁ`（于解脱知其解脱），今作「解脱故自知解脱」。"
        "「苦觉、乐觉、不苦不乐觉」之「觉」即 vedayita（所受），非「觉悟」，今作「若苦、若乐、"
        "不苦不乐」以免歧读。"
    ),
}


# --- SA 196 无常（二）（SN 35.33–42／43–51／52）------------------------------
_196_LIT, _196_MOD = all_impermanent("无常", "无常")

_196_SYNONYMS_LIT = (
    "（省文）如说「一切无常」，如是「一切苦」、「一切空」、「一切非我」，"
    "「一切虚业法」、「一切破坏法」，"
    "「一切生法」、「一切老法」、「一切病法」、「一切死法」、「一切愁忧法」、「一切烦恼法」，"
    "「一切集法」、「一切灭法」，"
    "「一切知法」、「一切识法」、「一切断法」、「一切觉法」、「一切作证」，"
    "「一切魔」、「一切魔势」、「一切魔器」，「一切然」、「一切炽然」、「一切烧」，"
    "皆如上二经广说。"
)
_196_SYNONYMS_MOD = (
    "（以下是原典的省文指示）如同上面说「一切无常」，把「无常」依次换成以下诸门，"
    "都照前二经（SA_195、SA_196）详说而各成一经；今按义类分列："
    "一、三法印之余——一切苦、一切空、一切非我；"
    "二、坏灭之名——一切虚业法、一切破坏法（palokadhamma，会溃散之法）；"
    "三、生老病死忧恼——一切生法、老法、病法、死法、愁忧法、烦恼法"
    "（jāti／jarā／byādhi／maraṇa／soka／saṅkilesika-dhamma，即巴利 SN35.33–42 之六门）；"
    "四、缘起生灭——一切集法、一切灭法（samudaya／nirodha-dhamma）；"
    "五、所应作——一切知法（应证知）、一切识法（应遍知）、一切断法（应断舍）、"
    "一切觉法、一切作证（应现证）；"
    "六、魔所摄——一切魔、一切魔势、一切魔器；"
    "七、烧然——一切然、一切炽然、一切烧（即次经 SA_197「一切烧然」之义）。"
)

SUTTAS["SA_196"] = {
    "lit": [
        OPEN_LIT,
        "尔时世尊告诸比丘：" + _196_LIT,
        "多闻圣弟子如是观者，于眼解脱，于色、眼识、眼触及眼触因缘所生受解脱；"
        "于耳、鼻、舌、身、意，法、意识、意触，乃至意触因缘所生受，亦皆解脱。"
        "我说彼解脱于生、老、病、死、忧、悲、恼、苦。",
        CLOSE_LIT,
        _196_SYNONYMS_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：" + _196_MOD,
        "多闻圣弟子这样观察的人，从眼得解脱，从色、眼识、眼触以及依眼触为缘所生的感受得解脱；"
        "从耳、鼻、舌、身、意，法、意识、意触，乃至依意触为缘所生的感受，同样都得解脱。"
        "我说这样的人已解脱于生、老、病、死、忧、悲、恼、苦。",
        CLOSE_MOD,
        _196_SYNONYMS_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 所列 SN35.43–51（`sabbaṁ aniccaṁ` 下开眼、色、眼识、眼触、"
        "触缘生受五支）与本经正文逐支相符，SN35.33–42 及 SN35.52 复与本经末段之诸门相应，"
        "resembling 之标仅因彼系为一组同式经、难定一一之对，非疑法义。"
        "信-校正：底本末句「我说彼生、老、病、死、忧、悲、恼、苦」语义倒错，"
        "文脉所须为「解脱」而非「有」；Anālayo 读作 I say that he is liberated from birth, "
        "old age, disease, death…，当是汉本脱「解脱于」三字，今补之。"
        "本经与前经（SA_195）之别：前经作「生厌→离贪→解脱→自知」之全链，本经省中间二支而直言"
        "「解脱」，并以「解脱于生老病死忧悲恼苦」结，故末段自称「如上二经广说」。"
        "末段二十四门，文言栏存底本语面全列，现代栏按义类分组并出可考之巴利名；"
        "「虚业法」一名义未详（Anālayo: of the nature of void activity），巴利未得确对，故不强解。"
    ),
}


# --- SA 197 烧然（SN 35.28 Āditta；三示现参 SF 270 Catuṣpariṣat）------------
_197_FIRE_LIT, _197_FIRE_MOD = all_impermanent("烧然", "燃烧")

SUTTAS["SA_197"] = {
    "lit": [
        "如是我闻：一时佛在伽耶山顶支提，与千比丘俱，皆旧结发梵志。",
        "尔时世尊为千比丘作三种示现教化。云何为三？谓神通示现、记心示现、教诫示现。",
        "神通示现者：世尊随其所应，入禅定正受，凌虚东上，现四威仪——行、住、坐、卧；"
        "复入火三昧，放种种光，青、黄、赤、白、红、颇梨色；水火俱现，"
        "或身下出火而身上出水，或身上出火而身下出水，周旋四方，亦复如是。"
        "作是种种神变已，还坐众中。是名神通示现。",
        "记心示现者：如彼之心、如彼之意、如彼之识，彼应作是念、不应作是念，"
        "彼应作是舍、彼应如是身证而住，佛悉知之。是名记心示现。",
        "教诫示现者，如世尊说：诸比丘！" + _197_FIRE_LIT,
        "以何烧然？贪火烧然，恚火烧然，痴火烧然；生、老、病、死、忧、悲、恼、苦火烧然。",
        "尔时千比丘闻佛所说，不取着故，心解脱于诸漏。" + CLOSE_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在伽耶山顶的支提，与一千位比丘同在，"
        "他们都是从前结发修行的婆罗门。",
        "那时，世尊为这一千位比丘作三种示导而教化他们。哪三种呢？"
        "就是神通示导、记心示导、教诫示导。",
        "神通示导是这样：世尊随所应度而入禅定正受，凌空升往东方，现四种威仪——"
        "行、住、坐、卧；又入火三昧，放出种种光焰，青、黄、赤、白、红、水晶（颇梨）色；"
        "水与火同时显现，或者下半身出火而上半身出水，或者上半身出火而下半身出水，"
        "四方周旋，也都如此。作了这些神变之后，便回到众中坐下。这叫神通示导。",
        "记心示导是这样：对方的心如何、意如何、识如何，他应当起这样的念、不应当起那样的念，"
        "他应当这样舍离、应当这样亲身证得而安住——佛都如实知见。这叫记心示导。",
        "教诫示导是这样，如世尊所说：比丘们！" + _197_FIRE_MOD,
        "被什么烧着呢？被贪之火烧着，被瞋之火烧着，被痴之火烧着；"
        "并被生、老、病、死、忧、悲、恼、苦之火烧着。",
        "那时，一千位比丘听佛所说，由于不再执取，心便从诸漏中解脱。" + CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：本经教诫段与 SN35.28（Ādittasutta）逐句相符——彼经亦设于伽耶山顶"
        "（Gayāsīsa）、千比丘众，说「一切烧然」而以贪火、瞋火、痴火及生老病死忧悲恼苦火为所烧"
        "（`rāgagginā dosagginā mohagginā ādittaṁ, jātiyā jarāya maraṇena…`）；"
        "「三种示现」一段不见于巴利此经，而与 SC 所列梵本 SF 270（Catuṣpariṣat-sūtra）相应，"
        "亦即三神变之定型说（`tīṇi pāṭihāriyāni`）。"
        "地名：「迦阇尸利沙支提」即 Gayāsīsa cetiya（伽耶山顶之支提），"
        "「旧萦发婆罗门」即 purāṇa-jaṭila（旧结发外道，优楼频螺迦叶三兄弟之众千人）。"
        "信-校正二事："
        "（一）「他心示现」易读作「他心通」，巴利作 ādesanā-pāṭihāriya（记说示导）——"
        "谓如实记说他人之心念而为之指授，非徒知其心，今作「记心示现」并于现代栏出其义。"
        "（二）底本「不起诸漏，心得解脱」语面费解，Anālayo 读作 by not clinging the minds… "
        "were liberated from the influxes，即巴利 `anupādāya cittāni vimucciṁsu`（不取着故，"
        "心得解脱）；「不起」当为「不取」之讹，今正作「不取着故，心解脱于诸漏」。"
        "「教诫示现」即 anusāsanī-pāṭihāriya，三示现中唯此为佛所重，故经名从其所教之「烧然」。"
    ),
}


# --- SA 198 罗睺罗（一）（SN 18.21 Anusaya／SN 22.91）-----------------------
_SELF_TRIAD_LIT = "我执、我所执、我慢随眠"
_SELF_TRIAD_MOD = "我执、我所执，以及潜伏的我慢随眠"

_NOT_SELF_LIT = (
    "若过去、若未来、若现在，若内、若外，若粗、若细，若好、若丑，若远、若近，"
    "彼一切非我、非异我、不相在，如实知之。"
)
_NOT_SELF_MOD = (
    "无论过去、未来、现在，内、外，粗、细，好、丑，远、近——"
    "这一切都非我、非异我、不相在，应当如实了知。"
)

_198_TAIL_LIT = (
    "（省文）如内入处，如是外入处——色、声、香、味、触、法；"
    "眼识乃至意识；眼触乃至意触；眼触生受乃至意触生受；眼触生想乃至意触生想；"
    "眼触生思乃至意触生思；眼触生爱乃至意触生爱——一一亦如上说，各成一经。"
)
_198_TAIL_MOD = (
    "（以下是原典的省文指示）如同上面就六内入处（眼耳鼻舌身意）所说，"
    "同样就六外入处——色、声、香、味、触、法；"
    "眼识乃至意识；眼触乃至意触；由眼触所生之受乃至由意触所生之受；"
    "由眼触所生之想乃至由意触所生之想；由眼触所生之思（cetanā，意志之动）乃至由意触所生之思；"
    "由眼触所生之爱（taṇhā）乃至由意触所生之爱——每一门也各按同一格式成一部经。"
)

SUTTAS["SA_198"] = {
    "lit": [
        "如是我闻：一时佛在王舍城耆阇崛山。",
        "尔时尊者罗睺罗往诣佛所，稽首佛足，退住一面，白佛言：世尊！云何知、云何见，"
        f"令此有识之身及外一切相，{_SELF_TRIAD_LIT}系着不生？",
        "尔时世尊告罗睺罗：善哉，罗睺罗！汝能问如来甚深之义。",
        "佛告罗睺罗：诸所有眼，" + _NOT_SELF_LIT + SIX_LIT,
        f"罗睺罗！如是知、如是见者，于此有识之身及外一切相，{_SELF_TRIAD_LIT}系着不生。"
        f"罗睺罗！{_SELF_TRIAD_LIT}系着不生者，是名断爱、断浊见，以正现观故，究竟苦边。",
        CLOSE_RAHULA_LIT,
        _198_TAIL_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在王舍城耆阇崛山（灵鹫山）。",
        "那时，罗睺罗尊者来到佛前，以头面礼佛足，退到一旁站立，对佛说：世尊！"
        f"该怎样知、怎样见，才能使这有识之身以及身外一切相状，都不再生起{_SELF_TRIAD_MOD}"
        "的缠缚执著？",
        "那时，世尊告诉罗睺罗：好啊，罗睺罗！你能向如来问这样甚深的义理。",
        "佛告诉罗睺罗：凡所有眼，" + _NOT_SELF_MOD + SIX_MOD,
        f"罗睺罗！这样知、这样见的人，对这有识之身以及身外一切相状，"
        f"便不再生起{_SELF_TRIAD_MOD}的缠缚执著。罗睺罗！这些不再生起的人，"
        "就叫做断除了贪爱、断除了浑浊之见，由于正确的现观，终尽苦的边际。",
        CLOSE_RAHULA_MOD,
        _198_TAIL_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 所列 SN18.21（Anusaya）／SN22.91 之巴利本文备于记录中，"
        "所须之定型语逐字可对；彼二经以五阴为所观，本经以六入处为所观，"
        "乃罗睺罗相应与六入处相应之各自编次（汉本 SA 23／24 即彼五阴之本），非法义之异。"
        "又本经末段之衍展列（内入处→外入处→识→触→触生受→想→思→爱）与巴利罗睺罗相应"
        "第二品之摄颂 `cakkhu rūpañca viññāṇaṁ, samphasso vedanāya ca; saññā sañcetanā "
        "taṇhā` 次第全同，足证此列非汉本自造，故不因平行标 `full/五阴` 而降级。"
        "信-校正三事："
        "（一）底本「我内识身」易读作「内在之识身」，巴利作 `imasmiñca saviññāṇake kāye`"
        "（此有识之身，即此具识之身躯），今作「此有识之身」。"
        "（二）底本「我、我所、我慢使系着」三名，巴利作 `ahaṅkāra-mamaṅkāra-mānānusayā`——"
        "ahaṅkāra＝我作（我执之造作）、mamaṅkāra＝我所作、mānānusaya＝我慢随眠；"
        "「使」为 anusaya（随眠）非「驱役」，沿用本项目 SA_103／116／142 之例，"
        "今作「我执、我所执、我慢随眠」。"
        "（三）「正无间等」之「无间等」＝ abhisamaya（现观），本项目 SA_105／109／123 已定此译，"
        "今作「以正现观故」；「究竟苦边」即 `dukkhassa antakiriyā`（作苦之边际）。"
        "「断爱浊见」句读有二读，Anālayo 读作 craving and murky views（爱与浊见），今从之。"
        "「非我、非异我、不相在」为阴相应／入处相应之通语（`netaṁ mama, nesohamasmi, "
        "na meso attā` 一类否定式），依本项目 SA_186 之例存底本语面。"
    ),
}


# --- SA 199 罗睺罗（二）（SN 18.22 Apagata／SN 22.92）-----------------------
SUTTAS["SA_199"] = {
    "lit": [
        "如是我闻：一时佛在王舍城迦兰陀竹园。",
        "尔时世尊告罗睺罗：云何知、云何见，于此有识之身及外一切相，"
        f"无有{_SELF_TRIAD_LIT}系着？",
        "罗睺罗白佛言：世尊是法根、法眼、法依。善哉世尊！愿为诸比丘广说此义；"
        "诸比丘闻已，当受奉行。",
        "佛告罗睺罗：善哉！谛听，当为汝说。诸所有眼，" + _NOT_SELF_LIT + SIX_LIT,
        f"罗睺罗！如是知、如是见者，于此有识之身及外一切相，{_SELF_TRIAD_LIT}系着不生。"
        "罗睺罗！如是比丘超越诸慢计，离于诸相，寂静解脱。"
        "罗睺罗！如是比丘断诸爱欲，转去诸结，究竟苦边。",
        CLOSE_RAHULA_LIT,
        "（省文）如内入处，如是外入处，乃至意触因缘所生受，亦如上广说。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在王舍城迦兰陀竹园。",
        "那时，世尊告诉罗睺罗：该怎样知、怎样见，才能使这有识之身以及身外一切相状，"
        f"都没有{_SELF_TRIAD_MOD}的缠缚执著？",
        "罗睺罗对佛说：世尊是法的根本、法的眼目、法的依止。太好了，世尊！"
        "愿世尊为比丘们详说这个义理；比丘们听了，当会领受奉行。",
        "佛告诉罗睺罗：好啊！仔细听，我为你说。凡所有眼，" + _NOT_SELF_MOD + SIX_MOD,
        "罗睺罗！这样知、这样见的人，对这有识之身以及身外一切相状，便不再生起"
        f"{_SELF_TRIAD_MOD}的缠缚执著。罗睺罗！这样的比丘超越了种种慢的计量，"
        "远离诸相，寂静而解脱。罗睺罗！这样的比丘断除了一切爱欲，转身舍离诸结，"
        "终尽苦的边际。",
        CLOSE_RAHULA_MOD,
        "（以下是原典的省文指示）如同上面就六内入处所说，同样就六外入处，"
        "乃至依意触为缘所生的感受，也照上面详说而各成一部经。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SC 所列 SN18.22（Apagata）之巴利本文备于记录中，"
        "所须之定型语逐字可对；五阴／六入处之编次差异同前经（SA_198）。"
        "本经与前经之别：前经由罗睺罗发问，本经由佛发问而罗睺罗请说；"
        "前经结于「断爱浊见、正现观、究竟苦边」，本经结于「超越慢计、寂静解脱」及"
        "「断诸爱欲、转去诸结」——正与巴利 SN18.21（`…anusayā na honti`）与 "
        "SN18.22（`…mānāpagataṁ mānasaṁ hoti vidhā samatikkantaṁ santaṁ suvimuttaṁ`）之别相合。"
        "信-校正：底本「越于二」义不可通，巴利作 `vidhā samatikkanta`——vidhā 谓慢之计量"
        "（胜、等、劣三种慢类之计度，Bodhi: discrimination；Anālayo: duality），"
        "求那跋陀罗似读 vidhā 为「二」（dvi）而致误，今据巴利正作「超越诸慢计」，"
        "并存底本「离诸相、寂灭解脱」以对 `santaṁ suvimuttaṁ`。"
        "「法根、法眼、法依」即 `bhagavaṁmūlakā dhammā, bhagavaṁnettikā, bhagavaṁpaṭisaraṇā`"
        "（诸法以世尊为根、为导、为归依），为经中定型语，今存汉本之简。"
    ),
}


# --- SA 200 罗睺罗（三）（SN 35.121 Rāhulovāda／MN 147）--------------------
_200_RECON_LIT = (
    "罗睺罗！一切无常。何等法无常？谓眼无常；色、眼识、眼触，"
    "及眼触因缘所生受、想、行、识，若苦、若乐、不苦不乐，彼一切无常。"
    "耳、鼻、舌、身、意，声、香、味、触、法，乃至意触因缘所生受，亦复如是。"
    "（底本此处唯作「如上无常广说」，今依所指之 SA_195／196 及巴利平行补出纲要，不演全文。）"
)
_200_RECON_MOD = (
    "罗睺罗！一切都是无常的。哪些法是无常的呢？就是说：眼是无常的；"
    "色、眼识、眼触，以及依眼触为缘所生的受、想、行、识，无论是苦、是乐、还是不苦不乐，"
    "这一切都是无常的。耳、鼻、舌、身、意，声、香、味、触、法，"
    "乃至依意触为缘所生的感受，也是一样。"
    "（原典此处只写「如上无常广说」，这里依它所指的 SA_195／196 与巴利平行补出纲要，"
    "不代拟全文。）"
)

def _200_ask(faculty_lit: str, faculty_mod: str) -> tuple[str, str]:
    """底本第一问作「解脱慧未熟」，后二问作「解脱智未熟」，今分别存之。"""
    lit = f"尔时世尊观察罗睺罗心，解脱之{faculty_lit}未熟，未堪任受增上法，问罗睺罗言："
    mod = (
        f"那时，世尊观察罗睺罗的心，见他解脱之{faculty_mod}还未成熟，"
        "还不堪领受更上一层的法，便问罗睺罗："
    )
    return lit, mod


_ASK1_LIT, _ASK1_MOD = _200_ask("慧", "慧")
_ASK2_LIT, _ASK2_MOD = _200_ask("智", "智")

SUTTAS["SA_200"] = {
    "lit": [
        OPEN_LIT,
        "尔时尊者罗睺罗往诣佛所，稽首佛足，退坐一面，白佛言：善哉世尊！为我说法。"
        "我闻法已，当独一静处，专精思惟，不放逸住；如是思惟：族姓子所以剃除须发，"
        "以正信故舍家出家，学道修持梵行者，正为见法自知作证：" + AWAKEN_LIT,
        _ASK1_LIT + "汝已为人说五受阴未？",
        "罗睺罗白佛：未也，世尊。",
        "佛告罗睺罗：汝当为人演说五受阴——色、受、想、行、识。",
        "尔时罗睺罗受佛教已，于异时为人演说五受阴；说已，还诣佛所，稽首佛足，退住一面，"
        "白佛言：世尊！我已为人说五受阴。唯愿世尊为我说法；我闻法已，当独一静处，"
        "专精思惟，不放逸住，乃至自知不受后有。",
        _ASK2_LIT + "汝已为人说六入处未？",
        "罗睺罗白佛：未也，世尊。佛告罗睺罗：汝当为人演说六入处。",
        "尔时罗睺罗于异时为人演说六入处；说已，来诣佛所，稽首礼足，退住一面，白佛言："
        "世尊！我已为人演说六入处。唯愿世尊为我说法；我闻法已，当独一静处，专精思惟，"
        "不放逸住，乃至自知不受后有。",
        _ASK2_LIT + "汝已为人说因缘法未？",
        "罗睺罗白佛：未也，世尊。佛告罗睺罗：汝当为人演说因缘法。",
        "尔时罗睺罗于异时为人广说因缘法已，来诣佛所，稽首礼足，退住一面，白佛言："
        "世尊！愿为我说法；我闻法已，当独一静处，专精思惟，不放逸住，乃至自知不受后有。",
        "尔时世尊复观察罗睺罗心，解脱之智未熟（如上广说），乃告罗睺罗言："
        "汝当于上所说诸法，独一静处，专精思惟，观察其义。",
        "尔时罗睺罗受佛教敕，于所闻法、所说法思惟称量，观察其义，作是念："
        "此诸法一切皆顺趣涅槃、流注涅槃、终归涅槃。",
        "尔时罗睺罗往诣佛所，稽首礼足，退住一面，白佛言：世尊！我已于所闻法、所说法，"
        "独一静处，思惟称量，观察其义，知此诸法皆顺趣涅槃、流注涅槃、终归涅槃。",
        "尔时世尊观察罗睺罗心，解脱之智已熟，堪任受增上法，告罗睺罗言：" + _200_RECON_LIT,
        "尔时罗睺罗闻佛所说，欢喜随喜，礼佛而退。",
        "尔时罗睺罗受佛教已，独一静处，专精思惟，不放逸住：族姓子所以剃除须发，着袈裟衣，"
        "以正信故舍家出家，学道纯修梵行者，正为见法自知作证——乃至自知不受后有。"
        "遂成阿罗汉，心善解脱。",
        CLOSE_RAHULA_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，罗睺罗尊者来到佛前，以头面礼佛足，退到一旁坐下，对佛说：太好了，世尊！"
        "请为我说法。我听了法，就独自在寂静处专心思惟，安住于不放逸；并这样思惟："
        "良家子之所以剃除须发、出于正信而舍家出家、学道修持梵行，正是为了见法而亲自证知："
        + AWAKEN_MOD,
        _ASK1_MOD + "你已经为人讲说五受阴了吗？",
        "罗睺罗对佛说：还没有，世尊。",
        "佛告诉罗睺罗：你应当为人演说五受阴——色、受、想、行、识。",
        "那时，罗睺罗领受佛的教导，后来便为人演说五受阴；说完之后，回到佛前，以头面礼佛足，"
        "退到一旁站立，对佛说：世尊！我已为人讲说五受阴了。愿世尊为我说法；我听了法，"
        "就独自在寂静处专心思惟，安住于不放逸，乃至自知不再受后有。",
        _ASK2_MOD + "你已经为人讲说六入处了吗？",
        "罗睺罗对佛说：还没有，世尊。佛告诉罗睺罗：你应当为人演说六入处。",
        "那时，罗睺罗后来便为人演说六入处；说完之后，来到佛前，以头面礼佛足，退到一旁站立，"
        "对佛说：世尊！我已为人演说六入处了。愿世尊为我说法；我听了法，就独自在寂静处专心思惟，"
        "安住于不放逸，乃至自知不再受后有。",
        _ASK2_MOD + "你已经为人讲说因缘法了吗？",
        "罗睺罗对佛说：还没有，世尊。佛告诉罗睺罗：你应当为人演说因缘法。",
        "那时，罗睺罗后来为人详说因缘法之后，来到佛前，以头面礼佛足，退到一旁站立，对佛说："
        "世尊！愿为我说法；我听了法，就独自在寂静处专心思惟，安住于不放逸，"
        "乃至自知不再受后有。",
        "那时，世尊又观察罗睺罗的心，见他解脱之智还未成熟（此处原典作「广说乃至」），"
        "便告诉罗睺罗：你应当把上面所说的诸法，在寂静处独自专心思惟，观察其中的义理。",
        "那时，罗睺罗领受佛的教敕，把先前所听、所讲的法反复思惟称量，观察其义，"
        "这样想道：这一切法都趣向涅槃、倾注涅槃、终归于涅槃。",
        "那时，罗睺罗来到佛前，以头面礼佛足，退到一旁站立，对佛说：世尊！我已把先前所听、"
        "所讲的法，在寂静处独自思惟称量、观察其义，知道这些法都趣向涅槃、倾注涅槃、终归于涅槃。",
        "那时，世尊观察罗睺罗的心，见他解脱之智已经成熟，堪能领受更上一层的法，"
        "便告诉罗睺罗：" + _200_RECON_MOD,
        "那时，罗睺罗听佛所说，欢喜随喜，礼佛而退。",
        "那时，罗睺罗领受佛的教导，独自在寂静处专心思惟，安住于不放逸："
        "良家子之所以剃除须发、身着袈裟、出于正信而舍家出家、学道纯修梵行，"
        "正是为了见法而亲自证知——乃至自知不再受后有。于是成就阿罗汉，心得善解脱。",
        CLOSE_RAHULA_MOD,
    ],
    "notes": (
        f"{PROV}"
        "review_status=gold_reconstructed，confidence=low：底本正文之法说核心仅作"
        "「罗睺罗！一切无常。何等法无常？谓眼无常，若色、眼识、眼触……如上无常广说」，"
        "为交叉指示而非全文；今依其所指之 SA_195／196 之六六式补出纲要，不演全文、不补造情节，"
        "并于文言栏以括注标明补出之界。"
        "SC 列 MN147／SN35.121（Rāhulovāda）为 resembling 平行：其框式与本经相合"
        "（`paripakkā rāhulassa vimuttiparipācaniyā dhammā`＝「解脱智熟，堪任受增上法」），"
        "而巴利以「眼常耶？无常耶？」之问答式说无常、苦、非我，汉本则作直陈式并接"
        "「如上无常广说」；又汉本之次第教授（五受阴→六入处→因缘法→思惟其义）不见于巴利，"
        "为汉本一系所独。今从汉本之直陈式（即其所指之 SA_195／196），不移入巴利之问答式。"
        "所补之「受、想、行、识」四类，据巴利平行 `yampidaṁ cakkhusamphassapaccayā uppajjati "
        "vedanāgataṁ, saññāgataṁ, saṅkhāragataṁ, viññāṇagataṁ`（凡依眼触为缘所生之受、想、行、识）；"
        "SA_195／196 于此处唯出受之三品（苦、乐、不苦不乐），今兼出而并存之。"
        "信-校正三事："
        "（一）「尼陀那法」为 nidāna 之音译，即因缘（法），今作「因缘法」而于此志其音译之原名。"
        "（二）「后住涅槃」之三语连文，巴利作 `nibbānaninnā nibbānapoṇā nibbānapabbhārā`"
        "（倾向涅槃、趣注涅槃、临趋涅槃），pabbhāra 谓如坡之下倾而终至，"
        "非「其后住于涅槃」，今作「终归涅槃」。"
        "（三）「正信非家，出家学道」为逐字对译之硬语（`saddhā agārasmā anagāriyaṁ pabbajati`），"
        "今作「以正信故舍家出家」以顺汉语。"
        "「解脱慧未熟」「解脱智未熟」二语底本互出，巴利统作 `vimuttiparipācaniyā dhammā`"
        "（能令解脱成熟之诸法），今分别存「解脱之慧」「解脱之智」而不强并为一。"
    ),
}


# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

# 逐经置信度：判准见模块 docstring
CONFIDENCE: dict[str, str] = {
    "SA_188": "high",
    "SA_189": "high",
    "SA_190": "high",
    "SA_191": "high",
    "SA_192": "medium",
    "SA_193": "medium",
    "SA_194": "high",
    "SA_195": "medium",
    "SA_196": "high",
    "SA_197": "high",
    "SA_198": "high",
    "SA_199": "high",
    "SA_200": "low",
}

# 底本正文核心仅作交叉指示、须依所指之经回填者：标 gold_reconstructed / low。
RECONSTRUCTED: dict[str, str] = {
    "SA_200": (
        "底本法说核心仅作「谓眼无常，若色、眼识、眼触……如上无常广说」，"
        "依所指之 SA_195／196 六六式及巴利平行（SN35.121）补出纲要，不演全文"
    ),
}

SIM_MAX = 0.55  # 繁转简嫌疑阈值（文言栏与求那跋陀罗底本之三元组相似度上限）

# 本脚本自身产出之状态；不可记为 pre-gold 状态，否则重跑会覆盖启发式草稿之来历。
OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

GOLD: dict[str, dict[str, str]] = {}
for _rid, _s in SUTTAS.items():
    _lit_paras: list[str] = list(_s["lit"])
    _mod_paras: list[str] = list(_s["mod"])
    assert len(_lit_paras) == len(_mod_paras), (
        f"{_rid} paragraph mismatch: lit={len(_lit_paras)} mod={len(_mod_paras)}"
    )
    GOLD[_rid] = {
        "kumarajiva_style_text": "\n".join(_lit_paras),
        "modern_psychology_text": "\n".join(_mod_paras),
        "notes": _s["notes"],
    }


def main() -> None:
    assert set(GOLD) == {f"SA_{i}" for i in range(188, 201)}, (
        "GOLD must cover SA_188–SA_200 exactly"
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

            v = validate_restyle(item.get("chinese_text") or "", lit, mod)
            item["validation"] = v
            item["forbidden_hits"] = v.get("forbidden_hits") or []

            sim = round(similarity_to_source(item.get("chinese_text") or "", lit), 3)
            item["similarity_to_source"] = sim

            lit_paras = lit.split("\n")
            mod_paras = mod.split("\n")
            para_ok = len(lit_paras) == len(mod_paras)
            item["paragraph_parallel"] = para_ok

            if v["status"] == "fail" and rid not in RECONSTRUCTED:
                item["review_status"] = "needs_doctrine_check"
            if sim >= SIM_MAX:
                item["review_status"] = "needs_restyle"

            report.append(
                {
                    "id": rid,
                    **v,
                    "sim": sim,
                    "paragraphs": len(lit_paras),
                    "paragraph_parallel": para_ok,
                    "confidence": item["confidence"],
                    "review_status": item["review_status"],
                }
            )
            (gold_dir / f"{rid.lower()}.json").write_text(
                json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        merged.append(item)

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa188-200.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fails = [r for r in report if r["status"] == "fail"]
    warns = [r for r in report if r["status"] == "warn"]
    oks = [r for r in report if r["status"] == "ok"]
    forbidden = [r for r in report if r["forbidden_hits"]]
    too_literal = [r for r in report if r["sim"] >= SIM_MAX]
    para_bad = [r for r in report if not r["paragraph_parallel"]]
    recon = [r for r in report if r["id"] in RECONSTRUCTED]
    max_r = max(report, key=lambda r: r["sim"])
    conf_split = {
        c: sum(1 for r in report if r["confidence"] == c) for c in ("high", "medium", "low")
    }

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_188–200 only)")
    print(f"validation: ok={len(oks)} warn={len(warns)} fail={len(fails)}")
    print(f"forbidden_hits={len(forbidden)}")
    print(
        f"sim>={SIM_MAX} (繁转简嫌疑): {len(too_literal)}  "
        f"max_sim={max_r['sim']} ({max_r['id']})  "
        f"mean_sim={round(sum(r['sim'] for r in report) / len(report), 3)}"
    )
    print(f"paragraph_parallel_violations={len(para_bad)}")
    print(f"gold={len(report) - len(recon)} gold_reconstructed={len(recon)}")
    print(f"confidence: {conf_split}")
    for r in report:
        print(
            r["id"],
            r["status"],
            f"sim={r['sim']}",
            f"paras={r['paragraphs']}",
            r["confidence"],
            r.get("issues"),
            r.get("warnings"),
        )


if __name__ == "__main__":
    main()
