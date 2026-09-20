# Holdvölgy 2026 — architecture

*How the prototype becomes the live site. §2 is measured, not assumed. The stack in §10 and
the ADRs in §11 are **PROPOSED** — recommended with reasons, decided by nobody yet. Terms
are defined in `10-ssot.md`. Written 2026-09-18.*

## 1. System context

| Actor | What they do with the site |
|---|---|
| Visitor (HU, EN) | reads the estate, the wines, the visit programmes; passes the 18+ gate |
| Buyer | browses the shop, buys wine and gift cards, reorders; may be a club member with a tier discount |
| Guest | sends a booking request for a tasting or cellar programme |
| Estate staff | edits content and prices, answers booking requests, fulfils orders, runs the club and the newsletter |
| Incumbent developer (KM Építő / kiszervezettmarketing.hu, per the live `generator` tag) | maintains the current WordPress; has a priced offer for the rebuild |
| The studio | designed and built the prototype; wrote this package |

External systems the live site already talks to: WooCommerce payment and shipping
providers (not identified from the front end), Mailchimp (newsletter, `mailchimp-for-
woocommerce`), Facebook/Meta pixel (`pixelyoursite`), Google Fonts, an analytics
plugin (`independent-analytics`, first-party), Amelia (booking plugin present but the
booking is a contact form — audit §2).

## 2. The live site, measured (2026-09-18, `curl`, from this environment)

