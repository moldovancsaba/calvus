# DiscountDirect — audit of the business logic

*2026-09-20 (hub audit action 7). `BUSINESS-LOGIC.md` (§1–§11), the SSOT's rules R1–R25
and settings, `TECHNICAL-DESIGN.md` and the prototype (`index.html`) read against each
other, the way business.direct's logic was audited the day before. Findings A1–A8 with a
severity and a fix; every fix is PROPOSED to the product owner. The audit changed one
thing: the rules register's order (R20 was listed after R21).*

## 1. Summary

| Severity | Findings |
|---|---|
| Major | A1 (legal basis for B2C e-mail in Hungary), A2 (two holdout mechanisms), A3 (no cross-channel cap) |
| Minor | A4 ("implemented" means the codebase this repo cannot see), A5 (rule order), A6 (silent channel default), A7 (prototype behind the decisions — already ask #1 / prerequisite P-4), A8 (minors and vulnerable buyers had no rule until today) |

**Verdict.** The logic is the most complete on the hub after business.direct's — 27
decisions, formulas on every rule, a consent model per channel, reference-price
discipline, a holdout. Its weak points are on the edges the law watches: the e-mail basis
in the first market, the sum of touches across channels, and the audiences it had not
named (minors, vulnerable buyers) until the policy record of 2026-09-20.

## 2. Findings

| # | Severity | Finding | Evidence | Fix (PROPOSED) |
|---|---|---|---|---|
| A1 | major | **R15 allows a marketing send on `legitimate_interest ∧ soft_opt_in ∧ order_count ≥ 1`.** The EU ePrivacy directive's existing-customer exception exists, but Hungary's Act XLVIII/2008 §6 requires the recipient's prior, express consent for direct marketing to natural persons and is generally read as not carrying the soft-opt-in exception for e-mail. In the first market the `consent` branch may be the only lawful one for e-mail to consumers. | SSOT R15, `LegalBasis`; research I §8b of business.direct | counsel confirms per market (prerequisite P-3); until then the HU market's e-mail basis defaults to `consent`; postal letters keep opt-out (Robinson-list) handling |
| A2 | major | **Two holdout mechanisms.** The SSOT defines a deterministic bucket (`SHA-256(buyer_id + ":" + scope) mod 10000`, R19); the technical design's schema carries `holdout_seed int default floor(random()*1000000)` and a boolean per offer. A random seed per buyer and a hash per scope give different holdouts. | SSOT R19; `TECHNICAL-DESIGN.md` schema | one mechanism: the SSOT's deterministic bucket (reproducible, auditable); drop `holdout_seed` |
| A3 | major | **No cross-channel cap.** `frequency_cap` is per channel (e-mail 4 / 30 d, chat 3 / 7 d, mailing 1 / 90 d, RCS 1 / 7 d): one seller may reach a buyer ~17 times a month within the rules. The research behind the cap (§6) argued for a total. | SSOT §4 `frequency_cap`, R16 | add a total per `(buyer, seller)` per 30 days (proposal: 6) enforced with the per-channel caps; deferred, never dropped, as R16 says |
| A4 | minor | The enumerations say **"Implemented"** for states and channels (`expired`, `cancelled`, `postal`, `in_app`) that live in the existing codebase (DD-000) this repo cannot see; the prototype implements `pending → accepted / declined` only, with flash limits "carried, never evaluated" (BL §4). A reader takes "implemented" as verified. | SSOT §2; BL §4, §8; prerequisite P-1 | label the column "reported implemented in DD-000 (not verified by this repo)" until P-1 gives access |
| A5 | minor | The rules register listed R21 before R20. | SSOT §6 | reordered in this commit |
| A6 | minor | A flash campaign with no channel checked "reports chat" — a silent default the seller did not choose. | BL §3.5 | the form requires at least one channel; no silent default |
| A7 | minor | The prototype predates D1–D26 (hand-off on accept, sold-out notice, rules block, advanced mode, print mode) and the docs say so; a client seeing the demo and the decisions side by side must be told which is current. | ask #1 → prerequisite P-4; the presentation's lede says it | as decided: freeze as the pre-decision reference or update — P-4 |
| A8 | minor | Until 2026-09-20 no rule addressed a buyer who may be a minor, a buyer in hardship, dark patterns or AI-written reasons. | SSOT §6b, R22–R25 (added by hub audit action 1) | done; counsel review in P-3 |

## 3. What is consistent (checked and found sound)

- Reference price: R5's `discount_base = min(current, lowest in 30 days)` and R18 match the
  EU price-indication rule; the prototype's strike-through follows it.
- Flash quantity: R10's atomic check against both limits and R11's sold-out notice with
  optional compensation match D2/D10/D14 and BL §3.5.
- One offer per recommendation (R2), the buyer-only transition (R6), the audit of both
  reasons (R3) — consistent across BL, SSOT and the prototype.
- Transparency (R21): the rules block on every rendering is in the architecture
  (`transparency` module) and the technical design (A13).
- The engineering docs never describe a delivery gap as shipped (BL §11) — the register
  in §8 is honest.

## 4. Recommended order

A1 first (a legal question for the first market); A2 and A3 before Release 1's scheduler;
A4 and A6 as text and form fixes; A7 is the product owner's standing decision.
