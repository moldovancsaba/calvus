# DiscountDirect — business logic breakdown

Derived from the prototype at `discountdirect/index.html` (v15) on 2026-09-17, function by
function and data structure by data structure. Everything below is what the prototype
*does*; §8 lists what it *implies* but does not do, which is the development backlog.
Sample data (one seller, eight buyers, 26 catalogue products, one running automation) is
in-memory and resets on reload.

## 1. Purpose and actors

DiscountDirect is a messaging surface between a **seller** (a web shop; the sample is
ElektroHome Kft.) and each of its **buyers**, in which the seller sends **personalised
discount offers** grounded in that buyer's purchase history with that seller — instead of
untargeted mass promotions. The buyer sees why every offer was sent.

| Actor | What they do in the prototype |
|---|---|
| Seller | Reads each buyer's history and recommendations; sends one-off offers on a chosen channel; runs one-product flash campaigns to every relevant buyer; sets up recurring per-buyer offer lists; chats. |
| Buyer | Sees one conversation (with this seller), the history that justifies the offers, and the offers themselves in chat, e-mail, postal letter or newsletter form; accepts or declines pending offers; chats. |
| Recommendation engine (implied) | Produces the per-buyer recommendation list and the per-product relevance set with a reason per buyer. In the prototype both are hard-coded "the way an engine's output would look". |

The unit of the system is the **seller–buyer pair**: a conversation with its history,
recommendations and timeline. Nothing crosses pairs except campaigns and automations,
which fan out to many pairs at once.

**Mission (product owner, 2026-09-17, D12).** DiscountDirect is a **retention system**:
it exists to avoid churn and raise customer lifetime value for the seller, and to make
every offer worth receiving for the buyer.

**Platform principle (D10, D13).** The platform ships **predefined rule sets** and
recommended user journeys — offer types, campaign shapes, sold-out handling,
compensation menus, incentives, timing ladders, consent settings. A seller runs on the
predefined rule set or switches an area to **advanced mode**, where its own business
decisions apply — percentages, vouchers, freebies, compensation. Legal and consent
defaults belong to the platform; advanced mode may add to them but never go below their
floor. Every rule in §3 is therefore a predefined default, not a constraint.

**Transparency (D14).** Everything is clearly communicated to the buyer: if compensation
is available it is stated; if an offer is first-come-first-served with limited quantity,
or carries any other rule, that rule appears on every communication of the offer.

## 2. Entities and data model (as coded)

| Entity | Fields | Notes |
|---|---|---|
| **Seller** | `name`, `sub` (tagline: category · response time) | Single seller in the prototype. |
| **Conversation** (= buyer relationship) | `id`, `buyer` (name), `color`, `buyerSub` (segment label), `history[]`, `recs[]`, `messages[]` | `buyerSub` encodes a segment — *Törzsvásárló / Visszatérő vevő / Új vevő* · order count · since year — as free text; a real model needs these as fields. |
| **PurchaseHistoryItem** | `item`, `when` (date text), `price` (HUF) | 2–9 items per buyer, 2023–2026. |
| **Recommendation** | `product`, `reason`, `orig`, `pct` | Per buyer. **Consumed when sent** (removed from the list); not linked to a catalogue id. |
| **CatalogueProduct** | `id`, `name`, `price`, `relevant[]` (buyer ids), `why{buyerId: reason}` | Relevance is a precomputed set per product with a per-buyer justification. 24 products relevant to one buyer, one to three, one to five. |
| **Message** — text | `from` (`seller`/`buyer`), `text`, `at` | Free chat. |
| **Message** — event | `from: seller`, `event{channel, text}`, `at` | A delivery on a non-chat channel (DM letter sent, newsletter sent, e-mail sent). |
| **Message** — offer | `from`, `offer{kind?, product, reason, orig, pct, status, channels[], limitH?, limitQty?}`, `at` | `kind = 'flash'` for campaign offers, absent for personal offers. `status ∈ pending / accepted / declined`. |
| **Automation** (recurring list) | `title`, `freq` (*Hetente / Kéthetente / Havonta*), `channels[]`, `products[]` (names), `next` (date text) | Per-buyer content is derived at render time from catalogue relevance, not stored. |
| **Channel** | enum: *Azonnali üzenet* (in-app chat), *E-mail*, *Mailing* (printed DM letter); plus *Hírlevél* (newsletter) as an event/automation channel | Icons: 💬 ✉️ 📮 🗞. |

