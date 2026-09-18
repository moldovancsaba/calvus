# Holdvölgy 2026 — technical design

*The detail under `11-architecture.md`: how each prototype page becomes a theme template,
how `catalogue.json` maps onto WooCommerce, what the forms, club, gate, languages, images,
SEO and operations do. Everything here follows the PROPOSED stack (ADR-1..9); if a decision
flips, the affected section is rewritten. Written 2026-09-18.*

## 1. Theme structure — one template per prototype page kind

`build.py` renders seven page kinds; the theme has the same seven. The prototype's markup
is the acceptance reference (ADR-8): a template is done when its rendered HTML matches the
prototype's structure and the gate criteria (`10-ssot.md` §7) at 390 and 1440.

| Page kind | Prototype | Theme template | Editable by staff |
|---|---|---|---|
| Home | `index.html`, `en/index.html` | `front-page.html` — hero, three cards, wine rail, dűlő teaser, visit, news, newsletter as patterns | every text and image; rail picks products by line |
| Birtok | `birtok.html` | `page-birtok.html` — story, ten-step timeline, dűlők with map and rocks, varieties, vintages, team | timeline steps, team members as a repeatable block |
| Tokaji aszú | `aszu.html` | `page-aszu.html` — Culture wall (from products of line Culture, ordered by vintage), making, ageing, Time Capsule, PreCulture, heritage | wall is data-driven; the rest text/images |
| Látogatás | `latogatas.html` | `page-latogatas.html` — cellar numbers, history, tickets, Experience, Trezor, geology, practical info, booking form, guestbook | tickets as a repeatable block; form fields fixed (§5) |
| Borok | `borok.html` | `archive-product.html` — grid with filter Mind/Száraz/Édes/Aszú/Hold and Hollo (product taxonomy `type` + line), sort by collection or price, two-up on phones | products only |
| Product | `bor/<id>.html` (32) | `single-product.html` — §3 blocks | product fields |
| Borklub | `borklub.html` | `page-borklub.html` — benefits, four tiers, how it works | tiers from reward-points settings (§6), text editable |
| Shared | header, footer, age gate, banner | `parts/header.html` (mega-nav ≥ 1024), `parts/footer.html`, `parts/bottom-bar.html` (< 1024, bottom action bar + sheet), `parts/age-gate.html` | navigation items in one menu (R11) |

Not in the prototype and therefore **WooCommerce's own screens restyled, not redesigned**:
cart, checkout, order confirmation, my account, gift-card purchase. Restyling = the token
layer (`14-token-map.md`) and the button/field components; no new layouts.

Tablet 768–1023 uses the phone navigation and the desktop grids as `05-layout-specs.md`
resolves it; the theme carries the same breakpoints (`--hv-*` in `theme.json`).

## 2. Content model

| Content | Storage | Notes |
|---|---|---|
| Products | WooCommerce product (simple) + taxonomy `wine_type` {szaraz, edes, aszu, pezsgo} + taxonomy `wine_line` (10 lines) + product meta (§3) | one product per catalogue row; sizes are separate products as on the live site (Vision 2018 and Vision 2018 Magnum are two rows), not variations |
| Tickets (4) | a `ticket` block pattern on Látogatás with name, duration, price, description | not products — nothing is sold online (ADR-7) |
| Club tiers (4) | reward-points plugin configuration | §6 |
| Timeline steps, team members, heritage milestones, dűlők | repeatable blocks inside the page (patterns), text + image | no custom post types: each list lives on exactly one page and is edited there |
| Site copy (HU, EN) | page content per language (ADR-3) | the prototype's compiled strings in `build.py` are the initial import |
| Media | WordPress media library, uploaded from `assets/img/` derivatives with their `alt` from the prototype | source URLs in `assets-used.md` |

## 3. Product mapping — `catalogue.json` → WooCommerce

