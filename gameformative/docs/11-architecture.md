# Architecture — the real build (proposed)

*Written 2026-09-25. The prototype is static HTML generated in this repository; this is the proposed
architecture for gameformative.com in production. Every stack decision is an ADR in status
**PROPOSED** until the owner flips it (the flip is the next D-number in `04-decisions.md`).*

## Context

```
 data providers ──► ingest ──► stats store ──► site renderer ──► CDN ──► readers (phone ≈ desktop)
 (openfootball CC0;            (results,        (static pages +        │
  licensed event/live feed)     tables,          live islands)          └─► newsletter, social cards
                                aggregates)
 newsroom CMS ────────────────────────────────► (articles, labels, corrections)
```

## The target, measured

| Quality | Target | Why | Prototype today |
|---|---|---|---|
| LCP (75th percentile, mobile) | ≤ 2.5 s | Core Web Vitals (register S1) | no images; one font family; under 75 kB of HTML per page |
| INP | ≤ 200 ms | S1 | 6 kB of script, all event handlers local |
| CLS | ≤ 0.1 | S1; tickers and ads must reserve space | strip and tiles have fixed heights; no ads |
| Time to first byte | ≤ 0.2 s from a CDN | the measured leaders: BBC 0.10 s, sportschau 0.074 s; NBA's 5.1 s is the cautionary case (G4) | static files |
| Accessibility | WCAG 2.2 AA | S2 | contrast gated; 44 px targets measured |
| Data freshness (live) | score change on page ≤ 10 s after the provider | a live match centre is only useful live | not built (no feed) |
| Data correctness | every published table reconciles | a stats site's whole product | converter asserts (R2–R7) |

## Containers

1. **Ingest** — pulls openfootball (daily) and the licensed provider (push or poll), normalises
   names through the reviewed team table, runs the same asserts as `data/convert.py`, and refuses to
   publish a competition that does not reconcile.
2. **Stats store** — matches, events, line-ups, and the derived tables and aggregates, versioned by
   input hash (as `stats.json` records its inputs today).
3. **Site renderer** — pre-renders every page that changes only when data changes (tables, reviews,
   articles); live islands (score strip, match centre) hydrate from a small JSON endpoint.
4. **Newsroom CMS** — articles with kind labels, byline, the "how this was made" note, correction
   history; automated round-ups rendered by template from the store, labelled.
5. **CDN / host** — static pages and JSON at the edge; purge on data change.

## Architecture decision records

**ADR-01 — Host on Vercel. PROPOSED.** Options: Vercel; GitHub Pages; Cloudflare Pages; own servers.
The domain's DNS already points at Vercel (`02-audit.md`), which removes a migration; Vercel serves
static and edge functions, which the live islands need. GitHub Pages cannot run the live endpoint.

**ADR-02 — Static-first rendering with live islands. PROPOSED.** Options: a server-rendered app on
every request (NBA.com's Next.js pattern, measured 5.1 s cold first byte, G4); fully client-rendered
(FIFA's empty `#root`, G5, invisible without JavaScript); static pages rebuilt on data change plus
small live components. The third keeps the prototype's measured performance and works without
JavaScript — the prototype is already the static half.

**ADR-03 — Keep the generator language: Python for ingest and rendering. PROPOSED.** Options:
Python (the converter and generator already exist and are gated); a JavaScript framework (Astro,
Next.js). Python keeps `convert.py`'s asserts as the ingest gate unchanged; a framework is worth it
only if the live islands grow into an app. Revisit at M3.

**ADR-04 — Licensed event data from one provider. PROPOSED, blocked on ask A1.** Options: Opta /
Stats Perform, Sportradar, Genius Sports; or no event data. Without one, xG, ratings and live
scores stay unavailable. Decided on price and terms, which are not public (register I14–I16).

**ADR-05 — Fonts self-hosted. PROPOSED.** The prototype loads Archivo from Google Fonts; production
self-hosts the subset it uses (one request fewer, no third-party request before consent).

**ADR-06 — Consent and analytics minimal by default. PROPOSED.** Options: a full CMP with ad-tech
(the German leaders, DE2–DE5); a privacy-first analytics tool with no personal data and no banner
until ads or a newsletter need consent. See `18-responsible-data.md`.

## Flows

- **Result arrives** → ingest validates → store updates → renderer rebuilds that league's pages,
  the home page and the strip → CDN purge. Target: minutes (non-live), seconds for the live islands.
- **Correction** → editor edits the piece → correction note appended with date → corrections page
  lists it.
- **Automated round-up** → round complete in the store → template renders the card → labelled
  Automated, published without edit (the template can only state what the data says).
