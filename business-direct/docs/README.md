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
| 04 decisions | `04-decisions.md` | D1–D13 |
| 05 design | `design-system.html` + `../assets/tokens.css` + `../assets/components.css` | **Gate 1 approved (D9)**: tokens and components, one source |
| 05 layouts | `05-layout-specs.md` + `layouts.html` + `frames/` | **Gate 2**: platform 1440 / 390, provider 390, family 390 — PROPOSED |
| 08 owner asks | `08-client-asks.md` | Eight items, the first being gate 2 |
| 06, 07, 10–14 | — | written when the stage arrives: build log with the first page, gate with the sweep, technical package after gate 2 |

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

**Next.** Gate 2 — the owner's approval of `layouts.html`. Then the first page: the platform
overview, generated from the data.
