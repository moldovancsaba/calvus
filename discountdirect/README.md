# DiscountDirect — project documentation

Everything next to the prototype: the idea and its evidence, the rules, the engineering
package, and — added 2026-09-18 — the customer side that the standard structure
requires. Files stay flat in this folder (every rendered URL is live and stays); this index
maps the standard slots onto them and is the process log.

| Slot | File | What it holds |
|---|---|---|
| Presentation | `bemutato.html` | **A megrendelőnek szóló bemutató, magyarul** — mi ez, mit nézzenek, mi valódi, mit kérünk, hogyan tovább |
| 00 brief | `EXECUTIVE.md` | The executive summary: problem, service, the nine levers, benefits, phases |
| 01 research | `RESEARCH.md` | Sourced research on offers, targeting, price, and every lever beyond price (74 links) |
| 02 audit | `AUDIT.md` | What exists: the prototype measured, the documents, the outside implementation, where prototype and decisions diverge |
| 03 sources and assets | `SOURCES.md` | Where the sample data and the research come from; what is fictional |
| 04 decisions | `BUSINESS-LOGIC.md` §10 (D1–D26) and `SSOT.md` §5 | The product owner's decisions with consequences |
| 05 design | `DESIGN.md` + `GDS-TOKEN-MAP.md` | Screens, components, tokens named after GDS 6.5.0 roles |
| 06 build log | `BUILD-LOG.md` | Every build round with what was measured |
| 07 gate | `GATE.md` | What is checked, the 2026-09-18 pass, deviations |
| 08 client asks | `CLIENT-ASKS.md` | The register of asks — none open for the presentation; prerequisites in `IMPLEMENTATION-PREREQUISITES.md` |
| logic audit | `LOGIC-AUDIT.md` | The business logic audited against the SSOT, the technical design and the prototype (2026-09-20): eight findings — the e-mail legal basis in Hungary, two holdout mechanisms, no cross-channel cap — with fixes PROPOSED |
| 10 SSOT | `SSOT.md` | Glossary, enums, entities, settings, decisions, rules, metrics |
| 11 architecture | `ARCHITECTURE.md` | Context, containers, flows, NFRs, the decided stack (D26), ADRs |
| 12 technical design | `TECHNICAL-DESIGN.md` | Schema, state machines, API, algorithms, integrations |
| 13 implementation plan | `IMPLEMENTATION-PLAN.md` | Milestones, issues with DoD, blocked register, Release 1 |
| 14 token map | `GDS-TOKEN-MAP.md` | Prototype tokens → GDS 6.5.0 |

The prototype is `index.html`.

## Process log

**2026-08-25 — the prototype, in one day.** Ten commits: the seller–buyer thread with offer
cards; channels, flash campaigns and automated lists; a full screen per function with
targeting and preview; the buyer view with its own inbox and per-channel delivery samples;
sample data grown to eight buyers, 26 products, multi-year histories; the channel-aware
timeline; a build version in the top bar.

**2026-08-27 — tokens named after GDS 6.5.0 roles** (`GDS-TOKEN-MAP.md`) for a 1:1 dev
hand-off, naming only.

**2026-09-17 — the documents, in one day.** Business logic broken down for development;
executive summary and research; research extended beyond price to every buying lever;
the product owner's decisions D1–D8, then D9–D11 with the platform-template principle,
D12–D14 with the engineering package (SSOT, architecture, technical design,
implementation plan); the remaining open items decided as D15–D25 and Release 1 fixed;
the engineering docs rebased on the existing implementation stack (D26); the owner marked
the stack verified.

**2026-09-18 — standard structure.** The customer side written: `bemutato.html` (HU),
`AUDIT.md`, `SOURCES.md`, `DESIGN.md`, `BUILD-LOG.md`, `GATE.md`, `CLIENT-ASKS.md`, this
index. The first measured pass of the prototype at 375 px found 103 px of horizontal
overflow on the chat screen and 12–17 tap targets under 44 px on every screen; one
phone-width rule fixed both (v16), desktop untouched. Recorded in `BUILD-LOG.md`.

**Next.** The product owner's items in `CLIENT-ASKS.md`; DD-000 on the implementation
repo (outside this one).