| Catalogue field | WooCommerce | Rule |
|---|---|---|
| `id` | product slug | **not** used as the public URL — the live slug is kept (§8); `id` is stored as SKU-like meta `hv_id` for traceability |
| `name` | product title | "Culture 2006" |
| `line` | taxonomy `wine_line` | one term per product |
| `type` | taxonomy `wine_type` | drives the Borok filter |
| `vintage` | meta `hv_vintage` (text) | may be empty |
| `size` | meta `hv_size` | `37,5 CL` etc., printed under the price |
| `price` | regular price (HUF, tax-inclusive as on the live shop) | `0` → product marked "price on request": no add-to-cart, *Érdeklődöm* mailto (as the prototype) |
| `variety`, `dulo` | meta `hv_variety`, `hv_dulo` | facts list |
| `cat` (hu/en) | short description, per language | "6 puttonyos tokaji aszú" |
| `tagline` (hu/en) | meta `hv_tagline`, per language | |
| `desc`, `tasting`, `vintage_note` (hu/en) | description + meta `hv_tasting`, `hv_vintage_note`, per language | rendered as the three tabs Kóstolási jegyzet · Az évjárat · Adatlap |
| `tech.*` | meta group `hv_tech` (11 keys, strings as printed) | Adatlap tab; absent on 1 product — tab hidden, not empty |
| `storage`, `serve_temp` (hu/en) | meta, per language | facts list |
| `render` | product image (WebP with alpha, R4) | one image per product; the same render for HU and EN |
| `live_url` | the product's current permalink | see §8 |

Import: a one-off WP-CLI/CSV import generated from `catalogue.json` by a script kept in
this repo (`data/export-woo.py`, to be written in M3) so the mapping is executable, not
prose. After import, WooCommerce is the source and the catalogue is retired.

Structured data: the prototype's Product/Offer JSON-LD is reproduced by the template
from the same fields (price, currency HUF, availability, image, sku = `hv_id`).

## 4. State machines

**Age gate**: `unknown → verified` (Igen; `sessionStorage hv-age=ok`, dialog closed for
the session) · `unknown → left` (Nem; navigate away). Rendered in every page's HTML,
`<dialog>` opened by script; no content hidden from crawlers.

**Booking request**: `submitted → received (e-mail + stored) → answered by staff`. The
site's only states are submit and confirmation; the rest is the estate's inbox.
Validation: required Név, E-mail, Borkóstoló, Dátum ≥ today, Vendégek száma ≥ 1, GDPR
checked; server-side; spam protection (honeypot + rate limit, no CAPTCHA that blocks
real guests).

**Order**: WooCommerce's (pending → processing → completed / cancelled / refunded);
untouched.

**Club membership**: `none → tier(5|10|15|20)` on reaching the threshold within a rolling
12 months; tier kept while spend in the window ≥ threshold; drops at window end
otherwise — implemented as reward-points rules (§6), verified with test orders on staging.

## 5. Forms

| Form | Fields | Goes to | Response |
|---|---|---|---|
| Booking request (Látogatás) | Név, E-mail, Telefon, Borkóstoló (4 programmes), Dátum, Vendégek száma, Üzenet, GDPR | e-mail to `visit@holdvolgy.com` (the address on the page) + stored entry | on-page confirmation "one working day" (the live copy); auto-reply |
| Newsletter (home, footer) | E-mail (+ GDPR) | Mailchimp for WooCommerce audience | double opt-in as Mailchimp does |
| Club sign-up | WooCommerce account creation | WooCommerce | tiers apply automatically |

Amelia: leave installed but inactive on the front end unless the estate decides to sell
timed slots (ADR-7). If it does, the booking block becomes Amelia's and this section is
rewritten.

## 6. Club tiers

