# business.direct — product definition

*The product definition. Written 2026-09-19; rewritten 2026-09-20 in the owner's definition
(D41): a standalone product for classified media owners — content generated and delivered to
every medium, the B2B sales process (contact, acquire, reduce churn), the owner's economics as a
service; ClassScout is the persona example and the first buyer. Everything here is what the
owner said, what the first customer's site exposes, and what the two reference videos show.*

## The product

**business.direct is a standalone product for classified media owners** — listing platforms,
directories, marketplaces of local businesses — to run the three jobs their business never
stops needing: **marketing** (content generated from the listings and delivered to every
medium, so visitors come and come back), **B2B sales** (every listed business contacted and
acquired as a paying advertiser through a lawful pipeline) and **retention** (churn seen weeks
ahead and answered with a touch). It runs as departments the owner approves, on the owner's
own data and plain-text knowledge files, with a human gate on everything, one loop that ranks
the next dollar, and **the owner's economics as a service** — what a listing sells for, what an
advertiser costs to win and is worth, what a visitor costs to bring in, what churn costs and
retention keeps, all costs and incomes, on one screen. Every site is an instance with its own
policy record; the second site is a record and a connector.

## The customer persona

The classified media owner: one person (or a very small team) who gathered the supply,
built the site, and is now the whole sales and marketing department for both sides of it —
thousands of listings not yet sold to the businesses on them, visitors who save and hear
nothing, advertisers who leave for reasons visible weeks earlier. The pain and the machine are
the same whether the listings are children's activities, sports clubs, jobs or second-hand goods.

## The example and first customer

**ClassScout**, operator of **Your Field NYC** (getyourfield.com; contact info@classscout.ai) —
"youth sports discovery, starting with your neighborhood": a children's-activity directory in
New York, families on one side, activity providers on the other, a catalogue gathered by a
pipeline with thousands of listings still to publish, one founder as the department. ClassScout
is the **example** every document uses to make the persona concrete and the **first buyer** of
the product. In the product's terms its visitors are "families" and its advertisers are
"providers" — the product shows each site's own words. The prototype runs on a demo sample of its public listings — demo data, never a statement about
the size or state of the customer's business.
*Most én sportolok!* (sport.doneisbetter.com) is a second directory pulled through the same
connector shape to prove the second instance.

**business.direct is a sibling of DiscountDirect** (D5): DiscountDirect retains a web shop's
customers; business.direct sells, fills and keeps a classified media site.

## The problem

One person cannot run marketing, sales and retention for thousands of listings. The money is
lost where nobody is: listings nobody contacted earn nothing; the second and third touch —
which bring 42 % of all replies — never get sent; enquiries the site forwards die unanswered (a lead
is 21× more likely to qualify in the first five minutes); the material that exists (offers,
dates, news, footage) is never published; a paying advertiser leaves for reasons visible weeks
earlier; the numbers are a feeling (research I, II). The tools on sale each do one job.

The first customer shows the shape: a marketplace whose prospects are the listed providers
and whose audience is families, with thousands of listings to publish and one founder as the
department. What the product computes for an owner, and how, is `economics.md`; the owner's
own numbers appear on the Economics screen once the site is connected.

**Where the shape came from.** The two videos the owner shared show the target: **the one-person sales and
marketing team** — an orchestrator over departments (research and intelligence, content,
distribution, creative, leads and conversations, reviews and reputation, results), a
**brand knowledge layer** kept as plain files, **human-in-the-loop** ("it drafts, it can't
post, it stops and asks, the owner still owns"), an intelligence recap, and integrations
that make the machine run while "nobody logs in".

## What is built

A clickable prototype in English with **three views** (D2, D10):

| View | Who | What they see |
|---|---|---|
| Media owner ("Platform" on Your Field) | the classified media owner | the machine across every listing: marketing, sales, retention, the approval queue, economics, the recap, integrations, the policy record |
| Advertiser ("Provider" on Your Field) | a listed business after claiming its page | its own one-person team: conversations with visitors, campaigns, the site's advertising products, results, knowledge files |
| Visitor ("Family" on Your Field) | a person using the site | what arrives: the weekly digest, saved-listing alerts, an advertiser's offer, and the controls over channel and frequency |

Three jobs: two flows at the front door (D14) and retention behind the pipeline (D41):

| Flow | What the machine does | Who approves |
|---|---|---|
| **B2C social** | Turns listings, updates and news into posts for Instagram, Facebook, TikTok and X — a provider spotlight, "this week in Park Slope", a new-camp announcement, a parent tip — scheduled, drafted (AI optional), and published only after approval, each with the link back to the listing page. Goal: new families on the platform. | platform operator |
| **B2B sales** | Works every listed provider through a pipeline — identified → contacted → replied → applied → managing → upgraded — with e-mail and phone from the card, sequences with human sign-off, the reply inbox, and the upsell ("and more": featured listing, camp placement, campaigns). Goal: providers who manage their own listing and buy more. | platform operator; the provider on their side |

**Retention (reduce churn)**: every managing advertiser watched for a renewal, a stale page, an unanswered enquiry, a listing that stopped surfacing; a touch drafted from its own numbers; kept and lost logged into the churn rate (D41). Behind them: **family digests and alerts**, **generated landing pages and SEO** (activity ×
neighbourhood × age), **provider campaigns** (trial classes, open spots, announcements,
registration — built from the card, approved by the provider, sent by the family's
preferences under the cap; phase 2, D22), **upgrades** (the platform's own products, D21)
and **activation** as the pipeline's first stages. Optional AI support is a layer the operator or provider switches
on per department, never a requirement (D6). An **intelligence dashboard** and an
**integrations** screen (the platform's own API first, then the social channels, e-mail,
phone/SMS) are part of the first build.

## What is real

The prototype's data is a **demo sample of the first customer's public listings**, pulled by
`data/fetch-yourfield.py` and never edited by hand: on each listing the name, category, area,
address, contact, sessions, trial policy, announcement, claim state and verified fields are the
site's own, and the site copy is the site's own. The sample's size and coverage are described in
the first-customer file (`first-customer-classscout.md`), not here, because they describe the demo,
not the customer's business. Everything that is not on the site — an advertiser's brand voice, a
campaign's results, the visitor persona and her saved items, the managing cohort — is **sample**
and is declared as sample on the page. No advertiser or visitor is contacted by the prototype.

## What is inert

Sending (e-mail, push, SMS, social), publishing generated pages, claiming a card,
connecting an integration with a key. Each is shown in place, visibly inert, with the reason.

## Where it stands

Every stage of the standard is done (2026-09-19). Gates 1 and 2 approved (D9, D16); the
prototype built in nine rounds (`build-log.md`) — the two flows, campaigns and upgrades,
conversations, economics, the research implemented, the audit implemented, the
responsible-data policy record and gate, the Simple and Advanced interfaces — and measured
(`gate.md`); the presentation, the business logic, the technical package (the stack
verified service by service and the system blueprint with modules and pseudo code, D37), the
audit and SWOT, and the policy framework written. Nothing is open for the presentation; what
the implementation needs after acceptance is `first-customer-classscout.md`; the build
starts with the sprint-0 checklist in `delivery-plan.md`. **Next: present.**
