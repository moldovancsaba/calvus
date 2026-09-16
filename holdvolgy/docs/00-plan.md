# Holdvölgy 2026 — research findings and implementation plan

Written 2026-09-16, before any second build. Part of the documentation set in `holdvolgy/docs/` — see `README.md` there for the index and process log. The first prototype (commit `8342956`) is
withdrawn as a design direction: it used a dark ground, a saturated gold accent and a
serif display face — none of which come from the Holdvölgy brand or from the wine
world's best sites. Everything below is what was actually measured or read.

## 1. What the benchmark sites do

Sites read directly (homepage plus what the fetcher could reach): Château Margaux,
Krug, Château d'Yquem, Château Suduiraut, Château Smith Haut Lafitte (FR); Opus One,
Stag's Leap Wine Cellars, Jordan (Napa/Sonoma); Catena Zapata (AR); IXSIR (LB);
Antinori, Tenuta San Guido (IT); Penfolds (AU); Bodega Garzón (UY); VIK (CL);
Klein Constantia (ZA); Royal Tokaji, Disznókő, Barta (Tokaj/Mád); Zorah (AM,
Awwwards HM); Pasqua (IT, Awwwards Site of the Month). Also the World's 50 Best
Vineyards 2025 list and the Awwwards wine gallery.

Unreachable from this environment and therefore not claimed: Château Musar and
Schloss Johannisberg (age gate blocks the fetcher), Vega Sicilia, Oremus, Egon Müller,
Château Climens, Dönnhoff, Château Héritage, Château Ksara, Szepsy (cert/TLS/empty).

### 1.1 Ground and colour — 13 light, 1 dark

