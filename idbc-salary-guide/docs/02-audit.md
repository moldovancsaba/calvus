# IDBC Salary Guide — audit of the client's starting point

*What the client had when the project started and what it has now, measured where
possible. Written 2026-09-18.*

## The client's site (idbc.hu), measured 2026-09-18

| Measure | Value |
|---|---|
| Platform | WordPress; WPML 4.8.5 (HU + EN); `performance-lab` + `webp-uploads`; no page builder detected on the home page |
| Home page HTML | 78,6 KB; 9 external scripts; 6 stylesheets |
| TTFB | 0,12 s (one measurement, from this environment) |
| Analytics | Google Tag Manager present |
| Multilingual | EN exists (`/en/`), so an EN edition of the guide is technically possible once EN copy exists |

The client's PDF mockup places the Salary Guide teaser inside this site's own template
(hero, three feature cards, text block) — the guide is embedded content, not a
standalone site (`SOURCES-AND-GAPS.md` gap 1).

## The client's specification vs. the data

The specs described more than the data could carry. Each divergence is recorded as a
numbered gap in `SOURCES-AND-GAPS.md` ("Current build vs. client intent"); the state on
2026-09-18:

| Gap | Status |
|---|---|
| 1 One page vs. eight-page site | mostly closed — seven pages exist; the home page waits for the client's structure demo |
| 2 No registration / paywall on static hosting | open by nature — a mock registration page exists; the real gate is the build's (`11-architecture.md`) |
| 3 TOP3 chart shape | closed 2026-08-17 |
| 4 No dedicated SAP page | closed 2026-08-17 |
| 5 Filters the data cannot support | Terület closed 2026-09-08 (per-area workbook); Generáció and Cégtulajdon remain impossible — a survey-design change, not code |
| 6 "Three stakeholder ranges" are one range with two labels | open — a labelling choice recorded; the client's own copy asserts real market data while the sheet's own banner still says sample values |

## The client's data, as it stands

| Set | Rows | Quality notes |
|---|---|---|
| Survey (final workbook, 2026-09-08) | 12 datasets × (12 employee + 13 employer questions), crosstabs by experience (employee) and company size (employer) | tabulated per area; two 1–4 scale questions carry only a weighted average by the client's choice; crosstab rows exist for empty segments (all-zero) — the pages hide those |
| Bértábla (Google Sheet, re-pulled 2026-09-18) | 432 rows, 13 areas, 39 standalone TOP3 rows | levels Trainee → Manager, 19 senior roles without a level; IDBC recommendation only on TOP3 rows; the sheet's banner still calls the figures sample values awaiting professional approval |
| Talent Insight (LinkedIn) | 39 TOP3 counts (37 filled), 15 pool counts (13 filled) | four numbers still owed by the client; position names differ from the bértábla by spelling and language — mapped by hand in `build-salary-data.py` |
| Expert Pool | 15 rows, 3 industries | as delivered |

## Defects found in the client's material, for the record

- `Salary Guide- kutatási eredmények-final_2.xlsx` (re-sent 2026-09-18) is byte-identical
  to the 2026-09-08 workbook.
- Talent Insight spellings: "Stategic Buyer", "Senior Tax Avisor"; bértábla: "Mechanical
  Designe Engineer" — kept as delivered on the pages that print them, mapped where a
  match was needed.
- The demo PNG for the Expert Pool tile reads "IDBC Expert Commuinty"; the page prints
  "Community".
- The `siteMap` block inside `guide-data.json` carried July statuses until 2026-09-18.
