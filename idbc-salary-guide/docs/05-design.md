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

## Tokens (as set in each page's `:root`)

| Token | Value | Role |
|---|---|---|
| `--dark` | `#132323` | navbar, hero card, primary text on green |
| `--dark-2` | `#0b1818` | footer |
| `--light-bg` | `#eef5ec` | page ground (with a faint dot pattern) |
| `--green` | `#a5df8f` | primary button, selects, summary cards, pill, highlight box |
| `--green-strong` | `#8fd474` | hover |
| `--text` | `#101818` | body |
| `--muted` | `rgba(16,24,24,.66)` | secondary copy |
| `--line` | `rgba(19,35,35,.18)` | borders |
| chart ramp | `#a5df8f` → `#55aa8b` → `#245d54` | offered → IDBC → expected; also the pool bars |
| type | Inter (system fallback), 900/800 weights for headings and labels | |
| radii | 28 / 14 / 18 px | hero, cards, tiles |
| tap floor | 44 px on phones | D17 |

The tokens are repeated in every page's `<style>`; `assets/chart.css` relies on them.
`14-token-map.md` is where they become a single definition for the production build.

## Layout

- **Navbar** fixed, flush to the top, overlaying the hero (from the SAP mockup); hamburger
  below 980 px; five items + two right-aligned actions (D19).
- **Hero** with a dark card bottom-left; eyebrow, `h1`, one sentence.
- **Summary block** of three green cards above every chart (band per perspective; on
  Expert Pool: pool size / positions / largest pool).
- **TOP3 chart**: wide layout above 700 px (role names in a left gutter, one shared
  axis), compact layout below (one block per position with its own scale; D18); LinkedIn
  pill under the role name; footnote under the chart (D22).
- **Tables**: desktop table; cards below 600 px of container width (D17); Bérek groups
  collapse behind a header showing the full band.
- **Area page**: summary text clamped to the media slot's height with "Olvass tovább";
  media slot = video placeholder or green key-thought box (D20).
- **Expert Community**: intro → two audience cards (join form behind a `<details>`,
  Ajánlatkérés anchor) → tiles (bar block anchored to the card bottom, D26) → contact form.
- **Articles** (SAP trends, case studies): one column, ≤ 760 px measure (D25).

## Measured at

375 px and desktop on every page after each change round since 2026-09-15; the numbers
are in the change notes in `SOURCES-AND-GAPS.md` and summarised in `07-gate.md`.
