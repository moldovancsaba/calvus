# Variant B — built from today's holdvolgy.com

*Built 2026-10-02 for the first client meeting; rebuilt the same day after the owner compared the first version with the live site and found it inconsistent. Decisions D21–D23 (`04-decisions.md`). Client-facing comparison: `osszehasonlitas.html`.*

## Where the two variants stand

There are two variants of the new site, and **neither has been reviewed or accepted by the client**. The owner's gate approvals recorded in D10–D13 were internal.

| | A | B |
|---|---|---|
| In one line | **reimagined for 2027** | **built from today's site** — to make it faster, with a dedicated mobile experience and better usability |
| Structure | new: five menu items, card-based home | the live site's: eight menu items, the live home flow |
| Look | new design language on the estate's colours and photographs | the live site's own look: logo, banners, champagne gradient, caps, cart tab, footer |
| Content | shared | shared |
| Location | `holdvolgy/` | `holdvolgy/b/` |

Both are bilingual (76 pages each), carry the age gate, the product pages with full fact sheets and the shop filters, and have a separately designed phone experience (D5). Both say on every page that the cart and forms are inert.

## What B takes from the live site (read 2026-10-02, HU and EN)

| Element | On holdvolgy.com |
|---|---|
| Logo | `HV-web-logo.png` (226 × 32, sunburst mark and wordmark), 3.8 kB |
| Menu | HU, eight items: Birtok, Borok, Borkóstoló, Bortrezor, Tokaji aszú, Borklub, Experience, Kapcsolat. EN, seven: Estate, Wines, Wine-tasting, Tokaji aszú, Wine club, Experience, Contact |
| Hero | four slides, uppercase Didot title, small-caps line, ghost button: *Tokaji aszú előjegyzés / PreCulture 2025* (`HV_Preculture_Deskop.png`, phone `mobil.png`); *Év pincészete 2026* (`ev_pinceszet3-Facebook-Cover-3.png`, phone `…Instagram-Story-3.png` — a finished banner with the portrait, the grapes, the vines and the estate's seal); *Borkóstolóélmény ajándékba* (`IMG_4697-3-scaled.jpg`, phone `pincejarat_nagy_termek.png`); *Tokaji aszú / Az élet nagy pillanataihoz* |
| Home flow | wines carousel → Holdvölgy kezdetek / Több mint borászat (mist ground) → the tagline over the dark cellar → photo mosaic → Aktualitások (HU) → champagne marquee → Látogass meg minket → three contacts → footer |
| Buttons and surfaces | `linear-gradient(90deg, #B8A689 2.08%, #E0D2BB 31.97%, #BAA793 100%)`, 12 px caps with 1.2 px tracking, padding 12 × 30; ghost buttons on photographs; the grey "mist" gradient; `#F4F4F4` footer band |
| Cart | a 40 × 100 px champagne tab on the right edge, a count box above it |
| Footer | links, newsletter card, social list, address with the logo, payment logos |
| Text | every string on B's home page is the live site's, HU and EN (menu, slides, section titles, the "how it started" paragraph, visit block, the three contacts, footer) |

## How B is built

One generator, two passes. `python3 holdvolgy/build.py` runs `build_all("a")` and then `build_all("b")`.

- **A is untouched except its banner.** B is a stylesheet layer (`CSS_B`) over A's `CSS`, plus its own header, home page, footer and age-gate mark. A's 76 pages differ from before by exactly one line each, the banner (verified: 76 insertions, 76 deletions, no other line). The live storefront in `customer.direct` strips the banner by its class, so its text can change safely.
- **B is a closed tree.** Relative links never leave `b/` except to the shared `assets/`; B's hreflang points at B; every B page carries `noindex`, no A page does; each variant's banner says which version it is (A: "A változat — Holdvölgy, 2027-re újragondolva"; B: "B változat — a mai oldalból kiindulva: gyorsabban, külön mobilélménnyel"). `holdvolgy/check.py` enforces all of it; a negative test (a B page linking into A, a B page without `noindex`) failed the gate as it should, after fixing a prefix-match bug in the first version of the rule (`holdvolgy/borok.html` starts with the string `holdvolgy/b`).
- **Assets.** The six hero banners and the logo come from the live site's media library (the estate's own images); originals are not committed (D7). Converted to WebP in a headless browser, alpha kept (D16):

