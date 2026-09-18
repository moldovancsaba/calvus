# DiscountDirect — architecture

Version 1.1 · 2026-09-18. System context, containers, components, key flows, data and
integration architecture, security, operations, the proposed stack and the architecture
decision records. Definitions are in `ssot.html`; details in `technical-design.html`.

## 1. System context

```
                 ┌──────────────────────────┐
   Seller staff ─┤                          ├─ Buyer (web / PWA, e-mail, letter,
   (console)     │      DiscountDirect      │   later RCS / WhatsApp)
                 │        platform          │
   Platform ops ─┤                          ├─ Print partner (PDF in, posted status out)
                 └───┬────────┬────────┬────┘
                     │        │        │
              Shop platform  E-mail   Messaging providers
              (orders,       provider (RCS / WhatsApp, milestone 2)
               products,     (send, bounce, open, click webhooks)
               checkout,
               stock)
```

External systems: the seller's **shop platform** (Shoprenter and UNAS first, then
WooCommerce and Shopify — D18; connector per platform), a transactional **e-mail
provider** (Resend — D26), a **print partner** (Pingen candidate, Release 1.1 — D15),
**messaging providers** later (WhatsApp first — D20), and an **identity provider** for
seller SSO (optional).

**Mission.** The platform is a retention system: churn and customer lifetime value are
the outcome metrics every container serves (D12).

## 2. Quality attributes

| Attribute | Target | Why |
|---|---|---|
| Tenancy isolation | no cross-seller data access, enforced by the tenant plugin on every query and by database roles on event collections (TD §1b) | multi-tenant SaaS, GDPR |
| Auditability | every offer traceable to model version, template, override version, reason source, holdout flag, consent basis | D4, D10, R15, DSA |
| Correctness of limits | flash quantity limits never oversold, coupons never double-redeemed | D2, D6, DSA "true scarcity" |
| Latency | accept → checkout page under 2 s p95; seller console interactions under 300 ms p95 | conversion at the accept moment |
| Scale (milestone 1 sizing) | 1 000 sellers, 50 000 buyers per seller max, 5 000 offers/s fan-out burst | flash campaigns to a whole base |
| Availability | 99.9 % for buyer-facing accept and checkout hand-off | revenue path |
| Privacy | data minimisation, retention per market, right to object in one tap | D8, GDPR Art. 21 |
| Portability | connectors and channel adapters behind interfaces; no provider lock-in in core | commodity providers |

## 3. Containers (D26: the existing Next.js spine, extended)

The diagram contains both current and target components. MongoDB, Resend, Cron, SSO,
Socket.IO and Redis-backed frequency caps are implemented. Blob-backed artifacts,
general Redis locks/counters, shop connectors, checkout hand-off and a separate
reporting projection are planned.

```
┌──────────────────────────────────────────────────────────────┐
│ Next.js 15 App Router on Vercel (Node 24)                     │
│  • server-rendered seller console and buyer app (GDS/Mantine) │
│  • Server Actions for UI mutations                            │
│  • Route Handlers: APIs, webhooks (Resend, shop connectors),   │
│    hand-off and coupon pages, cron entry points               │
└───────┬──────────────┬──────────────┬───────────────┬────────┘
        │              │              │               │
   MongoDB Atlas   Upstash Redis   Vercel Blob    Resend (out + inbound
   (Mongoose,      (caps, rate     (letters,      replies, webhooks,
    transactions,   limits, flash   exports,       unsubscribe)
    outbox, offer   counters,       PDFs, audit
    events, consent idempotency,    snapshots)
    events, campaign throttling)
    reservations)
        │
   Vercel Cron → durable outbox workers (fan-out, scheduler, deliveries,
                 write-backs, retention, rollups)
   Socket.IO realtime over Vercel with durable HTTP fallback (convenience only)
   DoneIsBetter SSO (seller staff and buyers; local password routes fail closed)
   Decision engine: a module inside the app in Release 1 (rules), a separate
   service behind the same interface from Release 2 (ADR-8)
   Reporting read model: MongoDB materialised aggregates, or a Postgres
   projection (Neon), never the primary store (D26)
```

