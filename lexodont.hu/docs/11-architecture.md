# Lexodont — architecture

*Unlike the other projects, the production system exists and was measured: this document
records the **as-built** stack of lexodont.hu (facts, 2026-09-18) and, in §5, what a second
iteration would change — those parts are PROPOSED. Written 2026-09-18.*

## 1. System context

| Actor | With the site |
|---|---|
| Patient (HU, EN) | reads specialties, prices, team, cases; books via Flexi-Dent; calls or e-mails |
| Practice staff | edit pages in WordPress; manage bookings in Flexi-Dent |
| Client's developer | built and maintains the custom theme |
| Calvus | supplied the wireframe (the specification) |

External: Flexi-Dent (practice management + booking widget), Google Analytics 4, Google
Maps, Google Fonts (Outfit), jsDelivr (Bootstrap Icons), WPML.

## 2. As built, measured

| Layer | Value |
|---|---|
| CMS | WordPress; custom theme `lexodont` (Bootstrap 5 bundle, jQuery 3.5.1, Owl Carousel, `style.css` 162 KB, `scripts.min.js`) |
| Plugins visible | WPML 4.7.1; Yoast SEO 28.4; performance-lab + webp-uploads |
| Booking | Flexi-Dent embed on `/idopontfoglalas/` |
| Languages | HU root, EN `/en/`, `hreflang` on every page |
| Analytics | GA4 `G-YEDLSJR6LH` via gtag |
| Media | WebP under `/uploads/` (via webp-uploads) |
| Performance (home) | 76 KB HTML, 6 scripts, 5 stylesheets, 30 images; TTFB 0,36 s; subpages 0,24–0,32 s |
| SEO | Yoast: canonical, OG, JSON-LD WebPage/breadcrumb, robots index |
| Security headers | not measured |
| Hosting, backups, monitoring | not visible from outside; not known |

## 3. Quality attributes (observed)

Fast origin; small pages; bilingual parity via WPML; SEO in place; one `h1` per page
except the booking page (none). Not measured: mobile tap targets, overflow, contrast,
Core Web Vitals — a second iteration starts by measuring them (`13` LX-001).

## 4. Containers

```
 patient ──▶ lexodont.hu (WordPress, theme "lexodont")
             ├─ pages: home, szakterületek/*, technológiák, áraink, esettanulmányok/*, tudásközpont/*, csapat, kapcsolat, legal
             ├─ WPML: /en/ mirror
             ├─ Yoast: SEO
             ├─ /idopontfoglalas/ ──▶ Flexi-Dent booking embed ──▶ practice calendar
             └─ GA4, Google Maps, Google Fonts, jsDelivr
```

## 5. What a second iteration would change (PROPOSED)

| ADR | Proposal | Why |
|---|---|---|
| ADR-1 | Keep the stack exactly as built | it is lean, fast, bilingual and owned by the client's developer; nothing in the wireframe's intent is unmet |
| ADR-2 | Measure before changing: phone-width tap targets and overflow on every live page, CWV, contrast | the wireframe's own findings (`07-gate.md`) may or may not have carried over |
| ADR-3 | Self-host Outfit and Bootstrap Icons | two third-party origins on every page; trivial to remove |
| ADR-4 | Add an `h1` to the booking page | the one page without one |
| ADR-5 | Decide the dropped wireframe items (WhatsApp CTA, OSM) explicitly | `08-client-asks.md` #4 |

No ADR proposes a rebuild. The wireframe's tokens are not a production system
(`14-token-map.md`).
