# Lexodont — design

*The wireframe's two fidelities, their tokens and layout; and what the built site chose
instead. Written 2026-09-18.*

## Two fidelities, one content

- **Polished** (`lexodont.hu/styles.css`): grey-scale "classic wireframe" (D5) — ground
  `#dcdcdc`, surface `#e2e2e2`, text `#2e2e2e`, lines `#8f8f8f`, primary `#4a4a4a`,
  radius 0, no shadows; Inter from Google Fonts; sticky header with brand text, six nav
  items and a booking CTA; sections `.section` / `.section-soft`; cards, case cards with
  the slider, staff grid, knowledge list, review grid, partner grid, three-column contact
  footer with the map.
- **Sketch** (`lexodont.hu_balsamic/styles.css`): Comic Sans / Marker Felt, 2 px `#444`
  borders, hatched "paper" hero, boxes in 2- and 3-column grids, underlined inline links —
  the Balsamiq idiom, for structural feedback (D10).

## Layout

Max width 1160 px; home sections in order: hero (image, kicker, `h1`, two CTAs, trust
list, wireframe note) → team cover + CTA → why-us (3 cards) → featured specialties (2 × 2)
+ CTAs → before/after (2 cases + CTA) → knowledge (text + 4 links) → reviews (3) → partners
(featured 2 + 5) → footer (contact, hours/parking, transport + map). Subpages: sub-hero
+ one content section + CTA panel + one-line footer.

## Tokens

| Token | Polished | Role |
|---|---|---|
| `--bg` / `--surface` / `--surface-soft` | `#dcdcdc` / `#e2e2e2` / `#d6d6d6` | grounds |
| `--text` / `--muted` | `#2e2e2e` / `#4f4f4f` | copy |
| `--line` | `#8f8f8f` | borders |
| `--primary` / `--primary-strong` / `--accent` | `#4a4a4a` / `#3e3e3e` / `#5a5a5a` | buttons, links |
| `--radius` / `--shadow` | `0` / `none` | wireframe flatness |
| `--split` | `50%` | before/after slider position (set by JS) |

Deliberately no brand colour: a wireframe asks about structure, not palette.

## What the built site chose

Outfit as the typeface, Bootstrap 5 components and grid, a real palette and photography,
Bootstrap Icons, Owl Carousel for galleries. The wireframe's tokens therefore map to
nothing in production — `14-token-map.md` records this rather than inventing a mapping.
