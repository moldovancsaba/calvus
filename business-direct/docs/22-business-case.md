# business.direct — business case

*For the owner (the product's economics) and for a prospective customer (what an operator pays
and gets). What this page answers: what the product costs to build and run, what it can be sold
for, how many customers pay it back, what a customer gains against the price, and what the first
customer's instance already shows. Every input is marked **measured**, **benchmark** (sourced) or
**hypothesis** (ours, the owner's decision). Formulas are the ones the product's Economics screen
computes (`16-analytics-and-unit-economics.md`); run costs are the vendors' own prices read on
2026-09-20 (`01g-research-real-system.md` §15). Written 2026-09-20, rewritten the same day for the
product, not the first customer (D39).*

## 1. The product in one line

Sales and marketing automation for the one-person operator: seven departments as automations,
the operator's knowledge as plain files, a human gate on everything, one loop that ranks the next
dollar. Sold as a subscription per operator instance. First paying customer: ClassScout
(Your Field NYC).

## 2. The market the customer is in (benchmarks)

| Fact | Figure | Source |
|---|---|---|
| Enquiries a small business loses | 62 % of calls unanswered; 78 % of customers buy from the first responder; 21× qualification within five minutes vs thirty | research I §2 |
| Follow-up | reminders cut no-shows 29 %; a three-touch sequence in order lifts reply rates from ~3 % to ~10 % | research I §3, II §5 |
| What the operator pays today for pieces of the job | scheduler $29–200/mo; clip cutter $15–29; avatar video $29; design $15; Yelp Receptionist (answering only) $99; stacked ≈ $200–400/mo, and the person still runs the department | research II §4, III |
| The incumbents' bet on the same job | Yelp bought Hatch (AI lead management) for $270 M, January 2026 | research III |

## 3. What it costs to build and run (the product's cost side)

| Line | Amount | Basis |
|---|---|---|
| Build | **34 developer-weeks** (two developers, nine two-week sprints) + the owner as product lead | `13-implementation-plan.md` §2b |
| Build cost | 34 × the blended rate per developer-week — **the owner's commercial input**; illustration at $2 500 / $4 000 / $6 000 → **$85 k / $136 k / $204 k** | hypothesis (illustration, not a quote) |
| Run cost per instance, pilot volume (≤ 300 prospects, ≤ 5 000 audience) | **≈ $50–75 / month** | vendor prices, `01g` §15 |
| Run cost per instance, sizing target (1 000 prospects, 50 000 audience) | **≈ $280–400 / month** | vendor prices, `01g` §15 |
| Shared platform cost (Vercel team, monitoring, one worker) | ≈ $30–60 / month regardless of customer count | `01g` §15 |
| Support and onboarding per customer | the policy record, the connector, the knowledge files: ≈ 2 days at onboarding, ≈ 2 hours a month after | hypothesis |

## 4. What it sells for (the pricing hypothesis — the owner decides)

| Tier | Includes | Price / month | Run cost / month | Contribution |
|---|---|---|---|---|
| **Machine** | all departments with template drafting, the pipeline, conversations, the human gate, the recap, one instance | **$249** | ≈ $60 | ≈ $190 (76 %) |
| **Machine + AI** | + AI drafting per department, the clip engine, generated media with credentials | **$449** | ≈ $90 (AI and transcription) | ≈ $360 (80 %) |
| **Second instance** | another brand or platform on the same account | + $149 | ≈ $60 | ≈ $90 |

Anchors: the tools replaced ($200–400 stacked), Yelp Receptionist ($99 for one job), the
category's SMB SaaS norms. Churn hypothesis 5 % / month (SMB SaaS 3–7 %), annual plans at 3 %.

## 5. The product's economics by customer count (hypothesis prices, pilot run cost)

| Customers (Machine + AI mix 50/50) | MRR | Contribution / month | Months to recover a $136 k build | Months to recover $85 k |
|---|---|---|---|---|
| 1 (the first customer) | $349 | ≈ $275 − $45 shared ≈ $230 | — (a reference customer, not a business) | — |
| 5 | $1 745 | ≈ $1 330 | ≈ 100 | ≈ 64 |
| 20 | $6 980 | ≈ $5 450 | ≈ 25 | ≈ 16 |
| 50 | $17 450 | ≈ $13 700 | ≈ 10 | ≈ 6 |
| 100 | $34 900 | ≈ $27 500 | ≈ 5 | ≈ 3 |

Reading: the product is a business at **twenty to fifty customers**; the first customer is the
reference case that proves the machine on real data and pays the run cost. The unit is
attractive — a 76–80 % contribution margin on a subscription that replaces a $200–400 stack and
a person's week — and the customer acquisition cost for the product itself is the open number:
the product's own machine will run its own sales flow (research II §5's sequences, the same
pipeline), and the first measured CAC is one cohort away.

