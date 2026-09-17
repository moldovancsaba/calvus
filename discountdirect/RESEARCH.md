# DiscountDirect — research: how B2C machines make people buy again, and how to fine-tune the idea

Read and compiled 2026-09-17. Every claim below carries a numbered source from §11;
figures that circulate without a primary source are marked *industry-reported*. The
purpose is practical: what the best B2C operators actually do, what the evidence says
works and what backfires, and what that means for DiscountDirect — the prototype at
`index.html` and its rules in `business-logic.html`.

One framing runs through the whole document: **the discount is only one lever, and
usually the most expensive one.** Part A (§1–§6) covers offers, targeting and price.
Part B (§7) covers what the strongest B2C machines actually run on — laziness, habit,
loyalty programmes, gamification, pack mentality, surprise, scarcity, choice
architecture and timing — and Part C (§8–§11) turns both into changes to the prototype.

## Part A — offers, targeting and price

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

## Part B — beyond price: every lever that makes people buy again

Most of what the best operators do is not discounting. This part goes lever by lever;
each has its own section with the evidence and what it means for DiscountDirect.

| # | Lever | In one line |
|---|---|---|
| 7.1 | Laziness and convenience | the easiest action wins |
| 7.2 | Habit and rhythm | become the customer's default |
| 7.3 | Loyalty programmes | points, tiers, paid membership, coalition cards, birthdays, expiry |
| 7.4 | Gamification | streaks, challenges, games, collections, progress |
| 7.5 | Pack mentality | herd cues, best-seller badges, group buying, referrals, community, live selling |
| 7.6 | Surprise and mystery | surprise gifts, blind boxes, variable rewards, lotteries |
| 7.7 | Scarcity, exclusivity and FOMO | drops, limited editions, waiting lists, back-in-stock |
| 7.8 | Choice architecture | fewer options, one default |
| 7.9 | Timing and attention | the right moment, the right cadence |
| §4 | Price | the last lever, and the only one that costs margin |

### 7.1 Laziness — remove effort, and the easiest action wins
- Fogg's behaviour model: a behaviour happens when motivation, **ability** and a
  prompt meet; when motivation is ordinary, lowering the effort is the cheapest way to
  trigger the action. [36]
- Baymard: 70 % of carts are abandoned; 26 % of US shoppers have abandoned because an
  account was required, 17 % because checkout was too long; the average large site can
  raise conversion 35 % through checkout design alone. [35]
- Defaults are the strongest form of "easy": switching a savings plan from opt-in to
  opt-out took participation from 50 % to 86 % with no change in the economics
  (Madrian & Shea). [37]
- Amazon built the lazy path into the product: Subscribe & Save is active for 23 % of
  US customers and gives sellers 20–35 % of their sales; the app's home page tested a
  **Buy Again** feed built from order history. [32][34]
- Across 156 000 customers, 77 % of repeat purchases are reorders (23 % cross-sells);
  half happen within 30 days and three quarters within 90. [33]
- Post-purchase offers that force payment re-entry lose ~78 % of conversion (§2.2). [7]

For DiscountDirect: the one-tap "Elfogadom" is the product. A reorder with no discount
and no effort converts better than a discount that needs a checkout.

### 7.2 Habit and rhythm — become the customer's default
- About 43 % of everyday actions are habitual — performed while thinking of something
  else (Wood & Neal). A shop that becomes the habit does not compete on price. [38]
- The Hook model (trigger → action → variable reward → investment): a habit forms when
  an external prompt is repeated at the moment of need, the action is trivial, the
  reward is not fully predictable, and the customer has invested something (history,
  preferences, a streak) that raises the cost of leaving. [39]
- Duolingo's streak mechanics are the reference case; the figures that circulate
  (streak-freeze cut churn ~21 %, 7-day streak users retain 2–4×) come from secondary
  analyses, not Duolingo filings — *industry-reported*. [40]
- Starbucks Rewards: 35.5 million 90-day-active US members, nearly 60 % of US
  company-operated revenue, members 5.6× more likely to visit daily. [30]
- Replenishment cadence is the retail habit: predicted run-out, then a reminder 5–7
  days before it (§2.2). [7]

