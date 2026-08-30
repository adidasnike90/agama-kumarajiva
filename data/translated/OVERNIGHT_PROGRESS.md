# Overnight gold progress

## Map
- **Continuous gold:** SA 1–1362 (no gaps) — **100%** of corpus
- **Status:** gold=1146 / gold_reconstructed=216
- **Full audit:** `data/translated/GOLD_AUDIT.md`（2026-08-26；P0=0 P1=0；白话=罗什风 0）
- **Audit:** `translate/quality_gate.py`；`python scripts/audit_gold_corpus.py` 可复跑

## Latest completed
- SA 1351–1362（林相应末：孔雀～鸽鸟）—
  `scripts/retranslate_sa1351_1362.py`, ok=12 warn=0 fail=0; gold=12;
  sim max=0.394 mean=0.286; confidence medium=12（SC 无专经平行）
- SA 1331–1350（林相应：不乐～波吒利）—
  `scripts/retranslate_sa1331_1350.py`, ok=20 warn=0 fail=0; gold=19 / gold_reconstructed=1;
  sim max=0.272 mean=0.161; needs_restyle=0; confidence high=13 medium=7;
  SA_1330_untouched / SA_1351_untouched; SA_1341 据 SN9.5 重构（汉「偏持戒」异叙事）
- SA 1311–1330（杂相应末＋夜叉相应：昙摩～害及无害）—
  `scripts/retranslate_sa1311_1330.py`, ok=20 warn=0 fail=0; gold=15 / gold_reconstructed=5;
  sim max=0.316 mean=0.116; confidence high=18 medium=2
- SA 1291–1310（杂相应续：火不烧～照明）—
  `scripts/retranslate_sa1291_1310.py`, ok=20 warn=0 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.357 mean=0.269; confidence high=12 medium=8
- SA 1271–1290（杂相应：四句法经～大地）—
  `scripts/retranslate_sa1271_1290.py`, ok=16 warn=4 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.345 mean=0.161; needs_restyle=0
- SA 1251–1270（譬喻相应／杂相应起：那提迦、枕木、釜、爪土、野狐）—
  `scripts/retranslate_sa1251_1270.py`, ok=16 warn=4 fail=0; gold=15 / gold_reconstructed=5;
  sim max=0.402 mean=0.215; needs_restyle=0
- SA 1231–1250（刹利相应末＋譬喻起：捕鱼、祠祀、繁缚）—
  `scripts/retranslate_sa1231_1250.py`, ok=20 warn=0 fail=0; gold=16 / gold_reconstructed=4;
  sim max=0.263 mean=0.118; needs_restyle=0
- SA 1211–1230（比丘尼相应末＋刹利起：龙胁、自恣、欲结、出离、鹿穽）—
  `scripts/retranslate_sa1211_1230.py`, ok=20 warn=0 fail=0; gold=16 / gold_reconstructed=4;
  sim max=0.198 mean=0.111; confidence high=18 medium=2
- SA 1191–1210（梵天相应末＋比丘尼／婆耆舍：空闲处、瞿迦黎、婆迦梵）—
  `scripts/retranslate_sa1191_1210.py`, ok=20 warn=0 fail=0; gold=12 / gold_reconstructed=8;
  sim max=0.147 mean=0.058; confidence high=20
- SA 1171–1190（六入处相应续：六种众生、毒蛇、苦法、树）—
  `scripts/retranslate_sa1171_1190.py`, ok=20 warn=0 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.282 mean=0.119; confidence high=17 medium=3
- SA 1151–1170（婆罗门相应＋六入处：阿修罗盐、瞋骂、返戾、婆私吒；波罗延、宾头卢、
  手足喻、龟、祺麦、琴、癞疮）—
  `scripts/retranslate_sa1151_1170.py`, ok=18 warn=2 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.292 mean=0.142; needs_restyle=0
- SA 1031–1050（业报相应：给孤独、达摩提离、长寿、淳陀、舍行、生闻、鞞闻摩、
  鞞纽多罗、随类、蛇行、圆珠、徒生、出不出）—
  `scripts/retranslate_sa1031_1050.py`, ok=20 warn=0 fail=0; gold=8 / gold_reconstructed=12;
  sim max=0.268 mean=0.14; confidence high=15 medium=5
- SA 1011–1030（诸天续＋业报起：覆、无明、信、生世间；叵求那、疾病、给孤独）—
  `scripts/retranslate_sa1011_1030.py`, ok=20 warn=0 fail=0; gold=15 / gold_reconstructed=5;
  sim max=0.366 mean=0.215; confidence high=17 medium=3
- SA 991–1010（诸天相应：鹿住、延清、阿练、憍慢、修福、种子、意、缚…）—
  `scripts/retranslate_sa991_1010.py`, ok=20 warn=0 fail=0; gold=13 / gold_reconstructed=7;
  sim max=0.307 mean=0.200; confidence high=18 medium=2
- SA 971–990（杂相应：上坐、尸婆、幢、阿难舍利弗、爱、帝释、鹿住）—
  `scripts/retranslate_sa971_990.py`, ok=20 warn=0 fail=0; gold=17 / gold_reconstructed=3;
  sim max=0.245 mean=0.132; confidence high=11 medium=9
- SA 951–970（婆蹉外道末＋杂相应起：无记／见／出家；舍罗步）—
  `scripts/retranslate_sa951_970.py`, ok=20 warn=0 fail=0; needs_restyle=0;
  sim max=0.389 mean=0.208
- SA 931–950（释氏相应末＋婆蹉外道相应起：六念／十一／十二／学无学、含罗／麤手、
  血泪母乳；土丸、豆粒、喜乐、苦恼、恐怖、彼爱、恒河、骨聚、城、山、过去）—
  `scripts/retranslate_sa931_950.py`, ok=19 warn=1 fail=0; gold=19 / gold_reconstructed=1;
  needs_restyle=0; sim max=0.393 mean=0.210; confidence high=19 medium=1;
  SA_930_untouched / SA_951+_untouched
- SA 911–930（聚落主末＋释氏相应：顶发、王发、驴姓、饥馑、种田、说何论、恶马、
  順調马；贤乘、鞭影、乘调、迦旃延、优婆塞、得果、一切行、自轻）—
  `scripts/retranslate_sa911_930.py`, ok=20 warn=0 fail=0; needs_restyle=0;
  sim max=0.378 mean=0.155
- SA 891–910（湖池、入界阴、不坏净、聚落主起）—
  `scripts/retranslate_sa891_910.py`, ok=20 warn=0 fail=0; gold=17 / gold_reconstructed=3;
  sim max=0.549 mean=0.215; confidence high=13 medium=7
- SA 871–890（天相应末＋修证相应：风云天、四正断、不放逸、四禅、三明、无为法）—
  `scripts/retranslate_sa871_890.py`, ok=20 warn=0 fail=0; gold=17 / gold_reconstructed=3;
  sim max=0.379 mean=0.303; confidence high=13 medium=7
- SA 851–870（法镜／难提／田业 → 天相应）—
  `scripts/retranslate_sa851_870.py`, ok=20 warn=0 fail=0; gold=12 / gold_reconstructed=8;
  sim max=0.396 mean=0.260; confidence high=9 medium=11
- SA 831–850（学相应：戒、三学、离车、不坏净、天道）—
  `scripts/retranslate_sa831_850.py`, ok=20 warn=0 fail=0; gold=16 / gold_reconstructed=4;
  sim max=0.300 mean=0.182; confidence high=15 medium=4 low=1
