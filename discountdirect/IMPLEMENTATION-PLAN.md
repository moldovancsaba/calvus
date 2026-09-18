# DiscountDirect — implementation plan

Version 1.1 · 2026-09-18. Milestones, epics and issues for milestone 1 (Foundation),
each issue with story, scope, design reference, pseudo code where the logic is not
trivial, acceptance criteria, Definition of Done, dependencies and what blocks it.
Milestones 2 and 3 are outlined at epic level. Definitions per `ssot.html`; design per
`technical-design.html` (TD); rules per `business-logic.html` (BL).

## Current implementation status

This is a target backlog, not evidence that every issue is open. The implementation
baseline verified through commit `0eb5d55` shows these groups:

| Status | Capabilities |
|---|---|
| Implemented | SSO roles and tenant guards; fixtures; markets/settings; product and purchase imports; recommendations and v1 segments; conversations with Socket.IO plus durable replay; personal offers; flash campaigns and MongoDB reservations; automations and buyer lists; durable delivery outbox; Resend outbound/inbound and suppressions; consent/privacy; frequency caps; coupons; pricing guardrails; 30-day reference-price evidence; campaign holdout and purchase-rate reporting |
| Foundation | Upstash client/key/TTL/Lua policy beyond the live frequency-cap counter; Vercel Blob private-key and signed-read contracts |
| Partial | Campaign reporting is on demand and not an incremental-margin read model; buyer/seller workflows exist but the marketplace inbox, reason editing and broader lifecycle remain incomplete |
| Planned | Checkout hand-off and connectors; postal PDF/partner flow; template override library and richer journeys; membership perks; WhatsApp/RCS; generalized Redis counters/locks; Blob-backed artifacts; materialized reporting and incremental margin |

The detailed issues below retain their acceptance criteria as target contracts. Where
an issue names a superseded technology or route shape, this status section plus D26–D27
and the technical design control implementation.

## 0. Conventions

- Issue IDs `DD-nnn`; labels `epic:<name>`, `area:<module>`, `blocked:<O-id>`.
- Estimates: **S** ≤ 2 days, **M** ≤ 5 days, **L** ≤ 10 days for one engineer.
- Every issue is a vertical slice where possible: schema + API + UI + tests + docs.
- Blocked issues are built up to the assumption in SSOT §5 and carry the `blocked:`
  label so the assumption is revisited before release.

## 1. Global Definition of Done

An issue is done only when all of the following are true:

1. Code merged to `main` behind a feature flag if user-visible and incomplete.
2. Unit tests for every rule the issue touches (table-driven, named by rule id).
3. Contract or integration test where an external interface is involved.
4. Tenant scoping verified for every new collection (a query without tenant context
   throws; a cross-tenant read test fails).
5. No PII in logs; new events registered in the observability catalogue (TD §7).
6. `ssot.html` updated if a term, enum, setting, rule or metric changed; TD updated
   if a schema, endpoint or algorithm changed; this plan updated if scope changed.
7. Acceptance criteria demonstrated on staging with the seed fixtures (TD §8).
8. Accessibility: 44 px targets, keyboard path, contrast on both console and buyer app.
9. Reviewed by one other engineer; no attribution metadata of any kind in commits.

## 2. Milestones

| Milestone | Outcome | Epics |
|---|---|---|
| M0 Foundations | repo, environments, schema, auth, tenancy, seed data | E0 |
| M1 Thread and offers | seller inbox, thread, recommendations (rules), personalised offer, accept/decline, reasons | E1, E2 |
| M2 Campaigns and lists | flash campaign with both limits and sold-out, recurring lists with scheduler | E3, E4 |
| M3 Channels | e-mail adapter, postal letter PDF and print modes, coupons, delivery statuses | E5 |
| M4 Consent and compliance | markets, legal basis, consents, objections, frequency caps, reference price | E6 |
| M5 Hand-off and orders | signed checkout hand-off, connectors (Shopify, WooCommerce, UNAS, Shoprenter), write-back | E7 |
| M6 Templates and journeys | template library, overrides, first journeys (run-out reminder, progress card, back-in-stock, birthday) | E8 |
| M7 Measurement | holdout, events, rollups, dashboards | E9 |
| M8 Buyer app | per-seller thread, marketplace inbox, usuals, preference centre | E10 |

