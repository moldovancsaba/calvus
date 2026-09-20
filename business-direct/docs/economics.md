# business.direct — the Economics department: the value for the media owner, and the model behind the screen

*For a classified media owner. What this page answers: what business.direct computes for you,
on your numbers, every night — what a listing sells for and earns, what an advertiser costs to
win and is worth, what a visitor costs to bring in and is worth, what churn costs and retention
keeps, all costs and incomes, and where the next dollar goes. Every input is marked **measured** (from the site's own data), **benchmark**
(sourced) or **assumption** (a placeholder on the screen until your data replaces it). The
formulas are the ones the product's Economics screen computes; Part B below is the department's
specification (the model, the events, the decision rules). No customer's numbers appear here: §3 is
an illustration on placeholders; the owner's numbers live on the owner's screen.*

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
| Reachable → replied | 5.5 % (top quartile); 3.4 % average; 10.7 % top decile; 42 % of replies come from the follow-ups | benchmark (K1) | `evidence.md` |
| Replied → applied | 40 % | assumption | — |
| Applied → managing | 80 % (the site confirms the claim) | assumption | — |
| Managing → paying within 3 months | 25 % | assumption; SMB activation 35–50 % | research II §2.2 |
| Paying → churned per month | 5 % (3–7 % range) | benchmark | research II §2.2 |
| At risk → kept by a retention touch | 30 % | assumption; measured from the retention log | — |

## 3. An illustration on placeholder inputs (not any customer's numbers)

To show what the screen does, run it on placeholders: a site with a few hundred reachable
listings, placements at $49 a month, 5 % monthly churn, the benchmark reply rate and the assumed
funnel rates above, a $150 tooling line and $120 of content stack. On those placeholders the screen
reports a CAC per paying advertiser near $1 200 against an LTV of $784 — **an LTV : CAC below 1**,
with a payback beyond two years — and says so plainly; it then shows the three inputs that turn
it: **scale** (four times the listings spreads the fixed tooling and cuts CAC under $400), **price
and term** (a placement mix near $90 with annual plans triples LTV), and **counting the demand
side** (the same outbound also produces answered enquiries and returning visitors, whose value the
screen computes separately). None of this is a statement about any customer: the owner's
Economics screen runs on the owner's listings, prices and events, and every figure carries its
status — measured, benchmark or placeholder — until the site's data replaces it.

## 4. Sensitivity (what moves the owner's answer most)

| Input | −50 % | Default | +50 % / top decile | Effect |
|---|---|---|---|---|
| Reply rate | 2.75 % | 5.5 % | 10.7 % | LTV : CAC roughly halves or doubles with it; the largest lever the product controls (propensity order, the visitor's enquiry as a touch, the call list) |
| Applied → managing → paying | 0.5× | 40 · 80 · 25 % | 1.5× | linear in CAC; measured from the first cohort |
| Monthly churn | 7 % | 5 % | 3 % | LTV $560 → $784 → $1 307; retention and annual plans are the levers |
| Placement price | $29 | $49 | $89 | LTV $464 → $784 → $1 424; the owner's pricing decision |
| Listings | ×1 | ×1 | ×4 | CAC falls by about two thirds as the fixed tooling is spread |
| Share kept by a retention touch | 15 % | 30 % | 45 % | the expected kept value scales linearly with it |

## 5. The costs the owner carries, as the product counts them

| Line | Default | Status |
|---|---|---|
| E-mail touches | 3 per prospect at $0.05 | assumption; sending domain and warm-up in tooling |
| Call tasks | $5 per phone-only prospect (operator minutes) | assumption |
| Operator time | 2 minutes per approval at $40 / hour; measured on the screen as "operator hours this week"; falls as departments earn auto-approval | measured in use |
| Sales tooling | $150 / month (sending domain, warm-up, enrichment) | assumption |
| Content stack | $120 / month (clip engine, image, audio) | assumption; research II §4 |

## 6. What the owner provides, and when

At onboarding: the site's API and channels; the policy record (jurisdictions, consent per
channel, the cap, the postal address, the privacy-policy clauses); the knowledge files. Then, as
they exist: the site's analytics events (visitors, sign-ups with source, saves, opens,
bookings), the real placement prices, a write key for claims and card flags, and one pilot
advertiser's numbers — each replaces an assumption on the screen. For the first customer the
list is `first-customer-classscout.md`.

## 7. The decision

Use the product; let the first cohort replace the assumptions. The screen is the argument: it
shows the owner's numbers, says which are real, and ranks the next dollar every week.

## Part B — the department's specification: the model, the events, the decision rules

*The specification of the Economics screen — the owner's economics as a service. Written on the owner's directive: "we will need ROI calculations and planning for
CAC and LTV for B2B clients, marketing value for the avid users, and all the other analytics
information that helps the system deliver data-driven marketing decisions." This is the
model the *Economics* screen (`../index.html?view=platform&screen=economics`) computes; the
screen's inputs are this document's assumptions, and every number that is not from the
catalogue or a cited benchmark is marked so. Terms are the SSOT's; the decision rules become
R16–R19 there.*