- SA 811–830（安那般那末＋学相应起：阿难、金毘罗、不疲、布萨；学／涅槃／尸婆迦等）—
  `scripts/retranslate_sa811_830.py`, ok=20 warn=0 fail=0; gold=17 / gold_reconstructed=3;
  sim max=0.386 mean=0.256; confidence high=16 medium=4
- SA 791–810（圣道分末＋安那般那念相应起：邪正／顺流逆流、沙门果、饶益、一明、
  断觉想、阿黎瑟吒、罽宾那、一奢能伽罗、迦摩、福利、金刚）—
  `scripts/retranslate_sa791_810.py`, ok=20 warn=0 fail=0; needs_restyle=0;
  sim max=0.451 mean=0.265
- SA 771–790（彼岸、一法、非法是法、断贪、邪正、向邪、生闻）—
  `scripts/retranslate_sa771_790.py`, ok=20 warn=0 fail=0; gold=12 / gold_reconstructed=8;
  sim max=0.392 mean=0.214; confidence high=13 medium=7
- SA 751–770（圣道分：起、迦摩、阿黎吒、舍利弗、三法、学、正士、漏尽、修／清净、
  聚、半、婆罗门、邪）—
  `scripts/retranslate_sa751_770.py`, ok=20 warn=0 fail=0; gold=15 / gold_reconstructed=5;
  sim max=0.382 mean=0.234; confidence high=13 medium=7
- SA 731–750（觉支末→圣道分起：支节、七道品、果报、不净观、死念、慈、安那般那念、
  无常；日出、无明）—
  `scripts/retranslate_sa731_750.py`, ok=20 warn=0 fail=0; gold=8 / gold_reconstructed=12;
  sim max=0.377 mean=0.245; confidence high=18 medium=2
  - 748 如理作意为前相（校正汉「正见」）
- SA 711–730（觉支相应 卷二十八末–二十九：无畏、转趣、火、食、一法、比丘、优波摩、
  阿那律、转轮王、年少／果报、不善聚、善知识、拘夷那竭、说、灭、分）—
  `scripts/retranslate_sa711_730.py`, ok=20 warn=0 fail=0; gold=20;
  sim max=0.347 mean=0.166; needs_restyle=0
- SA 691–710（根力末＋觉支起：七力、八力、九力、王力、如来力；不正思惟、不退、盖、
  障盖、木封、七觉支、听法）—
  `scripts/retranslate_sa691_710.py`, ok=20 warn=0 fail=0; gold=11 / gold_reconstructed=9;
  sim max=0.387 mean=0.211; confidence high=15 medium=5
  - 710「不得不乐」→「不得厌离」；觉支次第据 SN（喜先于猗）
- SA 671–690（根力相应 卷二十七末–二十八：四力、五力、当知、学力、白法／不善法、
  十力、乳母、师子吼、七力）—
  `scripts/retranslate_sa671_690.py`, ok=20 warn=0 fail=0; gold=7 / gold_reconstructed=13;
  sim max=0.42 mean=0.27; confidence high=16 medium=4
  - 686–687 第二力据 AN6.64 改「诸业因缘果报」
- SA 651–670（卷第二十七 根力相应续：沙门婆罗门、成×2、堂阁、信、二力／三力／四力、摄）—
  `scripts/retranslate_sa651_670.py`, ok=20 warn=0 fail=0; gold=12 / gold_reconstructed=8;
  sim max=0.372 mean=0.247; confidence high=12 medium=8
  - 661「数力」→思择力；659「发菩提心」→于如来一向净信
- SA 631–650（念处末＋阿育王传×2＋根力相应起：行／一切法、贤圣、光泽、波罗提木叉、
  纯陀、布萨；学、净、须陀洹、阿罗汉、当知、广说、略说、漏尽、沙门婆罗门）—
  `scripts/retranslate_sa631_650.py`, ok=18 warn=2 fail=0; gold=20;
  sim max=0.358 mean=0.197; confidence high=13 medium=5 low=2
  - warn：640／641 Aśokavadāna 压缩（low）
- SA 611–630（卷第二十六 念处相应：善聚、弓、不善聚、大丈夫、比丘尼、厨士、鸟、四果、
  私迦陀、猿猴、年少比丘、菴罗女、世间、郁低迦、婆醯迦、比丘、阿那律、优陀夷、行×2）—
  `scripts/retranslate_sa611_630.py`, ok=20 warn=0 fail=0; gold=20;
  sim max=0.328 mean=0.175; needs_restyle=0
- SA 591–610（卷第二十五天相应末＋念处相应起：输波罗、须达／生天、首长者、无烦天、
  常惊、颜色、睡眠、髻发、极难尽、池水、伊尼延、流、阿育王传、念处×2、净、甘露、集、正念）—
  `scripts/retranslate_sa591_610.py`, ok=19 warn=1 fail=0; gold=20;
  sim max=0.394 mean=0.262; needs_restyle=0
- SA 571–590（质多罗末＋天相应起：摩诃迦、系、阿鲁毗迦、尼乾、病相；欢喜园、钩锃、
  惭愧、不善知、善调、罗汉×2、月天子、手杻、独一住、利剑、天女、四转轮、罗吒园、古客）—
  `scripts/retranslate_sa571_590.py`, ok=20 warn=0 fail=0; gold=17 / gold_reconstructed=3;
  sim max=0.476 mean=0.360; confidence high=19 medium=1
  - reconstr.：573／575／590（peyyāla 压缩）
- SA 551–570（卷第二十三–二十四 大迦旃延／阿难／质多罗：诃梨×5、无相三昧、阇知罗、
  迦摩禅支、度量、四神足、瞿师多、尼犍、比丘尼、婆头、那迦达多、黎犀达多）—
  `scripts/retranslate_sa551_570.py`, ok=19 warn=1 fail=0; gold=19 / gold_reconstructed=1;
  sim max=0.365 mean=0.239; confidence high=10 medium=9 low=1
  - reconstr.：555（诃梨 peyyāla）；559/564 Doctrine 校正后过门禁
- SA 531–550（卷第二十一末–卷第二十三：牛车、呵责、恶口、诤讼、独一×2、松林／所患、
  尽诸漏、阿罗汉、何故出家、澡灌杖、执杖、摩偷罗、迦梨、迦旃延）—
  `scripts/retranslate_sa531_550.py`, ok=20 warn=0 fail=0; gold=19 / gold_reconstructed=1;
  sim max=0.453 mean=0.355; confidence high=15 medium=5
  - reconstr.：540（三种譬 cross-ref）；531–534 SN19 业报；535–545 阿那律念处；546–550 大迦旃延
- SA 491–510（卷第二十 舍利弗／目连／弟子所说：沙门出家所问、泥水、乘船逆流、枯树、戒、静、
  举罪、那罗犍陀、石柱、净口、圣默然、无相、寂灭、爱尽×2、帝释、天、屠牛系列）—
  `scripts/retranslate_sa491_510.py`, ok=19 warn=1 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.317 mean=0.224; confidence high=11 medium=8 low=1
  - reconstr.：491（peyyāla→SN39.1–15）、504（卷次错乱／帝释偈）
  - 501–503 目连默然／无相／心通问舍利弗
