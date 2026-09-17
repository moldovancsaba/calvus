# DiscountDirect — low-level technical design

Version 1.0 · 2026-09-17. Schema, state machines, API, algorithms with pseudo code,
integration contracts, security details, observability and testing. Terms per
`ssot.html`; structure per `architecture.html`.

## 1. Schema (PostgreSQL)

Conventions: `id uuid primary key default gen_random_uuid()`, `created_at timestamptz
not null default now()`, money in integer minor units with a `currency` code, every
tenant-scoped table has `seller_id` with a row-level-security policy.

```sql
create table sellers (
  id uuid primary key, name text not null, tagline text,
  market_code text not null references markets(code),
  settings jsonb not null default '{}'::jsonb,           -- SSOT §4 keys
  created_at timestamptz not null default now()
);
create table markets (
  code text primary key, currency text not null, locale text not null,
  legal_basis_by_channel jsonb not null,                  -- {"email":"legitimate_interest",...}
  soft_opt_in boolean not null, retention_days int not null,
  reference_price_days int not null default 30
);
create table buyers (
  id uuid primary key, email citext unique, phone text, postal_address jsonb,
  locale text not null default 'hu-HU', birthday date,
  created_at timestamptz not null default now()
);
create table relationships (
  id uuid primary key, seller_id uuid not null references sellers, buyer_id uuid not null references buyers,
  segment text not null check (segment in ('new','returning','loyal')),
  order_count int not null default 0, first_order_at timestamptz, last_order_at timestamptz,
  frequency_pref text, holdout_seed int not null default floor(random()*1000000),
  unique (seller_id, buyer_id)
);
create table products (
  id uuid primary key, seller_id uuid not null, external_id text not null,
  name text not null, price int not null, currency text not null, category text,
  consumable boolean not null default false, replenish_days int, stock int,
  synced_at timestamptz, unique (seller_id, external_id)
);
create table orders (
  id uuid primary key, relationship_id uuid not null references relationships,
  external_id text not null, ordered_at timestamptz not null,
  source text not null check (source in ('shop','handoff')), total int not null,
  unique (relationship_id, external_id)
);
create table order_lines (order_id uuid references orders, product_id uuid references products, qty int, price int, primary key (order_id, product_id));
create table price_history (product_id uuid, price int, valid_from timestamptz, primary key (product_id, valid_from));  -- R18
create table relevance (
  product_id uuid references products, buyer_id uuid references buyers, score real not null,
  reason_code text not null, reason_engine text not null, model_version text not null,
  computed_at timestamptz not null, primary key (product_id, buyer_id)
);
create table recommendations (
  id uuid primary key, relationship_id uuid references relationships, product_id uuid references products,
  pct_suggested int, reason_code text, reason_engine text, model_version text,
  state text not null default 'available' check (state in ('available','sent'))
);
create table templates (
  id uuid primary key, kind text not null, version int not null, defaults jsonb not null,
  legal boolean not null default false, floor jsonb not null default '{}'::jsonb, unique (kind, version)
);
create table seller_overrides (
  seller_id uuid references sellers, template_id uuid references templates,
  mode text not null check (mode in ('predefined','advanced')),   -- D13
  values jsonb not null default '{}'::jsonb, version int not null default 1,
  changed_by uuid, changed_at timestamptz not null default now(), primary key (seller_id, template_id)
);
create table campaigns (
  id uuid primary key, seller_id uuid not null, product_id uuid not null, pct int not null,
  limit_hours int not null, limit_qty_total int not null, limit_qty_per_buyer int not null,
  channels text[] not null, sent_at timestamptz, sold_out_at timestamptz,
  accepted_total int not null default 0,                   -- reconciliation truth for R10
  compensation jsonb, template_id uuid, override_version int
);
create table automations (
  id uuid primary key, seller_id uuid not null, title text not null,
  frequency text not null, channels text[] not null, product_ids uuid[] not null,
  next_run_at timestamptz, state text not null default 'active',
  discount_rule_override jsonb
);
create table automation_runs (id uuid primary key, automation_id uuid references automations, ran_at timestamptz, content_freeze jsonb, per_buyer_counts jsonb);
create table offers (
  id uuid primary key, seller_id uuid not null, relationship_id uuid not null references relationships,
  product_id uuid not null references products, kind text not null, orig int not null, pct int not null, price int not null,
  reason_engine text not null, reason_seller text, reason_source text not null default 'engine',
  channels text[] not null, status text not null default 'pending',
  limit_hours int, limit_qty_per_buyer int, expires_at timestamptz,
  sent_at timestamptz, responded_at timestamptz,
  campaign_id uuid references campaigns, automation_run_id uuid references automation_runs,
  template_id uuid, override_version int, model_version text, holdout boolean not null default false,
  checkout_url text, price_lock_until timestamptz, order_ref text,
  created_at timestamptz not null default now()
);
create index on offers (relationship_id, created_at desc);
create index on offers (campaign_id) where status = 'pending';
create table offer_events (
  id bigserial primary key, offer_id uuid not null references offers, type text not null,
  at timestamptz not null default now(), actor text not null, payload jsonb
);  -- append-only: revoke update, delete
create table messages (id uuid primary key, relationship_id uuid references relationships, from_role text, kind text, body text, channel text, offer_id uuid, at timestamptz default now());
create table deliveries (
  id uuid primary key, offer_id uuid references offers, message_id uuid references messages,
  channel text not null, status text not null default 'queued', provider_ref text,
  print_job_id uuid, at timestamptz not null default now()
);
create table coupons (code text primary key, offer_id uuid unique references offers, redeemed_at timestamptz, redeemed_channel text);
create table consents (
  id uuid primary key, buyer_id uuid references buyers, seller_id uuid,          -- null = inbox scope
  channel text not null, basis text not null, granted_at timestamptz, withdrawn_at timestamptz, source text
);
create table objections (buyer_id uuid, seller_id uuid, at timestamptz, primary key (buyer_id, seller_id));
create table print_jobs (id uuid primary key, offer_id uuid, mode text, pdf_ref text, status text, partner_ref text, posted_at timestamptz);
create table outbox (id bigserial primary key, aggregate text, aggregate_id uuid, type text, payload jsonb, created_at timestamptz default now(), relayed_at timestamptz);
create table metric_rollups (seller_id uuid, scope text, scope_id uuid, day date, metrics jsonb, primary key (seller_id, scope, scope_id, day));

alter table offers enable row level security;
create policy tenant_offers on offers using (seller_id = current_setting('app.seller_id')::uuid);
-- the same policy shape on every seller-scoped table
```

