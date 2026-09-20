# business.direct — business logic and single source of truth

*For the delivery team. What this document holds: Part A — the product's rules end to end, in the order money and messages move: who
the parties are, what each department does, what leaves, who approves, what it costs, what
stops it; Part B — the single source of truth: the product layer, glossary, enumerations, entities,
settings, the rules register R1–R37, metrics. The product's terms are **media owner · advertiser ·
visitor · listing** (Part B §1a); the sections keep the first instance's words — platform ·
provider · family · card — as the worked example, because every rule was built and tested on its
data. The decisions behind each rule are in `decisions.md`; the prototype (`../index.html`)
implements every rule in memory. A rule changes here first, then in the code, then in the copy.*

## 1. The three parties and what each gets

| Party (product term · the first instance's word) | Gets | Gives |
|---|---|---|
| **Media owner** · **Platform** (Your Field NYC) | more families (B2C social), providers who manage their page and buy upgrades (B2B sales), a machine that runs while nobody logs in, one approval queue | the catalogue, the family accounts and preferences, the channels' authority, the operator's approvals |
| **Advertiser** · **Provider** (a listed business) | its own one-person team the day it manages its page: replies, reminders, campaigns to families who saved it, results; a free page and paid reach | a claim, its knowledge files, its approvals, and — if it upgrades — a monthly or seasonal fee |
| **Visitor** · **Family** | what starts near them this week, alerts from providers they saved, offers only from providers they chose, one cap, one Stop | preferences, and consent where the law requires it |

## 2. The two flows at the front door (D14) — marketing to visitors, sales to advertisers

**B2C social publishing → visitors (families).** Every provider with news (announcement, trial, next
session) becomes a post draft with the link back to its page. The operator approves,
edits or skips; approved posts publish at their calendar slot through the platform's
channels. Families arrive on the listing page; the platform's sign-up captures them.
*Nothing publishes unapproved.*

**B2B sales → advertisers (providers).** Every provider enters the pipeline at *identified*.
The invitation sequence (one approval for the whole run, recipients in propensity order — R22)
moves those with an e-mail to *contacted*; a reply moves to *replied* and lands in the inbox with a drafted answer;
"Apply to manage" (or a confirmed yes) → *applied*; the platform's confirmation →
*managing*; a paid product → *upgraded*. Phone-only providers get a call task; providers
with neither get the website form. "Not my program" or unsubscribe stops everything for
that address.

## 2b. Two interfaces, one machine (D33)

**Simple** is for the owner's operator: *Home* shows what needs a person as ranked
recommendations — each with the reason (the research figure behind it) and one button —
and a single press runs every recommendation the machine judges safe: approving drafted
posts and real-footage clips, sending the invitation when the policy gate allows, filing
the radar note. It never answers a person, never moves money, never overrides a block: those
stay "needs your judgement". **Advanced** is for a professional: every screen, every input,
every rule. Both carry a *What is this?* panel per screen, a *How to use* screen, and
*Templates* — sequences, posts, campaigns, knowledge files and policy records for other
client types — that copy into the machine with one press. The same rules apply in both;
Simple changes what is shown, not what may happen (R29).

## 2c. Retention — reduce churn (D41)

The third job of B2B sales. Every managing or paying advertiser is watched for the signals that
precede a cancellation: a renewal due, no session or trial update for 30 days, an enquiry
unanswered for two days, no saves in 30 days (the listing stopped surfacing). For each signal the
machine drafts one touch from the advertiser's own numbers — a renewal reminder that arrives with
results (families saved, enquiries, enrolments), a nudge that names the stale field and the
families searching that activity in that neighbourhood — never a discount (R13, R37). The
operator approves; renewal reminders are safe to run from Home and may earn auto-approval (R25);
at-risk touches need judgement. Kept and lost are logged; the churn rate on the Economics screen
is measured from that log, and the retention lever (at risk × share kept × LTV against a touch's
cost) is ranked against acquisition every week (R16). Keeping an advertiser costs a touch;
replacing one costs a CAC.

## 3. The departments (D6) and what each may do alone

| Department | Runs alone | Needs a person |
|---|---|---|
| Social publishing (platform) | draft, schedule slots, read comments and DMs, draft the reply with the link to the listing; real footage first, generation only to fill gaps (R21) | publish, send the reply — "someone tags you — first, not a queue" (D25) |
| Provider sales (platform) | draft the sequence and the reply, move stages on events, build the call list | send, override a stage |
| Retention (platform) | watch renewals, page freshness, enquiry response and saves; draft the touch from the advertiser's numbers; log kept and lost | send — renewal reminders may earn auto-approval; at-risk touches need judgement (R37) |
| Weekly picks (platform → families) | build the Sunday digest and saved-provider alerts within the cap | nothing — the family's preferences are the approval (R2, R3) |
| Generated pages (platform) | compute activity × neighbourhood pages with ≥ 3 providers | publish through the platform |
| Market radar (platform) | the weekly note from the catalogue | read and file |
| Conversations and reputation (provider) | draft an answer to every enquiry (platform message, e-mail, missed call) from the knowledge files; text back a missed call | send — the provider approves or edits each answer (phase 3, D25) |
| Reminders (provider) | 3-day and 1-day session reminders to booked families | nothing — the booking is the consent |
| Campaigns (provider) | draft trial, open-spots, announcement and registration campaigns from the card; size the audience | approve, edit, skip |
| Page and visibility (provider) | keep sessions, trial and photos on the card current | choose an upgrade |

Nothing leaves without a person's approval or an earned auto-approval (R1, R25). AI is optional per department (R10). With it off, every draft is the listing's own text or
a template with merge fields; with it on, the knowledge files are the prompt and the draft
carries the ✦ badge until a person edits it.

## 4. Advertiser campaigns to visitors (provider campaigns, phase 2, D22)

A campaign is a provider's message to families, built from the provider's own card (R11):

| Kind | Built when | Default audience | Default channels |
|---|---|---|---|
| Trial class | the card has a trial policy | families who saved the provider + nearby families with a child in the age range **who turned "new provider nearby" on** (Q3) | e-mail + push; SMS only to families who consented for this provider |
| Open spots | the card has a next session | families who saved the provider | push |
| Announcement | the card has an announcement | saved + nearby | e-mail |
| Registration | a session's registration is open | saved | e-mail + push |

The provider approves, edits or skips; the platform sends by each family's preferences
and never past the cap (R3). A family sees why she received it (she saved the provider),
on which channel, and that it counts toward her monthly four. Audience sizes are sample in
the prototype (prerequisite P-5 — the platform's saves data).

## 4b. Conversations — the advertiser's own team answers visitors (phase 3, D25)

An **enquiry** is a family's message to a provider on any channel the provider exposes:
the platform's message, e-mail, a missed call (the machine texts back). The machine drafts
the answer from the provider's `knowledge/faq.md` and `offer.md` (R8) and the card (next
session, trial policy, ages); the provider approves, edits or skips; the answer goes back on
the same channel and into the family's inbox thread. Reply time is measured from the
enquiry to the sent answer — the metric the provider sees first (R14). A family asks from her
saved providers; the machine never lets a provider message a family who has not written
first or saved it (R11). **An enquiry to a provider that has not claimed its page** does
not vanish: it becomes the sales sequence's strongest touch — "a family asked about you,
claim your page and answer her in one click" — the provider moves to *contacted*, and the
family is told the provider has been notified (Q4). The machine stores no child's name at all — the
platform's own policy says it does not collect children's data — so every party, the family
included, sees "a child of 6" (R24, D31). On the platform side, a **comment or DM** on a published post gets
a drafted reply that links to the listing; the operator approves it.

## 5. Placements and money — what the owner sells to advertisers (D21)

The base machine is **bundled by the platform** for every listing — the invitation, the
replies, the reminders, the campaigns — because its job is the platform's own growth. The
**provider buys reach**, and the products are the platform's own, from its "List your
program" copy:

| Product | What the provider gets | Price (sample — the platform publishes none) |
|---|---|---|
| Featured listing | top of the neighbourhood and activity lists; the spotlight post every month | $49 / month |
| Camp placement | the camps guide and the March "camps near you" digest | $149 / season |
| Local discovery profile | photos, coach bio, reviews, booking on the card | $29 / month |

Choosing one moves the provider to *upgraded*; it changes where the provider appears, never
what a family receives (R12); the platform's intelligence screen sums the sample revenue. Billing is Stripe Checkout on the platform's account (ADR-9); the platform invoices, business.direct
records the entitlement. No discounting logic — that is DiscountDirect's domain (D5, R13).

## 6. Visitors (families): preferences, consent, cap, stop

- **Preferences** per channel: weekly picks (e-mail), saved-provider alerts (push), new
  provider nearby (push), texts from providers (SMS). Default: every channel off until the
  family turns it on (R28); the demo family has picks and alerts on.
- **Consent**: SMS only with written consent per provider, stored verbatim with its time
  and source (TCPA). E-mail and push run on preference.
- **Cap**: 4 **provider-originated** messages a month per family — campaigns and texts,
  across all providers. The platform's own digest and alerts run on the family's switches
  and do not count (D30; the audit found the earlier wording was consumed by the digest
  alone). Checked when a message is queued and again when it is sent.
- **Stop**: one tap turns every channel off and cancels what is queued, in one transaction.
- **Why you got this** on every message: the provider she saved, the channel, the count.

## 6b. Responsible data — for every customer (D32)

The machine carries one **policy record per instance** and a **gate** that reads it before
every send and every draft (`responsible-data.md`). Seventeen principles hold
whatever the customer: know who the service is for; a child is an age, never a name (R24); no
profiling or targeted advertising on a minor's data, not even with consent (R27);
high-privacy defaults that the person turns on (R28); consent that names channel and sender,
stored verbatim (R4); zero-party over inferred (R11); who sent it, why, how to stop, and the
postal address (R2, R23); disclosure when a machine wrote or made it (R20); retention with an
end date; and the gate is code (R26) — provider e-mail needs the postal address, the digest
needs the site's privacy policy to describe e-mail alerts, audiences need the saves opt-in, SMS
needs the consent text, generation needs the disclosure rule, a minor's data needs the
audience model and a DPIA. The client's value is lower exposure, a better-converting
audience, trust as the acquisition channel, and auditability: every send carries its policy
basis. For Your Field NYC (ClassScout) the gate today blocks provider e-mail (no postal
address, prerequisite P-1) and the digest (the policy does not yet describe e-mail alerts, prerequisite P-2).

## 6c. Beyond children (D35)

Seven more cases hold for every client (research V). **Children in real footage**: the
clip engine cuts a recording that shows a child only when the provider confirms written
parental consent for every child shown, and never puts a child's name on a clip (R30). **The
adults who work with children**: safeguarding is shown only as the platform verified it —
"not verified" is a displayed state, never a claim (R31). **People in vulnerable
circumstances**: no false urgency; "not now", "bereavement" or "can't afford" pauses all
marketing and gets a human; every purchase has a cooling-off (R32). **Protected
characteristics**: never an audience, a slot or a score, nor a proxy; delivery by
neighbourhood is audited (R33). **Accessibility**: WCAG 2.2 AA on every message, captions on
every clip (R34). **Sensitive categories** — health, location tracks, biometrics, Article 9,
hardship — are answered, never stored (R35). **Dark patterns and AI manipulation**: a banned
list on every draft and screen; Stop is one tap (R36).

## 7. Advertisers (providers): the law on the sales side

US (first market): commercial e-mail to a business needs no prior consent (CAN-SPAM);
every message carries the platform's **registered postal address** (a merge field, checked
by the gate — Q2; prerequisite P-1 for the address itself) and a working opt-out honoured within 10
business days — the machine honours it within one. A "not my program" or an unsubscribe
excludes the address from every sequence; a bounce lowers its score (Q6). The sending
domain is paced and guarded: warm-up, a daily cap, and a bounce rate above 2 % pauses the
sequence (R23). Hungary (reference): corporate addresses without
consent; a named person's address needs consent — the reference connector flags which is
which. SMS to providers is not used.

