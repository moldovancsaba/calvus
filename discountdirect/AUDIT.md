# DiscountDirect — audit of what exists

*Measured 2026-09-18. The "client" here is the product owner; there is no third-party
client site to audit — the starting point is the prototype itself, the documents, and an
implementation that lives outside this repository.*

## The prototype (`index.html`)

| Measure | Value |
|---|---|
| Form | one HTML file, 74 KB, inline CSS and ~830 lines of vanilla JavaScript, no dependency, no build |
| Screens | seller: Csevegések (3-pane), Villámajánlat, Ajánlatlisták; buyer: Csevegés, E-mail, Postai levél, Hírlevél — seven, switched by tabs, one URL |
| Sample data | one seller (ElektroHome Kft., fictional), 8 buyers, 26 products, multi-year purchase histories, automations — in memory, reset on reload |
| Version | v16 (top-bar note); v15 was the 2026-08-25 build, v16 the 2026-09-18 phone fix |
| Console | 0 errors on every screen |
| Desktop (1024) | 0 px overflow; 3-pane chat becomes one column below 1080 px |
| Phone (375), before 2026-09-18 | 103 px overflow on the chat screen, 10–29 px on the others; 12–17 targets under 44 px per screen |
| Phone (375), after | 0 px overflow; 0 targets under 44 px on every screen |
| Language | Hungarian throughout |

## The documents

Seven markdown sources rendered to HTML by `build-docs.py`, all dated 2026-09-17;
English, written for engineers; `RESEARCH.md` cites 74 sources. No Hungarian
customer-facing material existed before `bemutato.html` (2026-09-18).

## The outside implementation

D26 states the product is extended on an existing Next.js 15 / MongoDB Atlas / Vercel /
DoneIsBetter SSO / Resend implementation. **That code is not in this repository and no
URL for it is recorded here**; the owner marked the stack "verified" on 2026-09-17
(commit `30f4fb7`). Nothing about it was measured for this audit. DD-000 in the
implementation plan is the inventory step that would make it auditable.

## Where the prototype and the decisions diverge

The prototype predates D1–D26 (built 25 Aug, decided 17 Sep). The documents are
authoritative (`SSOT.md` §8); the prototype still shows the earlier behaviour in these
places:

| Behaviour | Prototype (v16) | Decided |
|---|---|---|
| Accepting an offer | accepted in the thread | hand-off to the shop's checkout with the price locked; confirmation written back (D1) |
| Flash sold-out | quantity counter only | both per-campaign and per-buyer limits; sold-out notice with optional compensation (D2, D10, D14) |
| Reason text | engine text only | engine + optional seller edit, both kept (D4) |
| Discount entry | free percentage | `discount_mode` setting with guardrails (D5) |
| Inbox mode | one seller | `inbox_mode` per seller, marketplace possible (D3) |
| Rules block on every message | absent | limits, first-come-first-served, expiry, compensation on every rendering (D14) |
| Predefined rule sets / advanced mode | absent | `OperatingMode {predefined, advanced}` per area (D13) |
| Print mode | letter mock only | seller print mode with PDF and "posted" action (D9, D15) |

Whether the prototype is updated to the decisions or frozen as the pre-decision
reference is `CLIENT-ASKS.md` #1.
