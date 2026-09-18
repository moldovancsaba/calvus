# Lexodont — technical design

*Because production exists outside this repo, this is the design of the relationship
between the wireframe and the live site: which wireframe page specifies which live
template, what the content model is in WordPress terms, and the checks a second iteration
runs. Written 2026-09-18.*

## 1. Wireframe page → live template

| Wireframe | Live | Status |
|---|---|---|
| `index.html` | front page | built as specified |
| `szakteruletek.html` | `/szakteruletek/` hub | built |
| nine `*.html` treatment pages | `/szakterulet/<slug>/` | built (slugs match the wireframe's file names where seen: fogszabalyozas, gyokerkezeles, implantologia, parodontologia) |
| `araink.html` | `/araink/` | built with real prices |
| `esettanulmanyok.html` | `/esettanulmanyok/` + `/esettanulmany/<n>-eset/` | built, one page per case |
| `csapat.html` | `/csapat/` | built, four dentists |
| `tudaskozpont-*.html` (4) | `/tudaskozpont/` + articles | built as a hub + posts |
| footer contact | theme footer | verbatim |
| — | `/technologiak/`, `/e-max-betet/`, `/ems/`, `/idopontfoglalas/`, `/en/*`, legal | added by the client's developer |

## 2. Content model in WordPress terms (as observed)

Pages for the hubs and static content; a custom post type or pages under
`/szakterulet/` for specialties; posts (or pages) for articles and cases; theme footer
options for the contact block; WPML translations per page. Not verified from the admin
side — an inventory is LX-002.

## 3. Booking

Flexi-Dent's embed script renders the booking UI inside `/idopontfoglalas/`; the page
itself carries no form and no `h1`. Data flows to the practice's Flexi-Dent account, not
to WordPress. Any change to booking is a Flexi-Dent configuration, not a site change.

## 4. Media

WebP via `webp-uploads`; 30 images on the home page from `/uploads/`; the wireframe's
picsum placeholders correspond to the real photographs slot by slot (hero, team cover,
why-us cards, two cases, eight → four portraits).

## 5. Checks a second iteration runs first (LX-001)

The wireframe gate's criteria applied to the live site: overflow at 390, tap targets
under 44 px, one `h1`, `alt` coverage, `hreflang`, console errors; plus Lighthouse on
the home and one specialty page; plus a Flexi-Dent booking test in HU and EN.
