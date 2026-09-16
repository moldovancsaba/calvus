# Phase 2 — the Látogatás (Visit) page, measured

Built 2026-09-16, HU `latogatas.html` and EN `en/latogatas.html`. Content from the
live `/borkostolo`, `/bortrezor`, `/holdvolgy-experience`, `/borkostolo-idopontfoglalas`
and `/borkostolo-ajandekkartyak` pages: the five pillars (UNESCO site, 1,8 km,
500 years, treasure hunt, vertical Aszú tasting), eight cellar-history milestones
from the late Middle Ages to the 2018 architecture award with their illustrated
cards, the four tasting programmes with durations and the one published price
(6 500 Ft/fő from), the Holdvölgy Experience day from Budapest, the Millennium
Bortrezor with its real terms (5-year lease, 30 bottles a year, 150 in all,
2 500 000 Ft estimated value) and three experiences, the geology (Cladosporium
cellare), the practical information (hours, closed days, one-working-day reply,
durations, under-18 and non-drinker rules) and the booking form with exactly the
live form's fields — Név, E-mail, Telefon, Borkóstoló (four options), Dátum,
Vendégek száma, Üzenet, GDPR — inert in the prototype with e-mail and phone beside it.

Every visit and booking link on the other pages now lands here: the desktop
*Foglalás* button and the phone bar's *Foglalás* → `#foglalas`; the Látogatás
mega-panel's three programmes → `#jegyek`; the sheet's Bortrezor and Experience →
`#trezor`, `#experience`; the home visit card and the Birtok call-to-action.

## Measured

| Check | Phone 390 | Tablet 768 (EN) | Desktop 1440 |
|---|---|---|---|
| Overflow / small taps | 0 / 0 (after fixing the consent checkbox and two inline links) | 0 / 0 | 0 / 0 |
| `h1` | "Borkóstoló a föld alatt" | "Tasting underground" | 1 |
| Images / no alt / broken | 21 / 0 / 0 | — / — / 0 | — |
| Hero source | cellar portrait-780.avif | cellar 1024.avif | cellar 1440.avif |
| Pillars / history / tickets / Experience / Trezor / info | 5 / 8 / 4 / 4 / 3 / 4 | tickets 2 col, info 2 col | 5 / 5 / 4 / 4 / 3 / 4 columns |
| Booking form | all 8 fields present, 4 programme options, two-column rows on ≥ 768 | | |
| In-page anchors | all resolve | | mega-panel: 4 links into this page |
| Console errors | 0 | 0 | 0 |
| Page height | 9,7 screens | | |

## Weight, cold

| | KB |
|---|---|
| Phone 390 | **800** |
| Tablet 768 | **797** |
| Desktop 1440 | **807** |

Under 1,5 MB; the cellar-history cards (330 KB) are the largest cost, lazy-loaded.

## Fixed in the same round, found by the owner on the live Birtok page

- The vineyard map's transparent areas rendered **black**: the converter had
  flattened the RGBA PNG to RGB. Re-encoded with alpha (WebP and AVIF), 58 KB; the
  map is designed for a near-white ground and now sits on the page's `#FAFAFA`.
- The map was **stretched tall** on the phone: the `<img>` carried a `height`
  attribute and the base stylesheet set only `max-width`. `img { height: auto }`
  is now in the base rule for every page. Birtok re-measured: 655 KB phone,
  975 KB desktop.
- Recorded as D16 so the converter and the base rule can't regress.
