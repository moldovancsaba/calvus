# System blueprint — the low-level technical design

*The document a developer builds gameformative.com from. Written 2026-09-26 after the client's review
("please update all documentation … to be able to pass to the developers including architecture
plan, low level technical design with pseudo codes"). It is stack-neutral: the modules, contracts,
state machines, jobs and pseudo code hold whichever framework and CMS the owner picks; the stack is
proposed, with every service verified and priced on the day, in `11-architecture.md` (ADRs) and the
services research in `01b-evidence.md`. Discoverability (AI search, sharing, SEO, links) is specified
in `15-discoverability.md`; the source catalogue in `16-source-catalogue.md`. Every module names the
prototype code it comes from, so nothing built in the prototype is lost.*

## 1. The system in one drawing

```
                      ┌──────────────── editorial ────────────────┐
 content team ─► CMS (structured articles, sources, catalogue) ─► review ─► named editor approves
                      │  validation on save: house rules, catalogue, links  │
                      └───────────────────────────┬────────────────────────┘
                                                  │ publish event (webhook)
                                                  ▼
 ┌──────────── build (static-first) ────────────────────────────────────────────────────────────┐
 │ fetch content → validate (M1, M2) → render pages (M4) + head/meta (M5) + share images (M6)    │
 │ → discovery files (M7: sitemap, news sitemap, feed, robots, llms.txt) → search index (M8)       │
 │ → gate (M13: the prototype's check.py, ported) → deploy to CDN                                  │
 └───────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                                 ▼
             CDN / host (static + a few functions) ─► readers, crawlers, answer engines, messengers
                                                 │
 jobs:  on publish → IndexNow ping (M10)   weekly → link check + archive (M9)   daily → backups
 later phase: data ingest (M14) → stats store → data pages
```

## 2. Repository layout (proposed)

```
/content-model/        schemas: article, source-ref, catalogue-entry, desk, subject, correction
/src/rules/            house rules + catalogue rules (M1, M2) — shared by CMS validation, build and gate
/src/render/           page templates (M4), head/meta builder (M5)
/src/share/            share-image generator (M6)
/src/discovery/        sitemap, news sitemap, feed, robots, llms.txt (M7)
/src/jobs/             link-check + archive (M9), IndexNow (M10), backups
/src/gate/             the build gate (M13) — every check of the prototype's check.py
/public/               static assets (tokens.css, site.css, site.js, icons, fonts self-hosted)
/tests/                unit (rules), contract (schemas), e2e (pages), accessibility, visual
```

## 3. Data contracts

**Article**

| Field | Type | Required | Rule |
|---|---|---|---|
| `slug` | string | yes | lowercase words joined by hyphens; immutable after first publish (a change leaves a redirect) |
| `desk` | enum(8) | yes | discover · define · design · develop · data · drive · defend · deal |
| `subject` | enum(11) | yes | the subject tags (`10-ssot.md`) |
| `kind` | enum | yes | Explainer · Analysis · News · Opinion (signed columns only) |
| `title` | string | yes | ≤ 110 characters (share-card and title-link fit) |
| `standfirst` | string | no | counted in the body length |
| `segments` | Segment[] | yes | ≥ 3 |
| `sources_used` | SourceRef[] | yes | ≥ 1; each resolves to a catalogue entry that was read |
| `sources_investigated` | SourceRef[] | yes | ≥ 1 |
| `byline` | Person or Desk | yes | a named person, or the desk with a named editor |
| `editor` | Person | yes to publish | the named editor who approved (EU AI Act Art. 50(4) editorial responsibility) |
| `published_at`, `updated_at` | datetime | set by workflow | ISO 8601 with zone |
| `cover` | CoverSpec | yes | drawn from the article's content (§4 M6) |
| `corrections` | Correction[] | no | append-only |
| `status` | enum | yes | the workflow state (§5) |

**Segment**: `{ heading: string (required), blocks: (Paragraph | Chart)[] }` — a Paragraph is text
(counted), a Chart is `{ chart_id, data, caption, table }` (not counted).

**SourceRef**: `{ url: string, note: string }` — `url` keys the catalogue; `note` is this article's
line on the source.

**CatalogueEntry**: `16-source-catalogue.md` §2.

**Correction**: `{ at: datetime, what_was_wrong: string, what_changed: string, by: Person }`.

## 4. Modules

### M1 — House rules (from the prototype's `content.py` `RULES`, `build.py` `check_rules`, `temp-startup-content/check-draft.py`)

Owns: the definition of the rules and the one function every layer calls — CMS validation on save,
the build, and the gate.

```
RULES = { min_chars: 800, max_chars: 3200, min_segments: 3 }

function body_chars(article):
    text = (article.standfirst or "")
    for seg in article.segments:
        for block in seg.blocks where block is Paragraph:
            text += plain_text(block)            # markdown stripped, link text kept, spaces kept
    return length(text)                          # headline, headings, charts, sources: not counted

function validate_article(article, catalogue) -> list of problems:
    problems = []
    n = body_chars(article)
    if n < RULES.min_chars or n > RULES.max_chars: problems += "body {n}: outside 800–3,200"
    if count(article.segments) < RULES.min_segments: problems += "fewer than 3 segments"
    if any(seg.heading is empty): problems += "a segment without a heading"
    if article.desk not in DESKS: problems += "not one of the eight desks"
    if empty(article.sources_used) or empty(article.sources_investigated): problems += "both source lists required"
    for ref in article.sources_used + article.sources_investigated:
        problems += validate_source_ref(ref, catalogue)              # M2
    for ref in article.sources_used:
        if catalogue[ref.url].checked.status == NOT_READ: problems += "cites as used a source we could not read"
    return problems
```

Tests: the owner's first article → 2,358 characters, 7 segments, valid; boundary cases 799 / 800 /
3,200 / 3,201; a segment without a heading; a used source marked not-read.

### M2 — Source catalogue (from `catalogue.py`, `build_catalogue`)

Owns: catalogue entries, their check history, and the catalogue pages.

```
function validate_source_ref(ref, catalogue):
    if ref.url not in catalogue: return ["uncatalogued source {ref.url}"]
    if not ref.note: return ["source note missing"]
    if not ref.url.startswith("https://"): return ["insecure or relative source URL"]
    return []

function canonical_source_url(url):
    if url matches doi pattern: return "https://doi.org/" + doi(url)          # Crossref display form
    return strip_tracking_parameters(url)

function catalogue_page_data(catalogue, articles):
    for entry in catalogue:
        entry.cited_in    = [a for a in articles if entry.url in urls(a.sources_used)]
        entry.consulted   = [a for a in articles if entry.url in urls(a.sources_investigated)]
        assert entry.cited_in or entry.consulted          # no orphans
    return group_by(entry.type, catalogue), group_by(entry.publisher, catalogue)
```

### M3 — Editorial workflow (§5)

Owns: states, transitions, roles, the audit log; blocks publication without an editor.

### M4 — Renderer (from `build.py` page functions)

Owns: every page type and its data. Page types: home, latest (paginated), article, desk, desks index,
subject, subjects index, source catalogue (and per-source pages at scale), how we work, corrections,
style guide (not indexed). Later phase: the data pages.

```
function render_site(content):
    pages = []
    pages += home(latest(content.articles, 1), content.desks)
    pages += latest_pages(content.articles, per_page = 12)            # "Load more" = next page link
    for a in content.articles where a.status == published:
        pages += article_page(a, related = same_desk_first(a, content.articles, 2))
    for d in DESKS: pages += desk_page(d, articles_on(d))
    for s in SUBJECTS: pages += subject_page(s, articles_tagged(s))
    pages += catalogue_pages(content.catalogue, content.articles)      # M2
    pages += how_we_work(), corrections_page(content)
    for p in pages: p.head = build_head(p)                             # M5
    return pages
```

Every page: one `h1`, `lang="en-GB"`, skip link, the desk bar, the footer; no layout shift from late
content (fixed-height bars; images with width and height).

### M5 — Head and metadata (from `build.py` `social`, the JSON-LD blocks)

Owns: title, description, canonical, robots, Open Graph, X card, icons, feed link, JSON-LD.

```
function build_head(page):
    head = []
    head += <title>{page.title} — gameformative</title>                    # ≤ 60 chars before the suffix where possible
    head += <meta name=description content={page.summary}>                 # 120–160 chars
    head += <link rel=canonical href={SITE_URL + page.path}>
    head += robots(page)                                                   # "index, follow, max-image-preview:large"
                                                                           # prototype/staging: "noindex, follow"
    head += open_graph(page)          # og:type (article|website), og:title, og:description, og:url,
                                      # og:image (+width 1200, height 630, alt, type), og:site_name, og:locale
    head += x_card(page)              # twitter:card=summary_large_image, title, description, image, image:alt
    if page.type == article:
        head += article:published_time, article:modified_time, article:section (desk), article:tag (subject)
        head += json_ld(NewsArticle(page), BreadcrumbList(home → desk → article))
    if page.type == home: head += json_ld(WebSite, Organization)
    if page.type == catalogue: head += json_ld(CollectionPage(ItemList(ScholarlyArticle|CreativeWork)))
    head += icons(favicon.svg, icon-32.png, apple-touch-icon 180, manifest), rss alternate
    return head

function NewsArticle(a):
    return { headline: a.title, description: summary(a), datePublished, dateModified,
             mainEntityOfPage: url(a), image: [share_image_url(a)], inLanguage: "en-GB",
             articleSection: desk_name(a), keywords: [desk_name(a), subject_name(a)],
             author: person_or_desk(a.byline), publisher: Organization(logo 512×512),
             citation: [ { @type: ScholarlyArticle|CreativeWork, name, url, identifier: doi_url } for s in a.sources_used ] }
```

### M6 — Share images (from `tools/render_images.py`)

Owns: one 1200×630 image per article and one default; the icon set.

```
function share_image(a):
    card = template(brand, kicker = desk + " · " + kind, headline = a.title (size steps 64/56/50 px by length),
                    art = cover(a.cover), footer = "Sources listed: {used} used · {investigated} investigated")
    png = render(card, 1200 × 630)            # headless browser or an image library (ADR in 11-architecture)
    png = quantise(png, 256 colours); strip metadata
    assert size(png) ≤ 300 kB and dims == 1200 × 630
    store at /share/{slug}-{content_hash}.png  # content-hashed name, so messengers never show a stale card
```

Regenerate on publish and whenever the headline, desk or cover changes.

### M7 — Discovery files (from `build_discovery`)

```
function sitemap(pages):       # every indexable page; <lastmod> = updated_at; split at 50,000 URLs
function news_sitemap(articles published in the last 48 h)      # if Google News is pursued (15-discoverability §3)
function feed(articles, n = 30):   # RSS 2.0 (+ atom:link self); title, link, guid, pubDate, category = desk, description
function robots():             # User-agent rules per 15-discoverability §1 (decision A12) + "Sitemap: <url>"
function llms_txt():           # site summary, articles, desks, standards, catalogue — markdown per llmstxt.org
```

### M8 — Site search

Owns: an index of articles, desks, subjects and catalogue entries built at deploy time; the search
page; the header control (inert in the prototype). The engine is an ADR (static index or hosted).

### M9 — Link check and archive (job)

```
weekly job link_check():
    for entry in catalogue:
        r = request(entry.url, method = HEAD then GET, timeout = 15 s, user_agent = "gameformative-linkcheck (+contact url)")
        record(entry, status = r.status, final_url = r.url, at = now)
        if r.status in (404, 410) or r.error: open_task(editor, entry, "source unreachable")
        if entry is used by any article and no archived copy: request_archive(entry.url)   # Internet Archive, rate-limited
    report: counts by status; entries changed since last run
```

Blocked responses (403, bot challenges) are recorded as "blocked", not as broken.

### M10 — IndexNow on publish (job)

```
on publish or update or delete(page):
    post { host, key, keyLocation, urlList: [page.url] } to the IndexNow endpoint     # 15-discoverability §3
    on failure: retry with backoff; never block the publish
```

### M11 — Corrections

Append-only corrections on each article (shown at its foot with dates), a public corrections page,
and an error-report form that reaches the editor. A correction updates `updated_at`, the sitemap
`lastmod`, and triggers M10.

### M12 — Analytics and consent

Privacy-first analytics without personal data by default (no banner needed until advertising or a
newsletter requires consent); events: page view, article read depth (25/50/75/100%), source-link
clicks (which sources readers open), share clicks by channel. Settings in `18-responsible-data.md`.

### M13 — The gate (from `check.py`)

Every check of the prototype's gate, run in CI before deploy: links and anchors resolve; one `h1`,
title and `lang` per page; token contrast AA in both themes; inert controls marked; the house rules
measured on the rendered page; every source linked to its catalogue entry; canonical, OG, X card,
share image exists and fits the budget; JSON-LD parses; sitemap and feed parse and list only real
pages. A red gate never deploys.

### M14 — Data pages (later phase; from `data/convert.py`, the data templates)

Ingest openfootball daily and a licensed provider; normalise names through the reviewed team table;
reconcile (goals for = goals against; points; files agree match by match; goal lists match scores);
refuse to publish a competition that fails. Live islands per `12-technical-design.md` §5.

## 5. The editorial workflow (state machine)

```
 draft ──submit──► in_review ──request changes──► changes_requested ──resubmit──► in_review
                      │
                      └─approve (editor; rules + links pass)─► approved ──schedule──► scheduled ──time──► published
 published ──correct (editor)──► published (+ correction, updated_at)
 published ──withdraw (editor-in-chief; reason required)──► withdrawn (page shows a withdrawal note; URL kept)
```

| Transition | Who | Guard |
|---|---|---|
| submit | writer | `validate_article` returns no problems |
| approve | named editor | re-validate; every link requested within 24 h; the editor ≠ the writer |
| publish | system | approved and scheduled time reached |
| correct | editor | correction note required |
| withdraw | editor-in-chief | reason required; URL never deleted |

Every transition writes an audit event `{article, from, to, by, at, note}`.

## 6. Security

CMS behind single sign-on with roles (writer, editor, editor-in-chief, admin); least privilege for
build tokens; secrets in the host's secret store, never in the repository; security headers (CSP
restricted to self and the font/analytics origins, HSTS, X-Content-Type-Options, Referrer-Policy
strict-origin-when-cross-origin, Permissions-Policy); dependency updates weekly; no third-party
share widgets or trackers (the share bar is plain links).

