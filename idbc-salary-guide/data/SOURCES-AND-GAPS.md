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
| `IDBC_bertabla` | Google Sheet | Real salary-band data → `salary.webBertabla` (270 rows, 8 areas) and `salary.expertPool` (15 rows). Includes the `UTMUTATO` instructions tab, captured verbatim in `salary.readme`. |
| `IDBC_web_bertabla_roviditett_import_v9.xlsx`, `Salary Guide ... minta.xlsx` | Excel | Duplicate exports of the two sheets above — not separately re-parsed, no new data. |
| `IDBC Salary Guide specifikáció` | Google Doc | Functional spec: registration/paywall gate, 3 data-driven functions (Bérezés, Igény-elvárás, Expert Pool), Google-Sheets-via-API + WordPress block-editor architecture. |
| `SG_landing_speci.docx` | Word doc | Full site map (8 pages) and per-page content-block breakdown — see `siteMap` in the data file. Added detail the shorter spec didn't have: split IT/Contracting result blocks, the Non-IT area filter, the 3-tier-range-vs-1-average-range table distinction, the full SAP product catalogue, and the Excel-download CTA. |
| `Szűrők` | Google Doc | The intended filter taxonomy (Terület, Téma, Generáció, Tapasztalati szint, Cégméret, Cégtulajdon) — see `filterDimensions` in the data file for which of these the real survey data actually supports. |
| `MEGBESZÉLÉS JEGYZET`, `Megbeszélés jegyzet bérsáv tábla`, `Vázlatos egyeztetés TH+Csaba+Bence 06.12.` | Doc/Sheets | Internal meeting notes — mostly superseded by the two spec docs above; the last one gives a rough frontend/backend effort breakdown per feature, no new content requirements. |
| `html demok/1_regisztracio.html` | HTML mockup | Real registration-page design (Gmail/Facebook/e-mail signup, private-vs-company account type toggle) — not yet built. |
| `html demok/2_savok.html` | HTML mockup | Real design for the B2C/B2B filterable trends dashboard — this is what the current "Piaci trendek" section is built from. |
| `html demok/3_SAP.html` | HTML mockup | Real design for a dedicated SAP article page (exec summary, contact card, product grid, TOP3 + full salary table) — not yet built as its own page. |
| `IDBC_SalaryGuide_home.pdf` | PDF mockup (lorem ipsum) | Shows the Salary Guide teaser as it would sit inside IDBC's main homepage template (hero, 3 feature cards, text block) — confirms this is meant to be embedded content, not a standalone site. |
| `IDBC_SalaryGuide_aloldal.pdf` | PDF mockup (lorem ipsum) | **Most important visual find**: shows the actual salary/trends article-page layout, including a horizontal **point-line chart** for the TOP3 salary comparison (three connected, labeled dots per role along one HUF axis) — a materially different (better) chart than the static range-cards currently deployed. |

## Current build vs. client intent — concrete gaps

1. **Single combined page vs. an 8-page site.** The live page merges what the
   spec splits into Home, Registration, IT trends, Non-IT+Perm trends,
   Bérek, SAP guide, Expert Pool, and Esettanulmányok. Fine as a working
   prototype; a production build would need real routing/pages.
2. **No registration/paywall gate.** Every mockup and both specs describe
   content sitting behind a login wall. Not implementable on static GitHub
   Pages without a real backend/auth provider.
3. **Salary TOP3 chart is the wrong shape.** Built as 3 static stat numbers
   per card; the client's own mockup shows a point-line chart connecting
   min → IDBC-recommended → max along one shared axis. This is fixable now
   with data we already have (see below) — no new client data needed.
4. **SAP gets no dedicated page.** The 20-item product catalogue is real
   client content (now captured in `sapProducts`) but isn't surfaced
   anywhere in the current build.
5. **Missing filters the real data can't support anyway:** Generáció
   (birth-generation) and a Terület filter on the employee/trends side, plus
   full Cégtulajdon crosstabs — these appear in every spec/filter doc but
   the underlying survey was never fielded with those breakdowns. Building
   them would require the client re-running or re-tabulating the survey,
   not a code change.
6. **"3 stakeholder ranges" (candidate / company / IDBC) is aspirational.**
   The SAP mockup's static example shows three independently-sourced
   expectation ranges. The real `webBertabla` sheet only has one range
   (min/max) plus one IDBC-recommended point — a single perspective, not
   three. Don't fabricate the other two; flag it as a data-collection gap
   if the client wants that exact chart.

## Schema in `guide-data.json`

- `editions`, `topics`, `answers` — survey trends (unchanged from before).
- `salary.webBertabla`, `salary.expertPool`, `salary.readme` — salary bands (unchanged from before).
- `filterDimensions` — **new**: every filter named in the client's `Szűrők` doc, each flagged `available` / `partial` / not-available against what the real data supports, with a note explaining the gap.
- `sapProducts` — **new**: the real 5-category, 20-item SAP product catalogue from the client's own SAP mockup/spec.
- `siteMap` — **new**: the full intended 8-page site structure with a `status` (`built` / `partially built` / `not built`) and note per page.
