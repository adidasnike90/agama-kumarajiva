#!/usr/bin/env python3
"""Build v2 academic reading order from Anesaki/Yinshun fascicle reconstruction.

Phase 1 (this script):
  - Reorder T99 fascicles (卷) per Anesaki as adopted by Yinshun.
  - Move known non-Āgama insertions (SA 604, 640, 641) to an appendix stream.
  - Emit dual IDs: sa_t99 (stable) + seq (academic reading order).

Phase 2 (future): map Yinshun's 51 saṃyuktas onto SA ranges (manual / CSA tables).

Usage:
  python scripts/build_v2_academic_order.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data" / "metadata"
OUT_DIR = META / "v2"

# Anesaki reconstructed fascicle order (T99 卷第 N), as cited in secondary
# literature and adopted by Yinshun's CSA. Lists **48** fascicles: T99 卷 23、25
# are the two units scholars identify with non-SA Aśokavadāna replacements
# (Anālayo 2015; Bucknell). See docs/V2_ORDER.md.
FASCICLE_ORDER_ANESAKI: list[int] = [
    1,
    10,
    3,
    2,
    *range(5, 10),  # 5–9
    43,
    11,
    13,
    12,
    *range(14, 22),  # 14–21
    31,
    24,
    *range(26, 31),  # 26–30
    41,
    *range(32, 36),  # 32–35
    47,
    *range(37, 41),  # 37–40
    46,
    42,
    4,
    44,
    45,
    36,
    22,
    *range(48, 51),  # 48–50
]

# T99 fascicle numbers omitted from Anesaki's 48-list. In traditional accounts
# these are the Asoka replacement scrolls; our juan_ends.json still maps
# continuous SA ranges onto 卷23／25 — those SA ids (except known insertions)
# are appended after the Anesaki stream so every non-insertion SA appears once
# (phase-1 coverage). Phase 2 may reassign them when CSA ranges are aligned.
FASCICLES_OMITTED_FROM_ANESAKI: list[int] = [23, 25]


def juan_ranges(juan_ends: list[list]) -> dict[int, tuple[int, int, str]]:
    """Map 1-based juan index → (sa_lo, sa_hi, label)."""
    out: dict[int, tuple[int, int, str]] = {}
    prev = 0
    for i, (end, label) in enumerate(juan_ends, start=1):
        out[i] = (prev + 1, int(end), str(label))
        prev = int(end)
    return out


def load_insertions() -> set[int]:
    path = META / "t99_insertions.json"
    if not path.exists():
        return {604, 640, 641}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {int(n) for n in raw.get("sutta_ids") or []}


def build() -> dict:
    juan_ends = json.loads((META / "juan_ends.json").read_text(encoding="utf-8"))
    jmap = juan_ranges(juan_ends)
    insertions = load_insertions()

    anesaki = FASCICLE_ORDER_ANESAKI
    omitted = FASCICLES_OMITTED_FROM_ANESAKI
    if len(anesaki) != 48 or set(anesaki) & set(omitted):
        raise SystemExit("Anesaki list must be 48 fascicles disjoint from omitted 23/25")
    if sorted(anesaki + omitted) != list(range(1, 51)):
        raise SystemExit(
            f"fascicle coverage error: "
            f"{set(range(1, 51)) - set(anesaki) - set(omitted)}"
        )

    main: list[dict] = []
    appendix: list[dict] = []
    seq = 0

    def emit_juan(juan: int, slot: int | None, *, stream: str) -> None:
        nonlocal seq
        lo, hi, label = jmap[juan]
        for sa in range(lo, hi + 1):
            rec = {
                "sa_t99": sa,
                "t99_juan": juan,
                "t99_juan_label": label,
                "stream": stream,
            }
            if slot is not None:
                rec["academic_fascicle_slot"] = slot
            if sa in insertions:
                rec["role"] = "appendix"
                rec["appendix_reason"] = "t99_asokavadana_insertion"
                appendix.append(rec)
            else:
                seq += 1
                rec["role"] = "main"
                rec["seq"] = seq
                if stream == "t99_juan_23_25_retained":
                    rec["placement_note"] = (
                        "T99 fascicle omitted from Anesaki 48-list; "
                        "retained in phase-1 main for SA coverage"
                    )
                main.append(rec)

    for slot, juan in enumerate(anesaki, start=1):
        emit_juan(juan, slot, stream="anesaki")

    # After Anesaki stream: retain 卷23／25 non-insertion suttas (see docs).
    for juan in omitted:
        emit_juan(juan, None, stream="t99_juan_23_25_retained")

    # Appendix gets its own sequences after main (A1, A2… as seq_appendix)
    for i, rec in enumerate(appendix, start=1):
        rec["seq_appendix"] = i

    all_sa = {r["sa_t99"] for r in main} | {r["sa_t99"] for r in appendix}
    if all_sa != set(range(1, 1363)):
        raise SystemExit(
            f"SA coverage error: got {len(all_sa)}, missing="
            f"{sorted(set(range(1, 1363)) - all_sa)[:20]}"
        )

    return {
        "schema_version": 1,
        "edition": "v2-academic-order",
        "phase": "1_fascicle_reorder",
        "title_zh": "经序重排（Anesaki／印顺卷次）",
        "title_en": "Academic reading order (Anesaki/Yinshun fascicle reconstruction)",
        "disclaimer_zh": (
            "本序依学界通行之卷次重排假说，非宣称恢复出土原典卷次；"
            "T99 经号（sa_t99）为永久文献锚点。不声称鸠摩罗什曾译《杂阿含》。"
        ),
        "basis": [
            {
                "name": "Anesaki fascicle reconstruction",
                "note": "48 T99 fascicles reordered; adopted in Yinshun CSA and later editions",
            },
            {
                "name": "Yinshun 印顺《杂阿含经论会编》",
                "note": "Critical edition adopting reconstructed fascicle order + 51 saṃyuktas (phase 2)",
            },
            {
                "name": "Fascicles 23 & 25 / insertions SA 604, 640–641",
                "note": (
                    "Anālayo/Bucknell: juan 23 & 25 are non-SA Aśokavadāna replacements. "
                    "Known insertion suttas → appendix; other SA ids mapped to those juan "
                    "numbers in juan_ends.json are retained at end of main (phase-1)."
                ),
            },
        ],
        "references": [
            "Anesaki, Masaharu (1908). The Four Buddhist Āgamas in Chinese…",
            "Anālayo (2015). Saṃyukta-āgama Studies — fascicles 23 & 25",
            "Bucknell, Roderick S. on ZA scrolls 23 & 25",
            "Yinshun. 雜阿含經論會編 (CSA); CBETA Y0030",
            "docs/V2_ORDER.md in this repository",
        ],
        "fascicle_order_anesaki_t99": anesaki,
        "fascicles_omitted_from_anesaki_t99": omitted,
        "counts": {
            "main": len(main),
            "appendix": len(appendix),
            "total_sa": len(main) + len(appendix),
        },
        "suttas_main": main,
        "suttas_appendix": appendix,
    }


def write_index(payload: dict) -> dict:
    """Compact id → seq map for web / fast lookup."""
    by_t99: dict[str, dict] = {}
    for r in payload["suttas_main"]:
        by_t99[str(r["sa_t99"])] = {
            "seq": r["seq"],
            "role": "main",
            "t99_juan": r["t99_juan"],
            "stream": r.get("stream"),
            "academic_fascicle_slot": r.get("academic_fascicle_slot"),
        }
    for r in payload["suttas_appendix"]:
        by_t99[str(r["sa_t99"])] = {
            "seq_appendix": r["seq_appendix"],
            "role": "appendix",
            "t99_juan": r["t99_juan"],
            "stream": r.get("stream"),
            "academic_fascicle_slot": r.get("academic_fascicle_slot"),
            "appendix_reason": r.get("appendix_reason"),
        }
    return {
        "schema_version": 1,
        "phase": payload["phase"],
        "by_sa_t99": by_t99,
        "reading_order_sa_t99": [r["sa_t99"] for r in payload["suttas_main"]],
        "appendix_sa_t99": [r["sa_t99"] for r in payload["suttas_appendix"]],
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = build()
    order_path = OUT_DIR / "academic_order.json"
    index_path = OUT_DIR / "academic_order_index.json"
    fasc_path = OUT_DIR / "fascicle_order_anesaki.json"

    order_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    index = write_index(payload)
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    fasc_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "fascicle_order_anesaki_t99": FASCICLE_ORDER_ANESAKI,
                "fascicles_omitted_from_anesaki_t99": FASCICLES_OMITTED_FROM_ANESAKI,
                "note": (
                    "Anesaki 48-fascicle reconstruction; Yinshun CSA adopts this order. "
                    "T99 juan 23 & 25 omitted from list (Asoka-replacement fascicles)."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    c = payload["counts"]
    print(
        f"wrote {order_path.relative_to(ROOT)} "
        f"(main={c['main']}, appendix={c['appendix']})"
    )
    print(f"wrote {index_path.relative_to(ROOT)}")
    print(f"wrote {fasc_path.relative_to(ROOT)}")
    # sanity: first / last main
    print(
        "main head:",
        [r["sa_t99"] for r in payload["suttas_main"][:5]],
        "… tail:",
        [r["sa_t99"] for r in payload["suttas_main"][-5:]],
    )
    print("appendix:", [r["sa_t99"] for r in payload["suttas_appendix"]])


if __name__ == "__main__":
    main()
