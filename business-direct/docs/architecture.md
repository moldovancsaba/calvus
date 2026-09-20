# business.direct — architecture and system blueprint

*Written 2026-09-19 for the first client, Your Field NYC (D11); phase 2 (campaigns, upgrades, recap — D21–D23) added the same day; on 2026-09-20 the stack became the **build baseline** (D37): every
service was verified against the vendor's own terms (`01g-research-real-system.md`), the modules,
drawings and pseudo code are in `architecture.md`, and ADR-15 to ADR-25 record the service
choices. The stack follows DiscountDirect's decided stack (D26 there) because the client platform
runs on the same family (`first-customer-classscout.md` §1); the owner flips any ADR with a decision. Terms are the
SSOT's (`business-logic.md`).*

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

The product's terms are media owner · advertiser · visitor · listing (SSOT §1a); the drawings
and identifiers use the first instance's words (platform · provider · family · card) because the
system was specified on its data — one instance's labels, not the product's roles. Three actors, one gate: nothing reaches a family, a provider or a channel without an
approval (R1). The platform stays the system of record for providers and families;
business.direct owns drafts, approvals, pipeline state, knowledge files, consent records
and the message log.

## 2. The target, measured (`first-customer-classscout.md`, 2026-09-19)

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

**Retention (D41).** Nightly `retention` job: for every managing or upgraded provider, read the
signals (entitlement renewal within 14 days, no card change in 30 days, an enquiry waiting > 48 h,
no saves in 30 days) → one draft per signal from the provider's own numbers → queue *waiting*
(renewal reminders under the department's earned auto-approval) → outbox → message log with
`kind: retain`; `entitlement.renewed` / `subscription.deleted` events close the loop as kept /
lost → `metrics_daily.churn`.

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
| App | Next.js 15, React, Mantine with GDS tokens | the client platform's stack; one design system across the family (D5, `architecture.md`) |
| Data | MongoDB Atlas (Mongoose) | DiscountDirect D26; document shapes match the platform's JSON |
| Cache/limits | Upstash Redis | caps and idempotency |
| Files | Vercel Blob | post media, audit snapshots |
| Jobs | Vercel Cron (Pro: one-minute granularity, 100 crons, 800 s per tick) + durable outbox in MongoDB; Vercel Workflows then Inngest are the named upgrade path | proven in DiscountDirect; no separate queue to run; the outbox row is event-shaped (ADR-18) |
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
| ADR-12 | **Media generation behind one `MediaAdapter` interface with the clip engine as the only v1 service**; vendors are configuration (a Higgsfield-class aggregator or Runway for video, Ideogram / Nano Banana / Firefly for image, ElevenLabs for audio) | (a) one vendor SDK in the app; (b) one interface, vendors as config; (c) no generation | (b): generative-video vendors change quickly (the register removed an unsourced claim, V16); human-first evidence puts the clip engine first; credentials and labels are the interface's job, not each vendor's |
| ADR-13 | **Propensity score computed in the nightly metrics job**, stored on `provider_state`, read by the sequence and call-list jobs | (a) score at send time; (b) nightly, stored; (c) a third-party lead-scoring service | (b): one number everyone reads, auditable, cheap; matches the events already logged |
| ADR-14 | **One policy record per instance, enforced by a gate in the outbox, the draft jobs and the schema** (D32) | (a) policy as documentation; (b) policy as configuration read by the code; (c) a third-party consent-management platform | (b): the enforcement record is a list of defaults and labels, not breaches — the rules must be code; a CMP handles cookies, not sequences, digests and audiences |
| ADR-11 | **Analytics as an append-only event log in MongoDB with nightly materialised metrics per `platform_id`**; no third-party analytics SaaS holds family data | (a) product-analytics SaaS (Amplitude / Mixpanel); (b) own event log + materialised views; (c) warehouse + BI | (b): the events already exist as collections; the metrics tree is small and known; family data stays in the platform's region (§8); a warehouse can be added when a second instance needs cross-instance reporting |
| ADR-10 | **Campaign audiences are resolved by the platform's saves and location, never uploaded lists** | (a) providers upload contacts; (b) audiences from the platform's data only | (b): consent lives on the platform (R4, R11); no provider list ever enters the machine |
| ADR-15 | **Vercel Pro hosts the app, the routes and the crons** | (a) Vercel; (b) Fly.io for everything; (c) a VPS | (a): the platform's own host; preview per branch; 40 crons at one-minute granularity; the one gap (long ffmpeg runs) goes to ADR-24 |
| ADR-16 | **MongoDB Atlas, M0 for the build and the pilot, M10 for production** | (a) Atlas; (b) Postgres on Neon | (a): D26 stays; the message log is the first collection that needs M10's backups and TTL headroom |
| ADR-17 | **Vercel Blob for media, snapshots and exports** | (a) Blob; (b) Cloudflare R2 | (a): public HTTPS URLs Meta can fetch, signed URLs for the worker, one vendor fewer |
| ADR-18 | **Vercel Cron + a MongoDB outbox; Vercel Workflows, then Inngest, when a measured limit is hit** (a tick past 800 s that cannot be batched, or a workflow that must wait days on an external event) | (a) cron + outbox; (b) Vercel Workflows; (c) Inngest; (d) Trigger.dev | (a): everything the machine needs today is a durable row and a one-minute drain; 100 crons per project and 800 s per tick on Pro (V1, V2); the row is kept event-shaped so (b) or (c) is a new consumer, not a migration |
| ADR-19 | **Resend for outbound and inbound e-mail** | (a) Resend; (b) Postmark | (a): D26; inbound as a signed webhook; delivery events feed the sending guard; List-Unsubscribe headers on every marketing message |
| ADR-20 | **Meta Graph API directly (Instagram API with Facebook Login for Business)** | (a) direct; (b) a scheduling SaaS as proxy | (a): the outbox stays the only sender and the audit snapshot stays in the message log; App Review starts in sprint 0 |
| ADR-21 | **Twilio with A2P 10DLC, built in the adapter's shape but switched off until the policy record allows SMS** | (a) Twilio; (b) Telnyx; (c) no SMS | (a): consent tooling and STOP handling; registration needs the privacy-policy and terms URLs the record holds |
| ADR-22 | **Claude API as the first `Drafter`: Sonnet 5 drafts, Haiku 4.5 classifies, Batch for nightly sets; `ai_meta` stored on every AI output** | (a) Claude; (b) OpenAI; (c) a local model | (a): quality per cost at ~$0.01 a draft with cached context; the vendor is an environment variable |
| ADR-23 | **Deepgram Nova (batch) for transcription** | (a) Deepgram; (b) Whisper API | (a): word timestamps and diarisation at ~$0.0043 a minute; the captions (R34) and the moment finder need the timestamps |
| ADR-24 | **One stateless media worker on Fly.io (ffmpeg, Deepgram, `c2pa-node`)** | (a) Fly.io container; (b) `ffmpeg-static` in a Vercel function; (c) Modal | (a): a 30-minute recording does not fit 300 s or 250 MB; auto-stop machines cost cents at pilot; (c) if a vision model joins |
| ADR-25 | **Sentry + Better Stack on `/api/health`; no analytics SaaS** | (a) Sentry + uptime; (b) Datadog | (a): free tiers cover the pilot; the five alerts are computed by the machine itself (ADR-11) |

## Part B — technical design: screens, content model, state machines, jobs, connectors and adapters

*Written 2026-09-19 on `architecture.md`'s PROPOSED containers. Where the prototype
already implements a rule, the section names the function in `assets/app.js` so a
developer can read the behaviour before the code exists.*

### 1. Screens and templates

| View | Screen | Template | Prototype function |
|---|---|---|---|
| Platform | Home (Simple) | recommendations ranked with reason and one button; the one safe press; the weekly routine | `platform.home`, `recommend`, `runSafe` |
| Platform | Overview (Advanced) | title + tiles + two columns (flow queue · pipeline and departments) + providers | `platform.overview` |
| Platform | Social publishing | week calendar + queue of post cards | `platform.social` |
| Platform | Provider sales | pipeline strip + sequences · reply inbox + providers in stage | `platform.sales` |
| Platform | Approvals | one list of every *waiting* draft | `platform.approvals` |
| Platform | Providers | search + chips + table + drawer | `platform.providers`, `openDrawer` |
| Platform | Generated pages | table | `platform.pages`, `genPages` |
| Platform | Integrations | card grid | `platform.integrations` |
| Platform | Policy | instance switch · gate table · principles · the record as an onboarding checklist | `platform.policy`, `policyGate` |
| Platform | Templates | sequences · posts · campaigns · knowledge files · policy records; "Use" copies into state | `platform.templates`, `TEMPLATES`, `data-tpl` |
| Platform | How to use | routine · states · rules · screens · documentation | `platform.help`, `HELP` |
| every screen | What is this? | a help panel per screen, from `HELP[role/screen]` | `helpBox()` |
| Platform | Knowledge and rules | file editors | `platform.knowledge`, `kfiles` |
| Platform | Intelligence | tiles + by department · radar and needs-you | `platform.intelligence` |
| Platform | Economics | tiles + next-dollar table + funnel strip + 12-month plan · inputs | `platform.economics`, `econ()`, `S.econ` |
| Provider | Today | hero card + (invitation · or · tiles, waiting enquiries, the four departments with earned auto-approval, the products when R19 allows, knowledge) | `provider.today` |
| Provider | Conversations | tiles + enquiry cards with drafted answers | `provider.conversations`, `enquiriesFor`, `enquiryCard` |
| Provider | Campaigns | approval cards built from the card | `provider.campaigns`, `campaignsFor`, `campaignCard` |
| Provider | Media | recording upload (inert) → clips into the platform's queue; the card photo | `provider.media`, `upload` action |
| Provider | Results | tiles + your return + what went out + plan ladder | `provider.results`, `ladder` |
| Provider | Knowledge | file editors | `SCREENS.provider.knowledge` |
| Family | Inbox | published post · digest · her conversations · campaigns from saved providers · provider SMS | `family.inbox` |
| Family | Saved | listing cards with *Ask about a trial* | `family.saved`, `data-ask` |
| Family | Saved | listing cards | `family.saved` |
| Family | Preferences | toggles + stop | `family.prefs` |

Navigation: rail ≥ 1024, bottom bar below (`app.css`), the role switch and the mode switch (Simple / Advanced, D33) in the top bar — `NAV_SIMPLE` / `NAV_ADV` and `BOTTOM_SIMPLE` / `BOTTOM_ADV` behind a proxy on `S.mode`;
deep links `?view=&screen=&stage=` (`app.js`, bottom; `stage` pre-sets the persona's pipeline stage for previews). Layout rules: `05-layout-specs.md`.

### 2. Content model (MongoDB, `platform_id` on every document)

```
providers_cache  { _id: <platform provider id>, platform_id, ...Provider (SSOT §3), synced_at }
provider_state   { provider_id, platform_id, stage, stage_changed_at, stage_changed_by, score, score_at, version }
drafts           { _id, platform_id, kind, provider_id?, family_id?, channels[], copy, media_blob?,
                   state, ai, scheduled_for?, why?, created_by: 'machine'|'person', version }
approvals        { draft_id, action: 'approve'|'edit'|'skip', by, at, diff? }         # append-only
sequences        { _id, platform_id, name, steps[{n, delay_days, subject, body, kind}], recipients[],
                   state, approved_by?, approved_at?, why }
threads          { provider_id, messages[{from:'them'|'us', channel, text, at, draft_id?}] }
families_prefs   { family_id (platform's), platform_id, prefs{picks,alerts,nearby,sms}, saved[] (mirror),
                   stopped_at?, version }
consents         { family_id, channel, provider_id?, text, captured_at, source, revoked_at? }   # append-only
messages         { _id, platform_id, to{family_id|provider_id|channel_account}, channel, draft_id,
                   sent_at, provider_message_id, status, opened_at?, clicked_at?, failed_reason? }  # append-only
knowledge_files  { owner: 'platform'|provider_id, path, text, updated_by, updated_at, version }
integrations     { platform_id, id, state, account_ref, token_ref, connected_by, connected_at }
generated_pages  { platform_id, activity, area, slug, provider_ids[], state, published_at? }
campaigns        { _id, platform_id, provider_id, kind, title, copy, channels[], state, ai, scheduled_for?,
                   audience_rule: 'saved'|'saved+nearby', audience_count?, approved_by?, approved_at?, version }
products         { platform_id, id, name, what, price_cents, interval: 'month'|'season', card_flag }
entitlements     { provider_id, platform_id, product_id, since, until?, stripe_subscription_id }
enquiries        { _id, platform_id, provider_id, family_id?, channel, from{name,kid,area}, text, received_at,
                   draft, state, ai, answered_at?, thread_id }
comments         { _id, platform_id, post_id, provider_id, channel, external_id, from, text, draft, state, ai, replied_at? }
events           { _id, platform_id, at, name, provider_id?, family_id?, draft_id?, campaign_id?, props{} }   # append-only, ADR-11
metrics_daily    { platform_id, day, cac_managing, cac_upgraded, ltv, payback, avid_families, avid_value, content_cpa, next_dollar[], rates{} }
assumptions      { platform_id, key, value, source: 'measured'|'benchmark'|'assumption', updated_by, updated_at }
sending          { platform_id, domain, warm_day, warm_days, daily_cap, bounce_rate, reply_sla_hours, postal_address }
opt_outs         { platform_id, provider_id, kind: 'not_mine'|'unsubscribed'|'bounced', at, source }   # append-only
auto_approval    { platform_id, owner, department, clean_weeks, earned_at?, revoked_at? }
policies         { platform_id, ...Policy (SSOT §3), version, updated_by, updated_at }   # D32; the gate reads it
experiments      { platform_id, name, treat_area, control_area, weeks, started_at, state, readout? }
media_assets     { _id, platform_id, provider_id?, adapter, generated: bool, credential: C2PA, blob_url, captions_url?, consent_ref?, shows_children?, used_in[] }
outbox           { _id, platform_id, kind, channel, to{}, copy, subject?, html?, media?, draft_id?, campaign_id?, step?, provider_id?, why, by,
                   countsTowardCap, state: queued|sending|sent|refused|dead, attempts, next_at, refused_reason?, policy_basis?, message_id?, created_at }   # D37, blueprint §7
media_jobs       { _id, recording_id, state: sent|done|failed, at }                       # the worker's job (blueprint §10)
sync_runs        { platform_id, at, count }                                               # /api/health reads the last one
stage_history    { provider_id, from, to, by, override, at }                              # append-only
tasks            { platform_id, kind: call|payment_failed|not_keyed|human_reply, provider_id?, family_id?, why, state, at }   # what needs a person
users            { sub, email, role: operator|provider, provider_id?, platform_id }        # SSO mapping (ADR-5)
instances        { platform_id, name, timezone, connector, base_url, key?, flags{social,campaigns,sms,clips,pages} }
webhook_log      { source, event_id, received_at, raw }                                   # 30 days, for replay
```

Indexes: `provider_state (platform_id, stage)`, `drafts (platform_id, state, scheduled_for)`,
`messages (family_id, sent_at)` for the cap query, `consents (family_id, channel, provider_id)`.

### 3. Data mapping — platform → cache

`data/fetch-yourfield.py` is the mapping (one function, `full(card)`), reproduced in the
sync worker: the list endpoint gives the card and `claimStatus`; the single record gives
sessions, announcement, trial policy, geo, verified fields. Missing neighbourhood → borough
(`app.js`, load). Diff on `updatedAt`; a new `sessions[]` id at a provider a family has
saved raises an *alert* draft.

### 4. State machines

**Draft (post)** — `waiting → scheduled → published`; `waiting → skipped`; `waiting → (edit) →
scheduled` with `ai=false` and an `approvals` row carrying the diff. Prototype:
`approve`, `edit`/`save`, `skip` actions.

**Draft (sequence, reply)** — `waiting → sent` (sequence: all steps enqueued; reply: one
message); `waiting → skipped`; radar notes `waiting → filed`. Prototype: `approveSeq`,
`approveReply`.

**Pipeline stage** — forward automatically on events; any move by a person is allowed and logged (R9, D30). Every change writes `stage.changed` with `by` and `reason`; the drawer shows the last three:

| From | To | Event | Prototype |
|---|---|---|---|
| identified | contacted | first sequence message sent | `sendInvitation` |
| identified | contacted | a family's ask to an unclaimed provider becomes sales step 2 (Q4) | `data-ask` |
| contacted | replied | inbound message from the provider | `sendInvitation` (sample replies) |
| replied | applied | claim request submitted (platform `claim-requests`) or a "yes" reply confirmed by the operator | `approveReply` |
| applied | managing | platform confirms the claim | `apply` (provider view) |
| managing | upgraded | a paid product on the platform | drawer chip only |
| any | any | operator moves by hand; logged with `stage_changed_by: 'operator'` | `data-setstage` |

**Campaign** — `waiting → scheduled → published`; `waiting → skipped`; edit sets `ai=false`
(prototype: `approveCampaign`, `saveCampaign`, `skipCampaign`). Sending resolves the audience
at send time (ADR-10), then the per-family preference and cap checks.

**Enquiry** — `waiting → sent`; `waiting → skipped`; edit sets `ai=false`; `answered_at −
received_at` is the reply time (prototype: `approveEnquiry`, `saveEnquiry`). **Comment** — the
same machine (prototype: `approveComment`).

**Entitlement** — `none → active` on the Stripe webhook; `active → ended` on cancellation;
the first `active` moves the provider to *upgraded* (prototype: `data-buy`).

**Family channel** — `on ↔ off` per channel; *Stop* → every channel off + cancel queued
drafts for that family. Consent for SMS is a separate append-only record; the toggle
cannot turn SMS on without a consent row.

### 5. Jobs (Vercel Cron → outbox workers; the cron table with schedules and batch sizes is `architecture.md` §6)

| Job | Schedule | Does |
|---|---|---|
| `sync` | hourly | pull the catalogue, diff, write `providers_cache`, raise alert drafts |
| `draft-social` | 08:00 daily | for providers with news and no draft this week: build a post draft from the knowledge files (AI if the department's switch is on, else the listing's own text — `draftCopy`) |
| `sequence-step` | 09:00 weekdays | for every approved sequence: enqueue the due step per recipient not yet replied; skip addresses with `not my program` or unsubscribe |
| `digest` | Sunday 17:00 build, 18:00 send | per family with `picks` on: saved + nearby-with-session rows; preference check (not counted toward the provider cap, R3); outbox |
| `publish` | every 5 min | send due `scheduled` posts through the adapter; write `messages`, snapshot to Blob |
| `send` | every minute | drain the outbox: for provider-originated messages the cap check again (R3), send, log; retry with backoff; dead-letter after 5 |
| `draft-campaigns` | daily 08:30 | for managing providers: one draft per kind per card event, none if one is waiting |
| `send-campaigns` | every 5 min | approved campaigns: resolve audience, preference + cap per family, outbox |
| `draft-answers` | on inbound webhook | enquiry or comment → draft from the knowledge files and the card within a minute (R14) |
| `entitlements` | webhook-driven | Stripe events → entitlements → stage → card flag through the connector |
| `clips` | on upload | refuse unless the provider confirmed written parental consent for a recording that shows children (R30); run `MediaAdapter.clips`; captions on every clip (R34); each clip becomes a post draft with `media.kind = 'real'` and the consent record attached |
| `retention` | nightly 03:30 | for every managing / upgraded provider: signals (renewal ≤ 14 d, card unchanged 30 d, enquiry waiting > 48 h, no saves 30 d) → one `retain` draft per signal from the provider's own numbers; kept / lost from entitlement events → `metrics_daily.churn` (R37) |
| `score` | nightly 02:30 | propensity per provider → `provider_state.score`; the sequence and call-list jobs read it (ADR-13) |
| `pattern-guard` | on every draft | refuse a draft with a banned pattern (false urgency, scarcity, confirmshaming, pressure on a stated vulnerability) or inaccessible output (R32, R34, R36) |
| `policy-gate` | before every send and draft; at schema validation | refuse a feature whose policy fields are missing; write the policy basis (clause, consent, cap) on every message (R26) |
| `sending-guard` | before every send | refuse when past the warm-up cap; pause the sequence at bounce ≥ 2 %; pace at the daily cap; block a provider template without `{postal_address}` (R23, Q2) |
| `auto-approve` | on draft | a department with four clean weeks sends without a person (R25); logged; the family's Stop cancels |
| `metrics` | nightly 02:00 | roll `events` into `metrics_daily`; replace an assumption with a measured rate once ≥ 100 observations exist (R16) |
| `retention` | nightly | drafts 90 days after final state; messages 24 months |

### 6. Connectors and adapters (per-adapter pseudo code: `architecture.md` §4.7)

```ts
interface PlatformConnector {
  listProviders(): Promise<ProviderCard[]>;      getProvider(id): Promise<Provider>;
  facets(): Promise<Facets>;                     siteCopy(): Promise<SiteCopy>;
  createClaimRequest(providerId, contact): Promise<void>;   // keyed
  notifyFamily(familyId, payload): Promise<void>;           // keyed
  publishPage(page): Promise<{url}>;                        // keyed (Sportolok: POST /api/ingest)
  savesFor(providerId): Promise<FamilyRef[]>;               // keyed — campaign audience (ADR-10)
  familiesNear(geo, ageRange): Promise<FamilyRef[]>;        // keyed — nearby audience
  setCardFlag(providerId, flag: 'featured'|'camp'|'profile', on): Promise<void>;  // keyed — upgrades
  // provider records carry contactKind: 'role' | 'person' (Q11); EU instances skip 'person' addresses without consent
}
interface MediaAdapter {   // D28, ADR-12
  clips(recording, listing): Promise<Clip[]>;          // v1: captions, listing link, C2PA on each clip
  video(still, brief): Promise<Asset>;                  // later: still-to-motion on the provider's real photo
  image(brief): Promise<Asset>;                         // later: tiles, headers; never a person (R15)
  audio(text, voice): Promise<Asset>;                   // later: voice-over
  // every Asset: { url, credential: C2PA, generated: boolean, label: per platform at publish }
}
interface ChannelAdapter {
  preview(draft): Rendered;   publish(draft): Promise<{providerMessageId}>;
  onInbound(webhook): InboundMessage | null;   verify(webhook): boolean;
}
```

`YourFieldConnector` maps `/api/public/*`; `SportolokConnector` maps `/api/*` incl.
`ingest`. Adapters: `ResendAdapter`, `MetaAdapter` (Instagram + Facebook), `TikTokAdapter`,
`XAdapter`, `TwilioAdapter`, `PlatformPushAdapter`.

### 7. Drafting (optional AI)

Prompt = the department's knowledge files (`rules/voice.md`, `rules/consent.md`,
`rules/social.md`; provider: `knowledge/*.md`) + the provider record + the event. Output is
a draft with `ai=true` and a `why` line the operator reads. With AI off: templates over the
listing's own text (the prototype's `draftCopy`, the sequence template with merge fields).
Published AI content is marked where Art. 50 applies; internal drafts carry the ✦ badge.

