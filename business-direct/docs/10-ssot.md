# business.direct — single source of truth

*Written 2026-09-19 after gate 2 and the first build round (D16–D18); the product layer
added 2026-09-20 (D41). Every term the other documents use is defined here; where a term is
DiscountDirect's, it says so (D5). **The product's terms** are media owner · advertiser ·
visitor · listing · instance; **the first instance's words** for them are platform · provider ·
family · card · Your Field NYC, and because the prototype and the engineering documents were
written on the first instance's data they use the instance's words in identifiers and
examples — the mapping in §1a is the rule. The prototype (`../index.html`, `assets/app.js`)
is the reference implementation of the enumerations and state machines below.*

## 1a. The product layer (D41)

| Product term | Meaning | The first instance's word (Your Field NYC) | In code |
|---|---|---|---|
| **Media owner** | the classified media owner who buys and runs business.direct; the operator is the person at the owner who approves | platform | `role = platform`, `platform_id` |
| **Listing** | a business's page on the site, built by the site from public data; the unit of inventory the owner sells | card | `providers_cache` |
| **Advertiser** | a listed business — a prospect until it manages its page, a customer once it pays for a placement | provider | `provider_id`, `provider_state` |
| **Visitor** | a person using the site; an engaged visitor saves, opens the digest and enquires | family | `family_id`, `families_prefs` |
| **Instance** | one site with its own policy record, connector, sending domain and products | Your Field NYC | `instances`, `policies` |
| **The three jobs** | marketing (content → media → visitors), B2B sales (contact → acquire), retention (reduce churn) | the two flows (D14) + retention (D41) | departments `social`, `picks`, `pages`, `radar` · `sales` · `retention` |
| **Placement / advertising product** | what the owner sells to an advertiser — featured, category, discovery profile | reach product | `products`, `entitlements` |


## 1. Glossary

