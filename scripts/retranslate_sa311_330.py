#!/usr/bin/env python3
"""Retranslate SA 311–330（卷第十三 六入處相應续）→ merge into final_translated_data.json.

本批二十经：富楼那、摩罗迦舅、经法、断欲、眼生、眼无常／苦／非我、
生闻一切／一切有／一切法、内外入处分别、六内／外／识／触／受／想／思／爱。

信：`raw_aligned_data.json` 内备巴利本文、Sujato 英译；有平行者以 SN／Pāli 厘义。
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

OPEN_LIT = "如是我闻：一时，佛在舍卫国祇树给孤独园。"
OPEN_MOD = "我是这样听说的：有一次，佛住在舍卫国祇树给孤独园。"

CLOSE_LIT = "佛说此经已，诸比丘闻佛所说，欢喜奉行。"
CLOSE_MOD = "佛说完这部经，比丘们听佛所说，都欢喜奉行。"

CLOSE_DEPART_LIT = "彼闻佛所说，欢喜随喜，作礼而去。"
CLOSE_DEPART_MOD = "他听佛所说，欢喜随喜，礼佛而去。"

CLOSE_BRAHMIN_LIT = "生闻婆罗门闻佛所说，欢喜随喜，从座起去。"
CLOSE_BRAHMIN_MOD = "生闻婆罗门听佛所说，欢喜随喜，从座而起离去。"

SIX_LIT = "耳、鼻、舌、身、意亦复如是。"
SIX_MOD = "耳、鼻、舌、身、意也是一样。"

AWAKEN_LIT = "「我生已尽，梵行已立，所作已作，自知不受后有。」"
AWAKEN_MOD = "「我生已尽，梵行已立，所作已作，自知不受后有。」"

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

# --- SA 311 富楼那（SN 35.88 / MN 145 Puṇṇa）---------------------------------
SUTTAS["SA_311"] = {
    "lit": [
        OPEN_LIT,
        "尔时，尊者富楼那来诣佛所，稽首礼足，退住一面，白佛言："
        "「善哉！世尊！愿为我略说法要。我闻法已，当独一静处，专精思惟，不放逸住，"
        "乃至自知不受后有。」",
        "佛告富楼那：「善哉！谛听，当为汝说。眼所知色，可爱、可乐、可意、长养欲；"
        "若比丘于彼欣悦、称叹、染著而住，则生耽喜。我说：耽喜集故，苦集。"
        "耳声、鼻香、舌味、身触、意法，亦复如是——欣悦、称叹、染著，则生耽喜；"
        "耽喜集故，苦集。」",
        "「若于眼所知色，不欣悦、不称叹、不染著，则耽喜息；耽喜息故，苦息。"
        "耳、鼻、舌、身、意亦复如是。富楼那！我已略说教诫，汝欲止何处？」",
        "富楼那白佛：「世尊！我欲往西方输卢那人间游行。」",
        "佛告富楼那：「输卢那人凶恶轻躁、粗暴好骂。汝若闻彼毁辱，当如之何？」"
        "答言：「当作是念：『彼人贤善有智——虽骂辱我，犹不以拳石打掷。』」",
        "「若以拳石打掷，当如之何？」"
        "「当作是念：『犹不以刀杖加我。』」",
        "「若以刀杖加汝，当如之何？」"
        "「当作是念：『犹不见杀。』」",
        "「假使杀汝，当如之何？」"
        "「当作是念：『有诸世尊弟子，厌患此身，求自害之具；"
        "今彼人以少方便，令我朽败之身得脱——彼实贤善有智。』」",
        "佛言：「善哉！富楼那！汝善修忍，堪于输卢那人间止住。"
        "宜往度未度、安未安，未得涅槃者令得涅槃。」",
        "富楼那闻法欢喜，作礼而去。晨朝著衣持钵，入舍卫城乞食；食已还，付嘱卧具，"
        "持衣钵往输卢那。夏安居中，为五百优婆塞说法，立五百僧伽蓝，衣卧供具悉备。"
        "三月过已，具足三明，于彼处入无余涅槃。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，富楼那尊者来见佛，稽首礼足，退住一面，对佛说："
        "「善哉！世尊！愿为我略说法要。我听法后，要独自静处，专精思惟，不放逸而住，"
        "直到自知不受后有。」",
        "佛告诉富楼那：「善哉！谛听，当为你说。眼所知的色，可爱、可乐、可意、长养欲；"
        "若比丘对它们欣悦、称叹、染著而住，就会生起耽喜。我说：耽喜集，苦就集。"
        "耳声、鼻香、舌味、身触、意法也是一样——欣悦、称叹、染著，则生耽喜；"
        "耽喜集故，苦集。」",
        "「若对眼所知色不欣悦、不称叹、不染著，则耽喜息；耽喜息故，苦息。"
        "耳、鼻、舌、身、意也是一样。富楼那！我已略说教诫，你想住在哪里？」",
        "富楼那白佛：「世尊！我想去西方输卢那人间游行。」",
        "佛说：「输卢那人凶恶轻躁、粗暴好骂。你若听他们毁辱，当怎么办？」"
        "答：「当作念：『这些人贤善有智——虽骂辱我，还不用拳石打我。』」",
        "「若用拳石打你呢？」"
        "「当作念：『还没用刀杖加我。』」",
        "「若用刀杖加你呢？」"
        "「当作念：『还不至于杀我。』」",
        "「假使杀你呢？」"
        "「当作念：『有世尊弟子厌患此身，另求自害之具；"
        "今这些人用很少的方便，就让我这朽败之身得脱——他们实在贤善有智。』」",
        "佛说：「善哉！富楼那！你善修忍辱，堪能住在输卢那人间。"
        "宜去度未度、安未安，未得涅槃者令得涅槃。」",
        "富楼那闻法欢喜，礼佛而去。晨朝著衣持钵，入舍卫城乞食；食已回来，付嘱卧具，"
        "持衣钵往输卢那。夏安居中为五百优婆塞说法，建立五百僧伽蓝，衣卧供具都备齐。"
        "三月过后，具足三明，就在那里入无余涅槃。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.88（Puṇṇa）／MN145 为 `full` 平行。"
        "信-校正：底本「欢喜→乐着→贪爱→阨碍→去涅槃远」链，巴利作 "
        "abhinandati/abhivadati/ajjhosāya → nandī → dukkhasamudaya（耽喜集故苦集）；"
        "今据 Pāli／Sujato 作「耽喜集故，苦集／耽喜息故，苦息」。"
        "输卢那忍辱递进问答及安居度众、三明入灭，汉巴同构。"
    ),
}

# --- SA 312 摩罗迦舅（SN 35.95 Mālukyaputta）--------------------------------
SUTTAS["SA_312"] = {
    "lit": [
        OPEN_LIT,
        "尔时，摩罗迦舅来诣佛所，稽首礼足，退坐一面，白佛言："
        "「善哉！世尊！愿为我略说法要。我闻法已，当独一静处，专精思惟，不放逸住，"
        "乃至自知不受后有。」",
        "佛告摩罗迦舅：「年少新学，于我法、律尚无懈怠；"
        "况汝年耆根熟，而求略说教诫耶？」"
        "摩罗迦舅再三请：「虽年耆，犹愿得闻略说。」",
        "佛言：「我今问汝，随意答我。若眼所未曾见之色——未曾见、不当见、亦不意其当见——"
        "于彼起欲、起爱、起染著不？」"
        "答言：「不也，世尊！」"
        "「耳声、鼻香、舌味、身触、意法——未曾了知者，亦如是问。」"
        "皆答：「不也，世尊！」",
        "佛告摩罗迦舅：「善哉！于所见，唯见为量；于所闻，唯闻为量；"
        "于所觉，唯觉为量；于所知，唯知为量。"
        "如是则不随彼；不随彼故，不在于彼；不在于彼故，"
        "不在此世、他世及两中间——是则苦边。」"
        "而说偈言：",
        "「汝不在于彼，彼亦不在此，亦不在中间，是名苦边际。」",
        "摩罗迦舅白佛：「已知。世尊！已知。善逝！」"
        "佛问：「汝云何于我略说中广解其义？」",
        "摩罗迦舅以偈答曰：",
        "「眼见众色时，若失于正念，取彼可爱相，心则生染著。"
        "爱念相既取，心常系不舍，种种爱增长，无量色集生。"
        "贪恚害觉起，损减坏其心，长养于众苦，远离般涅槃。"
        "见色不取相，正念任运住，心不染恶爱，亦不生系著。"
        "诸爱既不起，色集则不生，贪恚害觉灭，不能坏其心。"
        "众苦随损减，渐近于涅槃，日种尊所说，离爱般涅槃。"
        "耳声鼻香等，身触意念法，失念取爱相，过患亦复然。"
        "正念不染著，爱尽苦随灭，爱尽般涅槃，世尊之所说。」",
        "佛赞：「善哉！汝真于略说中广解其义。」",
        "摩罗迦舅欢喜作礼而去。独一静处，专精思惟，不放逸住，乃至漏尽，成阿罗汉。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，摩罗迦舅来见佛，稽首礼足，退坐一面，对佛说："
        "「善哉！世尊！愿为我略说法要。我听法后，要独自静处，专精思惟，不放逸而住，"
        "直到自知不受后有。」",
        "佛告诉摩罗迦舅：「年轻新学的比丘，在我法、律中尚且不懈怠；"
        "何况你年老根熟，还来求略说教诫？」"
        "摩罗迦舅再三请求：「我虽然年老，仍愿听略说。」",
        "佛说：「我现在问你，随意回答。对于眼所从未见过的色——从未见、不当见、也不想会见到——"
        "你会对其起欲、起爱、起染著吗？」"
        "答：「不会，世尊！」"
        "「耳声、鼻香、舌味、身触、意法——从未了知的，也同样问。」"
        "都答：「不会，世尊！」",
        "佛说：「善哉！在所见中，只以见为量；在所闻中，只以闻为量；"
        "在所觉中，只以觉为量；在所知中，只以知为量。"
        "这样就不会被那个带走；不被带走，就不住在其中；不住在其中，"
        "就不在此世、他世及两中间——这就是苦的边际。」"
        "并说偈：",
        "「你不在于彼，彼也不在此，也不在中间，这就是苦边。」",
        "摩罗迦舅白佛：「已知。世尊！已知。善逝！」"
        "佛问：「你怎样在我的略说里广解其义？」",
        "摩罗迦舅用偈回答：",
        "「眼见众色时，若失于正念，取那可爱相，心就生染著。"
        "爱念相既取，心常系不舍，种种爱增长，无量色集生。"
        "贪恚害觉起，损减坏其心，长养于众苦，远离般涅槃。"
        "见色不取相，正念任运住，心不染恶爱，也不生系著。"
        "诸爱既不起，色集则不生，贪恚害觉灭，不能坏其心。"
        "众苦随损减，渐近于涅槃，日种尊所说，离爱般涅槃。"
        "耳声鼻香等，身触意念法，失念取爱相，过患也一样。"
        "正念不染著，爱尽苦随灭，爱尽般涅槃，世尊之所说。」",
        "佛赞叹：「善哉！你真能在略说中广解其义。」",
        "摩罗迦舅欢喜礼佛而去。独自静处，专精思惟，不放逸而住，直到漏尽，成阿罗汉。",
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.95（Mālukyaputta）为 `full` 平行。"
        "信-校正：底本「见以见为量」据巴利 diṭṭhe diṭṭhamattaṃ 等作"
        "「于所见，唯见为量」；「不在此世、他世及两中间，是则苦边」据 Pāli 补明。"
        "偈颂据汉本广解义，参 Sujato 英译压缩重复六根句。"
        "底本三请三止之叙事略收，以合巴利先叹年耆、再许问答之序。"
    ),
}

# --- SA 313 经法（无平行）----------------------------------------------------
SUTTAS["SA_313"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「有经法，诸比丘于彼崇向；虽信、欲、闻、思惟、审谛忍各异，"
        "而能正知自记：" + AWAKEN_LIT,
        "诸比丘白佛：「世尊是法根、法眼、法依。愿广说，我等当受奉行。」",
        "佛告诸比丘：「谛听，善思。比丘眼见色已，觉知于色，而不起色贪——"
        "如实知：『我先眼识于色有贪，而今眼识于色无贪。』"
        "如是知者，于意云何——于此法为有信、有欲、有闻、有行思惟、有审谛忍不？」"
        "答言：「如是，世尊！」"
        "「归于此法，如实正知所见不？」"
        "答言：「如是，世尊！」",
        "「耳、鼻、舌、身、意法，亦复如是。"
        "是名有经法：比丘于此崇向，虽信欲闻思审忍有异，而能正知自记生尽不受后有。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「有一种经法，比丘们向它归向；"
        "虽然各人的信、欲、闻、思惟、审谛忍不尽相同，却能正知而自记："
        + AWAKEN_MOD,
        "比丘们白佛：「世尊是法根、法眼、法依。愿广说，我们当受奉行。」",
        "佛说：「谛听，善思。比丘眼见色后，觉知于色，却不起色贪——"
        "如实知道：『我从前眼识对色有贪，而现在眼识对色无贪。』"
        "这样知道的人，你们怎么看——对此法是否有信、有欲、有闻、有行思惟、有审谛忍？」"
        "答：「是的，世尊！」"
        "「归向此法，能如实正知所见吗？」"
        "答：「是的，世尊！」",
        "「耳、鼻、舌、身、意法，也是一样。"
        "这叫做有经法：比丘向它归向，虽信欲闻思审忍有异，仍能正知自记生尽不受后有。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "本经论「经法」：于六根境觉知而无贪，并如实知「先有贪、今无贪」，"
        "以此正知而自记漏尽；异信异欲等不碍此知。保守依汉本早期教理，confidence=medium。"
    ),
}

# --- SA 314 断欲（无平行）----------------------------------------------------
SUTTAS["SA_314"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「当断于欲。眼欲既断，则于眼已断、已知，"
        "根本永绝，犹如截多罗树头，后有永尽，不复更生。」" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「应当断欲。眼欲既断，对眼也就断尽、已知，"
        "根本永绝，像截断多罗树头一样，后有永尽，不再更生。」" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "断欲／断根本／多罗树头不复生——早期定型譬喻；无 SC 巴利主平行，confidence=medium。"
    ),
}

# --- SA 315 眼生（SN 26.1）---------------------------------------------------
SUTTAS["SA_315"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「眼若生起、安住、显现，苦亦生起，病亦安住，老死亦显现。」"
        + SIX_LIT,
        "「眼若息灭、止息、沉没，苦亦息灭，病亦止息，老死亦沉没。」" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「眼若生起、安住、显现，苦也随之生起，病也随之安住，老死也随之显现。」"
        + SIX_MOD,
        "「眼若息灭、止息、沉没，苦也随之息灭，病也随之止息，老死也随之沉没。」" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN26.1（Cakkhu）为 `full` 平行。"
        "据巴利 uppādo/ṭhiti/pātubhāvo 与 nirodho/vūpasamo/atthaṅgamo，"
        "作生起安住显现／息灭止息沉没，与苦、病、老死相对。"
    ),
}

# --- SA 316 眼无常（无平行；据 SN22.59 型校正「欲令如是」）--------------------
SUTTAS["SA_316"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「眼实无常。设眼是常，则无逼迫之苦，亦应得大自在。"
        "以无常故，苦逼于眼，不得自在。」" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「眼实在是无常的。假如眼是常住的，就不会有逼迫之苦，也应当得大自在。"
        "正因为无常，苦才逼迫于眼，不得自在。」" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "据 SN22.59 型校正：底本「欲令如是、不令如是」为欧化拙译，"
        "今作「得大自在／不得自在」。confidence=medium。"
    ),
}

# --- SA 317 眼苦 -------------------------------------------------------------
SUTTAS["SA_317"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「眼实是苦。设眼是乐，则无逼迫之苦，亦应得大自在。"
        "以是苦故，苦逼于眼，不得自在。」" + SIX_LIT,
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「眼实在是苦。假如眼是乐，就不会有逼迫之苦，也应当得大自在。"
        "正因为是苦，苦才逼迫于眼，不得自在。」" + SIX_MOD,
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "同 SA_316 型，标「眼是苦」；「得大自在／不得自在」据 SN22.59 型。confidence=medium。"
    ),
}

# --- SA 318 眼非我 -----------------------------------------------------------
SUTTAS["SA_318"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「眼实非我。设眼是我，则无逼迫之苦，亦应得大自在。"
        "以非我故，苦逼于眼，不得自在。」" + SIX_LIT,
        CLOSE_LIT,
        "（省文）如内六入处说无常、苦、非我三经，外六入处三经，亦如上说。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「眼实在不是我。假如眼是我，就不会有逼迫之苦，也应当得大自在。"
        "正因为非我，苦才逼迫于眼，不得自在。」" + SIX_MOD,
        CLOSE_MOD,
        "（以下是原典的省文指示）如同就内六入处所说无常、苦、非我三经，"
        "就外六入处也可各成三经，如上所说。",
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "同型无我论证；末「外六入处三经亦如是说」为省文指示，如实存为末段，不伪作各别全经。"
        "confidence=medium。"
    ),
}

# --- SA 319 生闻一切（SN 35.23 Sabba）---------------------------------------
SUTTAS["SA_319"] = {
    "lit": [
        OPEN_LIT,
        "时，有生闻婆罗门往诣佛所，共相问讯，退坐一面，白佛言："
        "「瞿昙！所谓一切——云何名一切？」",
        "佛告婆罗门：「一切者，谓十二入处：眼与色、耳与声、鼻与香、舌与味、"
        "身与触、意与法——是名一切。"
        "若有人言：『此非一切；沙门瞿昙所说一切，我今捨之，别立余一切』——"
        "彼唯有言说，问已不知，徒增疑惑。所以者何？非其境界故。」",
        CLOSE_BRAHMIN_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，有生闻婆罗门来见佛，互相问候后退坐一面，问："
        "「瞿昙！所谓『一切』——怎样叫一切？」",
        "佛告诉婆罗门：「一切，就是十二入处：眼与色、耳与声、鼻与香、舌与味、"
        "身与触、意与法——这叫做一切。"
        "若有人说：『这不是一切；沙门瞿昙所说的一切，我今捨掉，另立别的一切』——"
        "他只有空话，问了也不知，徒增疑惑。为什么？因为那不是他的境界。」",
        CLOSE_BRAHMIN_MOD,
    ],
    "notes": (
        f"{PROV}"
        "confidence=high：SN35.23（Sabba）为 `full` 平行。"
        "一切＝十二入处；拒立「余一切」者「非其境界」——据 Pāli／Sujato。"
        "汉本对话者为生闻婆罗门（巴利告诸比丘），场次从汉本，法义据 SN。"
    ),
}

# --- SA 320 一切有（无平行；承 SA_319 框）------------------------------------
SUTTAS["SA_320"] = {
    "lit": [
        OPEN_LIT,
        "时，有生闻婆罗门往诣佛所，问讯已，退坐一面，白佛言："
        "「瞿昙！所谓一切有——云何一切有？」",
        "佛告婆罗门：「我今问汝，随意答我。眼是有不？」"
        "答言：「是有，沙门瞿昙！」"
        "「色是有不？」"
        "答言：「是有！」"
        "「有眼、有色、有眼识、有眼触，及眼触因缘生受——若苦、若乐、不苦不乐不？」"
        "答言：「有！」"
        "耳、鼻、舌、身、意，亦如是问，皆答言有。",
        "「若复有言：『此非一切有；沙门瞿昙所说，我今捨之，别立余一切有』——"
        "彼唯有言说，问已不知，徒增疑惑。所以者何？非其境界故。」",
        CLOSE_BRAHMIN_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，有生闻婆罗门来见佛，问候后退坐一面，问："
        "「瞿昙！所谓『一切有』——怎样叫一切有？」",
        "佛说：「我现在问你，随意回答。眼是有吗？」"
        "答：「是有，沙门瞿昙！」"
        "「色是有吗？」"
        "答：「是有！」"
        "「有眼、有色、有眼识、有眼触，以及依眼触为缘所生的受——苦、乐、不苦不乐——都有吗？」"
        "答：「有！」"
        "耳、鼻、舌、身、意，也同样问，都答有。",
        "「若有人说：『这不是一切有；沙门瞿昙所说，我今捨掉，另立别的一切有』——"
        "他只有空话，问了也不知，徒增疑惑。为什么？因为那不是他的境界。」",
        CLOSE_BRAHMIN_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "承 SA_319『一切』框而问『一切有』；底本末「如是广说乃至非其境界故」为 peyyāla，"
        "今依 SA_319／SN35.23 拒立余说之定型语略补，不演他义。confidence=medium。"
    ),
}

# --- SA 321 一切法（无平行）--------------------------------------------------
SUTTAS["SA_321"] = {
    "lit": [
        OPEN_LIT,
        "时，有生闻婆罗门往诣佛所，问讯已，退坐一面，白佛言："
        "「沙门瞿昙！所谓一切法——云何为一切法？」",
        "佛告婆罗门：「眼及色、眼识、眼触，及眼触因缘生受——若苦、若乐、不苦不乐；"
        "耳、鼻、舌、身、意，法、意识、意触，及意触因缘生受——若苦、若乐、不苦不乐："
        "是名一切法。"
        "若复有言：『此非一切法；沙门瞿昙所说，我今捨之，别立一切法』——"
        "彼唯有言说，问已不知，徒增疑惑。所以者何？非其境界故。」",
        CLOSE_BRAHMIN_LIT,
        "（省文）如生闻婆罗门所问三经，有异比丘所问三经、尊者阿难所问三经、"
        "及世尊自说法眼法根法依三经，亦如上说。",
    ],
    "mod": [
        OPEN_MOD,
        "那时，有生闻婆罗门来见佛，问候后退坐一面，问："
        "「沙门瞿昙！所谓『一切法』——怎样叫一切法？」",
        "佛告诉婆罗门：「眼及色、眼识、眼触，以及依眼触为缘所生的受——苦、乐、不苦不乐；"
        "耳、鼻、舌、身、意，以及法、意识、意触，乃至依意触为缘所生的受——苦、乐、不苦不乐："
        "这叫做一切法。"
        "若有人说：『这不是一切法；沙门瞿昙所说，我今捨掉，另立一切法』——"
        "他只有空话，问了也不知，徒增疑惑。为什么？因为那不是他的境界。」",
        CLOSE_BRAHMIN_MOD,
        "（以下是原典的省文指示）如同生闻婆罗门所问这三经，"
        "异比丘所问三经、阿难尊者所问三经、以及世尊自说法眼法根法依三经，也可如上所说。",
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "『一切法』扩及识、触、触缘生受；拒立余说同 SA_319 定型。"
        "末段异问者／自说三经为省文指示，如实存，不伪作各别全经。confidence=medium。"
    ),
}

# --- SA 322 内外入处分别（无平行；有部分析语）--------------------------------
SUTTAS["SA_322"] = {
    "lit": [
        OPEN_LIT,
        "时，有异比丘往诣佛所，稽首佛足，退坐一面，白佛言："
        "「世尊说眼是内入处，略而不广。云何眼是内入处？」"
        "佛告比丘：「眼内入处者，四大所造净色，不可见，有对。"
        "耳、鼻、舌、身内入处，亦复如是。」",
        "复问：「意是内入处，云何？」"
        "「意内入处者，心、意、识——非色，不可见，无对。是名意内入处。」",
        "复问：「色是外入处，云何？」"
        "「色外入处者，四大所造，可见，有对。是名色外入处。」",
        "复问：「声是外入处，云何？」"
        "「声外入处者，四大所造，不可见，有对。香、味亦尔。」",
        "复问：「触是外入处，云何？」"
        "「触外入处者，四大及四大造色，不可见，有对。是名触外入处。」",
        "复问：「法是外入处，云何？」"
        "「法外入处者，十一入所不摄，不可见，无对。是名法外入处。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，有一位比丘来见佛，稽首佛足，退坐一面，问："
        "「世尊说眼是内入处，只略说未广分别。怎样叫眼是内入处？」"
        "佛说：「眼内入处，是四大所造的净色，不可见，有对。"
        "耳、鼻、舌、身内入处，也是一样。」",
        "又问：「意是内入处，怎样？」"
        "「意内入处，就是心、意、识——非色，不可见，无对。这叫意内入处。」",
        "又问：「色是外入处，怎样？」"
        "「色外入处，是四大所造，可见，有对。这叫色外入处。」",
        "又问：「声是外入处，怎样？」"
        "「声外入处，是四大所造，不可见，有对。香、味也是一样。」",
        "又问：「触是外入处，怎样？」"
        "「触外入处，是四大及四大造色，不可见，有对。这叫触外入处。」",
        "又问：「法是外入处，怎样？」"
        "「法外入处，是十一入所不摄的，不可见，无对。这叫法外入处。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "本经为内外入处之分别定义（净色／有对／无对等），近有部分析语；"
        "无 SC 巴利主平行，不作臆造，仅罗什风重写汉义。confidence=medium。"
    ),
}

# --- SA 323–330 六法身系列 ---------------------------------------------------
# SC 于 323–327、330 标 resembling SN35.60，然汉本仅列名数，与 sabbupādānapariññā
# 全文不相当——以汉本名数为准，不回填 SN35.60 全文。

SUTTAS["SA_323"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「所谓内六者：眼入、耳入、鼻入、舌入、身入、意入。"
        "此名内六入处。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「所谓内六：眼入、耳入、鼻入、舌入、身入、意入。"
        "这就叫内六入处。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "SC 标 SN35.60 为 resembling，然汉本仅列六内入处之名，与 sabbupādānapariññā 全文不相当；"
        "今依汉本名数作罗什风重写，不回填 SN 全文。confidence=medium。"
    ),
}

SUTTAS["SA_324"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「外入处者有六：色、声、香、味、触、法。"
        "如是六法，名为外六入。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「外入处有六种：色、声、香、味、触、法。"
        "这六法，叫做外六入。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "同 SA_323：SC resembling SN35.60，汉本仅列六外入处。confidence=medium。"
    ),
}

SUTTAS["SA_325"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「识身有六：眼识、耳识、鼻识、舌识、身识、意识——"
        "是名六识身。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「识身有六种：眼识、耳识、鼻识、舌识、身识、意识——"
        "这叫做六识身。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "同 SA_323：SC resembling SN35.60，汉本仅列六识身。confidence=medium。"
    ),
}

SUTTAS["SA_326"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「触身有六：眼触、耳触、鼻触、舌触、身触、意触——"
        "是名六触身。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「触身有六种：眼触、耳触、鼻触、舌触、身触、意触——"
        "这叫做六触身。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "同 SA_323：SC resembling SN35.60，汉本仅列六触身。confidence=medium。"
    ),
}

SUTTAS["SA_327"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「受身有六：眼触所生受，乃至意触所生受——"
        "是名六受身。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「受身有六种：眼触所生的受，一直到意触所生的受——"
        "这叫做六受身。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "同 SA_323：SC resembling SN35.60，汉本仅列六受身（触生受）。confidence=medium。"
    ),
}

SUTTAS["SA_328"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「想身有六：眼触所生想，乃至意触所生想——"
        "是名六想身。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「想身有六种：眼触所生的想，一直到意触所生的想——"
        "这叫做六想身。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "六想身（saññā）定型名数；无 SC 巴利主平行。confidence=medium。"
    ),
}

SUTTAS["SA_329"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「思身有六：眼触所生思，乃至意触所生思——"
        "是名六思身。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「思身有六种：眼触所生的思，一直到意触所生的思——"
        "这叫做六思身。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{NO_PARALLEL}"
        "六思身（cetanā）定型名数；无 SC 巴利主平行。confidence=medium。"
    ),
}

SUTTAS["SA_330"] = {
    "lit": [
        OPEN_LIT,
        "尔时，世尊告诸比丘：「爱身有六：眼触所生爱，乃至意触所生爱——"
        "是名六爱身。」",
        CLOSE_LIT,
    ],
    "mod": [
        OPEN_MOD,
        "那时，世尊告诉比丘们：「爱身有六种：眼触所生的爱，一直到意触所生的爱——"
        "这叫做六爱身。」",
        CLOSE_MOD,
    ],
    "notes": (
        f"{PROV}"
        "同 SA_323：SC resembling SN35.60，汉本仅列六爱身（触生爱）。confidence=medium。"
        "与 SA_304『六六』中六爱身名数相应，不回填 sabbupādānapariññā 全文。"
    ),
}

# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

CONFIDENCE: dict[str, str] = {
    "SA_311": "high",
    "SA_312": "high",
    "SA_313": "medium",
    "SA_314": "medium",
    "SA_315": "high",
    "SA_316": "medium",
    "SA_317": "medium",
    "SA_318": "medium",
    "SA_319": "high",
    "SA_320": "medium",
    "SA_321": "medium",
    "SA_322": "medium",
    "SA_323": "medium",
    "SA_324": "medium",
    "SA_325": "medium",
    "SA_326": "medium",
    "SA_327": "medium",
    "SA_328": "medium",
    "SA_329": "medium",
    "SA_330": "medium",
}

# 本批无「唯交叉指示、须回填全文」之经；省文指示如实存为末段。
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
    assert set(GOLD) == {f"SA_{i}" for i in range(311, 331)}, (
        "GOLD must cover SA_311–SA_330 exactly"
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

    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    web = ROOT / "web" / "public" / "final_translated_data.json"
    if web.parent.exists():
        web.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "data" / "translated" / "validation_report_sa311-330.json").write_text(
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

    print(f"merged total={len(merged)} retranslated={len(GOLD)} (SA_311–SA_330 only)")
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
