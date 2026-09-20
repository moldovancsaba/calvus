# IDBC Salary Guide — business logic

*Written 2026-09-20 (hub audit action 7). The rules of the guide end to end: who reads it
and who pays for it, what the data is and is not, how a figure reaches a page, the paywall
and the registration, the inert controls, fine-tuning, the data, and what the guide never
does. Terms are the SSOT's (`10-ssot.md`); the decisions are in `04-decisions.md`.*

## 1. The parties

| Party | Gets | Gives |
|---|---|---|
| **IDBC** (the client) | a research guide that presents its 2026 survey and its bértábla as a product: market trends by area, salary bands, the SAP guide, the Expert Community, case studies; leads through registration | the survey workbook, the bértábla sheet, the Talent Insight counts, the copy, the design demos |
| **A reader** — a company representative or a candidate | the trends and the bands behind a registration | an account (company / candidate), a privacy-notice acknowledgement; marketing consent only separately (R12) |
| **The studio** | — | the converters, the pages, the documentation |

## 2. The data — what is real, and how a figure reaches a page (R1, R6, R10)

- **No figure is invented.** Every number traces to a client file: the survey workbook
  (`build-guide-data.py`), the bértábla and the Talent Insight workbook
  (`build-salary-data.py`). A re-run is byte-identical; a renamed position fails the build
  rather than guessing (R6).
- **The survey** is tabulated as twelve datasets: the whole sample (*Összesített adatok*,
  first and default — R2) and eleven areas, each with employee and employer sides and
  their crosstabs (experience band; company size). A question with no data under a chosen
  segment is hidden, never substituted (R3); the two 1–4-scale questions show the weighted
  average only (R4).
- **The bértábla** gives one row per area + position + level, with min–max bands and, on
  TOP3 rows, IDBC's recommendation and the Talent Insight count. TOP3 rows are charted
  *and* listed in the table (R10). The band labels and the "valós piaci adatok" note ship as
  the client's wording; the divergence from the sheet's own banner is documented, not
  hidden (R8) — and is the first decision before publication (prerequisite P-1).
- **The Expert Community** shows a count per industry + position from the pool sheet and
  the market count from Talent Insight, always with the source printed.

## 3. The pages

Seven pages from one template set (R9): trends (home), eleven area pages from one
template, Bérek, SAP, Expert Pool, Esettanulmányok, Regisztráció. The client's header
menu on every page; footer navigation matches. Videos and highlights sit in labelled slots
until the client's files arrive (prerequisites C-4).

## 4. The paywall and the registration (R12–R14)

The guide is meant to sit behind a registration: an account with a type (company or
candidate). The form is an inert mock with the client's field list; its checkbox
acknowledges the privacy notice — **it is not marketing consent**. Production: the privacy
notice is real before registration runs; marketing e-mail needs its own unticked consent;
role addresses (`info@`) may be reached by legitimate interest with opt-out, named persons
and candidates only by consent (Act XLVIII/2008); no registrant's own salary is asked;
candidate matching in the Expert Pool needs the DPIA decision first (SSOT §6b).

## 5. Inert controls (R5)

Excel export, the EN switch, Kijelentkezés and every form submit are shown in place with
`is-unavailable`, `aria-disabled` and a `title` that says why; the gate checks every one.
Nothing pretends to work.

## 6. Fine-tuning (R11)

Since 2026-09-18 the guide is in fine-tuning: only the reported item changes; nothing is
restructured, hidden or removed unasked; working pages are the baseline. Every change is
measured (`07-gate.md`) and every push reports the live URL.

## 7. The data the guide holds about people

Nothing today. In production the account (e-mail, company, position, type, the notice
acknowledgement, the separate consent, created-at), the download log and the marketing
consent — with the retention and the gate rows of SSOT §6b.

## 8. The rules, mapped

| Rule | Where | Rule | Where |
|---|---|---|---|
| R1 no figure invented | §2 | R8 the client's wording, divergence documented | §2 |
| R2 the aggregate first | §2 | R9 one template per repeated thing | §3 |
| R3 no data → hidden, never substituted | §2 | R10 TOP3 in chart and table | §2 |
| R4 weighted average only | §2 | R11 fine-tuning: only the reported item | §6 |
| R5 inert controls marked | §5 | R12 notice acknowledgement ≠ marketing consent | §4 |
| R6 explicit mapping, fail loudly | §2 | R13 salary data aggregated, no Article 9 field | §2, §4 |
| R7 versioned shared assets | the gate | R14 the gate on registration, marketing, matching | §4, §7 |

## 9. What the guide never does

Invents or estimates a figure; substitutes the aggregate for a missing segment; asks a
reader's salary; treats the notice checkbox as marketing consent; pretends a control
works; restructures a working page unasked; publishes with the sheet's banner and the
page's note contradicting each other.
