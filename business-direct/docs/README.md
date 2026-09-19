# business.direct — project documentation

An automated marketing machine for B2B2C listing platforms — the one-person sales and
marketing team for a listed business, run by the platform, with the consumer as the
third role. Sibling of DiscountDirect. Built to the prototyping standard
(`PROTOTYPING.md`); this index is the process log.

| Slot | File | What it holds |
|---|---|---|
| 00 brief | `00-brief.md` | Client, problem, the three views and four automations, what is real, what is inert |
| 01 research | `01-research.md` | Sourced: reputation and claiming, speed to lead, reminders, digests, generated pages, marketplace monetisation, AI adoption and human-in-the-loop, EU AI Act Art. 50, Hungarian e-mail rules |
| 02 audit | `02-audit.md` | The two reference platforms measured; the 431-listing catalogue as pulled; the two reference videos frame by frame; what DiscountDirect already provides |
| 03 sources | `03-sources.md` | What is real (the platform's public data), what is sample, what is inherited |
| 04 decisions | `04-decisions.md` | D1–D8 |
| 05 design | `design-system.html` + `../assets/tokens.css` | **Gate 1** — tokens and components rendered live, PROPOSED |
| 08 owner asks | `08-client-asks.md` | Eight items, the first being gate 1 |
| 06, 07, 10–14 | — | written when the stage arrives: build log with the first page, gate with the sweep, technical package after the direction is agreed |

Rendered by `build.py` (`python3 business-direct/docs/build.py`); gate `python3 business-direct/check.py`
(also run by the root `check.py`). Data: `python3 business-direct/data/fetch-sportolok.py`.

## Process log

**2026-09-19 — stage 0–2.** The owner named the product, chose three views, all four
automations, real sport-platform data and the DiscountDirect family (D1–D5), then widened
the shape with two reference videos: the one-person machine with optional AI, an
intelligence dashboard and integrations (D6). The two platforms were measured; the 431
listings pulled through a converter (two parse artefacts fixed: doubled category label,
Budapest county); the videos read from 42 extracted frames; the research written with
its sources. Tokens proposed (D8) and the design-system page built as gate 1.

**Next.** Gate 1 — the owner's approval of `design-system.html`. Then the two layout
frames (1440 / 390) for the platform view, gate 2.