Timestamps are display strings (`'most'`, `'tegnap'`, `'ápr. 15.'`); currency is HUF,
formatted `hu-HU`; all UI strings are Hungarian.

## 3. Business rules, as implemented

### 3.1 Personalised offer (seller → one buyer)
- Source: the buyer's recommendation list. Each card shows product, reason, original
  price, discounted price and −pct. Decided (D4, §10): the reason is **written by the
  engine and editable by the seller**; both versions are kept.
- The seller picks **exactly one channel** per send (select: chat / e-mail / mailing).
- Sending appends an **offer message** (`status: pending`, `channels: [channel]`, `at: 'most'`)
  to the conversation and **removes the recommendation** — an offer is made once.
- Discounted price everywhere: `round(orig × (1 − pct/100))`.

### 3.2 Where an offer appears in the timeline
- If the offer's channels include *Azonnali üzenet*, it renders as a **chat bubble** on the
  sender's side (seller view: right; buyer view: mirrored).
- Otherwise it renders as a **full-width timeline event** headed by the channel labels
  ("✉️ E-mail + 📮 Mailing · ajánlat kiküldve" / "… · villámajánlat").
- Non-offer deliveries (a letter sent, a newsletter sent, a file e-mailed) are timeline
  events with their channel — the timeline is the single record of every touch, on every
  channel, in one place.

### 3.3 Buyer response to an offer
- Only the **buyer**, only on **seller-sent** offers, only while **pending**.
- Standard offer: *Elfogadom* → `accepted` ("Elfogadva") · *Most nem* → `declined`
  ("Elutasítva").
- Flash offer: *Megveszem most* → `accepted` ("Megvásárolva") · *Kihagyom* → `declined`
  ("Kihagyva").
- `accepted` and `declined` are terminal; the card then shows the status label only.
- **Accepting does not create an order** in the prototype. Decided (D1, §10): accepting
  **hands off to the shop's own checkout** with the offer's price locked; the order is
  closed in the shop and reported back to the thread.

### 3.4 Conversation list (seller inbox)
- One row per buyer: avatar (initials, buyer colour), name, **last-message preview**
  (text, or the event text, or "Ajánlat: product"), and a **badge = number of pending
  offers** in that conversation.
- Buyer view shows a single row — the conversation with this seller; which buyer the demo
  is showing is chosen in the top-bar persona selector, not in the list.

### 3.5 Flash campaign (⚡ Villámajánlat)
- **One product** (radio), from the whole catalogue; each option shows price and
  "N releváns vevő".
- Parameters: discount `pct ∈ {10, 15, 20, 25}` (default 15), time limit `∈ {6, 24, 48}` h
  (default 24), quantity limit `∈ {10, 20, 50}` (default 20), channels multi-select
  (default chat + e-mail; if none checked the send reports chat).
- **Targets = the product's relevant buyers**, each with the product's per-buyer reason;
  shown before sending ("Kik kapják?").
- Decided (D14, §10): the flash card and every channel rendering carry a **rules block**
  — expiry, total and per-buyer quantity, first-come-first-served, and the compensation
  if one is configured — before the buyer decides.
- Live preview of the card the buyer will see: tag "⚡ Villámajánlat · H óráig · Q db",
  templated reason "Csak H óráig vagy a készlet erejéig (Q db) — a korábbi vásárlásaid
  alapján neked szól.", prices, channel chips, disabled buy/skip buttons.
