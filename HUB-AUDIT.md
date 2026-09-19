# Calvus hub — cross-project audit

*2026-09-20. Every project on the hub compared with every other and with the standard
(`PROTOTYPING.md`): what business.direct misses that another project has, what
business.direct does that the others miss, and the recommended actions. Method: the
folders, gates, docs sets and live URLs were read and counted with scripts (not from
memory); every figure below is what the tool returned. Recommended actions are PROPOSED —
the owner decides which become work, and nothing here is a presentation blocker for any
project.*

## 1. The projects, measured

| Measure | Lexodont | Lexodont (Balsamiq) | IDBC Salary Guide | DiscountDirect | Holdvölgy | business.direct |
|---|---|---|---|---|---|---|
| What it is | dental site wireframe, two fidelities | the sketch mirror | client research guide, 7 pages, real survey data | retention engine prototype, docs flat | winery site HU + EN, generated | marketing machine prototype, three views |
| Live on the hub | yes | yes | yes | yes | yes | yes |
| Docs set (standard slots) | 00–08, 10–14 (15 md) | none — mirrored by Lexodont's docs | 00, 01, 02, 04, 05, 07, 08, 10–14 (13 md; no 03, 06 — `data/SOURCES-AND-GAPS.md` stands in) | full, flat, upper-case names (15 md) + EXECUTIVE | 00–14 with per-page build logs (20 md) | 00–19 incl. 01b–01f, 09, 16–19 (24 md) |
| Decisions in the register | D1–D15 | — | D1–D27 | D1–D27 | D1–D18 | D1–D35 |
| Research with sources | none (honestly declared) | — | client documents only, 0 links | 95 linked sources | benchmarks named, **0 links** | 224 linked sources, primary marked |
| Presentation (`bemutato`) | HU | — | HU | HU | HU | EN (client's language) |
| "What we ask today" | list of asks | — | 15 open asks | 9 open asks | asks in `00-plan.md` §6 | one decision; prerequisites separate |
| Gate checks | links, anchors, docs links, fidelity parity | — | + chart-asset version, inert markers | covered by Holdvölgy's gate | + stale-phrase scan, prototype banner | + data shape, script parse, stale-phrase scan, decision range, issue count, ask references, rules map |
| Widths measured (gate doc) | 390, 1440 | — | 375 only | 375, 1024 | 390, 1024, 1440 | 390, 768, 1024, 1440 |
| SSOT rules | R1–R7 | — | R1–R11 | R1–R21 | R1–R11 | R1–R36 |
| Architecture | 5 ADRs, stack PROPOSED | — | 8 ADRs, PROPOSED | 14 ADRs, **decided** (D26) | 9 ADRs, PROPOSED | 14 ADRs, PROPOSED |
| Business logic document | no | — | no | yes (`BUSINESS-LOGIC.md`) | no | yes (`09`) |
| Unit economics / analytics | no | — | no | no | no | yes (`16`, the Economics screen) |
| Audit + SWOT of the logic | no | — | no | no | no | yes (`17`) |
| Responsible-data policy record + gate | no | — | no | no | no | yes (`18`, R26–R36) |
| Sensitive-data exposure of the domain | **health** — a dental practice; booking through a third-party embed (Flexi-Dent) | same | **personal data at registration** (consent checkbox present), salary data | **consumer offers, consent per channel** (the strongest of the four) | **alcohol** — age gate on HU and EN pages; shop with orders | families and children — covered |
| Simple / Advanced interface, help, templates | no | — | no | no | no | yes |
| Prerequisites separated from asks | no | — | no | no | no | yes (`19`) |
| Stale-phrase scan in the gate | no | — | no | via Holdvölgy | yes | yes |

## 2. What business.direct misses that another project has

| # | The other project has | business.direct today | Recommended action | Effort |
|---|---|---|---|---|
| B1 | **IDBC's gate checks inert controls** (`is-unavailable` on every button that does nothing) | inert controls exist (Connect, Choose in production) with a `.inert` class but no gate check | add check 9: every inert control carries `aria-disabled` and a title; fail otherwise | small |
| B2 | **Holdvölgy's gate checks the prototype banner** on every page | one page, one banner, no check | add check 10: the banner text is the current one | small |
| B3 | **DiscountDirect's `EXECUTIVE.md`** — a one-page executive summary with the evidence | the presentation covers the executive story; no standalone summary for a reader who wants prose, not a page with previews | write `EXECUTIVE.md` (one page: thesis, evidence, economics finding, the ask) — or decide the presentation is enough | small |
| B4 | **Holdvölgy's asset inventory** (`asset-inventory.json`, `assets-used.md`) | media comes from the cards; no inventory of what the machine may reuse | not needed until the clip engine is real; note in the plan (BD-2-7) | none now |
| B5 | **DiscountDirect's decided stack** | ADRs PROPOSED by design (D19) | correct as is; flips become D-numbers when the client accepts | none |
| B6 | **Lexodont's two-fidelity parity check** | not applicable (one fidelity) | none | none |

business.direct misses nothing structural; B1 and B2 are gate hardening that the other
projects taught.

## 3. What business.direct does that the others miss

| # | business.direct has | Who misses it | Why it matters | Recommended action |
|---|---|---|---|---|
| A1 | **Sourced research** (224 links, primary marked, link-checked) | Holdvölgy (benchmarks named, no links), IDBC (client docs only), Lexodont (none, declared) | the standard requires "benchmarks with sources"; an unsourced figure cannot be defended in front of a client | Holdvölgy: add the links to `01-research-benchmarks.md` (the sites were measured — the URLs exist); IDBC: a short market section with sources is optional (the guide is the client's data); Lexodont: nothing — its honesty is correct |
| A2 | **A responsible-data policy record and gate** (R26–R36) | every other project | each has a sensitive domain: **Lexodont — health** (a booking embed collects patient data; GDPR Art. 9 applies; the docs mention the privacy page once); **IDBC — registration** (a consent checkbox exists, but no rule says what is stored, for how long, or that no marketing follows without consent); **DiscountDirect — consumer marketing** (consent per channel is in the SSOT, but no rule on minors, vulnerable buyers, dark patterns or AI disclosure); **Holdvölgy — alcohol** (the age gate is built on both languages, but no rule on marketing to minors, the shop's age check at purchase, or the wine-club's data) | add a **policy record section to each project's `10-ssot.md`** from the framework's schema (`business-direct/docs/18-…` §2), filled for that domain; the gate row per feature follows when each project is built for real |
| A3 | **A business-logic document** with a rules map the gate checks | Lexodont, IDBC, Holdvölgy | the rules live in prose across several docs; nothing checks that every SSOT rule is stated where a reader would look | for Holdvölgy and IDBC add a short `09-business-logic.md` (Holdvölgy: shop, club, age gate, HU/EN; IDBC: paywall, registration, data updates); Lexodont: not needed (a content site) |
| A4 | **Stale-phrase and consistency checks** in the gate | Lexodont, IDBC (stale scan); all four (decision range, issue count, ask references) | the owner caught stale text four times in Holdvölgy and again in business.direct; only two gates scan for it | port the stale scan and the decision-range check to `lexodont.hu/check.py` and `idbc-salary-guide/check.py`; the issue-count check where a plan exists |
| A5 | **Four widths measured** | IDBC (375 only), DiscountDirect (375, 1024), Lexodont (390, 1440) | the standard says phone and desktop are measured, not eyeballed; the tablet width is where two-column grids break | one measured pass at 768 and 1440 for IDBC, 390 and 1440 for DiscountDirect, 768 for Lexodont — written into each `07-gate.md` |
| A6 | **"What we ask today: one decision"** with prerequisites in a separate document | IDBC (15 open asks in the presentation's register), DiscountDirect (9), Lexodont (6) | the owner's rule (D34): an ask is never a presentation blocker | re-classify each project's asks into "nothing today" + `19-implementation-prerequisites.md`; the presentations' ask sections say so |
| A7 | **Unit economics** (CAC, LTV, the next dollar) | all | only relevant where a business runs: DiscountDirect (the retention engine) and Holdvölgy (the shop and club) | DiscountDirect: an economics section (offer margin, uplift, churn) would strengthen its executive summary; Holdvölgy: shop and club economics belong to the client's numbers — a prerequisite, not our work |
| A8 | **Audit + SWOT** of the logic | all | the audit found two critical contradictions in business.direct's own rules within a day of writing them | a one-hour audit of DiscountDirect's business logic against its SSOT (27 decisions, 21 rules) is the one worth doing — it is the other project with rules |
| A9 | **Simple / Advanced interface, help, templates** | all | only for prototypes an operator runs day to day | DiscountDirect's seller console is that case: a Simple mode with recommendations is a round of work when the project resumes; the others are sites, not consoles |
| A10 | **English throughout** where the client is English | — | correct per client | none — every other client is Hungarian and their presentations are in Hungarian, which is right |

## 4. What the others do well that business.direct should keep

- **Holdvölgy's generator** (one content source → HU and EN, every page) and its **per-page
  build logs** are the model for any multi-page, multi-language site; business.direct is
  one page in one language by directive and needs neither.
- **IDBC's data converters** with the client's workbooks as arguments, output verified
  byte-identical on a re-run — business.direct's converter follows the same discipline
  (the re-pull on 2026-09-19 was diffed record by record).
- **DiscountDirect's decided stack** shows what the ADRs become once a client says yes.
- **Lexodont's honesty** ("no research was done for this project") is the right way to
  record an absence.

## 5. Findings that are not about business.direct

| # | Finding | Project | Recommended action |
|---|---|---|---|
| F1 | The IDBC asks register has 15 open items, several already answered by the client's 2026-09-18 mail round (per its process log) | IDBC | close what the mail answered; move the rest to prerequisites (A6) |
| F2 | Holdvölgy's `08 client asks` slot points at `00-plan.md` §6 rather than a numbered register with states | Holdvölgy | a `08-client-asks.md` in the standard's form, or leave and note the deviation in `07`… — the standard allows a stated deviation |
| F3 | IDBC has no `03-sources.md`; `data/SOURCES-AND-GAPS.md` is the equivalent and richer | IDBC | note the deviation in the docs index (it already names the file) — no change |
| F4 | Holdvölgy's benchmark research names the sites but carries no links | Holdvölgy | add them (A1) |
| F5 | Lexodont's docs mention the privacy page once and the booking embed twice; a dental site is health data | Lexodont | a policy record paragraph (A2) before the site is built for real; nothing for the wireframe |
| F6 | DiscountDirect's SSOT has one mention of minors and none of vulnerable buyers or dark patterns, in a system that sends timed, limited offers | DiscountDirect | the framework's rules R32 (no pressure) and R36 (no dark patterns) are exactly its risk — add them to its SSOT (A2) |

## 6. Recommended actions, prioritised

| Priority | Action | Projects | Why first |
|---|---|---|---|
| 1 | Policy record section in each SSOT from the framework schema (A2) | Lexodont, IDBC, DiscountDirect, Holdvölgy | the owner's directive: responsible data for every client, not only business.direct; each has a sensitive domain |
| 2 | Port the stale-phrase scan and the decision-range check to the two gates that lack them (A4) | Lexodont, IDBC | the owner's stated pain, twice |
| 3 | Re-classify asks into "nothing today" + prerequisites (A6, F1) | IDBC, DiscountDirect, Lexodont | the owner's rule (D34) |
| 4 | Add the benchmark links (A1, F4) | Holdvölgy | the standard's requirement |
| 5 | Measure the missing widths (A5) | IDBC, DiscountDirect, Lexodont | the standard's requirement; cheap |
| 6 | Gate hardening in business.direct (B1, B2) | business.direct | learned from IDBC and Holdvölgy |
| 7 | Business-logic documents (A3) and the DiscountDirect audit (A8) | Holdvölgy, IDBC, DiscountDirect | when each project resumes |
| 8 | `EXECUTIVE.md` for business.direct (B3) | business.direct | optional; the presentation covers it |

None of these is required to present any project. Items 1–3 change what a client would
be told; 4–8 are quality. All are the owner's call.
