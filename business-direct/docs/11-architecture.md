# business.direct — architecture

*Written 2026-09-19 for the first client, Your Field NYC (D11); phase 2 (campaigns, upgrades, recap — D21–D23) added the same day; on 2026-09-20 the stack became the **build baseline** (D37): every
service was verified against the vendor's own terms (`01g-research-real-system.md`), the modules,
drawings and pseudo code are in `20-system-blueprint.md`, and ADR-15 to ADR-25 record the service
choices. The stack follows DiscountDirect's decided stack (D26 there) because the client platform
runs on the same family (`02-audit.md` §1); the owner flips any ADR with a decision. Terms are the
SSOT's (`10-ssot.md`).*

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
| Public API | 12 endpoints found in the site's bundles; no reference page; read-only without a key; the catalogue changes daily (one provider and 51 record updates between two pulls on the same day) | connector first, own copy of the catalogue second (ADR-2) |
| Home | 118 KB HTML, 24 scripts, TTFB 0.53 s | no performance debt to inherit |
| Providers | 253; 130 with e-mail, 181 with phone, 83 with a next session, 72 with a trial policy | the sales flow's reach and the digest's input are known numbers |
| Claims | 0 of 253 managing their page | the pipeline starts with everyone at *identified* |
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

## 4. Containers (build baseline, D37)

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
                alert fan-out, retention (thirteen schedules, blueprint §6)
  Media worker (Fly.io container): ffmpeg · Deepgram · c2pa-node — the one
                thing a Vercel function cannot do (ADR-24)
  Platform connector: YourFieldConnector | SportolokConnector (one interface)
  DoneIsBetter SSO for operator and provider sign-in (ADR-5)
  Sentry + Better Stack on /api/health (ADR-25)
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
| Media worker (ADR-24) | a stateless container on Fly.io: transcribe (Deepgram), find moments, cut 9:16 with burned captions (ffmpeg), sign (C2PA), upload to Blob, call back; refuses a recording that shows children without the consent reference (R30) — the second enforcement |
| Media adapters (D28) | `MediaAdapter.clips` (v1: a recording → captioned clips), `.video`, `.image`, `.audio` (later) behind one interface; every output carries a C2PA credential (R20); never a person (R15) |
| Sending domain per instance | warm-up schedule, daily cap, bounce monitor; the outbox refuses sends past the limits |
| Policy gate (D32) | reads the instance's policy record before every send and draft; blocks and explains |
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
upgrades → *upgraded*. Three touches 3–4 days apart in propensity order (D28); call task for phone-only.

**Family digest and alerts.** Sunday 17:00: for every family with `picks` on, build the
digest from saved providers + nearby providers with a session next week → preference check
(the digest and alerts are the platform's own and do not count toward the provider cap, R3)
→ outbox → Resend at 18:00. Alerts: catalogue sync diff (new session at a saved provider) →
preference check → platform push.

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
log of everything sent), `knowledge_files`, `integrations`, `generated_pages`, `campaigns`, `products`, `entitlements`, `enquiries`, `comments`, `events` (append-only, ADR-11) and `metrics_daily` (materialised). Every
document carries `platform_id` (Your Field, Sportolok) — one deployment, several
instances (ADR-2). Retention: message log 24 months; consent log for the life of the
account plus 5 years; drafts 90 days after their final state.

## 7. Integration architecture

| Integration | Direction | Auth | Notes |
|---|---|---|---|
| Your Field API | read catalogue, facets, site; write claim requests, demand capture, notifications, generated pages | none for reads; key for writes (prerequisite P-7) | polled daily + on demand; ETag/`updatedAt` diff |
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

## 10. Stack (build baseline, D37; each line verified in `01g-research-real-system.md`)

