# IDBC Salary Guide — single source of truth (SSOT)

*Definitions the technical documents (`11`–`14`) use without redefining. Everything is read
from what the prototype holds (`data/guide-data.json`, `data/areas.json`, the two converters,
the pages). Written 2026-09-18.*

## 1. Glossary

| Term | Meaning here |
|---|---|
| Survey | IDBC's 2026 research: two questionnaires (employee, employer), June–August 2026; the client's published sample sizes are 1 552 and 148 responses. |
| Question set | Which questionnaire variant a dataset follows: *Általános* or *IT + Contracting*. Two exist; each topic lists its questions per set. Formerly "edition". |
| Dataset | One tabulation of the survey: the whole sample (`__total__`, labelled *Összesített adatok*) or one of 11 areas. 12 datasets. |
| Topic | One of four groupings of questions: Munkahely váltás és toborzási kilátások · Home office · AI · Bérezés és juttatások. |
| Side | Employee (*Munkavállalók*, B2C in the workbook) or employer (*Munkáltatók*, B2B). |
| Segment | A crosstab dimension value: experience band on the employee side, company size on the employer side. *Összesített adatok* is the pseudo-segment for the whole dataset. |
| Weighted question | The two "Jelöld 1-4-ig terjedő skálán…" questions, shown only as a weighted average (D16). |
| Area (trends) | One of 11 areas with a summary text, a media slot and its own dataset (`areas.json`). |
| Area (bértábla) | One of 13 area codes in the salary sheet; display names are mapped in `build-salary-data.py` (D23). Not the same set as the trends areas. |
| Bértábla | The client's `IDBC_bertabla` Google Sheet, `WEB_BERTABLA_IMPORT` tab: one row per area + position + level. |
| TOP3 row | A standalone bértábla row flagged `x`: the three highlighted positions of an area, with min / IDBC / max and usually no level. 39 exist. |
| Level | `tapasztalati_szint`: Trainee · Junior · Medior · Senior · Team Leader · Manager, or none. |
| Band | min–max monthly gross HUF; on TOP3 rows also the IDBC recommendation. Labelled per D5. |
| Talent Insight count | LinkedIn Talent Insight's number of professionals in Hungary for a position; on TOP3 rows (`linkedin`) and pool rows. Always printed with a star and the footnote. |
| Expert Pool / Expert Community | IDBC's candidate community; the pool sheet gives a count per industry + position (15 rows). |
| SAP catalogue | 20 items in 5 categories (`sapProducts`), from the client's SAP spec. |
| Inert control | A control shown in place with class `is-unavailable`, `aria-disabled` and a `title` saying why: Excel export, EN, Kijelentkezés, form submits. |
| Gate | `python3 idbc-salary-guide/check.py` + the measured pass (`07-gate.md`). |

## 2. Enumerations

| Enum | Values |
|---|---|
| Topic | the four above, in that order |
| Question set | Általános · IT + Contracting |
| Dataset | `__total__` + IT · IT Contracting · Pénzügy és számvitel · Sales & Marketing · HR · BSC · Építőipar, ingatlan · Gyártás, termelés, mérnökség · Office Support & Ügyfélszolgálat · Logisztika és szállítás · Pharma & Life Sciences |
| Employee segment | kevesebb, mint 1 év · 1-2 év · 3-5 év · 6-10 év · 11-20 év · 20+ év (offered per topic only where a non-zero row exists, D6) |
| Employer segment | 50 fő alatti · 51-100 · 101-350 · 351-1000 · 1000+ |
| Question kind | single · multi · weighted (stacked chart; weighted bar 1–4) |
| Bértábla area code → name | BSC · PENZUGY → Pénzügy és számvitel · Sales · Marketing · HR · Office Support → Office Support & Ügyfélszolgálat · Retail · GYARTAS → Gyártás, termelés, mérnökség · LOGISZTIKA → Logisztika és szállítás · CP → Építőipar, ingatlan · PHARMA → Pharma & Life Sciences · IT · SAP |
| Level order | Trainee · Junior · Medior · Senior · Team Leader · Manager · (none) |
| Pool industry | Pharma · IT · Finance |
| Area media | video · highlight |
| Account type (registration) | cég · jelölt |
| Nav | Piaci trendek · Bérek · SAP · Expert Pool · Esettanulmányok · Ajánlatkérés · Kijelentkezés |

## 3. Canonical entities (as in `guide-data.json`)

