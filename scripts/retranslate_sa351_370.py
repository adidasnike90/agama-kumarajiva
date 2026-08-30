#!/usr/bin/env python3
"""Retranslate SA 351–370（卷第十四末–十五 因緣相應）→ merge into final_translated_data.json.

本批二十经：茂师罗、沙门婆罗门×3、老死、种智×2、无明增、思量×3、
多闻、说法、次法、见法般涅槃、毗婆尸等、修习、三摩提、十二因缘×2。

信：有平行者以 SN／Pāli／Sujato 厘义；无平行者 medium；
    唯交叉指示（SA 370）→ gold_reconstructed。
达：白话与罗什风逐段对照，段数严格相同。
雅：长文（≥400 字）sim < 0.45；短文 < 0.50（`assess_gold`）。
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

CLOSE_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

AWAKEN_LIT = "「我生已尽，梵行已立，所作已作，自知不受后有。」"
AWAKEN_MOD = "「我生已尽，梵行已立，所作已作，自知不受后有。」"

DO_CHAIN_LIT = (
    "缘无明行，缘行识，缘识名色，缘名色六入处，缘六入处触，缘触受，"
    "缘受爱，缘爱取，缘取有，缘有生，缘生老死忧悲恼苦——"
    "如是纯大苦聚集。"
)
DO_CHAIN_MOD = (
    "无明缘行，行缘识，识缘名色，名色缘六入处，六入处缘触，触缘受，"
    "受缘爱，爱缘取，取缘有，有缘生，生缘老死忧悲恼苦——"
    "这样纯大苦聚集。"
)
DO_CEASE_LIT = (
    "无明灭则行灭，行灭则识灭，乃至生灭则老死忧悲恼苦灭——"
    "如是纯大苦聚灭。"
)
DO_CEASE_MOD = (
    "无明灭则行灭，行灭则识灭，乃至生灭则老死忧悲恼苦灭——"
    "这样纯大苦聚灭。"
)

# 离信等五：aññatra saddhāya … diṭṭhinijjhānakkhantiyā
APART_LIT = "离信、离欲乐、离传闻、离觉想推求、离见审忍"
APART_MOD = "不靠信仰、不靠喜乐、不靠传闻、不靠推求、不靠见审忍"

LINKS_FWD_LIT = "生、有、取、爱、受、触、六入处、名色、识、行"
LINKS_FWD_MOD = "生、有、取、爱、受、触、六入处、名色、识、行"
LINKS_REV_LIT = "老死乃至行"
LINKS_REV_MOD = "老死乃至行"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)
NO_PARALLEL = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参同相应之巴利定型语厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」，本经作 medium。"
)

# ---------------------------------------------------------------------------
# 逐经
# ---------------------------------------------------------------------------

SUTTAS: dict[str, dict] = {}

# --- SA 351 茂师罗（SN 12.68 Kosambī）---------------------------------------
SUTTAS["SA_351"] = {
    "lit": [
        "如是我闻：一时，尊者那罗、尊者茂师罗、尊者殊胜、尊者阿难，"
        "住舍卫国象耳池侧。",
        "尔时，尊者那罗语尊者茂师罗言：「" + APART_LIT + "，"
        "汝有正自觉知见生否——所谓生缘故有老死？」"
        "茂师罗言：「" + APART_LIT + "，我知我见：生缘故有老死。」",
        "「如是有缘生，取缘有，爱缘取，受缘爱，触缘受，六入处缘触，"
        "名色缘六入处，识缘名色，行缘识，无明缘行——汝亦" + APART_LIT + "而知见否？」"
        "答言：「如是，我知我见：无明缘行。」",
        "「生灭则老死灭，乃至无明灭则行灭——汝亦" + APART_LIT + "而知见否？」"
        "答言：「如是，我知我见。」",
        "「有灭则寂灭、涅槃——汝亦" + APART_LIT + "而知见否？」"
        "答言：「如是，我知我见：有灭则寂灭、涅槃。」",
        "复问：「若尔，汝今便是漏尽阿罗汉耶？」"
        "尊者茂师罗默然；第二、第三问，亦默然不答。",
        "尔时，尊者殊胜语茂师罗：「止！我当代答尊者那罗。」"
        "茂师罗言：「止！汝为我答。」",
        "殊胜亦如茂师罗所答，自说：" + APART_LIT + "而知见——"
        "有灭则寂灭、涅槃。",
        "那罗问：「若尔，汝今便是漏尽阿罗汉耶？」"
        "殊胜言：「我以正慧如实善见：有灭则寂灭、涅槃；"
        "然我非漏尽阿罗汉。」",
        "「今当说譬。旷野路边有井，无绳无罐。"
        "行人热渴所逼，绕井谛观，如实知有水，而身不能触。"
        "如是，我如实善见有灭则寂灭、涅槃，而自身未得漏尽。」",
        "阿难语那罗：「彼殊胜所说，汝复云何？」"
        "那罗言：「殊胜善说，我无余言，唯随喜善。」",
        "时彼正士各说已，从座起去。",
    ],
    "mod": [
        "我是这样听说的：有一次，那罗、茂师罗、殊胜、阿难四位尊者，"
        "住在舍卫国象耳池边。",
        "那时，那罗对茂师罗说：「" + APART_MOD + "，"
        "你是否亲自生起正知正见——生为缘所以有老死？」"
        "茂师罗说：「" + APART_MOD + "，我知我见：生为缘所以有老死。」",
        "「同样，有缘生，取缘有，爱缘取，受缘爱，触缘受，六入处缘触，"
        "名色缘六入处，识缘名色，行缘识，无明缘行——"
        "你也" + APART_MOD + "而知道看见吗？」"
        "答：「是的，我知我见：无明缘行。」",
        "「生灭则老死灭，乃至无明灭则行灭——你也" + APART_MOD + "而知道看见吗？」"
        "答：「是的，我知我见。」",
        "「有的灭尽就是寂灭、涅槃——你也" + APART_MOD + "而知道看见吗？」"
        "答：「是的，我知我见：有灭则寂灭、涅槃。」",
        "又问：「既然如此，你现在就是漏尽阿罗汉吗？」"
        "茂师罗沉默；问第二、第三次，也沉默不答。",
        "那时，殊胜对茂师罗说：「停下！我来替你答那罗。」"
        "茂师罗说：「停下！你替我答。」",
        "殊胜也像茂师罗那样回答，并说自己" + APART_MOD + "而知道看见——"
        "有灭则寂灭、涅槃。",
        "那罗问：「既然如此，你现在就是漏尽阿罗汉吗？」"
        "殊胜说：「我以正慧如实清楚地看见：有灭则寂灭、涅槃；"
        "但我还不是漏尽阿罗汉。」",
        "「打个比方。旷野路边有一口井，没有绳子也没有罐。"
        "行人又热又渴，绕着井仔细看，如实知道有水，身体却碰不到。"
        "同样，我如实清楚地看见有灭则寂灭、涅槃，自己却还没得到漏尽。」",
        "阿难对那罗说：「殊胜这样说，你怎么看？」"
        "那罗说：「殊胜说得好，我没有别的话，只随喜这份善。」",
        "于是这些正士各自说完，起座离去。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.68（Kosambī）。"
        "信-校正：据 Pāli 补全缘起顺逆问答，及「有灭＝涅槃」而「非漏尽」之井喻；"
        "五离信等＝aññatra saddhāya…diṭṭhinijjhānakkhantiyā。"
        "汉本人物角色（那罗问、茂师罗默、殊胜答喻）与巴利 Saviṭṭha／Musīla／Nārada 对调，"
        "叙事框从汉；法义从 SN。住地从汉「象耳池侧」。"
    ),
}

# --- SA 352 沙门婆罗门（SN 12.14）-------------------------------------------
SUTTAS["SA_352"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「若沙门、婆罗门于诸法不如实知——"
        "法集、法灭、法灭道迹不如实知："
        "彼非真沙门、真婆罗门，亦不得沙门义、婆罗门义，"
        "不能于现法自知作证：" + AWAKEN_LIT,
        "「何法不如实知？谓老死不如实知，老死集、灭、灭道迹不如实知；"
        "生、有、取、爱、受、触、六入处、名色、识、行亦如是——"
        "行集、行灭、行灭道迹不如实知。」",
        "「若如实知诸法及其集、灭、灭道迹："
        "是真沙门、真婆罗门，得沙门义、婆罗门义，"
        "于现法自知作证：" + AWAKEN_LIT,
        "「如实知者：老死及其集、灭、灭道迹；"
        "乃至行及其集、灭、灭道迹。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「若沙门、婆罗门对各种法不能如实了知——"
        "对法的集、灭、灭道也不能如实了知："
        "他们就不是真正的沙门、婆罗门，也得不到沙门义、婆罗门义，"
        "不能在现法中亲自作证：" + AWAKEN_MOD,
        "「什么法不如实了知？就是老死，以及老死的集、灭、灭道；"
        "生、有、取、爱、受、触、六入处、名色、识、行也一样——"
        "对行的集、灭、灭道也不能如实了知。」",
        "「若能如实了知各种法及其集、灭、灭道："
        "才是真正的沙门、婆罗门，得到沙门义、婆罗门义，"
        "在现法中亲自作证：" + AWAKEN_MOD,
        "「如实了知的是：老死及其集、灭、灭道；"
        "乃至行及其集、灭、灭道。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.14（Dutiyasamaṇabrāhmaṇa）。"
        "删汉本「沙门之沙门数」等叠复；四谛式「集／灭／道」贯缘起支。"
    ),
}

# --- SA 353 沙门婆罗门（SN 12.13）-------------------------------------------
SUTTAS["SA_353"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「若沙门、婆罗门于六入处不如实知——"
        "六入处集、灭、灭道迹不如实知："
        "彼非真沙门、真婆罗门，不得沙门义、婆罗门义，"
        "不能现法自知作证：" + AWAKEN_LIT,
        "「于六入处不如实知，而欲于触如实知者，无有是处；"
        "触集、触灭、触灭道迹如实知者，无有是处。"
        "如是受、爱、取、有、生、老死如实知者，亦无有是处。」",
        "「若于六入处如实知，及其集、灭、灭道迹如实知："
        "于触如实知，斯有是处；"
        "如是受、爱、取、有、生、老死如实知，斯有是处。"
        "是则真沙门、真婆罗门，能现法自知作证：" + AWAKEN_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「若沙门、婆罗门对六入处不能如实了知——"
        "对六入处的集、灭、灭道也不能如实了知："
        "他们就不是真正的沙门、婆罗门，得不到沙门义、婆罗门义，"
        "不能在现法中亲自作证：" + AWAKEN_MOD,
        "「对六入处不能如实了知，却想对触如实了知，没有这样的道理；"
        "对触的集、灭、灭道如实了知，也没有这样的道理。"
        "这样，对受、爱、取、有、生、老死如实了知，也没有这样的道理。」",
        "「若对六入处如实了知，也对其集、灭、灭道如实了知："
        "就能对触如实了知，这才有道理；"
        "这样，对受、爱、取、有、生、老死如实了知，也才有道理。"
        "这才是真正的沙门、婆罗门，能在现法中亲自作证：" + AWAKEN_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.13（Samaṇabrāhmaṇa）。"
        "汉本以六入处为门、层层「无有是处／斯有是处」；"
        "巴利作全支列叙；骨从汉之条件链，义与 SN 同属「如实知缘起支」。"
        "底本有漏尽证智定型句，文学栏保留。"
    ),
}

# --- SA 354 沙门婆罗门（SN 12.29 等）---------------------------------------
SUTTAS["SA_354"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「若沙门、婆罗门于六入处不如实知——"
        "而欲超度触者，无有是处；"
        "欲超度触集、触灭、触灭道迹者，无有是处。"
        "如是欲超度受、爱、取、有、生、老死者，无有是处。」",
        "「若于六入处如实知，及其集、灭、灭道迹如实知——"
        "而超度触者，斯有是处；"
        "如是超度受乃至老死及其灭道迹者，斯有是处。」",
        "「如老死乃至六入处，三经如上。如老死乃至行，三经亦如是说。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「若沙门、婆罗门对六入处不能如实了知——"
        "却想超越触，没有这样的道理；"
        "想超越触的集、灭、灭道，也没有这样的道理。"
        "这样，想超越受、爱、取、有、生、老死，也没有这样的道理。」",
        "「若对六入处如实了知，也对其集、灭、灭道如实了知——"
        "才能超越触，这才有道理；"
        "这样，超越受乃至老死及其灭道，也才有道理。」",
        "「如同老死说到六入处，有三经如上。如同老死说到行，也有三经这样说。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.29；并 SN12.30、12.71、12.72–81。"
        "「超度」＝pariññā／完全了知而度；末段 peyyāla 省文如实存，不回填全文。"
    ),
}

# --- SA 355 老死（SN 12.28）-------------------------------------------------
SUTTAS["SA_355"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「当觉知老死，觉知老死集、老死灭、老死灭道迹。"
        "乃至当觉知行，觉知行集、行灭、行灭道迹。」",
        "「云何觉知老死？缘生故有老死——如是觉知老死。"
        "生集是老死集；生灭是老死灭；八圣道是老死灭道迹。」",
        "「云何觉知行？谓三行：身行、口行、意行。"
        "无明集是行集；无明灭是行灭；八圣道是行灭道迹。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「应当觉知老死，觉知老死的集、灭、灭道。"
        "乃至应当觉知行，觉知行的集、灭、灭道。」",
        "「怎样觉知老死？因为有生所以有老死——这样觉知老死。"
        "生集就是老死集；生灭就是老死灭；八圣道就是老死灭道。」",
        "「怎样觉知行？就是三行：身行、口行、意行。"
        "无明集就是行集；无明灭就是行灭；八圣道就是行灭道迹。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.28（Bhikkhu）。"
        "汉本省中间诸支为「乃至」；行＝三行（身口意），集因无明——据 SN／汉共许。"
        "巴利详释老与死之相，汉略，不臆补名相。"
    ),
}

# --- SA 356 种智（SN 12.33）-------------------------------------------------
SUTTAS["SA_356"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「我今说四十四智地。谛听善思。」",
        "「谓缘起十一支，各具四智：知彼法、知彼集、知彼灭、知彼灭道。"
        "自老死至行皆尔——合为四十四智。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「我现在说四十四个智的落点。仔细听，好好想。」",
        "「就是缘起十一支，每一支都有四智：了知那一法、了知它的集、灭、灭道。"
        "从老死一直到行都是这样——合起来四十四智。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.33（Ñāṇavatthu）。"
        "11 支×4（法／集／灭／道）＝44；汉本略列，不演巴利广释。"
    ),
}

# --- SA 357 种智（SN 12.34）-------------------------------------------------
SUTTAS["SA_357"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「有七十七种智。谛听，善思，当为汝说。」",
        "「云何七十七？生缘老死智，及非余缘老死智；"
        "过去生缘老死智，及非余过去缘智；"
        "未来生缘老死智，及非余未来缘智；"
        "复于法住智，知彼亦是无常、有为、心所缘生、尽法、变易法、离欲法、灭法。」",
        "「如是有乃至无明缘行，亦各有现、过、未正缘智与非余缘智，"
        "及于法住智作尽灭断知——是名七十七种智。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「有七十七种智。仔细听，好好想，我为你们说。」",
        "「什么是七十七？知道生是老死之缘，也知道没有生就没有老死；"
        "对过去：知道生是老死之缘，也知道无生则无老死；"
        "对未来：同样如此；"
        "再者，对这法住之智，也知道它本身无常、有为、由心所缘而生，"
        "是尽法、变易法、离欲法、灭法。」",
        "「同样，从有一直到无明缘行，也各有现在、过去、未来的正缘之智与非余缘之智，"
        "并对法住之智作尽灭的了知——这叫做七十七种智。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.34（Dutiyañāṇavatthu）。"
        "信-校正：「非余…缘」＝无彼缘则无果；法住智亦观无常尽灭——"
        "据 SN：even this knowledge of the stability of natural principles is liable to cease。"
        "11×7＝77。非「第一义空」类后出空义。"
    ),
}

# --- SA 358 无明增 → 据 SN 12.37 Natumha 校正 -----------------------------
SUTTAS["SA_358"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「此身非汝所有，亦非余人所有。"
        "当观为故业，由行、思愿所造，是所应受法。」",
        "「多闻圣弟子于缘起善正思惟："
        "此有故彼有，此起故彼起；此无故彼无，此灭故彼灭——"
        + DO_CHAIN_LIT
        + DO_CEASE_LIT
        + "」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「这个身体不是你们的，也不是别人的。"
        "应当看成旧业，由行与思愿所造成，是应当受用的法。」",
        "「多闻圣弟子对缘起善于正确地思维："
        "此有故彼有，此起故彼起；此无故彼无，此灭故彼灭——"
        + DO_CHAIN_MOD
        + DO_CEASE_MOD
        + "」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.37（Natumha）；并 SF162。"
        "据 SN12.37 校正：汉本题「无明增」及「增法／减法」peyyāla 与巴利「非汝所有／故业」异文；"
        "今以 Pāli／Sujato 为准改写，汉本增减法说不取。"
    ),
}

# --- SA 359 思量（SN 12.38 Cetanā 1）---------------------------------------
SUTTAS["SA_359"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「若有思量、有计画，又有使——"
        "则成攀缘，识得住立；识住立增长故，有未来有再生；"
        "有再生故，有未来生老病死忧悲恼苦——如是纯大苦聚集。」",
        "「若不思量、不计画，而犹有使——"
        "亦成攀缘，识得住立；乃至纯大苦聚集，亦复如是。」",
        "「若不思量、不计画、无使——"
        "则无攀缘，识不住立；识不住不增长故，无未来再生；"
        "无再生故，未来生老病死忧悲恼苦灭——如是纯大苦聚灭。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「若有意乐、有计画，又有随眠——"
        "就成了攀缘，识得以住立；识住立增长，就有未来的再生；"
        "有再生，就有未来的生老病死忧悲恼苦——这样纯大苦聚集。」",
        "「若没有意乐、没有计画，但还有随眠——"
        "也成攀缘，识得以住立；乃至纯大苦聚集，也是一样。」",
        "「若没有意乐、没有计画、也没有随眠——"
        "就没有攀缘，识不住立；识不住不增长，就没有未来再生；"
        "没有再生，未来生老病死忧悲恼苦就灭——这样纯大苦聚灭。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.38（Cetanā）。"
        "信-校正：汉本省「不思量而犹有使」中案；据 Pāli 三句补全——"
        "ceteti／pakappeti／anuseti → 思量／计画／使（随眠）。"
        "「攀缘识住」＝consciousness established on a support。"
    ),
}

# --- SA 360 思量（SN 12.39）-------------------------------------------------
SUTTAS["SA_360"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「若有思量、有计画，又有使——"
        "则成攀缘，识得住立；识住立增长故，名色得生；"
        "名色缘六入处，乃至生缘老死忧悲恼苦——如是纯大苦聚集。」",
        "「若不思量、不计画，而犹有使——亦复如是，纯大苦聚集。」",
        "「若不思量、不计画、无使——"
        "则无攀缘，识不住立；名色不生；名色灭则六入处灭，"
        "乃至老死忧悲恼苦灭——如是纯大苦聚灭。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「若有意乐、有计画，又有随眠——"
        "就成了攀缘，识得以住立；识住立增长，名色就会生起；"
        "名色缘六入处，乃至生缘老死忧悲恼苦——这样纯大苦聚集。」",
        "「若没有意乐、没有计画，但还有随眠——也是一样，纯大苦聚集。」",
        "「若没有意乐、没有计画、也没有随眠——"
        "就没有攀缘，识不住立；名色不生；名色灭则六入处灭，"
        "乃至老死忧悲恼苦灭——这样纯大苦聚灭。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.39（Dutiyacetanā）。"
        "与 359 同三句；差别在识住后接入名色及以下缘起链。据 SN 补中案。"
    ),
}

# --- SA 361 思量（SN 12.40）-------------------------------------------------
SUTTAS["SA_361"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「若有思量、有计画，又有使——"
        "则成攀缘，识得住立；识住立增长故，有趣向；"
        "有趣向故，有往来；有往来故，有生死；"
        "有生死故，有未来生老病死忧悲恼苦——如是纯大苦聚集。」",
        "「若不思量、不计画，而犹有使——亦复如是，纯大苦聚集。」",
        "「若不思量、不计画、无使——"
        "则无攀缘，识不住立；无趣向、无往来、无生死；"
        "未来生老病死忧悲恼苦灭——如是纯大苦聚灭。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「若有意乐、有计画，又有随眠——"
        "就成了攀缘，识得以住立；识住立增长，就有趣向；"
        "有趣向就有往来；有往来就有生死；"
        "有生死，就有未来生老病死忧悲恼苦——这样纯大苦聚集。」",
        "「若没有意乐、没有计画，但还有随眠——也是一样，纯大苦聚集。」",
        "「若没有意乐、没有计画、也没有随眠——"
        "就没有攀缘，识不住立；没有趣向、往来、生死；"
        "未来生老病死忧悲恼苦就灭——这样纯大苦聚灭。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.40（Tatiyacetanā）。"
        "nati／āgati-gati／cutūpapāta → 趣向／往来／生死。据 SN 补中案。"
    ),
}

# --- SA 362 多闻（无平行）---------------------------------------------------
SUTTAS["SA_362"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「云何名多闻比丘？如来云何安立？」",
        "诸比丘白佛：「世尊为法根、法眼、法依。唯愿开示，我等当奉行。」",
        "佛言：「闻说老病死，即能生厌、离贪、趣向灭尽——斯名多闻。"
        "闻生乃至行，亦能生厌、离贪、趣向灭尽——如来如是安立多闻比丘。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「怎样叫做多闻比丘？如来怎样安立？」",
        "比丘们说：「世尊是法的根本、眼睛、依止。请开示，我们当奉行。」",
        "佛说：「听闻老病死，就能生厌、离贪、趋向灭尽——这才叫多闻。"
        "听闻生一直到行，也能生厌、离贪、趋向灭尽——如来这样安立多闻比丘。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "「生厌、离贪、向灭尽」＝nibbidā／virāga／nirodha 向；"
        "「离欲」作「离贪」，避「厌故不乐」之误读。confidence=medium。"
    ),
}

# --- SA 363 说法（SN 12.16 说法者分）---------------------------------------
SUTTAS["SA_363"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「云何说法比丘？云何如来施设说法比丘？」",
        "诸比丘白佛：「世尊是法根、法眼、法依。愿说说法比丘，我等当受奉行。」",
        "佛告诸比丘：「若比丘说老病死，为令生厌、离贪、灭尽——是名说法比丘。"
        "如是说生乃至行，为令生厌、离贪、灭尽——是名如来所施设说法比丘。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「什么是说法比丘？如来怎样安立说法比丘？」",
        "比丘们说：「世尊是法根、法眼、法依。请说说法比丘，我们当受奉行。」",
        "佛告诉比丘们：「若比丘宣说老病死，为了令人生厌、离贪、灭尽——这叫说法比丘。"
        "同样，宣说生乃至行，为了令人生厌、离贪、灭尽——"
        "这就是如来所安立的说法比丘。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.16（Dhammakathika）之「说法者」分。"
        "汉分三经（363–365）对巴利一条之三义；本经＝teaches for nibbidā-virāga-nirodha。"
    ),
}

# --- SA 364 次法（SN 12.16 随法行分）---------------------------------------
SUTTAS["SA_364"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「云何名法次法向？」",
        "诸比丘白佛：「世尊是法根、法眼、法依。愿说，我等当受奉行。」",
        "佛告诸比丘：「若比丘于老病死，向于生厌、离贪、灭尽——是名法次法向。"
        "如是于生乃至行，向于生厌、离贪、灭尽——是名如来所施设法次法向。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「什么叫做法次法向？」",
        "比丘们说：「世尊是法根、法眼、法依。请说，我们当受奉行。」",
        "佛告诉比丘们：「若比丘对老病死，趋向生厌、离贪、灭尽——这叫法次法向。"
        "同样，对生乃至行，趋向生厌、离贪、灭尽——"
        "这就是如来所安立的法次法向。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN12.16 之「随法行」分（practices in line with the teaching）。"
        "删卷第十四尾题 paratext。"
    ),
}

# --- SA 365 见法般涅槃（SN 12.16 现法涅槃分）-------------------------------
SUTTAS["SA_365"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「云何见法般涅槃？云何比丘得见法般涅槃？」",
        "诸比丘白佛：「世尊是法根、法眼、法依。愿说，我等当受奉行。」",
        "佛告比丘：「若比丘于老病死，厌故离贪、灭尽，不起诸漏，心善解脱——"
        "是名比丘得见法般涅槃。"
        "如是于生乃至行，厌故离贪、灭尽，不起诸漏，心善解脱——"
        "亦名见法般涅槃。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「什么是见法般涅槃？比丘怎样得见法般涅槃？」",
        "比丘们说：「世尊是法根、法眼、法依。请说，我们当受奉行。」",
        "佛告诉比丘：「若比丘对老病死，因为厌离所以离贪、趋向灭尽，"
        "不起诸漏，内心善解脱——这叫比丘得见法般涅槃。"
        "同样，对生乃至行，厌故离贪、灭尽，不起诸漏，内心善解脱——"
        "也叫做见法般涅槃。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN12.16 之「现法涅槃」分（attained extinguishment in this very life）。"
        "「厌故离贪」＝nibbidā → virāga；不用「厌故不乐」。"
        "删卷第十五序题／译人 paratext。"
    ),
}

# --- SA 366 毗婆尸等（SN 12.4–9）-------------------------------------------
SUTTAS["SA_366"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「毗婆尸佛未成正觉时，独一静处，专精思惟，作是念："
        "『世间入于生死，生已熟坏，灭已复没，而于老死出要不如实知。』」",
        "「即正思惟：『何缘有老死？』得如实智：『有生故有老死，缘生故有老死。』"
        "复观：『何缘有生？』知：『缘有故有生。』"
        "『何缘有有？』知：『缘取故有有。』"
        "『何缘有取？』观见：味著顾念，触爱所增——当知缘爱有取。」",
        "「缘爱取，缘取有，缘有生，缘生老病死忧悲恼苦——"
        "如是纯大苦聚集。灯油炷增则灯常明——广说如前；城譬亦如是。」",
        "「如毗婆尸佛，尸弃、毗湿波浮、迦罗迦孙提、迦那迦牟尼、迦叶佛，皆如是说。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「毗婆尸佛还没有成正觉时，独自在静处专心思维，心想："
        "『世间陷入生死，生了就成熟败坏，灭了又沉没，却对出离老死的道路不能如实了知。』」",
        "「于是正确思维：『什么条件才有老死？』得到如实智："
        "『有生所以有老死，生是老死的缘。』"
        "再观：『什么缘才有生？』知道：『有为缘所以有生。』"
        "『什么缘才有有？』知道：『取为缘所以有有。』"
        "『什么缘才有取？』看见：味著顾念，由触与爱所增长——应当知道爱为缘而有取。」",
        "「缘爱有取，缘取有有，缘有有生，缘生有老病死忧悲恼苦——"
        "这样纯大苦聚集。如同灯加油添炷就一直亮——广说如同从前；城的譬喻也一样。」",
        "「如同毗婆尸佛，尸弃、毗湿波浮、迦罗迦孙提、迦那迦牟尼、迦叶佛，都是这样说。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：primary SN12.4（Vipassī）；并 SN12.5–9。"
        "未觉前逆观缘起；灯譬／城譬及余佛作 peyyāla 省文，如实存。"
        "「无间等」改为「如实智」（yathābhūtañāṇa），避译腔。"
    ),
}

# --- SA 367 修习（SC 列 SN12.83–92；汉义自洽）-----------------------------
SUTTAS["SA_367"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「宜勤修禅，令心内寂。"
        "心寂精勤，则缘起诸法如实证现。」",
        "「所谓老死及其集、灭、道现前；"
        "生乃至行，并彼集、灭、道，亦复现前。"
        "当知此等皆无常、有为、有漏。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「应当努力修禅，让心在内寂静。"
        "内心寂静又精勤，缘起的各种法就会如实显现。」",
        "「也就是老死以及它的集、灭、道呈现在前；"
        "从生一直到行，连同它们的集、灭、道，也呈现在前。"
        "应当知道这些都是无常、有为、有漏。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium：SC 列 SN12.83–92（Satthu 等省文十年），"
        "而汉本为禅思内寂令缘起支如实显现；与巴利「求师以知老死」字面异。"
        "无对齐英译入库，故不硬改作求师义；依汉本早期禅观义雅化。"
    ),
}

# --- SA 368 三摩提 ---------------------------------------------------------
SUTTAS["SA_368"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「当修无量等持，一心系念。"
        "等持成已，缘起支分如实证现。」",
        "「自老死至于行，并知彼无常、有为、有漏。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「应当修无量的等持，一心系念。"
        "等持成就以后，缘起的支分就会如实显现。」",
        "「从老死一直到行，并知道它们无常、有为、有漏。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=medium：同 367，SC 平行为省文十年；"
        "汉本以无量三摩提系念令缘起支显现。依汉本雅化。"
        "「三摩提」作「等持」（samādhi）。"
    ),
}

# --- SA 369 十二因缘（无平行）---------------------------------------------
SUTTAS["SA_369"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时，世尊告诸比丘：「昔毗婆尸佛未成正觉时，住菩提场，不久成佛。"
        "诣菩提树下，敷草为座，结跏趺坐，端身正念，一坐七日，"
        "于十二缘起逆顺观察："
        "此有故彼有，此起故彼起——"
        "缘无明行，乃至缘生有老死，及纯大苦聚集；"
        "纯大苦聚灭。」",
        "「七日已，从定觉，说偈言：」",
        "「『如是诸法生，梵志勤思禅；永离诸疑惑，知因缘生法。"
        "若知因生苦，知诸受灭尽；知因缘法尽，则知有漏尽。"
        "如是诸法生，梵志勤思禅；永离诸疑惑，知有因生苦。"
        "如是诸法生，梵志勤思禅；永离诸疑惑，知诸受灭尽。"
        "如是诸法生，梵志勤思禅；永离诸疑惑，知因缘法尽。"
        "如是诸法生，梵志勤思禅；永离诸疑惑，知尽诸有漏。"
        "如是诸法生，梵志勤思禅；普照诸世间，如日住虚空；"
        "破坏诸魔军，觉诸结解脱。』」",
        "「如毗婆尸佛，尸弃、毗湿波浮、迦罗迦孙提、迦那迦牟尼、迦叶佛，亦如是说。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时，世尊告诉比丘们：「从前毗婆尸佛还没有成正觉时，住在菩提场，不久将成佛。"
        "他走到菩提树下，铺草为座，结跏趺坐，端正身心、安住正念，一坐就是七天，"
        "对十二缘起作逆观、顺观："
        "此有故彼有，此起故彼起——"
        "无明缘行，乃至生缘老死，以及纯大苦聚集；"
        "以及纯大苦聚的灭尽。」",
        "「七天以后，从定中觉醒，说出偈颂：」",
        "「『这些法这样生起，梵志努力禅思；永远离开疑惑，了知因缘所生法。"
        "若知苦由因生，也知各种受灭尽；了知因缘法尽，就知道有漏尽。"
        "这些法这样生起，梵志努力禅思；永远离开疑惑，了知苦有因而生。"
        "这些法这样生起，梵志努力禅思；永远离开疑惑，了知各种受灭尽。"
        "这些法这样生起，梵志努力禅思；永远离开疑惑，了知因缘法尽。"
        "这些法这样生起，梵志努力禅思；永远离开疑惑，了知有漏尽。"
        "这些法这样生起，梵志努力禅思；普照一切世间，如同太阳停在虚空；"
        "摧破各种魔军，觉悟而结缚解脱。』」",
        "「如同毗婆尸佛，尸弃、毗湿波浮、迦罗迦孙提、迦那迦牟尼、迦叶佛，也是这样说。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "七日逆顺观十二支及出定偈；余佛 peyyāla。confidence=medium。"
    ),
}

# --- SA 370 十二因缘（bare 如前广说 → reconstructed）-----------------------
SUTTAS["SA_370"] = {
    "lit": [
        "如是我闻：一时，佛住郁毗罗尼连禅河侧大菩提场，不久当成正觉。",
        "往诣菩提树下，敷草为座，结跏趺坐，端身正念，一坐七日，"
        "于十二缘起逆顺观察："
        "此有故彼有，此起故彼起——"
        "缘无明行，乃至缘生有老死，及纯大苦聚集；纯大苦聚灭。"
        "（底本「如前广说」：出定说偈及余文，依 SA_369 毗婆尸七日观缘起纲要，不演全文。）",
        CLOSE_LIT,
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在郁毗罗、尼连禅河边的大菩提场，不久将成正觉。",
        "他走到菩提树下，铺草为座，结跏趺坐，端正身心、安住正念，一坐七天，"
        "对十二缘起作逆观、顺观："
        "此有故彼有，此起故彼起——"
        "无明缘行，乃至生缘老死，以及纯大苦聚集；以及纯大苦聚的灭尽。"
        "（底本只写「如前广说」：出定说偈等，按 SA_369 的纲要提示，不展开全文。）",
        CLOSE_MOD,
    ],
    "notes": (
        "底本正文核心仅作「正身正念……如前广说」之交叉指示；"
        "无 SC 巴利平行。gold_reconstructed：依 SA_369 七日逆顺观十二缘起纲要补出可读骨架，"
        "住地改为现法世尊之郁毗罗／尼连禅，不演偈颂全文。confidence=low。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_351": "high",
    "SA_352": "high",
    "SA_353": "high",
    "SA_354": "high",
    "SA_355": "high",
    "SA_356": "high",
    "SA_357": "high",
    "SA_358": "high",
    "SA_359": "high",
    "SA_360": "high",
    "SA_361": "high",
    "SA_362": "medium",
    "SA_363": "high",
    "SA_364": "high",
    "SA_365": "high",
    "SA_366": "high",
    "SA_367": "medium",
    "SA_368": "medium",
    "SA_369": "medium",
    "SA_370": "low",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_370": (
        "底本「正身正念……如前广说」为交叉指示，"
        "依 SA_369 七日逆顺观十二缘起纲要补骨架，不演偈颂全文"
    ),
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
    assert set(GOLD) == {f"SA_{i}" for i in range(351, 371)}, (
        "GOLD must cover SA_351–SA_370 exactly"
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

    # Snapshot SA_350 before merge to assert untouched
    sa350_before = None
    for rec in records:
        if rec["id"] == "SA_350":
            sa350_before = json.dumps(
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

    # Assert SA_350 untouched
    for rec in merged:
        if rec["id"] == "SA_350" and sa350_before is not None:
            sa350_after = json.dumps(
                {
                    "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
                    "modern_psychology_text": rec.get("modern_psychology_text"),
                    "notes": rec.get("notes"),
                    "review_status": rec.get("review_status"),
                    "confidence": rec.get("confidence"),
                },
                ensure_ascii=False,
            )
            assert sa350_before == sa350_after, "SA_350 must remain untouched"
            break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa351-370.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fails = [r for r in report if r["status"] == "fail"]
    warns = [r for r in report if r["status"] == "warn"]
    oks = [r for r in report if r["status"] == "ok"]
    forbidden = [r for r in report if r["forbidden_hits"]]
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(1, 371)
    )

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_351–SA_370 only)")
    print(f"validation: ok={len(oks)} warn={len(warns)} fail={len(fails)}")
    print(f"forbidden_hits={len(forbidden)}")
    print(
        f"needs_restyle (assess_gold): {len(needs_restyle)}  "
        f"max_sim={max_r['sim']} ({max_r['id']})  "
        f"mean_sim={round(sum(r['sim'] for r in report) / len(report), 3)}"
    )
    print(f"paragraph_parallel_violations={len(para_bad)}")
    print(f"gold={len(report) - len(recon)} gold_reconstructed={len(recon)}")
    print(f"confidence: {conf_split}")
    print(f"continuous_gold_SA_1–370={continuous}")
    print(f"SA_350_untouched=True")
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
