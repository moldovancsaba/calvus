# Research — the sports media industry, the leading sites, 2027 trends and best practice

*Written 2026-09-25 for the owner's brief (`00-brief.md`): look at how the sport media industry
works, what the 2027 colour, layout and UX trends are, and what BBC Sport, ESPN, NBA.com, FIFA and
the top sports sites in Germany, India and China do — then build the best prototype that research
supports. This page is the synthesis. Every source, with what we learned from it, is in
`01a-source-register.md`; the raw measurements are in `01b-evidence.md`. Source numbers below
(G4, R2, T6…) refer to that register.*

## 0. Method, and what it can and cannot show

- **Measured, not remembered.** 31 sports and stats sites were fetched with `curl` on 2026-09-25
  (the global and regional sets between 18:35 and 18:43 UTC), all from a single Hungarian connection. Their HTML and CSS were counted
  by script: bytes, time to first byte, framework, fonts, the ten most frequent colours, navigation
  labels, structured data, and ad and consent vendors. **Nine sites refused the request** (ESPN,
  The Athletic, kicker, ESPNcricinfo, cricinfo, NDTV Sports, FBref, Sofascore, WhoScored). They are
  named as blocked and not described. FIFA returned an empty page that fills in with JavaScript.
  Sportskeeda served its US edition to our location.
- **Rankings come from panels, not from assumption.** The "top sites" in each country were taken
  from Similarweb and Semrush (August 2026), cross-checked where two panels exist (R1–R13).
- **Industry figures were read at source.** Where a primary page blocked us, a named secondary
  write-up was read and labelled as such. Search-snippet figures are not used anywhere.
- **2027 is a forecast.** Everything about 2027 below is marked **projection** and names the
  forecaster. Pantone's 2027 colour does not exist yet; it is normally announced in December (T2).
- **Limits.** No JavaScript was run and no external page was rendered, so rendered layout, Core Web
  Vitals and script-injected ads of other sites are not measured. Paid panels were not bought.

## 1. The industry in 2026

- **Rights money still rises, more slowly.** Executives expect 7.4% annual growth across sport, but
  media rights only 5.1%, down from 6.1% in 2023 (PwC Global Sports Survey 2026, I4). Streamers are
  **projected** to spend US$14.2bn on rights in 2026 (Ampere, I1).
- **Data is the product around the product.** Stats Perform sells automated previews and recaps
  and produces highlights "up to 80% faster" (I10, I16). Opta Analyst, a stats-led editorial site,
  reaches about 1 million monthly visitors (I14). xG is now fans', fantasy players' and bookmakers'
  shared vocabulary (I15), but it is licensed data.
- **The business is advertising plus bundles.** All five stats sites we could load carry ads. The
  Athletic reached profit inside the New York Times bundle (I26, I27). Only 17% of people pay for
  online news (I11). The German leaders add pay-or-consent ("Pur-Abo", DE2, DE5) and put betting
  links in the nav (DE2, DE4, DE5).
- **Women's sport is the growth line.** Deloitte **projects** US$3bn elite revenue in 2026, up 340%
  since 2022 (I29). 46bn minutes were watched in 2025, 71% more than 2022 (I30).
- **Football is the right first sport**: 51% of people globally are fans (I19). India is
  cricket-first (R4, IN1, IN7) and China is NBA, CBA and football on apps (CN1–CN4, R13).

## 2. How fans get news now

- For the first time **social and video networks (54%) beat publishers' own sites and apps (51%)**
  as a way into news; 77% watch news video weekly; 10% use AI chatbots for news weekly (DNR 2026,
  I11). **The report has no sport-specific finding**, and none is attributed to it here.
- Trust in news is 37%. Only 12% are comfortable with news made entirely by AI, against 62% for
  news made by humans (I13). The AI recaps that MLS and ESPN published unreviewed drew criticism and
  carried errors (I32, I33).
- Web traffic worldwide is about half mobile, half desktop (StatCounter, August 2026: 49.36% /
  49.11%, S19). Similarweb puts mobile at 66.55% of all traffic (I22). **No open source gives a
  sports-only device split** (I25), so both widths are designed as first-class.

