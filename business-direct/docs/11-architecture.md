# business.direct — architecture

*Written 2026-09-19 for the first client, Your Field NYC (D11); phase 2 (campaigns, upgrades, recap — D21–D23) added the same day. The stack is PROPOSED
(§10, ADRs in §11): it follows DiscountDirect's decided stack (D26 there) because the
client platform runs on the same family (`02-audit.md` §1), and the owner or client flips
each ADR. Terms are the SSOT's (`10-ssot.md`).*

## 1. System context

```
 Families (web, e-mail, push, SMS)        Social channels (Instagram, Facebook, TikTok, X)
        ▲            ▲                              ▲
        │            │                              │ posts, replies to comments
        │            │                              │
 ┌──────┴────────────┴──────────────────────────────┴───────────────┐
 │  Your Field NYC (Next.js on Vercel) — the platform                │
 │   public API · accounts · saved items · claim requests · notify   │
 └──────────────────────────────▲───────────────────────────────────┘
                                │ reads the catalogue; writes claim requests,
                                │ notifications, generated pages (with a key)
 ┌──────────────────────────────┴───────────────────────────────────┐
 │  business.direct — the machine                                    │
 │   departments · drafts · approval queue · pipeline · knowledge    │
 │   intelligence · integrations                                     │
 └───────▲──────────────────────────────────▲───────────────────────┘
         │ approves, edits, reads             │ invitation, replies, apply-to-manage
   Operator (platform)                 Providers (e-mail, phone, their own view)
```

Three actors, one gate: nothing reaches a family, a provider or a channel without an
approval (R1). The platform stays the system of record for providers and families;
business.direct owns drafts, approvals, pipeline state, knowledge files, consent records
and the message log.

## 2. The target, measured (`02-audit.md`, 2026-09-19)

| Measure | Value | Consequence |
|---|---|---|
| Platform stack | Next.js + Mantine on Vercel, v0.201.105 | the machine can be a module of the same deployment or a sibling app on the same stack (ADR-1) |
| Public API | 12 endpoints found in the site's bundles; no reference page; read-only without a key | connector first, own copy of the catalogue second (ADR-2) |
| Home | 118 KB HTML, 24 scripts, TTFB 0.53 s | no performance debt to inherit |
| Providers | 252; 130 with e-mail, 180 with phone, 83 with a next session, 72 with a trial policy | the sales flow's reach and the digest's input are known numbers |
| Claims | 0 of 252 managing their page | the pipeline starts with everyone at *identified* |
| Reference instance | same stack, 431 listings, documented API incl. `POST /api/ingest` | the connector interface must fit two instances (ADR-2) |

## 3. Quality attributes

| Attribute | Target | Why |
|---|---|---|
| Human gate | 100 % of outbound content passes an approval; audit trail of who approved what, when | R1, the videos' operating rule, EU AI Act Art. 50 marking |
| Consent and caps | 0 messages beyond a family's cap or without the channel's consent; SMS never without written consent | TCPA damages $500–1 500 per message (research §8) |
| Opt-out latency | < 1 business day (law: 10) | CAN-SPAM |
| Freshness | catalogue refreshed at least daily; a provider's new session reaches saved families within 1 hour | alerts |
| Scale (first year, sizing) | 1 000 providers, 50 000 families, 200 posts/week, 5 000 e-mails/day | one city, then a second instance |
| Availability | 99.5 % for the operator console; the outbox is durable, delivery may lag | nobody logs in; the machine must not lose approved work |
| Portability | channel adapters and the platform connector behind interfaces; a second instance (Hungarian reference) is a configuration, not a fork | D11's "reference ideas" |

## 4. Containers (PROPOSED)

```
┌────────────────────────────────────────────────────────────────┐
│ business.direct app — Next.js 15 App Router on Vercel (Node 24) │
│  • operator console, provider view, family preferences (GDS)    │
│  • Server Actions for approvals, edits, stage moves             │
│  • Route Handlers: webhooks (Resend inbound, Meta, Twilio),     │
│    platform callbacks, cron entry points                        │
└───────┬──────────────┬──────────────┬──────────────┬───────────┘
        │              │              │              │
  MongoDB Atlas   Upstash Redis   Vercel Blob    Providers:
  (drafts,        (caps per       (media for     Resend (e-mail out + inbound)
   approvals,      family,         posts,        Meta Graph (IG/FB) · TikTok · X
   pipeline,       rate limits,    exports,      Twilio (SMS, consent proof)
   consent log,    idempotency)    audit         platform push (Your Field API)
   message log,                    snapshots)    LLM API (drafting, optional)
   knowledge files)
        │
  Vercel Cron → outbox workers: catalogue sync, draft generation,
                scheduled publishing, sequence steps, digest build,
                alert fan-out, retention
  Platform connector: YourFieldConnector | SportolokConnector (one interface)
  DoneIsBetter SSO for operator and provider sign-in (ADR-5)
```

