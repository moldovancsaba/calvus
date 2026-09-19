# business.direct — single source of truth

*Written 2026-09-19 after gate 2 and the first build round (D16–D18). Every term the
other engineering documents use is defined here; where a term is DiscountDirect's, it
says so (D5). The prototype (`../index.html`, `assets/app.js`) is the reference
implementation of the enumerations and state machines below.*

## 1. Glossary

| Term | Meaning | Where it shows |
|---|---|---|
| **Platform** | the listing site that runs the machine — Your Field NYC first (D11); *Most én sportolok!* a reference instance | the Platform view |
| **Operator** | the person at the platform who approves what leaves the machine; one person by design | the approval queue |
| **Provider** | a listed business — the platform's own word for it (`/api/public/providers`). Reference instances may call it *listing* | everywhere |
| **Family** | the consumer on Your Field; a parent with children and saved providers. Reference instances: *user*, *visitor* | the Family view |
| **Card** | a provider's public page and record on the platform, built by the platform's enrichment from the provider's own website | the drawer's "On the card (real)" |
| **Claim** | a provider taking over its card. The platform's `claimStatus` (`unclaimed` / unset today); business.direct's pipeline adds *applied* and *managing* | pipeline |
| **Flow** | one of the two front-door processes (D14): **B2C social publishing** and **B2B provider sales** | the rail's *Flows* group |
| **Department** | a bounded automation with its own approvals and an optional AI switch: social publishing, provider sales, weekly picks, generated pages, market radar; on the provider side: conversations and reputation, reminders, campaigns, page and visibility | department cards |
| **Draft** | anything the machine wrote and has not sent: a post, a sequence step, a reply, a digest | approval cards |
| **Approval** | the operator's (or provider's) decision on a draft: approve, edit-then-approve, skip | the queue, the toast |
| **Sequence** | a multi-step outbound series to providers (invitation → reminder → call task) with one approval for the whole run | provider sales |
| **Pipeline stage** | where a provider stands with the platform: see §2 | pipeline strip, drawer chips |
| **Reply inbox** | inbound messages from providers with a drafted answer each | provider sales |
| **Digest** | the family's weekly "this week near you" e-mail from saved providers and nearby providers with a session | family inbox |
| **Alert** | a push to a family when a saved provider adds a session | preferences |
| **Consent** | a family's recorded permission per channel, and per provider for SMS (TCPA, research §8) | preferences, the SMS's "why you got this" |
| **Cap** | the frequency cap across every channel: 4 messages per family per month (`rules/consent.md`) — DiscountDirect's term | preferences |
| **Knowledge file** | a plain-text file the machine reads before writing: voice, offer, FAQ, consent rules, social rules | knowledge screens |
| **Generated page** | an activity × neighbourhood landing page published only where ≥ 3 providers exist | generated pages |
| **Campaign** | a provider's message to families built from its card — trial class, open spots, announcement, registration — approved by the provider, sent by each family's preferences under the cap (D22) | provider campaigns, family inbox |
| **Audience** | the families a campaign may reach: those who saved the provider, plus nearby families with a child in the age range; sample counts today | campaign card |
| **Product** | one of the platform's paid reach products — featured listing, camp placement, local discovery profile (D21); prices sample | provider today, drawer, results |
| **Upgrade** | a provider buying a product; moves the stage to *upgraded* | pipeline |
| **Enquiry** | a family's message to a provider — platform message, e-mail or missed call — with an answer drafted from the provider's knowledge files (D25) | provider conversations, family inbox |
| **Comment** | a comment or DM on a published post, with a drafted reply that links to the listing (D25) | social publishing, approvals |
| **Propensity score** | 0–100 per provider from the card (e-mail, phone, trial, session, announcement, image, verified fields, unclaimed flag) and events (replied, applied, thread); orders the sequence and the call list (R22) | providers table, sequences |
| **Anchor** | the week's one piece per neighbourhood × activity, cut into a Reel, a carousel, a story, a digest item and a page update | social publishing |
| **Media adapter** | one of video, image, audio, clips — a service behind one interface; clips (from real footage) is v1, the rest later | media department |
| **Holdout** | a neighbourhood where the content engine is off for the experiment's weeks; the comparable treatment neighbourhood has it on | social anchors, economics |
| **Recap** | the weekly intelligence screen: what moved, by department, the market radar, what needs the operator (D23) | intelligence |
| **Integration** | a connector that gives the machine hands: the platform API, social channels, e-mail, push, SMS, Google Business Profile, calendar | integrations |
| **Real / sample** | real = from the platform's public API, never edited; sample = generated for the prototype from real providers and declared as such (D18) | every tile's third line |

