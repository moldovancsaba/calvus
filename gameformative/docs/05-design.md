# Design system — as built

*Tokens and components as implemented in `assets/tokens.css` and `assets/site.css`, shown live on
the style guide (`../styleguide/index.html`). Every choice traces to `01-research.md`; the reason is
given in `04-decisions.md`. Written 2026-09-25.*

## The idea

**The numbers are the picture.** No photographs; every cover, tile and chart is drawn from the data
the story is about (D9). The page structure follows the leaders the research measured — ink navy
bands, white or off-white surfaces, one saturated accent — and the colours are read from the 2027
forecasts (projections: WGSN × Coloro Luminous Blue and Energy Orange). The logo mark is a form line
rising to an orange point: a run of results, the latest one highlighted.

## Colour

| Token | Light | Dark | Role |
|---|---|---|---|
| `--gf-ground` | `#F7F6F2` | `#0B0F1A` | page background — a warm off-white (after Pantone 2026 Cloud Dancer) / ink navy |
| `--gf-surface` | `#FFFFFF` | `#141B2B` | cards, tables, charts |
| `--gf-sunk` | `#EFEDE7` | `#10172A` | tracks, segmented controls, banner |
| `--gf-ink` | `#0C1222` | `#F3F5F9` | headlines, figures |
| `--gf-text` | `#1F2637` | `#D5DAE4` | body text |
| `--gf-muted` | `#596175` | `#9AA3B6` | meta, captions |
| `--gf-line` / `--gf-line-strong` | `#E3E1DA` / `#C9C6BC` | `#27314A` / `#3A4666` | hairlines; neutral bars |
| `--gf-blue` | `#1F47E0` | `#7C95FF` | **Form Blue**: brand, links, primary buttons, W chips, the highlighted series |
| `--gf-orange` | `#E0560B` | `#FF8A3D` | **Energy Orange**: the one accent — L chips, the second series, the "notice this" bar |
| `--gf-orange-ink` | `#B23F00` | `#FF9E5E` | orange as text |
| `--gf-draw` | `#D9DCE3` | `#3A4560` | D chips, draw segments |
| `--gf-band` | `#0C1222` | `#050811` | the ink bands (World Cup, newsletter, footer, covers) in both themes |

The blue and orange are the studio's own sRGB readings of the two forecast colours; no forecaster
publishes hex values (register T6). **Contrast is a gate check, not a claim**: `check.py` computes
every text pair (ink, text, muted, blue, orange-ink on ground, surface and sunk; the on-colours on
blue, orange, draw and band; blue and orange as marks against the surface at 3:1) in both themes —
48 pairs, all passing WCAG 2.2 AA.

**Colour never carries meaning alone.** Form chips print W, D or L; outcome bars print H, D and A
with their percentages; the highlighted series in a chart also has a heavier or dashed stroke and a
direct label; the top-four and bottom-three table bands have a printed key.

## Type

One variable family, **Archivo** (Google Fonts, `wdth` 62–125, `wght` 400–900), in three widths:

| Use | Width | Weight | Size |
|---|---|---|---|
| Display — page titles, lead headline, scores, stat numbers | 72% (`--gf-condensed`) | 800 | 34–60 px, fluid |
| Card and chart headlines | 85% | 750 | 19–26 px |
| UI, body, tables | 100% | 400–800 | 14.5–18 px |
| Kicker, labels | 100% | 800, tracked caps | 11–12 px |

Tabular numerals (`font-variant-numeric: tabular-nums`) are set on the body, so every column of
figures aligns. Fallback: Arial Narrow, then the system sans.

## Space, shape, targets

8 px base; content max width 1240 px; gutters 16 px (phone) and 24 px; radius 10 px (cards),
6 px (chips, ties), pill (buttons, segmented controls). Every interactive element is at least
44 × 44 px on phones (`--gf-tap`), measured (`06-build-log.md`).

## Layout at the reference widths

