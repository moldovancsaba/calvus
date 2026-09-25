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
| 04 decisions | `04-decisions.md` | D1–D43, dated, with who and why |
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
| 15 idbc.hu alignment | `15-idbc-hu-alignment.md` | idbc.hu measured next to the prototype; what changes, the decisions first, the phased plan (2026-09-25, not built) |


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

**2026-09-25 — live sync built, a real converter break found first (D35).** The client
asked for sync (or at least an on-demand option) to the `IDBC_bertabla` sheet. Read the
actual live sheet before building anything — it hard-failed the converter: the `terulet`
column had been hand-retyped to the site's full display names instead of the old short
codes, plus two spelling variants. Per the owner's direct instruction, the sheet was
corrected to the prototype's canonical naming (Find & Replace, 42 + 15 cells, scoped and
case-exact) rather than the prototype adapting to the sheet; the converter was separately
hardened to tolerate either naming style so a future hand-edit can't silently break it
again. A second, unrelated break — an Expert Pool row with no headcount — now skips
gracefully instead of crashing the whole import. Re-running the corrected converter
surfaced a real, substantial update already sitting in the sheet: Expert Pool's entire
category system replaced (15 → 29 rows, a new IT/Non-IT taxonomy) and three SAP/Építőipar
position names reworded — applied as the client's actual current data. A new tab was added
directly to the live sheet requesting the two genuine remaining gaps (IT Contracting salary
rows, the missing Qualified Person headcount). `.github/workflows/idbc-sync-bertabla.yml`
(manual trigger only, gated, auto-commits on a real diff) is the ADR-2 upgrade path,
confirmed working end to end against the live sheet before being relied on.

**2026-09-25 — IDBCSYNC backfilled (D36).** The owner added an `IDBCSYNC` tab (`id`,
`változó`, `érték`, `megjelenés`, `segítség`) as the single sheet and asked for every value
the prototype uses, fully exploded. 13,160 rows went in — every page text, label, contact
and form field; every area field; the SAP catalogue; every salary, Expert Pool and Talent
Insight value; every survey percentage including each cell of the experience and
company-size breakdowns. All stored as text on purpose (as numbers, `1-5`/`6-10` answer
buckets would have turned into dates and the footer phone into a formula error). Imported
via `IMPORTDATA` from short-lived files on this project's Pages, frozen to plain values,
verified cell by cell against the source (0 mismatches, 0 formulas left), transport files
removed. Still pointing the old way, noted in the tab rather than silently changed:
`regisztracio/index.html`'s Ajánlatkérés button (the only page not yet on `kapcsolat/`).
The sync workflow still reads `WEB_BERTABLA_IMPORT`/`EXPERT_POOL_IMPORT`, not IDBCSYNC —
making IDBCSYNC the tab the site is built from is the next, separate step.

**2026-09-25 — Regisztráció's Ajánlatkérés fixed.** The one page the 2026-09-22 round missed
now opens the in-guide `kapcsolat/` page too (desktop and phone menu checked); IDBCSYNC row 7
updated to say so. No page links to `idbc.hu/ajanlatkeres/` any more (D30 complete).

**2026-09-25 — IDBCSYNC becomes the single source, synced every 15 minutes (D37).** The owner
asked for IDBCSYNC to be the source of all data on the prototype, a 15-minute sync, every other
tab hidden, the rows nobody needs to edit hidden and the technical `id` column hidden. D36's
rows could describe the site but not rebuild it, so the tab was rebuilt as one editable value
per row (17,637 rows) and the site wired to it: every visible text on the eight pages carries
a `data-sync` marker, every on-screen text in the page scripts a `/*sync:ID*/` marker, and
`data/idbcsync.py` rebuilds the data files and the page texts from the sheet, replacing both
old converters. Proven equal before it went live — the converter rebuilt the data with no
difference, and 584 home filter combinations, the 11 area pages, Bérek, SAP and Expert Pool
rendered the same HTML as the live site; the only intended visible change is the Piaci
trendek dropdown now using the areas' current names in tile order. The rows went into the
sheet through short-lived files on this project's Pages, were frozen to plain text, verified
cell by cell (0 differences) and the files removed; the sheet then shows only IDBCSYNC, with
column A and the 13,371 survey-figure and technical rows hidden, and the value column set to
plain text. The sync (`.github/workflows/idbc-sync-bertabla.yml`) runs every 15 minutes and on
demand, and refuses a sheet error before anything is published. Flagged: anyone with the
sheet's link can edit it, and so the live guide.

**2026-09-25 — idbc.hu measured; alignment plan; Phase 0 (D38).** The owner asked to learn
idbc.hu and plan the prototype's alignment with it. Home, `/go/sap/`, `/talent/`, a blog
article and `/kapcsolat/` were measured at 1440 and 375 px against the prototype
(`15-idbc-hu-alignment.md`): same colours, different typeface, scale and shell. The plan's
Phase 0 went out the same day — the footer's phone and floor corrected in IDBCSYNC to
idbc.hu's. A phone typed with a leading `+` turned into a formula error in the sheet before
any sync ran; the sync now refuses Sheets error values. The 15-minute schedule moved off the
quarter-hour marks, where GitHub had not started a single run in the first hour.

**2026-09-25 — the prototype takes idbc.hu's design (D39).** The owner asked to deliver the
alignment plan. One shared stylesheet and menu script now give all eight pages idbc.hu's
header, footer, heroes, type, buttons, cards and forms; Outfit stands in for Gilroy until IDBC
confirms the licence; the charts and pool tiles moved to idbc.hu's greens; the data
components kept their layouts and — checked across all 1,142 rendered states — every figure.
The new footer's 29 texts went into IDBCSYNC before the pages, so the sync never broke. Open
with the client: whether idbc.hu or their demos win where the two differ (A-2), the Gilroy
licence (A-1), their own photographs (C-6).

**2026-09-25 — client feedback on the published prototype (D40, D41).** Three survey
questions missing from the employer charts: the answers were in the sheet for every area; four
rows that place a question in a topic were missing. Added to `IDBCSYNC` (hidden, technical):
Home office now shows three employer questions in both question sets, AI five in the general
set, in the client's order. This corrects the 2026-09-22 answer (C-7), which said the data was
absent. The TOP3 chart's close amounts now stack upward over their own dots instead of
spreading sideways (the client's "valamelyik csússzon feljebb picit"), measured clean for every
Bérek area and SAP on phone and desktop. BSC's grey "Manager": yes, editable in the sheet
(`IDBCSYNC` row 2936, `SAL-BUSINESS-SERVICE-CENTER-BSC-039-SZINT`); not changed. Noted: two
import tabs (EXPERT_POOL_IMPORT, WEB_BERTABLA_IMPORT) were visible again in the sheet (someone
unhid them after 12:06 UTC), left as they are. GitHub has still not started a scheduled sync
run (none by 12:54 UTC, two hours after the schedule went in); the sync runs by manual
dispatch until it does.

**2026-09-25 — survey and header/footer rows hidden in IDBCSYNC (D42).** At the owner's
request: rows 3–59 (header and footer) and 111–386 (the survey section: topics, questions,
answer labels) are hidden where they stand; 3,957 rows stay visible. Values untouched, the
sync sees no change. Still no scheduled sync run by 13:10 UTC.

**2026-09-25 — IDBCSYNC sections in pastel colours (D43).** At the owner's request each of the
tab's 16 sections has its own pastel background, its heading row a deeper shade in bold; the
salary table's 13 areas alternate two aquas; row 1 is frozen. Values, hidden rows and the sync
unchanged (checked on a fresh export).

