# business.direct — research VI: the real system — every service verified, what it costs, what it needs, what it limits

> **Status — evidence.** Written while the project was framed around the first customer's site; the vocabulary of that time (client, platform, provider, family) is kept, the product's terms are in `product-definition.md` §5. Every figure the stakeholder documents use from this round was re-verified on 2026-09-20 in `evidence.md`, which is the authority where the two differ.


*Sixth research round, 2026-09-20; every row re-read against the vendor's page the same evening and
corrected where it was wrong — the status of each figure is in `evidence.md` §2 (V1–V16),
which is the authority where this file and the register differ. Originally written on the owner's instruction: "step to the next phase … make a
research and plan how we can make it a real system … exact services, what module goes where,
how it works, the architecture, the system drawings, everything with pseudo code." This document
is the research half: for every external service the machine depends on, the vendor's own terms
as read on 2026-09-20 — authentication, review or registration, rate limits, prices, and the
alternative considered. The plan half is `architecture.md` (modules, drawings, pseudo
code) and `delivery-plan.md` (sprints, acceptance tests). **P** marks a primary source
(the vendor's own documentation or pricing page), **A** a secondary summary. Prices and limits
change; every number carries the date it was read and is re-checked at contract signature. The
first customer is ClassScout (Your Field NYC); everything is English and US-first; a second instance is a
policy record and a connector (ADR-2), nothing here assumes one.*

## 0. What the machine needs from outside (the dependency list)

| Need | Service chosen | Alternative kept | Decision |
|---|---|---|---|
| App hosting, HTTP, cron, preview per branch | Vercel (Pro) | Fly.io for everything | ADR-15 |
| Database | MongoDB Atlas | Postgres on Neon | ADR-16 (stays D26) |
| Caps, rate limits, idempotency, locks | Upstash Redis | MongoDB counters | ADR-3 (stays) |
| Files (media, snapshots, exports) | Vercel Blob | Cloudflare R2 | ADR-17 |
| Jobs | Vercel Cron + a MongoDB outbox (§4) | Vercel Workflows, then Inngest, when a tick past 800 s or a days-long wait is needed | ADR-18 |
| E-mail out and inbound | Resend | Postmark | ADR-19 |
| Instagram + Facebook publishing and inbound | Meta Graph API (Instagram API with Facebook Login) | Buffer / Later API as a proxy | ADR-20 |
| SMS (later, families only, consent) | Twilio with A2P 10DLC registration | Telnyx | ADR-21 |
| Payments for upgrades | Stripe Checkout + Billing on the platform's account | Paddle | ADR-9 (stays) |
| Drafting (optional per department) | Claude API (Sonnet 5 default, Haiku 4.5 for classification, Batch for nightly work) | OpenAI | ADR-7 (stays), ADR-22 |
| Clip engine: transcription | Deepgram Nova (batch) | OpenAI Whisper API | ADR-23 |
| Clip engine: cutting, captions, C2PA | ffmpeg in a container worker + `c2pa-node` | Vercel function with `ffmpeg-static` | ADR-24 |
| Content credentials | C2PA via `@contentauth/c2pa-node` | none (label only) | R20 needs the credential |
| Generated images (later, never a person) | Nano Banana 2 (Gemini image) behind `MediaAdapter.image` | Ideogram, Firefly | ADR-12 (stays) |
| Sign-in for operators and providers | DoneIsBetter SSO | Auth.js with e-mail magic links | ADR-5 (stays) |
| Errors, logs, uptime | Vercel logs + Sentry (free tier) + a `/api/health` polled by Better Stack | Datadog | ADR-25 |

## 1. Hosting and runtime — Vercel

**P** [Vercel cron jobs: usage and pricing](https://vercel.com/docs/cron-jobs/usage-and-pricing),
[Vercel functions limits](https://vercel.com/docs/functions/limitations) — read 2026-09-20.

- **Cron**: **100 cron jobs per project on every plan**; Hobby once a day with ±59 min precision; **Pro and
  Enterprise once a minute, per-minute precision** (the cron *invokes* an HTTP route; the route's own duration
  limit applies) — V1. Pro is $20 per member per month.
- **Function duration**: 300 s default on every plan; **Pro maximum 800 s, 1 800 s in beta** with
  `maxDuration`; memory up to 4 GB on Pro; request body 4.5 MB; bundle 250 MB (5 GB in beta); Vercel
  Workflows exist for runs without a duration limit — V2. A single cron tick still drains a batch, never
  "everything". The outbox `send` job (every minute, batch of 100) sends 6 000 messages an hour, twelve
  times the sizing target of 5 000 a day (architecture §3).
- **Preview per branch** and production on `main` — the repo's existing model.
- **Why not Fly.io for everything**: the app is a Next.js console with Server Actions; Vercel is the
  platform the first customer already runs on (`first-customer-classscout.md`), the operator learns one dashboard, and the one
  thing Vercel cannot do (long ffmpeg runs) goes to one small container (§10).

## 2. Database — MongoDB Atlas

**P** [Atlas pricing](https://www.mongodb.com/pricing) — read 2026-09-20: **M0 free: 512 MB, shared,
no backups beyond the free snapshot, 500 connections**; M10 dedicated from ~$0.08/hour (~$57/month)
with continuous backup, 10 GB, and the connection headroom Server Actions need.

- Sizing (architecture §3): 1 000 providers × ~4 KB cache = 4 MB; 5 000 messages/day × 24 months × ~1 KB
  ≈ 3.6 GB in the message log at full scale → **M0 for the build and the pilot, M10 for production**;
  the message log is the first collection to need a TTL index (`retention` job).
- Mongoose stays (D26, DiscountDirect); schemas are validated with Zod at the boundary
  (`architecture.md` §5) so a bad webhook never reaches the model.
- **Change streams** are available from M10 (not on M0) — the blueprint does not depend on them; the
  outbox is polled by cron.

## 3. Caps and locks — Upstash Redis

**P** [Upstash pricing](https://upstash.com/pricing/redis) — read 2026-09-20: **free 256 MB, 500 000
commands a month**; pay-as-you-go $0.2 per 100 000 commands after; REST API (works from Vercel
functions without a persistent socket).

- The cap check is two commands per family per send (`INCR` + `EXPIRE`, or one Lua script); at
  5 000 sends a day that is ~300 000 commands a month — inside the free tier for the pilot.
- Idempotency keys for webhooks (`SET NX EX 86400`), one key per event id.
- Upstash is also where the `send` job takes its one-minute lock (`SET lock:send NX EX 55`) so two cron
  ticks never drain the same batch twice (§4).

## 4. Jobs — Vercel Cron + a durable outbox, Inngest as the upgrade path

**P** [Inngest: deploy to Vercel](https://www.inngest.com/docs/deploy/vercel),
[Inngest Next.js quick start](https://www.inngest.com/docs/getting-started/nextjs-quick-start),
[Inngest for Vercel (marketplace)](https://vercel.com/marketplace/inngest/account); **A**
[Inngest + Next.js guide, 2026](https://dev.to/stacknotice/inngest-nextjs-the-complete-guide-2026-2i33),
[Inngest: scheduled jobs](https://www.inngest.com/uses/scheduled-jobs) — read 2026-09-20.

- What Inngest adds: durable `step.run` / `step.sleep` / `step.waitForEvent` (a function can wait
  days for an approval event and resume), retries per step, concurrency keys, a cron in code,
  a dashboard; served from one `/api/inngest` route with `maxDuration`; free tier 100 000 step runs a
  month. Trigger.dev is the equivalent with its own workers.
- What the machine actually needs today: a durable queue of approved work, a sender that runs every
  minute in batches, retries with backoff, a dead-letter, and a lock. **A MongoDB `outbox` collection
  plus one cron tick a minute gives all of it** (blueprint §7) and adds no vendor, no second dashboard
  and no event-shape to keep in sync. Sequences do not need "sleep for three days" — the
  `sequence-step` job computes what is due from `sent_at + delay_days` every morning.
- **Decision (ADR-18)**: Vercel Cron + outbox. Move to Vercel Workflows (the same platform, no new vendor)
  or Inngest when either is measured: a job needs more than 800 s per tick and cannot be batched; a
  workflow needs to wait on an external event for days with state that is awkward to keep in a document.
  The outbox row shape is kept Inngest-compatible (an event name and a JSON payload) so the move is a
  new consumer, not a migration.

## 5. E-mail — Resend

**P** [Resend pricing](https://resend.com/pricing), [Resend inbound](https://resend.com/docs/dashboard/receiving/introduction),
[Resend webhooks](https://resend.com/docs/dashboard/webhooks/introduction) — read 2026-09-20.

- **Free: 3 000 e-mails a month, 100 a day, 3 domains**; Pro $20 a month for 50 000 e-mails, $35 for
  100 000; inbound on every plan — V5.
- **Inbound**: an MX record on a subdomain (`reply.<sending domain>`) delivers every incoming e-mail as
  a webhook (`email.received`) with the parsed headers and body; replies to a sequence therefore land
  in `threads` without polling. Webhooks are signed (Svix headers `svix-id`, `svix-timestamp`,
  `svix-signature`); the route verifies before it reads.
- **Delivery events** (`email.sent`, `delivered`, `bounced`, `complained`, `opened`, `clicked`) drive
  the sending guard's bounce rate (R23) and the metrics tree's open and click leaves.
- **Warm-up**: Resend has no automatic warm-up on shared IPs; the sending guard's own schedule
  (day 1–42, `sending.warm_day`) stays the control (D30, Q2).
- List-Unsubscribe headers (`List-Unsubscribe`, `List-Unsubscribe-Post`) are set on every marketing
  message so Gmail and Yahoo's one-click requirement is met; the body still carries the link and the
  postal address (CAN-SPAM, R2, R23).
- Why not Postmark: equivalent product; Resend is already the family's choice (D26) and its inbound
  webhook is simpler to wire than Postmark's inbound stream.

## 6. Instagram and Facebook — Meta Graph API

**P** [Instagram platform: content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing),
[Instagram platform: webhooks](https://developers.facebook.com/docs/instagram-platform/webhooks),
[Setup webhooks subscriptions](https://developers.facebook.com/documentation/instagram-platform/webhooks);
**A** [Hookdeck: Facebook webhooks](https://hookdeck.com/webhooks/skills/facebook-webhooks),
[Meta webhooks for Instagram messaging (walk-through)](https://innocentanyaele.medium.com/setup-meta-webhooks-for-instagram-messaging-and-respond-to-message-4575bc95c7a2) — read 2026-09-20.

- **Account**: the platform's Instagram must be a professional account (Business or Creator) linked to
  a Facebook Page; the app authenticates by **Facebook Login for Business** and holds a Page access
  token (long-lived, 60 days, refreshed) from which the Instagram user id is read.
- **Permissions and review**: `instagram_business_basic`, `instagram_business_content_publish`,
  `instagram_business_manage_comments`, `instagram_business_manage_messages`, `pages_manage_posts`,
  `pages_read_engagement`, `pages_manage_metadata`. Publishing to a page the app does not own requires
  **App Review** (typically two to four weeks; a screencast of the flow and a privacy-policy URL are
  required). *Prerequisite P-11 (v1 integrations) covers the review; it starts in sprint 1 so it is
  done before the publishing sprint.*
- **Publishing flow** (Instagram): create a media container `POST /{ig-user-id}/media` with
  `image_url` or `video_url` (a public HTTPS URL — Vercel Blob provides it) and the caption; poll
  `GET /{container-id}?fields=status_code` until `FINISHED`; then `POST /{ig-user-id}/media_publish`.
  Reels use `media_type=REELS`; carousels create child containers first. Facebook Page: `POST
  /{page-id}/photos` or `/videos` or `/feed`.
- **Limits**: **100 API-published posts per Instagram account per rolling 24 hours** (carousel counts
  once); the platform's rate limit is per app-user and per hour (calls = 200 × users); the machine
  publishes tens a week, not hundreds a day.
- **Inbound**: a Webhooks subscription on the Instagram object for `comments`, `messages`,
  `mentions`; on the Page object for `feed`. Meta `GET`s the callback with a `hub.challenge` to verify
  the URL, then `POST`s events signed with `X-Hub-Signature-256` (HMAC-SHA256 with the App Secret).
  Comments arrive with the media id and the commenter's username; replying is `POST
  /{comment-id}/replies`. DMs require the messaging permission and the app in **Live** mode.
- **Media constraints**: JPEG only for images (8 MB), 4:5 to 1.91:1 aspect ratio; Reels MP4/MOV, 3 s
  to 15 min, 9:16, ≤ 1 GB; captions ≤ 2 200 characters, 30 hashtags. The clip engine's output profile
  (blueprint §10) is set to these.
- Why not a scheduling SaaS (Buffer, Later) as a proxy: it would add a vendor between the outbox and
  the channel and put the audit snapshot outside the message log; the direct API is a few hundred
  lines.

## 7. SMS — Twilio with A2P 10DLC (families only, later, consent only)

**P** [Twilio A2P 10DLC overview](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc),
[Twilio messaging pricing (US)](https://www.twilio.com/en-us/sms/pricing/us) — read 2026-09-20.

- **Registration before any US SMS**: a Brand (low-volume standard $4 one-time, ≈ $4.41 with tax; a
  standard brand costs more and adds secondary vetting) and a Campaign use case ($15 one-time vetting;
  $2–10 a month by use case) — V8, re-checked at registration; campaign registration
  requires the sender's **privacy-policy URL and terms URL and sample messages**, and a described
  opt-in flow — the consent text the policy record stores (`consentText.sms`). Unregistered traffic is
  blocked by US carriers.
- **Price**: ~$0.0083 per outbound SMS segment plus carrier fees (~$0.003–0.005); a local number ~$1.15
  a month.
- **STOP/START/HELP** are handled by Twilio's Advanced Opt-Out automatically; the inbound webhook
  (`POST` with `X-Twilio-Signature`) writes the opt-out to `consents` (revoked) the same second (R4).
- **Missed-call capture** (phase 3 conversations): a Twilio number forwards to the provider's phone and
  posts a status callback when unanswered → an enquiry row. Voice minute ~$0.014.
- Decision: SMS stays off until the policy record's `channels.sms` is `consent` and counsel's consent
  text is in (P-3, P-4); the adapter is built in the same shape as e-mail so the switch is
  configuration.

## 8. Payments — Stripe (the platform is the merchant)

**P** [Stripe Checkout: subscriptions](https://docs.stripe.com/payments/checkout/how-checkout-works),
[Stripe webhooks](https://docs.stripe.com/webhooks), [Stripe Connect: on_behalf_of](https://docs.stripe.com/connect/separate-charges-and-transfers) — read 2026-09-20.

- **Checkout Session** in `mode: 'subscription'` with the product's price id creates the customer and
  the subscription; the machine never sees a card number. Customer Portal handles cancellation
  (cooling-off, R32: the machine sets `cancel_at_period_end` on request within 14 days and refunds
  through the API).
- **Webhooks**: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`,
  `invoice.payment_failed`; signed with `Stripe-Signature`; Stripe retries failed deliveries for up to
  three days. The `entitlements` job is idempotent on the event id.
- **Account model**: the platform's own Stripe account holds the keys (ADR-9). Connect's
  `on_behalf_of` is not available on Checkout subscriptions, so "business.direct as a Connect platform
  taking a fee" is not the v1 shape; if a revenue share is agreed later, it is an invoice between the
  two companies, not a Stripe fee.
- Stripe pricing: 2.9 % + $0.30 per successful card charge (US, standard); Billing 0.7 % on recurring
  when using the Billing product.

## 9. Drafting — Claude API

**P** [Claude API pricing](https://docs.claude.com/en/docs/about-claude/pricing),
[Batch processing](https://docs.claude.com/en/docs/build-with-claude/batch-processing) — read 2026-09-20.

- Prices per million tokens (input / output): **Opus 5 $5 / $25; Sonnet 5 $2 / $10; Haiku 4.5 $1 / $5**;
  the **Batch API halves both** for work that can wait up to 24 hours; prompt caching cuts repeated
  context (the knowledge files) to a tenth on reads.
- The machine's prompts are the knowledge files (voice, rules, the card) — ~4 000 tokens of context
  and ~300 tokens out per draft. At 200 drafts a day on Sonnet 5 with cached context: ≈ $0.01 per draft,
  ~$60 a month; the nightly `draft-social` and `draft-campaigns` batches use the Batch API; the
  inbound `draft-answers` (a minute, R14) uses the live API. Classification (a reply's sentiment, a
  vulnerability signal for R32, the banned-pattern check) runs on Haiku 4.5.
- Every AI output is stored with `ai: true`, the model id and the prompt version (`drafts.ai_meta`)
  so a marking rule (R20) and a later audit are queries.
- The provider is behind an interface (`Drafter`) — ADR-7 stays; the vendor is an environment
  variable.

## 10. The clip engine — transcription, cutting, captions, credentials

**P** [Deepgram pricing](https://deepgram.com/pricing) (Nova batch ~$0.0043 per minute, pay-as-you-go
with $200 free credit), [OpenAI audio pricing](https://openai.com/api/pricing/) (Whisper $0.006 per
minute), [`@contentauth/c2pa-node`](https://github.com/contentauth/c2pa-node) (Builder / Reader
API, Node 22+, signs with an X.509 certificate), [Fly.io Machines pricing](https://fly.io/docs/about/pricing/),
[Railway pricing](https://railway.com/pricing), [Modal pricing](https://modal.com/pricing) — read 2026-09-20.

- **Transcription**: Deepgram Nova batch at ~$0.0043/min with word timestamps and diarisation; a
  30-minute session recording costs ~$0.13. Whisper via OpenAI is $0.006/min without diarisation.
  Word timestamps drive the caption file (SRT/WebVTT, R34) and the "moment" finder (blueprint §10).
- **Cutting and captions**: ffmpeg (`-ss/-to` cuts, `subtitles=` burn-in, `scale=1080:1920` for
  9:16). It does not fit a Vercel function well (250 MB bundle limit, 300 s, no persistent scratch)
  — **one container worker** runs it: a Fly.io Machine (shared-cpu-1x, 1 GB, $0.0082/hour ≈ $5.92 a month while
  running; a stopped machine pays only its root file system, $0.15 per GB per 30 days; auto-start on
  request — V12) or Railway (from $5/month) — the blueprint
  picks Fly.io with `auto_stop_machines` so the pilot pays cents. Modal (per-second GPU/CPU billing,
  Python-first) is the alternative if the clip engine later adds a vision model.
- **Credentials**: `c2pa-node` builds a manifest (`c2pa.actions`: created / edited, `c2pa.ai_generated`
  where applicable) and signs it into the MP4 or JPEG; the signing certificate is the platform's
  (`CLIENT_C2PA_CERT`, `CLIENT_C2PA_KEY` in the worker's secrets), the manifest names the machine
  as the tool and the platform as the signer. Instagram and Facebook strip most metadata on upload —
  the credential is therefore also kept on the Blob copy and linked from the post's audit snapshot
  (R20 is met by the record; the visible label is set per platform rule).
- **Children in footage** (R30): the consent confirmation is a required input of the worker's request
  (`consent_ref`); without it the worker refuses the cut and returns the coach-only / place-only
  option — the rule is enforced twice, in the app and in the worker.

## 11. Generated images (later)

**P** [Gemini API pricing (image generation)](https://ai.google.dev/gemini-api/docs/pricing) —
read 2026-09-20: Nano Banana 2 (Gemini image) from ~$0.045 per 1K-square image to ~$0.15 per 4K
image; images carry SynthID; the machine adds its own C2PA manifest and the platform label. Only
behind `MediaAdapter.image`, never a person (R15), only when `aiDisclosure` is set (gate). Not in
Release 1.

## 12. Sign-in — DoneIsBetter SSO

The owner's own identity provider; used by the platform (D31 confirmed sign-in is DoneIsBetter).
Assumed: OIDC with an authorization-code flow and a JWT carrying `sub`, `email`, and a role claim
per client id; the machine keeps a `users` collection mapping `sub` → role (`operator`) or
`provider_id`. **A (assumption)**: the OIDC details are the owner's to confirm at sprint 0; the
fallback is Auth.js with e-mail magic links, which changes one file.

## 13. Observability

**P** [Sentry pricing](https://sentry.io/pricing/) (developer tier free: 5 000 errors a month),
[Better Stack uptime pricing](https://betterstack.com/uptime/pricing) (free: 10 monitors, checks up to every 30 s — V14) — read 2026-09-20.

- Vercel's own logs and function metrics cover requests; Sentry catches exceptions in Server Actions,
  routes and the worker with the `platform_id` tag; Better Stack polls `/api/health` (which reports
  outbox lag, the last sync time, the last cron tick) and pages on failure. The five alerts in
  architecture §9 are computed in `/api/health` and by the `metrics` job.

## 14. What each service needs before the first real run (folds into `first-customer-classscout.md`)

| Service | Needs | Lead time |
|---|---|---|
| Vercel Pro | a team, the domain, environment variables | a day |
| MongoDB Atlas | a project, an M0 cluster (M10 at production), IP allow-list for Vercel | a day |
| Upstash | a database in the same region (US-East) | minutes |
| Resend | the sending domain's DNS (SPF, DKIM, DMARC), an MX for `reply.` | a day; DNS is the platform's (P-11) |
| Meta | a Meta developer app owned by the platform's Business Manager, the Page and the Instagram account connected, App Review with a screencast, the privacy-policy URL | **two to four weeks** — start in sprint 1 |
| Twilio | account, brand and campaign registration with the privacy-policy and terms URLs | one to two weeks; only when SMS is switched on |
| Stripe | the platform's account, products and prices, webhook endpoint | a day; the prices are P-6 / P-12 |
| Claude API | an API key, a spend limit | minutes |
| Deepgram | an API key | minutes |
| Fly.io | an app, secrets (Deepgram key, C2PA cert), the worker's shared token | a day |
| C2PA certificate | an X.509 signing certificate in the platform's name (a public CA's document-signing cert, or a self-signed cert for the pilot with the caveat that verifiers show it as untrusted) | a week for a CA cert |
| DoneIsBetter SSO | a client id and secret for the machine, the redirect URL | the owner's, a day |

## 15. Monthly cost at pilot and at the sizing target

| Line | Pilot (Your Field, ≤ 300 providers, ≤ 5 000 families) | Sizing target (1 000 providers, 50 000 families) |
|---|---|---|
| Vercel Pro | $20 (one member) | $40 (two) — V1, V2 |
| MongoDB Atlas | $0 (M0) | ~$57 (M10) |
| Upstash | $0 | ~$5 |
| Vercel Blob | ~$1 | ~$10 |
| Resend | $0–20 | $20–90 |
| Meta | $0 | $0 |
| Claude API | ~$20 | ~$80 |
| Deepgram | ~$5 | ~$30 |
| Fly.io worker | ~$3 | ~$15 |
| Sentry, Better Stack | $0 | $0–26 |
| Stripe | 2.9 % + $0.30 per charge on the platform's account | same |
| Twilio (when on) | ~$3 + $0.01 per SMS | ~$20 + volume |
| **Total infrastructure** | **≈ $50–75 a month** | **≈ $280–400 a month** |

Against the economics model's ARPA of $49 (`economics.md`): the pilot's
infrastructure is covered by two upgraded providers; the sizing target's by eight.

## 16. What was not found or is assumed

- Meta's App Review duration is quoted from developer reports (two to four weeks), not from a
  published SLA; it is the schedule's largest external risk and starts in sprint 1.
- The Your Field API's rate limits are not published (`first-customer-classscout.md`); the connector polls hourly
  with ETag / `updatedAt` diffs and backs off on 429.
- DoneIsBetter SSO's protocol details are assumed to be OIDC (§12).
- Whether the platform will accept a `reply.` MX on its domain, or the machine sends from its own
  domain on the platform's behalf, is a sprint-0 configuration question (P-11); the sending guard
  works either way.
- A C2PA certificate in the platform's name is the platform's purchase; the pilot may run on a
  self-signed certificate with the caveat stated.
