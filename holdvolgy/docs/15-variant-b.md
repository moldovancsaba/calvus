# Variant B — the original design language

*Built 2026-10-02 on the client's request: "a variant with the original design language — make a version B with that and compare the two". Decisions D21 and D22 (`04-decisions.md`). Client-facing comparison: `osszehasonlitas.html`.*

## What B is

The same site as A — same 76 pages in HU and EN, same texts, prices, technical sheets and photographs, same five-item navigation (D4), same phone/desktop split (D5), same age gate, same shop behaviour — dressed in the design language of the live holdvolgy.com instead of the language approved in D12/D13. Navigation, content and structure are not part of "design language" here; the client can already compare those against the live site in `02-brand-and-site-audit.md`.

B lives in `holdvolgy/b/` (`b/index.html`, `b/en/index.html`, and the same page names below them). A stays at the project root, untouched, and remains the approved direction until the client chooses.

## What "the original design language" was measured to be

Read from the live site on 2026-10-02 (computed styles in the browser) on top of the Elementor kit of the 2026-09-16 audit:

| Element | Measured on holdvolgy.com |
|---|---|
| Display type | Didot, uppercase; h1 72 px / line 80 px, h2 52 px / line 78 px |
| Text and labels | Akzidenz-Grotesk BQ Extended, 11–12 px, letter-spacing about 0.1 em |
| Primary button | `linear-gradient(90deg, #B8A689 2.08%, #E0D2BB 31.97%, #BAA793 100%)`, white label, 12 px, 1.2 px tracking, padding 12 × 30, square |
| Ghost button | transparent, 1 px white border, white label, same size — on photographs |
| Text link | `#B8A689`, 14 px, 1.4 px tracking |
| Header | white, 104 px, 12 px menu, search / mail / language / menu icons on the right |
| Cart | a 40 × 100 px vertical champagne tab on the right edge, a white count box above it |
| Home hero | warm taupe wash; "ÉV PINCÉSZETE 2026" in uppercase Didot; three black-and-white photographs in thin white frames; a circular seal |
| Marquee band | a 52 px champagne band with the estate's seven words, scrolling: Türelem, Szellem, Lélek, Gondolat, Tudás, Elvek, Fantázia (EN: Patience, Spirit, Mind, Thoughts, Knowledge, Principals [sic], Imagination) |
| Section surfaces | `#FFFFFF`, `#FAFAFA`, `#F4F4F4`, `#F5F5F5`, `#B8A689`; a grey "mist" gradient (`#F5F5F5` → `#D9D8D7` → `#F5F5F5`) behind sections |
| Footer | grey band: contact roles, map, newsletter card with a champagne button, payment logos |
| Age gate | light grey card, the sunburst mark, champagne buttons |

## How B is built

One generator, two passes. `python3 holdvolgy/build.py` runs `build_all("a")` then `build_all("b")`.

- **A is byte-identical.** The B work is a stylesheet layer (`CSS_B`) appended after A's `CSS`, plus four places where the markup differs: the home hero with the marquee band, the cart link, the footer (a full-bleed band instead of a content-width one) and the age-gate mark. Every theme switch emits the original text when the theme is A. Verified by hashing all 77 A pages before and after: identical. This matters because the live storefront of the `moonvalley` tenant in `customer.direct` loads A's pages, tokens and catalogue from the published site.
- **B is a closed tree.** Relative links never leave `b/` except to the shared `assets/` (language switch included); B's hreflang points at B; every B page carries `noindex`, no A page does. `holdvolgy/check.py` enforces all of this and the banner rule per variant (A: two banners, B: two banners, each saying "B változat" / "Version B"). A negative test (a B page linking to A, a B page without `noindex`) failed the gate as it should, after fixing a prefix-match bug in the first version of the rule — `holdvolgy/borok.html` starts with the string `holdvolgy/b`; the rule now tests parent directories.
- **No new assets.** The home collage reuses three existing photographs (vineyard rows, the building from above, the candle niche), turned black and white in CSS. Nothing was downloaded; D6 and D7 stand. The age gate loads the existing `logo.svg` (the sunburst mark), lazily.

## A → B

