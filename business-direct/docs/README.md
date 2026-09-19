# business.direct — project documentation

An automated marketing machine for B2B2C listing platforms — the one-person sales and
marketing team for a listed business, run by the platform, with the consumer as the
third role. First client: **ClassScout**, operator of **Your Field NYC** (getyourfield.com);
built for any client, each with its own responsible-data policy record. Sibling of DiscountDirect.
Built to the prototyping standard (`PROTOTYPING.md`); this index is the process log.

| Slot | File | What it holds |
|---|---|---|
| presentation | `bemutato.html` | Standalone, English, on the product's tokens: one sentence, three numbers, five things to click with previews, how the machine decides, responsible by design, what is real, what we ask today (one decision) and what the implementation will need, what comes next |
| 00 brief | `00-brief.md` | Client (ClassScout · Your Field NYC), problem, the three views and the flows, what is real, where it stands |
| 01 research | `01-research.md` | Sourced: reputation and claiming, speed to lead, reminders, digests, generated pages, marketplace monetisation, AI adoption and human-in-the-loop, EU AI Act Art. 50, US CAN-SPAM and TCPA, the Hungarian reference market |
| 01b research II | `01b-research-acquisition-content-sales.md` | Acquiring customers for classified media (demand and supply side), content strategies, the AI creation services (Higgsfield and the video / image / audio / design / scheduling landscape with prices and the labelling rules), the sales processes with benchmarks; P1–P9 (implemented, D28) |
| 01c research III | `01c-research-data-driven-marketing.md` | Case studies and practices behind the data-driven decision flow: Yelp (Receptionist, Hatch, revenue per location), Angi, Thumbtack, Rover; LTV : CAC and payback lines; attribution → incrementality → MMM; Booking.com; next-best-action; P10–P12 (implemented, D28) |
| 01e research IV | `01e-research-responsible-data.md` | Responsible data and children's rights: the law by market (COPPA 2025, NY CDPA, California and the states, GDPR Art. 8, DSA Art. 28, the UK Children's Code), the enforcement record, the frameworks (privacy by design, ICO, ISO 27701, NIST, LEGO), the business value of doing it properly |
| 01f research V | `01f-research-beyond-children.md` | Beyond children: children in real footage, the adults who work with them, people in vulnerable circumstances, protected characteristics, accessibility, sensitive data categories, dark patterns and AI manipulation — the law and the enforcement behind each, the rule it becomes (R30–R36), how it generalises |
| 02 audit | `02-audit.md` | Your Field measured: API, 253 providers, field coverage, site copy, the platform's own policy and terms; the Hungarian reference instance; the two videos frame by frame; what DiscountDirect provides |
| 03 sources | `03-sources.md` | What is real (the platform's public data), what is sample (generated from real cards), what is inherited |
| 04 decisions | `04-decisions.md` | D1–D35 |
| 05 design | `design-system.html` + `../assets/tokens.css` + `../assets/components.css` | **Gate 1 approved (D9)**: tokens and components, one source |
| 05 layouts | `05-layout-specs.md` + `layouts.html` + `frames/` | **Gate 2 approved (D16)**: platform 1440 / 390, provider 390, family 390; the later screens reuse the same grids |
| 06 build log | `06-build-log.md` | Nine rounds: the prototype; presentation and package; editors and tablet; campaigns, upgrades, recap; conversations; economics; the research implemented; the audit implemented; the policy screen; the two interfaces |
| 07 gate | `07-gate.md` + `../check.py` | What the script checks (links, anchors, docs cross-links, data, script, stale phrases); the measured pass at 390, 768, 1024 and 1440 |
| 08 register of asks | `08-client-asks.md` | Every item that once needed the owner, with its state: none open for the presentation; the rest are prerequisites; four closed |
| 09 business logic | `09-business-logic.md` | The rules end to end: parties, the two flows, the two interfaces, departments, campaigns, conversations, money, families, responsible data for every client, law, the recap, data-driven decisions, what the research and the audit changed, what the machine never does |
| 10 SSOT | `10-ssot.md` | glossary, enumerations, entities, settings, rules R1–R36, metrics, document map |
| 11 architecture | `11-architecture.md` | context, the platform measured, quality attributes, containers, flows, integrations, stack and ADR-1–14 — **PROPOSED** (D19) |
| 12 technical design | `12-technical-design.md` | screens, content model, state machines, jobs, connector, media and channel adapter interfaces, drafting, i18n, operations |
| 13 plan | `13-implementation-plan.md` | seven milestones, 65 issues with a Definition of Done, blocked register (the prerequisites), risks, release scope in two halves |
| 14 token map | `14-token-map.md` | tokens and components → GDS + Mantine; contrast computed |
| 16 analytics | `16-analytics-and-unit-economics.md` | CAC / LTV / payback for providers, the marketing value of an avid family, content ROI, the next-dollar rule, the metrics tree, events and attribution, rules R16–R19; what is real vs assumed (D26) |
| 17 audit · SWOT | `17-business-logic-audit-and-swot.md` | Audit of the business logic: 19 findings with fixes; the SWOT with evidence; the recommendations Q1–Q12 (adopted and implemented, D30) |
| 18 policy framework | `18-responsible-data-policy-framework.md` | Seventeen principles, the policy record per instance, the gate (ten rows), onboarding, the client's value, two worked instances, how it generalises (D32, D35) |
| 19 prerequisites | `19-implementation-prerequisites.md` | What the implementation needs from ClassScout after acceptance — before the first send, before Release 1b, to confirm at acceptance — not required for the presentation or the planning (D34) |

Rendered by `build.py` (`python3 business-direct/docs/build.py`); gate `python3 business-direct/check.py`
(also run by the root `check.py`). Data: `python3 business-direct/data/fetch-yourfield.py`
(client) and `fetch-sportolok.py` (reference).

## Process log

**2026-09-19 — stage 0–2.** The owner named the product, chose three views, all four
automations, real platform data and the DiscountDirect family (D1–D5), then widened the
shape with two reference videos: the one-person machine with optional AI, an
intelligence dashboard and integrations (D6). The Hungarian instance was measured and
pulled (431 listings); the videos read from 42 extracted frames; the research written
with its sources. Tokens proposed (D8) and the design-system page built as gate 1.

**2026-09-19 — gate 1 approved (D9).** The owner approved the design system. Components
moved into `assets/components.css` as the single source for the page and the frames.

**2026-09-19 — the first client named (D10–D12).** Everything product- and client-facing
is English; **Your Field NYC** is the first platform; the Hungarian data became the
reference. A second converter pulled Your Field's 252 providers through the public API its
own front end uses (facets, site copy, provider list and full records). The US legal
section joined the research. The "Calvus Hub" link was removed from every user-facing page
in every project. The design-system page was re-issued in English on the client's data,
tokens and components unchanged. Personas fixed on the data (D13).

**2026-09-19 — the two primary flows (D14).** The owner set the front door: B2C social
communication to acquire families, and a B2B sales flow to bring providers to manage their
own listing and more. Two components added for them (D15), reviewed with gate 2.

**2026-09-19 — gate 2 built.** Four frames from the approved components and the real
providers: platform 1440 and 390, provider 390, family 390; the layout specification with
the tablet resolution and the assumptions the open asks force.

**2026-09-19 — gate 2 approved (D16), the prototype built (D17–D18).** "Approved and
Continue." One page, three views (`../index.html`, `assets/app.js`): the platform's nine
screens (overview, social publishing with a week calendar and queue, provider sales with the
pipeline strip, sequences and reply inbox, approvals, providers with chips, search and a
detail drawer, generated pages, integrations, knowledge and rules), the provider's today and
knowledge, the family's inbox, saved and preferences. Every approval moves state: an approved
post lands on the calendar and in the family's inbox; the approved invitation moves 130
providers to *contacted* and three sample replies arrive; "Apply to manage" in the provider
view moves the persona to *managing*. Measured at 390 and 1440 (`06-build-log.md`,
`07-gate.md`); gate clean.

**2026-09-19 — presentation and technical package (D19).** `bemutato.html` in English on
the product's tokens, with the prototype previewed per view (deep links `?view=&screen=`
added to `app.js`). The technical package `10`–`14`: SSOT, architecture with eight PROPOSED
ADRs on DiscountDirect's stack, technical design with the state machines the prototype
already implements, a six-milestone plan with 33 issues and an honest blocked register,
and the token map with computed contrast. The brief's status and `tokens.css`'s header
brought current.

