# Holdvölgy 2026 — single source of truth (SSOT)

*Definitions the other technical documents (`11`–`14`) use without redefining. Every entity
and enumeration below is read from what the prototype actually holds (`data/catalogue.json`,
`build.py`, the built pages) or from the live site audit (`02-brand-and-site-audit.md`).
Written 2026-09-18. Changes when a definition changes; the process log records when.*

## 1. Glossary

| Term | Meaning here |
|---|---|
| Birtok | The estate as a whole and the page that tells it: history, dűlők, geology, varieties, vintages, team. |
| Dűlő | A named vineyard site (cru) around Mád. The estate farms seven; the catalogue names four on wines: Becsek, Holdvölgy, Király, Nyulászó. |
| Parcella | A parcel within a dűlő; the estate has thirty. Not modelled per wine. |
| Line (collection) | The estate's naming of a wine family: Culture, Aszú Útkeresés, Signature, Eloquence, Intuition, Exaltation, Expression, Vision, Meditation, Hold and Hollo. A product belongs to exactly one line. |
| Type | The wine's commercial category: `szaraz` (dry), `edes` (sweet), `aszu` (Tokaji aszú), `pezsgo` (sparkling). |
| Aszú, puttonyos | Tokaji botrytised sweet wine; "6 puttonyos" is the traditional sweetness class. Culture is the estate's 6-puttonyos aszú line. |
| Culture wall | The vertical list of thirteen Culture vintages 2006–2018 with prices on the Tokaji aszú page. |
| PreCulture | A pre-order product (a future Culture vintage sold ahead). Listed; not purchasable in the prototype. |
| Trezor (Millennium Bortrezor) | Experiential programme: guests take part in a blend and receive a certificate. A page section and a ticket, not a product. |
| Ticket / programme | A visit product — a tasting or cellar programme with a price and duration. Four are listed on Látogatás; booking is a request, not a purchase. |
| Booking request | The form on Látogatás (Név, E-mail, Telefon, Borkóstoló, Dátum, Vendégek száma, Üzenet, GDPR). A message to the estate; no availability, no payment. |
| Borklub | The loyalty programme: four discount tiers earned by 12-month spend. |
| Age gate | The 18+ dialog shown before any page; "Nem" leaves the site. |
| Prototype banner | The one-line notice on every page that the cart and forms do not send. |
| Reference widths | 390 (phone) and 1440 (desktop); tablet 768–1023 resolved in `05-layout-specs.md`. |
| Gate | `python3 holdvolgy/check.py` plus the measured sweep (`11-gate-sweep.md`). Must print `GATE: CLEAN` before a push. |

## 2. Enumerations

| Enum | Values | Source |
|---|---|---|
| `product.type` | `szaraz` · `edes` · `aszu` · `pezsgo` | catalogue: 9 / 8 / 14 / 1 |
| `product.line` | Aszú Útkeresés · Culture · Eloquence · Exaltation · Expression · Hold and Hollo · Intuition · Meditation · Signature · Vision | catalogue |
| `product.size` | `37,5 CL` · `50 CL` · `75 CL` · `150 CL` | catalogue: 14 / 7 / 10 / 1 |
| `product.dulo` | `Becsek` · `Holdvölgy` · `Király` · `Nyulászó` · empty (blend or unspecified) | catalogue |
| Shop filter | Mind · Száraz · Édes · Aszú · Hold and Hollo | `borok.html` |
| Shop sort | by collection · by price | `borok.html` |
| Language | `hu` (primary, root) · `en` (`/en/`), `x-default` = hu | every page's `hreflang` |
| Club tier | 5 % @ 50 000 Ft · 10 % @ 150 000 Ft · 15 % @ 300 000 Ft · 20 % @ 600 000 Ft, each over 12 months | `borklub.html` |
| Ticket programme | the four programmes on Látogatás (names and prices as built) | `latogatas.html` |
| Page kind | home · birtok · aszu · latogatas · borok · product · borklub · redirect stub | `build.py` |

## 3. Canonical entities

The prototype has one data file. Everything else is content compiled into `build.py`.

**Product** (`data/catalogue.json`, 32 rows) — the only structured entity.

| Field | Type | Notes |
|---|---|---|
| `id` | slug | stable page name: `bor/<id>.html`, `en/bor/<id>.html` |
| `line`, `name`, `vintage`, `size` | text | `vintage` may be empty (non-vintage blends) |
| `price` | integer HUF | `0` means "price on request" (one product: `exaltation-2017-reserve`); rendered as *Ár egyeztetés alatt* |
| `type`, `variety`, `dulo` | enum / text | see §2 |
| `cat`, `tagline`, `desc`, `tasting`, `vintage_note`, `storage`, `serve_temp` | `{hu, en}` | client copy from the live HU and EN pages; EN may be empty where the live EN page has none |
| `tech` | object | `alkohol`, `cukor`, `sav`, `illo`, `so2`, `extrakt`, `fajta`, `alapbor`, `dulok`, `palack`, `besorolas` — strings as printed on the live sheet, present on 31 of 32 |
| `render` | asset key | bottle image under `assets/img/`, alpha preserved (D16) |
| `live_url` | URL | the live product page the data was read from |