- SA 511–530（卷第二十一 弟子所说：屠羊、堕胎、调象、好战、杀猪、断人头、锻铜、捕鱼、
  卜占、卖色、瞋恚、盗果／石蜜／二饼、比丘尼等）—
  `scripts/retranslate_sa511_530.py`, ok=20 warn=0 fail=0; gold=20;
  sim max=0.353 mean=0.294; confidence high=14 medium=5 low=1
  - SN19 目连地狱观系列；523 卖色保留全对话；529 无 SC 平行→low
- SA 471–490（卷第十九受相应末＋卷第二十舍利弗相应起：虚空、客舍、禅／止息、先时、禅思、
  交叉指示、比丘、如实知、沙门婆罗门、壹奢能伽罗、喜乐、无食乐、跋陀罗、优陀夷、一法×4、难等）—
  `scripts/retranslate_sa471_490.py`, ok=15 warn=5 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.399 mean=0.303; confidence high=10 medium=10
  - 472/473/476/479 罗什栏对齐巴利，lit_mod_gap 清零；490 难等（SN38.16 起，四十问序）
- SA 451–470（卷第十八／十九 界／受：界、触、受、想×2、正受、说、因、自作、瞿师罗、三界×3、
  上座名者、著使、触因、剑刺、三受、深嶮、箭）—
  `scripts/retranslate_sa451_470.py`, ok=20 warn=0 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.388 mean=0.304; confidence high=14 medium=6
  - 箭经（SN36.6）二箭／身受心受；火钻譬（466）；厌故离贪
- SA 431–450（卷第十七／十八：杖、五节、增上说法、黠慧、须达多、殿堂×2、虫、山、湖池、土、爪甲、
  四圣谛当生来生、眼药丸、鄙心、偈×2、行、界和合、少闻等）—
  `scripts/retranslate_sa431_450.py`, ok=20 warn=0 fail=0; gold=14 / gold_reconstructed=6;
  sim max=0.381 mean=0.217; confidence high=13 medium=7
- SA 411–430（卷第十七 界相應／谛相应：论、争、大力、宿命、说论、受持×2、如如、疑×2、
  深嶮、大热、大闇、千明、千世界×2、四圣谛、禅思、三摩提、杖）—
  `scripts/retranslate_sa411_430.py`, ok=20 warn=0 fail=0; gold=16 / gold_reconstructed=4;
  sim max=0.382 mean=0.250; confidence high=12 medium=8
  - 「如如」→如实不虚不异；大闇地狱→世界中间大闇；杖经据 SN56.33 改流转
- SA 391–410（卷第十六／十七 諦相應续／界相應首：沙门婆罗门、如实知、善男子、日月×3、
  佉提罗、因陀罗柱、论处、衣、百枪、平等正觉、如实知、申恕林、孔、龟、思惟×2、觉×2）—
  `scripts/retranslate_sa391_410.py`, ok=17 warn=3 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.322 mean=0.181; confidence high=19 medium=1
  - reconstr.：391（广说如上）、410（亲里／国土／不死觉）
  - 信-校正：394 前相＝正见；397 四谛皆现观；404 厌故离贪
- SA 371–390（卷第十六 食相應／諦相應：食、颇求那、子肉、有贪×5、转法轮、四圣谛×2、
  当知、已知、漏尽、边际、无有关键×2、五支六分、大医王、沙门婆罗门）—
  `scripts/retranslate_sa371_390.py`, ok=20 warn=0 fail=0; gold=18 / gold_reconstructed=2;
  sim max=0.387 mean=0.284; confidence high=10 medium=10
  - gold_reconstructed：373（须深交叉→SN12.63 三矛纲）、376（如前广说）
  - 374–378 各留异喻，不五通克隆；371 据 SN12.11 补缘起上溯
- SA 351–370（卷第十四／十五 因緣相應：茂師羅、沙門婆羅門×3、老死、種智×2、無明增、思量×3、
  多聞、說法／次法／見法般涅槃、毗婆尸等、修習、三摩提、十二因緣×2）—
  `scripts/retranslate_sa351_370.py`, ok=20 warn=0 fail=0; gold=19 / gold_reconstructed=1;
  sim max=0.395 mean=0.267; confidence high=15 medium=4 low=1
  - 信-校正：SA 358 据 SN12.37 Natumha 改写；359–361 补三思量；厌故离贪（362／365）
  - gold_reconstructed：SA 370（如前广说）
- SA 331–350（卷第十三／十四：六顧念、六覆、過去、有縛法、第一義空、六喜／憂／捨行、
  六常行×4、浮彌、拘絺羅、集生、三法、須深、十力、聖處、聖第子）—
  `scripts/retranslate_sa331_350.py`, ok=20 warn=0 fail=0; gold=20;
  sim max=0.387 mean=0.294; confidence high=6 medium=14
  - high：333（SN35.10）、343（SN12.24）、345（SN12.31）、347（SN12.70）、348（SN12.22）、350（SN12.49）
  - 信-校正：第一义空＝早期空（无如来藏）；「真实」→「已生」+厌故离贪（345）；须深法住智→涅槃智压缩
- P2 高 sim 轻修（15 条）：SA 33–34、38、43–44、67、76、78、84–85、194、235–237、242
  — sim 0.46–0.55 → 0.19–0.37；另 SA 308 据 SN35.136 再收（0.456→0.123）
- SA 311–330（卷第十二／十三 因緣相應续：富樓那、摩羅迦舅、經法、斷欲、眼生、
  眼是常／樂／我、生聞一切×3、眼是內入處、六內／外／識／觸／受／想／思／愛）—
  `scripts/retranslate_sa311_330.py`, ok=20 warn=0 fail=0; gold=20 / gold_reconstructed=0;
  sim max=0.395 mean=0.320; confidence high=4 medium=16
  - high：311（SN35.88）、312（SN35.95）、315（SN26.1）、319（SN35.23）
  - 信-校正：nandī→耽喜集／苦集（SA 311）；「欲令如是」→「得大自在」（316–318）
  - 323–330 名目表不回填 SN35.60 全文
- **Quality repair（2026-08-26）：** 据巴利／Sujato 重写，非繁转简。
  - P1 长经：SA 46（SN22.79）、271（SN22.84）、272（SN22.80）、285（SN12.10）
  - P0「厌故不乐」→「厌故离贪」：SA 81–82、124–125、127、186、289
  - needs_restyle 清零：SA 275（AN8.9）、278（SN35.96）、279（SN35.94）、280（MN150）
    sim 0.40–0.46 → 0.10–0.18
  - SA 273 罗什栏重写（sim 0.52→0.26）
- SA 291–310（卷第十二 因緣相應续：触法、思量观察、甚深、愚痴黠慧、非汝所有、因缘法、
  大空法、法说义说、缘起法、他、迦旃延、阿支罗、玷牟留、六六、六入处、人、见法、
  不染著、鹿纽×2）—
  `scripts/retranslate_sa291_310.py`, ok=19 warn=1 fail=0; gold=17 / gold_reconstructed=3;
  confidence high=14, medium=6
  - 本批以 SC 平行及 `raw_aligned_data.json` 内巴利／Sujato 厘义；SN 12 平行往往可据。
  - confidence 判准：
    - **high（14）**：SC `full` 平行逐句覆盖正文——SA 291（SN12.66）、292（SN12.51）、
      294（SN12.19）、296（SN12.20）、297（SN12.35–36）、298（SN12.1–2）、
      300（SN12.46）、301（SN12.15）、302（SN12.17）、303（SN12.18）、
      304（SN35.60／MN148）、308（SN35.136）、309（SN35.63）、310（SN35.64）。
    - **medium（6）**：SA 293／299／295（无 SC 平行）、305（MN149）、306／307（如上广说 peyyāla）。
  - 主要 信-校正：
    - 「内触法」→内察（sammasana）；「亿波提」→有支（upadhi）（SA 291）
    - 思量观察逆观取→爱→受→触→六入→名色→识→行→无明（SA 292）
    - 因缘法／缘生法、法住法界（SA 296）；大空法命身二见与中道（SA 297）
    - 缘起法说／义说各支定义（SA 298）；自作他作无记（SA 300）
    - 迦旃延有無二依、不取不住（SA 301）；阿支罗四问苦皆无记、牛触杀授记（SA 302）
    - 六六法非我、六分别六入染著／如实知（SA 304–305）
    - 染著六境则苦／集灭味患离则涅槃（SA 308）；第二住／一一住（SA 309–310）
  - gold_reconstructed（3）：SA 303（广说如阿支罗经）、306／307（眼色二法 peyyāla）。
