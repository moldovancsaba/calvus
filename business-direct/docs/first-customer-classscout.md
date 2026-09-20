# business.direct — first customer: ClassScout · Your Field NYC

*Everything specific to the first customer's instance in one place: their site measured, what in
the prototype is real and what is sample, the onboarding inputs by the feature each unblocks, the
pilot's SWOT and the closed register of asks. ClassScout is the example that makes the persona
concrete and the first buyer; the product is defined in `product-definition.md`. **The counts in
Part A and Part B describe the demo sample pulled from the site's public API on 2026-09-19 — the
prototype's data — and say nothing about the size or state of the customer's business, whose
catalogue is far larger; they appear in no stakeholder document (D45).** Assembled 2026-09-20 (D44).*

## Part A — the site measured (audit of the starting point)

*Measured 2026-09-19 with `curl` and the two converters (catalogue re-pulled the same evening: 253 providers, 51 records updated); the videos read frame by frame.
Your Field NYC is the first customer's instance; the Hungarian instance is the reference connector's data.*

### 1. The client platform: Your Field NYC (getyourfield.com)

| Measure | Value |
|---|---|
| Stack | Next.js + Mantine on Vercel (`data-dpl-id`), English; v0.201.105 |
| Home (`/nyc`) | 118 KB HTML, 24 scripts, 3 stylesheets; TTFB 0,53 s |
| Structure (sitemap, 280 URLs) | `/nyc/` home · `all` · `classes` · `camps` · `drop-in-activities` · `family-events` · `map` · 22 `neighborhood-guides/*` · **251 `providers/*`** |
| Public API (found in the site's own JS bundles; no reference page) | `browse-facets`, `site`, `providers`, `providers/{id}` (252 cards on the first pull, 253 on the re-pull the same evening), `browse?…`, `family-events`, `home-feed`, `meetup-groups`, `nearby-services?listingId=`, `claim-requests?city=`, `demand-capture`, `scout/recommend` (POST), `map-pins` (empty today) |
| Providers | **253**: Manhattan 108, Brooklyn 145; categories Classes 189 · Camps 44 · Drop-In Activities 20; 20 activity types in the facets (Martial Arts 76, Dance 39, Swimming 36, Soccer 33 …); 83 neighbourhood values on the cards, 21 neighbourhoods in the platform's guides |
| Provider record | name, category, borough, neighbourhood, address, geo, activity types, age ranges, short and long description, price with evidence and source, website, phone, e-mail, image, day/time tags, venue model, sessions with registration status, next occurrence (weekday, time, text), announcement, booking flag, trial policy, rating/reviews (all 0), badges, **field-level verification records** (field, method, source URL, verified by "enrichment"), updated/published dates, source count |
| Claim state | `unclaimed` on 15, unset on 237 — **none claimed** |
| Consumer features | sign-up, saved items, family plan with cost estimate, family preferences, neighbourhood detection, notifications endpoint |
| Site copy | hero "Find sports your child will *love*, close to home"; "How Your Field NY works" (choose your neighbourhood → compare local options → save and plan); trust pillars; newsletter "Get the latest kids activity picks for your neighborhood"; **"List your program — reach more NYC families with a featured listing, camp placement, or local discovery profile"** |

#### 1b. The platform's policy and terms (read 2026-09-19, both "last updated 2026-09-12")

| Clause | What it says | Consequence for business.direct |
|---|---|---|
| Audience | "intended for adults (18+)"; "we do not knowingly collect personal information from children"; telemetry contains "no child data" | no child's name anywhere in the machine; ages only (R24, D31) |
| E-mail | "we do not yet offer email alerts; if we add them, the preferences you set will be described here"; a "notify me" e-mail is opt-in only | the digest and alerts require a policy revision before launch (prerequisite P-2) |
| Account activity | views, saves and contacts are recorded for suggestions "only after you explicitly opt in", off by default | campaign audiences and the avid-family definition come only from opted-in accounts (prerequisite P-5) |
| Claims | "claim and update requests" are a platform feature (§e-1) | apply-to-manage rides on it |
| Sign-in | doneisbetter provides name and e-mail; no passwords | ADR-5 confirmed |
| Contact | info@classscout.ai; no postal address on the site | prerequisite P-1 — CAN-SPAM needs one |
| Provenance | listings "aggregated from public directories, civic sources, activity providers, and the Google Places API" | the card's `verifiedFields` and `sourceCount` are the provenance we cite |

### 2. The catalogue as pulled (`data/providers.json`, 253 rows — re-pulled 2026-09-19 evening: one provider added, Kids In Sports NYC; 26 records gained coordinates, 18 new descriptions, 3 new verified fields)

| Field | Coverage |
|---|---|
| Website | 253 — the activation channel exists for every provider |
| Phone / e-mail | 181 / 130 (73 phone only, 50 neither) |
| Coordinates | 246 |
| Age ranges | 183 (buckets 3–5, 6–8, 9–12, Teens) |
| Price with amount | 28 (evidence "stated" with source URL) — most prices are unknown to the platform |
| Sessions | 74; next occurrence 83 (weekday, start time, free text) |
| Trial policy | 72 (34 explicitly free) |
| Announcement | 26; booking enabled 10 |
| Verified fields | every record but one (Goldfish Swim School Gowanus); typically description, venue model, price, trial policy — read from the provider's official page |
| Claim | 15 `unclaimed`, 238 unset |

Facets and site copy are in `data/platform.json`. The converter is read-only; re-run to
refresh.

### 3. The reference instance: Most én sportolok! (sport.doneisbetter.com)

Same stack, Hungarian. 431 listings with coordinates, 8 categories, 20 counties, a
documented public API (`/api-reference`: facets, pins, site, nearby, intent search,
`POST /api/ingest`), `LocalBusiness` JSON-LD on every listing, a claim prompt on every
card (none claimed), a crawler-verified date on each. Pulled to
`data/reference-sportolok/` by `fetch-sportolok.py` (431 rows: 395 websites, 385
descriptions, 21 sessions in the next 7 days). Home 559 KB, TTFB 4,8 s cold. It proves
the machine generalises: two instances, one pattern, two converters of the same shape.

### 4. The reference videos (owner-supplied)

Two ~100 s vertical videos by the same creator (@structurewebworks / @restructural),
21 frames each read at 5 s intervals:

| | Video 1 — "62 AI agents run an entire social media team" | Video 2 — "The one-person sales & marketing team" |
|---|---|---|
| Structure | 03 Orchestrator → eight departments; 04 Knowledge layer + access ("Brand OS file system": `/brand-brain/voice-guide.md`, `positioning.md`, `messaging-pillars.md`, `/signals-seo`, `/content`, `/creative`, `/social`, `/reputation`, `/conversation`, `/reporting`); access control plane | research & intelligence (Google Trends, Semrush, SparkToro) → content engine (Claude + Surfer; `brief.md`, `offer.md`, `values.md`) → distribution (Metricool → IG/FB/TikTok/YouTube) → creative studio → lead capture & routing (ManyChat DMs, CallRail) → sales & booking (HubSpot, Twilio SMS, Calendly, payments) → results (Looker "Today's recap") → knowledge updated (`leads.md`, `customers.md`, `targets.md`) → back to research |
| Operating rule (captions) | "it reads what … brief draft … and it can't post … it doesn't go out"; "a rival launches, it reads it — that's a strategist"; "someone tags you — not a queue, first"; "it stops and asks"; "the owner still owns"; "everything else runs" | "first"; "nobody logs in"; "anyone"; "the information" |
| Example business | a skincare/social brand | "Structure Motors" — a test-drive request for a 911 GT3 RS handled from DM to calendar |

What business.direct takes from them: departments as the unit; the knowledge layer as
files the owner can read; approval before anything leaves; the recap; integrations as
the machine's hands. What it does not take: 62 agents and twenty subscriptions — the
provider is one coach with a phone.

### 5. What DiscountDirect already gives this project

SSOT terms (offer, channel, consent, frequency cap, holdout, predefined rule set /
advanced mode), the GDS token names, the decided stack (D26: Next.js 15, MongoDB Atlas,
Vercel, DoneIsBetter SSO, Resend, Vercel Cron + outbox, Socket.IO, Upstash, Blob — the
same family Your Field runs on), and the research on price and the nine buying levers.


## Part B — sources and assets: what is real, what is sample

*Every figure used in the product-facing documents has a row in `evidence.md` with its
source opened and its status (P · A · corrected · assumption · owner); the research rounds
(`01-research.md` … `01g-research-real-system.md`, `market.md`) hold the full evidence behind each.*

| Content | Source | Real or sample |
|---|---|---|
| 253 providers with every field listed in `first-customer-classscout.md` §2 | `data/fetch-yourfield.py` → `data/providers.json`, from getyourfield.com's public API, 2026-09-19 (re-pulled the same evening) | **real** — public data only; re-run to refresh |
| Boroughs, neighbourhoods, activity counts, site copy | same → `data/platform.json` | real |
| Claim state | the API's `claimStatus` (15 `unclaimed`; the rest unset) | real |
| The Hungarian reference instance (431 listings) | `data/fetch-sportolok.py` → `data/reference-sportolok/` | real, reference only |
| The provider persona's brand voice, knowledge files, results tiles, integration states | written for the prototype around **Brooklyn Force Soccer** (a real, explicitly unclaimed provider) | **sample**, declared on the page |
| Social post drafts, the invitation, the three provider replies, campaign drafts, family enquiries, comments on posts | generated in `assets/app.js` from real providers' cards (name, neighbourhood, trial policy, next session, announcement, ages, the coach's first name from the card's e-mail) and the knowledge files; the families who write (Priya, Jonah, Dana) and the audience counts are invented | **sample** (D18), labelled on every card |
| The platform's three reach products | names from the platform's own "List your program" copy (`platform.json`); prices invented | names real, prices sample (D21) |
| The family persona (a Park Slope parent, two children, saved items, channel preferences) | written for the prototype; the saved providers are real | sample |
| Research figures | `01-research.md`, each with its link; primary vs aggregator marked | real, cited |
| The target shape | two owner-supplied videos (`first-customer-classscout.md` §4), 42 frames extracted with a Swift/AVFoundation script — the videos themselves are not in the repo | owner input |
| Terms, tokens, stack | DiscountDirect's SSOT, GDS token map, ARCHITECTURE (D26) | inherited (D5) |

No provider, family or platform account is contacted or written to by the prototype.


## Part C — onboarding inputs: what the instance provides, and when

*The onboarding inputs of the first customer's instance (Your Field NYC), grouped by the
feature each unblocks. Nothing here is needed to present or to plan the product: every item is
defaulted or sampled in the prototype and declared on the screen, and the policy gate blocks
the feature until the field is set. Every later customer has the same list with its own values
— it is the product's onboarding checklist (`responsible-data.md` §4)
filled for one site. Written 2026-09-19; reframed 2026-09-20 (D41). The closed register of asks
(`register-of-asks.md`) is history.*

### 1. Before the first real message from this instance (legal and policy)

| # | Prerequisite | Who provides | Why | Unblocks |
|---|---|---|---|---|
| P-1 (ask #15) | The site's registered **postal address** for every advertiser e-mail | ClassScout | CAN-SPAM requires a physical address; the site publishes only info@classscout.ai | the policy gate's "provider e-mail" row; the sequences |
| P-2 (ask #16) | The platform's **privacy policy revised** to describe the digest and alerts ("we do not yet offer email alerts; if we add them, the preferences you set will be described here") | ClassScout (we draft the paragraph on request) | the family digest and alerts must be described before they run | the gate's "digest and alerts" row |
| P-3 (ask #18) | The **policy record** for Your Field NYC confirmed: audience model (adults, per the policy), retention periods, AI-disclosure choice, quiet hours | ClassScout | the gate reads the record before every send | the whole gate |
| P-4 (ask #13) | Counsel's view on **children's data**: which of New York's Child Data Protection Act and COPPA applies to a parent's account describing a child, and the consent texts | ClassScout's counsel | the machine already stores no child's name; this confirms wording | enquiry and campaign texts |

### 2. Before the keyed features (data and writes from the site)

| # | Prerequisite | Who provides | Why | Unblocks |
|---|---|---|---|---|
| P-5 (ask #17) | The **opted-in share**: how many accounts turned on activity recording (saves recorded "only after you explicitly opt in, off by default") | ClassScout | campaign audiences and the avid-family definition are only opted-in accounts | real audience counts on campaign cards |
| P-6 (asks #7, #10) | **Analytics events and counts**: families, sign-ups with source, saves, digest opens, bookings; the real prices of the three products | ClassScout | every assumption in the economics model becomes a measurement | the economics tiles; capture; cohorts |
| P-7 (ask #6) | A **key and the write contract** for claim requests, notifications, card flags, saves for audiences — or the decision that the machine stays read-only | ClassScout | apply-to-manage, upgrades' card flags, alerts | Release 1b |
| P-8 (ask #12) | Whether **review capture and price capture** are planned on the cards (0 reviews, 28 prices on 253 today) | ClassScout product | the AI-citation lever and the content engine depend on card quality | generated pages' readiness; anchors |
| P-9 (ask #8) | A **pilot provider** willing to share replies, trials booked, no-shows | ClassScout + one provider | the provider view's tiles are sample until then | provider results; "your return" |

### 3. Instance settings the prototype assumes (a "yes" at onboarding closes each)

| # | Assumption in the prototype | Where it shows |
|---|---|---|
| P-10 (asks #2, #3) | Demo personas: Brooklyn Force Soccer; a Park Slope parent with a child of 5 and a child of 9 | provider and family views |
| P-11 (ask #4) | v1 integrations = the platform API, e-mail, Instagram + Facebook, push; later = TikTok, X, SMS, Google Business Profile, calendars | integrations screen |
| P-12 (ask #5) | The site's advertising products and prices (featured listing, camp placement, discovery profile — sample prices today) and whether a conversations service line is priced (0 = included) | economics inputs; provider today |

### 4. What the presentation needs today

Nothing. The prototype, the presentation and the plan stand on defaults and samples that are
declared on every screen; the gate shows what each missing field blocks.


## Part D — the pilot's SWOT

*Note (D41): this SWOT was written when the documentation treated the first instance as the
project; it reads as the pilot's SWOT — the first customer's market, competitors (Sawyer) and
catalogue. The product's own market, competitors and SWOT are research VII (`market.md`).*

#### Strengths (internal, evidenced)

| # | Strength | Evidence |
|---|---|---|
| S1 | **The thesis is the incumbents' thesis.** Yelp bought exactly this (Hatch, $270 M, lead management + scoring; Receptionist at $99/month) three months before we drew it; Thumbtack sells its supply inside ChatGPT and Claude. | research III §1 |
| S2 | **Human gate on everything, from day one.** Every outbound path passes a person (R1); the outbox is the only sender (ADR-4); consent and caps are checked twice (ADR-3). This is the operating rule the reference videos and the Sprout consumer data both demand, and it is the hardest thing to retrofit. | business logic §3, §9 |
| S3 | **Real data, declared honestly.** 253 real providers, every tile labelled real / sample / benchmark / assumption, the economics screen exposing a 0.7 LTV : CAC rather than hiding it. Owners and clients can trust the numbers because the bad ones are shown. | analytics §2.4, §8 |
| S4 | **Single-player utility for the provider on day one** — conversations, reminders, campaigns, media work before the platform has sent a single family — which the cold-start literature says is the difference between marketplaces that seed supply and those that die on it. | research II §2.2; provider view |
| S5 | **One connector interface, two instances already pulled** (Your Field 253, Sportolok 431). Portability is built, not promised. | ADR-2; `data/` |
| S6 | **The owner owns the platform.** No integration negotiation, no API risk from a third party, family data never leaves the owner's estate. | brief; ADR-11 |
| S7 | **Documentation as a product**: SSOT, business logic, 28 decisions, 22 rules, three research rounds with primary sources, a gate that fails on stale text. A team can be onboarded from the folder. | this docs set |

#### Weaknesses (internal, evidenced)

| # | Weakness | Evidence |
|---|---|---|
| W1 | **Unit economics do not close at today's scale.** Outbound to 253 providers on $49 upgrades: LTV : CAC 0.7, payback 31 months. The service is a cost centre for the platform until the catalogue is ~4× larger or ARPA is higher. | analytics §2.4 |
| W2 | **Two rules cannot both hold** (A2) and one legal footer is wrong (A3). Small to fix; unacceptable to ship. | §2 |
| W3 | **The operator is the bottleneck by design.** R1 puts one person in front of every post, reply, campaign and enquiry; the economics model undercounts that cost (A10). | A10 |
| W4 | **Sample where it matters most**: audiences, trials, reply times, families per post, product prices. The screens are convincing and the numbers behind the two revenue levers (campaign reach, upgrade pitch) are invented until the platform's analytics arrive. | analytics §8; A7, A11 |
| W5 | **Thin cards**: 0 reviews, 28 prices, 83 next sessions of 253. The content engine and the AI-citation lever depend on card quality the machine does not control. | A15 |
| W6 | **Six dependencies on keyed platform endpoints** for the core loop (claims, audiences, notifications, flags, sources, bookings). | A16 |
| W7 | **No media production yet** — the clip engine is v1 in the plan, sample in the prototype; the strongest content lever (real footage) is unbuilt. | round 6 |

#### Opportunities (external, evidenced)

| # | Opportunity | Evidence |
|---|---|---|
| O1 | **AI answers and social search are replacing Google organic for local discovery** — the platform that is the cited, structured source wins; Yelp took 512,680 citations in a quarter. A curated, verified kids-activities catalogue is exactly the kind of source these engines cite. | research II §2.1 |
| O2 | **Youth-activity spend is up 46 % in five years** ($1,016 per child per sport) and parents choose the programme that shows up in their world (80 % pick the sponsoring brand). Providers can pay because the families do. | research I §3, II §2.1 |
| O3 | **SMBs already use AI for content (81 %) and want referrals (83 %)** — the provider is ready to accept drafts and a referral loop, which is what the machine sells. | research II §3 |
| O4 | **Yelp Receptionist proves a $99/month price point** for "never miss a call" in services; the provider-side conversations department can be a product line, not only a bundled feature. | research III §1 |
| O5 | **Owned audiences are cheap to build** (newsletter growth ~90 % unpaid; ~$1.50 per opt-in via cross-recommendation); the neighbourhood newsletter (P6) is a moat no channel algorithm can take. | research II §2.1 |
| O6 | **Open-source measurement** (Meridian, Robyn) and cheap generation APIs (cents per image) mean the analytics and media layers cost tooling, not licences. | research II §4, III §3 |
| O7 | **The second instance is a configuration** — every reference-idea platform (sport.doneisbetter.com, job portals, classifieds) is the same shape; the connector interface is the product. | ADR-2 |

#### Threats (external, evidenced)

| # | Threat | Evidence |
|---|---|---|
| T1 | **The incumbents move first and bigger.** Yelp ($270 M for Hatch), Angi, Thumbtack inside the assistants; **Sawyer** already sells booking, registration and a marketplace to kids'-activity providers — the exact provider the machine courts. A provider with Sawyer's booking tool needs a reason to answer our invitation. | research III §1; **P** [Sawyer for Business](https://www.hisawyer.com/for-business), [Sawyer marketplace](https://www.hisawyer.com/for-business/features/marketplace) |
| T2 | **Deliverability.** 47 % of AI-outbound deployments fail on domain reputation within 90 days; one bad week of sends and the platform's own transactional mail is at risk. | research II §5.1 |
| T3 | **Law is moving under the service**: TCPA damages $500–1,500 per text; EU AI Act Art. 50 live since August 2026 with four different platform label systems; children's-data statutes in New York; CAN-SPAM's address rule (A3). | research I §8, II §4.3; A13 |
| T4 | **Platform rules on AI content** — TikTok cuts reach ~60 % for 30 days after three unlabelled AI videos; Meta labels above the post. A labelling slip costs the channel, not just a post. | research II §4.3 |
| T5 | **Google's enforcement on generated pages** (50–80 % traffic loss for thin programmatic sites) — the generated-pages lever is one algorithm update from a penalty if readiness is not real. | research II §2.1 |
| T6 | **Vendor churn in generation**: generative-video vendors change quickly (K/V16: the earlier "Sora died in five months" had no source and was removed); Higgsfield's pricing could not even be read from its own page. Anything built on one vendor's API is fragile. | research II §4.1 |
| T7 | **The provider is one coach with a phone.** Adoption depends on a claim that costs one click and a tool that works alone; any onboarding friction and the supply side — where two-thirds of marketplaces die — stays unclaimed. | research II §2.2 |

#### The cross-reads (what the SWOT says to do)

- **S1 + T1 → position as the platform's own team, not a tool.** Sawyer sells software to the provider; we sell families to the provider and providers to the platform. Never compete on booking software; integrate with it (a Sawyer connector is a later adapter).
- **W1 + O2 + O4 → fix the model, not the pitch.** Price the conversations department for providers at the incumbent's line ($99) *or* keep it bundled and fund the machine as platform growth — decide, and put the decision in the economics defaults.
- **W3 + O3 → batch approvals and trust levels.** A provider who edited nothing for four weeks can have reminders and answers to FAQ questions auto-sent (still logged, still stoppable); R1 becomes "approval or an earned auto-approval per department".
- **W5 + O1 + T5 → card quality is the product.** Reviews and price capture on the platform are the precondition for the citation lever; without them, do not publish generated pages.
- **T2 + A9 → the sending guard is a rule, not a card** (R23).
- **T3 + A2 + A3 + A13 → a legal pass before the first send**: address, cap semantics, children's data, per-market disclosure.



## Part E — the closed register of asks

The items that once needed the owner or the first customer, with where each went, are history:
`register-of-asks.md`.
