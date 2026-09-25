# Decisions

*Numbered register. Each entry: date, the decision, by whom, why, what it replaced. A decision is
written here before it is code.*

**D1 — 2026-09-25 — Build the first version directly; the owner's review is the design gate.**
By: owner's instruction ("make the best possible prototype with documentation"). Why: the method
(`PROTOTYPING.md` §2) puts design-system and frame approval before layout; the owner asked for the
finished prototype in one round, as on Népszabadság (its D1). The design system is still built
first and live (`styleguide/index.html`), so the owner can approve or redirect it on a rendered
page. Replaced: separate token and frame approvals.

**D2 — 2026-09-25 — Football first; five leagues and the World Cup.** By: the team, from the
research. Why: 51% of people globally are football fans (register I19); the only open data verified
as free for commercial use is openfootball's football data (O1, O2); StatsBomb and NBA.com terms
forbid it (O3, O4). Cricket, NBA/CBA and women's football are expansions (`01-research.md` P12).

**D3 — 2026-09-25 — Every figure comes from openfootball through one converter; nothing typed,
nothing estimated.** By: the team. Why: `PROTOTYPING.md` §3.1 (no figure invented), and a stats site
whose numbers do not reconcile has no product. `data/convert.py` asserts that each table's goals
for equal its goals against, points reconcile with results, the two files for a competition agree
match by match, and every goal list matches its score. It stopped the first run on four World Cup
nations spelled differently in the two files — resolved by an explicit alias table, not fuzzy
matching.

**D4 — 2026-09-25 — Palette: warm off-white, ink navy, one blue, one orange.** By: the team, from
`01-research.md` §4. Why: the measured leaders use a near-black/navy structure and one saturated
accent, blue most often; WGSN × Coloro project Luminous Blue as 2027's colour and Energy Orange
among its key colours; blue with orange is the most colour-blind-safe pair. Hex values are our own
readings and are contrast-checked by the gate. Replaced: nothing (new brand).

**D5 — 2026-09-25 — Type: Archivo, one variable family with a width axis.** By: the team. Why: the
leaders pair condensed display with wider UI type (§5); the World Cup 26 face failed at small sizes
because it was condensed everywhere (T15). One family, three widths (72 / 85 / 100%), tabular
numerals, one font request.

**D6 — 2026-09-25 — Light by default, dark by system preference or toggle, both tokenised.** By: the
team. Why: NNG — light reads better for most, dark should be available (S11); three of five stats
sites and FIFA's own tokens offer both (ST4, ST6, ST7, G6). The choice is stored per device only.

**D7 — 2026-09-25 — Article copy is written from the data, with premises that stop the build.** By:
the team. Why: sample copy on a live data feed goes stale silently. Each article reads its figures
from `stats.json`, and each narrative claim ("City have won all five", "the last quarter-hour has
the most goals") is a `premise()` in `content.py` — a refresh that falsifies one stops the build
instead of publishing an untrue sentence.

**D8 — 2026-09-25 — Byline "gameformative data desk"; no invented journalists.** By: the team. Why:
there is no newsroom; fictional named reporters on a news site would misrepresent who wrote it
(Népszabadság used designed initials for the same reason). The Trust Project's expertise indicator
(S33) is met when the newsroom is named.

**D9 — 2026-09-25 — No photography; data graphics as covers.** By: the team. Why: no licensed photo
source, AI imagery ruled out (`PROTOTYPING.md` §3.1). The covers are drawn from the numbers the
story is about (a points race, goals per game, a scoreline), which is also the brand idea: the
numbers are the picture. A photo agency licence is ask A3.

**D10 — 2026-09-25 — Scores before stories: a latest-results strip on every page.** By: the team.
Why: every regional leader puts scores at the top (`01-research.md` §3.2). The strip does not move
on its own, so it needs no pause control; the live version's rules are in `12-technical-design.md`.

**D11 — 2026-09-25 — Visible navigation: a top nav on desktop, a five-tab bar on phones.** By: the
team. Why: NNG, visible beats hidden, and a tab bar holds 4–5 items (S7, S8). Home · Scores · Stats ·
Analysis · More; More holds World Cup 2026, How we count, the leagues, theme and sign-in.

**D12 — 2026-09-25 — Phone tables are compact until asked.** By: the team, after the first measured
pass. Why: the full twelve-column table at 375 px showed only P, W and D before scrolling — Pts was
off screen. Phones now show #, Team, P, GD, Pts with an "All columns" button (NNG, let users choose
columns, S9); desktop shows everything.

**D13 — 2026-09-25 — Our table order is stated, not hidden.** By: the team. Why: official
tie-breakers differ by competition (gap 4 in `03-sources.md`); applying each league's full rules
needs head-to-head logic the prototype does not need to prove the product. Every table says so.

**D14 — 2026-09-25 — Automated round-ups come from a template, and say so.** By: the team. Why:
Article 50 of the EU AI Act, in force from 2 August 2026, and the reader-trust evidence (§7). The
"in numbers" cards are filled by `build.py` from the results — no language model — and carry the
Automated label and a link to the policy. Replaced: nothing.