## 8. The owner's Monday recap (D23)

Every Monday the operator reads one screen: providers contacted, replies answered, applied
· managing · upgraded, posts published, families reached by campaigns, upgrade revenue; by
department; the market radar from the catalogue (largest activity, free trials, unknown
prices, page opportunities, unreachable providers); and "needs you" — approvals waiting,
providers who replied but did not apply, integrations still to connect. Real where the
catalogue is the source; sample until the platform's analytics and a pilot provider's
numbers arrive (prerequisites P-6 and P-9).

## 8b. Data-driven decisions (D26)

The recap is read; the economics are acted on. The system keeps CAC and LTV per provider
cohort, the marketing value of an avid family, the cost per family from content, and ranks
the next dollar weekly (touch · call · content) by expected LTV gained — on measured rates
where they exist and on documented assumptions where they do not, saying which (R16). The
sequence cadence, the content slots and the upgrade pitch follow the numbers (R17–R19).
The model and its events are `economics.md`.

## 8e. The rules, mapped (every SSOT rule → where this document states it)

| Rule | Where | Rule | Where |
|---|---|---|---|
| R1 human gate on everything | §3, §9 | R16 next-dollar ranking on measured or declared rates | §8b |
| R2 who, why, how to stop | §6, §7 | R17 sequence cadence follows the data | §8b |
| R3 the cap: 4 provider messages a month | §6 | R18 content slots follow families-per-post | §8b |
| R4 consent per channel, per provider for SMS | §6 | R19 the upgrade pitch at delivered value, 60-day floor | §5 |
| R5 provider e-mail without consent, opt-out honoured, "not my program" stops | §7 | R20 credentials and disclosure on generated and AI-drafted content | §6b, §9 |
| R6 generated pages only with ≥ 3 providers | §3 | R21 real footage beats generation | §3 |
| R7 every non-catalogue figure labelled sample | §1 (the machine says what is real), §8 | R22 propensity score orders sequences and the call list | §2 |
| R8 knowledge files read before every draft | §3 | R23 the sending guard | §7 |
| R9 stages move on events; a person may move any, logged | §2 | R24 a child is an age, never a name | §4b, §6b |
| R10 AI optional per department | §3 | R25 batch and earned auto-approval | §3 |
| R11 campaigns reach saved and opted-in nearby families only | §4, §4b | R26 the policy gate | §6b |
| R12 an upgrade changes where the provider appears, never what a family receives | §5 | R27 no profiling or targeting of minors | §6b |
| R13 the machine never discounts | §5 | R28 high-privacy defaults | §6, §6b |
| R14 a drafted answer within a minute; reply time from the enquiry | §4b | R29 the one press runs only safe recommendations | §2b |
| R15 never generate a person or a child | §9 | R30 children in footage with written parental consent | §6c |
| R31 safeguarding shown as verified only | §6c | R32 no pressure; "not now" pauses | §6c |
| R33 no protected characteristic or proxy | §6c | R34 accessible by default | §6c |
| R35 sensitive categories answered, never stored | §6c | R36 no dark pattern, no AI manipulation | §6c |
| R37 retention on the advertiser's own numbers, never a discount; kept and lost logged | §2c | | |

