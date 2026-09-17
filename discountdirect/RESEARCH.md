# DiscountDirect — research: how B2C machines upsell and cross-sell, and how to fine-tune the idea

Read and compiled 2026-09-17. Every claim below carries a numbered source from §11;
figures that circulate without a primary source are marked *industry-reported*. The
purpose is practical: what the best B2C operators actually do, what the evidence says
works and what backfires, and what that means for DiscountDirect — the prototype at
`index.html` and its rules in `business-logic.html`.

## 1. Why personalised offers pay — the evidence base

- McKinsey's *Next in Personalization* research: personalisation most often lifts revenue
  10–15 % (range 5–25 % by sector and execution), improves marketing efficiency 10–30 %,
  and companies that excel at it generate **40 % more revenue** from those activities than
  average players; 71 % of consumers expect personalised interactions and 76 % are
  frustrated when they don't get them. [1][2]
- Netflix (Gomez-Uribe & Hunt, ACM TMIS 2015): about **80 % of hours streamed** come from
  recommendations, and the system's value is estimated at **over $1 billion a year** in
  retained subscribers. [3]
- Amazon's "35 % of revenue from recommendations" is a widely repeated McKinsey estimate
  with no primary Amazon disclosure — *industry-reported*, useful as an order of magnitude
  only. [4]
- Barilliance's 2023 study: product recommendations account for up to **31 % of e-commerce
  revenue** in sessions where shoppers engage with them. [5]
- Automated, behaviour-triggered messages are where the money is: essential automated
  flows generate 30–50 % of a store's e-mail revenue on 2 % of the volume; post-purchase
  flows return **$2–5 per recipient**, abandoned-cart $3–8, VIP $5–15+. [6][7]

What the numbers share: the lift comes from **relevance and timing**, not from the size of
the discount.

## 2. How the best B2C operators upsell and cross-sell — the mechanics

### 2.1 The surfaces
Product page ("bought together"), cart, the **confirmation page** (one-click add before
the thank-you), post-purchase e-mail and SMS, the account/app home, and — increasingly —
the messaging thread (RCS, WhatsApp, in-app chat). [7][8]

### 2.2 The timing ladder (the single most transferable pattern)
Compiled benchmarks, sources in [7]:

| Moment | Offer type | Observed take rate |
|---|---|---|
| Confirmation page, t + 0 | complementary item, one click, under ~30–50 % of cart value | 10–16 % (14.6 % across 1 847 businesses) |
| 24–48 h, e-mail | upgrade / accessory | post-purchase sequences 11.3 % vs 1–3 % for generic promos |
| 7–14 days | category expansion | — |
| 5–7 days before predicted run-out | **replenishment**; for consumables the subscription upsell ("never run out, save 10–15 %") | 8–15 % |
| 60–90 days, durables | accessory / next-generation | — |

Two hard lessons: requiring payment re-entry cuts post-purchase conversion by ~78 %, and
some wallets (Apple Pay, Google Pay, Klarna) never show the post-purchase page — the
message channel is the fallback. [7]

### 2.3 Loyalty and context as the recommendation substrate
Sephora's Beauty Insider consolidates cross-channel history into one profile that drives
recommendations, early access and limited promotions [9]; Starbucks' Deep Brew chooses
offers from app and loyalty data plus context (weather, time, local events) — the
mechanics are documented, the revenue figures that circulate for it are not. [10]

### 2.4 Conversational and rich messaging
Sinch's retail cases: RCS delivers 3–7× the click-through of rich SMS; Clarins 2.5× CTR
and 79 % read rate; Cdiscount **+9 % average basket**; 54 % of US consumers prefer
abandoned-cart notices via RCS. Infobip: 71 % of consumers want personalised offers and
proactive assistance, only 34 % of brands provide them. [11][12] The thread is becoming
the storefront — which is DiscountDirect's premise.

## 3. Next best action and recommendations — what a decision engine actually needs