## 2. State machines

**Offer**
```
draft ──send──► pending ──accept──► accepted ──write-back──► (accepted, order_ref set)
                  │  │                  │
                  │  ├──decline───────► declined
                  │  ├──expiry (R8)───► expired
                  │  ├──sold-out (R11)► sold_out
                  │  └──withdraw──────► withdrawn
                  └── (mailing) coupon redeem (R13) ──► redeemed
Terminal: accepted, declined, expired, sold_out, redeemed, withdrawn.
Guards: accept requires status = pending ∧ now < expires_at ∧ R10 counters ok.
```
**Campaign**: `draft → sending → live → sold_out | expired → closed`.
**Automation**: `active ⇄ paused → stopped`; each run: `scheduled → running → done | failed`.
**Delivery**: `queued → sent → delivered → opened → clicked`; `failed`, `bounced`;
`mailing`: `queued → printed → posted`.
**Coupon**: `issued → redeemed`; a second redeem returns `already_redeemed`.
**PrintJob**: `created → submitted → printed → posted | failed`.

## 3. API (HTTP/JSON, versioned under `/v1`)

Auth: bearer token; seller endpoints require a seller role and set `app.seller_id`;
buyer endpoints require a buyer session. Errors: `{error: {code, message, details}}`;
codes include `validation`, `not_pending`, `expired`, `sold_out`, `per_buyer_limit`,
`consent_blocked`, `frequency_capped`, `guardrail`, `already_redeemed`.

