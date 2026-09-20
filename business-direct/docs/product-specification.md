# business.direct — product specification: how it works, how the customer uses it, what it delivers

*For the stakeholders who accept the product and the team who builds it. What this document
holds: the product screen by screen and role by role — what each screen shows, what the product
does on it alone, what needs a person, what state changes, and the benefit it delivers, measured
on the screen. The prototype (`../index.html`) is the reference for every screen described here;
the rules behind every behaviour are in `business-logic.md`; the numbers the Economics screen
computes are in `economics.md`. Product terms are used first — **media owner · advertiser ·
visitor · listing** — with the first customer's words (platform · provider · family · card) in
brackets, because the prototype runs on that instance. Written 2026-09-20 (D44).*

## 1. The product in one screen

A classified media owner logs in once a day. The product has already done the night's work:
read the listings for what is new, drafted the week's content, moved every prospect through
the pipeline on the events that happened, drafted an answer to every reply, enquiry and comment,
watched every paying advertiser for the signals before a cancellation, and computed the owner's
numbers. The owner sees **what needs a person**, approves it, and leaves. Nothing has left the
product without that approval; every message that left says why it went, who approved it and
how to stop it.

Three roles use it: the **media owner** (the operator who approves), the **advertiser** (a listed
business, once it manages its page, with its own team inside the product) and the **visitor**
(who never logs in to the product — preferences reach it by signed link).

## 2. The three jobs and the departments that do them

