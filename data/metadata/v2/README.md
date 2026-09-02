# V2 metadata

Supports the **separate V2 edition**《研究译注本（经序重排）》(`book_v2/`). V1《研究译注本（大正卷序）》(`book/`) stays on T99 order.

| File | Role |
|------|------|
| `fascicle_order_anesaki.json` | Anesaki/Yinshun T99 fascicle permutation |
| `academic_order.json` | Full dual-ID records (main + appendix) |
| `academic_order_index.json` | Compact index for web V1/V2 switch |
| `yinshun_samyukta_catalog.json` | Yinshun 51 saṃyuktas (**ranges TBD**, phase 2) |

```bash
make v2-order
make sync-web   # copies index → web/public/
make book-v2    # separate PDF with full front matter
```

See [docs/V2_ORDER.md](../../docs/V2_ORDER.md).
