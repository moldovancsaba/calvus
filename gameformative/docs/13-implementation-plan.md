# Implementation plan

*From the approved prototype to gameformative.com. Written 2026-09-25. Milestones, issues with a
Definition of Done, the blocked register, risks. Dates are set when the owner approves the
direction (ask A0) — none are promised here.*

## Milestones

| # | Milestone | Outcome |
|---|---|---|
| M0 | Direction approved | owner's "approved" or changes on the prototype and style guide (A0) |
| M1 | Static launch on open data | gameformative.com live with the prototype's page set on a daily openfootball refresh; newsroom named; corrections page live |
| M2 | Licensed data | xG, shots, ratings, possession filling the panels the prototype marks unavailable |
| M3 | Live | live score strip and match centre with the accessibility rules of `12-technical-design.md` §5 |
| M4 | Growth | newsletter, social stat cards, the first regional expansion (A6) |

## Issues

| # | Issue | Milestone | Definition of Done |
|---|---|---|---|
| 1 | Deploy the generated site to the host (ADR-01) with the domain | M1 | `https://gameformative.com/` serves the home page; HTTPS; 404 page; curl-verified |
| 2 | Scheduled refresh: fetch → convert → build → gate → publish | M1 | runs daily; a failing assert blocks publish and alerts; the published "data to" date advances |
| 3 | Remove the prototype banner; replace sample copy with newsroom copy | M1 | no "sample" text on any page; every article bylined to a named person or the desk with a named editor |
| 4 | Corrections page and error-report form | M1 | a public page listing corrections with dates; the form sends to the editor; linked from every article |
| 5 | Self-host and subset Archivo (ADR-05) | M1 | no third-party font request; LCP unchanged or better |
| 6 | Search | M1 | teams, competitions and articles searchable; the header control becomes live |
| 7 | Canonical URLs, sitemap, structured data audit | M1 | valid in Google's Rich Results test for NewsArticle and SportsEvent |
| 8 | Official tie-breakers per competition (D13) | M1 | each league's published rules applied; tested with constructed level-on-points cases |
| 9 | Provider contract and ingest (ADR-04) | M2 | provider data flows into the store with the same reconciliation asserts |
| 10 | xG, shots, ratings panels | M2 | the inert panels filled; glossary names the provider's definitions (S25) |
| 11 | Live islands: score strip and match centre | M3 | ≤ 10 s from provider to page; polite atomic announcements; a pause control; reduced motion honoured |
| 12 | Newsletter (A5) | M4 | double opt-in; sender named; unsubscribe in every mail; `18-responsible-data.md` record filled |
| 13 | Social stat cards (vertical and square images generated from the charts) | M4 | one card per analysis, alt text included |
| 14 | First expansion market (A6) | M4 | licensed data for that sport verified; language and navigation reviewed with a native editor |

## Blocked register

| Blocked | On | Unblocks |
|---|---|---|
| Issues 9–11 | A1 — a data provider chosen and contracted | M2, M3 |
| Issue 3 | A2 — a newsroom named | M1 |
| Photo-led formats | A3 | — |
| Ads, paywall, consent design | A4 | the consent part of issue 12 and ADR-06 |
| Issue 12 | A5 | M4 |

## Risks

| Risk | Trigger | Response |
|---|---|---|
| The open source lags or stops | no new result for 3 days in season | the "data to" date is on every page already; M2's provider becomes the primary source |
| A provider's terms forbid a use (betting, redistribution) | contract review | the licence check is part of issue 9's DoD; nothing publishes before it |
| Automated text drifts into claims | a template change | templates only state computed facts; every template change passes the gate and an editor's read |
| AI-regulation changes | EU guidance updates | the automation policy is one page; labels are components |
| Performance erodes with ads and live features | CWV at p75 over budget | reserved slots, lazy loading, the budget in `11-architecture.md` as a release check |

## Release scope for M1

Everything the prototype shows, on the daily open-data refresh, with the newsroom named and the
corrections page live. Not in M1: licensed data, live scores, accounts, newsletter, other sports.