| File | Source (`holdvolgy.com/wp-content/uploads/…`) | Original | Derivative |
|---|---|---|---|
| `b-hero-preculture-1440.webp` | `2025/12/HV_Preculture_Deskop.png` | 1512 × 792, 968 kB | 1440 × 754, 41 kB |
| `b-hero-preculture-m.webp` | `2025/12/mobil.png` | 410 × 700, 252 kB | 410 × 700, 20 kB |
| `b-hero-ev-1440.webp` | `2026/09/ev_pinceszet3-Facebook-Cover-3.png` | 1640 × 924, 502 kB | 1440 × 811, 26 kB |
| `b-hero-ev-m.webp` | `2026/09/ev_pinceszet3-Instagram-Story-3.png` | 1080 × 1920, 496 kB | 780 × 1387, 29 kB |
| `b-hero-tasting-1440.webp` | `2024/07/IMG_4697-3-scaled.jpg` | 2560 × 1707, 975 kB | 1440 × 960, 196 kB |
| `b-hero-tasting-m.webp` | `2024/07/pincejarat_nagy_termek.png` | 599 × 630, 866 kB | 599 × 630, 93 kB |
| `hv-web-logo.png` | `2023/10/HV-web-logo.png` | 226 × 32, 3.8 kB | copied as is |

  The fourth slide and the mosaic reuse A's photographs (`hero-aszu-*`, the showroom, the building from above, the vineyard, the bottles, the vineyard hut); the age gate loads the existing `logo.svg` lazily.

## B against the live site

**Same:** logo; the menu labels and order (HU eight, EN seven) with a drop-down under Borok and Borkóstoló; the four hero slides, their images, texts, button labels and order; the home flow; the champagne gradient and every button shape; Didot-style uppercase titles and tracked small caps (free equivalents, D3); the edge cart tab; the marquee words; the contacts; the footer structure; the shop's underlined tabs and bare bottles with a small-caps name; the age gate. In B the hero slider also pauses on hover and focus, stops when the visitor asked for reduced motion, has real buttons for its dots, and its hidden slides are not focusable.

**Improved** (the point of B):

| | Live site (measured 2026-10-02) | B |
|---|---|---|
| Home, phone, first load, all bytes | 17.9 MB, 250 requests | 0.85 MB, 28 requests |
| Home, desktop | 19.7 MB, 247 requests | 1.10 MB, 29 requests |
| Product page, phone / desktop | 9.9 MB / 11.0 MB, about 200 requests | 0.35 MB, 13 requests |
| Phone | (not compared) | a designed phone experience: bottom bar (Foglalás · Borok · Kosár · Menü), the full menu in one tap, hero text placed below the banner imagery, 44 px touch targets, two-column shop |
| Main headings on the home page | four `h1` (HU and EN) | one |
| Shop | underlined tabs, no prices in the grid | tabs working in place as filters (Mind, Száraz, Édes, Aszú, Hold and Hollo), price sort, the price under each bottle |

**Not carried:** the Aktualitások blog feed (a CMS feature); the payment logos (the cart is inert); the search and account icons (nothing to put behind them in a static prototype); the announcement strip; the gift boxes, gift bags and tasting tickets that the live shop sells as products (B shows the tastings on the Látogatás page). HU pages that exist only on the live site (partners, shipping and payment, terms, privacy, company details, newsletter) link to the live site in a new tab.

## Where B deliberately differs from the live site (D22)

Measured on the live site:

| Live | Measured | B |
|---|---|---|
| White label on the champagne gradient | 2.4 : 1 at the dark end, 1.5 : 1 at the light end | ink label, 7.1 : 1 and 11.3 : 1 |
| White title on the light banners (*Tokaji aszú előjegyzés*, *Év pincészete*) | 2.0 : 1 | ink title, 8.4 : 1 (titles on the photographic slides stay white, with a veil) |
| `#B8A689` text link on white | 2.4 : 1 | `#8B705B`, 4.6 : 1 |
| Body copy | 11–12 px | 14 px |
| English marquee | "Principals" | "Principles" |

Fonts stay D3's free equivalents (the live Didot and Akzidenz are the estate's licensed TTFs); if the estate hands over its font files and the licence allows web use, the change is the two font variables in `assets/tokens.css`. Bodoni Moda's optical size is capped at 30: left on automatic, its display hairlines are so thin that capitals look detached on screen.

## Verification (2026-10-02)