## 2. Enumerations

| Enumeration | Values | Source |
|---|---|---|
| `role` | `platform` · `provider` · `family` | D2; `app.js` `S.role` |
| `pipelineStage` | `identified` → `contacted` → `replied` → `applied` → `managing` → `upgraded` | D15; `STAGES` |
| `draftState` | `waiting` · `scheduled` · `published` · `skipped` (posts, campaigns); `waiting` · `sent` · `filed` · `skipped` (sequences, replies) | `stateBadge` |
| `campaignKind` | `Trial class` · `Open spots` · `Announcement` · `Registration` · `Hello` (fallback when the card has none of the four) | `campaignsFor` |
| `product` | `featured` · `camp` · `profile` | `S.products` |
| `enquiryChannel` | `Platform message` · `E-mail` · `Missed call` | `enquiriesFor` |
| `integrationTier` | `v1` · `later` (D21) | `S.integrations[].v1` |
| `channel` (B2C) | `Instagram` · `Facebook` · `TikTok` · `X` (posts); `email` · `push` · `sms` (families) | D14; `post.channels`, `family.prefs` |
| `channel` (B2B) | `email` · `phone` (from the card) · `website form` (neither on the card) | providers table, "Contact on card" |
| `department` (platform) | `social` · `sales` · `picks` · `pages` · `radar` | `S.ai` keys |
| `department` (provider) | `conversations` · `reminders` · `campaigns` · `page` | provider today |
| `integrationState` | `ok` (connected) · `off` (not connected) | `S.integrations` |
| `claimStatus` (platform's) | `unclaimed` · unset (237 of 252); the platform's own enumeration has more values we have not seen | `providers.json` |
| `activityType` | 20 values as the platform's `browse-facets` lists them (Martial Arts, Dance, Swimming, Soccer, …) | `platform.json` |
| `borough` | `Manhattan` · `Brooklyn` (today) | facets |

## 3. Canonical entities

| Entity | Fields (prototype) | Notes |
|---|---|---|
| **Provider** | `id`, `name`, `category`, `borough`, `neighborhood`, `address`, `lat`, `lng`, `activityTypes[]`, `primaryActivityType`, `ageRanges[]`, `ageMinMonths`, `ageMaxMonths`, `shortDescription`, `longDescription`, `price{amount,currency,unit,evidence}`, `website`, `phone`, `email`, `image`, `dayTimeTags[]`, `venueModel`, `sessions[{id,title,registration}]`, `nextOccurrence`, `announcement{title,description,badge}`, `bookingEnabled`, `trial{available,free,text}`, `rating`, `reviewCount`, `badges[]`, `claimStatus`, `verifiedFields[]`, `updatedAt`, `publishedAt`, `sourceCount` | the platform owns it; business.direct reads it (`fetch-yourfield.py`). One of 252 has no neighbourhood; the borough stands in |
| **ProviderState** (ours) | `providerId`, `stage`, `stageChangedAt`, `stageChangedBy` (`sequence` / `reply` / `operator` / `provider`), `thread[]` | in memory today (`S.stage`, `S.threads`) |
| **Draft** | `id`, `kind` (`post` / `sequence` / `reply` / `digest`), `providerId?`, `channels[]`, `copy`, `media?`, `state`, `ai` (bool: AI-drafted), `scheduledFor?`, `why?` | `S.posts`, `S.sequences`, `S.replies` |
| **Sequence** | `id`, `name`, `to[providerId]`, `steps[]`, `subject`, `body` (merge fields `{name}`, `{first name}`, `{neighborhood}`, `{activity}`, `{link}`), `state`, `why` | `S.sequences` |
| **Family** | `name`, `neighborhood`, `borough`, `kids[{name,age}]`, `saved[providerId]`, `prefs{picks,alerts,nearby,sms}`, `smsConsent[providerId]` | the platform owns the account; business.direct owns preferences and consent records |
| **KnowledgeFile** | `path`, `text`, `owner` (`platform` / `providerId`) | `S.knowledge` |
| **Integration** | `id`, `name`, `what`, `state`, `label`, `note` | `S.integrations` |
| **GeneratedPage** | `activity`, `area`, `n`, `slug` | computed (`genPages()`), threshold 3 |
| **Campaign** | `id`, `providerId`, `kind`, `title`, `copy`, `audience{saved,nearby}`, `channels[]`, `state`, `ai`, `scheduledFor?` | `S.campaigns[pid]`, built on first visit from the card |
| **Product** | `id`, `name`, `what`, `price` | `S.products` — the platform's list; prices sample |
| **Enquiry** | `id`, `providerId`, `from{name,kid,area}`, `channel`, `at`, `text`, `draft`, `state`, `ai`, `sentIn?` | `S.enquiries[pid]`; a family's ask is unshifted with `from.name` = the family |
| **Comment** | `id`, `postId`, `providerId`, `channel`, `from`, `text`, `draft`, `state`, `ai` | `S.comments`, created when a post is approved |
| **MediaAdapter** | `id`, `name`, `vendor`, `state` (`v1` / `later`), `use` | `S.media.adapters` |
| **Sending** | `domain`, `warmDay`, `warmDays`, `dailyCap`, `bounce`, `replySla` | `S.sending`; per `platform_id` in production |
| **Experiment** | `name`, `treat`, `control`, `weeks`, `week`, `state` | `S.experiment` |
| **Entitlement** | `providerId`, `productId`, `since`, `billingRef?` | `S.bought` |

## 4. Settings the prototype fixes

| Setting | Value | Why |
|---|---|---|
| Family frequency cap | 4 messages / month across every channel | research §4, `rules/consent.md` |
| Digest day and time | Sunday 18:00 | research §4 |
| Generated-page threshold | ≥ 3 providers | no thin pages, research §5 |
| Invitation sequence | invitation → reminder after 5 days → call task for phone-only providers | research §2–3 |
| Opt-out handling | every provider e-mail carries an opt-out; honoured within 10 business days | CAN-SPAM, research §8 |
| SMS to families | only with written consent per provider | TCPA, research §8 |
| AI drafts | optional per department; default on for social, sales, radar, provider conversations (and so campaigns); off for picks and pages | D6 |
| Campaign audience | saved families + nearby families in the age range; the provider cannot widen it | D22 |
| Products and prices | the platform's three products; prices sample until the platform sets them | D21 |
| v1 integrations | platform API, Resend, Instagram + Facebook, platform push | D21 |
| AI-content marking | drafts carry the ✦ AI badge internally; published content is marked per EU AI Act Art. 50 where it applies (from 2 Aug 2026) | research §7 |

## 5. Decision register

`04-decisions.md` holds D1–D28. The ones the engineering documents rest on: D2 (three
views), D5 (DiscountDirect sibling), D6 (departments, knowledge layer, human-in-the-loop,
optional AI, dashboard, integrations), D11 (Your Field first), D14 (two flows), D15
(post card and pipeline strip), D17 (one page, in-memory state), D18 (sample generated
from the real catalogue). Stack decisions are ADRs in `11-architecture.md` §11, all
PROPOSED.

## 6. Rules register

| # | Rule | Where enforced |
|---|---|---|
| R1 | Nothing leaves the machine without a person's approval — a post, a sequence, a reply, a digest change | approval queue; production: the outbox only takes `approved` drafts |
| R2 | Every message names why it was sent and how to stop it | post link, SMS "why you got this", e-mail footer |
| R3 | A family receives at most the cap, across all channels and all providers | production: Redis counter per family per month (ADR-3) |
| R4 | SMS to a family only with written consent for that provider; e-mail and push by preference | `family.prefs`, `smsConsent` |
| R5 | Provider e-mail without prior consent is lawful in the US (CAN-SPAM) but every message carries a working opt-out; a "not my program" reply stops the sequence for that address | `notMine` action |
| R6 | A generated page exists only where ≥ 3 providers exist | `genPages()` |
| R7 | Every non-catalogue figure is labelled sample until a real source feeds it | tiles' third line |
| R8 | The machine reads the knowledge files before every draft; the operator can read and edit them | knowledge screens |
| R9 | A pipeline stage moves forward automatically only on an event (e-mail sent, reply received, application submitted); backwards only by a person | `sendInvitation`, `approveReply`, drawer chips |
| R10 | AI is optional per department; with it off, copy is the listing's own text | `S.ai`, `draftCopy` |
| R11 | A campaign reaches only families who saved the provider or are nearby with a child in the age range, by their preferences, under the cap; the provider approves the copy, never the list | `campaignsFor`, `campaignCard` |
| R12 | An upgrade never changes what a family receives — it changes where the provider appears | products |
| R14 | Every enquiry gets a drafted answer within a minute and a sent answer only after the provider's approval; reply time is measured from the enquiry, not from the draft | `enquiriesFor`, `approveEnquiry` |
| R15 | The machine never generates a person or a child; it edits the provider's real photos and generates places, objects, type and motion only | media department |
| R20 | Every generated asset carries a C2PA credential at creation and the platform's disclosure at publish; the credential is kept in the audit snapshot | post card labels; outbox |
| R21 | A provider's real recording beats any generation; the clip engine is the v1 media service; generation fills gaps only | provider media, social queue |
| R22 | A propensity score per provider orders every sequence and the call list; it is recomputed nightly from the card and the events | `score()`, providers table |
| R16 | The next-dollar ranking runs weekly on measured rates where they exist and on the documented assumption where they do not; the recap says which | `econ()`; `16-analytics…` §4 |
| R17 | A sequence step is added or removed when its marginal reply rate per touch falls below the cost-per-touch breakeven for two consecutive weeks, inside the 4–7 benchmark | production |
| R18 | Content slots go to the neighbourhood × activity pairs with the highest families-per-post over four weeks; a new pair gets one slot a week to be measured | production |
| R19 | The upgrade card appears only when a provider's delivered value exceeds the product's annual price | provider results (P8) |
| R13 | The machine never discounts; offers with a price cut are DiscountDirect's domain (D5) | — |

## 7. Metrics

| Metric | Definition | View |
|---|---|---|
| Providers managing | providers in `managing` or `upgraded` / all providers | platform overview (real: 0 / 252 today) |
| Contactable | providers with e-mail / with phone | overview (130 / 180) |
| Families from social | sign-ups whose first session had a social referrer | overview (sample until a channel is connected) |
| Posts scheduled | approved posts this week / drafted | overview, calendar |
| Reply time | median time from an enquiry to the sent answer, per provider | provider conversations and results (sample until real enquiries) |
| Comments answered | replies sent / comments received on published posts | intelligence |
| Trials booked | bookings with `trial` in the session, per provider per week | provider today (sample) |
| Opt-outs | families who turned a channel off or stopped everything, per month | production only |
| Families reached by campaigns | sum of approved campaigns' audiences after the cap | intelligence (sample audiences) |
| Upgrade revenue | sum of active entitlements' prices per month | intelligence (sample prices) |
| CAC (managing / upgraded) | outbound cost ÷ new managing / paying providers | economics |
| LTV | ARPA × margin ÷ monthly churn | economics |
| Payback | CAC ÷ monthly contribution | economics |
| Avid family | saved ≥ 3, opened the last two digests, asked once | economics, family events |
| Marketing value of an avid family | platform capture of delivered value + referral value, per year | economics |
| Cost per family from content | content stack ÷ families from posts | economics |
| Next dollar | expected LTV gained per $ for touch / call / content | economics, recap |

## 8. Document map

| Doc | Holds |
|---|---|
| `00-brief.md` | client, problem, views, flows, what is real |
| `01-research.md` | sourced evidence, legal by market |
| `02-audit.md` | the platform measured, the catalogue's coverage, the videos, DiscountDirect's contribution |
| `03-sources.md` | real vs sample |
| `04-decisions.md` | D1–D18 |
| `05-layout-specs.md`, `design-system.html`, `layouts.html` | gates 1 and 2 |
| `06-build-log.md`, `07-gate.md` | rounds and the measured pass |
| `08-client-asks.md` | open items |
| `09-business-logic.md` | the rules end to end: parties, flows, departments, campaigns, money, families, law, recap |
| `16-analytics-and-unit-economics.md` | CAC, LTV, avid value, content ROI, next dollar, metrics tree, events, attribution |
| `10-ssot.md` (this) | terms, enumerations, entities, rules, metrics |
| `11-architecture.md` | context, quality attributes, containers, flows, stack, ADRs |
| `12-technical-design.md` | data model, state machines, connectors, jobs, operations |
| `13-implementation-plan.md` | milestones, issues with DoD, blocked register, risks |
| `14-token-map.md` | prototype tokens and components → production |
