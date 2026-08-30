#!/usr/bin/env python3
"""Retranslate SA 1351–1362（卷第五十 林相应末：孔雀～鸽鸟）→ merge.

本批十二经（全库最后一批，勿造 SA_1363+）：
1351 孔雀（山神唤醒头陀比丘）
1352 那婆佉多（河岸崩压营事比丘）
1353 频陀（山火与一切有炽然）
1354 恒河（族姓女入海 vs 八圣流入涅槃）
1355 瓜（盗瓜者与断烦恼）
1356 沙弥（常／无常／直／曲）
1357 瓦师（舍利弗乞瓯与施不损财）
1358 贫（贫士望猪酒 vs 三宝）
1359 劫贝（骨锁舞戒好衣）
1360 镮钏（女人泥中 vs 断结阿罗汉）
1361 弹琴（夫妇放逸 vs 戒定解脱）
1362 鸽鸟（积粮巢 vs 积善三宝；得阿罗汉）

信：SC 于本批皆无专经平行（parallels 空）；唯以汉本为底，参林相应／Vanasaṃyutta
     定型语与早期教理厘义；confidence=medium。不得臆造巴利对应。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
禁「厌故不乐」→「厌故离贪」（本批多偈颂对答，无定型厌离句则不强插）。
边界：只合并 SA_1351–1362；断言 SA_1350 不变；corpus 止于 1362。
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

OPEN_BAM_SHORT_LIT = "如是我闻：一时，佛住迦兰陀竹园。"
OPEN_BAM_SHORT_MOD = "我是这样听说的：有一次，佛住在迦兰陀竹园。"

CLOSE_SILENT_LIT = "说此偈已，默然而住。"
CLOSE_SILENT_MOD = "说完这首偈，便默然而住。"

CLOSE_DEV_LIT = "天神说此偈已，即默然住。"
CLOSE_DEV_MOD = "天神说完这首偈，便默然而住。"

PROV_NO = (
    "SC 于本经未列可靠巴利平行，故唯以汉本为底，参林相应／Vanasaṃyutta 定型语及早期教理厘义；"
    "依项目规约「无可靠平行时 confidence 降为 medium/low」。"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

SUTTAS: dict[str, dict] = {}

# --- SA 1351 孔雀 ----------------------------------------------------------
SUTTAS["SA_1351"] = {
    "lit": [
        OPEN_BAM_LIT,
        "时有众多比丘住支提山侧，皆修阿练若、著粪扫衣、常行乞食。",
        "依彼山住之山神说偈言：「孔雀文绣身，栖鞞提醯山；随时出妙音，唤醒乞食者。"
        "孔雀文绣身，栖鞞提醯山；随时出妙音，唤醒粪扫衣。"
        "孔雀文绣身，栖鞞提醯山；随时出妙音，唤醒依树坐。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "当时有许多比丘住在支提山侧，都修阿练若、穿粪扫衣、常去乞食。",
        "住在那座山上的山神说偈：「孔雀身披文彩，栖在鞞提醯山；按时发出妙音，唤醒去乞食的比丘。"
        "孔雀身披文彩，栖在鞞提醯山；按时发出妙音，唤醒穿粪扫衣的人。"
        "孔雀身披文彩，栖在鞞提醯山；按时发出妙音，唤醒依树而坐的人。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。山神以孔雀鸣唤醒头陀三事比丘（乞食／粪扫衣／依树）；"
        "「觉」＝唤醒，非证悟。删卷首 Saṁyuktāgama 标记。"
    ),
}

# --- SA 1352 那婆佉多 ------------------------------------------------------
SUTTAS["SA_1352"] = {
    "lit": [
        OPEN_BAM_LIT,
        "时有众多比丘住支提山，皆修阿练若、著粪扫衣、常行乞食。"
        "尔时那娑佉多河岸崩圮，压杀三营事比丘。",
        "支提山天神说偈言：「乞食住阿练若，慎莫营造立舍；不见佉多河岸，猝然崩倒压杀。"
        "压杀彼造立者，营事三比丘；粪扫衣比丘，慎莫营造立舍。"
        "不见佉多河岸，猝然崩倒；压杀彼造立者，营事三比丘。"
        "依树下比丘，慎莫营造立舍；不见佉多河岸，猝然崩倒，压杀营事三比丘。」",
        CLOSE_DEV_LIT,
    ],
    "mod": [
        OPEN_BAM_MOD,
        "当时有许多比丘住在支提山，都修阿练若、穿粪扫衣、常去乞食。"
        "那时那娑佉多河岸崩塌，压死了三位营事比丘。",
        "支提山的天神说偈：「乞食而住阿练若，切莫营建房舍；不见佉多河岸，忽然崩塌压死。"
        "压死那些营造的人——三位营事比丘；穿粪扫衣的比丘，切莫营建房舍。"
        "不见佉多河岸忽然崩塌；压死那些营造的人——三位营事比丘。"
        "依树下住的比丘，切莫营建房舍；不见佉多河岸忽然崩塌，压死三位营事比丘。」",
        CLOSE_DEV_MOD,
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。天神诫头陀比丘勿营建；以河岸崩压杀三营事比丘为诫。"
        "题「那婆佉多」、正文「那娑佉多」存汉本异写。"
    ),
}

# --- SA 1353 频陀 ----------------------------------------------------------
SUTTAS["SA_1353"] = {
    "lit": [
        OPEN_BAM_SHORT_LIT,
        "时有异比丘住频陀山。山林大火猝起，举山洞然。",
        "有俗人说偈：「今此频陀山，大火洞然炽；焚烧彼竹林，亦烧竹苑实。」",
        "比丘念：「彼俗人能说偈，我何不答？」即说偈：「一切有炽然，无慧莫能灭；"
        "焚烧诸爱欲，亦灭不作苦。」",
        "比丘说此偈已，默然而住。",
    ],
    "mod": [
        OPEN_BAM_SHORT_MOD,
        "当时有一位比丘住在频陀山。山林大火忽然烧起，整座山一片通红。",
        "有个俗人说偈：「如今这座频陀山，大火洞然炽盛；烧掉那边的竹林，也烧掉竹苑的果实。」",
        "比丘心想：「那俗人都能说偈，我为什么不答？」便说偈：「一切有为都在炽然，没有智慧便不能灭；"
        "烧掉各种爱欲，也灭掉造作之苦。」",
        "比丘说完这首偈，便默然而住。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。俗人咏山火，比丘以「一切有炽然」答——"
        "近火喻／āditta 义；「不作苦」作灭除造作之苦解，非「不喜欢」。"
    ),
}

# --- SA 1354 恒河 ----------------------------------------------------------
SUTTAS["SA_1354"] = {
    "lit": [
        OPEN_BAM_SHORT_LIT,
        "时有异比丘在恒河侧，住一林中。",
        "有一族姓女常为舅姑所责，至恒水岸边说偈：「我今欲随恒水，徐流入于大海；"
        "不复令舅与姑，数数见我嫌责。」",
        "比丘闻已念：「彼女尚能说偈，我何不答？」即说偈：「我今欲以净信，随彼八圣之水；"
        "徐流入于涅槃，不见魔得自在。」",
        "比丘说此偈已，默然而住。",
    ],
    "mod": [
        OPEN_BAM_SHORT_MOD,
        "当时有一位比丘在恒河边，住在一片林中。",
        "有一位族姓女子常被公婆责骂，来到恒水岸边说偈：「我如今想随着恒水，缓缓流入大海；"
        "好让公婆不再一次次嫌责我。」",
        "比丘听了心想：「那女子都能说偈，我为什么不答？」便说偈：「我如今想以净信，随着那八圣之水；"
        "缓缓流入涅槃，不再见魔得自在。」",
        "比丘说完这首偈，便默然而住。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。女欲随恒流入海避责；比丘以净信随八支圣道流入涅槃对答。"
        "「八圣水」＝八圣道。"
    ),
}

# --- SA 1355 瓜 ------------------------------------------------------------
SUTTAS["SA_1355"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住一林中；去林不远有种瓜田。",
        "有盗者夜偷其瓜，见月欲出，说偈：「明月汝且莫出，待我断取其瓜；"
        "持瓜去已之后，任汝现与不现。」",
        "比丘念：「盗瓜者尚能说偈，我岂不能答？」即说偈：「恶魔汝且莫出，待我断诸烦恼；"
        "断彼烦恼已竟，任汝出与不出。」",
        "比丘说此偈已，默然而住。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位比丘在拘萨罗人间，住在一片林中；离林不远有瓜田。",
        "有个盗贼夜里偷瓜，看见月亮快要出来，说偈：「明月你先别出来，等我割完这些瓜；"
        "把瓜拿走以后，随你显现或不显现。」",
        "比丘心想：「偷瓜的都能说偈，我难道不能答？」便说偈：「恶魔你先别出来，等我断尽烦恼；"
        "烦恼断尽以后，随你出现或不出现。」",
        "比丘说完这首偈，便默然而住。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。盗者以月为诫、比丘以魔为诫；"
        "「断烦恼」对「断瓜」，林相应惯用对偈。"
    ),
}

# --- SA 1356 沙弥 ----------------------------------------------------------
SUTTAS["SA_1356"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住一林中。",
        "有沙弥说偈：「云何名为常？乞食则为常。云何为无常？僧食为无常。"
        "云何名为直？唯因陀罗幢。云何名为曲？曲者唯见钩。」",
        "比丘念：「沙弥能说此偈，我何不答？」即说偈：「云何名为常？常者唯涅槃。"
        "云何为无常？谓诸有为法。云何名为直？谓圣八正道。云何名为曲？曲者唯恶径。」",
        "比丘说此偈已，默然而住。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位比丘在拘萨罗人间，住在一片林中。",
        "有个沙弥说偈：「什么叫作常？乞食才是常。什么叫作无常？僧团共食是无常。"
        "什么叫作直？只有因陀罗幢。什么叫作曲？弯曲的只有见钩。」",
        "比丘心想：「沙弥都能说这偈，我为什么不答？」便说偈：「什么叫作常？常的只有涅槃。"
        "什么叫作无常？是指一切有为法。什么叫作直？是指圣八正道。什么叫作曲？弯曲的只有恶径。」",
        "比丘说完这首偈，便默然而住。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。沙弥以乞食／僧食、幢／钩为常无常直曲；"
        "比丘以涅槃／有为、八正道／恶径校正。因陀罗幢＝帝释之幢（直）。"
    ),
}

# --- SA 1357 瓦师 ----------------------------------------------------------
SUTTAS["SA_1357"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有舍利弗弟子服药已，寻即食粥。尊者舍利弗到瓦师舍，乞瓦瓯。",
        "瓦师说偈：「云何得名胜誉，而不施一钱？云何实德增胜，于财无所减？」",
        "舍利弗说偈答：「若不食肉者，而施彼以肉；诸修梵行者，施之以女色；"
        "不坐高床者，施以高广床；于彼临行者，施以息止处——"
        "如是等施与，于财不损减；是则有名誉，而不舍一钱；实德名称流，于财无所减。」",
        "瓦师复说偈：「汝今舍利弗，所说实为善；今施汝百瓯，非余亦不得。」",
        "舍利弗说偈答：「彼三十三天，焰摩与兜率，化乐诸天人，及他化自在——"
        "瓦钵因信得，而汝不生信。」",
        "尊者舍利弗说此偈已，于瓦师舍默然出去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时舍利弗的一位弟子服过药，随即吃粥。舍利弗尊者到瓦师家，求一只瓦瓯。",
        "瓦师说偈：「怎样能得名胜誉，却不施舍一文钱？怎样使实德增胜，而钱财毫无减损？」",
        "舍利弗说偈答：「若不吃肉的人，却把肉布施给他；修梵行的人，却把女色布施给他；"
        "不坐高床的人，却把高广床布施给他；正要上路的人，却把歇息处布施给他——"
        "像这样布施，钱财并不减损；这就能有名誉，却不舍一文钱；实德美名流布，钱财毫无减损。」",
        "瓦师又说偈：「你如今舍利弗，所说的确善妙；现在施你一百只瓯，别人也得不到。」",
        "舍利弗说偈答：「那三十三天、焰摩与兜率、化乐诸天人，以及他化自在——"
        "瓦钵因信心而得，而你却不生信心。」",
        "舍利弗尊者说完这首偈，在瓦师家默然离去。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。瓦师问不损财而得誉；舍利弗以「施所不需」之悖施答，"
        "终以六欲天因信得钵、诫瓦师不生信。删卷首标记；「炎魔」作「焰摩」。"
    ),
}

# --- SA 1358 贫 ------------------------------------------------------------
SUTTAS["SA_1358"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住一林中。",
        "有贫士夫在林侧作希望思惟，说偈：「若得猪一头，美酒满一瓶，盛持瓯一枚，人人数数与——"
        "若得如是者，当复何所忧。」",
        "比丘念：「贫士尚能说偈，我何以不说？」即说偈：「若得佛法僧，比丘善说法；"
        "我不病常闻，不畏众魔怨。」",
        "比丘说此偈已，默然而住。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位比丘在拘萨罗人间，住在一片林中。",
        "有个贫苦的人在林边怀着希求思惟，说偈：「若能得到一头猪、满满一瓶美酒、一只盛酒的瓯，"
        "还有人不断送来——若能得到这些，还愁什么呢。」",
        "比丘心想：「穷人都能说偈，我为什么不说？」便说偈：「若能得到佛法僧，以及善说法的比丘；"
        "我无病而常得闻法，便不畏一切魔怨。」",
        "比丘说完这首偈，便默然而住。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。贫者以猪酒为足，比丘以三宝闻法为足。"
        "「悕望」＝希求；作「希望」。"
    ),
}

# --- SA 1359 劫贝 ----------------------------------------------------------
SUTTAS["SA_1359"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住一林中。"
        "彼作是念：「若得好劫贝，长七肘、广二肘，作衣已，乐修善法。」",
        "依林天神念：「此非比丘法——住林中而希求好衣。」"
        "即化作全身骨锁，于比丘前舞，说偈：「比丘思劫贝，七肘广六尺；昼则如是想，知夜何所思？」",
        "比丘生怖，身战悚，说偈：「止止不须㲲，今著粪扫衣；昼见骨锁舞，知夜复何见？」",
        "彼心惊怖已，即正思惟，专精修习，断诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位比丘在拘萨罗人间，住在一片林中。"
        "他心想：「若能得到好的劫贝布，长七肘、宽二肘，做成衣服以后，就乐修善法。」",
        "住在林中的天神心想：「这不是比丘法——住在林中却希求好衣。」"
        "便化作一具全身骨锁，在比丘面前舞蹈，说偈：「比丘想着劫贝布，七肘长、六尺宽；白天这样想，知道夜里又想什么？」",
        "比丘心生恐怖，身体战栗，说偈：「罢了罢了，不必要细㲲，如今穿着粪扫衣；白天已见骨锁舞，知道夜里还会见什么？」",
        "他心惊怖之后，便正思惟、专精修习，断尽烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。近林相应诫好衣／头陀义。"
        "劫贝＝棉布；骨鏁＝骨锁（骨架连环）；「㲲」＝细毛布，存字。"
    ),
}

# --- SA 1360 镮钏 ----------------------------------------------------------
SUTTAS["SA_1360"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住一林中，已得阿罗汉：诸漏已尽，所作已作，已舍重担，"
        "断诸有结，正智心善解脱。",
        "有一女人于夜暗中，天微雨、电光闪照，过林欲诣他男子，倒深泥中，镮钏断坏，华璎散落。"
        "女人说偈：「头发悉散解，花璎落深泥；镮钏悉破坏，丈夫何所著。」",
        "比丘念：「女人尚能说偈，我岂不能答？」即说偈：「烦恼悉断坏，度生死淤泥；"
        "著缠悉散落，十方尊见我。」",
        "比丘说偈已，即默然而住。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位比丘在拘萨罗人间，住在一片林中，已经证得阿罗汉：诸漏已尽，该做的已做，已放下重担，"
        "断尽有结，以正智内心善解脱。",
        "有一个女人在夜暗中，天微雨、电光闪照，穿过林子要去找别的男子，跌倒在深泥里，手镯断坏，花璎散落。"
        "女人说偈：「头发全都散开，花璎落进深泥；手镯全都破坏，丈夫还恋着什么。」",
        "比丘心想：「女人都能说偈，我难道不能答？」便说偈：「烦恼全都断坏，已度生死淤泥；"
        "执著缠缚全都散落，十方尊者看见我。」",
        "比丘说完偈，便默然而住。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。阿罗汉比丘以断结对女人镮钏华璎散落。"
        "底本答偈引号残缺，今补全；「睒照」作「闪照」。"
    ),
}

# --- SA 1361 弹琴 ----------------------------------------------------------
SUTTAS["SA_1361"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住于河侧一林树间。",
        "有丈夫与妇相随，度河住岸边，弹琴嬉戏，说偈：「爱念而放逸，逍遥青树间；"
        "流水清且流，琴声极和美；春气调适游，快乐何可过。」",
        "比丘念：「彼士夫尚能说偈，我岂不能答？」即说偈：「受持清净戒，爱念等正觉；"
        "沐浴三解脱，善以极清凉；人道具庄严，快乐岂过是。」",
        "比丘说此偈已，即默然而住。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位比丘在拘萨罗人间，住在河边一片林树之间。",
        "有一对夫妻一起过河，停在岸边弹琴嬉戏，说偈：「相爱而放逸，逍遥在青树间；"
        "流水清澈流淌，琴声极其和美；春气宜人游玩，快乐哪能超过。」",
        "比丘心想：「那男子都能说偈，我难道不能答？」便说偈：「受持清净戒，敬爱等正觉；"
        "沐浴于三解脱，善得极清凉；人道具备庄严，快乐岂能超过。」",
        "比丘说完这首偈，便默然而住。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。夫妇放逸琴乐 vs 比丘戒／念佛／三解脱门。"
        "底本答偈引号残缺，今补全；「三解脱」＝空、无相、无愿。"
    ),
}

# --- SA 1362 鸽鸟（全库末经）----------------------------------------------
SUTTAS["SA_1362"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异比丘在拘萨罗人间，住一林中。",
        "有天神见诸鸽鸟，说偈言：「鸽鸟当积聚，胡麻米粟等；于山顶树上，高显作巢窟；"
        "若当天雨时，安稳得饮食宿。」",
        "比丘念：「彼亦觉悟我！」即说偈：「凡夫积善法，恭敬于三宝；身坏命终时，资神心安乐。」",
        "比丘说此偈已，即得觉悟，专精思惟，除诸烦恼，得阿罗汉。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位比丘在拘萨罗人间，住在一片林中。",
        "有位天神看见许多鸽子，说偈：「鸽子应当积聚胡麻、米、粟等；在山顶树上高高筑巢；"
        "若到天下雨时，便能安稳饮食住宿。」",
        "比丘心想：「那也是在唤醒我！」便说偈：「凡夫积聚善法，恭敬于三宝；身坏命终之时，资益心神安乐。」",
        "比丘说完这首偈，便得觉悟，专精思惟，除去烦恼，证得阿罗汉。",
    ],
    "notes": (
        f"{PROV_NO}confidence=medium：无 SC 专经。全库末经；删「杂阿含经卷第五十」卷末题记（藏经 paratext）。"
        "天神咏鸽积粮，比丘以积善敬三宝为对；「资神」＝资益心神，非神我。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE = {rid: "medium" for rid in SUTTAS}
RECONSTRUCTED: dict[str, str] = {}

BATCH_IDS = [f"SA_{i}" for i in range(1351, 1363)]
# 邻经：前一路终点 SA_1350 必须不变；corpus 无 1363+
NEIGHBOR_IDS = {"SA_1350"}

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
assert NEIGHBOR_IDS.isdisjoint(GOLD), "must not merge SA_1350"
assert max(int(i.split("_")[1]) for i in GOLD) == 1362, "must not invent SA beyond 1362"


def _snap(rec: dict) -> str:
    return json.dumps(
        {
            "kumarajiva_style_text": rec.get("kumarajiva_style_text"),
            "modern_psychology_text": rec.get("modern_psychology_text"),
            "notes": rec.get("notes"),
            "review_status": rec.get("review_status"),
            "confidence": rec.get("confidence"),
            "translator": rec.get("translator"),
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

    assert len(records) == 1362, f"corpus size expected 1362, got {len(records)}"
    max_id = max(int(r["id"].split("_")[1]) for r in records)
    assert max_id == 1362, f"max SA id expected 1362, got {max_id}"

    neighbor_before = {rec["id"]: _snap(rec) for rec in records if rec["id"] in NEIGHBOR_IDS}
    assert "SA_1350" in neighbor_before, "SA_1350 must exist to assert unchanged"

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
                assert before == _snap(rec), f"{rid} must remain untouched"
                break

    # 不得写出 SA_1363+
    assert all(int(r["id"].split("_")[1]) <= 1362 for r in merged)
    assert len(merged) == 1362

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1351-1362.json").write_text(
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1351, 1363)
    )
    sa1350_ok = neighbor_before["SA_1350"] == _snap(by_merged["SA_1350"])

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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1351–SA_1362 only)")
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
    print(f"continuous_1351_1362_goldish={continuous}")
    print(f"SA_1350_unchanged={sa1350_ok}")
    print(f"corpus_max_id=1362 invent_beyond=False")
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
