# business.direct — project documentation

**business.direct** is a standalone product for classified media owners — listing platforms,
directories, marketplaces of local businesses — that runs the three jobs their business never
stops needing: **marketing** (content generated from the listings and delivered to every medium),
**B2B sales** (every listed business contacted and acquired as a paying advertiser) and
**retention** (churn seen weeks ahead), with a human gate on everything and the owner's own
economics as a service. Example persona and first buyer: **ClassScout**, operator of **Your Field
NYC**; the prototype runs on their real listings. Sibling of DiscountDirect. This index is also the
process log.

## The decision pack

| To decide (about an hour) | In this order |
|---|---|
| What the product is and why it matters to a classified media owner | [`presentation.html`](presentation.html) (20 min) → `executive-summary.md` (5 min) → `product-definition.md` (10 min) |
| What it computes for the owner and how it is used day to day | `economics.md` §1–§4 (10 min) → `product-specification.md` §1–§3 (15 min) |
| Who accepts what, by which criterion | `delivery-plan.md` §8 — the sign-off sheet (5 min); every figure's source: `evidence.md` |

| To build (the hand-over to the delivery team) | Read in this order |
|---|---|
| The rules and the vocabulary | `business-logic.md` (Part B §1a first) |
| The system | `architecture.md` (Part A the decisions, Part C the modules with pseudo code) |
| The work, the governance, the operating model | `delivery-plan.md` (§2b sprints, §3 issues, §5b governance, §7 operating model) |
| What the product must never do, and its legal position | `responsible-data.md` |
| The first instance | `first-customer-classscout.md` (their site, onboarding inputs by feature) |
| The screens | the prototype (`../index.html`) with `product-specification.md` beside it; the design set |

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
| `economics.md` | the Economics department: what the product computes for the owner, the funnel and rates, an illustration on placeholders, sensitivity; Part B the model, the events, the decision rules |
| `business-logic.md` | the rules R1–R37 end to end; Part B the SSOT: the product layer, glossary, enumerations, entities, settings, the rules register, metrics |
| `architecture.md` | context, quality attributes, containers, the ADRs; Part B the technical design; Part C the system blueprint with pseudo code; the token map as appendix |
| `delivery-plan.md` | milestones, the nine sprints with acceptance tests, the sprint-0 checklist, issues with a Definition of Done, the blocked register, risks with owners and triggers, governance, the operating model, the stakeholder sign-off sheet |
| `responsible-data.md` | the seventeen principles, the policy record per site, the gate, onboarding, the customer's value; Part B the product's processor position, the documents it must have, sub-processors, the counsel list |
| `first-customer-classscout.md` | their site measured, what is real and sample, the onboarding inputs by feature, the pilot's SWOT, the closed asks |
| `evidence.md` | the claims register — every figure with its source opened and its status — and the research base |

Rendered by `build.py` (`python3 business-direct/docs/build.py`); gate `python3 business-direct/check.py`
(also run by the root `check.py`). Data: `python3 business-direct/data/fetch-yourfield.py`
(the first customer's listings) and `fetch-sportolok.py` (the reference connector's data).

The process log — every round and decision, dated — is `build-log.md`.