| Container | Responsibility |
|---|---|
| Next.js app | seller console, buyer app, Server Actions, Route Handlers, webhook receivers, hand-off and coupon pages, cron entry points |
| MongoDB Atlas | system of record: every platform-owned entity, the append-only `offer_events`, consent events, campaign reservations, the durable outbox |
| Upstash Redis | **Implemented:** frequency-cap acceleration. **Planned:** rate limits, flash counters, idempotency locks, delivery throttling and worker coordination. MongoDB remains authoritative. |
| Vercel Blob | **Foundation only:** private key and signed-read contracts. Letter PDFs, privacy exports, list PDFs and audit snapshots remain planned. |
| Resend | outbound e-mail, inbound reply-to-thread, status webhooks, unsubscribe handling |
| Vercel Cron + outbox | scheduled and event-driven work: fan-out, scheduler, deliveries, write-backs, retention, rollups |
| Socket.IO | live updates in open threads; never the source of truth |
| DoneIsBetter SSO | authentication for seller staff and buyers |
| Decision engine | relevance, reason codes, replenishment (rules in Release 1); uplift and discount depth later |
| Reporting read model | **Planned:** SSOT §7 rollups, incrementality and margin analytics. Current campaign measurement is derived on demand from MongoDB purchases. |
| Shop connectors | **Planned:** modules per platform behind one interface, called from cron workers and webhook handlers. |

## 4. Core modules (inside the API)

| Module | Owns | Depends on |
|---|---|---|
| `identity` | sellers, staff, buyers, sessions, roles | — |
| `relationships` | pair, segment, history view, thread | connectors |
| `offers` | offer lifecycle, reasons, price rule, accept/decline | `pricing`, `consent`, `templates` |
| `campaigns` | flash campaign, fan-out request, limits, sold-out, compensation | `offers`, `decision` |
| `automations` | recurring lists, runs, per-buyer split | `offers`, `decision`, `scheduler` |
| `templates` | predefined rule sets, advanced-mode values, resolution with legal floors (R1) | — |
| `transparency` | rules block for every rendering (R21) | `offers`, `campaigns` |
| `pricing` | discount modes and guardrails (R4), reference price (R18) | `templates` |
| `consent` | legal basis per market (R15), consents, frequency caps (R16), objections | `templates` |
| `delivery` | channel selection, deliveries, status ingestion, coupons (R13), print jobs (R14) | adapters |
| `handoff` | signed checkout links, price lock, order write-back (R7) | connectors |
| `decision` (client) | calls the engine; caches relevance and recommendations | engine |
| `measurement` | holdout (R19), events, metric rollups (§7 of SSOT) | — |

## 5. Key flows

**F1 Personalised offer.** Seller opens a thread → console shows recommendations (engine
output cached per relationship) → seller picks one, optionally edits the reason (D4),
picks a channel → API validates pricing (R4), consent (R15) and cap (R16) → creates
`Offer(pending)`, marks the recommendation `sent` (R2), writes an outbox event → worker
sends through the adapter → `Delivery` status flows back through provider webhooks →
the thread shows the offer and its delivery states.

**F2 Flash campaign.** Seller configures product, pct, limits (total and per buyer),
channels → API previews targets from `Relevance` minus holdout (R19) and blocked buyers
(R15/R16) → on send, creates `Campaign` and enqueues fan-out → worker creates one
`Offer(flash, pending)` per target in batches, each with `expires_at` (R8), and sends →
accept requests hit an atomic counter check (R10) → at the last unit the campaign is
`sold_out`, remaining offers are marked, and `sold_out_notice` messages go out with the
compensation (R11, D10).

**F3 Accept → hand-off → order.** Buyer taps accept → API re-checks status, expiry and
limits atomically → offer `accepted`, a signed checkout URL is produced (R7) → buyer is
redirected to the shop's checkout with the locked price (connector: discount code or
pre-built cart) → shop order webhook arrives → connector matches `order_ref` → the offer
records the order; the thread shows "order confirmed" → if no write-back before the lock
expires, the offer stays `accepted` with a "not completed" flag for the seller.

