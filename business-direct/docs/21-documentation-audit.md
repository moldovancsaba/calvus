# business.direct — the deep audit and the transformation programme

*For the owner. What this document is: the audit of everything written for business.direct —
30 files, 469 KB, the prototype's copy, the hub's rows and the standard the project followed —
against what the product actually is, and the programme that replaces the set rather than
patching it. What went before it: two same-day rewrites of the top layer (D38, D39) that the
owner correctly called band-aids. The root of the damage is one wrong premise carried through
every document from the first commit; the programme starts from the premise, not from the pages.
Written 2026-09-20 (D40). Nothing in this document is executed yet: §7 lists the decisions that
are the owner's, and §8 the phases that follow the go.*

## 1. The premise that was wrong, and how it spread

**What the product is** (the owner's definition, 2026-09-20): a standalone product for
**classified media owners** to manage their businesses — it generates content and delivers it to
different media, and it runs the B2B sales process: contact, acquire, and reduce churn — with the
owner's economics (what a listing costs to advertise, an advertiser's LTV and CAC, the cost to
acquire visitors, all costs and incomes) delivered **in the product as a service**. ClassScout
(Your Field NYC) is the example that makes the persona concrete and the first buyer.

**What the documentation assumed.** From the first commit (`d47e6bd`, 2026-09-19) the brief
opened with "The owner's own product family … Your Field NYC"; D11 the same day made "Your Field
NYC the first client"; from then on every document — brief, research, audit, business logic,
SSOT, economics, SWOT, plan, prerequisites, presentation, hub row — was written as **a project
to market one listing platform's providers to its families**, with the platform's vocabulary
(platform · provider · family), the platform's monetisation (D21: "bundled by the platform,
providers buy reach"), the platform's catalogue as "the situation", and the platform's
competitors (Sawyer) as the threat. The product's own price, market, competitors, go-to-market,
legal position and operating model were never written, because the documents never had a
product as their subject.

**How it happened.** Three perception errors of mine, in sequence: (1) the only thing I could
measure — the catalogue pull — became the story; (2) "first client" was read as "the subject";
(3) the prototyping standard (`PROTOTYPING.md`) is a *client-site* standard (stage 0: "client,
problem"), and I followed it literally for a product. Each later round (research II–VI, the
audit and SWOT, the policy framework, the blueprint) inherited the premise and deepened it; the
gate could not catch it because it checks consistency, not truth.

