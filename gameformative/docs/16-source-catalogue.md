# The source catalogue — specification

*For developers and editors. The client asked for "a scientific catalog to visit from the articles
to see our trusted knowledge sources we work with" (review, 2026-09-26). This is what the catalogue
is, how it is modelled, how it is shown, and the rules that keep it honest. Built in the prototype on
2026-09-26: `catalogue.py` (the data), `sources/index.html` (the page), `build.py` and `check.py` (the
rules) — D32.*

## 1. What it is for

Readers see, for any article, not only the sources it cites but **what kind of sources they are,
who publishes them, and how we checked them** — and from any source, every article that relies on
it. Editors get one register of every source ever used or set aside, so a source is described once,
checked once per publication, and re-checked when it changes.

## 2. The model

One entry per source, keyed by its canonical URL (the DOI resolver URL where a DOI exists).

| Field | Type | Rule |
|---|---|---|
| `id` | slug | unique; stable forever (it is the anchor `#src-<id>` and, at scale, the page `sources/<id>`) |
| `title` | text | the source's own title, in its language |
| `publisher` | text | the journal, body, outlet or project |
| `date` | ISO date or year | only when read on the source |
| `issue` | text | volume(issue), pages — research only |
| `type` | enum | `research` · `official` · `dataset` · `stats` · `reporting` · `reference` |
| `doi` | text | shown as `https://doi.org/<doi>`, the form Crossref asks for |
| `licence` | text | only when read (e.g. openfootball: CC0 1.0) |
| `checked` | (date, what we did) | "Abstract read…", "Downloaded and converted…", or "Not read: …" — never more than we did |

An **article** keeps its own note on each source it lists (what the source contributed to *this*
article, or why it was set aside), and refers to the catalogue by URL. One fact, one place: the
source's identity lives in the catalogue, its role lives in the article.

## 3. The types and how we weigh them

| Type | Meaning | Can be *used* when |
|---|---|---|
| Peer-reviewed research | a study in a peer-reviewed journal | at least the abstract was read; the article says when only the abstract was read |
| Official body | a governing body, league, federation, regulator or court speaking for itself | the document was read |
| Open dataset | primary data we download and recompute | the licence allows it (StatsBomb's does not) |
| Statistics provider | a commercial or community statistics site | its terms allow the use |
| Reporting | journalism from an identified outlet | attributed to the outlet |
| Reference | a glossary, definition page or method note | the page was read |

A source whose `checked` status is "Not read" can **only** appear under *investigated but not used*.

## 4. The rules, as code

```
on build:
  for article in articles:
    for s in article.sources_used + article.sources_investigated:
      require s.url in CATALOGUE                         # every source is catalogued
    for s in article.sources_used:
      require not CATALOGUE[s.url].checked.startswith("Not read")   # never cite unread
  require every CATALOGUE entry is used or consulted by some article   # no orphans
  require ids unique

on gate (independent of the build, on the rendered pages):
  for every source <li> in every article: require a link to sources/index.html#src-<id>
  require every such anchor exists on the catalogue page
```

## 5. The page

`sources/index.html`: an introduction with the counts (computed, never typed); a jump list by type;
one section per type, each entry showing title (link to the source), publisher · issue · date ·
DOI, licence, "Checked <date>: <what we did>", **Cited in** (articles) and **Consulted, not cited,
for** (articles); a list of publishers and institutions. JSON-LD: `CollectionPage` with an
`ItemList` of `ScholarlyArticle` (research) or `CreativeWork`, with DOIs as `identifier`.

Every source entry in every article links to its catalogue anchor, labelled with its type
("Peer-reviewed research · catalogue entry").

## 6. At scale (production)

- **One page per source** (`/sources/<id>`) once the catalogue passes about 100 entries, and one page
  per publisher (`/sources/publishers/<slug>`) — each a hub that links every article citing it
  (internal linking; see `15-discoverability.md` §5). The anchors stay valid as redirects.
- **Link checking**: a weekly job requests every catalogued URL; a failure opens a task for the
  editor and, for a *used* source, adds an archived copy link (Internet Archive) after review.
- **Change detection**: for official documents that are revised (e.g. the WADA List), the checked
  date is renewed when the article is updated.
- **Filters**: by type, publisher, desk, year; open access where the publisher states it.
