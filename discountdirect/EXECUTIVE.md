# DiscountDirect — executive summary

*A direct, explained, consented relationship machine between a web shop and each of
its customers — where the discount is the last lever, not the first.* Prepared 2026-09-17. The evidence for every figure is in the research page;
the rules of the prototype are in the business-logic page.

## The problem

Web shops discount blindly. Mass coupons and newsletters go to everyone, so most of the
money subsidises customers who would have bought anyway — figures of 35 % of promotional
spend going to loyal buyers who needed no discount, and half of promotions failing to
return, circulate across the industry. Customers feel it as noise: 71 % want personalised
offers and proactive help, 34 % of brands deliver them, and 56 % unsubscribe after four
messages in a month. Meanwhile the revenue of a typical Hungarian web shop sits with a
small repeat-buying core: a quarter of online shoppers generate nearly 80 % of parcels.

## The service

DiscountDirect is a messaging surface between a seller and **each customer**, one thread
per relationship. Most of what travels in it is not a discount: a one-tap reorder of
the customer's usual items, a reminder timed to when they will run out, a progress
step toward a perk, a sample or a gift, early access for members. When an offer does
carry a price cut, it is:

- **grounded** in that customer's own purchase history with that shop,
- **explained** — every offer says why it was sent,
- **timed** — replenishment before run-out, accessories after a purchase, upgrades when
  the cycle turns,
- **limited and true** — flash offers with enforced time and quantity limits,
- **delivered where the customer is** — in-app chat, e-mail, rich messaging, and
  printed mail with a coupon for high-value items,
- **consented** — the customer sees the history that justifies each offer and controls
  channels and frequency.

Three seller tools sit on top: one-off personalised offers from a recommendation list,
one-product flash campaigns to every relevant customer, and recurring per-customer offer
lists that each customer receives only with the products relevant to them.

## Why not just discount

The strongest B2C machines run on eight levers before price, and the research page
carries the evidence for each:

- **Laziness.** The easiest action wins: defaults moved plan participation from 50 %
  to 86 % with no change in value; a quarter of shoppers abandon when asked to create
  an account. One-tap reorder beats a coupon that needs a checkout.
- **Habit.** Around 43 % of daily actions are habitual. A shop that owns the reorder
  rhythm does not compete on price; Starbucks members visit 5.6× more often.
- **Membership.** Prime members spend twice what non-members do; Costco renews at
  92 %; 84 % of Tesco's UK sales are Clubcard-linked. Hungarians already carry loyalty
  cards — 93 % are in a programme.
- **Progress.** A loyalty card issued with two of ten stamps already filled was
  completed by 34 % of customers against 19 % for an empty eight-stamp card.
- **Social proof.** The first five reviews carry the largest effect; "customers who
  own this also bought" is proof as well as recommendation.
- **Reciprocity.** A surprise coupon produced 11 % more spend than the same coupon
  received in advance; a sample or a gift is remembered longer than 15 % off.
- **Choice.** Six options sold ten times as often as twenty-four. One offer, one
  button, one default.
- **Timing.** Personalised, well-timed messages open at up to four times the rate;
  four messages in a month is where most people unsubscribe.

Discounts then go only where the evidence says they change behaviour: to persuadable
customers, at a learned depth, measured against a holdout.

## How it helps

**The seller** sells more to the customers it already has, at a discount depth the
customer actually needs, on a channel the customer reads — and knows what each offer
earned, because every send is measured against a holdout.

**The customer** gets fewer, better offers, understands why, and can say "not this, not
now, not this often" without leaving.

## The benefits, with the evidence behind them

| Benefit | What the evidence says |
|---|---|
| More revenue from existing customers | Personalisation lifts revenue 10–15 % (McKinsey); recommendations drive up to 31 % of e-commerce revenue (Barilliance); post-purchase flows return $2–5 per recipient (Klaviyo benchmarks) |
| Higher conversion per offer | Confirmation-page offers convert 10–16 %; replenishment reminders 8–15 % versus 1–3 % for generic promotions |
| More repeat orders without discounting | 77 % of repeat purchases are reorders; Subscribe & Save gives Amazon sellers 20–35 % of sales; a head-start progress card nearly doubled completion |
| Stronger retention | Membership programmes double spend (Prime 2:1) and hold renewal above 90 % (Costco); habit and progress mechanics keep customers without price cuts |
| Less wasted discount | Uplift-based targeting removes the 20–40 % of programmes with no incremental lift and stops discounting sure things |
| Better channels | Rich messaging carries 3–7× the click-through of SMS; Cdiscount saw +9 % basket |
| Trust and compliance by design | Explained offers raise trust; consent, frequency caps, true scarcity and the 30-day price rule keep the shop inside GDPR, ePrivacy and the Digital Services Act |

## How we implement it

**Phase 1 — Foundation (rules, not models).** Integrate with the shop's order data
(Shopify, WooCommerce, and the Hungarian platforms UNAS and Shoprenter as the first
connectors); build the seller–customer thread, **one-tap reorder of the customer's usuals with
saved payment**, offers with reasons, flash campaigns with enforced limits, recurring
lists, in-app and e-mail delivery; write reasons from rules (replenishment interval,
accessory of an owned product, upgrade after N months); ship the first non-price
message types — the run-out reminder and the progress card with a head start. Ship
with a **randomised holdout** and incremental-margin reporting from day one.

**Phase 2 — Decision engine.** Replace rules with a buyer × product relevance model and
reason codes; add uplift-based targeting so only persuadables are treated; add
event-driven timing (order confirmed, 24–48 h, 7–14 days, predicted run-out, 60–90 days);
add rich messaging (RCS/WhatsApp) and the buyer's preference centre; launch the
**named membership** with non-price perks (free delivery, early access, priority
answers), proof counts in the reason line, and send-time learned per customer.

**Phase 3 — Learned discounts and scale.** Discount depth as a bandit decision under a
margin floor and budget; subscription offers for consumables; bundles from co-purchase
patterns; samples, gifts and small probabilistic rewards as offer kinds; personalised
challenges in the Tesco Clubcard style; multi-seller buyer wallet; printed DM with
coupons for high-value durables.

**Compliance track, all phases.** Legitimate-interest assessment and soft opt-in for
existing customers, consent for profiling channels, Article 21 objection honoured in
one tap, frequency caps per channel, no fake urgency, 30-day-low reference prices.

**What success looks like.** Incremental contribution margin per campaign (not
acceptance rate); share of repeat orders that needed no discount; take rate by moment;
membership share of revenue; unsubscribe and decline rates per buyer; share of revenue
from the repeat core.

## Where to look

- The clickable prototype: [index.html](index.html)
- The rules it implements: [business-logic.html](business-logic.html)
- The research and sources: [research.html](research.html)
