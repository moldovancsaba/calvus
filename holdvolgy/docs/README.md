# Holdvölgy 2026 — project documentation

Owner directive 2026-09-16: the whole process is documented next to the project —
research, findings, decisions, assets, and every build round. This folder is that
record. Each file is dated inside; this index is the process log.

| File | What it holds |
|---|---|
| `bemutato.html` | **A birtoknak szóló bemutató, magyarul** — a birtok saját arculatában: hét lépés az élő oldalakkal, mi valódi, mit kérünk, hogyan tovább |
| `00-brief.md` | Two pages for a first reader: the client, the problem, what the prototype is, what is real, where it stands |
| `00-plan.md` | Research findings and the phased implementation plan — the approval document |
| `01-research-benchmarks.md` | Every estate site read, what it returned, and the sites that could not be reached |
| `02-brand-and-site-audit.md` | Holdvölgy's measured brand tokens, fonts, page architecture, product/booking/club pages, and defects found |
| `03-asset-inventory.md` | The 180 real images on the live site, grouped by use, with formats and sizes read from headers |
| `asset-inventory.json` | The same inventory, machine-readable: base image URL → pages it appears on |
| `04-decisions.md` | Decision log — what was decided, by whom, why, and what it replaced |
| `design-system.html` | Phase 1 gate 1: the design system rendered live from the tokens — colour, type, spacing, buttons, cards, bottles, dűlő rows, both navigations |
| `assets-used.md` | Every asset fetched for the build, its source URL, original and derivative sizes |
| `11-gate-sweep.md` | Phase 5: the whole-site sweep — method, 152 measurements over 76 pages, hand-off state |
| `10-shop-build.md` | Phase 3: the shop — catalogue, grid, product template, Borklub, measurements |
| `09-latogatas-build.md` | Phase 2: the Látogatás page — sources, booking form, measurements, and the map fix |
| `08-aszu-build.md` | Phase 2: the Tokaji aszú page — sources, the Culture wall, measurements |
| `07-birtok-build.md` | Phase 2: the Birtok page — content sources, sections, measurements at 390/768/1440, and the navigation fixes made in the same round |
| `06-home-build.md` | Gate 3: the built home page — what was built, and the measured results at 390, 768 and 1440 |
| `05-layout-specs.md` | Phase 1: the desktop-1440 and phone-390 layout specifications with schematics, tablet resolution and the home weight budget |
| `09-business-logic.md` | **Business logic** — the rules end to end: parties, what is sold and what is only presented, the age gate, the shop, the club, the visit, two languages, the data, the rules mapped, what the site never does (2026-09-20) |
| `10-ssot.md` | **Technical package** — glossary, enumerations, the product entity, settings, rules register, metrics, document map |
| `11-architecture.md` | The live site measured (platform, 23 plugins, weight, TTFB), quality attributes, target containers, the **PROPOSED** stack and nine ADRs |
| `12-technical-design.md` | Page kinds → theme templates, content model, `catalogue.json` → WooCommerce mapping, forms, club tiers, languages, URLs and redirects, images, performance, operations |
| `13-implementation-plan.md` | Milestones M0–M6 inside the change freeze, issues HV-000..084 with Definition of Done, blocked register, risks, Release 1 scope |
| `14-token-map.md` | `tokens.css` → `theme.json`, components → theme parts and patterns, what is not tokenised, how it is verified |

## The standard documentation structure

Every Calvus project carries the same set next to its prototype (owner decision
2026-09-18). Where this folder predates the standard, the slot maps to the existing file:

| Slot | Here |
|---|---|
| Presentation | `bemutato.html` |
| 00 brief | `00-brief.md` |
| 01 research | `01-research-benchmarks.md` |
| 02 audit | `02-brand-and-site-audit.md` |
| 03 sources and assets | `03-asset-inventory.md`, `asset-inventory.json`, `assets-used.md` |
| 04 decisions | `04-decisions.md` |
| 05 design | `design-system.html`, `05-layout-specs.md`, `frames/` |
| 06 build log | `06-home-build.md` … `10-shop-build.md` |
| 07 gate | `11-gate-sweep.md` + `holdvolgy/check.py` (run by the root `check.py`) |
| 08 client asks | `00-plan.md` §6 |
| 10–14 technical | `10-ssot.md`, `11-architecture.md`, `12-technical-design.md`, `13-implementation-plan.md`, `14-token-map.md` |

## Reading these on the web

GitHub Pages serves this folder. The styled, phone-readable versions are the rendered
pages — one per markdown file, listed in `build.py` (`index.html` for this file,
`brief.html`, `plan.html`, `benchmarks.html`, `audit.html`, `assets.html`,
`decisions.html`, `layouts.html`, the five build pages, `gate-sweep.html`, `ssot.html`,
`architecture.html`, `technical-design.html`, `implementation-plan.html`,
`token-map.html`) plus the hand-written `design-system.html` and `bemutato.html`. Run
`python3 holdvolgy/docs/build.py` (or `python3 build-docs.py` at the repo root) after
editing any `.md`; needs the `markdown` package. The `.md` files stay the source of
truth. Pages' Jekyll pass also auto-renders each `.md` to an unstyled `<name>.html`; the
generated names are deliberately different so the two never collide.

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

