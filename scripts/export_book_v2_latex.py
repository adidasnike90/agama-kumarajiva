#!/usr/bin/env python3
"""Export V2 academic-order research edition to book_v2/generated/.

V1 (book/) stays on T99 fascicle order. V2 is a **separate book**:
Anesaki/Yinshun fascicle reading order + appendix for T99 insertions.

Usage:
  make v2-order          # ensure academic_order.json exists
  python scripts/export_book_v2_latex.py
  make book-v2
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import export_book_latex as v1exp  # noqa: E402
from pipeline.titles import to_cn_num  # noqa: E402

CORPUS = ROOT / "data" / "translated" / "final_translated_data.json"
ORDER = ROOT / "data" / "metadata" / "v2" / "academic_order.json"
OUT_DIR = ROOT / "book_v2" / "generated"

tex_escape = v1exp.tex_escape
render_sutta = v1exp.render_sutta
write_reconstructed_index = v1exp.write_reconstructed_index



def _slot_chapter_title(slot: int, t99_juan: int, juan_label: str) -> str:
    return f"学术卷第{to_cn_num(slot)}（大正卷{juan_label}）"


def main() -> None:
    if not ORDER.is_file():
        raise SystemExit(f"missing {ORDER}; run: make v2-order")

    order = json.loads(ORDER.read_text(encoding="utf-8"))
    recs = json.loads(CORPUS.read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in recs}
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- main: group by academic_fascicle_slot (Anesaki stream) ---
    by_slot: dict[int, list[dict]] = {}
    retained: list[dict] = []
    for row in order["suttas_main"]:
        if row.get("stream") == "anesaki" and row.get("academic_fascicle_slot"):
            by_slot.setdefault(int(row["academic_fascicle_slot"]), []).append(row)
        else:
            retained.append(row)

    inputs: list[str] = []
    for slot in sorted(by_slot):
        rows = by_slot[slot]
        t99_juan = rows[0]["t99_juan"]
        jlabel = rows[0]["t99_juan_label"]
        title = _slot_chapter_title(slot, t99_juan, jlabel)
        chunk = [
            f"\\juan{{{tex_escape(title)}}}",
            f"\\label{{v2juan:{slot}}}",
            "",
        ]
        for row in rows:
            rid = f"SA_{row['sa_t99']}"
            if rid not in by_id:
                continue
            # Show both seq and T99 number in heading via existing sutta_heading;
            # add a thin editorial line for dual ID.
            seq = row["seq"]
            dual = (
                f"\\noindent\\textit{{学术序第{to_cn_num(seq)}经"
                f" · 大正第{to_cn_num(row['sa_t99'])}经}}\\par\\vspace{{0.25em}}\n"
            )
            body = render_sutta(by_id[rid], title_cmd="sattitlesec")
            # Insert dual-ID line after \sattitlesec{...}
            parts = body.split("\n", 1)
            body = parts[0] + "\n" + dual + (parts[1] if len(parts) > 1 else "")
            chunk.append(body)

        fname = f"slot_{str(slot).zfill(2)}.tex"
        (OUT_DIR / fname).write_text("\n".join(chunk), encoding="utf-8")
        inputs.append(f"\\input{{generated/{fname[:-4]}}}")

    # --- retained juan 23/25 block ---
    if retained:
        chunk = [
            r"\juan{附：大正卷二十三、二十五所收经（阶段一暂置）}",
            r"\label{v2juan:retained}",
            "",
            r"\noindent 下列经文在 Anesaki 四十八卷表中无对应卷位；"
            r"阶段一为保证不缺号而暂置于此，阶段二将按印顺相应表再挂接。"
            r"\par\vspace{1em}",
            "",
        ]
        for row in retained:
            rid = f"SA_{row['sa_t99']}"
            if rid not in by_id:
                continue
            seq = row["seq"]
            dual = (
                f"\\noindent\\textit{{学术序第{to_cn_num(seq)}经"
                f" · 大正第{to_cn_num(row['sa_t99'])}经}}\\par\\vspace{{0.25em}}\n"
            )
            body = render_sutta(by_id[rid], title_cmd="sattitlesec")
            parts = body.split("\n", 1)
            body = parts[0] + "\n" + dual + (parts[1] if len(parts) > 1 else "")
            chunk.append(body)
        (OUT_DIR / "retained_23_25.tex").write_text("\n".join(chunk), encoding="utf-8")
        inputs.append(r"\input{generated/retained_23_25}")

    # --- appendix: insertions ---
    app_chunk = [
        r"\juan{附录：T99 插入经（非早期相应经）}",
        r"\label{v2juan:appendix}",
        "",
        r"\noindent 第 604、640、641 经属阿育王传说杂入，不入学术正编阅读序；"
        r"保留于此以便与大正本对照。\par\vspace{1em}",
        "",
    ]
    for row in order["suttas_appendix"]:
        rid = f"SA_{row['sa_t99']}"
        if rid not in by_id:
            continue
        dual = (
            f"\\noindent\\textit{{附录 · 大正第{to_cn_num(row['sa_t99'])}经}}\\par\\vspace{{0.25em}}\n"
        )
        body = render_sutta(by_id[rid], title_cmd="sattitlesec")
        parts = body.split("\n", 1)
        body = parts[0] + "\n" + dual + (parts[1] if len(parts) > 1 else "")
        app_chunk.append(body)
    (OUT_DIR / "appendix_insertions.tex").write_text(
        "\n".join(app_chunk), encoding="utf-8"
    )
    inputs.append(r"\input{generated/appendix_insertions}")

    (OUT_DIR / "all_body.tex").write_text("\n".join(inputs) + "\n", encoding="utf-8")

    old = v1exp.OUT_DIR
    v1exp.OUT_DIR = OUT_DIR
    try:
        write_reconstructed_index(recs)
    finally:
        v1exp.OUT_DIR = old

    print(f"exported V2 book to {OUT_DIR}")
    print(f"  anesaki slots: {len(by_slot)}")
    print(f"  retained 23/25 rows: {len(retained)}")
    print(f"  appendix: {len(order['suttas_appendix'])}")


if __name__ == "__main__":
    main()