Four tiers as configuration in the reward-points extension (the plugin the live site
already runs): threshold spend 50 000 / 150 000 / 300 000 / 600 000 Ft over a rolling 12
months → 5 / 10 / 15 / 20 % discount on every order, plus the two gift experiences at
first attainment of the 15 % and 20 % tiers (manual fulfilment by staff, triggered by an
order note). If the extension cannot express "rolling 12 months", the fallback is a
scheduled recalculation (daily cron) writing the tier to customer meta — recorded as a
decision if taken.

## 7. Languages

Polylang or WPML (ADR-3): HU as default at the root, EN under `/en/`, every page and
product paired; `hreflang` hu / en / x-default emitted per pair; language switcher in
header and sheet links the counterpart page (not the EN home). The initial EN content is
the prototype's — the estate's own EN copy from the live `/en/` pages. Product meta
fields marked translatable. The current EN URLs (`/en/…`, `/en/wine/…`) are kept or
redirected (§8).

## 8. URLs, redirects, SEO

- **Every live URL is kept** (R6). Product permalinks stay `/bor/<live-slug>` (the
  catalogue holds each `live_url`); pages stay `/birtok`, `/tokaji-aszu`, `/borkostolo`,
  `/bortrezor`, `/holdvolgy-experience`, `/holdvolgy-borklub`, `/shop`, `/en/…`. Where the
  prototype merged pages (Borkóstoló + Experience + Bortrezor into Látogatás), the old
  URLs 301 to the section anchor. The redirect map is a file in the theme repo, written
  before cutover and tested on staging with the link audit from `check.py`.
- Canonical per page; sitemap per language; `noindex` on cart/checkout/account;
  Product/Offer JSON-LD (§3); Organization + LocalBusiness JSON-LD on home and Látogatás
  (address, hours from the practical info block).
- Titles and descriptions: the prototype's per page, editable.

## 9. Analytics, consent, privacy

Consent banner (one plugin) before any marketing script; PixelYourSite fires only after
consent; first-party analytics (`independent-analytics`, no cookies) may run without —
the client decides whether GA4 is wanted at all. The 18+ gate is not consent and stores
nothing beyond the session flag. Privacy policy and terms pages kept at their URLs.

## 10. Images

Derivatives generated once from the estate's originals (`assets-used.md` lists source →
derivative sizes): WebP, alpha preserved for bottle renders (R4), `srcset` at 390 / 780 /
1440 widths, `width`/`height` attributes on every `<img>` with `height: auto` in the
base CSS (D16), `loading="lazy"` below the fold, hero preloaded. Home budget < 1,5 MB
measured with all derivatives in place (`06-home-build.md` has the prototype's number).

## 11. Performance

Targets and how they are met: origin TTFB < 800 ms by removing the builder and runtime
translation (no measurement exists for the new origin yet — M5 measures it); LiteSpeed
page cache kept, CDN in front (ADR-5), browser caching for static assets (today
`no-store` on everything); CSS = tokens + one theme stylesheet (< 40 KB, the prototype's
is the reference); JS = the age gate, the phone sheet, the shop filter — no framework;
fonts self-hosted WOFF2 with `font-display: swap`; third-party requests limited to
payment provider, Mailchimp, pixel-after-consent.

## 12. Operations

Staging on the same host; deploy = theme package + plugin list + config export;
production cutover after 15 January (ADR-9): redirect map live → theme switch → plugin
prune → cache purge and warm → link audit → measurements → monitoring green.
Rollback = switch theme back and re-enable plugins (data untouched). Backups daily,
restore tested once on staging. Monitoring: uptime check every minute, alert to a named
estate contact and the developer; PHP error log to the same channel.

## 13. Hand-off artefacts

The theme repository (outside this repo) receives: `assets/tokens.css` → `theme.json`
(`14-token-map.md`), the prototype's HTML per page kind as the markup reference, the
compiled copy from `build.py` as the initial content, `data/catalogue.json` and
`data/export-woo.py` for the product import, `assets-used.md` for the media, the
redirect map, and the gate criteria as the acceptance checklist.
