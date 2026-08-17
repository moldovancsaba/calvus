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

## Schema in `guide-data.json`

- `editions`, `topics`, `answers` — survey trends (unchanged from before).
- `salary.webBertabla`, `salary.expertPool`, `salary.readme` — salary bands (unchanged from before).
- `filterDimensions` — **new**: every filter named in the client's `Szűrők` doc, each flagged `available` / `partial` / not-available against what the real data supports, with a note explaining the gap.
- `sapProducts` — **new**: the real 5-category, 20-item SAP product catalogue from the client's own SAP mockup/spec.
- `siteMap` — **new**: the full intended 8-page site structure with a `status` (`built` / `partially built` / `not built`) and note per page.

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
| Salary table | 3 columns, mockup shape | 5 columns, split values | n/a |

The SAP table follows the mockup exactly: `Job / terület` | `Átlagos range` |
`Juttatási megjegyzés`, with the band collapsed into one `min – max` cell. That
drops `Szint` and the IDBC figure from the table — the chart directly above
carries the IDBC recommendation as its own point on every row. The Bérsávok
table deliberately keeps the wider split-column layout; the mockup only ever
covered the SAP page.

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
