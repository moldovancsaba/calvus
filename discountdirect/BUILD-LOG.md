# DiscountDirect — build log

*Every build round with what changed and what was measured. Earlier rounds are
reconstructed from the commit history; from 2026-09-18 on, each round is written here.*

| Date | Round | What changed | Measured |
|---|---|---|---|
| 2026-08-25 | v1–v14 | wireframe added to the hub; channels, flash campaigns, automated lists; separate buyer inbox; full screen per function with targeting and preview; `hidden` attribute honoured; per-channel delivery samples; version note; sample data to 8 buyers / 26 products / multi-year histories; channel-aware timeline | desktop by eye; no recorded measurements |
| 2026-08-27 | v15 | tokens renamed to GDS 6.5.0 roles; `GDS-TOKEN-MAP.md` | none |
| 2026-09-17 | docs | seven documents written and rendered; decisions D1–D26 | link audit via `holdvolgy/check.py` (covers this folder) |
| 2026-09-18 | v16 | phone-width rule: `.app` and `.campaigns` collapse to `minmax(0, 1fr)`, tabs wrap, 12 px side padding, 44 px minimum on every control below 700 px | before: 103 / 29 / 29 / 20 / 10 px overflow across the five screens at 375 px, 12–17 targets under 44 px; after: 0 / 0 on all seven screens; desktop 1024 unchanged (0 px overflow, toggle 29 px as before); 0 console errors |
| 2026-09-18 | docs | customer side: presentation, audit, sources, design, build log, gate, client asks, index; renderer page list extended | `holdvolgy/check.py` clean |
