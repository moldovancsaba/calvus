# business.direct — system blueprint: modules, drawings, interfaces and pseudo code for the real system

*Written 2026-09-20 (D37) from `11-architecture.md` (the ADRs), `12-technical-design.md` (the
data model, the state machines, the jobs), `01g-research-real-system.md` (every service verified)
and the prototype (`../index.html`, `../assets/app.js`), which is the behavioural specification: every
screen, rule and state the prototype shows exists here as a module. This is the document a
developer builds from. It says **what module goes where, what it owns, what it calls, and how it
works** — in drawings, interfaces and pseudo code. The sprint plan with acceptance tests is
`13-implementation-plan.md`. Terms are the SSOT's (`10-ssot.md`); rules are cited as R-numbers.*

## 1. How to read this

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

## 2. Drawings

### 2.1 System context

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

### 2.2 Deployment (what runs where)

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

### 2.3 Module map (inside `src/modules`; arrows = imports; nothing imports a channel except the outbox)

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

### 2.4 The outbound pipeline (every message, every channel)

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

### 2.5 The inbound pipeline (every reply, comment, DM, STOP, payment)

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

### 2.6 The clip engine (D28, R30, R34, R20)

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

### 2.7 Draft state machine (unchanged from `12-technical-design.md` §4; the outbox adds its own)

```
 drafts:   waiting ──approve──▶ scheduled ──publish──▶ sent
             │  └──edit──▶ waiting (ai=false)         └──fail×5──▶ failed
             └──skip──▶ skipped
 outbox:   queued ──checks ok──▶ sending ──2xx──▶ sent
             │  └──refused (cap · consent · gate · guard)──▶ refused
             └──error──▶ queued (attempts+1, next_at = backoff) ──attempts≥5──▶ dead
```

## 3. Repository layout (one Next.js app, one worker, one package of pure rules)

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
    ui/                               # Mantine + GDS tokens (14-token-map.md); the prototype's components
  worker/                             # §10 — Dockerfile, server.ts, clips.ts, credentials.ts; deployed to Fly.io
  tests/                              # unit (rules), contract (connector fixtures), e2e (Playwright)
  vercel.json                         # crons (§6)
  fly.toml