### 8. Forms and inputs

Operator: approve/edit/skip (Server Actions, optimistic UI, `version` check); knowledge
file editor (textarea, saved on blur, versioned); sequence editor (subject, body, steps);
integration connect (OAuth redirect, callback stores `token_ref`). Provider: apply-to-manage
(one button → platform claim request), knowledge editor. Provider, phase 2: campaign approve / edit / skip; product choose → Stripe Checkout redirect.
Family: toggles, stop, consent capture (checkbox + text stored verbatim as proof).

### 9. i18n

Copy in English; the reference instance needs Hungarian. Strings in a per-instance
dictionary; dates and times in the instance's locale; legal footers per market (CAN-SPAM
address vs Hungarian Act XLVIII wording).

### 10. URLs and SEO

business.direct's own URLs are private (console). Generated pages are the platform's
(`getyourfield.com/nyc/<activity>-<area>`), written through the connector with the
platform's template, `LocalBusiness` JSON-LD per provider (the reference instance already
does this), and only where R6 holds.

### 11. Media

Post media: the provider's card image (from the platform) or an upload to Blob; alt text
required; conversion keeps alpha; served resized (1080 × 1350 IG, 1200 × 630 FB).

### 12. Performance

Console: server-rendered lists, paginated at 50 providers; the providers table filters on
the server. Digest build is a job, never a request. Caps in Redis, O(1) per check.

### 13. Operations

