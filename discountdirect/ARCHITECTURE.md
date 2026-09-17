# DiscountDirect — architecture

Version 1.0 · 2026-09-17. System context, containers, components, key flows, data and
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

External systems: the seller's **shop platform** (Shopify, WooCommerce, UNAS, Shoprenter
first; connector per platform), a transactional **e-mail provider**, a **print partner**
(D9), **messaging providers** later, and an **identity provider** for seller SSO (optional).

**Mission.** The platform is a retention system: churn and customer lifetime value are
the outcome metrics every container serves (D12).

## 2. Quality attributes

| Attribute | Target | Why |
|---|---|---|
| Tenancy isolation | no cross-seller data access, enforced in the database (row-level security) and in every query | multi-tenant SaaS, GDPR |
| Auditability | every offer traceable to model version, template, override version, reason source, holdout flag, consent basis | D4, D10, R15, DSA |
| Correctness of limits | flash quantity limits never oversold, coupons never double-redeemed | D2, D6, DSA "true scarcity" |
| Latency | accept → checkout page under 2 s p95; seller console interactions under 300 ms p95 | conversion at the accept moment |
| Scale (milestone 1 sizing) | 1 000 sellers, 50 000 buyers per seller max, 5 000 offers/s fan-out burst | flash campaigns to a whole base |
| Availability | 99.9 % for buyer-facing accept and checkout hand-off | revenue path |
| Privacy | data minimisation, retention per market, right to object in one tap | D8, GDPR Art. 21 |
| Portability | connectors and channel adapters behind interfaces; no provider lock-in in core | commodity providers |

## 3. Containers

```
┌───────────────┐   ┌───────────────┐   ┌──────────────────┐
│ Seller console│   │ Buyer app     │   │ Public hand-off  │
│ (SPA)         │   │ (PWA)         │   │ & coupon pages   │
└──────┬────────┘   └──────┬────────┘   └────────┬─────────┘
       └──────────┬────────┴─────────────────────┘
                  ▼
        ┌──────────────────┐        ┌──────────────────┐
        │ API (HTTP/JSON)  │◄──────►│ Decision engine  │
        │ auth, tenancy,   │        │ relevance, reason│
        │ core modules     │        │ codes, uplift,   │
        └───────┬──────────┘        │ replenishment    │
                │ outbox            └──────────────────┘
                ▼
        ┌──────────────────┐        ┌──────────────────┐
        │ Workers (queue)  │───────►│ Channel adapters │──► e-mail / print / RCS
        │ fan-out, sched-  │        └──────────────────┘
        │ uler, deliveries,│        ┌──────────────────┐
        │ write-backs      │◄──────►│ Shop connectors  │◄─► shop platforms
        └───────┬──────────┘        └──────────────────┘
                ▼
   ┌────────────┴───────────┐   ┌──────────┐   ┌──────────────┐
   │ PostgreSQL (OLTP, RLS) │   │ Redis    │   │ Object store │
   │ + append-only events   │   │ queues,  │   │ PDFs, exports│
   └────────────────────────┘   │ counters │   └──────────────┘
                                └──────────┘
```

| Container | Responsibility |
|---|---|
| Seller console | inbox, thread, recommendations, offer send, flash campaign, automations, templates and overrides, settings, metrics |
| Buyer app | thread per seller or marketplace inbox (D3), accept/decline, "my usuals", preferences and consent centre, history |
| Public pages | signed hand-off redirect (D1), coupon redemption page for store staff (D6), unsubscribe / object |
| API | authentication, tenancy, the core modules of §4, outbox writer |
| Workers | campaign fan-out, scheduler runs, delivery sends and status ingestion, order write-back, retention jobs, metrics rollups |
| Decision engine | relevance scores and reason codes, replenishment prediction, uplift targeting (milestone 2), discount depth (milestone 3); versioned models; batch and on-demand |
| Channel adapters | one per channel behind one interface: e-mail provider, print partner, RCS/WhatsApp |
| Shop connectors | one per platform behind one interface: products, orders, stock, checkout link or cart creation, order webhooks |
| PostgreSQL | system of record for platform-owned entities; append-only `offer_events`; RLS by `seller_id` |
| Redis | queues (fan-out, deliveries), atomic counters for flash limits and frequency caps |
| Object store | letter PDFs, exports |

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

