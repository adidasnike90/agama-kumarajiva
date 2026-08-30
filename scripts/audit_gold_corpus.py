#!/usr/bin/env python3
"""Full-corpus audit of gold / gold_reconstructed entries for Kumarajiva-style quality.

Checks beyond trigram similarity:
  - literary vs modern divergence (双栏不同步)
  - compression vs Gunabhadra source (罗什应删冗)
  - calque / peyyāla tics retained in literary column
  - missing similarity field (early batches)
  - validation re-run

Outputs:
  data/translated/GOLD_AUDIT.json
  data/translated/GOLD_AUDIT.md

Usage: python scripts/audit_gold_corpus.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from translate.similarity import similarity_to_source, _to_simplified_approx  # noqa: E402
from translate.validate import validate_restyle, _norm  # noqa: E402

CORPUS = ROOT / "data" / "translated" / "final_translated_data.json"
OUT_JSON = ROOT / "data" / "translated" / "GOLD_AUDIT.json"
OUT_MD = ROOT / "data" / "translated" / "GOLD_AUDIT.md"

GOLD_STATUSES = {"gold", "gold_reconstructed"}

# Gunabhadra calque tics — high count in literary = not Kumarajiva restyle
CALQUE_PATTERNS: list[tuple[str, str]] = [
    (r"所以者何", "suoyihezhe"),
    (r"比丘！", "biqiu_exclaim"),
    (r"是名", "shiming"),
    (r"彼.+?彼", "bi_bi"),
    (r"若.+?若.+?若", "ru_ru_ru"),
    (r"问已不知|問已不知", "wen_bu_zhi"),
    (r"增其疑惑", "zeng_yi"),
    (r"以非境界", "fei_jingjie"),
    (r"眼肉形内", "yan_rou"),
    (r"是无常之我|是無常之我", "wuchang_zhi_wo"),
    (r"厌故不乐|厭故不樂", "yan_bu_le"),
    (r"不实来实去|不實來實去", "bu_shi_lai"),
    (r"刹那时顷|剎那時頃", "chana"),
    (r"明目士夫", "mingmu_shifu"),
    (r"独一静处|獨一靜處", "duyi_jing"),
    (r"往诣佛所|往詣佛所", "wang_yi"),
    (r"退住一面|退住一面", "tui_zhu"),
]

# Known source errors that should NOT survive in literary if 信>雅
SOURCE_ERROR_MARKERS = [
    "是无常之我",
    "是無常之我",
    "厌故不乐",
    "厭故不樂",
    "空诸行常、恒、住、不变易法空",
    "空諸行常、恆、住、不變易法空",
]


@dataclass
class AuditRow:
    id: str
    review_status: str
    confidence: str
    sim_lit: float
    sim_mod: float
    lit_mod_gap: float
    lit_len: int
    src_len: int
    compression: float  # lit_len / src_len (lower = more compressed)
    calque_hits: dict[str, int] = field(default_factory=dict)
    calque_score: int = 0
    source_errors_in_lit: list[str] = field(default_factory=list)
    stored_sim: float | None = None
    sim_drift: float | None = None
    validation_status: str = "ok"
    validation_issues: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)
    lit_eq_mod: bool = False
    lit_mod_overlap: float = 0.0
    template_flags: list[str] = field(default_factory=list)
    tier: str = "P3"
    tier_reasons: list[str] = field(default_factory=list)
    batch: str = ""


def _src_body(chinese: str) -> str:
    s = _to_simplified_approx(chinese)
    for strip in (
        "samyuktagama杂阿含经",
        "杂阿含经卷",
        "雜阿含經卷",
        "宋天竺三藏求那跋陀罗译",
        "宋天竺三藏求那跋陀羅譯",
    ):
        s = s.replace(strip, "")
    return s


def _count_calques(text: str) -> dict[str, int]:
    hits: dict[str, int] = {}
    for pat, key in CALQUE_PATTERNS:
        n = len(re.findall(pat, text))
        if n:
            hits[key] = n
    return hits


def _lit_mod_identity(lit: str, mod: str) -> tuple[bool, float]:
    """True if columns are identical after norm; overlap = char-prefix match ratio."""
    nl = _norm(re.sub(r"\s+", "", lit))
    nm = _norm(re.sub(r"\s+", "", mod))
    if not nl or not nm:
        return False, 0.0
    if nl == nm:
        return True, 1.0
    overlap = sum(1 for a, b in zip(nl, nm) if a == b) / max(len(nl), len(nm))
    return False, round(overlap, 3)


def _wrong_devata_wording(lit: str, src: str = "") -> list[str]:
    """Known template bugs (e.g. 有天 used where 天子 required)."""
    flags: list[str] = []
    src_n = _to_simplified_approx(src)
    lit_n = _to_simplified_approx(lit)
    if "天子" in src_n and "天子" not in lit_n:
        if re.search(r"(?<!神)有天(?![子神])", lit_n):
            flags.append("wrong_有天非天子")
    if "厌故不乐" in lit or "厭故不樂" in lit:
        flags.append("yan_bu_le")
    return flags


def _four_char_ratio(text: str) -> float:
    """Rough Kumarajiva cadence proxy: 4-char chunks separated by punctuation."""
    chunks = re.split(r"[，。；：！？、\n]", text)
    fours = sum(1 for c in chunks if 3 <= len(c.strip()) <= 5)
    total = sum(1 for c in chunks if len(c.strip()) >= 2)
    return round(fours / total, 3) if total else 0.0


def _batch_label(n: int) -> str:
    """20-sutta batch label."""
    lo = ((n - 1) // 20) * 20 + 1
    hi = min(lo + 19, 1362)
    return f"SA{lo}-{hi}"


def _assign_tier(row: AuditRow) -> None:
    reasons: list[str] = []
    tier = "P3"

    if row.source_errors_in_lit:
        tier = "P0"
        reasons.append(f"底本讹句残留:{','.join(row.source_errors_in_lit)}")

    if row.lit_eq_mod:
        tier = "P0"
        reasons.append("白话栏与罗什风栏完全相同")

    if row.template_flags:
        tier = "P0"
        reasons.append(f"模板错字:{','.join(row.template_flags)}")

    if row.validation_status == "fail":
        tier = "P0"
        reasons.append(f"validate fail: {row.validation_issues}")

    if row.review_status == "gold_reconstructed":
        if row.sim_lit >= 0.52 and row.lit_len >= 200:
            tier = max(tier, "P1", key=_tier_rank)
            reasons.append("gold_reconstructed 但 sim 偏高，疑非纲要式重写")
        else:
            row.tier = "RECON"
            row.tier_reasons = ["交叉指示／省文重建，单独验收"]
            return

    # Hard fails — 繁转简
    if row.sim_lit >= 0.55:
        tier = "P0"
        reasons.append(f"sim_lit={row.sim_lit:.3f}>=0.55")

    if row.sim_lit >= 0.50 and row.lit_len >= 400:
        tier = "P0"
        reasons.append(f"长经 sim={row.sim_lit:.3f}>=0.50")

    if row.lit_mod_gap >= 0.15 and row.sim_lit >= 0.42:
        if _tier_rank(tier) < _tier_rank("P0"):
            tier = "P1"
        reasons.append(f"双栏不同步 gap={row.lit_mod_gap:.3f}")

    if row.calque_score >= 8 and row.sim_lit >= 0.40:
        if _tier_rank(tier) < _tier_rank("P1"):
            tier = "P1"
        reasons.append(f"求那体 calque_score={row.calque_score}")

    if row.sim_lit >= 0.48 and row.lit_len >= 300:
        if _tier_rank(tier) < _tier_rank("P1"):
            tier = "P1"
        reasons.append(f"中长经 sim={row.sim_lit:.3f}")

    if row.sim_lit >= 0.45 or (row.sim_lit >= 0.42 and row.compression >= 0.85):
        if tier == "P3":
            tier = "P2"
            reasons.append(
                f"sim={row.sim_lit:.3f} 或 compression={row.compression:.2f} 偏高"
            )

    if row.lit_mod_overlap >= 0.95 and row.lit_len >= 80 and not row.lit_eq_mod:
        if _tier_rank(tier) > _tier_rank("P1"):
            tier = "P1"
        reasons.append(f"白话与罗什风高度重合 overlap={row.lit_mod_overlap:.3f}")

    if row.stored_sim is None:
        reasons.append("未存 similarity（早期 batch 无门禁）")

    row.tier = tier
    row.tier_reasons = reasons or ["通过现行罗什风指标"]


def _tier_rank(t: str) -> int:
    return {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "RECON": 4}.get(t, 5)


def audit_record(rec: dict) -> AuditRow:
    src = rec.get("chinese_text") or ""
    lit = rec.get("kumarajiva_style_text") or ""
    mod = rec.get("modern_psychology_text") or ""
    src_body = _src_body(src)

    sim_lit = round(similarity_to_source(src, lit), 3)
    sim_mod = round(similarity_to_source(src, mod), 3) if mod else 0.0
    stored = rec.get("similarity_to_source")
    drift = round(abs(stored - sim_lit), 3) if stored is not None else None

    calque_hits = _count_calques(lit)
    calque_score = sum(calque_hits.values())

    src_len = len(_to_simplified_approx(src_body))
    lit_len = len(_to_simplified_approx(lit))
    compression = round(lit_len / src_len, 3) if src_len else 0.0

    source_errors = [m for m in SOURCE_ERROR_MARKERS if m in lit]

    v = validate_restyle(src, lit, mod)
    n = int(rec["id"].split("_")[1])
    lit_eq, overlap = _lit_mod_identity(lit, mod)

    row = AuditRow(
        id=rec["id"],
        review_status=rec.get("review_status", ""),
        confidence=rec.get("confidence", "?"),
        sim_lit=sim_lit,
        sim_mod=sim_mod,
        lit_mod_gap=round(sim_lit - sim_mod, 3),
        lit_len=lit_len,
        src_len=src_len,
        compression=compression,
        calque_hits=calque_hits,
        calque_score=calque_score,
        source_errors_in_lit=source_errors,
        stored_sim=stored,
        sim_drift=drift,
        validation_status=v["status"],
        validation_issues=v.get("issues") or [],
        validation_warnings=v.get("warnings") or [],
        lit_eq_mod=lit_eq,
        lit_mod_overlap=overlap,
        template_flags=_wrong_devata_wording(lit, src),
        batch=_batch_label(n),
    )
    _assign_tier(row)
    return row


def _md_table(rows: list[AuditRow], max_rows: int = 80) -> str:
    lines = [
        "| ID | tier | sim | gap | len | calque | 原因 |",
        "|----|------|-----|-----|-----|--------|------|",
    ]
    for r in rows[:max_rows]:
        reason = "; ".join(r.tier_reasons[:2])[:60]
        lines.append(
            f"| {r.id} | {r.tier} | {r.sim_lit:.3f} | {r.lit_mod_gap:.3f} | "
            f"{r.lit_len} | {r.calque_score} | {reason} |"
        )
    if len(rows) > max_rows:
        lines.append(f"| … | | | | | | 另有 {len(rows) - max_rows} 条 |")
    return "\n".join(lines)


def write_report(rows: list[AuditRow]) -> None:
    by_tier: dict[str, list[AuditRow]] = defaultdict(list)
    for r in rows:
        by_tier[r.tier].append(r)

    for tier in by_tier:
        by_tier[tier].sort(key=lambda x: (-x.sim_lit, -x.lit_len))

    by_batch: dict[str, list[AuditRow]] = defaultdict(list)
    for r in rows:
        by_batch[r.batch].append(r)

    tier_counts = Counter(r.tier for r in rows)
    sims = [r.sim_lit for r in rows if r.review_status == "gold"]
    missing_sim = sum(1 for r in rows if r.stored_sim is None)

    md: list[str] = [
        "# Gold Corpus Audit — Kumarajiva Style",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## 验收标准（本项目「雅」= 鸠摩罗什风，非繁转简）",
        "",
        "1. **信**：法义依巴利／SN 平行，底本讹句须校正，不得原样保留。",
        "2. **达**：literary / modern 段数平行，因果可读。",
        "3. **雅**：删梵式冗复、四字节奏、意译圆通；literary 栏不得「换字体」。",
        "",
        "机器指标：",
        "- `sim_lit`：literary 与底本三元组 Jaccard（≥0.55 = 繁转简，应拒收）",
        "- `lit_mod_gap`：literary 比 modern 更贴底本 → 双栏不同步",
        "- `compression`：lit_len/src_len（罗什风应显著删冗；≥0.85 可疑）",
        "- `calque_score`：求那体套语计数（所以者何、比丘！、是名…）",
        "",
        "## 总览",
        "",
        f"| 指标 | 值 |",
        f"|------|-----|",
        f"| gold + gold_reconstructed | {len(rows)} |",
        f"| gold only | {sum(1 for r in rows if r.review_status=='gold')} |",
        f"| gold_reconstructed | {sum(1 for r in rows if r.review_status=='gold_reconstructed')} |",
        f"| 未存 similarity | {missing_sim} |",
        f"| sim mean (gold) | {sum(sims)/len(sims):.3f} |" if sims else "",
        f"| sim max | {max(r.sim_lit for r in rows):.3f} ({max(rows, key=lambda x: x.sim_lit).id}) |",
        f"| sim≥0.55 | {sum(1 for r in rows if r.sim_lit>=0.55)} |",
        f"| sim≥0.50 | {sum(1 for r in rows if r.sim_lit>=0.50)} |",
        f"| sim≥0.45 | {sum(1 for r in rows if r.sim_lit>=0.45)} |",
        f"| lit_mod_gap≥0.12 | {sum(1 for r in rows if r.lit_mod_gap>=0.12)} |",
        f"| 白话=罗什风（完全相同） | {sum(1 for r in rows if r.lit_eq_mod)} |",
        f"| validate fail | {sum(1 for r in rows if r.validation_status=='fail')} |",
        f"| validate warn | {sum(1 for r in rows if r.validation_status=='warn')} |",
        f"| 底本讹句残留 | {sum(1 for r in rows if r.source_errors_in_lit)} |",
        "",
        "## 分级",
        "",
        "| Tier | 含义 | 数量 |",
        "|------|------|------|",
        "| **P0** | 必须立即重写（长经繁转简／sim≥0.55／讹句残留） | "
        f"{tier_counts.get('P0', 0)} |",
        "| **P1** | 应重写（中高 sim、双栏不同步、calque 重） | "
        f"{tier_counts.get('P1', 0)} |",
        "| **P2** | 轻修（borderline sim 或短经公式） | "
        f"{tier_counts.get('P2', 0)} |",
        f"| **P3** | 通过 | {tier_counts.get('P3', 0)} |",
        "| **RECON** | gold_reconstructed 交叉指示型，单独验收 | "
        f"{tier_counts.get('RECON', 0)} |",
        "",
        "## P0 — 立即动刀",
        "",
        _md_table(by_tier.get("P0", [])),
        "",
        "## P1 — 下一批动刀",
        "",
        _md_table(by_tier.get("P1", [])),
        "",
        "## P2 — 轻修（按 sim 降序前 30）",
        "",
        _md_table(
            sorted(by_tier.get("P2", []), key=lambda x: -x.sim_lit)[:30]
        ),
        "",
        "## 各 batch 风险（P0+P1 数 / gold 数，mean sim）",
        "",
        "| Batch | gold | P0 | P1 | P2 | mean sim | max sim |",
        "|-------|------|----|----|-----|----------|---------|",
    ]

    batch_order = sorted(
        by_batch.keys(),
        key=lambda b: int(re.search(r"\d+", b).group()) if re.search(r"\d+", b) else 0,
    )
    for batch in batch_order:
        br = by_batch[batch]
        p0 = sum(1 for r in br if r.tier == "P0")
        p1 = sum(1 for r in br if r.tier == "P1")
        p2 = sum(1 for r in br if r.tier == "P2")
        ms = sum(r.sim_lit for r in br) / len(br)
        mx = max(r.sim_lit for r in br)
        md.append(f"| {batch} | {len(br)} | {p0} | {p1} | {p2} | {ms:.3f} | {mx:.3f} |")

    md.extend(
        [
            "",
            "## 建议处理顺序",
            "",
            "1. **P0**：立即修复（validate fail、白话=罗什风、讹句残留、模板错字、sim≥0.55）",
            "2. **P1**：下一批重写（双栏不同步 + 高 sim、白话高度重合）",
            "3. **P2**：轻修（borderline sim / compression）",
            "4. **RECON**：216 部 gold_reconstructed 单独验收，不要求低 sim",
            "",
            "## RECON（交叉指示／省文）",
            "",
            "以下 gold_reconstructed 条目单独验收，不要求低 sim，但须确认：",
            "- 非繁转简；",
            "- 纲要补出依 SN／同型经；",
            "- notes 标明 reconstruction_basis。",
            "",
            _md_table(by_tier.get("RECON", []), max_rows=25),
            "",
        ]
    )

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    payload = {
        "generated": date.today().isoformat(),
        "total": len(rows),
        "tier_counts": dict(tier_counts),
        "rows": [asdict(r) for r in sorted(rows, key=lambda x: int(x.id.split("_")[1]))],
    }
    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    data = json.loads(CORPUS.read_text(encoding="utf-8"))
    gold = [r for r in data if r.get("review_status") in GOLD_STATUSES]
    gold.sort(key=lambda x: int(x["id"].split("_")[1]))
    rows = [audit_record(r) for r in gold]
    write_report(rows)

    non_gold = [
        r["id"]
        for r in data
        if r.get("review_status") not in GOLD_STATUSES
    ]

    tc = Counter(r.tier for r in rows)
    print(f"audited {len(rows)} gold entries")
    print(f"tier counts: {dict(tc)}")
    if non_gold:
        print(f"non-gold entries: {len(non_gold)} {non_gold}")
    print(f"written {OUT_MD}")
    print(f"written {OUT_JSON}")


if __name__ == "__main__":
    main()
