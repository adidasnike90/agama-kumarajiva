"""Shared helpers for Bilara / SuttaCentral fetching."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import httpx

BILARA_RAW = "https://raw.githubusercontent.com/suttacentral/bilara-data/published"
SC_API = "https://suttacentral.net/api"
USER_AGENT = "agama-kumarajiva/0.1 (+local research pipeline)"


def sa_bucket(n: int) -> str:
    """Map SA number to bilara folder name (best-effort)."""
    if 1 <= n <= 100:
        return "sa1-100"
    if 101 <= n <= 200:
        return "sa101-200"
    if 201 <= n <= 300:
        return "sa201-300"
    if 301 <= n <= 400:
        return "sa301-400"
    if 701 <= n <= 800:
        return "sa701-800"
    if 801 <= n <= 900:
        return "sa801-900"
    if 1101 <= n <= 1200:
        return "sa1101-1200"
    if 1201 <= n <= 1300:
        return "sa1201-1300"
    # Unknown / missing range in published tree — caller may fall back to HTML API.
    lo = ((n - 1) // 100) * 100 + 1
    hi = lo + 99
    return f"sa{lo}-{hi}"


def bilara_join(segments: dict[str, str], *, skip_meta: bool = True) -> str:
    """Join Bilara segment JSON into readable plain text."""
    lines: list[str] = []
    for key in sorted(segments.keys(), key=_segment_sort_key):
        # keys like sa1:0.1 are titles/headers; sa1:1.1 body
        if skip_meta and re.search(r":0\.", key):
            continue
        val = segments[key]
        # strip light HTML
        val = re.sub(r"<[^>]+>", "", val)
        lines.append(val.strip())
    text = "".join(lines) if _looks_cjk("".join(lines[:3])) else " ".join(lines)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _looks_cjk(s: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", s))


def _segment_sort_key(key: str) -> tuple:
    # sa1:2.3 -> (2, 3) ; sn22.12:1.1 -> similar
    m = re.search(r":(\d+)(?:\.(\d+))?(?:\.(\d+))?$", key)
    if not m:
        return (9999, 0, 0, key)
    return (int(m.group(1)), int(m.group(2) or 0), int(m.group(3) or 0), key)


def html_to_text(html: str) -> str:
    from html.parser import HTMLParser

    class _P(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.parts: list[str] = []
            self.skip = False

        def handle_starttag(self, tag: str, attrs) -> None:
            if tag in ("script", "style"):
                self.skip = True
            if tag in ("br", "p", "div", "li", "h1", "h2", "h3"):
                self.parts.append("\n")

        def handle_endtag(self, tag: str) -> None:
            if tag in ("script", "style"):
                self.skip = False

        def handle_data(self, data: str) -> None:
            if not self.skip:
                self.parts.append(data)

    p = _P()
    p.feed(html)
    text = "".join(p.parts)
    # Resolve CBETA gaiji markup left as ［A／B］ → Unicode from HTML comment if present
    def _gaiji_repl(m: re.Match[str]) -> str:
        code = m.group(2)
        try:
            return chr(int(code, 16))
        except ValueError:
            return m.group(1)

    # Prefer resolving from original HTML before strip
    html_resolved = re.sub(
        r"<span class='t-gaiji'>［[^］]+］<!--gaiji,,1\[[^\]]+\],2&#x([0-9A-Fa-f]+);,3--></span>",
        lambda m: chr(int(m.group(1), 16)),
        html,
    )
    if html_resolved != html:
        p2 = _P()
        p2.feed(html_resolved)
        text = "".join(p2.parts)
    # Fallback: known composition → char (when comment already stripped)
    for comp, code in (
        ("少／兔", 0x3779),
        ("木＊奈", 0x3B88),
        ("疊＊毛", 0x3CB2),
        ("卄／梨", 0x4527),
    ):
        text = text.replace(f"［{comp}］", chr(code))
        text = text.replace(f"[{comp}]", chr(code))
    # Strip Taishō inline refs like T 0001a07
    text = re.sub(r"T\s*\d{4}[a-c]\d{2}", "", text)
    text = re.sub(r"T\s*-?juan\d+", "", text)
    # Strip SuttaCentral HTML footer / headers
    text = re.sub(r"(?s)This Chinese translation.*", "", text)
    text = re.sub(r"(?s)^Sa[ṁm]yuktāgama雜阿含經\s*", "", text)
    text = re.sub(r"(?s)^Sa[ṁm]yuktāgama.*?\n+", "", text)
    text = re.sub(r"(?m)^SA\s+\d+[^\n]*\n+", "", text)
    text = re.sub(r"(?m)^（[〇一二三四五六七八九\d]+）[^\n]*\(SA\s*\d+\)\s*\n?", "", text)
    text = re.sub(r"宋天竺三藏求那跋陀羅譯\s*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class HttpClient:
    def __init__(self, cache_dir: Path | None = None, timeout: float = 60.0) -> None:
        self.cache_dir = cache_dir
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)
        self._client = httpx.Client(
            timeout=timeout,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def get_json(self, url: str, *, use_cache: bool = True) -> Any:
        cache_path = None
        if self.cache_dir and use_cache:
            safe = re.sub(r"[^\w.\-]+", "_", url)
            cache_path = self.cache_dir / f"{safe}.json"
            if cache_path.exists():
                return json.loads(cache_path.read_text(encoding="utf-8"))
        r = self._client.get(url)
        r.raise_for_status()
        data = r.json()
        if cache_path is not None:
            cache_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return data

    def get_text(self, url: str) -> str:
        r = self._client.get(url)
        r.raise_for_status()
        return r.text
