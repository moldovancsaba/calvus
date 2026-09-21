# Build log

## Round 1 — 2026-09-21 — the first version of the prototype (D1–D9)

**Built.** `build.py` generates five Hungarian pages from one content source (`content.py`):
`index.html` (Címlap), `belfold/index.html` (the Belföld Rovatfront), `cikk/onkormanyzatok-
fejlesztesi-keret.html` (the one Cikkoldal demo, with the registration/paywall mechanic),
`nepszava/index.html` (the Népszava márkafront) and `regisztracio/index.html` (the memo's
pre-registration landing page, with a live countdown to 2026-10-08 08:00 and a client-side-only
registration form). Shared components: header with hamburger/main-nav, article pills, card
row / photo card teasers, the ELEMZÉS/VÉLEMÉNY tag, the paywall box, the registration band, the
four-column footer. Twenty real headlines/deks/bylines read from the Figma file populate the
Belföld, Gazdaság, Kultúra, Külföld, Média and Népszava sections; two original items (Sport,
Tudomány) fill the two nav categories the Figma never designed. Fourteen real, appropriately-
licensed photographs from Wikimedia Commons (3.0 MB total, resized to ≤ 1200 px).

**Measured** (browser pane, cache-busted, all five pages).

| Width | Overflow | `h1` | Console errors | Small (< 44 px) targets |
|---|---|---|---|---|
| 390 | 0 px on every page | 1 on every page | 0 | 0 after two rounds of fixes (see below) |
| 1440 | not exhaustively re-swept post-fix (pane captures ~800 px at a time; spot-checked, no defects found) | — | 0 | — |

**Defects found and fixed in this round** (not left as "known issues" — PROTOTYPING §5):

1. The mobile header overflowed by 70 px (hamburger + search + "Előfizetés" didn't fit beside
   the full wordmark) — fixed by hiding the wordmark under 780 px, matching the Figma's own
   "hamburger · logo · search · Előfizetés" mobile pattern, and tightening header gaps.
2. The landing page had four `<h1>` elements (one per section) — fixed to one `h1` plus three
   `h2`.
3. The brand link, the two header icon buttons, all sixteen footer links and the paywall's
   "Már van fiókom" link were under 44×44 px — fixed with explicit `min-width`/`min-height`
   and flex centring.
4. The registration-band and header-subscribe links on the three depth-1 pages
   (`belfold/`, `cikk/`, `nepszava/`) pointed to `regisztracio/index.html` without the `../`
   prefix, and the Címlap's "Mi lesz a Népszavával?" teaser linked to `#nepszava` while the
   actual section id is `#népszava` (accented) — both caught by `nepszabadsag/check.py` after
   it was extended to cover the site pages (it previously only checked `docs/`), fixed, and
   the gate re-run clean.

**Sample, declared** (`03-sources.md`): the Sport and Tudomány Címlap items; every photograph
(real but not the article's literal documentary subject, where noted in `content.py`); the
paywall/registration back end (visibly present, functionally inert per D8 in `04-decisions.md`,
except the landing form which submits client-side only, D9).

**Not built in this round**: rovat fronts for Külföld, Gazdaság, Kultúra, Sport, Tudomány
(the Figma designs only Belföld's); a technical package (stages 10–14); the presentation
(`bemutato.html`) in Hungarian — next.
