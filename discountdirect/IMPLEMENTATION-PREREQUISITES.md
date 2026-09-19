# DiscountDirect — implementation prerequisites (after the product owner's go; nothing blocks the presentation)

*Written 2026-09-20 on the owner's rule (business.direct D34, hub audit action 3). The
prototype is the pre-decision reference and is presented as such; the engineering package
is written on D1–D28. These are the items the implementation needs, grouped by when they
block.*

## 1. Before Release 1's first sprint

| # | Prerequisite | Who | Why |
|---|---|---|---|
| P-1 (ask #3) | Access to, or an inventory of, the existing implementation (DD-000) | product owner | the whole plan builds on a codebase this repo cannot see |
| P-2 (ask #9) | Who designs Release 1's undesigned screens (`DESIGN.md` §"never designed") | product owner | before E1 |
| P-3 (ask #6) | Legal review of the consent templates and the legitimate-interest assessment per market (D8, D13) — and the policy record (SSOT §6b) confirmed: unknown age = no profiled offer, the vulnerability pause, the postal address on letters, the seller's policy naming the processor | product owner, counsel | E6; the gate reads the record |
| P-4 (ask #1) | Whether the prototype is updated to D1–D26 or frozen as the pre-decision reference | product owner | the demo and the engineering docs differ on hand-off, sold-out and advanced mode |

## 2. Before Release 1.1

| # | Prerequisite | Who | Why |
|---|---|---|---|
| P-5 (ask #4) | The print partner for the platform print service (Pingen candidate, D9/D15) | product owner | Release 1.1 |
| P-6 (ask #8) | The membership perk list and tier names (D22) | product owner | E8 |
| P-7 (ask #5) | Confirmation of the connector order Shoprenter → UNAS → WooCommerce → Shopify (D18) | product owner | E7 sequencing |

## 3. For the pitch and the brand

| # | Prerequisite | Who | Why |
|---|---|---|---|
| P-8 (ask #2) | Real sample data from one shop (products, a few anonymised histories) | a pilot shop | a pitch on a real catalogue |
| P-9 (ask #7) | A product name and brand for the buyer-facing app, or confirmation that "DiscountDirect" is it | product owner | the wordmark is text |

## 4. What the presentation needs today

Nothing. The prototype is the pre-decision reference; the executive summary and the
engineering package say where they differ.
