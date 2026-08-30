# 文档索引

本目录为 **Agama–Kumarajiva** 项目的技术与编辑文档。开源发布前建议按下列顺序阅读。

## 新来者

1. [../README.md](../README.md) — 项目概览与快速开始  
2. [GETTING_STARTED.md](GETTING_STARTED.md) — 环境、网页、PDF、语料  
3. [XIN_DA_YA.md](XIN_DA_YA.md) — 信达雅定义（翻译者必读）  

## 翻译与体例

| 文档 | 内容 |
|------|------|
| [XIN_DA_YA.md](XIN_DA_YA.md) | 信=巴利义、达=段平行、雅=罗什风；不做全典错简重排 |
| [STYLE_GUIDE.md](STYLE_GUIDE.md) | 删冗、四字节奏、禁用大乘后出词 |
| [EDITION_PRINCIPLES.md](EDITION_PRINCIPLES.md) | 研究译注本五层、标记、版权与 CC0/Anālayo |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 如何改经、merge、审计、提 PR |

## 工程

| 文档 | 内容 |
|------|------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | 语料字段、管线、导出路径 |
| [ROADMAP.md](ROADMAP.md) | 阶段目标与刻意不做的事 |
| [../book/README.md](../book/README.md) | LaTeX 全书与卷样章 |
| [../web/README.md](../web/README.md) | 三栏阅读器 |

## 运行时报告（非手册）

| 路径 | 内容 |
|------|------|
| `data/translated/OVERNIGHT_PROGRESS.md` | 批次进度 |
| `data/translated/GOLD_AUDIT.md` | Gold 语料机器审计 |
| `data/translated/PUBLICATION_AUDIT.md` | 出版级 metadata 审计 |

## Cursor / Agent 规则

仓库内 `.cursor/rules/agama-kumarajiva.mdc` 与 `prompts/kumarajiva_system.md` 为 Agent 编辑时的约束，与上述 Markdown 一致。