**F7 Measurement.** Every offer carries `holdout`, `model_version`, `template_id`,
`override_version`, `reason_source`, `channel`, `trigger` → nightly rollups compute the
SSOT §7 metrics → console dashboards read the rollups.

## 6. Data architecture

- **System of record** is PostgreSQL. Shop-owned entities (`Product`, `Order`) are
  mirrored, read-only, with `external_id` and a sync watermark per seller.
- **Append-only** `offer_events` for the audit trail; entity rows hold the current
  state, events hold the history. Never update an event.
- **Outbox pattern**: state changes and their side effects are committed together; a
  worker relays outbox rows to queues. Consumers are idempotent by `event_id`.
- **Counters** for flash limits and frequency caps live in Redis for speed, with the
  database as the source of truth on reconciliation (§4 A5 of the technical design).
- **Retention**: per market (`Market.retention_days`); a nightly job anonymises
  relationships past retention with no consent and no order in the window.
- **Reporting**: rollup tables in PostgreSQL for milestone 1; a warehouse export later.

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

- **Authentication**: seller staff by e-mail + one-time code or SSO; buyers by magic
  link or one-time code; short-lived access tokens, rotating refresh tokens.
- **Authorisation**: roles (`seller_admin`, `seller_agent`, `buyer`, `platform_ops`);
  every request carries a tenant context; PostgreSQL row-level security policies on
  `seller_id`; buyers see only their own relationships.
- **Signed links**: hand-off URLs and coupon codes are HMAC-signed with an expiry; the
  price is in the signed payload, never trusted from the client.
- **PII minimisation**: postal address only when `mailing` is consented; phone only
  when a messaging channel is consented; birthdays optional.
- **Legal**: R15 and R18 enforced in code, not policy; DSA "true scarcity": limits are
  enforced before the countdown is shown; the sold-out state is real.
- **Secrets**: provider keys per seller encrypted at rest with a per-tenant key.
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

## 10. Proposed stack (assumption A1, open to objection)

| Layer | Choice | Rationale |
|---|---|---|
| Language | TypeScript end to end | one language for console, buyer app, API, workers; strong typing on the domain model |
| API | Node 22 + Fastify | fast, plain HTTP/JSON, schema validation built in |
| Workers | BullMQ on Redis | queues, delayed jobs, retries, rate limiting in one library |
| Database | PostgreSQL 16 | RLS for tenancy, JSONB for template values, reliable counters |
| Front ends | React + Vite (console), React PWA (buyer) | shares the design tokens already named after GDS 6.5.0 |
| Decision engine | Python service (FastAPI) with scikit-learn/causalml for uplift; rules in milestone 1 | data-science tooling where it lives; versioned models |
| E-mail | Postmark or Amazon SES | transactional deliverability, webhooks for status |
| Object store | S3-compatible | PDFs, exports |
| Hosting | container platform (Kubernetes or a managed equivalent) in an EU region | data residency |

Alternatives considered: a single Next.js app (simpler, weaker worker story); Go for
the API (faster, second language); a managed BaaS (fast start, weak RLS and audit).

## 11. Architecture decision records

| ADR | Decision | Status |
|---|---|---|
| ADR-1 | Seller is the tenant; buyers are global identities linked to many sellers | accepted (D3) |
| ADR-2 | Offer is the single unit of delivery; campaigns and lists fan out into offers | accepted |
| ADR-3 | Append-only offer events plus current-state rows; outbox relay | accepted |
| ADR-4 | Checkout stays in the shop; the platform hands off with a signed link | accepted (D1) |
| ADR-5 | Flash limits enforced with atomic counters, database as reconciliation truth | accepted (D2) |
| ADR-6 | Predefined rule sets with a per-area advanced mode and versioning; legal templates carry a floor that advanced mode cannot go below | accepted (D10, D13) |
| ADR-10 | One transparency renderer composes the rules block for every channel | accepted (D14) |
| ADR-7 | Consent scope is a seller setting (per seller or inbox) | accepted (D11) |
| ADR-8 | Rules-based decision engine in milestone 1; model-based from milestone 2 behind the same interface | accepted |
| ADR-9 | Stack per §10 | proposed (A1) |
