# Gate 3 — the built home page, measured

Built 2026-09-16 from the approved design system (D12) and frames (D13).
`holdvolgy/build.py` generates `index.html` (HU) and `en/index.html` (EN) from one
content dictionary; the page is one responsive document with three designed states:
phone ≤ 767, tablet 768–1023, desktop ≥ 1024.

## What was built

- **Navigation, two systems.** Desktop: sticky 88 px header, wordmark, the five
  items, HU/EN, *Foglalás*, cart; *Borok* and *Látogatás* open mega-panels on hover
  **and on keyboard focus** (`:focus-within`, no JS). Phone and tablet: 60 px header
  with wordmark, language and cart only; a fixed 64 px bottom bar (Foglalás · Borok ·
  Kosár · Menü) and a native `<dialog>` sheet with the five items plus four secondary.
- **Hero, art-directed.** `<picture>` serves a 780 × 1040 portrait crop under 768,
  1024 w to 1279, 1440 w above — AVIF with WebP fallback. The sentence in Bodoni
  Moda at 34 / 48 / 64.
- **Age gate** as a `<dialog>`, on the light ground, remembered per session.
- Sections per the frames: three cards (compact rows on phone, 2 + 1 on tablet, 3 on
  desktop); the wine band (snap rail on phone, 3-column on tablet, 6 on desktop);
  seven dűlők (3 rows + link on phone; map + 7 rows above); visit; newsletter; footer.
- Every string, alt text and label lives once in `build.py` for both languages.
  `hreflang` hu / en / x-default on both pages.
- The withdrawn first-prototype shop page (`borok/`) was removed; wine links go to
  the band until Phase 3.

## Measured (local, browser at each reference size)

| Check | Phone 390 | Tablet 768 | Desktop 1440 |
|---|---|---|---|
| Horizontal overflow | 0 px | 0 px | 0 px |
| Tap targets under 44 px | 0 (after fixing the EN link, 35 → 44) | 0 (after fixing footer links, 30 → 44) | 0 (same fix) |
| `h1` count | 1 | 1 | 1 |
| Images without `alt` | 0 of 17 | 0 | 0 |
| Broken images | 0 | 0 | 0 |
| Hero source chosen | `hero-cellar-portrait-780.avif` | `hero-cellar-1024.avif` | `hero-cellar-1440.avif` |
| Hero / header height | 520 / 60 | 560 / 60 | 720 / 88 |
| Grid columns cards / bottles / dűlők / visit / footer | rows / rail / 3 rows | 2 (+1 spanning) / 3 / map above / stacked | 3 / 6 / 2 / 2 / 5 |
| Bottom bar | fixed, 64 px | fixed | hidden |
| Desktop nav | hidden | hidden | visible; mega-panel opens on focus with 7 links |
| Age gate | opens on fresh load, closes on Igen, remembered | — | same |
| Sheet | opens, lists 9 items, closes on ✕ / backdrop / link | same | n/a |
| Fonts loaded | Archivo, Bodoni Moda | same | same |
| Console errors | 0 | 0 | 0 |
| Page height | 3,0 screens | — | — |

## Weight, cold (bytes on disk plus the Google Fonts files a Chrome UA receives)

| | KB | vs 1,5 MB target |
|---|---|---|
| Phone 390 | **600** | under, 61 % headroom |
| Tablet 768 | **724** | under |
| Desktop 1440 | **734** | under, 52 % headroom |
| of which fonts | 149 | four woff2 files, latin + latin-ext |

For comparison the live holdvolgy.com home page measures 8,8 MB and 226 requests
(technical brief, 2026-09-08). This page makes 4 requests before fonts and images.

## Known limits, carried forward

- Wine, card and dűlő links point to in-page anchors until Phase 2–3 build their
  pages.
- The phone hero is a centre crop of the landscape photograph (§6 gap).
- Úrágya and Kakasok show a marked gap instead of a rock photograph (§6 gap).
- Hidden dűlő rows on the phone still download their thumbnails (4 × ~17 KB); the
  phone figure above includes them.
- The newsletter form is inert (prototype).
