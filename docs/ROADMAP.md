# Agama–Kumarajiva Roadmap

Honest scope: this is a **digital humanities + LLM style-transfer** project, not a claim that Kumarajiva translated the Āgamas.

## Phases

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 1–5 | Align, dual output, web reader, golden set, optional LoRA | earlier |
| 6 | Full-corpus gold (1362), LaTeX edition, web sync | **done (v1)** |
| **7** | **V2 as a separate book** + web V1/V2 edition switch (Anesaki/Yinshun order; V1 kept) | **in progress** |
| 8 | Yinshun 51-saṃyukta range map; refine juan 23/25; V2 PDF release | next |
| 9 | TTS, print-on-demand packaging | later |

## V2 (separate academic edition) — policy

- **Two products, one series**「研究译注本」: V1（大正卷序）`book/` · `make book`; V2（经序重排）`book_v2/` · `make book-v2`.
- **Website**: edition switch **V1 大正卷序 / V2 经序重排**.
- **Framing**: scholarly reading order, **not** “restoring the original scripture.”
- **Stable anchor**: T99 / `sa_t99` never renumbered.
- **Main sequence**: Anesaki 48-fascicle order as adopted by Yinshun CSA; insertions SA 604, 640–641 → appendix.
- **Data first**: reorder tables before rewriting prose; see [V2_ORDER.md](V2_ORDER.md).
- **Build**: `make v2-order` → `data/metadata/v2/`; then `make book-v2` / `make sync-web`.

## What we will **not** over-claim

- That fascicle reorder equals the one true ur-text order.
- Perfect doctrinal infallibility without human review.
- That literary restyling equals historical authenticity.

## Data sources

- Chinese + Patton EN: [bilara-data](https://github.com/suttacentral/bilara-data) (`published` branch)
- Parallels: `https://suttacentral.net/api/parallels/{uid}`
- SN Pali / Sujato EN: bilara-data
- Order reconstruction: Anesaki (1908); Yinshun CSA; Anālayo / Bucknell on fascicles 23 & 25

## Attribution

Downstream products must credit Taishō / CBETA tradition for Chinese, SuttaCentral for parallels and Bilara texts, named translators (Patton, Sujato, Anālayo, etc.), and Yinshun / Anesaki for reconstructed order where used.

## Documentation

See [docs/README.md](README.md) for the full index.