| Container | Responsibility |
|---|---|
| App | the three views; every mutation is a Server Action that writes an approval event |
| MongoDB | system of record for everything business.direct owns (SSOT §3) |
| Redis | frequency caps (R3), send rate limits, idempotency keys for webhooks |
| Blob | post media, exports, audit snapshots of what was published |
| Outbox workers | the only thing that sends; consumes `approved` drafts, writes the message log |
| Platform connector | read the catalogue; write claim requests, notifications, generated pages when keyed |
| Channel adapters | one per channel, same interface: `draft → preview`, `publish`, `inbound webhook → thread` |
| LLM | drafting only, behind the department's AI switch (R10); the knowledge files are the prompt context |

## 5. Key flows

**B2C social publishing.** Cron: catalogue sync → for each provider with news (announcement,
new session, trial) build a draft from the knowledge files → queue *waiting* → operator
approves / edits / skips → scheduled → worker publishes through the adapter at the slot →
message log + audit snapshot → comments and DMs arrive by webhook → drafted replies → queue.

**B2B provider sales.** Sequence approved once for a recipient set → worker sends step 1 by
Resend with the opt-out → stage *contacted* → inbound reply by webhook → thread + drafted
answer → queue → sent → stage *replied* → provider clicks apply → platform `claim-requests`
→ stage *applied* → platform confirms → *managing* → provider view unlocks → later
upgrades → *upgraded*. Reminder after 5 days to non-repliers; call task for phone-only.

**Family digest and alerts.** Sunday 17:00: for every family with `picks` on, build the
digest from saved providers + nearby providers with a session next week → cap check →
outbox → Resend at 18:00. Alerts: catalogue sync diff (new session at a saved provider) →
cap check → platform push.