Critical path: E0 → E1 → E2 → E7 (hand-off is the revenue path) with E6 in parallel from
M1, because no send may go out without `may_send`.

## 3. Issues

### E0 Foundations (M0) — on the existing implementation (D26)

**DD-000 Maintain the implementation baseline inventory** · S · area:platform
Story: as the team I keep the Release 1 plan grounded in the real DiscountDirect
repository instead of a greenfield assumption.
Scope: publish and maintain an inventory page in the implementation repo based on the
verified 2026-09-17 baseline: `package.json`, `src/lib/database-core.ts`, `vercel.json`,
`docs/architecture.md`, App Router routes, Mongoose models, domain services, Resend and
SSO integrations, cron jobs and the Socket.IO fallback. Every material stack or model
change updates SSOT D26 and TD §1b in the same pull request.
Acceptance: the inventory exists in the implementation repo; D26 and TD §1b match the
code; later issues' "existing" notes are corrected whenever implementation reality
changes.

**DD-001 Environments and CI on the existing repo** · S · area:platform · depends DD-000
Scope: Vercel preview/staging/production environments, MongoDB Atlas EU cluster per
environment, lint/type/test pipeline, secrets in Vercel, EU region confirmed.
Acceptance: a change merged to `main` deploys to staging automatically; production
needs a promotion.

**DD-002 Models v1, tenant plugin, event collections** · M · area:data · depends DD-001
Scope: TD §1 logical model realised as Mongoose schemas per §1b; the tenant plugin that
injects `seller_id` and throws without a context; insert-only `offer_events` and
`consent_events`; `outbox`; indexes; Blob keys on `print_jobs`.
Pseudo code (request wrapper):
```
withTenant(ctx.seller_id, () => handler())   // plugin reads the async-local tenant context
```
Acceptance: a query without a tenant context throws; a cross-tenant read returns
nothing; an update on an event document is refused by the model and by the database
role in production.

**DD-003 Roles on top of DoneIsBetter SSO** · M · area:identity · depends DD-002
Scope: SSO session → platform roles per SSOT §2 (`seller_admin`, `seller_agent`,
`buyer`, `platform_ops`); buyer identity linking across sellers; local password routes
stay fail-closed.
Acceptance: role matrix test over every Server Action and Route Handler; a password
route returns a hard refusal.

**DD-006 Upstash Redis** · S · area:platform · depends DD-001
Scope: client, key conventions (`cap:`, `camp:`, `lock:`, `rate:`), Lua script loading,
TTL policy, reconciliation job hook.
Acceptance: A5 and A8 scripts run against a staging Redis; a lost key is rebuilt from
MongoDB.

**DD-007 Vercel Blob** · S · area:platform · depends DD-001
Scope: private store, signed read URLs with expiry, key conventions per seller, retention
by market.
Acceptance: a letter PDF is written and read back through a signed URL; a cross-tenant
key is refused.

**DD-008 Rotate the Resend webhook secret and verify signatures** · S · area:security · depends DD-001
Scope: rotate the exposed signing secret, store it only in Vercel secrets, verify every
inbound Resend webhook, add replay protection by event id.
Acceptance: a webhook with the old secret is refused; a replayed event is ignored.

**DD-004 Seed fixtures from the prototype** · S · area:data · depends DD-002
Scope: ElektroHome, three buyers, catalogue, orders, relevance, recommendations exactly
as in `index.html`; loader script for dev/staging.
Acceptance: the seller inbox on staging shows Anna, Gábor, Réka with the same pending
counts as the prototype.

**DD-005 Markets table and seller settings registry** · S · area:platform · depends DD-002
Scope: `markets` with HU seeded (`legal_basis_by_channel`, `soft_opt_in`, retention),
settings JSON schema per SSOT §4 with validation on `PATCH /settings`.
Acceptance: invalid keys and out-of-range values rejected with `validation`; defaults
applied when absent.

