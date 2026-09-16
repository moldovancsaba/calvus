# Holdvölgy 2026 — project documentation

Owner directive 2026-09-16: the whole process is documented next to the project —
research, findings, decisions, assets, and every build round. This folder is that
record. Each file is dated inside; this index is the process log.

| File | What it holds |
|---|---|
| `00-plan.md` | Research findings and the phased implementation plan — the approval document |
| `01-research-benchmarks.md` | Every estate site read, what it returned, and the sites that could not be reached |
| `02-brand-and-site-audit.md` | Holdvölgy's measured brand tokens, fonts, page architecture, product/booking/club pages, and defects found |
| `03-asset-inventory.md` | The 180 real images on the live site, grouped by use, with formats and sizes read from headers |
| `asset-inventory.json` | The same inventory, machine-readable: base image URL → pages it appears on |
| `04-decisions.md` | Decision log — what was decided, by whom, why, and what it replaced |
| `design-system.html` | Phase 1 gate 1: the design system rendered live from the tokens — colour, type, spacing, buttons, cards, bottles, dűlő rows, both navigations |
| `assets-used.md` | Every asset fetched for the build, its source URL, original and derivative sizes |
| `06-home-build.md` | Gate 3: the built home page — what was built, and the measured results at 390, 768 and 1440 |
| `05-layout-specs.md` | Phase 1: the desktop-1440 and phone-390 layout specifications with schematics, tablet resolution and the home weight budget |

## Reading these on the web

GitHub Pages serves this folder. The styled, phone-readable versions are the
rendered pages — `index.html` (this file), `plan.html`, `benchmarks.html`,
`audit.html`, `assets.html`, `decisions.html` — generated from the markdown by
`build.py` (run `python3 holdvolgy/docs/build.py` after editing any `.md`; needs
the `markdown` package). The `.md` files stay the source of truth. Pages' Jekyll
pass also auto-renders each `.md` to an unstyled `<name>.html`; the generated
names above are deliberately different so the two never collide.

## Process log

**2026-09-16 — first prototype (withdrawn as a direction).** Commit `8342956` built a
two-page prototype on a dark ground with a gold accent and a serif display face, from
content fetched off holdvolgy.com. Owner rejected the aesthetic as generic ("the same
colour and typography everywhere") and required industry research before any
further build.

**2026-09-16 — technical context received.** The client's technical situation report,
25-task work list, offer template, the incumbent developer's priced offer and their
scheduling note were shared so the prototype work has the full picture. Commercial
response to those is explicitly not part of this project; the four acceptance
targets (server response < 800 ms, home page < 1,5 MB, < 12 front-end plugins, live
alerting) and the 15 Oct – 15 Jan change freeze are carried as constraints.

**2026-09-16 — research round.** 21 estate sites read (Napa, Sonoma, Bordeaux,
Champagne, Sauternes, Tuscany, Bolgheri, Mendoza, Lebanon, Uruguay, Chile, South
Africa, Rheingau, Tokaj/Mád, Armenia), the World's 50 Best Vineyards 2025 list, the
Awwwards wine gallery; Holdvölgy's own Elementor kit, fonts, page structures, product
pages, booking form, loyalty and Trezor pages read from the live site; 180 images
inventoried without downloading any. Findings in `01`–`03`, plan in `00`.

**2026-09-16 — decisions.** Owner: mobile and desktop are two designed experiences
(D5); commercially free web fonts, Google Fonts preferred (D3); the five-item
navigation is approved (D4); item data will be supplied by the client; full
documentation next to the project (this folder). Plan updated accordingly.

**2026-09-16 — "Go" (D10).** Owner approved the §4 direction. Phase 1 opened with
`assets/tokens.css` and the two layout specifications in `05-layout-specs.md`
(desktop 1440 as the editorial estate, phone 390 as the hospitality-and-buying tool
with a bottom action bar, tablet resolved explicitly, home weight budget per size).
This entry was missing from commit `96dee68` and is restored here.

**2026-09-16 — sequencing corrected (D11).** Owner asked whether the design system
had been approved; it had not. A live design-system page (`design-system.html`) is
now gate 1 of Phase 1, before the layouts. Assets for the home page were fetched
and converted (`assets-used.md`, 22 originals → 27 derivatives, 1,2 MB, originals
not committed) so the system page shows the real bottles on the real ground.

**2026-09-16 — gate 1 approved (D12).** Owner approved the design system. Gate 2
opened as two composed frames at the reference sizes (`frames/home-desktop-1440.html`,
`frames/home-phone-390.html`) built from the approved components and real assets,
embedded in `layouts.html`. Composing them surfaced two missing rock photographs
(Úrágya, Kakasok) — added to the plan's client-gap list.

**2026-09-16 — gate 2 approved (D13); gate 3 built.** The home page exists as one
responsive document generated in HU (`index.html`) and EN (`en/index.html`) by
`build.py`, with phone (≤ 767), tablet (768–1023) and desktop (≥ 1024) each
designed per the frames. Measurements are in `06-home-build.md`. The withdrawn
first-prototype shop page was removed.

**Next.** Gate 3 review of the built home page; then Phase 2 (Birtok, Tokaji aszú,
Látogatás pages).