- SA 271–290（卷第十一 陰相應续／卷第十二 因相應首：低舍、诸想、手声喻、弃舍、难陀×2、
  律仪、退不退、调伏、频头城、萦发目犍连、诸根修、种树、大树、佛缚、取、城邑、芦、无闻×2）—
  `scripts/retranslate_sa271_290.py`, ok=20 warn=0 fail=0; gold=16 / gold_reconstructed=4;
  confidence high=15, medium=5
  - Anālayo Fascicle 11（DDJBS 12, 2013）涵盖 SA 271–272；本批余经以 SC 平行及巴利／Sujato 厘义。
  - confidence 判准：
    - **high（15）**：SC `full` 平行逐句覆盖正文——SA 271（SN22.84）、272（SN22.80）、
      273（SN35.92–93）、274（SN35.101）、277（SN35.97）、278（SN35.96）、279（SN35.94）、
      280（MN150）、281（SN46.6）、282（MN152）、283（SN12.57）、284（SN12.56）、
      285（SN12.10）、288（SN12.67）、290（SN12.62）。
    - **medium（5）**：SA 275（AN8.9 增支部）、276（Tibetan parallel + 篋毒蛇交叉指示）、
      286／287（如上广说 peyyāla）、289（SN12.61／EA9.4 resembling）。
  - 主要 信-校正：
    - 低舍＝ Tissa；二路譬汉本左右次序与巴利有异，存汉本而 notes 志之（SA 271）
    - 「诸想」：三不善觉由想起／四念处无相三昧（SA 272）；卷末摄颂不入正文
    - 手声喻：诸行如幻如炎＝阳焰；二法＝眼色等（SA 273）
    - 难陀（Nanda）关根／知量／昼夜／正念（SA 275）；教尼之难陀另经（SA 276）
    - 目犍连问外道竞论→七觉→四念→三妙行→六入律仪（SA 281）
    - 诸根修：波罗奢那「眼不见色」非修根；五句厌不厌俱舍（SA 282）
    - 种树／大树譬配缘起集灭（SA 283–284）；佛缚灯譬（SA 285）；薪火譬（SA 286）
    - 三芦譬：识名色展转相依（SA 288）；猕猴譬＋触集受集（SA 289–290）
  - gold_reconstructed（4）：SA 276（篋毒蛇广说）、282（篋毒蛇广说末段）、
    286（依 SA 285 如上广说）、287（逆缘起广说 peyyāla）。
- SA 256–270（卷第十一 陰相應：無明×3、世間苦、滅、富留那、闡陀、應說、小土塼、泡沫、無知×2、河流、祇林、樹）—
  `scripts/retranslate_sa256_270.py`, ok=14 warn=1 fail=0; gold=15 / gold_reconstructed=0;
  confidence high=14, medium=1
  - Anālayo Fascicle 11（DDJBS 12, 2013）涵盖本批；SN 22 平行往往可据。
  - confidence 判准：
    - **high（14）**：SC `full` 平行逐句覆盖正文——SA 256（SN22.127）、257（SN22.135）、
      258（SN22.131）、259（SN22.122）、261（SN22.83）、262（SN22.90）、263（SN22.101）、
      264（SN22.96）、265（SN22.95）、266（SN22.99）、267（SN22.100）、268（SN22.93）、
      269（SN22.33）、270（SN22.102）。
    - **medium（1）**：SA 260（灭）— SC 未列平行，阿难／舍利弗问答式同无明系列，唯以汉本厘义。
  - 主要 信-校正：
    - 「无常、磨灭、生灭」→「集起法、灭没法、集起灭没法」（samudayadhamma／vayadhamma，SA 256，据 SN22.127）
    - 「无间等」→「现观」（abhisamaya）（SA 256–259）
    - 「野马」→「阳焰」（marīci，SA 265）
    - 阐陀所疑：知无常无我而不能信入诸行息止，以中道缘起得法眼净（SA 262，SN22.90／SN12.15）
    - 「生法计是我」＝于 jāti 计为我（SA 261）
    - 小土块譬：无常住之 self（SA 264）；转轮王资具罗什式压缩
  - SA 256 validation warn：`mark_not_in_output:无常` 为依平行改作「集起／灭没」之预期结果，非繁转简。
  - 卷末摄颂「输屡那三种……」及 SA 262 末 paratext 不入正文。
- SA 251–255（卷第十 六入處相應尾）— `scripts/retranslate_sa251_255.py`, ok=5 warn=0 fail=0;
  gold=5; confidence high=5; max_sim=0.359
  - SA_251 六触入处无明／明（cf. MA211）；「无间等」→「现观」
  - SA_252 优波先那蛇毒（SN35.69）；无我故色貌不变；蛇护偈汉本增
  - SA_253 毗纽迦旃延尼中道（SN35.133）；「非时」=不敬法；苦乐异生
  - SA_254 二十亿耳弹琴喻（AN6.55）；六解脱
  - SA_255 鲁醯遮门义（SN35.132）；迦旃延说真婆罗门

- SA 231–250（卷第十 六入處相應：三弥离提、世间、世间边、近住、清净乞食住、毗舍离、因、结法、取法、烧、知、味等、魔钩、四法品、七年、魔、纯陀、拘絺羅）—
  `scripts/retranslate_sa231_250.py`, ok=20 warn=0 fail=0; gold=20 / gold_reconstructed=0;
  confidence high=11, medium=9
  - Anālayo Fascicle 8 止于 SA 229；本批以 SC 平行及 `raw_aligned_data.json` 内巴利／Sujato 厘义。
  - confidence 判准：
    - **high（11）**：SC `full` 平行逐句覆盖正文——SA 231（SN35.82 lujjati）、234（SN35.116）、
      235（SN35.151 Antevāsika）、236（MN151）、239／240（SN35.109／110）、241（SN35.235 Āditta）、
      242（SN35.111／112）、246（SN4.24）、249（AN4.173）、250（SN35.232）。
    - **medium（9）**：平行框式或量不合——SA 232（SN35.85 问者为阿难、空义语面异）、
      233（SC 列 SN12.44 而汉本合 SN35.107）、237（SN35.118 框式异）、238／247／248（无平行）、
      243／244／245（汉本省文或缺 Fisherman 譬）。
  - 主要 信-校正：
    - 「危脆败坏」→「败坏崩坏」（lujjati 语源释 loka）（SA 231）
    - 「常恒不变易法空」→「于我与我所空」（SN35.85）（SA 232）
    - 「究竟苦集」→「究竟苦边」（dukkhakkhayāya）（SA 235）
    - 「有師有近住弟子」→「有近住弟子、有教者」（antevāsika／ācariyaka，非人间之师）（SA 235）
    - 「恩爱」→「贪爱」；「上座禅」＝ thero vihāra（SA 236）
    - 「不知不识不断不离欲」→「证知、遍知、离贪、断舍」（SA 242，沿 SA 190）
    - 「厌故不乐」→「厌故离贪」（virāga）（SA 241）
    - 二牛轭譬：中间 chandarāgo 为系（SA 250）
  - 省文摄记如实保留：SA 237（长者／阿难／佛说三经）、242（眼四经乃至意二十四经）、
    243（味等七经×内外）、244（秽说净说）、247（习近等系列）、不伪作全文。

