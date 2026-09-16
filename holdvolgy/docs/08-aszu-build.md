# Phase 2 — the Tokaji aszú page, measured

Built 2026-09-16, HU `aszu.html` and EN `en/aszu.html`, from the same content
source as the other pages. Content taken from the live `/tokaji-aszu` and
`/bor/culture-aszu` pages: the Culture statement, the three making steps and three
ageing steps (24 months in Seguin Moreau oak, 72 months in bottle, release at about
eight years), the Time Capsule and its eight life moments, the gift text, the
Holdvölgy guarantee, the PreCulture programme (opens every 10 December, World Aszú
Day; 6- and 3-bottle reservations 2018–2025) and the ten Tokaj heritage milestones
from the Miocene *Vitis tokaiensis* to the first Holdvölgy vintage in 2006.

The **Culture wall** carries all thirteen vintages 2006–2018 with the estate's own
renders and the webshop's September 2026 prices (27 500 → 133 000 Ft, the 2012 being
the 133 000 Ft item the plan had flagged as unconfirmed — it is the vintage, not a
format). Nobody else in Tokaj presents a vertical.

## Measured

| Check | Phone 390 | Tablet 768 (EN) | Desktop 1440 |
|---|---|---|---|
| Horizontal overflow / small taps | 0 / 0 | 0 / 0 | 0 / 0 |
| `h1` | "Meghatározó, gazdag, élettel teli" | "Defining, rich, full of life" | 1 |
| Images / no alt / broken | 23 / 0 / 0 | — / — / 0 | — |
| Hero source, height | portrait-780.avif | 1024.avif | 1440.avif, 720 px |
| Culture wall | 13 bottles, snap rail | 7 columns | 13 columns, bottles 160 px |
| Making + ageing steps | 6, stacked | 3 columns | 3 columns |
| PreCulture years | 8, 4 columns | 8 columns | 8 columns |
| Heritage milestones | 10, stacked | 2 columns | 2 columns |
| Language switch / reserve button | `en/aszu.html` / — | `../aszu.html` / `index.html#kapcsolat` | — |
| Fonts / console errors | Archivo, Bodoni Moda / 0 | 0 | 0 |
| Page height | 7,7 screens | — | — |

## Weight, cold

| | KB |
|---|---|
| Phone 390 | **738** |
| Tablet 768 | **746** |
| Desktop 1440 | **779** |

All under 1,5 MB; the wall (13 renders, 264 KB) and the PreCulture row (216 KB)
are lazy-loaded.

## Notes

- The hero is the site's own Aszú landing photograph (1512 × 798) — the phone
  portrait crop is upscaled and provisional; a portrait frame is in the client-gap
  list.
- PreCulture reservation buttons go to the contact block: the live site sells the
  reservation as a product, but a reservation flow is outside this prototype.
- The link audit caught a wrong filename for the 2025 PreCulture render before the
  push; fixed in the renderer.