**F4 Recurring list run.** Scheduler wakes the automation at `next_run_at` → worker
freezes content, computes the per-buyer split (R17) and discount (R12), applies consent
and caps, holdout → creates `Offer(list_item)` per item per buyer → sends the newsletter
per buyer → advances `next_run_at`.

**F5 Postal letter.** A `mailing` delivery renders the letter PDF (template, locale,
coupon R13) → `print_mode = platform_service`: a print job is sent to the partner and its
status is ingested (`printed`, `posted`); `seller`: the PDF is downloadable in the console
and the seller marks it posted (R14).

**F6 Consent and objection.** Buyer opens the preference centre (per seller or inbox per
`consent_scope`, D11) → changes channels, frequency, muted categories, or objects → the
change is effective for the next send; objection stops all marketing under legitimate
interest for that scope (R15).

**F7 Measurement.** Current flash campaigns freeze deterministic treatment and holdout
membership. Seller reporting compares distinct customers with imported purchases of the
same product during the campaign window and marks results comparable only when both
groups have at least ten members. Per-offer model/template attribution, nightly metric
rollups and incremental-margin dashboards are planned.

## 6. Data architecture

- **System of record** is MongoDB Atlas (D26). Shop-owned entities (`Product`,
  `Order`) are mirrored, read-only, with `external_id` and a sync watermark per seller.
- **Append-only** `offer_events` for the audit trail; entity rows hold the current
  state, events hold the history. Never update an event.
- **Outbox pattern**: state changes and their side effects are committed in one
  Mongoose transaction; Vercel Cron workers relay outbox rows. Consumers are idempotent
  by `event_id`, with short-lived Redis locks for concurrency.
- **Counters**: Redis accelerates frequency caps today; MongoDB sent-delivery history
  rebuilds missing counters. Flash inventory is enforced by MongoDB campaign balances
  and unique reservations. Redis flash counters remain planned.
- **Retention**: per market (`Market.retention_days`); a nightly job anonymises
  relationships past retention with no consent and no order in the window.
- **Reporting**: current campaign measurement is computed from transactional campaign
  snapshots and purchases. A separate materialised read model is planned before any
  primary-database change (D26–D27).

## 7. Integration architecture

- **Shop connector interface**: `listProducts`, `listOrders(since)`, `getStock`,
  `createCheckoutLink(offer)` or `createCart(offer)`, `registerWebhooks`, `verifyWebhook`.
  Implementations per platform; one worker pulls on a schedule and consumes webhooks.
- **Channel adapter interface**: `send(delivery)`, `parseStatusWebhook(request)`,
  `capabilities()` (rich cards, buttons). E-mail first; print partner implements
  `send` as job creation; RCS/WhatsApp in milestone 2.
- **Idempotency**: every outbound call carries the `delivery_id`; every inbound webhook
  is de-duplicated by provider event id.
- **Failure handling**: retries with backoff on transient errors; poison messages to a
  dead-letter queue with an ops alert; a delivery that fails is visible in the thread.

## 8. Security and privacy

- **Authentication** is DoneIsBetter SSO; local password routes fail closed (D26).
- **Authorisation**: roles (`seller_admin`, `seller_agent`, `buyer`, `platform_ops`);
  every request carries a tenant context; a Mongoose plugin injects `seller_id` into
  every tenant-scoped query and rejects queries without it; buyers see only their own
  relationships.
- **Signed links**: hand-off URLs and coupon codes are HMAC-signed with an expiry; the
  price is in the signed payload, never trusted from the client.
- **PII minimisation**: postal address only when `mailing` is consented; phone only
  when a messaging channel is consented; birthdays optional.
- **Legal**: R15 and R18 enforced in code, not policy; DSA "true scarcity": limits are
  enforced before the countdown is shown; the sold-out state is real.
- **Secrets**: provider keys per seller encrypted at rest with a per-tenant key; the
  Resend webhook signing secret is rotated before broad rollout (DD-008).
