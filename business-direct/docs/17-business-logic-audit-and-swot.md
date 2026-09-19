# business.direct — business logic audit and SWOT

*Commissioned by the owner 2026-09-19 ("a deep business logic audit of the system to have
a professional SWOT about the planned service"). Audited: `09-business-logic.md` (§1–§9),
the SSOT's rules R1–R22 and settings, `16-analytics-and-unit-economics.md`, the ADRs, and
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

## 3. SWOT of the planned service

### Strengths (internal, evidenced)

| # | Strength | Evidence |
|---|---|---|
| S1 | **The thesis is the incumbents' thesis.** Yelp bought exactly this (Hatch, $270 M, lead management + scoring; Receptionist at $99/month) three months before we drew it; Thumbtack sells its supply inside ChatGPT and Claude. | research III §1 |
| S2 | **Human gate on everything, from day one.** Every outbound path passes a person (R1); the outbox is the only sender (ADR-4); consent and caps are checked twice (ADR-3). This is the operating rule the reference videos and the Sprout consumer data both demand, and it is the hardest thing to retrofit. | business logic §3, §9 |
| S3 | **Real data, declared honestly.** 253 real providers, every tile labelled real / sample / benchmark / assumption, the economics screen exposing a 0.7 LTV : CAC rather than hiding it. Owners and clients can trust the numbers because the bad ones are shown. | analytics §2.4, §8 |
| S4 | **Single-player utility for the provider on day one** — conversations, reminders, campaigns, media work before the platform has sent a single family — which the cold-start literature says is the difference between marketplaces that seed supply and those that die on it. | research II §2.2; provider view |
| S5 | **One connector interface, two instances already pulled** (Your Field 253, Sportolok 431). Portability is built, not promised. | ADR-2; `data/` |
| S6 | **The owner owns the platform.** No integration negotiation, no API risk from a third party, family data never leaves the owner's estate. | brief; ADR-11 |
| S7 | **Documentation as a product**: SSOT, business logic, 28 decisions, 22 rules, three research rounds with primary sources, a gate that fails on stale text. A team can be onboarded from the folder. | this docs set |

### Weaknesses (internal, evidenced)

| # | Weakness | Evidence |
|---|---|---|
| W1 | **Unit economics do not close at today's scale.** Outbound to 253 providers on $49 upgrades: LTV : CAC 0.7, payback 31 months. The service is a cost centre for the platform until the catalogue is ~4× larger or ARPA is higher. | analytics §2.4 |
| W2 | **Two rules cannot both hold** (A2) and one legal footer is wrong (A3). Small to fix; unacceptable to ship. | §2 |
| W3 | **The operator is the bottleneck by design.** R1 puts one person in front of every post, reply, campaign and enquiry; the economics model undercounts that cost (A10). | A10 |
| W4 | **Sample where it matters most**: audiences, trials, reply times, families per post, product prices. The screens are convincing and the numbers behind the two revenue levers (campaign reach, upgrade pitch) are invented until the platform's analytics arrive. | analytics §8; A7, A11 |
| W5 | **Thin cards**: 0 reviews, 28 prices, 83 next sessions of 253. The content engine and the AI-citation lever depend on card quality the machine does not control. | A15 |
| W6 | **Six dependencies on keyed platform endpoints** for the core loop (claims, audiences, notifications, flags, sources, bookings). | A16 |
| W7 | **No media production yet** — the clip engine is v1 in the plan, sample in the prototype; the strongest content lever (real footage) is unbuilt. | round 6 |

### Opportunities (external, evidenced)

| # | Opportunity | Evidence |
|---|---|---|
| O1 | **AI answers and social search are replacing Google organic for local discovery** — the platform that is the cited, structured source wins; Yelp took 512,680 citations in a quarter. A curated, verified kids-activities catalogue is exactly the kind of source these engines cite. | research II §2.1 |
| O2 | **Youth-activity spend is up 46 % in five years** ($1,016 per child per sport) and parents choose the programme that shows up in their world (80 % pick the sponsoring brand). Providers can pay because the families do. | research I §3, II §2.1 |
| O3 | **SMBs already use AI for content (81 %) and want referrals (83 %)** — the provider is ready to accept drafts and a referral loop, which is what the machine sells. | research II §3 |
| O4 | **Yelp Receptionist proves a $99/month price point** for "never miss a call" in services; the provider-side conversations department can be a product line, not only a bundled feature. | research III §1 |
| O5 | **Owned audiences are cheap to build** (newsletter growth ~90 % unpaid; ~$1.50 per opt-in via cross-recommendation); the neighbourhood newsletter (P6) is a moat no channel algorithm can take. | research II §2.1 |
| O6 | **Open-source measurement** (Meridian, Robyn) and cheap generation APIs (cents per image) mean the analytics and media layers cost tooling, not licences. | research II §4, III §3 |
| O7 | **The second instance is a configuration** — every reference-idea platform (sport.doneisbetter.com, job portals, classifieds) is the same shape; the connector interface is the product. | ADR-2 |

### Threats (external, evidenced)

| # | Threat | Evidence |
|---|---|---|
| T1 | **The incumbents move first and bigger.** Yelp ($270 M for Hatch), Angi, Thumbtack inside the assistants; **Sawyer** already sells booking, registration and a marketplace to kids'-activity providers — the exact provider the machine courts. A provider with Sawyer's booking tool needs a reason to answer our invitation. | research III §1; **P** [Sawyer for Business](https://www.hisawyer.com/for-business), [Sawyer marketplace](https://www.hisawyer.com/for-business/features/marketplace) |
| T2 | **Deliverability.** 47 % of AI-outbound deployments fail on domain reputation within 90 days; one bad week of sends and the platform's own transactional mail is at risk. | research II §5.1 |
| T3 | **Law is moving under the service**: TCPA damages $500–1,500 per text; EU AI Act Art. 50 live since August 2026 with four different platform label systems; children's-data statutes in New York; CAN-SPAM's address rule (A3). | research I §8, II §4.3; A13 |
| T4 | **Platform rules on AI content** — TikTok cuts reach ~60 % for 30 days after three unlabelled AI videos; Meta labels above the post. A labelling slip costs the channel, not just a post. | research II §4.3 |
| T5 | **Google's enforcement on generated pages** (50–80 % traffic loss for thin programmatic sites) — the generated-pages lever is one algorithm update from a penalty if readiness is not real. | research II §2.1 |
| T6 | **Vendor churn in generation**: Sora died in five months; Higgsfield's pricing could not even be read from its own page. Anything built on one vendor's API is fragile. | research II §4.1 |
| T7 | **The provider is one coach with a phone.** Adoption depends on a claim that costs one click and a tool that works alone; any onboarding friction and the supply side — where two-thirds of marketplaces die — stays unclaimed. | research II §2.2 |

### The cross-reads (what the SWOT says to do)

- **S1 + T1 → position as the platform's own team, not a tool.** Sawyer sells software to the provider; we sell families to the provider and providers to the platform. Never compete on booking software; integrate with it (a Sawyer connector is a later adapter).
- **W1 + O2 + O4 → fix the model, not the pitch.** Price the conversations department for providers at the incumbent's line ($99) *or* keep it bundled and fund the machine as platform growth — decide, and put the decision in the economics defaults.
- **W3 + O3 → batch approvals and trust levels.** A provider who edited nothing for four weeks can have reminders and answers to FAQ questions auto-sent (still logged, still stoppable); R1 becomes "approval or an earned auto-approval per department".
- **W5 + O1 + T5 → card quality is the product.** Reviews and price capture on the platform are the precondition for the citation lever; without them, do not publish generated pages.
- **T2 + A9 → the sending guard is a rule, not a card** (R23).
- **T3 + A2 + A3 + A13 → a legal pass before the first send**: address, cap semantics, children's data, per-market disclosure.

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
