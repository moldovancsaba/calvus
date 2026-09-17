# DiscountDirect — executive summary

*A direct, explained, consented offer machine between a web shop and each of its
customers.* Prepared 2026-09-17. The evidence for every figure is in the research page;
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
per relationship. In it the seller sends offers that are:

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
| Less wasted discount | Uplift-based targeting removes the 20–40 % of programmes with no incremental lift and stops discounting sure things |
| Better channels | Rich messaging carries 3–7× the click-through of SMS; Cdiscount saw +9 % basket |
| Trust and compliance by design | Explained offers raise trust; consent, frequency caps, true scarcity and the 30-day price rule keep the shop inside GDPR, ePrivacy and the Digital Services Act |

## How we implement it

**Phase 1 — Foundation (rules, not models).** Integrate with the shop's order data
(Shopify, WooCommerce, and the Hungarian platforms UNAS and Shoprenter as the first
connectors); build the seller–customer thread, offers with reasons, flash campaigns with
enforced limits, recurring lists, in-app and e-mail delivery; write reasons from rules
(replenishment interval, accessory of an owned product, upgrade after N months). Ship
with a **randomised holdout** and incremental-margin reporting from day one.

**Phase 2 — Decision engine.** Replace rules with a buyer × product relevance model and
reason codes; add uplift-based targeting so only persuadables are treated; add
event-driven timing (order confirmed, 24–48 h, 7–14 days, predicted run-out, 60–90 days);
add rich messaging (RCS/WhatsApp) and the buyer's preference centre.

**Phase 3 — Learned discounts and scale.** Discount depth as a bandit decision under a
margin floor and budget; subscription offers for consumables; bundles from co-purchase
patterns; multi-seller buyer wallet; printed DM with coupons for high-value durables.

**Compliance track, all phases.** Legitimate-interest assessment and soft opt-in for
existing customers, consent for profiling channels, Article 21 objection honoured in
one tap, frequency caps per channel, no fake urgency, 30-day-low reference prices.

**What success looks like.** Incremental contribution margin per campaign (not
acceptance rate); take rate by moment; unsubscribe and decline rates per buyer; share of
revenue from the repeat core.

## Where to look

- The clickable prototype: [index.html](index.html)
- The rules it implements: [business-logic.html](business-logic.html)
- The research and sources: [research.html](research.html)
