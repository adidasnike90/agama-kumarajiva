#!/usr/bin/env python3
"""Retranslate SA 871–890（天相应末–修证相应）→ merge.

本批二十经：
871–872 天相应末（风云天 SN32.1 resembling；伞盖覆灯，无专平行）
873–890 修证相应起：
  873 四调伏 AN4.7｜874 三种子 Iti74
  875–879 四正断 AN4.13／SN49／AN4.14
  880–882 不放逸（四禅依；peyyāla 譬喻串）
  883 四种禅 SN34（三昧／正受矩阵）
  884–886 三明 AN3.58–59
  887–889 信／增益／等起（名字义，无专平行）
  890 无为法 SN43.11

信：有 AN／Iti／SN 者以巴利为准；peyyāla／「如上说」补纲 → gold_reconstructed。
达雅：白话与罗什风逐段对照；sim 门限见 assess_gold。
边界：只合并 SA_871–890；不触碰 SA_851–870、SA_891+；
      若 SA_870 已为 gold／gold_reconstructed，则断言其不变。
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

CLOSE_AN_LIT = "佛说此经已，尊者阿难闻佛所说，欢喜奉行。"
CLOSE_AN_MOD = "佛说完这部经，尊者阿难听佛所说，都欢喜奉行。"

EIGHT_LIT = "正见、正志、正语、正业、正命、正精进、正念、正定"
EIGHT_MOD = "正见、正志、正语、正业、正命、正精进、正念、正定"

FOUR_PADHANA_BODY_LIT = (
    "已起恶不善法断，生欲、精进、发勤、策心、持心；"
    "未起恶不善法不起，生欲、精进、发勤、策心、持心；"
    "未生善法令生，生欲、精进、发勤、策心、持心；"
    "已生善法令住不忘、修习增广，生欲、精进、发勤、策心、持心"
)
FOUR_PADHANA_BODY_MOD = (
    "已生起的恶不善法要断除，生起欲乐、精进、发动、策心、持心；"
    "尚未生起的恶不善法使它不生，生起欲乐、精进、发动、策心、持心；"
    "尚未生起的善法使它生起，生起欲乐、精进、发动、策心、持心；"
    "已生起的善法使它安住不忘、修习增长，生起欲乐、精进、发动、策心、持心"
)

# 不放逸根本定型（补「如上说，乃至涅槃」）
APPAMADA_CORE_LIT = (
    "皆依不放逸为根本，不放逸集、不放逸生、不放逸转；"
    "比丘不放逸者，能修诸善，乃至出要、远离、涅槃"
)
APPAMADA_CORE_MOD = (
    "都依不放逸为根本，由不放逸而集、而生、而转；"
    "比丘若不放逸，就能修习种种善法，一直到出要、远离、涅槃"
)

APPAMADA_TAIL_LIT = f"如是一切善法，{APPAMADA_CORE_LIT}。"
APPAMADA_TAIL_MOD = f"同样，一切善法，{APPAMADA_CORE_MOD}。"

THREE_VIJJA_LIT = (
    "无学宿命智证明、无学生死智证明、无学漏尽智证明"
)
THREE_VIJJA_MOD = (
    "无学的宿命智证明、无学的生死智证明、无学的漏尽智证明"
)

# 三明广说（据 AN3.58–59／SA_885）
VIJJA_PUBBE_LIT = (
    "云何无学宿命智证明？圣弟子知种种宿命：一生、百生、千生、百千生，"
    "乃至多劫成坏，我及有情曾如是名、如是生、如是种姓、如是食、"
    "如是苦乐、如是寿量；于此处死、余处生，于余处死、此处生——"
    "如是种种宿命皆悉了知，是名宿命智证明。"
)
VIJJA_PUBBE_MOD = (
    "什么是无学宿命智证明？圣弟子了知种种宿命：一生、百生、千生、百千生，"
    "乃至许多劫的成坏，自己和有情曾经有这样的名字、出身、种姓、食物、"
    "苦乐、寿量；在这里死、到别处生，在别处死、到这里生——"
    "这样种种宿命都如实了知，叫做宿命智证明。"
)

VIJJA_CUTA_LIT = (
    "云何无学生死智证明？圣弟子天眼净过人眼，见有情死时、生时，"
    "好色、恶色，胜、劣，趣善趣、趣恶趣，随业受生如实知："
    "此众生成就身口意恶行，谤毁圣人，邪见受邪法，身坏命终生恶趣泥犁；"
    "此众生成就身口意善行，不谤圣人，正见成就，身坏命终生善趣天、人中——"
    "是名生死智证明。"
)
VIJJA_CUTA_MOD = (
    "什么是无学生死智证明？圣弟子天眼清净，超过人眼，见有情死时、生时，"
    "好色、恶色，胜、劣，趣向善趣或恶趣，随业受生而如实了知："
    "这类众生成就身口意恶行，谤毁圣人，邪见受持邪法，身坏命终生恶趣地狱；"
    "这类众生成就身口意善行，不谤圣人，正见成就，身坏命终生善趣天、人中——"
    "叫做生死智证明。"
)

VIJJA_ASAVA_LIT = (
    "云何无学漏尽智证明？圣弟子如实知此是苦、此是苦集、此是苦灭、此是苦灭道迹；"
    "如是知、如是见已，欲漏、有漏、无明漏心解脱，解脱知见生："
    "『我生已尽，梵行已立，所作已作，自知不受后有。』是名漏尽智证明。"
)
VIJJA_ASAVA_MOD = (
    "什么是无学漏尽智证明？圣弟子如实知道这是苦、这是苦集、这是苦灭、这是苦灭道迹；"
    "这样知、这样见之后，欲漏、有漏、无明漏的心解脱，生起解脱知见："
    "『我生已尽，梵行已立，所作已作，自己知道不再受后有。』叫做漏尽智证明。"
)

VIJJA_GATHA_LIT = (
    "尔时世尊说偈言：\n"
    "「观察知宿命，见有情趣生，\n"
    "　诸漏皆永尽，是则牟尼明。\n"
    "　心得善解脱，远离诸贪爱，\n"
    "　三明悉通达，故说为三明。」"
)
VIJJA_GATHA_MOD = (
    "那时世尊说偈：\n"
    "「观察知宿命，见有情趣生，\n"
    "　诸漏皆永尽，是则牟尼明。\n"
    "　心得善解脱，远离诸贪爱，\n"
    "　三明悉通达，故说为三明。」"
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

# --- SA 871 风云天（SN32.1 resembling）---------------------------------------
SUTTAS["SA_871"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有风云天作是念：『我今欲以神通游戏。』"
        "如是念时，风云则起。如风云天，焰电天、雷震天、雨天、晴天、寒天、热天，亦复如是。」",
        CLOSE_BH_LIT,
        "如是说已，若异比丘问佛、佛问诸比丘，亦如是说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有风云天这样想：『我现在要以神通游戏。』"
        "这样一想，风云就生起。如同风云天，焰电天、雷震天、雨天、晴天、寒天、热天，也是这样。」",
        CLOSE_BH_MOD,
        "这样说完，如果有别的比丘问佛、或佛问比丘们，也是这样说。",
    ],
    "notes": (
        f"{PROV}confidence=medium：SC 标 SN32.1 resembling——"
        "巴利列寒／热／云／风／雨等云天众名，汉本则述诸天欲以神通游戏而感起风云等；"
        "叙事从汉，类属从 SN 云天相应。神力→神通。"
    ),
}

# --- SA 872 伞盖覆灯（无专平行）---------------------------------------------
SUTTAS["SA_872"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊于夜暗中，天时小雨，电光焰照。佛告阿难：「可以伞盖覆灯，持以随行。」",
        "尊者阿难受教，以伞盖覆灯，随佛后行。至一处，世尊微笑。"
        "阿难白佛：「世尊不以无因缘而笑；不審今日何因缘而发微笑？」",
        "佛告阿难：「如是！如来不以无因缘而笑。"
        "汝今持伞盖覆灯随我而行；我见梵天亦复如是，持伞盖覆灯，随拘邻比丘后行；"
        "帝释亦持伞盖覆灯，随摩诃迦叶后行；"
        "持国天王亦持伞盖覆灯，随舍利弗后行；"
        "增长天王亦持伞盖覆灯，随大目犍连后行；"
        "广目天王亦持伞盖覆灯，随摩诃拘絺罗后行；"
        "多闻天王亦持伞盖覆灯，随摩诃劫宾那后行。」",
        CLOSE_AN_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊在夜暗中，天正下着小雨，电光闪耀。佛告诉阿难：「可以用伞盖罩住灯，拿着跟随。」",
        "尊者阿难受教，用伞盖罩住灯，跟在佛后面走。到了一处，世尊微笑。"
        "阿难对佛说：「世尊不会无因无缘而笑；请问今天是什么因缘而发微笑？」",
        "佛告诉阿难：「是的！如来不会无因无缘而笑。"
        "你现在拿着伞盖罩灯跟着我走；我看见梵天也是这样，拿着伞盖罩灯，跟在拘邻比丘后面；"
        "帝释也拿着伞盖罩灯，跟在摩诃迦叶后面；"
        "持国天王也拿着伞盖罩灯，跟在舍利弗后面；"
        "增长天王也拿着伞盖罩灯，跟在大目犍连后面；"
        "广目天王也拿着伞盖罩灯，跟在摩诃拘絺罗后面；"
        "多闻天王也拿着伞盖罩灯，跟在摩诃劫宾那后面。」",
        CLOSE_AN_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：天王名据通例作持国／增长／广目／多闻"
        "（汉本袟栗帝罗色吒罗等音译压缩）；拘隣→拘邻，大目揵连→大目犍连。"
    ),
}

# --- SA 873 四调伏（AN4.7 Sobhana）-------------------------------------------
SUTTAS["SA_873"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四种善调伏众，能庄严僧伽。何等为四？"
        "比丘善调伏、比丘尼善调伏、优婆塞善调伏、优婆夷善调伏——"
        "聪明无畏、多闻持法、行法次法向，是名四众，能令僧伽光显。」",
        "尔时世尊说偈言：\n"
        "「才辩且无畏，多闻能持法，\n"
        "　行法次法向，是则僧中好。\n"
        "　比丘持净戒，比丘尼多闻，\n"
        "　信士与信女，净信亦复然；\n"
        "　如是名善众，如日能自照。」",
        CLOSE_BH_LIT,
        "如调伏，辩才、柔和、无畏、多闻、通达法、能说法、法次法向、随顺法行，亦如是说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四种善加调伏的众，能够庄严僧伽。哪四种？"
        "比丘善调伏、比丘尼善调伏、优婆塞善调伏、优婆夷善调伏——"
        "聪明无畏、多闻持法、依照法而实行法，叫做四众，能使僧伽光显。」",
        "那时世尊说偈：\n"
        "「才辩且无畏，多闻能持法，\n"
        "　行法次法向，是则僧中好。\n"
        "　比丘持净戒，比丘尼多闻，\n"
        "　信士与信女，净信亦复然；\n"
        "　如是名善众，如日能自照。」",
        CLOSE_BH_MOD,
        "如同「调伏」这样说，辩才、柔和、无畏、多闻、通达法、能说法、法次法向、随顺法行，也是这样说。",
    ],
    "notes": (
        f"{PROV}confidence=high：平行 AN4.7 Sobhana；"
        "据巴利校正：vinītā／viyattā／visāradā／bahussutā／dhammadharā／"
        "dhammānudhammappaṭipannā → 善调伏、聪明无畏、多闻持法、行法次法向；"
        "saṅghaṁ sobhenti → 庄严／光显僧伽（汉「善众」「日光自照」保留）。"
        "末 peyyāla 异门从汉。"
    ),
}

# --- SA 874 三种子（Iti74）----------------------------------------------------
SUTTAS["SA_874"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有三种子。何等为三？随生子、胜生子、下生子。"
        "云何随生子？父母不杀、不盗、不邪淫、不妄语、不饮酒，子亦随学，是名随生子。"
        "云何胜生子？父母不受此五戒，子能受持，是名胜生子。"
        "云何下生子？父母受持五戒，子不能受，是名下生子。」",
        "尔时世尊说偈言：\n"
        "「随生与胜生，智父之所欲；\n"
        "　下生非所愿，不能绍继故。\n"
        "　为人法之子，当为优婆塞；\n"
        "　于佛法僧宝，勤修清净心；\n"
        "　云除月光显，光荣及眷属。」",
        CLOSE_BH_LIT,
        "如五戒，信、戒、施、闻、慧，亦如是说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有三种孩子。哪三种？随生子、胜生子、下生子。"
        "什么是随生子？父母不杀、不盗、不邪淫、不妄语、不饮酒，孩子也跟着学，叫做随生子。"
        "什么是胜生子？父母不受持这五戒，孩子却能受持，叫做胜生子。"
        "什么是下生子？父母受持五戒，孩子却不能受，叫做下生子。」",
        "那时世尊说偈：\n"
        "「随生与胜生，智父之所欲；\n"
        "　下生非所愿，不能绍继故。\n"
        "　为人法之子，当为优婆塞；\n"
        "　于佛法僧宝，勤修清净心；\n"
        "　云除月光显，光荣及眷属。」",
        CLOSE_BH_MOD,
        "如同就五戒这样说，就信、戒、施、闻、慧，也是这样说。",
    ],
    "notes": (
        f"{PROV}confidence=high：平行 Iti74；"
        "三种子＝与父母同等／胜过／不及（atijāta／anujāta／avajāta 义）；"
        "五戒条从汉；末「信戒施闻慧」peyyāla 从汉。婬→邪淫。"
    ),
}

# --- SA 875 四正断（略，AN4.13／SN49）---------------------------------------
SUTTAS["SA_875"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「当知有四种正断：一断断，二律仪断，三随护断，四修断。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「应当知道有四种正断：一是断断，二是律仪断，三是随护断，四是修断。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：平行 AN4.13／SN49 四正勤名目略说；"
        "名相从汉传统（断断／律仪断／随护断／修断），广释见 SA_877–879。"
    ),
}

# --- SA 876 四正断＋偈-------------------------------------------------------
SUTTAS["SA_876"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「当知有四种正断：一断断，二律仪断，三随护断，四修断。」",
        "尔时世尊说偈言：\n"
        "「断断与律仪，随护及修习，\n"
        "　此四正断法，诸佛之所说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「应当知道有四种正断：一是断断，二是律仪断，三是随护断，四是修断。」",
        "那时世尊说偈：\n"
        "「断断与律仪，随护及修习，\n"
        "　此四正断法，诸佛之所说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：同 AN4.13／SN49 名目＋偈；"
        "与 SA_875 为略／略＋偈一对。"
    ),
}

# --- SA 877 四正断广（SN49；据 AN 校正名实）---------------------------------
SUTTAS["SA_877"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四正断。何等为四？断断、律仪断、随护断、修断。"
        "云何断断？比丘于已起恶不善法，生欲、精进、发勤、策心、持心而断，是名断断。"
        "云何律仪断？于未起恶不善法，生欲、精进、发勤、策心、持心令不起，是名律仪断。"
        "云何随护断？于已生善法，生欲、精进、发勤、策心、持心，令住不忘、修习增广，是名随护断。"
        "云何修断？于未生善法，生欲、精进、发勤、策心、持心令生起，是名修断。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四正断。哪四种？断断、律仪断、随护断、修断。"
        "什么是断断？比丘对已生起的恶不善法，生起欲乐、精进、发动、策心、持心而断除，叫做断断。"
        "什么是律仪断？对尚未生起的恶不善法，生起欲乐、精进、发动、策心、持心使它不生，叫做律仪断。"
        "什么是随护断？对已生起的善法，生起欲乐、精进、发动、策心、持心，使它安住不忘、修习增长，叫做随护断。"
        "什么是修断？对尚未生起的善法，生起欲乐、精进、发动、策心、持心使它生起，叫做修断。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN49／AN4.13；"
        "据巴利校正汉本第三、四项名实错置："
        "anurakkhaṇā（随护）＝护持已生善；bhāvanā（修）＝令未生善生；"
        "精勤句据 chanda／vāyāma／viriya／citta／padhāna 作生欲、精进、发勤、策心、持心。"
    ),
}

# --- SA 878 四正断广＋偈-----------------------------------------------------
SUTTAS["SA_878"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四正断。何等为四？断断、律仪断、随护断、修断。"
        "云何断断？比丘于已起恶不善法，生欲、精进、发勤、策心、持心而断，是名断断。"
        "云何律仪断？于未起恶不善法，生欲、精进、发勤、策心、持心令不起，是名律仪断。"
        "云何随护断？于已生善法，生欲、精进、发勤、策心、持心，令住不忘、修习增广，是名随护断。"
        "云何修断？于未生善法，生欲、精进、发勤、策心、持心令生起，是名修断。」",
        "尔时世尊说偈言：\n"
        "「断断及律仪，随护与修习，\n"
        "　如此四正断，诸佛之所说。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四正断。哪四种？断断、律仪断、随护断、修断。"
        "什么是断断？比丘对已生起的恶不善法，生起欲乐、精进、发动、策心、持心而断除，叫做断断。"
        "什么是律仪断？对尚未生起的恶不善法，生起欲乐、精进、发动、策心、持心使它不生，叫做律仪断。"
        "什么是随护断？对已生起的善法，生起欲乐、精进、发动、策心、持心，使它安住不忘、修习增长，叫做随护断。"
        "什么是修断？对尚未生起的善法，生起欲乐、精进、发动、策心、持心使它生起，叫做修断。」",
        "那时世尊说偈：\n"
        "「断断及律仪，随护与修习，\n"
        "　如此四正断，诸佛之所说。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：同 SA_877＋偈；"
        "据 AN／SN 校正随护／修之对应（见 SA_877 notes）。"
    ),
}

# --- SA 879 四正断（AN4.14 异门）---------------------------------------------
SUTTAS["SA_879"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「有四正断。何等为四？断断、律仪断、随护断、修断。"
        f"云何断断？若比丘{FOUR_PADHANA_BODY_LIT}，是名断断。"
        "云何律仪断？若比丘善护眼根，密护、调伏、向于防护；"
        "耳、鼻、舌、身、意根亦复如是，是名律仪断。"
        "云何随护断？若比丘于真实三昧之相善守护持——"
        "所谓青瘀、膨胀、脓烂、坏烂、啖残等相，修习守护，不令退失，是名随护断。"
        "云何修断？若比丘修四念处，是名修断。」",
        "尔时世尊说偈言：\n"
        "「断断律仪断，随护与修断，\n"
        "　此四正断法，正觉之所说；\n"
        "　比丘勤方便，得尽于诸漏。」",
        CLOSE_BH_LIT,
        "如四念处，四正断、四如意足、五根、五力、七觉支、八圣道分、四道、四法句、正观修习，亦如是说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「有四正断。哪四种？断断、律仪断、随护断、修断。"
        f"什么是断断？如果比丘{FOUR_PADHANA_BODY_MOD}，叫做断断。"
        "什么是律仪断？如果比丘善护眼根，密护、调伏、致力于防护；"
        "耳、鼻、舌、身、意根也是这样，叫做律仪断。"
        "什么是随护断？如果比丘对真实三昧的所缘相善加守护——"
        "也就是青瘀、膨胀、脓烂、坏烂、啖残等相，修习守护，不让退失，叫做随护断。"
        "什么是修断？如果比丘修四念处，叫做修断。」",
        "那时世尊说偈：\n"
        "「断断律仪断，随护与修断，\n"
        "　此四正断法，正觉之所说；\n"
        "　比丘勤方便，得尽于诸漏。」",
        CLOSE_BH_MOD,
        "如同四念处，四正断、四如意足、五根、五力、七觉支、八圣道分、四道、四法句、正观修习，也是这样说。",
    ],
    "notes": (
        f"{PROV}confidence=high：平行 AN4.14；"
        "四名异门：断断＝总摄四正勤；律仪＝护根；随护＝护不净相等三昧相；修＝修四念处等。"
        "汉「食不尽相」→啖残相；末道品 peyyāla 从汉。"
    ),
}

# --- SA 880 不放逸（依四禅）-------------------------------------------------
SUTTAS["SA_880"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「犹若世人营造宅舍，莫不以大地为依；"
        "比丘修四禅亦复如是——悉以不放逸为基，由之不放逸而集、生、转；"
        "若能不放逸，四禅可得成办。」",
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「就像世人盖房子，没有不以大地为依靠的；"
        "比丘修四禅也是这样——都以不放逸为根基，靠着不放逸而集起、生起、运转；"
        "若能不放逸，四禅就可以成办。」",
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：不放逸（appamāda）为修禅根本之定型譬；"
        "参 AN／SN 不放逸相应通义。禅法→诸禅。"
    ),
}

# --- SA 881 断贪等（peyyāla）-------------------------------------------------
SUTTAS["SA_881"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「譬如有人于世间有所建立，一切皆依于地；"
        f"如是比丘修习诸禅，{APPAMADA_CORE_LIT}。"
        "如是比丘能断贪欲、瞋恚、愚癡。」",
        CLOSE_BH_LIT,
        "如断贪欲、瞋恚、愚癡，调伏贪瞋癡、贪瞋癡究竟，出要、远离、涅槃，亦如是说。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「好比有人在世间有所建立，一切都依靠大地；"
        f"同样，比丘修习诸禅，{APPAMADA_CORE_MOD}。"
        "这样，比丘就能断除贪欲、瞋恚、愚癡。」",
        CLOSE_BH_MOD,
        "如同断除贪欲、瞋恚、愚癡，调伏贪瞋癡、贪瞋癡究竟，以及出要、远离、涅槃，也是这样说。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：底本「如上说」peyyāla；"
        "据 SA_880 不放逸依地譬补纲，差别句为断／调伏／究竟贪瞋痴及出要等。"
    ),
}

# --- SA 882 不放逸根本（譬喻串；SN49.13–22 类）-------------------------------
_SIMILES_LIT = [
    ("百草药木皆依于地而得生长", "种种善法"),
    ("黑沉水香于众香中最为第一", "种种善法"),
    ("诸坚固香中赤栴檀为第一", "一切善法"),
    ("水陆诸华中优钵罗华为第一", "一切善法"),
    ("陆地诸华中摩利沙华为第一", "一切善法"),
    ("一切兽迹中象迹为上", "一切诸善法"),
    ("一切走兽中师子为第一，所谓兽王", "一切善法"),
    ("一切屋舍堂阁以栋梁为第一", "一切善法"),
    ("阎浮诸果中得阎浮名者果最为第一", "一切善法"),
    ("一切俱毗陀罗树中萨婆耶旨罗俱毗陀罗为第一", "一切善法"),
    ("诸山中须弥山王为第一", "一切善法"),
    ("一切金中阎浮提金为第一", "一切善法"),
    ("一切衣中迦尸细叠为第一", "一切善法"),
    ("一切色中白色为第一", "一切善法"),
    ("众鸟中金翅鸟为第一", "一切善法"),
    ("诸王中转轮圣王为第一", "一切善法"),
    ("一切天王中四大天王为第一", "一切善法"),
    ("三十三天中帝释为第一", "一切善法"),
    ("焰摩天中焰摩天王为第一", "一切善法"),
    ("兜率陀天中兜率陀天王为第一", "一切善法"),
    ("化乐天中善化乐天王为第一", "一切善法"),
    ("他化自在天中他化自在天王为第一", "一切善法"),
    ("梵天中大梵王为第一", "一切善法"),
    ("阎浮提一切众流皆顺趣大海，大海最为第一，以能容受故", "一切善法皆顺趣不放逸"),
    ("一切雨滴皆归大海", "一切善法皆顺趣不放逸"),
    ("一切湖泊中阿耨达池为第一", "一切善法"),
    ("阎浮提诸河中四大河为第一——恒河、信度、缚刍、徙多", "一切善法"),
    ("众星光明中月为第一", "一切善法"),
    ("诸大身众生中罗睺阿修罗为第一", "一切善法"),
    ("诸受五欲者中顶生王为第一", "一切善法"),
    ("欲界诸神力中天魔波旬为第一", "一切善法"),
    (
        "一切众生——无足、两足、四足、多足，有色、无色，有想、无想、非想非非想——"
        "如来为第一",
        "一切善法",
    ),
    ("所有诸法有为、无为，离贪欲者为第一", "一切善法"),
    ("一切法众中如来众为第一", "一切善法"),
    ("一切诸界苦行中，梵行圣界为第一", "一切善法"),
]

_lit_882_paras = [OPEN_JET_LIT, "尔时世尊告诸比丘："]
_mod_882_paras = [OPEN_JET_MOD, "那时世尊告诉比丘们："]
for _i, (_sim, _subj) in enumerate(_SIMILES_LIT):
    if _i == 0:
        _lit_882_paras.append(
            f"「譬如{_sim}；如是{_subj}，{APPAMADA_CORE_LIT}。」"
        )
        _mod_882_paras.append(
            f"「好比{_sim}；同样，{_subj}，{APPAMADA_CORE_MOD}。」"
        )
    elif "顺趣不放逸" in _subj:
        _lit_882_paras.append(
            f"「譬如{_sim}；如是{_subj}，{APPAMADA_CORE_LIT}。」"
        )
        _mod_882_paras.append(
            f"「好比{_sim}；同样，{_subj}，{APPAMADA_CORE_MOD}。」"
        )
    else:
        _lit_882_paras.append(
            f"「譬如{_sim}；如是{_subj}，不放逸最为第一，{APPAMADA_CORE_LIT}。」"
        )
        _mod_882_paras.append(
            f"「好比{_sim}；同样，{_subj}，不放逸最为第一，{APPAMADA_CORE_MOD}。」"
        )
_lit_882_paras.append(CLOSE_BH_LIT)
_mod_882_paras.append(CLOSE_BH_MOD)

SUTTAS["SA_882"] = {
    "lit": _lit_882_paras,
    "mod": _mod_882_paras,
    "notes": (
        f"{PROV}confidence=high：SC 列 SN49.13–22 类不放逸／正勤譬喻串；"
        "汉「如上说，乃至涅槃」peyyāla 据 SA_880–881 不放逸定型补足；"
        "河名信度／缚刍／徙多，伽尸细㲲→迦尸细叠，宿焰摩→焰摩。"
    ),
}

# --- SA 883 四种禅（SN34 三昧／正受矩阵）------------------------------------
def _jhana_quad_lit(a: str, b: str) -> str:
    return (
        f"有禅{a}善而非{b}善；有禅{b}善而非{a}善；"
        f"有禅{a}善亦{b}善；有禅非{a}善亦非{b}善"
    )


def _jhana_quad_mod(a: str, b: str) -> str:
    return (
        f"有的禅者善于{a}而不善于{b}；有的善于{b}而不善于{a}；"
        f"有的{a}与{b}皆善；有的{a}与{b}皆不善"
    )


_JHANA_DIMS = [
    ("三昧", "正受"),
    ("住三昧", "住正受"),
    ("三昧起", "正受起"),
    ("三昧时", "正受时"),
    ("三昧处", "正受处"),
    ("三昧行境", "正受行境"),
    ("三昧念", "正受念"),
    ("三昧念与失念", "正受念与失念"),
    ("三昧转入", "正受转入"),
    ("三昧出", "正受出"),
    ("三昧方便", "正受方便"),
    ("三昧止", "正受止"),
    ("三昧举", "正受举"),
    ("三昧舍", "正受舍"),
]

_lit_883 = [
    OPEN_JET_LIT,
    "尔时世尊告诸比丘：「有四种禅者。何等为四？"
    + _jhana_quad_lit("三昧", "正受")
    + "。」",
]
_mod_883 = [
    OPEN_JET_MOD,
    "那时世尊告诉比丘们：「有四种禅者。哪四种？"
    + _jhana_quad_mod("三昧", "正受")
    + "。」",
]
for _a, _b in _JHANA_DIMS[1:]:
    _lit_883.append(f"「复次，四种禅者：{_jhana_quad_lit(_a, _b)}。」")
    _mod_883.append(f"「再者，四种禅者：{_jhana_quad_mod(_a, _b)}。」")
_lit_883.append(CLOSE_BH_LIT)
_mod_883.append(CLOSE_BH_MOD)

SUTTAS["SA_883"] = {
    "lit": _lit_883,
    "mod": _mod_883,
    "notes": (
        f"{PROV}confidence=high：primary SN34.1 及 SN34 诸经矩阵；"
        "三昧＝samādhi，正受＝samāpatti；"
        "汉「迎／来／恶」等拙译据 gocara／āvajjana／vuṭṭhāna 等义作行境／转入／出；"
        "念不念→念与失念。删梵式冗复而保留十四门四句。"
    ),
}

# --- SA 884 无学三明（略，AN3.58–59）-----------------------------------------
SUTTAS["SA_884"] = {
    "lit": [
        OPEN_JET_LIT,
        f"尔时世尊告诸比丘：「有无学三明。何等为三？谓{THREE_VIJJA_LIT}。」",
        VIJJA_GATHA_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"那时世尊告诉比丘们：「有无学三明。哪三种？就是{THREE_VIJJA_MOD}。」",
        VIJJA_GATHA_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：平行 AN3.58–59；"
        "三明＝宿命／生死（天眼）／漏尽。偈「见天恶趣生」→见有情趣生。"
    ),
}

# --- SA 885 无学三明广-------------------------------------------------------
SUTTAS["SA_885"] = {
    "lit": [
        OPEN_JET_LIT,
        f"尔时世尊告诸比丘：「有无学三明。何等为三？谓{THREE_VIJJA_LIT}。」",
        VIJJA_PUBBE_LIT,
        VIJJA_CUTA_LIT,
        VIJJA_ASAVA_LIT,
        VIJJA_GATHA_LIT,
        CLOSE_BH_LIT,
    ],
    "mod": [
        OPEN_JET_MOD,
        f"那时世尊告诉比丘们：「有无学三明。哪三种？就是{THREE_VIJJA_MOD}。」",
        VIJJA_PUBBE_MOD,
        VIJJA_CUTA_MOD,
        VIJJA_ASAVA_MOD,
        VIJJA_GATHA_MOD,
        CLOSE_BH_MOD,
    ],
    "notes": (
        f"{PROV}confidence=high：AN3.58–59 广说；"
        "三明内容据巴利／汉本厘定；欲有漏→欲漏、有有漏→有漏。"
    ),
}

# --- SA 886 婆罗门三明（对辩；补广说）---------------------------------------
SUTTAS["SA_886"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异婆罗门来诣佛所，与世尊面相问讯，问讯已，退坐一面，作是言："
        "「此是婆罗门三明，此是婆罗门三明。」",
        "佛告婆罗门：「云何名为婆罗门三明？」",
        "婆罗门白佛：「瞿昙！婆罗门父母具相，无诸瑕秽，七世相承无有讥嫌，"
        "世世为师，辩才具足；诵诸经典，通达物类名字、差品、字类分合、历世本末——"
        "此五种记皆悉通达，容色端正：是名婆罗门三明。」",
        "佛告婆罗门：「我不说名字言说为三明。贤圣法中说真实三明——"
        "谓无学三明：宿命智证明、生死智证明、漏尽智证明。」",
        VIJJA_PUBBE_LIT,
        VIJJA_CUTA_LIT,
        VIJJA_ASAVA_LIT,
        "尔时世尊说偈言：\n"
        "「诸行悉无常，持戒寂静禅；\n"
        "　知一切宿命，见有情趣生；\n"
        "　漏尽心解脱，贪瞋痴永尽；\n"
        "　我说是三明，非名字言说。」",
        "「婆罗门！是为圣法律中所说三明。」",
        "婆罗门白佛：「瞿昙！是真三明。」"
        "闻佛所说，欢喜随喜，从座起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位婆罗门来到佛那里，与世尊互相问候，问候完毕，坐在一边，说道："
        "「这才是婆罗门三明，这才是婆罗门三明。」",
        "佛告诉婆罗门：「怎样叫做婆罗门三明？」",
        "婆罗门对佛说：「瞿昙！婆罗门父母相貌端正，没有瑕秽，七世相承没有讥嫌，"
        "世世代代为人师长，辩才具足；能讽诵经典，通达事物名称、分类、字类分合、历代本末——"
        "这五种记诵都通达，容貌端正：这就叫做婆罗门三明。」",
        "佛告诉婆罗门：「我不说靠名字言说就是三明。在贤圣法中说的是真实三明——"
        "也就是无学三明：宿命智证明、生死智证明、漏尽智证明。」",
        VIJJA_PUBBE_MOD,
        VIJJA_CUTA_MOD,
        VIJJA_ASAVA_MOD,
        "那时世尊说偈：\n"
        "「诸行悉无常，持戒寂静禅；\n"
        "　知一切宿命，见有情趣生；\n"
        "　漏尽心解脱，贪瞋痴永尽；\n"
        "　我说是三明，非名字言说。」",
        "「婆罗门！这就是圣法律中所说的三明。」",
        "婆罗门对佛说：「瞿昙！这才是真三明。」"
        "听了佛所说，欢喜随喜，从座位起来离去。",
    ],
    "notes": (
        f"{PROV}confidence=high：对辩结构近 AN3.58 Tevijja；"
        "「如上经广说」→据 SA_885／AN 补三明广释；"
        "汉偈「一切法无常」等杂句据三明义收束为持戒寂禅＋三通。"
    ),
}

# --- SA 887 信---------------------------------------------------------------
SUTTAS["SA_887"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异婆罗门来诣佛所，与世尊面相问讯，问讯已，退坐一面，白佛言："
        "「瞿昙！我名信。」",
        "佛告婆罗门：「所谓信者，信增上于戒、施、闻、舍、慧，是名为信——"
        "非但名字为信也。」",
        "时婆罗门闻佛所说，欢喜随喜，从座起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位婆罗门来到佛那里，与世尊互相问候，问候完毕，坐在一边，对佛说："
        "「瞿昙！我名叫信。」",
        "佛告诉婆罗门：「所谓信，是在戒、施、闻、舍、慧上增长信心，这才叫做信——"
        "不是仅仅有个名字叫信。」",
        "当时婆罗门听了佛所说，欢喜随喜，从座位起来离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：名字义经；"
        "信＝于戒施闻舍慧增上（早期五法），非唯名。"
    ),
}

# --- SA 888 增益-------------------------------------------------------------
SUTTAS["SA_888"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异婆罗门来诣佛所，面相问讯，问讯已，退坐一面，白佛言："
        "「瞿昙！我名增益。」",
        "佛告婆罗门：「所谓增益者，信增益，戒、闻、舍、慧增益，是名增益——"
        "非但名字为增益也。」",
        "时婆罗门闻佛所说，欢喜随喜，从座起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位婆罗门来到佛那里，互相问候，问候完毕，坐在一边，对佛说："
        "「瞿昙！我名叫增益。」",
        "佛告诉婆罗门：「所谓增益，是信心增长，戒、闻、舍、慧也增长，这才叫做增益——"
        "不是仅仅有个名字叫增益。」",
        "当时婆罗门听了佛所说，欢喜随喜，从座位起来离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：与 SA_887 同型；"
        "增益＝信戒闻舍慧增上。"
    ),
}

# --- SA 889 等起-------------------------------------------------------------
SUTTAS["SA_889"] = {
    "lit": [
        OPEN_JET_LIT,
        "时有异婆罗门来诣佛所，问讯安否，问讯已，退坐一面，白佛言："
        "「世尊！我名等起。」",
        "佛告婆罗门：「夫等起者，起于信，起戒、闻、舍、慧，是名等起——"
        "非但名字为等起也。」",
        "时婆罗门闻佛所说，欢喜随喜，从座起去。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "当时有一位婆罗门来到佛那里，问候安好，问候完毕，坐在一边，对佛说："
        "「世尊！我名叫等起。」",
        "佛告诉婆罗门：「所谓等起，是生起信心，生起戒、闻、舍、慧，这才叫做等起——"
        "不是仅仅有个名字叫等起。」",
        "当时婆罗门听了佛所说，欢喜随喜，从座位起来离去。",
    ],
    "notes": (
        f"{NO_PARALLEL}confidence=medium：与 SA_887–888 同型；"
        "等起＝令信戒闻舍慧生起。"
    ),
}

# --- SA 890 无为法（SN43.11）-------------------------------------------------
SUTTAS["SA_890"] = {
    "lit": [
        OPEN_JET_LIT,
        "尔时世尊告诸比丘：「我今说无为，及趣无为之道。谛听，善思念之。"
        "何等无为？谓贪瞋痴永尽，诸烦恼永尽，是名无为。"
        f"何等无为道迹？谓八支圣道——{EIGHT_LIT}，是名趣无为之道。」",
        CLOSE_BH_LIT,
        "如说无为，难见、不动、不屈、不死、无漏、覆荫、洲渚、济渡、依止、拥护、"
        "不流转、离炽然、离烧燃、流通、清凉、微妙、安隐、无病、无所有、涅槃，皆亦如是。",
    ],
    "mod": [
        OPEN_JET_MOD,
        "那时世尊告诉比丘们：「我现在说无为，以及趣向无为的道路。仔细听，好好思惟。"
        "什么是无为？就是贪瞋痴永尽，诸烦恼永尽，叫做无为。"
        f"什么是无为道迹？就是八支圣道——{EIGHT_MOD}，叫做趣向无为的道路。」",
        CLOSE_BH_MOD,
        "如同说无为，难见、不动、不屈、不死、无漏、覆荫、洲渚、济渡、依止、拥护、"
        "不流转、离炽然、离烧燃、流通、清凉、微妙、安隐、无病、无所有、涅槃，也都是这样。",
    ],
    "notes": (
        f"{PROV}confidence=high：primary SN43.11；"
        "无为＝asaṅkhata（贪瞋痴等永尽）；道迹＝八支圣道；"
        "汉「正智」据道支校正为「正志」；末异名 peyyāla（难见…涅槃）从 SN43 系列。"
    ),
}

# ---------------------------------------------------------------------------
# confidence / reconstructed
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_871": "medium",
    "SA_872": "medium",
    "SA_873": "high",
    "SA_874": "high",
    "SA_875": "high",
    "SA_876": "high",
    "SA_877": "high",
    "SA_878": "high",
    "SA_879": "high",
    "SA_880": "medium",
    "SA_881": "medium",
    "SA_882": "high",
    "SA_883": "high",
    "SA_884": "high",
    "SA_885": "high",
    "SA_886": "high",
    "SA_887": "medium",
    "SA_888": "medium",
    "SA_889": "medium",
    "SA_890": "high",
}

RECONSTRUCTED: dict[str, str] = {
    "SA_881": "peyyāla「如上说」→ SA_880 不放逸依地譬＋断贪瞋痴差别",
    "SA_882": "「如上说，乃至涅槃」譬喻串 → 不放逸定型补足",
    "SA_886": "「如上经广说」→ SA_885／AN3.58–59 三明广释",
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
    assert set(GOLD) == {f"SA_{i}" for i in range(871, 891)}, (
        "GOLD must cover SA_871–SA_890 exactly"
    )
    assert set(CONFIDENCE) == set(GOLD), "CONFIDENCE must cover every retranslated id"
    assert not any(f"SA_{i}" in GOLD for i in range(851, 871))
    assert not any(f"SA_{i}" in GOLD for i in range(891, 911))

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

    by_status = {r["id"]: r.get("review_status") for r in records}
    _goldish = {"gold", "gold_reconstructed"}
    boundary_id = "SA_870" if by_status.get("SA_870") in _goldish else None

    boundary_before = None
    if boundary_id:
        for rec in records:
            if rec["id"] == boundary_id:
                boundary_before = _snap(rec)
                break

    # Neighbors must remain untouched (parallel batches)
    neighbor_ids = {f"SA_{i}" for i in list(range(851, 871)) + list(range(891, 911))}
    mid_before = {
        rec["id"]: _snap(rec) for rec in records if rec["id"] in neighbor_ids
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

    if boundary_id and boundary_before is not None:
        for rec in merged:
            if rec["id"] == boundary_id:
                assert boundary_before == _snap(rec), f"{boundary_id} must remain untouched"
                break

    for rid, before in mid_before.items():
        for rec in merged:
            if rec["id"] == rid:
                assert before == _snap(rec), f"{rid} (neighbor) must remain untouched"
                break

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa871-890.json").write_text(
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
        by_merged.get(f"SA_{i}", {}).get("review_status") in goldish
        for i in range(871, 891)
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_871–SA_890 only)")
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
    print(f"continuous_gold_SA_871–890={continuous}")
    print(f"neighbors_851–870_891–910_untouched=True")
    if boundary_id:
        print(f"{boundary_id}_untouched=True (was gold)")
    else:
        print("SA_870_boundary_assert_skipped (not gold)")
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