| Method and path | Role | Purpose |
|---|---|---|
| `GET /relationships?query=` | seller | inbox rows: buyer, last message, pending count |
| `GET /relationships/{id}` | seller, buyer | thread, history, recommendations, segment |
| `POST /relationships/{id}/messages` | both | chat message |
| `POST /relationships/{id}/offers` | seller | body `{recommendation_id \| product_id, pct, channel, reason_seller?}` → offer |
| `POST /offers/{id}/accept` | buyer | → `{status, checkout_url}` (R7) |
| `POST /offers/{id}/decline` | buyer | |
| `POST /offers/{id}/reason` | seller | edit `reason_seller` while pending (D4) |
| `POST /campaigns/preview` | seller | targets, blocked buyers, holdout count |
| `POST /campaigns` | seller | create and start fan-out |
| `GET /campaigns/{id}` | seller | counters, sold-out, deliveries |
| `POST /automations` · `PATCH /automations/{id}` · `DELETE` | seller | lists; `PATCH` for pause/resume/override |
| `POST /automations/preview` | seller | per-buyer split |
| `GET /templates` · `GET /templates/{id}` | seller | library with effective values |
| `PUT /templates/{id}/override` | seller admin | `{mode: predefined \| advanced, values}` (R1; legal templates enforce their floor) |
| `GET /settings` · `PATCH /settings` | seller admin | SSOT §4 keys, validated |
| `GET /me/inbox` | buyer | per-seller thread list or marketplace inbox (D3) |
| `GET /me/usuals` | buyer | reorder list with predicted run-out (R20) |
| `GET /me/preferences` · `PUT /me/preferences` | buyer | channels, frequency, muted categories, scope per D11 |
| `POST /me/object` | buyer | Art. 21 objection for a seller or the inbox |
| `POST /coupons/{code}/redeem` | seller agent, public page | R13 |
| `GET /handoff/{token}` | public | verifies, marks, redirects to the shop checkout |
| `POST /webhooks/shop/{seller_id}/{platform}` | connector | orders, stock, products |
| `POST /webhooks/channel/{channel}` | adapter | delivery statuses |
| `GET /metrics?scope=&id=&from=&to=` | seller | rollups per SSOT §7 |

## 4. Algorithms

### A1 Rule-set resolution: predefined or advanced mode (R1, D13)
```
function effective(seller, kind):
  t = latest template of kind
  o = seller_overrides[seller, t]
  if o is null or o.mode == 'predefined': return t.defaults
  v = deep_merge(t.defaults, o.values)                 # advanced mode: the seller's own values
  if t.legal: v = clamp_to_floor(v, t.floor)           # never below the legal/consent floor
  return v
```
`PUT /templates/{id}/override` with `mode = advanced` on a legal template returns
`validation` when a value is below `t.floor`; the console shows the floor next to the
field.

### A2 Relevance and reason codes, milestone-1 rules
```
function relevance(relationship):
  owned = products in orders(relationship)
  out = []
  for p in seller.products:
    if p in owned and p.consumable:
      days = days_until_runout(relationship, p)          # A3
      if days <= 14: out += (p, score=0.9 - days/100, code='REPLENISH', text="Utoljára {last} vásároltad; kb. {days} nap múlva fogy el")
    for q in owned:
      if accessory_of(p, q): out += (p, 0.7, 'ACCESSORY', "Illik a {q.name} termékedhez")
      if upgrade_of(p, q) and months_since(q) >= 18: out += (p, 0.6, 'UPGRADE', "A {q.name} után a következő generáció")
    if co_purchase_rate(p, owned) >= 0.2: out += (p, 0.5, 'CO_PURCHASE', "{n} hasonló vásárló vette ezzel")
  return top_k(dedupe_by_product(out), 5)
```
Reason texts are templated per locale; `reason_code` is the audit key.

### A3 Replenishment prediction (R20)
```
function days_until_runout(relationship, p):
  dates = ordered_at of orders(relationship) containing p, ascending
  if len(dates) >= 2: interval = median(diff(dates)) else interval = p.replenish_days
  if interval is null: return +inf
  return (dates.last + interval) - today
```

### A4 Per-buyer list split (R17, R12)
```
function split(automation):
  rule = automation.discount_rule_override ?? seller.settings.newsletter_discount_rule
  for buyer in buyers_of(seller):
    items = [p for p in automation.product_ids if (p, buyer) in relevance]
    if items == []: continue
    yield buyer, [(p, pct_for(buyer, p, rule), relevance[p, buyer].reason) for p in items]
```

### A5 Flash fan-out, atomic accept, sold-out (R9–R11)
Fan-out (worker, batches of 500):
```
targets = relevance(product).buyers - holdout(campaign) - blocked_by_consent_or_cap
for batch in chunks(targets, 500):
  insert offers(kind='flash', status='pending', expires_at = now + limit_hours, ...)
  enqueue deliveries
redis.set(f"camp:{id}:left", limit_qty_total)
```
Accept (API), atomic with Lua on Redis and confirmed in the database:
```
-- Lua: returns 1 on success, 0 when sold out, -1 when the buyer hit their limit
local left = tonumber(redis.call('GET', KEYS[1]))
local mine = tonumber(redis.call('GET', KEYS[2]) or 0)
if left <= 0 then return 0 end
if mine >= tonumber(ARGV[1]) then return -1 end
redis.call('DECR', KEYS[1]); redis.call('INCR', KEYS[2]); return 1
```
```
function accept(offer, buyer):
  assert offer.status == 'pending' and now < offer.expires_at   -> else not_pending / expired
  r = redis.eval(script, [camp_left, camp_buyer(buyer)], [limit_qty_per_buyer])
  if r == 0: return sold_out
  if r == -1: return per_buyer_limit
  in transaction:
    update offers set status='accepted', responded_at=now where id=offer.id and status='pending'   -- 1 row, else rollback + redis undo
    update campaigns set accepted_total = accepted_total + 1 where id=campaign.id
    insert offer_events(type='accepted')
    if accepted_total == limit_qty_total: enqueue sold_out(campaign)
  return handoff_url(offer)                                        # A6
sold_out(campaign):
  update offers set status='sold_out' where campaign_id=id and status='pending'
  for each such offer: create message(kind='event', offer_id, body=sold_out_notice(compensation))  -- D2, D10
  campaigns.sold_out_at = now
```

