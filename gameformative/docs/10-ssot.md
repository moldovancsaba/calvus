# Single source of truth — terms, entities, rules

*The one place where every term the other documents use is defined. Written 2026-09-25. The
reader-facing wording of the same terms lives in one place too — `content.py` `GLOSSARY`, rendered
on How we work (`how-we-count/`); if the two ever disagree, this table is the definition and the glossary is fixed.*

## Glossary

| Term | Definition |
|---|---|
| Competition | a league season (e.g. Premier League 2026/27) or a tournament (World Cup 2026) |
| Round / matchday | the source's round label; "matchday N" for leagues, stage names for knock-outs |
| Result | a match with a recorded full-time score (a `score.ft` pair, or a bare `[h, a]` pair in the 2026/27 files) |
| Fixture | a scheduled match without a result |
| P, W, D, L, GF, GA, GD, Pts | played, won, drawn, lost, goals for, goals against, goal difference, points (3/1/0) |
| PPG | points per game: Pts ÷ P, two decimals |
| Form | the last five results, oldest first |
| Goals per game | goals ÷ results, where a match with extra time counts its after-extra-time score; shoot-out penalties are never goals |
| Home win % / Draw % / Away win % | share of results with each outcome |
| BTTS | both teams scored: share of results with each side scoring |
| Clean sheet | a result in which the team conceded nothing |
| Minute bucket | 1–15, 16–30, 31–45+ (with first-half added time), 46–60, 61–75, 76–90+ (with added time), 91–120 |
| Automated | text a fixed template fills from the data, published without a human edit |
| Analysis / Explainer | human-written pieces (in the prototype: sample copy from the data desk) |
| Data desk | the byline for pieces with no named author |
| Data to | the latest date with a recorded result across the leagues shown |
| Article | a piece in one topic, of one kind (Explainer, Analysis, News, Opinion), with a headline, an optional standfirst, headed segments and two source lists |
| Body characters | the characters of the standfirst and every paragraph, spaces included; headline, segment headings, charts and source lists excluded (D19) |
| Segment | a part of an article under its own heading; every article has at least three |
| Sources used | the sources the article's text relies on, each with a link, publisher and a line on what it contributed |
| Sources investigated but not used | sources opened or requested for the article and set aside, each with the reason |
| Desk | one of the eight sections in `content.py` `DESKS` — Discover, Define, Design, Develop, Data, Drive, Defend, Deal — each defined by what the article does for the reader; every article has exactly one |
| Subject | one of the eleven subject tags in `content.py` `TOPICS` (the round-2 topic list); every article has one |

## Entities

| Entity | Key fields | Source |
|---|---|---|
| Competition | id, name, country, season, source file | `data/convert.py` `LEAGUES` |
| Team | source name → display name, three-letter code | `data/teams.py` (reviewed table) |
| Match | date, time, round, home, away, score (ht, ft, et, p), group | openfootball |
| Goal | scorer, minute, penalty, own goal | openfootball "-full" |
| Line-up | starters (captain), bench, substitutions (on, off, minute) | openfootball "-full" |
| Table row | the table fields + home/away splits, clean sheets, failed to score, form, PPG | computed |
| Aggregates | per competition: goals, per game, outcome shares, BTTS, 0–0s, biggest and highest | computed |
| Article | slug, kind, title, dek, key facts, body (paragraphs, headings, chart ids), cover | `content.py` |

## Rules register

| # | Rule | Where it is code | Tested by |
|---|---|---|---|
| R1 | Table order: points, goal difference, goals for, name | `convert.py` `table()` | the gate (reproduce) |
| R2 | A competition's goals for equal its goals against | `convert.py` asserts | `convert.py --check` |
| R3 | Points reconcile: 3 × decisive results + 2 × draws | `convert.py` asserts | `convert.py --check` |
| R4 | Two source files for one competition agree match by match | `convert.py` asserts | `convert.py --check` |
| R5 | Each match's goal list matches its score (after extra time) | `convert.py` `check_goal_lists()` | `convert.py --check` |
| R6 | Every source team name is in the reviewed table | `convert.py` `club()` / nations check | `convert.py --check` |
| R7 | Every knock-out winner has exactly one feeder match (the bracket resolves) | `convert.py` `feeders()` | `convert.py --check` |
| R8 | Own goals never count to a scorer; penalties do | `convert.py` `scorers()` | reproduce |
| R9 | A narrative claim in copy holds in the data, or the build stops | `content.py` `premise()` | `build.py --check` |
| R10 | Colour never alone: letters on chips, H/D/A on bars, keys on bands | `build.py` components | the rendered look |
| R11 | Every chart has a text alternative and its numbers as a table | `build.py` `figure()` | the rendered look |
| R12 | Inert controls: `aria-disabled` + a title saying why | `build.py` | `check.py` §11 |
| R13 | Automated text is labelled and links to the policy | `build.py` `roundup()` | the rendered look |
| R14 | Every article has 800–3,200 body characters | `content.py` `RULES`, `build.py` `check_rules()` | `check.py` §12 |
| R15 | Every article has at least three segments, each headed | same | `check.py` §12 |
| R16 | Every article lists sources used and sources investigated but not used, each linked, with a note | same | `check.py` §12 |
| R18 | Every article sits on exactly one of the eight desks, and its desk page exists | `build.py` `check_rules()` | `check.py` §12 |
| R17 | A source is linked only if it was requested on the day; one we could not read is marked so in the docs | editorial | `03-sources.md` §3 |

## Settings

| Setting | Value | Where |
|---|---|---|
| Asset version | `V` | `build.py` |
| Leagues shown | en, es, de, it, fr | `convert.py` `LEAGUES` |
| Phone breakpoint / desktop breakpoint | 720 / 1000 px | `site.css` |
| Items before "Load more" | 5 | `build.py` `build_analysis_index` |
| Theme choice storage | `localStorage["gf-theme"]`, per device | `site.js` |
| Desks | eight, in `DESKS` order (Discover → Deal) | `content.py` |
| Subjects | eleven, in `TOPICS` order | `content.py` |
| Article rules | 800–3,200 body characters, ≥ 3 segments, both source lists | `content.py` `RULES` |

## Document map

`00` brief · `01` research · `01a` sources researched · `01b` evidence · `02` audit · `03` inputs
and gaps · `04` decisions · `05` design · `06` build log · `07` gate · `08` asks · `10` this ·
`11` architecture · `12` technical design · `13` implementation plan · `14` token map · `18`
responsible data · presentation · `../temp-startup-content/` (the content team's handover pack, temporary).
