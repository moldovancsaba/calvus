# business.direct — project documentation

An automated marketing machine for B2B2C listing platforms — the one-person sales and
marketing team for a listed business, run by the platform, with the consumer as the
third role. First client: **Your Field NYC** (getyourfield.com). Sibling of DiscountDirect.
Built to the prototyping standard (`PROTOTYPING.md`); this index is the process log.

| Slot | File | What it holds |
|---|---|---|
| 00 brief | `00-brief.md` | Client, problem, the three views and four automations, what is real, what is inert |
| 01 research | `01-research.md` | Sourced: reputation and claiming, speed to lead, reminders, digests, generated pages, marketplace monetisation, AI adoption and human-in-the-loop, EU AI Act Art. 50, US CAN-SPAM and TCPA, the Hungarian reference market |
| 02 audit | `02-audit.md` | Your Field measured: API, 252 providers, field coverage, site copy; the Hungarian reference instance; the two videos frame by frame; what DiscountDirect provides |
| 03 sources | `03-sources.md` | What is real (the platform's public data), what is sample, what is inherited |
| presentation | `bemutato.html` | Standalone, English, on the product's tokens: one sentence, three numbers, the four things to click with previews, what is real, the asks, what comes next |
| 04 decisions | `04-decisions.md` | D1–D20 |
| 05 design | `design-system.html` + `../assets/tokens.css` + `../assets/components.css` | **Gate 1 approved (D9)**: tokens and components, one source |
| 05 layouts | `05-layout-specs.md` + `layouts.html` + `frames/` | **Gate 2 approved (D16)**: platform 1440 / 390, provider 390, family 390 |
| 06 build log | `06-build-log.md` | Round 1: the prototype; 1b: presentation and package; 2: editors real, tablet measured |
| 07 gate | `07-gate.md` + `../check.py` | Measured pass at 390, 768, 1024 and 1440: overflow, tap targets, navigation, console, links |
| 08 owner asks | `08-client-asks.md` | Seven open items (#1 closed by D20) |
| 10 SSOT | `10-ssot.md` | glossary, enumerations, entities, settings, rules, metrics, document map |
| 11 architecture | `11-architecture.md` | context, the platform measured, quality attributes, containers, flows, integrations, stack and ADR-1–8 — **PROPOSED** (D19) |
| 12 technical design | `12-technical-design.md` | screens, content model, state machines, jobs, connector and adapter interfaces, drafting, i18n, operations |
| 13 plan | `13-implementation-plan.md` | six milestones, 33 issues with a Definition of Done, blocked register, risks, release scope |
| 14 token map | `14-token-map.md` | tokens and components → GDS + Mantine; contrast computed |

Rendered by `build.py` (`python3 business-direct/docs/build.py`); gate `python3 business-direct/check.py`
(also run by the root `check.py`). Data: `python3 business-direct/data/fetch-yourfield.py`
(client) and `fetch-sportolok.py` (reference).

## Process log

**2026-09-19 — stage 0–2.** The owner named the product, chose three views, all four
automations, real platform data and the DiscountDirect family (D1–D5), then widened the
shape with two reference videos: the one-person machine with optional AI, an
intelligence dashboard and integrations (D6). The Hungarian instance was measured and
pulled (431 listings); the videos read from 42 extracted frames; the research written
with its sources. Tokens proposed (D8) and the design-system page built as gate 1.

**2026-09-19 — gate 1 approved (D9).** The owner approved the design system. Components
moved into `assets/components.css` as the single source for the page and the frames.

**2026-09-19 — the first client named (D10–D12).** Everything product- and client-facing
is English; **Your Field NYC** is the first platform; the Hungarian data became the
reference. A second converter pulled Your Field's 252 providers through the public API its
own front end uses (facets, site copy, provider list and full records). The US legal
section joined the research. The "Calvus Hub" link was removed from every user-facing page
in every project. The design-system page was re-issued in English on the client's data,
tokens and components unchanged. Personas fixed on the data (D13).

**2026-09-19 — the two primary flows (D14).** The owner set the front door: B2C social
communication to acquire families, and a B2B sales flow to bring providers to manage their
own listing and more. Two components added for them (D15), reviewed with gate 2.

**2026-09-19 — gate 2 built.** Four frames from the approved components and the real
providers: platform 1440 and 390, provider 390, family 390; the layout specification with
the tablet resolution and the assumptions the open asks force.

**2026-09-19 — gate 2 approved (D16), the prototype built (D17–D18).** "Approved and
Continue." One page, three views (`../index.html`, `assets/app.js`): the platform's nine
screens (overview, social publishing with a week calendar and queue, provider sales with the
pipeline strip, sequences and reply inbox, approvals, providers with chips, search and a
detail drawer, generated pages, integrations, knowledge and rules), the provider's today and
knowledge, the family's inbox, saved and preferences. Every approval moves state: an approved
post lands on the calendar and in the family's inbox; the approved invitation moves 130
providers to *contacted* and three sample replies arrive; "Apply to manage" in the provider
view moves the persona to *managing*. Measured at 390 and 1440 (`06-build-log.md`,
`07-gate.md`); gate clean.

**2026-09-19 — presentation and technical package (D19).** `bemutato.html` in English on
the product's tokens, with the prototype previewed per view (deep links `?view=&screen=`
added to `app.js`). The technical package `10`–`14`: SSOT, architecture with eight PROPOSED
ADRs on DiscountDirect's stack, technical design with the state machines the prototype
already implements, a six-milestone plan with 33 issues and an honest blocked register,
and the token map with computed contrast. The brief's status and `tokens.css`'s header
brought current.

**2026-09-19 — tested, round 2 (D20).** The owner clicked through with no correction. Round
2 made the sequence and reply editors real and measured the tablet widths (768 and 1024)
against the layout specification — both as specified.

**2026-09-19 — consistency pass.** Gate-2 wording that still read "PROPOSED · awaits the
owner" on `layouts.html`, `05-layout-specs.md`, the design-system page's §14 and
`components.css` brought to "approved (D16)". The repo rules (`CLAUDE.md`) now list
business.direct's gate, renderer and converter; the standard notes the deep-link pattern.

**Next.** Owner asks #2–8 (`08-client-asks.md`); an ADR the owner or client flips becomes
D21; a pilot provider's real numbers would replace the last sample tiles.
