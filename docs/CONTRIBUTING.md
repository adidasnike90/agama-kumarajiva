# 参与指南

感谢考虑为本项目贡献。本仓库是 **研究译本 + 数字人文管线**，贡献前请先读 [XIN_DA_YA.md](XIN_DA_YA.md) 与 [EDITION_PRINCIPLES.md](EDITION_PRINCIPLES.md)。

## 你能贡献什么

| 类型 | 说明 |
|------|------|
| **经文翻译修订** | 罗什风 / 白话 / notes；经 `retranslate_sa*.py` 或 golden JSON |
| **校勘与平行** | primary SN、parallels、confidence 标注 |
| **工程** | 导出、阅读器、审计脚本 |
| **文档** | 修正错误或补充入门说明 |

请勿提交：未标注来源的大段第三方译文、声称「罗什原本」的表述、后期大乘术语进入正文。

---

## 翻译质量门槛

1. **信**：有 SN 平行时，义理与平行一致；冲突处从平行并在 `notes` 标明「据 SN xx」。  
2. **达**：罗什风与白话 **段数、顺序平行**；开经结经不省。  
3. **雅**：删 Indic 式冗复、四字节奏；**不是**繁转简或仅改标点。  
4. **重建经**（`gold_reconstructed`）：底本仅为 peyyāla 时，最小补叙，经题标 ◇，notes 说明依据。  

机器门禁：`scripts/audit_gold_corpus.py`（白话≠罗什风、validate fail 等）。

---

## 改经工作流

### 方式 A：分批脚本（推荐）

1. 复制现有 `scripts/retranslate_sa311_330.py` 模式  
2. 在 `SUTTAS` 字典中写 `SA_n` 条目  
3. 运行脚本 merge 进 `data/translated/final_translated_data.json`  
4. 同步 `data/golden/sa_n.json`（若该经有 golden 文件）  

```bash
python scripts/retranslate_sa311_330.py
make publication-audit
make sync-web
```

### 方式 B：直接编辑 golden

编辑 `data/golden/sa_XXX.json`，再运行对应 merge 脚本或 `scripts/merge_all_gold.py`（若项目提供）。

---

## 提交前检查

```bash
make publication-audit    # P0/P1 与 gold 审计
make sync-web             # 若改动了语料且需网页一致
make book-export          # 可选：确认 LaTeX 导出无报错
```

在 PR 描述中请注明：

- 经号范围（如 SA_275–SA_280）  
- 所据 SN 或「无可靠平行」  
- 是否 `gold_reconstructed`  

---

## 代码与文档

- Python：与现有 `scripts/` 风格一致；小 diff 优先  
- 网页：`web/src/reader.ts` 须与 `book/reader.py` 显示逻辑保持同步  
- 文档：用户可见行为变更请更新 README 或 `docs/GETTING_STARTED.md`  

---

## 版权与许可

- **代码**贡献：在 [MIT](../LICENSE) 下发布。  
- **译本文字**与项目自撰文档：在 [CC BY 4.0](../LICENSE-CONTENT) 下发布；贡献即表示你拥有提交内容的权利，并同意在该许可下发布。  
- 嵌入的巴利／英译摘录须遵守 SuttaCentral 与各译者条款；见 [EDITION_PRINCIPLES.md](EDITION_PRINCIPLES.md)。  

---

## 行为准则

尊重佛教文献学与学术诚信：不伪造出处、不夸大 AI 自动「还原」能力、不将文体实验包装为历史定本。

问题与讨论：开源后通过 GitHub Issues；此前可联系仓库维护者。
