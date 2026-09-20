# business.direct — documentation audit and transformation plan

*Written 2026-09-20 on the owner's instruction after reading the live presentation: "the
presentation is about the client's problem, how to solve it and how we help with the solution
we provide — nobody cares about what to push on the UI"; on the URL: no Hungarian word in a URL
for an English-speaking client; and, after the first rewrite still centred on one customer's
listing count: "business.direct is a standalone PRODUCT for anybody who wants a one-man army —
ClassScout is just the first user who will pay for the service". The instruction: a Big4-level
audit of the project's documentation and a plan to transform it from content, meaning and
quality into an executable, result-oriented set. Every finding names the file and the sentence
it rests on. §6 records what shipped with this document (D38, then D39 the same day).*

## 1. Scope, standard and method

**Scope.** The 30 files of `business-direct/docs/` (27 rendered documents, the presentation,
the design system and the layout frames), the project's row on the hub, and the standard the
project followed (`PROTOTYPING.md`).

**Standard applied** — what a consulting deliverable (PwC / Accenture / a bank's strategy team)
is held to:

| # | Criterion | Test |
|---|---|---|
| C1 | **Audience and decision first** | the first screen states who it is for and what decision it supports; the "so what" precedes the "what" |
| C2 | **Client problem before our solution** | the client's situation and its cost are quantified in the client's numbers before any feature is named |
| C3 | **Business case** | investment, return, scenarios, sensitivity, break-even, the cost of doing nothing — with sources and marked assumptions |
| C4 | **Executable** | a reader can act without asking: owners, dates, acceptance criteria, dependencies, a next step |
| C5 | **One fact, one place** | a number or rule is stated once and referenced elsewhere; no drift between documents |
| C6 | **Evidence** | every figure carries its source and the date it was read; every measurement says what tool measured it |
| C7 | **Language and naming** | the client's language throughout — text, filenames, URLs; no internal jargon or foreign words |
| C8 | **Proportion** | the length matches the decision; research and engineering detail sit behind the summary, not in front of it |
| C9 | **Risk and governance** | risks with owners and triggers; who decides what; how the work is reviewed |
| C10 | **Consistency of state** | nothing describes a state that is no longer true |

**Method.** Every document was read in full on the day; each is scored against the ten criteria
(✔ meets · ◐ partly · ✘ fails · — not applicable); the findings are ranked by the harm they do to
the client decision, with a root cause and a fix.

## 2. Scorecard

| Document | Purpose today | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `bemutato.html` (presentation) | a guided tour of the prototype | ✘ | ✘ | ✘ | ◐ | ◐ | ◐ | **✘** | ✘ | ✘ | ✔ | **rebuild** (F1, F2) |
| `15-executive-summary.md` | the argument in prose | ◐ | ◐ | ✘ | ◐ | ✔ | ✔ | ✔ | ✔ | ✘ | ✔ | **rewrite** (F3) |
| `00-brief.md` | client, problem, what is built | ◐ | ◐ | — | ◐ | ✔ | ✔ | ✔ | ✔ | — | ✔ | reframe (F4) |
| `16-analytics-and-unit-economics.md` | the model behind the Economics screen | ✔ | ◐ | ◐ | ✔ | ✔ | ✔ | ✔ | ✔ | — | ✔ | keep; feeds the business case (F5) |
| `17-business-logic-audit-and-swot.md` | audit of the logic; SWOT | ✔ | ◐ | — | ✔ | ✔ | ✔ | ✔ | ✔ | ◐ | ✔ | keep |
| `01`–`01g` research (seven files) | evidence rounds | ◐ | ✔ | — | — | ◐ | ✔ | ✔ | ✘ | — | ✔ | keep behind the summary; one evidence index (F6) |
| `02-audit.md`, `03-sources.md` | the platform measured; real vs sample | ✔ | ✔ | — | ✔ | ✔ | ✔ | ✔ | ✔ | — | ✔ | keep |
| `04-decisions.md`, `06-build-log.md`, `07-gate.md`, `08-client-asks.md` | registers | ✔ | — | — | ✔ | ✔ | ✔ | ✔ | ◐ | — | ✔ | keep (history) |
| `09-business-logic.md`, `10-ssot.md` | rules and terms | ✔ | — | — | ✔ | ✔ | ✔ | ✔ | ◐ | — | ✔ | keep |
| `11`–`14`, `20` engineering set | architecture, design, plan, tokens, blueprint | ✔ | — | ◐ | ✔ | ✔ | ✔ | ✔ | ✔ | ◐ | ✔ | keep; add owners and a governance section (F7) |
| `18-responsible-data-policy-framework.md` | principles, record, gate | ✔ | ◐ | ◐ | ✔ | ✔ | ✔ | ✔ | ✔ | — | ✔ | keep; the client-value section moves up (F8) |
| `19-implementation-prerequisites.md` | what the client provides | ✔ | — | — | ✔ | ✔ | ✔ | ✔ | ✔ | ◐ | ✔ | keep; add dates and owners (F7) |
| `README.md` (docs index) | the index and the process log | ◐ | — | — | ◐ | ✔ | ✔ | ✔ | ✘ | — | ✔ | split the reading paths (F9) |
| hub row (`../../index.html`, `../../README.md`) | one paragraph | ◐ | ✘ | — | — | ✔ | — | ✔ | ✘ | — | ✔ | rewrite to the client's problem (F10) |

## 3. Findings (ranked by harm to the client decision)

| # | Severity | Finding | Evidence | Root cause | Fix |
|---|---|---|---|---|---|
| F0 | **Critical** | **The product is presented as one customer's project, and a data-pull artefact as the problem.** The presentation's first rewrite was titled "A proposal for ClassScout · Your Field NYC", its hero numbers were "0 of 253", "83 sessions", the business case's §1 was "the situation in the client's numbers" and the brief's first heading was "The client". business.direct is a standalone product — the one-person sales and marketing team for anyone who is their whole department; ClassScout is the first paying user, and the 253 providers are the demo's pull, not the customer's situation (their catalogue is far larger) | `presentation.html` (first rewrite), `15` §"The situation", `22` §1, `00-brief.md` §"The client", the hub row | the standard is a *client-prototype* standard ("Stage 0: client, problem"); D11 "Your Field first" was read as "Your Field is the subject"; the catalogue pull, being the only measured thing, became the story | every product-facing document rebuilt from the product outward: the customer segment and its pain → the product → the value and the price → proof (the first customer) → delivery → the decision; ClassScout a section, never the subject; catalogue counts demo facts at most; the standard gains a product-brief rule |
| F1 | **Critical** | **The presentation is a demo script, not a client presentation.** Its second section is titled "What to click, in this order"; five of its eight sections describe screens and buttons; the client's problem appears in one clause of the hero ("markets the businesses to families … drafts everything") and its cost nowhere; there is no business case, no delivery plan, no cost | `bemutato.html` §"What to click, in this order", cards 1–5 ("Click Approve and schedule on a post…") | the standard's presentation slot prescribes "the pages in a recommended order with previews and open buttons" (`PROTOTYPING.md` §4, slot *Presentation*) — a wireframe-review format applied to a service proposal | **rebuild** as `presentation.html`: situation → complication → question → answer; the client's problem in the client's numbers; the cost of doing nothing; the solution in one loop; the business case with scenarios and the honest finding; proof; risk and compliance as mitigation; delivery plan and cost; the one decision; the demo moved to an appendix |
| F2 | **Critical** | **The presentation's URL is a Hungarian word** (`bemutato.html`) for an English-speaking US client | the live URL | the standard names the slot after the Hungarian projects' file | `presentation.html`; `bemutato.html` stays as a redirect (a live URL is never deleted); every link updated; the standard names the file in the client's language |
| F3 | High | **The executive summary argues the thesis, not the client's case.** It opens with "A listing platform has three parties …" (our model), gives evidence about Yelp and Google, and reaches the client in section three; it has no investment, no return, no timeline | `15-executive-summary.md` §"The thesis", §"The evidence" | written as "the argument in prose", not as the page a decision-maker reads | rewrite SCQA: the client's situation and the complication in the first paragraph; the answer; the business case in three numbers; the plan in one line; the decision |
| F4 | High | **The brief describes the problem qualitatively** ("answer late, do not follow up trials") and moves to "the two videos the owner shared" — an internal reference a client cannot use | `00-brief.md` §"The problem" | written for the owner at the start of the project | reframe §"The problem" with the measured numbers (0 of 253 managing; 130 with e-mail; 83 with a next session; 0 reviews; 28 prices) and the sourced cost of each gap; the videos move to §"Where the shape came from" |
| F5 | High | **There is no business case document.** The unit economics exist (`16`) and are honest (LTV : CAC 0.7 at defaults), but nothing states the client's investment, the return by scenario, the break-even and the cost of doing nothing on one page | absence; `16` §2.4 gives the finding and three ways out but no scenario table | economics were built for the machine's decisions, not for the client's | **new `22-business-case.md`**: investment (build effort, run cost from research VI §15, the operator's hours), return by scenario (growth engine · larger catalogue · higher ARPA), sensitivity on the three rates, break-even, the cost of doing nothing; every input marked measured / benchmark / assumption |
| F6 | Medium | **Seven research documents, ~220 KB, with no single evidence index.** A reader who needs "the figure behind X" opens seven files | `01`, `01b`, `01c`, `01e`, `01f`, `01g` and `02` | rounds were added as the owner asked; each is sound on its own | an evidence index at the top of `03-sources.md` (claim → figure → file § → source) in the next phase; the research files unchanged |
| F7 | Medium | **Executable documents lack owners and dates.** The plan names sprints and acceptance tests but no sprint owner or review date; the prerequisites name "who provides" but not "by when"; risks have no trigger or owner | `13` §2b, `19` §1–3, `13` §5 | written before a delivery organisation existed | add an owner column (client · calvus · counsel), target dates relative to acceptance (A+n days), a risk owner and trigger; a governance section: weekly review, decision path, change control |
| F8 | Medium | **Responsible-data framework leads with principles; the client's value is §5.** A client reads seventeen principles before "what you get" | `18` §1 vs §5 | written as a framework for every client | in the presentation and the executive summary the value leads (exposure, audience quality, trust, auditability); the framework keeps its order as the reference |
| F9 | Medium | **The docs index is one 27-row table** for every reader; the client, the delivery team and the owner need three different paths | `README.md` §"Documents" | grew one row per document | split the index: *For the client* (presentation, executive summary, business case, prerequisites) · *For delivery* (SSOT, architecture, design, blueprint, plan, policy framework) · *Evidence and history* (research, audit, sources, decisions, build log, gate, asks) |
| F10 | Medium | **The hub row sells features, not the client's problem** ("B2C social publishing … B2B sales pipeline … optional AI; intelligence dashboard; integrations") | `../../index.html`, `../../README.md` | copied from the brief's "what is built" | one sentence on the client's problem, one on the result, one on the state |
| F11 | Low | **Internal vocabulary leaks into client-facing text**: "gate 1 / gate 2", "D-numbers", "R-numbers", "SSOT", "prototype banner", "inert" | presentation §"What is real"; executive summary §"What is different" ("rules R24–R36") | the engineering set's vocabulary is exact and was reused | client-facing documents use plain words; the numbers stay in the engineering set |
| F12 | Low | **Every document opens with a dated italic paragraph on how it came to be** ("Written 2026-09-19 on the owner's directive …") | every `.md` | the process log's habit, useful for the owner | keep the provenance line but after the purpose sentence: *what this is for, who reads it, what decision it supports*; then the provenance |