| Job | Departments | What runs alone | What needs a person |
|---|---|---|---|
| **Marketing** — content generated from the listings and delivered to every medium | social publishing; weekly picks (the digest and alerts); generated pages; market radar; media (the clip engine) | drafts, slots, reads comments and DMs, drafts the reply, builds the digest within the cap, computes pages where ≥ 3 listings exist, writes the weekly radar note, cuts clips from uploaded footage | publish; send a reply; publish a page; file the radar; confirm consent for footage that shows children |
| **B2B sales** — contact and acquire advertisers | prospect sales (the pipeline, sequences, the reply inbox, the call list); conversations (the advertiser's inbox); campaigns; placements | drafts the sequence and every reply, moves stages on events, orders recipients by propensity, builds the call list, sizes audiences, drafts campaigns from the listing | send; override a stage; approve a campaign; choose a placement |
| **Retention** — reduce churn | retention (signals, drafted touches, kept / lost) | watches renewals, page freshness, enquiry response and saves; drafts the touch from the advertiser's own numbers; logs kept and lost into the churn rate | send — renewal reminders may earn auto-approval; at-risk touches need judgement |
| **The numbers** | economics; the Monday recap; the policy record and gate | computes CAC, LTV, payback, visitor cost and value, churn and retention value, the next dollar, the twelve-month plan; blocks any feature whose policy fields are missing | change an input; complete a policy field; read the recap and decide |

The human gate: it drafts, it cannot send, it stops and asks. Simple mode shows the owner only
what needs a person, ranked, with the reason and one button; Advanced mode shows every screen
and input. A department that runs four clean weeks earns auto-approval for its routine messages
— every one still logged and stoppable (R25).

## 3. The media owner's screens (the "Platform" view on the first instance)

### 3.1 Home — Simple mode's first screen
- **Shows**: the recommendations, ranked — approve this week's posts and clips, send the invitation to the next batch (if the policy gate allows), answer the replies, send the renewal reminders, review the at-risk advertisers, complete a missing policy field, the next dollar — each with the reason (the research figure or the rule behind it) and one button.
- **Alone**: everything above is drafted overnight.
- **Needs a person**: one press, *Do the recommended actions*, runs every recommendation marked safe (approvals of posts and clips, the invitation when the gate allows, renewal reminders, filing the radar). Replies, at-risk touches and judgement calls stay with the owner.
- **State**: each action moves its items to *scheduled* / *sent* and logs the operator's decision.
- **Benefit**: the day's work in twenty minutes; the operator's hours are measured on Economics.

### 3.2 Overview (Advanced)
- **Shows**: tiles for each department (each labelled real or sample), this week's posts waiting, the pipeline across every listing, the departments with their AI switch, the listings table.
- **Needs a person**: approve and schedule a post from here; switch AI per department (R10).

### 3.3 Social publishing
- **Shows**: the week's drafts per channel (Instagram, Facebook, TikTok, X), each linking back to its listing; the calendar and slots; the week's anchor per neighbourhood × category; comments and DMs on published posts with a drafted reply; media labels (real footage · generated, credentialled, labelled at publish).
- **Alone**: drafts from what is new on the listings; slots; reads comments; drafts replies with the listing link.
- **Needs a person**: approve, edit or skip each post (editing removes the AI badge); approve real-footage clips as a batch; approve each comment reply.
- **State**: *waiting → scheduled → published*; a comment arrives as *waiting*.
- **Benefit**: every week's content published from material the site already has; visitors per post measured once a channel is connected.

### 3.4 Prospect sales (the pipeline)
- **Shows**: the pipeline strip — identified → contacted → replied → applied → managing → upgraded — with counts; the invitation sequence (three touches in propensity order) with one approval for the whole run; the sending card (domain, warm-up day, daily cap, bounce rate, reply SLA); the reply inbox with a drafted answer per reply; the call list for phone-only prospects.
- **Alone**: scores every listing; drafts the sequence and every reply; moves stages on events (a reply → *replied*; an application → *applied*; the site's confirmation → *managing*); turns a visitor's enquiry to an unclaimed listing into the strongest touch ("a visitor asked about you"); excludes opt-outs and "not my program"; refuses to send past the warm-up cap or the bounce limit (R23) or without the legal footer and postal address.
- **Needs a person**: approve the sequence; approve or edit each reply; override a stage (logged with who and why).
- **State**: stages move forward on events; a person may move any stage, logged.
- **Benefit**: every listing contacted in the right order; every reply answered within a business day; the cost per managing and per paying advertiser measured.

### 3.5 Retention
- **Shows**: managing advertisers, at risk, kept this month, LTV at risk and expected kept, the churn rate; the watch list with each advertiser's signals (renewal due, no update for 30 days, an enquiry unanswered for two days, no saves in 30 days); the drafted touches waiting.
- **Alone**: watches the four signals nightly; drafts one touch per signal from the advertiser's own numbers — a renewal reminder that arrives with results, a nudge naming the stale field and the visitors searching that category — never a discount (R37).
- **Needs a person**: approve or edit each touch; renewal reminders may run from Home's safe press.
- **State**: a touch approved marks the advertiser *kept* for the period; kept and lost feed the churn rate.
- **Benefit**: churn seen weeks ahead; keeping an advertiser costs a touch where replacing one costs a CAC — the lever is ranked against acquisition every week.

### 3.6 Approvals
- **Shows**: everything that would leave the product, newest first — sequences, replies, retention touches, comment replies, posts.
- **Needs a person**: approve, edit in the owner's own words, or skip.
- **Benefit**: one place where the human gate is visible and auditable.

### 3.7 Listings (the "Providers" table)
- **Shows**: every listing with contact on the card, next session, propensity score and stage; chips by contact, trial, claim state, stage; a search; a drawer per listing with the card (real), the stage history (who, why, when), the thread and the stage chips.
- **Alone**: the score (e-mail, phone, trial, session, announcement, image, verified fields, replied, applied, a visitor's save or ask, minus bounces and "not my program") orders who is written to first.
- **Benefit**: the whole supply side, worked in propensity order.

### 3.8 Generated pages
- **Shows**: category × neighbourhood pages the product can publish to the site for search and AI answers, with the count of listings and the readiness score.
- **Alone**: computes the pages; publishes only where ≥ 3 listings exist and readiness ≥ 3 of 4 (verified fields, a session, reviews, a last-verified date).
- **Needs a person**: publish through the site's connector.
- **Benefit**: the site becomes the structured, reviewed source AI answers cite.

### 3.9 Intelligence — the Monday recap
- **Shows**: what moved this week by department (contacted, replied, applied, managing, upgraded, kept; posts published; visitors reached; placement revenue), the market radar from the catalogue (largest category, free trials, unknown prices, page opportunities, unreachable listings), and *needs you* (approvals waiting, replied-not-applied, advertisers at risk, integrations to connect, the next dollar, the policy gate).
- **Benefit**: one screen on Monday; every tile says whether it is real or sample.

### 3.10 Economics
- **Shows**: CAC per managing and per paying advertiser; LTV, LTV : CAC and payback; the value of an engaged visitor; engaged visitors; advertisers at risk and the retention value; operator hours; cost per new visitor from content; the next-dollar ranking (retention touches, one more e-mail touch, the call list, a week of content); the funnel this quarter; the experiment running (a neighbourhood holdout); the twelve-month plan; every input, editable, with its status (measured · benchmark · assumption).
- **Alone**: recomputes every figure from the listings, this week's events and the inputs; flips a rate to *measured* at 100 observations (R16); the cadence, the content slots and the moment a placement is offered follow the numbers (R17–R19).
- **Needs a person**: change an input; act on the next dollar.
- **Benefit**: the owner's economics as a service — what a listing sells for, what an advertiser costs and is worth, what a visitor costs and is worth, what churn costs and retention keeps, all costs and incomes, on one screen, on the owner's own numbers.

### 3.11 Integrations
- **Shows**: the connectors that give the product hands — the site's API, e-mail, Instagram and Facebook, push (v1); TikTok, X, SMS, Google Business Profile, calendars (later) — with their state.
- **Needs a person**: connect with a key (the prototype shows states only).

### 3.12 Policy — the responsible-data record and the gate
- **Shows**: one record per site — identity and postal address, jurisdictions and the laws derived, audience model, child-data rule, channels and their consent basis, defaults, the cap, opt-out SLA, AI disclosure, retention, the site's privacy-policy clauses, media consent, safeguarding, vulnerability, protected characteristics, accessibility, sensitive categories, dark patterns — each field set / missing / placeholder, and the feature it blocks.
- **Alone**: blocks every feature whose fields are missing and says why (R26): advertiser e-mail needs the postal address; the digest needs the privacy policy to describe it; SMS needs the consent text; generated media needs the disclosure rule; a minor's field needs the audience model and a DPIA.
- **Needs a person**: complete the record — this is the onboarding checklist for any site.
- **Benefit**: the wrong default cannot ship; every send carries its policy basis.

### 3.13 Templates, Knowledge and rules, How to use
- **Templates**: sequences, posts, campaigns, knowledge files and policy records for other site types; *Use* copies one into the product.
- **Knowledge and rules**: the plain-text files the product reads before every draft — voice, consent rules, social rules; edit in place and every draft after follows (R8).
- **How to use**: the routine, the states, the rules that never move, the screens, the documentation.

## 4. The advertiser's screens (the "Provider" view)

| Screen | Shows | Alone | Needs the advertiser | Benefit |
|---|---|---|---|---|
| **Today** | until the page is claimed: the invitation and *Apply to manage my page*; after: today's numbers, what waits, the four departments, the knowledge files, the plan ladder; the site's placements appear once the product has delivered more than they cost (R19) | the departments' drafts | apply; approve; choose a placement | its own team the day it manages the page |
| **Conversations** | every visitor enquiry — a site message, an e-mail, a missed call — with an answer drafted from its own files and its listing; reply time | drafts within a minute (R14); texts back a missed call; FAQ answers earn auto-send after four clean weeks | approve or edit each answer | every enquiry answered within the hour |
| **Campaigns** | trial, open spots, announcement, registration — drafted from the listing, with the audience it may reach (visitors who saved it, nearby visitors who opted in) and the cap it runs under | drafts and sizes the audience from the site's data only (R11) | approve, edit, skip | messages only to visitors who chose it, under the cap |
| **Media** | a session recording upload; the consent confirmation when children appear (R30); the clips cut with captions and the listing link; the photos on the card | cuts, captions, credentials; refuses without consent | upload; confirm consent | real footage first, generated only to fill gaps, labelled |
| **Results** | what went out and what came back — enquiries, trials, the return against the plan; the plan ladder | computes from the message log | — | the advertiser sees its return before it is asked to pay |
| **Knowledge** | voice, offer, FAQ | every reply and campaign reads them first | edit | answers in its own words |

## 5. The visitor's side (the "Family" view — by signed link, never a login)

| Screen | Shows | Rules |
|---|---|---|
| **Inbox** | what arrived and why: a post, the Sunday digest built from saved listings and nearby sessions, an advertiser's campaign naming the listing saved, the channel and the count toward the cap; a text with the consent behind it | the cap: four advertiser-originated messages a month; the site's own digest and alerts follow the visitor's switches (R3); why-you-got-this on every message (R2) |
| **Saved** | the saved listings; *Ask about a trial* — the question lands in the advertiser's inbox, or, if the page is unclaimed, becomes the site's strongest sales touch and the visitor is told | a visitor writes first; an advertiser never messages a visitor who did not save or ask (R11) |
| **Preferences** | channel by channel (picks, alerts, nearby, texts), consent per advertiser, the cap, Stop | every switch off until the visitor turns it on (R28); SMS only with written consent per advertiser (R4); Stop turns everything off and cancels what is queued, in one transaction |

No child's name, photo or location exists in the product; a child is an age (R24).

## 6. Onboarding a site — the first week

1. Connect the site's API (read the listings; a key for writes when the site provides one) and the channels.
2. Fill the policy record on the Policy screen; the gate shows what each missing field blocks.
3. Write the knowledge files — voice, rules, offers — or start from the templates.
4. Load the placements (the site's own products and prices) and the sending domain.
5. Run the first week in Simple mode: the invitation to the first batch, the first posts, the first replies.
6. Read the first Monday recap; the first measured rates replace assumptions on Economics at 100 observations.

The second site is a policy record and a connector, not a rebuild.

## 7. What the product never does

Sends without an approval or a preference; discounts to keep an advertiser; texts without consent; sends past the sending domain's limits or without the postal address; shows a child's name; profiles or targets a minor; cuts footage that shows a child without written parental consent; claims safety it has not verified; pressures anyone; builds an audience on a protected characteristic; stores a sensitive category; runs a feature its policy record does not allow; publishes generated media unlabelled; generates a person; exceeds the cap; deletes a stage history; speaks as an AI — it speaks as the site or the advertiser.

## 8. The benefits, measured

| Benefit | Where it is measured |
|---|---|
| Sold inventory | the pipeline counts; CAC per managing and per paying advertiser; placement revenue in the plan |
| Visitors who come back | visitors per post (once a channel is connected); digest opens; cost per new visitor; the value of an engaged visitor |
| Advertisers who stay | at risk, kept, lost; the churn rate from the retention log; LTV at risk and kept |
| The next dollar | the weekly ranking of four levers by expected value per dollar |
| The owner's time | operator hours this week; departments' earned auto-approval |
| Lower exposure | the policy gate's report; the policy basis on every send; the delivery audit by neighbourhood |