| Measure | Value | Target |
|---|---|---|
| Platform | WordPress; theme `hello-elementor` + child `hello-theme-child-master`; Elementor 4.1.4 + Elementor Pro; page builder on every page | — |
| Commerce | WooCommerce + 8 extensions: side-cart-premium, bought-together, reward-points, one-click-order-reorder, ultimate-gift-card, variation-swatches, tm-extra-product-options, flexible-shipping | — |
| Languages | TranslatePress (runtime translation of one HU content tree into `/en/`) | — |
| Distinct plugins referenced on home + shop front end | **23** (list in §2.1) | **< 12** |
| Home HTML alone | **624 KB**; 79 `<script src>`, 76 stylesheets, 30 `<img>` | whole page **< 1,5 MB** |
| Home, whole page | **8,8 MB, 226 requests** (client's technical brief, 2026-09-08); the prototype's home measures 600–734 KB (`06-home-build.md`) | **< 1,5 MB** ✗ |
| Shop HTML alone | 887 KB | |
| TTFB, cached (`x-litespeed-cache: hit`) | HU 0,06 s · EN 0,06 s (three runs each) | **< 800 ms** ✓ |
| TTFB, cache miss | EN **4,49 s** (one cold hit) | **< 800 ms** ✗ |
| Cache policy sent to browsers | `cache-control: no-store, no-cache, must-revalidate` — the LiteSpeed page cache serves hits, browsers re-fetch everything | |
| Security headers | HSTS, `x-frame-options`, `x-content-type-options` present | |
| Alerting | none visible from outside; brief says none exists | **exists** |

**2.1 The 23 plugins.** agile-store-locator · ameliabooking · dynamic-content-for-
elementor · elementor · elementor-pro · flexible-shipping · independent-analytics ·
mailchimp-for-woocommerce · marquee-addons-for-elementor · one-click-order-reorder ·
pixelyoursite · sassy-social-share · smart-wishlist-for-more-convert · the-plus-addons-
for-elementor-page-builder · theplus_elementor_addon · translatepress-multilingual ·
woo-bought-together · woo-variation-swatches · woocommerce · woocommerce-reward-points ·
woocommerce-side-cart-premium · woocommerce-tm-extra-product-options · woocommerce-
ultimate-gift-card. (Referenced from the front end; the installed count may be higher.)

**Reading.** The 800 ms target is met by the page cache and missed by the origin: every
content edit or cache purge exposes a multi-second render, and the EN tree is produced at
request time by TranslatePress. The plugin target cannot be met while Elementor and its
four add-ons (7 of 23) build the pages. The weight target is decided by HTML and CSS/JS
count before any image is loaded. All three targets point at the same change: take the
page builder out of the rendering path.

## 3. Quality attributes

| Attribute | Requirement | Verified by |
|---|---|---|
| Performance | TTFB < 800 ms **at the origin** (cache miss), home < 1,5 MB, LCP under 2,5 s on 4G phone | `13` M5, WebPageTest / Lighthouse on staging |
| Plugin budget | < 12 active plugins serving the front end | `13` M5, plugin list in §10 |
| Availability | uptime monitor with alerting to a named person; error alerting from WordPress | `13` M0 |
| Accessibility | one `h1`, `alt` on every image, 44 px tap targets, no horizontal overflow at 390, visible focus, `dialog` age gate keyboard-operable | gate sweep criteria carried to staging |
| SEO | `hreflang` hu/en/x-default, canonical, Product/Offer JSON-LD, every current URL kept or 301'd (R6) | `12` §8 |
| Privacy | GDPR consent for marketing pixels; 18+ gate; no tracking before consent | `12` §9 |
| Bilingual parity | every page and product exists in EN with the estate's own copy | R3 |
| Change freeze | no production change 15 Oct – 15 Jan; staging work allowed (assumption A1) | `13` |
| Maintainability | estate staff edit content, prices and products without a developer; theme has no page builder dependency | `12` §2 |

## 4. Target containers (PROPOSED)

```
                 ┌──────────────── CDN / edge cache (Cloudflare or host CDN) ────────────────┐
browser ───────▶ │  full-page cache for anonymous HU and EN pages; images; fonts               │
                 └───────────────────────────────┬────────────────────────────────────────────┘
                                                 │ miss
                 ┌───────────────────────────────▼────────────────────────────────────────────┐
                 │  WordPress (LiteSpeed host as today)                                        │
                 │  ┌─────────────────────────┐  ┌──────────────────────────────────────────┐ │
                 │  │ theme "holdvolgy-2026"  │  │ WooCommerce core                          │ │
                 │  │ block theme from the    │  │ products = catalogue.json rows            │ │
                 │  │ prototype: tokens.css,  │  │ orders, customers, gift cards, reward     │ │
                 │  │ templates = build.py    │  │ points (club tiers), shipping, payment    │ │
                 │  │ page kinds, no builder  │  └──────────────────────────────────────────┘ │
                 │  └─────────────────────────┘  multilingual: one plugin, stored translations │
                 │  forms (booking request, newsletter) · SEO · consent · cache plugin          │
                 └───────────────┬───────────────────────────┬─────────────────┬──────────────┘
                                 │                           │                 │
                        payment / shipping           Mailchimp          uptime + error
                        providers (as today)                            alerting → person
```

Containers: **theme** (rendering, all markup and CSS from the prototype), **WooCommerce**
(everything transactional, unchanged data), **multilingual plugin** (stored per-language
content, not runtime translation), **forms** (booking request to e-mail + WP entry;
newsletter to Mailchimp), **cache + CDN**, **monitoring**.

## 5. Key flows

1. **Browse → product → cart → checkout** — theme renders the Borok grid and product
   template from WooCommerce data; cart and checkout are WooCommerce's own screens
   restyled with the tokens (not redesigned; the prototype has no checkout).
2. **Booking request** — Látogatás form posts to WordPress; e-mail to the estate;
   entry stored; auto-reply "one working day"; no availability (R2). Amelia stays
   installed only if the estate wants calendar availability later (`12` §5).
3. **Club** — spend over 12 months sets the tier; discount applied at checkout;
   the four tiers and thresholds are configuration, not code (`12` §6).
4. **Language** — `/en/` served from stored EN content; language switch links the
   translated counterpart; `hreflang` on every page.
5. **Age gate** — rendered server-side in every page, dismissed client-side, remembered
   for the session (as the prototype); no tracking before consent + gate.
6. **Content edit** — staff edit posts, pages, products in the block editor; theme
   patterns give them the prototype's sections; cache purges on publish.

## 6. Data architecture

The prototype's `catalogue.json` is the target product model expressed in WooCommerce
terms — the field-by-field mapping is `12-technical-design.md` §3. No new database:
WooCommerce's product, order, customer and coupon tables carry everything; the
tasting note, vintage note and technical sheet become product meta fields (or
attributes, decided in `12` §3). Content pages (home, Birtok, aszú, Látogatás,
Borklub) are block patterns with editable text and images — not builder layouts.

## 7. Integration architecture

| Integration | Today | Target |
|---|---|---|
| Payment, shipping | WooCommerce providers, flexible-shipping | unchanged; re-verify on staging |
| Newsletter | Mailchimp for WooCommerce | unchanged; the form is the theme's |
| Marketing pixel | PixelYourSite (Meta) | behind consent; one consent plugin |
| Analytics | independent-analytics (first-party) | keep (no consent needed) or GA4 behind consent — client choice |
| Booking | contact form (Amelia installed, unused for booking) | form plugin; Amelia optional later |
| Fonts | Google Fonts (Akzidenz is a licensed face on the live site) | Bodoni Moda + Archivo self-hosted (D3, and one fewer third-party request) |
| Store locator | agile-store-locator | remove unless the estate uses it (not in the prototype) |

## 8. Security and privacy

WordPress and plugin updates on a schedule; admin behind 2FA; HSTS and the existing
headers kept; backups daily with a tested restore; GDPR: consent banner gating pixels,
privacy policy and terms pages kept at their URLs; 18+ gate on every entry point; forms
with spam protection and no PII in URLs; no AI-generated imagery (R7).

## 9. Deployment and operations

Staging site (same host, `staging.` subdomain or host-provided) built during the
freeze; production untouched until 15 January; cutover = theme switch + plugin
prune + cache warm, with the redirect map from `12` §8 in place first; rollback = switch
theme back (WooCommerce data is shared, nothing migrates). Monitoring from day one on
staging: uptime check every minute with alert to a named estate contact and the
developer; WordPress error log shipped to the same channel.

## 10. Stack (PROPOSED)

| Layer | Today (measured) | Proposed | Why |
|---|---|---|---|
| CMS | WordPress | **WordPress, kept** | the estate's content, orders, customers and club live there; staff know it; the incumbent supports it; the "< 12 plugins" target is a WordPress metric — the brief assumes WordPress |
| Theme / rendering | Hello Elementor child + Elementor Pro + 4 add-ons | **custom block theme built from the prototype** (`tokens.css` → `theme.json`, `build.py` page kinds → block templates and patterns) | removes 7 plugins and the runtime page builder; the prototype *is* the spec, measured; staff keep the block editor |
| Commerce | WooCommerce + 8 extensions | **WooCommerce core + ≤ 4 extensions**: reward points (club), gift card, flexible shipping, one more if the estate needs it (bought-together *or* reorder) | keeps every transaction feature the site actually sells; drops side-cart, swatches, extra options, wishlist unless used |
| Multilingual | TranslatePress (runtime) | **Polylang or WPML — stored EN content** | EN is the estate's own copy already (D8); stored content is cacheable and editable; removes the cold-miss render |
| Forms | (contact form, provider not identified) | one form plugin (Fluent Forms / WPForms) | booking request + newsletter |
| SEO | (not identified) | one SEO plugin or theme-native JSON-LD (the prototype already emits it) | `hreflang`, canonical, sitemap |
| Consent | (none identified) | one consent plugin | pixel behind consent |
| Cache | LiteSpeed cache (host) | keep + CDN in front; fix browser cache headers | cache-miss TTFB is the failing number |
| Monitoring | none | uptime + error alerting | acceptance target |
| Fonts | Google Fonts | self-hosted WOFF2 | one fewer origin; D3 faces are OFL |

**Plugin count under this proposal: 9–10** (WooCommerce, 3–4 Woo extensions,
multilingual, forms, SEO, consent, cache, analytics) — under the target with room for
one the estate insists on.

## 11. Architecture decision records

All **PROPOSED** 2026-09-18. Flipping one to DECIDED is a `04-decisions.md` entry.

| ADR | Decision | Options considered | Why this one |
|---|---|---|---|
| ADR-1 | Stay on WordPress + WooCommerce | (a) keep; (b) headless WordPress + static front (Astro/Next, essentially this repo's `build.py` at scale); (c) replatform (Shopify + CMS) | (b) doubles the surface (two deploys, two skill sets) for an estate whose staff and developer are WordPress people, and WooCommerce data would still live in WP; (c) migrates orders, customers, club history and every URL for no target the brief sets. (a) meets all four targets once the builder goes. |
| ADR-2 | Replace Elementor with a custom block theme transcribed from the prototype | (a) keep Elementor and tune; (b) classic PHP theme; (c) block theme | (a) cannot reach < 12 plugins or the weight target; (b) works but loses the block editor's patterns for staff; (c) `theme.json` maps 1:1 onto `tokens.css` (`14-token-map.md`) and patterns map onto the prototype's sections. |
| ADR-3 | Stored-content multilingual (Polylang/WPML) instead of runtime translation | keep TranslatePress | the EN copy already exists as content (catalogue, live EN pages); runtime translation is the cold-miss cost and makes EN uneditable as content. Choice between Polylang and WPML is the developer's, on licence and WooCommerce support. |
| ADR-4 | Plugin budget ≤ 10, list in §10, every addition justified in writing | none | acceptance target < 12 with headroom |
| ADR-5 | CDN in front of the existing LiteSpeed cache; browser caching enabled for static assets | tune origin only | the origin will still miss; the target is measured at the edge and at the origin both |
| ADR-6 | Uptime + error alerting to a named person, from staging onward | none | acceptance target |
| ADR-7 | Booking stays a request form (no availability engine) in Release 1 | Amelia availability + payment | R2 and the audit: the live "booking system" is a form; availability is a business-process change the estate has not asked for |
| ADR-8 | The prototype is the specification: markup, CSS, copy and images are transcribed, not reinterpreted; deviations are recorded as decisions | redesign in the theme | three gates were approved on it; the measurements are its acceptance evidence |
| ADR-9 | Build on staging inside the freeze; cut over after 15 January (assumption A1: the freeze binds production only) | wait for the freeze to end before building | the freeze is the window; confirm A1 with the client in `13` blocked register |
