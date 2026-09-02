# 对照阅读器

Vite + React。侧栏切换三部产品（`localStorage`）；页眉可下载 PDF。

| 开关 | 书稿 | 界面 |
|------|------|------|
| **V1 卷序** | `book/` | 三栏：正文｜底本+平行｜今译 |
| **V2 重排** | `book_v2/` | 同上，经目按学术序 |
| **V3 法义** | `book_v3/` | **双栏**：正文｜今译（+附注） |
| PDF | `public/books/v1-taisho.pdf` · `v2-reorder.pdf` · `v3-dharma.pdf` | `make sync-web-pdfs` |

V3 篇题为通读新拟，列表显示章／篇名与所熔 SA。政策：[V2_ORDER.md](../docs/V2_ORDER.md)、[V3_DHARMA_READER.md](../docs/V3_DHARMA_READER.md)。

## 启动

```bash
make web
# http://127.0.0.1:5173
```

## 布局

**V1／V2**

```
经目 + 三栏（罗什风｜底本与平行｜白话）
```

**V3**

```
通读篇目 + 双栏（罗什风正文｜今译意）
```

更新数据：`make sync-web`（语料、V2 序、V3 单元、有则同步 PDF）。
