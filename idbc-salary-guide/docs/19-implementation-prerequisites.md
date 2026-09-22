# IDBC Salary Guide — prerequisites (the client's pending deliveries and the decisions for publication; nothing blocks presenting the current state)

*Written 2026-09-20 on the owner's rule (business.direct D34, hub audit action 3): an ask is
never a presentation blocker. The guide stands and is presentable as it is — every missing
piece has a declared placeholder on the page. The client's content deliveries land where
the table says when they arrive; the decisions are needed before publication or the
production build, not before the next review.*

## 1. Content the client has promised (lands in place when it arrives)

| # | Delivery | Lands in | Until then |
|---|---|---|---|
| C-1 (ask #1) | The home page's structure demo (copy already received: intro signed Dohos Ágnes and Illés József, methodology, six chamber logos, podcast playlist, sample sizes) | a new home page | the trends page is the home |
| C-2 (ask #2) | The Bérek and Expert Pool structure demos | layout adjustments, if any | the current pages |
| C-3 (asks #3–4) | Four LinkedIn Talent Insight counts (two Építőipar, two Expert Community) | TOP3 pills on Bérek; tile market lines | the pill / line is absent, by rule (no figure invented) |
| C-4 (asks #5–7) | Seven area videos, four area key thoughts, two case-study videos | `terulet/` media slot and highlight box; `esettanulmanyok/` | labelled placeholders |
| C-5 (ask #12) | Chamber logos, podcast embed | the home page (with C-1) | — |
| C-6 (ask #15) | IDBC's own hero photographs, or confirmation that the stock photographs stay | every page hero | stock (Unsplash) and one idbc.hu image |
| C-7 (ask #16, 2026-09-22) | The source Excel's "Téma besorolás" sheet checked for two survey questions missing from the parsed data (a home-office/recruiting-impact question; two non-IT AI employer questions) | `guide-data.json`'s topics, if the data exists | absent — may be genuine survey segmentation (IT respondents consistently get extra questions elsewhere too), not a parsing bug |
| C-8 (ask #17, 2026-09-22) | "IT Contracting" salary figures for Bérek, or confirmation the segment is folded into "IT" | `data/build-salary-data.py`'s `AREA_NAME`, already has the slot ready | the filter option simply doesn't appear (zero rows) |
| C-9 (ask #18, 2026-09-22) | Expert Pool page text content (client says previously sent; not received in this round) | `expert-pool/index.html` | the existing copy stays |

## 2. Decisions before publication

| # | Decision | Why |
|---|---|---|
| P-1 (ask #13) | **The bértábla banner**: the sheet says the figures are sample values awaiting professional approval; the pages say "valós piaci adatok" — which is true | nothing publishes with a contradiction between the source and the page |
| ~~P-2 (ask #9)~~ | ~~The area display names for the bértábla codes~~ — **resolved 2026-09-22**: the client's mail gave final wording for both Bérek's own list and, separately, Piaci trendek's (confirmed genuinely different from each other, not reconciled) | the Bérek filter labels |
| ~~P-3 (ask #8)~~ | ~~The Ajánlatkérés target~~ — **resolved 2026-09-22**: now the in-guide `kapcsolat/` contact-only page | the header link on every page |
| P-4 (ask #10) | Excel export: the file, or confirmation it is generated from the same data at build | the inert CTA on three pages |
| P-5 (ask #11) | Whether an English edition is wanted (there is no EN copy) | the inert EN switch |

## 3. Decisions for the production build (the technical package, `11-architecture.md` §11)

| # | Decision | Why |
|---|---|---|
| T-1 (ask #14) | Stack, paywall, hosting — the ADRs are PROPOSED | everything after the prototype |
| T-2 (SSOT §6b) | The responsible-data policy record confirmed: the real privacy notice behind the registration form, a separate marketing consent, retention, the Expert Pool DPIA decision | registration and marketing e-mail are gated on it |

## 4. What the next review needs from the client

Nothing. The guide is reviewed as it stands; the deliveries above improve it as they arrive.
