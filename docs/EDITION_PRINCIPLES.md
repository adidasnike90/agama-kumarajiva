# 《杂阿含经·仿罗什风新译》研究译注体例

## 书名与定位

- **书名**：杂阿含经·仿罗什风新译
- **V1**：研究译注本（大正卷序）——`book/` · `make book`
- **V2**：研究译注本（经序重排）——`book_v2/` · `make book-v2`（见 [V2_ORDER.md](V2_ORDER.md)）
- **体例定位**：研究译注本（五层对照；非伪托罗什译经）
- **副题（建议）**：Saṃyukta Āgama — A Kumarajiva-Style Research Translation
- **性质**：数字人文意义上的**文体实验译本** + **文献对照本**；**不是**历史文献，**不声称**鸠摩罗什曾译《杂阿含》。

## 读者与用途

供佛教学、佛教文献学、阿含／相应部比较研究者：

1. 以**仿罗什风古文**为主文，阅读早期阿含义理；
2. 对照 **T99 求那跋陀罗译本**（底本）；
3. 核校 **巴利相应部／汉译平行**（SuttaCentral 表）；
4. 参看 **现代白话**「今译意」；
5. 依 **校勘说明** 追溯据平行改正之处。

## 信达雅（本书操作定义）

| 层级 | 定义 |
|------|------|
| **信** | 对巴利／SN（及可用梵本、Sujato/Bodhi/Patton 英译）所显 **早期法义** 负责；T99 仅作定位与传统术语参照。冲突时从平行，于校勘记标明「据 SNxx」。 |
| **达** | 主文与今译意 **段数、叙事顺序平行**；因果可读。 |
| **雅** | **仿**鸠摩罗什译经之删冗、四字节奏、意译圆通；**非**繁转简，**非**伪托罗什手笔。 |

## 本书每层含义

| 层级 | 标签 | 内容 |
|------|------|------|
| 主文 | **【正文·仿罗什风】** | `kumarajiva_style_text`；全书主轴 |
| 今译 | **【今译意】** | `modern_psychology_text`；冷静白话，与主文逐段对应 |
| 底本 | **【底本·T99】** | `chinese_text`（求那跋陀罗译）；文献对照 |
| 平行 | **【平行】** | SC 平行表、`primary_sn_uid`、巴利／英译摘要 |
| 校勘 | **【校勘与说明】** | `notes`；据平行校正、重建依据、confidence |
| 元数据 | 经题行 | 卷、相应、经号、短题；**信度**（gold / ◇reconstructed；high/medium/low） |

## 标记符号

- **◇**（或经题后「重建」）：`gold_reconstructed`。底本仅为「亦如是」「余如前说」等 **peyyāla**；正文据 SN 或同型经 **最小补叙**，非 T99 逐字。
- **gold**：底本有较完整经叙，依平行义重写之 **full translation**。
- **confidence**：high / medium / low —— 与 SC 平行及人工审读强度对应；low/medium 处宜保守引用。

## 文献简称（Sigla）

| 简称 | 含义 |
|------|------|
| T99 | 大正新修大藏经第 99 册《杂阿含经》（求那跋陀罗译） |
| SA | 本研究译本编号（SA\_1 … SA\_1362） |
| SN / AN 等 | 巴利《相应部》等（SuttaCentral UID） |
| SC | SuttaCentral 平行与 Bilara 数据 |

## 本书刻意不做的

1. **不**改写或取代 **V1** 研究译注本（大正卷序）；**V2** 为同系列另册「研究译注本（经序重排）」（网站可切换），见 [V2_ORDER.md](V2_ORDER.md)，不改 `sa_t99` 经号；
2. **不**引入后期大乘／禅语汇（见 `glossary/forbidden_mahayana.txt`）；
3. **不**将重建经伪装为底本全文。
4. **不**声称学术重排即「恢复原典」或罗什曾译阿含。
## 质量门禁（成书数据）

成书源数据：`data/translated/final_translated_data.json`（1362 经）。  
机器审计：`scripts/audit_gold_corpus.py` → `data/translated/GOLD_AUDIT.md`（P0=0，白话≠罗什风，validate fail=0）。

## 版权与引用

本书【正文·仿罗什风】与【今译意】为原创，许可见仓库根目录 [LICENSE-CONTENT](../LICENSE-CONTENT)（**CC BY 4.0**）；代码见 [LICENSE](../LICENSE)（**MIT**）。其余为文献对照。【巴利平行与参考译文】中巴利、英译均仅刊 **600 字以内摘录**。

| 材料 | 来源 | 许可／条款 |
|------|------|------|
| 本项目原创译文与自撰文档 | Agama–Kumarajiva | **CC BY 4.0** |
| 本仓库代码 | Agama–Kumarajiva | **MIT** |
| 汉译底本 | 大正 T99 / CBETA | 传统佛典，文献引用 |
| 巴利原文 | Mahāsaṅgīti 数字本（SC Bilara） | 古文献，无现代版权 |
| SN 英译 | Bhikkhu Sujato | **CC0** |
| SA 英译（备用） | Charles Patton | **CC0** |
| SA 英译（fallback，约数十经） | Bhikkhu Anālayo | **非 CC0**；原刊《法鼓佛学学报》等；Anālayo 授权 SC 在其网站刊载，**不当然**延及本书；本书仅短摘录；商业印行前宜确认 |
| Bodhi 英译 | Wisdom Publications | **本书未嵌入** |
| 平行表 | SuttaCentral curated | 参考数据 |

**建议引用格式**（示例）：

> 《杂阿含经·仿罗什风新译》研究译注本，第 1 经，据《相应部》22.12 校正，2026.

> 《杂阿含经·仿罗什风新译》研究译注本，第 275 经，据《增支部》8.9 校正，2026.

经号与平行编号须与所引各经【平行】栏一致。

## 分卷

依 T99 五十卷（`data/metadata/juan_ends.json`，卷五十 = SA 1128–1362）；各卷内按相应（`samyukta_taisho.json`）与经号排列。一卷可含多个相应。

## 成书导出

- **LaTeX**：`make book-export` → `make book` → `book/build/main.pdf`  
- **网页**：`make sync-web` → `web/public/final_translated_data.json`  
- 底本层导出时经 `book/reader.py` 剥除 SC 前缀与错简卷题；详见 `book/README.md`。
