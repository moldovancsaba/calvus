# Design system — as built

*Tokens and components as implemented in `assets/tokens.css` and `assets/site.css`, shown live on
the style guide (`../styleguide/index.html`). Every choice traces to `01-research.md`; the reason is
given in `04-decisions.md`. Written 2026-09-25; rewritten 2026-09-26 to describe the site as it is —
how it got here is in `06-build-log.md`.*

## The idea

**The numbers are the picture.** No photographs; every cover and chart is drawn from the numbers
the story is about (D9) — the lead article's cover is its seed study's two estimates on one scale. The page structure follows the leaders the research measured — ink navy
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
| `--gf-blue` | `#1F47E0` | `#7C95FF` | **Form Blue**: brand, links, primary buttons, desk accents, the highlighted series |
| `--gf-orange` | `#E0560B` | `#FF8A3D` | **Energy Orange**: the one accent — article counts, the second series, the "notice this" bar |
| `--gf-orange-ink` | `#B23F00` | `#FF9E5E` | orange as text |
| `--gf-draw` | `#D9DCE3` | `#3A4560` | D chips, draw segments |
| `--gf-band` | `#0C1222` | `#050811` | the ink bands (how we source, newsletter, footer, covers) in both themes |

The blue and orange are the studio's own sRGB readings of the two forecast colours; no forecaster
publishes hex values (register T6). **Contrast is a gate check, not a claim**: `check.py` computes
every text pair (ink, text, muted, blue, orange-ink on ground, surface and sunk; the on-colours on
blue, orange, draw and band; blue and orange as marks against the surface at 3:1) in both themes —
48 pairs, all passing WCAG 2.2 AA.

**Colour never carries meaning alone.** The two source lists each have their own heading; the
current desk in the desk bar is marked with `aria-current`, not only a tint; in charts the highlighted
series also has a heavier or dashed stroke and a direct label, and form chips print W, D or L.

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
| Navigation | brand, search, theme on top; **tab bar** at the bottom: Home · Latest · Desks · Standards · More | as phone | brand, **top nav** (Home · Latest · Desks · How we work), search, theme, sign-in; no tab bar |
| Under the header | **desk bar** — the eight desks, swipe sideways; the current desk highlighted | the same | the same, one row |
| Home | lead article (cover, desk · kind, headline, opening, byline, reading time), Latest list, three cards, the eight desk tiles, the "how we source" band, newsletter (inert) | two-column grids | lead + Latest rail; three cards; desk tiles 3-up |
| Article | desk · kind · subject; headline; the desk's job; standfirst; byline with reading time and segments; **In this article**; headed segments; charts where the piece has data; **Sources used**; **Sources investigated but not used**; "More to read" below | as phone | 720 px text column + sticky "More to read" rail |
| Desk / subject page | name, what it is for, its articles — or a plain "none published yet" panel; the other desks / subjects | as phone | as phone, list items two-column |

## Components

- **Header**: brand (mark + "game**formative**"), top nav (desktop), search (inert), theme toggle,
  sign-in (inert, desktop). Sticky, translucent.
- **Desk bar** (`.gf-topicbar`): the eight desks; scrolls sideways on phones; the current desk is
  `aria-current` and tinted.
- **Tab bar and More sheet**: five tabs; More opens a dialog (focus moves in, Escape closes and
  returns focus) with the sections, the desks, All subjects, the later-phase data pages, theme and
  sign-in.
- **Article meta** (`.gf-cardmeta`): "Desk · Kind" on cards; "Desk · Kind · Subject: …" on the
  article, with the desk's job underneath (`.gf-deskline`).
- **Lead story, story card, list item**: data-graphic cover, meta, headline, the standfirst (or the
  opening of the first paragraph), date and reading time. Cards and list items are an `<article>`
  around one link.
- **Latest list** (`.gf-latest`), **desk tile** (`.gf-desk-tile`: name large, the desk's job, the
  article count in orange), **subject tile** (`.gf-topic-tile`).
- **In this article** (`.gf-toc-box`): the segment headings, linked.
- **Segment** (`.gf-seg-block`): a heading and its paragraphs; the paragraphs carry `data-count`,
  which is what the gate measures.
- **Source lists** (`.gf-sources`): *Sources used* in link blue, *Sources investigated but not used*
  in text colour, each entry: title (link) — publisher, date — one line on what it contributed or
  why it was set aside; then the link-check date and the body length.
- **How we source band** (`.gf-promise`): the three house rules as figures.
- **Charts**: bars (ranking), stacked bars (part-to-whole), columns (distribution), lines (a race) —
  chosen by the FT Visual Vocabulary; HTML labels at real size on every width; each with title,
  subtitle, source and "Show the numbers as a table".
- **Labels**: Analysis (blue), Explainer (neutral), Automated (orange, data pages only).
- **Inert panel**: dashed box that says plainly what is not there and why ("none published yet",
  "not built in the prototype").
- **Later-phase notice** (`.gf-later`): the strip on the data pages that says they are a preview.

The data pages (a later phase) keep their own components — league table with overall / home / away
and a compact phone mode, results list, stat tiles, bracket, group tables, match head, timeline and
line-ups — as built in round 1 (`06-build-log.md`).

## Motion

Only colour transitions on hover; nothing auto-plays, nothing auto-advances; smooth scrolling only
when the reader has not asked for reduced motion.

## Next for the design (not built)

- A **D-mark per desk** — all eight names begin with D, a pattern the brand can carry (an icon or a
  letterform per desk on tiles, covers and the desk bar). Needs the owner's and client's approval
  before it is drawn.
- **Covers for desks without data**: the data-graphic covers suit Data and the lead; Discover, Deal
  and Develop pieces will need a cover rule of their own (a number from the seed, a timeline, a
  typographic quote) once articles arrive.
