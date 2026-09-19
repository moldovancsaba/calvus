# business.direct — brief

*Stage 0 of the prototyping standard (`PROTOTYPING.md`). Written 2026-09-19, revised the same
day when the owner named the first client. Everything here is what the owner said, what the
client platform exposes, and what the two reference videos show — nothing else.*

## The client

**Your Field NYC** (getyourfield.com) — "youth sports discovery, starting with your
neighborhood": 252 providers of kids' classes, camps and drop-in activities across
Manhattan (107) and Brooklyn (145), 84 neighbourhoods, 20 activity types, saved items, a
family plan with cost estimates, a newsletter, and a "List your program" pitch to
providers. It is the owner's own product (Next.js + Mantine on Vercel), the **first
platform business.direct will run on** (D11). *Most én sportolok!* (sport.doneisbetter.com,
Hungary) and job portals / classifieds are reference ideas: the same pattern, other
instances.

**business.direct is a sibling of DiscountDirect** (D5): DiscountDirect retains a web shop's
customers; business.direct markets a *listed business* to the families on the platform —
and markets the platform to the business.

## The problem

A listing platform is B2B2C: **platform → listed business → consumer**. On Your Field every
provider was gathered from its own website by an enrichment pipeline (field-level
verification records say which fields were read from where); **none is claimed** — 15 are
marked `unclaimed` explicitly, 237 carry no claim state at all. The providers are small
operations — a soccer club run by one coach, a taekwondo school, a dance studio — that
answer late, do not follow up trials, and do not know the platform sends them families.
On the consumer side, parents can save and plan, but nobody tells them what starts near
them this week.

The two videos the owner shared show the target shape: **the one-person sales and
marketing team** — an orchestrator over departments (research and intelligence, content,
distribution, creative, leads and conversations, reviews and reputation, results), a
**brand knowledge layer** kept as plain files, **human-in-the-loop** ("it drafts, it can't
post, it stops and asks, the owner still owns"), an intelligence recap, and integrations
that make the machine run while "nobody logs in".

## What will be built

A clickable prototype in English with **three views** (D2, D10):

| View | Who | What they see |
|---|---|---|
| Platform | Your Field's operator | the machine across every provider: automations, audiences, the approval queue, the intelligence dashboard, integrations |
| Provider | a listed business after claiming its card | its own one-person team: knowledge files, departments, what is waiting for approval, what went out, results |
| Family | a parent using Your Field | what arrives: the weekly "near you" digest, saved-item alerts, a provider's trial offer or announcement, and the controls over channel and frequency |

Two flows are the front door (D14), and four automations sit behind them (D3):

| Flow | What the machine does | Who approves |
|---|---|---|
| **B2C social** | Turns listings, updates and news into posts for Instagram, Facebook, TikTok and X — a provider spotlight, "this week in Park Slope", a new-camp announcement, a parent tip — scheduled, drafted (AI optional), and published only after approval, each with the link back to the listing page. Goal: new families on the platform. | platform operator |
| **B2B sales** | Works every listed provider through a pipeline — identified → contacted → replied → applied → managing → upgraded — with e-mail and phone from the card, sequences with human sign-off, the reply inbox, and the upsell ("and more": featured listing, camp placement, campaigns). Goal: providers who manage their own listing and buy more. | platform operator; the provider on their side |

Behind them: **family digests and alerts**, **generated landing pages and SEO** (activity ×
neighbourhood × age), **provider campaigns** (trial classes, open spots, announcements,
registration — built from the card, approved by the provider, sent by the family's
preferences under the cap; phase 2, D22), **upgrades** (the platform's own products, D21)
and **activation** as the pipeline's first stages. Optional AI support is a layer the operator or provider switches
on per department, never a requirement (D6). An **intelligence dashboard** and an
**integrations** screen (the platform's own API first, then the social channels, e-mail,
phone/SMS) are part of the first build.

## What is real

The data: **252 real providers** from Your Field's public API (`data/fetch-yourfield.py`,
never edited by hand, D4/D11): name, category, borough, neighbourhood, address, 219 with
coordinates, every one with a website, 180 phones, 130 e-mails, 28 stated prices with
evidence, 73 with sessions, 83 with a next occurrence, 72 with a trial policy, 26 with an
announcement, 10 with booking enabled, claim state, verified fields. The site copy
(hero, how it works, trust pillars, newsletter, "List your program") is the platform's
own. Everything that is not on the platform — a provider's brand voice, a campaign's
results, the parent persona and her saved items — is **sample** and is declared as sample
in the page. No provider or family is contacted by the prototype.

## What is inert

Sending (e-mail, push, SMS, social), publishing generated pages, claiming a card,
connecting an integration with a key. Each is shown in place, visibly inert, with the reason.

## Where it stands

Stages 0–5 done 2026-09-19. **Gate 1 (design system) approved (D9)**, re-issued in
English on the client's data the same day; **gate 2 (layout frames) approved (D16)**; the
prototype built as one page with three views (`../index.html`, D17–D18) and measured at 390
and 1440 (`06-build-log.md`, `07-gate.md`); the presentation (`bemutato.html`) and the
technical package (`10`–`14`, stack PROPOSED) written. Tested by the owner and accepted (D20); round 2 shipped. **Phase 2 (D21–D24)**: provider
campaigns and results, upgrades, the intelligence recap, the business-logic document — asks
#4–6 assumed (D21) until answered. **Next: the owner's answers, or a flipped ADR.**
