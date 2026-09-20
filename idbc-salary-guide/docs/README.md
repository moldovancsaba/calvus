# IDBC Salary Guide — project documentation

The whole project next to the prototype: what it is, what the client gave, what was
decided, what was measured, what production needs. Each file is dated inside; this index
is the process log. Standard structure (owner decision 2026-09-18) — the same slots as
every project.

| Slot | File | What it holds |
|---|---|---|
| Presentation | `bemutato.html` | **Az IDBC-nek szóló bemutató, magyarul** — mit nézzenek, mi valódi, mit kérünk, hogyan tovább |
| 00 brief | `00-brief.md` | Two pages for a first reader: client, problem, what the prototype is, what is real, where it stands |
| 01 research | `01-research.md` | What was read (the client's specs, mockups, data, copy), the one external measurement, what was not researched and why |
| 02 audit | `02-audit.md` | idbc.hu measured; the spec vs. the data; the client's data as it stands; defects found in the material |
| 03 sources and assets | `../data/SOURCES-AND-GAPS.md` | Every source file and what it contributed, every gap, every change round with measurements — the running record since July |
| 04 decisions | `04-decisions.md` | D1–D28, dated, with who and why |
| 05 design | `05-design.md` | Where the look comes from (the client's mockups), tokens, layout |
| 06 build log | `../data/SOURCES-AND-GAPS.md` | the dated change notes are the build log |
| 07 gate | `07-gate.md` | The one-command gate, the measured pass, deliberate deviations |
| 19 prerequisites | `19-implementation-prerequisites.md` | The client's pending content deliveries, the decisions before publication (the bértábla banner first), the production-build decisions; nothing is needed for the next review (2026-09-20) |
| 08 client asks | `08-client-asks.md` | The register of asks with states — none open for the next review; the rest are prerequisites |
| 09 business logic | `09-business-logic.md` | The rules end to end — parties, the data and how a figure reaches a page, the paywall and registration, inert controls, fine-tuning, the rules mapped, what the guide never does (2026-09-20) |
| 10 SSOT | `10-ssot.md` | Glossary, enumerations, entities, settings, rules, metrics |
| 11 architecture | `11-architecture.md` | idbc.hu measured; the client's Sheets-API assumption examined; containers; **PROPOSED** stack; ADR-1..8 |
| 12 technical design | `12-technical-design.md` | Templates, content model, data pipeline, JSON slices, registration and gate, forms, media, analytics, performance, operations |
| 13 implementation plan | `13-implementation-plan.md` | M0–M6, SG-000..081 with DoD, blocked register, risks, Release 1 |
| 14 token map | `14-token-map.md` | Page tokens → one stylesheet; components → templates |


## Process log

**2026-07-30 — first build.** One combined page from the client's Drive folder: survey
trends, salary table, expert pool. Split the same day into standalone pages; the mobile
menu fixed.

**2026-07-31 — first client round.** Ordinal scales keep their order; zero-response
options hidden; benefits category filter added (later removed).

**2026-08-17 — the SAP mockup becomes the layout.** Point-line TOP3 chart built as a
shared component; dedicated SAP page; band labels per the mockup (D4, D5).

**2026-08-18 — filter semantics.** *Összes* pseudo-segment; empty combinations hidden
(D6). Documented in `SOURCES-AND-GAPS.md` on 2026-08-24.

**2026-08-24/25 — change round 2.** Eleven-area filter, then eleven area pages from one
template; the client's final area texts and names; the Finance infographic; questions
with no data hidden; the stacked chart kept for the scale questions (D8–D13).

**2026-09-01 — real per-area data.** The area pages read the client's per-area
re-tabulation; segment filters on the area pages (D15).

**2026-09-08 — final research workbook.** Survey half rebuilt; weighted-only questions;
*Összesített adatok* (D16).

**2026-09-15 — mobile.** Tables as cards below 600 px; area pages get the hamburger;
44 px tap floor (D17).

**2026-09-16 — workshop round.** SAP cards, white cards, compact chart with its own
scales; card header centring (D18).

**2026-09-18 — feedback round and the current bértábla.** Header, case studies, SAP copy,
Expert Community page, area media placeholders, registration mock, Talent Insight pill and
tiles (D19–D22). The Bérek page then showed no counts: the client's list was cut to a
reworked bértábla. The sheet became readable that afternoon and the salary data was
rebuilt from it — 13 areas, 432 rows, 37 of 39 counts (D23). Three corrections the same
day: tables always complete (D24), case studies as articles (D25), tile alignment (D26).
The owner set the rule for this phase: fix only the reported item.

**2026-09-18 — documentation standard (D27).** This folder written: brief, research,
audit, decision register, design, gate, client asks, and the technical
package `10`–`14` with every stack decision PROPOSED. The Hungarian presentation
`bemutato.html` added. `SOURCES-AND-GAPS.md` stays where CLAUDE.md rule 4 names it and
is the 03/06 slot.

**2026-09-18 — consistency pass.** Deprecated wording and comments removed after the day's
rounds (method note, area-page comments, the "edition" name, the converter's hard-coded
path) — details in `SOURCES-AND-GAPS.md`; no figure or layout changed.

**Next.** The client's structure demo for the home page; the four missing counts; the
stack decisions (blocked register in `13`).