- Sending appends **one pending flash offer per relevant buyer** (with `limitH`,
  `limitQty`, `channels`) and confirms "Elküldve N releváns vevőnek (names) — csatorna: …".
- Not enforced in the prototype: expiry after `limitH`, decrementing `limitQty` on
  purchase, first-come-first-served, stock.
- Decided (D2, §10): the quantity limit exists **both per campaign in total and per
  buyer**; both are set by the seller and both are enforced. When the campaign sells out,
  buyers who already received the offer are **informed** in the thread, and the seller may
  attach an **optional compensation** to that message — either **pre-configured** from the
  platform's menu (voucher, free delivery, priority on the next campaign) or the seller's
  own choice in **advanced mode** (D10, D13); when configured in advance it is shown on
  the flash card itself (D14).

### 3.6 Recurring personalised list (🗞 Automatikus ajánlatlista)
- **Many products** (checkboxes); each option lists the buyers it is relevant to.
- Frequency *Hetente / Kéthetente / Havonta* (default Kéthetente); channels multi-select
  (default e-mail; falls back to e-mail if none).
- **Per-buyer split** (the core rule): for every buyer, the list contains only the selected
  products whose relevance set includes that buyer; buyers with no matching product are
  left out entirely. The split is previewed live before starting.
- Starting creates an Automation titled "Ajánlatlista #n" with a next-send date
  (*Hetente* → "hétfő", *Kéthetente* → "szeptember 7.", *Havonta* → "szeptember 1." —
  hard-coded); the selection is cleared.
- Active automations show title, frequency, product count and channels, the per-buyer
  breakdown, next send, and **Leállítás** (delete).
