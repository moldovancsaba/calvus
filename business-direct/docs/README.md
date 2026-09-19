# business.direct — project documentation

An automated marketing machine for B2B2C listing platforms — the one-person sales and
marketing team for a listed business, run by the platform, with the consumer as the
third role. First client: **Your Field NYC** (getyourfield.com). Sibling of DiscountDirect.
Built to the prototyping standard (`PROTOTYPING.md`); this index is the process log.

| Slot | File | What it holds |
|---|---|---|
| 00 brief | `00-brief.md` | Client, problem, the three views and four automations, what is real, what is inert |
| 01 research | `01-research.md` | Sourced: reputation and claiming, speed to lead, reminders, digests, generated pages, marketplace monetisation, AI adoption and human-in-the-loop, EU AI Act Art. 50, US CAN-SPAM and TCPA, the Hungarian reference market |
| 01b research II | `01b-research-acquisition-content-sales.md` | Owner's ask 2026-09-19: acquiring customers for classified media (demand and supply side), content strategies, the AI creation services to add (Higgsfield and the video / image / audio / design / scheduling landscape with prices and the labelling rules), the sales processes with benchmarks — and nine proposals P1–P9 |
| 01c research III | `01c-research-data-driven-marketing.md` | Case studies and best practices behind the data-driven decision flow: Yelp (Receptionist, Hatch $270 M, revenue per location), Angi (revenue per lead), Thumbtack, Rover; LTV : CAC and payback lines; attribution → incrementality → MMM; Booking.com and next-best-action; the map from each finding to our services; P10–P12 |
| 02 audit | `02-audit.md` | Your Field measured: API, 252 providers, field coverage, site copy; the Hungarian reference instance; the two videos frame by frame; what DiscountDirect provides |
| 03 sources | `03-sources.md` | What is real (the platform's public data), what is sample, what is inherited |
| presentation | `bemutato.html` | Standalone, English, on the product's tokens: one sentence, three numbers, the four things to click with previews, what is real, the asks, what comes next |
| 04 decisions | `04-decisions.md` | D1–D27 |
| 05 design | `design-system.html` + `../assets/tokens.css` + `../assets/components.css` | **Gate 1 approved (D9)**: tokens and components, one source |
| 05 layouts | `05-layout-specs.md` + `layouts.html` + `frames/` | **Gate 2 approved (D16)**: platform 1440 / 390, provider 390, family 390 |
| 06 build log | `06-build-log.md` | Round 1: the prototype; 1b: presentation and package; 2: editors real, tablet measured; 3: phase 2 — campaigns, upgrades, recap; 4: phase 3 — conversations; 5: economics |
| 07 gate | `07-gate.md` + `../check.py` | Measured pass at 390, 768, 1024 and 1440: overflow, tap targets, navigation, console, links |
| 08 owner asks | `08-client-asks.md` | Seven open items (#1 closed by D20; #4–6 assumed by D21 until answered) |
| 09 business logic | `09-business-logic.md` | The rules end to end: parties, flows, departments, campaigns, money, families, law, recap, what the machine never does (D24) |
| 10 SSOT | `10-ssot.md` | glossary, enumerations, entities, settings, rules, metrics, document map |
| 11 architecture | `11-architecture.md` | context, the platform measured, quality attributes, containers, flows, integrations, stack and ADR-1–10 — **PROPOSED** (D19) |
| 12 technical design | `12-technical-design.md` | screens, content model, state machines, jobs, connector and adapter interfaces, drafting, i18n, operations |
| 13 plan | `13-implementation-plan.md` | seven milestones, 40 issues with a Definition of Done, blocked register, risks, release scope |
| 14 token map | `14-token-map.md` | tokens and components → GDS + Mantine; contrast computed |
| 16 analytics | `16-analytics-and-unit-economics.md` | CAC / LTV / payback for providers, the marketing value of an avid family, content ROI, the next-dollar rule, the metrics tree, events and attribution, rules R16–R19; what is real vs assumed (D26) |

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

**2026-09-19 — phase 2 (D21–D24).** "Continue with the next phase and update all related
documentation." Asks #4–6 assumed (D21) so the phase could ship: provider campaigns and
results, the platform's upgrade products, the intelligence recap, campaigns in the family
inbox with the reason line; `09-business-logic.md` written; SSOT, architecture (ADR-9
Stripe on the platform's account, ADR-10 audiences from the platform's data only),
technical design, plan (M5), token map, layout spec, brief, asks and the presentation
updated. Measured at 390 and 1440.

**2026-09-19 — phase 3 (D25).** Conversations on both sides: the provider's inbox of
family enquiries with answers drafted from its knowledge files, the family's "ask about a
trial" that lands there and comes back answered, comments on published posts with drafted
replies. The provider's "waiting for you" corrected to show enquiries. Business logic §4b,
SSOT, architecture, technical design and plan updated.

**2026-09-19 — consistency pass after rounds 3–4.** Brief, sources, layout spec, token map,
presentation, hub and README brought to the built state; the gate gained a stale-phrase scan
(proved to fire on a planted phrase) so the next round cannot leave such text behind.

**2026-09-19 — research II.** The owner asked for research on what the market says about
acquiring customers for classified media sites, content strategies, the AI content-creation
services to add (Higgsfield and the rest), and the sales processes. Written with 60+ linked
sources, primary marked; Sora's shutdown, the four platforms' AI-label rules and the cold
e-mail benchmarks change what the plan should assume. Nine proposals (P1–P9) wait for the
owner; each becomes a D-number.

**2026-09-19 — economics (D26).** The owner asked for ROI, CAC and LTV planning for the B2B
clients, the marketing value of avid users and the analytics that let the system decide.
Built as the platform's *Economics* screen (23 editable inputs, eight tiles, the next-dollar
ranking, the quarter's funnel, a 12-month plan) and written as `16-analytics-and-unit-economics.md`
(the model, the metrics tree, the events to log, attribution, R16–R19). The defaults expose
the first real finding: outbound alone does not pay for $49 upgrades on 252 providers.

**2026-09-19 — research III and the decision flow in the presentation.** The owner asked
for the industry's best case studies and practices as the source of the data-driven
services. Written with primary filings and releases (Yelp's Q4 2025 letter, the Hatch
acquisition, Yelp Receptionist pricing, Angi's 10-K, a16z's metrics, HBR on Booking.com,
Airbnb's cluster-randomised experiments, Google Meridian); each finding mapped to a
business.direct service; P10–P12 added. The presentation gained the decision flow —
events → metrics → next dollar → approval → measure — as its own section.

**Next.** The owner's decisions on P1–P12 and asks #2–10.