- SA 221–230（卷第九末／卷第十首 六入處相應：取、智识×2、断×2、计×2、增长、有漏无漏、三弥离提）—
  `scripts/retranslate_sa221_230.py`, ok=10 warn=0 fail=0; gold=10 / gold_reconstructed=0;
  confidence high=5, medium=5
  - 汉本取自 `raw_aligned_data.json`；SA 221–229 用 Anālayo Fascicle 8（DDJBS 18, 2016），
    SA 230 该篇已止，改依 SN 35.65–68。
  - confidence 判准：
    - **high（5）**：SC `full` 平行逐句覆盖正文——SA 224（SN35.24）、225（SN35.25，resembling
      因同组非疑法义）、226／227（SN35.90／35.91）、230（SN35.68 世间；省文摄 35.65 魔、35.66 众生）。
    - **medium（5）**：SC 未列平行（SA 221／228／229）；或所列 SN35.26／35.27 为四支
      「证知、遍知、离贪、断舍」（已用于 SA 190／191），而本经唯「知／识」二支（SA 222／223）。
  - 主要 信-校正：
    - 「取所取故」→「是故有取及所取」（upādāna 与 upādāniya）（SA 221）
    - 「不知不见」→「不知、不识」（经题智识；Anālayo 二处同读）（SA 223）
    - 「欲法」存汉本，志巴利 sabba（一切）之异（SA 224）
    - 「不计我见色」→「不计见色为我」；「乐我」之「乐」＝ nandati（乐着）非乐受（SA 226）
    - 「计者是病、痈、刺」＝ ejā rogo／gaṇḍo／salla；「计」＝ maññati（SA 227）
    - 「处变易法」之「处」＝ ṭhita（住而变易），非十二处（SA 228）
    - 无漏唯出世间意门，不补五色根（SA 229）
    - 「设施世间」＝ lokapaññatti；正文问世间＝ SN35.68，省文众生／魔，阙苦一经不补（SA 230）
  - SA 228「触缘受……广说乃至」依同卷 SA 218 缘起定型补中间诸支以便达，非整篇交叉指示，
    故不标 `gold_reconstructed`。省文摄记（226／227／228／230 末段）如实保留，不伪作全文。
  - 卷题 paratext 不入正文：SA 229 末「杂阿含经卷第八」、SA 230 首「杂阿含经卷第九」。

- SA 201–220（卷第九 六入處相應 次段）— `scripts/retranslate_sa201_220.py`, ok=20 warn=0 fail=0;
  gold=19 / gold_reconstructed=1（SA 207）; confidence high=11, medium=9
  - 脚本于 Claude 额度耗尽前已写完；本机修「婆罗门」笔误后跑通 merge
  - 信-校正要点：SA_202/220 底本「无常」→「非我」；SA_210「莫乐莫苦」→「有大苦、有大乐」；
    SA_213「身触」→「身结」；SA_214 触则受/思/想并列（非次第）；SA_211「有余之说」→「约六入处灭而说」

- SA 188–200（卷第九 六入處相應 首段）— `scripts/retranslate_sa188_200.py`, ok=13 warn=0 fail=0;
  gold=12 / gold_reconstructed=1（SA 200）; confidence high=9, medium=3, low=1
  - **本批与前批（斷知相應）之根本差别：平行可据。** SC 于十三经全列巴利平行，且
    `raw_aligned_data.json` 内已备巴利本文、Sujato 英译，及 Anālayo 之 SA 英译
    （'On the Six Sense-spheres (1) — A Translation of Saṁyukta-āgama Discourses 188 to 229
    (Fascicle 8)', DDJBS 18, 2016）。故本批得以巴利厘义，confidence 不再全批压为 medium。
  - confidence 判准（逐经列于脚本 `CONFIDENCE`）：
    - **high（9）**：SC 所列 `full` 平行之巴利本文／英译逐句覆盖本经正文
      （SA 188／189／190／191／194／196／197／198／199）。
      其中 SA 188／189／196 之 SC 标 `resembling`，然细核其犹疑在于 SN35.153–158、
      SN35.33–52 各为一组语面几同之经、难定一一之对，非疑法义；所据之句巴利逐字可对，
      故不因该标降级，并于 notes 具志此判断。
    - **medium（3）**：SA 192／193——SC 列 SN35.21／35.22（Dukkhuppāda）为平行，然彼说
      「眼之生住现起即苦之生、病之住、老死之现起」，与本经「不离欲、心不解脱则不堪任尽苦」
      实不相当；SA 195——SC 列 SN35.1–12（唯举六处，无「色、识、触、触缘生受」之六六列），
      与本经「一切无常」之量不合，实际同式者为 SN35.43–51（SC 系于次经 SA 196 名下），
      因所据平行係本篇另行认定，依 SA_123 之例降为 medium。
    - **low（1）**：SA 200，见下 `gold_reconstructed`。
  - 主要 信-校正：
    - 「当正观察眼无常」→「眼实无常，观眼无常，是名正见」：巴利 `aniccaṁyeva … cakkhuṁ`
      为直陈（眼实是无常，见其无常故名正见），非劝令式（SA 188）
    - 「离喜、离贪」平列 → 复其互摄式「喜尽则贪尽，贪尽则喜尽；喜贪俱尽」
      （`nandikkhayā rāgakkhayo; rāgakkhayā nandikkhayo`）；「心正解脱」→「心善解脱」
      （suvimutta）（SA 188／189）
    - 「正思惟」→「如理作意」：实译 `yoniso manasi karotha`（yoniso manasikāra），
      与八正道之「正志」（sammāsaṅkappa）无关，易致误读（SA 189）；并据
      `…samanupassanto cakkhusmimpi nibbindati` 补回底本所脱之「则于眼生厌」一支
    - 「不识、不知、不断、不离欲」四支语面含混 → 依
      `anabhijānaṁ aparijānaṁ avirājayaṁ appajahaṁ` 正作「证知、遍知、离贪、断舍」
      （abhijānāti／parijānāti／virājeti／pajahati）（SA 190／191）
    - SA 192 正说作「若于眼、色离欲」而反说唯作「于眼」，前后不齐；「色」为涉次经
      （SA 193 通篇作「眼、色」）而衍，今删，二经内外之别乃明
    - 「厌故不乐」之「不乐」＝ virāga（离贪）非「不喜欢」，作「厌故离贪」；
      「苦觉、乐觉」之「觉」＝ vedayita（所受）非「觉悟」（SA 195，沿用 SA_124／127 之例）
    - SA 196 末句「我说彼生、老、病、死、忧、悲、恼、苦」语义倒错，脱「解脱于」三字，
      据 Anālayo（liberated from birth, old age…）补
    - 「他心示现」→「记心示现」：`ādesanā-pāṭihāriya`（如实记说他人心念而为指授），
      非徒知他心；「不起诸漏，心得解脱」→「不取着故，心解脱于诸漏」
      （`anupādāya cittāni vimucciṁsu`，「不起」为「不取」之讹）（SA 197）
    - 「我、我所、我慢使系着」→「我执、我所执、我慢随眠」
      （`ahaṅkāra-mamaṅkāra-mānānusaya`，「使」＝ anusaya 随眠，沿用 SA_103／116／142）；
      「我内识身」→「此有识之身」（`imasmiñca saviññāṇake kāye`）；
      「正无间等」→「以正现观故」（abhisamaya，沿用 SA_105／109／123）（SA 198／199）
    - 「越于二」义不可通 → 「超越诸慢计」：实译 `vidhā samatikkanta`（vidhā 为慢之计量，
      胜／等／劣三慢类之计度），求那跋陀罗似读 vidhā 为「二」（dvi）而误（SA 199）
    - 「尼陀那法」→「因缘法」（nidāna 之音译）；「后住涅槃」→「终归涅槃」
      （`nibbānapabbhāra`，如坡下倾而终至，非「其后住于涅槃」）；
      「正信非家，出家学道」→「以正信故舍家出家」（SA 200）
  - `gold_reconstructed`／low：**SA 200** 底本法说核心仅作「谓眼无常，若色、眼识、眼触……
    如上无常广说」，为交叉指示而非全文；依所指之 SA 195／196 六六式补出纲要，
    不演全文、不补造情节，并于文言栏以括注标明补出之界。所补「受、想、行、识」四类据巴利平行
    `vedanāgataṁ, saññāgataṁ, saṅkhāragataṁ, viññāṇagataṁ`（SN35.121）；
    SA 195／196 于此处唯出受之三品，今兼出而并存。又汉本之次第教授（五受阴→六入处→因缘法→
    思惟其义）不见于巴利，为汉本一系所独，今从汉本之直陈式而不移入 MN147／SN35.121 之问答式。
  - 省文摄记如实保留为末段，不伪作各别全经：SA 188／195「如无常，如是苦、空、非我」、
    SA 196 二十四门（文言栏存底本全列，现代栏按义类分七组并出可考之巴利名；「虚业法」义未详，
    巴利未得确对，不强解）、SA 198 之衍展列（内入处→外入处→识→触→触生受→想→思→爱，
    与巴利罗睺罗相应第二品摄颂 `cakkhu rūpañca viññāṇaṁ, samphasso vedanāya ca; saññā
    sañcetanā taṇhā` 次第全同，足证非汉本自造）、SA 199 之「乃至意触因缘所生受」。
  - 罗什风削冗：SA 190–194 底本于反说、正说二段各将六根全出，今以「亦复如是」结（SA 194 二段皆然），
    法义不减而四字节奏得存。