- **Logging**: no PII in logs; events reference ids.

## 9. Deployment and operations

- Environments: `dev`, `staging` (with sandbox shop and e-mail provider), `prod`.
- Continuous integration: lint, type-check, unit and contract tests on every change;
  database migrations reviewed and applied forward-only.
- Observability: structured logs, metrics (queue depth, fan-out throughput, delivery
  failure rate, accept latency), traces on the accept → hand-off path; alerts on
  dead-letter growth and write-back lag.
- Service objectives: accept path availability 99.9 %; fan-out of 50 000 offers under
  10 minutes; write-back lag under 5 minutes p95.

## 10. Stack (decided, D26)

The product is extended on its existing spine; a rewrite is not on the table until the
business logic is complete.

| Layer | Current | Add for Release 1 |
|---|---|---|
| App and API | Next.js 15 App Router on Vercel, Node 24; Server Actions; Route Handlers | — |
| Database | MongoDB Atlas via Mongoose: transactions, optimistic versions, idempotent imports, outbox, campaign reservations, consent and offer events | reporting read model (materialised aggregates or Neon projection) |
| Cache and counters | Upstash Redis client/key policy; frequency caps wired with MongoDB authority | rate limits, flash counters, idempotency locks, throttling, worker coordination |
| Object storage | Vercel Blob client, private-key policy and signed-read foundation | wire letters, exports, PDFs and audit snapshots |
| E-mail | Resend: outbound, inbound replies, webhook verification, unsubscribe | keep; rotate the webhook secret |
| Jobs | Vercel Cron + durable outbox | — |
| Realtime | Socket.IO over Vercel with durable HTTP fallback | convenience layer only |
| Auth | DoneIsBetter SSO; local password routes fail closed | — |
| UI | SovereignSquad GDS, Mantine underneath | — |
| Decision engine | rules module inside the app | separate service from Release 2 (ADR-8) |
| Hosting | Vercel; MongoDB Atlas in an EU region | — |

Withdrawn: React/Vite + Fastify + PostgreSQL + BullMQ + SES (the first proposal, D16).
The earlier documents remain the business requirements; the stack is the one above.

## 11. Architecture decision records

| ADR | Decision | Status |
|---|---|---|
| ADR-1 | Seller is the tenant; buyers are global identities linked to many sellers | accepted (D3) |
| ADR-2 | Offer is the single unit of delivery; campaigns and lists fan out into offers | accepted |
| ADR-3 | Append-only offer events plus current-state documents; outbox relay | accepted |
| ADR-4 | Checkout stays in the shop; the platform hands off with a signed link | accepted (D1) |
| ADR-5 | Flash limits enforced with atomic Redis counters and MongoDB campaign reservations as reconciliation truth | accepted (D2, D26) |
| ADR-6 | Predefined rule sets with a per-area advanced mode and versioning; legal templates carry a floor that advanced mode cannot go below | accepted (D10, D13) |
| ADR-10 | One transparency renderer composes the rules block for every channel | accepted (D14) |
| ADR-7 | Consent scope is a seller setting (per seller or inbox) | accepted (D11) |
| ADR-8 | Rules-based decision engine in milestone 1; model-based from milestone 2 behind the same interface | accepted |
| ADR-9 | Greenfield stack (Fastify, Vite, PostgreSQL, BullMQ, SES) | superseded by ADR-14 |
| ADR-14 | Extend the existing Next.js / Vercel / MongoDB / Resend / SSO implementation. Redis frequency caps are live; remaining Redis uses and Blob artifacts are incremental additions. Add a reporting read model before any primary-database change; realtime is never authoritative. | accepted, updated (D26–D27) |
| ADR-11 | Release 1 is Hungary only; markets are configuration | accepted (D17) |
| ADR-12 | Connectors in the order Shoprenter, UNAS, WooCommerce, Shopify | accepted (D18) |
| ADR-13 | Seller print mode first; platform print service through a swappable partner | accepted (D15) |
