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

## Round 2 — 2026-09-21 — the Népszava sub-brand removed (D12)

**Removed, on the owner's explicit instruction** (a deliberate deviation from the Figma file,
made with the tradeoff stated plainly beforehand, not an error): the `Népszava` nav item; the
whole `nepszava/index.html` page (`build_nepszava()` deleted from `build.py`); the Címlap's
Népszava block (six-item grid, "A Népszabadság almárkája" heading); the front-page "Mi lesz a
Népszavával?" teaser; the footer's "Almárka" column, now three columns instead of four; and
the four Wikimedia Commons photographs sourced only for that section (`nepszava-interju.jpg`,
`nepszava-riport.jpg`, `nepszava-jegyzet.jpg`, `nepszava-hetkepe.jpg`). `content.py`'s `NAV`
list, `FOOTER_ALMARKA`, `NEPSZAVA_ITEMS` and `NEPSZAVA_VELEMENY` removed entirely; the Lead
story's second teaser link removed since its target no longer exists.

**Measured** (browser pane, cache-busted, all four remaining pages): 390 px — 0 px overflow,
one `h1`, 0 console errors, 0 sub-44 px targets except the one remaining inline teaser link
(same accepted pattern as before). Gate re-run clean after the removal — no dangling links to
the deleted page.

**Now four pages**, not five: `index.html`, `belfold/index.html`,
`cikk/onkormanyzatok-fejlesztesi-keret.html`, `regisztracio/index.html`.

## Round 3 — 2026-09-21 — real content in place of the two gray placeholders (D13)

**Owner flagged, from live-site screenshots**: an empty gray author-photo circle and a plain
gray "HIRDETÉS 970×250" box — "add content everywhere... be professional."

**Built.** `avatar()` in `build.py` renders a designed initials-mark (colored circle, the
author's own initials) for each of the six bylined authors — `content.py AUTHORS[*]
["avatar_color"]` gives each a distinct color. `ad_slot()` rewritten to render real ad
creative from `content.py AD_CREATIVES` — three fictional advertisers (a travel agency, a
home-goods retailer, a savings account) filling the Figma's three banner placements
(Címlap 970×250 "Városnéző Utazási Iroda", the Cikkoldal's inline 600×250 "Otthon Trend",
its rail 300×250 "Takarék Plusz"). `assets/site.css` gets `.avatar`/`.avatar-square`/
`.avatar-circle` and `.ad-creative` rules; the stale `.author-card img`/`.author-row img`
selectors (expecting an `<img>` that was never rendered) removed.

**Also fixed while measuring this round**: `.author-row`'s `align-items:center` vertically
centered the new avatar against the whole byline block (name + bio + button), landing it
beside the bio line instead of the name — changed to `flex-start` so the avatar aligns with
the top line, as a byline normally reads. Separately, the desktop main-nav's "Sport" link
measured 40×46 px (only the short nav words were under 44 px wide; `.main-nav a` had
vertical-only padding) — added horizontal padding and a `min-width`, first sub-44 px item
caught at 1440 px in this project's measured passes so far (earlier rounds tested mobile,
where the nav collapses to a full-width hamburger menu).

**Measured** (browser pane, cache-busted, all four pages, 390 and 1440): 0 px overflow, one
`h1`, 0 console errors, 0 sub-44 px targets besides the one already-accepted inline teaser
link. Gate re-run clean.

**Sample, declared** (`03-sources.md`): the six avatars and the three ad creatives — never a
real photograph or a real advertiser. The landing page's third placeholder (`editor-post`,
"A Szerkesztőség" latest-post box) was deliberately left as-is — it stands in for a specific
real post the client hasn't supplied yet (`03-sources.md` #4), not a generic slot, so filling
it with invented content would misrepresent real editorial activity rather than just dress up
a placeholder.
