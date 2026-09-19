# business.direct — audit of the starting point

*Measured 2026-09-19 with `curl` and the converter; the videos read frame by frame.*

## 1. The reference platforms

| Measure | Most én sportolok! (sport.doneisbetter.com) | Your Field NYC (getyourfield.com/nyc) |
|---|---|---|
| Stack | Next.js + Mantine on Vercel (`data-dpl-id`), HU | same stack, EN |
| Home | 559 KB HTML, 30 scripts, 3 stylesheets; TTFB 4,8 s cold | 118 KB, 24 scripts; TTFB 0,53 s |
| Content | hero, location step, 8 categories, 7 age bands, "this week", saved items, map, account | home, find sports, map, account; "no pins in this view" on first load |
| Public API | `/api-reference`: `browse-facets`, `map-pins`, `site`, `listings/[id]/nearby`, `scout?q=` (intent search with explanations), `POST /api/ingest` (create a discovery card, API key) | not checked |
| Listings | **431**, all with coordinates (`capped: false`, `unmapped: 0`) | not counted |
| Claim state | every listing shows "Az enyém ez a sportolási lehetőség" — **none claimed** | — |
| Verification | "Ellenőrzött" / "Checked recently" with a date on every listing (crawler check, not owner verification) | — |
| Ingestion | IDs `l-openclaw-<name>-<domain>` — cards created from the businesses' own websites | — |
| Structured data | `LocalBusiness` JSON-LD on every listing: name, description, url, sameAs (the business's site), address, geo | — |
| Version | 0.121.1 · sportolok · c8b7a08 | 0.201.105 |

## 2. The catalogue as pulled (`data/listings.json`, 431 rows)

| Field | Coverage |
|---|---|
| Category (8 facets + multi + default) | Edzőtermek 119 · Sportboltok 82 · Többféle lehetőség 63 · Bérelhető pályák 59 · Gyógytorna 44 · Sportegyesületek 26 · Tanfolyamok 17 · Szabadidősport 10 · Egyéb 6 · Versenyek 5 |
| County | 20; Budapest 190, Pest 58, Csongrád-Csanád 23, Bács-Kiskun 22, Veszprém 20 … |
| Locality | 147; Budapest 176 (districts appear in the locality string), Szeged 21, Debrecen 12 |
| Website (`sameAs`) | 395 of 431 — the activation channel exists for 92 % |
| Description | 385 |
| Opening hours (parsed from the page) | 175 |
| "When" tags (weekday/weekend, morning/evening, price) | 23 |
| Next session in the coming 7 days | 21 — the "this week" automation has thin real input today |
| Checked date | 431 (all between 2026-09-13 and 2026-09-18) |
| Age bands | every facet count equals 431 — ages are not yet a real per-listing attribute on this instance |

Facets and site copy are in `data/platform.json`. Territory has three levels (vármegye,
kerület, városrész); only the first is populated.

## 3. The reference videos (owner-supplied)

Two ~100 s vertical videos by the same creator (@structurewebworks / @restructural),
21 frames each read at 5 s intervals:

| | Video 1 — "62 AI agents run an entire social media team" | Video 2 — "The one-person sales & marketing team" |
|---|---|---|
| Structure | 03 Orchestrator → eight departments; 04 Knowledge layer + access ("Brand OS file system": `/brand-brain/voice-guide.md`, `positioning.md`, `messaging-pillars.md`, `/signals-seo`, `/content`, `/creative`, `/social`, `/reputation`, `/conversation`, `/reporting`); access control plane | departments: research & intelligence (Google Trends, Semrush, SparkToro) → content engine (Claude + Surfer; `brief.md`, `offer.md`, `values.md`) → distribution (Metricool → IG/FB/TikTok/YouTube) → creative studio → lead capture & routing (ManyChat DMs, CallRail) → sales & booking (HubSpot, Twilio SMS, Calendly, payments) → results (Looker "Today's recap") → knowledge updated (`leads.md`, `customers.md`, `targets.md`) → back to research |
| Operating rule (captions) | "it reads what … brief draft … and it can't post … it doesn't go out"; "a rival launches, it reads it — that's a strategist"; "someone tags you — not a queue, first"; "it stops and asks"; "the owner still owns"; "everything else runs" | "first"; "nobody logs in"; "anyone"; "the information" |
| Example business | a skincare/social brand | "Structure Motors" — a test-drive request for a 911 GT3 RS handled from DM to calendar |
| Tools shown | Claude, Surfer, Grammarly, GBP reviews, Podium, Yelp, Semrush, GA4, GSC, Ahrefs, Canva, Midjourney, Descript, CapCut, Looker, BigQuery | Claude Code as the orchestrator; HubSpot, ManyChat, Calendly, Twilio, Metricool, Looker Studio |

What business.direct takes from them: departments as the unit; the knowledge layer as
files the owner can read; approval before anything leaves; the recap; integrations as
the machine's hands. What it does not take: 62 agents and a tool stack of twenty
subscriptions — the listed business is one person with a phone.

## 4. What DiscountDirect already gives this project

SSOT terms (offer, channel, consent, frequency cap, holdout, predefined rule set /
advanced mode), the GDS token names, the decided stack (D26: Next.js 15, MongoDB Atlas,
Vercel, DoneIsBetter SSO, Resend, Vercel Cron + outbox, Socket.IO, Upstash, Blob), and the
research on price and the nine buying levers. business.direct reuses all of it and adds
the listing platform as the data source and the three roles.
