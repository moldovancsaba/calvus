# Lexodont — audit: the wireframe and the site that was built from it

*Measured 2026-09-18 with `curl` from this environment; the prototype measured in the
browser pane (`07-gate.md`).*

## The live site (lexodont.hu)

| Measure | Value |
|---|---|
| Platform | WordPress; custom theme `lexodont` (Bootstrap 5, jQuery 3.5.1, Owl Carousel, one `style.css` of 162 KB, one `scripts.min.js`); no page builder |
| Plugins visible from the front end | WPML 4.7.1 (`sitepress-multilingual-cms`), Yoast SEO 28.4, `performance-lab` + `webp-uploads`; Google Analytics 4 (`G-YEDLSJR6LH`) |
| Booking | **Flexi-Dent** embed (`publicapi.flexi-dent.hu/api/booking/embed/js`) on `/idopontfoglalas/` — a dental practice-management system, not a contact form |
| Languages | HU root, EN under `/en/` with `hreflang` hu / en / x-default on every page |
| Home | 76 KB HTML, 6 scripts, 5 stylesheets, 30 images from `/uploads/` (WebP), TTFB 0,36–0,38 s |
| Subpages | 30–80 KB; TTFB 0,24–0,32 s; last modified 2026-07-30 (Szakterületek) to 2026-09-18 (EN home) |
| Fonts, icons | Google Fonts Outfit; Bootstrap Icons 1.10.3 from jsDelivr |
| Map | Google Maps (the wireframe had OpenStreetMap) |
| Before/after | present on the home page (18 matches for the slider markup) |

## Wireframe → live, page by page

| Wireframe page | Live URL | Note |
|---|---|---|
| index (hero, why us, 4 featured specialties, 2 before/after cases, knowledge, reviews, partners, contact footer) | `/` | same `h1`; same section order; contact footer verbatim |
| szakteruletek + 9 treatment pages | `/szakteruletek/`, `/szakterulet/<slug>/` | live links show fogszabályozás, gyökérkezelés, implantológia, parodontológia as featured — the wireframe's four |
| araink (illustrative prices) | `/araink/` | real prices (15 000 · 5 000 · 10 000 · 29 000 · 35 000 · 51 000 · 135 000 Ft …); the wireframe's 210 000 Ft implant line is not on the live page as such |
| csapat (8 placeholder doctors with fun facts) | `/csapat/` | four real dentists: Dr. Gaál Petra, Dr. Kerekes Fanni, Dr. Makra Krisztián, Dr. Reichert Éva |
| esettanulmanyok (sliders) | `/esettanulmanyok/`, `/esettanulmany/1-eset/`, `/2-eset/` | one page per case, as the wireframe's "részletes esetlap" link implied |
| tudaskozpont-* (4 articles) | `/tudaskozpont/`, article URLs (e.g. the PRF article) | hub page + articles |
| (none) | `/technologiak/` | **new on the live site** — not in the wireframe |
| (none) | `/e-max-betet/`, `/ems/` | treatment/technology pages not in the wireframe |
| footer "Időpont foglalás" → `#kapcsolat` | `/idopontfoglalas/` with Flexi-Dent | the wireframe had no booking mechanism |
| WhatsApp CTA (commit 298a2af) | not found on the live home | dropped |
| OpenStreetMap embed | Google Maps | replaced |
| Impresszum, Adatkezelés `#` | `/adatkezelesi-tajekoztato/` | real |
| EN switch (none in wireframe) | `/en/` full mirror via WPML | added |

## The wireframe itself

| Measure | Polished (18 pages) | Sketch (15 pages) |
|---|---|---|
| Overflow at 390 / 1440 | 8 px on `parodontologia` at 390; 0 elsewhere | 0 |
| Tap targets under 44 px at 390 | index 5, esettanulmanyok 3 | 3–16 on every page (underlined inline links, 2 px-bordered buttons) |
| One `h1`, `alt` on every image, `<title>`, `lang` | all pages | all pages |
| Images | 49 of 49 are picsum.photos placeholders | 6 (sliders), all placeholders |
| JavaScript | before/after slider only (home, case studies) | same |
| Parity | — | lacked gyerekfogászat, gyökérkezelés, parodontológia (added to the polished set on 2026-04-09, never mirrored) — mirrored on 2026-09-18 so the gate's parity check is clean (D15) |
| `public/` (repo root) | 20 PNGs from the first build (crew, hero, team) — unreferenced since the switch to picsum on 2026-03-31; removed 2026-09-19 | |

## Reading

The wireframe did what a wireframe is for: the structure, navigation, section order and
copy tone it fixed are on the live site. What it did not carry — real photography, real
prices, a booking engine, a technologies page, EN — the client's developer added. The
prototype's remaining defects (phone tap targets, one 8 px overflow) are recorded, not
fixed: there is no reader left for the wireframe except this record. The three missing
sketch pages were added, because the gate would otherwise stay red by design.