## 6. The customer's case (what an operator pays and gets)

| Line | Value | Basis |
|---|---|---|
| Pays | $249 or $449 / month | §4 |
| Replaces | $200–400 / month of single-job tools | research II §4 |
| Time | seven departments' output for ≈ 20 minutes of approvals a day (≈ 7 h / month) against the ≈ 10–20 h / week a one-person operator spends on sales and marketing — or does not spend | hypothesis; the product measures the operator's hours from its own events (audit A10) |
| Response time | every enquiry drafted within a minute, answered within the hour; the single largest revenue lever in a small business | research I §2 |
| Pipeline | every prospect scored and touched three times in order; reply rate benchmark 5.5 % top-quartile, 10.7 % top-decile | research II §5 |
| Content | the week's posts, digest and clips from material that already exists; cost per new audience member measured per post | research II §3 |
| Control and exposure | nothing sent without approval; one policy record and a gate; an audit trail on every send | `18-responsible-data-policy-framework.md` |

Break-even for the customer: one enquiry a month answered that would otherwise have been lost,
in any category where a customer is worth more than the subscription.

## 7. The first customer's instance (measured; the worked example)

ClassScout runs Your Field NYC, a children's-activity marketplace: prospects are the listed
providers, the audience is families. The prototype runs on 253 of their providers pulled from
their public API (their catalogue is far larger; the pull is the demo's data, not their
situation). What the product's own model already told them, at their sample prices ($49 ARPA,
5 % churn) and the benchmark reply rate: outbound e-mail alone to that pull returns **0.7** of its
cost (CAC ≈ $1 200 against LTV $784; payback 31 months), and it turns positive as their catalogue
grows (≈ 2 at 1 000 prospects), as their products are priced for a category where families spend
$1 016 per child (≈ 6), or as the machine is treated as their growth engine (a new family for
≈ $4 against ≈ $6 of expected value; ≈ $610 k a year of provider revenue through their
introductions at 5 000 families). Every input is on their Economics screen; the first measured
numbers replace the assumptions at the end of sprint 2. That the product tells its customer this
is the product.

## 8. Sensitivity (the product)

| Input | Pessimistic | Hypothesis | Optimistic | Effect |
|---|---|---|---|---|
| Price (Machine) | $149 | $249 | $349 | contribution per customer $90 → $190 → $290 |
| Churn / month | 7 % | 5 % | 3 % | customer lifetime 14 → 20 → 33 months; LTV at $249: $2 700 → $3 800 → $6 300 |
| Run cost per instance | $120 | $60 | $40 | margin 52 % → 76 % → 84 % |
| Customers at month 12 | 5 | 20 | 50 | build recovered in ≈ 100 / 25 / 10 months (at $136 k) |
| Product CAC | $2 000 | $1 000 | $500 | LTV : CAC at hypothesis 1.9 → 3.8 → 7.6 |

## 9. What we need, and when

From the owner: the price (from the hypothesis), the developer rate, the go. From the first
customer, after the decision: a postal address for the legal footer, one privacy-policy
paragraph (drafted by us), the policy record confirmed, counsel's wording; later their analytics
events, a write key and a pilot prospect (`19-implementation-prerequisites.md`).

## 10. The decision

Build the product and run it for the first customer. The product's own first cohort — reply
rate, enquiries answered, audience per post, the operator's hours — is measured by the machine
itself from sprint 2 and replaces every hypothesis on this page.
