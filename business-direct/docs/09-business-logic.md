# business.direct — business logic

*Written 2026-09-19 with phase 2 (D21–D23). The machine's rules end to end, in the order
money and messages move: who the parties are, what each department does, what leaves, who
approves, what it costs, what stops it. Terms are the SSOT's (`10-ssot.md`); the decisions
behind each rule are in `04-decisions.md`; the prototype (`../index.html`) implements every
rule below in memory.*

## 1. The three parties and what each gets

| Party | Gets | Gives |
|---|---|---|
| **Platform** (Your Field NYC) | more families (B2C social), providers who manage their page and buy upgrades (B2B sales), a machine that runs while nobody logs in, one approval queue | the catalogue, the family accounts and preferences, the channels' authority, the operator's approvals |
| **Provider** (a listed business) | its own one-person team the day it manages its page: replies, reminders, campaigns to families who saved it, results; a free page and paid reach | a claim, its knowledge files, its approvals, and — if it upgrades — a monthly or seasonal fee |
| **Family** | what starts near them this week, alerts from providers they saved, offers only from providers they chose, one cap, one Stop | preferences, and consent where the law requires it |

## 2. The two flows at the front door (D14)

**B2C social publishing → families.** Every provider with news (announcement, trial, next
session) becomes a post draft with the link back to its page. The operator approves,
edits or skips; approved posts publish at their calendar slot through the platform's
channels. Families arrive on the listing page; the platform's sign-up captures them.
*Nothing publishes unapproved.*

**B2B provider sales → providers.** Every provider enters the pipeline at *identified*.
The invitation sequence (one approval for the whole run) moves those with an e-mail to
*contacted*; a reply moves to *replied* and lands in the inbox with a drafted answer;
"Apply to manage" (or a confirmed yes) → *applied*; the platform's confirmation →
*managing*; a paid product → *upgraded*. Phone-only providers get a call task; providers
with neither get the website form. "Not my program" or unsubscribe stops everything for
that address.

## 3. The departments (D6) and what each may do alone

| Department | Runs alone | Needs a person |
|---|---|---|
| Social publishing (platform) | draft, schedule slots, read comments and DMs, draft the reply with the link to the listing | publish, send the reply — "someone tags you — first, not a queue" (D25) |
| Provider sales (platform) | draft the sequence and the reply, move stages on events, build the call list | send, override a stage |
| Weekly picks (platform → families) | build the Sunday digest and saved-provider alerts within the cap | nothing — the family's preferences are the approval (R2, R3) |
| Generated pages (platform) | compute activity × neighbourhood pages with ≥ 3 providers | publish through the platform |
| Market radar (platform) | the weekly note from the catalogue | read and file |
| Conversations and reputation (provider) | draft an answer to every enquiry (platform message, e-mail, missed call) from the knowledge files; text back a missed call | send — the provider approves or edits each answer (phase 3, D25) |
| Reminders (provider) | 3-day and 1-day session reminders to booked families | nothing — the booking is the consent |
| Campaigns (provider) | draft trial, open-spots, announcement and registration campaigns from the card; size the audience | approve, edit, skip |
| Page and visibility (provider) | keep sessions, trial and photos on the card current | choose an upgrade |

AI is optional per department (R10). With it off, every draft is the listing's own text or
a template with merge fields; with it on, the knowledge files are the prompt and the draft
carries the ✦ badge until a person edits it.

## 4. Provider campaigns (phase 2, D22)

A campaign is a provider's message to families, built from the provider's own card:

| Kind | Built when | Default audience | Default channels |
|---|---|---|---|
| Trial class | the card has a trial policy | families who saved the provider + nearby families with a child in the age range **who turned "new provider nearby" on** (Q3) | e-mail + push; SMS only to families who consented for this provider |
| Open spots | the card has a next session | families who saved the provider | push |
| Announcement | the card has an announcement | saved + nearby | e-mail |
| Registration | a session's registration is open | saved | e-mail + push |

