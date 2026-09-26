# Architecture — the real build (proposed)

*Written 2026-09-25; updated 2026-09-26 for the articles-first launch. The prototype is static HTML
generated in this repository; this is the proposed architecture for gameformative.com in
production. Every stack decision is an ADR in status **PROPOSED** until the owner flips it (the flip
is the next D-number in `04-decisions.md`).*

## Context

```
 content team ──► drafts ──► source + rules check ──► named editor ──► site renderer ──► CDN ──► readers
 (articles)       (template)  (links requested,        (sign-off)      (static pages)          (phone ≈ desktop)
                               800–3,200, segments,                          │
                               both source lists)                            └─► newsletter, social cards
 ─ ─ ─ later phase ─ ─ ─
 data providers ──► ingest ──► stats store ──► data pages, live islands
 (openfootball CC0; licensed event/live feed)
```

The launch is the upper line: an editorial pipeline and a static site. The lower line is the
data-pages phase, kept in the prototype as a preview.

## The target, measured

| Quality | Target | Why | Prototype today |
|---|---|---|---|
| LCP (75th percentile, mobile) | ≤ 2.5 s | Core Web Vitals (register S1) | no images; one font family; under 75 kB of HTML per page |
| INP | ≤ 200 ms | S1 | about 5 kB of script, all event handlers local |
| CLS | ≤ 0.1 | S1; anything that loads late must reserve its space | fixed-height bars and tiles; no ads |
| Time to first byte | ≤ 0.2 s from a CDN | the measured leaders: BBC 0.10 s, sportschau 0.074 s; NBA's 5.1 s is the cautionary case (G4) | static files |
| Accessibility | WCAG 2.2 AA | S2 | contrast gated; 44 px targets measured |
| Article rules | every published article within the house rules | the owner's rules (D18) | asserted by the build, measured by the gate (check 12) |
| Source integrity | every linked source resolved on the day, every used source read | trust is the product (`01-research.md` §10) | done by hand for the first article (`03-sources.md` §3); to automate (issue 0) |
| Data correctness (later phase) | every published table reconciles | a stats page's whole product | converter asserts (R2–R7) |
| Data freshness (later phase, live) | score change on page ≤ 10 s after the provider | a live match centre is only useful live | not built (no feed) |

## Containers

1. **Editorial pipeline** — drafts in the template format; an automatic check of the house rules
   (`check-draft.py` today) and of every source link; the named editor's sign-off recorded with the
   article.
2. **Content store** — articles as structured data (desk, subject, kind, segments, both source
   lists, correction history), versioned; `content.py` is its prototype.
3. **Site renderer** — pre-renders every page; rebuilds on publish and on correction.
4. **CDN / host** — static pages at the edge; purge on publish.
5. **Later phase — ingest and stats store** — pulls openfootball daily and a licensed provider,
   normalises names through the reviewed team table, runs the same asserts as `data/convert.py`,
   refuses to publish a competition that does not reconcile; live islands (score strip, match
   centre) hydrate from a small JSON endpoint.

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

**ADR-04 — Licensed event data from one provider (later phase). PROPOSED, blocked on ask A1.** Options: Opta /
Stats Perform, Sportradar, Genius Sports; or no event data. Without one, xG, ratings and live
scores stay unavailable. Decided on price and terms, which are not public (register I14–I16).

**ADR-05 — Fonts self-hosted. PROPOSED.** The prototype loads Archivo from Google Fonts; production
self-hosts the subset it uses (one request fewer, no third-party request before consent).

**ADR-06 — Consent and analytics minimal by default. PROPOSED.** Options: a full CMP with ad-tech
(the German leaders, DE2–DE5); a privacy-first analytics tool with no personal data and no banner
until ads or a newsletter need consent. See `18-responsible-data.md`.

**ADR-07 — Articles as structured data, not free HTML. PROPOSED.** Options: a general-purpose CMS
with free-form rich text; structured articles (desk, subject, kind, headed segments, two typed source
lists) rendered by templates. The house rules and the source lists are only enforceable on
structure — the prototype's build and gate prove it. A headless CMS can hold the structure; the
choice of product follows the owner's hosting and team decisions.

## Flows

- **Article published** → the editor signs off → the rules and link checks pass → the renderer
  rebuilds the article, its desk and subject pages, the home and latest pages → CDN purge.
- **Correction** → the editor edits the piece → a correction note with the date is appended → the
  corrections page lists it.
- **Later phase — result arrives** → ingest validates → store updates → the data pages rebuild.
