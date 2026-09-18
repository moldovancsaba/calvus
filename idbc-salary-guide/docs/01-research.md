# IDBC Salary Guide — research

*What was read before and during the build, and what was deliberately not researched.
Written 2026-09-18.*

## What this project's research is

No benchmark study of competing salary guides was made, and none was asked for: the
client arrived with finished specifications, its own mockups and its own data, and the
brief was to build what they described against what the data could support. The
"research" here is therefore **reading the client's material closely** and measuring
it against itself — the full account, file by file, is the source table at the top of
`SOURCES-AND-GAPS.md`.

## The inputs, in one view

| Kind | Files | What they fixed |
|---|---|---|
| Specifications | `IDBC Salary Guide specifikáció` (Google Doc), `SG_landing_speci.docx` | the eight-page site map, the paywall, the three data functions, the WordPress + Sheets architecture assumption |
| Filter taxonomy | `Szűrők` (Google Doc) | the six intended filters; four were possible with the data (`filterDimensions` in the JSON) |
| Mockups | `1_regisztracio.html`, `2_savok.html`, `3_SAP.html`, `3_SAP_TOP3_chart_gradient_tooltip_categories.html`, `IDBC_SalaryGuide_home.pdf`, `IDBC_SalaryGuide_aloldal.pdf`, three PNG demos (2026-09-18) | the layout of every page; the point-line TOP3 chart; the tile and highlight designs |
| Data | `Salary Guide - munkaerőpiaci trendek - minta` → `Salary Guide- kutatási eredmények-final.xlsx` (2026-09-08, "végleges"); `IDBC_bertabla` (Google Sheet, reworked 2026-09-18); `Talent Insight riport.xlsx` (2026-09-18) | every number on the pages |
| Copy | `SG_Területi_összefoglalók_final.docx`, `SG - SAP tartalom.docx`, `SG- Esettanulmányok.docx`, `SG - Expert Community.docx`, `SG - kezdő oldal.docx` | every paragraph of text |
| Meeting notes | `MEGBESZÉLÉS JEGYZET`, `Megbeszélés jegyzet bérsáv tábla`, `Vázlatos egyeztetés TH+Csaba+Bence 06.12.` | context; superseded by the specs |

## The one external measurement

idbc.hu, where the guide will live, was measured on 2026-09-18 (`11-architecture.md`
§2): WordPress with WPML, no page builder detected, 78 KB HTML, 9 scripts, 6
stylesheets, TTFB 0,12 s. A lean host; the guide must not make it heavy.

## What was not researched, and why

- Competing salary guides (Hays, Randstad, Robert Walters): the client's positioning is
  its own survey and Expert Community, not a design contest. Worth a page if the client
  ever asks "how do we compare".
- The survey's methodology: taken as delivered. The published sample sizes (1 552 /
  148 in the home-page copy) are the client's; the workbook's per-question counts are
  what the pages show.
- WCAG beyond the basics: the tables-as-cards and tap-target work followed the specific
  rules cited in `SOURCES-AND-GAPS.md`; no screen-reader pass was made (recorded there).