- Not implemented: the scheduler, the actual sends, a per-item discount for list items
  (the newsletter mock uses the buyer's matching recommendation pct or 10 %).

### 3.7 How the same offer reaches the buyer on each channel (buyer view tabs)
- **Chat**: the timeline of §3.2 with the accept/decline actions of §3.3.
- **E-mail**: from `ajanlat@elektrohome.hu`, subject "Személyre szabott ajánlat: product
  −pct%", greeting by first name, the offer card, a CTA "Ajánlat megnyitása a
  DiscountDirectben", the line that replying continues the conversation in chat, and a
  footer with the reason for receipt plus *Leiratkozás · Ajánlatbeállítások*.
- **Postal letter (Mailing)**: letterhead and date, postal address, formal salutation
  (*Tisztelt X Úr!* / *Tisztelt X!* — the prototype guesses gender from the first name, a
  placeholder heuristic, not a rule), the offer, a **coupon code** `DIRECT-<pct>-<initials>`
  redeemable in store and online, and a pointer to the app. Decided (D6, §10): the coupon
  is **single-use** and **maps one-to-one to the online offer** — redeeming either closes
  both. Decided (D9, §10): the platform always produces the **printable content**;
  printing and posting is either a **DiscountDirect service** (print partner integrated
  by the platform) or done **by the seller** — the seller chooses.
- **Newsletter (Hírlevél)**: banner with the frequency of the first running automation,
  greeting, **every catalogue product relevant to this buyer** with its per-buyer reason
  and a discount (matching recommendation pct or 10 %), footer with *Leiratkozás ·
  Gyakoriság módosítása*. Decided (D7, §10): the list discount is a **seller-level default
  rule that each list can override**.
- Which offer the e-mail and letter feature: the **newest offer in the thread**, else the
  first recommendation, else the first relevant catalogue product at 15 %.

### 3.8 Transparency to the buyer
- The buyer's context pane shows their purchase history at this seller and the statement
  that offers are sent only on the basis of those orders and matching recommendations —
  "kéretlen tömegajánlat helyett". Every offer carries its reason. This is a product
  principle, not decoration: it is the consent story.

### 3.9 Chat
- Free text both ways; Enter or the button sends; the message is stamped 'most' and
  attributed to the current view's role.

## 4. State and lifecycle

**Offer**: `pending → accepted | declined` (terminal). Created by: recommendation send
(personal) or flash campaign send (flash). Only the buyer transitions it.

**Recommendation**: `available → sent` (removed from the list on send; the offer message is
the record).

**Automation**: `running → stopped` (deleted). `next` is display text; there is no clock.

**Flash offer limits** (`limitH`, `limitQty`): carried on the offer, displayed, never
evaluated.

## 5. Screens and navigation

| View | Tab | Screen | Panes |
|---|---|---|---|
| Seller | Csevegések | chat | buyer list · thread + composer · context (history, recommendations with channel select + send) |
| Seller | ⚡ Villámajánlat | flash | campaign setup (product, pct, hours, qty, channels, send, result) · targeting + live preview |
| Seller | 🗞 Ajánlatlisták | list | new list (products, frequency, channels, start, result) · per-buyer preview · active automations |
| Buyer | Csevegés | chat | own inbox (one row) · thread with accept/decline · context (history, "why these offers") |
| Buyer | E-mail / Postai levél / Hírlevél | mocks | the same offer rendered for that channel |

A top-bar toggle switches view; a persona selector (buyer view only) chooses which buyer
the demo shows. Every state change re-renders everything (`renderAll`).

## 6. Derived values

| Value | Rule |
|---|---|
| Discounted price | `round(orig × (1 − pct/100))` |
| Pending badge | count of offers with `status = pending` in the conversation |
| Last-message preview | text · event text · "Ajánlat: product" |
| "N releváns vevő" | `product.relevant.length` |
| Flash targets | `product.relevant` with `product.why[buyer]` |
| List split per buyer | selected products ∩ products relevant to the buyer |
| Newsletter items | all catalogue products relevant to the buyer |
| Newsletter discount | buyer's recommendation pct for that product, else 10 % |
| Featured deal (e-mail, letter) | newest offer → first recommendation → first relevant product at 15 % |
| Coupon code | `DIRECT-<pct>-<buyer initials>` |

## 7. Data the prototype treats as given

- The **recommendation list per buyer** and the **relevance set per product with a reason
  per buyer** — two separate hard-coded outputs of the same implied engine. Development
  should produce both from one model (buyer × product → score + reason) or make the
  catalogue relevance the single source and derive recommendations from it.
- Segment labels (*Törzsvásárló* etc.), order counts and "since" years as text.
- Dates and times as display strings.

## 8. What development has to build (implied, not implemented)

1. **Persistence and identity**: users, sellers, buyers, conversations, messages, offers,
   automations; roles and authentication for the two actors; a buyer with **many sellers**
   (the prototype has one). Decided (D3): a seller chooses whether its buyers see it in a
   **shared marketplace inbox** or in a **per-seller app**; both modes ship.
2. **Recommendation engine** (or its integration): purchase history → per-buyer product
   scores with human-readable reasons; segment derivation (loyal / returning / new, order
   count, tenure).
3. **Channel delivery**: chat push, transactional e-mail (with the CTA deep link and
   reply-to-thread), printed DM with coupon (print/post integration), newsletter compose
   and send; per-message delivery events written to the timeline.
4. **Offer lifecycle**: accept → **hand-off to the shop's checkout** with the price
   locked (a signed link or cart token), order confirmation written back to the thread;
   decline; expiry by `limitH`; per-campaign and per-buyer `limitQty` decrement and
   sold-out state; first-come handling for flash campaigns; sold-out notice with optional
   compensation; single-use coupon issuance and redemption mapped to the offer (D1, D2,
   D6).
5. **Scheduler** for automations: frequency → next run, per-run content freeze, per-buyer
   send, skip buyers with no relevant items, stop/pause.
6. **Consent and preferences**: unsubscribe per channel, frequency preference, legal
   basis for history-driven marketing **configured per market and channel — legitimate
   interest with soft opt-in where the market allows it, consent elsewhere** — with
   retention periods per market, and an audit of why each offer was sent (the reason is
   already first-class) (D8). In marketplace mode the buyer's consent and frequency cap
   apply **per seller or across the inbox — both scopes exist and are a setting** (D11).
7. **Pricing guardrails**: per seller, **either fixed steps or free entry**, both under
   guardrails (floor, margin, per-segment limits); the mode is a seller setting (D5).
8. **Timestamps, time zones, locale**: real datetimes; HUF and `hu-HU` today, others later.
9. **Metrics**: sent / opened / accepted / declined / expired per offer, campaign and
   automation; response time; badge counts from real state.
10. **Notifications** to the seller on buyer actions; to the buyer on new offers.
11. **Design system**: the CSS tokens are already named after GDS 6.5.0 roles
    (`GDS-TOKEN-MAP.md`); the dev build swaps the `:root` block for the GDS theme.
12. **Predefined rule sets, advanced mode and journeys** (D10, D13): a library of rule
    sets and recommended journeys — offer kinds, campaign defaults, incentives,
    sold-out and compensation handling, timing ladders, consent scope — a per-area
    **advanced mode** switch with the seller's own values above the legal floor, and
    versioning so an audit can show which rule set and which advanced values produced a
    given offer.
14. **Transparency renderer** (D14): one component that composes the rules block for
    every channel rendering of an offer from its limits, expiry, compensation and
    reference price.
13. **Print fulfilment** (D9): printable letter generation for every offer; an optional
    print-and-post service through an integrated partner, or download for the seller's
    own printing; delivery status back to the timeline either way.

## 9. Suggested domain model

```
Seller(id, name, tagline,
       inbox_mode: marketplace|per_seller,                                -- D3
       discount_mode: steps|free, discount_guardrails{floor_pct, max_pct, margin_floor},  -- D5
       newsletter_discount_rule,                                         -- D7 default
       print_mode: platform_service|seller,                               -- D9
       consent_scope: per_seller|inbox,                                   -- D11
       compensation_mode: preset|free)                                    -- D10
Template(id, kind: offer|campaign|journey|sold_out|compensation|timing|consent,
         version, defaults{})                                             -- D10 platform library
SellerOverride(seller_id, template_id, mode: predefined|advanced, values{}, version)   -- D13
Template(..., legal: bool, floor{})                                       -- legal floor for advanced mode
Market(code, legal_basis: legitimate_interest|consent, retention_days, soft_opt_in: bool)  -- D8
Buyer(id, name, postal_address, email, consents{chat,email,mailing,newsletter}, preferences{frequency})
Relationship(seller_id, buyer_id, segment, order_count, since)          -- one per pair
Order(id, relationship_id, product_id, price, ordered_at)               -- purchase history
Product(id, seller_id, name, price)
Relevance(product_id, buyer_id, score, reason)                          -- engine output
Recommendation(id, relationship_id, product_id, pct, reason, state)     -- available|sent
Offer(id, relationship_id, product_id, kind, orig, pct,
      reason_engine, reason_seller?,                                      -- D4
      channels[], status, limit_hours, limit_qty_per_buyer, expires_at, sent_at,
      responded_at, checkout_url?, order_ref?)                            -- D1 hand-off
Message(id, relationship_id, from, kind: text|event|offer_ref, body, channel?, at)
Campaign(id, seller_id, product_id, pct, limit_hours, limit_qty_total, limit_qty_per_buyer,
         channels[], sent_at, sold_out_at?,
         compensation?{kind: voucher|free_delivery|priority|custom, value})  -- D2, D10; fans out to Offers
Automation(id, seller_id, title, frequency, channels[], product_ids[], next_run_at, state,
           discount_rule_override?)                                      -- D7
Delivery(id, message_id|offer_id, channel, status, at,
         print_job_id?)                                                   -- per-channel send record; D9
Coupon(code, offer_id, single_use: true, redeemed_at?, redeemed_channel?)  -- D6, one per offer
```

## 10. Decisions of the product owner (2026-09-17)

The open questions were answered by the product owner in two rounds (D1–D8, then
D9–D11); the answers are recorded here and propagated into §1, §3, §8 and §9 with the
tag *Decided (Dn)*.

| # | Question | Decision | Consequence |
|---|---|---|---|
| D1 | Does accepting complete a purchase in-app, or hand off to the shop's checkout? | **Hand off** | Accept opens the shop's checkout with the offer price locked; the order confirmation is written back to the thread (§3.3, §8.4). |
| D2 | Flash quantity: per campaign total, or per buyer? What happens at sold-out for buyers who already received it? | **Both limits.** At sold-out, **inform** those buyers and offer **optional compensation** for the disappointment | Two counters, both enforced; a sold-out notice message type with an optional seller-chosen goodwill gesture (§3.5, §8.4). |
| D3 | One inbox across sellers (marketplace) or an app per seller? | **Both, set by the seller** | Seller setting `inbox_mode`; the buyer view must work in both (§8.1, §9). |
| D4 | Who owns the reason text? | **Both** — engine writes, seller may edit | Two fields kept; the buyer sees the seller's edit when present, the audit keeps both (§3.1, §9). |
| D5 | Discount authority: fixed steps or free entry with guardrails? | **Both, set by the seller** | Seller setting `discount_mode` plus guardrails that apply in either mode (§8.7, §9). |
| D6 | Postal coupon: single-use? maps to the online offer? | **Single-use, mapped to the online offer** | One coupon per offer; redeeming in store or online closes the offer everywhere (§3.7, §9). Who prints and posts remains open — see §11. |
| D7 | Newsletter discount: a rule, or set per list? | **Both** | Seller-level default rule, overridable per list (§3.6–3.7, §9). |
| D8 | Legal basis and retention for purchase-history marketing, per market | **Both bases** | Per-market configuration: legitimate interest with soft opt-in where allowed, consent elsewhere; retention per market (§8.6, §9). Read as "both legal bases, chosen per market"; correct if meant otherwise. |
| D9 | Postal letters: who prints and posts? | **Either** — a DiscountDirect service or the seller; **the platform always provides the printable content** | Seller setting `print_mode`; letter generation is core, print-and-post is an optional service (§3.7, §8.13, §9). |
| D10 | Sold-out compensation: fixed menu or free choice? | **Both** — pre-set from a menu, or chosen freely at the time. **General principle:** the platform provides built-in business-logic templates and user-journey recommendations that the seller can follow, modify or overwrite according to its business targets; the platform automates support for sellers and helps buyers (owner's words; since D13 the terms are *predefined rule set* and *advanced mode*) | Rule-set library with per-area advanced mode and versioning; every §3 rule is a default (§1, §3.5, §8.12, §9). |
| D11 | Marketplace mode: consent and frequency cap per seller or across the inbox? | **Both, as a setting** | `consent_scope` setting; the cap engine must count per seller or per inbox accordingly (§8.6, §9). |
| D12 | (mission) | The platform is a **well-designed retention system** to avoid churn and improve customer lifetime value | Stated in §1; churn and LTV become the north-star metrics (SSOT §7). |
| D13 | Who may change legal or consent defaults? Where do incentives come from? | **Platform owns legal and consent defaults; the seller keeps additional options within limits.** Percentages, vouchers, freebies and compensation come from **predefined rule sets** or from the seller in **advanced mode** — the system-wide term for the seller's own business decisions | `OperatingMode {predefined, advanced}` per area replaces follow/modify/overwrite; legal templates carry a floor (§1, §8.12, §9). |
| D14 | Compensation promised before sold-out or issued after? | **Everything clearly communicated**: compensation if available, first-come-first-served, limited quantities and every other rule on every communication | Rules block on every rendering (§3.5, §3.7); SSOT R21. |

## 11. Still open

1. Which print partner to integrate for the print-and-post service (D9); the commercial
   rules for it follow D13 (predefined rule set or advanced mode).
