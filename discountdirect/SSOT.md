# DiscountDirect — single source of truth (SSOT)

Version 1.0 · 2026-09-17. This document is the canonical definition of every term,
entity, enumeration, setting, rule, decision and metric in DiscountDirect. When two
documents disagree, this one wins; a change to a definition lands here first, with a
version bump, and the other documents follow.

**Precedence:** SSOT → `business-logic.html` (rules as implemented and decided) →
`architecture.html` → `technical-design.html` → `implementation-plan.html` →
`executive.html` / `research.html` (context). The prototype at `index.html` is an
illustration of the rules, never their definition.

## 1. Glossary

**Mission (product owner, D12).** DiscountDirect is a **retention system**: its purpose
is to avoid churn and raise customer lifetime value for the seller, and to make offers
worth receiving for the buyer. Discounts, campaigns, journeys and every other mechanism
serve that purpose.

| Term | Definition |
|---|---|
| **Predefined rule set** | The platform's built-in business logic for an area (offers, campaigns, compensation, incentives, timing, consent). The default operating mode. |
| **Advanced mode** | The seller's own business decisions replacing or extending a predefined rule set — percentages, vouchers, freebies, compensation, timing. Switched on per area; the seller owns the outcome. Never lowers a legal or consent floor (D13). |
| **Transparency rule** | Every communication states every rule that applies to it: limits, first-come-first-served, expiry, compensation if available, reference price. No hidden information (D14). |
| **Seller** | A web shop that uses the platform; the tenant. Owns products, orders, settings, templates overrides. |
| **Buyer** | A person who has bought from at least one seller and has an identity on the platform. One buyer, many sellers. |
| **Relationship** | The seller–buyer pair: history, segment, consents, thread. The unit of the system. |
| **Thread** | The single timeline of every touch between a seller and a buyer on every channel: messages, offers, deliveries, events. |
| **Offer** | A proposal from a seller to one buyer for one product with a price, a reason, one or more channels, and a lifecycle. Every campaign and list fans out into offers. |
| **Reason** | The human-readable justification attached to every offer. Written by the engine (`reason_engine`), optionally edited by the seller (`reason_seller`). The buyer sees the seller's edit when present. |
| **Recommendation** | An engine-scored product for one relationship, not yet sent. Sending converts it into an offer and removes it. |
| **Relevance** | The engine's per-product set of buyers for whom the product is relevant, with a reason each. Used by campaigns and lists. |
| **Campaign** | A one-product flash offer sent to every relevant buyer, with time and quantity limits (total and per buyer). |
| **Automation** (recurring list) | A scheduled per-buyer offer list: many products, a frequency, channels; each buyer receives only the products relevant to them. |
| **Template** | A platform-provided predefined rule set for an area of business logic or a user journey, with a legal floor where applicable. A seller runs it as predefined or in advanced mode (D13). |
| **Override** | A seller's modification or replacement of a template, versioned. |
| **Journey** | A recommended sequence of messages over time (e.g. order confirmed → t+0 complementary → 24–48 h upgrade → run-out reminder). A template kind. |
| **Hand-off** | The act of taking an accepted offer to the seller's own checkout with the price locked (D1). |
| **Delivery** | One send of one message or offer on one channel, with a status. |
| **Coupon** | A single-use code mapped one-to-one to an offer; redeeming it on any channel closes the offer everywhere (D6). |
| **Market** | A country-level configuration: legal basis, retention, currency, locale (D8). |
| **Consent scope** | Whether a buyer's consent and frequency cap are counted per seller or across the whole inbox in marketplace mode (D11). |
| **Holdout** | A randomly assigned share of a campaign's or automation's audience that receives nothing, used to measure incremental effect. |
| **Frequency cap** | The maximum number of marketing messages a buyer receives per channel per window. |
| **Segment** | A coarse class of relationship: new, returning, loyal (derived from order count and tenure). |
| **Print job** | The generation and optional printing and posting of a postal letter for an offer (D9). |
| **Compensation** | A goodwill gesture attached to a sold-out notice: preset from a menu or freely chosen (D10). |