### 1. What the numbers are for

The machine spends three things — e-mail touches, operator minutes and tool subscriptions —
and gets back providers who manage their page, providers who pay, and families who come,
save, ask and enrol. Data-driven marketing here means four questions the system can answer
from its own events, every week:

1. **What does a paying provider cost and what is it worth?** (CAC, LTV, payback, LTV:CAC)
2. **What is a family worth, and an *avid* one?** (marketing value on the demand side)
3. **Does content pay?** (cost per family from the content engine vs the value of a family)
4. **Where does the next dollar go?** (expected LTV gained per dollar, across the three
   levers: another touch, a call, a week of content)

### 2. The B2B model: providers (the platform's B2B clients)

#### 2.1 Funnel and rates

| Stage | Count | Rate to next | Source of the rate |
|---|---|---|---|
| Identified | from the instance's listings | — | the site |
| Reachable by e-mail | from the listings | reply **5.5 %** (top-quartile benchmark; 3.43 % average, 10.7 % top decile) | [Instantly 2026 benchmark](https://instantly.ai/cold-email-benchmark-report-2026) (research II §5.1) |
| Phone only | from the listings | a call converts ~3× an e-mail; half are reached | assumption; multi-channel +40 % (research II §5.1) |
| Website only | from the listings | not in the model until a form step exists | — |
| Replied → applied | — | **40 %** | assumption |
| Applied → managing | — | **80 %** (the platform confirms the claim) | assumption |
| Managing → upgraded within 3 months | — | **25 %** | assumption; SMB activation 35–50 % (research II §2.2) |

#### 2.2 Cost of acquisition

`cost = e-mailed × touches × cost per touch + phone-only × cost per call + approvals ×
operator minutes ÷ 60 × operator rate + tooling × 3 months`

Defaults: 3 touches at $0.05, $5 per call task, 2 operator minutes per approval at $40/h,
$150/month tooling (sending domain, warm-up, enrichment). **Operator hours** are the
dominant cost (audit A10): the screen counts every approval and shows the hours; batch
approval and earned auto-approval (R25) are the levers that bring them down. **CAC (managing)** = cost ÷ new
managing providers; **CAC (upgraded)** = cost ÷ new paying providers.

#### 2.3 Lifetime value

`contribution = ARPA × gross margin` · `LTV = contribution ÷ monthly churn` ·
`payback = CAC ÷ contribution` · **healthy when LTV : CAC ≥ 3 and payback ≤ 12 months**.

Defaults: ARPA $49/month (the first instance's three placements at placeholder prices: $49, $29,
$149 per season), margin 80 %, churn 5 %/month (SMB SaaS range 3–7 %, research II §2.2).
A **conversations line** input (default 0 = included in the placement; Yelp Receptionist sells the
same thing at $99) adds revenue per *managing* provider to the plan's MRR (Q12) — the
owner's pricing decision is one number on the screen.

#### 2.4 What the defaults say (the first data-driven finding)

On placeholder inputs (a few hundred reachable listings, $49 placements, 5 % churn, the
benchmark reply rate), one quarter of outbound yields about 2 managing and 0.6 paying advertisers
for ~$720 — **CAC (paying) ≈ $1,200 against an LTV of $784: LTV : CAC below 1, payback beyond two
years.** Raising the reply rate to the top decile (10.7 %) only reaches 1.3 : 1. That is the model
reporting an unfavourable lever honestly — on placeholders, not on any customer's numbers. On a
real instance it pays in one of three ways, and the screen shows which:

- **the marketing and sales departments as the site's growth engine, not a profit centre** (their
  return is visitors and managing advertisers, valued below), or
- **more listings** (the cost is mostly fixed tooling; at four times the listings CAC falls by
  about two thirds with the same rates), or
- **higher ARPA** (a seasonal placement, bundles) and lower churn (annual plans).

The screen makes each of these one input away.

### 3. The B2C model: families and the value of an avid user

#### 3.1 Definitions

