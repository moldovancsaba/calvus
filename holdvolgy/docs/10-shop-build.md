# Phase 3 — the shop: Borok grid, product pages, Borklub

Built 2026-09-16 from `holdvolgy/data/catalogue.json`, generated from the live shop
and every product page (D8 applied: one catalogue drives HU and EN). 32 products:
Culture 2006–2018 (13), Aszú Útkeresés 2007, Signature 2007/2013, Eloquence 2014,
Intuition No1/No2/No3/No8, Exaltation 2017 Reserve/2018, Vision 2018/2018 Magnum/2021,
Meditation 2023, Expression 2021 Reserve/2022, Hold and Hollo Dry/Sweet/Uppp. Each
carries the client's own name, category, size, price, tagline and description in
**both languages** — the English taken from the live `/en/wine/` pages, not
translated — plus variety and dűlő parsed from the category, and the estate's render.

Pages generated: `borok.html` + `en/borok.html` (grid), 32 + 32 product pages under
`bor/` and `en/bor/`, `borklub.html` + `en/borklub.html`. 130 HTML files in the
project now; every link and cross-page anchor audited.

## The grid

Filters Mind · Száraz · Édes · Aszú · Hold and Hollo (chips, `aria-pressed`), sort by
collection (with collection headings, linkable as `#line-culture` etc. from the
mega-panel) or by price either way, items without a price always last. Two columns on
the phone, three on tablet, four on desktop. Bottles as transparent objects on the
band colour, bounded inside a 4:5 figure.

## The product page

Render, collection, name, category and size, the tagline in Bodoni, the description,
a facts list (category, vintage, size, variety, dűlő), the price with size beneath,
*Kosárba* (inert) and *Kóstold a birtokon* → the tickets; four related wines from the
same collection; delivery line; a link to the live product page; Product/Offer JSON-LD
(validates, carries HUF price and the live URL). Exaltation 2017 Reserve shows
"Ár egyeztetés alatt" with *Érdeklődöm* — the live page shows 0 Ft.

## Borklub

The real programme: 5 / 10 / 15 / 20 % at 50 000 / 150 000 / 300 000 / 600 000 Ft
within 12 months, the two tier gifts, the three-step mechanism, the rules, and
how to join.

## Measured

| Check | Phone 390 | Desktop 1440 |
|---|---|---|
| Grid | 32 cards, 2 columns, 10 collection headings; Aszú filter → 14; price sort 4 000 → 133 000, no-price last | 4 columns; mega-panel links to 6 collection anchors |
| Product (Culture 2012) | `h1`, price 133 000 Ft · 37,5 CL, 4 facts, 4 related, JSON-LD Product with price; image 134×400 inside a 358×448 figure | two columns |
| Borklub | 4 tiers, 3 steps, 4 benefits | — |
| Overflow / small taps | 0 / 0 (after bounding figures and two link fixes) | 0 / 0 (after the "Visit" nav item, 42 → 44) |
| Console errors | 0 | 0 |

## Weight, cold

| | KB |
|---|---|
| Grid, all 32 renders (lazy) | **965** |
| Product page with 4 related | **334** |
| Borklub | **191** |

## Found and fixed in the gate

- Bottle images overflowed their figures on the phone: a percentage height inside an
  `aspect-ratio` grid cell resolves to auto, so the image fell back to its 720 px
  attribute. Figures are now positioned boxes and the image is absolutely centred with
  `max-height`/`max-width` bounds (D17).
- The live EN page for Vision 2021 carries Hungarian copy; the 2021 page here uses the
  same line's English from the 2018 page (noted for the client).
- Two live product URLs 404 on holdvolgy.com (Exaltation 2017 sweet, Eloquence 2013) —
  for the W22 broken-link list.