## 2. Enumerations

| Enum | Values | Notes |
|---|---|---|
| `OfferKind` | `standard`, `flash`, `list_item`, `reorder`, `reminder`, `progress`, `surprise`, `back_in_stock`, `price_drop`, `birthday`, `sold_out_notice` | The first three exist in the prototype; the rest are decided message types from the research. |
| `OfferStatus` | `draft`, `pending`, `accepted`, `declined`, `expired`, `sold_out`, `redeemed`, `withdrawn` | `accepted`, `declined`, `expired`, `sold_out`, `redeemed`, `withdrawn` are terminal. |
| `Channel` | `chat`, `email`, `mailing`, `newsletter`, `rcs`, `whatsapp` | Release 1: the first four (D20); `whatsapp` then `rcs` in Release 2. |
| `Frequency` | `weekly`, `biweekly`, `monthly`, `event` | `event` = trigger-driven journey step. |
| `DiscountMode` | `steps`, `free` | D5. Seller setting. |
| `InboxMode` | `marketplace`, `per_seller` | D3. Seller setting. |
| `ConsentScope` | `per_seller`, `inbox` | D11. Seller setting, applies in marketplace mode. |
| `PrintMode` | `platform_service`, `seller` | D9. Seller setting. |
| `CompensationMode` | `preset`, `free` | D10. Seller setting. |
| `CompensationKind` | `voucher`, `free_delivery`, `priority_next_campaign`, `custom` | D10. |
| `LegalBasis` | `legitimate_interest`, `consent` | D8. Per market and channel. |
| `TemplateKind` | `offer`, `campaign`, `list`, `journey`, `sold_out`, `compensation`, `timing`, `consent`, `discount` | D10. |
| `OperatingMode` | `predefined`, `advanced` | D10, D13. `predefined` follows the platform rule set; `advanced` applies the seller's own values, above the legal floor. |
| `DeliveryStatus` | `queued`, `sent`, `delivered`, `opened`, `clicked`, `failed`, `bounced`, `printed`, `posted` | The last two are for `mailing`. |
| `Segment` | `new`, `returning`, `loyal` | new: 1 order; returning: 2–4; loyal: ≥5 or tenure ≥ 24 months with ≥3 orders. |
| `ReasonSource` | `engine`, `seller` | D4. |
| `Role` | `seller_admin`, `seller_agent`, `buyer`, `platform_ops` | |

## 3. Canonical entities and ownership

"Owner" is the system of record. The shop connector mirrors the seller's shop data; the
platform never edits it.