**2026-09-19 — tested, round 2 (D20).** The owner clicked through with no correction. Round
2 made the sequence and reply editors real and measured the tablet widths (768 and 1024)
against the layout specification — both as specified.

**2026-09-19 — consistency pass.** Gate-2 wording that still read "PROPOSED · awaits the
owner" on `layouts.html`, `05-layout-specs.md`, the design-system page's §14 and
`components.css` brought to "approved (D16)". The repo rules (`CLAUDE.md`) now list
business.direct's gate, renderer and converter; the standard notes the deep-link pattern.

**2026-09-19 — phase 2 (D21–D24).** "Continue with the next phase and update all related
documentation." Asks #4–6 assumed (D21) so the phase could ship: provider campaigns and
results, the platform's upgrade products, the intelligence recap, campaigns in the family
inbox with the reason line; `09-business-logic.md` written; SSOT, architecture (ADR-9
Stripe on the platform's account, ADR-10 audiences from the platform's data only),
technical design, plan (M5), token map, layout spec, brief, asks and the presentation
updated. Measured at 390 and 1440.

**2026-09-19 — phase 3 (D25).** Conversations on both sides: the provider's inbox of
family enquiries with answers drafted from its knowledge files, the family's "ask about a
trial" that lands there and comes back answered, comments on published posts with drafted
replies. The provider's "waiting for you" corrected to show enquiries. Business logic §4b,
SSOT, architecture, technical design and plan updated.

