# business.direct — business case for ClassScout (Your Field NYC)

*For the decision-maker at ClassScout and the owner. What this page answers: what the machine
costs to build and run, what it returns under three scenarios, where the break-even is, and what
doing nothing costs. Every input is marked **measured** (from the platform's own catalogue),
**benchmark** (a sourced industry figure) or **assumption** (ours, to be replaced by the
platform's numbers under prerequisite P-6). The formulas are the ones the prototype's Economics
screen computes (`16-analytics-and-unit-economics.md`); the run costs are the vendors' own
prices read on 2026-09-20 (`01g-research-real-system.md` §15). Written 2026-09-20 (D38).*

## 1. The situation in the client's numbers (measured, 2026-09-19 pull)

| Measure | Value | What it means |
|---|---|---|
| Providers listed | 253 | the supply side the platform has gathered |
| Providers managing their own page | **0** | nobody on the supply side is a customer yet; no reviews, no photos of their own, no answers |
| Reachable by e-mail / by phone / by website only | 130 / 73 / 50 | the sales flow's reach without any data the platform does not already hold |
| With a next session on the card / a trial policy / an announcement | 83 / 72 / 26 | the demand-side content that exists today and is not published anywhere |
| Reviews / prices on the cards | 0 / 28 | the two fields AI answers and families look for first |
| Registered families | not disclosed (prerequisite P-6); 5 000 assumed | every family-side figure below scales with it |

## 2. The cost of doing nothing (benchmarks, sourced in `01-research.md` and `01b`)

- **The enquiry economics of a small provider**: 62 % of calls to small businesses go
  unanswered; 78 % of customers buy from the business that responds first; a lead contacted
  within five minutes is 21× more likely to qualify than after thirty. An unclaimed, unanswered
  card sends the family to the next provider — or off the platform.
- **The discovery shift**: organic Google sends 19 % fewer clicks to the same rankings; AI
  answers cite the structured, reviewed source; nearly half of Gen Z searches social before
  Google. A catalogue with 0 reviews and 28 prices is not the source that gets cited.
- **The category's money**: US families spend $1 016 per child per sport, up 46 % in five
  years. The platform captures none of it while providers stay unmanaged.
- **The incumbents' move**: Yelp bought Hatch for $270 M (January 2026) and sells Receptionist
  at $99 a month — the same "answer, follow up, convert" service, to the same small businesses.

Doing nothing keeps the platform a directory: supply gathered by a pipeline, demand served a
list, nobody paid.

## 3. What the machine changes (the answer, in one loop)

Events → nightly metrics → the next dollar ranked → a person approves → measure. Two flows at
the front door — **families brought to the listing page** by published real content, and
**providers brought to manage their page** by a sales sequence that honours the law and a cap —
and behind them provider campaigns, conversations and upgrades on the platform's own products.
Nothing leaves without a person; every message says why it was sent.

## 4. Investment

| Line | Amount | Basis |
|---|---|---|
| Build effort | **34 developer-weeks** (two developers × nine two-week sprints, seventeen weeks) + the owner as product lead | `13-implementation-plan.md` §2b |
| Build cost | 34 × blended rate per developer-week — **the rate is the commercial input, set by the owner**; illustration at $2 500 / $4 000 / $6 000 → $85 k / $136 k / $204 k | assumption (illustration only, not a quote) |
| Run cost, pilot (≤ 300 providers, ≤ 5 000 families) | **≈ $50–75 a month** | vendor prices, `01g` §15 |
| Run cost, sizing target (1 000 providers, 50 000 families) | **≈ $280–400 a month** | vendor prices, `01g` §15 |
| Operator time | 2 minutes per approval at $40/h; ~10 hours a month at pilot volume, falling with batch approval and earned auto-approval | assumption; `16` §2.2 |
| Sales tooling | $150 a month (sending domain, warm-up, enrichment) | assumption; `16` §2.2 |
| External lead times | Meta App Review two to four weeks (starts sprint 0); Twilio registration one to two weeks (only when SMS is switched on) | `01g` §14 |

## 5. Return — three scenarios (the model's formulas at the stated inputs)

The unit economics (`16` §2): contribution = ARPA × margin; LTV = contribution ÷ monthly churn;
CAC = outbound cost ÷ new paying providers; healthy at LTV : CAC ≥ 3 and payback ≤ 12 months.
Defaults: reply 5.5 % (benchmark, top quartile), applied 40 % (assumption), managing 80 %
(assumption), upgraded 25 % (assumption), ARPA $49 (sample prices), margin 80 %, churn 5 %/month
(benchmark range 3–7 %).

| Scenario | What changes | Outbound cost / quarter | New managing / upgraded per quarter | CAC (upgraded) | LTV | LTV : CAC | Payback |
|---|---|---|---|---|---|---|---|
| **0 · Defaults (the honest finding)** | 253 providers, $49 ARPA, 5 % churn | ≈ $720 | ≈ 2 / 0.6 | ≈ $1 200 | $784 | **0.7** | 31 months |
| **A · Growth engine** (recommended framing, D21) | the base machine is bundled by the platform; its return is counted in managed pages and families, not in upgrades | ≈ $720 + $120 content | ≈ 2 managing; ≈ 32 new families a month from content at 1.5 families per post (assumption) | — | — | content: **$4 per new family against $6 expected value** (thin, positive, measured by the connected channel); each managing provider answers enquiries within the hour instead of losing 62 % of calls | — |
| **B · Larger catalogue** | 1 000 providers, same rates and prices | cost mostly fixed tooling | ≈ 8 / 2 | **< $400** | $784 | **≈ 2** | ≈ 10 months |
| **C · Higher ARPA, lower churn** | mix ARPA $89 (camp placement $149/season in the mix), annual plans → churn 3 % | as 0 | as 0 | ≈ $1 200 (253) · < $400 (1 000) | **$2 373** | **≈ 2 (253) · ≈ 6 (1 000)** | 17 months (253) · 6 months (1 000) |

Reading: outbound e-mail alone, on today's catalogue and sample prices, does not pay for itself
— the model says so and the presentation says so. The machine pays as the platform's growth
engine (A) from day one, and as a profit centre once the catalogue grows (B) or the products are
priced for the category (C); the platform decides which, and each is one input on the Economics
screen.

**The family side (the marketing value the platform is building).** An avid family — saved ≥ 3
providers, opens the digest, has asked a provider — is worth ≈ $813 a year to the providers it
reaches (2 trials × 40 % enrolment × $1 016) and ≈ $42 a year to the platform at a 5 % capture
plus referrals (assumptions until measured). At 5 000 families and 15 % avid, that is ≈ $610 k a
year of provider revenue flowing through the platform's introductions — the number the upgrade
products are priced against.

## 6. Sensitivity (what moves the answer most)

| Input | −50 % | Default | +50 % / top decile | Effect on LTV : CAC (scenario 0 → B) |
|---|---|---|---|---|
| Reply rate | 2.75 % | 5.5 % | 10.7 % (top decile) | 0.35 → 1.3 at 253; the largest lever the machine controls (propensity order, the family's ask as a touch, the call list) |
| Applied → managing → upgraded | 0.5× | 40 % · 80 % · 25 % | 1.5× | linear in CAC; measured from the first cohort (R16, at 100 observations) |
| Monthly churn | 7 % | 5 % | 3 % | LTV $560 → $784 → $1 307; annual plans are the lever |
| ARPA | $29 | $49 | $89 | LTV $464 → $784 → $1 424; the platform's pricing decision |
| Catalogue size | 253 | 253 | 1 000 | CAC $1 200 → < $400; the fixed tooling is spread |

## 7. Break-even

- **Growth engine (A)**: the run cost at pilot (≈ $60 a month) is covered by **two** upgraded
  providers at $49; at the sizing target (≈ $340 a month) by **eight**.
- **Profit centre (B or C)**: LTV : CAC crosses 3 : 1 at roughly 1 000 providers with ARPA ≈ $70
  and churn ≤ 4 % — or at 253 providers only with ARPA ≥ $135 and churn ≤ 3 %.
- **Build cost**: recovered from upgrades alone only in B or C; in A it is the platform's
  investment in becoming the source that gets cited and the place families come back to —
  measured as new families per post, managed pages and answered enquiries from the first sprint.

## 8. What we need from the client, and when

Nothing before the decision. After it: the postal address, the privacy-policy paragraph, the
policy record confirmed and counsel's wording before the first real message; the opted-in share,
the analytics events, the write key and a pilot provider before the keyed release; the personas,
the integrations and the money model confirmed at acceptance (`19-implementation-prerequisites.md`).

## 9. The decision

Go ahead with the build (sprint 0 starts on the decision; Meta's review is submitted the same
week), or do not. The first measured numbers — reply rate, families per post, enquiries answered
— arrive at the end of sprint 2 and replace the assumptions above on the Economics screen.