**D15 — 2026-09-25 — Charts are HTML where text matters.** By: the team, while building. Why: an
SVG chart drawn at a fixed viewBox shrinks its labels to ~7 px on a phone. Bars, stacked bars and
columns are HTML; the line chart is an SVG stretched to its box with HTML labels over it, so text is
real text at every width. Cover graphics stay SVG (decorative, `aria-hidden`).

**D16 — 2026-09-25 — The browser was used only on the local prototype.** By: owner (declined an
external site in the in-app browser). Why: owner's call. Effect: the benchmark is built from
measured HTML and CSS, not rendered pages (`01-research.md` §0).

**D17 — 2026-09-25 — The launch is articles only.** By: owner ("At the very beginning we will start
with articles only to have a base with informative great edutainment content in the sport
industry"). What changed: gameformative is repositioned from a football statistics site to a sport
analytical and educational infotainment site — news, tactics, techniques, scientific research — and
the home page, navigation and topic structure are article-led. Replaced: D10's results strip (now the
topic bar) and the data-led home page. The data pages were live, so they stay (never delete a live
URL), out of the main navigation, marked "a later phase" and linked from the footer and More.

**D18 — 2026-09-25 — The house rules for every article.** By: owner. 800–3,200 characters, always
segmented, and two source lists at the end — the sources used and the sources investigated but not
used, not counted in the length. Enforced twice: `build.py` stops on a breach (`check_rules`), and
`check.py` measures the rendered page independently (check 12).

**D19 — 2026-09-25 — What a "character" is.** By: the team; to confirm with the owner (ask A8).
Characters of body text — the standfirst and every paragraph, spaces included. Headline, segment
headings, charts and the source lists are not counted. Why: it matches the count in the owner's own
draft (2,364 there; 2,358 by this definition — the difference is paragraph separators), and it is
what a reader reads.

**D20 — 2026-09-25 — Eleven topics.** By: the owner's list, plus one the owner's own description
names. International news, Sport science, Sport tech, Fan engagement, Sport analytics, Sponsorship,
Data intelligence, Athlete development, Training goods, Sport goods — the owner's ten — and Tactics &
technique, from "news, tactics, techniques, scientific research". Each topic has a page; a topic
with nothing published says so plainly.

**D21 — 2026-09-25 — Articles move from /analysis/ to /articles/, with redirects.** By: the team. Why:
the articles are no longer only analysis. The six old URLs (live since the first push) now redirect
(meta refresh, canonical, noindex) — none is deleted.

**D22 — 2026-09-25 — The owner's draft ships as written.** By: the team, per `PROTOTYPING.md` §3.1.
The first article is the owner's draft of 2026-09-25 (`docs/reports/gameformative-article-latest.md`
in the management repository, branch `cursor/gameformative-client-9b8a`), word for word — headline,
seven segments, both source lists with their notes. Removed: only the internal status block above
the article (status, version, scores, article id, a line about internal rules), which is not article
copy. Not added: a standfirst (the draft has none; cards show the opening of the first paragraph).
Its two used sources were opened and their abstracts support the text (`03-sources.md` §3).

**D23 — 2026-09-25 — The data articles gain honest "investigated" lists.** By: the team. Each lists
sources the research of 2026-09-25 actually opened or requested and set aside, with the real reason
(licence, a 403, proprietary data). None is invented for the look of the list.

**D24 — 2026-09-25 — An unsourced claim became a sourced one.** By: the team. The explainer's "LaLiga
and Serie A use head-to-head results first" came from general knowledge; under D18 it needed a
source. Flashscore España (LaLiga) and DAZN Italia (Serie A) were opened and confirm it; DAZN adds
Serie A's play-off, which the copy now mentions. A third page (365Scores) returned HTTP 500 and is
listed as investigated.

**D25 — 2026-09-25 — Empty topics say "none published yet".** By: the team. An earlier wording, "first
in preparation", implied work that does not exist.

**D26 — 2026-09-25 — The eight desks are the site's structure.** By: owner ("We need to use this
article structure"): Discover, Define, Design, Develop, Data, Drive, Defend, Deal, each defined by
what the article does for the reader — the owner's wording, verbatim, on every desk page and on How
we work. The desk bar replaces the topic bar; the phone tab bar's third tab is Desks. Every article
sits on exactly one desk; `build.py` refuses an article without a valid desk and `check.py` checks
that each article's desk page exists. Replaced: topics as sections (D20).

**D27 — 2026-09-25 — The eleven topics become subject tags.** By: the team. The topic pages were live
(pushed hours earlier), and "never delete a live URL" holds, so they stay — as subject pages: each
article shows "Subject: …" and links to it; the footer and More link "All subjects". Two axes, one
navigation: desks say what a piece does for you, subjects say what it is about.

**D28 — 2026-09-25 — The desks of the six articles.** By: the team; one to confirm (ask A11).
The GPS article → **Define** (its own source note says it "stays on definition literacy", and its
question is "which math are we using?"); **Defend** (injury systems, load practice) is the other
fit. The table explainer → Define. The four data analyses → Data.
