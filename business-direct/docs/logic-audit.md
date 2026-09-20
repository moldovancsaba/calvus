# business.direct — the business-logic audit (history)

*Commissioned by the owner 2026-09-19 ("a deep business logic audit of the system to have
a professional SWOT about the planned service"). Audited: `business-logic.md` (§1–§9),
the SSOT's rules R1–R22 and settings, `economics.md`, the ADRs, and
the prototype's behaviour (`assets/app.js`, rounds 1–6). Method: every rule read against
every other rule, against the prototype, against the real catalogue (253 providers, pulled
2026-09-19), and against the three research rounds. Findings are numbered A1–A18 with a
severity (**critical** = the service does not work or is unlawful as written; **major** =
a wrong number or a missing mechanism the plan depends on; **minor** = a text or model
inconsistency), and each names the fix. Nothing was changed by the audit except two
factual errors in our own documents (A1), corrected in the same commit. The SWOT follows in
§3; the recommendations in §4 are PROPOSED and become D-numbers when the owner decides.*

## 1. Audit summary

| Severity | Count | Findings |
|---|---|---|
| Critical | 2 | A2 (the cap is consumed by the digest alone), A3 (CAN-SPAM footer lacks a postal address) |
| Major | 8 | A4–A11 |
| Minor | 8 | A1, A12–A18 |

**Verdict.** The logic is coherent and unusually complete for a prototype — every outbound
path has a gate, every figure declares its source, the economics model tells the truth
about itself. It has two rules that cannot both hold (A2), one legal footer that must be
fixed before the first send (A3), and a set of dependencies on the platform (audiences,
writes, analytics, prices) that the plan already names but the service cannot ship without.
The thesis is sound and confirmed by the incumbents' own moves (Yelp's Hatch and
Receptionist); the economics only work as the platform's growth engine, not as a standalone
upgrade business at today's catalogue size.

## 2. Findings

### 2.1 Consistency of the rules

