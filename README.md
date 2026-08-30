# Agama–Kumarajiva

**《杂阿含经》仿罗什风研究译本** — 数字人文意义上的文体实验与文献对照工程。

将 [SuttaCentral](https://suttacentral.net/) 所依之 T99《杂阿含经》（求那跋陀罗译）在 **1362 部** 经上，对照巴利《相应部》等平行，产出：

- **仿鸠摩罗什风** 典雅汉语主文  
- **现代白话** 今译意（逐段平行）  
- **T99 底本** + 巴利／英译平行 + 校勘说明  

> **这不是历史伪造**：不声称鸠摩罗什曾译《杂阿含》；v1 **不**自动重排 Taishō 经序错简，只在 notes 中标注。

---

## 成果一览

| 产出 | 路径 / 命令 | 说明 |
|------|-------------|------|
| **三栏对照网页** | 本地 `make web`；线上 [GitHub Pages](https://adidasnike90.github.io/agama-kumarajiva/) | 罗什风｜底本+平行｜白话；1362 经可检索 |
| **研究译注 PDF** | `make book` → `book/build/main.pdf`；亦见 [Releases](https://github.com/adidasnike90/agama-kumarajiva/releases) | LaTeX 五层排版，约 2100+ 页 |
| **语料 JSON** | `data/translated/final_translated_data.json` | 全书源数据；亦在 `web/public/` |
| **黄金逐经稿** | `data/golden/sa_*.json` | 1362 文件，与 merge 脚本对应 |

---

## 快速开始

### 只读对照（网页）

```bash
git clone <repo-url> agama-kumarajiva && cd agama-kumarajiva
cd web && npm install && npm run dev
# 浏览器打开 http://127.0.0.1:5173
```

或于仓库根目录：`make web`

语料已随仓库提供；若你刚更新了 `data/translated/`，请先 `make sync-web`。

### 开发者环境

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd web && npm install && cd ..

make web              # 三栏阅读器
make book             # 需 TeX Live + ctex；见 docs/GETTING_STARTED.md
make publication-audit  # 语料质量审计
```

对齐管线（从 SC 拉新数据时）：

```bash
python scripts/run.py align --count 10   # 试点
# 或 make align / make align-full
```

---

## 常用命令

| 命令 | 作用 |
|------|------|
| `make web` | 启动三栏阅读器（Vite，127.0.0.1:5173） |
| `make sync-web` | 语料 JSON → `web/public/` |
| `make book-export` | 语料 → `book/generated/juan_*.tex` |
| `make book` | 导出 + XeLaTeX ×3 → `book/build/main.pdf` |
| `make publication-audit` | 出版级语料 + gold 审计 |
| `make align` | 对齐 10 经试点 |
| `make align-full` | 全库对齐（需网络） |

完整说明见 [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)。

---

## 仓库结构

| 路径 | 作用 |
|------|------|
| [`web/`](web/) | 三栏对照阅读器（Vite + React） |
| [`book/`](book/) | LaTeX 研究译注本 |
| [`data/translated/`](data/translated/) | 成书语料、审计报告、进度 |
| [`data/golden/`](data/golden/) | 逐经黄金 JSON |
| [`data/metadata/`](data/metadata/) | 五十卷界、相应品目 |
| [`data/aligned/`](data/aligned/) | Bilara 对齐缓存 |
| [`pipeline/`](pipeline/) | SC / Bilara 抓取与 SA↔SN 对齐 |
| [`translate/`](translate/) | 校验、相似度、质量门禁 |
| [`scripts/`](scripts/) | 分批重译、导出、审计 |
| [`prompts/`](prompts/) | Agent 系统提示 |
| [`glossary/`](glossary/) | 术语表、大乘禁用词 |
| [`docs/`](docs/) | **文档索引**（见下） |

---

## 文档

| 文档 | 读者 |
|------|------|
| [docs/README.md](docs/README.md) | 文档总索引 |
| [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) | 安装、网页、PDF、语料同步 |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | 数据流、目录、管线 |
| [docs/XIN_DA_YA.md](docs/XIN_DA_YA.md) | **信达雅**操作定义（必读） |
| [docs/EDITION_PRINCIPLES.md](docs/EDITION_PRINCIPLES.md) | 研究译注本五层体例、版权 |
| [docs/STYLE_GUIDE.md](docs/STYLE_GUIDE.md) | 罗什风改写范例 |
| [docs/ROADMAP.md](docs/ROADMAP.md) | 阶段规划与不承诺事项 |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | 参与翻译与提交流程 |
| [book/README.md](book/README.md) | LaTeX 构建细节 |
| [web/README.md](web/README.md) | 三栏阅读器说明 |

---

## 翻译原则（摘要）

优先级：**信 > 达 > 雅**。  
**信** = 对巴利／SN 之义，不是对求那跋陀罗之字。详见 [docs/XIN_DA_YA.md](docs/XIN_DA_YA.md)。

精译在 Cursor 等 Agent 环境完成（`prompts/kumarajiva_system.md`），经 `scripts/retranslate_sa*.py` merge 入语料。  
`review_status`: `gold` = 已精校；`gold_reconstructed` = 底本 peyyāla，据平行最小补叙（经题标 ◇）。

---

## 许可与署名

本仓库采用**分层许可**（详见根目录文件）：

| 层 | 范围 | 许可 |
|----|------|------|
| **代码** | `web/`、`scripts/`、`pipeline/`、`book/*.py`、Makefile 等 | [MIT](LICENSE) |
| **本项目原创文本** | 【正文·仿罗什风】、【今译意】、本书前言体例、项目自撰文档 | [CC BY 4.0](LICENSE-CONTENT) |
| **第三方对照材料** | T99 底本、巴利、Sujato／Patton 英译、Anālayo 短摘录等 | **各依原条款**，本项目不予再许可 |

第三方摘要：T99／CBETA 传统佛典；巴利与 Bilara 语料经 [SuttaCentral](https://suttacentral.net/)；Sujato、Patton 为 **CC0**；Anālayo 英译**非 CC0**（本书仅短摘录）。详见 [docs/EDITION_PRINCIPLES.md](docs/EDITION_PRINCIPLES.md) 与 `book/frontmatter/sources.tex`。

引用本译本时请标明书名、经号及所据平行；不得将本译本表述为历史罗什译经。

---

## 致谢

平行与数字文本：[SuttaCentral](https://suttacentral.net/)（Bhikkhu Sujato、Charles Patton、Bhikkhu Anālayo 等）。  
汉译底本：大正藏 T99 / CBETA 传统。