**Entities the live site has and the prototype only presents** (defined here so the
architecture can name them; their data lives in the client's WooCommerce today):
Order, Cart, Customer, Club membership (tier, 12-month window, spend), Gift card,
Booking request, Newsletter subscription, Ticket.

**Page** — generated by `build.py` from compiled content + catalogue; HU and EN are two
renders of one source (D8). **Asset** — every image with its source URL and derivative
sizes in `assets-used.md`; alpha-preserving conversion is a rule (R4).

## 4. Settings the prototype fixes

| Setting | Value | Where |
|---|---|---|
| Currency, price format | HUF, `27 500 Ft`, thin-space thousands | `build.py` `_fmt` |
| Languages | hu root, en under `/en/` | `build.py` |
| Age gate | shown on every page until accepted; accept stored in `sessionStorage` (`hv-age`) | inline script in every page, from `build.py` |
| Navigation | five items: Birtok · Borok · Tokaji aszú · Látogatás · Borklub (D4); desktop mega-nav, phone bottom bar + sheet (D5) | single-sourced in `build.py` (D15) |
| Home weight budget | < 1,5 MB with real renders | plan §5 |
| Tap floor | 44 px | tokens `--hv-tap` |

## 5. Decision register

Decisions D1–D18 are in `04-decisions.md` (design and process). Technical decisions
made in this package are recorded as **ADRs in `11-architecture.md` §11**, all in
status PROPOSED until the owner or client flips them; the log entry that flips one goes
to `04-decisions.md` as the next D-number.

## 6. Rules register

Standing rules the prototype obeys and the production build must keep.

| # | Rule | Origin |
|---|---|---|
| R1 | Hospitality before shop in every CTA pair. | plan §4 |
| R2 | No fake availability: booking is a request, stock is not shown, prices are the estate's. | plan §5, D9 |
| R3 | One catalogue drives HU and EN; product pages are never hand-edited. | D8 |
| R4 | Image conversions keep alpha; `img { height: auto }` in base CSS; images in aspect-ratio boxes are absolutely bounded. | D16, D17 |
| R5 | Exactly one `h1` per page; every image has `alt`; `hreflang` hu / en / x-default on every page. | gate sweep |
| R6 | A published URL is never deleted; it redirects. | D14 |
| R7 | No AI-generated imagery. | D6 |
| R8 | 18+ gate before any content; "Nem" leaves the site. | live site, kept |
| R9 | Component class names are namespaced; the gate checks for collisions. | D18 |
| R10 | No stale-state phrase on any page; the prototype banner says only what is inert. | check.py |
| R11 | Navigation and document indexes are single-sourced. | D15 |

## 7. Metrics

| Metric | Target | Where measured |
|---|---|---|
| Server response (TTFB) | < 800 ms | client brief; measured in `11-architecture.md` §2 |
| Home page weight | < 1,5 MB | client brief; `06-home-build.md` |
| Front-end plugins | < 12 | client brief; live count in `11-architecture.md` §2 |
| Live alerting | exists, reaches a person | client brief; `13-implementation-plan.md` |
| Horizontal overflow at 390 / 1440 | 0 px | `11-gate-sweep.md` |
| Tap targets under 44 px | 0 | `11-gate-sweep.md` |
| Pages without one `h1`, `alt`, `hreflang` | 0 | `11-gate-sweep.md` |
| Console errors per page type | 0 | build logs |
| Business (for the estate, after go-live) | EN share of sessions (up 145 % per brief), shop conversion, booking requests per month, club sign-ups | not measured here — analytics in `12-technical-design.md` §9 |

## 8. Document map

| Document | Purpose | Changes when |
|---|---|---|
| `00-brief.md` | what it is, what is real, where it stands | status changes |
| `10-ssot.md` | this file | a definition changes |
| `11-architecture.md` | measured current state, target containers, NFRs, stack ADRs | an architectural decision changes |
| `12-technical-design.md` | templates, data mapping, forms, images, i18n, SEO, ops detail | a design detail changes |
| `13-implementation-plan.md` | milestones, issues with DoD, blocked register, risks | scope or sequencing changes |
| `14-token-map.md` | prototype tokens and components → production theme | a token or component changes |
| `00-plan.md`, `01`–`11`, `bemutato.html` | the customer side: research, audit, assets, decisions, design, builds, gate, presentation | see `README.md` |