### E1 Thread and recommendations (M1)

**DD-010 Seller inbox and thread** · M · area:relationships · depends DD-003, DD-004
Story: as a seller agent I see one row per buyer with last message and pending count,
and open a thread showing history, recommendations and the timeline (BL §3.2, §3.4).
Acceptance: badge equals pending offers; timeline shows chat bubbles for chat offers and
full-width events for other channels; 390 px and 1440 px layouts pass the sweep.

**DD-011 Chat messages** · S · area:relationships · depends DD-010
Scope: durable conversation messages for both roles with real timestamps; Socket.IO
signals the other side and the durable HTTP timeline/replay remains authoritative.
Acceptance: message appears on the other role's open thread within 1 s on staging.

**DD-012 Rules-based decision engine v1** · L · area:decision · depends DD-004
Story: recommendations and relevance come from an engine, not fixtures.
Scope: TD A2 and A3 as a replaceable TypeScript rules module inside the Next.js app;
reason codes `REPLENISHMENT`, `COMPATIBLE_ACCESSORY`, `SAME_CATEGORY` with localised
texts and a stamped `model_version`. A separate service is a later scaling option.
Pseudo code: TD A2, A3.
Acceptance: on the seed data Anna's HEPA filter is `REPLENISH` with a run-out date;
Gábor's dashcam is `ACCESSORY`; a product with no basis is absent; reason texts are
`hu-HU`.
DoD: engine interface documented so a model-based engine can replace it (ADR-8).

**DD-013 Segment derivation** · S · area:relationships · depends DD-012
Scope: `new` / `returning` / `loyal` per SSOT §2 on every order ingest.
Acceptance: table-driven test over order counts and tenure.

### E2 Personalised offers (M1)

**DD-020 Send a personalised offer** · M · area:offers · depends DD-010, DD-012, DD-060
Story: as a seller agent I send one recommendation as an offer on one channel with an
optional edited reason (BL §3.1, D4).
Pseudo code:
```
POST /relationships/{id}/offers:
  rec = load(recommendation_id); assert rec.state == 'available'
  validate_pct(...)                                  # TD A11
  d = may_send(buyer, seller, channel)               # TD A8; blocked -> 409 consent_blocked, deferred -> 202 with time
  offer = insert(kind='standard', reason_engine=rec.reason_engine, reason_seller=body.reason_seller, price=R5)
  rec.state = 'sent'; insert offer_events('sent'); outbox('offer.send')
```
Acceptance: recommendation disappears; offer pending in the thread; a second send of the
same recommendation returns `not_pending`; the buyer sees the seller's reason when
edited, the audit shows both.

**DD-021 Accept and decline** · M · area:offers · depends DD-020
Story: as a buyer I accept or decline a pending offer; accepting takes me to checkout
(D1, BL §3.3).
Pseudo code: TD A5 (`accept`, standard offers skip the campaign counters) and A6.
Acceptance: only the buyer, only pending; `accepted` returns a hand-off URL valid for
`price_lock_minutes`; terminal states cannot change; events recorded.

**DD-022 Pricing guardrails, both modes** · M · area:pricing · depends DD-005
Scope: TD A11; `discount_mode` steps or free; per-segment maxima; margin floor when cost
is known; reference-price check R18 with `price_history`.
Acceptance: table-driven tests for every guardrail; a struck-through price above the
30-day low is refused with `guardrail:reference_price`.

**DD-023 Reason editing while pending** · S · area:offers · depends DD-020
Scope: `POST /offers/{id}/reason`, allowed while `pending` and when `reason_editable`.
Acceptance: buyer view updates; audit keeps the engine text and the edit history.

### E3 Flash campaigns (M2)

**DD-024 Transparency renderer: rules block on every communication** · M · area:offers · depends DD-020
Story: as a buyer I see every rule that applies to an offer — expiry, total and per-buyer
quantity, first-come-first-served, compensation if available, reference-price basis and
the reason — on the chat card, in the e-mail, on the letter, in the newsletter and in
the sold-out notice (D14).
Pseudo code: TD A13.
Acceptance: a template test fails for any channel rendering that omits the block; the
flash preview in the console shows the same block the buyer will see.