Dashboards: outbox lag, sends per channel per day, cap checks (0 violations), stage
transitions per day, opt-outs. Runbooks in §9 of the architecture. Backups: Atlas daily,
Blob versioned. Data deletion: platform webhook → delete `families_prefs`, anonymise
`messages`, keep `consents` (legal hold) with the id hashed.


## Part C — the system blueprint: modules, drawings, contracts, the outbox, security, the worker, tests, operations

*Written 2026-09-20 (D37) from `architecture.md` (the ADRs), `architecture.md` (the
data model, the state machines, the jobs), `01g-research-real-system.md` (every service verified)
and the prototype (`../index.html`, `../assets/app.js`), which is the behavioural specification: every
screen, rule and state the prototype shows exists here as a module. This is the document a
developer builds from. It says **what module goes where, what it owns, what it calls, and how it
works** — in drawings, interfaces and pseudo code. The sprint plan with acceptance tests is
`delivery-plan.md`. Terms are the SSOT's (`business-logic.md`); rules are cited as R-numbers.*

### 1. How to read this

- §2 drawings: context → deployment → modules → the two pipelines (outbound, inbound) → the clip
  engine. §3 the repository layout. §4 the module catalogue (one entry per module: owns, reads,
  exposes, pseudo code). §5 data contracts. §6 the job table. §7 the outbox in full. §8 security.
  §9 configuration. §10 the media worker. §11 testing. §12 operations. §13 the prototype → module map.
- Pseudo code is TypeScript-shaped and omits imports, error types and logging; `db.x` is the
  Mongoose model for collection `x`; `redis` is Upstash; `now()` is UTC; every function that writes
  takes `platformId` from the caller's session or the job's instance loop.
- Invariants that never move: **nothing sends except the outbox (ADR-4)**; **the policy gate runs on
  every draft and every send (R26)**; **the cap is checked at enqueue and at send (ADR-3)**; **a child is
  an age, never a name (R24)**; **every message row carries its `why` and its policy basis**.

### 2. Drawings

#### 2.1 System context

```
                 ┌─────────────────────────┐        ┌──────────────────────────────┐
  Families ─────▶│ Your Field NYC           │        │ Channels                     │
  (web, e-mail,  │ (the platform, Next.js)  │        │ Instagram · Facebook · e-mail │
   push, SMS)    │ accounts · saves · cards │        │ push · SMS (later)            │
                 └───────┬─────────▲────────┘        └──────▲───────────┬───────────┘
                 reads   │         │ writes (keyed)   publishes │         │ comments, DMs,
                 catalog │         │ claims, pages,   replies   │         │ replies, STOP
                 & saves │         │ flags, push                │         │ (webhooks)
                 ┌───────▼─────────┴────────────────────────────┴─────────▼───────────┐
                 │ business.direct — the machine                                       │
                 │ policy gate · catalogue · pipeline · drafting · approvals · outbox   │
                 │ channels · sequences · campaigns · conversations · families · media  │
                 │ billing · pages · analytics · recommendations · knowledge            │
                 └──────▲──────────────────────▲──────────────────────▲───────────────┘
                        │ approves, edits,      │ approves its own,    │ pays (Stripe
                        │ configures policy     │ edits its files      │ Checkout)
                   Operator (ClassScout)    Providers (own view)   Stripe / Claude / Deepgram
```

#### 2.2 Deployment (what runs where)

```
 Vercel (Pro, us-east)                                   Fly.io (iad)             SaaS
 ┌───────────────────────────────────────────────┐      ┌──────────────────┐     ┌────────────┐
 │ business-direct  (Next.js 15, Node 22)         │      │ media-worker      │     │ MongoDB    │
 │  app/(console)   operator · provider · family  │      │ ffmpeg · Deepgram │◀───▶│ Atlas M0/M10│
 │  app/api/cron/*  ← Vercel Cron (13 schedules)  │ HTTP │ c2pa-node         │     ├────────────┤
 │  app/api/webhooks/{resend,meta,twilio,stripe,  │─────▶│ POST /clips       │     │ Upstash    │
 │                    platform}                   │◀─────│ callback → app    │     │ Redis      │
 │  app/api/health                                │      └──────────────────┘     ├────────────┤
 │  src/modules/*   (the machine)                 │                               │ Vercel Blob│
 └──────┬──────────────┬─────────────┬────────────┘                               ├────────────┤
        │ Mongoose     │ REST        │ SDK                                        │ Resend     │
        ▼              ▼             ▼                                            │ Meta Graph │
     Atlas          Upstash        Blob · Resend · Meta · Twilio · Stripe · Claude│ Twilio     │
                                                                                  │ Stripe     │
   Sentry ◀── exceptions from app + worker        Better Stack ──▶ GET /api/health│ Claude API │
                                                                                  └────────────┘
```

#### 2.3 Module map (inside `src/modules`; arrows = imports; nothing imports a channel except the outbox)

```
                       ┌──────────┐
                       │  policy  │  gate(feature, ctx) · record(platformId)
                       └────▲─────┘
        ┌───────────────────┼──────────────────────────────┐
        │                   │                              │
 ┌──────┴─────┐      ┌──────┴──────┐                ┌──────┴──────┐
 │ catalogue  │      │  drafting   │                │  families   │
 │ connector  │─────▶│ drafter ·   │                │ prefs ·     │
 │ sync · diff│      │ patternGuard│                │ consents ·  │
 └──┬─────┬───┘      └──────┬──────┘                │ stop        │
    │     │                 │                        └──────┬──────┘
    │  ┌──▼────────┐  ┌─────▼──────┐  ┌───────────┐  ┌──────▼──────┐  ┌───────────┐
    │  │ pipeline  │  │ approvals  │  │ sequences │  │  campaigns  │  │conversations│
    │  │ stages ·  │  │ actions ·  │  │ step      │  │ draft ·     │  │ inbound ·  │
    │  │ score     │  │ autoApprove│  │           │  │ audience    │  │ answers    │
    │  └──┬────────┘  └─────┬──────┘  └─────┬─────┘  └──────┬──────┘  └─────┬──────┘
    │     │                 │               │               │               │
    │     └─────────────────┴───────────────┴───────┬───────┴───────────────┘
    │                                               │ enqueue(msg)
    │                                        ┌──────▼──────┐
    │                                        │   outbox    │  enqueue · send · caps · sendingGuard
    │                                        └──────┬──────┘
    │                                               │ adapter.publish
    │                                        ┌──────▼──────┐
    │                                        │  channels   │  resend · meta · twilio · platformPush
    │                                        └─────────────┘
    │
    ├──▶ pages (generate · publish via connector)      media (clips → worker · credentials · consent)
    ├──▶ billing (products · stripe · entitlements)     knowledge (files, versions)
    └──▶ analytics (events · metrics · assumptions · experiments) ◀── every module emits events
         recommend (home · runSafe)  reads pipeline, approvals, policy, sequences, analytics
```

#### 2.4 The outbound pipeline (every message, every channel)

```
 job or webhook ─▶ draft ─▶ patternGuard ─▶ policy.gate('draft') ─▶ drafts{waiting}
                                                                        │
                                            operator / provider approves│ (or autoApprove, R25)
                                                                        ▼
                          approvals{approve|edit|skip} ─▶ drafts{scheduled} ─▶ outbox.enqueue
                                                                                   │
                     ┌─────────────────────────────────────────────────────────────┘
                     ▼
 outbox{queued} ── cap check #1 (Redis, R3) ── consent check (R4) ── policy.gate('send') ── sendingGuard (R23)
                     │ any refusal → outbox{refused, reason}; the card shows why
                     ▼
 cron send (1/min, lock) ─▶ cap check #2 ─▶ adapter.publish ─▶ messages{sent, why, policy_basis}
                                   │                                  │
                                   │ error → attempts++, backoff       └─▶ blob snapshot (posts) · events
                                   └─▶ attempts ≥ 5 → outbox{dead}, alert
```

#### 2.5 The inbound pipeline (every reply, comment, DM, STOP, payment)

```
 Resend email.received ─┐
 Meta comments/messages ─┼─▶ /api/webhooks/{x} ─▶ verify signature ─▶ idempotency (Redis SET NX)
 Twilio inbound SMS ─────┤                                                     │
 Stripe events ──────────┤                                                     ▼
 Platform message ───────┘                                    channels[x].onInbound(payload) → InboundMessage
                                                                               │
                        ┌──────────────────────────────────────────────────────┤
                        ▼                          ▼                           ▼
                 STOP / unsubscribe        reply to a sequence         comment · DM · enquiry
                 families.stop /           threads + pipeline          conversations.inbound
                 optOuts (same tx)         stage → replied             → draft-answers (≤ 1 min, R14)
                                                   │                           │
                                                   └──────────▶ drafts{waiting} ◀┘   (the outbound pipeline again)
```

#### 2.6 The clip engine (D28, R30, R34, R20)

```
 provider uploads recording ─▶ Blob (private) ─▶ media.consent: showsChildren? ── no consent → refuse,
                                                                 │                  offer coach-only / place-only
                                                                 ▼ consent_ref
                                          POST worker /clips {blobUrl, listing, consent_ref, profile:'reels'}
                                                                 │
        worker: download → Deepgram (word timestamps) → moments (§10) → ffmpeg cut 9:16 + burn captions
                → c2pa sign → upload clips + .vtt to Blob → callback /api/media/callback {clips[]}
                                                                 │
                                        app: media_assets{generated:false, credential} → one draft per clip
                                             (media.kind='real', consent attached) → drafts{waiting}
```

#### 2.7 Draft state machine (unchanged from `architecture.md` §4; the outbox adds its own)

```
 drafts:   waiting ──approve──▶ scheduled ──publish──▶ sent
             │  └──edit──▶ waiting (ai=false)         └──fail×5──▶ failed
             └──skip──▶ skipped
 outbox:   queued ──checks ok──▶ sending ──2xx──▶ sent
             │  └──refused (cap · consent · gate · guard)──▶ refused
             └──error──▶ queued (attempts+1, next_at = backoff) ──attempts≥5──▶ dead
```

### 3. Repository layout (one Next.js app, one worker, one package of pure rules)

```
business-direct/                      # new repository, sibling of the platform (ADR-1)
  app/
    (console)/
      platform/[screen]/page.tsx      # home overview social sales approvals providers pages
                                      # intelligence economics integrations policy templates knowledge help
      provider/[screen]/page.tsx      # today conversations campaigns media results knowledge
      family/prefs/[token]/page.tsx   # signed link (ADR-6); inbox · saved · prefs
      layout.tsx                      # top bar: role · Simple/Advanced · persona (prototype parity)
    api/
      cron/[job]/route.ts             # one route, dispatches by job name; Vercel Cron calls it
      webhooks/resend/route.ts  meta/route.ts  twilio/route.ts  stripe/route.ts  platform/route.ts
      media/callback/route.ts         # the worker's callback (shared secret)
      health/route.ts
      auth/[...sso]/route.ts          # DoneIsBetter OIDC callback
  src/
    modules/                          # §4 — one folder per module, index.ts exports the public functions
      policy/ catalogue/ pipeline/ drafting/ approvals/ outbox/ channels/ sequences/ campaigns/
      conversations/ families/ media/ billing/ pages/ analytics/ recommend/ knowledge/
    db/                               # Mongoose models (12-technical-design §2) + zod schemas (§5)
    lib/                              # redis.ts blob.ts auth.ts ids.ts time.ts log.ts env.ts
    ui/                               # Mantine + GDS tokens (architecture.md); the prototype's components
  worker/                             # §10 — Dockerfile, server.ts, clips.ts, credentials.ts; deployed to Fly.io
  tests/                              # unit (rules), contract (connector fixtures), e2e (Playwright)
  vercel.json                         # crons (§6)
  fly.toml
```

Rules of the layout: a module's `index.ts` is its only public surface; `channels/*` is imported only
by `outbox` and the webhook routes (an ESLint `no-restricted-imports` rule enforces it — this is the
"a Server Action cannot send" test made static); `db/` is imported only by modules, never by pages;
pages call Server Actions in `modules/*/actions.ts`.

### 4. Module catalogue

Each entry: **Owns** (collections it writes), **Reads**, **Exposes** (its `index.ts`), **Rules**,
**Pseudo code** for the parts that are not obvious.

#### 4.1 `policy` — the record and the gate (ADR-14, R26)

