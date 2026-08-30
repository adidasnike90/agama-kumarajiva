"""Batch restyle engine (OpenAI-compatible API)."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from rich.console import Console

from translate import find_forbidden_hits, load_system_prompt, user_message

console = Console()
ROOT = Path(__file__).resolve().parents[1]


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def translate_one(client, model: str, record: dict[str, Any]) -> dict[str, Any]:
    system = load_system_prompt()
    resp = client.chat.completions.create(
        model=model,
        temperature=0.3,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message(record)},
        ],
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content or "{}"
    data = _extract_json(content)
    kuma = (data.get("kumarajiva_style_text") or "").strip()
    modern = (data.get("modern_psychology_text") or "").strip()
    notes = (data.get("notes") or "").strip()
    hits = find_forbidden_hits(kuma + "\n" + modern)
    record = dict(record)
    record["kumarajiva_style_text"] = kuma
    record["modern_psychology_text"] = modern
    record["notes"] = notes
    record["forbidden_hits"] = hits
    record["review_status"] = "machine" if not hits else "needs_doctrine_check"
    return record


def apply_demo_seeds(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Offline demo restyles for SA 1–2 so the reader works without an API key."""
    seeds = {
        "SA_1": {
            "kumarajiva_style_text": (
                "如是我闻：一时佛在舍卫国祇树给孤独园。\n"
                "尔时佛告诸比丘：汝等应当谛观诸色，明见无常。如是观者，名为正观。"
                "既具正观，则生厌离；贪爱永灭，说心解脱。"
                "受想行识，亦复如是。明见无常者，厌离贪尽，同获心解脱。"
                "心解脱者，若欲自证，则能自证：我生已尽，梵行已立，所作已作，自知不受后有。"
                "如观无常，苦、空、非我，亦复如是。\n"
                "时诸比丘闻佛所说，欢喜奉行。"
            ),
            "modern_psychology_text": (
                "观察身体与感受、认知、造作、识知这些经验都会变化。看清无常，就是正确的看。"
                "看清之后，对它们的黏着会松开；黏着松开，贪与喜乐的抓取会减弱；抓取减弱，心就松绑。"
                "受、想、行、识也用同样的方式看。苦、空、非我，也一样。"
                "这不是自我安慰的鸡汤，而是冷静的身心观察说明书。"
            ),
            "notes": "演示用人工样例，非正式定稿；平行经关系以 SuttaCentral 为准。",
        },
        "SA_2": {
            "kumarajiva_style_text": (
                "如是我闻：一时佛在舍卫国祇树给孤独园。\n"
                "尔时佛告诸比丘：当正思惟色，观色无常如实知。"
                "若能如是思惟观者，于色欲贪断；欲贪断者，说心解脱。"
                "受想行识，亦应如是思惟，观无常如实知，欲贪断，心解脱。\n"
                "时诸比丘闻佛所说，欢喜奉行。"
            ),
            "modern_psychology_text": (
                "把注意力稳稳放在色上，看见它不断变化，并如实知道这一点。"
                "这样看时，对色的贪欲会减弱；贪欲减弱，心的束缚就放松。"
                "对受、想、行、识也做同样的观察。"
            ),
            "notes": "演示样例；若已跑 API 翻译会被覆盖。",
        },
    }
    out = []
    for rec in records:
        rec = dict(rec)
        seed = seeds.get(rec.get("id") or "")
        if seed and not rec.get("kumarajiva_style_text"):
            rec.update(seed)
            rec["review_status"] = "demo_seed"
            rec["forbidden_hits"] = find_forbidden_hits(
                seed["kumarajiva_style_text"] + seed["modern_psychology_text"]
            )
        out.append(rec)
    return out


def main() -> None:
    load_dotenv(ROOT / ".env")
    parser = argparse.ArgumentParser(description="Restyle aligned SA records")
    parser.add_argument(
        "--in",
        dest="inp",
        type=Path,
        default=ROOT / "data" / "aligned" / "raw_aligned_data.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data" / "translated" / "final_translated_data.json",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Fill demo seeds only (no API calls)",
    )
    parser.add_argument("--limit", type=int, default=0, help="Translate only first N")
    args = parser.parse_args()

    records: list[dict[str, Any]] = json.loads(args.inp.read_text(encoding="utf-8"))
    if args.limit:
        records = records[: args.limit]

    if args.demo or not os.getenv("OPENAI_API_KEY"):
        if not args.demo and not os.getenv("OPENAI_API_KEY"):
            console.print(
                "[yellow]No OPENAI_API_KEY — writing demo seeds for SA_1/SA_2.[/yellow]"
            )
        records = apply_demo_seeds(records)
    else:
        from openai import OpenAI

        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.getenv("OPENAI_BASE_URL") or None,
        )
        model = os.getenv("OPENAI_MODEL", "deepseek-chat")
        done: list[dict[str, Any]] = []
        for rec in records:
            console.print(f"[cyan]Translating {rec['id']}…[/cyan]")
            done.append(translate_one(client, model, rec))
        records = done

    args.out.parent.mkdir(parents=True, exist_ok=True)
    # Also mirror into web/public for the reader
    args.out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    web_copy = ROOT / "web" / "public" / "final_translated_data.json"
    web_copy.parent.mkdir(parents=True, exist_ok=True)
    web_copy.write_text(args.out.read_text(encoding="utf-8"), encoding="utf-8")
    console.print(f"[green]Wrote → {args.out}[/green]")
    console.print(f"[green]Mirrored → {web_copy}[/green]")


if __name__ == "__main__":
    main()
