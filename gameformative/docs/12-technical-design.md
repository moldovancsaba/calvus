# Technical design

*How the prototype works, file by file, and what the real build adds. Written 2026-09-25.*

## 1. The prototype's pipeline

```
data/fetch.py      downloads 9 openfootball files → data/raw/          (run only to refresh)
data/convert.py    raw/ → stats.json, with the data asserts           (--check: reproduce only)
content.py         article copy, nav, glossary — figures read from stats.json, premises asserted
build.py           content.py + stats.json → every page               (--check: reproduce only)
check.py           the gate (07-gate.md)
docs/build.py      docs markdown → HTML, and presentation.html from presentation-source.md
```

Refresh: `python3 data/fetch.py && python3 data/convert.py && python3 build.py && python3 check.py`.
If a refreshed dataset breaks a copy premise, `build.py` stops and names the sentence to rewrite.

## 2. Content model

| Object | Fields | Notes |
|---|---|---|
| Article | slug, topic, kind, byline, origin (owner draft or data desk), title, standfirst (optional), segments [(heading, [paragraph or ("chart", id)])], sources_used[], sources_investigated[], cover | round 2; `check_rules()` enforces `RULES` before a page is written |
| Source | title, publisher (with date where known), url, note | the note says what it contributed, or why it was not used |
| Chart | id → a figure built by `build.py` `chart()` | nine ids today; each renders title, subtitle, the chart, source, data table |
| Cover | type (race, bars, final, minutes, explainer) | an SVG drawn from the data; decorative |
| Round-up | derived from a league's latest round | template only; labelled Automated |
| Glossary entry | term, definition | `content.py` `GLOSSARY` |

## 3. Data mapping

| Source field | Becomes |
|---|---|
| `matches[].score.ft` or bare `score: [h, a]` | a result; a list score is the 2026/27 files' shorthand |
| `score.et`, `score.p` | after-extra-time score (cumulative); shoot-out, shown in brackets, never goals |
| `round` "Matchday N" | round number for the points race; knock-out rounds by name |
| `group` "Group X" | the World Cup group tables; teams in the round of 32 are marked through |
| `goals1/goals2[].{name, minute, penalty, owngoal}` | scorers (own goals excluded), minute buckets, the final's timeline |
| `lineup[].starter/subs` | the final's line-ups and substitutions |
| `attendance`, `ground` | season and tournament attendance; the final's venue |
| team names | display name and code through `data/teams.py`; aliases for the two "-full" files |

## 4. Page templates

`build.py` has one function per template: home, latest (articles index), article (×6), topics index and topic (×11), how we work, style guide, redirects from `/analysis/`; and the data pages of the later phase — scores, stats hub, league (×5), season review, World Cup, match centre. Shared chrome:
banner, header, desk bar, footer, tab bar, More sheet (and the later-phase notice on the data pages). Every page: one `h1` (visually hidden
on the home page, where the lead headline is an `h2` inside a link), `lang="en"`, a description,
light and dark `theme-color`, JSON-LD where it applies (WebSite, NewsArticle, SportsEvent).

## 5. The live match centre (later phase — specified, not built)

- **Data**: provider push (or 5 s poll) into a per-match JSON at the edge: score, minute, events.
- **Score region**: `role="status"`, `aria-live="polite"`, `aria-atomic="true"` — present in the DOM
  before the first update; the full score is announced ("Spain 1, Argentina 0"), never one digit.
- **Events**: a `role="log"` list, newest first, with a "Key events" filter (goals, cards, VAR,
  substitutions) and periodic summaries.
- **Ticker rule**: anything that moves or updates for more than 5 s has a visible pause (WCAG 2.2.2);
  motion respects `prefers-reduced-motion`.
- **Markup**: `LiveBlogPosting` for text coverage; `BroadcastEvent` for any live video.
- **Stats panel**: possession, shots, xG, passes from the licensed provider; until then, the inert
  panel the prototype shows.

## 5a. How an article gets onto the site

1. The content team drafts in `../temp-startup-content/drafts/<slug>.md` from the template, and
   `check-draft.py` confirms the house rules (it counts exactly as the build does).
2. The named editor approves (`status: ready-for-editor` → approved).
3. The maintainer moves the article into `content.py` `articles()` — slug, desk, subject, kind,
   byline, origin, title, standfirst, segments, both source lists, cover — then runs `build.py`
   (which asserts the rules again) and the gate (which measures them on the page).
4. A future converter can read the draft format directly; the format is fixed so that it can
   (`13-implementation-plan.md` issue 7).

## 6. State and interaction

| Behaviour | Implementation | Without JavaScript |
|---|---|---|
| Theme | `data-theme` on `<html>`, set early by an inline script from `localStorage` | follows the system |
| Table sort | buttons in headers; `aria-sort`; a polite live region announces the order | table in rank order |
| Overall / home / away | three tables, one shown | overall shown |
| All columns (phones) | toggles `.is-full` on the table box | compact table |
| League filter (scores) | shows one league's block | all leagues shown |
| Load more (analysis) | reveals the next items; focus moves to the first new one | first five shown; the rest are also on the home page and hubs |
| More sheet | dialog; focus in, Escape out, focus returned | the footer holds the same links |

## 7. SEO and URLs

Readable, stable paths: `/stats/premier-league.html`, `/world-cup-2026/final.html`,
`/analysis/<slug>.html`. Titles lead with the subject and end "— gameformative". Production adds
canonical URLs, an XML sitemap, and `LiveBlogPosting` / `BroadcastEvent` markup on live pages.

## 8. Performance

No images; covers are inline SVG under 2 kB each; one font family (one request); 36 kB CSS, 6 kB
JS, both cacheable and versioned. Production: self-host and subset the font, inline critical CSS,
pre-compress, CDN.

## 9. Operations

The gate runs before every publish. Data refresh is a scripted pipeline; a failing assert stops
publication and names the competition and the check that failed. Corrections are logged with date
and text. Source files are kept by input hash, so any published table can be rebuilt exactly.