**What this means for a new site:** its own pages must be worth a direct visit. The biggest stats
site measured gets 72.9% of its traffic direct (FotMob, I24). Its numbers must be shareable into
the social and video feeds where discovery now happens, and it must be visibly human-edited and
sourced.

## 3. The benchmark — what the leaders do

### 3.1 Global (the owner's named sites)

| | BBC Sport | NBA.com | FIFA | Sky Sports | ESPN | The Athletic |
|---|---|---|---|---|---|---|
| Result | measured | measured | empty page | measured | **blocked** | **blocked** |
| First byte, cold | 0.10 s | **5.11 s** | 0.16 s | 0.11 s | — | — |
| Platform | React, server-rendered | Next.js | React, browser-rendered | server-rendered | — | — |
| theme-color | #FFFFFF | #000000 | #020F2A | #002A91 | — | — |
| Dark mode | .co.uk only | yes (5 rules) | yes, both themes tokenised | 1 rule | — | — |
| Type | own family (Reith) | Roboto + condensed display | own family + condensed P26 | own 2026 family + per sport | own "Ignite" (T19) | — |
| Scores up front | no | score strip | — | Live Sport section | — | — |

### 3.2 Germany, India, China (the top four by panel, with substitutes where blocked)

| Country | Site | What leads the page | Pattern |
|---|---|---|---|
| Germany | transfermarkt | tables and market values | data-first; pay-or-consent; betting in the nav |
| | sportschau | **Live & Ergebnisse** (live & results) | public broadcaster: fastest first byte, richest structured data, dark mode |
| | sport1, sport.de | **Heute Live**, Liveticker | live tickers; betting and bookmakers in the nav |
| India | cricbuzz | a live-score carousel | cricket-first; score before story |
| | Sportstar, Times of India | scorecards, match centre | cricket-first; paywall (Piano) |
| China | hupu, zhibo8 | fixture and score strips | extreme link density (zhibo8: 2,064 links); community forums |
| | dongqiudi, qq | today's matches; app download | app-first websites; a separate numeral font for scores (qq) |

**Across all three markets, scores come before stories.** Every regional leader puts a live
or latest-results strip, or a "live and results" nav item, at the top. Germany's leaders are
table-heavy, India's are cricket-first, and China's are app-first.

### 3.3 The stats and analytics sites

| Site | Theme | Patterns worth taking | Attribution |
|---|---|---|---|
| Opta Analyst | purple/magenta/orange, light only | predictions, Expected Points, power rankings | Opta is the brand |
| FotMob | light + dark | ratings, shot maps, percentile bars, xG leaderboards | **none visible** |
| Basketball-Reference | light only, system fonts | 50 sortable tables, glossary tooltips | "Data Provided By Sportradar" |
| Understat | **dark by default** | xG table, CSV/JSON/XLSX export | — |
| StatMuse | light + dark with toggle | plain-English question search, a data and glossary page | — |

Three of the five offer a dark theme, and every one takes a side between dense tables and
visual components. Only one names its data provider on the page.

## 4. Colour

### 4.1 What the leaders actually use (measured)

Counted from the HTML and CSS (G1–CN5, ST2–ST7). The recurring structure is a **near-black or deep
navy base, white, and one saturated accent**:

| Site | Base / structure | Accent |
|---|---|---|
| BBC Sport | #000000, #181818 | #ffd230 (yellow) |
| NBA.com | #000000, #1d428a | #c8102e (red), #0268d6 |
| FIFA | #020f2a, #03122b | #00b8ff, #0a84ff |
| Sky Sports | #0a1388, #002a91 | #214cb8 |
| transfermarkt | #00193f | #5ca6ff, #00aded |
| sport.de | #1c1c1c, #054850 | #f2e604 (yellow) |
| cricbuzz | — | #009270 (green) |
| Times of India | — | #e21b22 (red) |
| hupu | — | #c60100 (red) |
| Opta Analyst | #1d0a30 | #fd4890, #e56329 |