```

Rules of the layout: a module's `index.ts` is its only public surface; `channels/*` is imported only
by `outbox` and the webhook routes (an ESLint `no-restricted-imports` rule enforces it — this is the
"a Server Action cannot send" test made static); `db/` is imported only by modules, never by pages;
pages call Server Actions in `modules/*/actions.ts`.

## 4. Module catalogue

Each entry: **Owns** (collections it writes), **Reads**, **Exposes** (its `index.ts`), **Rules**,
**Pseudo code** for the parts that are not obvious.

### 4.1 `policy` — the record and the gate (ADR-14, R26)

Owns `policies`. Reads nothing else. Exposes `record(platformId)`, `gate(feature, ctx)`,
`basis(feature, ctx)`. Rules: R26 and every row of `18-responsible-data-policy-framework.md` §3.

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

### 4.2 `catalogue` — connector, sync, diff (ADR-2)

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

`YourFieldConnector` maps the twelve public endpoints found in `02-audit.md`; keyed writes
(`createClaimRequest`, `notifyFamily`, `publishPage`, `savesFor`, `familiesNear`, `setCardFlag`) throw
`NotKeyed` until `integrations.platform.key` exists (P-7), and every caller handles `NotKeyed` by
writing a task for the operator, never by failing silently.

### 4.3 `pipeline` — stages and the propensity score (ADR-13)

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

### 4.4 `drafting` — the drafter, the templates, the pattern guard (ADR-7, R10, R14, R32, R36)

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

### 4.5 `approvals` — the human gate and earned auto-approval (R1, R25)

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

### 4.6 `outbox` — see §7 (the full pseudo code)

Owns `outbox`, `messages`. Exposes `enqueue(msg)`, `cancelFor(familyId)`, and the job `send`.

### 4.7 `channels` — one adapter per channel (12-technical-design §6)

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

### 4.8 `sequences` — the three-touch sales sequence (D28, R23, Q2)

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

### 4.9 `campaigns` — provider campaigns, audiences from the platform only (ADR-10, R3, R11)

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

### 4.10 `conversations` — enquiries, comments, DMs, drafted answers (phase 3, R14)

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

### 4.11 `families` — preferences, consents, digest, alerts, Stop (ADR-6, R3, R4, R28)

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

### 4.12 `media` — the clip engine's app side, consent, credentials (D28, ADR-12, R15, R20, R30, R34)

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

### 4.12b `retention` — reduce churn (D41, R37)

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

### 4.13 `billing` — products, Stripe Checkout, entitlements (ADR-9, R32 cooling-off)

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

### 4.14 `pages` — generated neighbourhood × activity pages written to the platform (ADR-8)

Owns `generated_pages`. Reads `providers_cache`, `assumptions` (readiness). Exposes the operator's
`generate(activity, area)` and `publish(pageId)`; rules: ≥ 3 providers; readiness ≥ 3 of 4
(BD-4-11); JSON-LD `ItemList`; published only through `connector.publishPage` (keyed).

### 4.15 `analytics` — events, nightly metrics, assumptions, the experiment (ADR-11, R16–R19)

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

### 4.16 `recommend` — the Simple mode's Home and the one safe press (D33, R29)

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

### 4.17 `knowledge` — the knowledge files (R10)

Owns `knowledge_files`. Exposes `filesFor(ctx)` (platform files + the provider's files), the editors'
Server Actions with versions, `department(platformId, kind)` (the AI switch). Files are the prompt
context; every edit is versioned; a provider edits only its own.

## 5. Data contracts (Zod at every boundary; Mongoose models mirror them)

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
export const Policy = /* 18-responsible-data-policy-framework.md §2, every field typed; `postal_address` z.string().min(10) */;
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

Collections and indexes: `12-technical-design.md` §2 plus `outbox (platform_id, state, next_at)`,
`outbox (to.family_id, state)` for `cancelFor`, `messages (to.family_id, sent_at)` for the cap
query's fallback, `events (platform_id, at)`, `media_jobs (state)`, `sync_runs (platform_id, at)`,
`stage_history (provider_id, at)`, `tasks (platform_id, state)`. TTL index on `messages.sent_at`
(24 months) and `drafts.final_at` (90 days) — the `retention` job only reports what TTL did.

## 6. Jobs → `vercel.json` crons → `/api/cron/[job]`

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

## 7. The outbox in full (ADR-3, ADR-4, R3, R4, R23, R26)

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

## 8. Security

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

## 9. Configuration (`env.ts`, one Zod object)

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

## 10. The media worker (Fly.io, `worker/`)

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

## 11. Testing (what proves the invariants)

| Level | What | Tool |
|---|---|---|
| Static | no import of `channels/*` outside `outbox` and the webhook routes | ESLint `no-restricted-imports` (fails the build) |
| Unit | `policy.gate` per feature × missing field (framework §3, ten rows); `patternGuard` per banned pattern; `pipeline.setStage` illegal moves; `score`; `econ.*` against the prototype's numbers (the 24 inputs → LTV : CAC 0.7 at defaults); `findMoments` drops utterances with a name | Vitest |
| Contract | `YourFieldConnector` against recorded fixtures from `02-audit.md` (253 providers; a changed `updatedAt` → one diff event); schema-drift test fails when a field disappears | Vitest + fixtures |
| Integration | webhook routes with recorded payloads (Resend received/bounced, Meta comment + verification GET, Twilio STOP, Stripe `checkout.session.completed`) → the right row and no duplicate on replay; `families.stop` cancels queued rows in one transaction; the cap race (two sends, one slot → one sent, one refused) | Vitest against a MongoDB Memory Server + Upstash test db |
| End-to-end | the operator's routine on the console: approve a post → it appears `scheduled` → `publish` run with a stub adapter → `messages` row + snapshot; a provider approves a campaign → audience count shown before approval; a family opens the signed link and turns picks off → the next digest run skips them; Simple mode's press runs only `auto` recommendations | Playwright, against `next start` with `DRAFTER=template` and stub adapters |
| Load | 5 000 outbox rows drained within an hour at 100/minute; `send` tick < 60 s | a script, measured in the build log |
| Security | signature failure → 401 and no row; cron without secret → 401; provider A cannot read provider B (`assertOwns`) | Vitest |

Every rule R1–R36 that is code has at least one test that names it (`describe('R3 cap …')`), so the
rules map (`09-business-logic.md`) can be checked against the test names by the gate.

## 12. Operations

- **Health**: `/api/health` returns `{outbox_lag_s, dead_rows, last_sync_at, last_send_at, webhook_failures_24h, cap_violations (must be 0), send_errors_by_channel}`; Better Stack pages on non-200 or `outbox_lag_s > 1800`.
- **Runbooks** (`docs/runbooks/` in the new repo): Meta token expired (re-connect on the Integrations screen; queued posts wait, nothing is lost); a provider says "not my program" (the opt-out is automatic; check the thread); a family's deletion request (platform webhook or the operator's *Erase* action → `families.erase`, confirmation logged); bounce pause (the sequence card shows "paused: bounce ≥ 2 %"; fix the list, reset `sending.bounce_rate` after review); a dead outbox row (the Approvals screen's "failed" tab; retry or refuse with a reason).
- **Backups**: Atlas continuous backup at M10; Blob is the audit copy of every published post; the policy record's history is versioned in `policies` (`version` increments; old versions kept).
- **Release**: `main` → production; preview per branch; feature flags per instance in `instances.flags` (`social`, `campaigns`, `sms`, `clips`, `pages`) so a sprint ships dark.

## 13. The prototype → the modules (continuity)

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