**2026-09-19 — consistency pass after rounds 3–4.** Brief, sources, layout spec, token map,
presentation, hub and README brought to the built state; the gate gained a stale-phrase scan
(proved to fire on a planted phrase) so the next round cannot leave such text behind.

**2026-09-19 — research II.** The owner asked for research on what the market says about
acquiring customers for classified media sites, content strategies, the AI content-creation
services to add (Higgsfield and the rest), and the sales processes. Written with 60+ linked
sources, primary marked; Sora's shutdown, the four platforms' AI-label rules and the cold
e-mail benchmarks change what the plan should assume. Nine proposals (P1–P9) wait for the
owner; each becomes a D-number.

**2026-09-19 — economics (D26).** The owner asked for ROI, CAC and LTV planning for the B2B
clients, the marketing value of avid users and the analytics that let the system decide.
Built as the platform's *Economics* screen (23 editable inputs, eight tiles, the next-dollar
ranking, the quarter's funnel, a 12-month plan) and written as `16-analytics-and-unit-economics.md`
(the model, the metrics tree, the events to log, attribution, R16–R19). The defaults expose
the first real finding: outbound alone does not pay for $49 upgrades on 252 providers.

**2026-09-19 — research III and the decision flow in the presentation.** The owner asked
for the industry's best case studies and practices as the source of the data-driven
services. Written with primary filings and releases (Yelp's Q4 2025 letter, the Hatch
acquisition, Yelp Receptionist pricing, Angi's 10-K, a16z's metrics, HBR on Booking.com,
Airbnb's cluster-randomised experiments, Google Meridian); each finding mapped to a
business.direct service; P10–P12 added. The presentation gained the decision flow —
events → metrics → next dollar → approval → measure — as its own section.

**2026-09-19 — the research implemented (D28).** "Implement the results of the research
into our business logics and prototyping." Media department with the clip engine as v1 and
generation later, real/generated labels with C2PA, the weekly anchor plan, AI-citation
readiness per page, the public neighbourhood newsletter, sending infrastructure and the
three-touch sequence ordered by a propensity score, the upgrade card gated by delivered
value, a neighbourhood holdout running, cohorts by channel — in the prototype and in
business logic §8c, the SSOT (R15, R20–R22), the architecture (ADR-12, ADR-13), the
technical design, the plan and the presentation. Asks #9 and #11 closed.

**2026-09-19 — business logic audit and SWOT (D29).** Every rule read against every other
rule, the prototype, the catalogue and the research. Two critical findings — the family cap
as written is consumed by the weekly digest alone, and the invitation footer lacks the
postal address CAN-SPAM requires — eight major (nearby audiences vs the *nearby*
preference, enquiries to unclaimed providers lost, R9 wording, R19 on sample trials, the
score's missing negative signals, no sending-guard rule, operator time undercounted,
capture undefined), eight minor. The SWOT names Sawyer as the direct threat on the
provider side and the incumbents' own moves as the confirmation of the thesis. Q1–Q12
PROPOSED; asks #12–14.

**2026-09-19 — the audit implemented (D30).** All twelve recommendations in the prototype
and the documents: cap semantics, the postal-address gate, reachable audiences, the
unclaimed provider's ask as a sales touch, R9/R19/R20 revised and R23–R25 new, the score's
negative signals, operator hours and batch and earned approvals, capture measured, age
bands for children, stage history, consent proof, the conversations line as a pricing
input, Release 1 re-cut into read-only and keyed halves, positioning against Sawyer.

**2026-09-19 — the platform's own policy read (D31).** Asked to proceed on the open asks, the
platform's privacy policy and terms were read from its site: adults only and no children's
data (the machine now stores no child's name — ages only), no e-mail alerts yet (policy
revision before the digest, ask #16), saves recorded only after an opt-in that is off by
default (audiences from opted-in accounts, ask #17), claims an existing feature, no postal
address published (ask #15 stays open). Audit A19 recorded.

**2026-09-19 — responsible data for every client (D32).** The owner's directive: the first
client is ClassScout, the system must serve any client, and children's rights are respected
whatever the client. Research IV read the law by market, the enforcement record, the
regulators' and LEGO's frameworks, and the evidence that responsible practice pays. The
framework: ten principles, one policy record per instance, a gate in the outbox and the
jobs (R26–R28, ADR-14). Built as the platform's *Policy* screen with two instances (Your
Field NYC / ClassScout and the Hungarian reference) — the gate today blocks provider e-mail
(no postal address) and the digest (policy clause), and the sample invitation stops at the
gate once and explains. Client naming corrected throughout.

**2026-09-19 — two interfaces (D33).** Simple: Home with ranked recommendations, the reason
behind each, one button each, and "Do the recommended actions" for the safe ones; a reduced
navigation. Advanced: everything. A What-is-this panel on every screen, a How-to-use screen,
and Templates that copy sequences, knowledge files and policy records for other client
types into the machine. Simple is the default; `?mode=advanced` opens the other.

**2026-09-19 — asks re-classified (D34).** The owner: the open items are tasks for the day
the client accepts, not for the presentation or the planning. They now live in
`19-implementation-prerequisites.md` in three groups — before the first send, before
Release 1b, to confirm at acceptance — and the register records that nothing is open for
the presentation. The presentation's asks section now reads "What we ask of you today: one
decision — go ahead", followed by what the implementation will need.

**2026-09-19 — consistency sweep.** The owner found inconsistent and deprecated statements.
Fixed: the brief's status (stopped at phase 3), the SSOT's cap definition and document map
(D1–D18), the digest's cap wording in the architecture, the technical design and the plan,
the index's plan count (40 → 62 issues) and ADR range (10 → 14), the presentation's round
count, children's names in the gate-2 frames and the design-system sample, the root README
and hub summaries, and every "ask #n" reference outside the register — now the
prerequisite code. The gate gained a consistency check (decision range, issue count, ask
references) and was proved to fire on planted drift.

**2026-09-19 — business logic and system consistency.** Checked rule by rule and setting by
setting against the prototype: the provider's *apply* skipped the *applied* stage the
business logic and the state machine describe (fixed: applied by the provider, managing by
the platform, both in the history); the SSOT's opt-out setting said ten business days while
the policy says one; its campaign-audience setting predated Q3; family defaults were not a
setting; the Draft entity lacked `media`, and AutoApproval and Recommendation were not
entities. The business logic gained a rules map (§8e) and the gate a check that every SSOT
rule is stated there.

**2026-09-19 — beyond children (D35).** The owner asked what other cases a responsible
business must cover. Research V found seven — two of them gaps in our own category: real
footage of children (the clip engine now refuses a recording that shows children until the
provider confirms written parental consent) and the adults who coach them (safeguarding
shown only as verified). Plus people in vulnerable circumstances, protected characteristics
in targeting, accessibility, sensitive data categories, dark patterns and AI manipulation —
rules R30–R36, seven policy fields, three gate rows, the Policy screen's seventh card.

**Next.** Present. After acceptance, the prerequisites checklist.
