# IDBC Salary Guide — decision register

*Numbered, dated, with who decided and what it replaced. Reconstructed on 2026-09-18 from
the dated entries in `SOURCES-AND-GAPS.md` and the commit history; from here on, a new
decision is added here first. "Owner" is the Calvus side; "client" is IDBC.*

| # | Date | Decision | By | Why / what it replaced |
|---|---|---|---|---|
| D1 | 2026-07-30 | Bérezés and Expert Pool become standalone pages; the trends page keeps the survey only | owner | one combined page had grown past what a reader could hold; also the spec's page split |
| D2 | 2026-07-30 | Empty salary columns are hidden rather than shown as dashes | owner | a column of "–" reads as missing data |
| D3 | 2026-07-31 | Ordinal answer scales keep their order; 0 %-response options are hidden everywhere | owner | zero-respondent options presented as findings |
| D4 | 2026-08-17 | Adopt the client's `3_SAP` mockup as the layout of all three subpages; build the point-line TOP3 chart from it as a shared component | owner | replaced the static range cards; the mockup was the client's own design |
| D5 | 2026-08-17 | The salary band's two ends are labelled "Vállalatok által kínált bér" / "Jelöltek által elvárt bér" per the mockup, although the sheet holds one range | owner | a labelling choice, recorded as gap 6 with its risk; the neutral "Min./Max." was rejected |
| D6 | 2026-08-18 | "Összes" (later "Összesített adatok") is a pseudo-segment, always first and default; segment options are computed per topic | owner | landing on a real segment with zero respondents |
| D7 | 2026-08-24 | Two topics renamed and the EU pay-transparency question moved to the end of Bérezés | client | editorial |
| D8 | 2026-08-24 | Eleven-area filter on the trends page with a per-area summary block; the summaries do not filter the survey until re-tabulated data exists | client ask, owner scope | honest skeleton over a fake filter |
| D9 | 2026-08-25 | Questions with no data under a real segment are hidden outright; the aggregate is never shown in their place; one panel-level sentence remains | owner, refining the client's per-question message | the client saw the message version live and the owner simplified |
| D10 | 2026-08-25 | The stacked whole-sample chart is the only rendering of the two 1–4 scale questions; the mean-bar variant is rejected | owner | "the stacked chart is the good one" |
| D11 | 2026-08-25 | The area dropdown is replaced by eleven area links opening a dedicated area page from one template; area texts move to `areas.json` | owner, after client feedback | one renderer for eleven areas instead of eleven copies |
| D12 | 2026-08-25 | Until per-area data exists, area pages show the matching edition's pooled sample and say so | owner | never claim area-level data that does not exist |
| D13 | 2026-08-25 | The client's final area names and texts are adopted; five labels renamed | client | `SG_Területi_összefoglalók_final.docx` |
| D14 | 2026-08 | The Bérsávok table returns to neutral Minimum / Maximum headers; the chart keeps the stakeholder labels; the client's "valós piaci adatok" note is shipped as their copy | client | recorded next to gap 6 |
| D15 | 2026-09-01 | Area pages read the client's per-area re-tabulation; the pooled stand-in (D12) is retired | owner, on client data | closes the client's 2026-09-01 feedback on missing segment filters |
| D16 | 2026-09-08 | The final workbook replaces the survey half; `datasets` replaces editions/answers; the two 1–4 questions show the weighted average only; the aggregate is labelled "Összesített adatok" | client (data and labels), owner (schema) | "ez már a teljesen végleges kutatási anyag" |
| D17 | 2026-09-15 | Below 600 px of container width the salary tables render as cards; Bérsávok groups collapse behind a header, SAP rows do not | owner | 419 px of sideways overflow on a phone |
| D18 | 2026-09-16 | SAP cards collapse like Bérsávok'; the panel behind the mobile cards is dropped, the cards stay white; the TOP3 chart gets a narrow one-block-per-position layout with its own value scale under every chart | client (workshop) | corrected once by the client the same day |
| D19 | 2026-09-18 | Header on every page: Piaci trendek · Bérek · SAP · Expert Pool · Esettanulmányok, Ajánlatkérés and Kijelentkezés right-aligned; Ajánlatkérés links to `idbc.hu/ajanlatkeres/` pending confirmation | client (menu), owner (target) | the client named the item, not the target |
| D20 | 2026-09-18 | Area media: seven areas get a video placeholder, four a key-thought box; the Finance infographic slot is retired | client | their list of which area gets which |
| D21 | 2026-09-18 | Expert Pool becomes the Expert Community page with the client's copy; tiles per the client's PNG; join and contact forms inert | client (copy, tile), owner (inert forms) | |
| D22 | 2026-09-18 | TOP3 rows carry a LinkedIn pill and a footnote; counts matched by an explicit table, never guessed; a renamed position fails the build | owner | the first pass showed zero pills because the old bértábla did not match |
| D23 | 2026-09-18 | The salary data is rebuilt from the client's current bértábla (13 areas, 432 rows, 39 standalone TOP3 rows); area codes get the names already used on the trends pages; Sales and Marketing stay split | owner, on client data | the Talent Insight list was cut to this table |
| D24 | 2026-09-18 | The Bérek and SAP tables always show and include the TOP3 rows | owner, reverting the same day's exclusion | the owner saw a missing table on Retail; the table is the complete reference |
| D25 | 2026-09-18 | Esettanulmányok is a conventional article, not a card grid | client and owner (workshop) | the first pass had not been briefed |
| D26 | 2026-09-18 | Expert Pool tile bars align to the card bottom so tiles with and without a market line line up | client note | |
| D27 | 2026-09-18 | Standard documentation structure; technical package written with every stack decision in status PROPOSED | owner | see `11-architecture.md` §11; the flip of any ADR is the next D-number here |
| D28 | 2026-09-20 | A **responsible-data policy record** for the guide (SSOT §6b, PROPOSED): the registration checkbox is a notice acknowledgement, not marketing consent; B2B role addresses by legitimate interest, named persons and candidates by consent; salary data stays aggregated; the privacy notice must be real before registration runs — rules R12–R14 | Calvus, on the owner's directive (responsible data for every client) and the hub audit | docs only; no page changed (fine-tuning rule) |

## Standing rules that came out of these

- No figure is ever invented; an inert control is shown with an "unavailable" treatment and a reason (D2, D9, D12, D22).
- The client's own copy ships as written, even where it asserts more than the source data does — and the divergence is recorded (D5, D14).
- One template per repeated thing (area pages, tiles, chart) — never eleven copies (D11).
- In fine-tuning, only the reported item changes; nothing is restructured or hidden unasked (D24, D25).
