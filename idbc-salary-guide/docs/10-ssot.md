# IDBC Salary Guide — single source of truth (SSOT)

*Definitions the technical documents (`11`–`14`) use without redefining. Everything is read
from what the prototype holds (the `IDBCSYNC` sheet tab, `data/idbcsync.py`, the files it
writes, the pages). Written 2026-09-18; the data sections updated 2026-09-25 for D37.*

## 1. Glossary

| Term | Meaning here |
|---|---|
| IDBCSYNC | The `IDBCSYNC` tab of the client's `IDBC_bertabla` Google Sheet: one row per value (`id`, `változó`, `érték`, `megjelenés`, `segítség`). The only source of every text and figure on the guide; `data/idbcsync.py` reads `id` and `érték` only (D37). |
| Survey | IDBC's 2026 research: two questionnaires (employee, employer), June–August 2026; the client's published sample sizes are 1 552 and 148 responses. |
| Question set | Which questionnaire variant a dataset follows: *Általános* or *IT + Contracting*. Two exist; each topic lists its questions per set. Formerly "edition". |
| Dataset | One tabulation of the survey: the whole sample (`__total__`, labelled *Összesített adatok*) or one of 11 areas. 12 datasets. |
| Topic | One of four groupings of questions: Munkahely váltás és toborzási kilátások · Home office · AI · Bérezés és juttatások. |
| Side | Employee (*Munkavállalók*, B2C in the workbook) or employer (*Munkáltatók*, B2B). |
| Segment | A crosstab dimension value: experience band on the employee side, company size on the employer side. *Összesített adatok* is the pseudo-segment for the whole dataset. |
| Weighted question | The two "Jelöld 1-4-ig terjedő skálán…" questions, shown only as a weighted average (D16). |
| Area (trends) | One of 11 areas with a summary text, a media slot and its own dataset (`areas.json`). |
| Area (bértábla) | One of 13 salary areas, each with one name row (`SAL-<key>-NAME`) and a fixed key (`kod`) — SAP's key keeps its rows on the SAP page whatever the area is called (D37). Not the same set as the trends areas. |
| Bértábla | The salary table: one row per area + position + level. Until 2026-09-25 the sheet's `WEB_BERTABLA_IMPORT` tab; since D37 IDBCSYNC's `SAL-` rows (the old tab is hidden and no longer read). |
| TOP3 row | A standalone bértábla row flagged `x`: the three highlighted positions of an area, with min / IDBC / max and usually no level. 39 exist. |
| Level | `tapasztalati_szint`: Trainee · Junior · Medior · Senior · Team Leader · Manager, or none. |
| Band | min–max monthly gross HUF; on TOP3 rows also the IDBC recommendation. Labelled per D5. |
| Talent Insight count | LinkedIn Talent Insight's number of professionals in Hungary for a position; on TOP3 rows (`linkedin`) and pool rows. Always printed with a star and the footnote. |
| Expert Pool / Expert Community | IDBC's candidate community; a count per industry + position (IDBCSYNC `EXPERT-` rows: 30, one — Qualified Person — without a count yet, so not shown). |
| SAP catalogue | 25 items in 5 categories (`sapProducts`, IDBCSYNC `SAPPROD-` rows), from the client's SAP spec. |
| Inert control | A control shown in place with class `is-unavailable`, `aria-disabled` and a `title` saying why: Excel export, EN, Kijelentkezés, form submits. |
| Gate | `python3 idbc-salary-guide/check.py` (run by the root `check.py`) + the measured pass (`07-gate.md`). |

## 2. Enumerations

| Enum | Values |
|---|---|
| Topic | the four above, in that order |
| Question set | Általános · IT + Contracting |
| Dataset | `__total__` + one per trends area, keyed by the area's slug and labelled with its name, in the areas' order (D37) |
| Employee segment | kevesebb, mint 1 év · 1-2 év · 3-5 év · 6-10 év · 11-20 év · több, mint 20 év — IDBCSYNC `SURVEY-EMPLOYEE-SEG1…6` (offered per topic only where a non-zero row exists, D6) |
| Employer segment | 50 fő alatti · 51-100 fő · 101-350 fő · 351-1000 fő · 1000 fő feletti — `SURVEY-EMPLOYER-SEG1…5` |
| Question kind | single · multi · weighted (stacked chart; weighted bar 1–4) |
| Bértábla area (sheet order) | IT · SAP · Pénzügy és számvitel · Sales · Marketing · HR · Retail · Office Support · Business Service Center (BSC) · Logisztika, Szállítás · Gyártás, Termelés, Mérnökség · Építőipar, Ingatlan · Pharma, Life Sciences |
| Level order | Trainee · Junior · Medior · Senior · Team Leader · Manager · (none) |
| Pool industry | IT · Non-IT |
| Area media | video · highlight |
| Account type (registration) | cég · jelölt |
| Nav | Piaci trendek · Bérek · SAP · Expert Pool · Esettanulmányok · Ajánlatkérés · Kijelentkezés |

