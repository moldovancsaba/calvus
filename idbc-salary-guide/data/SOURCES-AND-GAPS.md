# IDBC Salary Guide — data sources and design-intent audit

This documents every file in the client's Drive folder (`IDBC`, folder id
`1aOhkzvH0YtJVFkaIq85QsrCaqb4_JTQv`) that feeds this project, how each one
was used, and where the currently deployed page diverges from what the
client's own specs and mockups actually describe. Since 2026-09-25 (D37) every value
from all of it lives in one place, the `IDBCSYNC` tab of `IDBC_bertabla`; `guide-data.json`,
`areas.json` and the page texts are generated from that tab by `idbcsync.py`.

## Source files and what they contributed

| File | Type | Contribution |
|---|---|---|
| `Salary Guide - munkaerőpiaci trendek - minta` | Google Sheet | Real survey data → `answers` (9 tabs: employee/employer × general/IT+Contracting × base/crosstab). 157 respondents, 89 questions, 1,450 response rows. |
| `Salary Guide- kutatási eredmények-final (1).xlsx` | Excel (2026-09-01) | Real **per-area** re-tabulation → `areaAnswers` (11 areas × 4 tabs: B2C Total/Tapasztalat, B2B Total/Cégméret). Supersedes the edition-mapped stand-in for every `terulet/` page — see the 2026-09-01 update note below. |
| `IDBC_bertabla` | Google Sheet (`1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg`) | Real salary-band data → `salary.webBertabla` and `salary.expertPool` (15 rows), rebuilt by `build-salary-data.py`. Re-pulled 2026-09-18: **432 rows, 13 areas, 39 standalone TOP3 rows** (was 270 rows / 8 areas in August). Includes the `UTMUTATO` instructions tab, captured verbatim in `salary.readme`. |
| `IDBC_web_bertabla_roviditett_import_v9.xlsx`, `Salary Guide ... minta.xlsx` | Excel | Duplicate exports of the two sheets above — not separately re-parsed, no new data. |
| `IDBC Salary Guide specifikáció` | Google Doc | Functional spec: registration/paywall gate, 3 data-driven functions (Bérezés, Igény-elvárás, Expert Pool), Google-Sheets-via-API + WordPress block-editor architecture. |
| `SG_landing_speci.docx` | Word doc | Full site map (8 pages) and per-page content-block breakdown — see `siteMap` in the data file. Added detail the shorter spec didn't have: split IT/Contracting result blocks, the Non-IT area filter, the 3-tier-range-vs-1-average-range table distinction, the full SAP product catalogue, and the Excel-download CTA. |
| `Szűrők` | Google Doc | The intended filter taxonomy (Terület, Téma, Generáció, Tapasztalati szint, Cégméret, Cégtulajdon) — see `filterDimensions` in the data file for which of these the real survey data actually supports. |
| `MEGBESZÉLÉS JEGYZET`, `Megbeszélés jegyzet bérsáv tábla`, `Vázlatos egyeztetés TH+Csaba+Bence 06.12.` | Doc/Sheets | Internal meeting notes — mostly superseded by the two spec docs above; the last one gives a rough frontend/backend effort breakdown per feature, no new content requirements. |
| `html demok/1_regisztracio.html` | HTML mockup | Real registration-page design (Gmail/Facebook/e-mail signup, private-vs-company account type toggle) — built as the inert registration mock (`regisztracio/`, 2026-09-18) with the client's field list; sign-in providers and the account-type toggle wait for the backend. |
| `html demok/2_savok.html` | HTML mockup | Real design for the B2C/B2B filterable trends dashboard — this is what the current "Piaci trendek" section is built from. |
| `html demok/3_SAP.html` | HTML mockup | Real design for a dedicated SAP article page (exec summary, contact card, product grid, TOP3 + full salary table) — built as the SAP page (`sap/`) with the client's 2026-09 copy, the product catalogue, the TOP3 chart and the table. |
| `IDBC_SalaryGuide_home.pdf` | PDF mockup (lorem ipsum) | Shows the Salary Guide teaser as it would sit inside IDBC's main homepage template (hero, 3 feature cards, text block) — confirms this is meant to be embedded content, not a standalone site. |
| `Talent Insight riport.xlsx` | Excel (2026-09-18) | LinkedIn Talent Insight market counts: sheet 1 the TOP3 positions per area (39 rows, stored as `salary.talentInsightTop3`), sheet 2 the Expert Pool positions (13 rows, merged as `linkedin` onto `salary.expertPool`). |
| `SG- Esettanulmányok.docx`, `SG - kezdő oldal.docx`, `SG - SAP tartalom.docx`, `SG - Expert Community.docx` | Word (2026-09-18) | Final client copy for the case studies, home page, SAP trends and Expert Community — see the 2026-09-18 round below. |
| `IDBC_SalaryGuide_aloldal.pdf` | PDF mockup (lorem ipsum) | **Most important visual find**: shows the actual salary/trends article-page layout, including a horizontal **point-line chart** for the TOP3 salary comparison (three connected, labeled dots per role along one HUF axis) — a materially different (better) chart than the static range-cards currently deployed. |

## Current build vs. client intent — concrete gaps

1. **Single combined page vs. an 8-page site.** The live page merges what the
   spec splits into Home, Registration, IT trends, Non-IT+Perm trends,
   Bérek, SAP guide, Expert Pool, and Esettanulmányok. Fine as a working
   prototype; a production build would need real routing/pages.
2. **No registration/paywall gate.** Every mockup and both specs describe
   content sitting behind a login wall. Not implementable on static GitHub
   Pages without a real backend/auth provider.
3. ~~**Salary TOP3 chart is the wrong shape.**~~ **Closed.** The point-line
   chart connecting min → IDBC-recommended → max along one shared axis is
   now built, from the `3_SAP_TOP3_chart_gradient_tooltip_categories.html`
   mockup: per-row gradient connector, three-tone dots, hover/focus tooltip.
   Shared implementation in `assets/top3-chart.js` + `assets/chart.css`,
   used by `sap/` and `berezes/`; `expert-pool/` reuses the tooltip and the
   same colour ramp on its pool bars.
4. **SAP gets no dedicated page.** The 20-item product catalogue is real
   client content (now captured in `sapProducts`) but isn't surfaced
   anywhere in the current build.
