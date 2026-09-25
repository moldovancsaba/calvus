# IDBC Salary Guide — design

*Where the look comes from, what the tokens are, and how the pages are laid out. There was
no separate design-system approval gate: the client supplied the design as mockups and the
pages transcribe them. Written 2026-09-18.*

## Source of the design

| Page | Designed by | Reference |
|---|---|---|
| Registration | client | `html demok/1_regisztracio.html` (not yet transcribed — the mock uses the guide's own components) |
| Piaci trendek | client | `html demok/2_savok.html` — the B2C/B2B filterable dashboard |
| SAP, Bérek, Expert Pool | client | `3_SAP.html`, then `3_SAP_TOP3_chart_gradient_tooltip_categories.html` (D4): fixed navbar over the hero, eyebrow, EN/HU switch, three summary cards, point-line chart, table, Excel CTA |
| Area pages | owner, on the trends page's components; highlight box per the client's `Highlight 1.png` | |
| TOP3 pill, Expert Pool tile | client | `TOPpozi 2.png`, `A bekezdés szövege-2 1.png` (2026-09-18) |
| Home teaser | client | `IDBC_SalaryGuide_home.pdf` — inside idbc.hu's template (not built) |
| Page frame (every page) | idbc.hu | measured 2026-09-25; `15-idbc-hu-alignment.md`, D39 |

## Since 2026-09-25: idbc.hu's design (D39)

The page frame — tokens, type, header, footer, heroes, buttons, cards, forms — now follows
idbc.hu, measured on 2026-09-25 (`15-idbc-hu-alignment.md`). The data components (TOP3
chart, salary tables, survey charts and filters, Expert Pool tiles) keep the client's demo
layouts above and only take idbc.hu's tokens. Everything shared lives in one file,
`assets/site.css` (with `assets/site.js` for the header menu); each page's own `<style>`
keeps only what is specific to that page and loads before it.

## Tokens (`assets/site.css`, `:root`)

| Token | Value | Role |
|---|---|---|
| `--dark` | `#121c1b` | header, footer, dark cards and buttons, text on green |
| `--dark-2` | `#14201f` | hero band and hero card |
| `--ground` / `--light-bg` | `#f5f9f2` + a light noise texture | page ground |
| `--green` | `#a4dd8c` | primary accent: header button group, selects, area tiles, pills |
| `--green-strong` | `#93d17a` | hover |
| `--green-mid` | `#35715c` | eyebrows on light, the home figures' cards |
| `--green-teal` | `#4ca283` | chart middle point |
| `--green-pale` | `#daf1d0` | plain hero band, figures on the green-mid cards |
| `--text` | `#121c1b` | body |
| `--muted` | `rgba(18,28,27,.66)` | secondary copy |
| `--line` | `rgba(18,28,27,.14)` | borders |
| `--footer-text` | `#a2a9a8` | footer copy |
| chart ramp | `#a4dd8c` → `#4ca283` → `#35715c` | offered → IDBC → expected; pool bars and legend |
| type | Outfit 400–800 (stand-in for idbc.hu's Gilroy until IDBC confirms the licence, A-1); titles 56/64 → 28/36 on phones, `h1` 40/48, `h2` 32/40, body 16/24, copy 18/28 | |
| radii | 32 (hero, footer top 56), 24 (cards), 16, 8 (buttons, selects, pills) | |
| buttons | 8 px corners, weight 600, 56 px (default), 40 px (header), 64 px (form submit); dark with a soft light glow, green, and dark/green outlines | |
| container | 1280 px; sections 48 px (32 on phones); sides 16 px on phones | |
| breakpoints | 1200 (header menu), 1023 / 767 (footer columns, phone scale) | |
| tap floor | 44 px on phones | D17 |

## Layout

- **Header** (`.sg-header`): idbc.hu's floating dark bar — 1312 px wide, 79 px tall, bottom
  corners 32 px, fixed; idbc.hu's SVG logo (links to idbc.hu), a divider, the guide's own
  "Salary Guide" link, EN/HU pills, the five guide links, the green-framed button group
  (Ajánlatkérés, Kijelentkezés); below 1200 px a green menu icon opens the links as 48 px
  rows.
- **Hero** (`.sg-hero`): dark band, photo with 32 px corners, centred dark card (eyebrow,
  `h1` 62/64, one sentence) overlapping the photo's lower edge — Kezdőoldal, Bérek, SAP, Expert
  Pool. **Plain hero** (`.sg-hero--plain`, idbc.hu's "hero type 2"): pale green band with
  rounded bottom — Esettanulmányok, Regisztráció, Kapcsolat, area pages. Per-page photo crops
  keep faces clear of the card (the client's 2026-09-22 "heads cut off" point).
- **Section titles** 56/64 bold, no rule under the intro block; eyebrows are small green
  sentence-case lines, not uppercase labels.
- **Home figures** as idbc.hu's number cards (`#35715c`, 32 px corners); **area tiles** as
  green rows with the dark arrow square.
- **Copy** regular weight at 16–18 px; labels 600 at 14 px (the demos' 700–900 weights at
  12–15 px are gone).
- **Forms**: white card with a soft green glow, underline fields, dark 64 px submit.
- **Footer** (`.sg-footer`): idbc.hu's — logo, contact, social icons, the guide's own column,
  idbc.hu's three link columns, bottom bar with Panaszbejelentő and Adatkezelési tájékoztató
  (linked to idbc.hu's own pages).
- **TOP3 chart, tables, survey charts, Expert Pool tiles**: unchanged in layout and figures
  (1,142 rendered states compared before and after), on the new tokens.

## Measured at

375 px and desktop on every page after each change round since 2026-09-15; the numbers
are in the change notes in `SOURCES-AND-GAPS.md` and summarised in `07-gate.md`.
