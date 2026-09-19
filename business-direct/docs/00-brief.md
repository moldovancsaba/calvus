# business.direct — brief

*Stage 0 of the prototyping standard (`PROTOTYPING.md`). Written 2026-09-19, before any
page exists. Everything here is what the owner said, what the two reference platforms
expose, and what the two reference videos show — nothing else.*

## The client

The owner's own product family. The reference platforms are DoneIsBetter listing sites —
*Most én sportolok!* (sport.doneisbetter.com, a Hungarian sports-opportunity directory) and
*Your Field NYC* (getyourfield.com, kids' activities by borough) — and the pattern
generalises to job portals, classifieds and any listing site. **business.direct is a
sibling of DiscountDirect** (D5): DiscountDirect retains a web shop's customers;
business.direct markets a *listed business*.

## The problem

A listing platform is B2B2C: **platform → listed business → consumer**. On the sport
platform 431 businesses are listed, ingested by a crawler from their own websites; none has
claimed its card ("Az enyém ez a sportolási lehetőség" appears on every one). The
businesses are one-person or few-person operations — a gym, a physio, a climbing wall, a
squash club — that do no marketing, answer no reviews, send no reminders, and do not know
they are listed. The consumer side has facets, ages, a map and saved items, but nobody
tells a consumer what is on near them this week.

The two videos the owner shared show the target shape: **the one-person sales and
marketing team** — an orchestrator over departments (research and intelligence, content,
distribution, creative, leads and conversations, reviews and reputation, results), a
**brand knowledge layer** kept as plain files, **human-in-the-loop** ("it drafts, it can't
post, it stops and asks, the owner still owns"), an intelligence recap, and integrations
that make the machine run while "nobody logs in".

## What will be built

A clickable prototype with **three views** (D2):

| View | Who | What they see |
|---|---|---|
| Platform | the operator of a listing site | the machine across every listing: automations, audiences, approval queue, the intelligence dashboard, integrations |
| Business | a listed business after claiming its card | its own one-person team: knowledge layer, departments, what is waiting for approval, what went out, results |
| Consumer | a person using the listing site | what arrives: the weekly "near you" digest, saved-item alerts, a business's offer or event, and the controls over channel and frequency |

Four automations are clickable (D3): **consumer digests and alerts**, **business
activation** (you are listed — claim, verify, add), **generated landing pages and SEO**
(category × place × age), **business campaigns** (offers, open slots, course starts,
events — DiscountDirect's offer cards on listing data). Optional AI support is a layer
the owner can switch on per department, never a requirement (D6). An **intelligence
dashboard** and an **integrations** screen (the platform's own API first) are part of
the first build (D6).

## What will be real

The data: **431 real listings** from the sport platform's public API and pages (8
categories, 20 counties, 147 localities, 395 websites, 385 descriptions, 21 with a next
session), pulled by `data/fetch-sportolok.py` and never edited by hand (D4). The site copy
and facets are the platform's own. Everything that is not on the platform — a business's
brand voice, its offers, the results of a campaign — is **sample** and is declared as
sample in the page. No listed business is contacted by the prototype.

## What will be inert

Sending (e-mail, push, SMS, social posts), publishing generated pages to the platform,
claiming a card, connecting an integration with a key. Each is shown in place, visibly
inert, with the reason.

## Where it stands

Stage 0–2 done 2026-09-19 (this brief, `01-research.md`, `02-audit.md`, `03-sources.md`,
the data converter). **Gate 1 — the design system (`design-system.html`) — awaits the
owner's approval.** No layout, no page before that (standard §2).
