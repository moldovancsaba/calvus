# business.direct — responsible data: the policy record and gate for every customer, and the product's own legal position

*Part A is the framework every customer's site runs under; Part B is the product's own position as
processor and the list of questions for counsel. **Nothing here is legal advice**: every legal
sentence in this document and in the research is the product team's reading, written so counsel
can confirm or correct it. The first customer is ClassScout, operator of Your Field NYC; the
framework is written so that the second, third and any later customer — a sports directory, a
job portal, a classifieds site — gets the same protection by configuration, not by a new
build. The research behind it is `01e-research-responsible-data.md`; the reference
implementation is the platform's *Policy* screen (`../index.html?view=platform&screen=policy`)
and the policy gate in the outbox. The owner's directive: respect children's rights whatever
the client, care for customers' data, use it commercially but properly, and deliver business
value for the client.*

## 1. Principles (the machine's own, for any instance)

| # | Principle | Where it lives |
|---|---|---|
| 1 | **Know who the service is for.** Every instance declares its audience model: adults only, mixed, or child-directed. Nothing else is decided before this. | policy `audienceModel` |
| 2 | **A child is an age, never a name.** Minimum by default: no name, no photo, no location of a child anywhere in the machine; an age or an age band at most, and only where the client's own policy allows it. | R24, policy `childData` |
| 3 | **No profiling or targeting on a minor's data, ever** — not with consent, not with a parent's consent (the California and Oregon bans and DSA Art. 28 are the floor). | R27 |
| 4 | **High-privacy defaults.** Every switch that shares, locates or increases frequency starts off; the family, the candidate, the buyer turns it on. | R28, `family.prefs` |
| 5 | **Consent names the channel and the sender** and is stored verbatim with time and source; preference is enough for the platform's own service messages where the law allows, never for a third party's. | R4, `consents` |
| 6 | **Zero-party over inferred.** The machine acts on what the person told it — saves, asks, preferences — not on what it guesses. | R11, avid definition |
| 7 | **Every commercial message says who sent it, why, and how to stop** — and carries the sender's postal address where the market requires it; opt-outs honoured within one business day. | R2, R23, `postalAddress` |
| 8 | **Disclosure when a machine wrote or made it**, per market's rule. | R20 |
| 9 | **Retention with an end date**, per data class, per instance. | policy `retention` |
| 10 | **The gate is code.** A feature does not run until the policy fields it needs are set; the operator sees what is blocked and why. | R26, the policy gate |
| 11 | **Children in real footage only with written parental consent**, kept with the clip; never a child's name on a clip. | R30, `mediaConsent` |
| 12 | **Safeguarding is shown as verified or not — never claimed.** | R31, `safeguarding` |
| 13 | **No pressure on anyone.** No false urgency or scarcity; "not now" pauses marketing and gets a human; a cooling-off on every purchase. | R32, `vulnerability` |
| 14 | **No protected characteristic, directly or by proxy**, in any audience, slot or score; delivery audited. | R33, `protected` |
| 15 | **Accessible by default** — WCAG 2.2 AA on every message, captions on every clip. | R34, `accessibility` |
| 16 | **Sensitive categories are answered, never stored** — health, location tracks, biometrics, Art. 9, hardship. | R35, `sensitive` |
| 17 | **No dark pattern, no AI manipulation** — a banned list on every draft and screen; Stop is one tap. | R36, `darkPatterns` |

## 2. The policy — one record per instance

```
policy {
  platform_id, client, instance, operator_contact, postal_address,          # identity; the address CAN-SPAM needs
  jurisdictions: ['US-NY', 'US'] | ['HU', 'EU'] | …,                          # the laws in force
  laws: [...derived from jurisdictions],                                       # CAN-SPAM, TCPA, COPPA, NY CDPA, GDPR, DSA 28, Act XLVIII, AI Act 50
  audienceModel: 'adults' | 'mixed' | 'child-directed',                        # principle 1
  ageOfDigitalConsent: 13 | 16 | …,                                            # GDPR Art. 8 per member state; COPPA 13
  childData: 'none' | 'age-band' | 'age' | 'with-parental-consent',           # principle 2
  minorsMarketing: { profiling: false, targetedAds: false, pushQuietHours: [21, 7] },   # principle 3; Nebraska-style hours
  channels: { email: 'preference' | 'consent', push: ..., sms: 'consent', social: 'public' },
  consentText: { sms: '...', email: '...' },                                   # stored verbatim per consent
  defaults: { picks: on/off, alerts: ..., nearby: off, sms: off },            # principle 4
  cap: { providerMessagesPerMonth: 4, countsPlatformDigest: false },
  optOutSlaHours: 24,
  aiDisclosure: 'none' | 'label' | 'label+text',                               # principle 8, per market
  retention: { messages: '24m', consents: 'account+5y', drafts: '90d', events: '24m' },
  privacyPolicy: { url, lastUpdated, clauses: { emailAlerts: bool, savesOptIn: bool, childrenNone: bool } },
  dpia: { done: bool, at? },                                                   # required for a mixed or child-directed instance
  mediaConsent, safeguarding, vulnerability, protected, accessibility, sensitive, darkPatterns   # research V, R30–R36
}
```

