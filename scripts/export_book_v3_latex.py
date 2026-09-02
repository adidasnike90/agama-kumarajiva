#!/usr/bin/env python3
"""Export V3 法义读本 to book_v3/generated/ — 正文 + 今译 + 附注 only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import export_book_latex as v1exp  # noqa: E402
from book.reader import (  # noqa: E402
    label_literary,
    label_modern,
    normalize_chinese_quotes,
)
from pipeline.titles import to_cn_num  # noqa: E402

UNITS = ROOT / "data" / "translated" / "v3_reader_units.json"
CATALOG = ROOT / "data" / "metadata" / "v3" / "catalog.json"
OUT_DIR = ROOT / "book_v3" / "generated"

tex_escape = v1exp.tex_escape
tex_paragraphs = v1exp.tex_paragraphs


def render_unit(u: dict) -> str:
    title = tex_escape(u["title"])
    lit = normalize_chinese_quotes(u.get("kumarajiva_style_text") or "")
    mod = normalize_chinese_quotes(u.get("modern_psychology_text") or "")
    note = (u.get("note") or "").strip()
    sources = u.get("source_sas") or [u.get("source_sa")]
    sources = [s for s in sources if s is not None]
    src_txt = "、".join(str(x) for x in sources[:8])
    if len(sources) > 8:
        src_txt += "等"
    lines = [
        f"\\sattitlesec{{{title}}}",
        f"\\noindent\\textit{{通读第{to_cn_num(u['seq'])}篇"
        f"（新拟篇题）· 熔大正第{src_txt}经}}\\par\\vspace{{0.25em}}",
        f"\\noindent{{\\bfseries {label_literary()}}}\\par",
        "\\begin{quotation}",
        tex_paragraphs(lit),
        "\\end{quotation}",
        f"\\noindent{{\\bfseries {label_modern()}}}\\par",
        "\\begin{quotation}\\small",
        tex_paragraphs(mod),
        "\\end{quotation}",
    ]
    if note:
        lines += [
            r"\noindent{\bfseries 【附注】}\par",
            r"\begin{quotation}\footnotesize",
            tex_paragraphs(note),
            r"\end{quotation}",
        ]
    lines += [r"\suttahrule", ""]
    return "\n".join(lines)
    if note:
        lines += [
            r"\noindent{\bfseries 【附注】}\par",
            r"\begin{quotation}\footnotesize",
            tex_paragraphs(note),
            r"\end{quotation}",
        ]
    lines += [r"\suttahrule", ""]
    return "\n".join(lines)


def main() -> None:
    if not UNITS.is_file():
        raise SystemExit(f"missing {UNITS}; run: make v3-reader")
    units = json.loads(UNITS.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8")) if CATALOG.is_file() else {}
    chapters = {c["id"]: c for c in catalog.get("chapters", [])}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    by_ch: dict[int, list[dict]] = {}
    for u in units:
        by_ch.setdefault(int(u["chapter_id"]), []).append(u)

    inputs: list[str] = []
    for cid in sorted(by_ch):
        ch = chapters.get(cid, {"title": f"第{cid}章", "blurb": ""})
        title = ch.get("title") or f"第{cid}章"
        blurb = ch.get("blurb") or ""
        chunk = [
            f"\\juan{{{tex_escape(title)}}}",
            f"\\label{{v3ch:{cid}}}",
            "",
        ]
        if blurb:
            chunk += [
                f"\\noindent\\textit{{{tex_escape(blurb)}}}\\par\\vspace{{1em}}",
                "",
            ]
        for u in sorted(by_ch[cid], key=lambda x: x["seq"]):
            chunk.append(render_unit(u))
        fname = f"chapter_{str(cid).zfill(2)}.tex"
        (OUT_DIR / fname).write_text("\n".join(chunk), encoding="utf-8")
        inputs.append(f"\\input{{generated/{fname[:-4]}}}")

    (OUT_DIR / "all_body.tex").write_text("\n".join(inputs) + "\n", encoding="utf-8")

    # Compact source index
    idx = [
        r"\chapter*{附录：出处简表}",
        r"\addcontentsline{toc}{chapter}{附录：出处简表}",
        "",
        r"下表便于回指研究译注本；篇名为通读新拟，非大正原题。",
        "",
        r"\begin{longtable}{rp{7cm}ll}",
        r"\toprule",
        r"通读序 & 所熔大正经号 & 新拟篇名 & 章 \\",
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        r"通读序 & 所熔大正经号 & 新拟篇名 & 章 \\",
        r"\midrule",
        r"\endhead",
    ]
    for u in units:
        sources = u.get("source_sas") or [u.get("source_sa")]
        src = "、".join(str(x) for x in sources if x is not None)
        idx.append(
            f"{u['seq']} & {tex_escape(src)} & "
            f"{tex_escape(u['title'])} & {tex_escape(u['chapter_title'])} \\\\"
        )
    idx += [r"\bottomrule", r"\end{longtable}", ""]
    (OUT_DIR / "source_index.tex").write_text("\n".join(idx) + "\n", encoding="utf-8")

    print(f"exported V3 book to {OUT_DIR} ({len(units)} units, {len(by_ch)} chapters)")


if __name__ == "__main__":
    main()