What the audit found sound: the engineering set (`10`–`14`, `20`) is complete, consistent and
executable (17 modules with pseudo code, 65 issues with a Definition of Done, 9 sprints with
acceptance tests, every service verified with dates and links); the registers are honest; the
gate keeps the set consistent (decision ranges, issue counts, stale phrases); the economics do
not hide the unfavourable finding. The failure is at the top of the pyramid — the two documents
a client opens first — and in the standard that shaped them.

## 4. Target state — the document set a decision-maker expects

```
                       ┌──────────────────────────────┐
 the client opens ──▶  │ presentation.html             │  20 minutes: problem → answer → value → plan → decision
                       │ 15 executive summary          │  one page, SCQA, the three numbers
                       │ 22 business case              │  investment, return by scenario, break-even, cost of doing nothing
                       │ 19 prerequisites              │  what we need from you, when, why
                       └──────────────┬───────────────┘
 the delivery team ──▶ ┌──────────────┴───────────────┐
                       │ 10 SSOT · 11 architecture · 12 design · 20 blueprint · 13 plan · 18 policy framework · 14 tokens │
                       └──────────────┬───────────────┘
 the evidence ───────▶ ┌──────────────┴───────────────┐
                       │ 03 sources (evidence index) · 01–01g research · 02 audit · 16 economics · 17 audit and SWOT │
                       │ 04 decisions · 06 build log · 07 gate · 08 asks · 21 this audit                             │
                       └──────────────────────────────┘
```