## 3. The policy gate (R26) — what runs only when what is set

| Feature | Needs | Blocked otherwise |
|---|---|---|
| Any provider e-mail (sequences, replies) | `postal_address`, opt-out footer, `jurisdictions` | the outbox refuses; the sequence card shows why |
| Family digest and alerts | `privacyPolicy.clauses.emailAlerts = true`, `channels.email` set | the digest job does not run; the family sees "coming when the policy is published" |
| Campaign audiences from saves / nearby | `privacyPolicy.clauses.savesOptIn = true`, the platform's opt-in signal available | audiences are 0; the campaign card says so |
| SMS to families | `channels.sms = 'consent'`, `consentText.sms` | the SMS toggle cannot turn on |
| Generated media, AI-drafted messages | `aiDisclosure` set | generation and unedited AI sends are blocked |
| Any minor's data | `audienceModel`, `childData`, `dpia.done` for mixed / child-directed | the family entity accepts no child field beyond what `childData` allows |
| Push notifications | `minorsMarketing.pushQuietHours` | no push in quiet hours on a mixed instance |
| Clips from a recording that shows children | `mediaConsent` rule · consent confirmed per recording | the clip engine refuses; offers a coach-only or place-only cut (R30) |
| Safeguarding on a card | `safeguarding` rule | shown only as verified; "not verified" is displayed (R31) |
| Any draft or screen | `darkPatterns` list · `accessibility` rule | drafts with a banned pattern refused; inaccessible output refused (R34, R36) |

The gate runs before every send (`sending-guard`), on every draft (`draft-*` jobs) and at
schema level (the family entity). The *Policy* screen lists every field, its state (set /
missing / placeholder) and every feature it blocks.

## 4. Client onboarding — the checklist the screen shows