### A13 Transparency renderer (R21, D14)
```
function rules_block(offer, campaign?, locale):
  lines = []
  if offer.expires_at: lines += t('expires_at', offer.expires_at)
  if campaign: lines += t('fcfs_total', campaign.limit_qty_total); lines += t('per_buyer', campaign.limit_qty_per_buyer)
  if campaign and campaign.compensation: lines += t('compensation', campaign.compensation)     # shown before sold-out
  if offer.pct > 0: lines += t('reference_price', reference_price(offer.product), market.reference_price_days)
  lines += t('reason', offer.reason_seller ?? offer.reason_engine)
  return lines
```
Every channel template (chat card, e-mail, letter, newsletter, sold-out notice) calls
`rules_block` and renders every line; a rendering without it fails the template test.
Reconciliation: hourly, `campaigns.accepted_total` is the truth; Redis keys are rebuilt
from it if they diverge.

### A6 Hand-off and write-back (R7, D1)
```
function handoff_url(offer):
  offer.price_lock_until = now + settings.checkout_handoff.price_lock_minutes
  token = hmac_sign({offer_id, price, currency, exp: price_lock_until})
  return f"{platform_base}/handoff/{token}"

GET /handoff/{token}:
  claims = verify(token) -> else 410
  offer = load(claims.offer_id); assert offer.status == 'accepted'
  link = connector(seller).createCheckoutLink({product, qty:1, price: claims.price, ref: offer.id})
  insert offer_events('handoff_opened'); redirect 302 link

on shop order webhook(order):
  if order.attributes.ref matches an offer: offer.order_ref = order.external_id; insert orders(source='handoff'); event 'order_written_back'
  else: ingest as ordinary order; recompute relationship counts and segment
lock expiry job: accepted offers past price_lock_until without order_ref get event 'handoff_not_completed' (status unchanged)
```

### A7 Coupons (R13, D6)
```
code = base32(hmac(offer_id))[:10] formatted DIRECT-XXXX-XXXX
redeem(code, channel):
  in transaction: select coupon for update
    if redeemed_at: return already_redeemed
    coupon.redeemed_at = now; coupon.redeemed_channel = channel
    offer.status = 'redeemed' (from pending or accepted); event 'redeemed'
```

### A8 Consent and frequency cap (R15, R16, D8, D11)
```
function may_send(buyer, seller, channel):
  m = seller.market
  scope_key = (buyer, seller) if seller.settings.consent_scope == 'per_seller' else (buyer)
  if objected(scope_key): return blocked('objection')
  basis = m.legal_basis_by_channel[channel]
  if basis == 'legitimate_interest':
    ok = m.soft_opt_in and relationship.order_count >= 1 and channel in buyer.channels_allowed
  else:
    ok = consent(scope_key, channel).granted and not withdrawn
  if not ok: return blocked('consent')
  cap, window = seller.settings.frequency_cap[channel]
  if redis.count(f"cap:{scope_key}:{channel}", window) >= cap: return deferred(next_window_start)
  return allowed
on send: redis.incr with expiry = window
```
Deferred sends are re-queued at the window boundary and logged as `deferred`.

### A9 Holdout (R19)
```
holdout(buyer, scope_id) = (murmur3(buyer.id + scope_id) % 100) < seller.settings.holdout_pct
```
Deterministic, so the same buyer is consistently held out within one campaign or
automation and independently across them.

### A10 Scheduler (F4)
```
every minute: for a in automations where state='active' and next_run_at <= now:
  lock a; run = create automation_run(content_freeze = snapshot(products, prices, relevance))
  for buyer, items in split(a):
    if holdout(buyer, a.id): continue
    d = may_send(buyer, seller, channel)  ; if blocked: skip ; if deferred: enqueue at time
    create offers(kind='list_item') per item; enqueue newsletter delivery
  a.next_run_at = next(a.frequency, now); run.done
```