### 3.1 Propensity is not enough; uplift is the target
The classic segmentation (Radcliffe & Surry, 1999): **persuadables** (buy only if
treated), **sure things** (buy anyway), **lost causes** (never buy), **sleeping dogs**
(buy less if treated). A propensity model finds likely buyers — which includes sure
things, whose discount is pure margin loss. An uplift model estimates the *difference*
treatment makes and targets persuadables only. When propensity-driven programmes are
re-measured with uplift methods, 20–40 % typically show negligible incremental lift;
banking and telco projects report 29–59 % revenue increases from switching. [13][14][15]

### 3.2 An NBA pipeline in practice (Grid Dynamics)
Inputs: profile, interaction history, past treatments, outcomes. Stages: bias correction
(propensity-score matching), uplift estimation (S/T/X-learners or uplift trees),
**treatment selection by predicted uplift** from a small menu of 5–10 actions, and
offline evaluation with incremental-gains and decile-uplift curves before anything goes
live. [14]

### 3.3 Discount depth as a learned decision
ASOS's DISCO framework allocates personalised discount codes with a **contextual bandit
(Thompson sampling) inside an integer programme** that enforces the cost budget — the
depth of each customer's discount is learned, under a margin constraint, rather than
fixed. [16]

### 3.4 Explanations are not decoration
Zhang & Chen's survey: explainable recommendation improves transparency, persuasiveness,
effectiveness, trustworthiness and satisfaction; process-based explanations foster
trust through perceived control and fairness. [17][18] DiscountDirect's "reason" on every
offer is the right instinct — it should be generated by the same model that scores the
offer, not written by hand.

## 4. Discount economics — what backfires

- *Industry-reported* but consistent across sources: most promotional volume is not
  incremental (figures of 94 % non-incremental category revenue and 35 % subsidising
  loyal buyers who would have paid full price circulate), and 50–60 % of promotions fail
  to return; cannibalisation runs 20–60 % for broad coupons versus 10–25 % for targeted
  ones. [19][20]
- Promotion fatigue is real: brands running flash sales more than twice a month see
  conversion drop 15–25 %. [21]
- The only honest metric is **incremental contribution margin against a randomised
  holdout** that never saw the offer. [19]

## 5. Urgency and scarcity — the evidence and the legal line

Countdown timers lift conversion by ~8.6 % on average (studies range 8–32 %); timers
under six hours and quantity limits tied to real stock work best; transparent urgency
outperforms fake urgency, which destroys trust. [21] The law now draws the line: the EU
Digital Services Act prohibits dark patterns including **fake countdowns and untrue
scarcity claims**; the Omnibus Directive requires struck-through prices to be the lowest
of the previous 30 days; the Digital Fairness Act is expected in Q4 2026. [22][23]
Consequence for DiscountDirect: a flash campaign's time and quantity limits must be
**enforced and true**, and the "was" price must be the 30-day low.

## 6. Channels, consent and frequency

- GDPR Recital 47: direct marketing *may* be a legitimate interest, subject to the data
  subject's reasonable expectations at collection; Article 21 gives an absolute right to
  object. ePrivacy adds the **soft opt-in**: existing customers may be e-mailed about
  similar products on an opt-out basis, but profiling technologies need consent, and a
  documented legitimate-interest assessment is expected. [24][25]
- Frequency: 56 % of US consumers unsubscribe after four or more messages from one
  company in 30 days; practitioner caps are 2–4 e-mails a month and at most one SMS a
  week, segmented by engagement. [26]

## 7. The Hungarian market context

PwC Hungary's *Online Retail Big Picture* (June 2026): online retail turnover reached
**HUF 2 092 billion** in 2025 (about EUR 5.7 bn), 4.4 million people shop online, roughly
**a quarter of shoppers generate nearly 80 % of parcels**, cross-border marketplaces take
about 18 % of turnover, and 60 % of orders are placed on mobile. [27] The concentration is
the point: a Hungarian web shop's revenue sits with a small, repeat-buying core — exactly
the buyers DiscountDirect addresses one by one.

## 8. What this means for DiscountDirect — fine-tuning the idea

The prototype's rules are in `business-logic.html`. Against the evidence above, twelve
changes, each traceable to a source:

