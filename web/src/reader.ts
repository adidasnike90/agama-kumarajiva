/** Reader-facing display helpers (mirrors book/reader.py). */

export function cleanChineseText(text: string): string {
  if (!text) return "";
  let s = text.trim();
  s = s.replace(/^Saṁyuktāgama(?:雜阿含經|杂阿含经)?\s*/, "");
  s = s.replace(
    /^(?:\u3000\s*\n+)?(?:雜阿含經|杂阿含经)卷[^\n]+\n+\s*宋天竺三藏求那跋陀(?:罗|羅)譯\s*\n+/,
    "",
  );
  s = s.replace(
    /^[ \u3000\t]*(?:雜阿含經|杂阿含经)\s*卷第[^\n]*\n+/gm,
    "",
  );
  s = s.replace(
    /\n+[ \u3000\t]*(?:雜阿含經|杂阿含经)\s*卷第[^\n]*\s*$/,
    "",
  );
  s = s.replace(/(?:雜阿含經|杂阿含经)\s*卷第[^\n]*\s*$/gm, "");
  s = s.replace(/\n{3,}/g, "\n\n");
  return s.trim();
}

export function cleanNotes(notes: string): string {
  if (!notes) return "";
  let s = notes;
  s = s.replace(/本经 SC 平行表所列平行及.*?传统术语。/, "");
  s = s.replace(
    /SC 于本经未列可靠巴利平行.*?medium\/low」。/,
    "无可靠巴利平行，依汉本并参同类型经厘定。",
  );
  s = s.replace(/confidence\s*=\s*high[：:]?/g, "据平行经");
  s = s.replace(/confidence\s*=\s*medium[：:]?/g, "平行较弱");
  s = s.replace(/confidence\s*=\s*low[：:]?/g, "无强平行");
  s = s.replace(/review_status\s*=\s*gold_reconstructed[，,]?/g, "");
  s = s.replace(/gold_reconstructed[，,]?/g, "");
  s = s.replace(/`raw_aligned_data\.json`/g, "语料");
  s = s.replace(/\s+/g, " ").trim().replace(/^[ ；，。]+|[ ；，。]+$/g, "");
  s = s.replace(/[：:](?=[。．.])/g, "");
  s = s.replace(/^(平行较弱|无强平行|据平行经)\s*$/, "");
  s = s.replace(/(平行较弱|无强平行|据平行经)\s*$/, "");
  return s.trim().replace(/^[ ；，。]+|[ ；，。]+$/g, "");
}

/** Replace ASCII '…' with nested Chinese quotes 『…』 in reader-facing prose. */
export function normalizeChineseQuotes(text: string): string {
  if (!text) return "";
  return text.replace(/'([^'\n]+)'/g, "『$1』");
}

/** Known Aśokavadāna insertions in T99 (mirrors data/metadata/t99_insertions.json). */
export const T99_INSERTION_IDS = new Set(["SA_604", "SA_640", "SA_641"]);

export function isT99Insertion(id: string): boolean {
  return T99_INSERTION_IDS.has(id);
}

export function t99InsertionTag(): string {
  return "〔T99插入·非相应经〕";
}

export function suttaReaderTag(rec: {
  id: string;
  review_status?: string;
}): string {
  if (rec.review_status === "gold_reconstructed") return "〔重建经·底本略〕";
  if (isT99Insertion(rec.id)) return t99InsertionTag();
  return "";
}

export function englishSourceLabel(rec: {
  english_sn_text?: string;
  english_sa_text?: string;
}): { text: string; attr: string } | null {
  const sn = (rec.english_sn_text || "").trim();
  if (sn) return { text: sn, attr: "Bhikkhu Sujato（CC0）" };
  const sa = (rec.english_sa_text || "").trim();
  if (!sa) return null;
  if (sa.startsWith("Thus I have heard") || sa.includes("Bhagavān")) {
    return { text: sa, attr: "Charles Patton（CC0）" };
  }
  return {
    text: sa,
    attr: "Bhikkhu Anālayo（原刊《法鼓佛学学报》等；SC 经译者授权在其平台刊载；本书仅短摘录）",
  };
}