| # | Severity | Finding | Evidence | Fix |
|---|---|---|---|---|
| **A1** | minor | Two documents swapped the real counts: 72 providers have a phone and no e-mail, 50 have neither; research II §5.1 and analytics §2.1 said 50 and 72. The economics screen always computed them correctly. | `providers.json`: e-mail 130, phone-only 72, neither 50 | corrected in this commit |
| **A2** | **critical** | **The frequency cap of 4 messages per family per month "across everything — digest, alerts, campaigns, texts", with the weekly digest counting as one, is consumed by the digest alone** (4–5 Sundays a month). As written, no alert, campaign or text can ever be sent to a family with the digest on — the provider campaigns (D22) and the alerts (R3) are dead letters. | business logic §6, SSOT settings, R3 | decide one: (a) the cap counts provider-originated messages only (campaigns, texts) and the platform's own digest and alerts run on preference — 4 provider messages a month is still the research's number; or (b) raise the cap to 8 and count everything. **Recommended: (a)**, which is what the prototype's inbox already shows |
| **A3** | **critical** | The invitation footer reads "Your Field NYC · Brooklyn · unsubscribe". CAN-SPAM requires a **valid physical postal address** in every commercial e-mail; a borough is not one. | research I §8, II §5.1; `app.js` sequence body | put the platform's registered postal address in every provider e-mail template (a merge field `{postal_address}` per `platform_id`); make it a gate check |
| A4 | major | Campaign audiences include "nearby families with a child in the age range", but the family's preference *New provider nearby* defaults **off** and the inbox only shows campaigns from *saved* providers. The audience count sells the provider a reach the preferences would not allow. | business logic §4, `campaignsFor` audience, `family.prefs.nearby = false` | the nearby audience is resolved through the platform's saves **and** the `nearby` preference; the campaign card shows the reachable count, not the nearby population (R11 stated explicitly) |
| A5 | major | A family can ask an **unclaimed** provider a question (Saved → *Ask about a trial* works for any saved provider), but the machine only answers for managing providers. The enquiry vanishes — the worst experience for the family and a wasted signal for sales. | `provider.conversations` locked until managing; `data-ask` on every saved provider | route an enquiry to an unclaimed provider into the **sales sequence's step 2** ("a family asked about you — answer her in one click") and tell the family the provider has been notified; this is the strongest touch the research describes (58 % of replies come from the first relevant message) |
| A6 | major | R9 says stages move forward only on events; the drawer's stage chips let the operator move a provider forward by hand, logged as an override. The two are reconcilable but the rule text is not: "forward on events only" vs "operator moves by hand". | SSOT R9; `data-setstage` | R9 reworded: forward automatically only on events; a person may move any stage in either direction and the move is logged with the reason |
| A7 | major | **R19 gates the upgrade on delivered value > the cheapest product's annual price, but delivered value is computed from sample trials** (`hash(pid) % 4`); with real numbers most providers will sit below the gate for months, and the product cards — the only revenue — never appear. | `provider.today` R19 block; analytics §2.4 | keep R19 as the *pitch* rule but add a floor: after 60 days managing, show the products with the honest line "the machine has delivered $X so far" — the provider can still buy; the number stays truthful |
| A8 | major | The propensity score rewards *unclaimed* +10 and *e-mail* +30, so the first recipients are exactly the providers the platform's enrichment already marked and reached with its own claim prompt. There is no signal for "has not been contacted by the platform before" and no penalty for a bounce or a "not my program". | `score()` | add: −40 after "not my program", −100 after unsubscribe (excluded), −20 after a bounce, +15 when a family saved or asked; take the platform's own claim-prompt history through the connector when keyed |
| A9 | major | The sending guard (warm-up day, daily cap 60, bounce < 2 %) exists as state and a card but **no rule in the SSOT says the outbox refuses a send past it** — R-numbers cover consent and caps for families, not for the sending domain. | `S.sending`; SSOT rules | add **R23**: the outbox refuses any send past the warm-up cap or the bounce limit and alerts; bounce > 2 % pauses the sequence |
| A10 | major | The economics model prices operator time at 2 minutes per approval, but the prototype puts **every** post, sequence, reply, comment, campaign and enquiry through a person. At 5 posts + 3 comments + 130-recipient sequence + replies + campaigns a week, the operator's minutes, not the tooling, are the dominant cost — and the model's cost line understates it. | analytics §2.2; the approvals count reaches 14+ in a session | model approvals as a rate (events × minutes) and show "operator hours this week" as a tile; R1 stays — but batch approvals (approve a whole week's anchor cuts at once) become a product rule |
| A11 | major | The value of an avid family ($42/year to the platform) rests on a 5 % "capture" assumption with no mechanism behind it: upgrades are bought by providers, and nothing in the logic ties a provider's purchase to the families delivered except R19's pitch. | analytics §3.1 | define capture as a measurable: upgrades bought within 30 days of a campaign result or an answered enquiry ÷ all upgrades; log it (`entitlement.started` with the attributed event) |

### 2.2 Legal and trust

| # | Severity | Finding | Evidence | Fix |
|---|---|---|---|---|
| A12 | minor | The SMS consent text is "stored verbatim" by rule, but the prototype's consent record is a provider id list with no text, time or source. | `smsConsent: ['prov-…']`; business logic §6 | the entity in technical design §2 (`consents`) is right; the prototype should show the proof on the preference row ("consented 2026-09-02 on the booking form") so the rule is visible |
| A13 | minor | Children's first names and ages are stored and shown on every enquiry and campaign ("Leo (5)"). Not consent-gated anywhere. New York's Child Data Protection Act (effective 20 June 2025) restricts processing the personal data of users under 18 unless strictly necessary or consented, and COPPA covers data collected from children under 13; the docs do not say which applies to a parent's account describing a child. **P** [NY Attorney General guidance](https://ag.ny.gov/child-data-protection-act-guidance); **A** [Goodwin](https://www.goodwinlaw.com/en/insights/publications/2025/06/alerts-practices-dpc-new-yorks-child-data-protection-act-now-effect) | family entity; enquiry cards | counsel question added to the asks; until answered, the machine uses the child's **age band** in provider-facing text and the name only in the family's own view |
| A14 | minor | AI-content marking is specified for social posts (R20) but the **drafted replies and campaigns sent by e-mail or SMS** carry no disclosure rule; EU AI Act Art. 50 covers text interactions with people in some cases, and the Hungarian reference instance is in the EU. | R20 scope | R20 extended: every AI-drafted message that a person did not edit carries the instance's disclosure line where the market requires it; US: none required today, logged anyway |

| A19 | major (found after the audit, D31) | The platform's own privacy policy (2026-09-12) says it does not knowingly collect children's data and does not yet offer e-mail alerts, and records saves only after an explicit opt-in that is off by default. The machine as designed stored children's names, plans a digest and alerts, and sizes audiences from saves. | `getyourfield.com/privacy`, `/terms` (read with `curl`) | no child's name stored (done); policy revision before the digest launches (ask #16); audiences from opted-in accounts only (ask #17) |

### 2.3 The data and the platform dependency

| # | Severity | Finding | Evidence | Fix |
|---|---|---|---|---|
| A15 | minor | **Reviews are 0 on all 253 cards and prices known on 28** — the two properties AI answers cite most. The generated-page readiness can never reach 4 of 4 today; the "AI-citation" lever (P5) is a platform product problem before it is ours. | `providers.json`; pages screen | ask #12: does the platform plan reviews and price capture? Until then readiness caps at 3 of 4 and the pages carry "no reviews yet" honestly |
| A16 | minor | Six mechanisms depend on the platform's keyed endpoints or data the prototype does not have: claim requests, audiences (saves, location), notifications, card flags for upgrades, sign-up sources, bookings. Each is an ask (#5, #6, #10) — but the plan's Release 1 includes three of them. | plan B1, B7, B9 | Release 1 re-cut into what ships **read-only** (sales sequence, inbox, provider view, content queue, economics on assumptions) and what waits for the key; the presentation says so |
| A17 | minor | The reference instance (Hungary) needs consent for named-person e-mail addresses; the connector interface has no "address is a named person" flag. | research I §8b; `PlatformConnector` | add `contactKind: 'role' \| 'person'` to the connector's provider record; the sequence job skips `person` addresses without consent on EU instances |
| A18 | minor | "Never delete a provider's stage history" (business logic §9) has no store: `provider_state` holds one stage; the history lives in `events`. Fine in production, but the prototype's drawer shows no history. | technical design §2 | the drawer lists the last three `stage.changed` events with who and why |

## 3. The pilot's SWOT

Moved to `first-customer-classscout.md` Part D.

## 4. Recommendations — adopted and implemented as D30 (2026-09-19)

The owner adopted all twelve. Each row's implementation is in the prototype (`app.js?v=9`),
business logic §8d, the SSOT (R3, R9, R11, R19, R20, R22 revised; R23–R25 new), the
technical design and the plan (BD-1-12–14, BD-3-9, BD-4-12–13). Two halves stay with the
platform: A15 (reviews and prices on the cards — ask #12) and A16's keyed endpoints (ask
#5); the postal address itself is ask #15.

| # | Recommendation | Closes |
|---|---|---|
| Q1 | Cap semantics: 4 **provider-originated** messages per family per month; the platform's digest and alerts run on preference | A2 |
| Q2 | Postal address merge field in every provider e-mail; gate check on the template | A3 |
| Q3 | Campaign audience = saved families + families with *nearby* on; the card shows the reachable count | A4 |
| Q4 | An enquiry to an unclaimed provider becomes sales step 2 ("a family asked about you") and the family is told | A5 |
| Q5 | R9 reworded; R19 with a 60-day floor; R23 sending guard; R20 extended to AI-drafted messages | A6, A7, A9, A14 |
| Q6 | Propensity score: bounce, not-my-program, unsubscribe, saves and asks as signals | A8 |
| Q7 | Operator hours as a modelled cost and a tile; batch approvals; earned auto-approval per department after four clean weeks | A10, W3 |
| Q8 | Capture defined as a measurable (upgrades within 30 days of a delivered result) | A11 |
| Q9 | Children's data: age band in provider-facing text; counsel question on NY CDPA / COPPA (ask #13) | A13 |
| Q10 | Release 1 re-cut into read-only and keyed halves; asks #12 (reviews, prices on the platform) and #13 added | A15, A16 |
| Q11 | Connector `contactKind` for EU instances; stage history in the drawer; consent proof on the preference row | A12, A17, A18 |
| Q12 | Strategic: position against Sawyer as "families, not software"; decide bundled vs $99 conversations line in the economics defaults | S1/T1, W1/O4 |

## 5. What the audit changed in the rules (D30)

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
| A13 children's data | R24 age band in provider-facing text; counsel question prerequisite P-4 |
| A14 disclosure on drafted messages | R20 extended: an AI-drafted, unedited answer carries the market's disclosure and is logged |
| A17 EU named addresses | connector `contactKind`; EU instances skip `person` addresses without consent |
| A18 stage history | logged per change; the drawer shows the last three |
| S1/T1 Sawyer | positioning: families, not software — a Sawyer connector is a later adapter, never a competing booking tool |
| W1/O4 the conversations line | an economics input: 0 = bundled (D21), 99 = the incumbent's price; the plan's MRR follows it |

## 6. What the research changed in the rules (D28)

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
| Voice agents pay back fastest on inbound, after-hours and follow-ups; Yelp Receptionist at $99 (research II §5.1, III §1) | missed-call text-back stays in v1; voice remains "later" until Twilio and consent (prerequisites P-11 and P-12) |