Rules for the top layer: the client's numbers before ours; plain words; every claim sourced by
link to the evidence layer; the honest finding stated, not softened; the decision asked once.

## 5. Transformation plan

| Phase | Deliverable | Acceptance | Status |
|---|---|---|---|
| **1 — the top of the pyramid** | `presentation.html` (SCQA; the demo as an appendix); `bemutato.html` → redirect; `15-executive-summary.md` rewritten; **`22-business-case.md`** new; `00-brief.md` §"The problem" quantified; hub row rewritten; every link updated; the standard's presentation slot rewritten (structure and filename in the client's language) | a reader who opens only the presentation can state the client's problem in numbers, the answer, the return by scenario, the cost, the timeline and the decision; no Hungarian word in any business.direct URL; gate clean | **shipped with this document (D38)** |
| **2 — executable** | owners and target dates (A+n) in `13` §2b and `19`; risk owners and triggers in `13` §5; a governance section (weekly review, decision path, change control) in `13`; the evidence index in `03`; **the product's vocabulary in the SSOT and the business logic** (operator · prospect · audience member as the generic terms; platform · provider · family as the first customer's instance of them) | every sprint, prerequisite and risk has an owner and a date or trigger; every figure in the top layer resolves to one row of the evidence index | next |
| **3 — the reading paths and the voice** | `README.md` split into the three paths; the purpose sentence first in every document; internal vocabulary removed from the top layer | each document's first sentence says what it is for and who reads it; the top layer contains no D-, R-, gate- or SSOT-reference | next |
| **4 — the gate** | `check.py` verifies the top layer: `presentation.html` exists and carries the six sections in order; the executive summary and the business case cite the same three headline numbers; no `bemutato` link remains in business.direct | gate rows added; `GATE: CLEAN` | next |

