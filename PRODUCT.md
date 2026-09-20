# The product standard — what a product needs that a client-site prototype does not

*Added 2026-09-20 after business.direct's audit (`business-direct/docs/documentation-audit.md`):
the prototyping standard (`PROTOTYPING.md`) is written for a client's site — stage 0 is "client,
problem". A product followed it literally and every document became one customer's project. This
page is the standard for a product; `PROTOTYPING.md` still governs the prototype inside it.*

## 1. The premise, written first

The **product** is the subject. Its **customer segment** is named (for business.direct: classified
media owners). A **first customer** is the example that makes the persona concrete and the first
buyer — a section in every document, never the subject. Data pulled from the first customer's site
is demo material and is labelled so; its counts are never "the situation".

## 2. The document set (twelve, in English, named for what they are)

| # | Document | Holds |
|---|---|---|
| 1 | presentation | the customer and their week → the complication → the question → the product → how the customer uses it → the benefits → the first customer as proof → delivery → the decision; the demo as an appendix |
| 2 | executive summary | one page, situation → complication → question → answer, the decision |
| 3 | product definition | the product in the owner's words: the jobs, the departments, the vocabulary, the persona, what it is not |
| 4 | product specification | how it works and how the customer uses it, screen by screen and role by role; what runs alone and what needs a person; the benefits, measured |
| 5 | market | the segment, what customers run and buy today, the gap, the product's SWOT |
| 6 | the value the product computes for its user | the product's own economics feature: what it calculates for the customer about the customer's business — never the product's own price or costs unless the owner opens that phase |
| 7 | business logic and SSOT | the rules end to end; the product layer and the customer instance's mapping; glossary, entities, settings, the rules register |
| 8 | architecture and blueprint | the ADRs, the design, the modules with pseudo code, the tests, operations |
| 9 | delivery plan and operating model | sprints with acceptance tests, owners, dates, governance, risks with triggers; onboarding, support, incidents, offboarding; the stakeholder sign-off sheet |
| 10 | responsible data and the legal position | the policy record and gate per customer; the product's own position as processor; the counsel list with one disclaimer |
| 11 | the first customer | everything instance-specific: their site measured, what is real, onboarding inputs, the pilot's SWOT |
| 12 | evidence | the claims register — every figure with its source opened and its status — and the research base |

Plus the prototype, the design set (`PROTOTYPING.md` stages 3–6) and the history (decisions, build
log, gate, closed registers, audits).

## 3. Acceptance criteria for every document

1. The first paragraph says what the document is for, who reads it and what decision it supports.
2. The subject is the product; the first customer appears as the example and is named as such.
3. Product terms first; the customer instance's words in brackets or in the worked example.
4. Every figure has a row in the evidence register with its source opened; a figure from memory or a search summary is never labelled as read.
5. One fact, one place; counts are computed by the renderer, never written.
6. Internal vocabulary (decision and rule numbers, gate names) stays in the delivery and history documents.
7. Measured at 390 and 1440; one `h1`; 44 px targets; no console errors.
8. The gate is clean, and the gate checks the framing (the customer never the subject; the product's own money never in the set unless that phase is open), the register, the redirects and the set.
9. A stakeholder can act from the document alone.
10. Nothing describes a state that is no longer true; every old URL that was live redirects.

## 4. The rules that came from the audit

- A presentation is about the customer's problem, the product and the value — never a tour of the UI.
- Filenames and URLs are in the customer's language.
- What the product computes for its user (its economics feature) and what the product itself costs are two different things; the second is a separate phase the owner opens.
- Legal paperwork is a phase the owner opens; until then every legal sentence is "the product team's reading, to be confirmed" with the questions listed for counsel.
- Nothing is asked of the owner that is the team's to decide; routine decisions are made and logged.