## 9. What the machine never does

Sends without an approval or a preference; discounts to keep an advertiser (R37); answers a family without the provider's approval; texts without consent; sends past the domain's warm-up cap or bounce limit (R23); sends a provider e-mail without the postal address; shows a child's name to anyone (R24); profiles or targets a minor (R27); cuts a clip that shows a child without written parental consent (R30); claims safety it has not verified (R31); pressures anyone (R32, R36); builds an audience on a protected characteristic (R33); stores a sensitive category (R35); runs a feature its policy record does not allow (R26); publishes generated media unlabelled; generates a person or a child; exceeds the cap; deletes
a provider's stage history; discounts; publishes a generated page with fewer than three
providers; speaks as an AI to a family or a provider — the product speaks as the platform
or the provider.

## Part B — the single source of truth: the product layer, glossary, enumerations, entities, settings, the rules register, metrics

*Written 2026-09-19 after gate 2 and the first build round (D16–D18); the product layer
added 2026-09-20 (D41). Every term the other documents use is defined here; where a term is
DiscountDirect's, it says so (D5). **The product's terms** are media owner · advertiser ·
visitor · listing · instance; **the first instance's words** for them are platform · provider ·
family · card · Your Field NYC, and because the prototype and the engineering documents were
written on the first instance's data they use the instance's words in identifiers and
examples — the mapping in §1a is the rule. The prototype (`../index.html`, `assets/app.js`)
is the reference implementation of the enumerations and state machines below.*

