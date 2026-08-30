import { useEffect, useMemo, useState, type ReactNode } from "react";
import type { SutraRecord } from "./types";
import { cleanChineseText, cleanNotes, englishSourceLabel, normalizeChineseQuotes, suttaReaderTag } from "./reader";

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

export default function App() {
  const [records, setRecords] = useState<SutraRecord[]>([]);
  const [activeId, setActiveId] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [query, setQuery] = useState("");

  useEffect(() => {
    const dataUrl = `${import.meta.env.BASE_URL}final_translated_data.json`;
    fetch(dataUrl)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data: SutraRecord[]) => {
        setRecords(data);
        if (data[0]) setActiveId(data[0].id);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return records;
    return records.filter(
      (r) =>
        r.id.toLowerCase().includes(q) ||
        r.title.toLowerCase().includes(q) ||
        (r.primary_sn_uid || "").toLowerCase().includes(q),
    );
  }, [records, query]);

  const active = records.find((r) => r.id === activeId) || filtered[0];

  return (
    <div className="flex h-full flex-col overflow-hidden">
      <header className="shrink-0 border-b border-[#5c4a2e]/50 bg-[#14100c]/95 px-5 py-4 backdrop-blur">
        <div className="mx-auto flex max-w-[1600px] flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl text-[#f0d9a8]">杂阿含 · 罗什风对照</h1>
            <p className="mt-1 text-sm text-[#a89880]">
              风格迁移 · 信＝巴利／梵本义 · 雅＝罗什风（非汉译简体化） · 平行据 SuttaCentral
            </p>
          </div>
          {active ? (
            <div className="text-right text-xs text-[#b8a48a]">
              <div>{active.id}</div>
              <div>
                {active.primary_sn_uid
                  ? `主平行 ${active.primary_sn_uid}`
                  : "无 SN 主平行"}
              </div>
              <div>
                状态 {active.review_status || "raw"}
                {active.translator ? ` · ${active.translator}` : ""}
                {active.confidence ? ` · ${active.confidence}` : ""}
              </div>
              {active.validation?.status ? (
                <div>校验 {active.validation.status}</div>
              ) : null}
            </div>
          ) : null}
        </div>
      </header>

      <div className="mx-auto flex min-h-0 w-full max-w-[1600px] flex-1 gap-4 overflow-hidden p-4">
        <aside className="flex h-full max-h-full w-64 shrink-0 flex-col overflow-hidden rounded-xl border border-[#5c4a2e]/40 bg-[#18140f]">
          <div className="shrink-0 border-b border-white/10 p-3">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="搜索经号 / 标题"
              className="w-full rounded-md border border-[#5c4a2e]/60 bg-[#0f0c09] px-3 py-2 text-sm outline-none focus:border-[#c4a35a]"
            />
            <p className="mt-2 text-xs text-[#8a7a60]">
              共 {filtered.length} 部
            </p>
          </div>
          <nav className="min-h-0 flex-1 overflow-y-auto overscroll-contain p-2">
            {error ? (
              <p className="p-2 text-sm text-red-300">加载失败：{error}</p>
            ) : null}
            {filtered.map((r) => (
              <button
                key={r.id}
                type="button"
                onClick={() => setActiveId(r.id)}
                className={`mb-1 w-full rounded-lg px-3 py-2 text-left text-sm transition ${
                  active?.id === r.id
                    ? "bg-[#3a2e1c] text-[#f0d9a8]"
                    : "text-[#cbb89a] hover:bg-[#241c14]"
                }`}
              >
                <div className="font-medium">{r.id}</div>
                <div className="truncate text-xs opacity-70">{r.title}</div>
              </button>
            ))}
          </nav>
        </aside>

        <main className="flex min-h-0 min-w-0 flex-1 flex-col gap-3 overflow-hidden">
          {!active ? (
            <p className="text-[#a89880]">尚无数据。请先运行对齐与翻译脚本。</p>
          ) : (
            <>
              <div className="rounded-lg border border-[#5c4a2e]/30 bg-[#18140f] px-4 py-3 text-sm text-[#cbb89a]">
                <div className="text-[#f0d9a8]">
                  {active.review_status === "gold_reconstructed" ? "◇ " : ""}
                  {active.title}
                </div>
                {(() => {
                  const tag = suttaReaderTag(active);
                  return tag ? (
                    <div className="mt-1 text-xs text-[#c4a35a]">{tag}</div>
                  ) : null;
                })()}
                {active.notes ? (
                  <div className="mt-2 text-xs leading-5 text-[#9a8b70]">
                    <span className="text-[#c4a35a]">校勘：</span>
                    {cleanNotes(active.notes)}
                  </div>
                ) : null}
                {active.forbidden_hits && active.forbidden_hits.length > 0 ? (
                  <div className="mt-1 text-xs text-amber-300">
                    禁用词命中：{active.forbidden_hits.join("、")}
                  </div>
                ) : null}
                {active.validation?.warnings &&
                active.validation.warnings.length > 0 ? (
                  <div className="mt-1 text-xs text-[#b8a070]">
                    校验提示：{active.validation.warnings.join("；")}
                  </div>
                ) : null}
              </div>

              <div className="grid min-h-0 flex-1 gap-3 overflow-hidden lg:grid-cols-3">
                <Panel
                  title="罗什风新译"
                  subtitle="据平行义改写 · 须见罗什风，禁止繁转简"
                  tone="gold"
                >
                  {normalizeChineseQuotes(active.kumarajiva_style_text) || (
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
                    {cleanChineseText(active.chinese_text)}
                  </div>
                  {(() => {
                    const en = englishSourceLabel(active);
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
                  {active.pali_text ? (
                    <div className="mt-4 border-t border-white/10 pt-4">
                      <div className="mb-1 text-xs tracking-widest text-[#7f9bb8]">
                        Pāli
                      </div>
                      <div className="font-sans text-[14px] leading-7 text-[#a8b4c0] italic">
                        {active.pali_text}
                      </div>
                    </div>
                  ) : null}
                </Panel>
                <Panel
                  title="现代白话"
                  subtitle="与罗什风逐段对照 · 开经结经不省"
                  tone="plain"
                >
                  {normalizeChineseQuotes(active.modern_psychology_text) || (
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