1. **Score relevance, don't hard-code it.** Replace the fixed relevance sets with a
   buyer × product score plus a machine-written reason code (§3.2, §3.4). The reason
   stays first-class in the UI.
2. **Target uplift, not propensity.** Send to persuadables; never discount a sure thing.
   Keep a permanent randomised holdout (5–10 %) per campaign and automation and report
   incremental margin, not acceptance (§3.1, §4).
3. **Detect replenishment cycles from history.** Anna buys HEPA filters every ~8 months
   in the sample data; the engine should predict run-out and fire 5–7 days before it —
   the highest-converting moment in the ladder (§2.2).
4. **Add the timing ladder to automations.** Frequency today is weekly/fortnightly/
   monthly; the evidence favours event-driven triggers — order confirmed (t + 0),
   24–48 h, 7–14 days, predicted run-out, 60–90 days for durables (§2.2).
5. **Make the discount a decision.** Replace the fixed 10/15/20/25 steps with a learned
   depth under a margin floor and a budget (DISCO pattern), with seller-set guardrails
   (§3.3, §4).
6. **Frequency caps per buyer per channel**, and offer-fatigue signals (declines,
   unsubscribes, non-opens) feeding back into targeting (§6).
7. **True scarcity only.** Enforce `limitH` and `limitQty`, show real remaining stock,
   expire visibly, and keep the 30-day-low price rule on every "was" price (§5).
8. **Consent by channel and preference controls** in the buyer view: frequency, channels,
   "why this" and "don't show me this category" — the buyer's context pane already
   frames the consent story (§6, §3.4).
9. **Post-purchase moment in the thread.** The order-confirmed event is the best cross-
   sell moment; the timeline already records events — make that event carry a one-click
   complementary offer (§2.2).
10. **Subscription upsell for consumables** as an offer type ("never run out, −10–15 %"),
    with the buyer's actual interval as the default (§2.2).
11. **Rich channels.** In-app chat first; RCS/WhatsApp as the next channel (3–7× the
    click-through of SMS); printed DM stays for high-value durables where a coupon in the
    hand still converts (§2.4).
12. **Measurement built in from day one**: every offer stamped with model version,
    reason code, holdout flag, channel, timing trigger and outcome; a dashboard that reads
    incremental margin, take rate, unsubscribe rate and frequency per buyer (§4, §6).

Product ideas the evidence supports beyond the current scope: a buyer-initiated "ask for
a deal" in the thread; bundles from co-purchase patterns; a win-back trigger at the
segment's typical churn point; a buyer "offer wallet" across sellers.

## 9. What not to build

Mass newsletters to everyone (non-incremental, fatigue), fake urgency (illegal in the EU),
discounts to sure things (margin loss), profiling without a consent path (ePrivacy),
and acceptance rate as the success metric (measures generosity, not value).

## 10. Open research questions

Optimal discount-depth model for a small catalogue with thin history; the right holdout
size for a single web shop's volume; whether a buyer-side "reason" changes acceptance
(A/B); RCS availability and cost on Hungarian carriers.

## 11. Sources consulted

