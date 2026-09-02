import { useEffect, useMemo, useState, type ReactNode } from "react";
import type { SutraRecord } from "./types";
import {
  cleanChineseText,
  cleanNotes,
  englishSourceLabel,
  normalizeChineseQuotes,
  suttaReaderTag,
} from "./reader";

type Edition = "v1" | "v2" | "v3";

type OrderIndex = {
  by_sa_t99: Record<
    string,
    {
      seq?: number;
      seq_appendix?: number;
      role: string;
    }
  >;
  reading_order_sa_t99: number[];
  appendix_sa_t99: number[];
};

type V3Unit = {
  id: string;
  seq: number;
  chapter_id: number;
  chapter_title: string;
  title: string;
  source_sa: number;
  source_sas?: number[];
  primary_sn_uid?: string;
  review_status?: string;
  kumarajiva_style_text: string;
  modern_psychology_text: string;
  note?: string;
};

function saNum(id: string): number {
  const m = id.match(/(\d+)/);
  return m ? Number(m[1]) : 0;
}

function Panel({
  title,
  subtitle,
  children,
  tone,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
  tone: "gold" | "ink" | "plain";
}) {
  const tones = {
    gold: "border-[#8b6914]/60 bg-[#2a2116]",
    ink: "border-[#4a5560]/50 bg-[#1c2228]",
    plain: "border-[#3d4a3a]/50 bg-[#1a221c]",
  } as const;
  return (
    <section
      className={`flex min-h-0 flex-1 flex-col overflow-hidden rounded-xl border ${tones[tone]}`}
    >
      <header className="border-b border-white/10 px-4 py-3">
        <h2 className="text-sm tracking-[0.2em] text-[#d4b483] uppercase">
          {title}
        </h2>
        {subtitle ? (
          <p className="mt-1 text-xs text-[#a89880]">{subtitle}</p>
        ) : null}
      </header>
      <div className="flex-1 overflow-auto px-4 py-4 text-[17px] leading-8 whitespace-pre-wrap">
        {children}
      </div>
    </section>
  );
}

function editionLabel(edition: Edition): string {
  if (edition === "v1") return "V1 研究译注本（大正卷序）· 经号与五十卷依 T99";
  if (edition === "v2")
    return "V2 研究译注本（经序重排）· Anesaki／印顺卷次（大正经号仍保留）";
  return "V3 法义读本 · 通读删定 · 仅正文与今译";
}

