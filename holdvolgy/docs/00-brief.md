# Holdvölgy 2026 — brief

*Who this is for: anyone opening this project for the first time — client, estate staff,
a developer picking up the build. Two pages of what it is, what is real, and where it
stands. Written 2026-09-18; the process log in `README.md` is the dated trail.*

## The client

Holdvölgy — a Tokaji wine estate in Mád: seven dűlők, thirty parcels, a 1,8 km cellar
on three levels, thirteen Culture aszú vintages 2006–2018, open direct-to-consumer
sales with prices in HU and EN, a loyalty club, visits and tastings, an experiential
programme (Trezor). The live site is holdvolgy.com — WordPress, Elementor, WooCommerce
(measured in `11-architecture.md` §2).

## The problem the estate brought

A 2026 rebuild of the site. The client's technical brief (received 2026-09-16, not in
this repo) sets four acceptance targets — server response under 800 ms, home page
under 1,5 MB, fewer than 12 front-end plugins, live alerting — and a change freeze on
the live site from 15 October to 15 January. A first prototype (commit `8342956`) was
withdrawn as a direction: dark ground, gold accent, generic. The owner required
industry research before any second build.

## What the prototype is

A complete, generated, bilingual site on the estate's own brand, served from this repo
on GitHub Pages: home, Birtok, Tokaji aszú, Látogatás, Borok with 32 product pages,
Borklub — HU and EN, 76 pages. Built through three approval gates (design system →
layout frames → home) and five phases, every page measured at 390 and 1440. The
research (21 estate sites), the audit of the live site, the asset inventory, every
decision and every build round are in this folder. The client-facing walkthrough is
`bemutato.html`.

Live: <https://moldovancsaba.github.io/calvus/holdvolgy/> · EN
<https://moldovancsaba.github.io/calvus/holdvolgy/en/>

## What is real and what is not

- **Real:** every text, price, image and technical sheet is the estate's, taken from
  the live site (`assets-used.md`, `data/catalogue.json`); the palette is the one
  measured from the live Elementor kit; the fonts are commercially free equivalents
  chosen by the owner (D3).
- **Inert, by design:** the cart, the booking form, the newsletter field and the club
  sign-up do not send. Every page says so in its banner. Nothing pretends to be
  available that is not (no fake stock, no fake dates).
- **Placeholders:** none. Where the estate has not supplied something (founder and
  team portraits, two rock photographs, harvest dates and awards as structured data),
  the slot is absent, not faked — the list is plan §6 (`00-plan.md`) and the bemutató's "Hat dolog".

## Where it stands

| | |
|---|---|
| Customer side | complete — presentation, research, audit, assets, decisions, design system, layouts, build logs, gate sweep (0 defects over 152 measurements) |
| Technical side | proposed — SSOT, architecture with a **PROPOSED** stack, technical design, implementation plan and token map written 2026-09-18 (`10`–`14`); nothing decided with the client yet |
| Open with the client | review of the whole; the items in plan §6; the stack decision; who builds (the incumbent developer has a priced offer) |
| Timing | production is frozen 15 Oct – 15 Jan; the plan builds on staging inside the freeze and goes live early 2027 (`13-implementation-plan.md`) |

## How to read this folder

Customer side first (`README.md` index, then `bemutato.html` for the client's view);
technical side `10`–`14` in order — the SSOT defines the words the others use.