For DiscountDirect: a fixed rhythm the customer can predict ("your usual, every
fourth week, one tap") beats random blasts; the thread's job is to become the reorder
habit.

### 7.3 Loyalty programmes — points, tiers, paid membership, coalition cards
**What the big ones deliver**
- Prime members spend $1 170 a year against $570 for non-members, chiefly because they
  shop more often; Prime renews at 97–99 %. [28][33]
- Costco renews 92.3 % in the US and Canada and earned about $5.3 billion in fees in
  fiscal 2025 — the fee is the profit, the low prices are the reason to keep paying it.
  [29]
- Tesco Clubcard: 84 % of UK sales are Clubcard-linked; personalised digital coupons
  go to over 9 million customers; the programme is thirty years old. [31]
- Starbucks Rewards: 35.5 million 90-day-active US members, nearly 60 % of US
  company-operated revenue, members 5.6× more likely to visit daily. [30]
- Nike claims members spend about 3× non-members — from Nike's own communications,
  *industry-reported*. [46]

**The programme types, and what the Bond Loyalty Report 2025 says about them** [59]
- *Points and cashback* (Tesco, SuperShop): simple, but the average American belongs to
  17.4 programmes and is active in 8.8 — a points card alone is not differentiation.
- *Tiers* (Starbucks levels, airline status): 44 % of retail and hospitality members
  have reached a higher tier; of those, 78 % say the benefits make them spend more, 75 %
  felt a sense of accomplishment, 71 % felt special. 73 % of consumers adjust spending
  to earn more benefits.
- *Paid membership* (Prime, Costco, Walmart+, eMAG Genius): the customer pays to be
  loyal, and then behaves consistently with having paid. eMAG Genius members — the
  paid programme of the largest marketplace in Hungary and Romania — order up to 5×
  more often than regular customers (eMAG's own figure). [60]
- *Coalition cards* (SuperShop in Hungary: OMV, SPAR, OBI, Jegy.hu and others; 1.7
  million cards used at SPAR in 2024): reach without owning the relationship. [61]

**Mechanics inside a programme that carry their own evidence**
- *Birthday and anniversary messages*: birthday e-mails open at ~43 % and convert at
  roughly ten times the average promotional e-mail (0.72 % vs 0.07 %, vendor
  benchmark); fewer redemption steps, higher conversion. [62]
- *Points expiry and loss aversion*: "your points expire in 14 days" raises redemption
  when paired with a path to redeem; practitioners use a 30-day / 7-day / 24-hour
  reminder ladder and report loss-framed messages beating gain-framed ones by 30–50 %
  (vendor data). One academic study finds the opposite for purchase behaviour — expiry
  and binding thresholds can depress it — so expiry is a redemption tool, not a sales
  tool. [63]
- *Endowed progress* (§7.4) and *tier anniversaries* keep the programme visible between
  purchases.

**Hungary**: 93 % of internet users over 15 belong to a loyalty programme; 42 % want
personalised discounts; two thirds are reluctant to hand over data unless it is needed
for the benefit. Commitment and consistency (Cialdini; Freedman & Fraser): a small
first "yes" — joining, saving a preference — raises the chance of the larger later
"yes". [47][55]

For DiscountDirect: a named membership per seller, with non-price perks (free delivery,
early access, priority answers) and a visible tier, is the container the offers live
in. Points are optional; the tier and the perks are not.

### 7.4 Gamification — streaks, challenges, games, collections, progress
- *Endowed progress* (Nunes & Drèze, JCR 2006): a car-wash card needing 8 stamps but
  issued with 2 already stamped was completed by 34 % of customers versus 19 % for an
  8-stamp card with none — same effort, a visible head start. [41]
- *Personalised challenges*: Tesco Clubcard Challenges set individual spend thresholds
  over six weeks, offered to up to 10 million customers; Global Loyalty Award 2025. [31]
- *Streaks*: Duolingo is the reference case; the figures that circulate (streak-freeze
  cut churn ~21 %, 7-day-streak users retain 2–4×) come from secondary analyses, not
  Duolingo filings — *industry-reported*. [40]
- *Games inside the shop*: Temu opens on a spin-the-wheel and runs Fishland and
  Farmland, where daily visits and invited friends earn free products; Shopee runs
  daily check-in coins, Shopee Farm and coin drops during live streams. Reported
  effects (38 % use the wheel most, half of users make unplanned purchases because of
  the games) are vendor or survey figures, and Temu's mechanics have drawn regulatory
  and consumer-protection criticism for gambling-like design. [64][65]
- *Collect-to-win*: McDonald's revived Monopoly in October 2025 and posted its best US
  same-store quarter in more than two years (+6.8 % in Q4); the 2025 game required the
  app, turning a promotion into an app-install and CRM programme. [66]
- Academic evidence: a Portuguese grocery study (203 loyalty-card users) links ease of
  use to programme satisfaction to loyalty; industry claims of "47 % more engagement"
  are vendor-reported. [42][43]

For DiscountDirect: progress cards with a head start, personalised challenges
("three orders in six weeks unlocks free delivery for a year") and a visible streak
of on-time reorders are honest game mechanics; wheels and farms are not this product.

### 7.5 Pack mentality — herd cues, group buying, referrals, community, live selling
- *Reviews*: Spiegel Research Center — the first five reviews carry the largest
  conversion effect; purchase likelihood peaks between 4.2 and 4.5 stars and falls
  toward 5.0. [44]
- *Bandwagon badges*: "Best seller", "Amazon's Choice", "trending" — Profitero found
  Amazon's Choice worth about +25 % conversion and Best Seller about +45 % views
  (secondary reporting); a 2025 study on the bandwagon heuristic in e-commerce shoppers
  confirms popularity cues shift choice. [67]
- *"Frequently bought together"* is social proof as much as recommendation; real-time
  proof notifications lift conversion 10–15 % across ~20 000 sites (vendor data). [44]
- *Group buying*: Pinduoduo's team purchase — share the item, friends join, everyone
  pays less — took it to 725 million users; ARPU grew 53 % a year against 40 % buyer
  growth. The mechanism is the pack: the buyer recruits the pack to get the price. [68]
- *Referrals*: referred customers have ~16 % higher lifetime value, 37 % higher
  retention and convert 3–5× better than paid leads; Dropbox's two-sided referral grew
  sign-ups 3 900 % in 15 months (100 000 → 4 million). [69]
- *Live selling*: McKinsey reports live-commerce conversion approaching 30 %, up to ten
  times conventional e-commerce; 71 % of viewers trust the host over reviews. [70]
- *Community*: Peloton holds monthly connected-fitness churn near 1.6 % on community,
  instructors and lifecycle messaging — *industry-reported* from filings summaries. [45]

For DiscountDirect: proof in the reason line ("31 customers who own this filter bought
these pre-filters"), a two-sided "bring a friend" that rewards both, and a group offer
in the Pinduoduo shape ("three of you unlock the price") are all pack mechanics that
cost less than a discount to one person.

### 7.6 Surprise and mystery — gifts, blind boxes, variable rewards, lotteries
- *Surprise beats size*: surprise coupons handed over in-store led to 11 % higher spend
  than the same coupons received in advance. [49]
- *Reciprocity*: free samples raise later ratings and purchase (JECR 2023); the
  obligation fades within about a week if no purchase opportunity follows. [48]
- *Variable reward* is the third step of the Hook model (§7.2): an outcome that is not
  fully predictable is what people come back for. [39]
- *Blind boxes*: Pop Mart passed $5 billion revenue in 2025 (+185 %), selling over 100
  million Labubu units; its own study says 70 % of buyers purchase three or more boxes
  to get the one they want. The mechanism is variable-ratio reinforcement — the same
  as gambling — and the criticism follows. [71]
- *Lotteries instead of discounts*: Gaertig & Simmons (JCR 2025, 8 969 participants) —
  uncertain promotions ("1 in 10 orders is free") beat equivalent sure discounts **only
  when the sure discount is or seems trivial**; a 1 % lottery discount produced 54 %
  more spend than a 1 % fixed discount. [50]
- *Non-price promotions*: NielsenIQ — bundles carry 40 % of promoted revenue against
  52 % for price cuts; gift-with-purchase promotions relate positively to repeat
  purchase and advocacy. [51]

For DiscountDirect: a surprise sample in the next parcel, an unannounced gift after
the fifth order, a mystery item in the recurring list, or "one in ten orders free"
where a 3 % discount would be ignored — memorable, cheap, and none of them lowers the
reference price. Not for minors, not as a slot machine.

### 7.7 Scarcity, exclusivity and FOMO — drops, limited editions, waiting lists
- *Drops*: Nike's SNKRS app runs on controlled scarcity — timed releases, member-only
  draws, some launches over 10 million app opens in a day; estimates put SNKRS at $2.5–3
  billion a year (secondary). Limited editions command 30–50 % price premiums. [72]
- *Back-in-stock alerts* are true scarcity made useful: 58–65 % open rates and 14–25 %
  conversion, against 1–3 % for browse-abandonment e-mails — the highest-converting
  automated message in e-commerce. [73]
- *Price-drop and wish-list alerts*: 5–15 % conversion, 2–3× generic promotions. [74]
- *Countdowns and quantity limits*: ~8.6 % average lift when true; fake ones are
  prohibited under the Digital Services Act (§5). [21][22]

For DiscountDirect: the flash campaign already has time and quantity limits — enforce
them and show real remaining stock; add member-only early access to flash campaigns,
a waiting list with a back-in-stock message, and price-drop alerts on items a
customer has looked at. Exclusivity that is true is the cheapest FOMO there is.

### 7.8 Choice architecture — fewer options, one clear default
- Iyengar & Lepper's jam study: 24 flavours drew more tasters, 6 flavours sold ten
  times as often (30 % vs 3 %); later meta-analyses find the effect real but
  conditional on complexity and time pressure. [52]
- The decoy effect (Ariely's Economist pricing, 68 % → 84 % for the target option)
  became a pricing-page staple, but large replications with realistic stimuli found
  it mostly disappears — use with caution. [53]
- The Behavioural Insights Team's EAST checklist — Easy, Attractive, Social, Timely —
  is the practitioner summary of this whole section. [54]
- Free-shipping thresholds set 20–30 % above the average order lift order value
  12–30 % (industry-reported ranges; thresholds over 40 % above AOV push shoppers to
  abandon). [57]

For DiscountDirect: one offer per message, at most three choices, one default
already selected.

### 7.9 Timing and attention
- Personalised push notifications open at up to 4× the rate of generic ones; sending in
  a user's own preferred window lifts opens up to 40 %; retail apps peak 8–9 and 18–20;
  a day-3 / day-7 / day-14 re-engagement ladder recovers 10–25 % of lapsing users —
  all vendor benchmarks. [56]
- HelloFresh's add-on market lifted order value about 15 % by asking at the weekly
  order moment, not in a separate campaign — *industry-reported*. [58]
- Frequency caps are part of timing: four messages in 30 days is where 56 % unsubscribe
  (§6). [26]

### 7.10 The levers side by side

| Lever | Mechanism | Strongest evidence | DiscountDirect use |
|---|---|---|---|
| Laziness | lower effort, defaults | Madrian & Shea 50 → 86 %; Baymard 26 % / 17 % | one-tap reorder, saved payment, "your usual" |
| Habit | repeated prompt at the moment of need | Wood 43 %; Starbucks 5.6× daily | replenishment rhythm, predictable cadence |
| Loyalty programme | commitment, tiers, paid membership | Prime 2:1; Costco 92 %; tiers 78 % spend more; Genius 5× | named membership, tier, non-price perks, birthday |
| Gamification | progress, challenges, streaks | Nunes & Drèze 34 % vs 19 %; Tesco Challenges | head-start progress, personalised challenge, reorder streak |
| Pack mentality | herd cues, group buying, referral | badges +25 %; referral LTV +16 %; live 30 % | proof in the reason, bring-a-friend, group offer |
| Surprise | reciprocity, variable reward | surprise coupon +11 %; 1 % lottery +54 % spend | sample, gift, mystery item, small lottery |
| Scarcity | true limits, exclusivity | back-in-stock 14–25 % conversion; SNKRS | enforced limits, early access, waiting list |
| Choice | fewer options | jam 30 % vs 3 % | one offer, ≤3 choices, one default |
| Timing | right moment, right cadence | personalised push 4×; frequency cap | send-time per customer, re-engagement ladder |
| Price | last resort, margin cost | uplift 20–40 % non-incremental | learned depth, persuadables only |

## Part C — what this means for the prototype

## 8. The Hungarian market context

PwC Hungary's *Online Retail Big Picture* (June 2026): online retail turnover reached
**HUF 2 092 billion** in 2025 (about EUR 5.7 bn), 4.4 million people shop online, roughly
**a quarter of shoppers generate nearly 80 % of parcels**, cross-border marketplaces take
about 18 % of turnover, and 60 % of orders are placed on mobile. [27] The concentration is
the point: a Hungarian web shop's revenue sits with a small, repeat-buying core — exactly
the buyers DiscountDirect addresses one by one. And 93 % of them already carry loyalty
cards: membership is expected here, personalisation is wanted (42 %), and data
reluctance is high — the benefit has to be visible before the data is asked for. [47]

## 9. Fine-tuning the idea — twenty-eight changes to the prototype

The prototype's rules are in `business-logic.html`. Against the evidence above,
twenty-eight changes, each traceable to a source. The first twelve are about offers and
price (Part A); the other sixteen are the non-price levers (Part B) and matter more.

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

13. **Make reorder the default message type, not the offer.** "Your usual — one tap"
    with no discount attached; the discount appears only when the uplift model says
    the customer will not reorder otherwise (§7.1, §3.1).
14. **A "my usuals" surface for the buyer** built from order history, with the
    predicted next date on each item — the Buy Again pattern inside the thread (§7.1).
15. **Saved payment and address inside the accept step**; never send the buyer to a
    checkout that asks again (§7.1).
16. **A named membership with a tier** per seller, joined with one tap, with non-price
    perks — free delivery, early access to flash campaigns, priority answers — and a
    visible level the buyer can lose (§7.3).
17. **Progress with a head start**: "3 of 5 orders toward free delivery" as a message
    type, issued with the first stamp already earned; personalised challenges in the
    Clubcard shape (§7.4).
18. **Surprise as offer kinds**: sample in the next parcel, gift after the Nth order,
    mystery item in the recurring list, and a small probabilistic reward ("one in ten
    orders free") where the sure discount would be trivial (§7.6).
19. **Proof in the reason line**: what similar customers did, with real counts, never
    invented ones; a "best seller among customers like you" badge on the card (§7.5).
20. **Bring a friend, two-sided**: both the buyer and the friend get the perk; the
    referral lives in the thread as a shareable card (§7.5).
21. **Group offers**: "three of you unlock the price" — the buyer recruits the pack,
    the seller gets three orders for one discount (§7.5).
22. **One offer per message, at most three choices, one default selected**; the
    recommendation list in the seller view is for the seller, the buyer sees one card
    (§7.8).
23. **Send-time per customer** learned from when they open and accept, plus a lapse
    ladder at day 3 / 7 / 14 of inactivity relative to their own rhythm (§7.9, §7.2).
24. **Birthday and anniversary messages** with a one-step reward (§7.3).
25. **Waiting list and back-in-stock messages** for sold-out flash items — the
    highest-converting automated message there is (§7.7).
26. **Price-drop alerts** on items the buyer has viewed or declined (§7.7).
27. **Member-only early access** to flash campaigns, so exclusivity is real (§7.7).
28. **Investment the buyer keeps**: preferences, usuals, progress, tier and history
    visible in the buyer view, so leaving has a cost the buyer can see (§7.2).

Product ideas the evidence supports beyond the current scope: a buyer-initiated "ask for
a deal" in the thread; bundles from co-purchase patterns; a win-back trigger at the
segment's typical churn point; a buyer "offer wallet" across sellers; seller-to-buyer
content at the moment of use (how to change the filter, when to reorder).

## 10. What not to build

Mass newsletters to everyone (non-incremental, fatigue), fake urgency (illegal in the EU),
discounts to sure things (margin loss), profiling without a consent path (ePrivacy),
and acceptance rate as the success metric (measures generosity, not value). And on the
non-price side: never lead with a discount where convenience or a reminder would do;
no streaks, timers, badges or progress bars that are not true; no membership that is
only a coupon in disguise; no wheel-and-farm mechanics that borrow from gambling.

## 11. Research questions, decided for Release 1

The questions this research left open were decided on 2026-09-17 (SSOT D21–D24):
discount depth stays rule-based until 2 000 offers have outcomes; the holdout is 10 %,
pooled at seller level for sellers under 1 000 active relationships; reason experiments
compare wordings only, since a reason is always shown; WhatsApp precedes RCS in Hungary;
the default non-price perks are free delivery and early access; membership is per
seller first. Each stays open as a research topic for Release 2 and later.

## 12. Sources consulted

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
28. CIRP — *Amazon Prime shoppers outspend the rest* (2024 spend, $1 170 vs $570). https://cirpamazon.substack.com/p/amazon-prime-shoppers-outspend-the
29. Yahoo Finance / Zacks — *Costco's renewal rate slips to 89.8 %* and *Costco membership fees surge in 2025*. https://finance.yahoo.com/news/costcos-renewal-rate-slips-89-132600457.html · https://finance.yahoo.com/news/costco-membership-fees-surge-2025-142000361.html
30. Starbucks — *Starbucks unveils reimagined loyalty program* (2026) and Form 8-K FY2025 (34.6 m active members). https://about.starbucks.com/press/2026/starbucks-unveils-reimagined-loyalty-program-to-deliver-more-meaningful-value-personalization-and-engagement-to-members/ · https://www.sec.gov/Archives/edgar/data/829224/000082922425000013/sbux-12292024xexhibit991.htm
31. Eagle Eye — *Tesco Clubcard Challenges: personalization at scale*; The Grocer — *Tesco Clubcard: a 30-year legacy*. https://eagleeye.com/case-studies/tesco-clubcard-challenges · https://www.thegrocer.co.uk/comment-and-opinion/why-tesco-clubcard-is-a-30-year-legacy-of-supermarket-loyalty/701617.article
32. Red Stag Fulfillment — *What percentage of Amazon customers use Subscribe & Save?*; Velocity Sellers — *Subscribe & Save data deep-dive 2026*. https://redstagfulfillment.com/what-percentage-of-amazon-customers-use-subscribe-and-save/ · https://www.velocitysellers.com/2026/07/05/amazon-subscribe-save-data-deep-dive-2026/
33. BS&Co — *Repeat purchase rate benchmarks: 156K customers*. https://bsandco.us/blog-post/repeat-purchase-rate-benchmarks
34. NACS — *New Amazon feature to help "Buy Again"* (2023). https://www.convenience.org/stay-current/news/2023/october/11/5-new-amazon-feature_tech
35. Baymard Institute — *Cart abandonment rate statistics*. https://baymard.com/lists/cart-abandonment-rate
36. Fogg, B. J. — *Fogg Behavior Model*. https://www.behaviormodel.org/
37. Madrian, B. & Shea, D. — *The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior*, NBER w7682 (2000). https://www.nber.org/papers/w7682
38. APA Monitor — *Harnessing the power of habits* (Wood & Neal, 43 % of daily behaviour). https://www.apa.org/monitor/2020/11/career-lab-habits
39. Eyal, N. — *The Hooked Model: how to manufacture desire in 4 steps*. https://www.nirandfar.com/how-to-manufacture-desire/
40. Sensor Tower — *Duolingo's streak feature*; StriveCloud — *Duolingo gamification explained* (secondary figures). https://sensortower.com/blog/duolingo-streak-feature-app-engagement-growth · https://www.strivecloud.io/duolingo-gamification-explained
41. Nunes, J. & Drèze, X. — *The Endowed Progress Effect*, Journal of Consumer Research 32(4), 2006 (summary via Loyalty & Reward Co). https://loyaltyrewardco.com/loyalty-psychology-series-endowed-progress-effect/
42. *Playing to win: the impact of gamified loyalty programs in grocery retail*, Spanish Journal of Marketing – ESIC, 2025. https://doi.org/10.1108/SJME-10-2024-0276
43. Mastercard Advisors — *The impact of gamification on loyalty strategies* (industry figures). https://www.mastercardservices.com/en/advisors/consumer-engagement-loyalty-consulting/insights/impact-gamification-loyalty-strategies
44. Spiegel Research Center, Northwestern — *From reviews to revenue*. https://spiegel.medill.northwestern.edu/from-reviews-to-revenue/
45. Propel — *Peloton retention strategy teardown* (secondary). https://www.trypropel.ai/resources/blogs/peloton-retention-strategy-teardown
46. Joy — *Nike loyalty program: 7 pillars behind 300M members* (secondary). https://joy.so/blog/nike-loyalty-program/
47. Euronics — *A magyarok szívesen regisztrálnak hűségprogramokba*; marketing.hu — *Szeretik a magyarok a hűségprogramokat*. https://euronics.hu/blog/a-magyarok-szivesen-regisztralnak-husegprogramokba/ · https://marketing.hu/cikkek/hirek/szeretik-a-magyarok-a-husegprogramokat
48. Journal of Electronic Commerce Research 24(3), 2023 — *The reciprocity and diagnosticity effects* (free sampling). http://www.jecr.org/sites/default/files/2023vol24no3_Paper1.pdf
49. InsideBE — *Use reciprocity to increase sales* (surprise-coupon study). https://insidebe.com/articles/use-reciprocity-to-increase-sales/
50. Gaertig, C. & Simmons, J. P. — *Why (and When) Are Uncertain Price Promotions More Effective Than Equivalent Sure Discounts?*, Journal of Consumer Research 52(5), 2025. https://academic.oup.com/jcr/article/52/5/1022/8171334
51. NielsenIQ — *The relevance of price and non-price promotions* (2024). https://nielseniq.com/global/en/insights/commentary/2024/the-relevance-of-price-and-non-price-promotions/
52. Iyengar & Lepper (2000) via Econsultancy — *Want more sales? Give consumers fewer options*; *A Better Test of Choice Overload* (arXiv 2212.03931) for the replication picture. https://econsultancy.com/want-more-sales-give-consumers-fewer-options/ · https://arxiv.org/pdf/2212.03931
53. The Conversation — *The decoy effect*; Atticus Li — *The decoy effect: the pricing-page tactic that doesn't replicate*. https://theconversation.com/the-decoy-effect-how-you-are-influenced-to-choose-without-really-knowing-it-111259 · https://atticusli.com/replication-crisis/decoy-effect-asymmetric-dominance/
54. Behavioural Insights Team — *EAST: four simple ways to apply behavioural insights* (2014, revised 2024). https://www.bi.team/publications/east-four-simple-ways-to-apply-behavioural-insights/
55. Simply Psychology — *Techniques of compliance* (Freedman & Fraser foot-in-the-door). https://www.simplypsychology.org/compliance.html
56. MobiLoud — *50+ push notification statistics*; Business of Apps — *Push notifications statistics (2026)*. https://www.mobiloud.com/blog/push-notification-statistics · https://www.businessofapps.com/marketplace/push-notifications/research/push-notifications-statistics/
57. Digital Applied — *Free shipping threshold strategy 2026* (industry ranges). https://www.digitalapplied.com/blog/free-shipping-threshold-strategy-2026-ecommerce-playbook
58. The Brand Hopper — *HelloFresh marketing strategy* (add-on figures, secondary). https://thebrandhopper.com/brand/a-deep-dive-into-the-marketing-strategies-of-hellofresh/
59. Bond Brand Loyalty — *The 2025 Bond Loyalty Report*, executive summary. https://info.bondbrandloyalty.com/tlr2025/executive-summary
60. eMAG Marketplace — *The eMAG Genius program* (Hungary). https://marketplace.emag.hu/infocenter/emag-academy/the-emag-genius-program/?lang=en
61. SPAR Magyarország — *SuperShop hűségprogram*; SuperShop — programismertető. https://www.spar.hu/szolgaltatasok/supershop-husegprogram · https://www.supershop.hu/
62. Omnisend — *Birthday emails: examples and best practices* (benchmarks). https://www.omnisend.com/blog/birthday-emails-tips-and-best-practices/
63. Voucherify — *Guide to loyalty points expiration*; Li, Swaminathan & Kim — *Point redemption in loyalty programs*, Journal of Service Research 2025. https://www.voucherify.io/blog/guide-to-loyalty-points-expiration · https://journals.sagepub.com/doi/10.1177/10946705241246341
64. E-commerce Germany News — *Temu: king of extensive marketing, low prices and gamification*; Jeu: aide et référence — *Temu: the (false) promise of a jackpot?* https://ecommercegermany.com/blog/temu-king-of-extensive-marketing-low-prices-gamification/ · https://aidejeu.ca/en/articles/temu-false-promise-jackpot/
65. *The influence of gamification and reward coins on purchase decisions (Shopee, Indonesia)*, 2024. https://www.researchgate.net/publication/382366176_THE_INFLUENCE_OF_GAMIFICATION_AND_REWARDS_COIN_ON_PURCHASE_DECISIONS_SURVEY_ON_SHOPEE_CONSUMERS_IN_INDONESIA
66. CNBC — *McDonald's Q4 2025 earnings*; Restaurant Business — *McDonald's sales soared last quarter, thanks to the Grinch and Monopoly*. https://www.cnbc.com/2026/02/11/mcdonalds-mcd-q4-2025-earnings.html · https://www.restaurantbusinessonline.com/financing/mcdonalds-sales-soared-last-quarter-thanks-grinch-monopoly
67. *Following the herd: the influence of the bandwagon heuristic on e-commerce shoppers*, arXiv 2505.14861; WebToffee — *The psychology of best sellers* (Profitero figures, secondary). https://arxiv.org/pdf/2505.14861 · https://www.webtoffee.com/blog/psychology-behind-best-sellers/
68. Inside Startups — *From 0 to 725 million users: growth levers used by Pinduoduo*; UXmatters — *How Pinduoduo's group-buying model shapes the Asian e-commerce experience*. https://insidestartups.substack.com/p/from-0-725-million-users-growth-levers · https://www.uxmatters.com/mt/archives/2024/12/how-pinduoduos-group-buying-model-shapes-the-asian-ecommerce-experience-1.php
69. Extole — *Referral marketing statistics 2026*; Viral Loops — *How Dropbox grew 3 900 % with referrals*. https://www.extole.com/blog/referral-stats-to-know-in-2026/ · https://viral-loops.com/blog/dropbox-grew-3900-simple-referral-program/
70. McKinsey — *It's showtime! How live commerce is transforming the shopping experience*. https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/its-showtime-how-live-commerce-is-transforming-the-shopping-experience
71. Exploding Topics — *Blind boxes: the retail hack behind Labubu*; Current Psychology 2025 — *Why do you engage in blind box consumption?* https://explodingtopics.com/blog/blind-box-trends · https://link.springer.com/article/10.1007/s12144-025-08150-x
72. Indigo9 Digital — *How Nike is using mobile apps to increase sales* (SNKRS); Shopify — *Limited drops: use scarcity to drive sales*. https://www.indigo9digital.com/blog/how-nike-is-turning-your-smart-phone-into-a-digital-shopping-assistant · https://www.shopify.com/blog/limited-drops
73. MarketingSherpa — *Back-in-stock alert emails achieve 22.45 % conversion*; Storebeep — *Back-in-stock notification benchmarks 2026*. https://marketingsherpa.com/article/case-study/backinstock-alert-emails-achieve-2245 · https://storebeep.com/blog/back-in-stock-notification-benchmarks-2026
74. Sequenzy — *Price drop alert emails that convert*; Swym — *Email conversion rate by industry*. https://www.sequenzy.com/for/price-drop-alert-email · https://www.getswym.com/statistics/email-conversion-rate-by-industry
