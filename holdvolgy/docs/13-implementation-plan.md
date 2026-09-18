# Holdvölgy 2026 — implementation plan

*Milestones, issues with a Definition of Done, what is blocked and on whom, risks. Sized
for whoever builds — the incumbent developer, Calvus, or both — under the PROPOSED stack
(`11-architecture.md`). Nothing here is scheduled until the blocked register is empty.
Written 2026-09-18.*

## 0. Conventions

Issue ids `HV-nnn`; epics E0–E8; milestones M0–M6. Every issue names its acceptance in
measurable terms taken from the prototype's gate (`10-ssot.md` §7). "Matches the
prototype" means: same section order, same copy, same images, gate criteria green at 390
and 1440, and a side-by-side screenshot in the build log.

## 1. Global Definition of Done

An issue is done when: built on staging; HU and EN both; gate criteria measured and
recorded (one `h1`, `alt`, `hreflang`, 0 px overflow, 0 tap targets under 44 px, 0
console errors); the affected URLs in the redirect map still resolve; no new plugin
without a written justification (ADR-4); the build log entry written.

## 2. Milestones

| M | Name | Exit criterion | Freeze |
|---|---|---|---|
| M0 | Baseline and staging | staging clone of production; monitoring live on staging; the 23-plugin inventory confirmed from the admin side; theme repo created with `theme.json` from `14-token-map.md` | before or during |
| M1 | Theme foundation | header/mega-nav, bottom bar + sheet, footer, age gate, banner-free base; tokens render the design-system page's components identically | during |
| M2 | Content pages | Home, Birtok, Tokaji aszú, Látogatás, Borklub as templates + patterns, HU + EN, matching the prototype | during |
| M3 | Shop | product import from `catalogue.json`; Borok archive with filters and sort; product template with the three tabs; cart/checkout restyled; club tiers configured and tested | during |
| M4 | Language and URLs | EN parity on every page and product; `hreflang`; redirect map live on staging and audited | during |
| M5 | Performance and plugin prune | origin TTFB < 800 ms measured on staging (cache off); home < 1,5 MB; ≤ 10 front-end plugins; LCP < 2,5 s at 390 on throttled 4G | during |
| M6 | Cutover | after 15 January: production switch per `12` §12; measurements repeated on production; monitoring green 7 days | after |

Indicative effort for one experienced WordPress developer with the prototype in hand: M0
one week; M1 two; M2 three; M3 three; M4 one; M5 one; M6 one plus a week of watching.
About twelve weeks, comfortably inside the freeze window if M0 starts by early November.

## 3. Issues

### E0 Foundations (M0)
- **HV-000** Confirm assumption A1 with the client (freeze binds production only) — DoD: written yes/no in `04-decisions.md`.
- **HV-001** Staging environment on the current host, copy of production data — DoD: staging URL reachable, admin access for the builder, `noindex`.
- **HV-002** Plugin inventory from the admin (installed, active, licensed, last update) — DoD: table in the build log; each of the 23 marked keep / replace / remove with the reason.
- **HV-003** Monitoring: uptime check + PHP error alerting to a named estate contact and the developer — DoD: a forced 500 on staging produces an alert within 2 minutes.
- **HV-004** Theme repository with `theme.json` generated from `tokens.css` (`14`) and the prototype HTML per page kind checked in as reference — DoD: `theme.json` values equal the token values, verified by a script.
- **HV-005** Decide multilingual plugin (Polylang vs WPML) on WooCommerce support and licence — DoD: ADR-3 detail recorded in `04-decisions.md`.

### E1 Theme foundation (M1)
- **HV-010** Header + desktop mega-nav (≥ 1024) from `parts/header.html` — DoD: five items (D4), matches design-system page.
- **HV-011** Phone bottom action bar + sheet (< 1024) — DoD: matches `05-layout-specs.md`; 44 px targets.
- **HV-012** Footer — DoD: matches prototype; newsletter field wired (E5).
- **HV-013** Age gate as a `<dialog>` in every page, session-remembered, keyboard-operable — DoD: R8; no content hidden from crawlers.
- **HV-014** Base stylesheet: tokens + components (buttons, card, bottle, dűlő row, form field) — DoD: ≤ 40 KB; `img { height: auto }` (R4).
- **HV-015** Self-hosted Bodoni Moda + Archivo WOFF2, `font-display: swap` — DoD: no Google Fonts request.

### E2 Content pages (M2)
- **HV-020** Home template + patterns — DoD: matches `index.html` / `en/index.html`; weight ≤ prototype's 734 KB desktop.
- **HV-021** Birtok — timeline and team as repeatable blocks — DoD: matches; portraits slot ready for the client's images.
- **HV-022** Tokaji aszú — Culture wall data-driven from products of line Culture — DoD: 13 vintages with live prices; matches.
- **HV-023** Látogatás — tickets block, practical info, guestbook — DoD: matches; form in E5.
- **HV-024** Borklub — tiers rendered from configuration — DoD: four tiers equal the settings in E3.
- **HV-025** Initial content import HU + EN from `build.py` strings — DoD: no copy differs from the prototype (diff script).