The provider approves, edits or skips; the platform sends by each family's preferences
and never past the cap (R3). A family sees why she received it (she saved the provider),
on which channel, and that it counts toward her monthly four. Audience sizes are sample in
the prototype (ask #6 — the platform's saves data).

## 4b. Conversations (phase 3, D25)

An **enquiry** is a family's message to a provider on any channel the provider exposes:
the platform's message, e-mail, a missed call (the machine texts back). The machine drafts
the answer from the provider's `knowledge/faq.md` and `offer.md` and the card (next
session, trial policy, ages); the provider approves, edits or skips; the answer goes back on
the same channel and into the family's inbox thread. Reply time is measured from the
enquiry to the sent answer — the metric the provider sees first. A family asks from her
saved providers; the machine never lets a provider message a family who has not written
first or saved it (R11). **An enquiry to a provider that has not claimed its page** does
not vanish: it becomes the sales sequence's strongest touch — "a family asked about you,
claim your page and answer her in one click" — the provider moves to *contacted*, and the
family is told the provider has been notified (Q4). The machine stores no child's name at all — the
platform's own policy says it does not collect children's data — so every party, the family
included, sees "a child of 6" (R24, D31). On the platform side, a **comment or DM** on a published post gets
a drafted reply that links to the listing; the operator approves it.

## 5. Upgrades and money (D21: bundled base, provider-bought upgrades)

The base machine is **bundled by the platform** for every listing — the invitation, the
replies, the reminders, the campaigns — because its job is the platform's own growth. The
**provider buys reach**, and the products are the platform's own, from its "List your
program" copy:

| Product | What the provider gets | Price (sample — the platform publishes none) |
|---|---|---|
| Featured listing | top of the neighbourhood and activity lists; the spotlight post every month | $49 / month |
| Camp placement | the camps guide and the March "camps near you" digest | $149 / season |
| Local discovery profile | photos, coach bio, reviews, booking on the card | $29 / month |

Choosing one moves the provider to *upgraded*; the platform's intelligence screen sums the
sample revenue. Billing is Stripe (ADR-9, PROPOSED); the platform invoices, business.direct
records the entitlement. No discounting logic — that is DiscountDirect's domain (D5).

## 6. Families: preferences, consent, cap, stop

- **Preferences** per channel: weekly picks (e-mail), saved-provider alerts (push), new
  provider nearby (push), texts from providers (SMS). Default: picks and alerts on.
- **Consent**: SMS only with written consent per provider, stored verbatim with its time
  and source (TCPA). E-mail and push run on preference.
- **Cap**: 4 **provider-originated** messages a month per family — campaigns and texts,
  across all providers. The platform's own digest and alerts run on the family's switches
  and do not count (D30; the audit found the earlier wording was consumed by the digest
  alone). Checked when a message is queued and again when it is sent.
- **Stop**: one tap turns every channel off and cancels what is queued, in one transaction.
- **Why you got this** on every message: the provider she saved, the channel, the count.

## 7. Providers: the law on the sales side

US (first market): commercial e-mail to a business needs no prior consent (CAN-SPAM);
every message carries the platform's **registered postal address** (a merge field, checked
by the gate — Q2; ask #15 for the address itself) and a working opt-out honoured within 10
business days — the machine honours it within one. A "not my program" or an unsubscribe
excludes the address from every sequence; a bounce lowers its score (Q6). The sending
domain is paced and guarded: warm-up, a daily cap, and a bounce rate above 2 % pauses the
sequence (R23). Hungary (reference): corporate addresses without
consent; a named person's address needs consent — the reference connector flags which is
which. SMS to providers is not used.

## 8. The intelligence recap (D23)