## 3. Canonical entities (as in `guide-data.json`, all written by `data/idbcsync.py` from IDBCSYNC)

| Entity | Key fields | IDBCSYNC rows |
|---|---|---|
| `datasets[slug]` | `label`, `questionSet`, `employee{base, cross}`, `employer{base, cross}`; `base[question]` = `{kind: "simple", items[{label, percent, count}]}` or `{kind: "weighted", scaleMax, items[{label, value}]}`; `cross[question]` = `{kind: "matrix-percent", groups[], items[{label: segment, values[{group, percent, count}]}]}` | `SURVEY-<AREA>-<SIDE>-Qnn-[SEGk-](N\|OPTmm)`; question text and answer labels once per question (`SURVEY-<SIDE>-Qnn-TEXT`, `-OPTmm`); `count` = percent × respondents (`…-N`) |
| `topics[]` | `topic`, `questionSets{set: {Munkavállalók[], Munkáltatók[]}}` — the question lists per set | `SURVEY-TOPICt-NAME`, membership `SURVEY-TOPICt-SETn-<SIDE>-kk` (hidden) |
| `segments` | `employee[]`, `employer[]` — labels in dropdown order | `SURVEY-<SIDE>-SEGk` |
| `keepSourceOrder[]` | questions whose answers keep the questionnaire order | `SURVEY-<SIDE>-Qnn-SORREND` = igen |
| `totalKey`, `totalLabel` | `__total__`, *Összesített adatok* | `SURVEY-TOTAL-LABEL` |
| `salary.webBertabla[]` | `id`, `kod`, `terulet`, `szint`, `pozicio`, `top3`, `min`, `idbc`, `max`, `juttatas`, `linkedin?` | `SAL-<key>-NAME`, `SAL-<key>-nnn-<FIELD>` |
| `salary.expertPool[]` | `iparag`, `pozicio`, `darab`, `linkedin?` | `EXPERT-nn-<FIELD>` |
| `sapProducts[]` | `category`, `items[]` | `SAPPROD-CATn-NAME`, `-ITEMm` |
| `areas.json.areas[]` | `slug`, `name`, `edition` (question set), `summary`, `media` | `AREA-<SLUG>-NAME`, `-SUMMARY`, `-MEDIA`, `-EDITION` |
| page texts | every marked element and script text | the row named by `data-sync` / `data-sync-attr` / `data-sync-href` / `/*sync:ID*/` |

Removed 2026-09-25 (D37), read by no page: `generatedFrom`, `salary.talentInsightTop3`,
`salary.readme`, `filterDimensions`, `siteMap`, and `areas.json`'s `dataKey` bridge.

Entities the production build adds (defined here, designed in `12`): **Account** (name,
e-mail, company, position, type, consent, created), **Lead** (an account handed to
IDBC's CRM), **Download** (an Excel export event), **Media** (video URL per area /
case study).

## 4. Settings the prototype fixes