export default function App() {
  const [records, setRecords] = useState<SutraRecord[]>([]);
  const [v3Units, setV3Units] = useState<V3Unit[]>([]);
  const [orderIndex, setOrderIndex] = useState<OrderIndex | null>(null);
  const [edition, setEdition] = useState<Edition>(() => {
    const saved = localStorage.getItem("agama-edition");
    if (saved === "v2" || saved === "v3") return saved;
    return "v1";
  });
  const [activeId, setActiveId] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [query, setQuery] = useState("");

  useEffect(() => {
    localStorage.setItem("agama-edition", edition);
  }, [edition]);

  useEffect(() => {
    const base = import.meta.env.BASE_URL;
    Promise.all([
      fetch(`${base}final_translated_data.json`).then((r) => {
        if (!r.ok) throw new Error(`语料 HTTP ${r.status}`);
        return r.json();
      }),
      fetch(`${base}academic_order_index.json`)
        .then((r) => (r.ok ? r.json() : null))
        .catch(() => null),
      fetch(`${base}v3_reader_units.json`)
        .then((r) => (r.ok ? r.json() : []))
        .catch(() => []),
    ])
      .then(([data, idx, v3]: [SutraRecord[], OrderIndex | null, V3Unit[]]) => {
        setRecords(data);
        setOrderIndex(idx);
        setV3Units(Array.isArray(v3) ? v3 : []);
        if (data[0]) setActiveId(data[0].id);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  useEffect(() => {
    if (edition === "v3") {
      if (v3Units[0] && !v3Units.some((u) => u.id === activeId)) {
        setActiveId(v3Units[0].id);
      }
    } else if (records[0] && activeId.startsWith("V3-")) {
      setActiveId(records[0].id);
    }
  }, [edition, v3Units, records, activeId]);

  const filteredRecords = useMemo(() => {
    const q = query.trim().toLowerCase();
    let list = records;
    if (q) {
      list = records.filter(
        (r) =>
          r.id.toLowerCase().includes(q) ||
          r.title.toLowerCase().includes(q) ||
          (r.primary_sn_uid || "").toLowerCase().includes(q),
      );
    }
    if (edition !== "v2" || !orderIndex) return list;

    const rank = (id: string): number => {
      const n = saNum(id);
      const info = orderIndex.by_sa_t99[String(n)];
      if (!info) return 1_000_000 + n;
      if (info.role === "appendix") return 2_000_000 + (info.seq_appendix || 0);
      return info.seq || 1_000_000 + n;
    };
    return [...list].sort((a, b) => rank(a.id) - rank(b.id));
  }, [records, query, edition, orderIndex]);

  const filteredV3 = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return v3Units;
    return v3Units.filter(
      (u) =>
        u.id.toLowerCase().includes(q) ||
        u.title.toLowerCase().includes(q) ||
        u.chapter_title.toLowerCase().includes(q) ||
        String(u.source_sa).includes(q) ||
        (u.primary_sn_uid || "").toLowerCase().includes(q),
    );
  }, [v3Units, query]);

  const activeRecord =
    edition === "v3"
      ? null
      : records.find((r) => r.id === activeId) || filteredRecords[0];
  const activeV3 =
    edition === "v3"
      ? v3Units.find((u) => u.id === activeId) || filteredV3[0]
      : null;
  const activeOrder = activeRecord
    ? orderIndex?.by_sa_t99[String(saNum(activeRecord.id))]
    : undefined;

  const base = import.meta.env.BASE_URL;
  const pdfV1 = `${base}books/v1-taisho.pdf`;
  const pdfV2 = `${base}books/v2-reorder.pdf`;
  const pdfV3 = `${base}books/v3-dharma.pdf`;

  const btn = (ed: Edition, label: string, disabled = false) => (
    <button
      type="button"
      onClick={() => setEdition(ed)}
      disabled={disabled}
      className={`flex-1 rounded px-1.5 py-1.5 ${
        edition === ed
          ? "bg-[#3a2e1c] text-[#f0d9a8]"
          : "text-[#8a7a60] hover:bg-[#241c14]"
      } disabled:opacity-40`}
    >
      {label}
    </button>
  );

  return (
    <div className="flex h-full flex-col overflow-hidden">
      <header className="shrink-0 border-b border-[#5c4a2e]/50 bg-[#14100c]/95 px-5 py-4 backdrop-blur">
        <div className="mx-auto flex max-w-[1600px] flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl text-[#f0d9a8]">杂阿含 · 罗什风对照</h1>
            <p className="mt-1 text-sm text-[#a89880]">{editionLabel(edition)}</p>
            <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs">
              <a
                href={pdfV1}
                download="杂阿含-研究译注本-大正卷序.pdf"
                className="text-[#c4a35a] underline-offset-2 hover:text-[#f0d9a8] hover:underline"
              >
                V1 PDF
              </a>
              <span className="text-[#5c4a2e]">·</span>
              <a
                href={pdfV2}
                download="杂阿含-研究译注本-经序重排.pdf"
                className="text-[#c4a35a] underline-offset-2 hover:text-[#f0d9a8] hover:underline"
              >
                V2 PDF
              </a>
              <span className="text-[#5c4a2e]">·</span>
              <a
                href={pdfV3}
                download="杂阿含-法义读本.pdf"
                className="text-[#c4a35a] underline-offset-2 hover:text-[#f0d9a8] hover:underline"
              >
                V3 PDF
              </a>
            </div>
          </div>
          {edition !== "v3" && activeRecord ? (
            <div className="text-right text-xs text-[#b8a48a]">
              <div>{activeRecord.id}</div>
              {edition === "v2" &&
              activeOrder?.role === "main" &&
              activeOrder.seq != null ? (
                <div>学术序 seq {activeOrder.seq}</div>
              ) : null}
              {edition === "v2" && activeOrder?.role === "appendix" ? (
                <div>V2 附录（T99 插入）</div>
              ) : null}
              <div>
                {activeRecord.primary_sn_uid
                  ? `主平行 ${activeRecord.primary_sn_uid}`
                  : "无 SN 主平行"}
              </div>
              <div>状态 {activeRecord.review_status || "raw"}</div>
            </div>
          ) : null}
          {edition === "v3" && activeV3 ? (
            <div className="text-right text-xs text-[#b8a48a]">
              <div>
                通读第 {activeV3.seq} 篇
                {activeV3.source_sas?.length
                  ? ` · 熔 SA ${activeV3.source_sas.join("/")}`
                  : activeV3.source_sa
                    ? ` · 大正第 ${activeV3.source_sa} 经`
                    : ""}
              </div>
              <div>{activeV3.chapter_title}</div>
              <div>
                {activeV3.primary_sn_uid
                  ? `主平行 ${activeV3.primary_sn_uid}`
                  : "无 SN 主平行"}
              </div>
            </div>
          ) : null}
        </div>
      </header>

      <div className="mx-auto flex min-h-0 w-full max-w-[1600px] flex-1 gap-4 overflow-hidden p-4">
        <aside className="flex h-full max-h-full w-64 shrink-0 flex-col overflow-hidden rounded-xl border border-[#5c4a2e]/40 bg-[#18140f]">
          <div className="shrink-0 border-b border-white/10 p-3">
            <div className="mb-2 flex gap-1 text-[11px]">
              {btn("v1", "V1 卷序")}
              {btn("v2", "V2 重排", !orderIndex)}
              {btn("v3", "V3 法义", v3Units.length === 0)}
            </div>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={edition === "v3" ? "搜索篇名 / 章 / 经号" : "搜索经号 / 标题"}
              className="w-full rounded-md border border-[#5c4a2e]/60 bg-[#0f0c09] px-3 py-2 text-sm outline-none focus:border-[#c4a35a]"
            />
            <p className="mt-2 text-xs text-[#8a7a60]">
              {edition === "v3"
                ? `共 ${filteredV3.length} 篇 · 法义通读`
                : `共 ${filteredRecords.length} 部 · ${
                    edition === "v2" ? "学术序" : "大正经号"
                  }`}
            </p>
          </div>
          <nav className="min-h-0 flex-1 overflow-y-auto overscroll-contain p-2">
            {error ? (
              <p className="p-2 text-sm text-red-300">加载失败：{error}</p>
            ) : null}
            {edition === "v3"
              ? filteredV3.map((u) => (
                  <button
                    key={u.id}
                    type="button"
                    onClick={() => setActiveId(u.id)}
                    className={`mb-1 w-full rounded-lg px-3 py-2 text-left text-sm transition ${
                      activeV3?.id === u.id
                        ? "bg-[#3a2e1c] text-[#f0d9a8]"
                        : "text-[#cbb89a] hover:bg-[#241c14]"
                    }`}
                  >
                    <div className="font-medium">
                      {u.seq}. {u.title}
                    </div>
                    <div className="truncate text-xs opacity-70">
                      {u.chapter_title} · SA {u.source_sa}
                    </div>
                  </button>
                ))
              : filteredRecords.map((r) => {
                  const info = orderIndex?.by_sa_t99[String(saNum(r.id))];
                  return (
                    <button
                      key={r.id}
                      type="button"
                      onClick={() => setActiveId(r.id)}
                      className={`mb-1 w-full rounded-lg px-3 py-2 text-left text-sm transition ${
                        activeRecord?.id === r.id
                          ? "bg-[#3a2e1c] text-[#f0d9a8]"
                          : "text-[#cbb89a] hover:bg-[#241c14]"
                      }`}
                    >
                      <div className="font-medium">
                        {r.id}
                        {edition === "v2" &&
                        info?.role === "main" &&
                        info.seq != null
                          ? ` · seq ${info.seq}`
                          : ""}
                        {edition === "v2" && info?.role === "appendix"
                          ? " · 附录"
                          : ""}
                      </div>
                      <div className="truncate text-xs opacity-70">{r.title}</div>
                    </button>
                  );
                })}
          </nav>
        </aside>

        <main className="flex min-h-0 min-w-0 flex-1 flex-col gap-3 overflow-hidden">
          {edition === "v3" ? (
            !activeV3 ? (
              <p className="text-[#a89880]">尚无法义读本数据。请运行 make v3-reader。</p>
            ) : (
              <>
                <div className="rounded-lg border border-[#5c4a2e]/30 bg-[#18140f] px-4 py-3 text-sm text-[#cbb89a]">
                  <div className="text-[#f0d9a8]">
                    {activeV3.review_status === "gold_reconstructed" ? "◇ " : ""}
                    {activeV3.title}
                  </div>
                  <div className="mt-1 text-xs text-[#c4a35a]">
                    {activeV3.chapter_title}
                  </div>
                  {activeV3.note ? (
                    <div className="mt-2 text-xs leading-5 text-[#9a8b70]">
                      <span className="text-[#c4a35a]">附注：</span>
                      {activeV3.note}
                    </div>
                  ) : null}
                </div>
                <div className="grid min-h-0 flex-1 gap-3 overflow-hidden lg:grid-cols-2">
                  <Panel title="罗什风正文" subtitle="法义通读主文" tone="gold">
                    {normalizeChineseQuotes(activeV3.kumarajiva_style_text) || (
                      <span className="text-[#8a7a60]">尚未生成</span>
                    )}
                  </Panel>
                  <Panel title="今译意" subtitle="与正文对照" tone="plain">
                    {normalizeChineseQuotes(activeV3.modern_psychology_text) || (
                      <span className="text-[#6f7a68]">尚未生成</span>
                    )}
                  </Panel>
                </div>
              </>
            )
          ) : !activeRecord ? (
            <p className="text-[#a89880]">尚无数据。请先运行对齐与翻译脚本。</p>
          ) : (
            <>
              <div className="rounded-lg border border-[#5c4a2e]/30 bg-[#18140f] px-4 py-3 text-sm text-[#cbb89a]">
                <div className="text-[#f0d9a8]">
                  {activeRecord.review_status === "gold_reconstructed" ? "◇ " : ""}
                  {activeRecord.title}
                </div>
                {(() => {
                  const tag = suttaReaderTag(activeRecord);
                  return tag ? (
                    <div className="mt-1 text-xs text-[#c4a35a]">{tag}</div>
                  ) : null;
                })()}
                {activeRecord.notes ? (
                  <div className="mt-2 text-xs leading-5 text-[#9a8b70]">
                    <span className="text-[#c4a35a]">校勘：</span>
                    {cleanNotes(activeRecord.notes)}
                  </div>
                ) : null}
              </div>

              <div className="grid min-h-0 flex-1 gap-3 overflow-hidden lg:grid-cols-3">
                <Panel
                  title="罗什风新译"
                  subtitle="据平行义改写 · 须见罗什风，禁止繁转简"
                  tone="gold"
                >
                  {normalizeChineseQuotes(activeRecord.kumarajiva_style_text) || (
                    <span className="text-[#8a7a60]">尚未生成</span>
                  )}
                </Panel>
                <Panel
                  title="底本与平行"
                  subtitle="求那跋陀罗译 + 参考英译 / SN"
                  tone="ink"
                >
                  <div className="mb-4">
                    <div className="mb-1 text-xs tracking-widest text-[#7f9bb8]">
                      汉译底本
                    </div>
                    {cleanChineseText(activeRecord.chinese_text)}
                  </div>
                  {(() => {
                    const en = englishSourceLabel(activeRecord);
                    return en ? (
                      <div className="mb-4 border-t border-white/10 pt-4">
                        <div className="mb-1 text-xs tracking-widest text-[#7f9bb8]">
                          参考英译（{en.attr}）
                        </div>
                        <div className="font-sans text-[15px] leading-7 text-[#c5d0da]">
                          {en.text}
                        </div>
                      </div>
                    ) : null;
                  })()}
                  {activeRecord.pali_text ? (
                    <div className="mt-4 border-t border-white/10 pt-4">
                      <div className="mb-1 text-xs tracking-widest text-[#7f9bb8]">
                        Pāli
                      </div>
                      <div className="font-sans text-[14px] leading-7 text-[#a8b4c0] italic">
                        {activeRecord.pali_text}
                      </div>
                    </div>
                  ) : null}
                </Panel>
                <Panel
                  title="现代白话"
                  subtitle="与罗什风逐段对照 · 开经结经不省"
                  tone="plain"
                >
                  {normalizeChineseQuotes(activeRecord.modern_psychology_text) || (
                    <span className="text-[#6f7a68]">尚未生成</span>
                  )}
                </Panel>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}
