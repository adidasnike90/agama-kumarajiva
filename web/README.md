# 三栏对照阅读器

Vite + React 实现的 **1362 经** 对照界面：仿罗什风主文、T99 底本与平行、现代白话。

## 启动

```bash
# 在 web/ 目录
npm install
npm run dev

# 或在仓库根目录
make web
```

打开 **http://127.0.0.1:5173**

## 布局

```
┌─────────────┬──────────────┬──────────────┬──────────────┐
│  经目列表   │  罗什风新译  │ 底本与平行   │  现代白话    │
│  搜索/选择  │  (主文)      │ T99+英/巴利  │  (今译意)    │
└─────────────┴──────────────┴──────────────┴──────────────┘
```

- **经目**：`id`、`title`；可搜经号或短题  
- **底本**：经 `cleanChineseText()` 剥除 SC 前缀与错简卷题  
- **英译**：优先 Sujato（SN，CC0）；否则 Patton / Anālayo（见 attribution 行）  
- **校勘**：页内展示 `notes`（经 `cleanNotes()` 简化）  

显示逻辑与 PDF 导出共用规范，实现于 `src/reader.ts`（镜像 `book/reader.py`）。

## 数据

默认加载 `/final_translated_data.json`（即 `public/final_translated_data.json`）。

更新语料：

```bash
# 仓库根目录
make sync-web
```

主源文件：`data/translated/final_translated_data.json`。

## 构建与部署

```bash
npm run build    # 输出 dist/（本地 base=/）
GITHUB_PAGES=true npm run build  # GitHub Pages（base=/agama-kumarajiva/）
npm run preview  # 本地预览 dist
```

推送到 `master` 时，`.github/workflows/pages.yml` 会自动构建并部署到  
**https://adidasnike90.github.io/agama-kumarajiva/**（需在仓库 Settings → Pages 选择 Source: GitHub Actions）。

## 开发说明

| 文件 | 作用 |
|------|------|
| `src/App.tsx` | 布局、经目、三栏 |
| `src/reader.ts` | 底本/notes/英译来源清洗 |
| `src/types.ts` | 语料 TypeScript 类型 |
| `public/final_translated_data.json` | 语料（由 sync 复制） |

修改 `reader.ts` 时，请同步更新 `book/reader.py` 以保持 PDF 与网页一致。

更多见 [docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md)。
