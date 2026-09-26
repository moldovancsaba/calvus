# Implementation plan

*From the approved prototype to gameformative.com. Written 2026-09-25; re-cut 2026-09-26 for the
articles-first launch (the data work moved to M3). Milestones, issues with a
Definition of Done, the blocked register, risks. Dates are set when the owner approves the
direction (ask A0) — none are promised here.*

## Milestones

| # | Milestone | Outcome |
|---|---|---|
| M0 | Direction approved | the owner's and the client's "approved", or changes, on the prototype and style guide (A0) |
| M1 | **Articles launch** | gameformative.com live with the article site: home, latest, the eight desks, subjects, articles under the house rules, How we work; the named editor signing off; the corrections page live. The content team supplies the articles |
| M2 | Growth | newsletter, social cards from the articles' own graphics, search |
| M3 | **Later phase — data pages** | the football statistics pages on a daily open-data refresh, then licensed data (xG, ratings) and live scores |

## Issues

| # | Issue | Milestone | Definition of Done |
|---|---|---|---|
| 0 | Editorial workflow: draft → rules check → link check (every link requested) → named editor's sign-off → publish | M1 | no article publishes without a passing rules check, a recorded link check and the editor's name; the gate's check 12 passes |
| 1 | Deploy the generated site to the host (ADR-01) with the domain | M1 | `https://gameformative.com/` serves the home page; HTTPS; 404 page; curl-verified |
| 2 | Remove the prototype banner and the sample data articles, or replace them with newsroom articles | M1 | no "sample" text on any page; every article bylined to a named person, or the desk with a named editor |
| 3 | Corrections page and error-report form | M1 | a public page listing corrections with dates; the form reaches the editor; linked from every article |
| 4 | Self-host and subset Archivo (ADR-05) | M1 | no third-party font request; LCP unchanged or better |
| 5 | Canonical URLs, sitemap, structured data audit | M1 | valid in Google's Rich Results test for NewsArticle |
| 6 | Covers for every desk (`05-design.md`, next) | M1 | every article has a cover drawn from its own content; no stock or AI imagery |
| 7 | A converter from the draft format to the content store | M1 | a `ready-for-editor` draft that passes `check-draft.py` becomes a page with no hand-copying; the build's rules assert agrees with the checker |
| 8 | Search over articles, desks and subjects | M2 | the header control becomes live |
| 9 | Newsletter (A5) | M2 | double opt-in; sender named; unsubscribe in every mail; `18-responsible-data.md` record filled |
| 10 | Social cards from each article's cover and one key line | M2 | one card per article, alt text included |
| 11 | Data pages on a daily open-data refresh: fetch → convert → build → gate | M3 | runs daily; a failing assert blocks publish; the "data to" date advances |
| 12 | Official tie-breakers per competition (D13) | M3 | each league's published rules applied; tested with constructed level-on-points cases |
| 13 | Provider contract and ingest (ADR-04); xG, shots, ratings panels | M3 | provider data flows in with the same reconciliation asserts; the inert panels filled |
| 14 | Live islands: score strip and match centre | M3 | ≤ 10 s from provider to page; polite atomic announcements; a pause control; reduced motion honoured |

## Blocked register

| Blocked | On | Unblocks |
|---|---|---|
| Issues 0, 2 | A2 — the named editor | M1 |
| Issue 13–14 | A1 — a data provider chosen and contracted | M3 |
| Photo-led formats | A3 | — |
| Ads, paywall, consent design | A4 | the consent part of issue 9 and ADR-06 |
| Issue 9 | A5 | M2 |

## Risks

| Risk | Trigger | Response |
|---|---|---|
| Too few articles at launch for eight desks | a desk empty at launch | empty desks say so plainly already; the content team's plan puts a first article on every desk (`../temp-startup-content/article-plan.md`) |
| The open source lags or stops (later phase) | no new result for 3 days in season | the "data to" date is on every data page; the licensed provider becomes the primary source |
| A provider's terms forbid a use (betting, redistribution) | contract review | the licence check is part of issue 9's DoD; nothing publishes before it |
| Automated text drifts into claims | a template change | templates only state computed facts; every template change passes the gate and an editor's read |
| AI-regulation changes | EU guidance updates | the automation policy is one page; labels are components |
| Performance erodes with ads and live features | CWV at p75 over budget | reserved slots, lazy loading, the budget in `11-architecture.md` as a release check |

## Release scope for M1

The article site as the prototype shows it — home, latest, the eight desks, subjects, articles,
How we work — with the content team's articles, the named editor signing off and the corrections
page live. Not in M1: the data pages, licensed data, live scores, accounts, newsletter, search.
