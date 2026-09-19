# business.direct — technical design

*Written 2026-09-19 on `11-architecture.md`'s PROPOSED containers. Where the prototype
already implements a rule, the section names the function in `assets/app.js` so a
developer can read the behaviour before the code exists.*

## 1. Screens and templates

| View | Screen | Template | Prototype function |
|---|---|---|---|
| Platform | Overview | title + tiles + two columns (flow queue · pipeline and departments) + providers | `platform.overview` |
| Platform | Social publishing | week calendar + queue of post cards | `platform.social` |
| Platform | Provider sales | pipeline strip + sequences · reply inbox + providers in stage | `platform.sales` |
| Platform | Approvals | one list of every *waiting* draft | `platform.approvals` |
| Platform | Providers | search + chips + table + drawer | `platform.providers`, `openDrawer` |
| Platform | Generated pages | table | `platform.pages`, `genPages` |
| Platform | Integrations | card grid | `platform.integrations` |
| Platform | Knowledge and rules | file editors | `platform.knowledge`, `kfiles` |
| Provider | Today | hero card + (invitation · or · tiles, waiting, team, knowledge) | `provider.today` |
| Provider | Knowledge | file editors | `SCREENS.provider.knowledge` |
| Family | Inbox | published post · digest · provider SMS | `family.inbox` |
| Family | Saved | listing cards | `family.saved` |
| Family | Preferences | toggles + stop | `family.prefs` |

Navigation: rail ≥ 1024, bottom bar below (`app.css`), the role switch in the top bar;
deep links `?view=&screen=` (`app.js`, bottom). Layout rules: `05-layout-specs.md`.

## 2. Content model (MongoDB, `platform_id` on every document)

```
providers_cache  { _id: <platform provider id>, platform_id, ...Provider (SSOT §3), synced_at }
provider_state   { provider_id, platform_id, stage, stage_changed_at, stage_changed_by, version }
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
```

Indexes: `provider_state (platform_id, stage)`, `drafts (platform_id, state, scheduled_for)`,
`messages (family_id, sent_at)` for the cap query, `consents (family_id, channel, provider_id)`.

## 3. Data mapping — platform → cache

`data/fetch-yourfield.py` is the mapping (one function, `full(card)`), reproduced in the
sync worker: the list endpoint gives the card and `claimStatus`; the single record gives
sessions, announcement, trial policy, geo, verified fields. Missing neighbourhood → borough
(`app.js`, load). Diff on `updatedAt`; a new `sessions[]` id at a provider a family has
saved raises an *alert* draft.

## 4. State machines

**Draft (post)** — `waiting → scheduled → published`; `waiting → skipped`; `waiting → (edit) →
scheduled` with `ai=false` and an `approvals` row carrying the diff. Prototype:
`approve`, `edit`/`save`, `skip` actions.

**Draft (sequence, reply)** — `waiting → sent` (sequence: all steps enqueued; reply: one
message); `waiting → skipped`; radar notes `waiting → filed`. Prototype: `approveSeq`,
`approveReply`.

**Pipeline stage** — forward on events only (R9):

| From | To | Event | Prototype |
|---|---|---|---|
| identified | contacted | first sequence message sent | `sendInvitation` |
| contacted | replied | inbound message from the provider | `sendInvitation` (sample replies) |
| replied | applied | claim request submitted (platform `claim-requests`) or a "yes" reply confirmed by the operator | `approveReply` |
| applied | managing | platform confirms the claim | `apply` (provider view) |
| managing | upgraded | a paid product on the platform | drawer chip only |
| any | any | operator moves by hand; logged with `stage_changed_by: 'operator'` | `data-setstage` |

**Family channel** — `on ↔ off` per channel; *Stop* → every channel off + cancel queued
drafts for that family. Consent for SMS is a separate append-only record; the toggle
cannot turn SMS on without a consent row.

## 5. Jobs (Vercel Cron → outbox workers)