1. Identity: client, instance, operator contact, **postal address**.
2. Jurisdictions → the laws (derived, shown).
3. Audience model; age of digital consent; child-data rule; DPIA if mixed or child-directed.
4. Channels and their consent basis; consent texts; defaults (all high-privacy).
5. The client's published privacy policy: URL, date, the three clauses the machine needs
   (e-mail alerts described, saves opt-in described, children's data stance).
6. Cap, opt-out SLA, retention, AI disclosure.
7. Beyond children: media consent, safeguarding, vulnerability, protected characteristics, accessibility, sensitive categories, dark patterns (research V).
8. The gate report: what is blocked until which field is set.

## 5. What the client gets (the business value, in their words)

- **Lower exposure**: the enforcement record (research IV §2) is a list of defaults, labels
  and nudges; the gate makes the wrong default impossible to ship.
- **A better audience**: every message goes to a person who saved, asked or opted in —
  zero-party data converts better than inferred data (research IV §4) and needs no profiling.
- **Trust as acquisition**: in a category where half of privacy-aware consumers have
  switched a company over data practices and 83 % of small businesses grow on referrals,
  the trusted platform is the one parents recommend.
- **Auditability**: every send carries its policy basis (which clause, which consent, which
  cap) in the message log; a regulator's question is a query, not a search.
- **Portability**: the second instance is a policy record and a connector, not a rebuild.

## 6. Two instances, one framework (worked examples)

| Field | Your Field NYC (ClassScout) | Most én sportolok! (reference, Hungary) |
|---|---|---|
| jurisdictions | US-NY, US | HU, EU |
| laws | CAN-SPAM, TCPA, COPPA (2025 rule), NY CDPA, EU AI Act 50 where EU users | GDPR (Art. 8 at 16 in Hungary), Act XLVIII/2008, DSA Art. 28, EU AI Act 50 |
| audienceModel | adults (the policy says 18+) | adults (athletes' guardians) — to confirm |
| childData | none — ages only in the family's own preferences | none |
| channels | e-mail preference, push preference, SMS consent, social public | e-mail consent for B2C, role addresses for B2B without consent, no SMS |
| postal address | **missing** (prerequisite P-1) | to obtain |
| privacyPolicy clauses | e-mail alerts **not yet described**; saves opt-in **described (off by default)**; children **none** | to read |
| aiDisclosure | label (platform rules) | label + text (Art. 50) |
| gate today | sequences blocked in production (address); digest blocked (clause); audiences from opted-in accounts only | everything blocked until the policy is filled |

## 7. How the framework generalises

| Client type | What changes | What does not |
|---|---|---|
| Kids' activities (Your Field) | audience adults, child data none, parents consent for SMS | the gate, the cap, the address, the disclosure |
| Sports directory (Sportolok) | athletes may be minors — `audienceModel: mixed`, DPIA, quiet hours, no profiling | same |
| Job portal | candidates' data is sensitive; apprentices 16–18 are minors under some laws; consent for B2C, role addresses for employers | same |
| Classifieds | sellers' addresses and phone numbers are personal data; buyers' locations off by default | same |

The record changes values; the rules and the gate do not.

## Part B — the product's legal position: processor for the media owner, the documents it must have, the counsel list

*Phase D of the transformation programme (`documentation-audit.md` §8). The responsible-data
framework (`responsible-data.md`) governs **the customer's** policy record —
what each media owner's site may send, to whom, under which law. This document is about
**business.direct's own obligations** as the company that operates the product on the owner's
data. **Nothing here is legal advice**: every statement is the product team's reading, written so
that counsel can confirm or correct it; §6 is the list of questions for counsel. Every legal
sentence in `01e`, `01f`, `responsible-data.md` and `business-logic.md` §7 carries the same status. Written 2026-09-20 (D42).*

### 1. The roles (the reading counsel confirms)

| Data | Who decides why and how (controller) | Who processes on instruction (processor) | Notes |
|---|---|---|---|
| Listings and the advertisers' contact details (the site's catalogue) | the media owner | business.direct | business contact data; for EU sites, a named person's e-mail is personal data (Act XLVIII, GDPR) |
| Visitors' accounts, saves, preferences, consents | the media owner (the site holds the account) | business.direct (mirrors preferences and consents, sends on instruction) | visitors never sign in to the product (ADR-6) |
| Messages sent and received through the product | the media owner | business.direct | the message log is the owner's record; the product keeps it for the retention period the owner sets |
| The product's own operational data (events, metrics, the operator's approvals) | business.direct, as necessary to run the service | — | contract; no marketing use across customers |
| The product's telemetry about the owner's users (errors, health) | business.direct | — | minimised; no visitor content in error reports |

In GDPR terms business.direct is a **processor** for the media owner (controller) — or a
sub-processor where the owner is itself a processor for its advertisers; under the CCPA/CPRA a
**service provider**. The first customer's site is US-only with adult users by its own policy
(D31); the framework's children's-data rules apply to any instance where minors may be present.

### 2. The documents the product must have before the first customer contract

| # | Document | What it must say (in outline) | Owner | Status |
|---|---|---|---|---|
| L1 | **Terms of service** (owner ↔ business.direct) | the service (the three jobs as departments with a human gate), the owner's responsibilities (the policy record's truth, the postal address, its own privacy policy, the channels' authority), acceptable use (no purchased lists, no messages to people who did not save, ask or opt in — R11, ADR-10), the human gate as an operating condition, availability, fees and cooling-off, liability caps, termination and data return | counsel drafts on the product team's outline | **to write** |
| L2 | **Data processing agreement** (Art. 28 GDPR-shaped, usable for US customers) | subject matter and duration, nature and purpose, the data categories in §1, the controller's instructions (the policy record *is* the instruction set), confidentiality, security (§4), sub-processors (§3) with notice of change, assistance with data-subject rights (export, deletion via the platform webhook — blueprint §8), breach notification (72 h to the owner), deletion or return at the end, audit rights | counsel | **to write** |
| L3 | **The product's privacy policy** | what business.direct itself collects (the operator's account via SSO, approvals, operational telemetry), the processor role for everything else, the sub-processors, retention, the children's-data stance (§5), contact | counsel | **to write** |
| L4 | **Sub-processor list** (§3) | public page; notice before a change | product team | drafted below |
| L5 | **Security statement** | blueprint §8 in plain words: encryption in transit and at rest, secrets, webhook signatures, idempotency, access scoped per instance, append-only audit collections, backups, incident process, the runbooks | product team | **to write from `architecture.md` §8, §12** |
| L6 | **Retention and deletion schedule** | per data class per instance: messages 24 months, consents account + 5 years, drafts 90 days, events 24 months (framework §2); deletion on the owner's instruction and at the end of the contract | product team | drafted in `responsible-data.md` §2 |
| L7 | **AI-disclosure statement** | which departments may use a model, that every output is marked internally and disclosed to recipients where the instance's law requires (R20, EU AI Act Art. 50 where EU users), that no decision about a person is automated (the human gate) | product team + counsel | **to write** |
| L8 | **Children's-data stance** (§5) | in L3 and in the DPA's data categories | counsel | drafted below |

