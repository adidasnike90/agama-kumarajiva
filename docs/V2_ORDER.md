# V2 研究译注本（经序重排）

> **产品关系**：**V1 研究译注本（大正卷序）保留**；**V2 是同系列另册**。网站用开关切换，不是把 V1「改成」学术序。

| | **V1** | **V2** |
|--|--------|--------|
| **正式名** | 研究译注本（大正卷序） | 研究译注本（经序重排） |
| 书稿 | `book/` · `make book` | `book_v2/` · `make book-v2` |
| 网页开关 | 「V1 大正卷序」 | 「V2 经序重排」 |
| 编排 | T99／CBETA 五十卷经目 | Anesaki／印顺卷次阅读序 |
| 经号 | `sa_t99` 1–1362 | 同号为永久锚点，另标 `seq` |

系列书名均为《杂阿含经·仿罗什风新译》；「研究译注本」为体例定位，括注区分经序。

> **定位**：依学界通行之卷次重排假说编排的**对照读本**，**不是**「恢复出土原典」或「罗什若译阿含之卷次」。

## 分期

| 阶段 | 内容 | 状态 |
|------|------|------|
| **1** | 序表 + 网页开关 + 另册 `book_v2`（**完整前言体例封面**） | **已落地** |
| **2** | 印顺 **51 相应** 与 SA 区间对照表（会编／Bingenheimer／SC） | 目录已建，区间未填 |
| **3** | V2 PDF 发布；网页默认仍可记本地偏好 | 导出管线已就绪 |
| **4** | 按新序微调译文（仅必要时） | 未开始 |

## 双编号

| 字段 | 含义 |
|------|------|
| `sa_t99` | 大正／CBETA／本仓库经号（1–1362），**永不改号** |
| `seq` | V2 正编阅读序（1…1359；不含插入） |
| `seq_appendix` | 附录序（插入经 604、640、641） |
| `t99_juan` | 该经在 `juan_ends.json` 中的 T99 卷号 |
| `academic_fascicle_slot` | Anesaki 48 卷流中的卷位（1–48）；卷 23／25 保留段无此字段 |

## 卷次重排依据

Anesaki 所复原、印顺《杂阿含经论会编》所采用之 **48** 个 T99 卷第顺序：

`1, 10, 3, 2, 5–9, 43, 11, 13, 12, 14–21, 31, 24, 26–30, 41, 32–35, 47, 37–40, 46, 42, 4, 44–45, 36, 22, 48–50`

**卷 23、25** 在 Anālayo、Bucknell 等叙述中为阿育王传替补卷，故不在上表。  
本仓库 `juan_ends.json` 仍为若干 SA 标了卷 23／25：阶段 1 将其中**非插入**经文接在 Anesaki 流之后（`stream=t99_juan_23_25_retained`），以保证 1359 经正编不缺号；阶段 2 对照会编后再决定是否改挂相应。

## 附录（非早期相应经）

| `sa_t99` | 处理 |
|----------|------|
| 604, 640, 641 | Aśokavadāna 杂入；**不入正编 `seq`** |

## 生成与成书

```bash
make v2-order        # 序表 → data/metadata/v2/
make sync-web        # 索引 → web/public/（网站开关用）
make book-v2         # 另册 PDF → book_v2/build/main.pdf
make book            # V1：book/build/main.pdf
```

| 产出 | 说明 |
|------|------|
| `data/metadata/v2/academic_order.json` | 全量双编号记录 |
| `data/metadata/v2/academic_order_index.json` | 紧凑索引（网页用） |
| `data/metadata/v2/fascicle_order_anesaki.json` | 卷次排列 |
| `data/metadata/v2/yinshun_samyukta_catalog.json` | 51 相应名录（区间待填） |
| `book_v2/generated/` | V2 LaTeX 正文 |
| `book_v2/build/main.pdf` | V2 独立 PDF |

Python：`pipeline.v2_order`（`reading_order_sa_t99()`, `academic_seq()`, `is_appendix()`）。

## 不做的宣称

- 不声称唯一正确「原经序」  
- 不声称鸠摩罗什曾译《杂阿含》  
- **不**用 V2 取代或改写 V1 书稿树  
- 阶段 1 **不**自动改写经文，只建**阅读顺序**与另册排版  