**DD-030 Campaign preview and targets** · S · area:campaigns · depends DD-012, DD-060, DD-090
Scope: `POST /campaigns/preview` → relevant buyers, blocked (consent), deferred (cap),
holdout count, expected sends.
Acceptance: preview numbers equal the fan-out result on send.

**DD-031 Fan-out worker** · M · area:campaigns · depends DD-030
Pseudo code: TD A5 fan-out; batches of 500; idempotent by `(campaign_id, buyer_id)`.
Acceptance: 50 000 targets fan out under 10 minutes on staging; re-running the job
creates no duplicates.

**DD-032 Atomic accept with both limits** · M · area:campaigns · depends DD-031, DD-021
Pseudo code: TD A5 Lua script and transaction; `limit_qty_total` and
`limit_qty_per_buyer` (D2).
Acceptance: 1 000 concurrent accepts on a 20-unit campaign yield exactly 20 accepted;
a buyer with `limit_qty_per_buyer = 1` gets `per_buyer_limit` on the second accept;
Redis loss recovers from `campaigns.accepted_total`.

**DD-033 Expiry job** · S · area:campaigns · depends DD-031
Scope: pending flash offers past `expires_at` → `expired` every minute (R8).
Acceptance: the buyer card shows "lejárt"; no accept after expiry.

**DD-034 Sold-out notice with compensation** · M · area:campaigns · depends DD-032, DD-080
Story: when a campaign sells out, buyers who still had it pending are told, with the
campaign's compensation if configured (D2, D10).
Pseudo code: TD A5 `sold_out`; compensation resolved from `compensation_mode`:
`preset` → chosen from `compensation_presets` at campaign creation; advanced mode →
the seller's own compensation at creation.
Acceptance: every other pending offer becomes `sold_out` within 1 minute; each such
buyer gets one notice; the compensation appears as its own message with a redeemable
element (voucher code, free-delivery flag, priority flag on the next campaign); when
configured in advance it was already visible on the flash card (DD-024, D14).

### E4 Recurring lists (M2)

**DD-040 Automation CRUD and per-buyer split preview** · M · area:automations · depends DD-012
Pseudo code: TD A4.
Acceptance: preview matches the prototype's split on the seed data; buyers with no
matching product are absent.

**DD-041 Scheduler and runs** · M · area:automations · depends DD-040, DD-060, DD-090
Pseudo code: TD A10; content freeze per run; `next_run_at` from frequency; pause/resume.
Acceptance: a biweekly list runs on the right dates in `Europe/Budapest`; a paused list
does not run; a run is idempotent when retried.

**DD-042 List discount rule and override** · S · area:automations · depends DD-040, DD-022
Scope: R12 (D7): seller default rule, per-list override.
Acceptance: table-driven tests over `recommendation_pct` and `fixed` modes.

### E5 Channels (M3)

**DD-050 Delivery model and outbox relay** · M · area:delivery · depends DD-002, DD-006
Scope: `deliveries`, outbox relay through Vercel Cron workers with Redis locks,
idempotent consumers, dead-letter collection and alert; Socket.IO notifies open threads
but the outbox is the record.
Acceptance: a failed adapter call retries with backoff and lands in the dead-letter
queue after 5 attempts; the thread shows the failure.

**DD-051 E-mail adapter on Resend** · M · area:delivery · depends DD-050, DD-008
Scope: TD §5 `ChannelAdapter` over the existing Resend integration (outbound, inbound
reply-to-thread, unsubscribe); templates per BL §3.7 (subject,
greeting, card, CTA deep link, reply-to-thread, footer with reason and unsubscribe);
status webhooks (`delivered`, `opened`, `clicked`, `bounced`).
Acceptance: staging send to a sandbox inbox renders per the prototype's e-mail tab;
statuses appear in the thread.

