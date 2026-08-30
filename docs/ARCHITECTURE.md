# 架构与数据流

## 总览

```
SuttaCentral Bilara / API
        │
        ▼
  pipeline/ + scripts/align_corpus.py
        │
        ▼
  data/aligned/          data/metadata/
        │                      │
        └──────────┬───────────┘
                   ▼
     scripts/retranslate_sa*.py  (Cursor Agent + prompts/)
                   │
                   ▼
     data/golden/sa_*.json  ──merge──►  data/translated/final_translated_data.json
                   │                           │
                   │                           ├── make sync-web ──► web/public/
                   │                           │
                   │                           └── export_book_latex.py ──► book/generated/
                   │                                              │
                   │                                              └── xelatex ──► book/build/main.pdf
                   │
                   └── audit_gold_corpus.py / publication_corpus.py
```

**单一事实来源（成书）**：`data/translated/final_translated_data.json`。

---

## 语料记录（`SutraRecord`）

与 `web/src/types.ts` 一致：

| 字段 | 用途 |
|------|------|
| `id` | `SA_1` … `SA_1362` |
| `title` | T99 经题行（卷、相应、经号、短题） |
| `kumarajiva_style_text` | 【正文·仿罗什风】 |
| `modern_psychology_text` | 【今译意】 |
| `chinese_text` | T99 底本（导出时经 `clean_chinese_text` 清洗） |
| `pali_text` / `english_sn_text` | 所据 SN 平行 |
| `english_sa_text` | Patton / Anālayo 等 SA 英译（备用） |
| `parallels` / `primary_sn_uid` | SC 平行表 |
| `notes` | 校勘与说明 |
| `review_status` | `gold` / `gold_reconstructed` |
| `confidence` | high / medium / low |
| `validation` | 机器校验结果 |

---

## 分卷与相应

两套正交划分：

| 元数据 | 文件 | 说明 |
|--------|------|------|
| **五十卷** | `data/metadata/juan_ends.json` | T99 物理分册；卷五十 = SA 1128–1362 |
| **相应品目** | `data/metadata/samyukta_taisho.json` | 约 51 种主题经群 |

一卷可跨多个相应；LaTeX/网页按经号排序，多相应卷内用 `\samyukta{}` 分节。逻辑见 `book/reader.py` 的 `samyukta_sections()`。

经号中文数字：`pipeline/titles.py` 的 `to_cn_num()`（101+ 作「一〇二」式）。

---

## 主要模块

### `pipeline/`

- 从 Bilara 拉取 SA 汉文、Patton 英译、SN 巴利与 Sujato 英译  
- SC API 平行表  
- `titles.py`：卷/相应/短题  

### `translate/`

- `validate.py`：字段完整性、禁用词  
- `similarity.py` / `quality_gate.py`：罗什风 vs 底本相似度门禁（防繁转简）  

### `book/reader.py`

阅读器与导出的共享逻辑：

- `clean_chinese_text` — 底本清洗  
- `normalize_chinese_quotes` — 引号  
- `clean_notes` — 校勘条 humanize  
- `format_parallels_reader` — 平行摘要  
- `samyukta_sections` / `juan_chapter_title` — 卷/相应标题  

网页镜像：`web/src/reader.ts`。

### `scripts/export_book_latex.py`

语料 → `book/generated/juan_01.tex` … `juan_50.tex` + `all_juan.tex` + 重建经目录。

### `scripts/sync_web_corpus.py`

复制 JSON 至 `web/public/`（无变换）。

---

## 目录约定

| 路径 | 版本控制 |
|------|----------|
| `book/generated/*.tex` | gitignore；`make book-export` 生成 |
| `book/build/` | gitignore；LaTeX 产物 |
| `data/cache/` | gitignore；Bilara 缓存 |
| `data/golden/` | **跟踪**；逐经源稿 |
| `web/public/final_translated_data.json` | **跟踪**；便于 clone 即读 |

---

## 刻意边界（v1）

- **不**自动重排 Taishō 经序错简  
- **不**声称历史罗什译本  
- **不**在正文中引入大乘/禅后出术语（见 `glossary/forbidden_mahayana.txt`）  

见 [ROADMAP.md](ROADMAP.md)。
