# business.direct — responsible data and marketing policy framework (for every client)

*Written 2026-09-19 (D32). The first client is ClassScout, operator of Your Field NYC; the
framework is written so that the second, third and any later client — a sports directory, a
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