**DD-052 Postal letter PDF** · M · area:delivery · depends DD-050
Scope: letter per BL §3.7 with the neutral salutation "Tisztelt {teljes név}!" (D23), locale,
coupon code (DD-053); PDF stored in the object store.
Acceptance: PDF matches the prototype's letter tab; address block validated.

**DD-053 Coupons, single-use, mapped to the offer** · S · area:delivery · depends DD-020
Pseudo code: TD A7.
Acceptance: redeem once succeeds and closes the offer everywhere; a second redeem
returns `already_redeemed`; store-staff page works on a phone.

**DD-054 Print modes: platform service or seller** · M · area:delivery · depends DD-052
Scope: `print_mode` (D9); `platform_service` → `PrintPartner.submit` and status
ingestion; `seller` → download in the console and a "posted" action.
Acceptance: both modes advance the delivery to `printed` / `posted`; partner failures
surface in the thread. Release 1 ships the `seller` mode; the `platform_service` mode
integrates Pingen behind `PrintPartner` in Release 1.1 (D15); its commercial terms come
from the predefined rule set or advanced mode (D13).

**DD-055 Newsletter renderer** · S · area:delivery · depends DD-041, DD-051
Scope: per-buyer newsletter per BL §3.7 with the list's items, reasons, discounts,
frequency banner, footer.
Acceptance: matches the prototype's newsletter tab for Anna on the seed data.

### E6 Consent and compliance (M4, starts in M1)

**DD-060 `may_send`: legal basis per market and channel** · M · area:consent · depends DD-005
Pseudo code: TD A8 (basis part); R15 (D8).
Acceptance: table-driven tests over basis × soft opt-in × order count × consent ×
objection; no send path bypasses `may_send` (a lint rule or a test on every sender).

**DD-061 Consent records and preference centre API** · M · area:consent · depends DD-060
Scope: `consents`, `GET/PUT /me/preferences`, channels allowed, frequency preference,
muted categories; scope per `consent_scope` (D11).
Acceptance: a withdrawn consent blocks the next send; scope switch changes which
records apply.

**DD-062 Objection in one tap** · S · area:consent · depends DD-061
Scope: `POST /me/object` for a seller or the inbox; stops legitimate-interest marketing
immediately (Art. 21).
Acceptance: objection recorded with source; next `may_send` returns `blocked:objection`.

**DD-063 Frequency caps with scope** · M · area:consent · depends DD-060
Pseudo code: TD A8 (cap part); R16; per-seller or inbox counters (D11); deferral, never
silent drop.
Acceptance: the fifth e-mail in 30 days is deferred to the window boundary and logged;
switching `consent_scope` to `inbox` counts across sellers.

**DD-064 Reference price history** · S · area:pricing · depends DD-070
Scope: `price_history` fed by product sync; R18 check.
Acceptance: the 30-day low is computed correctly across sync gaps.

**DD-065 Retention and anonymisation job** · S · area:consent · depends DD-005
Scope: nightly job per `Market.retention_days`.
Acceptance: an inactive relationship past retention is anonymised; audit rows keep ids
only.

### E7 Hand-off and shop connectors (M5)

**DD-070 Connector interface and product/order sync** · M · area:connectors · depends DD-002
Scope: TD §5 `ShopConnector`; sync worker with watermark; webhook registration and
verification; `products`, `orders`, `order_lines`.
Acceptance: a contract test suite every connector must pass; sync is idempotent.

**DD-074 Shoprenter connector** · M · **DD-073 UNAS** · M · **DD-072 WooCommerce** · M ·
**DD-071 Shopify** · M — all depend on DD-070, built in this order (D18)
Acceptance: each passes DD-070's contract suite against a sandbox store; checkout link
carries the locked price (discount code or pre-built cart) and the `ref`.

**DD-075 Signed hand-off and price lock** · M · area:handoff · depends DD-021, DD-070
Pseudo code: TD A6.
Acceptance: `GET /handoff/{token}` verifies and redirects within 2 s p95; tampered or
expired tokens get 410; event `handoff_opened` recorded.

**DD-076 Order write-back** · M · area:handoff · depends DD-075
Pseudo code: TD A6 webhook branch; lock-expiry job.
Acceptance: an order with the `ref` sets `order_ref` and shows "order confirmed" in the
thread; an accepted offer without an order after the lock gets `handoff_not_completed`;
segments and counts recompute.