Every Old World reference and every hospitality-led estate sits on a white or cream
ground with dark type: Margaux, Krug, Yquem, Suduiraut, Smith Haut Lafitte, Opus One,
Stag's Leap, Jordan, Antinori, San Guido, Penfolds, Garzón, Klein Constantia, Royal
Tokaji, Disznókő, Barta, IXSIR, Zorah. Accent colour is carried by photography, not by
CSS — "earth tones emerge through photography rather than bold digital colors"
(Zorah), "no aggressive accent colors compete for attention" (Smith Haut Lafitte).
The single dark-ground site is VIK (#1 on the 50 Best list), which is a hotel-and-art
estate with titanium-gold architecture to justify it.

Conclusion: the dark-cellar-and-gold treatment is the exception, and it belongs to a
brand that isn't Holdvölgy.

### 1.2 Typography — sans body everywhere, serif only as accent

Antinori, Disznókő, Penfolds, Garzón, Catena, Smith Haut Lafitte, Stag's Leap, IXSIR,
VIK: sans-serif throughout. Krug and Pasqua: sans body with an italic serif used as
punctuation ("HOUSE OF THE _UNCONVENTIONAL_"). Jordan and Royal Tokaji: serif reserved
for the wordmark. Nobody sets running text or cards in a serif.

### 1.3 How they sell — three distinct models, and Holdvölgy is in the third

1. **No transaction at all** — Margaux, Yquem, Krug, San Guido, Suduiraut, Catena,
   Royal Tokaji, Disznókő, Zorah. First growths and allocation houses: "Find a
   retailer", trade extranet, visits. Prices never shown.
2. **Allocation / membership gate** — Opus One ("Acquire our wines", no prices),
   Stag's Leap (four membership tiers, prices behind login), VIK (R.E.D. Society),
   Jordan (mailing list = 3 000 reward points). Scarcity as the mechanism.
3. **Open DTC with prices** — Penfolds (RRP on every card, 6-packs, badges "LIMITED
   EDITION / 100 POINT", filters by type/varietal/region/occasion, gift guide, member
   pricing), Garzón ("Online bottle price from $U 9860"), Barta (free delivery over
   15 000 Ft on the hero), Klein Constantia (shop + tasting room + club).

Holdvölgy already sells openly with prices, a loyalty programme (5–20 % at
50k/150k/300k Ft annual spend, 12-month tiers, quarterly offers, limited reserves),
gift cards from 6 500 Ft, a pre-order product (PreCulture) and an experiential
programme (Trezor: guests take part in the blend and receive a certificate). That is
the Penfolds/Garzón model with an Opus-One-style allocation layer on top. The site
should be designed as a **shop-and-hospitality estate**, not as a first growth
pretending prices don't exist. In Tokaj this is also a genuine differentiator:
neither Royal Tokaji nor Disznókő sells online.

### 1.4 Navigation — the same five words

Across the set the top level is some ordering of: Estate · Wines · Visit/Experiences ·
Club/Membership · Contact, with Shop as a persistent button. Nobody exceeds seven
items. Holdvölgy's current header has eleven plus a mega-menu duplicate.

### 1.5 Storytelling devices that recur

- A single sentence over the hero photograph: "Praise the balance in life" (SHL),
  "A unique terroir / Unparalleled surroundings" (Garzón), "The wine of kings and the
  king of wines" (Disznókő). Never a paragraph.
- Named vineyards as first-class objects: FAY and S.L.V. (Stag's Leap), Adrianna
  (Catena), six mapped sites with soil and altitude (IXSIR), Öreg Király and Kővágó
  (Barta). Holdvölgy has seven named dűlők **and a rock photograph for each** — no
  benchmark site has that asset.
- A founding number: 1843 (Krug), 1855 (Margaux, Suduiraut), 1976 (Stag's Leap),
  26 generations (Antinori), 1 800 m (IXSIR), 6 000 years (Zorah). Holdvölgy's are
  1,8 km / 3 szint / 500 év — already on the tasting page, badly duplicated (each
  appears twice in the DOM).
- Vintage as narrative: "The story of a year" (Krug), 2023 microsite (Yquem),
  Culture 2006–2018 vertical (Holdvölgy already lists thirteen vintages with prices,
  and PreCulture is an en-primeur programme like Yquem's). Nobody else in Tokaj
  presents a vertical.
- Provenance: Krug iD (app per bottle), VIK "Authentication". Holdvölgy's Trezor
  certificate and Time Capsule ("Kóstold vissza életed nagy pillanatait") are the
  same idea and are already written.
- Hospitality-first CTAs: "Book a visit", "Reserve your seat", "Secure a reservation"
  — always above "Shop".

### 1.6 Award galleries are not a reliable source

Of the Awwwards wine listings, Post Familiar (Site of the Day 2024) no longer
resolves and Bijou (HM 2025) is a parked domain. Pasqua's award site is a loading
screen with "START THE EXPERIENCE". The estates that endure are the ones on the 50
Best list, and their sites are quiet.

## 2. What Holdvölgy actually is (measured from the live site)

**Palette (Elementor kit 16):** primary `#B8A689` warm greige, secondary `#1D1D1B`
near-black, text `#666666`, grounds `#FFFFFF` / `#FAFAFA` / `#F4F4F4` / `#D9D9D9`,
supporting `#BAA793`, `#8B705B` brown, `#9B9796` grey. **Light ground, muted
champagne-greige accent, no saturated gold.**

**Type:** Akzidenz-Grotesk BQ Extended for everything (196 declarations) with Didot
on h1–h6 (kit-level rule). A wide grotesque plus a high-contrast Didone wordmark — a
distinctive, defensible pairing that the benchmark pattern supports (sans body,
serif as accent). The first prototype used neither.

**Language:** HU primary, EN full mirror including shop (`/en/shop`, "EN PRIMEUR",
"MUSCAT BLANC À PETITS GRAINS"). Per the technical brief EN visitors are up 145 %
this year. EN is a primary surface.

**Current page architecture (heading order as rendered):**
- Home: four competing `h1`s (Év pincészete / Ajándék / Tokaji aszú / Előjegyzés),
  then ten wine-category `h2`s, then Kezdetek, tagline, news, visit, team, newsletter.
- Birtok: foundations → ten-step timeline (1998–2019, each an illustrated card) →
  gallery → dűlők and terroir → rocks → varieties → vintages 2021–2025 → team (9
  people).
- Tokaji aszú: Culture → making → ageing → Time Capsule (eight life moments) →
  gift → guarantee → Culture vintages → PreCulture → Tokaj heritage (eleven dated
  milestones from Vitis Tokaiensis to the first Holdvölgy vintage).
- Borkóstoló: "Borkóstoló a föld alatt" → 1,8 km / 3 szint / 500 év → cellar
  history (seven milestones) → tickets (three programmes) → Experience → geology
  ("10 millió éves vulkáni nyomok") → visit info → guestbook.
- Shop: categories = Borválogatások · Culture · Édes · Száraz és félszáraz · Hold
  and Hollo · Díszdobozok. Culture page lists 13 vintages 2006–2018 (27 500 → 67 000 Ft
  on the vintage list; 133 000 Ft also appears on the page).

**Product pages are thin.** `/bor/szaraz-valogatas-vision` has 1 705 characters of
visible text, of which the product-specific part is the name, three vintages and
prices. No tasting note, no dűlő, no alcohol/sugar/acid, no serving temperature, no
award, no pairing. The category *names* carry the information ("TOKAJI SZÁRAZ
FURMINT, KIRÁLY") — the pages don't.

**Booking is a contact form**, not a booking engine: Név, E-mail, Telefonszám,
Borkóstolók (select), Dátum, Vendégek száma, Üzenet, GDPR. No availability, no
payment. The technical brief's "foglalási rendszer" is this form.

**Three AI-generated images are live** on Borkóstoló and Experience
(`ChatGPT-Image-2026.-apr.-27…png`). Given the brief and the owner's instruction,
these must not be carried into the prototype; real photography replaces them.

## 3. Asset inventory (180 unique base images on the crawled pages)

Nothing has been downloaded. Sizes and formats were read from HTTP headers and the
first 33 bytes of each file.

| Group | Count / spec | Use in prototype |
|---|---|---|
| Bottle renders `HV_<Line>_<yy>-NEW-1347x1347[_DIJ].png` | 40, 1347², **RGBA transparent**, ~290 KB each | Every product card and hero; sit on the greige ground with a soft shadow. `_DIJ` = award-badge variant. |
| Culture vertical 2006–2018 | 13 of the above | The vintage wall on the Aszú page |
| PreCulture barrel/bottle per year 2018–2025 | 8, 1347² RGBA | En-primeur timeline |
| Hold and Hollo Dry / Sweet / Uppp | 3, 1347² RGBA | Entry line |
| Tasting-programme mockups | 4 (2022) + 5 icons (600²) | Ticket cards |
| Cellar photography `hv-pince-hero.jpg` (521 KB), `hv_pincerendszer_pincealagut_lepcsovel_4-3.jpg`, `…trezor_uvegtabla…`, `Aszu_Landing_11-1.jpg` | JPEG | Page heroes — the single sentence over a photograph |
| Vineyard photography `hv_ke_szolo_dulok_furmint…holdvolgy_dulo_5_2018`, `dulok_becsek_dulo_latvany`, `hv_ke_hangulat_bebujik_a_nap`, `2021_riport_koverszolo` | JPEG | Dűlő section, EN home |
| Founder `pascal_founder_2.jpg` | 22 KB (small) | Estate story — ask for a larger file |
| Rock photographs `MVW_HV_kozet_*` | 7, 1400² RGBA, ~1 MB each | One per dűlő — the asset nobody else has. Must be converted to WebP/AVIF; at 1 MB each they'd blow the 1,5 MB page budget on their own. |
| Vineyard map `hv_dulok_birtok.png` | 2000×1180 RGBA | Dűlő overview |
| Timeline cards `*_birtok-413.png`, cellar history `*_pince_honlap.png` | 413×462 RGBA | Illustrated cards, only usable at ≤ 413 px — fine for a card strip, not for heroes |
| `aszusodas_folyamata-1.png` | not a PNG despite the name (462 KB) | Aszú process diagram — inspect before use |
| Logos `HV-web-logo.png`, `hv-megamenu-logo.svg`, `LOGO2.svg` | SVG available | Header |
| AI-generated (3) | — | **Excluded** |

Gaps to request from the client: a large founder portrait, team portraits (nine
names, no images on the crawled pages), a horizontal cellar photograph for mobile
heroes, the aszú process diagram as a real PNG/SVG.

## 4. Design direction — derived, not chosen

1. **Light ground, their palette.** `#FAFAFA` page, `#FFFFFF` cards, `#1D1D1B`
   type, `#B8A689` as the only accent, `#8B705B` for hover. No gold, no dark
   sections.
2. **Their type, in free faces.** Owner decision 2026-09-16: commercially free
   web fonts only, Google Fonts preferred. The live site's pairing (Akzidenz-Grotesk
   BQ Extended + Didot) is therefore reproduced with **Archivo** at width 112–125
   (variable `wdth` axis) for nav, body, cards and prices, and **Bodoni Moda**
   (variable optical size) for h1/h2 and the wordmark, and for nothing else. Both
   are SIL OFL. Fallbacks `"Helvetica Neue", Arial, sans-serif` and
   `Didot, "Bodoni 72", serif`. See `04-decisions.md` D3.
3. **Photograph + one sentence** heroes, per §1.5. Existing copy already has the
   sentences: "A tokaji álmot töltjük pohárba az élet nagy pillanataihoz" (home),
   "Borkóstoló a föld alatt" (tasting), "A gondolatok bora" (estate).
4. **Bottles on the ground colour, never on a coloured panel.** The renders are
   transparent; treat them as objects (Penfolds' isolated-bottle grid is the
   reference, with Holdvölgy's greige instead of white).
5. **Seven dűlők, seven rocks.** A section no competitor can copy: the vineyard map
   with each rock photograph, soil, exposure, varieties (the Birtok page already has
   "Telepítések · Expozíció · Kőzet · Fajták" per dűlő).
6. **Culture vertical as a wall**, 2006 → 2018, each vintage a bottle and a price;
   PreCulture as the en-primeur row beneath it. This is Yquem's vintage microsite
   idea with Holdvölgy's own catalogue.
7. **Five-item navigation**: Birtok · Borok · Látogatás · Borklub · Kapcsolat, with
   Foglalás as the button and the cart icon. Everything else (Aszú, Trezor, Ajándék,
   Experience) lives one level down.
8. **Hospitality before shop** in every CTA pair, per the benchmarks.
9. **One `h1` per page**; the four competing hero blocks on the current home become
   one hero and three cards.
10. **Product pages carry the content** they currently lack: dűlő, variety, vintage,
    residual sugar / alcohol where the client provides it, serving, awards (the
    `_DIJ` renders exist because awards exist), pairing, "Kóstold a birtokon".
11. **Two experiences, not one layout that reflows.** Desktop and phone are designed
    separately, each at its own reference size (1440 and 390), and tablet is a
    resolved third state rather than whatever falls out in between.
    - *Desktop is the editorial estate*: wide photography, the dűlő map with the
      seven rocks laid out spatially, the Culture vertical as a single row of
      thirteen bottles, a visible mega-navigation, hover states, a four-up product
      grid of isolated bottles. It exists to make the estate felt.
    - *Phone is a hospitality-and-buying tool*: the technical brief records that
      more than half of gifting-season purchases happen on mobile. Booking, shop,
      club and cart reachable in two taps from anywhere via a persistent bottom
      action bar; the vertical becomes a swipeable rail; the dűlők a stack with the
      rock as the card image; the product grid two-up; the story sections
      shortened to their sentence and a "tovább". It exists to let someone book or
      buy in the car park at Mád.
    - Photography is art-directed per device with `<picture>` and `media`, not
      scaled: a landscape cellar frame for desktop and a separately cropped
      portrait frame for phone. This is why the asset gaps in §3 ask for both.
    - Navigation is two systems (mega-nav; bottom bar plus sheet), not one menu
      collapsed behind a hamburger.

## 5. Implementation plan

Constraints: static HTML, no build step; two languages; the 1,5 MB home-page and
one-`h1` targets from the technical brief are adopted as the prototype's own gate;
mobile-first with the 44 px floor and zero horizontal overflow already established
in this repo.

### Phase 0 — approval (this document)
Owner confirms the direction in §4 and the page list below. Nothing is built before.

### Phase 1 — foundation (one commit)
- `holdvolgy/assets/tokens.css` with the kit-16 palette and the two type families.
- Two layout specs before any page: desktop at 1440 and phone at 390, each with its
  own navigation system, hero framing and grid, per §4.11; tablet resolved
  explicitly.
- Shared header/footer markup — mega-nav for desktop, bottom action bar plus sheet
  for phone — and the age gate restyled on the light ground.
- Home rebuilt: one hero (cellar photograph + tagline), three cards (Év pincészete,
  Borkóstoló, PreCulture), wine lines strip with bottle renders, dűlő teaser, visit,
  newsletter. Home weight measured against 1,5 MB with the real renders in place.

### Phase 2 — the pages that carry the estate (one commit each)
- **Birtok**: story, ten-step timeline with the illustrated cards, seven dűlők with
  rocks and map, varieties, team (placeholders until portraits arrive).
- **Tokaji aszú**: Culture vertical wall, aszú making/ageing, Time Capsule, PreCulture
  en-primeur row.
- **Látogatás**: 1,8 km / 3 szint / 500 év, cellar history, three tickets with the
  mockups, Experience, Trezor, geology, practical info, booking form modelled on the
  current fields (it stays a request form — no fake availability).

### Phase 3 — commerce
- **Borok** grid with the 40 renders, filters Száraz / Édes / Aszú / Hold and Hollo /
  Válogatások, sort by price, two-up on phones.
- **Product page template** per §4.10, driven from one JSON catalogue file so HU
  and EN share data.
- **Borklub** page with the real tiers and rules.

### Phase 4 — English
- `holdvolgy/en/` mirror of every page from the same JSON, `hreflang` pairs with
  `x-default`, EN copy taken from the live `/en/` pages where it exists.

### Phase 5 — gate and hand-off
- Per-page measurement run **twice, as two checklists**: desktop at 1440 (weight,
  requests, `h1` count, alt coverage, hover/focus states, console) and phone at 390
  (weight with the phone-cropped images, tap targets, overflow, two-tap reach of
  Foglalás / Borok / Kosár, console); Product/Offer JSON-LD on product pages.
- SOURCES note listing every asset URL used and every gap still open.

Each phase ends with the Rule-2 gate and a live verification, as with the other
projects in this repo.

## 6. What needs the client

Large founder and team portraits; the aszú process diagram as a real image;
technical data per wine (residual sugar, alcohol, acidity) — owner confirmed
2026-09-16 that item data will be supplied; confirmation of the Culture 133 000 Ft
item (which vintage/format); whether EN copy should be carried verbatim from the
live site. The webfont question is closed (D3).