| | Phone (375–719) | Tablet (720–999) | Desktop (1000+, reference 1440) |
|---|---|---|---|
| Navigation | brand, search, theme on top; **five-tab bar** at the bottom (Home, Scores, Stats, Analysis, More) | as phone | brand, **six-item top nav**, search, theme, sign-in; no tab bar |
| Results strip | swipe; compact label | swipe + arrow buttons | swipe + arrow buttons |
| Home | one column: lead, the table, numbers (2×2), stories, leagues, bands | two-column grids | lead story + table rail; 4-up numbers, 3-up stories, 4-up leagues |
| League table | **compact** (#, Team, P, GD, Pts) + "All columns"; team codes | full | full, sortable, overall / home / away |
| Charts | full width; HTML labels at real size | two-up | two-up |
| World Cup bracket | each round as a grid of ties | as phone | five-column bracket tree, ties aligned to their feeders |
| Article | single column; rail below | as phone | 720 px text column + sticky rail |

## Components

- **Header**: brand (mark + "game**formative**"), top nav (desktop), search (inert), theme toggle,
  sign-in (inert, desktop). Sticky, translucent.
- **Results strip**: the latest round of all five leagues, one chip per match (league, codes, score,
  winner in bold), linking to the league's results; arrow buttons on wider screens.
- **Tab bar and More sheet**: five tabs; More opens a dialog (focus moves in, Escape closes and
  returns focus).
- **Labels**: Analysis (blue), Explainer (neutral), Automated (orange), Season/Tournament review
  (muted). Every piece carries one.
- **Stat tile**: a condensed figure, what it counts, its context; the accent tile has an orange top
  rule.
- **Story card / list item / lead story**: data-graphic cover, label, headline, dek, date.
- **League snapshot**: top five, last three results as form chips, points.
- **League table**: sortable headers (buttons, announced to screen readers), sticky header and team
  column, zone bands with a key, form chips, overall / home / away views, compact phone mode.
- **Results list**: home — score — away, winner in bold, date; fixtures show kick-off time.
- **Charts**: bars (ranking), stacked bars (part-to-whole), columns (distribution by minute), lines
  (points race) — chosen by the FT Visual Vocabulary; each in a figure with title, subtitle, source
  and "Show the numbers as a table".
- **Band**: ink navy block for the World Cup review and the newsletter, in both themes.
- **Match head, timeline, line-ups**: the match centre; goals and substitutions by minute.
- **Bracket**: the knockout rounds in tree order (the converter walks back from the final).
- **Inert panel**: dashed box that says what is not built and why (xG, live data, statistics).
- **Transparency note**: on every article — who wrote it, where every figure comes from, the
  corrections link.

## Motion

Only colour transitions on hover; smooth scrolling of the strip only when the reader has not asked
for reduced motion. Nothing auto-plays, nothing auto-advances.

## Round 2 — articles first (2026-09-25)

The tokens, type and colour are unchanged. What changed is the structure:

| | Phone | Desktop |
|---|---|---|
| Navigation | tab bar: Home · Latest · Topics · Standards · More | top nav: Home · Latest · Topics · How we work |
| Under the header | **topic bar** — all eleven topics, swipe sideways; the current topic highlighted | the same, one row |
| Home | lead article (cover, topic · kind, headline, opening, byline, reading time), Latest list, more cards, topic tiles (compact), the sourcing promise band, newsletter (inert) | lead + Latest rail; three cards; topic tiles 3-up; bands |
| Article | topic · kind, headline, standfirst, byline with reading time and segment count, **In this article** (the segment headings, linked), headed segments, charts where the piece has data, **Sources** — used, then investigated but not used, each with publisher and a one-line reason; "More to read" below | 720 px text column with a sticky "More to read" rail |
| Topic page | name, what it covers, its articles — or a plain "none published yet" panel | the same |

New components: `.gf-topicbar`, `.gf-cardmeta` (topic · kind), `.gf-latest`, `.gf-topic-tile` and
`.gf-topic-grid`, `.gf-promise` (the three rules as figures), `.gf-toc-box`, `.gf-seg-block`,
`.gf-sources` and `.gf-source-list` (the "investigated" list set in text colour, the "used" list in
link blue, so the two read differently without relying on colour alone — each has its own heading),
`.gf-later` (the data pages' notice). Story cards and list items are now an `<article>` around one
link, so screen readers announce each as an article.

The cover of the first article is drawn from its seed source's two numbers: the pooled odds ratio
(1.33, CI 0.85–2.07) and the pooled relative risk (2.33, CI 1.65–3.30) on one scale with the
no-effect line at 1 — the article's argument in one picture, and no photograph needed.