### E8 Templates and journeys (M6)

**DD-080 Predefined rule sets and advanced mode** · M · area:templates · depends DD-005
Pseudo code: TD A1; legal templates enforce their floor.
Scope: kinds per SSOT §2; versioning; `GET /templates`, `PUT /templates/{id}/override`
with `mode: predefined | advanced`; console UI with a per-area **Advanced mode** switch,
the seller's values next to the predefined ones and the legal floor shown; "advanced
mode" is the term used everywhere in the UI (D13).
Acceptance: effective values resolve per mode; an advanced value below a legal floor is
refused with `validation`; every offer stamps `template_id` and `override_version`.

**DD-081 Journey runner (event-driven automations)** · L · area:automations · depends DD-041, DD-080, DD-076
Scope: `Frequency = event`; triggers `order_confirmed`, `predicted_runout`,
`inactivity_days`, `birthday`; steps with delays; each step a message type.
Pseudo code:
```
on trigger(evt, relationship): for j in active journeys of seller with j.trigger == evt.type:
  schedule step 1 at now + j.steps[0].delay
run step: if may_send and not holdout: create offer(kind=step.kind, template=j) ; schedule next
```
Acceptance: order confirmed → t+0 complementary → 24–48 h upgrade → run-out reminder
fire on the seed data with fixed clocks.

**DD-082 Run-out reminder and one-tap reorder** · M · depends DD-012 (Release 1 uses a daily run-out job; DD-081 generalises it in Release 1.1)
Scope: `reorder` and `reminder` kinds with `pct = 0` by default; "my usuals" endpoint
(R20).
Acceptance: Anna gets a HEPA reminder six days before the predicted run-out; accepting
hands off with no discount.

**DD-083 Progress card with a head start** · M · depends DD-081
Scope: `progress` kind; counter per relationship; first stamp pre-filled; perk on
completion (free delivery flag for N days).
Acceptance: a buyer at 3 of 5 sees the card; the perk is applied at 5.

**DD-084 Back-in-stock and price-drop messages** · M · depends DD-070, DD-081
Scope: waiting list on sold-out flash items; stock webhook triggers `back_in_stock`;
`price_history` drop triggers `price_drop` for viewers/decliners.
Acceptance: a stock increase sends one message per waiting buyer, capped and consented.

**DD-085 Birthday message** · S · depends DD-081
Acceptance: fires once per year per relationship, only with a stored birthday and a
one-step reward.

**DD-086 Membership and tier** · L · depends DD-080, DD-083
Scope: named membership per seller (D22), tier from order count, default perks free
delivery and early access `early_access_minutes` (60) before flash campaigns, priority
answers; samples and gifts in advanced mode; join with one tap.
Acceptance: members receive flash campaigns `early_access_minutes` before others; tier
is visible to the buyer; leaving is one tap.

### E9 Measurement (M7)

**DD-090 Holdout assignment** · S · area:measurement · depends DD-002
Pseudo code: TD A9; SHA-256 bucket assignment with pooled or per-campaign scope (D21).
Acceptance: the same buyer is consistently held out within one campaign; distribution
within 1 point of `holdout_pct` over 100 000 buyers.

**DD-091 Event catalogue and metric rollups (reporting read model)** · M · depends DD-050
Scope: TD §7 events; nightly rollups per SSOT §7 into the `metric_rollups` read model as
MongoDB materialised aggregates; a documented path to a Postgres projection (Neon) if
analytics outgrow them (D26); attribution window 14 days.
Acceptance: incremental margin computed against the holdout on the seed data with
synthetic orders; take rate by kind and channel.

**DD-092 Seller dashboard** · M · depends DD-091
Acceptance: per campaign and automation: sends, take rate, incremental margin,
deferred/blocked counts, sold-out disappointment; per seller: no-discount repeat share,
unsubscribe rate, frequency distribution.

### E10 Buyer app (M8, parts earlier)

