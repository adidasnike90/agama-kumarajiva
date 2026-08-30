#!/usr/bin/env python3
"""Retranslate SA 711–730（觉支相应 卷二十八末–二十九）→ merge.

本批二十经：无畏×2 SN46.56；转趣 SN46.52；火 SN46.53；食 SN46.2／51；
一法×2 SN46.49／50（内／外支）；比丘 SN46.4；优波摩 SN46.8；阿那律（无专平行）；
转轮王×2 SN46.42；年少／果报 SN46.3；不善聚 SN47.45／AN5.52；善知识 SN45.2；
拘夷那竭 SN46.16；说 SN46.22；灭 SN46.27；分 SN46.41。

信：有 SN 平行者据巴利／Sujato 厘义；无专经 → medium。
    peyyāla／交叉指示补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_711–730；不触碰 SA_691–710（并行批次）；
      断言 SA_710 不变（若尚未 gold 则断言 SA_690）。
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

OPEN_GRID_LIT = "如是我闻：一时，佛住王舍城耆阇崛山中。"
OPEN_GRID_MOD = "我是这样听说的：有一次，佛住在王舍城耆阇崛山中。"

CLOSE_BH_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_BH_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

SEVEN_LIT = "念觉支、择法觉支、精进觉支、喜觉支、轻安觉支、定觉支、舍觉支"
SEVEN_MOD = "念觉支、择法觉支、精进觉支、喜觉支、轻安觉支、定觉支、舍觉支"

FIVE_NIV_LIT = "贪欲、瞋恚、睡眠、掉悔、疑"
FIVE_NIV_MOD = "贪欲、瞋恚、昏沉睡眠、掉举后悔、疑"

NISSAYA_LIT = "依远离、依离欲、依灭、向于舍"
NISSAYA_MOD = "依于远离、依于离欲、依于灭、而趋向舍"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
)

# 七觉支满链（无畏等）
CHAIN_LIT = (
    f"彼修念觉支，念满足已，于法简择思惟，修择法觉支；"
    f"择法满足已，精进方便，修精进觉支；"
    f"精进满足已，离诸食想而生喜，修喜觉支；"
    f"喜满足已，身心轻安，修轻安觉支；"
    f"轻安已而心定，修定觉支；"
    f"定满足已，贪忧息，舍心生，修舍觉支；舍觉支满足。"
)
CHAIN_MOD = (
    f"他修念觉支，念满足后，对法简择思惟，修择法觉支；"
    f"择法满足后，精进用功，修精进觉支；"
    f"精进满足后，离开对饮食的想而生喜，修喜觉支；"
    f"喜满足后，身心轻安，修轻安觉支；"
    f"轻安之后心定，修定觉支；"
    f"定满足后，贪与忧息灭，舍心生起，修舍觉支；舍觉支满足。"
)

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 711 无畏（烦恼／清净；SN46.56 系）------------------------------------
SUTTAS["SA_711"] = {
    "lit": [
        OPEN_GRID_LIT,
        "时有无畏王子，步涉游观，来诣佛所，问讯已，退坐一面，白佛言："
        "「世尊！有沙门、婆罗门作如是见、如是说：无因无缘，众生烦恼；无因无缘，众生清净。"
        "世尊云何？」",
        "佛告无畏：「彼说非思量、非善说。所以者何？有因有缘，众生烦恼；有因有缘，众生清净。」",
        "「何因何缘众生烦恼？谓贪欲增上，于他财、他众具起贪；于他有情起瞋恨，欲打缚伏；"
        f"不舍瞋恚；身睡心怠；心掉动、内不寂静；于过、现、未而生疑。"
        f"此五盖——{FIVE_NIV_LIT}——是众生烦恼之因缘。」",
        "无畏白佛：「瞿昙！一分之盖，已足扰心，何况一切？」"
        "复问：「何因何缘众生清净？」",
        "佛告无畏：「若人有胜念，久作久说能随忆持，于是修念觉支。"
        f"{CHAIN_LIT}"
        "无畏！此因此缘，众生清净。」",
        "无畏白佛：「若一分觉支满足，已令清净，何况一切？"
        "当何名此经？云何奉持？」"
        "佛言：「当名此为觉支经。」",
        "无畏白佛：「我是王子，安乐常求安乐；今登山而肢体疲极，"
        "得闻觉支经，疲劳尽忘。」"
        "王子无畏闻已，欢喜随喜，稽首礼足而去。",
    ],
    "mod": [
        OPEN_GRID_MOD,
        "那时有无畏王子，步行游观，来到佛所，问讯后坐在一边，对佛说："
        "「世尊！有沙门、婆罗门持这样的见、这样说：没有因缘，众生就烦恼；没有因缘，众生就清净。"
        "世尊怎么看？」",
        "佛告诉无畏：「他们那样说，没有经过思量，也不是善说。为什么？有因有缘，众生才烦恼；有因有缘，众生才清净。」",
        "「什么因缘使众生烦恼？就是贪欲强盛，对别人的财物、用具起贪；对其他有情起瞋恨，想打、绑、压制；"
        f"不舍瞋恚；身体昏沉、心里懈怠；心掉动、内里不安静；对过去、现在、未来起疑。"
        f"这五盖——{FIVE_NIV_MOD}——就是众生烦恼的因缘。」",
        "无畏对佛说：「瞿昙！哪怕一分盖，也够扰乱心了，何况全部？」"
        "又问：「什么因缘使众生清净？」",
        "佛告诉无畏：「如果人有殊胜的念，长久所作所说都能随顺忆持，这时就修念觉支。"
        f"{CHAIN_MOD}"
        "无畏！这就是众生清净的因缘。」",
        "无畏对佛说：「若一分觉支满足，已能使清净，何况全部？"
        "这部经该叫什么名字？该怎样受持？」"
        "佛说：「应当叫作觉支经。」",
        "无畏对佛说：「我是王子，安乐也常求安乐；今天上山，四肢疲惫，"
        "听了觉支经，疲倦都忘了。」"
        "王子无畏听完，欢喜随喜，叩头礼足后离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.56 Abhaya；"
        "本经以「烦恼／清净」立问（SA 异传），SN 作「无智无见／智见」。"
        "五盖为染因、七觉支为净因，与 SN 同构；汉「如是缘清净」误置于染段末，"
        "据前后问答校正。觉分→觉支；猗→轻安。"
    ),
}

# --- SA 712 无畏（无智无见；peyyāla）------------------------------------------
SUTTAS["SA_712"] = {
    "lit": [
        OPEN_GRID_LIT,
        "时有无畏王子来诣佛所，白佛言：「世尊！有沙门、婆罗门作如是见、如是说："
        "无因无缘，众生无智无见；无因无缘，众生有智有见。世尊云何？」",
        "佛告无畏：「彼说非善。有因有缘，众生无智无见；有因有缘，众生有智有见。"
        f"无智无见之因缘，谓五盖——{FIVE_NIV_LIT}；"
        f"智见之因缘，谓七觉支——{SEVEN_LIT}，次第满足，如上说。」",
        "无畏闻已，欢喜随喜，礼佛足而去。",
    ],
    "mod": [
        OPEN_GRID_MOD,
        "那时有无畏王子来到佛所，对佛说：「世尊！有沙门、婆罗门持这样的见、这样说："
        "没有因缘，众生就无智无见；没有因缘，众生就有智有见。世尊怎么看？」",
        "佛告诉无畏：「他们那样说并不善。有因有缘，众生才无智无见；有因有缘，众生才有智有见。"
        f"无智无见的因缘，就是五盖——{FIVE_NIV_MOD}；"
        f"智见的因缘，就是七觉支——{SEVEN_MOD}，按次第满足，如同前面所说。」",
        "无畏听完，欢喜随喜，礼佛足后离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.56；与 SA_711 同本，差别在「无智无见／智见」"
        "（≈ aññāṇa／adassana、ñāṇa／dassana），最贴近 SN。"
        "gold_reconstructed：汉「如上说」→据 SA_711／SN 补五盖、七觉支纲。"
    ),
}

# --- SA 713 转趣（SN46.52）----------------------------------------------------
SUTTAS["SA_713"] = {
    "lit": [
        OPEN_JET_LIT,
        "时众多比丘晨朝入城乞食，以时尚早，过外道精舍。外道言："
        "「瞿昙教弟子断五盖、住四念处、修七觉支；我等亦尔。与彼有何异？」"
        "诸比丘不喜，乞食已，往白世尊。",
        "佛告比丘：「彼若作是说，汝当反问：五盖种应有十，七觉支种应有十四。"
        "何等为十？何等为十四？如是问者，彼则骇散，不能善答。"
        "除如来及声闻众，我不见余众闻此能随喜。」",
        "「何等五盖说为十？内贪、外贪，各是盖，非智、非等觉，不转趣涅槃；"
        "瞋与瞋相、睡与眠、掉与悔、于善法疑与于不善法疑，亦复如是。是名五盖为十。」",
        "「何等七觉支说为十四？内法念住、外法念住，各是念觉支，是智、是等觉，能转趣涅槃；"
        "择善／择不善、断不善精进／长养善精进、喜／喜处、身轻安／心轻安、"
        "定／定相、舍善法／舍不善法——各成一觉支，是智、是等觉，能转趣涅槃。"
        "是名七觉支为十四。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时许多比丘清晨进城乞食，因为时间还早，就经过外道精舍。外道说："
        "「瞿昙教弟子断五盖、住四念处、修七觉支；我们也是这样。跟他有什么不同？」"
        "比丘们心里不高兴，乞食回来后，把这话告诉世尊。",
        "佛告诉比丘：「他们若这样说，你们应当反问：五盖按种类该有十，七觉支按种类该有十四。"
        "什么是十？什么是十四？这样一问，他们就会慌乱，答不好。"
        "除了如来和声闻众，我没看见别的人听了这个能随喜。」",
        "「怎样把五盖说成十？内贪、外贪，各自是盖，不是智、不是等觉，不能转趣涅槃；"
        "瞋与瞋的相、昏沉与睡眠、掉举与后悔、对善法的疑与对不善法的疑，也是一样。这叫五盖为十。」",
        "「怎样把七觉支说成十四？内法上的念住、外法上的念住，各自是念觉支，是智、是等觉，能转趣涅槃；"
        "择善／择不善、断不善的精进／长养善的精进、喜／喜处、身轻安／心轻安、"
        "定／定相、舍善法／舍不善法——各自成就一觉支，是智、是等觉，能转趣涅槃。"
        "这叫七觉支为十四。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.52 Pariyāya（五盖十、七觉十四）。"
        "罗什风压缩外道对扬与十／十四反复套语；「转趣涅槃」≈ nibbāna-ninna。"
    ),
}

# --- SA 714 火（SN46.53；peyyāla 开场）----------------------------------------
SUTTAS["SA_714"] = {
    "lit": [
        OPEN_JET_LIT,
        "时众多比丘遇外道，如上说。佛告比丘：「若外道作是说，当复问："
        "心微劣犹豫时，应修何觉支、何为非时？心掉动犹豫时，应修何觉支、何为非时？"
        "如是问者，彼则骇散。」",
        "「诸比丘！心微劣、犹豫时，不应修轻安、定、舍觉支——譬如小火，益以焦炭，火则灭；"
        "尔时当修择法、精进、喜觉支——譬如小火，足其干薪，火则炽。」",
        "「心掉动、犹豫时，不应修择法、精进、喜觉支——譬如炽火，更投干薪，火逾盛；"
        "尔时当修轻安、定、舍觉支——譬如燃火，益以焦炭，火则息。"
        "念觉支者，于一切时兼助。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时许多比丘遇到外道，情形如同前面所说。佛告诉比丘：「若外道这样说，还应当再问："
        "心微弱、犹豫时，该修哪些觉支、哪些不该修？心掉动、犹豫时，该修哪些觉支、哪些不该修？"
        "这样一问，他们就会慌乱。」",
        "「诸比丘！心微弱、犹豫时，不该修轻安、定、舍觉支——好比小火，再加焦炭，火反而灭；"
        "这时该修择法、精进、喜觉支——好比小火，添上干柴，火就旺起来。」",
        "「心掉动、犹豫时，不该修择法、精进、喜觉支——好比大火，再加干柴，火更猛；"
        "这时该修轻安、定、舍觉支——好比燃烧的火，加上焦炭，火就熄下去。"
        "念觉支在任何时候都起辅助作用。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.53 Aggi（羸心／掉心配觉支，火喻）。"
        "gold_reconstructed：汉「众多比丘如上说」→据 SA_713 补外道对扬开场；"
        "压缩问答「如是世尊」套语。"
    ),
}

# --- SA 715 食（SN46.2／51）---------------------------------------------------
SUTTAS["SA_715"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「五盖、七觉支，皆有食、有不食。譬如身依食而立；五盖、七觉支亦依食而住。」",
        "「贪欲盖食——于净相不正思惟；瞋恚盖食——于障碍相不正思惟；"
        "睡眠盖食——于微弱、不乐、欠呿、多食、懈怠不正思惟；"
        "掉悔盖食——于心不寂静不正思惟；"
        "疑盖食——于过、现、未犹豫不正思惟。未生令生，已生令增。」",
        "「贪欲盖不食——思惟不净；瞋恚盖不食——思惟慈心；"
        "睡眠盖不食——思惟明照；掉悔盖不食——思惟寂止；"
        "疑盖不食——思惟缘起。未生令不生，已生令断。」",
        "「念觉支食——思惟四念处；择法觉支食——择善与不善；"
        "精进觉支食——思惟四正断；喜觉支食——于喜及喜处思惟；"
        "轻安觉支食——于身、心轻安思惟；定觉支食——思惟四禅；"
        "舍觉支食——思惟断界、无欲界、灭界。未生令生，已生令增。」",
        "「七觉支不食者，于上诸处不思惟：未生令不生，已生令退。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「五盖、七觉支，都有食、有不食。好比身体靠食物才能立住；五盖、七觉支也靠食才能住。」",
        "「贪欲盖的食——对净相作不正思惟；瞋恚盖的食——对障碍相作不正思惟；"
        "睡眠盖的食——对微弱、不乐、打呵欠、多食、懈怠作不正思惟；"
        "掉悔盖的食——对心不寂静作不正思惟；"
        "疑盖的食——对过去、现在、未来犹豫而作不正思惟。未生的使生，已生的使增长。」",
        "「贪欲盖的不食——思惟不净；瞋恚盖的不食——思惟慈心；"
        "睡眠盖的不食——思惟明照；掉悔盖的不食——思惟寂止；"
        "疑盖的不食——思惟缘起。未生的使不生，已生的使断除。」",
        "「念觉支的食——思惟四念处；择法觉支的食——择善与不善；"
        "精进觉支的食——思惟四正断；喜觉支的食——对喜和喜处思惟；"
        "轻安觉支的食——对身、心轻安思惟；定觉支的食——思惟四禅；"
        "舍觉支的食——思惟断界、无欲界、灭界。未生的使生，已生的使增长。」",
        "「七觉支的不食，就是对这些处所不去思惟：未生的使不生，已生的使退失。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.2／SN46.51 Āhāra（盖与觉支之食／不食）。"
        "据 SN 校正：掉悔食汉列「亲族等觉」→作「心不寂静」（cetaso avūpasamo）；"
        "罗什风重排为盖食→盖不食→觉支食→觉支不食，删汉本交错重复。"
    ),
}

# --- SA 716 一法（内支／不正思惟；≈SN46.49 系）--------------------------------
SUTTAS["SA_716"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「于内法中，我不见一法，能令未生恶不善法生、已生者增广，"
        "未生善法不生、已生者退，如不正思惟。」",
        f"「不正思惟者：未生五盖——{FIVE_NIV_LIT}——令生，已生令增；"
        f"未生七觉支——{SEVEN_LIT}——令不生，已生令退。」",
        "「我不见一法，能令未生恶法不生、已生者断，未生善法生、已生者增广，如正思惟。」",
        f"「正思惟者：未生五盖令不生，已生令断；未生七觉支令生，已生令增。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「在内法之中，我看不见有哪一法，能使未生的恶不善法生起、已生的增长，"
        "未生的善法不生、已生的退失，像不正思惟这样。」",
        f"「不正思惟：未生的五盖——{FIVE_NIV_MOD}——使它生起，已生的使它增长；"
        f"未生的七觉支——{SEVEN_MOD}——使它不生，已生的使它退失。」",
        "「我看不见有哪一法，能使未生的恶法不生、已生的断除，未生的善法生起、已生的增长，像正思惟这样。」",
        f"「正思惟：未生的五盖使它不生，已生的使它断除；未生的七觉支使它生起，已生的使它增长。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：内容合 SN46.49 Ajjhattikaṅga（内支＝yoniso／ayoniso）；"
        "SC 表列 resembling SN46.29（断结之法＝七觉支）为另一经旨，本经不从。"
        "据理校正：汉「不正思惟」段误写择法等「令生」→改为令不生／令退。"
    ),
}

# --- SA 717 一法（外支／善知识；SN46.50）--------------------------------------
SUTTAS["SA_717"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「于外法中，我不见一法，能令未生恶不善法生、已生者增广，"
        "未生善法不生、已生者退，如恶知识、恶伴党。」",
        f"「恶知识者：未生五盖令生，已生令增；未生七觉支令不生，已生令退。」",
        "「我不见一法，能令未生恶法不生、已生者断，未生善法生、已生者增广，"
        "如善知识、善伴党、善随从。」",
        f"「善知识者：未生五盖令不生，已生令断；未生七觉支令生，已生令增。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「在外法之中，我看不见有哪一法，能使未生的恶不善法生起、已生的增长，"
        "未生的善法不生、已生的退失，像恶知识、恶同伴这样。」",
        f"「恶知识：未生的五盖使它生起，已生的使它增长；未生的七觉支使它不生，已生的使它退失。」",
        "「我看不见有哪一法，能使未生的恶法不生、已生的断除，未生的善法生起、已生的增长，"
        "像善知识、善同伴、善随从这样。」",
        f"「善知识：未生的五盖使它不生，已生的使它断除；未生的七觉支使它生起，已生的使它增长。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.50 Bāhiraṅga（外支＝kalyāṇamitta）；"
        "与 SA_716 内／外相对。罗什风压缩对称句。"
    ),
}

# --- SA 718 比丘（舍利弗；SN46.4）---------------------------------------------
SUTTAS["SA_718"] = {
    "lit": [
        OPEN_JET_LIT,
        f"尊者舍利弗告诸比丘：「有七觉支——{SEVEN_LIT}。"
        "此七觉支我已决定而得，不待强求；晨朝、日中、日暮，随所欲入。」",
        "「譬如王大臣箱中有种种衣，随时取用，得大自在。"
        "我于念觉支，清净纯白：起知起，住知住，灭知灭；"
        "择法、精进、喜、轻安、定、舍，亦复如是。」",
        "诸比丘闻尊者所说，欢喜奉行。",
    ],
    "mod": [
        OPEN_JET_MOD,
        f"尊者舍利弗告诉比丘们：「有七觉支——{SEVEN_MOD}。"
        "这七觉支我已经决定得到，不必强求；清晨、正午、傍晚，随我想入就入。」",
        "「好比王的大臣箱子里有各种衣服，随时取用，很自在。"
        "我对念觉支，清净纯白：生起知道生起，安住知道安住，灭去知道灭去；"
        "择法、精进、喜、轻安、定、舍，也是一样。」",
        "比丘们听了尊者所说，都欢喜奉行。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.4 Vattha（舍利弗随意入七觉支，衣喻）。"
        "据 SN：「得大自在」意译随意披衣；知起／住／灭。"
    ),
}

# --- SA 719 优波摩（SN46.8）---------------------------------------------------
SUTTAS["SA_719"] = {
    "lit": [
        "如是我闻：一时，佛住巴连弗邑。"
        "尊者优波摩、尊者阿提目多住鸡林精舍。",
        "晡时，阿提目多从禅觉，诣优波摩所，问言："
        "「能知方便修七觉支，如是乐住正受、如是苦住正受不？」",
        "优波摩言：「能。若修念觉支时思惟：心未善解脱，睡眠未害，掉悔未调，"
        "精进不得平等——如是苦住。择法乃至舍，亦如是。」",
        "「若思惟：心已善解脱，睡眠已害，掉悔已调，不待强勤而得平等——"
        "如是乐住。知方便修七觉支，则知乐住与苦住。」",
        "二尊者论已，各从座起而去。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在巴连弗邑。"
        "尊者优波摩、尊者阿提目多住在鸡林精舍。",
        "下午，阿提目多从禅定出来，到优波摩那里，问："
        "「能不能知道方便修七觉支时，怎样是乐住正受、怎样是苦住正受？」",
        "优波摩说：「能。若修念觉支时这样想：心还没善解脱，睡眠还没除掉，掉悔还没调伏，"
        "精进不得平等——这就是苦住。择法一直到舍，也是一样。」",
        "「若这样想：心已经善解脱，睡眠已经除掉，掉悔已经调伏，不必强求就得平等——"
        "这就是乐住。知道方便修七觉支，就知道乐住与苦住。」",
        "两位尊者讨论完，各自起座离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.8 Upavāna；"
        "汉作优波摩／阿提目多、巴连弗，SN 作 Upavāna／Sāriputta、憍赏弥——从汉地人事。"
        "义据 SN：心善解脱、害睡眠、调掉悔、精进平等 → 乐住。"
    ),
}

# --- SA 720 阿那律（无专平行）-------------------------------------------------
SUTTAS["SA_720"] = {
    "lit": [
        OPEN_JET_LIT,
        "尊者阿那律住松林精舍。众多比丘来问："
        "「知方便修七觉支时生乐住不？」",
        "阿那律言：「知。修念觉支时善思惟：心善解脱，善害睡眠，善调掉悔；"
        "精勤不怠，身轻安不动乱，系心而住，一心正受。"
        "择法、精进、喜、轻安、定、舍，亦如是。是名乐住。」",
        "诸比丘欢喜随喜而去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "尊者阿那律住在松林精舍。许多比丘前来问："
        "「知道方便修七觉支时能生起乐住吗？」",
        "阿那律说：「知道。修念觉支时好好思惟：心已善解脱，已善除睡眠，已善调掉悔；"
        "精勤不懈怠，身体轻安不动乱，把心系住，一心正受。"
        "择法、精进、喜、轻安、定、舍，也是一样。这叫做乐住。」",
        "比丘们欢喜随喜后离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：无 SC 专经平行；与 SA_719 同系（知方便→乐住），"
        "说者为阿那律，唯正面乐住、不及苦住。参 SN46.8 定型语。"
    ),
}

# --- SA 721 转轮王（略；SN46.42）----------------------------------------------
SUTTAS["SA_721"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「转轮圣王出世，有七宝现：金轮、象、马、珠、女、主藏臣、主兵臣。」",
        f"「如是如来出世，有七觉支宝现——{SEVEN_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「转轮圣王出现于世时，有七宝出现：金轮、象、马、珠、女、主藏臣、主兵臣。」",
        f"「同样，如来出现于世时，有七觉支宝出现——{SEVEN_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.42 Cakkavatti（七宝∥七觉支宝）。"
        "汉本此经搀入金轮游行残句，据 SN／下经结构校正为略说；广说见 SA_722。"
    ),
}

# --- SA 722 转轮王（广；SN46.42 系）--------------------------------------------
SUTTAS["SA_722"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「转轮圣王出世，七宝现于世间。」",
        "「金轮宝者：刹利灌顶王于月十五日沐浴受斋，大臣围绕；金轮自东方出，千辐齐毂，轮相具足。"
        "王两手承轮，循古圣王道乘虚游行四天下；所至之处，小王奉迎归伏，愿王止此教化。"
        "王告言：但当如法善化，非法者来白。轮还，住虚空于正殿之上。」",
        "「象宝：纯色鲜好，七支拄地，一日调伏，如经年所调；王乘之晨旦周行四海，日中还宫。」",
        "「马宝：纯青乌尾，一日调伏；王乘之晨出周行四海，日中还宫。」",
        "「摩尼珠宝：形有八楞，光泽无隙，宫中常为灯明；阴雨之夜持以导军，光明照及一由旬。」",
        "「女宝：不长不短、不粗不细，寒时体暖、热时体凉，软语爱语，先起后卧，瞻王意色，身口不违。」",
        "「主藏臣宝：本行布施，生得天眼，水陆远近有主无主之藏悉见；王须宝时，乃至海中出金瓮以奉。」",
        "「主兵臣宝：聪明智辩，知王宜去宜住、宜出宜入；四兵顿止不令疲极，现法后世功德之事悉白于王。」",
        f"「如是如来、应、等正觉出兴于世，七觉支宝现——{SEVEN_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「转轮圣王出现于世时，七宝出现在世间。」",
        "「金轮宝：刹利灌顶王在月十五日沐浴持斋，大臣围绕；金轮从东方出现，千辐、轮毂整齐，轮相具足。"
        "王两手托着轮，沿着古圣王的道路在虚空中游历四天下；所到之处，小王迎接归顺，请王留在这里教化。"
        "王说：你们只管如法善加教化，有非法的再来告诉我。轮回来后，停在正殿的虚空中。」",
        "「象宝：颜色纯正鲜美，四足与鼻等七处拄地，一天就能调好，像调了整年一样；王乘着它清晨走遍四海，中午回宫。」",
        "「马宝：纯青色、乌黑的尾巴，一天就能调好；王乘着它清晨走遍四海，中午回宫。」",
        "「摩尼珠宝：有八个棱角，光泽没有瑕疵，在宫里常常当作灯；雨夜拿着它走在军队前面，光照达到一由旬。」",
        "「女宝：不高不矮、不粗不细，冷时身体暖、热时身体凉，软语爱语，先起后睡，观察王的神色，身口都不违背。」",
        "「主藏臣宝：因往昔布施，生来有天眼，水里陆上远近、有主无主的伏藏都能看见；王需要宝物时，甚至能从海里取出装满金子的瓮献上。」",
        "「主兵臣宝：聪明善辩，知道王该离开该停留、该出该入；军队驻扎行进不使疲累，现法后世有功德的事都禀报给王。」",
        f"「同样，如来、应供、等正觉出现于世时，七觉支宝出现——{SEVEN_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：SN46.42 之广说（七宝各别）；结归七觉支宝与略经同。"
        "罗什风压缩各方国归伏套语与调象马重复，义不删宝。"
    ),
}

# --- SA 723 年少（SN46.3 系；侍奉闻法）----------------------------------------
SUTTAS["SA_723"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「善哉！年少比丘当供养奉事诸尊长老。所以者何？"
        "供养奉事，则时时得闻深妙之法；闻已，身正、心正。」",
        "「尔时修念觉支，念满足；于法简择思惟，修择法觉支；"
        "乃至精进、喜、轻安、定、舍觉支，修习满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「很好！年轻比丘应当供养奉事各位尊长老。为什么？"
        "供养奉事，就能时时听到深妙的法；听了以后，身也正、心也正。」",
        "「这时修念觉支，念满足；对法简择思惟，修择法觉支；"
        "一直到精进、喜、轻安、定、舍觉支，都修习满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling SN46.3 Sīla（闻法→二正→七觉支链）。"
        "本经特嘱年少事长老；gold_reconstructed：汉「乃至捨觉分」→压缩觉支链。"
    ),
}

# --- SA 724 果报（SN46.3 系；见持戒者）----------------------------------------
SUTTAS["SA_724"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「若比丘持戒、修德、有惭愧、成真实法——"
        "见此人者多得果报；闻、随忆念、随出家，皆多功德，何况亲近恭敬奉事。」",
        "「所以者何？亲近奉事，则时时得闻深妙之法；闻已，身正、心正；"
        "方便修习七觉支，自念至舍，修习满足。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「如果比丘持戒、修德、有惭愧、成就真实法——"
        "见到这样的人就多得果报；听闻、随顺忆念、随他出家，都有很多功德，何况亲近恭敬奉事。」",
        "「为什么？亲近奉事，就能时时听到深妙的法；听了以后，身也正、心也正；"
        "方便修习七觉支，从念到舍，都修习满足。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：resembling SN46.3（见／闻持戒等有大果）；"
        "与 SA_723 同链，开端改「年少事长」为「见持戒者多果」。"
        "gold_reconstructed：汉「乃至捨觉分」→七觉支满足。"
    ),
}

# --- SA 725 不善聚（AN5.52／觉支相应异传）------------------------------------
SUTTAS["SA_725"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「说不善积聚者，谓五盖——{FIVE_NIV_LIT}，是为正说。"
        "所以者何？纯一不善之聚，唯五盖。」",
        f"「说善积聚者，谓七觉支——{SEVEN_LIT}，是为正说。"
        "所以者何？纯一满净之聚，唯七觉支。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告诉比丘：「说到不善的积聚，就是五盖——{FIVE_NIV_MOD}，这样说才正确。"
        "为什么？纯粹的不善积聚，只有五盖。」",
        f"「说到善的积聚，就是七觉支——{SEVEN_MOD}，这样说才正确。"
        "为什么？纯粹圆满清净的积聚，只有七觉支。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：不善聚≈AN5.52／SN47.5（五盖）；"
        "善聚 SN47.45 作四念处，本经在觉支相应以七觉支为善聚（与 SA_611 念处本对观）。"
    ),
}

# --- SA 726 善知识（SN45.2；觉支版）-------------------------------------------
SUTTAS["SA_726"] = {
    "lit": [
        "如是我闻：一时，佛住王舍城夹谷精舍。尊者阿难亦在彼住。",
        "阿难独坐思惟：「半梵行者，所谓善知识、善伴党、善随从。」"
        "从禅觉，往白世尊。",
        "佛告阿难：「莫作是言。纯一满净、梵行清白，即是善知识、善伴党、善随从——"
        "非半，乃全体也。」",
        f"「我为善知识故，有众生于我取得念觉支，{NISSAYA_LIT}；"
        f"择法、精进、喜、轻安、定、舍觉支，亦{NISSAYA_LIT}。"
        "以是当知：善知识者，梵行全体。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在王舍城夹谷精舍。尊者阿难也住在那里。",
        "阿难独自静坐思惟：「梵行的一半，就是善知识、善同伴、善随从。」"
        "从禅定出来，前去禀告世尊。",
        "佛告诉阿难：「不要这样说。纯粹圆满清净、梵行清白，就是善知识、善同伴、善随从——"
        "不是一半，而是全体。」",
        f"「因为我是善知识，有众生在我这里取得念觉支，{NISSAYA_MOD}；"
        f"择法、精进、喜、轻安、定、舍觉支，也{NISSAYA_MOD}。"
        "因此应当知道：善知识就是梵行的全体。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN45.2 Upaḍḍha（善知识＝全梵行，非半）；"
        f"SN 以八支道说明，本经在觉支相应以七觉支＋{NISSAYA_LIT} 说明——从汉相应。"
        "据 SN 校正：「半」→「全体」。"
    ),
}

# --- SA 727 拘夷那竭（SN46.16 系）---------------------------------------------
SUTTAS["SA_727"] = {
    "lit": [
        "如是我闻：一时，佛在力士聚落人间游行，于拘夷那竭城、希连河间住。",
        "佛告阿难：「四重襞叠敷郁多罗僧，我今背痛，欲小卧息。」"
        "阿难受教敷已。世尊右胁而卧，足足相累，正念正智。",
        "佛告阿难：「汝说七觉支。」"
        f"阿难白佛：「念觉支，世尊自觉成等正觉，说{NISSAYA_LIT}；"
        f"择法、精进、喜、轻安、定、舍，亦复如是。」",
        "佛问：「汝说精进耶？」阿难言：「说精进。世尊！善逝！」"
        "佛言：「唯精进，修习多修习，得无上正尽觉。」说已，端身正坐系念。",
        "时有异比丘说偈赞叹：闻法能忍疾、七觉支善说、身婴苦患而端坐听——"
        "故当专思，听大师所讲。说偈已，从座起去。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛在力士聚落人间游行，住在拘夷那竭城与希连河之间。",
        "佛告诉阿难：「把郁多罗僧叠成四层铺好，我现在背痛，想稍微躺下休息。」"
        "阿难遵命铺好。世尊右侧卧，两足相叠，正念正智。",
        "佛告诉阿难：「你说说七觉支。」"
        f"阿难对佛说：「念觉支，是世尊自己觉悟成等正觉后所说，{NISSAYA_MOD}；"
        f"择法、精进、喜、轻安、定、舍，也是一样。」",
        "佛问：「你是在说精进吗？」阿难说：「是说精进。世尊！善逝！」"
        "佛说：「正是精进，修习多修习，能得无上正尽觉。」说完，端正身体坐起，系念。",
        "当时有一位比丘说偈赞叹：听法能忍住病痛、七觉支说得好、身体大病却端坐听法——"
        "所以应当专心，听大师所说。说完偈，起座离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.16 Gilāna（病中说觉支而起）；"
        "SN 作大目犍连／竹林，汉作阿难／拘夷那竭——从汉本事。"
        "罗什风压缩长偈为要旨；「阿耨多罗三藐三菩提」→「无上正尽觉」。"
    ),
}

# --- SA 728 说（SN46.22）------------------------------------------------------
SUTTAS["SA_728"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「有七觉支。何等为七？{SEVEN_LIT}。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告诉比丘：「有七觉支。哪七支？{SEVEN_MOD}。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.22 Desanā（七觉支略说名目）。"
        "gold_reconstructed：汉「乃至捨觉分」→列七支全名。"
    ),
}

# --- SA 729 灭（SN46.27）------------------------------------------------------
SUTTAS["SA_729"] = {
    "lit": [
        OPEN_JET_LIT,
        f"佛告比丘：「当修七觉支——{SEVEN_LIT}。"
        f"修念觉支，{NISSAYA_LIT}；择法、精进、喜、轻安、定、舍，亦复如是。"
        "如是修习，能趣爱尽。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"佛告诉比丘：「应当修七觉支——{SEVEN_MOD}。"
        f"修念觉支，{NISSAYA_MOD}；择法、精进、喜、轻安、定、舍，也是一样。"
        "这样修习，能趋向爱的尽灭。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.27 Taṇhānirodha（七觉支→渴爱灭）。"
        "据 SN 点明「爱尽」；汉仅列依远离等。"
    ),
}

# --- SA 730 分（SN46.41；三慢）------------------------------------------------
SUTTAS["SA_730"] = {
    "lit": [
        OPEN_JET_LIT,
        "佛告比丘：「过去诸沙门、婆罗门，凡能舍三种分别——我胜、我等、我劣——"
        "皆由修习七觉支故；未来、现在能舍者，亦复如是。」",
        f"「何等七？{SEVEN_LIT}。"
        "修此七支，则能舍彼三分。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "佛告诉比丘：「过去的沙门、婆罗门，凡是能舍掉三种分别——我更胜、我相等、我更劣——"
        "都是因为修习七觉支；未来、现在能舍的，也是一样。」",
        f"「哪七支？{SEVEN_MOD}。"
        "修这七支，就能舍掉那三种分别。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN46.41 Vidhā（舍三分别／三慢靠七觉支）。"
        "gold_reconstructed：汉仅「过去未来修七觉分」peyyāla → 据 SN 补 tisso vidhā"
        "（我胜／我等／我劣）及三世句。"
    ),
}

# ---------------------------------------------------------------------------
# Confidence / reconstruction
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_711": "high",
    "SA_712": "high",
    "SA_713": "high",
    "SA_714": "high",
    "SA_715": "high",
    "SA_716": "high",
    "SA_717": "high",
    "SA_718": "high",
    "SA_719": "high",
    "SA_720": "medium",
    "SA_721": "high",
    "SA_722": "high",
    "SA_723": "high",
    "SA_724": "high",
    "SA_725": "high",
    "SA_726": "high",
    "SA_727": "high",
    "SA_728": "high",
    "SA_729": "high",
    "SA_730": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_712": "无畏 peyyāla：无智无见／智见＋五盖／七觉支纲自 SA_711／SN46.56",
    "SA_714": "外道对扬开场据 SA_713；火喻配觉支据 SN46.53",
    "SA_723": "乃至捨觉分 → 压缩七觉支满足链",
    "SA_724": "乃至捨觉分 → 七觉支满足",
    "SA_728": "乃至捨觉分 → 七觉支全名",
    "SA_730": "peyyāla「过去未来修」→ SN46.41 三分别＋三世",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(711, 731)}, (
        "GOLD must cover SA_711–SA_730 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    # Parallel batch owns 691–710
    assert not any(f"SA_{i}" in GOLD for i in range(691, 711))

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

    # Boundary: SA_710 if gold, else SA_690
    _goldish = {"gold", "gold_reconstructed"}
    boundary_id = "SA_710"
    for rec in records:
        if rec["id"] == "SA_710" and rec.get("review_status") not in _goldish:
            boundary_id = "SA_690"
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

    # Snapshot 691–710 to assert untouched
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
        if rec["id"] in {f"SA_{i}" for i in range(691, 711)}
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
    (ROOT / "data" / "translated" / "validation_report_sa711-730.json").write_text(
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
    continuous_711_730 = all(
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(711, 731)
    )
    untouched_691_710 = all(f"SA_{i}" not in GOLD for i in range(691, 711))

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_711–SA_730 only)")
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
    print(f"continuous_gold_SA_711–730={continuous_711_730}")
    print(f"SA_691–710_untouched={untouched_691_710}")
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