- **Family**: an account on the platform (count is the platform's — prerequisite P-6; 5,000 assumed).
- **Avid family**: saved ≥ 3 providers, opened the last two digests, asked a provider at
  least once — the behaviour the machine can observe. Assumed 15 % of families.
- **Value delivered to providers per avid family per year** = trials per year × trial →
  enrolment rate × provider revenue per enrolment. Defaults 2 × 40 % × **$1,016** (US
  families' average spend per child per sport, 2024 — [Project Play](https://projectplay.org/news/2025/2/24/project-play-survey-family-spending-on-youth-sports-rises-46-over-five-years)) ≈ **$813/year**.
- **Marketing value of an avid family to the platform** = the platform's capture of that
  value — **capture is measured** as upgrades bought within 30 days of a delivered result
  (a campaign sent, an enquiry answered) ÷ all upgrades (audit A11, Q8); 5 % assumed until
  measured + the
  referral value (0.3 new families per avid family per year × the share who become avid ×
  their capture). Defaults ≈ **$42/year**.
- **Expected value of a new family** = P(avid) × avid value ≈ $6 at the defaults — the
  number a content post has to beat.

#### 3.2 Content ROI

`cost per family from content = content stack $/month ÷ (posts per week × 4.33 × new
families per post)`. Defaults $120 ÷ (5 × 4.33 × 1.5) ≈ **$4 per family**, against $6
expected value: positive, thin, and entirely dependent on *families per post*, which is
the one number a connected channel measures (research II §3).

### 4. Where the next dollar goes (the allocation rule)

Every week the system ranks three actions by **expected LTV gained per dollar**:

| Action | Cost | Expected gain |
|---|---|---|
| Retention touches to the at-risk advertisers | at risk × (cost per touch + operator minutes) | at risk × share kept (`churnSaved`, 30 % assumed, measured from the retention log) × LTV |
| One more e-mail touch to the unreplied | unreplied × cost per touch | unreplied × reply rate × 42 % (share of replies after step one) × apply × managing × upgrade × LTV |
| Call the phone-only providers | phone-only × cost per call | phone-only × ½ reached × reply rate × 3 × apply × managing × upgrade × LTV |
| A week of the content engine | content stack ÷ 4.33 | posts per week × families per post × expected value of a new family |

The recap's "needs you" shows the winner; the operator still approves. At the defaults the
e-mail touch wins (cheap), the content week second, the call list third — and every one of
these flips when a real rate replaces an assumption.

### 5. The metrics tree the system maintains

```
Platform revenue (MRR)
├─ upgraded providers × ARPA                       ← entitlements
│   ├─ managing providers × upgrade rate           ← pipeline events
│   │   └─ contacted × reply × apply × managing    ← sequence + inbox events
│   └─ churn                                        ← entitlement ended
└─ families delivered to providers (the product)
    ├─ avid families × trials × enrolment           ← saves, asks, campaign clicks, bookings
    ├─ new families from content                    ← post → listing → sign-up (UTM/referrer)
    └─ referrals                                    ← platform's invite events
Cost
├─ outbound (touches, calls, operator minutes)     ← messages, tasks, approvals
├─ content stack (media adapters)                  ← adapter usage
└─ tooling
```

Every leaf is an event the machine already writes (`messages`, `approvals`,
`provider_state`, `entitlements`, `campaigns`, `enquiries`) or one the platform must expose
(saves, sign-ups with source, bookings — prerequisites P-6 and P-9). Metrics are materialised nightly per
`platform_id` (architecture ADR-11).

### 6. Events and attribution (what to log)

| Event | Fields | Feeds |
|---|---|---|
| `touch.sent` / `touch.replied` | provider_id, step, channel, cost | reply rate, CAC |
| `stage.changed` | provider_id, from, to, by | funnel rates |
| `approval` | draft kind, minutes (from open to decision) | operator cost |
| `entitlement.started` / `.ended` | provider_id, product, price | ARPA, churn, LTV |
| `post.published` / `post.clicked` / `signup` | post_id, channel, utm, family_id | families per post, content CPA |
| `family.saved` / `family.asked` / `digest.opened` | family_id, provider_id | avid definition |
| `campaign.sent` / `.clicked` / `booking` | campaign_id, family_id, provider_id | trials, enrolment value |
| `adapter.used` | adapter, units, cost | content stack cost |

Attribution: last touch within 7 days for a sign-up (post → listing → account); a booking is
attributed to the campaign or enquiry that preceded it within 30 days; an upgrade is
attributed to the pipeline (always) and to the campaign result shown at the moment of
purchase (P8) — both recorded, neither double-counted in revenue.

### 7. Decision rules (proposed R16–R19)

| # | Rule | Effect |
|---|---|---|
| R16 | The next-dollar ranking runs weekly on measured rates where they exist and on the documented assumption where they do not; the recap shows which is which | no allocation on a hidden assumption |
| R17 | A sequence step is added or removed when its measured marginal reply rate per touch falls below the cost-per-touch breakeven for two consecutive weeks | the cadence follows the data, inside the 4–7 benchmark |
| R18 | Content slots go to the neighbourhood × activity pairs with the highest families-per-post over the trailing 4 weeks; new pairs get one slot a week to be measured | the engine learns where families come from |
| R19 | The upgrade card appears only when a provider's delivered value (trials × enrolment value) exceeds the product's annual price — the sale is made by the number | P8; no upgrade pitch below breakeven |

### 8. What is real, what is assumed (2026-09-19)

Real on a connected instance: the listing counts by contact channel (the screen computes them from the site's data) and the stage counts. Benchmarks: reply rates
(Instantly), activation range and churn range (research II), $1,016 per child per sport
(Project Play). Assumptions: every conversion rate after reply, ARPA, margin, cost per
touch and call, operator minutes, tooling, family count, avid share, trials, enrolment,
capture, referral, families per post, content cost. Each is one input on the screen and
one line here; the platform's analytics (prerequisite P-6) and a pilot provider (prerequisite P-6) replace them
in that order.

