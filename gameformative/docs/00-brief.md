# Brief — gameformative.com

*Written 2026-09-25, the day the project opened. For anyone picking the project up: what was asked,
what the prototype is, what in it is real, and where it stands.*

## The ask, verbatim

> "I need you to create a new prototype called gameformative.com it is a game analytics informative
> site with new, articles, statistics. I need you to make a deep research how the sport media
> industry looks like, what are the 2027 trends colours layouts and check the largest sites like bbc
> sport, espn, nba.com, fifa, and the top sport new sites in Germany, India and china, do the home
> work about colours, ux, mobile and desktop best practices and make the best possible prototype
> with documentation for gameformative.com. Check the nepszabadsag prototype as that is another news
> media project of ours"

Owner, 2026-09-25. Later the same day: "In our documentation you need to list all sources you
researched with a short summary what we learned" — answered by `01a-source-register.md`.

## Round 2 — articles first (owner, 2026-09-25, later the same day)

> "At the very beginning we will start with articles only to have a base with informative great
> edutainment content in the sport industry … Gameformative will be a sport analytical and
> educational infotainment media site to support readers with news, tactics, techniques, scientific
> research about sport and related subjects." Topics: international news, sport science news, sport
> tech news, fan engagement, sport analytics, sponsorship, data intelligence in sport, athletes
> development, training goods, sport goods, "and similar topics". Articles "not shorter than 800
> characters and not longer than 3200. Always segmented", and at the end — not counted — "all
> source … not only we used but next to it the articles and source we investigated but not used".

**What that changed:** the product is now an article site first; the statistics described below are
a later phase, kept live and linked from the footer (D17). The first article is the owner's own
draft (D22). The rules are enforced by the build and the gate (D18, `07-gate.md` check 12).

## Round 3 — the eight desks (owner, 2026-09-25)

The owner set the article structure: eight desks, each defined by what the article does for the
reader — Discover, Define, Design, Develop, Data, Drive, Defend, Deal. They are now the site's
sections; the round-2 topics are kept as each article's subject tag (D26–D28).

## Who and what (round 1 — the statistics site, now a later phase)

- **The product:** gameformative.com, a new football **analytics + news + statistics** site in
  English: results and tables, analysis and explainers built on the numbers, season and tournament
  reviews, a method page that says what every number means.
- **Who it serves:** fans who follow more than one league and want the numbers explained, not just
  listed. The research (`01-research.md` §1–2) puts them on phones and desktops in roughly equal
  measure, arriving increasingly through social and video feeds, and trusting human-edited,
  sourced work more than automated copy.
- **Whose project:** the studio's own (the owner calls it "ours"). There is no client brand, no
  newsroom and no data contract yet — the domain was registered on the day (`02-audit.md`).
- **Precedent:** Népszabadság (`../../nepszabadsag/`), the studio's other news-media prototype —
  its generator pattern (`content.py` + `build.py`), prototype banner, gate and documentation set
  are followed here; its Hungarian print-daily design is deliberately not (each project carries its
  own brand).

## What the prototype is

A 19-page static site, generated from one content file and one data file:

| Page | What it shows |
|---|---|
| Home | lead analysis, the Premier League table, "the numbers this week", analysis, the four other leagues, World Cup review, automated round-ups, newsletter (inert) |
| Scores | the latest round and next fixtures for five leagues, filterable |
| Tables & stats, and one page per league (5) | full table (overall / home / away, sortable, compact on phones), key numbers, points race, team leaders, clean sheets, results, fixtures |
| Premier League 2025/26 | complete season: final table, title race, goals by minute, top scorers, attendance |
| World Cup 2026 and its final | the bracket, twelve groups, scorers, goals by stage; the final as a match centre |
| Analysis (index + 5 pieces) | four analyses and one explainer, with charts |
| How we count | glossary, data sources, table rules, labels, automation and AI, corrections, accessibility |
| Style guide | the design system, live |

## What is real, sample, inert, not built

- **Real:** every result, table, goal, scorer, line-up and attendance — openfootball's
  public-domain (CC0) data for the 2026/27 Premier League, LaLiga, Bundesliga, Serie A and Ligue 1
  (results to 20 September 2026), the complete 2025/26 Premier League, and all 104 matches of the
  2026 World Cup. Every derived figure is computed by `data/convert.py`; nothing is typed.
- **Sample:** the article copy — written for the prototype by the "data desk" (no named newsroom
  exists), every number in it read from the data, and the build stops if a data refresh would make
  a sentence untrue (`04-decisions.md` D7).
- **Inert, shown in place:** search, sign-in, the newsletter form, and the panels for xG, shots,
  possession, player ratings and live scores — each says why.
- **Not built:** a live data feed, accounts, the newsletter, the corrections page and form, other
  sports, women's football, photography, advertising slots.

## Where it stands

First version built and measured 2026-09-25 (`06-build-log.md`); gate clean (`07-gate.md`). The
design-system and frame gates of the method were compressed into the owner's instruction to build
"the best possible prototype" (D1) — the owner's review of the rendered site is that gate.

## How to read this folder

`README.md` is the index and the dated process log. Read `01-research.md` for the why,
`05-design.md` for the system, `04-decisions.md` for every choice, `presentation.html` for the
one-page argument.