## Earlier completed
- SA 103–129（卷第五 陰相應余部 ＋ 卷第六 羅陀相應）— `scripts/retranslate_sa103_129.py`,
  ok=27 warn=0 fail=0; gold=26 / gold_reconstructed=1（SA 126）; confidence high=11, medium=15, low=1
  - 此批即先前 needs_revision 之缺口（SA 1–102 与 SA 130+ 之间），补齐后 `gold` 连续段合为单一区间。
  - 信-校正（据 SN22.1／22.2／22.85／22.86／22.89、SN23.1–23.22、SN44.2、MN35、SN35.81）：
    - SA_103 浣衣譬：汉本「乳母衣……以种种杂香薰令消灭」不成譬，据 SN22.89
      `vatthaṁ saṅkiliṭṭhaṁ … gandhaparibhāvite karaṇḍake nikkhipanti` 改作「垢衣以灰、碱、牛粪揉治，
      净后置于香箧，余气乃尽」；华香譬「根／茎叶须精粗」据 `mūla／nāḷa／patta／kiñjakkha` 之分位
      正作「茎、瓣、蕊」；华名巴利作三（uppala／paduma／puṇḍarīka＝优钵罗／钵昙摩／分陀利），
      汉本多出「拘牟头」（kumuda），今从巴利之三
    - SA_103／116：「我慢、我欲、我使」＝ asmi-māna／asmi-chanda／asmi-anusaya，「使」为随眠（anusaya）
      非「驱役」，沿用 SA_142 之例
    - SA_104：删「苦者寂静、清凉、永沒」之增语（巴利仅作 `niruddhaṁ tadatthaṅgataṁ`，此处所答为
      「不施设如来死后有无」，非赞涅槃）；「如来见法真实、如住，无所得、无所施设」据
      `diṭṭheva dhamme saccato thetato tathāgate anupalabbhiyamāne` 厘正，作「于现法中，如来实、谛
      求之而不可得」；杀者譬（vadhaka paccāmitta）存汉本二重反问，汉巴义合
    - SA_106：补巴利枢要末句 `pubbe cāhaṁ etarahi ca dukkhañceva paññapemi dukkhassa ca nirodhaṁ`
      （我从昔来及今现在，唯说苦与苦灭），汉本脱
    - SA_107：汉本佛答「于苦患身，常当修学不苦患身」语面不通，据 SN22.1
      `āturo hāyaṁ kāyo aṇḍabhūto pariyonaddho … āturakāyassa me sato cittaṁ anāturaṁ bhavissatī`
      补「如卵裹壳」之譬并改作「身虽苦患，令心不苦患」
    - SA_108：汉本善／不善法四重假设推论句读错乱（条件句与结论句相混），依 SN22.2 之
      `abhavissa … nayidaṁ bhagavā … vaṇṇeyya / yasmā … tasmā … vaṇṇeti` 厘正
    - SA_109：「行即是我，我即是行」之「行」为「白」之讹（承前八遍处之末），正作「白即是我」；
      「如折多罗树」＝ tālāvatthukatā，作「如断多罗树头」；「非不消煬、非不寂灭」双重否定为衍文，
      作「消尽寂灭」
    - SA_110：「得随意自在，令彼如是、不令如是」依项目通例保留「大自在」而复其巴利之第一人称式，
      作「汝于彼得大自在耶？谓：我色当如是，我色莫如是」；随喜偈据 MN35
      `aggihuttaṁ mukhaṁ yaññānaṁ, sāvittī chandaso mukhaṁ` 正名——「闈陀」所译为 chandas
      （韦陀诗律）非泛言「经典」，作「韦陀诗律」、「婆毘谛」＝ sāvittī（娑毘谛颂）；末句巴利作「僧伽为最」，
      汉本作「等正觉为最」，存汉本之异而志之。布施果报显作「布施给有／无贪瞋痴者之果报」，
      免「施者有贪」之误读
    - SA_112：「断知」＝ pariññā（遍知）非「断」与「知」二事；据 SN23.4 补出所遍知之法（五阴）／
      遍知（贪瞋痴尽）／遍知之人（阿罗汉）三分之架构，而存汉本「忧悲恼苦尽」之语面
    - SA_122：补巴利末句 `taṇhākkhayo hi, rādha, nibbānaṁ`（爱尽即是涅槃，汉本脱此定义句）与
      `akīḷaniyaṁ karissatha`（令不复可玩）；「众生（satta）」＝「染著（sajjati）」之语源双关，
      汉译「染著缠绵」恰得其意，存之
    - SA_123：SC 所列 SN23.9／23.10 与本经四谛式不合，实际平行为 SN22.105（Sakkāya）一系，
      据以定「有身集」＝ `taṇhā ponobbhavikā nandirāgasahagatā`；confidence 降为 medium
    - SA_124／127：「厌故不乐」＝ `nibbidā virāgo`，「不乐」为离贪（virāga）非「不喜欢」；
      「断法」＝ khayadhamma（会断尽之法）非「应断之法」
    - 「无间等」＝ abhisamaya 一律作「现观」（SA_105／109／123）；SA_105 汉本「起慢无间等；非无间等故」
      句读错乱，正作「不悉解义而起于慢；慢不现观故，慢则不断」；SA_123「止慢无间等」＝
      `sammā mānābhisamayā`，作「以正观慢现观故，究竟苦边」
  - confidence=medium 者（15 经）：SC 未列巴利平行（SA_105／109／113／115／116／117／118／119）、
    平行标为 resembling 或标注与内容不合（SA_111／112／114／123／125／128／129）。
  - `gold_reconstructed`／low：SA_126 底本正文仅作「余如前说」，依 SA_121／124 全经式补出所指之纲要
    （无常、苦、变易 → 非我 → 厌 → 离贪 → 解脱），不演全文、不补造情节。
  - 省文摄记（SA_125「第三经亦如是」、SA_127 诸观法名目、SA_128「如是比十四经」）如实保留为末段，
    不伪作各别全经；卷末摄颂「彼多罗十问……」与卷题不入正文。
  - SA_113–119 七经底本同一句式（唯所断之法有别），脚本以共用 frame 生成，避免七经语面漂移。