**DD-100 Buyer thread and accept flow** · M · depends DD-021 — the buyer side of E2 as a
PWA at 390 px first.
**DD-101 Marketplace inbox or per-seller mode** · M · depends DD-100, DD-005 — `inbox_mode`
(D3) switches the buyer's entry screen; both tested.
**DD-102 "My usuals"** · S · depends DD-082.
**DD-103 Preference centre UI** · M · depends DD-061, DD-062, DD-063 — channels,
frequency, muted categories, "why this offer", object.
**DD-104 History and audit view for the buyer** · S · depends DD-020 — the consent story
of BL §3.8: history, reason (engine or seller), basis.

## 4. Blocked register

Empty. O1–O3 and A1 were resolved on 2026-09-17 (D13–D16, then D26 for the stack);
the recommended decisions D15–D25 in `ssot.html` §5 complete the specification of
Release 1. DD-000 confirms the implementation baseline first.

## 5. Milestones 2 and 3 (epic level)

- **Model-based engine**: buyer × product relevance model, uplift targeting
  (persuadables only), learned send-time; same interface as DD-012 (ADR-8).
- **Rich channels**: RCS and WhatsApp adapters behind DD-051's interface; rich cards
  with accept buttons.
- **Learned discount depth**: bandit allocation under the guardrails of DD-022.
- **Pack mechanics**: two-sided referral card, group offers ("three of you unlock the
  price"), best-seller counts in the reason line.
- **Surprise kinds**: sample-in-parcel, gift after N orders, mystery item, small
  probabilistic reward.
- **Subscriptions**: consumable subscription offers with the buyer's own interval.
- **Multi-seller buyer wallet** and print-and-post pricing (O2).

## 6. Risks

| Risk | Mitigation |
|---|---|
| Oversell in flash campaigns under load | DD-032 concurrency test in CI; reconciliation job |
| A send path bypassing consent | DD-060 acceptance: every sender goes through `may_send`; test enumerates senders |
| Connector drift across four shop platforms | DD-070 contract suite as the gate for every connector |
| Advanced-mode values breaking legal defaults | ADR-6, legal floor enforced in A1 (D13) |
| Thin history for the engine on small shops | rules v1 degrades to `replenish_days` and category defaults |
| Print partner choice (O2) arrives late | interface-first design; DD-054 ships the seller mode first |

## 7. Release 1 — the first deliverable version (D25)

Release 1 is Hungary only (D17), on the four Release 1 channels (D20), with the seller
print mode (D15), Shoprenter and UNAS connectors (D18) and the buyer app at phone
width first. It is complete when every issue below meets the global Definition of Done.

| Epic | Issues in Release 1 |
|---|---|
| E0 Foundations | DD-000, 001, 002, 003, 004, 005, 006, 007, 008 |
| E1 Thread | DD-010, 011, 012, 013 |
| E2 Offers | DD-020, 021, 022, 023, 024 |
| E3 Flash | DD-030, 031, 032, 033, 034 |
| E4 Lists | DD-040, 041, 042 |
| E5 Channels | DD-050, 051, 052, 053, 054 (seller mode), 055 |
| E6 Consent | DD-060, 061, 062, 063, 064, 065 |
| E7 Hand-off | DD-070, 074, 073, 075, 076 |
| E8 Rule sets | DD-080, 082 |
| E9 Measurement | DD-090, 091, 092 |
| E10 Buyer app | DD-100, 101, 102, 103, 104 |

Release 1.1: DD-072 WooCommerce, DD-071 Shopify, DD-054 platform print service
(Pingen), DD-081 journey runner, DD-083 progress card, DD-084 back-in-stock and
price-drop, DD-085 birthday, DD-086 membership. Release 2 and 3: §5.

Indicative sequencing for one team of four engineers plus one data engineer, on the
existing implementation (D26): E0 two weeks; E1–E2 and E6 in parallel four weeks; E3–E4 and E5 four weeks; E7 four weeks
(connectors in parallel); E8–E10 four weeks; hardening and the compliance test pass two
weeks. About twenty weeks to Release 1, with the critical path through E7.