**Blue in the brand or structure is the single most common choice**: FIFA, Sky, NBA and
transfermarkt use it. The accent is always one high-chroma colour, never a rainbow.

### 4.2 What the forecasts say — projections

- **WGSN × Coloro, Colour of the Year 2027: Luminous Blue** (Coloro 125-28-38), a lapis/cobalt blue.
  The S/S 27 key colours are **Energy Orange**, Pop Pink, Meadowland Green and Clay (T6).
  **Projection.**
- **Pantone 2026: Cloud Dancer**, a soft white described as a "structural anchor" (T1). The 2027
  colour is not announced (T2).
- Figma's 2026 trends put **dark mode as a standard feature** and neon accents on dark (T9);
  Adobe's put saturated palettes and oversized type (T8). The 2027 web forecasts are agency blogs
  (T12, T13) and add "data-driven design" and "real-time content". **Projection.**

### 4.3 The accessibility constraint

Blue with orange is the most reliable pair for colour-blind readers, while green against red is the
worst (S12). WCAG 2.2 requires 4.5:1 for text and 3:1 for chart marks and controls (S2). ESPN chose
its 2026 red "for web accessibility and digital visibility" (T19).

**Conclusion for gameformative:** a warm off-white ground in the spirit of Cloud Dancer, and an ink
navy for bands and dark mode, which is the leaders' structure. On it, one brand blue read from
Luminous Blue and one accent read from Energy Orange. That gives a 2027-forward palette that is
also the colour-blind-safe pair. The hex values are our own readings: no forecaster publishes hex
(T6), and every pair is contrast-checked by the gate in both themes (`07-gate.md`).

## 5. Type

- **Every leader owns its type**: Reith (G1), Sky Sports Brand 2026 (G8, T21), ESPN Ignite (T19),
  FIFASans and P26 (G5), Bundesliga's new font (T18). Sky replaced six fonts with one family of five
  weights (T21).
- **Condensed display for scores and headlines, wider cuts for UI.** The World Cup 26 face is
  ultra-condensed black, and it failed at small UI sizes (T15). NBA pairs Roboto with condensed
  display cuts (G4). Tencent sets numerals in a separate face (CN4).
- **Conclusion:** one variable family with a **width axis** — Archivo, 62–125% width — gives
  condensed display (72%), card headlines (85%) and a normal-width UI (100%) from one file, with
  tabular numerals throughout. Choosing a single variable family is our engineering decision, not a
  sourced trend (T26).

## 6. Layout and UX — mobile and desktop best practice

