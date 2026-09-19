# Lexodont — implementation plan

*There is nothing to build: the site is live. This is the plan for a second iteration
if `08-client-asks.md` #1 is answered yes, and the closing steps if it is answered no.
Everything PROPOSED. Written 2026-09-18.*

## If the engagement is complete

- **LX-000** Mark the wireframe "delivered" on the hub card and in the repo README; URLs
  stay live (rule). DoD: hub text changed; both prototypes still return 200.
- **LX-00A** Delete nothing that a page references. `public/` (unreferenced, recorded in `03-sources.md`) was removed on the owner's instruction, 2026-09-19.

## If there is a second iteration

| Issue | What | DoD |
|---|---|---|
| LX-001 | Measure the live site: gate criteria at 390 / 1440 on every page, Lighthouse, booking test HU/EN | numbers in `06-build-log.md` |
| LX-002 | Admin-side inventory: plugins, post types, theme version, hosting, backups, monitoring | table in `11-architecture.md` §2 replaces "not known" |
| LX-003 | GA4 read: top pages, booking-page funnel, EN share | findings in `01-research.md` |
| LX-004 | Decide the dropped and added items (`08` #4, #5) | `04-decisions.md` D15+ |
| LX-005 | Fixes from LX-001 (tap targets, overflow, booking `h1`, self-hosted fonts/icons) | re-measured green |

Order: LX-001 → LX-002/003 in parallel → LX-004 → LX-005. Two to three days of work for
one person, all measurement-led.

## Blocked register

| Item | Blocked on |
|---|---|
| everything | `08-client-asks.md` #1 |
| LX-002, LX-003 | client access |

## Risks

The only real one: presenting the 2026-03 wireframe to the client again as if current —
the live site has moved past it. This folder exists so that cannot happen by accident.