**Provider campaigns (phase 2).** Catalogue sync → for a managing provider with a trial
policy, next session, announcement or open registration: build a campaign draft → the
provider approves / edits / skips in its view → audience resolved (saved families + nearby
in the age range, from the platform's saves) → per family: preference and cap check →
outbox → channel adapter → message log with the reason line.

**Conversations (phase 3).** Inbound: platform message (webhook from the platform), e-mail
(Resend inbound), missed call (Twilio voice webhook) → `enquiries` row → draft from the
provider's knowledge files + card → provider view → approve / edit → outbox → the same
channel + the family's inbox thread; reply time logged. A family's "ask about a trial"
is a platform message to a saved provider. Comments and DMs on published posts arrive by
the channel adapter's webhook → drafted reply with the listing link → operator approves.

**Upgrades.** Provider chooses a product → Stripe Checkout (the platform's account) →
webhook → `entitlements` row → stage *upgraded* → the platform connector sets the
featured / camp / profile flag on the card.

**Preferences and stop.** A family's change is written first, then the caps; *Stop* sets
every channel off and cancels queued messages for that family in the same transaction.

## 6. Data architecture

MongoDB collections: `providers_cache` (the catalogue copy, refreshed by sync, never
edited), `provider_state`, `drafts`, `approvals` (append-only), `sequences`, `threads`,
`families_prefs`, `consents` (append-only, with the proof text), `messages` (append-only
log of everything sent), `knowledge_files`, `integrations`, `generated_pages`, `campaigns`, `products`, `entitlements`, `enquiries`, `comments`. Every
document carries `platform_id` (Your Field, Sportolok) — one deployment, several
instances (ADR-2). Retention: message log 24 months; consent log for the life of the
account plus 5 years; drafts 90 days after their final state.

## 7. Integration architecture

| Integration | Direction | Auth | Notes |
|---|---|---|---|
| Your Field API | read catalogue, facets, site; write claim requests, demand capture, notifications, generated pages | none for reads; key for writes (ask #5) | polled daily + on demand; ETag/`updatedAt` diff |
| Resend | out + inbound webhook | API key; signed webhooks | provider e-mail, family digest; unsubscribe link per message |
| Meta Graph (Instagram, Facebook) | publish, read comments/DMs | OAuth per page | approval required by the platform; publish only from the outbox |
| TikTok, X | publish | OAuth | same adapter interface; second release |
| Twilio | SMS out, inbound STOP | API key | consent proof stored before the first send (R4) |
| Platform push | out | via the platform's notifications endpoint | the platform owns the device tokens |
| Google Business Profile, calendar | provider-side, read reviews / write bookings | OAuth per provider | third release |
| LLM API | drafting | API key | optional per department; prompts are the knowledge files; outputs marked as AI drafts |
| Stripe (ADR-9) | provider upgrades: checkout, subscription, webhook → entitlement | API key; signed webhooks | the platform is the merchant; business.direct records the entitlement and the stage |

## 8. Security and privacy

Operator and provider sign-in through DoneIsBetter SSO (ADR-5); provider access is scoped
to its own `provider_id`. Families never sign in to business.direct — preferences are
reached through signed links from the platform's account or through the platform's own
UI (ADR-6). Secrets in Vercel environment; webhooks verified by signature; idempotency
keys on every inbound event. Personal data: families' names, children's first names and
ages, saved providers, preferences, consent — minimised, exportable, deletable on the
platform's account deletion via a webhook. No data leaves the region the platform uses.

## 9. Deployment and operations

Vercel preview per branch, production on `main`; MongoDB Atlas with daily backups;
Upstash and Blob in the same region. Cron schedules: sync hourly, drafting 08:00 daily,
digest Sunday 17:00/18:00, sequences 09:00 weekdays, retention nightly. Alerting on:
outbox lag > 30 min, webhook signature failures, cap violations (must be zero), send
errors per channel. Runbooks for: a channel's token expiry, a provider's "not my program",
a family's deletion request.

## 10. Stack (PROPOSED)

| Layer | Choice | Reason |
|---|---|---|
| App | Next.js 15, React, Mantine with GDS tokens | the client platform's stack; one design system across the family (D5, `14-token-map.md`) |
| Data | MongoDB Atlas (Mongoose) | DiscountDirect D26; document shapes match the platform's JSON |
| Cache/limits | Upstash Redis | caps and idempotency |
| Files | Vercel Blob | post media, audit snapshots |
| Jobs | Vercel Cron + durable outbox in MongoDB | proven in DiscountDirect; no separate queue to run |
| E-mail | Resend | D26; inbound parsing for replies |
| Social | Meta Graph API first; TikTok and X second | reach on the family side (research §4) |
| SMS | Twilio | consent tooling, STOP handling |
| Auth | DoneIsBetter SSO | the family's existing identity provider |
| AI | one LLM provider behind an interface, configurable | drafting quality; optional (R10) |
| Billing | Stripe (Checkout + Billing, the platform's account) | upgrades (ADR-9) |

## 11. Architecture decision records (all PROPOSED)

| ADR | Decision | Options considered | Reason |
|---|---|---|---|
| ADR-1 | business.direct is a **sibling app** on the platform's stack, not a module inside Your Field | (a) module in the platform repo; (b) sibling app; (c) separate stack | (b): a second instance (Sportolok) must run from the same code; the platform's release cadence stays its own |
| ADR-2 | **One platform connector interface**, two implementations; the catalogue is cached in MongoDB with `platform_id` | (a) read the API live per request; (b) cached copy with sync; (c) database access to the platform | (b): the public API has no reference page and no rate contract; diffs drive alerts |
| ADR-3 | **Frequency caps in Redis**, checked at enqueue and again at send | (a) count in MongoDB; (b) Redis counters; (c) trust the schedule | (b): atomic and fast; the double check makes a cap violation impossible in a race |
| ADR-4 | **The outbox is the only sender**; UI actions never call a channel | (a) send from the Server Action; (b) outbox | (b): R1 audit trail, retries, a cancel on *Stop* |
| ADR-5 | **DoneIsBetter SSO** for operators and providers | (a) own auth; (b) SSO; (c) platform's sessions | (b): the family's identity provider; one account for a provider across the platform and the machine |
| ADR-6 | **Families do not sign in to business.direct**; preferences by signed link or through the platform's UI | (a) family accounts here; (b) signed links + platform UI | (b): no second account, no second password; data minimisation |
| ADR-7 | **AI drafting behind an interface, optional per department**, outputs marked | (a) AI always on; (b) optional per department; (c) none | (b): D6; EU AI Act Art. 50 marking; the provider with AI off still gets the listing's own text |
| ADR-8 | **Generated pages are written to the platform** through its API, not hosted by business.direct | (a) host here; (b) write to the platform | (b): search authority belongs to the platform's domain (research §5) |
| ADR-9 | **Upgrades billed by Stripe on the platform's account**; business.direct stores only the entitlement | (a) business.direct as merchant; (b) the platform as merchant via Stripe; (c) invoices by hand | (b): the platform already sells "List your program"; one merchant, one tax position; the machine never holds card data |
| ADR-10 | **Campaign audiences are resolved by the platform's saves and location, never uploaded lists** | (a) providers upload contacts; (b) audiences from the platform's data only | (b): consent lives on the platform (R4, R11); no provider list ever enters the machine |
