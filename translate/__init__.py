"""Load system prompts and forbidden-term checks."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_system_prompt() -> str:
    return (ROOT / "prompts" / "kumarajiva_system.md").read_text(encoding="utf-8")


def load_forbidden_terms() -> list[str]:
    path = ROOT / "glossary" / "forbidden_mahayana.txt"
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def find_forbidden_hits(text: str) -> list[str]:
    return [t for t in load_forbidden_terms() if t in text]


def user_message(record: dict) -> str:
    parts = [
        f"## id\n{record.get('id')}",
        f"## title\n{record.get('title')}",
        f"## chinese_source\n{record.get('chinese_text')}",
    ]
    if record.get("english_sa_text"):
        parts.append(f"## english_sa\n{record['english_sa_text']}")
    if record.get("primary_sn_uid"):
        parts.append(f"## primary_sn_uid\n{record['primary_sn_uid']}")
    if record.get("pali_text"):
        parts.append(f"## pali_parallel\n{record['pali_text']}")
    if record.get("english_sn_text"):
        parts.append(f"## english_sn\n{record['english_sn_text']}")
    parts.append(
        "请按系统提示输出严格 JSON（仅 JSON，不要 Markdown 代码围栏）。"
    )
    return "\n\n".join(parts)
