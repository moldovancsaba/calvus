# business.direct — project documentation

**business.direct** is a standalone product for classified media owners — listing platforms,
directories, marketplaces of local businesses — that runs the three jobs their business never
stops needing: **marketing** (content generated from the listings and delivered to every medium),
**B2B sales** (every listed business contacted and acquired as a paying advertiser) and
**retention** (churn seen weeks ahead), with a human gate on everything and the owner's own
economics as a service. Example persona and first buyer: **ClassScout**, operator of **Your Field
NYC**; the prototype runs on their real listings. Sibling of DiscountDirect. This index is also the
process log.

## The set

| Reader | Start here | Then |
|---|---|---|
| **A classified media owner; the stakeholders** | [`presentation.html`](presentation.html) | `executive-summary.md` · `product-definition.md` · `product-specification.md` · `market.md` · `economics.md` |
| **The delivery team** | `business-logic.md` | `architecture.md` · `delivery-plan.md` (sprints, governance, the operating model, the sign-off sheet) · `responsible-data.md` · the design set (`design-system.html`, `layouts.html`, `05-layout-specs.md`, `frames/`) |
| **The first customer** | `first-customer-classscout.md` | the Policy and Economics screens of the prototype |
| **Anyone checking a figure** | `evidence.md` | research I–VI (`01-research.md` … `01g-research-real-system.md`) and `market.md` (VII) |
| **History** | `decisions.md` | `build-log.md` · `gate.md` · `register-of-asks.md` · `logic-audit.md` · `documentation-audit.md` |

| Document | What it holds |
|---|---|
| `presentation.html` | the customer and their week → what they lose → the question → the product → how the owner uses it → the benefits → the first customer → delivery → the decision; the demo as an appendix (`bemutato.html` and every earlier page name redirect here or to their new home) |
| `executive-summary.md` | one page: situation, complication, question, the product, how it is used, the benefits, the proof, the decision |
| `product-definition.md` | the product in the owner's words: the three jobs, the departments, the vocabulary, the persona, ClassScout as example and first buyer, the problem, what is built, what is real |
| `product-specification.md` | how it works and how the customer uses it, screen by screen and role by role; what runs alone, what needs a person; onboarding; what it never does; the benefits, measured |
| `market.md` | the classified-media segment, what owners run and buy, the gap, the product's SWOT |
| `economics.md` | the Economics department: what the product computes for the owner, the funnel and rates, the first customer's worked example, sensitivity; Part B the model, the events, the decision rules |
| `business-logic.md` | the rules R1–R37 end to end; Part B the SSOT: the product layer, glossary, enumerations, entities, settings, the rules register, metrics |
| `architecture.md` | context, quality attributes, containers, the ADRs; Part B the technical design; Part C the system blueprint with pseudo code; the token map as appendix |
| `delivery-plan.md` | milestones, the nine sprints with acceptance tests, the sprint-0 checklist, issues with a Definition of Done, the blocked register, risks with owners and triggers, governance, the operating model, the stakeholder sign-off sheet |
| `responsible-data.md` | the seventeen principles, the policy record per site, the gate, onboarding, the customer's value; Part B the product's processor position, the documents it must have, sub-processors, the counsel list |
| `first-customer-classscout.md` | their site measured, what is real and sample, the onboarding inputs by feature, the pilot's SWOT, the closed asks |
| `evidence.md` | the claims register — every figure with its source opened and its status — and the research base |