Owns `policies`. Reads nothing else. Exposes `record(platformId)`, `gate(feature, ctx)`,
`basis(feature, ctx)`. Rules: R26 and every row of `responsible-data.md` §3.

```ts
type Feature = 'provider_email' | 'digest' | 'alerts' | 'audience_saves' | 'sms' | 'ai_draft' |
               'generated_media' | 'minor_field' | 'push' | 'clips_children' | 'safeguarding_claim' | 'any_draft';

const NEEDS: Record<Feature, (p: Policy, ctx) => string[]> = {   // returns the missing fields
  provider_email:  p => miss(p, ['postal_address', 'jurisdictions']),
  digest:          p => miss(p, ['channels.email']).concat(p.privacyPolicy.clauses.emailAlerts ? [] : ['privacyPolicy.clauses.emailAlerts']),
  alerts:          p => NEEDS.digest(p),
  audience_saves:  p => p.privacyPolicy.clauses.savesOptIn ? [] : ['privacyPolicy.clauses.savesOptIn'],
  sms:             p => (p.channels.sms === 'consent' && p.consentText.sms) ? [] : ['channels.sms', 'consentText.sms'],
  ai_draft:        p => p.aiDisclosure ? [] : ['aiDisclosure'],
  generated_media: p => NEEDS.ai_draft(p),
  minor_field:     (p, ctx) => (p.audienceModel !== 'adults' && !p.dpia.done) ? ['dpia'] : (ctx.field !== 'age' && p.childData === 'none') ? ['childData'] : [],
  push:            (p, ctx) => (p.audienceModel !== 'adults' && inQuietHours(ctx.at, p.minorsMarketing.pushQuietHours)) ? ['quietHours'] : [],
  clips_children:  (p, ctx) => ctx.consentRef ? [] : ['mediaConsent'],
  safeguarding_claim: () => ['never'],                      // R31: never claimed, only displayed as verified
  any_draft:       p => miss(p, ['darkPatterns', 'accessibility']),
};

export async function gate(feature: Feature, ctx: {platformId; at?; field?; consentRef?}): Promise<{ok: true} | {ok: false; missing: string[]}> {
  const p = await record(ctx.platformId);                   // cached 60 s in memory per instance
  const missing = NEEDS[feature](p, ctx);
  return missing.length ? {ok: false, missing} : {ok: true};
}
export function basis(feature, ctx) { /* the clause / consent / cap the send relies on → stored on messages.policy_basis */ }
```

The *Policy* screen renders `NEEDS` inverted: per field, the features it blocks (framework §3).

#### 4.2 `catalogue` — connector, sync, diff (ADR-2)

Owns `providers_cache`. Exposes `connector(platformId): PlatformConnector` (12-technical-design §6),
`sync(platformId)`, `providers(platformId, filter)`. Rules: the cache is never edited by hand.

```ts
export async function sync(platformId) {
  const c = connector(platformId);
  const remote = await c.listProviders();                                 // GET /api/public/providers, paged; ETag honoured
  const local = await db.providers_cache.find({platform_id: platformId}).lean();
  const byId = index(local, '_id');
  for (const r of remote) {
    const prev = byId.get(r.id);
    const doc = mapProvider(r, platformId);                              // 12-technical-design §3
    if (!prev) { await db.providers_cache.create(doc); await events.emit('provider.new', {provider_id: r.id}); await pipeline.ensure(r.id, platformId); continue; }
    const changes = diff(prev, doc, ['sessions', 'trial', 'announcement', 'registration', 'email', 'phone', 'claimed']);
    if (changes.length) { await db.providers_cache.replaceOne({_id: r.id}, doc); await events.emit('provider.changed', {provider_id: r.id, changes}); }
    if (changes.includes('sessions')) await events.emit('provider.new_session', {provider_id: r.id});   // → families.alerts, drafting
    if (changes.includes('claimed') && doc.claimed) await pipeline.setStage(r.id, 'managing', 'platform confirmed');
  }
  await db.sync_runs.create({platform_id: platformId, at: now(), count: remote.length});   // /api/health reads the last one
}
```

`YourFieldConnector` maps the twelve public endpoints found in `first-customer-classscout.md`; keyed writes
(`createClaimRequest`, `notifyFamily`, `publishPage`, `savesFor`, `familiesNear`, `setCardFlag`) throw
`NotKeyed` until `integrations.platform.key` exists (P-7), and every caller handles `NotKeyed` by
writing a task for the operator, never by failing silently.

#### 4.3 `pipeline` — stages and the propensity score (ADR-13)

Owns `provider_state`. Exposes `ensure`, `setStage(providerId, to, by)`, `score(providerId)`,
`byStage(platformId, stage)`. Rules: forward moves are event-driven only (technical design §4);
the operator's override is logged; the score is the prototype's `score(p)` verbatim.

```ts
const FORWARD = { identified: ['contacted'], contacted: ['replied'], replied: ['applied'], applied: ['managing'], managing: ['upgraded'] };
export async function setStage(providerId, to, by, opts = {override: false}) {
  const s = await db.provider_state.findOne({provider_id: providerId});
  if (!FORWARD[s.stage]?.includes(to) && !opts.override) throw new IllegalMove(s.stage, to);
  await db.provider_state.updateOne({provider_id: providerId, version: s.version}, {$set: {stage: to, stage_changed_at: now(), stage_changed_by: by}, $inc: {version: 1}});
  await db.stage_history.create({provider_id: providerId, from: s.stage, to, by, override: opts.override, at: now()});
  await events.emit('stage.changed', {provider_id: providerId, from: s.stage, to, by});
}
export function score(p: Provider, st: ProviderState): number {           // 0–100, nightly (ADR-13)
  let s = 0;
  s += p.email ? 25 : 0;  s += p.phone ? 10 : 0;  s += p.nextSession ? 20 : 0;  s += p.trial ? 15 : 0;
  s += Math.min(p.savesCount ?? 0, 10) * 2;  s += p.photos >= 3 ? 5 : 0;  s += p.contactKind === 'role' ? 5 : 0;
  return Math.min(100, s);
}
```

#### 4.4 `drafting` — the drafter, the templates, the pattern guard (ADR-7, R10, R14, R32, R36)