| Layer | Choice | Reason |
|---|---|---|
| App | Next.js 15, React, Mantine with GDS tokens | the client platform's stack; one design system across the family (D5, `14-token-map.md`) |
| Data | MongoDB Atlas (Mongoose) | DiscountDirect D26; document shapes match the platform's JSON |
| Cache/limits | Upstash Redis | caps and idempotency |
| Files | Vercel Blob | post media, audit snapshots |
| Jobs | Vercel Cron (Pro: one-minute granularity, 300 s per tick) + durable outbox in MongoDB; Inngest is the named upgrade path | proven in DiscountDirect; no separate queue to run; the outbox row is Inngest-shaped (ADR-18) |
| Media processing | one Fly.io container: ffmpeg, Deepgram Nova, `c2pa-node` | a Vercel function cannot run ffmpeg for minutes (ADR-24) |
| Observability | Vercel logs, Sentry (free tier), Better Stack on `/api/health` | the five alerts of §9 (ADR-25) |
| E-mail | Resend | D26; inbound parsing for replies |
| Social | Meta Graph API first; TikTok and X second | reach on the family side (research §4) |
| SMS | Twilio | consent tooling, STOP handling |
| Auth | DoneIsBetter SSO | the family's existing identity provider |
| AI | Claude API behind the `Drafter` interface: Sonnet 5 for drafts, Haiku 4.5 for classification, the Batch API for the nightly sets; `DRAFTER=template` runs the machine without AI | drafting quality; optional (R10); ADR-22 |
| Billing | Stripe (Checkout + Billing, the platform's account) | upgrades (ADR-9) |

## 11. Architecture decision records (the build baseline since D37; the owner flips any with a decision)

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
| ADR-12 | **Media generation behind one `MediaAdapter` interface with the clip engine as the only v1 service**; vendors are configuration (a Higgsfield-class aggregator or Runway for video, Ideogram / Nano Banana / Firefly for image, ElevenLabs for audio) | (a) one vendor SDK in the app; (b) one interface, vendors as config; (c) no generation | (b): Sora's shutdown in 2026 showed vendors churn; human-first evidence puts the clip engine first; credentials and labels are the interface's job, not each vendor's |
| ADR-13 | **Propensity score computed in the nightly metrics job**, stored on `provider_state`, read by the sequence and call-list jobs | (a) score at send time; (b) nightly, stored; (c) a third-party lead-scoring service | (b): one number everyone reads, auditable, cheap; matches the events already logged |
| ADR-14 | **One policy record per instance, enforced by a gate in the outbox, the draft jobs and the schema** (D32) | (a) policy as documentation; (b) policy as configuration read by the code; (c) a third-party consent-management platform | (b): the enforcement record is a list of defaults and labels, not breaches — the rules must be code; a CMP handles cookies, not sequences, digests and audiences |
| ADR-11 | **Analytics as an append-only event log in MongoDB with nightly materialised metrics per `platform_id`**; no third-party analytics SaaS holds family data | (a) product-analytics SaaS (Amplitude / Mixpanel); (b) own event log + materialised views; (c) warehouse + BI | (b): the events already exist as collections; the metrics tree is small and known; family data stays in the platform's region (§8); a warehouse can be added when a second instance needs cross-instance reporting |
| ADR-10 | **Campaign audiences are resolved by the platform's saves and location, never uploaded lists** | (a) providers upload contacts; (b) audiences from the platform's data only | (b): consent lives on the platform (R4, R11); no provider list ever enters the machine |
| ADR-15 | **Vercel Pro hosts the app, the routes and the crons** | (a) Vercel; (b) Fly.io for everything; (c) a VPS | (a): the platform's own host; preview per branch; 40 crons at one-minute granularity; the one gap (long ffmpeg runs) goes to ADR-24 |
| ADR-16 | **MongoDB Atlas, M0 for the build and the pilot, M10 for production** | (a) Atlas; (b) Postgres on Neon | (a): D26 stays; the message log is the first collection that needs M10's backups and TTL headroom |
| ADR-17 | **Vercel Blob for media, snapshots and exports** | (a) Blob; (b) Cloudflare R2 | (a): public HTTPS URLs Meta can fetch, signed URLs for the worker, one vendor fewer |
| ADR-18 | **Vercel Cron + a MongoDB outbox; Inngest when a measured limit is hit** (a tick > 300 s that cannot be batched, > 40 schedules, or a workflow that must wait days on an external event) | (a) cron + outbox; (b) Inngest now; (c) Trigger.dev | (a): everything the machine needs today is a durable row and a one-minute drain; the row is kept event-shaped so (b) is a new consumer, not a migration |
| ADR-19 | **Resend for outbound and inbound e-mail** | (a) Resend; (b) Postmark | (a): D26; inbound as a signed webhook; delivery events feed the sending guard; List-Unsubscribe headers on every marketing message |
| ADR-20 | **Meta Graph API directly (Instagram API with Facebook Login for Business)** | (a) direct; (b) a scheduling SaaS as proxy | (a): the outbox stays the only sender and the audit snapshot stays in the message log; App Review starts in sprint 0 |
| ADR-21 | **Twilio with A2P 10DLC, built in the adapter's shape but switched off until the policy record allows SMS** | (a) Twilio; (b) Telnyx; (c) no SMS | (a): consent tooling and STOP handling; registration needs the privacy-policy and terms URLs the record holds |
| ADR-22 | **Claude API as the first `Drafter`: Sonnet 5 drafts, Haiku 4.5 classifies, Batch for nightly sets; `ai_meta` stored on every AI output** | (a) Claude; (b) OpenAI; (c) a local model | (a): quality per cost at ~$0.01 a draft with cached context; the vendor is an environment variable |
| ADR-23 | **Deepgram Nova (batch) for transcription** | (a) Deepgram; (b) Whisper API | (a): word timestamps and diarisation at ~$0.0043 a minute; the captions (R34) and the moment finder need the timestamps |
| ADR-24 | **One stateless media worker on Fly.io (ffmpeg, Deepgram, `c2pa-node`)** | (a) Fly.io container; (b) `ffmpeg-static` in a Vercel function; (c) Modal | (a): a 30-minute recording does not fit 300 s or 250 MB; auto-stop machines cost cents at pilot; (c) if a vision model joins |
| ADR-25 | **Sentry + Better Stack on `/api/health`; no analytics SaaS** | (a) Sentry + uptime; (b) Datadog | (a): free tiers cover the pilot; the five alerts are computed by the machine itself (ADR-11) |