| Practice | Source | In the prototype |
|---|---|---|
| Scores before stories: a results strip at the top of every page | the regional pattern (3.2), G4, G8 | the latest-results strip on every page |
| Visible navigation, not a hidden hamburger | S7 | desktop top nav; phone tab bar |
| A phone tab bar of 4–5 items | S8 | Home · Scores · Stats · Analysis · More |
| Touch targets ≥ 44×44 (Apple) / 48 dp (Android); WCAG floor 24×24 | S2, S4, S5, S6 | 44 px everywhere on phones, measured |
| Tables: sticky header and first column, let the user choose columns | S9 | compact phone table (#, team, P, GD, Pts) + "All columns"; sticky team column |
| "Load more", not infinite scroll, where the footer matters | S10 | analysis index |
| Light by default, dark available | S11, T9, ST4, ST7 | follows the system, with a toggle; tokenised both ways like FIFA (G6) |
| Charts: pick by relationship, label directly, never colour alone, data table for every chart | S12, S14, S15 | bars for rankings, lines for races, stacked bars for outcomes; H/D/A and W/D/L letters printed; "Show the numbers as a table" |
| Reflow to 320 px; no pinch-zoom blocking | S2, G4 | measured 0 px overflow at 375; normal viewport meta |
| Auto-updating tickers need a pause control; live scores are announced politely and in full | S2, S17 | the strip does not auto-move; the live specification is in `12-technical-design.md` |
| Core Web Vitals: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 | S1 | no images, one font family, 6 kB of JS; charts are HTML or small SVG |
| Structured data for articles, events and live blogs | S22, S23, DE3 | NewsArticle, SportsEvent, WebSite on the prototype pages |

## 7. Trust, automation and AI

- **EU AI Act Article 50 applies from 2 August 2026** (S26). AI-generated text published to inform
  the public must be disclosed, unless a human reviewed it and a named person or organisation holds
  editorial responsibility (S30). Spell-checking does not count as review (S27). Deepfakes and
  chatbots must always be disclosed. There is an EU icon set (S31).
- Readers prefer human-made news (I13). Unreviewed automated recaps drew criticism and carried
  errors (I32, I33). Corrections should be prompt, say what was wrong, and be listed publicly (S32).
  The Trust Project asks for labels on the type of work and a way for readers to report errors
  (S33).
- **Conclusion:** gameformative labels every piece (Analysis, Explainer, Automated, Season review).
  Its automated round-ups come from a fixed template, not a language model, and say so. Every
  article carries a "how this was made" note, and the site publishes its method, glossary,
  corrections and automation policy on one page ("How we count").

## 8. Proposals — and what was built from each

| # | Proposal | Built |
|---|---|---|
| P1 | A stats-led football site first; other sports when licensed data exists | football: five leagues and the World Cup; other sports not shown |
| P2 | Scores before stories: a latest-results strip on every page | yes |
| P3 | Off-white ground, ink navy, one blue and one orange — the leaders' structure on the 2027 forecast colours and the colour-blind-safe pair | yes, `05-design.md` |
| P4 | One variable family with a width axis; condensed display, wide UI, tabular numerals | yes, Archivo |
| P5 | Light default, dark available, both tokenised | yes |
| P6 | Visible nav: top nav on desktop, five-tab bar on phones | yes |
| P7 | Tables that work on a phone: compact by default, all columns on request, sortable, sticky team | yes |
| P8 | Every chart: direct labels, letters not only colour, the numbers as a table | yes |
| P9 | Data provenance on every page; licences checked before use; nothing estimated | yes: openfootball CC0; xG and live panels shown as not available |
| P10 | Labels, automation policy, corrections, a glossary — the Trust Project indicators and Article 50 | yes, "How we count" |
| P11 | A live match centre with a polite live region and a pause control | specified, not built: needs a licensed live feed (`13-implementation-plan.md`) |
| P12 | Women's football, cricket (for India) and NBA/CBA (for China) as regional expansions | not built: no open, licensed data verified (O3, O4, O5) |

## 9. What a next round would read

Rendered layouts and Core Web Vitals of the leaders, captured in a real browser; the blocked sites
(ESPN, The Athletic, kicker, ESPNcricinfo, FBref, Sofascore) from a browser session; the Chinese
sports apps; data-provider price lists (Opta/Stats Perform, Sportradar, Genius Sports) for the
licensed-data decision; and a sports-only device split from a paid panel.

## 10. Round 2 — what the research says about an articles-first launch (2026-09-25)

The owner moved the launch to articles (D17). The research supports it, and shapes how:

- **Trust is the product.** Trust in news is 37%, and readers prefer human-made news (I11, I13). The
  Trust Project asks for the type of work to be labelled, and for readers to be able to act on
  errors (S33). The owner's rule — every article lists the sources used and the sources investigated
  but not used — goes further than the usual practice: we saw no site in the benchmark that publishes
  what it looked at and set aside (we measured home pages, not every article page, so this is an
  observation, not a survey). It is the site's clearest point of difference.
- **Short, scannable pieces fit how people read now.** Discovery runs through feeds (I11). Readers
  arriving from a feed decide fast, so 800–3,200 characters under headings, with the headings listed
  at the top, suits them (S7 on visible navigation applies inside the article too).
- **Explaining the evidence is a gap worth taking.** The stats sites we measured (§3.3) are built
  around numbers, ratings and predictions. Stats Perform sells automation (I10, I16),
  and the automated recaps that went wrong (I32, I33) are the counter-model: gameformative explains,
  cites and signs.
- **The data work is not lost.** Data articles are one kind of article (Sport analytics), and the
  data pages become a later phase (§8 P1–P11 still hold for it).
