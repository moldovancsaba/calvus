# business.direct — analytics and unit economics

*Written 2026-09-19 on the owner's directive: "we will need ROI calculations and planning for
CAC and LTV for B2B clients, marketing value for the avid users, and all the other analytics
information that helps the system deliver data-driven marketing decisions." This is the
model the *Economics* screen (`../index.html?view=platform&screen=economics`) computes; the
screen's inputs are this document's assumptions, and every number that is not from the
catalogue or a cited benchmark is marked so. Terms are the SSOT's; the decision rules become
R16–R19 there.*

## 1. What the numbers are for

The machine spends three things — e-mail touches, operator minutes and tool subscriptions —
and gets back providers who manage their page, providers who pay, and families who come,
save, ask and enrol. Data-driven marketing here means four questions the system can answer
from its own events, every week:

1. **What does a paying provider cost and what is it worth?** (CAC, LTV, payback, LTV:CAC)
2. **What is a family worth, and an *avid* one?** (marketing value on the demand side)
3. **Does content pay?** (cost per family from the content engine vs the value of a family)
4. **Where does the next dollar go?** (expected LTV gained per dollar, across the three
   levers: another touch, a call, a week of content)

## 2. The B2B model: providers (the platform's B2B clients)

### 2.1 Funnel and rates

| Stage | Count today (real) | Rate to next | Source of the rate |
|---|---|---|---|
| Identified | 252 | — | catalogue |
| Reachable by e-mail | 130 | reply **5.5 %** (top-quartile benchmark; 3.43 % average, 10.7 % top decile) | [Instantly 2026 benchmark](https://instantly.ai/cold-email-benchmark-report-2026) (research II §5.1) |
| Phone only | 72 | a call converts ~3× an e-mail; half are reached | assumption; multi-channel +40 % (research II §5.1) |
| Website only | 50 | not in the model until a form step exists | — |
| Replied → applied | — | **40 %** | assumption |
| Applied → managing | — | **80 %** (the platform confirms the claim) | assumption |
| Managing → upgraded within 3 months | — | **25 %** | assumption; SMB activation 35–50 % (research II §2.2) |

### 2.2 Cost of acquisition

`cost = e-mailed × touches × cost per touch + phone-only × cost per call + approvals ×
operator minutes ÷ 60 × operator rate + tooling × 3 months`

Defaults: 3 touches at $0.05, $5 per call task, 2 operator minutes per approval at $40/h,
$150/month tooling (sending domain, warm-up, enrichment). **Operator hours** are the
dominant cost (audit A10): the screen counts every approval and shows the hours; batch
approval and earned auto-approval (R25) are the levers that bring them down. **CAC (managing)** = cost ÷ new
managing providers; **CAC (upgraded)** = cost ÷ new paying providers.

### 2.3 Lifetime value

`contribution = ARPA × gross margin` · `LTV = contribution ÷ monthly churn` ·
`payback = CAC ÷ contribution` · **healthy when LTV : CAC ≥ 3 and payback ≤ 12 months**.

Defaults: ARPA $49/month (the platform's three products at sample prices: $49, $29,
$149/season), margin 80 %, churn 5 %/month (SMB SaaS range 3–7 %, research II §2.2).
A **conversations line** input (default 0 = bundled per D21; Yelp Receptionist sells the
same thing at $99) adds revenue per *managing* provider to the plan's MRR (Q12) — the
owner's pricing decision is one number on the screen.

### 2.4 What the defaults say (the first data-driven finding)

With the defaults, one quarter of outbound to the current catalogue yields about 2 managing
and 0.6 upgraded providers for ~$720 — **CAC (upgraded) ≈ $1,200 against an LTV of $784:
LTV : CAC 0.7, payback 31 months.** Raising the reply rate to the top decile (10.7 %) only
reaches 1.3 : 1. The model is telling the truth about the business: *outbound e-mail to a
252-provider catalogue cannot pay for itself on $49 upgrades.* It pays in one of three
ways, and the plan should say which:

- **the base machine is the platform's growth engine, not a profit centre** (D21: bundled;
  its return is families and managed pages, valued below), or
- **a larger catalogue** (the cost is mostly fixed tooling; at 1,000 providers CAC falls
  under $400 with the same rates), or
- **higher ARPA** (camp placement at $149/season, bundles) and lower churn (annual plans).

The screen makes each of these one input away.

## 3. The B2C model: families and the value of an avid user

### 3.1 Definitions

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

### 3.2 Content ROI

`cost per family from content = content stack $/month ÷ (posts per week × 4.33 × new
families per post)`. Defaults $120 ÷ (5 × 4.33 × 1.5) ≈ **$4 per family**, against $6
expected value: positive, thin, and entirely dependent on *families per post*, which is
the one number a connected channel measures (research II §3).

## 4. Where the next dollar goes (the allocation rule)

Every week the system ranks three actions by **expected LTV gained per dollar**:

| Action | Cost | Expected gain |
|---|---|---|
| One more e-mail touch to the unreplied | unreplied × cost per touch | unreplied × reply rate × 42 % (share of replies after step one) × apply × managing × upgrade × LTV |
| Call the phone-only providers | phone-only × cost per call | phone-only × ½ reached × reply rate × 3 × apply × managing × upgrade × LTV |
| A week of the content engine | content stack ÷ 4.33 | posts per week × families per post × expected value of a new family |

The recap's "needs you" shows the winner; the operator still approves. At the defaults the
e-mail touch wins (cheap), the content week second, the call list third — and every one of
these flips when a real rate replaces an assumption.

## 5. The metrics tree the system maintains

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

## 6. Events and attribution (what to log)

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

## 7. Decision rules (proposed R16–R19)

| # | Rule | Effect |
|---|---|---|
| R16 | The next-dollar ranking runs weekly on measured rates where they exist and on the documented assumption where they do not; the recap shows which is which | no allocation on a hidden assumption |
| R17 | A sequence step is added or removed when its measured marginal reply rate per touch falls below the cost-per-touch breakeven for two consecutive weeks | the cadence follows the data, inside the 4–7 benchmark |
| R18 | Content slots go to the neighbourhood × activity pairs with the highest families-per-post over the trailing 4 weeks; new pairs get one slot a week to be measured | the engine learns where families come from |
| R19 | The upgrade card appears only when a provider's delivered value (trials × enrolment value) exceeds the product's annual price — the sale is made by the number | P8; no upgrade pitch below breakeven |

## 8. What is real, what is assumed (2026-09-19)

Real: 252 · 130 · 72 · 50 (catalogue — e-mail · phone only · neither; corrected by the audit, the screen always computed them right); this session's stage counts. Benchmarks: reply rates
(Instantly), activation range and churn range (research II), $1,016 per child per sport
(Project Play). Assumptions: every conversion rate after reply, ARPA, margin, cost per
touch and call, operator minutes, tooling, family count, avid share, trials, enrolment,
capture, referral, families per post, content cost. Each is one input on the screen and
one line here; the platform's analytics (prerequisite P-6) and a pilot provider (prerequisite P-6) replace them
in that order.
