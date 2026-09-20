# business.direct — the value for the media owner: the economics as a service

*For a classified media owner. What this page answers: what business.direct computes for you,
on your numbers, every night — what a listing sells for and earns, what an advertiser costs to
win and is worth, what a visitor costs to bring in and is worth, what churn costs and retention
keeps, all costs and incomes, and where the next dollar goes — and what it read on the first
customer's listings. Every input is marked **measured** (from the site's own data), **benchmark**
(sourced) or **assumption** (a placeholder on the screen until your data replaces it). The
formulas are the ones the product's Economics screen computes (`16-analytics-and-unit-economics.md`
is the department's specification). Written 2026-09-20 (D41). ClassScout (Your Field NYC) is
the worked example.*

## 1. What the product computes for the owner

| Question the owner asks | The product's answer | Inputs |
|---|---|---|
| **What does a listing sell for?** | the site's advertising products and their prices — featured placement, category placement, discovery profile — with the plan ladder every advertiser is on | the site's products (Your Field: $49 / month, $149 / season, $29 / month — sample until the site sets them) |
| **What does an advertiser cost to win?** | **CAC** = outbound cost (touches, calls, operator minutes, tooling) ÷ new managing advertisers; and ÷ new paying advertisers | touches per prospect, cost per touch, cost per call, operator minutes per approval and rate, tooling |
| **What is an advertiser worth?** | **LTV** = monthly contribution (price × margin) ÷ monthly churn; **payback** = CAC ÷ contribution; healthy at LTV : CAC ≥ 3 and payback ≤ 12 months | price, margin, churn |
| **What does a visitor cost to bring in?** | cost per new visitor from content = content stack ÷ (posts × new visitors per post); compared with what an engaged visitor is worth | posts per week, new visitors per post (measured once a channel is connected), content stack |
| **What is a visitor worth?** | value delivered to advertisers per engaged visitor per year (enquiries × conversion × the advertiser's revenue per conversion) and the site's share of it (capture, measured as placements bought within 30 days of a delivered result) | engaged share, enquiries per year, conversion, revenue per conversion, capture, referrals |
| **What does churn cost, what does retention keep?** | LTV at risk = advertisers at risk × LTV; expected kept = at risk × share kept by a touch × LTV; keeping costs a touch, replacing costs a CAC | churn, share kept (measured from the retention log) |
| **Where does the next dollar go?** | four levers ranked weekly by expected value per dollar: one more touch to the unreplied, the call list, a week of content, retention touches to the at-risk | all of the above |
| **What is the plan?** | twelve months of managing and paying advertisers, monthly revenue (placements + any priced service line), cost and cumulative cash — every month follows the inputs | the funnel rates, churn, price |
| **Which numbers are real?** | every tile says measured / benchmark / assumption; a rate flips to measured at 100 observations | the event log |

## 2. The funnel and its rates (what the owner sees on the sales side)

| Stage | Rate to next | Status | Source |
|---|---|---|---|
| Listed → reachable | by e-mail, by phone, by website only — from the listings | measured | the site's own data |
| Reachable → replied | 5.5 % (top quartile); 3.4 % average; 10.7 % top decile; 42 % of replies come from the follow-ups | benchmark (K1) | `23-claims-register.md` |
| Replied → applied | 40 % | assumption | — |
| Applied → managing | 80 % (the site confirms the claim) | assumption | — |
| Managing → paying within 3 months | 25 % | assumption; SMB activation 35–50 % | research II §2.2 |
| Paying → churned per month | 5 % (3–7 % range) | benchmark | research II §2.2 |
| At risk → kept by a retention touch | 30 % | assumption; measured from the retention log | — |

## 3. The worked example — what the product read on the first customer's listings (2026-09-19 pull)

Your Field NYC, 253 providers pulled (the demo's data; the customer's catalogue is far larger):
130 reachable by e-mail, 73 by phone only, 50 by website only; 0 managing; sample prices $49 /
$29 / $149 per season.

| The screen says | Value | Reading |
|---|---|---|
| CAC · managing advertiser | ≈ $300 | one quarter of outbound (three touches, the call list, the operator's minutes, $150 tooling) wins ≈ 2 managing advertisers |
| CAC · paying advertiser | ≈ $1 200 | ≈ 0.6 paying per quarter at the assumed rates |
| LTV · paying advertiser | $784 | $49 × 80 % margin ÷ 5 % churn |
| **LTV : CAC** | **0.7** — below the 3 : 1 line | outbound alone, on this pull at sample prices, does not pay for a $49 placement; payback 31 months |
| Cost per new visitor from content | ≈ $4 | $120 content stack ÷ (5 posts × 1.5 new visitors per post) |
| Value of an engaged visitor | ≈ $42 a year to the site; ≈ $813 to the advertisers it reaches | 2 enquiries × 40 % conversion × $1 016 (Project Play: family spend per child per sport); 5 % capture |
| Advertisers at risk (sample cohort) | 4 of 7 managing | LTV at risk ≈ $3 100; expected kept at 30 % ≈ $940 |
| Next dollar | retention touches, then one more e-mail touch | keeping an advertiser costs a touch; replacing one costs the CAC above |

**What turns it — three inputs on the same screen.** (a) **Scale**: at 1 000 listings the
tooling is spread and CAC falls under $400 (LTV : CAC ≈ 2, payback ≈ 10 months). (b) **Price for
the category**: a placement mix at $89 with annual plans (3 % churn) makes LTV $2 373 (≈ 2 at
253 listings, ≈ 6 at 1 000). (c) **Count the demand side**: the same outbound also produces
managing advertisers who answer enquiries and visitors who come back — at 5 000 visitors and
15 % engaged, ≈ $610 k a year of advertiser revenue flows through the site's introductions, the
number the placements are priced against. The owner chooses which; the product shows each.

## 4. Sensitivity (what moves the owner's answer most)

| Input | −50 % | Default | +50 % / top decile | Effect |
|---|---|---|---|---|
| Reply rate | 2.75 % | 5.5 % | 10.7 % | LTV : CAC 0.35 → 0.7 → 1.3 at 253 listings; the largest lever the product controls (propensity order, the visitor's enquiry as a touch, the call list) |
| Applied → managing → paying | 0.5× | 40 · 80 · 25 % | 1.5× | linear in CAC; measured from the first cohort |
| Monthly churn | 7 % | 5 % | 3 % | LTV $560 → $784 → $1 307; retention and annual plans are the levers |
| Placement price | $29 | $49 | $89 | LTV $464 → $784 → $1 424; the owner's pricing decision |
| Listings | 253 | 253 | 1 000 | CAC $1 200 → < $400; fixed tooling spread |
| Share kept by a retention touch | 15 % | 30 % | 45 % | expected kept ≈ $470 → $940 → $1 400 on the sample cohort |

## 5. The costs the owner carries, as the product counts them

| Line | Default | Status |
|---|---|---|
| E-mail touches | 3 per prospect at $0.05 | assumption; sending domain and warm-up in tooling |
| Call tasks | $5 per phone-only prospect (operator minutes) | assumption |
| Operator time | 2 minutes per approval at $40 / hour; measured on the screen as "operator hours this week"; falls as departments earn auto-approval | measured in use |
| Sales tooling | $150 / month (sending domain, warm-up, enrichment) | assumption |
| Content stack | $120 / month (clip engine, image, audio) | assumption; research II §4 |
| The product's run cost per site | ≈ $50–75 / month at pilot volume; ≈ $280–400 at 1 000 listings and 50 000 visitors | vendors' prices, `01g` §15 — carried by the product, not the owner |

## 6. What the owner provides, and when

At onboarding: the site's API and channels; the policy record (jurisdictions, consent per
channel, the cap, the postal address, the privacy-policy clauses); the knowledge files. Then, as
they exist: the site's analytics events (visitors, sign-ups with source, saves, opens,
bookings), the real placement prices, a write key for claims and card flags, and one pilot
advertiser's numbers — each replaces an assumption on the screen. For the first customer the
list is `19-implementation-prerequisites.md`.

## 7. The decision

Use the product; let the first cohort replace the assumptions. The screen is the argument: it
shows the owner's numbers, says which are real, and ranks the next dollar every week.
