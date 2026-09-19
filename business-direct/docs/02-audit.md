# business.direct — audit of the starting point

*Measured 2026-09-19 with `curl` and the two converters (catalogue re-pulled the same evening: 253 providers, 51 records updated); the videos read frame by frame.
Your Field NYC is the client (D11); the Hungarian instance is the reference.*

## 1. The client platform: Your Field NYC (getyourfield.com)

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

### 1b. The platform's policy and terms (read 2026-09-19, both "last updated 2026-09-12")

| Clause | What it says | Consequence for business.direct |
|---|---|---|
| Audience | "intended for adults (18+)"; "we do not knowingly collect personal information from children"; telemetry contains "no child data" | no child's name anywhere in the machine; ages only (R24, D31) |
| E-mail | "we do not yet offer email alerts; if we add them, the preferences you set will be described here"; a "notify me" e-mail is opt-in only | the digest and alerts require a policy revision before launch (prerequisite P-2) |
| Account activity | views, saves and contacts are recorded for suggestions "only after you explicitly opt in", off by default | campaign audiences and the avid-family definition come only from opted-in accounts (prerequisite P-5) |
| Claims | "claim and update requests" are a platform feature (§e-1) | apply-to-manage rides on it |
| Sign-in | doneisbetter provides name and e-mail; no passwords | ADR-5 confirmed |
| Contact | info@classscout.ai; no postal address on the site | prerequisite P-1 — CAN-SPAM needs one |
| Provenance | listings "aggregated from public directories, civic sources, activity providers, and the Google Places API" | the card's `verifiedFields` and `sourceCount` are the provenance we cite |

## 2. The catalogue as pulled (`data/providers.json`, 253 rows — re-pulled 2026-09-19 evening: one provider added, Kids In Sports NYC; 26 records gained coordinates, 18 new descriptions, 3 new verified fields)

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

## 3. The reference instance: Most én sportolok! (sport.doneisbetter.com)

Same stack, Hungarian. 431 listings with coordinates, 8 categories, 20 counties, a
documented public API (`/api-reference`: facets, pins, site, nearby, intent search,
`POST /api/ingest`), `LocalBusiness` JSON-LD on every listing, a claim prompt on every
card (none claimed), a crawler-verified date on each. Pulled to
`data/reference-sportolok/` by `fetch-sportolok.py` (431 rows: 395 websites, 385
descriptions, 21 sessions in the next 7 days). Home 559 KB, TTFB 4,8 s cold. It proves
the machine generalises: two instances, one pattern, two converters of the same shape.

## 4. The reference videos (owner-supplied)

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

## 5. What DiscountDirect already gives this project

SSOT terms (offer, channel, consent, frequency cap, holdout, predefined rule set /
advanced mode), the GDS token names, the decided stack (D26: Next.js 15, MongoDB Atlas,
Vercel, DoneIsBetter SSO, Resend, Vercel Cron + outbox, Socket.IO, Upstash, Blob — the
same family Your Field runs on), and the research on price and the nine buying levers.