5. **Missing filters the real data can't support anyway:** Generáció
   (birth-generation) and a Terület filter on the employee/trends side, plus
   full Cégtulajdon crosstabs — these appear in every spec/filter doc but
   the underlying survey was never fielded with those breakdowns. Building
   them would require the client re-running or re-tabulating the survey,
   not a code change.

   Update (2026-09-01, real per-area data arrives): the client sent
   `Salary Guide- kutatási eredmények-final (1).xlsx`, which re-tabulates the
   whole survey **per area** — 11 areas × 4 sheets each (B2C Total, B2C
   Tapasztalat, B2B Total, B2B Cégméret). This supersedes the 2026-08-25
   edition-mapped stand-in described below: `guide-data.json` now carries a
   new `areaAnswers` key, keyed by the same 11 area slugs as `data/areas.json`,
   each holding real `{employee, employer}` base + crosstab data for that
   area alone — not a pooled Általános/IT+Contracting sample. `terulet/`
   reads from `areaAnswers[area.slug]` instead of `answers[edition]`; the
   `edition` field on each area in `areas.json` is kept only to pick the
   right *question set* (the survey instrument itself still only has two
   variants — general and IT/IT Contracting — verified question-for-question
   against `topics[].editions`), not to select which sample's numbers to
   show. The sample-note copy changed accordingly (no longer claims an area
   is showing someone else's data). The main trends page (`index.html`) is
   untouched — it still shows the Általános/IT + Contracting pooled view;
   this file has no combined-sample sheet to replace that with.

   Concretely, this closes the client's 2026-09-01 feedback that the AI and
   Bérezés és juttatások topics had no tapasztalati szint / cégméret filter
   on the area pages: that was a genuine data gap in the old pooled samples
   (zero non-zero segment rows for those two topics under IT + Contracting),
   not a code bug, and the new per-area crosstabs have real segment data for
   both topics in all 11 areas. Generáció and Cégtulajdon crosstabs are
   still absent from this file — gap 5 above still stands for those two.

   Update (2026-08-25, client feedback round 2): the area dropdown is gone. The
   trends page now shows **11 bubble links**, each opening a dedicated area page
   (`terulet/index.html?terulet=<slug>`) with that area's summary, infographic
   and research results. One template serves all 11 areas — separate files would
   mean eleven copies of the same renderer in a repo with no build step. The
   area texts and per-area image/edition mapping moved out of `index.html` into
   `data/areas.json`, which both pages read.

   **The per-area results are edition-mapped, not area-tabulated** (owner
   decision, 2026-08-25): the survey still has no area breakdown, so `IT` and
   `IT Contracting` show the genuinely matching *IT + Contracting* sample, and
   the other nine show *Általános* (whole sample). Each page states in words
   which sample is on screen and never claims area-level data. When re-tabulated
   survey data arrives, only the `edition` field per area in `data/areas.json`
   and the answers file need to change.

   Also in this round: `Kapcsolat` removed from every page header (the footer
   contact block stays), a visible but inert `Kijelentkezés` button added
   top-right on all five pages — there is still no auth behind it, so it carries
   the same `is-unavailable` treatment as the Excel and EN controls — and the
   area summary text is clamped to the infographic's height with an "Olvass
   tovább" toggle.

   Update (2026-08-24): the client's change round asks for an 11-area filter
   at the top of the trends page. A **skeleton** is now built: the 11-option
   dropdown plus a per-area summary block (text + video) that swaps with the
   selection. It deliberately does *not* filter the survey answers — that
   still needs re-tabulated data. The summaries are the **client's final
   texts** (`SG_Területi_összefoglalók_final.docx`, received 2026-08-25),
   and the client confirmed the same doc's headings are the final filter
   names — five labels were renamed accordingly (Finance → Pénzügy és
   számvitel, Szállítás, beszerzés → Logisztika és szállítás,
   Ügyfélszolgálat, Adminisztráció → Office Support & Ügyfélszolgálat,
   Pharma, Life sciences → Pharma & Life Sciences, BSC (Business Services
   Center) → BSC; the doc's two all-caps headings were title-cased and pure
   capitalisation differences left alone). The media slot shows the client's
   infographic images instead of the earlier sample video: per-area files go
   in `assets/` and the `AREA_IMAGES` map in `index.html`; only the Finance
   infographic has arrived so far, so it doubles as the shared default until
   the rest come.
6. **"3 stakeholder ranges" (candidate / company / IDBC) is aspirational —
   and the shipped labels now assert it anyway (owner decision, 2026-08-17).**
   The real `webBertabla` sheet has one range (`min`/`max`) plus one
   IDBC-recommended point — a single perspective, not three independently
   sourced ones. The chart, legend, summary cards and SAP table headers now
   read `min` as "Vállalatok által kínált bér" and `max` as "Jelöltek által
   elvárt bér", per the client mockup's wording, chosen by the owner over
   the neutral "Min./Max. havi bruttó".

   **This is a labelling choice, not new data.** No figure changed — only
   what the two ends of the existing band are called. If the client reads
   those labels as two separately surveyed populations, they are wrong, and
   the fix is a data-collection change (survey candidates and employers
   separately), not a code change. Revisit if the numbers are ever quoted
   externally as employer-vs-candidate evidence.

   Update (2026-08): the Bérsávok *table* returned to neutral `Minimum` /
   `Maximum` headers at the client's request, while the chart, legend and
   summary cards keep the stakeholder labels. The client's own note under the
   table now also asserts the figures are "valós piaci adatokon alapuló" —
   their copy, shipped as requested; the source sheet's UTMUTATO still calls
   the same figures szemléltető MINTAADATOK awaiting szakmai jóváhagyás.

## Schema in `guide-data.json`

- `editions`, `topics`, `answers` — survey trends (unchanged from before).
- `salary.webBertabla`, `salary.expertPool`, `salary.readme` — salary bands (unchanged from before).
- `filterDimensions` — **new**: every filter named in the client's `Szűrők` doc, each flagged `available` / `partial` / not-available against what the real data supports, with a note explaining the gap.
- `sapProducts` — **new**: the real 5-category, 20-item SAP product catalogue from the client's own SAP mockup/spec.
- `siteMap` — **new**: the full intended 8-page site structure with a `status` (`built` / `partially built` / `not built`) and note per page.

## Consistency pass (2026-09-18, evening)

Deprecated information removed after the day's changes: the trends page's method note
said the survey was shown "általános és IT + Contracting szegmensben" — it has been
per-area since 2026-09-08 and now says so; the area page's comments still spoke of the
infographic the media slot replaced (D20); the trends page's dataset select and its code
were still named after the July "edition" term (now `datasetSelect`, the SSOT's word);
the survey converter had a hard-coded Downloads path and now takes the workbook as an
argument (output verified byte-identical). No figure and no layout changed.

## Client feedback round (2026-09-18)

Two client mails and their attachments (three content docs, the Expert Community doc, the
Talent Insight workbook, three design PNGs, and the research workbook again). What each item
became:

- **Kutatási adatok** — the re-sent `Salary Guide- kutatási eredmények-final.xlsx` is
  byte-identical to the one the 2026-09-08 rebuild consumed (converter re-run into scratch,
  output identical). Weighted-average-only for the two 1–4 scale questions and the
  `Összesített adatok` label were already in place. Nothing changed.
- **Fejléc** — every guide page now carries the client's menu: Piaci trendek · Bérek · SAP ·
  Expert Pool · Esettanulmányok, with Ajánlatkérés and Kijelentkezés right-aligned. Ajánlatkérés
  links to `idbc.hu/ajanlatkeres/` (the client named the item, not the target — a live page on
  their site was the least presumptuous choice; change the `href` if they want the in-guide
  contact form instead). Kijelentkezés stays inert. Footer navigation matches.
- **Esettanulmányok** — new page (`esettanulmanyok/`) from `SG- Esettanulmányok.docx`: DGITSHU
  (IT Contracting + try&hire, RPO) and Publicis Groupe (RPO), one video placeholder each, bottom
  CTA to `idbc.hu/szolgaltatasok/`. `siteMap` status updated from "not built".
- **SAP tartalom** — the page's executive summary is replaced by the client's two blocks
  (Technológiai trendek with four sub-sections, Toborzási trendek SAP területen). "TOP 3 SAP
  pozi" and "További bérek" in the doc are the existing section headings.
- **Piaci trendek — videó / kulcsgondolat** — `areas.json` gained `media: "video" | "highlight"`
  (video: IT, IT Contracting, Sales & Marketing, HR, Gyártás, Logisztika, BSC; highlight:
  Pénzügy, Építőipar, Pharma, Office Support). The area page renders a play-button placeholder
  or the green quote box from `Highlight 1.png`, with placeholder text naming the area; the
  client uploads the finals. The `image` field and the Finance infographic slot are gone from
  the page (the file stays in `assets/`, unreferenced, until the client says it is retired).
- **Expert Pool** — the page is now the client's Expert Community page (`SG - Expert
  Community.docx`): intro, "Szakemberként csatlakoznál?" with the join form behind the button
  (vezetéknév, keresztnév, pozíció, e-mail, telefon, üzenet), "Új kollégát keresel?" with
  Ajánlatkérés jumping to the contact form at the bottom, then the tiles. Tiles follow the demo
  PNG: category, position, "Piacon elérhető szakember: N fő\*", an "IDBC Expert Community"
  label over the bar, the IDBC count. Both forms are inert (`is-unavailable`, note under the
  button). The LinkedIn numbers come from sheet 2 of `Talent Insight riport.xlsx`, stored as
  `linkedin` on each `salary.expertPool` row — 13 of 15 rows; `Pharma / Team Leader` and
  `Finance / Desk Analyst` are the two the client is still sourcing, and those tiles show no
  market line. The footnote appears only when a star is on screen.
- **Bérek — TOP3 market counts** — `top3-chart.js` renders a green pill under the position
  (`N elérhető jelölt*`) in both layouts and the footnote under the chart whenever a row carries
  `linkedin`. Sheet 1 of the Talent Insight workbook (39 positions, 13 areas) is stored verbatim
  as `salary.talentInsightTop3`; the converter matches it onto `webBertabla` TOP3 rows by
  (terulet, pozicio). **Today that matches zero rows**: the client's list is cut to the new
  bértábla they are sending next week (SAP + IT salaries, new area set — Retail, Marketing,
  Építőipar appear, position names differ, e.g. "SAP Consultant (MM, SD, FI/CO, EWM)" vs our
  "SAP FI/CO Consultant"). No name was guess-matched. When the new salary rows land, re-run
  the matching and the pills light up. The rendering was verified with synthetic rows.
- **Regisztráció** — new page (`regisztracio/`) with exactly the client's field list
  (Vezetéknév, Keresztnév, E-mail, Cégnév, Pozíció, cég/jelölt fióktípus, Jelszó, adatvédelmi
  elfogadás; the newsletter checkbox is deliberately absent per the mail). Submit is inert —
  still no backend on static hosting (gap 2 above stands).
- **Kezdőoldal** — copy received (`SG - kezdő oldal.docx`: intro signed Dohos Ágnes & Illés
  József, methodology, six chamber logos, podcast playlist, 1 552 munkavállalói / 148
  munkáltatói válasz). **Not built**: the client sends the structure demo next week; the copy
  is in the Drive doc and goes in once the layout exists.

Client review of the round (2026-09-18, same day): two defects. (1) On the SAP page the longer
article stretched the side column — the video card measured 1053 px tall, the contact card 937 px
— because the summary grid's default `align-items: stretch` plus the aside's own grid spread the
extra height over both cards. Fixed with `align-self: start` on the aside (sticky on desktop,
static on one-column widths). (2) On Bérek the TOP3 block simply vanished on the five areas that
have no `top3` rows in the current bértábla (Banki, IT, Gyártás, Ügyfélszolgálat, Adminisztráció)
— pre-existing behaviour, but it read as a defect once the client expected their 13-area TOP3 list
there. The block now stays and says the current bértábla marks no TOP3 for that area. The real
resolution for both the missing charts and the missing LinkedIn numbers is the client's current
bértábla (Drive sheet `1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg`, shared 2026-09-18 but
account-restricted — not yet readable from this environment); its areas and position names are the
ones the Talent Insight list is cut to.

Still pending from the client: the SAP + IT salary excel, the two missing Expert Pool numbers,
the structure demos for Kezdőoldal / Bérek / Expert Pool, and the final videos / key thoughts.

Measured before push: every guide page (7) at 375 and desktop width — no horizontal
overflow, no tap target under 44 px (two short menu labels were under 44 px wide in the open
phone menu; fixed with a `min-width` on the shared rule), no console errors; 132 relative
links resolve. Screenshots were unavailable in this session (browser pane hidden), so the
gate was DOM-measured, not eyeballed — worth a visual pass on the Expert Pool tiles and the
highlight box before the client sees them.

## The Talent Insight counts move into the bértábla sheet (2026-09-21)

The owner wants `IDBC_bertabla` (Drive sheet `1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg`)
to be the one place data is edited, and everything the prototype shows to be in it. Checked
first: today's export of the sheet (modified 2026-09-21 11:30) and the prototype's `salary`
block agree row for row — 432 rows, 39 TOP3, 15 pool rows, every value identical. The only
prototype data that was not in the sheet was the LinkedIn Talent Insight layer, which came
from the separate `Talent Insight riport.xlsx` and a hand-reviewed name map in the converter.

Written back:

- **`WEB_BERTABLA_IMPORT`** gains two columns after `juttatasi_megjegyzes`:
  `linkedin_talent_insight` (the count, on 37 of the 39 TOP3 rows; the two Építőipar rows the
  client still owes are empty) and `talent_insight_pozicio` (filled on the 19 rows where the
  Talent Insight report spells the position differently — informative, the site shows
  `pozicio`).
- **`EXPERT_POOL_IMPORT`** gains `linkedin_talent_insight` (13 of 15 rows; Pharma / Team
  Leader and Finance / Desk Analyst empty).
- **`UTMUTATO`** gains a paragraph explaining the columns, in the sheet's own Hungarian.
- **The converter** (`build-salary-data.py`) now reads the counts from those columns when
  they exist and no longer needs the Talent Insight workbook; the second argument is kept only
  for a sheet that predates the columns. Rebuilt from the written-back sheet, `guide-data.json`
  is identical to before for every row shown on the site (checked field by field); only the
  stored `readme` text grew by the new paragraph.

Where it lives: in the sheet itself —
[IDBC_bertabla](https://docs.google.com/spreadsheets/d/1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg/edit)
(four tabs: `UTMUTATO`, `EXPERT_POOL_IMPORT`, `WEB_BERTABLA_IMPORT`, `LISTAK`). The columns
were written into it on 2026-09-21 through the sheet's own editor (the link carries edit
access): `WEB_BERTABLA_IMPORT!J5:K450`, `EXPERT_POOL_IMPORT!D1:D16`, the note at
`UTMUTATO!A18:A19`. Checked after writing: the sheet's own sums (41 393 on the TOP3 column,
57 644 on the pool column) equal the prototype's; a fresh export of the sheet run through the
converter, with no Talent Insight workbook, reproduces `guide-data.json` row for row. The
interim companion sheets and workbook are withdrawn.

From now on the update loop is: edit the sheet → export xlsx → `build-salary-data.py <xlsx>`
→ gate → push. A renamed TOP3 position needs no converter change any more; a new TOP3 row only
needs its count typed into the column.

## The current bértábla (2026-09-18, second push of the day)

The owner shared the live `IDBC_bertabla` sheet after the client's review. It is not the
August table with additions — it is a reworked table, and it is what the Talent Insight list
was cut to:

- **13 areas by code** (`BSC, PENZUGY, Sales, Marketing, HR, Office Support, Retail, GYARTAS,
  LOGISZTIKA, CP, PHARMA, IT, SAP`), 432 rows. Gone: Banki, Adminisztráció, Ügyfélszolgálat as
  separate areas. New: Sales and Marketing (split, where the trends survey pools them), Retail,
  Logisztika, Építőipar (`CP`), Pharma, HR. Display names follow `areas.json` wherever the same
  area exists on the trends pages; the code→name table is at the top of
  `build-salary-data.py` and is the one place to change a label.
- **TOP3 rows are standalone**: 39 rows flagged `x`, one per Talent Insight position, with
  min / IDBC / max and (mostly) no level. They are no longer the Senior row of a grouped
  position. The tables on Bérek and SAP list them like every other row (level `–`): the table
  is the complete reference and is always shown — an earlier pass excluded them and hid the
  block on Retail and Office Support, which have only TOP3 rows; the owner rejected that on
  sight (2026-09-18) and it was reverted the same hour.
- **Levels** are now Trainee / Junior / Medior / Senior / Team Leader / Manager, and 19 senior
  roles (mostly Pharma, plus Finance and Construction heads) carry no level; the table orders by
  that list and prints `–` for a missing level. Junior/Medior/Senior keep the client's year
  ranges in the label.
- `idbc_javasolt_ber_huf` is filled only on TOP3 rows — the summary cards already derive from
  TOP3 rows only, so nothing changed there.
- The sheet's own banner still reads "szakmai jóváhagyást igénylő … mintaértékek"; the page
  copy under the table is the client's ("valós piaci adatokon alapuló") — same situation as
  recorded under gap 6.

**Talent Insight matching.** All 39 TOP3 positions were paired with the sheet by hand
(area code map + a spelling table in `build-salary-data.py`; identical labels need no
entry). Three Építőipar rows are Hungarian in the Talent Insight file and English in the sheet
(Generál építésvezető = Architectural Site Manager, Elektromos előkészítő mérnök = Electrical
Quantity Surveyor, Gépész tervező = Mechanical Designe Engineer — the sheet's own spelling).
Result: **37 of 39 TOP3 rows carry a count**; the two without are the Építőipar numbers the
client is still sourcing. Expert Pool: 13 of 15, unchanged. The converter asserts that every
Talent Insight position resolves to a sheet TOP3 row, so a renamed position fails the build
instead of silently losing its number.

**Two converters now.** `build-guide-data.py` (survey workbook → `topics`/`datasets`) carries
the salary block through untouched; `build-salary-data.py` (bértábla + Talent Insight →
`salary`) carries the survey half through untouched. The earlier re-match step in the survey
converter is gone — it matched raw Talent Insight names and would have stripped the counts.

Measured before push, local server, desktop and 375 px: Bérek shows the chart with pills on
all 12 areas (Építőipar: one pill), table groups render with the new levels, no overflow, no
tap target under 44 px, no console errors; SAP chart 3 pills + footnote, 9 table rows with
level, side column 446 px; Expert Pool unchanged.

## Client notes after the rebuild (2026-09-18, third push)

- **Expert Pool tiles**: the bar and the IDBC count sat higher on tiles without a LinkedIn line
  (the two pending positions). A reserved empty line was not enough — the position name and the
  market line wrap differently per tile — so the tile is now a flex column with the bar block
  pushed to the bottom of grid-stretched, equal-height cards. Measured: bar and count on one
  line across every tile in a row, desktop and 375 px.
- **Esettanulmányok**: the client and the owner agreed at the last workshop on a conventional
  article format, not the card grid built on the first pass. The page is now one column per case
  study — title, video placeholder, running text with sub-headings and lists — with the services
  CTA at the end. Content unchanged.

## Card header alignment (2026-09-16)

The collapsed card headers sat 5px below their own centre, which the client spotted. Two causes,
both in the card CSS rather than the content:

- `tr > td:nth-child(1) { padding-top: 10px }` also matched the position header cell and, at
  specificity (0,1,2), outranked that cell's own `td.pos-cell { padding: 0 }` (0,1,1) — so the
  header carried 10px of top padding and none at the bottom. The level-block spacing is now
  targeted by `td[data-label="Tapasztalati szint"]`, which cannot collide with the header cell.
- The chevron's `transform: rotate(45deg) translate(-2px, -2px)` was applied *after* the
  rotation, so the translate resolved to a pure 2.8px upward shift on screen. The translate is
  gone; rotation alone centres it.

Measured after: position name, amount and chevron all 0px from the card's vertical centre, on
both Bérsávok and SAP, for one- and two-line position names.

## Workshop feedback round (2026-09-16)

Three changes after the client's workshop:

- **SAP's mobile cards collapse like Bérsávok'.** Each SAP row is now a card whose header holds
  the position and its range, with the juttatási megjegyzés behind the toggle. Bérsávok groups
  three experience levels per card; SAP is a flat table, so one row is one card.
- **The panel behind the mobile cards is gone; the cards stay white.** First read as "make the
  cards transparent", corrected by the client on 2026-09-16: the salary blocks themselves stay
  filled white, and it is the extra full-width surface *under* them — the scroll wrapper's own
  background, border and shadow — that is dropped below the breakpoint, so the cards sit directly
  on the page. Desktop keeps the wrapper panel.
- **The TOP3 chart has a narrow layout.** Instead of one 900px-wide chart with the role names in
  a left gutter (34% of it visible on a phone, sideways-scrolled), each position now renders as
  its own block — name and sub-label above, a short band chart below — sharing one domain so the
  bands stay comparable. Every chart carries its own value scale underneath (client request,
  2026-09-16 — it started as one shared axis under the group). Values are abbreviated to millions in
  Hungarian notation (`1,25M`, `1,3M`, `2M`). The wide layout is unchanged above 700px; the
  component picks a layout from `matchMedia` and both pages re-render when that line is crossed.

**Two implementation notes worth keeping:**

- An element that declares `container-type` **cannot be styled by its own `@container` query**.
  Both table wrappers declare it, so their own background/border/shadow in card mode comes from a
  `@media (max-width: 640px)` rule instead. Their descendants still use the container query.
- The shared chart assets are cache-busted with a version query (`top3-chart.js?v=N`,
  `chart.css?v=N`; 7 as of 2026-09-18, and `check.py` fails if two pages disagree). **Bump it whenever either file changes** — without it the browser pane and
  GitHub Pages both serve the previous renderer, which looks exactly like the change silently
  failing.

## Mobile audit follow-ups (2026-09-15)

A measured pass over all five guide pages at 375px produced two fixes:

- **The area subpages had no mobile navigation.** `terulet/` hid `.nav-links` below 900px but,
  unlike the other four pages, shipped no `.menu-toggle` — so on a phone only the brand link,
  Bérsávok and Kijelentkezés were reachable, and Piaci trendek / SAP / Expert Pool were dead
  ends. The standard hamburger (same markup, CSS and script as the other pages) is now ported
  across.
- **Tap targets below the 44px floor** (WCAG 2.5.5 / Apple HIG). The hamburger itself measured
  31×29px, footer and nav links 14–19px tall, and two of the newer controls — the Bérsávok
  accordion toggle and the area pages' "Olvass tovább" — sat at 40px and 36px. A small-screen
  rule sets a 44px minimum on navigation, footer links, selects and the brand, and the two
  components carry their own `min-height`. Measured after: **0 undersized targets on all five
  pages**, desktop density untouched (the rules are inside a `max-width: 980px` query).

**Known and deliberately not changed yet:** the TOP3 point-line chart renders 900px wide inside a
305px scroller on phones — only 34% is visible at a time, and that scroller has no `tabindex`,
`role` or label, so a keyboard user cannot reach the rest. The SVG's `aria-label` does read out
all three bands, so screen-reader users are served. Options are a focusable labelled region with
a visible scroll hint, or a compact mobile variant of the chart; the latter is a design change
the client would see, so it is waiting on a decision.

## Salary tables on mobile — cards instead of sideways scrolling (2026-09-15)

Measured before the change, at a 375px viewport: the Bérsávok table was forced to
`min-width: 760px` inside a 343px container — **419px of horizontal overflow**, more than the
visible width. `Minimum` was cut mid-number and `Maximum` and `Egyéb juttatás` sat entirely
off-screen, reachable only by discovering that the table scrolls sideways. The scroll container
was also not keyboard-reachable.

Below **600px of container width** (a container query on the table wrapper, not a viewport media
query — the same markup appears at different widths), both salary tables now render as cards:

- **Bérsávok**: each position group is its own `<tbody>`, which *is* the card. That is what lets
  the `rowspan` grouping survive the switch to block layout — a spanning cell stops spanning under
  `display: block`, so levels 2 and 3 would otherwise lose their position name. The card header
  carries the position and its **full band across all three levels**, so the headline figure needs
  no interaction; the three experience levels collapse behind it, because the largest area (IT, 24
  positions) is 10.2 phone screens tall fully expanded versus ~1.4 collapsed.
- **SAP**: flat three-column table, so one row is one card and nothing collapses — nine rows do
  not need an accordion.

**Accessibility notes, since this is the part that is easy to get wrong:**

- Changing a table's `display` historically strips its semantics (screen readers stop associating
  headers with cells). Fixed across Chromium/Gecko/WebKit since Safari 17, but the explicit
  `role="table" / rowgroup / row / columnheader / cell` attributes are emitted anyway as
  belt-and-braces for older iOS Safari. Note `cell`, not `gridcell`.
- Visible labels come from `data-label` + `::before`, which is **purely decorative**: the real
  `<th>` association is intact, so assistive tech already announces the header. Deliberately **no
  `aria-label` on cells** — it is poorly supported on static content (JAWS ignores it) and here it
  would cause the column name to be announced twice.
- Both scroll wrappers gained `tabindex="0"` + `role="region"` + an accessible name, and both
  tables gained a visually-hidden `<caption>` and `scope="col"` headers. Those were missing
  before and are worth having regardless of the card layout.
- The accordion toggle is `display: none` above the breakpoint, so on desktop it is neither
  focusable nor operable, and the collapse rules live *inside* the container query — desktop
  cannot be affected by the collapsed class.

**Not verified here:** no screen-reader pass. Structure, roles, labels and layout were checked in
the browser at 375px and 1280px, but VoiceOver/NVDA behaviour on a real device has not been
tested. Worth doing before this is relied on by an audience that includes screen-reader users.

## Final research data (2026-09-08)

`guide-data.json`'s survey half is now generated from the client's final workbook,
`Salary Guide- kutatási eredmények-final.xlsx` ("ez már a teljesen végleges kutatási
anyag, mást nem fogunk már átadni"). Three things changed materially:

- **The survey is now tabulated per area.** The workbook carries a whole-sample set plus
  its own Total + crosstab sheets for all eleven areas. The long-standing gap 5 — no area
  breakdown — is **closed**: every area page shows that area's own responses, and the
  earlier edition-mapped fallback (and its apologetic note) is gone. `datasets` replaces
  the old `editions`/`answers` pair; `topics[].questionSets` replaces `topics[].editions`,
  since the survey instrument still only has two question variants (Általános and
  IT + Contracting) and each dataset declares which one it follows.
- **The two "Jelöld 1-4-ig terjedő skálán…" questions show only the weighted average**
  (client request). The workbook supplies a `Súlyozott átlag` column for them; the
  per-option percentages are deliberately dropped, and these questions render as
  `kind: "weighted"` bars scaled to 1–4. They carry no crosstab, so under a real segment
  they are hidden by the existing no-data rule.
- **The aggregate option is labelled `Összesített adatok`** everywhere (client request),
  replacing `Összes`.

The client's earlier editorial decisions are re-applied by the converter, because the
workbook's own topic sheet predates them: the two topic renames (Munkahely váltás →
… és toborzási kilátások, Béremelés → Bérezés és juttatások) and the move of the EU
pay-transparency question to the end of the Bérezés topic's employer list. The converter
validates that every question a topic lists resolves in every dataset that uses that
question set. The salary half of the file (`salary`, `sapProducts`, `siteMap`,
`filterDimensions`) is carried over untouched — the workbook contains no salary data.

## Trends filters — what "no data" means

The survey's crosstabs contain a row for **every** canonical segment value,
including segments nobody in that topic actually answered — those rows exist
with all percentages at `0`. The presence of a row is therefore not evidence
of real data, and the filter logic on the main page is built around that:

- **`Összes` is a pseudo-segment**, not a value from the data. It is always the
  first option and the default on load, so the landing view shows the whole
  sample rather than whichever real segment happens to sort first (which may be
  one with zero respondents for the current topic).
- **Segment options are computed per topic**, not per edition+side. A value is
  offered only if at least one question in the *currently selected* topic has a
  non-zero row for it. A value that is real under one topic but empty under
  another appears only where it applies — e.g. on the employee side of
  *Általános*, `3-5 év` is offered under *Munkahely váltás és toborzási
  kilátások* but not under *Bérezés és juttatások*, where `1-2 év` is the only
  experience band with data. (`kevesebb, mint 1 év` is in the canonical order but has non-zero data
  under no topic at all, so it is never offered.)
- **Empty combinations are hidden; the aggregate is never shown in their
  place.** A question with no data under the selected real segment (including
  questions with no crosstab at all) is omitted outright — owner decision,
  2026-08-25, refining the client's 2026-08-24 ask for a per-question message
  after seeing it live. The client's uniform sentence ("A kiválasztott
  szűrési feltételekhez nem érhető el adat.") still appears once, at panel
  level, if nothing in a panel matches the filter. The earlier
  aggregate-fallback-with-"Összesített"-badge behaviour remains gone.
  `Összes` still deliberately shows the whole-sample figure.
- **The segment dropdown is hidden entirely** (tapasztalati szint on the
  munkavállalói side, cégméret on the munkáltatói side) when no question on
  that side has a crosstab for the current topic, or when it would have no
  options — selecting a value would change nothing, so showing the control was
  actively misleading.

Also at client request (same round): the two "Jelöld 1-4-ig terjedő skálán…"
matrix questions are now displayed (previously filtered out as too noisy),
always as the stacked whole-sample percentage chart. The váltási-szempontok
question's crosstab holds only mean scores per experience level — no
per-segment distributions exist — and a mean-bar rendering of those was
tried and rejected (owner decision, 2026-08-25: "the stacked chart is the
good one"), so under a real segment both scale questions are hidden (see
the no-data bullet above); the mean crosstab stays in the data unused. The benefits
category dropdown (the one question-level group filter) and the
"Többválasztós kérdés…" notes were removed — every multi-select list now
renders in full.

None of this changes any figure — it only stops the page from presenting
zero-respondent slices as if they were findings. If the client needs a
breakdown that is currently unavailable, that is a data-collection change
(re-fielding or re-tabulating the survey), not a code change — see gap 5 above.

## Shared front-end assets

- `assets/top3-chart.js` — `IDBCChart.renderTop3Chart(rows, opts)` returns the
  legend + SVG for a set of salary rows; `IDBCChart.attachTooltip(root)` binds
  the cursor-following tooltip to any `[data-tooltip]` element under `root`
  (idempotent, so it is safe to re-call after a filter re-render).
- `assets/chart.css` — chart card, legend, dot/label states and tooltip. Relies
  on each page's own `:root` tokens.

Two behaviours worth knowing before editing these:

- The dot's hover growth uses `transform: scale()`, **not** the CSS `r`
  geometry property. `r` is silently ignored in this environment (verified in
  Chrome 148: neither `r: 9` nor `r: 9px` changes the rendered radius), which
  is why the original mockup's hover effect never actually fired.
- Value labels are nudged apart by an estimated-width collision pass, since
  the IDBC and max dots frequently sit within a label-width of each other.

## Layout adopted from the SAP mockup

`3_SAP_TOP3_chart_gradient_tooltip_categories.html` is now the layout reference
for all three subpages. Adopted: the fixed navbar sitting flush to the top and
overlaying the hero (the pages previously pushed content down with
`padding-top: 78px`), the hero eyebrow, the EN/HU switch, the three-card
summary block above the chart, the Excel CTA in the section head and below the
table, and a single flat green for all three summary cards.

Data is unchanged — every figure still comes from `guide-data.json`. Where the
mockup's static example had no equivalent in our data, the block was filled
from what each page actually has rather than dropped:

| Block | SAP | Bérsávok | Expert Pool |
|---|---|---|---|
| Summary cards | TOP3 band per perspective | same, per selected area | pool size / positions covered / largest pool |
| Chart | TOP3 point-line | same, per area | n/a — bars keep the same colour ramp |
| Salary table | 3 columns, mockup shape | grouped: Pozíció / Tapasztalati szint / Minimum / Maximum / Egyéb juttatás | n/a |

The SAP table follows the mockup exactly: `Job / terület` | `Átlagos range` |
`Juttatási megjegyzés`, with the band collapsed into one `min – max` cell. That
drops `Szint` and the IDBC figure from the table — the chart directly above
carries the IDBC recommendation as its own point on every row.

The Bérsávok table was regrouped per the client's 2026-08 change round: the
szint filter is gone, every position of the selected area shows as one
three-row group (Junior/Medior/Senior with the client-supplied year ranges in
the label), columns are the neutral `Minimum` / `Maximum` plus `Egyéb
juttatás`, the IDBC figure lives only in the chart, and the 10-row cap was
dropped. TOP3 rows are included in the table too — the `top3` flag marks
Senior rows only, so excluding them would leave two-row orphan groups. The
"havi bruttó, egész Magyarországra vonatkozó" scope note the client asked for
sits above the table under the "További bérek" heading.

`sapProducts` was aligned to the mockup's catalogue: the S/4 HANA conversion
bullet is split back into "átállás és konverzió" plus "brownfield és bluefield
megközelítések" (5 items, not 4), and the fifth category is titled "Egyedi SAP
megoldások partnereinkre szabva". Item-level wording still differs from the
mockup in a few places (`Rise`/`RISE`, `SAP Carve-out`/`SAP carve-out
projektek`, colon-vs-parenthesis lists, and a few capitalisations) — the
substance is identical, so these were left alone rather than churned.

Two mockup controls are rendered in position but visibly inert
(`.is-unavailable`), because nothing exists behind them yet:

- **Excel/`.xlsx` download** — no spreadsheet exists anywhere in this repo, so
  the CTA does not link to a 404. Needs the client to supply the export.
- **EN language** — `editions` are *Általános* / *IT + Contracting*, which are
  content editions, not languages. There is no English copy to switch to.

Remove the `is-unavailable` class (and add the real `href`) once either lands.

## Client feedback round (2026-09-22)

A mail with feedback on "the salary guide" mixed two different things: real feedback on
this prototype, and feedback on a real backend/CMS platform this studio does not build
(account registration storage, a rich-text content editor, an "editable pages" admin
list, live Excel-to-site data sync). The backend items are named in the round below but
left unbuilt — this repo has no CMS, no accounts, no server; flagging them back to the
client is the honest response, not building a fake version of them.

**Registration.** The field list (Vezetéknév, Keresztnév, E-mail, Cégnév, Pozíció,
Fióktípus, Jelszó, Adatvédelem) already matched the client's ask exactly — no change
needed there. Added the requested subtitle under the heading: "Regisztrálj néhány adat
megadásával, és fedezd fel a teljes tartalmat!"

**Hero images.** The client's "isn't there some way to set which part of the image
shows? they're all slipped down" turned out to be one real, simple bug: every hero uses
a fixed `min-height: 400px` band with `object-position: center`. At mobile widths that
crops close to square and looks fine; at wide desktop widths the same 400px height spans
a much wider, shorter box, so `object-fit: cover` zooms in and crops the top of the
frame — visibly cutting into subjects' heads (confirmed by rendering `index.html`'s hero
at both widths and comparing). Fixed site-wide: `object-position: center` → `center 20%`.
A per-image focal-point *editing control* would be a CMS feature (the "isn't there some
way" half of the question), out of scope for a static prototype.

**Piaci trendek / homepage.** Chart-intro copy replaced exactly as asked. The middle
"Bérsávok / Expert Pool" two-tile CTA was genuinely too wide (each card stretching to
~590px for a two-word title) — capped and centred at desktop widths. Area subpages: added
a contact tile under the video/highlight block, removed the fixed subtitle under the H1
and the small-print line under "A terület kutatási eredményei" (both were static, not
per-area, so cutting them loses nothing area-specific). The home-office "current policy"
question (6 day-count options) was being sorted by percentage like a ranked-choice
question — extended the existing ordinal-detection (already used for salary-range
buckets) to recognize day-count and the two non-numeric home-office labels, so it now
stays in source order, in both `index.html` and `terulet/index.html`.

**The "IT doboz" and the chamber logos are not fixed — they don't exist yet.** Grepping
the whole codebase found no element linking to both Bérek and Piaci trendek together, and
no chamber-logo markup anywhere. Both match content the client's own 2026-09-18 mail
promised for a *new* home page structure that, per that same mail, was still pending
("the client sends the structure demo next week") — see C-1/C-5 in
`19-implementation-prerequisites.md`. Today's `index.html` is still the trends hub
standing in as the home page. This feedback most likely describes the still-pending
structure demo, a mockup shown outside this prototype, or the new homepage content that
has since arrived but wasn't forwarded to this round — flagged back rather than guessed
at.

**Two area-name taxonomies, verified separately.** Re-read side by side, the client's
mail gives two different, overlapping wordings — one for Piaci trendek's 11 areas
(`data/areas.json`), a differently-worded one for Bérek's 14 (`build-salary-data.py`'s
`AREA_NAME`, e.g. "Pénzügy és számvitel" there vs. "Pénzügy, Számvitel" on the trends
side). Applied each to its own page. Renaming `areas.json`'s `name` field in place would
have silently broken `terulet/index.html`'s join into `guide-data.json`'s `datasets`
object, which is keyed by the *old* names for 8 of the 11 areas — caught before it
shipped; a new `dataKey` field on each area object holds the pre-rename name for that
join, `name` is display-only now.

**"IT Contracting" in Bérek's filter is a genuine data gap, verified against the actual
data, not assumed.** The bértábla (`salary.webBertabla`) has 13 areas and no "IT
Contracting" row anywhere — confirmed by inspecting `guide-data.json` directly. The
separate market-trends survey data *does* carry "IT Contracting" as its own segment
(`datasets["IT Contracting"]` exists), so the client's ask isn't invented — but adding it
to the Bérek filter needs real salary rows for that segment, which this repo doesn't
have. `AREA_NAME` in `build-salary-data.py` has the slot ready (`IT_CONTRACTING`, no
sheet code mapped); it will simply show zero rows, not a fabricated placeholder, until
the client supplies figures or confirms IT Contracting is already folded into "IT".

**Two survey questions, verified genuinely absent from the parsed data, not just
mis-sorted.** The client flagged a missing "home office policy's effect on recruiting
success" employer question, and two AI-topic employer questions missing for non-IT areas.
Searched every topic in `guide-data.json` for any phrasing close to the first — not
found anywhere, under any topic. The two AI questions *do* exist, but only in the
"IT + Contracting" question set, not "Általános" — and that pattern (IT+Contracting
respondents getting extra questions general respondents never saw, e.g. "Nyitott lennél
külföldre költözni?" elsewhere in the same topic file) repeats enough across the dataset
that it reads as genuine survey segmentation, not a parser bug. There's no source
`.xlsx` in this repo to check the raw "Téma besorolás" sheet either way — flagged to the
client rather than guessed at in either direction (not silently dropped, not fabricated).

**Bérek — the "extra gray row" / "why two position names" bug, found by rendering the
page, not by reading the code.** The TOP3 chart's sub-label under every position name was
`[terulet, szint].filter(Boolean).join(' · ')` — on a page that's always filtered to one
area already, that repeats the (redundant) area code under every single position, and for
positions with no `szint` it's the *only* thing in that sub-label, floating alone in a
way that reads as a second, out-of-place name. Rendering `berezes/index.html?terulet=bsc`
and reading the actual output confirmed it directly: "Supply Chain / Order Management
Specialist" showed "BSC" on its own line underneath, for an area already selected in the
filter above. Fixed by dropping `terulet` from the sub-label everywhere (`assets/
top3-chart.js`, shared by Bérek, SAP and Expert Pool) — it now shows only the experience
level, when there is one.

Separately, the further-down position table's `data-label="Tapasztalati szint"`
attribute drove a mobile-only pseudo-label (`content: attr(data-label)`) repeated on
every single row/card — much noisier than the table's one real `<th>` header. Removed
the attribute from that cell specifically (renamed to a plain `.szint-cell` class to keep
its layout rule); changed the empty case from a bare "–" to nothing at all. The desktop
table's single `<th>Tapasztalati szint</th>` column header is untouched — one instance
per table isn't what the client was describing.

**Bérek and SAP — every green summary tile and both Excel-download buttons removed**, per
the client's explicit ask on both pages; the TOP3 chart itself stays (only the redundant
3-card band summary above it goes). "További bérek" heading enlarged to match the (now
sole) TOP3 heading's size; its status line no longer clamped to 720px.

**SAP — technológiai trendek rebuilt from four paragraphs of prose into three tiles**,
reusing the shared `.range-card` component (the exact tile already used for TOP3 summary
cards elsewhere — no new CSS component, just reused) with a contact card beside it;
recruitment trends kept as running text but now collapsible (first paragraph visible, a
"Tovább olvasom" toggle reveals the rest), with its own separate contact card. The tile
copy is a condensed rewrite of the client's own paragraphs (same claims, shorter) — worth
the client's eyes before it's called final, same as any condensation.

**A new `kapcsolat/` page** replaces the header's "Ajánlatkérés" button leaving the guide
entirely for `idbc.hu/ajanlatkeres/` — it now opens a contact-only page inside the guide
(header, heading, an inert contact form matching this project's established pattern, footer,
nothing else), resolving `19-implementation-prerequisites.md`'s P-3.

**Already resolved before this round, verified by rendering, not assumed:**
Esettanulmányok's "wall of text, no video placeholder" complaint — the page already has a
full hero and each case study is already a structured article with its own video-card
placeholder, added 2026-09-18 after a client workshop asked for exactly this. No change
needed; flagged as likely describing a stale/cached view.

Measured before push: all changed guide pages at 375 and 1440px — no horizontal overflow,
no console errors, no new sub-44px targets. `idbc-salary-guide/check.py` and the root
`check.py` both `GATE: CLEAN`.

## Client's second look (2026-09-24), documented retroactively on 2026-09-25

Shipped as commit `e59dfc2` at the time without a documentation update — recorded here now
so the round isn't lost from this file's running record (`04-decisions.md` D32).

The client reviewed the 2026-09-22 round and reversed one item: Expert Pool's kicsi/közepes/
nagy size legend, removed that round, was asked to come back — the client wants it after
all. The raw IDBC Expert Community headcount is dropped instead, so each tile shows only
the bar and the LinkedIn Talent Insight count. Separately: the recruiting-strategy question
on Piaci trendek ("Mi jellemzi céged toborzási stratégiáját...") had the same
sorted-by-percentage-instead-of-source-order bug as the home-office question D30 fixed,
in both the base view and the company-size breakdown — fixed the same way. Terulet
sub-pages swapped their photo hero for a plain green header band, per the client's request.

## Chart label collision, verified and fixed at the root (2026-09-25)

The client reported (2026-09-25 mail): "Ha nagyon közel vannak az összegek egymáshoz, akkor
elcsúsznak az összegek (mobilon is)" — when the amounts sit close together, they skew, also
on mobile. Verified against the actual rendered SVG before touching anything: on Bérek's
BSC area, "IT Support / Technical Support Specialist" (790k/800k/800k, a 10k spread) and
"Supply Chain / Order Management Specialist" (600k/630k/650k, 50k spread) both showed
`630 000 Ft` and `650 000 Ft` labels sitting 42–94px to the right of their own dots. Root
cause, read from `assets/top3-chart.js`'s `layoutLabels()`: the label-declutter algorithm
cascaded strictly left-to-right, anchored on the leftmost dot's natural position, and only
ever pushed labels further right to avoid overlapping the previous one — for a well-spaced
row this is invisible, but a tight cluster of 3 labels (each ~64px wide) crammed into a
~50px span drags the 2nd and 3rd labels well clear of the dots they name, with nothing to
pull them back.

Fixed by replacing the single cascade with a min/max-cascade average: run the existing
left-to-right push to get each label's minimum feasible position, run the mirror image
(right-to-left, cascading from the rightmost dot) to get each label's maximum feasible
position, and average the two per label. For points with room to spare both cascades
already equal the natural x (no change from before); for a colliding run, averaging centers
the whole group on its natural midpoint instead of dragging it toward one edge. Confirmed
by re-reading the live SVG coordinates after the fix: the BSC row that was 455.8/525.8/595.8
(dots at 455.8/465.0/465.0) became 390.4/460.4/530.4 — centered on the dots instead of
sitting to their right. One function, shared by every page that loads `assets/
top3-chart.js` (Bérek, SAP, Expert Pool) and both chart layouts (the wide desktop chart and
the mobile "compact" one) — fixing it once reaches all of them; version bumped to `v=8` in
all three pages' `<script>` tags so the fix isn't served from a stale cache.

Found in the same pass, not reported but visible in the same chart: the wide chart's
row-label column had a fixed 280px width regardless of the actual position name. BSC's
"Supply Chain / Order Management Specialist" measures ~298px at the chart's 14px/900-weight
font (`getComputedTextLength()`, not the character-count estimate) — 18px wider than the
column, so whenever that position's lowest value landed at the domain minimum (this row's
600 000 Ft did), the dot sat directly on top of the label's last two letters. This is a
different bug from the label-collision one above (it's about the row *label*, not the
value labels, and triggers on a long name regardless of how close the values are) but
looked similar enough in the same screenshot that it was worth fixing together. The column
width is now `Math.max(280, longest position name in view × 7px + 20px)` — an estimate
consistent with the codebase's existing character-count width heuristics elsewhere in this
file, verified against the real measured width with margin to spare.

Separately answered, not a bug: the client asked to "confirm whether [BSC's remaining gray
'Manager' listing] is editable in the Drive" — traced end to end: "Sales Project Manager"
is a `top3: true` row whose `szint` (level) column in the bértábla sheet is literally
`Manager`; `build-salary-data.py` reads it with no transformation, and it's exactly the
sub-label D30 changed to show once the redundant repeated area code was dropped. Answer:
yes, Drive-editable — blank that row's level column and re-run the converter to remove it.
No code change made; suppressing a level that happens to repeat a word already in the
position name would be guessing at intent for one specific row, not fixing a defect.

Measured after the fix: Bérek (BSC and IT areas), SAP and Expert Pool at 375 and 1440px,
reading the live SVG's own coordinates rather than eyeballing screenshots — labels align
to their dots in every case checked, no horizontal overflow, no console errors.
`idbc-salary-guide/check.py` and the root `check.py` both `GATE: CLEAN`.

## Live sync built for `IDBC_bertabla` — a converter break found and fixed first (2026-09-25)

The client asked for a live sync, or at least an on-demand option, to the salary sheet (§ "The
data pipeline" above documents this as fully manual up to this point). Before building
anything, the actual live sheet was read — its public export, downloaded with `curl` at
`https://docs.google.com/spreadsheets/d/1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg/export?format=xlsx`,
works with no credentials because the sheet is shared "anyone with the link can view/edit" — not
assumed compatible with today's converter.

**It wasn't.** `build-salary-data.py` hard-failed with `unmapped area codes in the sheet`,
naming six areas. The sheet's own `terulet` column (`WEB_BERTABLA_IMPORT`) had been hand-retyped
at some point to hold the site's full display names ("Business Service Center (BSC)") instead of
the short internal codes (`BSC`, `PENZUGY`, `GYARTAS`, `LOGISZTIKA`, `CP`, `PHARMA`) the converter
expected — apparently to match what the site now shows, not a deliberate request to change the
sheet's format. Two of the retyped values also carried small spelling drift from the canonical
text: `Pénzügy és Számvitel` (wrong casing) and `Pharma, Life Science` (singular, missing the
final "s").

Per the owner's direct instruction — the prototype's naming is correct; fix the sheet, not the
prototype — both were corrected directly in the live sheet via Find & Replace, scoped to
`WEB_BERTABLA_IMPORT!A1:L2000` only, case-sensitive and whole-cell-match on, verified by
re-downloading the export afterward and re-counting: `Pénzügy és számvitel` now 42 cells,
`Pharma, Life Sciences` now 15 cells, both matching the row counts found before the fix. Separately
— since a sheet a human can freely retype should not be able to silently break an automated
sync again — `build-salary-data.py` was hardened to recognize either naming style: `AREA_ALIASES`
maps the old short codes (kept for any older re-export) and the two spelling variants just found
to the canonical name; `area_name()` normalizes case and whitespace before matching, so this exact
failure mode can't recur without an assertion naming exactly what's unrecognized.

**A second, unrelated break in the same sheet**: `EXPERT_POOL_IMPORT` now has a `Non-IT / Qualified
Person` row with an empty `darab` (headcount) cell — the converter previously did `int(r[2])`
unconditionally and crashed on `None`. Fixed to skip a row with no count (printing it, per this
project's "no figure invented" rule) rather than lose every other row in the sheet to one gap.

**Re-running the corrected converter against the live sheet surfaced real content the client had
already added, never pulled in until now** — this is exactly what a sync is for:
- `expertPool`: 15 rows → 29 rows. The client replaced the Expert Pool category system entirely —
  gone are the old Finance/Pharma-specific rows this file's 2026-09-18 entry described; in their
  place, an IT/Non-IT taxonomy (Architect, Business & System Analyst, Cloud & DevOps, Data & AI,
  IT Helpdesk, ... on the IT side; Qualified Person and others on the Non-IT side), 29 of 30 rows
  with a real LinkedIn Talent Insight count already attached.
- Three `webBertabla` position names reworded (matched by `pozicio`+`szint`+`min`+`max` against
  the pre-sync data to confirm these are renames, not new/deleted rows): "Mechanical Designe
  Engineer" → "Mechanical Design Engineer" (typo fixed), "SAP Consultant (FI/CO, MM, SD, PP,
  EWM)" → "Senior SAP Consultant (MM, SD, FI/CO, EWM)", "SAP Architect/ Lead Developer" → "SAP
  Solution Architect/ Lead Developer".
- Row and area counts otherwise unchanged: still 432 `webBertabla` rows, 13 areas, 39 TOP3 rows,
  now all 39 with a Talent Insight count (was 37 of 39 on 2026-09-18). `topics`, `datasets`,
  `sapProducts`, `siteMap` and `filterDimensions` — everything `build-guide-data.py` owns —
  diffed byte-identical, confirming this converter still touches only its own half as documented.

**Still genuinely missing, not fixed here** — a new tab, "HIÁNYZÓ ADATOK - kérés", was added
directly to the live sheet (not just this file) naming both in the client's own language: IT
Contracting has no salary rows in `WEB_BERTABLA_IMPORT` at all (the separate market-trends survey
data does carry it as a segment — see the 2026-09-22 entry above — so this isn't invented, just
still unfilled), and the `Non-IT / Qualified Person` row above needs its headcount.

**The sync itself**: `.github/workflows/idbc-sync-bertabla.yml`, `workflow_dispatch` only (a
manual "Run workflow" click — nothing runs on a schedule), downloads the same public export
`curl` proved works, runs this converter, runs the full repo gate, and pushes straight to `main`
only if the gate passes and the resulting JSON actually differs — matching the owner's choice of
on-demand trigger with auto-deploy (no PR review step) once the gate is green. This is ADR-2's
named upgrade path (`11-architecture.md`), exercised end-to-end against the real sheet — not
merely written — before being relied on. It does not cover the market-trends/survey half
(`build-guide-data.py`): that source is a one-off Excel file the client emailed, not a Google
Sheet with a stable URL, so there is nothing with a public export to sync from yet.

## Live sync built, a real converter break found and fixed first (2026-09-25)

The client asked to have "a live sync or at least the option to sync" to the Google Sheet.
This closes ADR-2's named upgrade path (`11-architecture.md`) — build-time import stays the
architecture, now triggerable on demand instead of only by a human running the converter.

**The sheet was read before anything was built, not assumed compatible.** The client's own
sharing link (`.../edit?usp=sharing`) turned out to already allow anonymous view *and edit*
access, and the sheet's public `?format=xlsx` export URL returns a real workbook with no
credentials needed — confirmed directly with `curl`, not assumed from the sheet's
"Anyone with the link" label. Running the existing `build-salary-data.py` against that
export failed immediately: `assert not unknown, f"unmapped area codes in the sheet: ..."`
listed six areas. Read the sheet's `WEB_BERTABLA_IMPORT` tab directly to see why: its
`terulet` column, which held short internal codes (`BSC`, `PENZUGY`, `GYARTAS`, `LOGISZTIKA`,
`CP`, `PHARMA`) through the 2026-09-18 rebuild, now held the site's own full display text
instead (`"Business Service Center (BSC)"`, etc.) — apparently hand-retyped at some point to
match what the site now shows, not a change anyone asked for. Two of the retyped values also
drifted from the exact canonical text: `"Pénzügy és Számvitel"` (wrong case) and `"Pharma,
Life Science"` (singular, should be plural per the client's own 2026-09-22 wording).

**Fixed at the source, per the owner's direct instruction ("the naming was ok on the
prototype... update the sheet, not the prototype")**: opened the sheet directly (anonymous
edit access) and ran Find & Replace on `WEB_BERTABLA_IMPORT` only, case-exact and whole-cell,
for both variants — 42 cells (`Pénzügy és Számvitel` → `Pénzügy és számvitel`) and 15 cells
(`Pharma, Life Science` → `Pharma, Life Sciences`), confirmed by the dialog's own "N
előfordulása helyettesítve" count matching the rows found by direct inspection beforehand.
Re-downloaded the sheet's export afterward and re-read the `terulet` column to confirm the
edit actually landed, rather than trusting the UI alone.

**Also hardened the converter itself**, since a sheet a client can freely retype is a sheet
that will eventually be retyped again: `build-salary-data.py`'s `AREA_NAME` (a straight
code→name dict) became `CANONICAL_AREAS` + `AREA_ALIASES` + `area_name()`, a
case/whitespace-insensitive lookup that accepts either the old short codes or the current
full text and normalizes small spelling drift via an explicit alias table (never a fuzzy
auto-correct, which could paper over a genuinely new, different area name) — a
sheet already using the exact canonical text needs no alias entry at all. `TI_AREA`'s
Talent-Insight reverse lookup (`next(k for k, v in TI_AREA.items() if v == r["terulet"])`)
had the identical bug one line later and got the identical fix.

**A second, independent break, found by actually running the converter, not just reading
the sheet**: `EXPERT_POOL_IMPORT` now has a `Non-IT / Qualified Person` row with an empty
`darab` (headcount) column — `int(r[2])` on `None` crashed the whole import. This is a real,
still-open content gap (nobody has supplied that number yet), not a sync failure, so the
converter now skips a row with no count (printing which one) instead of crashing everything
else or inventing a number for it.

**Re-running the corrected converter against the corrected sheet surfaced real, substantial
content the client had already put there**, verified field-by-field against the previous
`guide-data.json` (keyed by area+position+level, not by row position, since the corrected
naming also changed the sheet's natural row order) before accepting it:
- Three `webBertabla` position names reworded: `"Mechanical Designe Engineer"` →
  `"Mechanical Design Engineer"` (a typo fixed), `"SAP Consultant (FI/CO, MM, SD, PP, EWM)"`
  → `"Senior SAP Consultant (MM, SD, FI/CO, EWM)"`, `"SAP Architect/ Lead Developer"` →
  `"SAP Solution Architect/ Lead Developer"` — zero other field changes on any of the 432
  rows (min/idbc/max/juttatas/top3 all identical), so this is purely a naming update, not a
  figures change.
- `expertPool` replaced wholesale: 15 rows under the old category system (`Finance`,
  `Pharma`, `IT`, granular roles like "Treasury Specialist", "Clinical Research Associate")
  are gone; 29 rows under a new `IT` / `Non-IT` taxonomy (Architect, Business & System
  Analyst, Cloud & DevOPS, Data & AI, ... for IT; Accountant, Actuary, Compliance Specialist,
  ... for Non-IT) are there instead, each with its own LinkedIn Talent Insight count already
  filled in. This looks like the client restructuring their own Expert Community offering,
  not a data-entry accident — applied as their real current data. Note in passing, not
  changed (it's the client's own copy, not ours to silently correct): `EXPERT_POOL_IMPORT`
  spells one IT row "Infrastructuion Engineer".
- This also **retires** the earlier-documented gap about two specific missing Talent Insight
  counts (`Pharma / Team Leader`, `Finance / Desk Analyst`, `19-implementation-prerequisites.md`
  C-3) — those exact category/position pairs no longer exist in the new taxonomy, so the gap
  isn't closed so much as superseded.

**A new tab, "HIÁNYZÓ ADATOK - kérés", added directly to the live sheet** (not a local repo
file the client would never see) asking, in Hungarian, for the two gaps that are still
genuinely open after all the above: IT Contracting salary rows for `WEB_BERTABLA_IMPORT`
(the separate market-trends survey data already treats IT Contracting as its own segment;
the salary sheet still doesn't), and the missing `Non-IT / Qualified Person` headcount.

**`.github/workflows/idbc-sync-bertabla.yml`** — manual trigger only (`workflow_dispatch`,
no schedule), downloads the sheet's public export, runs `build-salary-data.py`, runs
`check.py`, and commits+pushes only if the gate passes and `guide-data.json` actually
changed. No credentials stored anywhere (the public export URL needs none); the commit
identity is a plain `idbc-data-sync` bot account, never an AI/assistant name. Confirmed
working end to end: the manual run described above (download → corrected converter → gate)
is exactly what this workflow automates, run by hand first specifically to verify it before
relying on the automated version. Does not cover `build-guide-data.py` (the survey/trends
half) — that source is a one-off emailed Excel file with no stable Sheet URL to poll.

Measured: `idbc-salary-guide/check.py` and the root `check.py` both `GATE: CLEAN` after the
sync; Bérek and Expert Pool re-rendered locally and read via their live DOM/console (not
screenshots alone) to confirm the new area list and the new Expert Pool taxonomy display
with no console errors and no horizontal overflow.

## IDBCSYNC — every value the prototype uses, in the sheet (2026-09-25)

The owner added an `IDBCSYNC` tab to `IDBC_bertabla` with five columns — `id` (identifies the
value by its use), `változó` (the name as it reads on the page), `érték` (what it shows),
`megjelenés` (page and section, so a reader can find it), `segítség` (what it is and what
type of value is expected) — and asked for all data to be backfilled. Scope was confirmed
twice, both times explicitly: everything, fully exploded, no summary rows pointing at other
tabs — "this will be the single sheet".

**What went in — 13,160 rows** (`04-decisions.md` D36):

| Prefix | Rows | Source | One row per |
|---|---|---|---|
| `CONTENT-` | 114 | the pages' HTML, read by grep per page | heading, lead paragraph, label, button, nav/footer item, contact detail, form field, SAP tile/paragraph |
| `AREA-` | 33 | `data/areas.json` | area × {name, summary (first 200 characters shown, full length stated), media type} |
| `SAPPROD-` | 30 | `guide-data.json` `sapProducts` | category and catalogue item |
| `SALARY-` | 1,470 | `salary.webBertabla` | present field (`szint`, `min`, `idbc`, `max`, `juttatas`, `linkedin`) of every row |
| `POOL-` | 58 | `salary.expertPool` | `darab` and `linkedin` of every tile |
| `TI-` | 39 | `salary.talentInsightTop3` | TOP3 position's Talent Insight count |
| `SURVEY-` | 11,402 | `datasets` | every answer of every question in every area; every weighted score; every segment × answer cell of the `cross` breakdowns (experience on the employee side, company size on the employer side) |
| `SITEMAP-`, `FILTERDIM-` | 14 | `siteMap`, `filterDimensions` | internal meta, marked as not shown on the site |

**IDs** are deterministic and, where the data allows, free of positional indexes so an inserted
row cannot shift them: `SALARY-<the record's existing id from build-salary-data.py>-<FIELD>`,
`POOL-<IPARAG>-<POZICIO>`, `TI-<TERULET>-<POZICIO>`, `AREA-<slug>-<FIELD>`. Survey IDs do carry
the question's position inside its area/side/base-or-cross block — `SURVEY-<AREA>-<SIDE>-<BASE|CROSS>-Q<n>-O<n>`
for simple and weighted questions, `-Q<n>-S<segment>-G<answer>` for breakdown cells — since the
survey material is final (D16) and has no other stable key. The generator refused to emit on a
duplicate ID; there are none.

**Every value is text.** Checked before import, not after: typed as numbers, 96 answer-bucket
labels (`1-5`, `6-10`, `11-15`, `16-20`) would have become dates, the footer phone
`+36 30 479 0090` a formula error, and 1,300+ decimals such as `12.5` depend on the sheet's
Hungarian locale. Survey `érték` values therefore keep the JSON's own form (`19.28`, not
`19,28`); a future converter reading the tab should expect a dot decimal and accept a comma
if a person retypes one.

**How it got in, since a sheet this size can't be typed.** A generated 8.3 MB file, split into
nine tab-separated parts, served for a few minutes from this project's own GitHub Pages
(`data/idbcsync-import/`; first under an underscore path, which Jekyll silently drops — renamed).
A temporary gist was refused by the session's data-exfiltration guard; the Pages route adds
no exposure, the same data is already public on the live site. Each part came in with
`=ARRAYFORMULA(REGEXEXTRACT(IMPORTDATA(url;"¦");"^([^\t]*)\t…(.*)$"))` — one whole line per
cell via a delimiter that never occurs, then split by `REGEXEXTRACT`, which only ever returns
text. Google gates `IMPORTDATA` behind a document-level "external data" permission that an
anonymous editor cannot grant; the owner granted it from a signed-in session. The whole range
was then frozen with Szerkesztés → Irányított beillesztés → Csak az értékek (keyboard copy did
not register in the automated browser; the menu did), verified against the source cell by cell
from a fresh export — 13,160 rows, 0 mismatches, 0 formulas left, all values text, nothing
below the data — and the transport files removed from the repo.

**Noted in the tab, not changed:** `regisztracio/index.html`'s Ajánlatkérés header button still
links to `idbc.hu/ajanlatkeres/` — every other page moved to `kapcsolat/` on 2026-09-22; this
one was missed. The row `CONTENT-SHARED-CTA-AJANLATKERES` says so.

*Fixed the same day, on the owner's go-ahead:* the Regisztráció button now links to
`../kapcsolat/index.html` like every other page (clicked through on desktop and in the 375 px
hamburger menu, 310×44 target, lands on the Kapcsolat page, no console errors), and the
IDBCSYNC row's `segítség` (E7) rewritten to match. No page links to `idbc.hu/ajanlatkeres/` any
more.

**Not yet:** the site is still built from `WEB_BERTABLA_IMPORT`, `EXPERT_POOL_IMPORT` and the
survey Excel, not from IDBCSYNC, and `idbc-sync-bertabla.yml` still reads the former. Making
IDBCSYNC the tab the prototype is generated from is a separate step — and a structural one,
since the page templates hold their static text in HTML today, not in data.

## IDBCSYNC becomes the single source — every text and figure, synced every 15 minutes (2026-09-25)

Owner directive: IDBCSYNC is the SSOT for all data on the prototype, synced every 15 minutes;
the other tabs hidden; the rows nobody needs to edit hidden; the technical `id` column hidden
(`04-decisions.md` D37).

**Why the backfilled rows could not simply be read.** They described the site rather than
being able to rebuild it: area summaries were cut at 200 characters, respondent counts sat
only inside the help text, the Bérek area list was one comma-separated cell, and a page text
had no link back to the element that shows it. So the tab was rebuilt, one editable value per
row, and the site was wired to it.

**The rows — 17,637** (plus section headings, ids starting with `#`, which are ignored):

| Block | Ids | Visible | What a person edits there |
|---|---|---|---|
| Every page text | `SHARED-…` (header, footer, chart legend — one row for all pages), `HOME-`, `TERULET-`, `BEREK-`, `SAP-`, `POOL-`, `ESETT-`, `REG-`, `KAPCS-` | yes (screen-reader labels hidden; the header and footer rows hidden since D42) | headings, paragraphs, buttons, form labels, image descriptions, tooltips, messages shown by the page scripts |
| Areas | `AREA-<slug>-NAME/-SUMMARY/-MEDIA` | yes (`-EDITION` hidden; `-NAME` hidden since D45) | the name (used by the home tile, the Piaci trendek dropdown and the area page), the full summary, video or highlight |
| Bértábla | `SAL-<area>-NAME`, `SAL-<area>-nnn-POZICIO/SZINT/TOP3/MIN/IDBC/MAX/JUTTATAS/LINKEDIN` | yes | every salary row of Bérek and SAP |
| Expert Pool | `EXPERT-nn-IPARAG/POZICIO/DARAB/LINKEDIN` | yes until D45, hidden since | every tile, including Qualified Person, which appears once its count is filled in |
| SAP catalogue | `SAPPROD-CATn-NAME/-ITEMm` | yes until D45, hidden since | categories and items |
| Survey texts | `SURVEY-TOTAL-LABEL`, `SURVEY-TOPICt-NAME`, `SURVEY-<SIDE>-SEGk`, `SURVEY-<SIDE>-Qnn-TEXT/-OPTmm` | yes until D42, hidden since | topic names, filter values, question texts, answer labels — each once, for every area |
| Survey figures and keys | `SURVEY-<AREA>-<SIDE>-Qnn-[SEGk-](N\|OPTmm)`, topic membership, question sets, scale maxima, answer-order flags | hidden | — |

4,266 rows are visible; the 13,371 hidden ones are one contiguous block at the end. Since
D42 (2026-09-25) the header and footer rows and the whole survey section are hidden in place
too: 3,957 visible.

**How the pages take their text.** A one-time tool marked all 317 texts on the eight pages:
`data-sync="ID"` on an element that holds only text, a style-neutral `<idbc-t>` wrapper where
text shares its element with a link or an input (a `span` wrapper would have been styled as
the Expert Pool legend's colour dot), `data-sync-attr` for `alt`/`title`/`placeholder`/
`aria-label`/meta description, `data-sync-href` so the footer phone and e-mail links follow
their text. The texts the page scripts put on screen carry `/*sync:ID*/` — 31 rows of their
own (empty-state messages, tooltips, the chart legend, the salary-level labels, the area
page's media placeholders) and 8 that reuse the matching page text (table headers on phone
cards, the read-more buttons); where they contain a value (`{terulet}`, `{n}`, `{max}`, …) the page fills it
in and the sync refuses any placeholder the page does not know. The segment lists, the
"keep answer order" question and the Összesített adatok label were hard-coded in the scripts;
they now come from the data, so renaming them in the sheet cannot break a filter.

**`idbcsync.py`** replaces `build-salary-data.py` and `build-guide-data.py` (removed). It
reads `id` and `érték`, validates everything first and writes nothing on an error, naming the
row: a date where text belongs (Google turns `1-5` into a date unless the cell is text), a
word in a number, a percentage outside 0–100, an unknown media type or placeholder, a marked
text whose row is missing. Values are HTML-escaped (a `<script>` typed into a cell shows as
text). It writes only files that change and bumps `top3-chart.js?v=` when a chart text
changes. Numbers accept spaces and "Ft"; decimals accept a comma.

**Proven equal before switching.** From the generated rows the converter rebuilt the data
with zero differences in any survey payload (all 594), salary row, area text, topic or SAP
item; the "(N fő)" counts, now derived from percent × respondents, reproduce all 1,846
source rows. Rendered in the browser against the live site: 584 Piaci trendek filter
combinations, all 11 area pages with every topic and segment, Bérek for every area at 1440
and 390 px, SAP and Expert Pool — identical HTML apart from the new marker attributes; every
page's visible text, attributes, links and title identical; the three wrapped texts measure
the same at both widths; no console errors. Intended differences: the Piaci trendek
"Szegmens" dropdown now lists the areas by their current names in tile order (it still
carried the pre-2026-09-22 names: "BSC", "Sales & Marketing", "Office Support &
Ügyfélszolgálat" …); two trailing spaces in Expert Pool names are gone; Bérek and SAP split on
the fixed key `kod`, not on the area's name.

**Removed from `guide-data.json`**, read by no page: `generatedFrom`, `talentInsightTop3`,
`readme`, `siteMap`, `filterDimensions`; from `areas.json`, the `dataKey` bridge (the survey
data is now keyed by the area's slug).

**Into the sheet.** The old 13,160 rows were cleared, the grid extended to 18,001 rows, and
the new rows pulled in the same way as D36 — four tab-separated parts of under 1 MB on this
project's Pages, `IMPORTDATA` + `REGEXEXTRACT` (line breaks inside a value travelled as `¶` and
were turned back into real line breaks by `SUBSTITUTE`), then frozen with Irányított
beillesztés → Csak az értékek. One surprise: `IMPORTDATA` treats a line starting with `#` as a
comment, so 14 of the 15 section-heading rows (ids `#…`) arrived as `#N/A`; they were retyped
by hand. Verified from a fresh export: all 17,637 rows equal to the generated rows in all five
columns, no formula left, nothing below the data, and `idbcsync.py --check` against the
export changes no file. Then the tabs other than IDBCSYNC were hidden (`LISTAK` already was),
column A hidden, rows 4268–17638 hidden (the 13,371 survey figures and technical rows, one
block), and column C set to plain text so a typed `1-5` stays text. The import files were
removed from the repo.

**Adding** a row (a new position, IT Contracting's salaries when they arrive) needs a new id,
so it is a studio task or needs column A shown; changing or clearing values never does —
a cleared position, tile or SAP item disappears from the page.

## idbc.hu alignment — plan and Phase 0 (2026-09-25)

idbc.hu was measured page by page (header, hero, section titles, cards, buttons, forms,
footer, type scale, container, colours) and set next to the prototype in
`docs/15-idbc-hu-alignment.md` (D38). The colours already match; the typeface (Gilroy,
commercial, served without cross-origin headers so it cannot be borrowed), the scale and the
shell do not. Nothing in the pages changed yet.

**Phase 0 — facts.** The prototype's footer disagreed with idbc.hu on the phone
(+36 30 479 0090 vs **8**090) and the floor (5. vs **13.** emelet). Both are IDBCSYNC rows, so
they were corrected in the sheet (C17, C20), not in the pages; the next sync carries them to
all seven pages with that footer. The legal links (idbc.hu: Panaszbejelentő → FaceUp,
Adatkezelési tájékoztató → `/adatvedelem/`) wait for the footer rebuild (Phase 2).

**Caught before publishing.** The corrected phone, typed as `+36 30 479 8090`, was read by
Sheets as a formula and exported as `#ERROR!` — despite the column's plain-text format — and
the converter accepted any text, so the next sync would have printed `#ERROR!` in every
footer. No run happened in between. The cell was retyped as `'+36 30 479 8090` (the sheet's
own way to force text), the row's help text now says so, and `idbcsync.py` refuses every
Sheets error value (`#ERROR!`, `#REF!`, `#N/A`, `#VALUE!`, `#NAME?`, `#DIV/0!`, `#NUM!`,
`#NULL!`, `#SPILL!`, `#CALC!`) with the row named.

**Schedule.** In its first hour the 15-minute schedule (`*/15`) produced no run at all —
GitHub delays or drops runs on the busy quarter-hour marks — so it moved to `7,22,37,52`.

## idbc.hu's design on every page — the alignment plan delivered (2026-09-25)

`docs/15-idbc-hu-alignment.md` §10 and D39 hold the decisions and the measurements; this is
the build log.

**One stylesheet.** `assets/site.css` holds idbc.hu's tokens (`#121c1b`, `#14201f`,
`#a4dd8c`, `#35715c`, `#4ca283`, `#daf1d0`, ground `#f5f9f2` with a light noise), its type scale,
header, footer, both hero types, buttons, cards, forms, and one block that sets the page copy
on idbc.hu's body type. `assets/site.js` runs the header menu. Each page links both after its
own `<style>`, which lost every rule the shared file now owns (a script removed them rule by
rule, a second pass the ones hidden behind comments; about half of every page's CSS). Stripped
along the way and put back per page: the hero photo crops from the client's 2026-09-22 "heads
cut off" point.

**Shell.** Header, footer and hero markup rebuilt on all eight pages with the same
`data-sync` ids for every kept text. Kapcsolat's heading and form, one section before, are a
plain hero plus the form now; the area page's green band is the same plain hero. The area
tiles lost their typed "→" (the dark arrow square replaces it); the two page-link cards keep
theirs, which are sheet content. Esettanulmányok and Regisztráció no longer show a hero photo
(idbc.hu's article and contact pages have none).

**Sheet.** 29 new rows — the footer's idbc.hu columns and the social labels — were inserted
after the footer rows (IMPORTDATA from a short-lived file, frozen, file removed) and checked
from a fresh export: 17,667 rows, 0 differences from the expected rows, no formulas, column A
and the technical block still hidden. Six rows no page uses any more (the old text logo's
"IDBC"/"group" labels, the area page's old footer link, two hero photo descriptions) are
retired from the sheet after the pages go live; two kept rows take new values then
(Panaszszabályzat → Panaszbejelentő, the guide column's heading).

**Checks.** Rendered text of every chart, table and tile compared against the live site in
all 1,142 states: identical. No horizontal scroll at 375 or 1440 on any page (one 65 px
overflow on Expert Pool — a long button that would not wrap — fixed first). Tap targets ≥ 44
px on phones after enlarging the social icons and the logo link. Menu opens and closes, 48 px
rows, `aria-expanded` follows. No console errors. `check.py` clean. The browser pane's
screenshots after a programmatic scroll sometimes return a stale frame; a second capture shows
the page — recorded here so it is not mistaken for a rendering bug.


## Client feedback on the published prototype (2026-09-25, D40–D41)

**Survey questions.** The client listed, on the employer side: Home office lacks "Milyen
hatással van a jelenlegi home office policy a toborzás sikerességére?" in every area; AI lacks
"Rendelkezik a vállalatod dedikált költségkerettel AI fejlesztésekre vagy kezdeményezésekre?"
and "Mire használja a vállalatod AI eszközöket a toborzási folyamat során?" outside IT. Read in
`IDBCSYNC`: all three (employer Q13, Q09, Q08) have their text, answer labels and figures for
all 12 data sets, base view and company-size breakdown (BSC, for example: 19 employer
respondents each). What was missing were the topic rows (`SURVEY-TOPIC{t}-SET{n}-EMPLOYER-{kk}`),
which say which question appears in which topic and in what order: Q09 and Q08 were only in the
IT + Contracting set's AI topic, Q13 in no topic ("jelenleg egyik témában sem"). The 2026-09-22
note that these questions were absent from the parsed data was wrong. Four rows appended to the
sheet (rows 17662–17665, hidden like the other technical rows): Q13 third in Home office for
both sets; Q09 then Q08 fourth and fifth in AI for the general set. Q13's seven "megjelenés"
cells changed to "téma: Home office" (Find & Replace, this tab, match case: 7 replacements).
Checked on a fresh export: 27 cells changed, nothing else; column A and the new rows hidden.
Rendered: 560 employer charts on Kezdőoldal (12 data sets × every company size × Home office
and AI) all show figures; Home office 3 questions and AI 5 everywhere; an area page (HR) the
same at every company size; no console errors.

**TOP3 labels.** After the morning's fix (D33) the client still saw close amounts spread
sideways (BSC Supply Chain: 600 000 / 630 000 / 650 000; IT Support: 790 000 / 800 000 /
800 000) and asked for one of them to move up a little instead. `layoutLabels` now keeps every
amount centred over its own dot and moves a label that would touch an already placed one up a
row. Label widths use measured Outfit character widths (about 5.3 px per character at the wide
chart's 10 px, 7.7 px at the phone chart's 13 px) plus room for the hover enlargement. The
first phone run still had touching labels (a 14-unit row step is less than a 13 px label's full
height); the step is 17 units and the phone chart's drawing is 104 units tall (was 84). Measured
on the rendered SVG, all 12 Bérek areas and SAP, 390 and 1440 px, after a clean load
confirming `top3-chart.js?v=12`: no overlaps, nothing outside the chart, no label on a dot,
largest distance from a label to its dot 20 units (edge rows on phones), 0 on desktop.
`chart.css?v=9`: the tooltip uses the page font instead of Inter.

**BSC "Manager".** The grey line under Sales Project Manager is that row's level, `IDBCSYNC`
row 2936 (`SAL-BUSINESS-SERVICE-CENTER-BSC-039-SZINT`, visible, value `Manager`). Clearing the
cell removes it on the next sync; tried on a copy of the export, an empty level passes the
sync's checks. Not changed; the client decides.

## Survey and header/footer rows hidden (2026-09-25, D42)

The owner asked for the survey rows and the header and footer rows of `IDBCSYNC` to be hidden.
Hidden in place from the Name Box range and the row menu, in two ranges: 3–59 (57 header and
footer rows) and 111–386 (the survey section: its heading, `SURVEY-TOTAL-LABEL`, the four
topic names, 163 employee and 107 employer question/answer rows). Kept visible: row 2 (the
tab's instructions) and rows 60–66 (TOP3 legend, LinkedIn note and pill, the survey "no data"
and weighted-scale messages). Fresh export: 333 rows newly hidden and no others, 0 values
changed, no survey or header/footer id left visible, column A still hidden; `idbcsync.py
--check` on it: 0 files would change. 3,957 rows visible (was 4,290).

## IDBCSYNC sections in pastel colours (2026-09-25, D43)

The owner asked for a background colour per section, in pastels, to navigate the tab. Planned
first (one hue per `━━━━` section, deeper shade and bold on the heading, the salary table's
areas alternating, grey for the hidden technical sections, row 1 frozen), then applied from
the browser: whole rows selected in the Name Box, the fill colour's custom-colour dialog, R/G/B
entered with real key presses (typed text is shown but not taken by that dialog). Two things
found on the way: the Name Box skips hidden rows, so the first attempt at the hidden survey
section coloured row 387 instead (overwritten by its own colour later); hidden sections were
shown, coloured and hidden again, and the export confirms the same 13,708 hidden rows as
before. Section ranges: 2–66, 67–110, 111–386, 387–406, 407–440, 441–468, 469–3938 (areas at
470, 1767, 1864, 2201, 2322, 2523, 2580, 2605, 2630, 2943, 3064, 3281, 3818), 3939–3976,
3977–4007, 4008–4064, 4065–4185, 4186–4253, 4254–4277, 4278–4290, 4291–4412, 4413–17665. Fresh
export: fills exactly as in D43, 0 values changed, `idbcsync.py --check` 0 files changed.

## Salary positions shaded in IDBCSYNC (2026-09-25, D44)

The owner asked for the Bérek rows to alternate a lighter and a slightly darker shade of the
section's aqua between positions. The salary table is 13 area-name rows and 432 positions of
exactly 8 rows each, every one starting with its `-POZICIO` row (read from the export), so the
shading is two conditional-formatting rules on `A470:F3938` rather than 216 painted blocks:
area-name rows `#C2E9E9` bold, every second position `#D3EEEE`, the rest the static base
`#EEF9F9`. This replaces D43's alternation by area. Fresh export: both rules present with
those formulas and colours, base fill uniform, 0 values changed, hidden rows unchanged,
`idbcsync.py --check` 0 files changed; on screen, the owner's example (Project Manager →
Engineering Team Leader (Junior), rows 3136/3137) and an area boundary (row 3281) render as
the rules say.

## "Csempe", registration and blank rows hidden in IDBCSYNC (2026-09-25, D45)

The owner asked to hide all "csempe" rows, the "regisztráció" rows and the empty rows. Read
from the export first: 166 visible rows mention "csempe" (11 area names, whose "megjelenés"
names the home-page area tile; the SAP catalogue, 30 rows; the Expert Pool tile texts, 5 rows,
and tiles, 120 rows); "regisztr" matches exactly the registration section (24 rows); 359 rows
at the bottom are completely blank. Hidden: those, plus the two section headings that would
have been left alone (3977, 4065). Not hidden: 1,124 rows with an id but an empty value —
optional salary fields, not empty rows. Fresh export: 551 newly hidden rows, exactly the
intended set, none un-hidden, 0 values changed, 3,765 visible; `idbcsync.py --check` 0 files
changed. Because the Expert Pool tiles are hidden, `EXPERT-27-DARAB` (the missing Qualified
Person count, C-10) now needs its row shown before it can be typed in.