**Why band-aids cannot fix it.** Nine of the thirty files are built on the premise in their
structure, not in their wording (§3, class A); a further eleven carry it in their vocabulary and
examples (class B); the prototype's roles and copy are the first instance's. Rewriting the top
three pages (D38, D39) left the reader one click from the old frame — the owner found it on the
first random click (`implementation-prerequisites.html`: "after the client accepts the
prototype").

## 2. Method and the standard applied

Every file was read in full on 2026-09-20 (the `.md` sources, the presentation, the two design
pages, `assets/app.js`'s user-facing strings, the hub rows, `PROTOTYPING.md`). Each finding names
the file and the sentence. Findings are classed by *what kind of error* they are — the owner's
words: assumptions, hallucinations, perceptions, misunderstandings — because the fix differs by
class:

| Class | Meaning | Fix |
|---|---|---|
| **A — wrong premise (misunderstanding)** | the document's structure rests on "business.direct = the first customer's project" | rewrite from the product outward, or replace |
| **B — wrong vocabulary and examples (perception)** | the content is right but stated in the first instance's terms, so it reads as instance-specific | generalise the terms; keep the instance as the worked example |
| **C — assumption stated as fact** | a figure or claim that is ours, presented without its status | mark it, source it, or remove it |
| **D — unverified claim (hallucination risk)** | a figure written from memory or from a search summary and labelled as read from the source | open the source and verify, or downgrade the label |
| **E — contradiction or stale state** | two documents disagree, or a document describes a state that is no longer true | one fact, one place |
| **F — gap** | something a product needs that no document holds | write it |
| **G — sprawl** | the same content in several places; length beyond the decision | consolidate |

The standard is the one a consulting deliverable is held to (§2 of the previous version, kept
as C1–C10 in §5): audience and decision first; the customer's problem before our solution; a
business case; executable; one fact, one place; evidence; the customer's language; proportion;
risk and governance; consistency of state — and, added after D39, **the right subject**.

## 3. Findings

### 3.1 Class A — the premise, document by document

| # | File | Evidence | What is wrong | Fix |
|---|---|---|---|---|
| A1 | `19-implementation-prerequisites.md` | title: "after the client accepts; not needed for the presentation"; §1 "before the first real message"; every row "Who provides: ClassScout" | a product's first customer does not "accept a prototype"; they onboard. The document mixes three different things: the **product's own launch prerequisites** (none written — see F-findings), the **first customer's onboarding inputs** (postal address, policy record, key) and **the owner's product decisions** (P-10–P-12 personas, integrations, money) | split into the product launch checklist (new), the first-customer onboarding file (instance) and the owner's decision register; the word "accept" disappears |
| A2 | `08-client-asks.md` | "every item that once needed the owner or the client"; eighteen numbered items | a register of asks to a *client* about a *client project*; for a product these are owner decisions or customer onboarding inputs | close the register into history; owner decisions live in `04`, onboarding inputs in the instance file |
| A3 | `09-business-logic.md` | §1 "The three parties … Platform (Your Field NYC) · Provider · Family"; §5 "the base machine is bundled by the platform … the provider buys reach"; §7 "US (first market)"; §8 "the operator reads one screen: providers contacted…" | the product's rules are written as the first instance's rules: the parties, the money, the market and the recap are the instance's. The product's parties are *operator · prospect / customer · audience member*; the product's money is the subscription; the instance's monetisation is a feature inside it (the operator's own products) | rewrite as the product's business logic with the instance as the worked example in every section; the rules R1–R36 survive with generic wording |
| A4 | `10-ssot.md` | §1 "Client: ClassScout first"; "Platform / instance"; "Provider: the platform's own word"; "Family: the consumer on Your Field"; §2 `role = platform · provider · family`; §3 entities `Provider`, `Family` | the glossary has no product layer; the instance's roles are the enumeration | add the product layer (operator, instance, prospect, customer, audience member, channel, department) and map the first instance's terms to it; entities generic with instance mapping |
| A5 | `16-analytics-and-unit-economics.md` | "The B2B model: providers (the platform's B2B clients)"; "The B2C model: families" | the model is the *operator's* economics (their prospects, their audience) — right as the product's Economics feature, wrong as the product's business case; the product's own CAC / LTV / churn is absent | keep as the feature specification, retitle "the operator's economics — the Economics department"; the product's economics live in `22` |
| A6 | `17-business-logic-audit-and-swot.md` | §3 "SWOT of the planned service": S6 "the owner owns the platform"; T1 "Sawyer already sells booking … to kids'-activity providers"; W1 "unit economics do not close at today's scale (253 providers)" | the SWOT is of the first instance's deployment; the product's competitors (AI marketing-team products, agent platforms, all-in-one SMB suites) are absent; S6 contradicts "ClassScout will pay" | new SWOT of the product; the first-instance SWOT moves to the instance file as "what the pilot faces" |
| A7 | `01-research.md`, `01b`, `01c` | 01 §1 "the listed business that does nothing…", §6 "how listing platforms monetise", §8 "first market: New York", §8b "reference market: Hungary"; 01b §2 "how to find and acquire customers for classified media sites"; 01c §1 "the incumbents in our category" (Yelp, Angi, Thumbtack) | evidence gathered for a listing platform's growth, not for a product sold to operators; the incumbents named are the first customer's category's incumbents. Much of it stays valid *as evidence for what the operator's departments must do* — but there is no research on the product's market (who buys "an AI marketing team", at what price, from whom) | keep as the operator-side evidence base (one consolidated file with an index); add the product-market research (F1) |
| A8 | `04-decisions.md` D21 | "Money: the base machine bundled by the platform; providers buy reach" | defines the first instance's monetisation as "the money model"; the product's price was undecided until D39's hypothesis | D21 re-scoped to "the operator's products feature"; the product's pricing decision is the owner's (§7) |
| A9 | `13-implementation-plan.md` | §4 "Blocked register: … provided by ClassScout after acceptance"; §6 "Release 1a read-only against the platform … the presentation says which half is which" | releases are cut by the first customer's key, not by the product's value; the second-instance milestone proves generality but no *second customer onboarding* is planned | plan rewritten as the product's roadmap (releases by capability) with the first instance's pilot as one track |
| A10 | `assets/app.js`, `index.html` | role switch "Platform · Provider · Family"; HELP `platform/sales`: "every provider through the pipeline"; 21 × "Your Field", 9 × "getyourfield" in copy; `<title>` fixed today | the prototype presents the instance's roles as the product's roles; a second customer would see "Family" for their audience | product copy generalised (Operator · Customer · Audience) with the instance's names shown as labels from the instance record; code identifiers: owner's decision (§7) |
| A11 | `README.md` (docs), hub row, `HUB-AUDIT.md` matrix | docs README's 27-row index and process log narrate a client project; hub audit compares it as one | history stays; the index becomes the product's reading paths (client · delivery · evidence · history) | in the consolidation (§8, phase D) |

### 3.2 Class B — vocabulary and examples

| # | File | Evidence | Fix |
|---|---|---|---|
| B1 | `11-architecture.md`, `12-technical-design.md`, `20-system-blueprint.md` | context drawing "Families … Your Field NYC … Providers"; collections `families_prefs`, `provider_state`; Zod `FamilyPrefs`, `provider_id`; job `digest` "per family" | the engineering is generic in structure (`platform_id` on every record, a policy record per instance, a connector interface) but instance-named in every identifier and drawing. Two options in §7: rename to product terms, or keep and document the mapping |
| B2 | `18-responsible-data-policy-framework.md` | worked examples "Your Field NYC" and "Most én sportolok!"; "the family, the candidate, the buyer" | framework is already for every customer; wording generalised, examples kept |
| B3 | `01e`, `01f` research | "a parent's account describing a child", "the provider" | evidence stands; the rules it becomes are generic |
| B4 | `14-token-map.md`, `05-layout-specs.md`, design pages | "platform 1440 / provider 390 / family 390" | fine as the first instance's frames; label them so |
| B5 | `presentation.html`, `15`, `22` (D39 versions) | product-first now, but §6 "Proof" and the appendix still explain the demo in instance terms without saying "these are the first customer's names for operator · customer · audience" | one sentence of mapping in each |

### 3.3 Class C — assumptions stated as facts

| # | Where | The statement | Status | Fix |
|---|---|---|---|---|
| C1 | `13` §2b, `22` §3, presentation §8 | "two developers, nine sprints, seventeen weeks" | my estimate; never validated against a team, a velocity or the blueprint's 65 issues | label "estimate (unvalidated)"; validate with whoever builds it before it is quoted |
| C2 | `22` §4, presentation §5 | "$249 / $449 a month" | my hypothesis, declared as such — but anchored on two figures of class D (below) | keep as hypothesis; anchors verified first |
| C3 | `16` §2.1, `22` §7 | applied 40 %, managing 80 %, upgraded 25 %, churn 5 %, ARPA $49, avid 15 %, capture 5 %, families per post 1.5, 5 000 families | declared assumptions; but they drive every "finding" quoted in the top layer ("LTV : CAC 0.7", "$610 k") as if they were results | the top layer quotes a *model on assumptions*, never a finding; the phrase "already found" is removed |
| C4 | `00` (original), `17` S6 | "the owner's own product family … Your Field"; "the owner owns the platform" | contradicts "ClassScout is the first paying user"; **ownership of Your Field / ClassScout is not known to me** | owner's answer (§7, Q1); until then no document states who owns the platform |
| C5 | `01g` §12, `11` ADR-5 | "DoneIsBetter SSO — the owner's own identity provider" | assumption from the reference site; whether the product uses it, and for whose users, depends on Q1 | mark; resolve with Q1 |
| C6 | `02` §4, `00` | "the two reference videos show the target shape" — the departments list, "nobody logs in" | owner-supplied input, correctly cited; but the product definition rests on 42 frames I read, not on a written product brief from the owner | the product definition (F2) is written and the owner confirms it |
| C7 | `19` P-10 | personas "Brooklyn Force Soccer", "a Park Slope parent, a child of 5 and a child of 9" | invented for the demo; declared | stays declared demo material in the instance file |
| C8 | `09` §7, `10` §4 | "Hungary (reference): corporate addresses without consent" | legal reading of Act XLVIII §6 by me, not counsel; the same for every legal sentence in `01e`, `01f`, `18` | every legal statement carries "not legal advice; counsel confirms per market" once at the top of the legal file (F5) |

### 3.4 Class D — unverified claims (hallucination risk)

| # | Where | The claim | What actually happened | Fix |
|---|---|---|---|---|
| D1 | `01g` throughout | 22 vendor rows marked **P "read 2026-09-20"** | for most rows I did not open the vendor page; the figures come from search-result summaries or from memory. Known conflict: Twilio 10DLC brand registration was recorded as "$44 brand + $15 vetting" in the search notes and written as "$4 one-time … secondary vetting $40" in the document. Better Stack (10 monitors, 3-minute checks), Sentry (5 000 errors), Fly.io (~$0.007/h), MongoDB M10 (~$57), Stripe Billing 0.7 % are from memory | **re-verify every row by opening the page**; relabel "P" only where the page was read; where a figure cannot be verified, remove the number and keep the vendor and the link |
| D2 | presentation hero, `22` §2, `15` | "62 % of calls to small businesses go unanswered" | source is an aggregator quoting a 2016 study of 85 businesses (research I marks it **A**); it is a hero number on the product's first screen | replace with a **P**-grade figure or drop it from the hero; hero numbers are primary-source only |
| D3 | presentation, `22` | "78 % of customers buy from the business that responds first" | research I cites it via two vendor blogs (**A**), the original source (Lead Connect / Vendasta) not opened | verify or drop from the hero |
| D4 | `11` ADR-12, `17` T6 | "Sora's shutdown in 2026 showed vendors churn"; "Sora died in five months" | I cannot point to the source in the research files that establishes it; `01b` §4 only says "Sora already did" | verify with a primary source or remove |
| D5 | `22` §2, presentation §2 | "the tools stack to $200–400 a month" | my sum of the class-D price points in `01b` §4.1 (Buffer/Later "$29–200", OpusClip, HeyGen, Canva) | recompute from verified prices; state the basket |
| D6 | `01g` §6 | Meta: "100 API-published posts per account per rolling 24 hours"; App Review "two to four weeks" | the limit is from a search summary (plausible, unopened); the review duration is developer folklore | open the Meta page; label the duration "reported, no SLA" (already done) |
| D7 | `01`–`01f` | ~150 figures with links, gathered over five rounds | links exist; I did not re-open them in the audit. The gate checks links resolve, not that the page says what we cite | phase A opens every link cited in the top layer; the rest sampled (20 %) with the result recorded in the claims register |
| D8 | `02` §1 | "public API … found in the site's own JS bundles"; endpoint list | measured with `curl` at the time — verifiable; keep, but it is the first instance's, not the product's |
| D9 | `06-build-log.md`, `07-gate.md` | "measured at 390 / 768 / 1024 / 1440", "no console errors" | measured in the browser pane at the time; recorded honestly; keep |

### 3.5 Class E — contradictions and stale state (found in this reading)

| # | Documents | Contradiction | Fix |
|---|---|---|---|
| E1 | `09` §6 "Default: picks and alerts on"; `10` §4 "weekly picks on, saved-provider alerts on" ↔ R28 (`10` §6, `18` principle 4) "every switch … starts off"; `20` §5 Zod `prefs` all `false` | the family defaults are stated both ways | R28 wins; `09` and `10` §4 corrected; the prototype's family persona re-seeded |
| E2 | `09` §6b "Ten principles" ↔ `18` §1 seventeen principles | count stale since D35 | one sentence in `09` |
| E3 | `17` S7 "28 decisions, 22 rules, three research rounds" | stale (39, 36, six) — a history document quoting live counts | history documents never quote live counts; the gate adds the check |
| E4 | `01g` Twilio figures ↔ the search notes (D1) | two different prices | verify |
| E5 | `22` §7 vs `16` §2.4 | both compute the first instance's economics; `22` says "0.7", `16` says "≈ 0.7 … 1.3 at top decile" — same, but two places | `22` cites `16`, never restates |
| E6 | `13` §2b S2 "with a test policy record" ↔ `19` §1 "the policy record confirmed before the first real message" | the sprint plan sends test e-mails before the record is confirmed; consistent only if "test" means to our own addresses | say so in the plan |
| E7 | README (docs) "27 rendered documents" / hub README "six research rounds" / `21` "30 files" | counts drift with every addition | counts computed by the renderer, not written |
| E8 | `bemutato.html` → redirect; `06` build log and `README` process log still describe it as the presentation | history; acceptable if labelled | the process log entry of D38 says it |

### 3.6 Class F — gaps a product needs (nothing written)

| # | Gap | Why it matters | Where it goes |
|---|---|---|---|
| F1 | **Product-market research**: who buys "an AI sales and marketing team" today (HubSpot Breeze agents, Jasper, Lindy, Relevance AI, ManyChat, Metricool, OpusClip, Hatch/Yelp, agency retainers), at what price, with what churn, through which channels; what they lack (the human gate, the policy gate, the recap) | the product's positioning and price rest on it; today they rest on my hypothesis | new research round VII → the product definition |
| F2 | **Product definition and positioning**: the segment, the jobs, the promise, what it is not, the name of each part in the customer's words | the one document every other document should derive from | new `00` (replaces the brief) |
| F3 | **The product's go-to-market and operating model**: how business.direct acquires operators, onboarding, support, SLA — *the product's own pricing and costs are out of this phase by the owner's instruction* | a product without a channel is a prototype | later phase |
| F4 | **The product's legal position**: business.direct processes the operator's prospect and audience data — it is a **processor** (GDPR) / service provider (CCPA) for the operator; it needs its own terms of service, privacy policy, data-processing agreement, sub-processor list (Vercel, MongoDB, Upstash, Resend, Meta, Twilio, Stripe, Anthropic, Deepgram, Fly), security statement, retention and deletion commitments, and — because the first instance's audience includes parents describing children — the children's-data stance in its own policy, not only the customer's | the responsible-data framework (`18`) governs *the customer's* record; nothing governs *the product's* obligations | new legal file; counsel |
| F5 | **Legal disclaimer and counsel path** for every legal statement in `01e`, `01f`, `18`, `09` §7 | today they read as legal advice | one file, one disclaimer, one list of the questions for counsel |
| F6 | **Operating model**: who runs the product (support, incident response, the runbooks exist in `20` §12), onboarding steps for a customer, the policy-record interview, the knowledge-file workshop, offboarding and data return | the customer buys an operated service, not code | new, short |
| F7 | **Roadmap by capability** (not by the first customer's key): what ships for every operator in R1, R2, R3; what is instance-specific | `13` is a build plan for one instance's pilot | rewritten `13` |
| F8 | **A claims register**: every figure in the top layer with its status (P / A / assumption / hypothesis / owner-stated / unverified) and the date verified | the only defence against class D recurring | new, machine-checked by the gate |
| F9 | **Product standard**: `PROTOTYPING.md` is for client sites; a product needs the stages above (definition, market, price, legal, operating model, roadmap) | the standard caused A-class errors | `PRODUCT.md` or a section |

### 3.7 Class G — sprawl

30 files, 469 KB. The rules are stated in `09`, `10` §6, `18` §1–3 and `20` §4; "what the research
changed" and "what the audit changed" tables repeat in `09` §8c–§8d, `04`, `17` §4 and `01b` §6;
three audits (`17`, `21`, `../../HUB-AUDIT.md`); seven research files with no index; the
process log in `README.md` repeats the decisions. A reader who wants "what is the product and
what does it cost" opens six files. The target set is eleven documents (§6).

## 4. What survives the audit unchanged

The engineering is sound and generic in structure: `platform_id` on every record, one policy
record per instance, the connector and adapter interfaces, the outbox as the only sender, the
policy gate, the seventeen modules with pseudo code, the test plan. The responsible-data
framework and rules R1–R36 are right for every customer once their wording is generic. The
research on what the operator's departments must do (speed to lead, follow-up, content, labels,
children's rights, the law by market) is evidence the product needs. The prototype works and
is measured. The registers (decisions, build log, gate) are honest history. None of this is
thrown away; it is re-homed under the product.

## 5. Scorecard against the standard (after D39; before the programme)

| Document | Subject right? | C1 audience | C2 problem | C3 case | C4 executable | C5 one fact | C6 evidence | C7 language | C8 proportion | C9 governance | C10 state | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `presentation.html` | ✔ (D39) | ✔ | ✔ | ◐ | ◐ | ◐ | ◐ (D2, D3, D5) | ✔ | ✔ | ✘ | ✔ | keep; hero numbers re-sourced; mapping sentence |
| `15-executive-summary.md` | ✔ (D39) | ✔ | ✔ | ◐ | ◐ | ✔ | ◐ | ✔ | ✔ | ✘ | ✔ | keep; C3 clause |
| `22-business-case.md` | ✔ (D39) | ✔ | ✔ | ◐ (hypothesis) | ◐ | ◐ (E5) | ◐ (D5) | ✔ | ✔ | ✘ | ✔ | keep; anchors verified; §7 cites `16` |
| `00-brief.md` | ✔ (D39) | ◐ | ✔ | — | ◐ | ✔ | ✔ | ✔ | ◐ | — | ✔ | replaced by the product definition (F2) |
| `19-implementation-prerequisites.md` | **✘** | ✘ | — | — | ◐ | ✔ | ✔ | ✘ | ✔ | ✘ | ✘ | split (A1) |
| `08-client-asks.md` | **✘** | — | — | — | ✔ | ✔ | ✔ | ✘ | ✔ | — | ✔ | closed into history (A2) |
| `09-business-logic.md` | **✘** | ✔ | — | — | ✔ | ✔ | ✔ | ✘ | ◐ | — | ◐ (E1, E2) | rewritten (A3) |
| `10-ssot.md` | **✘** | ✔ | — | — | ✔ | ✔ | ✔ | ✘ | ◐ | — | ◐ (E1) | product layer added (A4) |
| `16-analytics-and-unit-economics.md` | ◐ (feature, not case) | ✔ | ◐ | ◐ | ✔ | ✔ | ✔ | ◐ | ✔ | — | ✔ | retitled (A5) |
| `17-business-logic-audit-and-swot.md` | **✘** (instance SWOT) | ✔ | ◐ | — | ✔ | ✔ | ✔ | ◐ | ✔ | ◐ | ✘ (E3) | product SWOT new; this one to history (A6) |
| `01`–`01f` research | ◐ (operator-side evidence) | ◐ | ✔ | — | — | ◐ (D7) | ✔ | ✔ | ✘ | — | ✔ | consolidated evidence base (A7, G) |
| `01g-research-real-system.md` | ✔ | ✔ | — | ◐ | ✔ | ✔ | **✘** (D1) | ✔ | ✔ | — | ✔ | every row re-verified |
| `02-audit.md`, `03-sources.md` | ◐ (first instance) | ✔ | ✔ | — | ✔ | ✔ | ✔ | ✔ | ✔ | — | ✔ | moved into the instance file |
| `11`, `12`, `20` | ◐ (B1) | ✔ | — | ◐ | ✔ | ✔ | ✔ | ◐ | ✔ | ◐ | ✔ | merged into one architecture + blueprint; identifiers per §7 Q3 |
| `13-implementation-plan.md` | **✘** (A9) | ✔ | — | — | ◐ | ✔ | ✔ | ◐ | ✔ | ✘ | ◐ (E6) | rewritten as the roadmap + the pilot track |
| `18-responsible-data-policy-framework.md` | ✔ | ✔ | ◐ | ◐ | ✔ | ✔ | ✔ | ◐ | ✔ | — | ✔ | wording generic; joined by the product's own legal file (F4) |
| `04`, `06`, `07` | history | ✔ | — | — | ✔ | ✔ | ✔ | ✔ | ◐ | — | ✔ | keep; no live counts (E3) |
| `README.md` (docs), hub rows | ◐ | ◐ | — | — | ◐ | ✔ | ✔ | ✔ | ✘ | — | ✔ | reading paths (A11) |
| `assets/app.js` copy | **✘** (A10) | — | — | — | — | — | — | ✘ | — | — | ✔ | generalised copy; identifiers per Q3 |

## 6. Target state — the product's document set (eleven documents; every old URL redirects)

```
 the customer / a prospect ─▶  1 presentation.html            the customer's problem → the product → value → price → first customer → decision
                               2 executive summary            one page, SCQA
                               3 product definition           segment, jobs, promise, what it is not, the vocabulary (replaces 00)
                               4 the value                    the economics the product computes for the owner (their listings, advertisers, visitors, churn); the first instance as example
                               5 legal and responsible data   the product's own position (ToS, privacy, DPA, sub-processors) + the customer policy record and gate (18) + the counsel list
 the delivery team ──────────▶  6 business logic and SSOT      one file: the product's rules R1–R36 in product terms, glossary, entities, settings; the first instance's mapping
                               7 architecture and blueprint   one file: 11 + 12 + 20, identifiers per Q3
                               8 roadmap and plan             releases by capability; the pilot track; owners, dates, governance, risks with triggers
                               9 operating model              onboarding, support, incidents, offboarding, the policy interview, the knowledge workshop
 the evidence ───────────────▶ 10 evidence base               01–01g consolidated with an index and the claims register (status per figure)
 the first customer ─────────▶ 11 instance: ClassScout        their platform measured (02), sources (03), onboarding inputs (from 19), the pilot's SWOT, personas — everything instance-specific in one place
 history ────────────────────▶    decisions · build log · gate · this audit · the closed register of asks
```

## 7. The owner's answers (2026-09-20) and what they settled

| # | Question | The owner's answer | Consequence |
|---|---|---|---|
| Q1 | who owns Your Field / ClassScout | *not the question*: ClassScout is an example of the client persona — a classified media owner — and the first buyer/user of the product | the product definition is the classified media owner; ownership is irrelevant to the documents; every "the owner's own product" claim about Your Field is removed |
| Q2 | price and developer rate | *"why on earth should I care about developer costs?"* — and, restated 2026-09-20: **no cost calculation of business.direct itself happens in this phase — not its price, not its build or run cost, not its legal paperwork.** The product's job is to calculate costs and value **for its users, about the users' own services** (their listing price, advertiser LTV and CAC, visitor acquisition cost, churn, all costs and incomes) | the developer rate, build-cost and run-cost lines are deleted from every product-facing document; `22` is the media owner's value with the Economics screen as the product; nothing about the product's own money remains in the set |
| Q3–Q6 | identifiers, definition, consolidation, go-to-market | *no sense* — not the owner's questions | decided here: identifiers stay the first instance's with the mapping in SSOT §1a; the product definition is `00-brief.md` in the owner's words; consolidation proceeds without asking; go-to-market, the product's pricing and its legal paperwork are out of this phase |

The owner's standing instruction: business.direct is built anyway — deliver the product
prototype, the presentation, how it works, how it serves its customers, how the customers use
it, and what benefits they have. Everything below is executed in that order.

### 7a. The original questions (kept for the record)

| # | Question | Why it is yours | What changes with the answer |
|---|---|---|---|
| Q1 | **Who owns Your Field NYC / ClassScout?** The first brief called it "the owner's own product family"; you call ClassScout the first paying user | if it is yours, the first instance is in-house and "customer" is a role you play; if it is a client, the product needs the DPA, the API key negotiation and the data-ownership terms of F4 from day one | the instance file, the legal file, ADR-5 (SSO), the blocked register |
| Q2 | **The price and packaging** (the hypothesis: $249 / $449 / +$149) and **the developer rate** | commercial | the business case stops being a hypothesis |
| Q3 | **Code identifiers**: rename `provider_id` / `family_id` / `platform` to product terms (`prospect`, `audience_member`, `operator`) throughout the blueprint and the prototype, or keep the first instance's names in code with a documented mapping | cost vs clarity: renaming touches the prototype (90 KB of JS), the blueprint's pseudo code and every schema; keeping them means every future customer's developer reads "family" for their audience | the blueprint, the prototype's copy and code, the SSOT's entity table |
| Q4 | **The product definition** (F2): the seven departments as I read them from the videos, the two flows, the human gate — confirm or correct in your words before it becomes the root document | every other document derives from it | everything |
| Q5 | **Consolidation to eleven documents** with redirects from every old URL | thirty files become eleven; history stays | the whole set |
| Q6 | **The product's go-to-market**: does business.direct sell itself through its own machine (its own pipeline of operators), through the calvus network, through partners — or is the first year the first customer only? | the product's CAC, the roadmap's order, the second instance's date | the business case §5, the roadmap |

## 8. The programme (executed from the owner's answers; every phase ends in a gate-clean push)

**Done 2026-09-20 (D42, the same evening):** phase A — the claims register (`23`): 36 figures opened at
their source, seven corrected in the documents (Vercel's limits, Resend's domains, Twilio's fees,
Fly's price, Better Stack's checks, the reminder review's actual finding, the Gen Z figure), two
A-grade hero numbers removed, one unsourced claim (Sora) removed; phase B — research VII (`01h`) and
the product SWOT; phase C — the business logic's headings and parties in product terms; phase D —
the product's legal position and the counsel list (`24`); phase E — risk owners and triggers,
dates relative to the go, the governance section (`13` §5, §5b); phase F — the reading paths on
the index and the evidence pointer in `03` (the eleven-document consolidation with redirects is
the remaining step); phase G — two gate checks (banned framing phrases in the top layer; no
unverified row in the register).

**Done 2026-09-20 (D41), same day as the answers:** the product definition (`00`); the presentation,
executive summary and value document rewritten for the classified media owner; the product layer
in the SSOT (§1a) with the instance mapping; the business logic's parties and the **retention**
job (R37) — the third job the owner named and the documentation had not had; retention built
into the prototype (screen, department, recommendations, the economics lever and tile, product
role labels); the first-customer onboarding file reframed; the register of asks closed; the
economics document retitled as the department's specification; the pilot SWOT labelled; the
architecture, design, blueprint and plan given the retention job and the mapping sentence.
Remaining phases follow.


| Phase | Deliverable | Acceptance | Depends on |
|---|---|---|---|
| **A — truth** | **done** — `23-claims-register.md` | no "unverified" in the top layer; the gate reads the register | — |
| **B — the root** | **done** — the definition (`00`), research VII and the product SWOT (`01h`) | every later document cites the definition | — |
| **C — the rules in product terms** | **done** — SSOT §1a, the business logic's parties, headings and §2c, R37, E1–E2, the prototype's role labels; the instance's words stay inside the sections as the worked example | every rule reads in product terms with the instance as the example | — |
| **D — the product's legal position** | **done** — `24-legal-and-data-processing.md` (roles, L1–L8, sub-processors, security, the children's-data stance, ten questions for counsel); `18` stays the customer's record | counsel has the list | — |
| **E — delivery** | **done in part** — risk owners and triggers, dates relative to the go, reviews, the decision path and change control (`13` §5, §5b); the operating model for onboarding and support (F6) and the architecture + blueprint merge (B1) remain | a developer and a customer-success person can each act from their file | C |
| **F — consolidation** | **done in part** — the reading paths on the index (client · delivery · first instance · evidence · history) and the evidence pointer in `03`; the eleven-document merge with redirects remains | thirty files → eleven + history; no broken or Hungarian URL; the renderer computes every count | A–E |
| **G — the gate and the standard** | **done in part** — two gate checks (banned framing phrases in the top layer; no unverified row in the register); the product standard (F9) remains | `GATE: CLEAN` with the new checks; the standard names the product stages | F |

Order of work: A and B together, then the rest of C, D and E, then F, then G. Until F the live
set carries a banner on every page: *this set is being replaced — the product is defined in
`presentation.html` and `22-business-case.md`; the rest still reads as the first instance's
project*.

## 9. What this audit itself gets wrong if unread

It is written by the person who made the errors, on the same day, without the owner's product
definition in hand. Q4 exists for that reason: the definition in §1 is my reading of the videos
and the owner's messages, and it is the first thing to confirm or correct.

## 10. The plan to fix all documentation and plans (the consolidation programme, D43)

*The audit's finding was one wrong premise spread through thirty-three files. Phases A–G repaired the
content in place; this plan replaces the set. It is the plan the owner asked for on 2026-09-20: what
each existing file becomes, what the final set is, in what order the work runs, and what "done" means
for every page. Out of this phase by the owner's instruction: the product's own price, costs and
legal paperwork, and go-to-market.*

### 10.1 The final set — twelve documents, the prototype, the design set, the evidence, the history

| # | Final document (file) | Reader | What it holds | Built from |
|---|---|---|---|---|
| 1 | **The presentation** `presentation.html` | a classified media owner; the stakeholders | the customer → the complication → the question → the product → how the owner uses it → the benefits → the first customer → delivery → the decision; the demo as an appendix | rewritten D41; final pass for the sign-off shape |
| 2 | **Executive summary** `executive-summary.md` | the stakeholders | one page, SCQA, the decision | `15` |
| 3 | **Product definition** `product-definition.md` | everyone | the product for classified media owners: the three jobs, the departments, the human gate, the loop, the vocabulary (media owner · advertiser · visitor · listing · instance), what it is not, the persona, the first customer as example | `00`, SSOT §1a |
| 4 | **Product specification** `product-specification.md` — *new* | the stakeholders; the delivery team | **how it works and how the customer uses it**, screen by screen and role by role: the owner's day (Home, the inbox, the recap, Economics, Policy, Templates, How to use), the advertiser's team (today, conversations, campaigns, media, results, knowledge), the visitor's side (inbox, saved, preferences, Stop); every state, every approval, what each department does alone and what needs a person; **the benefits per role, measured on the screen**; the prototype as the reference for every screen | the prototype's screens and help texts, `09` §2b–§4b, `05`, the presentation §5–§6 |
| 5 | **The market** `market.md` | the stakeholders | the classified-media segment and how it earns, what owners run and buy today, the gap, the product's SWOT; the first customer's category evidence referenced, not repeated | `01h`; the reusable parts of `01b` §2 and `01c` §1 |
| 6 | **The value — the Economics department** `economics.md` | the stakeholders; the delivery team | what the product computes for the owner about the owner's services (listing price, advertiser CAC and LTV, visitor cost and value, churn and retention, costs, incomes, the next dollar, the plan), the formulas, the inputs and their status, the events, the decision rules R16–R19, the first customer's worked example, sensitivity | `22` + `16` merged |
| 7 | **Business logic and SSOT** `business-logic.md` | the delivery team | the product layer and glossary, enumerations, entities, settings, the rules R1–R37 end to end with the first instance as the worked example, the rules map, what the product never does | `09` + `10` merged |
| 8 | **Architecture and blueprint** `architecture.md` | the delivery team | context, quality attributes, containers, the ADRs (the build baseline), the content model and state machines, connectors and adapters, the module catalogue with pseudo code, data contracts, the cron table, the outbox, security, configuration, the media worker, tests, operations; the token map as an appendix | `11` + `12` + `20` + `14` merged |
| 9 | **Delivery plan and operating model** `delivery-plan.md` | the delivery team; the owner | milestones, the nine sprints with acceptance tests, the sprint-0 checklist, issues with a Definition of Done, owners, dates relative to the go, reviews, decision path, change control, risks with triggers; **the operating model** — onboarding a site (the policy interview, the connector, the knowledge workshop), support, incidents, offboarding and data return; the **stakeholder sign-off sheet** — who accepts what, by which criterion, with the evidence link | `13` + new |
| 10 | **Responsible data and the legal position** `responsible-data.md` | the delivery team; counsel | the seventeen principles, the policy record per site, the gate, onboarding checklist, the customer's value; the product's own position as processor, the documents it must have, sub-processors, security, the children's-data stance, the counsel list — with the one disclaimer at the top | `18` + `24` merged; `01e`, `01f` as evidence |
| 11 | **First customer: ClassScout · Your Field NYC** `first-customer-classscout.md` | the first customer; the delivery team | their site measured, what is real and what is sample, the onboarding inputs by the feature each unblocks, the pilot's SWOT, the personas, the closed asks — everything instance-specific in one place | `02` + `03` + `19` + `17` §3 + `08` |
| 12 | **Evidence** `evidence.md` | anyone checking a figure | the claims register (every figure, source opened, status) and the index to research I–VII | `23` + an index; research `01`–`01h` kept as the evidence base |
| — | **The prototype** `../index.html` | everyone | the reference for every screen; product role labels with the instance's words | v22; a copy pass (product terms first in help texts) |
| — | **The design set** `design-system.html`, `layouts.html`, `05-layout-specs.md`, `frames/` | the delivery team | tokens, components, the approved frames | unchanged; labelled the first instance's frames |
| — | **History** `decisions.md` (D-register), `build-log.md`, `gate.md`, the closed register of asks, this audit | the owner | never edited except to append | `04`, `06`, `07`, `08`, `21` |

Every current rendered URL keeps working: each old page becomes a redirect to its section in the
new set (`bemutato.html` → `presentation.html` is the model). Filenames are English and say what
the document is; numbers go.

### 10.2 What "done" means for every document (the acceptance criteria)

1. The first paragraph says what the document is for, who reads it and what decision it supports.
2. The subject is the product; the first customer appears as the example and is named as such.
3. Product terms first (media owner · advertiser · visitor · listing); the instance's words in brackets or in the worked example only.
4. Every figure has a row in the evidence document with its source opened; none of the product's own price, costs or legal paperwork appears.
5. One fact, one place: a number or rule is stated once and linked elsewhere; counts are computed by the renderer.
6. Internal vocabulary (D-numbers, R-numbers, gate names) stays in the delivery and history documents; the stakeholder documents use plain words with links.
7. Measured at 390 and 1440: no horizontal scroll, one `h1`, 44 px targets, no console errors.
8. The gate is clean: links, anchors, the framing check, the register check, the redirect check, the decision range.
9. A stakeholder can act from the document alone: owners, dates, criteria, a next step.
10. Nothing describes a state that is no longer true.

### 10.3 The order of work

| Step | Deliverable | Why this order | Done when |
|---|---|---|---|
| 1 | **Product specification** (4) and the presentation's final pass (1) | the two things the owner asked for by name — how it works, how customers use it, the benefits — and the pages a stakeholder opens first | every screen of the prototype has its section; the presentation links to it; criteria 1–7 |
| 2 | **Business logic and SSOT** (7), **Economics** (6) | the rules and the numbers everything else cites; the merges remove the duplicated rule statements | one rules register, one glossary, one economics model; criteria 3–6 |
| 3 | **Architecture and blueprint** (8), **Delivery plan and operating model** (9) with the sign-off sheet | the delivery team's two files; the operating model and the sign-off sheet are new | a developer builds from 8 and a customer-success person onboards from 9; the sign-off sheet names every stakeholder |
| 4 | **Responsible data and the legal position** (10), **First customer** (11), **Market** (5), **Evidence** (12) | merges of finished content | every instance-specific sentence lives in 11; every figure in 12 |
| 5 | **Redirects, index, hub, notice, gate, standard** | the cut-over: every old URL redirects, the index is the five reading paths, the hub row and root README name the final set, the replacement notice is removed, the gate checks the final set (redirects, counts, framing, register), `PRODUCT.md` records the product stages so the next product starts right | `GATE: CLEAN`; every old URL answers 200 and lands on its new home; nothing on the site says "being replaced" |
| 6 | **Final review** | every document read once more against §10.2 in a single sitting; the prototype's help texts in product terms; every page measured; the live site checked with curl | a dated entry in the build log with the measurements; D-number closing the programme |

### 10.4 What the plan deliberately leaves out

The product's own price and packaging, its build and run costs, its legal documents' signature, and
its go-to-market — by the owner's instruction, not this phase. The research files stay as evidence
and are not rewritten. The design set is not redesigned.

