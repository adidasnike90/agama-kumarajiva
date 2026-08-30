# Agama–Kumarajiva Roadmap

Honest scope: this is a **digital humanities + LLM style-transfer** project, not a claim that Kumarajiva translated the Āgamas, and not an automatic fix for all Taishō disorder.

## Phases

| Phase | Deliverable | Status target |
|-------|-------------|---------------|
| 1 | Align SA Chinese + Patton EN + SC parallels + SN (Pali/Sujato) for a pilot set | v0.1 |
| 2 | Prompted dual output: Kumarajiva-like + modern plain Chinese | v0.1 |
| 3 | Three-column web reader for human review | v0.1 |
| 4 | Golden set (human-edited) + eval checklist | v0.2 |
| 5 | Optional LoRA/SFT on open model after ≥50–100 reviewed sutras | later |
| 6 | Full-corpus gold (1362 suttas), LaTeX research edition, web reader sync | **done** (v1) |
| 7 | TTS, print-on-demand packaging | later |

## What we will **not** over-claim

- “One-click 错简 restoration” — use SuttaCentral parallels and published scholarly order (e.g. Yinshun / Bingenheimer tables) as **data**, not as AI magic.
- Perfect doctrinal infallibility without human review.
- That literary restyling equals historical authenticity.

## Data sources

- Chinese + Patton EN: [bilara-data](https://github.com/suttacentral/bilara-data) (`published` branch)
- Parallels: `https://suttacentral.net/api/parallels/{uid}`
- SN Pali / Sujato EN: bilara-data
- Fallback HTML: SuttaCentral `/api/suttas/{uid}`

## Attribution

Downstream products must credit Taishō / CBETA tradition for Chinese, SuttaCentral for parallels and Bilara texts, and named translators (Patton, Sujato, Anālayo, etc.).

## Documentation

See [docs/README.md](docs/README.md) for the full index (getting started, architecture, contributing, edition principles).
