# Phase 5 — the whole-site gate sweep

Run 2026-09-16 over every site page (docs excluded) at both reference widths.

## Method

Each page was loaded in a same-origin iframe of the exact width — 390 and 1440 —
from the local server, and measured after load: `<title>` present, `lang`, one `h1`,
images without `alt`, three `hreflang` links, horizontal overflow, every visible tap
target ≥ 44 px (age gate and sheet excluded as hidden), the token stylesheet resolved
(page ground `#FAFAFA`), both web fonts loaded, the bottom bar shown below 1024 and
hidden above, the desktop navigation shown at 1440. No headless-browser dependency
was added; the sweep ran in the app's browser pane.

Limit: console errors are not captured per iframe; they were checked page-type by
page-type in the earlier gates (home, Birtok, aszú, Látogatás, shop, product, club),
all zero.

## Result

| | |
|---|---|
| Pages measured | **76** (13 site pages + 32 HU product pages + 32 EN product pages; the redirect stub is not a page) |
| Measurements | **152** (each page at 390 and 1440) |
| Defects | **0** |
| One `h1` everywhere | yes |
| No image without `alt` | yes |
| `hreflang` hu / en / x-default everywhere | yes |
| No horizontal overflow at either width | yes |
| No tap target under 44 px at either width | yes |
| Tokens and both fonts resolved everywhere | yes |
| Navigation system correct for the width everywhere | yes |

Link audit at the same commit: 3 738 relative references across 93 HTML files, 0
broken; every cross-page anchor resolves; every doc page links every other.

## Re-run after the readiness review (2026-09-17)

The product template changed (tasting note, vintage note, fact sheet), so the sweep
ran again on the new build: **76 pages, 152 measurements, 0 defects**, with one
criterion added — no fixed-positioned element inside `main` — after the fact-sheet
section's class collided with the menu dialog's (D18).

## Hand-off state

- `holdvolgy/build.py` generates every page in both languages from one content
  source; `holdvolgy/data/catalogue.json` is the shop. `python3 holdvolgy/build.py`
  regenerates the site; `python3 holdvolgy/docs/build.py` regenerates the docs.
- `assets/img/` holds 130 committed derivatives (WebP/AVIF), every one traced to its
  source URL in `assets-used.md`; no original is committed.
- Open client items (from the plan's §6): founder and team portraits; rock
  photographs for Úrágya and Kakasok; portrait-format hero photographs for the phone;
  per-wine technical data; the aszú process diagram; whether to keep the live site's
  English copy verbatim (Vision 2021's EN page is Hungarian).
- Client-side findings for the technical work list: two product URLs 404 on the live
  site; Exaltation 2017 Reserve priced 0 Ft; three AI-generated images live.