| Job | Schedule | Does |
|---|---|---|
| `sync` | hourly | pull the catalogue, diff, write `providers_cache`, raise alert drafts |
| `draft-social` | 08:00 daily | for providers with news and no draft this week: build a post draft from the knowledge files (AI if the department's switch is on, else the listing's own text — `draftCopy`) |
| `sequence-step` | 09:00 weekdays | for every approved sequence: enqueue the due step per recipient not yet replied; skip addresses with `not my program` or unsubscribe |
| `digest` | Sunday 17:00 build, 18:00 send | per family with `picks` on: saved + nearby-with-session rows; cap check; outbox |
| `publish` | every 5 min | send due `scheduled` posts through the adapter; write `messages`, snapshot to Blob |
| `send` | every minute | drain the outbox: cap check again (R3), send, log; retry with backoff; dead-letter after 5 |
| `retention` | nightly | drafts 90 days after final state; messages 24 months |

## 6. Connectors and adapters

```ts
interface PlatformConnector {
  listProviders(): Promise<ProviderCard[]>;      getProvider(id): Promise<Provider>;
  facets(): Promise<Facets>;                     siteCopy(): Promise<SiteCopy>;
  createClaimRequest(providerId, contact): Promise<void>;   // keyed
  notifyFamily(familyId, payload): Promise<void>;           // keyed
  publishPage(page): Promise<{url}>;                        // keyed (Sportolok: POST /api/ingest)
}
interface ChannelAdapter {
  preview(draft): Rendered;   publish(draft): Promise<{providerMessageId}>;
  onInbound(webhook): InboundMessage | null;   verify(webhook): boolean;
}
```

`YourFieldConnector` maps `/api/public/*`; `SportolokConnector` maps `/api/*` incl.
`ingest`. Adapters: `ResendAdapter`, `MetaAdapter` (Instagram + Facebook), `TikTokAdapter`,
`XAdapter`, `TwilioAdapter`, `PlatformPushAdapter`.

## 7. Drafting (optional AI)

Prompt = the department's knowledge files (`rules/voice.md`, `rules/consent.md`,
`rules/social.md`; provider: `knowledge/*.md`) + the provider record + the event. Output is
a draft with `ai=true` and a `why` line the operator reads. With AI off: templates over the
listing's own text (the prototype's `draftCopy`, the sequence template with merge fields).
Published AI content is marked where Art. 50 applies; internal drafts carry the ✦ badge.

## 8. Forms and inputs

Operator: approve/edit/skip (Server Actions, optimistic UI, `version` check); knowledge
file editor (textarea, saved on blur, versioned); sequence editor (subject, body, steps);
integration connect (OAuth redirect, callback stores `token_ref`). Provider: apply-to-manage
(one button → platform claim request), knowledge editor. Family: toggles, stop, consent
capture (checkbox + text stored verbatim as proof).

## 9. i18n

Copy in English; the reference instance needs Hungarian. Strings in a per-instance
dictionary; dates and times in the instance's locale; legal footers per market (CAN-SPAM
address vs Hungarian Act XLVIII wording).

## 10. URLs and SEO

business.direct's own URLs are private (console). Generated pages are the platform's
(`getyourfield.com/nyc/<activity>-<area>`), written through the connector with the
platform's template, `LocalBusiness` JSON-LD per provider (the reference instance already
does this), and only where R6 holds.

## 11. Media

Post media: the provider's card image (from the platform) or an upload to Blob; alt text
required; conversion keeps alpha; served resized (1080 × 1350 IG, 1200 × 630 FB).

## 12. Performance

Console: server-rendered lists, paginated at 50 providers; the providers table filters on
the server. Digest build is a job, never a request. Caps in Redis, O(1) per check.

## 13. Operations

Dashboards: outbox lag, sends per channel per day, cap checks (0 violations), stage
transitions per day, opt-outs. Runbooks in §9 of the architecture. Backups: Atlas daily,
Blob versioned. Data deletion: platform webhook → delete `families_prefs`, anonymise
`messages`, keep `consents` (legal hold) with the id hashed.
