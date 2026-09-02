# Agama–Kumarajiva Roadmap

Honest scope: this is a **digital humanities + LLM style-transfer** project, not a claim that Kumarajiva translated the Āgamas.

## Phases

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 1–5 | Align, dual output, web reader, golden set, optional LoRA | earlier |
| 6 | Full-corpus gold (1362), LaTeX edition, web sync | **done (v1)** |
| **7** | **V2** 研究译注本（经序重排）+ 网页开关 | **done** |
| **8** | **V3** 法义读本（通读熔文）+ 网页双栏 | **done (v3.0)** |
| 9 | Yinshun 51-saṃyukta range map; refine V2 juan 23/25 | next |
| 10 | Deeper V3 literary rewrite; TTS; print packaging | later |

## V2 (separate academic edition) — policy

- **Products**: V1（大正卷序）`book/`; V2（经序重排）`book_v2/`; see also V3 below.
- **Website**: edition switch **V1 / V2 / V3**.
- **Framing**: scholarly reading order, **not** “restoring the original scripture.”
- **Stable anchor**: T99 / `sa_t99` never renumbered.
- **Build**: `make v2-order` → `make book-v2` / `make sync-web`.

## V3 (dharma reader) — policy

- **Readable first**: new pedagogical titles; melt many SA into continuous sections.
- **Layers**: literary + modern + notes only (no base/parallel panels).
- **Not** 序分/正宗分/流通分 chapter labels; spirit of open→doctrine→close only.
- **Build**: `make v3-reader` → `make book-v3`.
- See [V3_DHARMA_READER.md](V3_DHARMA_READER.md).

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