### E3 Shop (M3)
- **HV-030** Taxonomies `wine_type`, `wine_line`; product meta fields per `12` §3 — DoD: schema documented in the theme repo.
- **HV-031** `data/export-woo.py` and the import — DoD: 32 products, every field present, one "price on request".
- **HV-032** Borok archive: filter, sort, two-up on phones — DoD: matches `borok.html`.
- **HV-033** Product template with Kóstolási jegyzet · Az évjárat · Adatlap and JSON-LD — DoD: matches a sample of 5 product pages incl. the tab-less one.
- **HV-034** Cart, checkout, account restyled with tokens — DoD: a test order completes on staging in HU and EN.
- **HV-035** Club tiers in reward points — DoD: test customers at each threshold receive the right discount; rolling-window behaviour recorded.
- **HV-036** Gift card and shipping extensions verified — DoD: gift card purchase and a shipping quote succeed on staging.

### E4 Language and URLs (M4)
- **HV-040** Every page and product paired HU/EN with `hreflang` — DoD: sweep shows 3 `hreflang` links on every page.
- **HV-041** Redirect map for merged pages and any changed slug — DoD: every URL in `03-asset-inventory.md`/audit resolves 200 or 301 to the right anchor.
- **HV-042** Sitemaps per language; `noindex` on transactional screens — DoD: sitemap validates.

### E5 Forms and consent (M2–M3)
- **HV-050** Booking request form — DoD: `12` §5 validation; e-mail + entry; auto-reply; honeypot.
- **HV-051** Newsletter to Mailchimp — DoD: double opt-in lands in the audience.
- **HV-052** Consent banner gating PixelYourSite — DoD: no pixel request before consent (network log).

### E6 Performance and plugin prune (M5)
- **HV-060** Deactivate Elementor, Pro, the four add-ons, TranslatePress, and the unused Woo extensions on staging — DoD: front end renders without them; plugin count ≤ 10.
- **HV-061** CDN in front; browser cache headers for static assets — DoD: assets served with long max-age; HTML cache policy documented.
- **HV-062** Measurements: origin TTFB (cache off) HU and EN, home weight, LCP at 390 — DoD: all under target, numbers in the build log.

### E7 Cutover (M6)
- **HV-070** Cutover rehearsal on staging — DoD: runbook in `12` §12 executed end to end once.
- **HV-071** Production cutover after 15 January — DoD: runbook steps ticked; link audit clean; measurements repeated; monitoring green for 7 days.
- **HV-072** Hand-over session with estate staff (editing pages, products, prices, answering bookings) — DoD: staff edit a product price and a page text unaided.

### E8 Client items (any time; content, not code)
- **HV-080** Founder and team portraits; **HV-081** Úrágya and Kakasok rock photographs; **HV-082** harvest dates, awards, ageing potential as structured data; **HV-083** Culture 133 000 Ft item confirmed; **HV-084** EN copy confirmation — DoD each: received, imported, page updated (plan §6).

## 4. Blocked register

| Item | Blocked on | Unblocks |
|---|---|---|
| ADR-1..9 status | owner / client decision on the stack | everything from M0 |
| A1 (freeze binds production only) | client | M0–M5 timing |
| Who builds | client (incumbent's offer vs Calvus vs both) | M0 |
| Admin access to production/hosting | client | HV-001, HV-002 |
| Multilingual plugin choice | builder (HV-005) | M4 |
| HV-080..084 | client | content completeness, not the build |

## 5. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| The incumbent's offer is an Elementor rebuild | targets cannot be met (§2 of the architecture) | put the measured numbers in front of the client with the offer |
| Reward-points extension cannot express rolling 12-month tiers | club rules diverge from the page | `12` §6 fallback; verify in HV-035 before M2 copy is final |
| WooCommerce screens look foreign next to the theme | brand break at the moment of purchase | HV-034 restyle is in scope; not a redesign |
| EN content drift after go-live (staff edit HU only) | parity lost | the multilingual plugin's "needs translation" state; monthly check in the process log |
| Freeze assumption A1 wrong | build cannot start until mid-January | ask in HV-000 first |
| Client data (portraits, photos) arrives late | pages ship with slots absent | slots are absent by design (R2); nothing blocks go-live |

## 6. Release scope

**Release 1 (go-live, early 2027):** M0–M6 as above — the whole prototype as the live
site, shop and club working on WooCommerce as today, booking as a request form, EN
parity, targets measured and met.

**Not in Release 1, recorded so nobody expects it:** timed booking with availability and
payment (ADR-7), a redesigned checkout, gift-card page redesign, blog/news beyond the home
teaser, a members-only area, PreCulture purchase flow (needs the estate's allocation
rules), print or e-mail templates.