**2026-09-16 — home approved; Phase 2 Birtok built.** Owner: "Perfect, continue".
The Birtok page exists in HU and EN with the estate's own content end to end
(`07-birtok-build.md`). In the same round the owner found a dead link from a cached
hub card to the deleted shop URL, and the design-system page's navigation had
drifted — both fixed structurally (D14, D15): a redirect at the old URL, a
single-sourced navigation, a whole-project link audit in the gate.

**2026-09-16 — Phase 2: Tokaji aszú built.** HU and EN, with the Culture wall of
thirteen vintages and prices, making and ageing, Time Capsule, PreCulture and the
Tokaj heritage milestones (`08-aszu-build.md`). The pre-push link audit caught a
wrong render filename; fixed before the push.

**2026-09-16 — Phase 2 complete: Látogatás built; map defect fixed.** The visit
page in HU and EN with tickets, Experience, Bortrezor, geology, practical
information and the booking form (`09-latogatas-build.md`). The owner found the
vineyard map black and stretched on the live Birtok page — two converter/CSS
defects, fixed at the root (D16).

**2026-09-16 — Phase 3 built: shop, product pages, Borklub.** `data/catalogue.json`
holds 32 products with the client's HU and EN copy from the live shop; the grid,
32 + 32 product pages and the club page are generated from it (`10-shop-build.md`).
The wine links across the site now land on real product pages.

**2026-09-16 — Phase 5: whole-site sweep, zero defects.** Every one of the 76 site
pages measured at 390 and 1440 (152 measurements) with no defect on any criterion
(`11-gate-sweep.md`). The plan's five phases are complete; the open items are the
client's (portraits, two rock photographs, portrait hero frames, technical data).

**2026-09-16 — stale prototype banner.** The owner quoted the banner still saying the
shop pages were to come in Phase 3. It now states only what is inert in the
prototype (cart, forms) on every page in both languages.

**2026-09-16 — the gate becomes one command (`holdvolgy/check.py`).** After the owner
had to catch stale text four times, staleness is now something the gate scans for:
phrases that were true once, the prototype banner on every page, plus the link,
anchor and docs-nav audits. Its first run found the shop's collection anchors
existing only after JavaScript (now rendered statically) and the design-system page
still carrying its pre-approval eyebrow. CLAUDE.md rule 2 names the command.

**2026-09-16 — readiness review.** Every site file compared live against the repo
(238 identical), every EN page scanned for Hungarian, every page type looked at top
to bottom on the phone and desktop. Findings fixed: product descriptions ran into
the live page's tabs — parsing them properly put a tasting note, vintage note and
full technical sheet on 31 product pages (closing a §6 gap); the tagline printed
twice; the fact-sheet section's class collided with the menu dialog and floated over
the page (D18). The claude.ai plan page was republished with its status.

**2026-09-17 — client presentation page.** The owner asked whether the plan and the
client presentation live on GitHub Pages or only as a claude.ai artifact. The plan
did (`plan.html`); a client-facing presentation did not exist. `bemutato.html` is
now that page, in Hungarian: what to look at, why it looks this way, what is real,
what was measured, what we ask of the estate, and what comes next.

**2026-09-17 — the presentation rebuilt in the estate's own visual language.** The
owner rejected the documentation-shell version: the bemutató is now a standalone
page on the Holdvölgy design system — cellar photograph and one sentence, three
numbers, a seven-step walk through the live pages shown in scaled phone frames with
open-in-HU/EN buttons, what is real, six asks, three next steps. Direct address to
the estate, short sections, no documentation chrome.

**2026-09-17 — documentation pages on the site tokens.** The docs stylesheet carried
its own palette and a dark-mode override that turned the documentation pages dark on
a phone in dark mode — the treatment rejected for the site. The docs now use
`assets/tokens.css` directly and stay on the light ground in every colour scheme.

**2026-09-18 — technical package written (D19).** The owner set a standard
documentation structure for every project — customer side as this folder already had
it, plus a technical side on the DiscountDirect pattern. `00-brief.md` and `10`–`14`
added. The live site was measured for it (WordPress, Elementor, WooCommerce; 23
front-end plugins against a target of 12; 8,8 MB home; cached TTFB 0,06 s, cold 4,5 s).
The proposed stack — stay on WordPress and WooCommerce, replace Elementor with a block
theme transcribed from the prototype, stored-content multilingual, CDN, monitoring — is
in `11-architecture.md` §10–11 in status **PROPOSED**; nothing is decided with the
client yet. The docs renderer's page list and navigation grew by six pages.

**Next.** Client review of the whole; the stack decision and who builds (blocked
register in `13`); then the items in §6 of the plan as they arrive.