Rendered by `build.py` (`python3 business-direct/docs/build.py`); gate `python3 business-direct/check.py`
(also run by the root `check.py`). Data: `python3 business-direct/data/fetch-yourfield.py`
(the first customer's listings) and `fetch-sportolok.py` (the reference connector's data).

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
view moves the persona to *managing*. Measured at 390 and 1440 (`build-log.md`,
`gate.md`); gate clean.

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
inbox with the reason line; `business-logic.md` written; SSOT, architecture (ADR-9
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
ranking, the quarter's funnel, a 12-month plan) and written as `economics.md`
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
`first-customer-classscout.md` in three groups — before the first send, before
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

**2026-09-20 — the hub audit's actions (D36).** The cross-project audit (`../../hub-audit.html`)
was run and the owner approved every action: on this project, two gate checks from the
other gates and the executive summary; on the other four projects, responsible-data policy
records, the stale and consistency checks, asks re-classified, sourced benchmarks, the
missing widths measured, business-logic documents for Holdvölgy and IDBC, and an audit of
DiscountDirect's logic.

**2026-09-20 — the real system (D37).** The owner asked for the next phase: research and a plan
to build the machine for real. Research VI reads every service's own terms on the day (auth,
review, limits, prices, the alternative) and the monthly cost; the system blueprint gives the
drawings, the modules with pseudo code, the contracts, the crons, the outbox, security, the media
worker, the tests and the operations; the architecture's ADRs become the build baseline with
ADR-15–25 for the service choices; the plan is re-cut into nine sprints with an acceptance test
each and a sprint-0 checklist.

**2026-09-20 — the documentation audited and the top of the pyramid rebuilt (D38).** The
owner read the live presentation: a guided tour of screens under a Hungarian filename, for an
English-speaking client whose problem it never quantified. A Big4-standard audit of the whole
set (`documentation-audit.md`: ten criteria, a scorecard, twelve findings with root causes)
found the engineering set sound and the two documents a client opens first failing. Shipped
the same day: `presentation.html` rebuilt as situation → complication → question → answer →
value → proof → responsible by design → delivery → decision, with the demo as an appendix;
`bemutato.html` left as a redirect; the executive summary rewritten in the same shape; a new
business case with three scenarios, sensitivity and break-even; the brief's problem quantified;
the hub row rewritten; the standard's presentation slot corrected (structure, and the filename
in the client's language). Phases 2–4 of the plan (owners and dates, reading paths, gate rows)
follow.

**2026-09-20 — the product, not the customer (D39).** The D38 rewrite still made one customer's
listing count the story. The owner's correction: business.direct is a standalone product — the
one-person sales and marketing team for anybody who is their whole department; ClassScout is
the first paying user. The presentation, executive summary, business case and brief were
rebuilt from the product outward with the first customer as proof; the audit gained F0; the standard gained the product rule.

**2026-09-20 — the deep audit (D40).** The owner opened one page at random and found the
first instance's frame intact ("after the client accepts the prototype"): D38 and D39 were
band-aids. Every file was read and classed by the kind of error; the audit names my own
unverified vendor figures and A-grade hero numbers, the gaps a product needs (its own legal
position, market, business model, operating model, roadmap), and a seven-phase programme with
six decisions that are the owner's. Every rendered page now carries a replacement notice.

**2026-09-20 — the product in the owner's words; retention added (D41).** The owner answered:
a standalone product for classified media owners — content to every medium, B2B sales (contact,
acquire, reduce churn), the owner's economics in the product as a service; ClassScout the persona
example and first buyer; developer costs are not the owner's concern. The product definition,
presentation, executive summary and value document were rewritten accordingly; the product layer
went into the SSOT with the instance mapping; **retention** — the third job, missing until now —
was built into the prototype (screen, recommendations, the churn lever and tile, a sample cohort)
and specified in the rules (R37), the architecture, the design, the blueprint and the plan; the
onboarding file was reframed and the register of asks closed.

**2026-09-20 — the plan to fix all documentation and plans (D43).** Audit §10: the final set of
twelve documents (a product specification new among them), the disposition of every existing
file, ten acceptance criteria per document, six steps in order.

**2026-09-20 — the consolidation executed (D44).** Thirty-three files became the final set: twelve
documents with English names, the prototype, the design set, the research base and the history;
the product specification written; every old URL a redirect; the replacement notice removed; the
gate rewritten for the final set; the product standard recorded at the hub (`PRODUCT.md`).

**Next.** Present to the stakeholders with the sign-off sheet (`delivery-plan.md` §8).