| Entity | Key fields | Source |
|---|---|---|
| `datasets[id]` | `label`, `questionSet`, `employee{base, cross}`, `employer{base, cross}`; `base[question] = {kind, options[], percent[], count[], weighted?}`; `cross[question][segment]` likewise | survey workbook via `build-guide-data.py` |
| `topics[]` | `topic`, `questionSets{set: {employee[], employer[]}}` — the question lists per set | workbook's "Téma besorolás" tab + client renames (D7) |
| `salary.webBertabla[]` | `id`, `kod`, `terulet`, `szint`, `pozicio`, `top3`, `min`, `idbc`, `max`, `juttatas`, `linkedin?` | bértábla via `build-salary-data.py` |
| `salary.talentInsightTop3[]` | `terulet`, `pozicio`, `linkedin` — the client's list verbatim | Talent Insight sheet 1 |
| `salary.expertPool[]` | `iparag`, `pozicio`, `darab`, `linkedin?` | pool sheet + Talent Insight sheet 2 |
| `salary.readme` | the sheet's UTMUTATO text verbatim | bértábla |
| `sapProducts[]` | `category`, `items[]` | SAP spec |
| `filterDimensions` | every intended filter with `available: true/false/"partial"` and why | `Szűrők` doc vs data |
| `siteMap.intendedPages[]` | page, status, note | specs; statuses maintained by hand |
| `areas.json.areas[]` | `slug`, `name`, `edition` (question set), `media`, `summary` | client texts (D13), media list (D20) |

Entities the production build adds (defined here, designed in `12`): **Account** (name,
e-mail, company, position, type, consent, created), **Lead** (an account handed to
IDBC's CRM), **Download** (an Excel export event), **Media** (video URL per area /
case study).

## 4. Settings the prototype fixes

| Setting | Value |
|---|---|
| Default dataset / segment | `__total__` / *Összesített adatok* |
| Chart breakpoint | compact layout ≤ 700 px viewport |
| Table card mode | container width < 600 px |
| Asset version | `?v=7` on `top3-chart.js` and `chart.css` — bump on every change |
| Tap floor | 44 px below 980 px |
| Currency format | `hu-HU` grouping, ` Ft`; millions abbreviated `1,25M` in the compact chart |

## 5. Decision register

`04-decisions.md` (D1–D27). Technical decisions in this package are ADRs in
`11-architecture.md` §11, PROPOSED until flipped; the flip is the next D-number.

## 6. Rules register

| # | Rule | Origin |
|---|---|---|
| R1 | No figure is invented or estimated; every number traces to a client file. | README of the repo; D22 |
| R2 | *Összesített adatok* is first and default; a real segment is offered only where the topic has a non-zero row. | D6 |
| R3 | A question with no data under the selected segment is hidden; the aggregate is never substituted; one panel-level sentence if a panel is empty. | D9 |
| R4 | The two 1–4 questions render as the weighted average only. | D16 |
| R5 | An inert control is shown in place with `is-unavailable` and a `title`. | repo principle; gate check 5 |
| R6 | Talent Insight counts are matched by an explicit table; a renamed position fails the build. | D22 |
| R7 | The shared chart assets are versioned; every page loads the same version. | gate check 4 |
| R8 | The band labels (D5) and the "valós piaci adatok" note (D14) ship as the client's wording; the divergence from the sheet is documented, not hidden. | gap 6 |
| R9 | One template per repeated thing: area page, tile, chart. | D11 |
| R10 | Tables are complete: TOP3 rows are listed in the table as well as charted. | D24 |
| R11 | In fine-tuning, only the reported item changes. | owner, 2026-09-18 |

## 7. Metrics

| Metric | Target | Where |
|---|---|---|
| Overflow at 375 / desktop; tap targets < 44 px; console errors | 0 / 0 / 0 | `07-gate.md` |
| Data freshness | pages rebuilt within one working day of a new client workbook | converters |
| Guide page weight (production) | ≤ 300 KB JSON per page after splitting (`12` §4); today one 1,1 MB file | `13` |
| Registration conversion, downloads, filter use | reported monthly to the client | `12` §9 |
| Business (client's) | leads by account type; Ajánlatkérés clicks; Expert Community joins | CRM |

## 8. Document map

| Document | Purpose | Changes when |
|---|---|---|
| `00-brief.md` | what it is, what is real, where it stands | status changes |
| `SOURCES-AND-GAPS.md` | every source file, every gap, every change round | any input or build changes |
| `04-decisions.md` | the register | a decision is made |
| `10-ssot.md` | this file | a definition changes |
| `11-architecture.md` | measured host, containers, PROPOSED stack, ADRs | an architectural decision changes |
| `12-technical-design.md` | templates, data pipeline, registration, export, media, analytics | a design detail changes |
| `13-implementation-plan.md` | milestones, issues with DoD, blocked register, risks | scope or sequencing changes |
| `14-token-map.md` | page tokens and components → production | a token or component changes |
