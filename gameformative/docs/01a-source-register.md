# Sources researched — the full register

*Every source the research for gameformative touched on 2026-09-25, with what it contributed. The
synthesis is `01-research.md`; the raw notes, fetch times and measurements are `01b-evidence.md`.*

**How to read the status column.**
**Measured** — the page was fetched with `curl` (desktop Chrome user agent, from Hungary) and its
HTML and CSS were counted by script. **Opened** — the page or document was read in full.
**Opened (secondary)** — the primary was blocked, so a named news write-up of it was read instead.
**Blocked** — the site refused the request (the reason is given). Nothing is said about its design.
**Snippet only** — seen only in a search-result summary. Not relied on for any figure in the
prototype or the presentation. **Projection** — a forecast by the named source, not a finding.

All fetches were made from a single Hungarian connection, with no JavaScript run. A geo-edition,
a consent pop-up or an advert added by script after page load is therefore not in these numbers.

## 1. The global sports sites the owner named

| # | Source | Status | What we learned |
|---|---|---|---|
| G1 | BBC Sport, [bbc.com/sport](https://www.bbc.com/sport) | Measured 18:35 UTC | React rendered on the server, all CSS inline; 682 kB HTML, 0.10 s to first byte. ReithSans/ReithSerif; light only (`color-scheme: only light`). The sport nav is Football, Cricket, F1, Rugby U, Tennis, Golf, Cycling, Athletics, More. No ad network in the HTML; a "Football Extra" newsletter block. |
| G2 | BBC Sport, [bbc.co.uk/sport](https://www.bbc.co.uk/sport) | Measured | Not the same page as .com: a different global nav, and it supports dark mode (`light dark`, 398 custom properties). One brand can serve two editions with different theme support. |
| G3 | ESPN, [espn.com](https://www.espn.com/) | **Blocked**: AWS WAF JavaScript challenge (HTTP 202) | Nothing about its design. Its March 2026 brand system is covered from its own press room (T19, T20). |
| G4 | NBA.com, [nba.com](https://www.nba.com/) | Measured | Next.js; the slowest first byte of the set, 5.1 s cold. Has a score strip, and a nav led by Games, Schedule, Watch, News, then Stats, Standings, Teams, Players, Fantasy. Fonts: Roboto family, Knockout, Action NBA Cond. `user-scalable=no` blocks pinch-zoom, an accessibility failure we avoid. |
| G5 | FIFA, [fifa.com/en](https://www.fifa.com/en) | Measured, but only an empty page | Renders entirely in the browser (an empty `#root`), so its nav and structure could not be read. theme-color `#020F2A`. Fonts: FIFASans, Poppins, Noto Sans, and the P26 family from widths ultra-condensed to expanded. |
| G6 | FIFA theme palette API (`cxm-api.fifa.com/…/themePalette`) | Measured | 38 palette sets, each with light and dark tokens (brandPrimary `#0a84ff`, textDefault `#03122B`). A large sports brand tokenises both themes, as we do. |
| G7 | The Athletic, [nytimes.com/athletic](https://www.nytimes.com/athletic/) | **Blocked**: DataDome captcha (HTTP 403) | Nothing about its design or paywall. Its business results are in I27 and I28. |
| G8 | Sky Sports, [skysports.com](https://www.skysports.com/) | Measured | Server-rendered; 0.11 s to first byte. A 2026 brand font plus a face per sport. Sections: Top Stories, **Live Sport**, Latest News, **Watch**, Pundits. An Opta widget font variable, Sourcepoint consent, Outbrain. The nav lists 15 sports. |

## 2. Which sites are the top ones — rankings by country

| # | Source | Status | What we learned |
|---|---|---|---|
| R1 | Similarweb, Top Sports Websites Germany, Aug 2026 | Opened (top 5 without login) | 1 kicker.de, 2 transfermarkt.de, 3 sportschau.de, 4 sport1.de. |
| R2 | Semrush, Most visited sports websites Germany, Aug 2026 | Opened | Same order as R1, with visits: kicker 77.67M, transfermarkt 51.83M, sportschau 20.03M, sport1 11.23M, sport.de 10.56M. Two independent panels agree. |
| R3 | IVW via sportjournalist.de, 12 May 2025 | Opened | kicker had 246M visits (April 2025). Sport1 left IVW on 31 Mar 2025, so IVW no longer compares the field. |
| R4 | Similarweb, Top Sports Websites India, Aug 2026 | Opened | 1 cricbuzz, 2 cricinfo, 3 a betting/fantasy site, 4 espncricinfo. Cricket dominates. |
| R5 | Similarweb, cricbuzz competitors, Aug 2026 | Opened | India country rank: cricbuzz #26, cricinfo #27, espncricinfo #312, NDTV Sports #856. |
| R6 | Semrush, India sports, Aug 2026 | Opened | Disagrees with R4: thehindu.com (whole domain) and sportskeeda first, with no cricbuzz. Panels differ, and we say so. |
| R7 | Comscore "Sports Highlights on Digital 2025 – India", via passionateinmarketing.com | **Blocked** (403); snippet only | Cricbuzz #1 with 53M unique visitors. Not used as a figure. |
| R8 | afaqs, 5 Apr 2021 (Comscore) | Opened | Sportskeeda was #2 in India during IPL 2020. Old context only. |
| R9 | Similarweb, sportskeeda.com, Aug 2026 | Opened | The US is its top country (36.81%), India 8.13%. That explains why it served us its US edition. |
| R10 | Similarweb `top-websites/china/sports/` | Opened | Has no China list; the URL serves the worldwide list. |
| R11 | Similarweb competitor pages (dongqiudi, sina sports), Aug 2026 | Opened | China ranks: hupu #28, zhibo8 #62, dongqiudi #628, sports.qq #975, sina sports #1,838. |
| R12 | Chinaz 体育综合 ranking, 20 Sep 2026 | Opened | An SEO score, not traffic: hupu, CCTV sport, sina, sohu, 163, qq. |
| R13 | Maigoo brand list, 11 Jun 2026 | Opened | An editorial index of apps and platforms (CCTV Sports, Migu, Tencent Sports, iQiyi, Dongqiudi, Hupu). Shows China's sport is app-first. |

## 3. Germany, India, China — the sites measured

| # | Site | Status | What we learned |
|---|---|---|---|
| DE1 | kicker.de | **Blocked**: DataDome (403) | The top German site could not be seen. sport.de (#5) was measured instead. |
| DE2 | transfermarkt.de | Measured | Data-first: "Tabelle" appears 183 times; nav includes Marktwerte, Wettbewerbe, Statistiken. Sourcepoint consent, with "Pur-Abo" pay-or-consent. Oswald and Source Sans variable fonts. Betting (Sportwetten) in the nav. |
| DE3 | sportschau.de | Measured | Public broadcaster: no ad or consent vendor. The fastest cold first byte of all, 0.074 s. The richest JSON-LD (32 NewsArticle). The only regional site with dark mode (a system setting or a cookie). Nav led by **Live & Ergebnisse**; "live-ticker" appears 93 times. |
| DE4 | sport1.de | Measured | WordPress and React, 78 scripts. Nav: Heute Live, Wetten & Spiele. Barlow font. |
| DE5 | sport.de | Measured | 977 links on the home page; "Liveticker" appears 89 times. A 30-plus-sport A–Z nav. Titillium Web; theme-color `#1c1c1c`; bookmakers ("Wettanbieter") in the nav. |
| IN1 | cricbuzz.com | Measured | Next.js. The first screen after the nav is a match carousel with live and finished scores. Nav: Live Scores, Schedule, Archives, News, Series, Teams, Videos, Rankings. Inter font. `user-scalable=no`. |
| IN2 | espncricinfo.com, IN3 cricinfo.com, IN4 sports.ndtv.com | **Blocked**: Akamai "Access Denied" (403) | Not described. |
| IN5 | sportskeeda.com | Measured — **US edition served** | NFL/NBA/MLB nav from our location, so its India layout was not observed. Inter and Barlow Condensed. |
| IN6 | sportstar.thehindu.com | Measured | Bootstrap; "scorecard" appears 95 times, "matchcenter" 27; a Statsman stats column; Piano paywall; Taboola. |
| IN7 | timesofindia.indiatimes.com/sports | Measured | Cricket-first nav (Cricket, Asian Games T20, IND vs AFG, Live Cricket Score). Rethink Sans; theme-color `#af2c2c`. |
| CN1 | hupu.com | Measured | China rank #28. Opens with a CBA/NBA fixture strip; community ("步行街") is central. No `lang` attribute, no viewport: a desktop-only page. System CJK fonts. |
| CN2 | zhibo8.com | Measured | The densest portal: 2,064 links, 34.9 per 10 kB. "直播" (live) appears 185 times and "比分" (scores) 59. 1.39 s cold first byte (served from China). |
| CN3 | dongqiudi.com | Measured | App-first (Nuxt): only 45 links. Opens with "today's important matches" and scores; asks visitors to download the app via a QR code. |
| CN4 | sports.qq.com | Measured | A Vue app shell with 14 links. DINPro and Blender Pro set only the numerals: a separate numeric face for scores. |
| CN5 | sports.sina.com.cn | Measured | The sport channel sits inside a general portal; 935 links. Element UI palette. |

## 4. Statistics and analytics sites

| # | Site | Status | What we learned |
|---|---|---|---|
| ST1 | fbref.com | **Blocked**: Cloudflare challenge (403) | Not described. |
| ST2 | theanalyst.com (Opta Analyst) | Measured | WordPress. Purple, magenta and orange; Big Shoulders Text and Lora; no dark mode. The Opta brand is itself the attribution. Content: Supercomputer predictions, Expected Points table, Power Rankings, FPL. Its tables render in the browser (0 in the HTML). |
| ST3 | sofascore.com | **Blocked**: JSON 403 from Varnish | Not described. |
| ST4 | fotmob.com | Measured | Next.js; dark mode; Inter. xG leaderboards, decimal player ratings, shot maps, percentile bars, heatmaps. **No data provider credited anywhere**, the opposite of what we do. |
| ST5 | basketball-reference.com | Measured | Server-rendered with system fonts. 50 sortable tables with glossary tooltips; "Data Provided By Sportradar" with a logo. The model for dense, citable tables. |
| ST6 | understat.com | Measured | Dark by default. xG, NPxG, PPDA and xPTS in its table; CSV, JSON and XLSX export. |
| ST7 | statmuse.com | Measured | Astro; dark mode with a toggle; plain-English question search; a Data & Glossary page; a betting ("Money") section. |
| ST8 | whoscored.com | **Blocked**: Cloudflare block page (403) | Not described. |

## 5. The industry — size, audience, business, AI

| # | Source | Status | What we learned |
|---|---|---|---|
| I1 | SportsPro, 2 Feb 2026 (Ampere data) | Opened (secondary) | **Projection:** streamers will spend US$14.2bn on sports rights in 2026, 7% more than 2025. Prime Video's share is US$3.8bn (27%). |
| I2 | IBC, 26 Nov 2025 (Ampere) | Opened (secondary) | **Projection:** rights spend reaches $78bn by 2030. Whether that is global is unclear in the text, so it is not used as a headline figure. US spend was $30.5bn in 2025. |
| I3 | Ampere Analysis, the article itself | Opened, no body returned | Nothing. |
| I4 | Consultancy.uk, 13 May 2026 (PwC Global Sports Survey 2026) | Opened (secondary) | Executives expect 7.4% annual growth; media rights 5.1% (down from 6.1%). 18–34s favour social highlights and creator-led content. |
| I5 | PwC primary pages (pwc.co.uk, pwc.ch) | **Blocked** (403) | Not read. |
| I6 | PwC sponsorship/ticketing rates, sample size | Snippet only | Not used. |
| I7 | Deloitte 2026 Global Sports Industry Outlook, 17 Feb 2026 | Opened | Media rights "continue to climb". Women's commercial revenue is growing at double digits. AI as the "connective engine". **Projection:** 20 stadiums open in 2027. |
| I8 | Statista, sports media rights by region 2025–2030 | Opened; figures paywalled | Only confirms that the Ampere series exists. |
| I9 | Statista, 2023 rights value | Snippet only | Not used. |
| I10 | Stats Perform, Opta Pulse launch, 12 May 2026 | Opened | Highlights produced "up to 80% faster": automation is the industry's direction. |
| I11 | **Reuters Institute Digital News Report 2026**, full PDF, 16 Jun 2026 | Opened in full | Social and video networks (54%) now beat publishers' own sites and apps (51%) for news. 10% use AI chatbots for news weekly. Trust 37%; 17% pay. **The report has no finding specific to sport**, and we attribute none to it. |
| I12 | Reuters Institute DNR 2025, executive summary | Opened | 27% want AI summaries of articles. Social video news use rose from 52% (2020) to 65%. |
| I13 | Reuters Institute, Generative AI and News Report 2025, 7 Oct 2025 | Opened | 12% are comfortable with fully AI-made news, against 62% for human-made. Hence our human-written copy, labelled automation and named editorial responsibility. |
| I14 | Stats Perform, About Opta Analyst | Opened | Opta Analyst has about 1 million monthly visitors and 55,000 newsletter subscribers. A benchmark for a stats-led publication. |
| I15 | Stats Perform on xG | Opened | xG is used by commentators, fantasy platforms and sportsbooks. It is the metric fans now expect, and it needs licensed data. |
| I16 | Stats Perform, Automated Insights | Opened | Sells automated previews and recaps, with no statement on human review. |
| I17 | Advanced Television / Nielsen, 1 May 2026 (second screen) | Snippet only | Not used. |
| I18 | Nielsen, Tops of Sports (for 2026) | Opened | 37% of the US population expected more interest in the 2026 World Cup. |
| I19 | Nielsen, Global Sports Report 2025 | Opened | 51% of people globally are football fans. Football is the right first sport. |
| I20 | Market-size vendors (Grand View and others) | Snippet only | Paid-report estimates; not cited. |
| I21 | FSGA industry research | Opened; figures members-only | Nothing usable. |
| I22 | Similarweb, platforms page, Aug 2026 | Opened | 66.55% of all web traffic worldwide is mobile. This is not sports-specific. |
| I23 | Similarweb, Top Sports Websites (worldwide), Aug 2026 | Opened | 1 espn, 2 marca, 3 cricbuzz, 4 cricinfo, 5 mlb. No device split. |
| I24 | Similarweb, fotmob.com and espn.com | Opened | FotMob: 26.9M visits over 3 months, 72.9% direct traffic. ESPN: 518.7M visits over 3 months. No device split. |
| I25 | ESPN desktop/mobile share | Snippet only, internally inconsistent | Not used. |
| I26 | TheNextWeb, 6 Aug 2026 (NYT Q2 2026) | Opened (secondary) | 13.4M digital subscribers; The Athletic is sold inside a bundle; AI search summaries are reducing referral traffic. |
| I27 | Nieman Lab, 5 Nov 2024 | Opened | The Athletic's first quarterly profit was $2.6m. |
| I28 | Axios on The Athletic; Yahoo Finance summaries | **Blocked** (403) / snippet only | Not used. |
| I29 | Deloitte UK, women's elite sport, 8 Apr 2026 | Opened | **Projection:** US$3bn revenue in 2026, up 340% since 2022. A clear expansion path; the prototype has no women's data yet (gap 7 in `03-sources.md`). |
| I30 | Nielsen, Women & Sports 2026 | Opened | 46bn minutes of women's sport watched in 2025, 71% more than in 2022. |
| I31 | Nielsen/PepsiCo on women's football by 2030 | Snippet only (projection) | Not used. |
| I32 | Awful Announcing, 14 Oct 2025 | Opened | MLS published AI recaps "not reviewed by editorial staff" and was criticised for thin copy. |
| I33 | Front Office Sports, 5 Sep 2024 | Opened | ESPN's AI recaps carried factual errors. Lesson: automation is labelled and reviewed. |
| I34 | Gannett/LedeAI recaps, 2023 | Snippet only | Not used. |

## 6. Open data — what the prototype may legally use

| # | Source | Status | What we learned |
|---|---|---|---|
| O1 | [openfootball/football.json](https://github.com/openfootball/football.json) | Opened; licence and files read | **CC0 1.0**: "Use as you please with no restrictions whatsoever". 2025/26 complete (23 league files), 2026/27 in progress (8 files). Results, plus goals and line-ups in the "-full" files; no xG. **The prototype's data source.** |
| O2 | [openfootball/worldcup.json](https://github.com/openfootball/worldcup.json) | Opened | CC0 1.0. The 2026 file has all 104 matches with results; the "-full" file adds scorers, line-ups, substitutions and attendance. |
| O3 | StatsBomb open data and its LICENSE.pdf (8 Sep 2023) | Opened | No redistribution and no commercial use ("commercially exploit the data or any analysis derived…"). **Not usable on a public or monetised site.** |
| O4 | NBA.com Terms of Use (13 Jul 2026) | Opened | Statistics are limited to news reporting or non-commercial use, with no betting or fantasy use. **Not usable as a data source.** |
| O5 | nflverse/nflverse-data | Opened (API metadata only) | GitHub lists it as CC-BY-4.0. Each dataset's terms need checking before NFL is added. |
| O6 | chadwickbureau/baseballdatabank; jalapic/engsoccerdata | Opened; no licence confirmed | Not used. |

## 7. Colour and design forecasts, sports identities

| # | Source | Status | What we learned |
|---|---|---|---|
| T1 | Pantone, Color of the Year 2026 press release, 4 Dec 2025 | Opened | **Cloud Dancer** (11-4201), "a billowy white" and a "structural anchor". It informed our warm off-white ground. |
| T2 | Pantone, Color of the Year 2026 page | Opened | No hex given. **The 2027 colour is not announced** (it normally comes in early December). |
| T3 | Young House Love, 2027 paint colours, updated 16 Sep 2026 | Opened | Paint brands' 2027 picks lean earthy and muted. Consumer paint, not a web forecast. |
| T4 | WGSN, Colour of the Year 2026: Transformative Teal, 3 Sep 2024 | Opened | Dark blue fused with aqua green. |
| T5 | WGSN, Key Colours A/W 26/27, 7 Oct 2024 | Opened | Transformative Teal, Wax Paper, Fresh Purple, Cocoa Powder, Green Glow. |
| T6 | **WGSN × Coloro, Colour of the Year 2027, 29 Apr 2025** | Opened — **projection** | **Luminous Blue** (125-28-38); S/S 27 key colours are Energy Orange, Pop Pink, Meadowland Green and Clay. The basis of our blue and orange (our own sRGB readings; no hex is published). |
| T7 | FashionUnited, A/W 27/28 key colours, 17 Sep 2025 | Opened — projection | Russet, Peaceful Lilac, Maize, Deep Green. |
| T8 | Adobe Express, Top 10 graphic design trends 2026, 12 Dec 2025 | Opened | Oversized playful type, saturated palettes, tactile texture, freeform editorial layouts. |
| T9 | Figma, Top Web Design Trends 2026 | Opened | **Dark mode as a standard feature**, bold and kinetic type, retrofuturism with neon accents, motion. |
| T10 | Figma, State of the Designer 2026 | Opened; data gated | Survey figures seen as snippet only; not used. |
| T11 | Shutterstock, 2025 Creative Impact Report | Opened | No colour trends. Believability drops after three campaign messages. |
| T12 | WebFX, "Web Design Trends in 2027", 10 Oct 2025 | Opened — projection (agency) | Includes data-driven design, real-time content and dark mode. |
| T13 | Graticle, "Way Too Early 2027 Web Design Predictions" | Opened — projection (agency) | "Proof of personhood" (signals that a human made it); personalised homepages. |
| T14 | 1000logos, FIFA World Cup 26 identity, 23 May 2023 | Opened | The first emblem with a photographic trophy; 16 host-city colourways; a custom typeface with Noto Sans secondary. |
| T15 | Pimp my Type, FIFA 2026 typography, 18 Jun 2026 | Opened | Ultra-condensed black type breaks down at small UI sizes. **Use condensed type for display, wider cuts for UI**, which is exactly our type rule. |
| T16 | Vasava, UEFA Champions League 24/27 rebrand | Opened | A prismatic "refracted" display face; "more colourful, bolder and younger". |
| T17 | UEFA, 2024 final identity, 31 Aug 2023 | Opened | A new artist-led identity for each final. |
| T18 | Creative Bloq (Mutabor), Bundesliga identity, 16 Feb 2026 | Opened | Moves from flat design to texture, 3D and a new "tape-like" font; "motion first". |
| T19 | Marketing Brew, ESPN brand identity, 9 Mar 2026 | Opened | ESPN's first formal guidelines. The custom "Ignite" face is slanted 7°. **One red chosen for accessibility and digital visibility.** |
| T20 | ESPN Press Room, 27 Mar 2026 | Opened | The "speedline" motion device; a system built from phone icon to billboard. |
| T21 | Design Week, Sky Sports redesign, 15 Oct 2025 | Opened | One five-weight custom face replaced six sport fonts; "live is still king". |
| T22 | Premier League, digital relaunch, 1 Jul 2025 | Opened | Matchday Live, vertical Matchday Stories, personalisation, an AI assistant over 30+ seasons of data. |
| T23 | Sports Video Group, NBA on NBC/Peacock, 21 Oct 2025 | Opened | Live data overlays, "Key Play Catch-Up", vertical highlights. |
| T24 | ScoreVision, sports graphics trends 2025–26, 6 Aug 2025 | Opened | Bold condensed type for screens; neon and glow accents for stats. |
| T25 | NewscastStudio (ESPN college football), Design Week (FIFA) | **Blocked** (403) | Not used. |
| T26 | Tottenham variable font; Premier League 2016 identity details | Snippet only | Not used. |

## 8. Standards and best practice

| # | Source | Status | What we learned |
|---|---|---|---|
| S1 | web.dev, Web Vitals (updated 31 Oct 2024) | Opened | LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1, measured at the 75th percentile. Our performance budget. |
| S2 | W3C, WCAG 2.2 (12 Dec 2024) | Opened | 4.5:1 text contrast; 3:1 for UI and chart marks; colour never alone; reflow at 320 px; **pause control for anything auto-updating over 5 s (score tickers)**; focus not obscured by sticky headers; 24×24 minimum targets. |
| S3 | W3C WAI, Understanding 2.4.13 Focus Appearance | Opened | It is AAA, not AA. We meet it anyway with a 3 px outline. |
| S4 | W3C WAI, Understanding 2.5.8 Target Size | Opened | 24×24 is the AA floor. We build 44×44 on phones. |
| S5 | Apple Human Interface Guidelines, Accessibility | Opened | 44×44 pt default touch target. |
| S6 | Google Android Accessibility Help, touch targets | Opened | 48×48 dp with 8 dp spacing. |
| S7 | Nielsen Norman Group, hidden vs visible navigation, 24 Jul 2016 | Opened | Visible navigation is found and used more than a hamburger menu. We use a visible tab bar on phones and a visible top nav on desktop. |
| S8 | NNG, Basic Patterns for Mobile Navigation, 15 Nov 2015 | Opened | A tab bar suits 4–5 items. Ours has five, the fifth being "More". |
| S9 | NNG, Mobile Tables, 17 Sep 2017 | Opened | Sticky header and first column, clear scroll cues, let users choose columns. We have a compact phone table with "All columns". |
| S10 | NNG, Infinite Scrolling, 4 Sep 2022 | Opened | "Load more" beats infinite scroll when users need the footer. We use "Load more" on the analysis index. |
| S11 | NNG, Dark Mode vs Light Mode, 2 Feb 2020 | Opened | Light performs better for most readers. Offer dark, don't force it. We follow the system setting, default light, with a toggle. |
| S12 | Datawrapper, colours for colour-blind readers, 23 Jun 2020 | Opened | Blue with orange is the safest pair; label directly; "get it right in black & white". Our chart palette and direct labels. |
| S13 | Okabe & Ito, Color Universal Design | Opened | The standard colour-blind-safe palette (no hex in the text). |
| S14 | W3C WAI, Complex Images tutorial (8 Apr 2026) | Opened | Every chart gets a text alternative and its data as a table. We have "Show the numbers as a table" on every chart. |
| S15 | Financial Times, Visual Vocabulary | Opened | Choose the chart by the relationship shown: ranking → bars, change over time → lines, part-to-whole → stacked bars. |
| S16 | MDN, `prefers-reduced-motion` | Opened | Honoured site-wide. |
| S17 | MDN, ARIA live regions | Opened | Scores in a polite, atomic live region; tickers are not live regions by default. Used for sort announcements now and specified for live scores. |
| S18 | Bootstrap 5.3 and Tailwind breakpoints | Opened | Common breakpoints. Ours are 720 and 1000, plus reflow to 320. |
| S19 | StatCounter, desktop vs mobile, Aug 2026 | Opened | Worldwide, all web: mobile 49.36%, desktop 49.11%. Both widths matter. |
| S20 | Reuters Institute DNR 2026 and 2025, executive summaries | Opened | See I11 and I12. |
| S21 | Press Gazette / Reuters Institute on live blogs, 20 Jun 2013 | Opened (old data) | Readers value visible corrections on live pages. |
| S22 | schema.org LiveBlogPosting | Opened | Markup for the live match pages of the real build. |
| S23 | Google Search Central, video structured data (24 Sep 2026) | Opened | BroadcastEvent gives a LIVE badge; Clip or SeekToAction give "key moments". |
| S24 | Premier League, Match Centre explainer series, 21 Feb 2025 | Opened | "Why did that happen" explainers as a format. |
| S25 | Opta Analyst, football stats definitions, 23 Jul 2024 | Opened | xG, xA, big chance and PPDA defined by the provider. A glossary names its provider because definitions differ. |
| S26 | European Commission, "Safer and more transparent AI", 2 Aug 2026 | Opened | **EU AI Act Article 50 applies from 2 Aug 2026.** |
| S27 | European Commission FAQ, Article 50, 24 Jul 2026 | Opened | Human review means "deliberate examination of the substance"; spell-checking does not count. |
| S28 | Cooley, 3 Aug 2026 | Opened | Guidelines adopted 20 Jul 2026. Fines up to €15m or 3% of turnover. |
| S29 | WAN-IFRA Editors Weblog, 7 Jul 2026 | Opened | The Digital Omnibus did not defer Article 50. Machine-readable marking has a grace period to 2 Dec 2026. |
| S30 | artificialintelligenceact.eu, Article 50 text | Opened | 50(4): AI-generated public-interest text must be disclosed unless human-reviewed under someone's editorial responsibility. Our automation policy. |
| S31 | European Commission, Code of Practice on AI-generated content (final 10 Jun 2026) | Opened | There is a standard EU icon set for labelling. |
| S32 | BBC Editorial Guidelines 3.4.34, Correcting Mistakes | Measured (curl) | Correct promptly, say what was wrong, keep a public corrections page. Our corrections policy. |
| S33 | The Trust Project, Trust Indicators | Opened | Eight indicators, including the type of work (news, analysis, opinion) and actionable feedback. Our labels and the How we count page. |
| S34 | Nieman Lab on the Guardian live-blog format; live-blog "difficult to understand" statistic | **Blocked** (403) / snippet only | Not used. |

## 9. Article sources checked (round 2, 2026-09-25)

The sources behind the articles. Each article lists its own; this is the record of the check.

| # | Source | Status | What we learned |
|---|---|---|---|
| AR1 | Sport Mont 2026, "Wearable-Monitored External Workload (GPS/GNSS/IMU) and Lower-Limb Muscle Injuries in Football" (doi 10.26773/smj.260219) | Opened (abstract) | Twelve studies, four pooled. Odds-ratio pooling gave no significant link (OR 1.33, 0.85–2.07); relative-risk pooling gave more than double the risk (RR 2.33, 1.65–3.30). Speed zones, sprint metrics and ACWR formulas "varied substantially". The seed of the GPS article. |
| AR2 | Frontiers in Public Health, 13 Aug 2026, "Acute:chronic workload ratio and load management for team sports: a multilevel meta-analysis" | Opened (abstract) | 16 studies, 797 athletes: a small-to-moderate link (g = 0.35); the ratio is "not supported … as a stand-alone causal or predictive model". |
| AR3 | PMC11366842, machine learning and training load in soccer (Sensors) | Opened (abstract) | 25 professional players with a first non-contact muscle injury; ML on external and internal load. Investigated, not used by the article. |
| AR4 | Sensors (MDPI), doi 10.3390/s26134228 | **Blocked** (403) | Not read; listed by the draft as investigated, not used. |
| AR5 | Discover Artificial Intelligence (Springer), doi 10.1007/s44163-026-01021-9 | **Blocked** (JavaScript challenge) | Not read; listed by the draft as investigated, not used. |
| AR6 | Flashscore España, LaLiga tie-break criteria | Opened | For two teams level on points, the goal difference in the matches between them comes first; three or more teams use a mini-table of their matches. |
| AR7 | DAZN Italia, Serie A "chi vince a pari punti" | Opened | Head-to-head points first, then head-to-head goal difference, overall goal difference, goals, a draw; a play-off (spareggio) for the title. |
| AR8 | 365Scores, LaLiga tie-break criteria | **Failed** (HTTP 500) | Not read; listed as investigated. |

## What we did not research, and why

- **Paid panels** (Similarweb Pro, Comscore, Nielsen full reports, Statista) are behind logins or
  paywalls. Where only a summary was public, only the summary is used.
- **Rendered layouts of external sites** were not captured. The owner declined opening external
  sites in the in-app browser on 2026-09-25, so it was used only for the local prototype, and
  everything in sections 1–4 comes from the HTML and CSS as served.
  Computed colours, rendered layout and Core Web Vitals of those sites are therefore not measured.
- **Chinese mobile apps**, where most of that market's sports consumption happens (R13, CN3), were
  not examined; only their websites were.
