# IDBC Salary Guide — data sources and design-intent audit

This documents every file in the client's Drive folder (`IDBC`, folder id
`1aOhkzvH0YtJVFkaIq85QsrCaqb4_JTQv`) that feeds this project, how each one
was used, and where the currently deployed page diverges from what the
client's own specs and mockups actually describe. `guide-data.json` in this
folder is the single consolidated data source built from all of it.

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

How it was delivered: the connector in this environment can rename or move the client's sheet
but not write cells into it, so the columns exist as (a) the complete workbook
`IDBC_bertabla_talent_insight_2026-09-21.xlsx` — today's sheet plus the columns, ready to
import over the original — and (b) a Google Sheet in the owner's Drive,
`IDBC_bertabla — LinkedIn Talent Insight oszlopok (2026-09-21)`, the same 54 rows in
paste-ready form. Until the columns are in `IDBC_bertabla` itself, the converter's fallback
path (sheet + Talent Insight workbook) still produces the same data.

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
