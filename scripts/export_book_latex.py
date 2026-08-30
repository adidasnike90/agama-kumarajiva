#!/usr/bin/env python3
"""Export full SA corpus to LaTeX research edition (book/generated/).

Usage:
  python scripts/export_book_latex.py
  cd book && xelatex -interaction=nonstopmode main.tex  # x3 for TOC

Output:
  book/generated/juan_*.tex
  book/generated/all_juan.tex
  book/generated/reconstructed_index.tex
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from book.reader import (  # noqa: E402
    clean_chinese_text,
    clean_notes,
    normalize_chinese_quotes,
    format_parallels_reader,
    juan_chapter_title,
    label_critical,
    label_literary,
    label_modern,
    label_parallels,
    label_source,
    samyukta_sections,
    simp,
    sutta_heading,
    sutta_tag,
    uid_to_reader,
)
from pipeline.titles import juan_label, short_title, to_cn_num  # noqa: E402

CORPUS = ROOT / "data" / "translated" / "final_translated_data.json"
OUT_DIR = ROOT / "book" / "generated"

_TEX_ESC = str.maketrans(
    {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
)

_CN = "零一二三四五六七八九十"


def tex_escape(text: str) -> str:
    if not text:
        return ""
    return text.translate(_TEX_ESC)


def tex_paragraphs(text: str) -> str:
    text = text.strip()
    if not text:
        return r"\textit{（无）}" + "\n"
    parts = re.split(r"\n\s*\n", text)
    if len(parts) == 1:
        parts = [p for p in text.split("\n") if p.strip()]
    out: list[str] = []
    for i, p in enumerate(parts):
        p = p.strip()
        if not p:
            continue
        out.append(tex_escape(p))
        if i < len(parts) - 1:
            out.append("\n\n")
    return "".join(out) if out else r"\textit{（无）}" + "\n"


def format_parallels(rec: dict) -> str:
    lines = [tex_escape(simp(line)) for line in format_parallels_reader(rec)]
    return "\n\n".join(lines) + "\n" if lines else r"\textit{（无）}" + "\n"


def render_sutta(rec: dict, *, title_cmd: str = "sattitle") -> str:
    n = int(rec["id"].split("_")[1])
    heading = tex_escape(sutta_heading(n, rec))
    tag = sutta_tag(rec)
    tag_block = f"\\noindent\\textit{{{tex_escape(tag)}}}\\par\\vspace{{0.2em}}\n" if tag else ""

    lit = normalize_chinese_quotes(rec.get("kumarajiva_style_text") or "")
    mod = normalize_chinese_quotes(rec.get("modern_psychology_text") or "")
    src = clean_chinese_text(rec.get("chinese_text") or "")
    notes = clean_notes(rec.get("notes") or "")

    return "\n".join(
        [
            f"\\{title_cmd}{{{heading}}}",
            tag_block,
            f"\\noindent{{\\bfseries {label_literary()}}}\\par",
            "\\begin{quotation}",
            tex_paragraphs(lit),
            "\\end{quotation}",
            f"\\noindent{{\\bfseries {label_modern()}}}\\par",
            "\\begin{quotation}\\small",
            tex_paragraphs(mod),
            "\\end{quotation}",
            f"\\noindent{{\\bfseries {label_source()}}}\\par",
            "\\begin{quotation}\\footnotesize",
            tex_paragraphs(src),
            "\\end{quotation}",
            f"\\noindent{{\\bfseries {label_parallels()}}}\\par",
            "\\begin{quotation}\\footnotesize",
            format_parallels(rec),
            "\\end{quotation}",
            f"\\noindent{{\\bfseries {label_critical()}}}\\par",
            "\\begin{quotation}\\footnotesize",
            tex_paragraphs(notes) if notes else r"\textit{（无额外校勘）}",
            "\\end{quotation}",
            "\\suttahrule",
            "",
        ]
    )


def juan_file_id(jlabel: str) -> str:
    """卷第一→01, 卷第十一→11, 卷第二十五→25, 卷第五十→50."""
    s = jlabel.replace("第", "").replace("卷", "")
    if s == "十":
        n = 10
    elif len(s) == 1:
        n = _CN.index(s)
    elif len(s) == 2 and s[1] == "十":
        n = _CN.index(s[0]) * 10
    elif len(s) == 2 and s[0] == "十":
        n = 10 + _CN.index(s[1])
    elif len(s) == 3 and s[1] == "十":
        n = _CN.index(s[0]) * 10 + _CN.index(s[2])
    else:
        n = 0
    return str(n).zfill(2)


def juan_ranges() -> list[tuple[int, int, str]]:
    ends = json.loads((ROOT / "data" / "metadata" / "juan_ends.json").read_text())
    out: list[tuple[int, int, str]] = []
    start = 1
    for end, label in ends:
        out.append((start, int(end), label))
        start = int(end) + 1
    return out


def write_reconstructed_index(recs: list[dict]) -> None:
    recon = [r for r in recs if r.get("review_status") == "gold_reconstructed"]
    lines = [
        r"\chapter*{附录：重建经目录}",
        r"\addcontentsline{toc}{chapter}{附录：重建经目录}",
        "",
        r"以下 \textbf{" + str(len(recon)) + r"} 部汉本仅为「亦如是」等一句，",
        r"据巴利或同型经补最小可读文；引用时请注明「重建」。",
        "",
        r"\begin{longtable}{@{}rlc@{}}",
        r"\toprule",
        r"经号 & 短题 & 备注 \\",
        r"\midrule",
        r"\endhead",
    ]
    for r in sorted(recon, key=lambda x: int(x["id"].split("_")[1])):
        n = int(r["id"].split("_")[1])
        lines.append(
            f"第{to_cn_num(n)}经 & {tex_escape(simp(short_title(n, r.get('title'))))} & "
            f"重建 \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\clearpage", ""])
    (OUT_DIR / "reconstructed_index.tex").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    recs = json.loads(CORPUS.read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in recs}
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    juan_inputs: list[str] = []
    for start, end, jlabel in juan_ranges():
        sections = samyukta_sections(start, end)
        chapter = juan_chapter_title(start, end)
        chunk = [f"\\juan{{{tex_escape(chapter)}}}", f"\\label{{juan:{jlabel}}}", ""]
        multi_section = len(sections) > 1
        title_cmd = "sattitle" if multi_section else "sattitlesec"
        for sec_lo, sec_hi, sec_label in sections:
            if multi_section:
                chunk.append(f"\\samyukta{{{tex_escape(sec_label)}}}")
                chunk.append("")
            for n in range(sec_lo, sec_hi + 1):
                rid = f"SA_{n}"
                if rid in by_id:
                    chunk.append(render_sutta(by_id[rid], title_cmd=title_cmd))

        fname = f"juan_{juan_file_id(jlabel)}.tex"
        (OUT_DIR / fname).write_text("\n".join(chunk), encoding="utf-8")
        juan_inputs.append(f"\\input{{generated/{fname[:-4]}}}")

    (OUT_DIR / "all_juan.tex").write_text("\n".join(juan_inputs) + "\n", encoding="utf-8")
    write_reconstructed_index(recs)

    print(f"exported {len(recs)} suttas to {OUT_DIR}")
    print(f"  juan files: {len(juan_inputs)}")
    print(
        "  reconstructed:",
        sum(1 for r in recs if r.get("review_status") == "gold_reconstructed"),
    )


if __name__ == "__main__":
    main()