### 3. Sub-processors (from research VI; every one under a contract with a DPA)

| Sub-processor | Purpose | Data it sees | Region |
|---|---|---|---|
| Vercel | hosting, functions, cron, Blob (media, snapshots) | all application data in transit; media files | US (iad1) |
| MongoDB Atlas | the database | all application data at rest | US-East |
| Upstash | caps, locks, idempotency | ids and counters only | US-East |
| Resend | e-mail out and inbound | recipients, message content | US |
| Meta (Instagram, Facebook) | publishing, comments, DMs | published content, commenters' public handles | Meta's |
| Twilio (when SMS is on) | SMS, missed-call capture | phone numbers, message content | US |
| Stripe | the owner's advertiser payments (on the owner's own account) | none through business.direct beyond the entitlement | — |
| Anthropic (Claude API) | drafting and classification when the department's switch is on | the knowledge files, the listing, the thread being answered — no visitor account data beyond what a message contains | US (the API's data-use terms: no training on API inputs) |
| Deepgram | transcription of uploaded recordings | the audio | US |
| Fly.io | the media worker | the recording and the clips while processing | US (iad) |
| Sentry | errors | stack traces with instance id; no message content | US |
| Better Stack | uptime | none | — |
| DoneIsBetter SSO | the operator's sign-in | operator e-mail and name | the owner's |

Rule: a sub-processor is added only with notice to every customer; a recording that shows
children never leaves the worker without the consent reference (R30).

### 4. Security commitments (what the owner can be promised, from `architecture.md` §8)

Encryption in transit (HTTPS, HSTS) and at rest (Atlas, Blob); secrets in the platform's
encrypted environment; every webhook verified by signature before it is read; idempotency on
every inbound event; access scoped to the operator's instance and to an advertiser's own
records; append-only audit collections (approvals, consents, messages, opt-outs, events); daily
backups at production tier; the incident runbooks in `architecture.md` §12; breach notice to the owner within
72 hours of confirmation.

### 5. The children's-data stance of the product itself

business.direct stores no child's name, image or location on any instance (R24); a child is
an age, and only where the instance's policy record allows the field (`childData`). It never
profiles or targets a minor, with or without consent (R27). It cuts footage that shows a child
only with the operator's confirmation of written parental consent, kept with the clip (R30). For
an instance whose audience may include minors, the policy record requires the audience model and
a DPIA before the family entity accepts any minor's field (R26, framework §3). The product's own
privacy policy says this; the owner's policy record makes it enforceable per site.

### 6. The questions for counsel (one list; every legal sentence in the set depends on it)

1. Is the processor / service-provider reading in §1 right for the first customer (US, adult
   users), and what changes if a later instance has EU users or minors?
2. Which of L1–L8 must exist before the first real message is sent, and which before the
   contract is signed?
3. CAN-SPAM: the postal address in every advertiser e-mail is the **owner's** — confirm; may the
   product's own address be used where the owner has none?
4. TCPA / A2P 10DLC: the consent text stored verbatim per visitor per advertiser (R4) — confirm
   the wording; who is the "sender" for registration, the owner or the product?
5. Children's data (New York Child Data Protection Act, COPPA 2025): a parent's account
   describing a child by age only — confirm no consent flow is needed and the wording of the
   age field (`first-customer-classscout.md` P-4).
6. EU instances: named-person e-mail addresses need consent under Act XLVIII/2008 §6 — confirm;
   the connector's `contactKind` flag is the mechanism (`logic-audit.md` A17).
7. AI disclosure: for the first customer (US), which messages, if any, must carry a disclosure;
   for EU users, the Art. 50 wording.
8. The DPA's breach-notice window and liability cap for a product of this size.
9. Whether the retention schedule in L6 satisfies the owner's own obligations to its users.
10. Whether the product may use aggregated, de-identified metrics across customers for
    benchmarks (today: no, by design).

Until counsel answers, the product runs the pilot on test addresses and the owner's own
accounts only, and every legal sentence in the documentation reads as "the product team's
reading, to be confirmed".