- SA 172–187（卷第七／第八 斷知相應）— `scripts/retranslate_sa172_187.py`, ok=16 warn=0 fail=0;
  gold=14 / gold_reconstructed=2（SA 184/185）; confidence medium=14, low=2
  - 本相应 SC 平行表全空，依项目规约「无可靠平行时降为 medium/low」，全批 confidence 上限定为
    **medium**（不因道品定型语可考而升作 high）；SA 184/185 之法数系依经内经数回填，
    非底本语面直译，故标 `gold_reconstructed` / low。
  - 斷知相應为省文经（peyyāla）之极致：正文一式，末段以「一一八经」「三十二经」等指示衍展。
    正文全出问答；末段省文指示译为可读之衍展说明并标出经数，不伪作全文。
  - SuttaCentral 平行表于 SA 172–187 **十六经全未列巴利平行**（`parallels` 皆空），故不托 SN 某经；
    以汉本为底，参 Anālayo 英译（DDJBS 17, 2015, Fascicle 7）及道品巴利定型语厘义。
  - 主要 信-校正：
    - 「欲定断行成就如意足」→「欲三昧勤行成就神足」：「断行」实译 padhāna-saṅkhāra（勤行），
      非 pahāna（断），与本相应通篇之「断」同字异义（SA 179，medium）
    - 「苦习尽道」等四项 → 四通行（苦迟／苦速／乐迟／乐速通行），依四项八经＝三十二经之数；
      并志 Anālayo 正文之四谛异读（SA 184，gold_reconstructed/low）
    - 「除觉分」→「轻安觉支」（passaddhi），不作「除去」解（SA 182）
    - 「身身观住」→「随修内身观身而住」（ajjhattaṁ kāye kāyānupassī viharati）（SA 176/177）
    - 「起欲、方便、摄心增进」首出处补足四正断五支定型语（SA 178）
    - 「映翳」＝遮蔽；「独证」→「触证」（SA 187）
    - 「无贪法句」三句（无贪／无恚／无痴）与巴利四法句（AN4.29）不合，存汉本而志异
      （SA 185，gold_reconstructed/low）
  - SA 186 无常百余异名、SA 187 六十余烦恼名：文言栏存底本全列，现代栏按义类分组加括注。

## Validation (SA 103–129)
```
ok=27 warn=0 fail=0 · forbidden_hits=0
sim>=0.55 (繁转简嫌疑)=0 · max_sim=0.445 (SA_125) · 均值 0.351
paragraph_parallel_violations=0
gold=26 gold_reconstructed=1
```
Report: `data/translated/validation_report_sa103-129.json`

区间外不变式：`final_translated_data.json` 中 SA 1–102 与 SA 130–1362 共 1335 条，
跑前跑后 sha256 完全一致（`ea804574…`），区间内重跑亦逐字幂等；`gold` 连续段为单一区间 (1, 187)。

底本 paratext：SA_103／SA_111 为卷第五／卷第六之首经，其 `chinese_text` 含译者题记
「宋天竺三藏求那跋陀羅譯」（`raw_aligned_data.json` 已剥除，pipeline 版尚存）。此题记与卷题、
卷末摄颂同属藏经 paratext，不入正文；亦不得据以称罗什译（见项目 vision）。

并发事故与修复：本区间曾由两个 agent 并发处理，后者的 `scripts/retranslate_sa103_129.py`
覆写了前者的同名脚本（仓库尚无 commit，无从 checkout 恢复）。前者已落盘于本文件的
信-校正条目被逐条复核后重新并入现行脚本（SA_103 浣衣譬／华香譬、SA_104 删「寂静清凉」增语、
SA_107「如卵裹壳」、SA_109「白即是我」、SA_110 诗律与自在句、SA_112 三分架构、SA_122 涅槃定义句、
SA_124/127「不乐」＝virāga，及 confidence 下调），故本节所述与现行数据一致。
教训：跨 agent 并发写同一 range 前应先 `git commit`，或按 range 分派文件名。

## Validation (SA 172–187)
```
ok=16 warn=0 fail=0 · forbidden_hits=0
sim>=0.55 (繁转简嫌疑)=0 · max_sim=0.412 (SA_172) · 均值 0.359
paragraph_parallel_violations=0
gold=14 gold_reconstructed=2
```
Report: `data/translated/validation_report_sa172-187.json`

## Validation (SA 188–200)
```
ok=13 warn=0 fail=0 · forbidden_hits=0
sim>=0.55 (繁转简嫌疑)=0 · max_sim=0.469 (SA_194) · 均值 0.352
paragraph_parallel_violations=0
gold=12 gold_reconstructed=1 · confidence high=9 medium=3 low=1
```
Report: `data/translated/validation_report_sa188-200.json`

Corpus: 1362 records · gold=187 · gold_reconstructed=13 · needs_revision=1162

## Invariants held this run
- SA ≤ 171 未动：171 条既有 gold 之 lit/mod/notes/status/confidence 与各 range 脚本逐字相同
  （0 mismatch）；`gold` 连续段为单一区间 (1, 187)
- 用 aligned `chinese_text`（16/16 与 `raw_aligned_data.json` 一致）
- 无繁转简：输出无繁体残留；`similarity_to_source` 逐经入库，SIM_MAX=0.55 闸门 0 命中
- 现代栏与文言栏段数一一对应（build 时 assert ＋ merge 时记 `paragraph_parallel`）
- forbidden_mahayana 命中 0
- `prior_review_status` provenance 闸：脚本自产状态（gold/gold_reconstructed/needs_*）不回写为
  pre-gold 状态，故重跑不覆盖启发式草稿之来历（幂等）
- 与 SA 103–129 批次并发写 `final_translated_data.json` 未互相覆盖（已逐条比对 golden 复核）
- SA 103–129 批次同样以「区间外 sha256 前后一致」验明未触及 SA 1–102 与 SA 130+，
  且输出无繁体残留（`癰/閡/敵/僕/慮` 已依既有 gold 用字改作 `痈/阂/敌/仆/虑`）