### 1a. The product layer (D41)

| Product term | Meaning | The first instance's word (Your Field NYC) | In code |
|---|---|---|---|
| **Media owner** | the classified media owner who buys and runs business.direct; the operator is the person at the owner who approves | platform | `role = platform`, `platform_id` |
| **Listing** | a business's page on the site, built by the site from public data; the unit of inventory the owner sells | card | `providers_cache` |
| **Advertiser** | a listed business — a prospect until it manages its page, a customer once it pays for a placement | provider | `provider_id`, `provider_state` |
| **Visitor** | a person using the site; an engaged visitor saves, opens the digest and enquires | family | `family_id`, `families_prefs` |
| **Instance** | one site with its own policy record, connector, sending domain and products | Your Field NYC | `instances`, `policies` |
| **The three jobs** | marketing (content → media → visitors), B2B sales (contact → acquire), retention (reduce churn) | the two flows (D14) + retention (D41) | departments `social`, `picks`, `pages`, `radar` · `sales` · `retention` |
| **Placement / advertising product** | what the owner sells to an advertiser — featured, category, discovery profile | reach product | `products`, `entitlements` |


### 1. Glossary

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

### 2. Enumerations

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
| `claimStatus` (platform's) | `unclaimed` · unset (most of the demo sample); the platform's own enumeration has more values we have not seen | `providers.json` |
| `activityType` | 20 values as the platform's `browse-facets` lists them (Martial Arts, Dance, Swimming, Soccer, …) | `platform.json` |
| `borough` | `Manhattan` · `Brooklyn` (today) | facets |

### 3. Canonical entities

| Entity | Fields (prototype) | Notes |
|---|---|---|
| **Provider** | `id`, `name`, `category`, `borough`, `neighborhood`, `address`, `lat`, `lng`, `activityTypes[]`, `primaryActivityType`, `ageRanges[]`, `ageMinMonths`, `ageMaxMonths`, `shortDescription`, `longDescription`, `price{amount,currency,unit,evidence}`, `website`, `phone`, `email`, `image`, `dayTimeTags[]`, `venueModel`, `sessions[{id,title,registration}]`, `nextOccurrence`, `announcement{title,description,badge}`, `bookingEnabled`, `trial{available,free,text}`, `rating`, `reviewCount`, `badges[]`, `claimStatus`, `verifiedFields[]`, `updatedAt`, `publishedAt`, `sourceCount` | the platform owns it; business.direct reads it (`fetch-yourfield.py`). One listing in the demo sample has no neighbourhood; the borough stands in |
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

### 4. Settings the prototype fixes

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

### 5. Decision register

`decisions.md` holds D1–D47; every rule below names the decision behind it.

### 6. Rules register

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

### 7. Metrics

| Metric | Definition | View |
|---|---|---|
| Providers managing | providers in `managing` or `upgraded` / all providers | platform overview (the demo sample: none managing at the pull) |
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