## 6. What shipped with this document (phase 1 — D38, corrected by D39 the same day)

- `presentation.html` — the **product's** presentation: **The customer** (the one-person army:
  the week they have, the week they get, what they want) → **The complication** (what doing it
  alone costs, sourced; the market sells pieces, not a team) → **The question** → **The
  product** (marketing, sales, conversations; the human gate, the loop, the hands) → **The
  value** (what changes in a week; the pricing hypothesis; the honest finding as the product's
  virtue) → **Proof — the first customer** (ClassScout; the prototype on their real data; what
  it already found for them; built for the second customer) → **Responsible by design** →
  **Delivery** → **The decision**; the demo as a one-paragraph appendix.
- `bemutato.html` — a redirect to `presentation.html` (the URL stays live).
- `15-executive-summary.md` — the product in SCQA; three numbers: the price and margin, the build, the first customer.
- `22-business-case.md` — the product's cost side, the pricing hypothesis, economics by customer count, the customer's case, the first customer's instance as the worked example, sensitivity.
- `00-brief.md` — §"The product", §"The customer", §"The first customer"; §"The problem" is the operator's, with the first customer's measured instance as the example and the pull declared demo data.
- Hub row, docs index, navigation, renderer, gate, standard (stage 0 product rule, stage 7 structure and filename) — updated; links to `bemutato.html` replaced.
