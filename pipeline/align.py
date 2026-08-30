"""Fetch SA Chinese, Patton EN, SC parallels, and SN Pali/EN."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from rich.console import Console

from pipeline import (
    BILARA_RAW,
    SC_API,
    HttpClient,
    bilara_join,
    html_to_text,
    sa_bucket,
)
from pipeline.titles import normalize_title

console = Console()
ROOT = Path(__file__).resolve().parents[1]


def fetch_bilara_sa(client: HttpClient, n: int) -> dict[str, Any]:
    bucket = sa_bucket(n)
    root_url = (
        f"{BILARA_RAW}/root/lzh/sct/sutta/sa/{bucket}/sa{n}_root-lzh-sct.json"
    )
    en_url = (
        f"{BILARA_RAW}/translation/en/patton/sutta/sa/{bucket}/"
        f"sa{n}_translation-en-patton.json"
    )
    out: dict[str, Any] = {
        "uid": f"sa{n}",
        "bucket": bucket,
        "chinese_segments": None,
        "english_sa_segments": None,
        "chinese_text": "",
        "english_sa_text": "",
        "title": "",
        "errors": [],
    }
    raw_title = ""
    try:
        segs = client.get_json(root_url)
        out["chinese_segments"] = segs
        out["chinese_text"] = bilara_join(segs, skip_meta=True)
        title_bits = [v for k, v in segs.items() if re.search(r":0\.", k)]
        raw_title = re.sub(r"<[^>]+>", "", " ".join(title_bits[:4])).strip()
    except Exception as e:  # noqa: BLE001 — collect soft failures per sutra
        out["errors"].append(f"bilara_zh:{e}")
        try:
            data = client.get_json(f"{SC_API}/suttas/sa{n}")
            html = (data.get("root_text") or {}).get("text") or ""
            out["chinese_text"] = html_to_text(html)
            raw_title = (data.get("root_text") or {}).get("title") or ""
            ot = (data.get("suttaplex") or {}).get("original_title") or ""
            if ot and ot not in raw_title:
                raw_title = f"{raw_title} {ot}".strip()
        except Exception as e2:  # noqa: BLE001
            out["errors"].append(f"html_zh:{e2}")

    out["title"] = normalize_title(n, raw_title)

    try:
        en = client.get_json(en_url)
        out["english_sa_segments"] = en
        out["english_sa_text"] = bilara_join(en, skip_meta=True)
    except Exception as e:  # noqa: BLE001
        out["errors"].append(f"bilara_en_patton:{e}")
        try:
            data = client.get_json(f"{SC_API}/suttas/sa{n}/analayo?lang=en")
            html = (data.get("translation") or {}).get("text") or ""
            out["english_sa_text"] = html_to_text(html)
            out["errors"].append("used_analayo_fallback")
        except Exception as e2:  # noqa: BLE001
            out["errors"].append(f"html_en:{e2}")
    return out


def fetch_parallels(client: HttpClient, uid: str) -> list[dict[str, Any]]:
    data = client.get_json(f"{SC_API}/parallels/{uid}")
    # API returns {uid: [parallels...]}
    items = data.get(uid) or next(iter(data.values()), [])
    cleaned: list[dict[str, Any]] = []
    for item in items:
        to = item.get("to") or {}
        cleaned.append(
            {
                "uid": to.get("uid"),
                "acronym": to.get("acronym"),
                "root_lang": to.get("root_lang"),
                "original_title": to.get("original_title"),
                "translated_title": to.get("translated_title"),
                "type": item.get("type"),
                "resembling": item.get("resembling"),
                "remark": item.get("remark"),
            }
        )
    return cleaned


def sn_bilara_paths(sn_uid: str) -> tuple[str, str]:
    """e.g. sn22.12 -> sn/sn22/sn22.12_..."""
    m = re.match(r"^(sn)(\d+)\.(\d+)$", sn_uid)
    if not m:
        raise ValueError(f"Unsupported SN uid: {sn_uid}")
    coll, vagga, num = m.group(1), m.group(2), m.group(3)
    base = f"sutta/{coll}/{coll}{vagga}/{coll}{vagga}.{num}"
    pali = f"{BILARA_RAW}/root/pli/ms/{base}_root-pli-ms.json"
    en = f"{BILARA_RAW}/translation/en/sujato/{base}_translation-en-sujato.json"
    return pali, en


def fetch_sn(client: HttpClient, sn_uid: str) -> dict[str, Any]:
    out: dict[str, Any] = {
        "uid": sn_uid,
        "pali_text": "",
        "english_sn_text": "",
        "errors": [],
    }
    try:
        pali_url, en_url = sn_bilara_paths(sn_uid)
        pali = client.get_json(pali_url)
        en = client.get_json(en_url)
        out["pali_text"] = bilara_join(pali, skip_meta=True)
        out["english_sn_text"] = bilara_join(en, skip_meta=True)
    except Exception as e:  # noqa: BLE001
        out["errors"].append(str(e))
    return out


def pick_primary_sn(parallels: list[dict[str, Any]]) -> str | None:
    sn = [p for p in parallels if (p.get("uid") or "").startswith("sn")]
    if not sn:
        return None
    # Prefer exact (resembling False) then first
    sn_sorted = sorted(sn, key=lambda p: (bool(p.get("resembling")), p.get("uid") or ""))
    return sn_sorted[0].get("uid")


def build_record(client: HttpClient, n: int) -> dict[str, Any]:
    sa = fetch_bilara_sa(client, n)
    parallels = []
    try:
        parallels = fetch_parallels(client, f"sa{n}")
    except Exception as e:  # noqa: BLE001
        sa["errors"].append(f"parallels:{e}")
    primary_sn = pick_primary_sn(parallels)
    sn_block = None
    if primary_sn:
        sn_block = fetch_sn(client, primary_sn)
    return {
        "id": f"SA_{n}",
        "uid": f"sa{n}",
        "title": sa.get("title") or f"SA {n}",
        "chinese_text": sa.get("chinese_text") or "",
        "english_sa_text": sa.get("english_sa_text") or "",
        "parallels": parallels,
        "primary_sn_uid": primary_sn,
        "pali_text": (sn_block or {}).get("pali_text") or "",
        "english_sn_text": (sn_block or {}).get("english_sn_text") or "",
        "errors": (sa.get("errors") or []) + ((sn_block or {}).get("errors") or []),
        "kumarajiva_style_text": "",
        "modern_psychology_text": "",
        "notes": "",
        "review_status": "raw",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and align SA pilot corpus")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data" / "aligned" / "raw_aligned_data.json",
    )
    args = parser.parse_args()

    cache = ROOT / "data" / "cache"
    records: list[dict[str, Any]] = []
    with HttpClient(cache_dir=cache) as client:
        for n in range(args.start, args.start + args.count):
            console.print(f"[cyan]Fetching SA {n}…[/cyan]")
            rec = build_record(client, n)
            if rec["errors"]:
                console.print(f"  [yellow]warnings:[/yellow] {rec['errors']}")
            records.append(rec)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    console.print(f"[green]Wrote {len(records)} records → {args.out}[/green]")


if __name__ == "__main__":
    main()
