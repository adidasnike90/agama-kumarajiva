#!/usr/bin/env python3
"""Retranslate SA 1191–1210（梵天相应末＋比丘尼相应＋婆耆舍三经）→ merge.

本批二十经：
1191–1197 梵天相应（空闲处 SN6.13、集会 SN1.37、瞿迦黎 SN6.7、
         梵天 SN6.6、婆迦梵 SN6.4、邪见 SN6.5、入灭 SN6.15）
1198–1207 比丘尼相应（旷野 SN5.1 … 动头 SN5.8）
1208–1210 婆耆舍赞偈（揭伽他 SN8.11、憍陈如 SN8.9、舍利弗 SN8.6）

信：有 SN 平行者据巴利／Sujato 厘义；汉本拙译／错名／窜入异经据平行校正。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
厌故离贪：生厌→离贪→解脱（禁「厌故不乐」）。
边界：只合并 SA_1191–1210；断言 SA_1190／SA_1211 关键字段不变。
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

OPEN_CAMP_LIT = "如是我闻：一时，佛住瞻婆国揭伽池侧。"
OPEN_CAMP_MOD = "我是这样听说的：有一次，佛住在瞻婆国揭伽池边。"

VANISH_LIT = "魔波旬念：「比丘尼已知我。」忧愁不乐，即没不现。"
VANISH_MOD = "魔波旬心想：「比丘尼已经认出我。」忧愁不乐，随即隐没不见。"

PROV = (
    "本经 SC 平行表所列平行及 `raw_aligned_data.json` 内之巴利本文、Sujato 英译并用以厘定法义；"
    "求那跋陀罗汉本用于定位经文与传统术语。"
)

SUTTAS: dict[str, dict] = {}

# --- SA 1191 空闲处（SN6.13 Andhakavinda）---------------------------------
SUTTAS["SA_1191"] = {
    "lit": [
        "如是我闻：一时，佛住摩揭陀安陀迦频陀。时世尊于闇夜露地而坐，天微雨。"
        "娑婆主梵天沙婆钵底夜已深，放光照遍安陀迦频陀，来诣佛所，稽首一面立，说偈：",
        "「当习近空闲边林床座，为求解脱诸结缚；"
        "若于彼处不得乐，当住僧中自护念。"
        "家家行乞护诸根，警觉正念而乞食；"
        "当习近空闲床座，离怖于无畏中解脱。"
        "恶蛇出没、电光雷震，闇夜之中；"
        "比丘坐彼，身毛不竖。"
        "此我亲见，非传闻说：于一梵行中，"
        "有千人已胜死魔；学人五百有余，"
        "又十十之十，皆须陀洹，不趣畜生。"
        "其余有分于福者，我不能数，恐成妄说。」",
        "梵天说已，欢喜随喜，即没不现。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在摩揭陀的安陀迦频陀。那时佛在黑夜里露地而坐，天正下着细雨。"
        "娑婆世界主梵天沙婆钵底夜已深，放出光明照遍安陀迦频陀，来到佛前，顶礼后站在一边，说偈：",
        "「应当常去空闲偏僻的住处，为了从结缚中解脱；"
        "若在那里找不到喜乐，就住在僧团中自我守护、保持正念。"
        "挨家挨户乞食，守护诸根，警觉而正念；"
        "应当常去空闲住处，脱离怖畏，在无畏中得解脱。"
        "恶蛇出没、电闪雷鸣的黑夜里；"
        "比丘坐在那里，毫毛也不竖起。"
        "这是我亲眼所见，不是道听途说：在同一份梵行之中，"
        "就有上千人征服了死神；学人五百有余，"
        "再加上十个十个的十，都是须陀洹，不再堕畜生。"
        "其余分有福德的人，我无法计数，怕说错了。」",
        "梵天说完，欢喜随喜，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN6.13 Andhakavindasutta。"
        "据 SN 校正：住处摩揭陀安陀迦频陀（汉作拘萨罗空闲）；夜雨露地；"
        "偈「僧中自护」「千人胜死」「须陀洹数」从巴利；删汉「乃至不究竟」等赘。"
    ),
}

# --- SA 1192 集会（SN1.37 Samaya；亦近 DN20 首）---------------------------
SUTTAS["SA_1192"] = {
    "lit": [
        "如是我闻：一时，佛住释氏迦毘罗卫大林中，与五百比丘俱，皆是阿罗汉。"
        "十方世界诸天大多来集，欲见世尊及比丘僧。",
        "时有四净居天作是念：「佛在大林与五百罗汉俱，十方诸天来集。"
        "我等亦可各说一偈赞之。」譬如力士屈伸臂顷，从净居没，现于佛前，稽首一面立。",
        "第一说偈：「大林中大集会，天众皆来集；"
        "我等来此法会，瞻礼难胜之僧。」",
        "第二说偈：「诸比丘心专定，自心正直已；"
        "如善御执缰，智者守护诸根。」",
        "第三说偈：「已断桩与门闩，拔因陀罗柱而不动；"
        "清净无垢而游行，明眼所调之大龙。」",
        "第四说偈：「归依佛者，终不堕恶趣；"
        "舍此人身后，当满诸天众。」",
        "四天说已，即没不现。",
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在释迦族迦毘罗卫的大森林里，和五百比丘在一起，都是阿罗汉。"
        "十方世界的多数天神都来集会，想见世尊和比丘僧。",
        "当时有四位净居天这样想：「佛在大森林里和五百罗汉在一起，十方诸天来集会。"
        "我们也可以每人说一首偈来赞叹。」就像力士一伸一屈手臂那样快，他们从净居天隐没，出现在佛前，顶礼后站在一边。",
        "第一位说偈：「大森林里有大集会，天众都来了；"
        "我们来到这法会，瞻仰那不可战胜的僧团。」",
        "第二位说偈：「比丘们心专一入定，已经把自己的心调直；"
        "像善御者握住缰绳，有智慧的人守护诸根。」",
        "第三位说偈：「已经砍断木桩和门闩，拔掉因陀罗柱而不动摇；"
        "清净无垢地游行，是明眼者所调伏的大龙。」",
        "第四位说偈：「归依佛的人，终不会堕入恶趣；"
        "舍弃这人身之后，将充实天众。」",
        "四位天神说完，随即隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN1.37 Samayasutta（亦近 DN20 Mahāsamaya 首分）。"
        "据 SN：说偈者为净居天（suddhāvāsa），非汉「四梵天王」；"
        "第二偈「执缰护根」、第三「桩／闩／因陀罗柱」从巴利校正汉「消融恩爱刺」。"
    ),
}

# --- SA 1193 瞿迦黎（SN6.7 Kokālika）--------------------------------------
SUTTAS["SA_1193"] = {
    "lit": [
        OPEN_BAM_LIT,
        "时世尊昼日宴坐。有别梵天子梵、净居别梵，各依门柱而立。"
        "子梵即于佛前，就瞿迦梨比丘说偈：",
        "「欲以有量测无量，智者岂作此计量？"
        "量彼不可量者，我观彼是覆障凡夫。」",
        "（汉本广说：娑婆主梵天以世尊宴坐故，入提婆达多党瞿迦梨房，扣户告言："
        "「于舍利弗、目连当起净信，莫长夜得不饶益。」瞿迦梨反诘梵天既得阿那含何故来；"
        "梵天谓「不可治」，说上偈已，往白世尊；佛印可之。）",
        "佛告梵天：「如是。于不可量处而欲筹量，是阴盖凡夫。」",
        "梵天闻已，欢喜随喜，作礼即没。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "那时佛白天在静坐。有独立梵天子梵和净居独立梵，各自靠着门柱站立。"
        "子梵就在佛前，针对瞿迦梨比丘说偈：",
        "「想用有限的尺度去量那不可量的，有智慧的人怎么会这样计量？"
        "去量那不可量者的人，我认为他是被障覆的凡夫。」",
        "（汉译本写得更细：娑婆世界主梵天因为世尊在静坐，便走进提婆达多一党瞿迦梨的房，敲门告诉他："
        "「对舍利弗、目连应当起清净信心，不要长夜受苦。」瞿迦梨反问梵天既已证阿那含为什么还来；"
        "梵天觉得「不可救药」，说了上面的偈，再去禀告世尊；佛加以印可。）",
        "佛对梵天说：「正是这样。在不可量处却想去筹量，那是被盖障的凡夫。」",
        "梵天听完，欢喜随喜，作礼后隐没不见。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN6.7 Kokālikasutta（SC 亦列 SN6.8／6.9 相近）。"
        "据 SN 核心偈：不可量而欲量＝覆障凡夫；汉入房对话保留为平行叙事，义不违。"
    ),
}

# --- SA 1194 梵天（SN6.6 Brahmaloka）--------------------------------------
SUTTAS["SA_1194"] = {
    "lit": [
        OPEN_JET_LIT,
        "时世尊昼日宴坐。别梵天子梵与净居别梵各依门立。"
        "子梵语净居：「今非时见佛；某梵世丰乐，而彼梵天住于放逸。当往警策。」",
        "即于佛前没，现彼梵世。彼梵遥见，问：「从何处来？」"
        "答：「从阿罗汉正等觉世尊所来。汝何不往承事？」",
        "彼梵不纳，化作千身夸神通。子梵化二千身，言：「佛神通过于我等，当往承事。」",
        "彼梵说偈：「三金翅、四鹄、五百虎鹰禅者；"
        "此宫殿炽然，照北方。」",
        "子梵答：「纵宫殿炽照北方，智者见色中有恼、常颤，"
        "是故慧者不乐于色。」",
        "二梵警策已即没。其后彼梵乃往承事世尊。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时佛白天在静坐。独立梵天子梵和净居独立梵各自靠门站着。"
        "子梵对净居说：「现在不是见佛的时候；某梵世很繁荣，可那里的梵天住在放逸里。我们应当去警策他。」",
        "他们就在佛前隐没，出现在那个梵世。那位梵天远远看见，问：「你们从哪里来？」"
        "答：「从阿罗汉、正等觉世尊那里来。你为什么不去承事他？」",
        "那位梵天不接受，化作一千个身体夸耀神通。子梵化作两千个身体，说：「佛的神通超过我们，你应当去承事。」",
        "那位梵天说偈：「有三百金翅、四百天鹅、五百只入禅的虎鹰；"
        "这座宫殿烧着光，照亮北方。」",
        "子梵答：「即使宫殿烧着光照亮北方，有智慧的人看见色里有恼害、常常颤动，"
        "因此有慧的人不在色上取乐。」",
        "两位梵天警策完毕就隐没了。后来那位梵天才去承事世尊。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN6.6 Brahmalokasutta。"
        "据 SN 全幅重写：放逸梵天夸宫殿／神通，子梵以「色中有恼」折之；"
        "汉末窜入「迦吒务陀低沙／谤圣地狱」偈属 SN6.9 系，不取（gold_reconstructed）。"
    ),
}

# --- SA 1195 婆迦梵（SN6.4 Baka）------------------------------------------
SUTTAS["SA_1195"] = {
    "lit": [
        OPEN_JET_LIT,
        "时婆迦梵天起恶邪见：「此处常、恒、永恒、纯一、不堕法；"
        "不生不老不死、不出不生，更无过此之出离。」",
        "世尊知彼心念，如力士屈伸臂顷，于祇桓没，现彼梵世。"
        "婆迦遥见，言：「善来！此处常恒……更无出离。」",
        "佛言：「异哉婆迦！无明所覆。实无常而言常，实有出离而言无。」",
        "婆迦说偈：「七十二作福者，得自在，已过生老；"
        "此为梵之最后有，众人皆归仰。」",
        "佛答：「此寿极短，非长；尼罗浮陀百千之寿，我悉知之，而汝自谓长存。」",
        "婆迦请说昔所修戒业。佛次第记：旷野饥众以慈救度；"
        "村邑为贼所掠而救护；恒河恶龙捉船而以力解脱——"
        "「此汝往昔戒行，我忆之如眠起。」",
        "婆迦信佛知己寿及余事，叹为正觉。世尊为种种说法示教照喜已，还祇桓。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时婆迦梵天生起邪恶见：「这里是常的、恒的、永恒的、完整的、不会堕落的；"
        "不生、不老、不死、不迁、不再生，再也没有比这更高的出离。」",
        "世尊知道他的心思，像力士一伸一屈手臂那样快，从祇树给孤独园隐没，出现在那个梵世。"
        "婆迦远远看见，说：「欢迎！这里是常恒……再也没有出离。」",
        "佛说：「可叹啊婆迦！被无明所覆。其实是无常却说常，其实另有出离却说没有。」",
        "婆迦说偈：「我们七十二位作福者，已得自在，度过了生老；"
        "这是梵天最后一次受生，许多人都来归仰。」",
        "佛答：「这里的寿命其实很短，并不长；尼罗浮陀狱百千倍的寿命我都知道，而你却自以为长存。」",
        "婆迦请佛说出他从前修过的戒行。佛依次记起：在旷野里以慈心救济饥渴大众；"
        "解救被强盗掠走的村邑；在恒河里以神力救出被恶龙抓住的船——"
        "「这是你往昔的戒行，我记得像从睡眠中醒来一样清楚。」",
        "婆迦相信佛知道自己的寿命和其他事，赞叹这才是正觉。世尊为他种种说法开示鼓励后，回到祇园。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN6.4 Bakabrahmasutta。"
        "据 SN：邪见五支（常／恒／永恒／纯一／不堕）及「更无出离」；"
        "佛责无明；三则往昔戒业（饥众／掠村／龙船）从巴利；住处从 SN 作祇园。"
    ),
}

# --- SA 1196 邪见（SN6.5 Aññatarabrahma）----------------------------------
SUTTAS["SA_1196"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有一梵天起恶见：「无有沙门、婆罗门能来至此。」",
        "世尊知已，如力士屈伸臂顷，现彼梵世，于彼梵天上虚空结跏趺坐，入火界定。",
        "大目犍连以天眼见佛，亦没祇桓而现梵世，于东方、佛座之下空中入火界定。"
        "摩诃迦叶现南方；摩诃劫宾那现西方；阿那律现北方：皆在佛下，入火界定。",
        "目犍连说偈问梵天：「汝昔邪见今犹在否？见梵世有光明过其上否？」"
        "梵天答：「彼见已舍；我见光明过梵世。今日岂可言我常恒？」",
        "世尊警策已还祇桓。梵天问目犍连：「世尊余弟子亦有如是大德大力否？」"
        "目犍连说偈：「具三明、观他心、漏尽阿罗汉，其数无量。」"
        "即为说法示教照喜已，还舍卫。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时有一位梵天生起邪见：「没有沙门或婆罗门能来到这里。」",
        "世尊知道后，像力士一伸一屈手臂那样快，出现在那个梵世，在梵天上方虚空中结跏趺坐，进入火界定。",
        "大目犍连用天眼看见佛，也从祇园隐没出现在梵世，在东方、比佛更低的空中进入火界定。"
        "摩诃迦叶出现在南方；摩诃劫宾那在西方；阿那律在北方：都在佛的下方，进入火界定。",
        "目犍连用偈问梵天：「你从前的邪见现在还在吗？看见有光明超过梵世了吗？」"
        "梵天答：「那个见已经舍了；我看见光明超过梵世。今天怎么还能说我常恒？」",
        "世尊警策完毕回到祇园。梵天问目犍连：「世尊其余弟子也有这样的大德大力吗？」"
        "目犍连说偈：「具足三明、能观他心、漏尽的阿罗汉，数目多得无法计量。」"
        "于是为他说法开示鼓励后，回到舍卫。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN6.5 Aññatarabrahmasutta。"
        "据 SN 校正弟子：目犍连／迦叶／劫宾那／阿那律四方侍坐入火界（汉作憍陈如／舍利弗等）；"
        "邪见核心为「无能至此」；偈问见从巴利。"
    ),
}

# --- SA 1197 入灭（SN6.15 Parinibbāna）------------------------------------
SUTTAS["SA_1197"] = {
    "lit": [
        "如是我闻：一时，佛住拘尸那竭力士生地、坚固双树间，临般涅槃。"
        "告诸比丘：「诸行是灭法，当勤精进。」——此如来最后教诫。",
        "世尊顺次入初禅乃至灭想受定，复顺次还出，至四禅已，即于中夜无余涅槃而般涅槃。",
        "般涅槃时，娑婆主梵天说偈：「世间有情皆当舍此身聚；"
        "如是无等大师，如来力具足，正觉已入灭。」",
        "释提桓因说偈：「诸行无常，是生灭法；生已还灭，寂灭为乐。」",
        "阿难说偈：「尔时大恐怖，令人身毛竖；众相具足之正觉，今已般涅槃。」",
        "阿那律说偈：「出息入息已止，心住不动；"
        "明眼者依寂静而入灭。心不懈怠，忍受诸受；"
        "心解脱如灯尽。」",
    ],
    "mod": [
        "我是这样听说的：有一次，佛住在拘尸那竭力士的生地、两棵坚固树之间，即将般涅槃。"
        "告诉比丘们：「诸行是会灭尽的法，你们应当勤奋。」——这是如来最后的教诫。",
        "世尊依次进入初禅一直到灭受想定，再依次退出来，到第四禅之后，就在中夜于无余涅槃中般涅槃。",
        "般涅槃时，娑婆世界主梵天说偈：「世间有情都终须放下这身躯；"
        "这样无比的大师，如来力具足，正觉者已经入灭。」",
        "帝释说偈：「诸行都是无常的，本质是生起又坏灭；生起之后灭去，它们的平息才是安乐。」",
        "阿难说偈：「那时多么恐怖，令人毛发竖起；具足一切殊胜之相的正觉者，如今已经般涅槃。」",
        "阿那律说偈：「出息入息已经停止，心安住不动；"
        "明眼者依于寂静而入灭。心不退缩，安忍各种感受；"
        "心的解脱如同灯火熄灭。」",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN6.15 Parinibbānasutta。"
        "据 SN：最后教诫 appamāda；禅定上下出入后入灭；偈序梵天→帝释→阿难→阿那律；"
        "汉「双树生花／七日焚身」等属广本涅槃叙事，略从 SN 梵天相应短经。"
    ),
}

# --- 比丘尼相应共用入林框 -----------------------------------------------
_BHIKKHUNI_GO_LIT = (
    "时{name}比丘尼晨朝著衣持钵，入舍卫城乞食；食已还，洗足已，"
    "持坐具入安陀林，于树下入昼正受。"
)
_BHIKKHUNI_GO_MOD = (
    "那时{name}比丘尼清晨穿衣持钵，进城乞食；吃完回来，洗脚后，"
    "拿着坐具进入安陀林，在树下作日中禅。"
)
_MARA_APPROACH_LIT = (
    "魔波旬欲令生怖、退失禅定，化作端正年少，来至其所，说偈："
)
_MARA_APPROACH_MOD = (
    "魔波旬想让她恐惧、退失禅定，就化作端正少年，来到她面前，说偈："
)
_KNOW_LIT = "比丘尼念：「此必恶魔欲乱我。」知已，以偈答："
_KNOW_MOD = "比丘尼心想：「这一定是恶魔想来扰乱我。」知道以后，用偈回答："

# --- SA 1198 旷野（SN5.1 Āḷavikā）-----------------------------------------
SUTTAS["SA_1198"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="阿臈毘"),
        _MARA_APPROACH_LIT,
        "「世间无出要，空闲何所为？当受五欲乐，莫令后变悔。」",
        _KNOW_LIT,
        "「世间有出要，我以慧亲证；放逸亲族之恶魔，汝不知彼道。"
        "诸欲如剑矛，诸阴是砧板；汝所说欲乐，于我是苦、是不乐。"
        "舍诸喜乐，破无明蕴；以灭尽作证，安住离诸漏。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="阿臈毘"),
        _MARA_APPROACH_MOD,
        "「世间没有出离，空闲处能做什么？应当享受五欲之乐，别让以后后悔。」",
        _KNOW_MOD,
        "「世间有出离，我以智慧亲自证得；放逸者的亲族——恶魔啊，你不知道那条道。"
        "欲乐像剑和矛，诸阴就是砧板；你所说的欲乐，对我来说是苦、是不可乐的。"
        "舍弃各种喜乐，破开无明之蕴；以灭尽作为证验，安住而离开诸漏。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.1 Āḷavikāsutta。"
        "据 SN：魔劝受欲／无出要；尼答有出要、欲如剑矛、阴如砧板；"
        "「不乐」对 arati，不作「厌故不乐」。"
    ),
}

# --- SA 1199 素弥（SN5.2 Somā）--------------------------------------------
SUTTAS["SA_1199"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="苏摩"),
        _MARA_APPROACH_LIT,
        "「仙人所到境，甚难可企及；二指之智，女人所不能到。」",
        _KNOW_LIT,
        "「心善等持时，女形复何为？智生正观法，女身何所碍。"
        "若作男女想，或计我是谁，乃是魔所应说。已离爱苦，安住漏尽。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="苏摩"),
        _MARA_APPROACH_MOD,
        "「仙人才能到达的境界，非常难以企及；凭着两指宽的智慧，女人是到不了的。」",
        _KNOW_MOD,
        "「当心善加等持时，女身的形相又能怎样？智慧生起、正确观察法时，女身有什么障碍。"
        "若还想着『我是女』『我是男』，或计着『我是什么』，那才是魔该说的话。已离开爱苦，安住漏尽。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.2 Somāsutta。"
        "据 SN：魔以「女智浅」讥；尼答心定智生则女形无碍，取男女想者乃魔可乘。"
    ),
}

# --- SA 1200 瞿昙弥（SN5.3 Kisāgotamī）------------------------------------
SUTTAS["SA_1200"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="吉离舍瞿昙弥"),
        _MARA_APPROACH_LIT,
        "「汝丧子而泣耶？独坐林中，岂求男子？」",
        _KNOW_LIT,
        "「丧子之边已度，男子之边亦尽；我不忧不哭，亦不畏汝。"
        "一切处喜已灭，无明蕴已破；摧死军队，已离爱苦，安住无漏。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="吉离舍瞿昙弥"),
        _MARA_APPROACH_MOD,
        "「你是丧子才哭泣吗？独自坐在林中，难道是在找男人？」",
        _KNOW_MOD,
        "「丧子的边际我已经度过，男人的边际也已到头；我不忧愁不哭泣，也不怕你。"
        "一切处的喜乐已经灭尽，无明之蕴已经打破；我摧破了死神的军队，已离爱苦，安住而无漏。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.3 Kisāgotamīsutta。"
        "据 SN：魔讥丧子求男；尼答已度丧子／男子边，喜灭、破无明、胜死军。"
    ),
}

# --- SA 1201 莲华（SN5.5 Uppalavaṇṇā）-------------------------------------
SUTTAS["SA_1201"] = {
    "lit": [
        OPEN_JET_LIT,
        "时优钵罗色比丘尼晨朝著衣持钵乞食已，入安陀林，立一盛花坚固树下入定。",
        _MARA_APPROACH_LIT,
        "「妙花树下独住，美色无等侣；痴人，不畏恶徒耶？」",
        _KNOW_LIT,
        "「纵百千恶徒来，我毛亦不竖、亦不怖；独处亦不畏汝。"
        "我能隐没，或入汝腹，或住两眉间——汝犹不见。"
        "心已自在，神足善修，一切缚已解，不畏于汝。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时优钵罗色比丘尼清晨穿衣持钵乞食回来，进入安陀林，站在一棵开满花的坚固树下入定。",
        _MARA_APPROACH_MOD,
        "「你来到开满花的树下独自站着，美色没有第二人；傻姑娘，不怕恶徒吗？」",
        _KNOW_MOD,
        "「即使有十万个像你这样的恶徒来，我毫毛也不动、也不惊慌；独自一人也不怕你。"
        "我能够隐没，或者进入你肚子，或者站在两眉之间——你仍然看不见我。"
        "我的心已经自在，神足善加修习，一切束缚都解开了，不怕你。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.5 Uppalavaṇṇāsutta。"
        "据 SN：魔以独美恐吓；尼答神通自在、入腹／眉间不可见；删汉赘「吐三垢」定型尾。"
    ),
}

# --- SA 1202 石室（SN5.10 Vajirā；汉名讹）---------------------------------
SUTTAS["SA_1202"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="跋耆罗"),
        _MARA_APPROACH_LIT,
        "「众生云何造？作者为谁？何处生？何处灭？」",
        _KNOW_LIT,
        "「汝谓有众生，此是恶见；唯是空行聚，此处无众生可得。"
        "如聚材成车，世名为车；诸阴和合，假名众生。"
        "唯苦生、住、灭；离苦无另有生灭。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="跋耆罗"),
        _MARA_APPROACH_MOD,
        "「这个众生是谁造的？作者在哪里？众生从哪里生起？又在哪里灭去？」",
        _KNOW_MOD,
        "「你以为真有『众生』，这是恶见；这里只是空的行聚，找不到众生。"
        "如同部件组装起来，世俗就叫做『车』；诸阴和合时，假名叫做『众生』。"
        "只是苦在生起、停留、灭去；离开苦，没有别的生灭。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.10 Vajirāsutta。"
        "据 SN：车喻／行聚无众生／唯苦生灭；尼名据 Vajirā＝跋耆罗"
        "（汉题「石室」、文作「尸罗」皆讹；石室义近 Selā＝下经）。"
    ),
}

# --- SA 1203 鼻黎（SN5.9 Selā）--------------------------------------------
SUTTAS["SA_1203"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="洗罗"),
        _MARA_APPROACH_LIT,
        "「此形谁所造？作者为谁？何处起？何处灭？」",
        _KNOW_LIT,
        "「此形非自作，亦非他作；依因缘生，因灭则灭。"
        "如种子依地味与湿润而抽芽；阴、界、六处亦依因生，因坏则灭。已离爱苦，安住漏尽。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="洗罗"),
        _MARA_APPROACH_MOD,
        "「这个形体是谁造的？作者在哪里？从哪里生起？在哪里灭去？」",
        _KNOW_MOD,
        "「这个形体不是自己造的，也不是别人造的；依因缘而生，因坏就灭。"
        "如同种子依靠土地的养分和湿润而发芽；阴、界、六处也是依因而生，因坏就灭。已离开爱苦，安住漏尽。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.9 Selāsutta。"
        "据 SN：bimba 非自／他作，因缘生灭；种子喻；阴界入。"
        "尼名据 Selā＝洗罗（汉「毘罗／鼻黎」音讹）。"
    ),
}

# --- SA 1204 毘阇（SN5.4 Vijayā）------------------------------------------
SUTTAS["SA_1204"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="毘阇耶"),
        _MARA_APPROACH_LIT,
        "「汝少我亦少，当共五伎乐；何用禅思为？」",
        _KNOW_LIT,
        "「色声香味触可意者，尽付于汝，非我所须。"
        "此腐朽坏身，我厌患之，欲爱已拔。"
        "色界有情、无色住者、及诸寂定——一切处闇已破。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="毘阇耶"),
        _MARA_APPROACH_MOD,
        "「你年轻我也年轻，一起享受五支伎乐吧；禅思有什么用？」",
        _KNOW_MOD,
        "「色、声、香、味、触这些可意的，全部交还给你，不是我所要的。"
        "这个会腐烂败坏的身体，我厌患它，欲爱已经拔除。"
        "住于色界的、住于无色的、以及各种寂静定——在这一切上，黑暗都已打破。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.4 Vijayāsutta。"
        "据 SN：魔劝五伎乐；尼付还五欲、厌此坏身、欲爱已拔；"
        "「厌患」对 aṭṭīyāmi／harāyāmi，生厌故离贪。"
    ),
}

# --- SA 1205 折罗（SN5.6 Cālā）--------------------------------------------
SUTTAS["SA_1205"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="遮罗"),
        "魔波旬来问：「比丘尼！汝不乐何等？」答：「我不乐于生。」",
        "魔说偈：「生则受诸欲；谁教汝不乐生？」",
        _KNOW_LIT,
        "「生则有死，生则触诸苦——缚、杀、恼害；是故不乐生。"
        "佛说超越生之法，为断一切苦，安我于谛。"
        "色界、无色有情不了知灭，还来受后有。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="遮罗"),
        "魔波旬前来问：「比丘尼！你不喜欢什么？」答：「我不乐于受生。」",
        "魔说偈：「生了就能享受诸欲；谁教你不乐于生？」",
        _KNOW_MOD,
        "「有生就有死，生了就会碰到种种苦——捆绑、杀害、恼害；所以不乐于生。"
        "佛说了超越受生的法，为了断尽一切苦，把我安住在真理上。"
        "色界和无色界的有情不了知灭，还会再来受后有。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.6 Cālāsutta。"
        "据 SN：不乐于生（na jātiṃ rocemi）；生则死／苦故生厌；"
        "超越生、安于谛；不了灭则还受有——厌故离贪，不作「厌故不乐」套语。"
    ),
}

# --- SA 1206 优婆折罗（SN5.7 Upacālā）-------------------------------------
SUTTAS["SA_1206"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="优波遮罗"),
        "魔问：「欲生于何处？」答：「我无处欲生。」",
        "魔说偈：「三十三、炎摩、兜率、化乐、他化自在——愿生当受乐。」",
        _KNOW_LIT,
        "「彼诸天为欲缚所缚，还堕魔境界。"
        "一切世间苦火炽然、烟起、燃烧、动摇；"
        "不动不燃、非凡夫所习、魔所不至处——我心乐彼。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="优波遮罗"),
        "魔问：「你想生在哪里？」答：「我哪里都不想生。」",
        "魔说偈：「三十三天、炎摩、兜率、化乐、他化自在——把心愿放在那里，就会受乐。」",
        _KNOW_MOD,
        "「那些天都被欲的束缚绑着，还会再落入魔的范围。"
        "一切世间苦火在燃烧、冒烟、起火、动摇；"
        "那不动不燃、不是凡夫常去、魔到不了的地方——我的心乐于那里。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.7 Upacālāsutta。"
        "据 SN：无处欲生；五欲天仍为欲缚、随魔；乐魔所不至之不动处。"
    ),
}

# --- SA 1207 动头（SN5.8 Sīsupacālā）--------------------------------------
SUTTAS["SA_1207"] = {
    "lit": [
        OPEN_JET_LIT,
        _BHIKKHUNI_GO_LIT.format(name="尸利沙遮罗"),
        "魔问：「汝乐何等外道？」答：「我都不乐。」",
        "魔说偈：「依谁剃发作沙门相？不乐诸道，岂非愚痴游行？」",
        _KNOW_LIT,
        "「此外诸道耽诸见，于法不巧；我不乐彼法。"
        "有释种所生无等佛，伏一切、破魔、无处败；"
        "解脱无著，明眼见一切，尽诸业、灭诸依而得解脱——"
        "彼是我师，我乐彼教。」",
        VANISH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        _BHIKKHUNI_GO_MOD.format(name="尸利沙遮罗"),
        "魔问：「你喜欢哪一家外道？」答：「我哪一家都不喜欢。」",
        "魔说偈：「你依仗谁剃了头发、作出沙门的样子？却不喜欢各家外道，岂不是愚痴地游行？」",
        _KNOW_MOD,
        "「这以外的各道都沉溺在种种见里，不精通法；我不喜欢他们的法。"
        "有一位出生在释迦族的无等佛，战胜一切、摧破魔军、无处被打败；"
        "解脱而无执著，明眼看见一切，到达一切业的尽、依着灭尽而得解脱——"
        "他是我的老师，我喜欢他的教法。」",
        VANISH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN5.8 Sīsupacālāsutta。"
        "据 SN：不乐外道见；唯乐释种佛之教——伏魔、明眼、业尽依灭。"
    ),
}

# --- SA 1208 揭伽他（SN8.11 Gaggarā）--------------------------------------
SUTTAS["SA_1208"] = {
    "lit": [
        OPEN_CAMP_LIT,
        "时世尊与大众俱，色声名称皆最胜。尊者婆耆舍念：「当于佛前以月譬赞之。」"
        "即从座起，偏袒合掌白言：「世尊！欲有所说。善逝！欲有所说。」"
        "佛言：「欲说者便说。」",
        "即说偈：「如月停虚空，离云翳而净照；"
        "如是央耆罗大牟尼，名称光耀遍世间。」",
        "诸比丘闻已，皆大欢喜。",
    ],
    "mod": [
        OPEN_CAMP_MOD,
        "那时世尊和大众在一起，容色与名称都最为殊胜。尊者婆耆舍心想：「应当在佛前用月亮的比喻来赞叹。」"
        "就从座位起来，偏袒右肩合掌说：「世尊！我想说几句。善逝！我想说几句。」"
        "佛说：「想说就说吧。」",
        "便说偈：「如同月亮停在虚空，离开云翳而洁净照耀；"
        "像这样，央耆罗大牟尼，您的名称光耀遍及整个世间。」",
        "比丘们听了，都大为欢喜。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN8.11 Gaggarāsutta。"
        "据 SN：佛于大众中色声最胜；婆耆舍月／日无垢喻赞 Aṅgīrasa；汉「十五布萨月初」略从 SN。"
    ),
}

# --- SA 1209 憍陈如（SN8.9 Koṇḍañña）--------------------------------------
SUTTAS["SA_1209"] = {
    "lit": [
        OPEN_BAM_LIT,
        "时尊者阿若憍陈如久别后来诣佛所，以头面触佛足，口称：「憍陈如！憍陈如！」",
        "会中婆耆舍念：「当于佛前以上座譬赞之。」起白佛欲说；佛听许。",
        "即说偈：「佛后觉之上座憍陈如，精进猛利；"
        "空闲阿练若中常得远离乐住。声闻所应、依师教者，彼皆已得，不放逸而学。"
        "大德力、三明、他心智明了；憍陈如——佛法之继承者，头面礼师足。」",
        "诸比丘闻已，皆大欢喜。",
    ],
    "mod": [
        OPEN_BAM_MOD,
        "那时尊者阿若憍陈如经过很久才来到佛那里，用头面触佛的脚，口称：「憍陈如！憍陈如！」",
        "会中的婆耆舍心想：「应当在佛前用上座的方式来赞叹他。」起身向佛请求许可；佛允许了。",
        "便说偈：「佛之后觉悟的上座憍陈如，精进猛利；"
        "在空闲阿练若中常常得到远离的安乐住。声闻所应证、依从师教的，他都已得到，不放逸地修学。"
        "有大威德、三明、善于了知他心；憍陈如——佛法的继承者，头面顶礼老师的脚。」",
        "比丘们听了，都大为欢喜。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN8.9 Koṇḍaññasutta。"
        "据 SN：住处竹园；久别触足自报姓名；偈「佛后觉／常得远离乐／三明他心／佛继承者」；"
        "汉作揭伽池侧，从 SN 改正。"
    ),
}

# --- SA 1210 舍利弗（SN8.6 Sāriputta）------------------------------------
SUTTAS["SA_1210"] = {
    "lit": [
        OPEN_JET_LIT,
        "时尊者舍利弗于堂上为诸比丘说法：言辞善练、明了、畅达、能显义；"
        "诸比丘专心侧听。",
        "婆耆舍念当面前赞之，起白舍利弗欲说；舍利弗听许。",
        "即说偈：「深慧聪敏，善知道非道；大慧舍利弗，为比丘说法。"
        "或略或广；如鹦鹉声，辩才流出。"
        "说时闻其美声——可意、清澈、柔和；诸比丘心喜，倾耳而听。」",
        "诸比丘闻已，皆大欢喜。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时尊者舍利弗在堂上为比丘们说法：言辞熟练、清楚、流畅、能把义理说明白；"
        "比丘们都专心侧耳听着。",
        "婆耆舍心想应当当面赞叹，起身向舍利弗请求；舍利弗答应了。",
        "便说偈：「智慧深、聪明，善于知道什么是道、什么不是道；大智慧的舍利弗，为比丘说法。"
        "有时简略，有时详细；像鹦鹉的叫声，辩才涌流出来。"
        "说法时人们听他甜美的声音——可意、清澈、柔和；比丘们心里欢喜，侧耳倾听。」",
        "比丘们听了，都大为欢喜。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN8.6 Sāriputtasutta。"
        "据 SN：住处祇园（汉作揭伽池侧，改正）；略广说法、鹦鹉声喻、美声倾耳从巴利。"
    ),
}

# ---------------------------------------------------------------------------
CONFIDENCE = {
    "SA_1191": "high",
    "SA_1192": "high",
    "SA_1193": "high",
    "SA_1194": "high",
    "SA_1195": "high",
    "SA_1196": "high",
    "SA_1197": "high",
    "SA_1198": "high",
    "SA_1199": "high",
    "SA_1200": "high",
    "SA_1201": "high",
    "SA_1202": "high",
    "SA_1203": "high",
    "SA_1204": "high",
    "SA_1205": "high",
    "SA_1206": "high",
    "SA_1207": "high",
    "SA_1208": "high",
    "SA_1209": "high",
    "SA_1210": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_1191": "汉拘萨罗空闲→SN6.13 摩揭陀安陀迦频陀＋夜雨露地偈序。",
    "SA_1192": "汉「四梵天」→SN1.37 四净居天；偈据巴利护根／桩闩校正。",
    "SA_1194": "删汉窜入谤圣地狱偈（属 Kokālika 系）；据 SN6.6 放逸梵天／色中有恼重写。",
    "SA_1196": "四方弟子据 SN 目犍连／迦叶／劫宾那／阿那律（汉憍陈如／舍利弗等）。",
    "SA_1197": "据 SN6.15 最后教诫＋禅顺逆出入；偈序梵→释→阿难→阿那律；略汉焚身广叙。",
    "SA_1202": "尼名据 SN Vajirā＝跋耆罗（汉尸罗／石室讹）；车喻／唯苦从巴利。",
    "SA_1209": "住处据 SN 竹园（汉揭伽池）；偈「佛后觉／佛法继承者」从巴利。",
    "SA_1210": "住处据 SN 祇园（汉揭伽池）；鹦鹉声／略广从巴利。",
}

OWN_STATUSES = {"gold", "gold_reconstructed", "needs_doctrine_check", "needs_restyle"}

BATCH_IDS = [f"SA_{i}" for i in range(1191, 1211)]
NEIGHBOR_IDS = {"SA_1190", "SA_1211"}

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
assert NEIGHBOR_IDS.isdisjoint(GOLD), "neighbors must not be in GOLD"


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

    neighbor_before = {
        rec["id"]: _snap(rec) for rec in records if rec["id"] in NEIGHBOR_IDS
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
                assert before == _snap(rec), f"{rid} (neighbor) must remain untouched"
                break

    assert NEIGHBOR_IDS.isdisjoint(GOLD), "neighbors must not be in GOLD"

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa1191-1210.json").write_text(
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish for i in range(1191, 1211)
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_1191–SA_1210 only)")
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
    print(f"continuous_1191_1210_goldish={continuous}")
    print(f"SA_1190_untouched={'SA_1190' in neighbor_before}")
    print(f"SA_1211_untouched={'SA_1211' in neighbor_before}")
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