- **Rendered pages:** 12 page kinds (home, Birtok, Tokaji aszú, Látogatás, Borok, Borklub, two product pages, and EN home, Birtok, Borok, product) at 390, 768, 1100 and 1440 — 48 captures, no horizontal overflow, no console error, no failed request, no broken image, one `h1`. Images were scrolled into view before capture. Home, all four hero slides (desktop and phone), the shop, the footer and the age gate were looked at, side by side with the live pages, not only measured. The menu was checked at 1024, 1060, 1099, 1100, 1180, 1280, 1440 and 1920 px: full menu from 1100, the compact bar-and-sheet pattern below.
- **Behaviour (headless browser, 35 checks):** age gate; mega panel; cart tab geometry; language switch inside B both ways; the live menu labels and order in HU and EN; slider dots, autoplay after about 6.5 s, hidden slides unfocusable, no autoplay under reduced motion; carousel arrows and its live order; shop filters, price sort, tab styling; phone: bottom bar, hero text below the imagery, menu sheet with all eight items; footer links open in a new tab and none is a `#` placeholder; no script errors.
- **Weight:** table above; first load, no cache, every response including the external fonts (149 kB). Measured the same way on the live site and on A and B (A: 0.57 MB phone / 0.77 MB desktop, 19 / 24 requests).

## The live site, re-read, and what it changed in the data (2026-10-02)

The owner found inconsistencies between B and the live site, so every statement the project makes about the live site was re-checked against it that day. Results:

- **Still true:** four `h1` on the home page (HU and EN); three generated images on the Borkóstoló and Experience pages; Exaltation 2017 Reserve priced at 0 Ft; the harvest date "2012. Október" is a default on 28 of 32 product pages.
- **No longer true, corrected in the client documents:** the live product pages now carry a full fact sheet (30 of 32) — the audit of 2026-09-16 said they carried none; only one product URL returned 404 (not two), and that was our own stale link; the English Vision 2021 page is in English; the live home page is 17.9 MB on a phone (the 8.8 MB in the client's technical brief of 2026-09-08 and the audit is out of date).
- **Our product data had drifted from the live shop in two ways, both fixed in `data/catalogue.json` (`refreshed`: 2026-10-02):**
  1. *Hold and Hollo Dry* is now the **2025** vintage on the live shop: price 4 350 Ft (was 4 000), analysis values 13,5 % / 8,6 g/l / 7 g/l / 17 014 bottles, a new tasting note, a new English category. The product keeps its id and URL (`bor/hold-and-hollo-dry-2024.html`) because a published URL is never moved (D14); the name, vintage, price, live link and the home page's bottle band say 2025.
  2. *Raw page text in 14 products' text fields* (labels such as "borleírás tárolás és fogyasztás", the description repeated, "TASTING NOTES.", a trailing "READ THE FULL VINTAGE REPORT", a stray "FACT SHEET", and "TÁROLÁS … Szüret 2012. Október …" shown as the vintage note of the three Hold and Hollo products). Descriptions, tasting notes and vintage notes were re-read from the live pages with a parser that agreed with 95 of the 97 values already clean; the English tasting and vintage text of Vision 2021 (which differed from the live page) was replaced; Exaltation 2018's grape field lost a swallowed label. The product template now omits an empty "Az évjárat" column instead of printing its heading alone.
- **The `moonvalley` tenant in `customer.direct` still holds the old Hold and Hollo Dry values** (2024, 4 000 Ft); that is managed in its admin or by re-running its import.
- **A defect found in A by a width sweep, fixed the same day.** Sweeping every page from 360 to 1920 px, A overflowed horizontally on narrow laptop windows, and had since the first build: the header by up to 32 px between 1024 and 1056 px, the home page's visit block by up to 118 px between 1024 and 1150 px (it also overflowed in the published version). A rule that applies only from 1024 to 1239 px fixes both; the phone and the 1440 layouts are unchanged. B's timeline got three columns from 1024 to 1199 px for the same reason. After the fix no page of either variant, nor the presentation or the comparison page, overflows at any width from 360 to 1920 px.
- **Effect on A:** its banner (76 pages), the narrow-window rule (in every A page's stylesheet), and the refreshed content on 28 pages (24 product pages, both shop lists, both home pages' bottle band). Nothing in A's design at phone or desktop size changed.

## Not done

- **The live storefront (`customer.direct`, tenant `moonvalley`) shows A.** Porting B there is a separate step, to be taken only if the client chooses B.
- **Two rock photographs (Úrágya, Kakasok) are still missing** from both variants; the slots say so.
- **The estate's own font files** are not in either variant.

## Regenerate

```
python3 holdvolgy/build.py          # A, then B
python3 holdvolgy/docs/build.py     # this page and the index
python3 holdvolgy/check.py          # must print GATE: CLEAN
```

After any change to B's layer, hash the A pages before and after; they must not move.