## Invariants held (SA 188–200 run)
- **SA ≤ 187 未动**：`final_translated_data.json` 中区间外 1349 条（SA 1–187 ＋ SA 201–1362）
  跑前跑后 sha256 完全一致（`a773a4bf…`）；区间内重跑逐字幂等
  （连跑三次 `final_translated_data.json` 全文 sha256 皆 `fa884b7d…`，stdout 亦全同）
- `gold`／`gold_reconstructed` 连续段仍为**单一区间 (1, 200)**，无洞
- 现代栏与文言栏段数一一对应（build 时 assert ＋ merge 时记 `paragraph_parallel`，0 违例）
- 无繁转简：`similarity_to_source` 逐经入库，SIM_MAX=0.55 闸门 0 命中（max 0.469 SA_194）；
  繁体残留 0——以「已核 187 经 gold 输出之用字集」为基准扫描，本批新出字皆为正体简化字
  （符级继耽陈溃卧玻璃萦螺录编躯鹫坡拟敕），初稿之 `後`／`髮` 二字已改作 `后`／`发`
- forbidden_mahayana 命中 0
- `prior_review_status` provenance 闸：脚本自产状态（gold/gold_reconstructed/needs_*）不回写为
  pre-gold 状态，故重跑不覆盖启发式草稿之来历
- `data/golden/sa_188…200.json` 与 `final_translated_data.json` 逐条相同；
  `web/public/final_translated_data.json` 与之全同

底本 paratext（承前）：SA_188 为卷之首经，`final_translated_data.json` 内其 `chinese_text`
仍含译者题记「宋天竺三藏求那跋陀羅譯」（`raw_aligned_data.json` 已剥除，pipeline 版尚存），
情形与 SA_103／SA_111 同。此题记与卷题同属藏经 paratext，不入正文，亦不得据以称罗什译。
故本批 13 经中 12 经之 `chinese_text` 与 aligned 逐字相同，SA_188 之异仅此题记一项。
又底本于 SA_188 前题「杂阿含经卷第八」而 SC 卷次作卷第九，此为大正藏卷次与相应分卷之异，
同 SA_187 之例，志之不改。

## Validation (SA 256–270)
```
ok=14 warn=1 fail=0 · forbidden_hits=0
sim>=0.55 (繁转简嫌疑)=0 · max_sim=0.411 (SA_269) · 均值 0.303
paragraph_parallel_violations=0
gold=15 gold_reconstructed=0 · confidence high=14 medium=1 low=0
```
Report: `data/translated/validation_report_sa256-270.json`

Corpus: 1362 records · gold=286 · gold_reconstructed=18 · needs_revision=1058
（gold＋gold_reconstructed＝290，连续段为单一区间 (1, 290)）

## Validation (SA 271–290)
```
ok=20 warn=0 fail=0 · forbidden_hits=0
sim>=0.55 (繁转简嫌疑)=0 · max_sim=0.526 (SA_271) · 均值 0.414
paragraph_parallel_violations=0
gold=16 gold_reconstructed=4 · confidence high=15 medium=5 low=0
```
Report: `data/translated/validation_report_sa271-290.json`

## Invariants held (SA 271–290 run)
- **SA ≤ 270 未动**：merge 只写入 SA_271–SA_290
- `gold` 连续段为**单一区间 (1, 290)**，无洞
- 现代栏与文言栏段数一一对应（0 违例）
- 无繁转简：SIM_MAX=0.55 闸门 0 命中（max 0.526 SA_271）
- forbidden_mahayana 命中 0
- `data/golden/sa_271…290.json` 与 `final_translated_data.json` 逐条相同

Corpus: 1362 records · gold=265 · gold_reconstructed=14 · needs_revision=1083
（gold 连续段 (1, 250) + 本批 15 经；SA 251–255 待另一 agent）

## Invariants held (SA 256–270 run)
- **SA ≤ 255 未动**：merge 只写入 SA_256–SA_270
- 现代栏与文言栏段数一一对应（0 违例）
- 无繁转简：SIM_MAX=0.55 闸门 0 命中（max 0.411 SA_269）
- forbidden_mahayana 命中 0
- `data/golden/sa_256…270.json` 与 `final_translated_data.json` 逐条相同

## Validation (SA 231–250)
```
ok=20 warn=0 fail=0 · forbidden_hits=0
sim>=0.55 (繁转简嫌疑)=0 · max_sim=0.527 (SA_237) · 均值 0.377
paragraph_parallel_violations=0
gold=20 gold_reconstructed=0 · confidence high=11 medium=9 low=0
```
Report: `data/translated/validation_report_sa231-250.json`

Corpus: 1362 records · gold=250 · gold_reconstructed=14 · needs_revision=1098
（gold＋gold_reconstructed＝250，连续段为单一区间 (1, 250)）

## Invariants held (SA 231–250 run)
- **SA ≤ 230 未动**：merge 只写入 SA_231–SA_250；SA 1–230 跑前跑后逐条一致
- `gold` 连续段为**单一区间 (1, 250)**，无洞
- 现代栏与文言栏段数一一对应（0 违例）
- 无繁转简：SIM_MAX=0.55 闸门 0 命中（max 0.527 SA_237）
- forbidden_mahayana 命中 0
- `data/golden/sa_231…250.json` 与 `final_translated_data.json` 逐条相同

## Validation (SA 221–230)
```
ok=10 warn=0 fail=0 · forbidden_hits=0
sim>=0.55 (繁转简嫌疑)=0 · max_sim=0.419 (SA_224) · 均值 0.365
paragraph_parallel_violations=0
gold=10 gold_reconstructed=0 · confidence high=5 medium=5 low=0
```
Report: `data/translated/validation_report_sa221-230.json`

Corpus: 1362 records · gold=216 · gold_reconstructed=14 · needs_revision=1132
（gold＋gold_reconstructed＝230，连续段为单一区间 (1, 230)）

## Invariants held (SA 221–230 run)
- **SA ≤ 220 未动**：`final_translated_data.json` 中 SA 1–220 之 lit/mod/notes/status/confidence/translator
  跑前跑后逐条 sha256 一致（0 mismatch）；merge 只写入 SA_221–SA_230
- `gold`／`gold_reconstructed` 连续段为**单一区间 (1, 230)**，无洞
- 现代栏与文言栏段数一一对应（build 时 assert ＋ merge 时记 `paragraph_parallel`，0 违例）
- 无繁转简：`similarity_to_source` 逐经入库，SIM_MAX=0.55 闸门 0 命中（max 0.419 SA_224）；
  文言／白话栏繁体残留 0
- forbidden_mahayana 命中 0
- `prior_review_status` provenance 闸：本批十条先前为启发式 `needs_revision`，重跑不把脚本自产
  状态回写为 pre-gold 来历；连跑三次全文 sha256 皆 `ed00e72a…`，stdout 亦全同
- `data/golden/sa_221…230.json` 与 `final_translated_data.json` 逐条相同；
  `web/public/final_translated_data.json` 与之全同
- 9/10 经 `chinese_text` 与 aligned 逐字相同；**SA_230** 之异仅卷首译者题记
  「宋天竺三藏求那跋陀羅譯」（`raw_aligned_data.json` 已剥除，pipeline 版尚存），
  情形与 SA_188／103／111 同。此题记与卷题同属藏经 paratext，不入正文，亦不得据以称罗什译。

## Validator
- `missing_aggregate` now requires explicit 五阴/五受阴 context (fixes SA 94/95 false positives)
