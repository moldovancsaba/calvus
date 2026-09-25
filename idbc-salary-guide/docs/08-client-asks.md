# IDBC Salary Guide — the register of asks

*Every item that once needed the client, with its state. Since 2026-09-20 (owner's rule:
an ask is never a presentation blocker) the open items are the client's pending content
deliveries and the decisions for publication, listed in `19-implementation-prerequisites.md`.*

## Open for the next review

A 2026-09-22 feedback mail mixed real prototype fixes (closed this round, see
`README.md`'s process log and `SOURCES-AND-GAPS.md`'s 2026-09-22 entry) with three items
this studio cannot resolve without more from the client. The client repeated #16 on
2026-09-25 (its own mail, unchanged) — the parsed data still doesn't have it; still needs
the source file, not a re-ask:

| # | Item | What's needed |
|---|---|---|
| 16 | Two survey questions ("current home office policy's effect on recruiting success"; two AI questions for non-IT employers) don't exist anywhere in the parsed research data | The source Excel's "Téma besorolás" sheet checked — this repo has no copy of it. If the data exists, it's a converter fix; if those segments were genuinely never asked, it's not something to fabricate. |
| 17 | "IT Contracting" as a Bérek salary segment — the bértábla sheet has no rows for it (the separate market-trends survey data does have it) | IT Contracting salary figures from the client, or confirmation the segment is already folded into "IT" today. Since D37 the figures go into `IDBCSYNC` as new `SAL-` rows (new ids, so the studio adds them once the figures arrive); the area appears in the Bérek filter as soon as it has one row. **Asked directly in the sheet itself** on 2026-09-25 — a new tab, "HIÁNYZÓ ADATOK - kérés". |
| 18 | Expert Pool page text content — the client says this was sent previously; it never reached this implementation round | Resend, or point to where it lives. |
| 21 | `EXPERT_POOL_IMPORT`'s `Non-IT / Qualified Person` row has no headcount (2026-09-25 sync) | The number, or confirmation the row should be removed. **Asked directly in the sheet itself** on 2026-09-25 — same new tab. |

## Moved to the prerequisites (`19-implementation-prerequisites.md`)

| # | Item | Now |
|---|---|---|
| 1 | Kezdőoldal structure demo | C-1 — content pending from the client |
| 2 | Bérek and Expert Pool structure demos | C-2 — content pending |
| 3 | Two Építőipar Talent Insight counts | C-3 — content pending |
| 4 | Two Expert Pool Talent Insight counts | C-3 — content pending |
| 5 | Area videos (7) | C-4 — content pending |
| 6 | Area key thoughts (4) | C-4 — content pending |
| 7 | Case-study videos (2) | C-4 — content pending |
| 8 | Ajánlatkérés target | ~~P-3~~ — **resolved 2026-09-22**, now the in-guide `kapcsolat/` page |
| 9 | Area labels for the bértábla codes | ~~P-2~~ — **resolved 2026-09-22**, the client's mail gave the final wording for both Piaci trendek's and Bérek's own separate lists |
| 10 | Excel export | P-4 — before publication |
| 11 | EN edition | P-5 — before publication |
| 12 | Chamber logos, podcast embed | C-5 — content pending |
| 13 | The bértábla banner (sample values vs "valós piaci adatok") | P-1 — before publication |
| 14 | Decisions on the technical package | T-1 — production build |
| 15 | Hero photographs | C-6 — content pending |

## Closed

See the process log in `README.md` for every item closed by a client mail round (2026-08-24,
2026-08-25, 2026-09-01, 2026-09-08, 2026-09-18, 2026-09-22, 2026-09-24, 2026-09-25).

Three 2026-09-25 items answered without needing anything further from the client:

| # | Item | Answer |
|---|---|---|
| 19 | TOP3 chart labels "skewing" when values sit close together | Fixed — a label-placement bug, reached every page sharing the chart, D33 |
| 20 | Whether BSC's "Sales Project Manager" showing "Manager" is Drive-editable | Yes — it's the bértábla sheet's own `szint` column for that row, read verbatim; blank it there and re-run the converter to remove it, D34 |
| 22 | Live (or on-demand) sync to the `IDBC_bertabla` sheet | Built — `.github/workflows/idbc-sync-bertabla.yml`, manual trigger, gated, auto-commits on a real diff. Along the way: the sheet's own area naming had drifted from the site's and was corrected in the sheet; Expert Pool's whole category system had already changed in the sheet (15 → 29 rows, new IT/Non-IT taxonomy) and is now live on the site, D35 |