| Entity | Key fields | Owner |
|---|---|---|
| `Seller` | id, name, tagline, market_code, settings (§4) | Platform |
| (physical) | Entities are MongoDB collections with Mongoose schemas, `seller_id` on every tenant-scoped document, `version` for optimistic concurrency, and an append-only `offer_events` collection (D26). The tables in `technical-design.html` §1 are the logical model; §1b gives the collection mapping. | |
| `Buyer` | id, email, phone?, postal_address?, locale, birthday? | Platform (identity), buyer (profile edits) |
| `Relationship` | seller_id, buyer_id, segment, order_count, first_order_at, last_order_at, consents[], frequency_pref, holdout_bucket | Platform (derived from orders + buyer choices) |
| `Product` | id, seller_id, external_id, name, price, currency, category, consumable: bool, replenish_days?, stock? | Shop (via connector) |
| `Order` | id, relationship_id, external_id, lines[{product_id, qty, price}], ordered_at, source: shop\|handoff | Shop (via connector) |
| `Relevance` | product_id, buyer_id, score, reason_code, reason_engine, computed_at, model_version | Decision engine |
| `Recommendation` | id, relationship_id, product_id, pct_suggested, reason_code, reason_engine, state: available\|sent | Decision engine (state by platform) |
| `Offer` | id, relationship_id, product_id, kind, orig, pct, price, reason_engine, reason_seller?, reason_source, channels[], status, limit_hours?, limit_qty_per_buyer?, expires_at?, sent_at, responded_at?, campaign_id?, automation_run_id?, template_id?, override_version?, holdout: bool, checkout_url?, order_ref? | Platform |
| `OfferEvent` | id, offer_id, type, at, actor, payload | Platform (append-only) |
| `Campaign` | id, seller_id, product_id, pct, limit_hours, limit_qty_total, limit_qty_per_buyer, channels[], sent_at, sold_out_at?, compensation? | Platform |
| `Automation` | id, seller_id, title, frequency, channels[], product_ids[], next_run_at, state, discount_rule_override? | Platform |
| `AutomationRun` | id, automation_id, ran_at, content_freeze, per_buyer_counts | Platform |
| `Template` | id, kind, version, defaults, legal: bool, floor (the minimum a seller in advanced mode must keep) | Platform |
| `SellerOverride` | seller_id, template_id, mode: OperatingMode, values, version, changed_by, changed_at | Seller |
| `Delivery` | id, offer_id\|message_id, channel, status, provider_ref?, print_job_id?, at | Platform |
| `Coupon` | code, offer_id, single_use: true, redeemed_at?, redeemed_channel? | Platform |
| `Consent` | buyer_id, seller_id?, scope, channel, basis, granted_at, withdrawn_at?, source | Platform (buyer's choice) |
| `Market` | code, legal_basis_by_channel, retention_days, soft_opt_in: bool, currency, locale, reference_price_days: 30 | Platform |
| `PrintJob` | id, offer_id, mode, pdf_ref, status, partner_ref?, posted_at? | Platform / print partner |
| `Message` | id, relationship_id, from_role, kind: text\|event\|offer_ref, body, channel?, at | Platform |

## 4. Seller settings registry

| Key | Type / values | Default | Decision |
|---|---|---|---|
| `inbox_mode` | `InboxMode` | `per_seller` | D3 |
| `discount_mode` | `DiscountMode` | `steps` | D5 |
| `discount_steps` | int[] | `[10,15,20,25]` | D5 |
| `discount_guardrails` | {floor_pct, max_pct, margin_floor_pct, per_segment_max{}} | {0, 30, 10, {}} | D5 |
| `newsletter_discount_rule` | {mode: recommendation_pct\|fixed, fixed_pct} | recommendation_pct, 10 | D7 |
| `print_mode` | `PrintMode` | `seller` | D9, D15 (Release 1: `seller` only) |
| `consent_scope` | `ConsentScope` | `per_seller` | D11 |
| `compensation_mode` | `CompensationMode` | `preset` | D10 |
| `compensation_presets` | CompensationKind[] | `[voucher, free_delivery, priority_next_campaign]` | D10 |
| `frequency_cap` | {email_per_30d, chat_per_7d, mailing_per_90d, rcs_per_7d} | {4, 3, 1, 1} | research §6 |
| `holdout_pct` | int 0–20 | 10 | research §4, D21 |
| `holdout_mode` | `per_campaign` \| `pooled` | `pooled` under 1 000 active relationships, else `per_campaign` | D21 |
| `min_outcomes_for_learning` | int | 2000 | D21 |
| `early_access_minutes` | int | 60 | D22 |
| `flash_defaults` | {pct, limit_hours, limit_qty_total, limit_qty_per_buyer, channels[]} | {15, 24, 20, 1, [chat,email]} | prototype + D2 |
| `list_defaults` | {frequency, channels[]} | {biweekly, [email]} | prototype |
| `reason_editable` | bool | true | D4 |
| `advanced_mode` | {offers, campaigns, lists, compensation, incentives, timing, consent: bool} | all false | D13; per area; `consent` may only tighten |
| `checkout_handoff` | {mode: signed_link\|cart_token, price_lock_minutes} | {signed_link, 60} | D1 |

Buyer-level preferences: `frequency_pref` (per seller or inbox per `consent_scope`),
`channels_allowed[]`, `muted_categories[]`, `locale`.

## 5. Decision register

| ID | Decision (2026-09-17) | Where applied |
|---|---|---|
| D1 | Accept hands off to the shop's checkout with the price locked | rules R7, TD §4 A6 |
| D2 | Flash quantity limited both per campaign and per buyer; at sold-out inform buyers who received it, optional compensation | R9–R11 |
| D3 | Marketplace inbox or per-seller app, seller setting | `inbox_mode` |
| D4 | Reason written by the engine, editable by the seller, both kept | R3 |
| D5 | Discount authority: fixed steps or free entry, both under guardrails, seller setting | R4 |
| D6 | Postal coupon single-use, mapped one-to-one to the online offer | R13 |
| D7 | Newsletter discount: seller default rule, overridable per list | R12 |
| D8 | Legal basis per market: legitimate interest with soft opt-in where allowed, consent elsewhere; retention per market | R15 |
| D9 | Platform generates printable content; printing and posting by a DiscountDirect service or by the seller | R14 |
| D10 | Compensation preset or free choice; in general the platform provides business-logic templates and journey recommendations that sellers follow, modify or overwrite (owner's words; terminology since D13: predefined rule set / advanced mode) | R1, R11 |
| D11 | Consent and frequency cap per seller or across the inbox, a setting | R16 |
| D12 | The platform is a retention system: avoid churn, raise customer lifetime value | mission, metrics §7 |
| D13 | Legal and consent defaults belong to the platform; the seller keeps additional options within limits. Incentives (percentages, vouchers, freebies, compensation) come from predefined rule sets or from the seller in **advanced mode**; "advanced mode" is the system-wide term for the seller's own business decisions | R1, `advanced_mode`, `OperatingMode` |
| D14 | Everything is clearly communicated to the buyer: compensation if available, first-come-first-served, limited quantity and every other rule appear on every communication | R21 |
| D15 | Print partner (recommended, applied) | Release 1 ships the **seller print mode** only (PDF download, "posted" action). The platform print-and-post service follows in Release 1.1 through an API-first provider that posts through the domestic postal network; **Pingen** is the first integration candidate, behind the `PrintPartner` interface so it can be swapped | R14, DD-054 |
| D16 | Technology stack (recommended, applied) | superseded by D26 | — |
| D17 | Release 1 market (recommended, applied) | **Hungary only**: `hu-HU`, HUF, the HU market row seeded; further markets are configuration, not code | `markets` |
| D18 | Connector order (recommended, applied) | **Shoprenter and UNAS first** (the leading Hungarian rental platforms), then WooCommerce, then Shopify | DD-071–074 |
| D19 | Providers and hosting (recommended, applied) | superseded by D26: **Resend** for e-mail, **Vercel** hosting, **Vercel Blob** object storage | architecture §10 |
| D20 | Release 1 channels (recommended, applied) | **chat, e-mail, postal letter (seller print mode), newsletter**. RCS and WhatsApp in Release 2, **WhatsApp first** in Hungary because it does not depend on carrier RCS support | `Channel` |
| D21 | Measurement defaults (recommended, applied) | Holdout **10 %**; sellers with fewer than 1 000 active relationships use one **pooled seller-level holdout** instead of per-campaign ones; learned discount depth is enabled only after **2 000 offers with outcomes** | R19, `holdout_pct`, `min_outcomes_for_learning` |
| D22 | Membership unit and perks (recommended, applied) | **Per seller** in Release 1; default perks **free delivery** and **early access 60 minutes** before a flash campaign; samples and gifts in advanced mode; a cross-seller wallet in Release 3 | DD-086, `early_access_minutes` |
| D23 | Salutation (recommended, applied) | Neutral formal salutation **"Tisztelt {teljes név}!"** on letters and e-mails; no inference of gender from names | BL §3.7, DD-052 |
| D24 | Reason experiments (recommended, applied) | The reason is always present (D14); experiments compare **engine wording against seller wording** only, never reason against no reason | DD-091 |
| D25 | Release 1 scope (recommended, applied) | The issue list in `implementation-plan.html` §7; everything else is Release 1.1 or later | plan §7 |
| D26 | Stack: extend the existing implementation, do not rewrite (product owner, 2026-09-17) | The product already has a working spine: **Next.js 15 App Router on Vercel (Node 24), MongoDB Atlas with Mongoose transactions, DoneIsBetter SSO (local password routes fail closed), Resend for outbound and inbound e-mail with webhook verification and unsubscribe, Vercel Cron with a durable outbox, Socket.IO realtime with a durable HTTP fallback, the SovereignSquad GDS with Mantine under it.** Target: add **Upstash Redis** (frequency caps, rate limits, flash counters, idempotency locks, throttling, worker coordination) and **Vercel Blob** (letters, exports, PDFs, audit snapshots); keep Resend; realtime is a convenience layer, the durable MongoDB event log is authoritative; add a **reporting read model** (MongoDB materialised aggregates, or a Postgres projection) before any primary-database change. The greenfield stack of the first proposal (Fastify, Vite, PostgreSQL, BullMQ, SES) is withdrawn. | ADR-14; architecture §3, §10; TD §1b, §3 |

### Open questions

None for Release 1. O1 → D13, O2 → D15, O3 → D14, A1 → D16 → D26. D15–D25 were
recommended and applied on 2026-09-17 so that Release 1 is fully specified; the product
owner may overrule any of them, in which case this register changes first.

**Verification note (D26).** The implementation repository the owner cites
(`/Users/Shared/Projects/discountdirect`: `package.json`, `src/lib/database-core.ts`,
`docs/architecture.md`) was not reachable from the machine that maintains these
documents on 2026-09-17, so the stack facts in D26 are recorded as stated by the owner.
Issue DD-000 verifies them against the code before any other Release 1 work starts.

## 6. Rules register

| ID | Rule | Formula / condition | Source |
|---|---|---|---|
| R1 | Every business rule below is a predefined rule set; in advanced mode the seller's values apply, never below a legal or consent floor | `effective = advanced ? max(values, template.floor) : template.defaults`; `template.legal ⇒ values ≥ floor` | D10, D13 |
| R2 | An offer is made once: sending removes the recommendation | `Recommendation.state := sent` | BL §3.1 |
| R3 | Buyer sees `reason_seller ?? reason_engine`; audit keeps both | | D4 |
| R4 | Discount validity | `steps`: `pct ∈ discount_steps`; `free`: `floor ≤ pct ≤ max`; both: `price ≥ cost × (1 + margin_floor)` when cost known; `pct ≤ per_segment_max[segment]` | D5 |
| R5 | Price | `price = round(orig × (1 − pct/100))` in the market currency's minor unit | BL §3.1 |
| R6 | Only the buyer, only on seller-sent offers, only while pending, may accept or decline | | BL §3.3 |
| R7 | Accept → hand-off | `checkout_url = sign({offer_id, price, expires: now + price_lock_minutes})`; `order_ref` set by write-back; offer stays `accepted` until write-back or lock expiry | D1 |
| R8 | Expiry | `flash`: `expires_at = sent_at + limit_hours`; a pending offer past `expires_at` becomes `expired` | BL §3.5 |
| R9 | Campaign fan-out | one pending offer per buyer in `Relevance(product)`, minus holdout, minus buyers blocked by R15/R16 | BL §3.5 |
| R10 | Quantity enforcement | accept succeeds only if `campaign.accepted_total < limit_qty_total` and `buyer_accepted < limit_qty_per_buyer`, checked atomically | D2 |
| R11 | Sold-out | when `accepted_total = limit_qty_total`: campaign `sold_out_at := now`; every other pending offer → `sold_out`; a `sold_out_notice` message is sent to those buyers with the campaign's compensation if any | D2, D10 |
| R12 | List discount | `pct = automation.discount_rule_override ?? seller.newsletter_discount_rule` applied per item; `recommendation_pct` mode uses the buyer's matching recommendation else `fixed_pct` | D7 |
| R13 | Coupon | one code per `mailing` offer; `redeem(code)` closes the offer on every channel; a second redeem is refused | D6 |
| R14 | Print | every `mailing` delivery produces a PDF; `print_mode = platform_service` creates a partner print job, `seller` exposes the PDF for download; either way `Delivery.status` advances to `printed`/`posted` | D9 |
| R15 | Legal basis | a marketing send on channel `c` in market `m` is allowed iff `basis(m,c) = legitimate_interest ∧ soft_opt_in ∧ relationship.order_count ≥ 1 ∧ ¬objected` or `basis(m,c) = consent ∧ consent(buyer, seller\|inbox, c).granted` | D8 |
| R16 | Frequency cap | counted per `(buyer, seller, channel)` if `consent_scope = per_seller`, else per `(buyer, channel)`; a send that would exceed the cap is deferred to the next window, never dropped silently, and logged | D11, research §6 |
| R17 | Per-buyer list split | `items(buyer) = {p ∈ automation.product_ids : buyer ∈ Relevance(p)}`; buyers with `items = ∅` are skipped | BL §3.6 |
| R18 | Reference price | any struck-through price must be the lowest price of the previous `Market.reference_price_days` (30) | research §5 |
| R19 | Holdout | `holdout = hash(buyer_id, campaign_id\|automation_id) mod 100 < holdout_pct`; holdout buyers get no offer and are excluded from R16 counting | research §4 |
| R21 | Transparency | every rendering of an offer (chat card, e-mail, letter, newsletter, sold-out notice) includes a rules block listing: expiry, quantity limits (total and per buyer), first-come-first-served, compensation if configured, reference price basis, the reason | D14 |
| R20 | Consumable replenishment | `next_runout = last_order_at + median(interval of last n orders of the product, n ≥ 2) ?? product.replenish_days`; reminder at `next_runout − 6 days` | research §2.2 |

## 7. Metric definitions

| Metric | Definition |
|---|---|
| Incremental contribution margin | `Σ margin(orders, treated) / |treated| − Σ margin(orders, holdout) / |holdout|`, per campaign or automation, over the attribution window (14 days) |
| Take rate | `accepted / (pending + accepted + declined + expired + sold_out)` per kind, moment and channel |
| No-discount repeat share | `orders from reorder/reminder offers with pct = 0 / all orders attributed to the platform` |
| Membership share | `revenue from buyers with an active membership / revenue from all platform buyers` |
| Unsubscribe rate | `withdrawn consents / deliveries` per channel per 30 days |
| Frequency | `deliveries per buyer per channel per 30 days` (distribution, not mean) |
| Sold-out disappointment | `sold_out offers / campaign offers`; target under 20 % |
| Churn (retention mission, D12) | `relationships with no order in 2 × their median interval (or 180 days) / active relationships`, monthly |
| Customer lifetime value | `Σ contribution margin per relationship over 24 months`, cohort by first order month; the platform's north-star delta is treated minus holdout |
| Hand-off completion | `orders written back / accepted offers` within `price_lock_minutes` |

## 8. Document map

| Document | Purpose | Changes when |
|---|---|---|
| `ssot.html` | definitions, enums, settings, decisions, rules, metrics | any definition changes |
| `business-logic.html` | rules as implemented in the prototype and as decided | a rule or decision changes |
| `architecture.html` | system context, containers, flows, NFRs, stack, ADRs | an architectural decision changes |
| `technical-design.html` | schema, state machines, API, algorithms, integrations | a design detail changes |
| `implementation-plan.html` | milestones, issues, DoD | scope or sequencing changes |
| `executive.html`, `research.html` | why and what the evidence says | new evidence |
