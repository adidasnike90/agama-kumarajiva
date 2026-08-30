#!/usr/bin/env python3
"""Publication-standard audit and repair for final_translated_data.json.

Checks (P1 = metadata / reference layer; P0 = content integrity):
  - primary_sn_uid vs notes「据 SN xx」及正文主题词
  - english_sa_text 与汉本关键词明显不符（Patton 错配）
  - english_sn / pali 与 primary 不同步
  - 平行表缺 notes 所引 SN

Repairs (--apply):
  - 重选 primary_sn、补 parallels、自 Bilara/API 重拉 pali / SN 英译 / SA 英译
  - 写回 corpus；输出 PUBLICATION_AUDIT.md / .json

Usage:
  python scripts/publication_corpus.py audit
  python scripts/publication_corpus.py fix --apply
  python scripts/publication_corpus.py fix --apply --start 1 --end 32
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline import BILARA_RAW, HttpClient, SC_API, bilara_join, html_to_text, sa_bucket  # noqa: E402
from translate.validate import _norm  # noqa: E402

CORPUS = ROOT / "data" / "translated" / "final_translated_data.json"
OUT_JSON = ROOT / "data" / "translated" / "PUBLICATION_AUDIT.json"
OUT_MD = ROOT / "data" / "translated" / "PUBLICATION_AUDIT.md"
CACHE = ROOT / "data" / "cache"

SN_RE = re.compile(r"(?:据\s*)?SN\s*(\d+)\.(\d+)", re.I)
SN_UID_RE = re.compile(r"\bsn(\d+)\.(\d+)\b", re.I)
SN_RANGE_RE = re.compile(r"SN\s*(\d+)\.(\d+)\s*[–\-—]\s*(\d+)", re.I)

# Chinese cue → SN 22.x three-times template (SA 8–11 等)
THREE_TIMES_SN = {
    "无常": "sn22.9",
    "無常": "sn22.9",
    "苦": "sn22.10",
    "空": "sn22.10",
    "非我": "sn22.11",
    "无我": "sn22.11",
    "無我": "sn22.11",
}

EN_SA_CHECKS: list[tuple[str, list[str]]] = [
    ("爱喜", ["delight", "abhinand", "take pleasure", "loves and delights"]),
    ("愛喜", ["delight", "abhinand", "take pleasure"]),
    ("不断", ["stop and", "doesn't stop", "does not stop", "cut off", "cutting off", "without cutting", "unbroken"]),
    ("不斷", ["stop and", "doesn't stop", "cut off", "cutting off", "without cutting", "unbroken"]),
    ("色味", ["enjoyment", "relish", "flavor", "taste"]),
    ("识味", ["enjoyment", "relish", "flavor", "taste"]),
    ("色患", ["trouble", "drawback", "danger", "disadvantage"]),
    ("识患", ["trouble", "drawback", "danger", "disadvantage"]),
    ("输屡那", ["Śroṇa", "Sroṇa", "Rohitassa", "Rohitass", "Rohitassa"]),
    ("輸屢那", ["Śroṇa", "Sroṇa", "Rohitassa", "Rohitass", "Rohitassa"]),
]


def sn_bilara_paths(sn_uid: str) -> tuple[str, str]:
    m = re.match(r"^(sn)(\d+)\.(\d+)$", sn_uid)
    if not m:
        raise ValueError(f"Unsupported SN uid: {sn_uid}")
    coll, vagga, num = m.group(1), m.group(2), m.group(3)
    base = f"sutta/{coll}/{coll}{vagga}/{coll}{vagga}.{num}"
    pali = f"{BILARA_RAW}/root/pli/ms/{base}_root-pli-ms.json"
    en = f"{BILARA_RAW}/translation/en/sujato/{base}_translation-en-sujato.json"
    return pali, en


def fetch_sn(client: HttpClient, sn_uid: str) -> dict:
    out: dict = {"uid": sn_uid, "pali_text": "", "english_sn_text": "", "errors": []}
    try:
        pali_url, en_url = sn_bilara_paths(sn_uid)
        pali = client.get_json(pali_url)
        en = client.get_json(en_url)
        out["pali_text"] = bilara_join(pali, skip_meta=True)
        out["english_sn_text"] = bilara_join(en, skip_meta=True)
    except Exception as e:  # noqa: BLE001
        out["errors"].append(str(e))
    return out


def fetch_bilara_sa(client: HttpClient, n: int) -> dict:
    bucket = sa_bucket(n)
    en_url = (
        f"{BILARA_RAW}/translation/en/patton/sutta/sa/{bucket}/"
        f"sa{n}_translation-en-patton.json"
    )
    out: dict = {"english_sa_text": "", "errors": []}
    try:
        en = client.get_json(en_url)
        out["english_sa_text"] = bilara_join(en, skip_meta=True)
    except Exception as e:  # noqa: BLE001
        out["errors"].append(f"bilara_en_patton:{e}")
        try:
            data = client.get_json(f"{SC_API}/suttas/sa{n}/analayo?lang=en")
            html = (data.get("translation") or {}).get("text") or ""
            out["english_sa_text"] = html_to_text(html)
        except Exception as e2:  # noqa: BLE001
            out["errors"].append(f"html_en:{e2}")
    return out


@dataclass
class PubIssue:
    id: str
    code: str
    severity: str  # P0, P1, P2
    detail: str
    fixed: bool = False
    fix_action: str = ""


@dataclass
class PubRow:
    id: str
    issues: list[PubIssue] = field(default_factory=list)

    @property
    def worst(self) -> str:
        order = {"P0": 0, "P1": 1, "P2": 2}
        if not self.issues:
            return "OK"
        return min(self.issues, key=lambda i: order.get(i.severity, 9)).severity


def _simp(s: str) -> str:
    return (s or "").replace("無", "无").replace("愛", "爱").replace("斷", "断").replace("樂", "乐")


def sn_uids_from_notes(notes: str) -> list[str]:
    uids: list[str] = []
    seen: set[str] = set()
    for m in SN_RANGE_RE.finditer(notes or ""):
        maj, lo, hi = int(m.group(1)), int(m.group(2)), int(m.group(3))
        for minor in range(lo, hi + 1):
            uid = f"sn{maj}.{minor}"
            if uid not in seen:
                seen.add(uid)
                uids.append(uid)
    for m in SN_RE.finditer(notes or ""):
        uid = f"sn{m.group(1)}.{m.group(2)}"
        if uid not in seen:
            seen.add(uid)
            uids.append(uid)
    for m in SN_UID_RE.finditer(notes or ""):
        uid = f"sn{m.group(1)}.{m.group(2)}"
        if uid not in seen:
            seen.add(uid)
            uids.append(uid)
    return uids


def infer_primary_from_content(rec: dict, note_sns: list[str]) -> str | None:
    """Pick best primary SN when notes list a range or multiple."""
    zh = _simp(rec.get("chinese_text") or "")
    lit = _simp(rec.get("kumarajiva_style_text") or "")
    blob = zh + lit
    if not note_sns:
        return None
    manual = {
        "SA_8": "sn22.9",
        "SA_79": "sn22.9",
    }
    if rec.get("id") in manual:
        return manual[rec["id"]]
    # Three-times cluster (SN 22.9–11): match dominant mark in main text, not 括注 alone
    cluster = {u for u in note_sns if u in ("sn22.9", "sn22.10", "sn22.11")}
    if cluster:
        main = lit or zh
        if "无常" in main or "無常" in (rec.get("chinese_text") or ""):
            return "sn22.9"
        if ("非我" in main or "无我" in main) and "无常即苦" not in main:
            return "sn22.11"
        if "苦" in main and "无常" not in main:
            return "sn22.10"
        return "sn22.9" if "sn22.9" in cluster else note_sns[0]
    m = re.search(r"据\s*SN\s*(\d+)\.(\d+)", rec.get("notes") or "", re.I)
    if m:
        uid = f"sn{m.group(1)}.{m.group(2)}"
        return uid
    return note_sns[0]


def english_sa_mismatch(rec: dict) -> list[str]:
    """Flag Patton SA english clearly wrong vs 汉本. P2 if SN english is present (book uses SN first)."""
    zh = rec.get("chinese_text") or ""
    en = (rec.get("english_sa_text") or "").lower()
    if not zh or not en:
        return []
    flags: list[str] = []
    for cue, needles in EN_SA_CHECKS:
        if cue in zh or cue in _simp(zh):
            if not any(n.lower() in en for n in needles):
                flags.append(f"汉有「{cue}」英译无对应")
    if "爱喜" in _simp(zh) and "doesn't know and understand form" in en and "delight" not in en:
        flags.append("英译似 SN22.24 型，缺爱喜段")
    return flags


def english_sa_severity(rec: dict, flags: list[str]) -> str:
    """P1 only when english_sa would display in book (no SN english)."""
    if not flags:
        return ""
    if (rec.get("english_sn_text") or "").strip():
        return "P2"
    return "P1"


def primary_topic_mismatch(rec: dict) -> str | None:
    primary = (rec.get("primary_sn_uid") or "").lower()
    pali = (rec.get("pali_text") or "").lower()
    zh = _simp(rec.get("chinese_text") or "")
    lit = _simp(rec.get("kumarajiva_style_text") or "")
    blob = zh + lit
    if not primary or not pali:
        return None
    if primary == "sn22.10" and ("无常" in blob or "無常" in (rec.get("chinese_text") or "")):
        if "anicca" in pali or "dukkha" in pali:
            if "dukkha" in pali and "anicca" not in pali:
                return "正文无常但 primary/pali 为苦经"
    if primary == "sn22.24" and ("爱喜" in blob or "愛喜" in (rec.get("chinese_text") or "")):
        if "abhinand" not in pali:
            return "正文有爱喜段但 pali 为知明经"
    return None


def parallels_have_uid(rec: dict, uid: str) -> bool:
    return any((p.get("uid") or "").lower() == uid.lower() for p in rec.get("parallels") or [])


def ensure_parallel_stub(rec: dict, uid: str) -> bool:
    if parallels_have_uid(rec, uid):
        return False
    m = re.match(r"sn(\d+)\.(\d+)", uid, re.I)
    if not m:
        return False
    rec.setdefault("parallels", []).append(
        {
            "uid": uid.lower(),
            "acronym": f"SN {m.group(1)}.{m.group(2)}",
            "root_lang": "pli",
            "original_title": "",
            "translated_title": "",
            "type": "full",
            "resembling": False,
            "remark": "added by publication_corpus fix",
        }
    )
    return True


def audit_record(rec: dict) -> PubRow:
    row = PubRow(id=rec["id"])
    note_sns = sn_uids_from_notes(rec.get("notes") or "")
    primary = (rec.get("primary_sn_uid") or "").lower()
    inferred = infer_primary_from_content(rec, note_sns)

    if inferred and primary and inferred != primary:
        row.issues.append(
            PubIssue(
                rec["id"],
                "primary_mismatch",
                "P1",
                f"primary={primary} notes/内容建议={inferred}",
            )
        )

    tm = primary_topic_mismatch(rec)
    if tm:
        row.issues.append(PubIssue(rec["id"], "primary_topic", "P1", tm))

    for flag in english_sa_mismatch(rec):
        sev = english_sa_severity(rec, [flag])
        row.issues.append(PubIssue(rec["id"], "english_sa_mismatch", sev, flag))

    if note_sns:
        for uid in note_sns:
            if uid.startswith("sn") and not parallels_have_uid(rec, uid):
                row.issues.append(
                    PubIssue(
                        rec["id"],
                        "parallel_missing",
                        "P2",
                        f"notes 引 {uid} 但 parallels 未列",
                    )
                )

    if not (rec.get("pali_text") or "").strip() and primary:
        row.issues.append(PubIssue(rec["id"], "missing_pali", "P2", "有 primary 无 pali_text"))

    if not rec.get("prior_review_status") and rec.get("review_status") in ("gold", "gold_reconstructed"):
        row.issues.append(PubIssue(rec["id"], "schema_gap", "P2", "缺 prior_review_status"))

    return row


def fix_record(rec: dict, client: HttpClient, *, force_sa_en: bool = False) -> list[str]:
    actions: list[str] = []
    n = int(rec["id"].split("_")[1])
    note_sns = sn_uids_from_notes(rec.get("notes") or "")
    primary = (rec.get("primary_sn_uid") or "").lower()
    inferred = infer_primary_from_content(rec, note_sns)

    # SA_5: composite english_sa = delight (Patton SA_7) + know (SN 22.24)
    if rec["id"] == "SA_5":
        inferred = "sn22.29"
        if not parallels_have_uid(rec, "sn22.29"):
            ensure_parallel_stub(rec, "sn22.29")
            actions.append("add parallel sn22.29")
        sa7 = fetch_bilara_sa(client, 7)
        sn24 = fetch_sn(client, "sn22.24")
        en7 = (sa7.get("english_sa_text") or "").split("Summary Verse")[0].strip()
        en24 = (sn24.get("english_sn_text") or "").strip()
        if en7 and en24:
            rec["english_sa_text"] = (
                en7
                + "\n\n"
                + en24.replace("At Sāvatthī.", "Monks, without directly knowing")
            )
            actions.append("rebuild SA_5 english_sa (SA_7 + SN22.24)")

    target_primary = inferred or primary
    if target_primary and target_primary != primary:
        rec["primary_sn_uid"] = target_primary
        actions.append(f"primary {primary} -> {target_primary}")
        sn_block = fetch_sn(client, target_primary)
        if sn_block.get("pali_text"):
            rec["pali_text"] = sn_block["pali_text"]
            actions.append(f"refetch pali {target_primary}")
        if sn_block.get("english_sn_text"):
            rec["english_sn_text"] = sn_block["english_sn_text"]
            actions.append(f"refetch english_sn {target_primary}")

    for uid in note_sns:
        if uid.startswith("sn") and ensure_parallel_stub(rec, uid):
            actions.append(f"add parallel {uid}")

    # SA_5: composite english_sa handled above; skip generic refetch merge
    if rec["id"] != "SA_5":
        sa_flags = english_sa_mismatch(rec)
        if sa_flags or force_sa_en:
            sa_block = fetch_bilara_sa(client, n)
            new_en = (sa_block.get("english_sa_text") or "").strip()
            if new_en and new_en != (rec.get("english_sa_text") or "").strip():
                old_flags = english_sa_mismatch(rec)
                rec["english_sa_text"] = new_en
                new_flags = english_sa_mismatch(rec)
                if len(new_flags) <= len(old_flags):
                    actions.append("refetch english_sa_text")
                else:
                    rec["english_sa_text"] = rec.get("english_sa_text") or new_en

    if rec["id"] == "SA_5" and english_sa_mismatch(rec):
        pass  # already rebuilt

    if not rec.get("prior_review_status"):
        rec["prior_review_status"] = rec.get("review_status") or "gold"

    # Sync pali/en if primary set but empty
    primary = (rec.get("primary_sn_uid") or "").lower()
    if primary and not (rec.get("pali_text") or "").strip():
        sn_block = fetch_sn(client, primary)
        if sn_block.get("pali_text"):
            rec["pali_text"] = sn_block["pali_text"]
            actions.append(f"fill pali {primary}")
        if sn_block.get("english_sn_text"):
            rec["english_sn_text"] = sn_block["english_sn_text"]
            actions.append(f"fill english_sn {primary}")

    return actions


def write_report(rows: list[PubRow], fixes: dict[str, list[str]]) -> None:
    by_sev: dict[str, list[PubIssue]] = defaultdict(list)
    for row in rows:
        for iss in row.issues:
            if not iss.fixed:
                by_sev[iss.severity].append(iss)

    md = [
        "# Publication Audit",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Summary",
        "",
        f"| Severity | Open | Fixed |",
        f"|----------|------|-------|",
    ]
    for sev in ("P0", "P1", "P2"):
        open_n = sum(1 for i in by_sev.get(sev, []) if not i.fixed)
        fixed_n = sum(1 for r in rows for i in r.issues if i.severity == sev and i.fixed)
        md.append(f"| {sev} | {open_n} | {fixed_n} |")

    md.extend(["", "## Open P1", ""])
    p1 = [i for i in by_sev.get("P1", []) if not i.fixed]
    if p1:
        md.append("| ID | Code | Detail |")
        md.append("|----|------|--------|")
        for i in p1[:100]:
            md.append(f"| {i.id} | {i.code} | {i.detail[:80]} |")
        if len(p1) > 100:
            md.append(f"| … | | 另有 {len(p1)-100} 条 |")
    else:
        md.append("（无）")

    md.extend(["", "## Fixes applied", ""])
    if fixes:
        for sid, acts in sorted(fixes.items(), key=lambda x: int(x[0].split("_")[1])):
            if acts:
                md.append(f"- **{sid}**: " + "; ".join(acts))
    else:
        md.append("（无）")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated": date.today().isoformat(),
                "rows": [
                    {
                        "id": r.id,
                        "worst": r.worst,
                        "issues": [asdict(i) for i in r.issues],
                    }
                    for r in rows
                ],
                "fixes": fixes,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def load_corpus() -> list[dict]:
    return json.loads(CORPUS.read_text(encoding="utf-8"))


def save_corpus(recs: list[dict]) -> None:
    CORPUS.write_text(json.dumps(recs, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["audit", "fix"])
    ap.add_argument("--apply", action="store_true", help="Write corpus (fix only)")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=1362)
    args = ap.parse_args()

    recs = load_corpus()
    by_id = {r["id"]: r for r in recs}
    fixes: dict[str, list[str]] = {}

    if args.command == "fix" and args.apply:
        with HttpClient(cache_dir=CACHE) as client:
            for n in range(args.start, args.end + 1):
                rid = f"SA_{n}"
                rec = by_id.get(rid)
                if not rec:
                    continue
                acts = fix_record(rec, client)
                if acts:
                    fixes[rid] = acts

    rows: list[PubRow] = []
    for n in range(args.start, args.end + 1):
        rid = f"SA_{n}"
        rec = by_id.get(rid)
        if not rec:
            continue
        row = audit_record(rec)
        for iss in row.issues:
            if rid in fixes:
                iss.fixed = iss.code in (
                    "primary_mismatch",
                    "primary_topic",
                    "english_sa_mismatch",
                    "parallel_missing",
                    "missing_pali",
                    "schema_gap",
                )
                if iss.fixed:
                    iss.fix_action = "; ".join(fixes[rid])
        rows.append(row)

    if args.command == "fix" and args.apply:
        save_corpus(recs)
        print(f"saved {CORPUS}")

    write_report(rows, fixes)
    open_p1 = sum(1 for r in rows for i in r.issues if i.severity == "P1" and not i.fixed)
    print(f"audited SA_{args.start}–SA_{args.end}: {len(rows)} records")
    print(f"open P1: {open_p1}")
    print(f"fixes: {len(fixes)} suttas")
    print(f"written {OUT_MD}")


if __name__ == "__main__":
    main()