Every Monday the operator reads one screen: providers contacted, replies answered, applied
· managing · upgraded, posts published, families reached by campaigns, upgrade revenue; by
department; the market radar from the catalogue (largest activity, free trials, unknown
prices, page opportunities, unreachable providers); and "needs you" — approvals waiting,
providers who replied but did not apply, integrations still to connect. Real where the
catalogue is the source; sample until the platform's analytics and a pilot provider's
numbers arrive (asks #6–7).

## 8b. Data-driven decisions (D26)

The recap is read; the economics are acted on. The system keeps CAC and LTV per provider
cohort, the marketing value of an avid family, the cost per family from content, and ranks
the next dollar weekly (touch · call · content) by expected LTV gained — on measured rates
where they exist and on documented assumptions where they do not, saying which (R16). The
sequence cadence, the content slots and the upgrade pitch follow the numbers (R17–R19).
The model and its events are `16-analytics-and-unit-economics.md`.

## 8d. What the audit changed (D30)

| Audit finding | Rule / behaviour now |
|---|---|
| A2 the cap consumed by the digest | cap = 4 provider-originated messages; digest and alerts on preference (§6) |
| A3 no postal address | `{postal_address}` in every provider e-mail; the sequence card shows the gate check |
| A4 nearby audience vs preference | reachable nearby = opted in; the card shows the reachable count (§4) |
| A5 enquiries to unclaimed providers lost | the ask becomes sales step 2 and moves the provider to *contacted* (§4b) |
| A6 R9 wording | forward automatically on events; a person may move any stage, logged with who and why |
| A7 R19 on sample trials | R19 keeps the pitch rule with a 60-day floor and the honest number |
| A8 score signals | +15 saved or asked, −40 not my program, −20 bounce, unsubscribed excluded |
| A9 no sending-guard rule | R23 |
| A10 operator time undercounted | operator hours tile; batch approval of real-footage clips; earned auto-approval per department after four clean weeks (reminders earned; FAQ answers week 1 of 4) — every auto-sent message still logged and stoppable |
| A11 capture undefined | capture = upgrades within 30 days of a delivered result ÷ upgrades; measured on the economics screen |
| A12 consent proof invisible | the preference row shows when and where consent was given |
| A13 children's data | R24 age band in provider-facing text; counsel question ask #13 |
| A14 disclosure on drafted messages | R20 extended: an AI-drafted, unedited answer carries the market's disclosure and is logged |
| A17 EU named addresses | connector `contactKind`; EU instances skip `person` addresses without consent |
| A18 stage history | logged per change; the drawer shows the last three |
| S1/T1 Sawyer | positioning: families, not software — a Sawyer connector is a later adapter, never a competing booking tool |
| W1/O4 the conversations line | an economics input: 0 = bundled (D21), 99 = the incumbent's price; the plan's MRR follows it |

## 8c. What the research changed (D28)

| Research finding | Rule / behaviour now in the system |
|---|---|
| Human-made content first; generated media must be labelled on every platform (research II §3, §4.3) | **R21** a provider's real recording beats any generation; the clip engine is the v1 media service; **R20** every generated asset carries a C2PA credential at creation and the platform's label at publish; **R15** never generate a person or a child |
| One anchor a week, cut into many pieces; keywords in text, caption and audio (research II §3) | the social department plans one anchor per neighbourhood × activity per week — Reel, carousel, story, digest item, page update — and `rules/social.md` carries the keyword rule |
| AI answers cite structured, reviewed, current pages (research II §2.1) | a generated page is published only when its readiness (verified fields on every provider, a session, reviews, a last-verified date and answer block) is ≥ 3 of 4 |
| Owned audiences grow product- and community-led (research II §2.1) | the digest is also a public neighbourhood newsletter anyone can join without an account, cross-recommended between neighbourhoods |
| 58 % of replies come from step one, 4–7 touches, warm-up 4–6 weeks, bounce < 2 %, domain reputation is the failure mode (research II §5.1) | three touches 3–4 days apart (invitation → "a family saved you" → reminder) then a call task; a sending domain per instance with warm-up day count, daily cap and bounce limit — the machine will not send past them; replies within one business day |
| Lead scoring orders spend; next-best-action (research III §4) | **R22** a propensity score per provider (e-mail, phone, trial, session, announcement, image, verified fields, unclaimed flag, replied, applied, thread) orders every sequence and the call list, nightly |
| Sell the upgrade at the activation moment; Angi and Yelp report revenue per lead / location (research III §1, §5) | R19 in force: the product cards appear only when delivered value exceeds the cheapest product's annual price; the provider's results carry "your return" |
| Marketplace experiments must be clustered; MMM waits under $1 M spend (research III §3) | the first experiment is a neighbourhood holdout (content on in one neighbourhood, off in a comparable one, four weeks); attribution stays last-touch until then |
| Cohorts, not averages (research III §2) | cohort LTV per acquisition channel shown as *assumption* until 100 observations, then *measured* (R16) |
| Voice agents pay back fastest on inbound, after-hours and follow-ups; Yelp Receptionist at $99 (research II §5.1, III §1) | missed-call text-back stays in v1; voice remains "later" until Twilio and consent (asks #4–5) |

## 9. What the machine never does

Sends without an approval or a preference; answers a family without the provider's approval; texts without consent; sends past the domain's warm-up cap or bounce limit (R23); sends a provider e-mail without the postal address; shows a child's name to a provider (R24); publishes generated media unlabelled; generates a person or a child; exceeds the cap; deletes
a provider's stage history; discounts; publishes a generated page with fewer than three
providers; speaks as an AI to a family or a provider — the product speaks as the platform
or the provider.
