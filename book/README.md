# 《杂阿含经·仿罗什风新译》研究译注本（LaTeX）

> 项目总文档：[../README.md](../README.md) · [../docs/README.md](../docs/README.md) · 入门：[../docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md)

## 书名

**杂阿含经·仿罗什风新译**（研究译注本）  
副题：Saṃyukta Āgama — A Kumarajiva-Style Research Translation

## 内容

每经五层（与网页阅读器对应，研究排版）：

1. **【正文·仿罗什风】** — 主文  
2. **【今译意】** — 现代白话  
3. **【底本·求那跋陀罗译】** — T99 全文（导出时剥除 SC 前缀与错简卷题）  
4. **【巴利平行与参考译文】** — SC 平行、巴利／英译摘要  
5. **【校勘与说明】** — notes、confidence、重建标记 ◇  

前言、版权说明、体例见 `frontmatter/`；体例 Markdown 见 `docs/EDITION_PRINCIPLES.md`。

## 构建

依赖：**XeLaTeX** + **ctex** 宏集（TeX Live 完整版通常已含）。

```bash
# 从语料导出 LaTeX（1362 经 → generated/juan_*.tex）
make book-export

# 编译全书 PDF（xelatex 三遍以生成目录与书签）
make book
```

输出：

- `book/build/main.pdf`（约 2100+ 页，含底本与今译）
- `book/build/sample_juan01.pdf`（卷一样章；与 `make book` 同步编译）

### 卷一样章

`make book` 会在全书编译后自动编译 `sample_juan01.tex`（两遍，以生成样章目录）。
若仅需样章、不编全书，可在导出后手动执行：

```bash
make book-export
cd book && xelatex -interaction=nonstopmode -output-directory=build sample_juan01.tex
cd book && xelatex -interaction=nonstopmode -output-directory=build sample_juan01.tex
```

### 封面

扉页插图：`book/assets/cover.png`（线条风格·菩提树下悟道，灰黄纸色）。  
排版见 `frontmatter/cover.tex`；换图后重新 `make book` 即可。

## 分卷

- `data/metadata/juan_ends.json`：T99 五十卷（SA 1–1362；卷五十含 SA 1128–1362）  
- `data/metadata/samyukta_taisho.json`：相应品目  
- 一卷可跨多个相应；导出时在 `\samyukta{}` 处分节  

`generated/juan_01.tex` … `juan_50.tex` 可单独 `\input` 印行。

## 显示层清洗

`book/reader.py`（网页 `web/src/reader.ts` 同步）在导出／阅读时处理：

- 剥除 `Saṁyuktāgama` 前缀与 T99 错简卷题（`雜阿含經卷第…`）  
- 嵌套引号：`'` → `『』`  
- 校勘 notes 去机器 audit 套语  

## 体量与精简

若仅印主文＋校勘，可改 `scripts/export_book_latex.py` 省略底本／今译层。