| Setting | Value |
|---|---|
| Default dataset / segment | `__total__` / *Összesített adatok* |
| Chart breakpoint | compact layout ≤ 700 px viewport |
| Header menu breakpoint | links fold behind the menu icon below 1200 px (idbc.hu's) |
| Table card mode | container width < 600 px |
| Asset version | `?v=` on `top3-chart.js` (10), `chart.css` (8), `site.css` and `site.js` (1) — bump on every change; the sync bumps `top3-chart.js` itself when a chart text changes in the sheet |
| Tap floor | 44 px below 980 px |
| Currency format | `hu-HU` grouping, ` Ft`; millions abbreviated `1,25M` in the compact chart |

## 5. Decision register

`04-decisions.md` (D1–D39). Technical decisions in this package are ADRs in
`11-architecture.md` §11, PROPOSED until flipped; the flip is the next D-number.

## 6. Rules register

| # | Rule | Origin |
|---|---|---|
| R1 | No figure is invented or estimated; every number traces to a client file. | README of the repo; D22 |
| R2 | *Összesített adatok* is first and default; a real segment is offered only where the topic has a non-zero row. | D6 |
| R3 | A question with no data under the selected segment is hidden; the aggregate is never substituted; one panel-level sentence if a panel is empty. | D9 |
| R4 | The two 1–4 questions render as the weighted average only. | D16 |
| R5 | An inert control is shown in place with `is-unavailable` and a `title`. | repo principle; gate check 5 |
| R6 | Talent Insight counts are read from the bértábla sheet's own column, row by row; the explicit name table is only the fallback for a sheet without the column, and there a renamed position fails the build. | D22, D29 |
| R7 | The shared chart assets are versioned; every page loads the same version. | gate check 4 |
| R8 | The band labels (D5) and the "valós piaci adatok" note (D14) ship as the client's wording; the divergence from the sheet is documented, not hidden. | gap 6 |
| R9 | One template per repeated thing: area page, tile, chart. | D11 |
| R10 | Tables are complete: TOP3 rows are listed in the table as well as charted. | D24 |
| R11 | In fine-tuning, only the reported item changes. | owner, 2026-09-18 |
| R12 | The registration checkbox acknowledges the privacy notice; marketing needs its own unticked consent; role addresses by legitimate interest with opt-out, named persons by consent (§6b). | Act XLVIII/2008 |
| R13 | Salary data stays aggregated; no registrant's own salary is asked or stored; no Article 9 field exists (§6b). | GDPR |
| R14 | Registration, marketing e-mail and candidate matching run only when the policy record's fields for them are set (the gate). | §6b |

## 6b. Responsible-data policy record (PROPOSED, 2026-09-20)

*One record per instance, per the framework in `business-direct/docs/18-responsible-data-policy-framework.md` (owner directive 2026-09-19: responsible data for every client; hub audit 2026-09-20, action 1). Filled for a B2B research guide with a registration
paywall in Hungary; every value is a proposal until the client confirms it.*

| Field | Value (PROPOSED) | Why |
|---|---|---|
| client · instance | IDBC · the Salary Guide (HU) | — |
| jurisdictions · laws | HU, EU — GDPR, Infotv., Act XLVIII/2008 (B2B: corporate addresses without consent; a named person's address needs consent), EU AI Act Art. 50 for generated media | research and the registration form |
| audienceModel | adults — company representatives and candidates (`type: cég / jelölt`) | the paywall's account types |
| childData | none | — |
| sensitiveCategories | salary figures are the survey's, anonymised and aggregated (R1: every number traces to a client file); a registrant's own salary is never asked; no Article 9 field on the form | GDPR Art. 9 |
| channels · consent | the registration checkbox is a **privacy-notice acknowledgement, not marketing consent** — a separate, unticked consent is needed before any marketing e-mail; candidates (individuals) and named company contacts by consent; role addresses (`info@`) by legitimate interest with opt-out | Act XLVIII/2008 |
| defaults · cap · optOutSla | nothing on by default; at most one guide-related mail a month; opt-out within one business day | R28 |
| aiDisclosure | label (any generated image on the trends pages) | Art. 50 |
| retention | registration accounts while the guide edition is live + 12 months; marketing consent until withdrawn; download logs 12 months | to confirm with counsel |
| privacyPolicy | the `Adatkezelési tájékoztató` linked from the form must name the guide, the account, the Excel download, cookies, and any marketing use — today the link is `#` | the gate blocks registration until the notice is real |
| dpia | not required (B2B) — recommended if candidate profiles are matched to jobs (Expert Pool) | GDPR Art. 35 |
| vulnerability · darkPatterns · accessibility | no pressure; no pre-ticked box (the form's box is unticked — keep it); WCAG 2.2 AA | R32, R36, R34 |

**Gate rows for the production guide:** registration needs the real privacy notice;
marketing e-mail needs a separate consent; the Expert Pool's candidate matching needs the
DPIA decision. Rules R12–R14.

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
| `09-business-logic.md` | the rules end to end, mapped to the SSOT's rules |
| `10-ssot.md` | this file | a definition changes |
| `11-architecture.md` | measured host, containers, PROPOSED stack, ADRs | an architectural decision changes |
| `12-technical-design.md` | templates, data pipeline, registration, export, media, analytics | a design detail changes |
| `13-implementation-plan.md` | milestones, issues with DoD, blocked register, risks | scope or sequencing changes |
| `14-token-map.md` | page tokens and components → production | a token or component changes |