1. McKinsey & Company — *The value of getting personalization right—or wrong—is multiplying* (Next in Personalization 2021). https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/the-value-of-getting-personalization-right-or-wrong-is-multiplying
2. McKinsey — *What is personalization?* (explainer, 2023). https://www.mckinsey.com/~/media/mckinsey/featured%20insights/mckinsey%20explainers/what%20is%20personalization/what-is-personalization.pdf
3. Gomez-Uribe, C. A. & Hunt, N. — *The Netflix Recommender System: Algorithms, Business Value, and Innovation*, ACM TMIS 6(4), 2015. https://dl.acm.org/doi/10.1145/2843948
4. Firney — *Amazon's 35% revenue from recommendations* (secondary). https://www.firney.com/news-and-insights/ai-product-recommendations-from-amazons-35-revenue-model-to-your-e-commerce-platform
5. Barilliance — *Recommendations drive a third of e-commerce revenue*. https://www.barilliance.com/recommendations-drive-third-e-commerce-revenue/
6. 1Digital Agency — *The 7 essential Klaviyo flows (with revenue benchmarks)*, 2026. https://www.1digitalagency.com/blog/the-7-essential-klaviyo-flows-every-shopify-store-needs-with-revenue-benchmarks-70284/
7. Digital Applied — *Post-purchase upsell: the 2026 eCommerce AOV playbook* (compiles Yotpo, Focus Digital, Opensend, GemPages, Klaviyo data). https://www.digitalapplied.com/blog/post-purchase-upsell-thank-you-page-2026-ecommerce-playbook
8. Omnisend — *Post-purchase email guide*. https://www.omnisend.com/blog/post-purchase-emails/
9. CommerceNext — *Omnichannel retailing examples* (Sephora). https://community.commercenext.com/5-omnichannel-retailing-examples-that-drive-results/
10. Marketer in the Loop — *Starbucks' AI-powered hyper-personalization with Deep Brew* (mechanics; results unsourced). https://marketerintheloop.com/p/starbucks-ai-powered-hyper-personalization-with-deep-brew
11. Sinch — *RCS use cases and examples* (Clarins, Courir, Cdiscount cases). http://sinch.com/blog/rcs-use-cases-and-examples/
12. Infobip — *Conversational commerce in retail*. https://www.infobip.com/blog/conversational-commerce-in-retail
13. Radcliffe, N. J. & Surry, P. D. — *Differential response analysis: modeling true response by isolating the effect of a single action*, Credit Scoring and Credit Control VI, 1999 (via Wikipedia, *Uplift modelling*). https://en.wikipedia.org/wiki/Uplift_modelling
14. Grid Dynamics — *Next best action model: building and evaluation*. https://www.griddynamics.com/blog/next-best-action-churn-prevention
15. California Management Review — *To treat or not to treat? Five lessons from uplift modeling*, 2025. https://cmr.berkeley.edu/2025/11/to-treat-or-not-to-treat-five-lessons-learned-from-using-uplift-modeling-to-optimize-marketing-campaigns/
16. *DISCO: An end-to-end bandit framework for personalised discount allocation* (ASOS), arXiv 2406.06433. https://arxiv.org/pdf/2406.06433
17. Zhang, Y. & Chen, X. — *Explainable recommendation: a survey and new perspectives*, 2018/2020. https://arxiv.org/abs/1804.11192
18. *Why process-based explanations foster algorithmic trust*, JTAER 2026. https://doi.org/10.3390/jtaer21070208
19. Insight Lime Analytics — *How to (really) measure your coupons and discounts*. https://www.insightlimeanalytics.com/blog/how-to-measure-discounts
20. Accuris — *The heavy toll of over-promoting*. https://www.accuris.com/post/the-heavy-toll-of-over-promoting
21. Heartly — *The psychology behind flash sales* (timer and frequency figures). https://www.heartly.io/blog/flash-sale-psychology-urgency-fomo
22. European Parliament Think Tank — *Regulating dark patterns in the EU: towards digital fairness*, 2025. https://epthinktank.eu/2025/01/14/regulating-dark-patterns-in-the-eu-towards-digital-fairness/
23. DynamicPricing.AI — *EU pricing regulatory rules* (Omnibus 30-day rule). https://dynamicpricing.ai/eu-pricing-regulatory-compliance-ecommerce/
24. GDPR Recital 47. https://gdpr-info.eu/recitals/no-47/
25. GDPR Register — *Direct marketing GDPR rules and exceptions* (soft opt-in). https://www.gdprregister.eu/articles/direct-marketing-rules-and-exceptions/
26. Braze — *Frequency capping: what it is, how it works*; FlareLane — *How many messages a month is too many*. https://www.braze.com/resources/articles/whats-frequency-capping · https://flarelane.com/en/blog/message-frequency-capping/
27. PwC Hungary — *Online Retail Big Picture* (June 2026), via Daily News Hungary. https://dailynewshungary.com/hungarian-spending-online-foreign-retailers/