### A11 Discount guardrails (R4, D5)
```
function validate_pct(seller, relationship, product, pct):
  g = effective(seller, 'discount')          # merges settings.discount_guardrails
  if seller.settings.discount_mode == 'steps': assert pct in seller.settings.discount_steps
  else: assert g.floor_pct <= pct <= g.max_pct
  if segment_max := g.per_segment_max.get(relationship.segment): assert pct <= segment_max
  if product.cost: assert round(product.price*(1-pct/100)) >= product.cost*(1+g.margin_floor_pct/100)
  if reference_price(product) < product.price: raise guardrail('reference_price')   # R18
```

### A12 Reason ownership (R3, D4)
```
on send: offer.reason_engine = recommendation.reason_engine; offer.reason_seller = body.reason_seller (if settings.reason_editable)
buyer view: offer.reason_seller ?? offer.reason_engine ; audit view: both + reason_code + model_version
```

## 5. Integration contracts (TypeScript)

```ts
interface ShopConnector {
  listProducts(since?: Date): AsyncIterable<ProductDTO>;
  listOrders(since?: Date): AsyncIterable<OrderDTO>;
  getStock(externalIds: string[]): Promise<Record<string, number>>;
  createCheckoutLink(input: { externalProductId: string; qty: number; unitPrice: number; currency: string; ref: string; expiresAt: Date }): Promise<{ url: string }>;
  registerWebhooks(callbackUrl: string): Promise<void>;
  verifyWebhook(req: RawRequest): Promise<{ kind: 'order' | 'product' | 'stock'; payload: unknown }>;
}
interface ChannelAdapter {
  channel: 'email' | 'mailing' | 'rcs' | 'whatsapp';
  capabilities(): { richCard: boolean; buttons: boolean };
  send(d: DeliveryDTO): Promise<{ providerRef: string }>;
  parseStatus(req: RawRequest): Promise<{ providerRef: string; status: DeliveryStatus; at: Date }>;
}
interface PrintPartner extends ChannelAdapter { channel: 'mailing'; submit(job: { pdfRef: string; address: PostalAddress }): Promise<{ partnerRef: string }>; }
```

## 6. Security details

- Tokens: JWT (RS256), 15-minute access, 30-day rotating refresh; `aud` = console or buyer.
- Hand-off tokens: HMAC-SHA256 over `offer_id|price|currency|exp` with a per-seller key;
  base64url; verified server-side, never decoded by the client.
- RLS: `set local app.seller_id` per request in a transaction; platform ops use a
  separate role with audit logging.
- Webhooks: signature verification per provider; replay protection by event id.
- Rate limits: accept endpoint 10/min per buyer; coupon redeem 5/min per code.

## 7. Observability

Domain events emitted as metrics: `offer_sent`, `offer_accepted`, `offer_declined`,
`offer_expired`, `campaign_sold_out`, `handoff_opened`, `order_written_back`,
`delivery_failed`, `send_deferred_cap`, `send_blocked_consent`. Traces span
accept → hand-off → connector. Dashboards: fan-out throughput, accept latency,
write-back lag, deferred/blocked ratios, dead-letter depth.

## 8. Testing strategy

- Unit: pricing (R4, R5, R18), consent (R15, R16), split (R17), replenishment (A3),
  holdout (A9), template resolution (A1) — table-driven.
- Concurrency: flash accept under 1 000 parallel requests never exceeds either limit.
- Contract: connector and adapter interfaces against recorded provider fixtures.
- End to end: the prototype's sample data (ElektroHome, Anna Kovács / Gábor Nagy /
  Réka Szabó) as seed fixtures; the seven-step client journey as a Playwright script.
- Compliance: a test asserting no marketing send without a passing `may_send`.

## 9. Mapping the prototype to the design

| Prototype (index.html) | Design |
|---|---|
| `state.conversations[].messages` with `type: offer` | `offers` + `messages(kind='offer_ref')` |
| recommendation cards with hard-coded reasons | `recommendations` from the engine (A2) |
| `relevance` sets per product | `relevance` table |
| flash campaign form and fan-out loop | `POST /campaigns`, A5 |
| automations with per-buyer split | `automations`, A4, A10 |
| buyer tabs chat / e-mail / letter / newsletter | `deliveries` per channel, templates per channel |
| `DIRECT-<pct>-<initials>` coupon | A7 |
| "Miért kapom?" context pane | R3, R15 audit view |
