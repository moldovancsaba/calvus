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
| 04 decisions | `04-decisions.md` | D1–D34, dated, with who and why |
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

**2026-09-22 — client feedback round, studio scope only (D30–D31).** A client mail mixed
feedback on this prototype with feedback on a real backend/CMS the studio does not build
(account storage, a rich-text editor, an "editable pages" admin list, live Excel sync) —
triaged first, the backend items flagged back rather than faked (`08-client-asks.md`).
Everything in the studio's own scope fixed in one round: registration subtitle copy; the
hero crop (heads were being cut off at wide viewports — a fixed-height hero band cropping
more as the page gets wider, not a missing editing feature); Piaci trendek's chart-intro
copy and the middle two-tile CTA's width; the Ajánlatkérés header button now opens a new
in-guide `kapcsolat/` page instead of leaving the guide entirely; every green summary tile
and Excel-download CTA removed from Bérek and SAP; SAP's technológiai trendek rebuilt from
prose into tiles with its own contact card, recruitment trends kept as collapsible text
with a second contact card; the TOP3 chart's redundant per-position area sub-label dropped
(the client's "extra gray row / two position names" read); Bérek's table drops the
"Tapasztalati szint" pseudo-label on mobile; the home-office policy question kept in source
order instead of being re-sorted by percentage (D30). Separately, verified the client's
mail actually gives **two different area-naming lists** for Piaci trendek and Bérek, not
one — applied each to its own page rather than reconciling them, and caught a real bug the
rename would otherwise have caused (`terulet/index.html` joins survey data by the *old*
area names; a bridge field keeps that join working, D31). Two items already resolved on
the live prototype before this round: the Esettanulmányok "wall of text" complaint (already
a structured article layout with video placeholders, added 2026-09-18 per a client
workshop) and the Regisztráció field list (already exactly the client's list). Flagged back
to the client, not fixed here: the homepage's chamber logos/podcast/"IT doboz" (still
pending their structure demo, C-1/C-5 in `19-implementation-prerequisites.md`); two survey
questions and an "IT Contracting" salary segment that don't exist in the parsed data at all
(needs the source Excel checked — may be genuine survey segmentation, not a parsing bug);
the Expert Pool text content the client says was sent but never reached this round. Gate
clean at 390 and 1440, no console errors, no new sub-44 px targets.

**2026-09-24 — client's second look (D32), documented retroactively.** The client asked to
keep Expert Pool's size legend after all (reversing this same week's D30 removal) and drop
the raw headcount instead; the recruiting-strategy question on Piaci trendek got the same
ordinal-order fix as D30's home-office question; terulet sub-pages got a plain green header
instead of a photo hero. Shipped as commit `e59dfc2` without a documentation update at the
time — recorded here on 2026-09-25 so the register stays complete, per CLAUDE.md's rule
that documentation ships with the change regardless of which session makes the commit.

**2026-09-25 — TOP3 chart label collision, fixed at the root (D33–D34).** The client
reported labels "skewing" when TOP3 values sit close together. Verified against the
rendered SVG's actual coordinates rather than assumed: the label-declutter algorithm only
ever cascaded right from the leftmost dot, so a tight cluster's 2nd and 3rd labels drifted
40–90 px from their own dots. Replaced with a min/max-cascade average, centering a
colliding group on its natural midpoint instead — one shared function
(`assets/top3-chart.js`), so the fix reaches Bérek, SAP and Expert Pool, both chart
layouts, in one place (D33). Also found and fixed in the same pass: a long position name
(BSC's "Supply Chain / Order Management Specialist", ~298 px at the chart's font) could
overflow the wide chart's fixed 280 px row-label column, so its lowest-value dot sat on
top of the label's last letters — the column now sizes to the longest name in view. Separately
answered, not changed: the client asked whether BSC's "Sales Project Manager" showing
"Manager" underneath is Drive-editable — traced the data path and confirmed yes, that's the
bértábla sheet's own `szint` column, read verbatim (D34). Gate clean; verified with real
SVG coordinates, not just a visual glance, on Bérek (BSC and IT), SAP and Expert Pool at
390 and 1440, no console errors.