| | A | B |
|---|---|---|
| Ground | `#FAFAFA` | `#FFFFFF` |
| Home hero | cellar photograph, dark veil, sentence headline | taupe wash, uppercase "Év pincészete 2026", tagline beneath, collage, seal |
| Display type | Bodoni Moda, sentence case | Bodoni Moda, uppercase, optical size capped at 30 |
| Body | Archivo expanded 15 px | Archivo expanded 14 px, 0.04 em tracking; labels 0.1 em |
| Primary button | solid `#B8A689`, ink label | champagne gradient, ink label |
| Secondary button | transparent, `#B8A689` border, fills ink on hover | transparent, ink border, fills ink on hover, square |
| Text link | `#8B705B`, 12 px caps | `#8B705B`, 14 px, 0.1 em |
| Header | translucent, 88 px | white, 104 px, uppercase 12 px menu |
| Cart | ring icon in the header | 40 × 100 px champagne edge tab, count box (desktop; phone keeps the bottom bar's cart) |
| Wine band | flat `#F4F4F4` | the original mist gradient |
| Marquee | — | champagne band, seven words |
| Footer | content-width, light | full-bleed `#F4F4F4`, uppercase column heads; newsletter on a raised card with a champagne rule |
| Age gate | ring mark | sunburst mark on a grey card |
| Filter chips | pill, ink when active | square, champagne when active |

## What B deliberately does not copy (D22)

Measured contrast and size on the original:

| Original | Measured | B |
|---|---|---|
| White label on champagne | 2.4 : 1 at the dark end, 1.5 : 1 at the light end | ink label, 7.1 : 1 and 11.3 : 1 |
| White hero title on the taupe wash | 2.0 : 1 | ink title, 8.4 : 1 |
| `#B8A689` text link on white | 2.4 : 1 | `#8B705B`, 4.6 : 1 |
| Body copy | 11–12 px | 14 px |
| Four `h1` on the home page | — | one |

Fonts stay D3's free equivalents (the original's Didot and Akzidenz files are the estate's licensed TTFs). Bodoni Moda's optical-size axis, left on automatic, draws display hairlines so thin that capitals look detached on screen (found by looking, in the rendered headings: "TOK AJI", "MEGH ATÁROZÓ"); B caps the axis at 30. If the estate hands over its own font files and the licence allows web use, the change is the two font variables in `assets/tokens.css`.

## Verification (2026-10-02)

- **Rendered pages:** 12 page kinds (home, Birtok, Tokaji aszú, Látogatás, Borok, Borklub, two product pages, and EN home, Birtok, Borok, product) at 390, 768 and 1440 — 36 captures: no horizontal overflow, no console error, no failed request, no broken image, one `h1` each. Images were scrolled into view before capture (lazy images do not load otherwise). The home hero, interior hero, product page, card grids, footer and the age gate were looked at, not only measured.
- **Behaviour (headless browser):** age gate opens on a fresh session, shows the mark, closes and stays closed; mega panel opens on hover; the cart tab is fixed on the right edge at 40 × 100 px; language switch stays inside B in both directions; shop shows 32 products, filters, sorts by price monotonically, chip state is champagne; phone menu sheet opens and closes, bottom bar shows, edge tab hides; the marquee stops under reduced motion; no script errors.
- **Weight (first load, page and images, uncompressed):** home 414 → 432 kB on phone, 636 → 648 kB on desktop; product page 194 → 200 kB. External fonts are the same 149 kB in both.
- **Comparison page:** both frames load without the age gate (the page sets the session flag, as the presentation does), scale to fit, follow the page, language and device selections, scroll together by proportion, keep the position when switching between A and B, and open external links in a new tab; no horizontal overflow at 390 px.

## Not done

- **The live storefront (`customer.direct`, tenant `moonvalley`) shows A.** Porting B there means a second appearance preset and a second source root; it is a separate step, to be taken only if the client chooses B.
- **B is not pushed.** It exists in the working tree; the comparison page works against the published paths only after a push.
- **Two rock photographs (Úrágya, Kakasok) are still missing** from both variants; the slots say so.

## Regenerate

```
python3 holdvolgy/build.py          # A, then B
python3 holdvolgy/docs/build.py     # this page and the index
python3 holdvolgy/check.py          # must print GATE: CLEAN
```

After any change to B's layer, hash the A pages before and after; they must not move.