## 7. Tests

| Level | What | Tool class |
|---|---|---|
| Unit | M1 rules (boundaries), M2 catalogue rules, M5 head builder, M7 sitemap/feed | the framework's unit runner |
| Contract | every content document validates against its schema | schema validator in CI |
| End-to-end | every page: overflow 0 at 375 and 1440, one `h1`, 44 px targets on phones, no console errors; share bar; Load more; theme | headless browser |
| Accessibility | WCAG 2.2 AA automated rules + a manual keyboard/screen-reader pass per template | axe-class scanner + manual |
| Visual | per template at 375 and 1440, light and dark | screenshot diff |
| Discovery | OG/X tags present and image fetchable; JSON-LD valid; sitemap/feed valid | the gate (M13) + the platforms' debuggers at launch |

## 8. Operations

Deploy on every publish (static rebuild; incremental where the framework allows). Rollback = redeploy
the previous build. Content backed up daily (CMS export) and kept 30 days. Monitoring: uptime, build
failures, link-check report, Core Web Vitals field data. Runbook entries: failed build, broken
source spike, share cards stale in a messenger (rename the image by content hash, re-scrape in the
platform's debugger).

## 9. Prototype → module map

| Prototype | Module |
|---|---|
| `content.py` `RULES`, `body_chars`; `build.py` `check_rules`; `temp-startup-content/check-draft.py` | M1 |
| `catalogue.py`; `build.py` `build_catalogue`, `source_list` | M2 |
| (not in the prototype) | M3 |
| `build.py` page functions; `assets/tokens.css`, `site.css`, `site.js` | M4 |
| `build.py` `social`, `abs_url`, JSON-LD blocks | M5 |
| `tools/render_images.py` | M6 |
| `build.py` `build_discovery`, `indexable` | M7 |
| (inert header control) | M8 |
| the manual link checks of 2026-09-25 (`03-sources.md` §3) | M9 |
| — | M10, M11, M12 |
| `check.py` | M13 |
| `data/convert.py`, `data/teams.py`, the data page functions | M14 |