Owns `drafts`. Reads `knowledge_files`, `providers_cache`, `policies`. Exposes
`draft(kind, ctx): Draft`, `patternGuard(text): Violation[]`, `templates`. The `Drafter` interface
has two implementations: `ClaudeDrafter` and `TemplateDrafter` (the listing's own text; used when
the department's AI switch is off — the machine works without AI).

```ts
interface Drafter { draft(kind: DraftKind, ctx: DraftContext): Promise<{copy: string; why: string; ai: boolean; ai_meta?: {model; prompt_version}}> }

export async function draft(kind, ctx) {
  const dept = await knowledge.department(ctx.platformId, kind);                           // ai switch per department (R10)
  const gate = await policy.gate('any_draft', ctx);  if (!gate.ok) return refuse(gate.missing);
  const d = dept.ai ? claudeDrafter : templateDrafter;
  if (dept.ai) { const g = await policy.gate('ai_draft', ctx); if (!g.ok) return refuse(g.missing); }
  const out = await d.draft(kind, {...ctx, files: await knowledge.filesFor(ctx)});          // voice.md, rules/*.md, the card
  const violations = patternGuard(out.copy);                                                // R32, R36 banned list; R34 checks
  if (violations.length) { await events.emit('draft.refused', {kind, violations}); return refuse(violations.map(v => v.pattern)); }
  return db.drafts.create({...ctx.ids, kind, copy: out.copy, why: out.why, ai: out.ai, ai_meta: out.ai_meta, state: 'waiting', created_by: 'machine', platform_id: ctx.platformId});
}

const BANNED: [RegExp, string][] = [
  [/\b(today only|last chance|only \d+ (spots|places) left|hurry|don'?t miss out)\b/i, 'false urgency or scarcity'],
  [/\b(are you sure you want to miss|no thanks, i (don'?t|do not) want)\b/i, 'confirmshaming'],
  [/\b(limited time|ends (tonight|soon))\b/i, 'false urgency'],
];
export function patternGuard(text) {
  const v = BANNED.filter(([re]) => re.test(text)).map(([, pattern]) => ({pattern}));
  if (/\b(bereave|can'?t afford|not now|please stop)\b/i.test(text)) v.push({pattern: 'pressure on a stated vulnerability'});   // never in OUR copy
  if (text.length > 0 && !/https?:\/\//.test(text) && /\[link\]/.test(text)) v.push({pattern: 'unresolved link'});
  return v;
}
```

`ClaudeDrafter` calls the Messages API with the knowledge files as a cached system prompt, the card
as the user turn, `max_tokens: 400`, and stores `ai_meta`. Nightly batch kinds (`social`,
`campaign`) go through the Batch API; `answer` (a reply within a minute, R14) goes live.

#### 4.5 `approvals` — the human gate and earned auto-approval (R1, R25)

Owns `approvals`, `auto_approval`. Exposes Server Actions `approve(draftId)`, `edit(draftId, copy)`,
`skip(draftId)`, `approveBatch(ids)` and the job `autoApprove`. Rules: an edit sets `ai=false` and
stores the diff; auto-approval is earned after four clean weeks per department and lost on an edit or
a complaint.

```ts
export async function approve(draftId, by) {
  const d = await db.drafts.findOneAndUpdate({_id: draftId, state: 'waiting'}, {$set: {state: 'scheduled', scheduled_for: d.scheduled_for ?? nextSlot(d)}}, {new: true});
  if (!d) throw new Conflict();
  await db.approvals.create({draft_id: draftId, action: 'approve', by, at: now()});
  await outbox.enqueue(fromDraft(d, by));                    // the only way out; enqueue re-runs the checks
}
export async function autoApprove(platformId) {             // job: on draft (called by drafting after create)
  for (const a of await db.auto_approval.find({platform_id: platformId, earned_at: {$ne: null}, revoked_at: null}))
    for (const d of await db.drafts.find({platform_id: platformId, state: 'waiting', kind: a.department}))
      await approve(d._id, `auto:${a.department}`);        // logged as auto; a family's Stop still cancels in the outbox
}
```

#### 4.6 `outbox` — see §7 (the full pseudo code)

Owns `outbox`, `messages`. Exposes `enqueue(msg)`, `cancelFor(familyId)`, and the job `send`.

#### 4.7 `channels` — one adapter per channel (12-technical-design §6)

Owns nothing. Exposes `adapters[channel]: ChannelAdapter`. Imported only by `outbox` and the webhook
routes. Each adapter: `preview`, `publish`, `verify`, `onInbound`.

```ts
// resend.ts
publish: async (m) => resend.emails.send({from: m.from, to: m.to, subject: m.subject, html: m.html, text: m.text,
   headers: {'List-Unsubscribe': `<${m.unsubscribeUrl}>`, 'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click'}, tags: [{name: 'message_id', value: m.id}]}).then(r => ({providerMessageId: r.id})),
verify: (req) => svix.verify(rawBody, headers, RESEND_WEBHOOK_SECRET),
onInbound: (evt) => evt.type === 'email.received' ? {kind: 'reply', channel: 'email', from: evt.data.from, text: stripQuoted(evt.data.text), inReplyTo: evt.data.headers['in-reply-to']} :
           evt.type === 'email.bounced' ? {kind: 'bounce', to: evt.data.to} : evt.type === 'email.complained' ? {kind: 'complaint', to: evt.data.to} : null,

// meta.ts  (Instagram + Facebook Page)
publish: async (m) => {
  const token = await integrations.token(m.platformId, 'meta');                       // long-lived page token, refreshed by the `tokens` job
  if (m.channel === 'instagram') {
    const body = m.media.kind === 'video' ? {media_type: 'REELS', video_url: m.media.url, caption: m.copy} : {image_url: m.media.url, caption: m.copy};
    const {id: container} = await graph.post(`/${igUserId}/media`, body, token);
    await until(async () => (await graph.get(`/${container}?fields=status_code`, token)).status_code === 'FINISHED', {every: 5_000, max: 240_000});
    const {id} = await graph.post(`/${igUserId}/media_publish`, {creation_id: container}, token);
    return {providerMessageId: id};
  }
  const {id} = await graph.post(`/${pageId}/${m.media ? (m.media.kind === 'video' ? 'videos' : 'photos') : 'feed'}`, {message: m.copy, url: m.media?.url}, token);
  return {providerMessageId: id};
},
verify: (req) => hmacSha256(META_APP_SECRET, rawBody) === req.headers['x-hub-signature-256'].slice(7),
onInbound: (evt) => flatten(evt.entry).map(ch => ch.field === 'comments' ? {kind: 'comment', external_id: ch.value.id, post_id: ch.value.media.id, from: ch.value.from.username, text: ch.value.text}
                                             : ch.field === 'messages' ? {kind: 'dm', ...} : null).filter(Boolean),
reply: (commentId, text) => graph.post(`/${commentId}/replies`, {message: text}, token),

// twilio.ts   publish only when policy.gate('sms') ok and a consents row exists (checked in outbox); onInbound handles STOP → families.stop
// platformPush.ts   publish → connector.notifyFamily (keyed; NotKeyed → operator task)
```

The Meta webhook route also answers the verification `GET` (`hub.mode=subscribe`, `hub.verify_token`,
returns `hub.challenge`).

#### 4.8 `sequences` — the three-touch sales sequence (D28, R23, Q2)

Owns `sequences`. Reads `provider_state`, `providers_cache`, `opt_outs`, `sending`. Exposes the editor's
Server Actions and the job `sequenceStep`. Rules: the template must contain `{postal_address}` and the
opt-out footer or it cannot be approved (BD-1-12); step 2 only where a save exists; recipients in
score order; phone-only providers become call tasks.

```ts
export async function sequenceStep(platformId) {                                       // 09:00 weekdays
  const g = await policy.gate('provider_email', {platformId});  if (!g.ok) return skip('gate', g.missing);
  for (const seq of await db.sequences.find({platform_id: platformId, state: 'approved'})) {
    const excluded = new Set((await db.opt_outs.find({platform_id: platformId})).map(o => o.provider_id));
    const recipients = (await pipeline.byStage(platformId, ['identified', 'contacted']))
      .filter(r => !excluded.has(r.provider_id)).sort((a, b) => b.score - a.score);         // propensity order (ADR-13)
    for (const r of recipients) {
      const p = await catalogue.get(r.provider_id);
      if (!p.email) { await tasks.upsert({kind: 'call', provider_id: p.id, why: 'phone-only'}); continue; }
      const lastStep = await db.messages.findOne({provider_id: p.id, kind: 'sequence'}, {sort: {sent_at: -1}});
      const next = lastStep ? seq.steps.find(s => s.n === lastStep.step + 1) : seq.steps[0];
      if (!next || (lastStep && daysSince(lastStep.sent_at) < next.delay_days)) continue;
      if (next.n === 2 && !(p.savesCount > 0)) continue;                                   // step 2 needs a save
      if (lastStep && await threads.hasReply(p.id)) continue;                              // replied → stage replied, sequence stops
      await outbox.enqueue({platformId, kind: 'sequence', step: next.n, channel: 'email', to: {provider_id: p.id, email: p.email},
        subject: merge(next.subject, p), html: merge(next.body, p, {postal_address: (await sending.get(platformId)).postal_address}),
        why: `step ${next.n} of ${seq.name}; score ${r.score}`, by: `sequence:${seq._id}`});
      if (next.n === 1) await pipeline.setStage(p.id, 'contacted', 'sequence step 1');
    }
  }
}
```

#### 4.9 `campaigns` — provider campaigns, audiences from the platform only (ADR-10, R3, R11)

Owns `campaigns`. Reads `providers_cache`, `entitlements`, `families_prefs`. Exposes the provider's
Server Actions and the jobs `draftCampaigns` (08:30) and `sendCampaigns` (5 min).

```ts
export async function draftCampaigns(platformId) {
  for (const p of await pipeline.byStage(platformId, ['managing', 'upgraded'])) {
    const card = await catalogue.get(p.provider_id);
    for (const kind of kindsFor(card))                                                   // trial · new_session · announcement · registration (09-business-logic §4)
      if (!(await db.campaigns.exists({provider_id: p.provider_id, kind, state: 'waiting'})))
        await drafting.draft('campaign', {platformId, provider_id: p.provider_id, kind, card, audience_rule: 'saved'});
  }
}
export async function sendCampaigns(platformId) {
  const g = await policy.gate('audience_saves', {platformId});
  for (const c of await db.campaigns.find({platform_id: platformId, state: 'scheduled', scheduled_for: {$lte: now()}})) {
    if (!g.ok) { await db.campaigns.updateOne({_id: c._id}, {$set: {audience_count: 0, note: `blocked: ${g.missing}`}}); continue; }
    const audience = await resolveAudience(c);                                            // savesFor(provider) [+ familiesNear(geo, ageBand)] — keyed
    await db.campaigns.updateOne({_id: c._id}, {$set: {audience_count: audience.length, state: 'sending'}});
    for (const f of audience)
      await outbox.enqueue({platformId, kind: 'campaign', campaign_id: c._id, channel: pickChannel(f.prefs), to: {family_id: f.id},
        copy: c.copy, why: `you saved ${c.provider_name}` /* the reason line, R11 */, provider_id: c.provider_id, by: `campaign:${c._id}`});
    await db.campaigns.updateOne({_id: c._id}, {$set: {state: 'sent'}});
  }
}
async function resolveAudience(c) {                                                       // never an uploaded list (ADR-10)
  const conn = catalogue.connector(c.platform_id);
  const saved = await conn.savesFor(c.provider_id);                                       // opted-in accounts only (D31)
  const near = c.audience_rule === 'saved+nearby' ? await conn.familiesNear(card.geo, card.ageBand) : [];
  return uniqBy([...saved, ...near], 'id').filter(f => !f.stopped);                       // R33: nothing but saves and the family's chosen neighbourhood
}
```

#### 4.10 `conversations` — enquiries, comments, DMs, drafted answers (phase 3, R14)

Owns `enquiries`, `comments`, `threads`. Exposes `inbound(msg: InboundMessage)` (called by the webhook
routes after `onInbound`), the provider's Server Actions, and `draftAnswers` (on inbound).

```ts
export async function inbound(m: InboundMessage, platformId) {
  if (m.kind === 'stop' || m.kind === 'unsubscribe') return families.stop(m.from, platformId, m.channel);
  if (m.kind === 'bounce' || m.kind === 'complaint') return sending.record(platformId, m);          // R23 guard input
  if (m.kind === 'reply') {                                                                          // to a sequence
    const p = await catalogue.byEmail(platformId, m.from);  if (!p) return threads.orphan(m);
    if (/not my program/i.test(m.text)) return optOuts.add(platformId, p.id, 'not_mine');           // R: excluded forever (BD-1-7)
    await threads.append(p.id, {from: 'them', channel: 'email', text: m.text, at: now()});
    await pipeline.setStage(p.id, 'replied', 'reply received');
    await classify(m.text).then(c => c.vulnerable && families.pause(p.id, 'stated vulnerability'));   // R32 pause + human task
    return drafting.draft('answer', {platformId, provider_id: p.id, thread: await threads.get(p.id)});
  }
  if (m.kind === 'comment' || m.kind === 'dm') {
    const post = await db.messages.findOne({provider_message_id: m.post_id});
    const row = await db.comments.create({platform_id: platformId, post_id: m.post_id, provider_id: post?.provider_id, channel: m.channel, external_id: m.external_id, from: m.from, text: m.text, state: 'waiting'});
    return drafting.draft('comment_reply', {platformId, comment_id: row._id, listingUrl: post?.listing_url});
  }
  if (m.kind === 'enquiry') {                                                                        // platform message · missed call
    const row = await db.enquiries.create({...m, platform_id: platformId, state: 'waiting', from: {name: m.from.name, kid: m.from.kidAge /* an age, never a name — R24 */, area: m.from.area}});
    return drafting.draft('answer', {platformId, provider_id: m.provider_id, enquiry_id: row._id});
  }
}
```

`classify` runs Haiku 4.5 with a fixed prompt returning `{vulnerable: bool, intent: 'yes'|'later'|'no'|'question'}`
and is stored on the thread; a sensitive category in the text (R35: health, hardship) is answered
and never written as a field — the prompt is told to return only the two flags.

#### 4.11 `families` — preferences, consents, digest, alerts, Stop (ADR-6, R3, R4, R28)

Owns `families_prefs`, `consents`. Exposes `prefsLink(familyId)`, the family's Server Actions,
`stop`, `pause`, and the jobs `digest` (Sunday 17:00 build / 18:00 send) and `alerts` (on
`provider.new_session`). Rules: high-privacy defaults; the digest and alerts do not count toward
the provider cap; Stop cancels queued work in the same transaction.

```ts
export async function stop(familyRef, platformId, channel?) {
  const session = await mongoose.startSession();
  await session.withTransaction(async () => {
    const f = await db.families_prefs.findOne({family_id: familyRef.family_id, platform_id: platformId}).session(session);
    const prefs = channel ? {...f.prefs, [channel]: false} : {picks: false, alerts: false, nearby: false, sms: false};
    await db.families_prefs.updateOne({_id: f._id}, {$set: {prefs, stopped_at: channel ? f.stopped_at : now()}}).session(session);
    await db.consents.create([{family_id: f.family_id, channel: channel ?? 'all', text: 'STOP', captured_at: now(), source: 'inbound', revoked_at: now()}], {session});
    await outbox.cancelFor(f.family_id, channel, session);                                          // queued rows → refused('stopped')
  });
  await events.emit('family.stopped', {family_id: familyRef.family_id, channel});
}
export async function digest(platformId, phase: 'build' | 'send') {
  const g = await policy.gate('digest', {platformId});  if (!g.ok) return skip('gate', g.missing);
  if (phase === 'build')
    for (const f of await db.families_prefs.find({platform_id: platformId, 'prefs.picks': true, stopped_at: null})) {
      const saved = await catalogue.many(f.saved);                                                 // mirror of the platform's saves (opted-in)
      const near = f.prefs.nearby ? await catalogue.withSessionNextWeek(platformId, f.area, agesOf(f)) : [];
      const rows = pickDigestRows(saved, near, 6);  if (!rows.length) continue;
      await drafting.draft('digest', {platformId, family_id: f.family_id, rows});                  // TemplateDrafter; the digest is not AI
    }
  else
    for (const d of await db.drafts.find({platform_id: platformId, kind: 'digest', state: 'waiting'}))
      await outbox.enqueue({...fromDraft(d), channel: 'email', countsTowardCap: false /* R3 */, why: 'your Sunday picks (you turned on picks)'});
}
export async function alerts(evt: {provider_id}, platformId) {
  const g = await policy.gate('alerts', {platformId});  if (!g.ok) return;
  for (const f of await db.families_prefs.find({platform_id: platformId, saved: evt.provider_id, 'prefs.alerts': true, stopped_at: null}))
    await outbox.enqueue({platformId, kind: 'alert', channel: 'push', to: {family_id: f.family_id}, countsTowardCap: false, copy: alertCopy(evt), why: 'new session at a provider you saved', by: 'alerts'});
}
```

Preference pages are reached by a signed link (`/family/prefs/[token]`, HMAC over `family_id +
exp`, 30-day expiry, issued by the platform's account page or by every message's footer). A family
record holds `kids: [{age}]` only — the Zod schema has no name field, so one cannot be added by
accident (R24, gate `minor_field`).

#### 4.12 `media` — the clip engine's app side, consent, credentials (D28, ADR-12, R15, R20, R30, R34)

Owns `media_assets`. Exposes the provider's upload Server Action, `requestClips(recordingId)`,
`onWorkerCallback(payload)`, `MediaAdapter` (v1: `clips` only; `image`/`video`/`audio` throw
`NotEnabled` until a vendor is configured and `aiDisclosure` is set).

```ts
export async function requestClips(recordingId, by) {
  const r = await db.media_assets.findById(recordingId);
  if (r.shows_children && !r.consent_ref) throw new NeedsConsent(['coach-only', 'place-only']);   // R30, enforced here and in the worker
  const g = await policy.gate('clips_children', {platformId: r.platform_id, consentRef: r.consent_ref});  if (!g.ok) throw new Blocked(g.missing);
  const job = await db.media_jobs.create({recording_id: r._id, state: 'sent', at: now()});
  await fetch(`${WORKER_URL}/clips`, {method: 'POST', headers: {authorization: `Bearer ${WORKER_TOKEN}`},
    body: JSON.stringify({job_id: job._id, blob_url: await blob.signedUrl(r.blob_key, 3600), listing: await catalogue.get(r.provider_id),
      consent_ref: r.consent_ref ?? null, cut: 'full', profile: 'reels', callback: `${APP_URL}/api/media/callback`})});
}
export async function onWorkerCallback(p) {                                                   // verified by shared secret
  for (const c of p.clips) {
    const asset = await db.media_assets.create({platform_id: p.platform_id, provider_id: p.provider_id, adapter: 'clips', generated: false,
      credential: c.c2pa_manifest_id, blob_url: c.url, captions_url: c.vtt_url, duration_s: c.duration, consent_ref: p.consent_ref});
    await drafting.draft('social', {platformId: p.platform_id, provider_id: p.provider_id, media: {kind: 'real', asset_id: asset._id}, moment: c.moment_text});
  }
  await db.media_jobs.updateOne({_id: p.job_id}, {$set: {state: 'done'}});
}
```

#### 4.12b `retention` — reduce churn (D41, R37)

Owns nothing new (drafts of kind `retain` in `drafts`; kept / lost in `events`). Reads
`provider_state`, `entitlements`, `providers_cache`, `enquiries`, `families_prefs.saved`. Exposes
the job `retention` (nightly 03:30) and `atRisk(platformId)` for the screen and the recommendations.

```ts
export async function retention(platformId) {
  for (const st of await pipeline.byStage(platformId, ['managing', 'upgraded'])) {
    const p = await catalogue.get(st.provider_id), ent = await db.entitlements.findOne({provider_id: p.id, until: null});
    const signals = [];
    if (ent && daysUntil(ent.renews_at) <= 14) signals.push({kind: 'renewal', at: ent.renews_at});
    if (daysSince(p.updatedAt) >= 30) signals.push({kind: 'stale'});
    if (await db.enquiries.exists({provider_id: p.id, state: 'waiting', received_at: {$lt: hoursAgo(48)}})) signals.push({kind: 'unanswered'});
    if ((await db.events.countDocuments({name: 'save', provider_id: p.id, at: {$gt: daysAgo(30)}})) === 0) signals.push({kind: 'no_saves'});
    for (const s of signals)
      if (!(await db.drafts.exists({kind: 'retain', provider_id: p.id, 'props.signal': s.kind, state: {$in: ['waiting', 'scheduled']}})))
        await drafting.draft('retain', {platformId, provider_id: p.id, signal: s, numbers: await results.forProvider(p.id, 90)});   // the advertiser's own numbers; never a discount (R13, R37)
  }
}
// kept / lost: onStripeEvent → events 'retention.kept' (renewed after a retain touch within 30 d) | 'retention.lost' (subscription.deleted); metrics() rolls them into churn and churnSaved
```

#### 4.13 `billing` — products, Stripe Checkout, entitlements (ADR-9, R32 cooling-off)

Owns `products`, `entitlements`. Exposes the provider's `checkout(productId)` Server Action, the
webhook handler `onStripeEvent`, `cancelWithinCoolingOff`.

```ts
export async function checkout(productId, providerId, platformId) {
  const prod = await db.products.findOne({platform_id: platformId, id: productId});
  const s = await stripe.checkout.sessions.create({mode: 'subscription', line_items: [{price: prod.stripe_price_id, quantity: 1}],
    client_reference_id: `${platformId}:${providerId}:${productId}`, success_url: `${APP_URL}/provider/results?upgraded=1`, cancel_url: `${APP_URL}/provider/today`,
    subscription_data: {metadata: {platform_id: platformId, provider_id: providerId, product_id: productId}}});
  return s.url;                                                                                 // the card is never seen by the machine
}
export async function onStripeEvent(evt) {                                                      // idempotent on evt.id (Redis SET NX)
  const md = evt.data.object.metadata ?? parseRef(evt.data.object.client_reference_id);
  switch (evt.type) {
    case 'checkout.session.completed':
    case 'customer.subscription.updated': {
      const sub = evt.data.object;  if (sub.status !== 'active' && sub.status !== 'trialing') return;
      const first = !(await db.entitlements.exists({provider_id: md.provider_id, platform_id: md.platform_id}));
      await db.entitlements.updateOne({stripe_subscription_id: sub.id}, {$set: {...md, since: new Date(sub.current_period_start * 1000), until: null}}, {upsert: true});
      if (first) await pipeline.setStage(md.provider_id, 'upgraded', 'stripe: first active');
      await catalogue.connector(md.platform_id).setCardFlag(md.provider_id, (await db.products.findOne({id: md.product_id})).card_flag, true).catch(notKeyedTask);
      await events.emit('upgrade.active', {...md, amount: sub.plan.amount});  break;
    }
    case 'customer.subscription.deleted': await db.entitlements.updateOne({stripe_subscription_id: evt.data.object.id}, {$set: {until: now()}}); await setCardFlag(false); break;
    case 'invoice.payment_failed': await tasks.upsert({kind: 'payment_failed', provider_id: md.provider_id}); break;
  }
}
```

#### 4.14 `pages` — generated neighbourhood × activity pages written to the platform (ADR-8)

Owns `generated_pages`. Reads `providers_cache`, `assumptions` (readiness). Exposes the operator's
`generate(activity, area)` and `publish(pageId)`; rules: ≥ 3 providers; readiness ≥ 3 of 4
(BD-4-11); JSON-LD `ItemList`; published only through `connector.publishPage` (keyed).

#### 4.15 `analytics` — events, nightly metrics, assumptions, the experiment (ADR-11, R16–R19)

Owns `events`, `metrics_daily`, `assumptions`, `experiments`. Exposes `events.emit(name, props)`,
the jobs `metrics` (02:00) and `score` (02:30), and the economics screen's reader.

```ts
export async function metrics(platformId, day = yesterday()) {
  const e = await db.events.find({platform_id: platformId, at: within(day)}).lean();
  const n = countBy(e, 'name');                                                                 // sequence.sent, reply.received, stage.changed→applied, upgrade.active, digest.opened, …
  const rates = {
    reply:   ratio(n['reply.received'], n['sequence.sent']),  apply: ratio(n['stage.applied'], n['reply.received']),
    managing: ratio(n['stage.managing'], n['stage.applied']),  upgrade: ratio(n['upgrade.active'], n['stage.managing']),
  };
  for (const [key, r] of Object.entries(rates))                                                 // R16: assumption → measured at 100 observations
    if (r.n >= 100) await db.assumptions.updateOne({platform_id: platformId, key: `rate.${key}`}, {$set: {value: r.value, source: 'measured', updated_at: now()}}, {upsert: true});
  const a = await assumptions.all(platformId);                                                   // the 24 inputs of the economics model (16-analytics §2)
  const cac = econ.cac(a), ltv = econ.ltv(a);                                                    // the prototype's econ() verbatim
  await db.metrics_daily.replaceOne({platform_id: platformId, day}, {platform_id: platformId, day, rates, cac_managing: cac.managing, cac_upgraded: cac.upgraded, ltv, payback: econ.payback(a),
    avid_families: await families.avidCount(platformId), avid_value: econ.avidValue(a), content_cpa: econ.contentCpa(a, n), next_dollar: econ.nextDollar(a)}, {upsert: true});
  await auditDelivery(platformId, day);                                                          // R33: sends per neighbourhood vs audience share; flags > 1.5× skew
}
```

#### 4.16 `recommend` — the Simple mode's Home and the one safe press (D33, R29)

Owns nothing. Reads approvals, pipeline, policy, sequences, sending, analytics. Exposes
`home(platformId): Recommendation[]` and the Server Action `runSafe(ids)`. The list and the `auto`
flag are the prototype's `recommend()` verbatim: approvals of posts and clips, the invitation when
the gate allows, filing the radar note are `auto: true`; replies and judgement calls are never.

```ts
export async function runSafe(ids, by, platformId) {
  const recs = (await home(platformId)).filter(r => ids.includes(r.id) && r.auto);                 // a non-auto id is ignored, never run
  for (const r of recs) { await r.run(by); await events.emit('recommendation.run', {id: r.id, by}); }   // each logged as the operator's decision
  return recs.map(r => r.id);
}
```

#### 4.17 `knowledge` — the knowledge files (R10)

Owns `knowledge_files`. Exposes `filesFor(ctx)` (platform files + the provider's files), the editors'
Server Actions with versions, `department(platformId, kind)` (the AI switch). Files are the prompt
context; every edit is versioned; a provider edits only its own.

### 5. Data contracts (Zod at every boundary; Mongoose models mirror them)

```ts
export const OutboxRow = z.object({
  _id: z.string(), platform_id: z.string(), kind: z.enum(['sequence', 'answer', 'comment_reply', 'social', 'campaign', 'digest', 'alert', 'sms']),
  channel: z.enum(['email', 'instagram', 'facebook', 'push', 'sms']),
  to: z.object({family_id: z.string().optional(), provider_id: z.string().optional(), email: z.string().email().optional(), channel_account: z.string().optional()}),
  copy: z.string(), subject: z.string().optional(), html: z.string().optional(), media: z.object({kind: z.enum(['image', 'video']), url: z.string().url(), asset_id: z.string()}).optional(),
  draft_id: z.string().optional(), campaign_id: z.string().optional(), step: z.number().optional(), provider_id: z.string().optional(),
  why: z.string().min(1),                                   // the reason line — never empty
  by: z.string().min(1),                                    // who approved: a person's id, `auto:<department>`, `sequence:<id>`
  countsTowardCap: z.boolean().default(true),               // false for the platform's own digest and alerts (R3)
  state: z.enum(['queued', 'sending', 'sent', 'refused', 'dead']).default('queued'),
  attempts: z.number().int().default(0), next_at: z.date(), refused_reason: z.string().optional(),
  policy_basis: z.object({feature: z.string(), clause: z.string().optional(), consent_id: z.string().optional(), cap: z.string().optional()}).optional(),
  created_at: z.date(),
});
export const FamilyPrefs = z.object({
  family_id: z.string(), platform_id: z.string(),
  prefs: z.object({picks: z.boolean().default(false), alerts: z.boolean().default(false), nearby: z.boolean().default(false), sms: z.boolean().default(false)}),   // R28 all off
  kids: z.array(z.object({age: z.number().int().min(0).max(17)})).max(6),   // an age, never a name (R24) — no other field exists
  area: z.string().optional(), saved: z.array(z.string()).default([]), stopped_at: z.date().nullable().default(null), paused_until: z.date().nullable().default(null), version: z.number().int(),
}).strict();
export const Policy = /* responsible-data.md §2, every field typed; `postal_address` z.string().min(10) */;
export const InboundMessage = z.discriminatedUnion('kind', [
  z.object({kind: z.literal('reply'), channel: z.literal('email'), from: z.string().email(), text: z.string(), inReplyTo: z.string().optional()}),
  z.object({kind: z.literal('comment'), channel: z.enum(['instagram', 'facebook']), external_id: z.string(), post_id: z.string(), from: z.string(), text: z.string()}),
  z.object({kind: z.literal('dm'), channel: z.enum(['instagram', 'facebook']), external_id: z.string(), from: z.string(), text: z.string()}),
  z.object({kind: z.literal('enquiry'), channel: z.enum(['platform', 'phone']), provider_id: z.string(), from: z.object({name: z.string(), kidAge: z.number().optional(), area: z.string().optional()}), text: z.string()}),
  z.object({kind: z.literal('stop'), channel: z.enum(['email', 'sms', 'push']), from: z.object({family_id: z.string().optional(), phone: z.string().optional(), email: z.string().optional()})}),
  z.object({kind: z.literal('bounce'), to: z.string()}), z.object({kind: z.literal('complaint'), to: z.string()}),
]);
export const Event = z.object({platform_id: z.string(), at: z.date(), name: z.string(), provider_id: z.string().optional(), family_id: z.string().optional(), draft_id: z.string().optional(), campaign_id: z.string().optional(), props: z.record(z.unknown()).default({})});
```

Collections and indexes: `architecture.md` §2 plus `outbox (platform_id, state, next_at)`,
`outbox (to.family_id, state)` for `cancelFor`, `messages (to.family_id, sent_at)` for the cap
query's fallback, `events (platform_id, at)`, `media_jobs (state)`, `sync_runs (platform_id, at)`,
`stage_history (provider_id, at)`, `tasks (platform_id, state)`. TTL index on `messages.sent_at`
(24 months) and `drafts.final_at` (90 days) — the `retention` job only reports what TTL did.

### 6. Jobs → `vercel.json` crons → `/api/cron/[job]`

| Cron (UTC; New York is UTC−4/−5, schedules are set in local time by the instance's `timezone` and converted at deploy) | Job | Module | Batch / limit |
|---|---|---|---|
| `0 * * * *` | `sync` | catalogue | all providers, paged; ETag |
| `* * * * *` | `send` | outbox | 100 rows, lock 55 s |
| `*/5 * * * *` | `publish` | outbox (posts due) | 20 rows (Meta container polling ≤ 4 min) |
| `*/5 * * * *` | `send-campaigns` | campaigns | 5 campaigns |
| `0 8 * * *` | `draft-social` | drafting | Batch API for the day's set |
| `30 8 * * *` | `draft-campaigns` | campaigns | same |
| `0 9 * * 1-5` | `sequence-step` | sequences | 200 recipients |
| `0 17 * * 0` / `0 18 * * 0` | `digest build` / `digest send` | families | all families with picks |
| `0 2 * * *` | `metrics` | analytics | yesterday |
| `30 2 * * *` | `score` | pipeline | all providers |
| `30 3 * * *` | `retention` | retention | managing and upgraded providers |
| `0 3 * * *` | `retention` + `tokens` | analytics / channels | report TTL; refresh Meta long-lived tokens < 10 days from expiry |
| `0 4 * * 1` | `delivery-audit` | analytics | weekly R33 report |
| `0 */6 * * *` | `health-rollup` | ops | outbox lag, dead rows, webhook failures → `/api/health` |

Event-driven (no cron): `alerts` (from `sync`'s `provider.new_session`), `draft-answers` (from the
webhook routes), `autoApprove` (after a draft is created), `entitlements` (Stripe webhook),
`clips` (upload → worker → callback). Fourteen schedules, under Pro's forty.

The cron route:

```ts
export async function GET(req, {params}) {
  if (req.headers.get('authorization') !== `Bearer ${CRON_SECRET}`) return new Response('no', {status: 401});
  const job = JOBS[params.job];  if (!job) return new Response('unknown', {status: 404});
  for (const platformId of await instances.active())                              // one deployment, several instances (ADR-2)
    try { await job(platformId); } catch (e) { log.error({job: params.job, platformId, e}); sentry(e); }
  return Response.json({ok: true});
}
export const maxDuration = 300;
```

### 7. The outbox in full (ADR-3, ADR-4, R3, R4, R23, R26)

```ts
export async function enqueue(m: OutboxRowInput) {
  const row = OutboxRow.parse({...m, _id: id(), state: 'queued', attempts: 0, next_at: m.scheduled_for ?? now(), created_at: now()});
  const refusal = await checks(row, 'enqueue');                                     // check #1 — same function as at send
  if (refusal) { await db.outbox.create({...row, state: 'refused', refused_reason: refusal}); await events.emit('outbox.refused', {reason: refusal, kind: row.kind}); return {refused: refusal}; }
  await db.outbox.create(row);  return {queued: row._id};
}

async function checks(row, phase): Promise<string | null> {
  const p = await policy.record(row.platform_id);
  const feature = FEATURE_OF[row.kind];                                              // sequence → provider_email, digest → digest, campaign → audience_saves, sms → sms, alert → alerts/push
  const g = await policy.gate(feature, {platformId: row.platform_id, at: now()});  if (!g.ok) return `policy: ${g.missing.join(', ')}`;
  if (row.to.family_id) {
    const f = await db.families_prefs.findOne({family_id: row.to.family_id, platform_id: row.platform_id});
    if (!f || f.stopped_at) return 'stopped';
    if (f.paused_until && f.paused_until > now()) return 'paused (stated vulnerability)';         // R32
    if (!f.prefs[PREF_OF[row.channel]] && row.countsTowardCap) return `preference off: ${row.channel}`;
    if (row.channel === 'sms' && !(await db.consents.exists({family_id: f.family_id, channel: 'sms', revoked_at: null}))) return 'no sms consent';   // R4
    if (row.countsTowardCap) {                                                       // R3 — provider-originated only; the platform's digest and alerts do not count
      const key = `cap:${row.platform_id}:${row.to.family_id}:${month()}`;
      const n = phase === 'send' ? await redis.incr(key) : Number(await redis.get(key) ?? 0) + 1;   // check #2 increments atomically (ADR-3)
      if (phase === 'send') await redis.expire(key, 40 * 86400);
      if (n > p.cap.providerMessagesPerMonth) { if (phase === 'send') await redis.decr(key); return `cap ${p.cap.providerMessagesPerMonth}/month reached`; }
    }
  }
  if (row.to.provider_id) {
    if (await db.opt_outs.exists({platform_id: row.platform_id, provider_id: row.to.provider_id})) return 'opted out / not my program';
    const s = await sending.get(row.platform_id);                                    // R23 guard
    if (row.channel === 'email') {
      if (!row.html?.includes(s.postal_address) || !/unsubscribe/i.test(row.html)) return 'footer: postal address or unsubscribe missing';
      if (s.bounce_rate >= 0.02) return 'paused: bounce rate ≥ 2 %';
      const sentToday = await redis.incrby(`sent:${row.platform_id}:${today()}`, phase === 'send' ? 1 : 0);
      if (sentToday >= Math.min(s.daily_cap, warmupCap(s.warm_day))) return 'daily send cap reached (warm-up)';
    }
  }
  if (!row.why) return 'no reason line';
  return null;
}

export async function send(platformId) {                                             // cron, every minute
  if (!(await redis.set(`lock:send:${platformId}`, '1', {nx: true, ex: 55}))) return;
  const rows = await db.outbox.find({platform_id: platformId, state: 'queued', next_at: {$lte: now()}}).sort({next_at: 1}).limit(100);
  for (const row of rows) {
    const claimed = await db.outbox.findOneAndUpdate({_id: row._id, state: 'queued'}, {$set: {state: 'sending'}});  if (!claimed) continue;
    const refusal = await checks(row, 'send');                                       // check #2, atomic on the cap
    if (refusal) { await db.outbox.updateOne({_id: row._id}, {$set: {state: 'refused', refused_reason: refusal}}); continue; }
    try {
      const {providerMessageId} = await channels.adapters[row.channel].publish(row);   // the ONLY call into a channel
      const msg = await db.messages.create({platform_id: platformId, to: row.to, channel: row.channel, kind: row.kind, draft_id: row.draft_id, campaign_id: row.campaign_id, step: row.step,
        provider_id: row.provider_id, sent_at: now(), provider_message_id: providerMessageId, status: 'sent', why: row.why, by: row.by, policy_basis: policy.basis(FEATURE_OF[row.kind], row)});
      await db.outbox.updateOne({_id: row._id}, {$set: {state: 'sent', message_id: msg._id}});
      if (row.draft_id) await db.drafts.updateOne({_id: row.draft_id}, {$set: {state: 'sent', final_at: now()}});
      if (row.kind === 'social') await blob.put(`snapshots/${msg._id}.json`, JSON.stringify({row, providerMessageId, at: now()}));   // audit snapshot
      await events.emit(`${row.kind}.sent`, {message_id: msg._id, provider_id: row.provider_id, family_id: row.to.family_id, channel: row.channel});
    } catch (e) {
      const attempts = row.attempts + 1;
      if (attempts >= 5) { await db.outbox.updateOne({_id: row._id}, {$set: {state: 'dead', error: String(e)}}); await alerts.ops('outbox.dead', row); }
      else await db.outbox.updateOne({_id: row._id}, {$set: {state: 'queued', attempts, next_at: addMinutes(now(), 2 ** attempts), error: String(e)}});
    }
  }
}

export async function cancelFor(familyId, channel?, session?) {
  await db.outbox.updateMany({'to.family_id': familyId, state: 'queued', ...(channel ? {channel} : {})}, {$set: {state: 'refused', refused_reason: 'stopped'}}, {session});
}
```

Why the cap is counted at send and only read at enqueue: enqueue is a forecast (the card can say
"1 of 4 this month"), send is the truth; a race of two rows against one remaining slot ends with one
`sent` and one `refused` because `INCR` is atomic (the BD-3-3 test).

### 8. Security

| Concern | Mechanism |
|---|---|
| Sign-in | DoneIsBetter OIDC (ADR-5); session cookie `httpOnly`, `SameSite=Lax`; `users {sub, role: 'operator' \| 'provider', provider_id?, platform_id}` |
| Authorisation | every Server Action starts with `const u = await requireRole('operator' \| 'provider')`; provider actions add `assertOwns(u, provider_id)`; family pages need a valid signed token only |
| Webhooks | signature verified on the raw body before parsing (Resend/Svix, Meta HMAC, Twilio, Stripe); idempotency `SET NX EX 86400` on the event id; the raw payload stored 30 days in `webhook_log` for replay |
| Cron | `Authorization: Bearer CRON_SECRET` (Vercel sets it); the route is not linked anywhere |
| Worker | shared bearer token both ways; the worker reaches Blob through signed URLs only; the callback carries `job_id` + HMAC |
| Secrets | Vercel environment (encrypted), Fly secrets; no secret in the repo; `env.ts` parses with Zod at boot and fails fast |
| Tokens | Meta long-lived tokens stored encrypted (`integrations.token_ref` → Vercel KV-style AES-GCM with `INTEGRATIONS_KEY`); refreshed by the `tokens` job |
| Personal data | families: `family_id`, prefs, `kids[].age`, area, saves — nothing else (R24, R28, R35); sensitive categories never a field; exports and deletion via `/api/webhooks/platform` `account.deleted` → `families.erase` (prefs, consents kept as a tombstone per retention) |
| Children | schema has no name field; `minor_field` gate; no clip without `consent_ref`; no push in quiet hours on a mixed instance |
| Rate limiting | Upstash `ratelimit` on webhook routes (1 000/min) and Server Actions (60/min per user) |
| Transport | HTTPS only; HSTS; CSP with the Mantine nonce; no third-party script (ADR-11: no analytics SaaS) |
| Audit | `approvals`, `consents`, `messages`, `opt_outs`, `events`, `stage_history` are append-only (no update path in the module; a MongoDB role without `update` on them in production) |

### 9. Configuration (`env.ts`, one Zod object)

```
APP_URL  CRON_SECRET  MONGODB_URI  UPSTASH_REDIS_REST_URL  UPSTASH_REDIS_REST_TOKEN  BLOB_READ_WRITE_TOKEN
SSO_ISSUER  SSO_CLIENT_ID  SSO_CLIENT_SECRET  SESSION_SECRET  INTEGRATIONS_KEY
RESEND_API_KEY  RESEND_WEBHOOK_SECRET  META_APP_ID  META_APP_SECRET  META_VERIFY_TOKEN
TWILIO_ACCOUNT_SID  TWILIO_AUTH_TOKEN  TWILIO_NUMBER            (unset until SMS is switched on)
STRIPE_SECRET_KEY  STRIPE_WEBHOOK_SECRET
ANTHROPIC_API_KEY  DRAFTER=claude|template  DRAFT_MODEL=claude-sonnet-5  CLASSIFY_MODEL=claude-haiku-4-5-20251001
WORKER_URL  WORKER_TOKEN  SENTRY_DSN
```

Per-instance configuration lives in the database, not the environment: `policies`, `sending`,
`integrations`, `products`, `assumptions`, `instances {platform_id, name, timezone, connector:
'yourfield', base_url, key?}`. Adding an instance is a row plus a connector class (ADR-2).

### 10. The media worker (Fly.io, `worker/`)

```
POST /clips  {job_id, blob_url, listing{name, url, activity, area}, consent_ref|null, profile:'reels', callback}
 1. if listing.shows_children && !consent_ref → 422 {refused: 'consent', options: ['coach-only', 'place-only']}    # R30, second enforcement
 2. download to /tmp; ffprobe (duration, resolution)
 3. Deepgram: POST /v1/listen?model=nova-3&smart_format=true&utterances=true&diarize=true  → words[{word, start, end, speaker}]
 4. moments = findMoments(words, transcript):
      score each utterance by: coach instruction verbs ("watch", "try", "good"), laughter/cheer markers,
      a child's-name-free check (drop any utterance containing a capitalised token not in listing.name — names never on a clip),
      length 8–25 s, spread across the recording; take the top N=4
 5. for each moment: ffmpeg -ss start -to end -i in.mp4 -vf "scale=-2:1920,crop=1080:1920,subtitles=cap.srt:force_style='FontSize=18,Outline=2'"
      -c:v libx264 -preset veryfast -crf 23 -c:a aac out.mp4            # 9:16, captions burned in (R34); also write .vtt
 6. c2pa: Builder with manifest {claim_generator:'business.direct clip engine', assertions:[{label:'c2pa.actions', data:{actions:[{action:'c2pa.edited', softwareAgent:'ffmpeg'}]}}],
      title: listing.name} signed with CLIENT_C2PA_CERT/KEY → embedded in out.mp4; manifest id recorded           # R20
 7. upload out.mp4 + .vtt to Blob (public read for Meta's fetch, unguessable path)
 8. POST callback {job_id, clips:[{url, vtt_url, duration, moment_text, c2pa_manifest_id}], consent_ref}  (HMAC)
```

Output profile per channel (Meta constraints, research VI §6): Reels 1080×1920 MP4 H.264 AAC ≤ 90 s;
Facebook the same file; a still for the Instagram feed is a JPEG frame at 1080×1350. The worker is
stateless; a job that fails is retried once by the app, then surfaces as a task.

### 11. Testing (what proves the invariants)

| Level | What | Tool |
|---|---|---|
| Static | no import of `channels/*` outside `outbox` and the webhook routes | ESLint `no-restricted-imports` (fails the build) |
| Unit | `policy.gate` per feature × missing field (framework §3, ten rows); `patternGuard` per banned pattern; `pipeline.setStage` illegal moves; `score`; `econ.*` against the prototype's numbers (the 24 inputs → LTV : CAC 0.7 at defaults); `findMoments` drops utterances with a name | Vitest |
| Contract | `YourFieldConnector` against recorded fixtures from `first-customer-classscout.md` (253 providers; a changed `updatedAt` → one diff event); schema-drift test fails when a field disappears | Vitest + fixtures |
| Integration | webhook routes with recorded payloads (Resend received/bounced, Meta comment + verification GET, Twilio STOP, Stripe `checkout.session.completed`) → the right row and no duplicate on replay; `families.stop` cancels queued rows in one transaction; the cap race (two sends, one slot → one sent, one refused) | Vitest against a MongoDB Memory Server + Upstash test db |
| End-to-end | the operator's routine on the console: approve a post → it appears `scheduled` → `publish` run with a stub adapter → `messages` row + snapshot; a provider approves a campaign → audience count shown before approval; a family opens the signed link and turns picks off → the next digest run skips them; Simple mode's press runs only `auto` recommendations | Playwright, against `next start` with `DRAFTER=template` and stub adapters |
| Load | 5 000 outbox rows drained within an hour at 100/minute; `send` tick < 60 s | a script, measured in the build log |
| Security | signature failure → 401 and no row; cron without secret → 401; provider A cannot read provider B (`assertOwns`) | Vitest |

Every rule R1–R36 that is code has at least one test that names it (`describe('R3 cap …')`), so the
rules map (`business-logic.md`) can be checked against the test names by the gate.

### 12. Operations

- **Health**: `/api/health` returns `{outbox_lag_s, dead_rows, last_sync_at, last_send_at, webhook_failures_24h, cap_violations (must be 0), send_errors_by_channel}`; Better Stack pages on non-200 or `outbox_lag_s > 1800`.
- **Runbooks** (`docs/runbooks/` in the new repo): Meta token expired (re-connect on the Integrations screen; queued posts wait, nothing is lost); a provider says "not my program" (the opt-out is automatic; check the thread); a family's deletion request (platform webhook or the operator's *Erase* action → `families.erase`, confirmation logged); bounce pause (the sequence card shows "paused: bounce ≥ 2 %"; fix the list, reset `sending.bounce_rate` after review); a dead outbox row (the Approvals screen's "failed" tab; retry or refuse with a reason).
- **Backups**: Atlas continuous backup at M10; Blob is the audit copy of every published post; the policy record's history is versioned in `policies` (`version` increments; old versions kept).
- **Release**: `main` → production; preview per branch; feature flags per instance in `instances.flags` (`social`, `campaigns`, `sms`, `clips`, `pages`) so a sprint ships dark.

### 13. The prototype → the modules (continuity)

| Prototype (`assets/app.js`) | Module |
|---|---|
| `policyGate()`, `policyBlocked()`, `S.policies` | `policy` |
| `data/providers.json`, `#nProv`, catalogue tiles | `catalogue` (`providers_cache`) |
| `S.stage`, `setStage()`, `S.history`, `score(p)` | `pipeline` |
| `TEMPLATES`, `HELP`, drafts with `ai`, the voice file's banned list | `drafting` (+ `knowledge`) |
| approvals screen, `S.approvalsMade`, `S.auto` | `approvals` |
| `sendInvitation()` R23 guard, `S.sending` | `outbox` + `sequences` |
| `S.integrations` v1 flags | `channels` + `integrations` |
| `campaignsFor`, `S.campaigns`, audiences | `campaigns` |
| `enquiriesFor`, `commentsFor`, `S.threads`, `S.replies` | `conversations` |
| `S.family` (kids as ages, prefs, saved, smsConsent), Stop | `families` |
| `S.media` (consent, uploads, adapters) | `media` + the worker |
| `S.products`, `S.bought` | `billing` |
| `retentionFor()`, `retentionDrafts()`, `S.retained`, the Retention screen | `retention` |
| generated pages screen | `pages` |
| `econ()`, `S.econ` (24 inputs), `S.experiment`, `S.attributed` | `analytics` |
| `recommend()`, `runSafe`, Home | `recommend` |
| `S.mode` Simple/Advanced, `NAV_SIMPLE`/`NAV_ADV`, `?view=&screen=&mode=` | `app/(console)/layout.tsx` |

Nothing in the prototype has no home; nothing in the modules has no screen or job.


## Appendix — the token map: prototype tokens and components → production

*Written 2026-09-19. What the prototype's CSS becomes in production. The prototype does not
consume a design-system package — it is dependency-free HTML — but its custom properties
are named after General Design System 6.5.0 roles (the same convention as DiscountDirect's
`GDS-TOKEN-MAP.md`, D5/D8), so the production build maps 1:1 without a rename pass.*

### 1. How the handoff works

The whole colour and shape contract is `assets/tokens.css` (one `:root` block). In
production the app loads the GDS theme stylesheet and Mantine's theme is generated from the
same roles; `tokens.css` is deleted. Every `var(--gds-…)` in `components.css` and `app.css`
then resolves to the governed value. No selector or markup changes for the token layer.

### 2. Tokens

| Role (prototype = GDS 6.5.0 name) | Value here | Source | Production |
|---|---|---|---|
| `--gds-bg-canvas` | `#f8fafc` | GDS canonical light | GDS |
| `--gds-bg-surface` | `#ffffff` | GDS | GDS |
| `--gds-bg-inverse` | `#111827` | GDS | GDS |
| `--gds-bg-muted` | `#f1f5f9` | GDS | GDS |
| `--gds-text-body` / `-meta` / `-on-inverse` | `#111827` / `#64748b` / `#f8fafc` | GDS | GDS |
| `--gds-border-card` / `-strong` | `#e2e8f0` / `#cbd5e1` | GDS | GDS |
| `--gds-brand-accent` / `-tint` / `-strong` | `#0f766e` / `#e6f4f2` / `#115e59` | **product-owned** (D8: business.direct teal; DiscountDirect indigo) | the product's brand override in the GDS theme |
| `--gds-status-ok` / `-wait` / `-off` / `-danger` (+ tints) | `#15803d` / `#b45309` / `#64748b` / `#b91c1c` | GDS semantic status | GDS |
| `--gds-radius-card` / `-control` / `-pill` | 14 / 10 / 999 px | GDS | GDS |
| `--gds-elevation-card` | two-layer shadow | GDS | GDS |
| `--gds-font` / `--gds-font-mono` | system stacks | GDS | GDS (Inter where the platform uses it) |
| `--gds-t-title` / `-h2` / `-body` / `-meta` | clamp 22–30 / 18 / 14 / 12 px | prototype | Mantine `fontSizes` |
| `--gds-tap` | 44 px | prototype rule (PROTOTYPING.md) | Mantine component `size` at phone widths |
| `--gds-gutter` / `--gds-content-max` | 16 px / 1400 px | prototype | layout constants |

Contrast (WCAG relative luminance, computed 2026-09-19): accent on white 5.5:1,
accent-strong on tint 6.7:1, status-ok on ok-tint 4.6:1, status-wait on wait-tint 4.5:1,
meta on surface 4.8:1 — all ≥ 4.5:1; the wait pair sits exactly at the threshold and is
used only at 12 px bold badges, so production should darken `--gds-status-wait` a step if
it appears in body text.

### 3. Components → Mantine + GDS

| Prototype class (`components.css`) | Production | Notes |
|---|---|---|
| `.btn`, `.btn.sec`, `.btn.ghost`, `.btn.danger`, `.btn.inert` | `Button` variants filled / light / subtle / red; `inert` = `disabled` with a tooltip | 44 px min height below 980 |
| `.badge.b-ok/.b-wait/.b-off/.b-danger/.b-ai` | `Badge` with the status colours; `b-ai` is a product variant (✦) | the AI badge is required by ADR-7 |
| `.topbar`, `.brand`, `.roles`, `.topnote` | `AppShell.Header` + `SegmentedControl` for the role switch | roles become route groups |
| `.rail`, `.bottombar` (`app.css`) | `AppShell.Navbar` ≥ 1024; a fixed `Tabs` bar below | counts as `Indicator` |
| `.grid`, `.card`, `.dept-list`, `.toggle` | `SimpleGrid`, `Card`, `List`, `Switch` | the AI switch is a `Switch` with a label |
| `.approval`, `.preview`, `.why` | product component `ApprovalCard` (Card + actions column) | the `why` line is mandatory (R2) |
| `.post` (D15) | product component `PostCard` (media 72 px, channels, copy, link, state) | media from Blob |
| `.pipeline` (D15) | product component `PipelineStrip` (6 stages, `on`/`done`) | click filters the list |
| `.tiles`, `.tile`, `.bars` | `SimpleGrid` of `Paper` with a sparkline (`@mantine/charts`) | every tile shows its source (R7) |
| `.tbl` | `Table` with `ScrollArea`, server pagination | 50 per page |
| `.kfile` | `Textarea` in a `Code`-styled `Paper` with a path label | versioned saves |
| `.listing`, `.pin`, `.ladder` | `Card` with an avatar; the ladder is the provider's plan (products, `done` = active entitlement) | family saved, provider results, drawer |
| campaign card (= `.approval` + `.preview` + `.why`) | product component `CampaignCard` — the approval card with the audience line | provider campaigns, family inbox (read-only) |
| media adapter card, sending card, experiment card (= `.card` + `.dept-list` / `.foot`) | `Card` with status badges | social publishing, sales, economics |
| recommendation card (= `.approval` with a `safe to run` / `needs your judgement` badge) | `RecommendationCard` | Home |
| help bar and help card (`.helpbar`, `.helpcard` in `app.css`) | `Collapse` + `Alert` | every screen |
| enquiry card, comment card (= `.approval` + `.why` + `.preview`) | product component `ReplyCard` — "they wrote" + the drafted answer + approve / edit / skip | provider conversations, platform social, approvals |
| product card (= `.card` + `.foot`) | `Card` with price and a `Button` → Stripe Checkout | provider today |
| `.push`, `.digest`, `.sms` | preview renderers for the three family channels | used by `ChannelAdapter.preview` |
| `.field`, `.search`, `.chip` (`app.css`) | `TextInput`, `Chip.Group` | |
| `.drawer`, `.thread`, `.msg` (`app.css`) | `Drawer` + a `ThreadView` product component | |
| `.week`, `.slot` (`app.css`) | product component `WeekCalendar` | drag-to-reschedule is a later issue |
| `.toast` (`app.css`) | `Notifications` | |
| `.empty` (`app.css`) | product `EmptyState` | every screen has one |

### 4. What has no mapping

The frames' `frame.css` and the docs' `docs.css` are documentation only. The
design-system page (`design-system.html`) is the reference for review, not a component
library; production's storybook is generated from the Mantine components above.

