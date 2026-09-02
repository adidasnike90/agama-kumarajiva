# 入门指南

本文说明如何在本地运行 **三栏阅读器**、构建 **LaTeX PDF**，以及语料如何在各产出之间同步。

## 前置依赖

| 用途 | 依赖 |
|------|------|
| Python 管线 | Python 3.11+，`pip install -r requirements.txt` |
| 三栏网页 | Node.js 18+，`cd web && npm install` |
| 全书 PDF | TeX Live（含 **XeLaTeX**、**ctex**、Noto CJK 字体） |

Linux 示例（Fedora）：

```bash
sudo dnf install texlive-xetex texlive-ctex google-noto-sans-cjk-fonts
```

---

## 1. 三栏对照阅读器

### 启动

```bash
# 方式 A：Makefile（推荐）
make web

# 方式 B：直接进入 web/
cd web && npm run dev
```

浏览器打开：**http://127.0.0.1:5173**

### 三栏含义

| 栏 | 数据字段 | 说明 |
|----|----------|------|
| 罗什风新译 | `kumarajiva_style_text` | 主文；据 SN 等平行义改写 |
| 底本与平行 | `chinese_text` + 英/巴利 | T99 底本（已剥 SC 前缀与错简卷题）+ 参考译文 |
| 现代白话 | `modern_psychology_text` | 与罗什风逐段对照 |

左侧边栏：1362 经列表，支持按经号/标题搜索。

### 语料同步

网页读取 `web/public/final_translated_data.json`。主语料在 `data/translated/final_translated_data.json`。

修改语料后：

```bash
make sync-web
# 刷新浏览器即可（Vite 热更新不自动复制 JSON，须先 sync）
```

### 生产构建（可选）

```bash
cd web && npm run build
# 静态文件在 web/dist/，可部署到任意静态托管
```

---

## 2. 研究译注本与法义读本 PDF（LaTeX）

```bash
make book      # V1 研究译注本（大正卷序）→ book/build/main.pdf
make book-v2   # V2 研究译注本（经序重排）→ book_v2/build/main.pdf
make book-v3   # V3 法义读本（通读熔文）→ book_v3/build/main.pdf
```

V3 仅正文＋今译＋附注；篇题新拟。详见 [V3_DHARMA_READER.md](V3_DHARMA_READER.md)。

### V1 一键构建细节

```bash
make book
```

等价于：

```bash
make book-export                    # Python → book/generated/
cd book && xelatex -output-directory=build main.tex  # ×3
cd book && xelatex -output-directory=build sample_juan01.tex  # ×2（卷一样章）
```

输出：

- **`book/build/main.pdf`**（约 2100+ 页，含底本与今译）
- **`book/build/sample_juan01.pdf`**（卷一样章，与 `make book` 同步更新）

### 仅编样章（不编全书）

```bash
make book-export
cd book && xelatex -interaction=nonstopmode -output-directory=build sample_juan01.tex
cd book && xelatex -interaction=nonstopmode -output-directory=build sample_juan01.tex
```

### 显示层清洗

导出与网页共用 `book/reader.py`（网页为 `web/src/reader.ts`）：

- 底本：去除 `Saṁyuktāgama` 前缀、T99 错简卷题（`雜阿含經卷第…`）  
- 引号：ASCII `'` → 中文嵌套 `『』`  
- 校勘 notes：去除机器 audit 套语  

详见 [book/README.md](../book/README.md)。

---

## 3. 语料与审计

### 主语料

`data/translated/final_translated_data.json` — 1362 条记录，每条含：

- 主文 / 白话 / 底本 / 巴利 / SN 英译 / notes / parallels / confidence 等  

字段定义见 [ARCHITECTURE.md](ARCHITECTURE.md)。

### 质量审计

```bash
make publication-audit
```

生成/更新：

- `data/translated/PUBLICATION_AUDIT.md`  
- `data/translated/GOLD_AUDIT.md`  

### 改经工作流（摘要）

1. 编辑或运行 `scripts/retranslate_saXXX_YYY.py`  
2. merge 进 `final_translated_data.json`  
3. `make sync-web`（若需网页）  
4. `make publication-audit`  
5. 可选 `make book-export && make book`  

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 4. 数据对齐（可选）

从 SuttaCentral / Bilara 拉取新对齐数据：

```bash
make align          # 10 经试点
make align-full     # SA 51–1362，需网络与较长时间
make metadata       # 重建 SC 元数据表
```

对齐结果写入 `data/aligned/`。

---

## 5. 常见问题

**网页空白或经目为 0**  
→ 检查 `web/public/final_translated_data.json` 是否存在；运行 `make sync-web`。

**PDF 中文乱码或缺字**  
→ 确认已安装 ctex 与 Noto CJK；见 `book/preamble.tex` 字体设置。

**某经底本仍见卷题**  
→ 应已通过 `clean_chinese_text` 剥除；若发现遗漏请提 issue 并附经号。

**全书缺经**  
→ 确认 `data/metadata/juan_ends.json` 卷五十止于 SA 1362；重新 `make book-export`。