| Term | Meaning | Where it shows |
|---|---|---|
| **Client** | the company that buys business.direct — **ClassScout** first, operator of Your Field NYC | policy record |
| **Platform / instance** | the listing site the machine runs on — Your Field NYC first (D11); *Most én sportolok!* a reference instance; each instance has its own policy record (D32) | the Platform view |
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
| **Cap** | 4 provider-originated messages per family per month — campaigns and texts across all providers; the platform's digest and alerts follow the family's switches and do not count (D30; `rules/consent.md`) — DiscountDirect's term | preferences |
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
| **Mode** | `simple` (guided, semi-automatic: Home with recommendations and one safe press) or `advanced` (every screen and input); the rules are identical in both (D33) | top bar, `?mode=` |
| **Recommendation** | a ranked suggestion computed from state — what, why (with the figure), safe to run or needs judgement — shown on Home and run by one press when safe | `recommend()` |
| **Template** | a starting point the operator copies into the machine: a sequence, a post or campaign pattern, a knowledge file, a policy record for another client type | `TEMPLATES`, the *Templates* screen |
| **Help** | the *What is this?* panel per screen and the *How to use* screen | `HELP` |
| **Retention** | the department that watches every managing advertiser for the signals before a cancellation (a renewal due, a stale page, an unanswered enquiry, a listing that stopped surfacing) and drafts a touch from the advertiser's own numbers; kept and lost are logged (D41) | the Retention screen; `retentionFor()` |
| **At risk** | a managing or paying advertiser with at least one retention signal this week | Retention watch list; economics tile |
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
| `department` (platform) | `social` · `sales` · `retention` · `picks` · `pages` · `radar` | `S.ai` keys; the Retention screen |
| `department` (provider) | `conversations` · `reminders` · `campaigns` · `page` | provider today |
| `integrationState` | `ok` (connected) · `off` (not connected) | `S.integrations` |
| `claimStatus` (platform's) | `unclaimed` · unset (238 of 253); the platform's own enumeration has more values we have not seen | `providers.json` |
| `activityType` | 20 values as the platform's `browse-facets` lists them (Martial Arts, Dance, Swimming, Soccer, …) | `platform.json` |
| `borough` | `Manhattan` · `Brooklyn` (today) | facets |

## 3. Canonical entities

| Entity | Fields (prototype) | Notes |
|---|---|---|
| **Provider** | `id`, `name`, `category`, `borough`, `neighborhood`, `address`, `lat`, `lng`, `activityTypes[]`, `primaryActivityType`, `ageRanges[]`, `ageMinMonths`, `ageMaxMonths`, `shortDescription`, `longDescription`, `price{amount,currency,unit,evidence}`, `website`, `phone`, `email`, `image`, `dayTimeTags[]`, `venueModel`, `sessions[{id,title,registration}]`, `nextOccurrence`, `announcement{title,description,badge}`, `bookingEnabled`, `trial{available,free,text}`, `rating`, `reviewCount`, `badges[]`, `claimStatus`, `verifiedFields[]`, `updatedAt`, `publishedAt`, `sourceCount` | the platform owns it; business.direct reads it (`fetch-yourfield.py`). One of 253 has no neighbourhood; the borough stands in |
| **ProviderState** (ours) | `providerId`, `stage`, `stageChangedAt`, `stageChangedBy` (`sequence` / `reply` / `operator` / `provider`), `thread[]` | in memory today (`S.stage`, `S.threads`) |
| **Draft** | `id`, `kind` (`post` / `sequence` / `reply` / `digest`), `providerId?`, `channels[]`, `copy`, `media{kind: real / generated, src}` (posts, D28), `state`, `ai` (bool: AI-drafted), `editing?`, `scheduledFor?`, `why?` | `S.posts`, `S.sequences`, `S.replies` |
| **Sequence** | `id`, `name`, `to[providerId]`, `steps[]`, `subject`, `body` (merge fields `{name}`, `{first name}`, `{neighborhood}`, `{activity}`, `{link}`), `state`, `why` | `S.sequences` |
| **Family** | `name`, `neighborhood`, `borough`, `kids[{age}]` (ages only, R24), `saved[providerId]`, `prefs{picks,alerts,nearby,sms}`, `smsConsent[providerId]` | the platform owns the account; business.direct owns preferences and consent records |
| **KnowledgeFile** | `path`, `text`, `owner` (`platform` / `providerId`) | `S.knowledge` |
| **Integration** | `id`, `name`, `what`, `state`, `label`, `note` | `S.integrations` |
| **GeneratedPage** | `activity`, `area`, `n`, `slug` | computed (`genPages()`), threshold 3 |
| **Campaign** | `id`, `providerId`, `kind`, `title`, `copy`, `audience{saved,nearby}`, `channels[]`, `state`, `ai`, `scheduledFor?` | `S.campaigns[pid]`, built on first visit from the card |
| **Product** | `id`, `name`, `what`, `price` | `S.products` — the platform's list; prices sample |
| **Enquiry** | `id`, `providerId`, `from{name,kid,area}`, `channel`, `at`, `text`, `draft`, `state`, `ai`, `sentIn?` | `S.enquiries[pid]`; a family's ask is unshifted with `from.name` = the family |
| **Comment** | `id`, `postId`, `providerId`, `channel`, `from`, `text`, `draft`, `state`, `ai` | `S.comments`, created when a post is approved |
| **MediaAdapter** | `id`, `name`, `vendor`, `state` (`v1` / `later`), `use` | `S.media.adapters` |
| **Sending** | `domain`, `warmDay`, `warmDays`, `dailyCap`, `bounce`, `replySla` | `S.sending`; per `platform_id` in production |
| **OptOut** | `providerId`, `kind` (`not mine` / `unsubscribed` / `bounced`), `at` | `S.optOut`; excluded from every sequence |
| **StageChange** | `providerId`, `from`, `to`, `by` (`sequence` / `reply` / `family ask` / `provider` / `operator`), `at`, `reason?` | `S.history`; production: `events` |
| **Policy** | `platform_id`, `client`, `instance`, `contact`, `postalAddress`, `jurisdictions[]`, `laws[]`, `audienceModel`, `ageOfConsent`, `childData`, `minors{profiling,targetedAds,quietHours}`, `channels{}`, `consentText{}`, `defaults`, `cap`, `optOutSla`, `aiDisclosure`, `retention`, `privacyPolicy{url,lastUpdated,emailAlerts,savesOptIn,childrenNone}`, `dpia`, `mediaConsent`, `safeguarding`, `vulnerability`, `protected`, `accessibility`, `sensitive`, `darkPatterns` (D35) | `S.policies[instance]`; one per instance (D32) |
| **Experiment** | `name`, `treat`, `control`, `weeks`, `week`, `state` | `S.experiment` |
| **Entitlement** | `providerId`, `productId`, `since`, `billingRef?`, `attributedTo?` (the delivered result that preceded the purchase, Q8) | `S.bought`, `S.attributed` |
| **AutoApproval** | `owner`, `department`, `cleanWeeks`, `earned` (R25) | `S.auto` |
| **Recommendation** | `id`, `what`, `why`, `auto` (safe to run), `go?`, `act?` | `recommend()` (D33) |
| **RetentionTouch** | a `Draft` of kind `retain`: `providerId`, `renewal` (bool), `incoming` (the signals), `draft`, `state`; approving it marks the advertiser kept | `S.replies` with `kind: 'retain'`, `S.retained` |

## 4. Settings the prototype fixes

| Setting | Value | Why |
|---|---|---|
| Family frequency cap | 4 provider-originated messages / month; digest and alerts on preference | research §4, D30, `rules/consent.md` |
| Postal address | `{postal_address}` merge field per `platform_id`, required in every provider e-mail; the gate blocks a template without it | CAN-SPAM, D30, prerequisite P-1 |
| Earned auto-approval | four clean weeks per department; reminders earned by default (the booking is the consent) | D30 |
| Conversations line | economics input; 0 = bundled | D21, D30 |
| Digest day and time | Sunday 18:00 | research §4 |
| Generated-page threshold | ≥ 3 providers | no thin pages, research §5 |
| Invitation sequence | three touches 3–4 days apart (invitation → "a family saved you" → reminder), then the call task for phone-only providers (D28) | research II §5.1 |
| Opt-out handling | every provider e-mail carries an opt-out and the postal address; honoured within one business day (the law allows 10) | CAN-SPAM, research §8, policy `optOutSla` |
| SMS to families | only with written consent per provider | TCPA, research §8 |
| AI drafts | optional per department; default on for social, sales, radar, provider conversations (and so campaigns); off for picks and pages | D6 |
| Campaign audience | saved families + nearby families in the age range who turned "new provider nearby" on; the provider cannot widen it | D22, D30 (Q3) |
| Visitor defaults | every channel off until the visitor turns it on (R28); the demo visitor turned picks and alerts on and consented to one provider's SMS on 2026-09-02 | R28, policy `defaults` |
| Products and prices | the platform's three products; prices sample until the platform sets them | D21 |
| v1 integrations | platform API, Resend, Instagram + Facebook, platform push | D21 |
| AI-content marking | drafts carry the ✦ AI badge internally; published content is marked per EU AI Act Art. 50 where it applies (from 2 Aug 2026) | research §7 |

## 5. Decision register

`04-decisions.md` holds D1–D43. The ones the engineering documents rest on: D2 (three
views), D5 (DiscountDirect sibling), D6 (departments, knowledge layer, human-in-the-loop,
optional AI, dashboard, integrations), D11 (Your Field first), D14 (two flows), D15
(post card and pipeline strip), D17 (one page, in-memory state), D18 (sample generated
from the real catalogue). Stack decisions are ADRs in `11-architecture.md` §11 — the build
baseline since D37; the owner flips any with a decision.

## 6. Rules register

| # | Rule | Where enforced |
|---|---|---|
| R1 | Nothing leaves the machine without a person's approval — a post, a sequence, a reply, a digest change | approval queue; production: the outbox only takes `approved` drafts |
| R2 | Every message names why it was sent and how to stop it | post link, SMS "why you got this", e-mail footer |
| R3 | A family receives at most 4 provider-originated messages a month (campaigns, texts) across all providers; the platform's digest and alerts follow her switches and do not count (D30) | production: Redis counter per family per month (ADR-3) |
| R4 | SMS to a family only with written consent for that provider; e-mail and push by preference | `family.prefs`, `smsConsent` |
| R5 | Provider e-mail without prior consent is lawful in the US (CAN-SPAM) but every message carries a working opt-out; a "not my program" reply stops the sequence for that address | `notMine` action |
| R6 | A generated page exists only where ≥ 3 providers exist | `genPages()` |
| R7 | Every non-catalogue figure is labelled sample until a real source feeds it | tiles' third line |
| R8 | The machine reads the knowledge files before every draft; the operator can read and edit them | knowledge screens |
| R9 | A pipeline stage moves forward automatically only on an event (e-mail sent, reply received, application submitted, a family's ask); a person may move any stage in either direction and every move is logged with who and why (D30) | `setStage`, `S.history`, drawer chips |
| R10 | AI is optional per department; with it off, copy is the listing's own text | `S.ai`, `draftCopy` |
| R11 | A campaign reaches only families who saved the provider, or who are nearby with a child in the age range **and** turned "new provider nearby" on, by their preferences, under the cap; the card shows the reachable count; the provider approves the copy, never the list (D30) | `campaignsFor`, `campaignCard` |
| R12 | An upgrade never changes what a family receives — it changes where the provider appears | products |
| R14 | Every enquiry gets a drafted answer within a minute and a sent answer only after the provider's approval; reply time is measured from the enquiry, not from the draft | `enquiriesFor`, `approveEnquiry` |
| R15 | The machine never generates a person or a child; it edits the provider's real photos and generates places, objects, type and motion only | media department |
| R20 | Every generated asset carries a C2PA credential at creation and the platform's disclosure at publish; the credential is kept in the audit snapshot. An AI-drafted message a person did not edit carries the market's disclosure line where required and is logged either way (D30) | post card labels; enquiry sent line; outbox |
| R21 | A provider's real recording beats any generation; the clip engine is the v1 media service; generation fills gaps only | provider media, social queue |
| R22 | A propensity score per provider orders every sequence and the call list; recomputed nightly from the card and the events: +15 when a family saved or asked, −40 after "not my program", −20 after a bounce, 0 and excluded after unsubscribe (D30) | `score()`, `S.optOut` |
| R23 | The outbox refuses any send past the sending domain's warm-up cap; a bounce rate ≥ 2 % pauses the sequence and alerts; recipients are paced at the daily cap (D30) | `sendInvitation`, `S.sending` |
| R24 | The machine stores no child's name; a child is an age ("a child of 6") to every party, the family included — the platform's policy does not collect children's data (D30, D31; counsel prerequisite P-4) | `S.family.kids`, `enquiryCard` |
| R26 | **The policy gate**: a feature runs only when the instance's policy fields it needs are set — provider e-mail needs the postal address; the digest needs the published e-mail clause; audiences need the saves opt-in; SMS needs the consent text; generation needs the disclosure rule; a minor's data needs the audience model and a DPIA (D32) | `policyGate()`, `sending-guard`, the *Policy* screen |
| R27 | No profiling and no targeted advertising on a minor's data, on any instance, with or without consent (DSA Art. 28, California, Oregon, Nebraska as the floor) | policy `minors` |
| R28 | High-privacy defaults on every instance: nothing that shares, locates or increases frequency is on until the person turns it on; push respects quiet hours where minors may be present | policy `defaults`, `family.prefs` |
| R29 | The one-press run in Simple mode executes only recommendations the machine marks safe — approvals of drafts it wrote from real data, sends the policy gate allows, filing — never a reply to a person, never a purchase, never an override of a block; each action is logged as the operator's (D33) | `runSafe`, `recommend().auto` |
| R30 | A recording that shows a child is cut only when the provider confirms written parental consent for every child shown; the clip carries no child's name or identifying detail; the consent record is kept with the clip; without it the clip engine refuses and offers a coach-only or place-only cut (D35) | `S.media.consent`, `upload` |
| R31 | A provider's safeguarding status (background checks, training, welfare contact) is shown only as the platform verified it; "not verified" is a displayed state; marketing copy never claims safety (D35) | provider hero |
| R32 | No false urgency or scarcity in any draft; a person who writes "not now", "bereavement" or "can't afford" gets a pause on all marketing and a human reply; every purchase has a cooling-off (D35) | `rules/voice.md`, the gate |
| R33 | No audience, content slot or score is built or optimised on a protected characteristic or a proxy for one; neighbourhood delivery is audited for disparity; housing, employment and credit instances add their market's rules (D35) | policy `protected` |
| R34 | Every message, page and post meets WCAG 2.2 AA; captions on every clip; alt text on every image (D35) | policy `accessibility` |
| R35 | No health, location-track, biometric, Article 9 or financial-hardship data is stored about a person; when one arrives in a message it is answered, not recorded; no audience, slot or score uses one (D35) | policy `sensitive` |
| R37 | Retention runs on the advertiser's own numbers, never on a discount: a managing or paying advertiser at risk gets one drafted touch per signal, approved by the operator (renewal reminders may run under an earned auto-approval); kept and lost are logged and feed the churn rate; the retention lever is ranked against acquisition every week | Retention screen; `retentionFor`, `retentionDrafts`; economics `churnSaved` |
| R36 | A banned-pattern list is enforced on every draft and screen — no false urgency, no pre-ticked consent, no confirmshaming, no obstruction of Stop or unsubscribe, no hidden cost; an AI draft that scores or exploits a person's vulnerability is refused (D35) | `rules/voice.md`, policy `darkPatterns` |
| R25 | Approvals may be batched (one decision for a week's real-footage clips) and a department may earn auto-approval after four clean weeks (no edits, no complaints); every auto-sent message is logged and the family can stop it (D30) | `approveClips`, `S.auto` |
| R16 | The next-dollar ranking runs weekly on measured rates where they exist and on the documented assumption where they do not; the recap says which | `econ()`; `16-analytics…` §4 |
| R17 | A sequence step is added or removed when its marginal reply rate per touch falls below the cost-per-touch breakeven for two consecutive weeks, inside the 4–7 benchmark | production |
| R18 | Content slots go to the neighbourhood × activity pairs with the highest families-per-post over four weeks; a new pair gets one slot a week to be measured | production |
| R19 | The upgrade card appears when a provider's delivered value exceeds the cheapest product's annual price, or after 60 days managing with the honest delivered number (D30) | provider today |
| R13 | The machine never discounts; offers with a price cut are DiscountDirect's domain (D5) | — |

## 7. Metrics

| Metric | Definition | View |
|---|---|---|
| Providers managing | providers in `managing` or `upgraded` / all providers | platform overview (real: 0 / 253 today) |
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
| `04-decisions.md` | D1–D43 |
| `05-layout-specs.md`, `design-system.html`, `layouts.html` | gates 1 and 2 |
| `06-build-log.md`, `07-gate.md` | rounds and the measured pass |
| `08-client-asks.md` | the register of asks, with states |
| `19-implementation-prerequisites.md` | what the implementation needs after acceptance; nothing for the presentation |
| `09-business-logic.md` | the rules end to end: parties, flows, departments, campaigns, money, families, law, recap |
| `16-analytics-and-unit-economics.md` | CAC, LTV, avid value, content ROI, next dollar, metrics tree, events, attribution |
| `15-executive-summary.md` | one page: the classified media owner's situation, the product, how they use it, the benefits, the proof, the decision |
| `22-business-case.md` | the value for the media owner: what the product computes, the funnel and rates, the first customer's worked example, sensitivity, costs |
| `21-documentation-audit.md` | the deep audit by error class; the owner's answers; the transformation programme and its status |
| `23-claims-register.md` | every figure with its source opened and its status |
| `24-legal-and-data-processing.md` | the product as processor; the documents it must have; the counsel list |
| `01h-research-product-market.md` | the product's market, the site software, the tools bought for the pieces, the gap, the product SWOT |
| `18-responsible-data-policy-framework.md` | principles, the policy record, the gate, onboarding, the client's value, worked instances |
| `10-ssot.md` (this) | terms, enumerations, entities, rules, metrics |
| `11-architecture.md` | context, quality attributes, containers, flows, stack, ADRs |
| `12-technical-design.md` | data model, state machines, connectors, jobs, operations |
| `13-implementation-plan.md` | milestones, sprints with acceptance tests, issues with DoD, blocked register, risks |
| `01g-research-real-system.md` | every external service verified: auth, review, limits, prices, alternatives, cost |
| `20-system-blueprint.md` | drawings, repository layout, modules with pseudo code, contracts, crons, the outbox, security, the worker, tests, operations |
| `14-token-map.md` | prototype tokens and components → production |
