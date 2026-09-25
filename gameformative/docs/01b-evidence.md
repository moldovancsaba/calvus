# Evidence — the research notes in full

*The complete working notes behind `01-research.md` and `01a-source-register.md`, kept as written on 2026-09-25 so every figure in the synthesis can be traced to the fetch or page it came from. Four research passes ran the same day; each is reproduced below with its method, timestamps, raw measurements and limitations. Local working-file paths were removed; nothing else was edited.*

## A. Global sites — BBC Sport, ESPN, NBA.com, FIFA, The Athletic, Sky Sports

**When:** 2026-09-25. Main fetch batch started 18:35:12 UTC and ran until 18:35:20 UTC. The FIFA palette and JS were fetched at 18:37:22 UTC. The ESPN and Athletic retry ran at 18:37:35 UTC.
**Where from:** the egress IP geolocates to **HU (Hungary)** (ipinfo.io/country). The CDN POPs seen were CloudFront BUD50 (ESPN) and Fastly SOF (NYT). All results are from a non-UK, non-US vantage point.
**Client:** `curl -s -L --compressed -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" -H 'Accept-Language: en-GB,en;q=0.9' -H 'Accept: text/html,...' -w '%{http_code} %{time_starttransfer} %{time_total} %{size_download} %{url_effective}'`

Caveats that apply to all sites:

- `size_download` is the **compressed transfer size**. "HTML bytes (decoded)" is the size after decompression.
- TTFB is `time_starttransfer` from a single HU vantage point. Run 2 was immediately after run 1, so it is likely edge-warm.
- Colour counts are raw textual occurrences of hex (3/6/8-digit, 3-digit expanded) and `rgb()/rgba()` in HTML plus the fetched CSS. They are not weighted by rendered area. A few hex-like fragments (e.g. `#add`) could be false positives.
- "Third-party keywords" means a substring appears in the HTML. It proves a reference, not that a tag fired.
- Keyword counts include class names, JSON and scripts, so they are clues, not UI counts.

### Summary table

| | BBC Sport (.com) | BBC Sport (.co.uk) | ESPN | NBA.com | FIFA | The Athletic | Sky Sports |
|---|---|---|---|---|---|---|---|
| HTTP status | 200 | 200 | **202, AWS WAF JS challenge** | 200 | 200 (SPA shell) | **403, DataDome captcha** | 200 |
| Final URL | bbc.com/sport | bbc.co.uk/sport (no redirect) | espn.com/ | nba.com/ | fifa.com/en | nytimes.com/athletic/ | skysports.com/ |
| Transfer size | 73,339 | 75,715 | 1,988 | 66,937 | 1,884 | 771 | 51,572 / 51,573 |
| HTML decoded | 682,291 | 701,013 | (challenge page) | 496,678 | 4,555 | (block page) | 591,057 |
| TTFB run1 / run2 (s) | 0.102 / 0.059 | 0.292 / 0.050 | 0.025 / 0.014 (challenge) | **5.109 / 1.244** | 0.161 / 0.138 | 0.145 / 0.147 (403) | 0.113 / 0.054 |
| Framework | React SSR (react-helmet `data-rh`, `window.__INITIAL_DATA__`), CSS-in-JS | same | n/a | **Next.js pages router** (`__NEXT_DATA__`, `/_next/`, gssp) | **Client-rendered React SPA** (empty `#root`, CRA-style `static/js/main.[hash].js`, react-dom/createRoot in bundle) | n/a | Server-rendered, no JS framework marker; `sdc-site-*` / `ui-sitewide-*` components |
| `<script>` tags (with src) | 63 (55) | 62 (54) | n/a | 45 (39) | 7 (6) | n/a | 42 (2; 18 are `text/template`) |
| Stylesheet links / inline `<style>` | 0 / 3 | 0 / 3 | n/a | 8 / 1 | 1 / 0 | n/a | 2 / 1 |
| theme-color | #FFFFFF | #FFFFFF | n/a | #000000 | #020F2A | n/a | #002A91 |
| color-scheme meta | `only light` | `light dark` | n/a | none | none | n/a | none |
| prefers-color-scheme in HTML+CSS | 0 | 2 (dark) | n/a | 5 (dark) | 1 (dark), plus API palette with light/dark sets | n/a | 1 (dark) |
| Manifest | yes | yes | n/a | yes | yes | n/a | yes |
| Primary fonts | ReithSans / ReithSerif | same | n/a | Roboto, Roboto Condensed/Slab, Knockout, Action NBA Cond | FIFASans, Poppins, Noto Sans, P26 family | n/a | Sky Text, Sky Headline, Sky Sports Brand 2026 |
| lang | en-GB | en-GB | (challenge: en) | en | en | (block: en) | en |
| Viewport | width=device-width, initial-scale=1 | same | n/a | ...maximum-scale=1, **user-scalable=no** | width=device-width,initial-scale=1 | n/a | ...minimum-scale=1, viewport-fit=cover |
| JSON-LD types | CollectionPage, NewsMediaOrganization, ImageObject, ItemList | same | n/a | WebPage x2, SportsOrganization, Organization, BreadcrumbList, ListItem | none | n/a | Organization, ImageObject, Person, PostalAddress, ContactPoint, WebSite |
| Ads/consent/analytics refs | chartbeat, comscore, optimizely, permutive, piano, segment | + scorecardresearch | n/a | securepubads.g.doubleclick, tealium, braze, newrelic, segment, akamai | OneTrust (cdn.cookielaw.org), Adobe DTM, Conviva, THEOplayer, PingOne (CSP allows many more) | n/a | GTM, google-analytics, googlesyndication, Sourcepoint (privacy-mgmt), Outbrain, Adobe DTM, Chartbeat, Qualtrics, dotmetrics |

### BBC Sport: https://www.bbc.com/sport and https://www.bbc.co.uk/sport

**Fetch results**

- bbc.com: runs at 18:35:13 UTC returned 200. TTFB 0.102197 / 0.059134 s, total 0.116 / 0.072 s. 73,339 bytes transferred, 682,291 decoded. Final URL `https://www.bbc.com/sport`.
- bbc.co.uk: 200. TTFB 0.292003 / 0.049771 s, total 0.307 / 0.064 s. 75,715 bytes transferred, 701,013 decoded. No redirect to .com from the HU IP.

**Platform and assets**

- Platform hints: 48 `data-rh="true"` attributes (react-helmet), plus `window.__INITIAL_DATA__`, `__WEBAPP_CONFIG__`, `__REQUEST_CONTEXT__` and `__ENVIRONMENT_VARIABLES__`. Emotion-style `css-xxxxx` classes. No `__NEXT_DATA__`, `_next/`, Nuxt or AMP markers. No generator meta.
- Scripts: .com has 63 tags (55 with src), .co.uk has 62 (54). No `<link rel=stylesheet>`; all CSS is inline in 3 `<style>` blocks (161,687 B on .com, 182,589 B on .co.uk).
- Domains referenced: static.files.bbci.co.uk, ichef.bbci.co.uk, feeds.bbci.co.uk, account.bbc.com, cloud.email.bbc.com, plus social links. .co.uk also references sb.scorecardresearch.com.
- Third-party substrings found: chartbeat, comscore, optimizely, permutive, piano, segment. No doubleclick, GTM, OneTrust, Sourcepoint, Taboola or Outbrain in the HTML.

**Theme and dark mode**

- theme-color is `#FFFFFF` on both. Manifest: `https://static.files.bbci.co.uk/core/manifest.11b0cb15....json`.
- **color-scheme differs:** .com has `only light`. .co.uk has `light dark`, with 2 `prefers-color-scheme: dark` occurrences and 398 CSS custom properties (26 on .com).

**Fonts**

- @font-face families: ReithSans (10), ReithSerif (10), ReithRounded (2), ReithSemiRounded (2).
- Dominant stack: `ReithSans,Helvetica,Arial,freesans,sans-serif` (82 occurrences).

**Top 10 colours**

- .com: #000000 86, #ffffff 67, #c8c8c8 54, #181818 48, #ffd230 20, #f8f8f8 16, #606060 14, #387b12 14, #787878 12, #f0f0f0 10.
- .co.uk: #ffffff 357, #000000 222, #181818 166, #f8f8f8 114, #f0f0f0 84, #c8c8c8 54, #505050 50, #202020 42, #d8d8d8 32, #ff4c98 30.

**Navigation**

- Global nav on .com: Home, News, Sport, Business, Technology, Health, Culture, Arts, Travel, Earth, Audio, Video, Live.
- Global nav on .co.uk: Home, News, Sport, Earth, Reel, Worklife, Travel, Culture, Future, Music, TV, Weather, Sounds. The editions differ.
- Sport nav (both): Home, Football, Cricket, Formula 1, Rugby U, Tennis, Golf, Cycling, Athletics, More. The "More" menu adds an A–Z of 23 sports plus England/Scotland/Wales/Northern Ireland, Quizzes and News Feeds.

**Page structure**

- h2 section headings (13): [lead story], Video, More sports news, More news & analysis, More video, Only from the BBC, "Insight: Must-read sports stories", More to explore, Our latest podcasts, **Football Extra newsletter**, Things you need to know, Find us here, Find out more.
- 74 `data-testid="promo"` cards and 6 `spc-container`.
- No "most read" string, no app-store prompts, and no ticker class found in the static HTML.
- "live" occurs 1,009–1,040 times, mostly in data and class names; "fixtures" 19, "scores" 31.

**JSON-LD:** CollectionPage, NewsMediaOrganization, ImageObject, ItemList.
**lang and viewport:** en-GB; `width=device-width, initial-scale=1`.

### ESPN: https://www.espn.com/

**Blocked. Nothing about the site's design was measured.**

- Both runs at 18:35:13 UTC and a retry at 18:37:35 UTC returned **HTTP 202**. The response was 1,988 bytes, TTFB 0.025 / 0.014 / 0.013 s, final URL `https://www.espn.com/`.
- Headers: `server: CloudFront`, `x-amzn-waf-action: challenge`, `x-cache: Error from cloudfront`, POP `BUD50-P3`.
- The body is an AWS WAF JavaScript challenge page (loads `...token.awswaf.com/.../challenge.js`, empty `challenge-container`). Its noscript text says JavaScript is required to verify the visitor is not a robot.
- The challenge was not bypassed. Every design field is unmeasured. A real browser session would be needed.

### NBA.com: https://www.nba.com/

**Fetch results:** 200 at 18:35:13 UTC. **TTFB 5.109417 s on run 1 and 1.244413 s on run 2**, the slowest of the set. Total 5.120 / 1.257 s. 66,937 bytes transferred, 496,678 decoded.

**Platform and assets**

- **Next.js pages router.** `__NEXT_DATA__` is present (231,777 B of JSON), with `page: "/[[...root]]"`, `gssp: true` (getServerSideProps) and buildId `C0E7a9q2u2RKy38vn91Q2`. Assets are under `/_next/static/`.
- Scripts: 45 tags, 39 with src. 8 stylesheet links plus 1 inline `<style>`. The first 4 CSS files were fetched, at 244,918, 16,724, 2,975 and 3,735 bytes (all 200).
- Third-party refs: securepubads.g.doubleclick.net, tags.nba.com (Tealium substring present), fonts.googleapis.com / gstatic, braze, newrelic, segment, akamai. There is no OneTrust or Sourcepoint substring.

**Theme and dark mode**

- theme-color `#000000`. Manifest `/site-manifest.json`. No color-scheme meta.
- 5 `prefers-color-scheme: dark` occurrences in the fetched CSS. 428 custom properties.

**Fonts**

- @font-face: Roboto (40), Roboto Condensed (16), Roboto Slab (16), Action NBA Cond Web (3), Knockout, Knockout Wide, and a full WNBA family set.
- Common values: `var(--font-body)`, `Knockout Wide,sans-serif`, `var(--font-table)`.

**Top 10 colours:** #000000 359, #ffffff 331, #0268d6 227, #1d428a 225, #f6f6f6 216, #c8102e 215, #e7e7e7 214, #222222 213, #f2aa32 210, #d0021b 210. The counts are clustered around 210–227, which suggests a repeated team-colour table in the CSS.

**Navigation:** top-level header items from `__NEXT_DATA__.props.pageProps.layout.header.links` are Games, Schedule, Watch, News, Season Preview, NBA Cup, Stats, Standings, Teams, Players, NBA Play, Fantasy, (Spacer), League Pass, Store, Tickets, Affiliates.

**Page structure**

- `ScoreStrip` (2), `scorestripCalendar`, `scoreStripBroadcasterLimit`, `ScoreStripLocalization` and `scoreboard` are present, so there is a **score strip**.
- "watch" 164, "video" 169, "standings" 40, "podcast" 19, "newsletter" 4.
- "app store" and "google play" appear 2 each, which points to app links.
- Only 5 h2s, which are story headlines such as "Live updates: 2026 Dallas Mavericks media day".

**JSON-LD:** WebPage x2, SportsOrganization, Organization, BreadcrumbList, ListItem.
**lang and viewport:** lang `en`. Viewport `width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no`. This disables pinch-zoom, which is an accessibility flag.

### FIFA: https://www.fifa.com/en

**Fetch results:** 200 at 18:35:20 UTC. TTFB 0.161 / 0.138 s. 1,884 bytes transferred, 4,555 decoded. Final URL `https://www.fifa.com/en`. Response headers show Azure Front Door plus Akamai (`akamai-grn`, `_abck`/`bm_sz` Bot Manager cookies). It was not blocked.

**Platform and assets**

- **Client-rendered SPA.** The body is only `<div id="root"></div>`, so there is **no server-rendered content, nav or JSON-LD**. Those fields are unmeasurable without executing JS.
- Bundle `/static/js/main.433c8b28.js` (302,555 bytes transferred) contains `react-dom`, `createRoot` and `__reactFiber`. That points to React, in a CRA-style build layout.
- Scripts: 7 tags (6 with src) plus 1 stylesheet, `/static/css/main.7c0c488d.css` (171,082 bytes transferred, 200).
- HTML refs: cdn.cookielaw.org and geolocation.onetrust.com (**OneTrust**), assets.adobedtm.com, THEOplayer, Conviva, PingOne (auth), cxm-api.fifa.com.
- The CSP header *allows* doubleclick, googletagmanager, googlesyndication, tealium, facebook, tiktok, snapchat and others. That shows they are permitted, not that they loaded.

**Theme and dark mode**

- theme-color `#020F2A`. Manifest `/manifest.webmanifest`. No color-scheme meta.
- 1 `prefers-color-scheme: dark` in CSS. 227 custom properties.
- **Theme palette API** (`https://cxm-api.fifa.com/fifaplusweb/api/themePalette`, preloaded by the page, 200, 6,069 bytes transferred): 38 palette entries, each with `light` and `dark` token sets. The first entry's light tokens are brandPrimary #0a84ff, brandSecondary #045694, brandTertiary #f43056, bgPrimary #EEF2FB, textDefault #03122B, success #30D158, warning #FF9F0A.

**Fonts**

- Preloaded woff2: noto-sans-700, noto-sans-italic, noto-sans-regular, poppins-500/600/italic.
- @font-face: FIFASans Regular/Medium/Bold/Italic; Poppins; Noto Sans; P26 UltraCondensed/Condensed/Normal/Expanded/SemiExpanded; Open Sans; FFVideoFont.
- Main value: `var(--fcds-fifa-font-primary)` (132), with stack `FIFASans Regular, Poppins, Noto Sans, Helvetica Neue, Arial`.

**Top 10 colours (HTML + main CSS):** #ffffff 294, #000000 119, #00b8ff 63, #505b73 47, #e4e8f0 46, #0070df 42, #03122b 37, #00182f 36, #a5acbb 35, #020f2a 30.

**Navigation, structure and JSON-LD:** not measurable, because the static HTML is empty. "standings" appears 3 times, but only in the `ENABLED_FEATURES` config string (e.g. FIFA20MatchRail, FIFA20Standings, FIFA20VerticalVideo, FIFA20Shop).
**lang and viewport:** lang `en`, `dir="ltr"`. Viewport `width=device-width,initial-scale=1`.

### The Athletic: https://www.nytimes.com/athletic/

**Blocked. Nothing about the site's design was measured.**

- Both runs at 18:35:20 UTC and a retry at 18:37:35 UTC returned **HTTP 403**. The response was 771 bytes, TTFB 0.145 / 0.147 / 0.250 s.
- Headers: `server: DataDome`, `x-datadome: protected`, `x-datadome-riskscore: 0.86`, `x-nyt-route: ta-home-lohp`, `x-gdpr: 1`.
- The body loads a `geo.captcha-delivery.com` / `ct.captcha-delivery.com` captcha and shows "Please enable JS and disable any ad blocker".
- The captcha was not bypassed. The paywall status could not be assessed. Every design field is unmeasured.

### Sky Sports: https://www.skysports.com/

**Fetch results:** 200 at 18:35:20 UTC. TTFB 0.113 / 0.054 s, total 0.122 / 0.061 s. 51,572 / 51,573 bytes transferred, 591,057 decoded. Final URL unchanged.

**Platform and assets**

- Server-rendered HTML with no framework marker: no Next, Nuxt, React root or AMP. BEM-style components: `sdc-site-carousel` (935 class hits), `sdc-site-tile`, `ui-sitewide-main-nav`, `ui-tile-live-event`, `sdc-site-pundits`. There are also 2 `type="module"` scripts.
- Scripts: 42 tags, only 2 external. 18 are `text/template` login templates.
- 2 stylesheets were fetched: site-main-sass (85,449 bytes transferred) and site-main (12,365 bytes transferred).
- Third-party refs: googletagmanager, google-analytics, googlesyndication, **Sourcepoint** (`privacy-mgmt`), **Outbrain**, Adobe DTM, Chartbeat, Qualtrics, dotmetrics.
- Domains: e0.365dm.com (images, 127 refs), skybet.com, news.sky.com, nowtv.com.

**Theme and dark mode**

- theme-color `#002A91`. Manifest `/assets/manifest.json`. No color-scheme meta.
- 1 `prefers-color-scheme: dark` in CSS. 730 custom properties, the most of the set.

**Fonts**

- @font-face: "Sky Sports Brand 2026" (4), Sky Text (2), Sky Headline (+ fallback), Sky Display, and per-sport faces: Sky Football, Sky Premier League, Sky Cricket, The Hundred, Sky F1, Sky Golf.
- Main value: `var(--sports-branding-skysports-font),"Sky Text"`.

**Top 10 colours:** #ffffff 161, #000000 25, #f4f5f7 18, #e2e2e2 17, #4a4a4a 15, #214cb8 14, rgba(0,0,0,.2) 14, #0a1388 12, rgba(0,0,0,.1) 11, #707070 10.

**Navigation**

- Main nav: Football, F1, Cricket, Rugby Union, Rugby League, Golf, Boxing, NFL, Tennis, NBA, Racing, Darts, Netball, MMA, More Sports.
- Footer/utility nav: Podcasts, Upcoming on Sky, Get Sky Sports, **Sky Sports App**, Sky Sports with no contract, Kick It Out, British South Asians in Football.

**Page structure**

- h2 sections: Top Stories, **Live Sport**, Don't Miss These, Latest News, **Watch**, Around Sky, Pundits, Features, Shows and Podcasts.
- `ui-tile-live-event` appears 44 times (live-event tiles). There is an Opta widget font variable (`--opta-widget-brand-font`), which suggests Opta scores widgets.
- No "newsletter" and no "most read" strings. 3 advert slots (`ui-advert-slot`).

**JSON-LD:** Organization, ImageObject, Person, PostalAddress, ContactPoint, WebSite. No NewsArticle or SportsEvent.
**lang and viewport:** lang `en`. Viewport `width=device-width, initial-scale=1.0, minimum-scale=1, viewport-fit=cover`.

### Not measured, and why

- **ESPN and The Athletic:** bot walls (AWS WAF challenge and DataDome captcha). They cannot be measured without a real browser, so no design facts are recorded.
- **FIFA:** nav, page structure and JSON-LD are rendered client-side and are absent from the static HTML.
- **CSS coverage:**
  - NBA: only 4 of 8 stylesheets were fetched.
  - Sky: CSS injected by JS modules was not captured.
- **Rendered values:** none of the sites were measured for computed colours, layout, CWV (LCP/CLS/INP) or JS-injected third parties. That would need a headless browser.
- **"Most read":** no site's static HTML contained the string, and it may be loaded client-side.
- **Vantage point:** all results are from Hungary. UK or US edition content and geo-gating may differ (e.g. BBC .co.uk was served without a redirect to .com).

## B. Germany, India, China — the top sports sites by country

Prepared 2026-09-25. All measurements were fetched between 2026-09-25T18:38Z and 18:43Z with curl 
(UA: desktop Chrome 140 on macOS, `-L --compressed`, `Accept-Language: en-US`). **Vantage point: Hungary** 
(`ipinfo.io/country` = HU; CloudFront POP `BUD50` and Cloudflare `-BUD` in response headers). So geo-served 
`curl-results.txt`, `analysis.json`, `analyze.py`.

### 1. Which sites are "top" (sourced rankings)

#### Germany
| Source (date) | Order |
|---|---|
| Similarweb "Top Sports Websites Ranking in Germany", Aug 2026 (updated 2026-09-01) — https://www.similarweb.com/top-websites/germany/sports/ (only top 5 visible without login) | 1 kicker.de, 2 transfermarkt.de, 3 sportschau.de, 4 sport1.de, 5 cruzswim.org |
| Semrush "Most visited sports websites in Germany", Aug 2026 — https://www.semrush.com/website/top/germany/sports/ | 1 kicker.de 77.67M, 2 transfermarkt.de 51.83M, 3 sportschau.de 20.03M, 4 sport1.de 11.23M, 5 sport.de 10.56M, 6 fupa.net 7.41M, 7 flashscore.de 7.27M, 8 fussballtransfers.com 7.21M, 9 spox.com 7.01M |
| IVW (via VDS/sportjournalist.de, published 2025-05-12) — https://www.sportjournalist.de/news/meldungen-und-medien/auch-sport1-hat-die-online-ivw-verlassen-fb-3979/?news%5Bnr%5D=3979 | kicker 246.01M visits (Apr 2025), far ahead of other IVW-measured sports sites. Sport1 left Online-IVW on 2025-03-31, so IVW no longer compares the field. |

**Picked top 4: kicker.de, transfermarkt.de, sportschau.de, sport1.de.** Two independent panels agree on the order. sport.de (#5 Semrush) was measured as a substitute because kicker blocked us.

#### India
| Source (date) | Order |
|---|---|
| Similarweb "Top Sports Websites Ranking in India", Aug 2026 (updated 2026-09-01) — https://www.similarweb.com/top-websites/india/sports/ | 1 cricbuzz.com, 2 cricinfo.com, 3 india-batery.com (betting/fantasy), 4 espncricinfo.com, 5 073m.com |
| Similarweb cricbuzz.com competitors, Aug 2026 — https://www.similarweb.com/website/cricbuzz.com/competitors/ | India country rank: cricbuzz #26, cricinfo #27, espncricinfo #312, sports.ndtv.com #856 |
| Semrush India sports, Aug 2026 — https://www.semrush.com/website/top/india/sports/ | 1 thehindu.com 36.7M (whole domain, not sports-only), 2 sportskeeda.com 20.52M, 3 chess.com, 4 cricinfo.com 15.65M, 5 espn.in, 6 espncricinfo.com 6.98M … (cricbuzz is not in this Semrush list, so the two panels disagree) |
| Comscore "Sports Highlights on Digital 2025 – India" (reported Nov 2025, via search snippet; the source article https://www.passionateinmarketing.com/cricbuzzs-dominance-as-indias-no-1-cricket-platform-reinforced-by-comscore-report/ returned **HTTP 403** to WebFetch) | Cricbuzz #1, 53M unique visitors (figure from the search snippet only, not verified) |
| Comscore via afaqs, 2021-04-05 (old) — https://www.afaqs.com/news/media/sportskeeda-becomes-the-2nd-largest-sports-website-in-india-source-comscore | Sportskeeda #2 in India during IPL 2020 |

Similarweb's sportskeeda.com page (Aug 2026) shows the **US** as its top country (36.81%, India 8.13%), with global rank #7,658 — https://www.similarweb.com/website/sportskeeda.com/. sportstar.thehindu.com: Similarweb shows 1.9M visits over 3 months and no rank.

**Picked top 4: cricbuzz.com, espncricinfo/cricinfo.com (one ESPN property), sportskeeda.com, plus #4 = sports.ndtv.com (Similarweb India rank).** espncricinfo, cricinfo and NDTV Sports all returned **403 Akamai "Access Denied"**. I measured **sportstar.thehindu.com** (The Hindu; thehindu.com is #1 in Semrush) and **timesofindia.indiatimes.com/sports** instead, so India has 4 measured sites.

#### China
| Source (date) | Order |
|---|---|
| Similarweb `top-websites/china/sports/` — **no China country list**: the URL serves the Worldwide list (confirmed by title and filter). https://www.similarweb.com/top-websites/china/sports/ | n/a |
| Similarweb China country ranks, Aug 2026, from competitor pages — https://www.similarweb.com/website/dongqiudi.com/competitors/ , https://www.similarweb.com/website/sports.sina.com.cn/competitors/ | hupu.com #28, zhibo8.com #62, news.zhibo8.com #108, dongqiudi.com #628, sports.qq.com #975, sports.cctv.com #1,110, sports.sina.cn #1,573, sports.sina.com.cn #1,838, sports.163.com #2,349, sports.sohu.com #4,129 |
| Chinaz 体育综合 ranking (SEO composite + Baidu weight, not traffic), updated 2026-09-20 — https://top.chinaz.com/hangye/index_tiyu_tiyuzonghe.html | 1 hupu.com, 2 sports.cctv.com, 3 sports.sina.com.cn, 4 sports.sohu.com, 5 sports.163.com, 6 sports.qq.com |
| Maigoo brand list, 2026-06-11 (editorial index, covers apps and platforms) — https://www.maigoo.com/top/434017.html | 央视体育, 咪咕体育, 腾讯体育, 爱奇艺体育, 懂球帝, 虎扑体育 … |

**Picked top 4 (by Similarweb China country rank): hupu.com, zhibo8.com, dongqiudi.com, sports.qq.com.** sports.sina.com.cn was also measured as a portal reference. All returned HTTP 200 from HU with no geo-block.

### 2. Summary table (measured)

"HTML decoded" is the size of the saved file. "wire" is curl `size_download` (gzip bytes). r2 TTFB is lower almost everywhere because of warm DNS/TLS/CDN, so treat r1 as the cold figure. "3P resource hosts" counts third-party hosts in script/iframe/img/stylesheet/preconnect tags and in URLs inside inline scripts. It does **not** count runtime-injected tags, because no JS was executed.

| Site | HTTP | Final URL | HTML decoded / wire bytes | TTFB r1 / r2 (s) | Scripts ext/inline | CSS links | `<a>` (outside `<script>`) | 3P resource hosts | theme-color | prefers-color-scheme | lang |
|---|---|---|---|---|---|---|---|---|---|---|---|
| de_transfermarkt | 200 | https://www.transfermarkt.de/ | 393,708 / 51,246 | 0.923 / 0.021 | 25/17 | 15 | 503 (503) | 6 | — | HTML:0 CSS:0 | de |
| de_sportschau | 200 | https://www.sportschau.de/ | 1,555,227 / 194,371 | 0.074 / 0.033 | 2/3 | 1 | 573 (573) | 9 | — | HTML:2 CSS:0 | de |
| de_sport1 | 200 | https://www.sport1.de/ | 620,809 / 97,352 | 0.466 / 0.023 | 22/56 | 8 | 257 (254) | 12 | — | HTML:0 CSS:0 | de |
| de_sportde | 200 | https://www.sport.de/ | 626,338 / 89,871 | 0.221 / 0.040 | 8/40 | 1 | 977 (977) | 18 | #1c1c1c | HTML:0 CSS:0 | de |
| in_cricbuzz | 200 | https://www.cricbuzz.com/ | 435,772 / 68,311 | 0.622 / 0.250 | 5/69 | 2 | 156 (156) | 14 | — | HTML:0 CSS:0 | en |
| in_sportskeeda | 200 | https://www.sportskeeda.com/ | 658,297 / 110,691 | 0.520 / 0.313 | 8/56 | 3 | 425 (425) | 14 | — | HTML:0 CSS:0 | en |
| in_sportstar | 200 | https://sportstar.thehindu.com/ | 226,105 / 41,944 | 0.301 / 0.049 | 5/66 | 11 | 316 (316) | 20 | — | HTML:0 CSS:0 | en |
| in_toisports | 200 | https://timesofindia.indiatimes.com/sports | 823,079 / 159,680 | 0.237 / 0.070 | 3/19 | 14 | 668 (660) | 15 | #af2c2c | HTML:0 CSS:0 | en |
| cn_hupu | 200 | https://www.hupu.com/ | 578,181 / 84,533 | 0.333 / 0.058 | 5/2 | 3 | 253 (253) | 11 | — | HTML:0 CSS:0 | none |
| cn_zhibo8 | 200 | https://www.zhibo8.com/ | 606,347 / 72,191 | 1.386 / 1.093 | 5/4 | 3 | 2064 (495) | 4 | — | HTML:0 CSS:0 | none |
| cn_dongqiudi | 200 | https://www.dongqiudi.com/ | 336,423 / 54,373 | 0.126 / 0.068 | 6/1 | 0 | 45 (45) | 4 | — | HTML:0 CSS:0 | none |
| cn_qqsports | 200 | https://sports.qq.com/ | 738,639 / 92,837 | 1.110 / 0.617 | 8/11 | 1 | 14 (14) | 8 | — | HTML:0 CSS:0 | none |
| cn_sina | 200 | https://sports.sina.com.cn/ | 316,265 / 72,612 | 0.858 / 0.021 | 15/26 | 4 | 935 (924) | 8 | red | HTML:0 CSS:0 | none |
| de_kicker | 403 | https://www.kicker.de/ | blocked page 772 B | 0.093 / 0.063 | — | — | — | — | — | — | — |
| in_espncricinfo | 403 | https://www.espncricinfo.com/ | blocked page 372 B | 0.101 / 0.056 | — | — | — | — | — | — | — |
| in_cricinfo | 403 | https://www.cricinfo.com/ | blocked page 368 B | 0.229 / 0.042 | — | — | — | — | — | — | — |
| in_ndtvsports | 403 | https://sports.ndtv.com/ | blocked page 369 B | 0.134 / 0.033 | — | — | — | — | — | — | — |
#### Blocked (could not be measured; not described from memory)

- **kicker.de**: HTTP 403, 772 B. The body is a DataDome challenge ("Please enable JS and disable any ad blocker", `geo.captcha-delivery.com`, header `x-datadome: protected`, CloudFront BUD50). WebFetch also got 403. I did not attempt to bypass it.
- **espncricinfo.com / cricinfo.com**: HTTP 403 `AkamaiGHost` "Access Denied" (368–372 B). WebFetch also got 403 for espncricinfo.
- **sports.ndtv.com**: HTTP 403 Akamai "Access Denied" (369 B).

#### Cross-site observations (evidenced)

- **Consent**: none of the German sites served a server-side consent wall. All 4 returned full article HTML. Consent runs as a client-side CMP: transfermarkt, sport1 and sport.de load Sourcepoint (`cdn.privacy-mgmt.com` / `_sp_` / `__tcfapi`). transfermarkt's HTML also contains "Pur-Abo ... Nutzung mit Tracking und Cookies" (the pay-or-consent model), and sport.de's header contains "PUR-Abo / PUR verwalten / PUR kaufen". sportschau (public broadcaster ARD) references no CMP or ad vendor, and its only analytics-like host is `lwqvhgk.pa-cd.com` (a Piano Analytics collection-style domain; my attribution, not confirmed). The Indian sites use Google Funding Choices (sportskeeda), TrustArc `consent.truste.com` (sportstar) and OneTrust inline refs (TOI). The Chinese sites show no CMP or TCF. The only China "TCF" hit is a substring match in dongqiudi. The Chinese sites use Baidu Tongji (dongqiudi, sina) and Tencent Aegis/Galileo telemetry (qq).
- **Dark mode**: sportschau is the only site with evidenced dark mode. An inline script checks cookie `darkmode_content` **or** `matchMedia('(prefers-color-scheme: dark)')` and toggles `.theme-dark`, and its CSS defines `.theme-dark{--color-…}` tokens (462 custom properties). No other site had `prefers-color-scheme` in HTML or the fetched CSS. Only 3 sites set `theme-color`: sport.de `#1c1c1c`, TOI `#af2c2c`, sina `red`.
- **lang/viewport**: all 4 German and 4 Indian sites declare `lang` (de/en). **None of the 5 Chinese pages declares `<html lang>`**. hupu and zhibo8 have **no viewport meta** (desktop-only PC pages). dongqiudi, qq and sina set `user-scalable=no`/`maximum-scale=1`. So do transfermarkt and cricbuzz.
- **Link density (Chinese portal pattern)**: `<a>` per 10 kB of HTML: zhibo8 34.9 and sina 30.3 vs German 3.8–16.0 and Indian 3.7–14.3. zhibo8 has 2,064 `<a>` tags, of which 1,569 are in JS-embedded HTML strings (schedule/match lists) and 495 in static markup. sina has 935. The app-first Chinese products are the opposite: dongqiudi (Nuxt SSR) serves 45 `<a>`, and sports.qq.com is a Vue SPA shell (`<div id="app">`) with only 14 `<a>` and 1,413 visible text chars.
- **Live scores in header/first screen**: cricbuzz's first visible text after the nav is a match carousel (JPN vs NEP, AFG vs NEP "NEP won" …). hupu opens with a CBA/NBA fixture strip (未开始 = not started + time). dongqiudi opens with "今日重要赛事 · 16场" plus scores ("尼日利亚 2 - 1 马达加斯加 FT"). zhibo8's first screen has "比分" (score) 59× and "直播" (live) 185×, with per-match "互动直播 / 手机看直播 / 比分 / 动画" links. qq opens with "热门比赛". On the German side, sportschau's first nav item is "Live & Ergebnisse" (Live & results) and "live-ticker" appears 93×. sport.de's nav includes "Heute Live" and has 89 "liveticker" hits. sport1's nav has "Heute Live". transfermarkt is data-first ("Tabelle" 183×, nav "Marktwerte/Wettbewerbe/Statistiken").
- **Cricket-first India**: cricbuzz nav = Live Scores · Schedule · Archives · News · Series · Teams · Videos · Rankings ("cricket" 448×, "ipl" 89×). TOI Sports nav starts sports · Cricket · Asian Games 2026 · Asian Games Men's/Women's T20 · IND vs AFG · IND vs WI … · Live Cricket Score. Sportstar nav: Asian Games 2026 · Cricket · Football · Hockey. **sportskeeda served its US edition to the HU vantage** (nav NFL · NBA · MLB · EPL · WNBA · Tennis …, `user-geo.staticc.workers.dev` present). Its India cricket-first layout could not be observed from this location.
- **App-download prompts** (HTML evidence): hupu header "手机虎扑 | 下载虎扑App" (mobile Hupu | download app). dongqiudi nav "下载App / 扫描下载 懂球帝客户端" (QR scan to download). zhibo8 "下载 / 扫码下载". sportskeeda "download app" plus App Store/Play links. sport1 has App Store and Play links. cricbuzz, sportstar and TOI have Play links. transfermarkt has "App herunterladen".
- **Betting in nav (Germany)**: transfermarkt "Sportwetten", sport1 "Wetten & Spiele / Sportwetten / Online Casinos", sport.de "Wettanbieter".
- **JSON-LD**: sportschau is the richest (32 NewsArticle + ItemList/BreadcrumbList), followed by cricbuzz (41 SiteNavigationElement, 10 NewsArticle, 3 VideoObject). **No Chinese site emits any JSON-LD.**
- **Fonts**: DE uses custom brand faces (transfermarkt Source Sans Pro/Oswald/UniviaPro, sportschau "Thesis", sport1 Barlow, sport.de Titillium Web). IN uses Inter (cricbuzz, sportskeeda), Rethink Sans (TOI) and Noto Sans Display plus Bootstrap (sportstar). CN relies on system CJK stacks: PingFang SC (hupu, qq), Microsoft YaHei/Hiragino (sina), and zhibo8 declares no font-family at all in its fetched CSS. qq adds DINPro-Bold and BlenderPro-Heavy for numerals/scores.
- **TTFB**: the only cold TTFB above 1 s were zhibo8 (1.386 s, still 1.093 s warm) and qq (1.110 s). Both are served from China with no EU edge seen. sportschau was fastest cold (0.074 s).

### 3. Per-site raw measurements

Keyword counts are raw case-insensitive substring counts over the whole HTML, including URLs and scripts, so they are indicators, not UI element counts. Colours are the 10 most frequent hex/rgb(a) values in inline `<style>`, `style=`, `fill/stroke/color` attributes and up to 3 fetched CSS files (URLs listed). They are normalised (#fff becomes #ffffff) and include 8-digit alpha hex. sportschau and TOI express most colours via `var(--…)` tokens, so their hex counts are low.

Nav translations (DE/CN): transfermarkt "Transfers & Gerüchte"=transfers & rumours, "Marktwerte"=market values, "Wettbewerbe"=competitions, "Sportwetten"=sports betting; sportschau "Live & Ergebnisse"=live & results, "Hintergrund"=background, "Tor des Monats"=goal of the month; sport1 (footer-side nav, HTML) "Derzeit beliebt"=trending, "Heute Live"=live today, "Wetten & Spiele"=betting & games; sport.de "Alle Sportarten von A-Z"=all sports A-Z, "Wettanbieter"=bookmakers; hupu 虎扑首页 home · NBA · CBA · 足球 football · 步行街 "walking street" (off-topic forum) · 社区 community · 电竞 esports · 游戏中心 game centre; zhibo8 首页 home · NBA视频 NBA video · 足球视频 football video · NBA资讯/足球资讯 news · 电竞 esports · 综合 other sports · 比分 scores · 数据 data · NBA资料库 NBA database · 下载 download; dongqiudi 首页 home · 比赛 matches · 数据 data · 赛事 competitions · 懂球号 creator accounts · 红钻充值 "red diamond" top-up · 下载App; qq (no SSR nav) first screen 热门比赛 hot matches · 热点资讯 hot news tabs (NBA/综合体育/中国篮球/国际足球/中国足球/网球/NFL/赛车) · 精彩视频 videos; sina top bar is the Sina portal (新闻 news, 财经 finance, 娱乐 entertainment …), i.e. the sports channel sits inside a general portal.

#### de_transfermarkt

- Fetches: run1 2026-09-25T18:38:03Z HTTP 200 TTFB 0.922881s total 0.926075s wire 51246 B; run2 2026-09-25T18:38:04Z HTTP 200 TTFB 0.021466s total 0.023120s wire 51246 B; redirects 0; final URL https://www.transfermarkt.de/
- html_bytes_decoded: 393708
- lang: de
- viewport: width=device-width, initial-scale=1.0, maximum-scale=2.0, user-scalable=no
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["Svelte/Kit", "jQuery"]
- scripts_total: 42
- scripts_external: 25
- scripts_inline: 17
- stylesheet_links: 15
- inline_style_blocks: 0
- a_tags: 503
- a_tags_outside_scripts: 503
- a_per_10kB: 13.08
- img_tags: 252
- iframes: 0
- visible_text_chars: 16124
- anchor_text_chars: 8598
- anchor_text_share: 0.533
- nav_elements: 1
- third_party_hosts: ["cdn.privacy-mgmt.com", "cdn.stroeerdigitalgroup.de", "imagesrv.adition.com", "img.a.transfermarkt.technology", "tmsi.akamaized.net", "tmssl.akamaized.net"]
- vendor_labels: ["IAB TCF API (inline ref)", "Sourcepoint (inline ref)", "Sourcepoint CMP", "Stroeer", "gtag (inline ref)"]
- jsonld_types: [["Organization", 1]]
- keyword_counts: {"liveticker": 5, "spielplan": 10, "tabelle": 183, "video": 29, "podcast": 2, "play.google.com": 1, "app herunterladen": 1, "ipl": 1, "fußball": 9, "bundesliga": 46, "nba": 5}
- css_fetched: ["https://tmssl.akamaized.net/styles/tm-main.min.css?lm=1790344580 (227,961 B)", "https://tmssl.akamaized.net/css/stylesheets/main_desktop.css?lm=1790344142 (4,339 B)", "https://tmssl.akamaized.net/styles/tm-discover.min.css?lm=1790344580 (32,764 B)"]
- top_colors_html_plus_css: [["#ffffff", 163], ["#00193f", 80], ["#5ca6ff", 54], ["#dddddd", 30], ["#00aded", 29], ["#333333", 29], ["#429535", 21], ["#1d75a3", 18], ["rgba(0,0,0,0)", 16], ["#e4e4e4", 14]]
- hsl_oklch_counts: 8
- css_custom_props_defined: 130
- font_families_top: [["var(--tm-septenary-font, 'SourceSansPro-VF', sans-serif)", 27], ["var(--tm-secondary-font, 'Oswald-VF', 'Oswald-fallback', sans-serif)", 23], ["var(--tm-primary-font, 'Source Sans Pro', 'Source Sans Pro-fallback', sans-serif", 20], ["'SourceSansPro-VF', sans-serif", 8], ["var(--tm-tertiary-font, 'OSB', 'OSB-fallback', sans-serif)", 4], ["inherit", 4]]
- font_face_names: ["OSB", "OSB-fallback", "OSL", "OSL-fallback", "Oswald", "Oswald-VF", "Oswald-fallback", "Source Sans Pro", "Source Sans Pro-fallback", "SourceSansPro-VF", "UniviaPro", "UniviaPro-fallback"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: ["News", "Transfers & Gerüchte", "Marktwerte", "Wettbewerbe", "Statistiken", "Community", "Gaming", "Berater-Support", "Berater-Firmen", "PremiumService", "Video ▶️", "Neueste Transfers", "Gerüchteküche", "Alle Foren", "Alle News", "Marktwert-Analyse", "Vereinsforen Bundesliga", "Vereinsforen 2. Bundesliga", "Vereinsforen 3. Liga", "Sportwetten"]
- consent_wall_signals: ["Einwilligung", "cookie", "Consent", "Datenschutz", "Pur-Abo"]

#### de_sportschau

- Fetches: run1 2026-09-25T18:38:04Z HTTP 200 TTFB 0.074221s total 0.096367s wire 194371 B; run2 2026-09-25T18:38:05Z HTTP 200 TTFB 0.032592s total 0.055454s wire 194371 B; redirects 0; final URL https://www.sportschau.de/
- html_bytes_decoded: 1555227
- lang: de
- viewport: width=device-width
- theme_color: null
- color_scheme_meta: null
- framework_hints: []
- scripts_total: 5
- scripts_external: 2
- scripts_inline: 3
- stylesheet_links: 1
- inline_style_blocks: 1
- a_tags: 573
- a_tags_outside_scripts: 573
- a_per_10kB: 3.77
- img_tags: 237
- iframes: 0
- visible_text_chars: 21802
- anchor_text_chars: 20546
- anchor_text_share: 0.942
- nav_elements: 5
- third_party_hosts: ["images.mdr.de", "images.ndr.de", "lwqvhgk.pa-cd.com", "perr.h-cdn.com", "player.h-cdn.com", "www.mdr.de", "www.ndr.de", "zagent29.h-cdn.com", "zagent30.h-cdn.com"]
- vendor_labels: []
- jsonld_types: [["ListItem", 33], ["NewsArticle", 32], ["collectionPage", 1], ["ItemList", 1], ["BreadcrumbList", 1]]
- keyword_counts: {"liveticker": 6, "live-ticker": 93, "spielplan": 5, "tabelle": 102, "ergebnisse": 360, "video": 472, "podcast": 80, "google play": 1, "play.google.com": 1, "football": 12, "fußball": 105, "bundesliga": 323, "nba": 9}
- css_fetched: ["https://www.sportschau.de/resources/assets/css/main-0fb773189f71e4e4fcae.css (726,141 B)"]
- top_colors_html_plus_css: [["#00000000", 58], ["#ffffff", 21], ["#000000", 16], ["#ffffff00", 6], ["#00000080", 6], ["#001e50", 4], ["#9e9e9e99", 4], ["#ffffffaa", 4], ["#cccccc", 3], ["#003480", 3]]
- hsl_oklch_counts: 0
- css_custom_props_defined: 462
- font_families_top: [["var(--font-family-body),sans-serif", 47], ["var(--font-family-headline),sans-serif", 28], ["inherit", 12], ["var(--font-family-overline),sans-serif", 8], ["Thesis", 5], ["var(--font-family-default)", 3]]
- font_face_names: ["Thesis", "ardplayer", "ardplayer-audio"]
- prefers_color_scheme_in_html: 2
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 92
- nav_labels_first: ["Live & Ergebnisse", "Livestreams", "Newsticker", "Hintergrund", "Fußball", "Basketball", "Handball", "Eishockey", "Tennis", "Radsport", "Leichtathletik", "Formel 1", "Wintersport", "Mehr Sport", "Regional", "Podcasts", "Videos", "Audios", "Tor des Monats", "TV", "Untermenü TV einblenden Pfeil rechts", "Archiv", "Themen", "Einstellungen einblenden Pfeil rechts", "7-Tage-Überblick", "Nations League (M)", "Bundesliga (M)", "Bundesliga (F)", "2. Bundesliga (M)", "2. Bundesliga (F)"]
- consent_wall_signals: ["cookie", "Datenschutz"]

#### de_sport1

- Fetches: run1 2026-09-25T18:38:05Z HTTP 200 TTFB 0.465802s total 0.470331s wire 97352 B; run2 2026-09-25T18:38:05Z HTTP 200 TTFB 0.023436s total 0.027270s wire 97352 B; redirects 0; final URL https://www.sport1.de/
- html_bytes_decoded: 620809
- lang: de
- viewport: width=device-width, initial-scale=1
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["React", "WordPress"]
- scripts_total: 78
- scripts_external: 22
- scripts_inline: 56
- stylesheet_links: 8
- inline_style_blocks: 20
- a_tags: 257
- a_tags_outside_scripts: 254
- a_per_10kB: 4.24
- img_tags: 76
- iframes: 2
- visible_text_chars: 5964
- anchor_text_chars: 4840
- anchor_text_share: 0.812
- nav_elements: 4
- third_party_hosts: ["ad-delivery.net", "applets.ebxcdn.com", "brwsrfrm.com", "btloader.com", "cdn.privacy-mgmt.com", "creative-cdn.oddsserve.com", "imasdk.googleapis.com", "s.w.org", "static.criteo.net", "stats.wp.com", "v0.wordpress.com", "www.googletagmanager.com"]
- vendor_labels: ["Criteo", "GPT (inline ref)", "GTM", "IAB TCF API (inline ref)", "Sourcepoint (inline ref)", "Sourcepoint CMP"]
- jsonld_types: [["ImageObject", 2], ["WebPage", 1], ["ReadAction", 1], ["BreadcrumbList", 1], ["ListItem", 1], ["WebSite", 1], ["SearchAction", 1], ["EntryPoint", 1], ["PropertyValueSpecification", 1], ["Organization", 1]]
- keyword_counts: {"liveticker": 12, "spielplan": 23, "tabelle": 4, "ergebnisse": 11, "video": 310, "podcast": 93, "app store": 1, "google play": 1, "apps.apple.com": 1, "play.google.com": 1, "football": 3, "fußball": 10, "bundesliga": 97, "nba": 6, "cba": 4, "wwe": 4}
- css_fetched: ["https://www.sport1.de/wp-content/plugins/sport1-blocks/build/src/blocks/newsticker/style-index.css?m=1790327848g (21,506 B)", "https://www.sport1.de/_static/??-eJx1zEsOwkAIANALOdJP4mdhPIulxEyKQICJ7e276crE7Vs8+FpBlSRJMG7vKgFh6tmXiRWXgKlVniEc4QCrYsoMkRtTqTLTesaIE/yvUJ2OyCkaZ0l6Bfnv8fw8+uu9G4fbZeh29ZI5MQ== (53,056 B)", "https://www.sport1.de/_static/??-eJytzEsOgkAQhOELObSoCbgwnmUYRtLa8wjVg+H2gonufaxq89dH92xciuqjUpYycAQhp1Fr00lyN5AFvIIm7n26vrcKHCsHbOhL4HkauTO2/wPGwf4GZLGzMNQU/gy6rJFIouX1KqCz+KEs9Gqdw6lujtv9rmkP7QNLe4rd (64,259 B)"]
- top_colors_html_plus_css: [["#ffffff", 77], ["#000000", 51], ["#e5e5e5", 16], ["#106bfe", 10], ["#777777", 9], ["#72849f", 9], ["#2b333f", 7], ["rgba(7,20,30,.7)", 7], ["#1068fe", 6], ["rgba(43,51,63,.7)", 6]]
- hsl_oklch_counts: 0
- css_custom_props_defined: 112
- font_families_top: [["VideoJS", 50], ["Barlow Regular", 16], ["", 13], ["Barlow Bold", 10], ["Arial,Helvetica,sans-serif", 5], ["inherit", 2]]
- font_face_names: ["Barlow Bold", "Barlow Bold Italic", "Barlow Regular", "Barlow Regular Italic", "Barlow SC Black Italic", "Barlow SC Regular Italic", "Barlow W Bold", "Barlow W Regular", "VideoJS", "sport1-styleguide"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: []
- consent_wall_signals: ["cookie", "Consent", "Datenschutz"]

#### de_sportde

- Fetches: run1 2026-09-25T18:38:38Z HTTP 200 TTFB 0.221424s total 0.268690s wire 89871 B; run2 2026-09-25T18:38:39Z HTTP 200 TTFB 0.039657s total 0.041812s wire 89871 B; redirects 0; final URL https://www.sport.de/
- html_bytes_decoded: 626338
- lang: de
- viewport: width=device-width, initial-scale=1.0
- theme_color: #1c1c1c
- color_scheme_meta: null
- framework_hints: []
- scripts_total: 48
- scripts_external: 8
- scripts_inline: 40
- stylesheet_links: 1
- inline_style_blocks: 1
- a_tags: 977
- a_tags_outside_scripts: 977
- a_per_10kB: 15.97
- img_tags: 443
- iframes: 2
- visible_text_chars: 32390
- anchor_text_chars: 22302
- anchor_text_share: 0.689
- nav_elements: 1
- third_party_hosts: ["ad-delivery.net", "adctrl.emsmobile.de", "brwsrfrm.com", "btloader.com", "cdn-gl.nmrodam.com", "cdn.static-fra.de", "de.wikipedia.org", "s.hs-data.com", "schema.org", "sso.guj.de", "static.cleverpush.com", "static.criteo.net", "te-static.technical-service.net", "twitter.com", "widgets.teads-xo.com", "www.facebook.com", "www.googletagmanager.com", "www.wikidata.org"]
- vendor_labels: ["Criteo", "GPT (inline ref)", "GTM", "IAB TCF API (inline ref)", "Meta", "Sourcepoint (inline ref)", "TCF (inline ref)", "Teads", "X", "ads(generic)"]
- jsonld_types: [["WebSite", 1], ["SearchAction", 1], ["Organization", 1], ["ImageObject", 1]]
- keyword_counts: {"liveticker": 89, "live-ticker": 2, "spielplan": 7, "tabelle": 80, "ergebnisse": 89, "video": 129, "football": 24, "fußball": 71, "bundesliga": 144, "nba": 34, "cba": 2}
- css_fetched: ["https://s.hs-data.com/comon/prj/isdc/v2/sportde/static/css/dist/default.min.css?v=20260925 (410,311 B)"]
- top_colors_html_plus_css: [["#ffffff", 128], ["#054850", 99], ["#767676", 84], ["#1c1c1c", 55], ["#f2e604", 55], ["#e8e8e8", 44], ["#f3f3f3", 33], ["#e1e1e3", 14], ["#bababa", 12], ["#075f61", 12]]
- hsl_oklch_counts: 0
- css_custom_props_defined: 92
- font_families_top: [["hs-icons", 4], ["Titillium Web,Arial,Helvetica,sans-serif", 4]]
- font_face_names: ["Titillium Web", "hs-icons"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: ["Fußball", "Formel 1", "NFL", "Tennis", "Wintersport", "Oktagon MMA", "Handball", "Eishockey", "Basketball", "Motorsport", "Radsport", "US-Sport", "Boxen", "Darts", "Am. Football", "Golf", "Hockey", "Reitsport", "Rugby", "Volleyball", "Leichtathletik", "Schwimmsport", "Tischtennis", "Triathlon", "Schach", "Sport-Mix", "Alle Sportarten von A-Z", "Olympia", "Paralympics", "Die Finals"]
- consent_wall_signals: ["cookie", "Consent", "Datenschutz", "PUR"]

#### in_cricbuzz

- Fetches: run1 2026-09-25T18:38:05Z HTTP 200 TTFB 0.622437s total 0.670145s wire 68311 B; run2 2026-09-25T18:38:06Z HTTP 200 TTFB 0.249861s total 0.265029s wire 68311 B; redirects 0; final URL https://www.cricbuzz.com/
- html_bytes_decoded: 435772
- lang: en
- viewport: height=device-height,  width=device-width, initial-scale=1.0,  minimum-scale=1.0, maximum-scale=1.0,  user-scalable=no, target-densitydpi=device-dpi, viewport-fit=cover
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["Next.js", "webpack"]
- scripts_total: 74
- scripts_external: 5
- scripts_inline: 69
- stylesheet_links: 2
- inline_style_blocks: 2
- a_tags: 156
- a_tags_outside_scripts: 156
- a_per_10kB: 3.67
- img_tags: 47
- iframes: 0
- visible_text_chars: 9958
- anchor_text_chars: 5341
- anchor_text_share: 0.536
- nav_elements: 0
- third_party_hosts: ["c.amazon-adsystem.com", "cdnapisec.kaltura.com", "com.cricbuzz.android", "fonts.googleapis.com", "fonts.gstatic.com", "in.pinterest.com", "itunes.apple.com", "play.google.com", "securepubads.g.doubleclick.net", "twitter.com", "www.facebook.com", "www.instagram.com", "www.youtube.com", "x.com"]
- vendor_labels: ["Amazon Ads", "DoubleClick", "GPT (inline ref)", "Google static", "Meta", "X", "YouTube", "ads(generic)"]
- jsonld_types: [["SiteNavigationElement", 41], ["NewsArticle", 10], ["ImageObject", 6], ["PostalAddress", 4], ["WPSideBar", 3], ["VideoObject", 3], ["Organization", 2], ["WPHeader", 1], ["WebPage", 1], ["ViewAction", 1], ["EntryPoint", 1], ["WPFooter", 1]]
- keyword_counts: {"live score": 2, "live-score": 4, "scorecard": 8, "video": 153, "ranking": 15, "points table": 6, "play.google.com": 2, "cricket": 448, "ipl": 89}
- css_fetched: ["https://www.cricbuzz.com/_next/static/css/e8f4dab59157788a.css (134,314 B)"]
- top_colors_html_plus_css: [["#00000000", 52], ["#ffffff", 49], ["#009270", 28], ["#000000", 25], ["#f0f0f0", 19], ["#464646", 19], ["rgba(0,0,0,.1)", 19], ["#222222", 13], ["#f9fafb", 13], ["#fafafa", 12]]
- hsl_oklch_counts: 9
- css_custom_props_defined: 59
- font_families_top: [["Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,H", 2], ["ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,mo", 2], ["GF:Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900\\u0026display=swap\\", 2], ["inherit", 1], ["Inter,sans-serif", 1], ["Constantia,Lucida Bright,Lucidabright,Lucida Serif,Lucida,DejaVu Serif,Bitstream", 1]]
- font_face_names: []
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 36
- nav_labels_first: []
- consent_wall_signals: []

#### in_sportskeeda

- Fetches: run1 2026-09-25T18:38:06Z HTTP 200 TTFB 0.520156s total 0.525316s wire 110691 B; run2 2026-09-25T18:38:07Z HTTP 200 TTFB 0.313497s total 0.319936s wire 110949 B; redirects 0; final URL https://www.sportskeeda.com/
- html_bytes_decoded: 658297
- lang: en
- viewport: width=device-width, initial-scale=1.0, user-scalable=yes
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["AMP"]
- scripts_total: 64
- scripts_external: 8
- scripts_inline: 56
- stylesheet_links: 3
- inline_style_blocks: 46
- a_tags: 425
- a_tags_outside_scripts: 425
- a_per_10kB: 6.61
- img_tags: 351
- iframes: 1
- visible_text_chars: 59040
- anchor_text_chars: 1616
- anchor_text_share: 0.027
- nav_elements: 1
- third_party_hosts: ["assets.govisibl.io", "c.amazon-adsystem.com", "cdn.jsdelivr.net", "en.wikipedia.org", "fundingchoicesmessages.google.com", "openads-cdn.adsrvr.org", "sb.scorecardresearch.com", "securepubads.g.doubleclick.net", "user-geo.staticc.workers.dev", "www.facebook.com", "www.googletagmanager.com", "www.instagram.com", "www.linkedin.com", "x.com"]
- vendor_labels: ["Amazon Ads", "Comscore", "DoubleClick", "GPT (inline ref)", "GTM", "Meta", "ads(generic)", "gtag (inline ref)"]
- jsonld_types: [["Organization", 2], ["ImageObject", 2], ["WebPage", 1], ["Thing", 1], ["WebSite", 1]]
- keyword_counts: {"live score": 8, "scorecard": 3, "video": 301, "ranking": 4, "standings": 4, "google play": 1, "apps.apple.com": 1, "play.google.com": 1, "download app": 1, "cricket": 97, "ipl": 14, "football": 226, "bundesliga": 2, "nba": 80, "kabaddi": 8, "wwe": 157}
- css_fetched: ["https://staticg.sportskeeda.com/css/production/side-menu-bundle-958fb1dd8a.css (11,250 B)", "https://staticg.sportskeeda.com/css/production/desktop/side-menu--homepage-bundle-bcdddd3a42.css (561 B)", "https://staticg.sportskeeda.com/css/production/user-notifications/notifications-bundle-bcb5a3210a.css (2,528 B)"]
- top_colors_html_plus_css: [["rgba(0,0,0,0)", 160], ["rgb(128,128,128)", 87], ["#ffffff", 46], ["#2d2d2d", 26], ["#d32f2f", 26], ["#999999", 18], ["#474747", 11], ["#000000", 9], ["#666666", 9], ["#f5f5f5", 7]]
- hsl_oklch_counts: 0
- css_custom_props_defined: 106
- font_families_top: [["", 9], ["'Inter', -apple-system, BlinkMacSystemFont,", 1], ["sans-serif", 1]]
- font_face_names: ["Barlow Condensed", "Inter"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 31
- nav_labels_first: ["NFL", "NBA", "MLB", "EPL 2026-27", "WNBA", "Tennis", "NCAAB", "NCAAF", "WWE", "Soccer", "Golf", "NHL", "Sports News", "MMA", "US Olympics", "AEW", "NASCAR", "Gaming", "IndyCar", "MotoGP"]
- consent_wall_signals: ["cookie"]

#### in_sportstar

- Fetches: run1 2026-09-25T18:38:37Z HTTP 200 TTFB 0.300542s total 0.302580s wire 41944 B; run2 2026-09-25T18:38:38Z HTTP 200 TTFB 0.048735s total 0.050433s wire 41943 B; redirects 0; final URL https://sportstar.thehindu.com/
- html_bytes_decoded: 226105
- lang: en
- viewport: width=device-width,initial-scale=1
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["jQuery"]
- scripts_total: 71
- scripts_external: 5
- scripts_inline: 66
- stylesheet_links: 11
- inline_style_blocks: 5
- a_tags: 316
- a_tags_outside_scripts: 316
- a_per_10kB: 14.31
- img_tags: 112
- iframes: 1
- visible_text_chars: 7845
- anchor_text_chars: 6340
- anchor_text_share: 0.808
- nav_elements: 0
- third_party_hosts: ["accounts.google.com", "ads.pubmatic.com", "cdn.cxense.com", "cdn.polyfill.io", "cdn.taboola.com", "cdn.tinypass.com", "consent.truste.com", "experience.tinypass.com", "fonts.googleapis.com", "sb.scorecardresearch.com", "securepubads.g.doubleclick.net", "static.chartbeat.com", "twitter.com", "www.facebook.com", "www.google-analytics.com", "www.googletagmanager.com", "www.instagram.com", "www.npttech.com", "www.thehindugroup.com", "www.youtube.com"]
- vendor_labels: ["Chartbeat", "Comscore", "DoubleClick", "GA", "GPT (inline ref)", "GTM", "IAB TCF API (inline ref)", "Meta", "Piano", "PubMatic", "Taboola", "X", "YouTube", "ads(generic)"]
- jsonld_types: [["ImageObject", 2], ["PostalAddress", 2], ["Organization", 2], ["NewsMediaOrganization", 1], ["SiteNavigationElement", 1]]
- keyword_counts: {"live score": 4, "livescore": 3, "scorecard": 95, "matchcenter": 27, "match-center": 2, "video": 6, "podcast": 4, "standings": 4, "google play": 3, "play.google.com": 2, "cricket": 127, "ipl": 20, "football": 193, "bundesliga": 3, "nba": 1, "kabaddi": 5}
- css_fetched: ["https://assetsss.thehindu.com/theme/css/SSRX/bootstrap.min.css?ver=1789561776 (155,799 B)", "https://assetsss.thehindu.com/theme/css/SSRX/bootstrap.min.css?ver=1789561776 (155,799 B)", "https://assetsss.thehindu.com/theme/css/SSRX/owlcarousel.min.css?ver=1789561776 (3,351 B)"]
- top_colors_html_plus_css: [["#ffffff", 197], ["#000000", 122], ["#212529", 82], ["#0d6efd", 70], ["#6c757d", 66], ["#dc3545", 50], ["#198754", 50], ["#dee2e6", 42], ["#f8f9fa", 36], ["#ffc107", 34]]
- hsl_oklch_counts: 0
- css_custom_props_defined: 36
- font_families_top: [["", 10], ["var(--bs-font-sans-serif)", 6], ["inherit", 4], ["var(--bs-font-monospace)", 2], ["var(--bs-font-monospace)!important", 2], ["GF:Noto+Sans+Display:ital,wght@0,400;0,700;0,900;1,400;1,700;1,900", 2]]
- font_face_names: ["alternate-gothic-atf"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: ["Asian Games 2026", "Cricket", "Football", "Hockey", "Shorts", "Who's 100th GM", "Magazine", "Buy Print", "Login", "Account", "Subscribe", "Go to Search", "Posters", "Columns", "Star Life", "Statsman", "Archery", "Athletics", "Badminton", "Basketball", "Boxing", "Chess", "Cue Sport", "ESPORTS", "Golf", "Kabaddi", "MMA", "Motorsport", "Shooting", "Squash"]
- consent_wall_signals: ["cookie", "Consent"]

#### in_toisports

- Fetches: run1 2026-09-25T18:38:38Z HTTP 200 TTFB 0.237195s total 0.265446s wire 159680 B; run2 2026-09-25T18:38:38Z HTTP 200 TTFB 0.069886s total 0.087445s wire 159680 B; redirects 0; final URL https://timesofindia.indiatimes.com/sports
- html_bytes_decoded: 823079
- lang: en
- viewport: width=device-width, initial-scale=1, maximum-scale=1
- theme_color: #af2c2c
- color_scheme_meta: null
- framework_hints: ["React"]
- scripts_total: 22
- scripts_external: 3
- scripts_inline: 19
- stylesheet_links: 14
- inline_style_blocks: 1
- a_tags: 668
- a_tags_outside_scripts: 660
- a_per_10kB: 8.31
- img_tags: 238
- iframes: 1
- visible_text_chars: 45053
- anchor_text_chars: 42624
- anchor_text_share: 0.946
- nav_elements: 1
- third_party_hosts: ["accounts.google.com", "ade.clmbtech.com", "assets.toiimg.com", "c.amazon-adsystem.com", "fonts.gstatic.com", "onelinksmartscript.appsflyer.com", "securepubads.g.doubleclick.net", "static.clmbtech.com", "static.toiimg.com", "tpapi.timespoints.com", "twitter.com", "www.facebook.com", "www.googletagmanager.com", "www.linkedin.com", "www.youtube.com"]
- vendor_labels: ["Amazon Ads", "DoubleClick", "GPT (inline ref)", "GTM", "Google static", "IAB TCF API (inline ref)", "Meta", "OneTrust (inline ref)", "X", "YouTube", "ads(generic)", "gtag (inline ref)"]
- jsonld_types: [["Organization", 1], ["ImageObject", 1]]
- keyword_counts: {"live score": 12, "live-score": 36, "scorecard": 48, "match-center": 31, "video": 528, "podcast": 5, "ranking": 42, "standings": 31, "points table": 9, "play.google.com": 2, "cricket": 294, "ipl": 96, "football": 120, "nba": 152, "kabaddi": 5, "wwe": 160}
- css_fetched: ["https://assets.toiimg.com/assets/92625.cc13317c.chunk.css (63,765 B)", "https://assets.toiimg.com/assets/74151.2a3713b4.chunk.css (151,839 B)", "https://assets.toiimg.com/assets/59812.00dfcdaf.chunk.css (84,391 B)"]
- top_colors_html_plus_css: [["#a5a5a5", 328], ["#ffffff", 51], ["#e21b22", 37], ["#595959", 28], ["#1a1a1a", 23], ["rgba(var(--primary-dark-color-rgba)", 22], ["#a6a6a6", 18], ["#000000", 13], ["#f6f6f6", 12], ["#ececec", 11]]
- hsl_oklch_counts: 0
- css_custom_props_defined: 7
- font_families_top: [["'Rethink Sans'", 4], ["Rethink Sans,-apple-system,BlinkMacSystemFont,Helvetica Neue,Segoe UI,sans-serif", 1], ["monospace,sans-serif", 1]]
- font_face_names: ["Rethink Sans"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: ["sports", "Cricket", "Asian games 2026", "Asian Games Men's T20", "Asian Games Women's T20", "IND Vs AFG", "IND Vs WI", "NFL", "NBA", "NHL", "MLB", "International Sports", "WWE", "Tennis", "Live Cricket Score", "Esports", "WPL", "Ashes", "Formula E", "NFL Schedule", "F1", "Saudi Football", "Badminton", "Hockey", "MMA", "Videos", "Racing", "Athletics", "Wrestling", "Shooting"]
- consent_wall_signals: ["cookie", "Consent"]

#### cn_hupu

- Fetches: run1 2026-09-25T18:38:07Z HTTP 200 TTFB 0.332515s total 0.350299s wire 84533 B; run2 2026-09-25T18:38:08Z HTTP 200 TTFB 0.058437s total 0.075185s wire 84533 B; redirects 0; final URL https://www.hupu.com/
- html_bytes_decoded: 578181
- lang: null
- viewport: null
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["React"]
- scripts_total: 7
- scripts_external: 5
- scripts_inline: 2
- stylesheet_links: 3
- inline_style_blocks: 0
- a_tags: 253
- a_tags_outside_scripts: 253
- a_per_10kB: 4.48
- img_tags: 604
- iframes: 1
- visible_text_chars: 17536
- anchor_text_chars: 9568
- anchor_text_share: 0.546
- nav_elements: 0
- third_party_hosts: ["activity-static.hoopchina.com.cn", "assets-football.hoopchina.com.cn", "at.alicdn.com", "i1.hoopchina.com.cn", "i10.hoopchina.com.cn", "i11.hoopchina.com.cn", "i3.hoopchina.com.cn", "i4.hoopchina.com.cn", "i5.hoopchina.com.cn", "sports.cctv.com", "w1.hoopchina.com.cn"]
- vendor_labels: []
- jsonld_types: []
- keyword_counts: {"直播": 5, "赛程": 8, "排名": 4, "视频": 7, "下载": 3, "football": 265, "nba": 284, "cba": 293, "英超": 38, "wwe": 1}
- css_fetched: ["https://at.alicdn.com/t/font_1543847_zo49096ka1r.css (18,943 B)", "https://w1.hoopchina.com.cn/games/static/pc-hupuhome-web/manifest_f34dbb32.css (146,243 B)", "https://w1.hoopchina.com.cn/games/static/pc-hupuhome-web/bbsIndex_b86b2571.css (18,145 B)"]
- top_colors_html_plus_css: [["#7b7e86", 509], ["#c60100", 248], ["#ffffff", 84], ["#191c22", 28], ["#9c9fa4", 20], ["#c01e2e", 18], ["rgba(0,0,0,.5)", 13], ["#1890ff", 12], ["#f6f6f6", 11], ["#000000", 10]]
- hsl_oklch_counts: 1
- css_custom_props_defined: 6
- font_families_top: [["PingFangSC-Regular", 9], ["slick", 6], ["PingFangSC-Regular,PingFang SC", 3], ["PingFangSC-Semibold,PingFang SC", 3], ["", 2], ["swiper-icons", 2]]
- font_face_names: ["FontAwesome", "iconfont", "slick", "swiper-icons"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: []
- consent_wall_signals: []

#### cn_zhibo8

- Fetches: run1 2026-09-25T18:38:08Z HTTP 200 TTFB 1.385671s total 1.934440s wire 72191 B; run2 2026-09-25T18:38:10Z HTTP 200 TTFB 1.092940s total 1.928658s wire 72191 B; redirects 0; final URL https://www.zhibo8.com/
- html_bytes_decoded: 606347
- lang: null
- viewport: null
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["jQuery"]
- scripts_total: 9
- scripts_external: 5
- scripts_inline: 4
- stylesheet_links: 3
- inline_style_blocks: 0
- a_tags: 2064
- a_tags_outside_scripts: 495
- a_per_10kB: 34.86
- img_tags: 1178
- iframes: 3
- visible_text_chars: 7409
- anchor_text_chars: 3615
- anchor_text_share: 0.488
- nav_elements: 0
- third_party_hosts: ["duihui.duoduocdn.com", "pca.zhibo8.cc", "static4style.duoduocdn.com", "tu.duoduocdn.com"]
- vendor_labels: []
- jsonld_types: []
- keyword_counts: {"video": 27, "比分": 59, "直播": 185, "赛程": 2, "排名": 4, "视频": 22, "集锦": 1, "下载": 2, "football": 312, "nba": 573, "cba": 124, "中超": 5, "英超": 7}
- css_fetched: ["https://static4style.duoduocdn.com/www/css/index_v2/reset.css?v=0.01 (2,645 B)", "https://static4style.duoduocdn.com/static/pcmain/css/index.v6.css?v=0.03 (35,076 B)", "https://static4style.duoduocdn.com/static/pcmain/css/menu.v2.css?v=0.2 (3,368 B)"]
- top_colors_html_plus_css: [["#ffffff", 17], ["#0082ff", 11], ["#051019", 10], ["rgba(0,0,0,0.1)", 6], ["#efefef", 5], ["#b5b7ba", 5], ["#f7f7f7", 4], ["#1e2830", 3], ["#cccccc", 3], ["#eeeeee", 2]]
- hsl_oklch_counts: 0
- css_custom_props_defined: 0
- font_families_top: []
- font_face_names: []
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: []
- consent_wall_signals: ["cookie"]

#### cn_dongqiudi

- Fetches: run1 2026-09-25T18:38:12Z HTTP 200 TTFB 0.125573s total 0.134191s wire 54373 B; run2 2026-09-25T18:38:12Z HTTP 200 TTFB 0.068015s total 0.077194s wire 54373 B; redirects 0; final URL https://www.dongqiudi.com/
- html_bytes_decoded: 336423
- lang: null
- viewport: width=device-width, initial-scale=1, minimum-scale=1.0, maximum-scale=1, user-scalable=no
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["Nuxt", "Vue"]
- scripts_total: 7
- scripts_external: 6
- scripts_inline: 1
- stylesheet_links: 0
- inline_style_blocks: 1
- a_tags: 45
- a_tags_outside_scripts: 45
- a_per_10kB: 1.37
- img_tags: 72
- iframes: 0
- visible_text_chars: 2219
- anchor_text_chars: 1389
- anchor_text_share: 0.626
- nav_elements: 2
- third_party_hosts: ["bdimg7.qunliao.info", "hm.baidu.com", "img1.qunliao.info", "sd.qunliao.info"]
- vendor_labels: ["Baidu", "Baidu Tongji", "TCF (inline ref)"]
- jsonld_types: []
- keyword_counts: {"video": 961, "ranking": 12, "standings": 118, "比分": 1, "直播": 2, "赛程": 1, "积分榜": 1, "视频": 1, "集锦": 6, "下载": 3, "ipl": 2, "football": 1, "nba": 3, "cba": 1, "中超": 3, "英超": 15}
- css_fetched: []
- top_colors_html_plus_css: [["#3fae2a", 27], ["#94a3b8", 25], ["#ffffff", 19], ["rgba(0,0,0,.5)", 17], ["#f1f5f9", 17], ["#334155", 9], ["#f8fafc", 9], ["#1e293b", 7], ["#475569", 7], ["#06b8ff", 6]]
- hsl_oklch_counts: 9
- css_custom_props_defined: 2
- font_families_top: [["Source Sans Pro,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,", 1], ["-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif", 1]]
- font_face_names: []
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: ["首页", "比赛", "数据", "赛事", "懂球号", "下载App"]
- consent_wall_signals: []

#### cn_qqsports

- Fetches: run1 2026-09-25T18:38:12Z HTTP 200 TTFB 1.110049s total 1.347626s wire 92837 B; run2 2026-09-25T18:38:13Z HTTP 200 TTFB 0.617048s total 0.621194s wire 92837 B; redirects 0; final URL https://sports.qq.com/
- html_bytes_decoded: 738639
- lang: null
- viewport: width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1.3,user-scalable=no,viewport-fit=cover
- theme_color: null
- color_scheme_meta: null
- framework_hints: ["Vue"]
- scripts_total: 19
- scripts_external: 8
- scripts_inline: 11
- stylesheet_links: 1
- inline_style_blocks: 0
- a_tags: 14
- a_tags_outside_scripts: 14
- a_per_10kB: 0.19
- img_tags: 30
- iframes: 0
- visible_text_chars: 1413
- anchor_text_chars: 76
- anchor_text_share: 0.054
- nav_elements: 0
- third_party_hosts: ["aegis.cdn-go.cn", "galileotelemetry.tencent.com", "mat1.gtimg.com", "new.inews.gtimg.com", "puui.qpic.cn", "sports3.gtimg.com", "vmedia.qpic.cn", "vpic-cover.puui.qpic.cn"]
- vendor_labels: ["Tencent Aegis", "Tencent CDN"]
- jsonld_types: []
- keyword_counts: {"video": 498, "直播": 21, "赛程": 4, "视频": 6, "集锦": 31, "ipl": 180, "nba": 556, "cba": 20, "中超": 7, "英超": 26}
- css_fetched: ["https://mat1.gtimg.com/sports/sports-pc/styles/style.93cf9c91.css (223,583 B)"]
- top_colors_html_plus_css: [["#ffffff", 37], ["rgba(0,0,0,0)", 28], ["rgba(0,0,0,.5)", 20], ["#000000", 19], ["rgba(0,0,0,.8)", 11], ["rgb(000/0)", 9], ["#ff5a5a", 8], ["rgba(0,0,0,.06)", 8], ["#f8d7a5", 6], ["#ffebc9", 6]]
- hsl_oklch_counts: 1
- css_custom_props_defined: 148
- font_families_top: [["PingFangSC-Medium", 20], ["PingFangSC-Regular", 12], ["DINPro-Bold", 3], ["BlenderPro-Heavy", 2], ["PingFangSC", 1], ["swiper-icons", 1]]
- font_face_names: ["BlenderPro-Heavy", "DINPro-Bold", "Emoji", "swiper-icons"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: []
- consent_wall_signals: []

#### cn_sina

- Fetches: run1 2026-09-25T18:38:39Z HTTP 200 TTFB 0.858103s total 1.114015s wire 72612 B; run2 2026-09-25T18:38:40Z HTTP 200 TTFB 0.021104s total 0.025311s wire 72612 B; redirects 0; final URL https://sports.sina.com.cn/
- html_bytes_decoded: 316265
- lang: null
- viewport: width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0,user-scalable=no
- theme_color: red
- color_scheme_meta: null
- framework_hints: ["Vue", "jQuery"]
- scripts_total: 41
- scripts_external: 15
- scripts_inline: 26
- stylesheet_links: 4
- inline_style_blocks: 1
- a_tags: 935
- a_tags_outside_scripts: 924
- a_per_10kB: 30.27
- img_tags: 101
- iframes: 0
- visible_text_chars: 24618
- anchor_text_chars: 19032
- anchor_text_share: 0.773
- nav_elements: 2
- third_party_hosts: ["h5.sinaimg.cn", "hm.baidu.com", "n.sinaimg.cn", "n0.sinaimg.cn", "n1.sinaimg.cn", "n3.sinaimg.cn", "pluto.sina.cn", "www.sinaimg.cn"]
- vendor_labels: ["Baidu", "Baidu Tongji", "Baidu Tongji (inline ref)", "Sina CDN"]
- jsonld_types: []
- keyword_counts: {"video": 5, "比分": 1, "直播": 6, "赛程": 14, "积分榜": 4, "排名": 29, "视频": 4, "football": 13, "bundesliga": 1, "nba": 20, "cba": 17, "中超": 2, "英超": 5, "wwe": 2}
- css_fetched: ["https://news.sina.com.cn/css/pctianyi/tianyi.css (40,557 B)", "https://n0.sinaimg.cn/sports/0c2cef0d/20250619/swiper-bundle.min.css (13,681 B)", "https://n1.sinaimg.cn/sports/0c2cef0d/20250625/element.css (232,512 B)"]
- top_colors_html_plus_css: [["#ffffff", 210], ["#409eff", 143], ["#c0c4cc", 102], ["#909399", 59], ["#606266", 56], ["#303133", 49], ["#ebeef5", 48], ["#f56c6c", 43], ["#e4e7ed", 39], ["#67c23a", 34]]
- hsl_oklch_counts: 0
- css_custom_props_defined: 18
- font_families_top: [["arial", 2], ["'videofont'", 2], ["swiper-icons", 2], ["element-icons", 2], ["'Hiragino Sans GB','Microsoft Yahei','微软雅黑','Simsun','宋体','Arial'", 1], ["MicrosoftYaHei-Bold", 1]]
- font_face_names: ["element-icons", "swiper-icons", "videofont"]
- prefers_color_scheme_in_html: 0
- prefers_color_scheme_in_css: 0
- dark_mode_hints: 0
- nav_labels_first: ["新浪体育", "新浪首页", "新闻", "体育", "财经", "娱乐", "科技", "博客", "图片", "专栏", "...", "汽车", "教育", "时尚", "女性", "星座", "医药", "房产", "历史", "视频", "收藏", "育儿", "读书", "佛学", "游戏", "旅游", "邮箱", "导航", "注册", "登录"]
- consent_wall_signals: ["cookie"]

### 4. Response headers (single HEAD-like GET, 18:42Z)

- transfermarkt: nginx behind CloudFront BUD50 (Miss). sportschau: no server header. sport1: nginx + CloudFront BUD50. sport.de: Cloudflare (BUD) + CloudFront IST50. cricbuzz: nginx. sportskeeda: nginx + CloudFront BUD50 (Hit). sportstar: Cloudflare BUD. TOI: Akamai (akamai-timesinternet-grn). hupu: nginx. zhibo8: no server header. dongqiudi: openresty, **HTTP/1.1**. qq: TAPISIX/2.1.8. sina: Tengine + Alibaba Swift cache (60 s). espncricinfo/cricinfo: AkamaiGHost 403. kicker: CloudFront + DataDome 403.

### 5. Limitations

- Single vantage point (Hungary) and no JS execution, so runtime-injected ads/CMP overlays, client-rendered navs (qq, cricbuzz nav partially) and geo editions (sportskeeda) reflect this vantage only.
- Similarweb country lists expose only the top 5 without login. China has no public Similarweb country category page, so the China order uses per-site country ranks.
- Comscore India 2025 numbers come from a search snippet; the source article returned 403.

## C. Industry, stats and analytics sites, open data

**Status labels:** **OPENED** = I retrieved the page/document myself and the quote comes from that retrieval. **OPENED (secondary)** = I opened a news write-up because the primary page blocked me. **SNIPPET ONLY, NOT OPENED** = seen only in a search-engine summary; verify before publishing. **PROJECTION** = a forecast, with its source.

---

### Part A — Sports media industry

#### A1. Market size and growth (rights, digital content)

| # | Finding (exact wording / figures) | Source | Status |
|---|---|---|---|
| 1 | Streamers "US$14.2 billion on sports rights in 2026" (**PROJECTION**, Ampere), "seven per cent more than the US$13.2 billion" paid in 2025; Prime Video "US$3.8 billion in 2026, which would account for 27 per cent of the total"; "About 44 per cent of that total will be paid by global generalist streamers" | SportsPro, 2 Feb 2026 — https://www.sportspro.com/news/broadcast-ott/sports-rights-streaming-spend-2026-amazon-prime-video-dazn-peacock-february-2026/ | OPENED (secondary, Ampere data) |
| 2 | Ampere: sports rights spend **PROJECTION** "$78bn" by 2030; US spend $30.5bn in 2025, "more than $36bn" by 2030; Europe $18.3bn (2025) → $21.3bn (2030); Asia $7.2bn → $9.9bn; US grew 122% from $13.8bn (2015). Quote from Dan Harraghy (Ampere): "Sports rights remain a reliable driver of value in media." Note: the page's wording on whether $78bn is global or a sum of the regions shown was unclear in my extraction; check before citing. | IBC, 26 Nov 2025 — https://www.ibc.org/monetisation/news/sports-rights-spend-to-top-78bn-by-2030/22851 | OPENED (secondary) |
| 3 | Ampere's own article page (https://www.ampereanalysis.com/insight/us-sports-rights-spend-hits-305bn-outpacing-the-wider-tv-market) returned only a header with no body | Ampere | Opened, no content |
| 4 | PwC Global Sports Survey 2026: "7.4%" yearly growth expected over the next 3–5 years; media rights "5.1% (down from 6.1% in 2023)"; betting-related rights "7.7%"; regional: Asia 9.4%, Europe 6.7%, US "above 8%"; sample "over 500 senior sports executives globally and 7,250 fans". Quote: "Social media highlights are favoured by 18 to 34-year-olds, with meaningful engagement in creator-led content and interactive formats"; "four-in-five investors now favour assets offering multiple revenue levers; from sponsorship and hospitality to women's sport, endurance formats and creator-led competitions" | Consultancy.uk, 13 May 2026 — https://www.consultancy.uk/news/amp/44066/global-sports-sector-set-for-more-measured-growth-as-media-rights-plateau | OPENED (secondary). The PwC primaries returned HTTP 403 to both WebFetch and curl: pwc.co.uk press release, pwc.ch/en/insights/sport/sports-survey-2026.html, pwc.co.uk/…/sports-survey.html |
| 5 | Search snippets for the same PwC survey: sponsorship 6.9%, ticketing/hospitality 6.7%; "517 senior executives", fielded "June and September 2025" | pwc.ch / insidersport.com (the latter also 403) | SNIPPET ONLY, NOT OPENED |
| 6 | Deloitte 2026 Global Sports Industry Outlook (published 17 Feb 2026; authors Tweardy, Harwood, Deweese, Bridge, Harris, Amato). Quotes: "The value of media rights continues to climb worldwide"; "Commercial revenues in women's sports are growing at double-digit rates"; "AI may serve as the connective engine that strengthens organizations from within, breaking down data silos". The signposts include "AI agents deployment for ticketing and content creation" and "20 stadiums opening in 2027" (**PROJECTION**) | https://www.deloitte.com/us/en/insights/industry/technology/technology-media-telecom-outlooks/sports-industry-outlook.html | OPENED |
| 7 | Statista "Global sports media rights spending by region 2025–2030" (published 3 Feb 2026; source Ampere, released Nov 2025). The public text says spending "would exceed ** billion U.S. dollars" by 2030. **The values are paywalled** (asterisks) | https://www.statista.com/statistics/1340782/global-sports-media-rights-spending-by-region/ | OPENED (figures hidden) |
| 8 | Statista: 2023 sports media rights value "nearly 56 billion U.S. dollars", up from 54.7bn | statista.com/statistics/1453558 | SNIPPET ONLY, NOT OPENED |
| 9 | Opta Pulse (Stats Perform, 12 May 2026): "produce high-quality sports highlights up to 80% faster than traditional workflows" | https://www.statsperform.com/insights/opta-pulse-launch/ | OPENED |

#### A2. How fans consume news (Reuters Institute DNR 2025 and 2026)

**DNR 2026** (published 16 June 2026; I downloaded and read the full PDF, https://reutersinstitute.politics.ox.ac.uk/sites/default/files/2026-06/DNR%202026%20FINAL_2.pdf; landing page https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026). OPENED.

- "social media and video networks are for the first time the single most widely used way of accessing online news (used by 54% of all respondents), ahead of news organisations' own websites and apps (51%)."
- "10% of people use AI chatbots for news, up from 7% last year … (16% of under-35s …)". The most popular chatbot feature is "the ability to ask follow-up questions" (42% of chatbot users).
- "77% of people globally consume online news video each week." Video on publishers' own sites and apps went "backwards, down 5pp this year." 27% watch on-demand news via apps like YouTube on smart TVs.
- Weekly use for news: TikTok 20%, Instagram 26%, YouTube 34%, Facebook 43%.
- Creators: 27% get some news from news-focused creators and 46% from creators of any type. Only 3% rely solely on creators.
- Trust in news fell to 37%, the lowest since 2015. Payment for online news is "unchanged at 17%" across 20 countries. Concern about fake news is 62%.
- Context: people spend "four to five hours each day" on smartphones.
- **Sport-specific findings:** I searched the full text for "sport". **The 2026 report has no sport-specific consumption finding.** The word appears only in country pages: brand lists (Marca, Nemzeti Sport, Siam Sport), a mention of DAZN, and Swiss debate about the public broadcaster crowding out private media "in sports". Treat any claim that "DNR says X about sports news" as unsupported.

**DNR 2025** executive summary, https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025/dnr-executive-summary (published 17 June 2025). OPENED.

- AI chatbots: "7% use for news each week … under-25s (15%)".
- Interest in AI features: "Summarised versions of news articles" 27%, translations 24%, story recommendations 21%, chatbot Q&A 18%. "a majority (66%) is interested in at least one of them".
- Social video grew from 52% (2020) to 65% (2025). Any video grew from 67% to 75%.
- Payment 18% (20 countries). Trust 40%. Selective avoidance 40%.
- The summary contains no sport-specific data.

**Reuters Institute, Generative AI and News Report 2025** (7 Oct 2025; covers AR, DK, FR, JP, UK, US), https://reutersinstitute.politics.ox.ac.uk/generative-ai-and-news-report-2025-how-people-think-about-ais-role-journalism-and-society. OPENED.

- "12%" are comfortable with news made entirely by AI, against "62%" for news made entirely by humans. The figure is 21% with human oversight and 43% when humans lead with AI assistance.
- "Only 33% think journalists 'always' or 'often' check AI outputs".
- The most-seen audience-facing feature is AI summaries (19%). "19% see AI labels daily".
- The report does not compare comfort by topic (sport against politics).

#### A3. Analytics and data content for fans, betting and fantasy, second screen

- Opta Analyst: "1 million" monthly visitors, 700,000 social followers, 40 million monthly social impressions, 55,000 newsletter subscribers. It won SJA Specialist Publisher of the Year 2025. It is "cited in global publications and broadcasters with a combined monthly audience of over one billion". Source: https://www.statsperform.com/about/opta-analyst/ (OPENED, no date shown).
- Stats Perform on xG: "Commentators, fantasy leagues, and digital fan platforms rely on xG for deeper engagement"; "Sportsbooks and oddsmakers use goal expectancy models like xG". Source: https://www.statsperform.com/insights/expected-goals-xg-the-football-metric-changing-analysis-betting-and-fan-engagement/ (OPENED, undated; references an April 2025 match).
- Stats Perform Automated Insights: pre-game previews "in multiple languages", live insights, and "Post-game recaps using Opta and OptaAI data". The page makes no statement on accuracy or human review. Source: https://www.statsperform.com/automated-insights/ (OPENED).
- Second screen: "86% of Millennials and 83.2% of GenZ" football fans against 79.4% of all football fans. Source: Advanced Television / Nielsen, 1 May 2026, https://www.advanced-television.com/2026/05/01/data-football-viewership-growing-across-the-us/ — SNIPPET ONLY, NOT OPENED. The claims "77% of sports fans multitask" and "63% … started following the NBA because of a specific player" are also SNIPPET ONLY.
- Nielsen Tops of Sports (for 2026), https://www.nielsen.com/insights/2025/tops-of-sports-2026/ (OPENED, undated): streaming sports documentaries reached "16,937 million total viewing minutes in 2024, an 113% increase from 2021"; "37% of U.S. general population expect increased FIFA World Cup 2026 interest". The Spring 2026 edition (https://www.nielsen.com/insights/2026/tops-of-sports/) is behind a download wall.
- Nielsen 2025 Global Sports Report, https://www.nielsen.com/insights/2025/global-sports-report-2025/ (OPENED, undated): "51% of people globally are fans of football"; "Fans 50 and older who use streaming to watch sports grew 21% in two years".
- Market-research sizing (Grand View, FMI, e.g. sports analytics market "USD 6,002.4 million in 2025" → 36,204.9m by 2035) is SNIPPET ONLY and comes from paid-report vendors. Low reliability; do not cite.
- FSGA fantasy player counts: the page (https://thefsga.org/industry-research/) was OPENED but the figures are for members only.

#### A4. Mobile share of traffic

- Similarweb platforms page, **August 2026, worldwide, all categories**: "Mobile traffic market share is the largest … with 66.55%". https://www.similarweb.com/platforms/ (OPENED). **This is not sports-specific.**
- Similarweb Top Sports Websites, August 2026 (updated 1 Sep 2026): 1 espn.com, 2 marca.com, 3 cricbuzz.com, 4 cricinfo.com, 5 mlb.com, 6 as.com, 7 073m.com, 8 sports.yahoo.com, 9 gazzetta.it, 10 mundodeportivo.com. The public page shows **no device split**. https://www.similarweb.com/top-websites/sports/ (OPENED).
- fotmob.com on Similarweb: about 26.9M visits over 3 months (down 21.75% month on month). Audience is US 20.15% and UK 13.93%; 76.92% male; 25–34 is the largest age group; 72.93% of traffic is direct. Competitors: SofaScore, Transfermarkt, ESPN, FlashScore. **No device split shown.** https://www.similarweb.com/website/fotmob.com/ (OPENED).
- espn.com on Similarweb: "518.7M" visits over 3 months. **No device split shown.** (OPENED)
- A search snippet claimed ESPN is "42.71% desktop / 42.71% mobile" and FotMob "76.03%" desktop. The two ESPN numbers are identical, so the snippet is internally inconsistent and **untrustworthy**: SNIPPET ONLY, NOT OPENED, do not use.
- **Gap:** I found no open, primary source for a sports-category mobile share. The best defensible statement is the global 66.55% (Similarweb, Aug 2026) combined with DNR 2026's "four to five hours each day" on smartphones.

#### A5. Subscription/paywall vs advertising

- NYT Q2 2026 (TheNextWeb, 6 Aug 2026), https://thenextweb.com/news/new-york-times-q2-2026-digital-subscriber-miss (OPENED, secondary):
  - "13.4 million digital subscribers" with 280k net adds, which missed expectations.
  - Digital subscription revenue up 16.4% to $408m.
  - The bundle is "Games, Cooking, Wirecutter and The Athletic".
  - The article says AI search summaries are reducing referral traffic.
- Search snippets: Q2 2026 digital advertising $114m (+20.7%) "driven by … news, sports and games"; The Athletic had its "largest audience ever during the World Cup" with a "550-person sports newsroom" (Yahoo Finance earnings summaries). SNIPPET ONLY, NOT OPENED.
- The Athletic's first quarterly profit was $2.6m (Q3 2024). Source: Nieman Lab, 5 Nov 2024, https://www.niemanlab.org/reading/the-athletic-is-now-profitable-for-the-first-time/ (OPENED).
- Axios (20 May 2025) on The Athletic being "solidly profitable", with ads from BetMGM, eBay and StubHub and "6 million subscribers": the page returned 403, so SNIPPET ONLY.
- Stats sites measured in Part B are all advertising-funded (GPT/Prebid/pub.network/AdSense tags found). StatMuse and Understat also have sign-in or "Personal cabinet" areas. Basketball-Reference upsells Stathead.
- DNR 2026: only 17% pay for online news, and "Growing reader revenue is likely to prove harder".

#### A6. Women's sport growth

- Deloitte UK press release (8 Apr 2026), https://www.deloitte.com/uk/en/about/press-room/womens-elite-sports-revenues-2026.html (OPENED). All figures below are a **2026 PROJECTION**:
  - Revenue of "US$3 billion", up from US$2.4bn in 2025 (+25%) and +340% since 2022.
  - Split: commercial 45% (US$1.35bn), matchday 30% (US$911m), broadcast 25% (US$765m).
  - Football 35% and basketball 35%.
  - North America US$1.64bn (54%), Europe US$434m (14%).
- Nielsen "Women & Sports" (2026), https://www.nielsen.com/insights/2026/women-sports/ (OPENED):
  - "46 billion minutes" of women's sports were viewed in 2025, "+71%" since 2022.
  - 28.3 billion minutes were viewed in H1 2026, "on record pace".
  - 122.5M US fans; 52% of the US population is interested.
  - Ad spend is up 120% since 2022.
- Nielsen 2025 Global Sports Report: "47% of fans of women's sports are female" (OPENED).
- Nielsen/PepsiCo press release: women's football is expected in the "global top 5 sports by 2030 with over 800M fans" (**PROJECTION**) — SNIPPET ONLY (headline).
- StatsBomb open data includes WSL, NWSL, Liga F, Frauen-Bundesliga, Serie A Women, the Women's Euro 2025 and Women's World Cups (see Part C). It could seed women's content in research-only contexts, but not commercially.

#### A7. AI in sports media and trust

- MLS AI recaps carried this disclaimer: "This story was automatically generated based on match data. Content has not been reviewed by editorial staff." Criticism focused on thin, lifeless copy. Source: Awful Announcing, 14 Oct 2025, https://awfulannouncing.com/mls/ai-generated-match-recaps-criticism.html (OPENED).
- ESPN's generative-AI recaps of NWSL and PLL (Sep 2024) had "the date of an NWSL game wrong and an incorrect record for one team". ESPN said "each AI-generated story will get reviewed by a human editor", bylined "ESPN Generative AI Services". Source: Front Office Sports, 5 Sep 2024, https://frontofficesports.com/espn-ai-generated-soccer-lacrosse/ (OPENED).
- Gannett/LedeAI high-school recaps (2023) contained "[[WINNING_TEAM_MASCOT]]" placeholders and were paused. SNIPPET ONLY, NOT OPENED.
- Trust numbers (Reuters Gen AI 2025, above): 12% are comfortable with fully AI-made news and 62% prefer human-made.
- Implication for the prototype: label automated recaps, keep a human in the loop, and state the data source.

---

### Part B — Competitor stats sites (measured with curl on 2026-09-25)

Method: `curl -s -L --compressed -A "Mozilla/5.0 (Macintosh…) Chrome/140…" -H Accept… -w "%{http_code} %{time_starttransfer} %{size_download} %{url_effective}"`, run from Budapest (cf-ray `…-BUD`). I fetched the homepage plus one data page per site. For loaded sites, colours and fonts come from a Python counter over the HTML plus up to 3 linked CSS files. The framework hints are regex heuristics; I call a hint "confirmed" only where a generator tag or `/_next/` path settles it.

| Site | Home: status / TTFB / bytes | Data page tested | Result |
|---|---|---|---|
| fbref.com | **403** / 0.059s / 3,378 | /en/comps/9/Premier-League-Stats → 403, 3,423 B | **Blocked: Cloudflare managed challenge.** Headers `cf-mitigated: challenge`, `server: cloudflare`; page title "Just a moment...". **Not described.** |
| theanalyst.com | 200 / 0.038s / 108,431 | /competition/premier-league/stats → 200, 0.030s, 86,939 B | Loaded |
| sofascore.com | **403** / 0.034s / 48 | /tournament/football/england/premier-league/17 → 403, 48 B | **Blocked: body `{"error": {"code": 403, "reason": "Forbidden" }}`**, `server: Varnish`, JSON content-type. This is not a Cloudflare challenge. The page is fully client-rendered and denies non-browser clients. **Not described.** |
| fotmob.com | 200 / 0.199s / 82,305 | /leagues/47/overview/premier-league → 200, 0.604s, 145,872 B | Loaded (CloudFront) |
| basketball-reference.com | 200 / 0.068s / 57,810 | /players/j/jamesle01.html → 200, 0.176s, 240,048 B | Loaded (Cloudflare, no challenge) |
| understat.com | 200 / 0.298s / 3,975 | /league/EPL → 200, 0.287s, 4,686 B | Loaded, but only as a thin HTML shell (Apache/2.4.29 Ubuntu); the data comes from JS |
| statmuse.com | 200 / 0.917s / 82,134 | /nba → 200, 0.484s, 42,390 B | Loaded (CloudFront) |
| whoscored.com | **403** / 0.028s / 1,767 | /regions/252/tournaments/2/… → 403, 1,770 B | **Blocked: Cloudflare WAF block page** ("Attention Required! \| Cloudflare", "Sorry, you have been blocked"). This is a hard block, not a JS challenge. **Not described.** |

#### theanalyst.com (Opta Analyst)

- **Stack:** WordPress 7.1, confirmed by the generator tag, plus the "Seriously Simple Podcasting 3.17.0" plugin. It runs nginx behind Varnish (x-cache HIT). Ads are served via pub.network and googletag.
- **Theme and design:**
  - theme-color is `#1d0a30` (deep purple).
  - I found no dark-mode CSS: 0 `prefers-color-scheme: dark` rules, although the main theme CSS was mostly inline.
  - Fonts are **Big Shoulders Text** (Light to ExtraBold; display) and **Lora** (serif body), self-hosted woff2.
  - Top 10 colours: #ffffff(108), #000000(63), #1d0a30(54), #fd4890(32), #b225c3(26), #e02b8f(24), #ff006e(21), #e56329(20), #eb842c(20), #eeeeee(8). The palette is purple, magenta and orange gradients.
- **Nav labels:** Premier League › Articles, Stats, Predictions, Expected Points Table, Power Rankings, FPL, Newsletter; Champions League; Football Predictions; competition list (PL, UCL, La Liga, Bundesliga, Serie A, Ligue 1, Championship, **WSL**); Opta Stats.
- **Data patterns found in the HTML:**
  - "opta" appears 188 times and "stats perform" 9 times. Opta attribution is the brand itself.
  - "Opta Supercomputer" projections, "Expected Points Table", Power Rankings, FPL content, and roughly 135 matches for predictions/supercomputer terms.
  - 53 inline SVGs.
  - The server HTML has **0 `<table>` elements**, so the stats tables render client-side.
  - No radar, percentile or heatmap strings appear in the server HTML.

#### fotmob.com

- **Stack:** Next.js, confirmed by `/_next/static/`; React; Emotion-style class names; CloudFront. The ad stack is GPT, and the HTML contains "odds/bet" strings 125 times.
- **Theme and design:**
  - No theme-color meta tag.
  - **Dark mode: yes.** 493 dark-theme selector hits come from class or data-theme toggles, not `prefers-color-scheme`. The CSS variables include light and dark `--MFColorScheme-*` pairs.
  - Fonts are **Inter** plus Walsheim and Cabinet Grotesk (next/font, self-hosted).
  - Top 10 colours: #ffffff(43), #2ad572(42; FotMob green), #911712(36), #76b4e5(33), #69a8d8(33), #ff4646(32), #c00808(30), #095bb6(28), #0850a0(28), #bd0510(28). Many of these are team colours embedded in the data.
- **Nav labels:** Matches, News, Transfer Center, Rumors, TV schedules, Predictor, Lineup Builder, FIFA Rankings Men / Women, Newsletter, FAQ. The league sub-nav is Overview, Table, Fixtures, Player stats, Team stats, Transfers, Seasons.
- **Data patterns in the HTML/JSON:**
  - xG appears 203 times, e.g. "Expected goals (xG)" and "xG per 90" stat leaderboards.
  - **Player ratings** appear 112 times as decimal values, e.g. `"rating":7.99`.
  - **Shot map** appears 97 times (colour-scheme variables `Shotmap-Fullscreen`).
  - **Percentile rank** bars appear 16 times (`detailedStats-percentileRankBackground`).
  - **Heatmap** appears 8 times.
  - "momentum" appears 24 times.
  - There are no `<table>` elements; everything is div/SVG components.
  - **No visible data-provider attribution:** 0 hits for Opta, Stats Perform and Sportradar in the HTML.

#### basketball-reference.com (Sports Reference)

- **Stack:** Custom server-rendered HTML from cdn.ssref.net, with no SPA framework. Ads are served via pub.network and GPT.
- **Theme and design:**
  - theme-color is `#4d4438`.
  - **No dark mode:** 0 rules.
  - Fonts are system fonts only (Verdana/Arial/sans-serif), with no webfonts.
  - Top 10 colours: #ffffff(137), #454340(104), #747678(65), #c9cbcd(61), #efeeed(56), #8f5400(53; brand amber-brown), #000000(50), #404445(48), #eeeeee(32), #aaaaaa(31).
- **Nav labels:** Players, Teams, Seasons, Leaders, Scores, WNBA, Draft, Hub (NEW), Stathead, Newsletter, "Full Site Menu Below".
- **Data patterns:**
  - **50 `<table>` elements** across the 2 pages, with classes such as `sortable stats_table`, `stats_table sortable row_summable`, `suppress_glossary sortable stats_table`.
  - **18,989 `data-stat=` cell attributes** on the LeBron page. These are sortable headers with glossary tooltips (`data-tip`, e.g. "2007-08 NBA Scoring Champ").
  - There are 114 HTML comment blocks on the player page.
  - "radar" appears 6 times and "glossary" 9 times.
  - **Attribution:** "Data Provided By" plus a SportRadar logo linking to sportradar.com, on both pages.

#### understat.com

- **Stack:**
  - Apache/Ubuntu serves the page; jQuery 1.9.1/1.12.4, jQuery UI, **Chart.js 2.7.2/2.9.3**, typeahead, jTable, alasql and xlsx.core.
  - The data is embedded or loaded via `league.min.js`, so the server shell has **0 `<table>` elements**. There are 2 `<canvas>` elements for charts.
  - Ads come from AdSense and adlook.
- **Theme and design:**
  - theme-color is `#ffffff`.
  - **Dark mode: yes, and it is the default.** `<body class="theme-dark">`, `localStorage.getItem("theme") || 'DARK'`, and 396 theme-dark selector hits.
  - Fonts are **Anton** (display) and **Barlow**, plus FontAwesome.
  - Top 10 colours: #272729(47), #ffffff(44), #ececec(38), #343436(35), #669966(28; green accent), #f6f6f6(25), #aba9a8(21), #cecece(21), #797979(19), #ccac00(6).
- **Nav labels:** EPL, La liga, Bundesliga, Serie A, Ligue 1, RFPL, Main page, Personal cabinet, and a "Find player by name" search box.
- **Data patterns from the EPL page text:**
  - League table columns: W D L G GA PTS **xG NPxG xGA NPxGA NPxGD PPDA OPPDA DC ODC xPTS**.
  - Overall/Home/Away tabs; Table/Charts toggle; "Last games" filter (All/3/5/10); date range; position filter (GK D M F S).
  - **Export "csv json xlsx"**.
  - The season selector runs from 2014/2015 to 2026/2027.

#### statmuse.com

- **Stack:** **Astro v5.13.7**, confirmed by the generator tag, with Tailwind-style utility classes (`dark:bg-gray-3`) and CloudFront. Framework-island hints (React/Vue/Svelte) are heuristic only.
- **Theme and design:**
  - No theme-color meta tag.
  - **Dark mode: yes.** 2 `prefers-color-scheme: dark` rules, 194 `dark:` class hits, and a "Toggle Theme" control.
  - Font is **Calibre** (self-hosted `/fonts/calibre.woff2`).
  - Top 10 colours: #ffffff(55), #dd3636(25), #00c1d8(22), #0086ff(18), #eac428(16), #333333(16), #003ca8(14), #39cccc(14), #32c771(9), #ffc72c(9).
- **Nav labels:**
  - Sports: Home, NFL, CFB, MLB, WNBA, FC, NBA, NHL, PGA, **Money**.
  - Site: Scores, News, Trending, Trending Sports, Trending Money, Trending Live, Examples, **Data & Glossary**, Gallery, About, Blog, Shop, Sign in.
- **Data patterns:**
  - A natural-language question box ("Search StatMuse, save time.").
  - Feed cards with one-line stat facts, e.g. "Michael Penix in his season debut: 18-25 256 YDS 1 TD".
  - 21 `<table class="whitespace-nowrap w-full">` elements; 136 SVGs; a glossary page link; "odds/bet" appears 82 times.
  - No data-provider attribution string was found in the HTML.

#### Sites not described (blocked)
fbref.com (Cloudflare challenge), sofascore.com (Varnish JSON 403) and whoscored.com (Cloudflare block). I describe nothing about their design from memory. Loading them would need a real browser session, which this task did not use.

#### Cross-site takeaways

1. Dark mode is standard on the modern data sites (FotMob, StatMuse, Understat defaults to dark). The legacy sites (bbref) and editorial ones (Opta Analyst) lack it.
2. There are two presentation camps:
   - Dense sortable HTML tables with glossary tooltips and heavy SEO (bbref).
   - JS-rendered visual components: ratings, shot maps, percentile bars, xG leaderboards (FotMob, Understat).
3. Attribution varies: explicit "Data Provided By" plus logo (bbref/Sportradar), brand-as-attribution (Opta), or none visible (FotMob, StatMuse).
4. Data export (CSV/JSON/XLSX on Understat) and glossary pages are differentiators.
5. Betting and prediction content ("Predictor", "Supercomputer", "Money", odds) appears on 4 of the 5 loadable sites.

---

### Part C — Open data licensing

#### openfootball/football.json — **CC0 1.0 (public domain dedication)** — OPENED

- The GitHub API licence field reads `CC0-1.0`, and LICENSE.md begins "CC0 1.0 Universal".
- The README says: "The football.json schema, data and scripts are dedicated to the public domain. Use as you please with no restrictions whatsoever."
- Repo description: "Free open public domain football data in JSON … No API key required". Last push 2026-09-22T09:33:50Z.
- The README states that the latest season (2026 & 2026/27) is "auto-updated once a day (5 o'clock UTC)" from the upstream Football.TXT, but "for the upstream Football.TXT datasets for now there's no automatic (daily) update", i.e. the upstream is updated by hand.
- Raw files are served with `access-control-allow-origin: *` and `cache-control: max-age=300`, so they can be fetched directly from a browser.
- Data scope: fixtures and results. The `-full` files add goals, lineups, subs, bookings, referees, ground and attendance. There are **no xG or advanced stats**.

**2025-26 files (23):**

- at.1, at.1-full, at.2
- be.1
- de.1, de.1-full, de.2
- en.1, en.1-full, en.2, en.3, en.4
- es.1, es.2
- fr.1, fr.2
- gr.1
- it.1, it.2
- nl.1
- pt.1
- sco.1
- tr.1

Also for 2025: ar.1, br.1, br.2, cn.1, co.1, copa.l, jp.1, mls.

**2026-27 files (8):** de.1, en.1, en.2, es.1, fr.1, it.1, nl.1, pt.1. Also 2026/br.1.

- For 2026-27 there are **no** de.2, at, be, sco, tr, gr or `-full` files yet.

Content check:
| File | Name | Matches | With FT score | Last result date |
|---|---|---|---|---|
| 2026-27/en.1.json | English Premier League 2026/27 | 380 | 50 | 2026-09-20 (Matchday 5) |
| 2026-27/de.1.json | Deutsche Bundesliga 2026/27 | 306 | 36 | 2026-09-20 (Matchday 4) |
| 2026-27/es.1.json | Spain Primera División 2026/27 | 380 | 69 | 2026-09-20 (Matchday 7) |
| 2025-26/en.1.json | English Premier League 2025/26 | 380 | 380 | 2026-05-24 (complete) |
| 2025-26/de.1.json | Deutsche Bundesliga 2025/26 | 306 | 306 | 2026-05-16 (complete) |

The current-season data lagged about 5 days on 2026-09-25: the last results were from 2026-09-20.

#### openfootball/worldcup.json — **CC0 1.0** — OPENED

- The licence field is `CC0-1.0` and LICENSE.md begins "CC0 1.0 Universal". Last push 2026-08-11.
- 2026 files: worldcup.json, worldcup-full.json, worldcup.groups.json, worldcup.quali_playoffs.json, worldcup.squads.json, worldcup.stadiums.json, worldcup.teams.json. There is also 2025/clubworldcup.json.
- **2026/worldcup.json has results.** It contains 104 matches, all 104 with FT scores.
- According to that file, the Final (match 104, 2026-07-19, New York/New Jersey, East Rutherford) was Spain 1–0 Argentina after extra time (FT 0–0), scorer Ferran Torres 106'. The README says "Congrats to Spain! World Cup champs 2026!". I report this as what the dataset says; I did not verify it independently.

#### StatsBomb open data — **NOT openly licensed; not usable commercially** — OPENED

- https://github.com/statsbomb/open-data. The GitHub API showed no licence (the API call returned null fields). The README asks users to "state the data source as StatsBomb and use our logo".
- **LICENSE.pdf**, "StatsBomb Public Data User Agreement", last updated 8 September 2023. Exact excerpts:
  - 1.2: "The User may not: 1.2.1. edit, distort, distribute, reproduce, sell or in any way provide the data to any external or third party; 1.2.2. commercially exploit the data or any analysis derived from the use of the Service"
  - 1.4: "The User is required to accredit any publication of analysis formed from StatsBomb Data with the StatsBomb brand logo."
  - 2.1: "StatsBomb have full rights to withhold the Service at any time without prior warning"
  - 7: "all data provided through the Service, is the property of StatsBomb."
  - Governed by English law.
- Contents: 80 competition-seasons, e.g. the 2018 and 2022 FIFA World Cups, Euro 2020/2024, Copa América 2024, AFCON 2023, 1. Bundesliga 2023/24, Ligue 1 2021–23, La Liga 2004–2021 (the Messi era), PL 2003/04 and 2015/16, MLS 2023, and women's competitions (WSL, NWSL, Liga F, Frauen-Bundesliga, Serie A Women, Women's Euro 2022/2025, WWC 2019/2023).
- **Verdict:** Use it only for non-commercial research or analysis write-ups with the logo. Do not redistribute the raw data, and do not use it on a monetised site.

#### NBA.com statistics — **restrictive** — OPENED

- Terms of Use at https://www.nba.com/termsofuse ("LAST UPDATED: July 13, 2026").
- §9: "NBA Statistics may only be used, displayed, or published for legitimate news reporting or private, non-commercial purposes" and "may not be used in connection with any sponsorship or commercial identification".
- The terms also bar use with gambling, fantasy or comprehensive database products without consent.
- The page does not explicitly address scraping.
- **Verdict:** Do not build a data product on NBA stats endpoints.

#### nflverse/nflverse-data — **CC-BY-4.0** (GitHub licence field) — OPENED (API metadata only)

- Automated NFL data repository, last pushed 2026-09-16.
- It is likely usable with attribution. I did not read the README licence section (grep returned nothing), so confirm the per-dataset terms, especially any upstream NFL data, before using it.
- The nflreadr package shows "NOASSERTION".

#### Checked but no licence confirmed

- chadwickbureau/baseballdatabank: the API returned nulls, likely rate limiting or a moved repo.
- jalapic/engsoccerdata: no licence field; data covers 1871–2022.
Neither should be used until the licence is confirmed.

#### Part C bottom line
For a public (and potentially monetised) prototype, **openfootball football.json + worldcup.json (CC0)** is the only verified, unrestricted source here. It covers fixtures and results (plus lineups, goals and cards in `-full` files) for the major European leagues in 2025-26 (complete) and 2026-27 (in progress), and the complete 2026 World Cup. Advanced metrics (xG, ratings) must come from licensed providers such as Opta/Stats Perform or Sportradar, or be computed in-house from data with permissive licences. StatsBomb and NBA.com data are **not** usable commercially.

## D. 2027 colour and design forecasts, sports identities, UX and accessibility practice

Compiled 2026-09-25. Everything in the findings sections was read on the page cited unless it is marked **[snippet only]**. That label means the claim appeared only in a search-result summary and the page itself was not opened or could not be opened (403, bot wall, JS-only, or timeout). Anything about 2027 is labelled **PROJECTION** and names who made the forecast. None of it is a finding. Hex values appear only where a source gave them. **None of the opened sources gave a hex value.** Pantone and Coloro publish only their own codes, and those codes are listed below.

---

### 1. Colour forecasts

#### 1.1 Pantone Color of the Year
| Year | Colour | Code | Hex | Source |
|---|---|---|---|---|
| 2026 | **Cloud Dancer**, described as "a billowy white" meant to be calming | PANTONE 11-4201 | Not given on either Pantone page | [1], [2] (press release, 4 Dec 2025) |
| 2027 | **Not announced as of 2026-09-25.** Pantone normally announces in early December; the 2026 colour was announced on 4 Dec 2025 [1]. | — | — | [3] tracks 2027 paint-brand colours and does not list Pantone (updated 16 Sep 2026) |

- This is the first time Pantone has picked a white [snippet only: TIME/NPR headlines; Pantone's own page does not say it].
- Pantone describes Cloud Dancer as a "structural anchor" that works alongside other hues [1].
- Paint-brand "2027 colours of the year" have already been announced. These are consumer paint picks and are **not forecasts for web or UI**. They lean earthy and muted: Sherwin-Williams *Celery* (herbal green), Behr *Grounded* (mossy olive), Glidden *Artifact* (smoky blue), Valspar *Cottage Door* (steely blue), Dutch Boy *Deep Rooted* (earthy orange), Graham & Brown *Rose Earth* [3]. No hex values given.

#### 1.2 WGSN × Coloro
| Item | Colour(s) | Coloro code | Source |
|---|---|---|---|
| Colour of the Year 2026 | **Transformative Teal**, "a fluid fusion of classic dark blue and aqua green" | not given in article | [4] (3 Sep 2024) |
| A/W 26/27 key colours | Transformative Teal, Wax Paper (creamy off-white), Fresh Purple, Cocoa Powder (red-toned brown), Green Glow (bright yellow-green with a "nocturnal" quality) | not given | [5] (7 Oct 2024) |
| **Colour of the Year 2027 — PROJECTION (WGSN × Coloro)** | **Luminous Blue**, compared to lapis lazuli and cobalt | **125-28-38** | [6] (press release, 29 Apr 2025) |
| **S/S 27 key colours — PROJECTION (WGSN × Coloro)** | Luminous Blue (125-28-38), **Energy Orange** (018-57-34), **Pop Pink** (151-73-22), **Meadowland Green** (050-61-19), **Clay** (014-60-13) | as listed | [6] |
| **A/W 27/28 key colours — PROJECTION (WGSN × Coloro, reported by FashionUnited)** | Russet (013-30-24), Peaceful Lilac (135-78-11), Maize (036-65-23), Deep Green (082-30-14) | as listed | [7] (17 Sep 2025) |

- WGSN's stated reasoning for 2027 (projection): the theme is "interconnectedness" between opposites such as nature/technology and online/offline. Bright hues act as "coping mechanisms", Energy Orange signals resilience and safety, and Pop Pink signals playful joy [6].
- Coloro codes follow a hue-lightness-chroma notation. Coloro and WGSN give no hex conversion. Any sRGB value would be our own approximation and must be labelled that way.

#### 1.3 Design-trend reports, 2026
**Adobe Express, "Top 10 graphic design trends for 2026"** (12 Dec 2025) [8]:

1. Sensory/tactile design ("puffy" textures, hyper-real objects)
2. Exaggerated, playful type (oversized sans)
3. Immersive high-energy style (saturated palettes)
4. Surreal imagery
5. Organic/imperfect design
6. Freeform editorial layouts
7. Warm, personal style
8. Local/cultural flavour
9. Collage/layering
10. Maximalist "controlled chaos"

No hex values.

**Adobe business "2026 Creative Trends Forecast"** [snippet only; the page timed out twice]. Summarised as a move toward "organic, analog, realistic, human-centered design" as a backlash against hi-tech styling.

**Figma, "Top Web Design Trends for 2026"** (undated resource page) [9]:

- 3D/immersive
- Experimental navigation
- Vibrant palettes ("dopamine", Y2K)
- Bold/kinetic typography
- **Dark mode as a standard feature**
- Motion design (scroll-triggered animation, micro-interactions)
- Gamification
- Neumorphism
- **Retrofuturism with neon accents**
- Maximalism
- Collage
- Neo-brutalism
- Sustainable web design

**Figma, State of the Designer 2026** [10]: the landing page was opened but the data sits behind a form. The survey figures below are **[snippet only]**: 906 designers surveyed, and 91% say AI tools improve their designs.

**Behance Trend Report 2025/26** [snippet only; only an Instagram post and third-party galleries were found, and no Behance-published report page was opened]. Themes attributed to it: refined or "vibrant" minimalism (clean layout, bold type, colour pops), human-centred imperfection, texture and grain.

**Shutterstock:**

- No 2026 "Creative Trends" report was found. Shutterstock's current flagship is the **2025 Creative Impact Report** [11]. It contains no colour trends. Findings:
  - 61% of audiences are more inclined to share immersive or interactive experiences.
  - Believability drops after three campaign messages.
  - Branded GIFs had engagement up to 4.8× GIPHY benchmarks.
- A Shutterstock investor release notes that 2026 is crowded with the Winter Olympics, the FIFA World Cup and the US midterms [snippet only].

#### 1.4 Published 2027 web/UI trend forecasts — ALL PROJECTIONS
These come from agencies and content marketers. None is a standards body or a research institution.

- **WebFX (Macy Storm, 10 Oct 2025) — PROJECTION** [12]. Twenty "2027 trends":
  - predictive UX, cognitive-inclusive (neurodiverse) design, conversational/chat-first UI, hyper-personalisation
  - dark mode, ethical/inclusive design, illustration, animation, brutalism, minimalism with micro-interactions
  - experimental navigation, organic themes, vintage, **data-driven design**, gamification, collage, AR/VR
  - **real-time content**, emotional design
- **Graticle Design, "Way Too Early 2027 Web Design Predictions" (early 2026) — PROJECTION** [13]:
  - conversational "Oracle" interfaces replacing menus
  - ambient/context-adaptive design
  - "anti-aesthetic" rawness
  - **"proof of personhood"** (human-made signals)
  - dynamic, personalised homepages
  - spatial/3D UI on 2D screens
  - decentralised identity logins
- Other 2027 lists (viton13, Devoq, draftly, WetNose, gitinfosys) were **[snippet only]** and were not opened.

---

### 2. Sports brand and media visual trends, 2023–2026

| Brand | When | What changed | Source |
|---|---|---|---|
| **FIFA World Cup 26** | Launched 17–18 May 2023, Griffith Observatory, LA | **First World Cup emblem to use a photographic trophy.** The "26" is built from 48 squares and quarter-circles, one per team. The main mark is black and white (gold trophy). There are 16 host-city colourways, a custom tournament typeface, and Noto Sans as the secondary face. Campaign line: "We Are 26". | [14] (1000logos, 23 May 2023). Design Week original returned 403. |
| FWC26 typeface | Used through the June–July 2026 tournament | Custom face by **Pangram Pangram**, used mostly in all-caps **Ultra Condensed Black**. Typographer Oliver Schöndorfer criticises it for UI use: at small sizes the counters close up, the slashed zero reads as an 8, and country codes blur. His advice is to use "slightly wider and not too bold" cuts for UI and keep ultra-condensed for display. | [15] (Pimp my Type, 18 Jun 2026, upd. 8 Jul 2026) |
| **UEFA Champions League 24/27** (Vasava) | 2024 | Starball redrawn as refracting glass ("Kick of Light"). **Champions Display Refracted**, where each character can take a different colour and edges carry a prismatic gradient, plus new Italic/"Ritalic" styles. Light-wave texture, updated broadcast motion (wipes, lower thirds), and a brief to be "more colourful, bolder and younger". | [16] |
| UCL final identities | Annual | Artist-led host-city identity each year, e.g. Supermundane for London 2024. The trophy stays central. | [17] (UEFA, 31 Aug 2023) |
| **Bundesliga / 2. Bundesliga** (Mutabor + DFL) | Launched for 2025/26 | Moves away from flat design toward **texture, spatiality and 3D elements**. A "slider" switches between 'Official' and 'Dynamic' tonalities. AI was used for a key-visual setting. A **new expressive "tape-like" special font** is added to the proprietary type system. The player icon is redrawn in 2D and takes on club colours or Bundesliga red. | [18] (Creative Bloq, by Heinrich Paravicini of Mutabor, 16 Feb 2026). Some icon details are **[snippet only]**. |
| **ESPN** | DTC app launched 21 Aug 2025; brand guidelines formalised Mar 2026 | First formal brand guidelines in ESPN's roughly 50-year history. Logo and custom typeface **"Ignite"** all slant at **7°**, and there is a "speedline" motion device. A single ESPN red was chosen from about two dozen, with "web accessibility and digital visibility" as the criteria. Built for work from phone icon to billboard. | [19] (Marketing Brew, 9 Mar 2026), [20] (ESPN Press Room, 27 Mar 2026) |
| **Sky Sports** (F37) | 15 Oct 2025 | Type-led redesign. **Sky Sports Sans** comes in five weights and replaces six sport-specific fonts. It has "angular cuts, sharp terminals" and motion rules that vary by sport. Framing: "live is still king", with social clips as the surrounding layer. | [21] (Design Week, Rob Alderson) |
| **Premier League** | Digital relaunch 1 Jul 2025 | Rebuilt web and app: **Matchday Live** (verified scores, stats, table), **vertical "Matchday Stories"**, myPremierLeague personalisation, and an **AI assistant (Microsoft Copilot)** over 30+ seasons of data. The visual identity is still essentially the 2016 DesignStudio system (lion, Premier Sans, five bright colours); no newer rebrand was found. | [22] (PL, 1 Jul 2025); 2016 identity [snippet only] |
| **NBA on NBC/Peacock** | From Oct 2025 | Streaming data layer: "Performance View" overlays (player pointers, shooting streaks, scoring-probability zones), real-time stats in browse, "Key Play Catch-Up", vertical 9:16 highlight clips, predictive game. | [23] (SVG, 21 Oct 2025) |
| ESPN college football graphics | Sep 2025 | Two-year graphics and branding overhaul | [snippet only; NewscastStudio returned 403] |
| Tottenham Hotspur | n.d. | Variable type family developed from TH Caps | [snippet only] |

**Cross-cutting visual patterns (with sources):**

- **Condensed or heavy display type for scores and headlines.** Seen in FWC26 [15] and in bold, wide or condensed faces for LED and venue screens [24]. The lesson from FWC26 is to pair condensed display type with a wider, lighter UI cut [15].
- **Custom type systems replacing several fonts.** Sky Sports Sans [21], ESPN Ignite [19], Bundesliga's proprietary type [18], and UCL Champions Display Refracted [16].
- **Neon, glow and high-chroma accents.** Seen in "neon & glowing effects" and electric gradients for stats [24] and in "retrofuturism with neon accents" [9]. The UCL prismatic refraction [16] is a more refined version of the same idea.
- **Dark UI.** Dark mode is treated as a standard feature [9][12]. A 2026 blog summary describes near-black bases with a single high-energy accent and oversized numerals for live stats [snippet only].
- **Motion as part of the brand.** Examples: the ESPN speedline [20], Bundesliga's "motion first" approach [18], UCL broadcast wipes [16], and Sky's per-sport motion rules [21].
- **Texture and tactility returning after flat design.** Seen in Bundesliga [18], Adobe [8] and Behance [snippet only].
- **Variable fonts.** Beyond Tottenham [snippet only], none of the opened sources confirms that a current sports identity ships as a variable font. Treat this as a technical choice, not a documented sports trend.

---

### 3. UX/UI best practice (primary sources)

#### 3.1 Core Web Vitals (web.dev, page updated 31 Oct 2024) [25]
| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP | ≤ 2.5 s | 2.5–4 s | > 4 s |
| INP | ≤ 200 ms | 200–500 ms | > 500 ms |
| CLS | ≤ 0.1 | 0.1–0.25 | > 0.25 |

Measure at the **75th percentile** of page loads, separately for mobile and desktop [25].

#### 3.2 WCAG 2.2 (W3C Recommendation, current version dated 12 Dec 2024) [26]

- **1.4.3 Contrast (Minimum), AA:** 4.5:1 for text; 3:1 for large text (≥ 18pt, or ≥ 14pt bold).
- **1.4.11 Non-text Contrast, AA:** 3:1 for UI components and meaningful graphics. This covers chart lines, bars, icons and focus rings.
- **1.4.1 Use of Color, A:** colour must not be the only way information is conveyed.
- **1.4.10 Reflow, AA:** content must work at 320 CSS px wide.
- **2.2.2 Pause, Stop, Hide, A:** moving or auto-updating content lasting more than 5 s needs a pause mechanism. **This covers score tickers and carousels.**
- **2.4.7 Focus Visible, AA.**
- **2.4.11 Focus Not Obscured (Minimum), AA:** sticky headers and footers must not fully hide the focused element.
- **2.4.13 Focus Appearance is AAA, not AA** [26][27]. It asks for an indicator at least as large as a 2 CSS px perimeter with 3:1 change contrast. It is still a good target, but it is not required for AA.
- **2.5.8 Target Size (Minimum), AA:** targets at least **24×24 CSS px**. Exceptions: enough spacing (a 24 px circle that does not overlap), an equivalent control, inline links, user-agent controls, and essential cases such as maps and data visualisations. W3C recommends meeting 24×24 regardless of spacing [28].
- **2.3.3 Animation from Interactions, AAA:** motion triggered by interaction can be disabled.

#### 3.3 Touch targets on native platforms

- **Apple HIG:** iOS/iPadOS default control size **44×44 pt**, minimum **28×28 pt**. macOS default 28×28 pt [29] (read from Apple's HIG JSON data).
- **Android / Material:** at least **48×48 dp** (about 9 mm), with **8 dp** or more between targets [30].

#### 3.4 Navigation (Nielsen Norman Group)

- **Hidden (hamburger) vs visible navigation:** visible or combination navigation was found and used more, and faster, than hidden navigation. On Bloomberg's hidden menu, 44% of users used the navigation. BBC's visible/combo navigation had the fastest time to first use, at 21 s. If navigation must be hidden, make it prominent and labelled rather than icon-only [31] (Pernice & Budiu, 24 Jul 2016).
- **Tab bar vs hamburger:** a tab or navigation bar suits about 4–5 top-level options. Beyond 5, touch targets get too small. Hamburger menus suit content-heavy, browse-mostly sites [32] (Budiu, 2015).
- These are NNG's latest articles on the topic but they are dated (2015–16). The principles are durable; the specific numbers are old.

#### 3.5 Data tables on mobile (NNG, Schade, 17 Sep 2017) [33]

- Sticky column headers and a **sticky first column**.
- Clear horizontal-scroll cues (cut-off content or arrows, not dots).
- Legible column widths; complex tables may fit only two readable columns.
- Let users choose which rows or columns to show.
- Accordions for grouped data.
- Don't force landscape.
- Design the desktop table first.

#### 3.6 Infinite scroll vs pagination (NNG, Neusesser, 4 Sep 2022) [34]

- **Infinite scroll** suits aimless browsing of homogeneous feeds such as news streams.
- It is a poor fit when users need to find, compare or reach the footer.
- **"Load more"** keeps the footer reachable and gives users control.
- Pitfalls: Back returns to the top, an "illusion of completeness", and slow loads.

#### 3.7 Dark mode (NNG, Budiu, 2 Feb 2020) [35]

- In studies, light mode (positive polarity) performs better for people with normal vision, especially with small text.
- Dark mode helps some users with visual impairments, e.g. cataracts.
- **Do not default everyone to dark.** Let users switch. Reading-heavy products (news, magazines) should offer dark mode throughout.
- Material's dark-theme guidance (e.g. #121212 surfaces) could not be verified because the page is JS-rendered. **Not cited.**

#### 3.8 Data visualisation accessibility

- **Datawrapper (Lisa Charlotte Muth, 23 Jun 2020)** [36]:
  - Blue is the safest hue; blue with orange or red is the most reliable pair.
  - Avoid green with red or orange at the same lightness.
  - "Get it right in black & white."
  - Use direct labels rather than legends, plus shapes, dashes and patterns.
  - Keep to 3–4 colours at most.
  - Test with simulators such as Coblis and Color Oracle.
- **Okabe & Ito, Color Universal Design** (2002, rev. 2008) [37]: eight-colour colour-blind-safe palette (black, orange, sky blue, bluish green, yellow, blue, vermillion, reddish purple). The page opened did not state RGB/hex values in text, so none are given here.
- **W3C WAI Complex Images tutorial** (updated 8 Apr 2026) [38]: charts need a short alt text plus a long description, preferably including the underlying **data table**. Use figure/figcaption or an adjacent link.
- **FT Visual Vocabulary** [39]: chooses chart type by relationship. The nine categories are deviation, correlation, ranking, distribution, change over time, magnitude, part-to-whole, spatial, and flow.
- WCAG 1.4.1 and 1.4.11 [26]: never rely on colour alone, and keep 3:1 contrast for chart marks.

#### 3.9 Motion

- **`prefers-reduced-motion`** (MDN) [40]: values `reduce` and `no-preference`. Baseline "widely available" since January 2020. Scaling and panning animations can trigger vestibular disorders.
- Reduced-motion toggles exist in macOS, iOS, Windows 11, Android 9+, GNOME and KDE.

#### 3.10 Live updates for assistive tech (MDN ARIA live regions) [41]

- Use `aria-live="polite"` by default. Use `assertive` sparingly.
- `role="status"` or `role="log"` suit live commentary.
- `role="marquee"` (tickers) and `role="timer"` are implicitly `aria-live="off"`.
- Use `aria-atomic="true"` so a score such as "2–1" is read in full, not just the digit that changed.
- The live region must exist in the DOM before updates arrive.

#### 3.11 Responsive breakpoints (common defaults)

- **Bootstrap 5.3** [42]: <576 (xs), ≥576 sm, ≥768 md, ≥992 lg, ≥1200 xl, ≥1400 xxl.
- **Tailwind CSS** [43]: sm 640 (40rem), md 768 (48rem), lg 1024 (64rem), xl 1280 (80rem), 2xl 1536 (96rem). Container queries are built in, with sizes from 256 to 1280 px.
- Design down to **320 CSS px** for WCAG Reflow [26].

#### 3.12 Mobile vs desktop share

- **StatCounter, worldwide, all web, August 2026:** mobile **49.36%**, desktop **49.11%**, tablet **1.54%** [44]. This is all web traffic, not news only.
- **Reuters Institute Digital News Report 2026** (16 Jun 2026; 48 markets, about 2,000 respondents each) [45]:
  - For the first time, social/video networks (54%) are used for news more than publishers' own sites and apps (51%). TV is 52%.
  - Trust in news is 37%.
  - 42% sometimes or often avoid news.
  - AI chatbots are used for news weekly by 10% (16% of under-35s).
  - Trust in chatbot answers is 20%.
  - The executive summary gives **no global smartphone vs computer split**.
- **DNR 2025** (17 Jun 2025, Nic Newman) [46]:
  - The smartphone is the first device checked in the morning in many markets.
  - Social video news use rose from 52% in 2020 to 65%.
  - Respondents expect AI to make news "less trustworthy" (net −18) and "less transparent" (−8).
- India DNR: 68% say the smartphone is their main news device [snippet only].
- Similarweb news-category device split was **not verified**; it is paywalled or needs a connector.

---

### 4. News and sport patterns

#### 4.1 Live blogs

- **Guardian liveblog format (2014):** a clickable "key events" list at the top or left, plus periodic bullet summaries [snippet only; Nieman Lab returned 403]. This pattern is now standard.
- **Reuters Institute / Thurman research (2013):**
  - 11% of UK news consumers used a live page weekly (Japan 35%).
  - Live blogs for breaking news were more popular than sport live blogs.
  - 40% of UK users felt live blogs were more balanced than articles.
  - Readers valued visible corrections [47] (Press Gazette, 20 Jun 2013). **This data is old.**
  - Separately, more than 25% of UK users found live blogs "difficult to understand" [snippet only].
- **schema.org `LiveBlogPosting`** [48]: fields `coverageStartTime`, `coverageEndTime`, and `liveBlogUpdate` (one BlogPosting per update).
- **Google "LIVE" badge for video** (updated 24 Sep 2026) [49]: requires `BroadcastEvent` with `isLiveBroadcast: true`, plus `startDate` and `endDate` (endDate is required once the stream ends). Google suggests the Indexing API for timely crawling.

#### 4.2 Key moments

- **Google video key moments** [49]: two routes. `Clip` markup needs name, startOffset and url; the video must be at least 30 s long; no two clips may share a start time; deep-linkable timestamps are required. The alternative is `SeekToAction`. The `nosnippet` meta tag opts out.
- In-product examples: NBC/Peacock "Key Play Catch-Up" and vertical "Can't Miss Highlights" [23]; Premier League "Matchday Stories" [22].

#### 4.3 Match centres and score tickers

- **Premier League Matchday Live:** verified live scores, stats, reporting and live table, linking out to official broadcasts. Includes a personalised "Line Up" tracker and an AI assistant over historic data [22].
- **Peacock:** live data overlays, stats inside browse, and a companion predictive game [23].
- **Premier League "Match Centre"** is a different thing: an officiating and VAR **explainer** series (e.g. Key Match Incident Panel accuracy of 86%, VAR errors down from 24 to 13) [50]. It is a good model for "why did that happen" explainers.
- Accessibility rules for tickers: WCAG 2.2.2 pause control [26]; ARIA live-region etiquette [41]; sufficient target size and contrast [26][28].

#### 4.4 Stats glossary

- **Opta Analyst definitions** (23 Jul 2024) [51]:
  - xG runs 0–1 and is trained on about one million historical shots.
  - xA is based on pass type, end-point and length.
  - "Big chance" always includes penalties.
  - PPDA = opposition passes outside the pressing team's defensive third ÷ defensive actions.
- Glossary entries should name the data provider, since metric definitions differ between providers.

#### 4.5 AI transparency: EU AI Act Article 50 — VERIFIED as applying from 2 Aug 2026

- **Applies from 2 August 2026**, confirmed by the European Commission [52][53], Cooley [54] and WAN-IFRA Editors Weblog [55].
- **Grace period (adopted, not proposed):** providers of generative systems placed on the market before 2 Aug 2026 have until **2 December 2026** for Art. 50(2) machine-readable marking [53][54][55]. The Digital Omnibus pushed Annex III high-risk duties to 2 Dec 2027, but **did not defer Article 50** [55].
- **Art. 50(4), text:** deployers must disclose AI-generated or manipulated text published to inform the public on matters of public interest. **Exception:** the text has undergone human review or editorial control *and* a natural or legal person holds editorial responsibility [56].
  - The Commission FAQ defines human review as "deliberate examination of the substance".
  - Editorial control means an accountable editorial entity, e.g. an editor-in-chief, that can approve, alter or reject content.
  - **Spell- or grammar-checks alone do not count** [53].
- **Deepfakes** (image, audio, video) must be disclosed. Artistic, satirical or fictional works need only a light-touch notice [56].
- **Chatbots and assistants** must tell users they are interacting with AI [52].
- **Form of disclosure:** "clear and distinguishable", given "at the latest" at first interaction or exposure, and meeting accessibility requirements [56].
- **Supporting material:**
  - The **Code of Practice on Transparency of AI-generated Content** was finalised on 10 Jun 2026, with about 190 signatories by 31 Jul 2026 [57].
  - **The EU has published a standard set of icons** for labelling AI content [52][57].
  - Commission guidelines were adopted on 20 Jul 2026 [54].
- **Penalties:** up to €15 m or 3% of worldwide turnover [52][54].

#### 4.6 Corrections policy

- **BBC Editorial Guidelines 3.4.34** [58]: serious factual errors are corrected "promptly, clearly and appropriately". A correction should say what was wrong as well as putting it right, and be scheduled for the audience that saw the error. The BBC keeps a public Corrections and Clarifications page.

#### 4.7 Trust Project indicators [59] (© 2016 Trust Project)

1. Best Practices (funding, mission, standards, ethics/corrections policies)
2. Journalist Expertise
3. Type of Work (news / opinion / analysis / sponsored labels)
4. References
5. Methods
6. Locally Sourced
7. Diverse Voices
8. Actionable Feedback

---
---

### IMPLICATIONS FOR GAMEFORMATIVE (interpretation, not findings)

1. **Palette.**
   - Use a near-neutral base, either Cloud-Dancer-style off-white or a dark neutral, with **one high-chroma accent** for live and interactive states.
   - The WGSN 2027 projections (Luminous Blue, Energy Orange, Pop Pink) fit sport well. **Blue with orange** is also Datawrapper's most colour-blind-safe pair [36]. Consider saturated blue as the brand colour, orange as the "live/alert" colour, and grey for context.
   - Derive our own hex values and check every pair against 4.5:1 for text and 3:1 for UI and chart marks.
2. **Themes.**
   - Offer light and dark from launch, with a user toggle plus `prefers-color-scheme`.
   - Default to light for long-form reading, following NNG [35].
   - Dark suits match-centre and live views, where the pattern is well established. Keep dark optional; don't make it the only mode.
3. **Type.**
   - Use a **condensed/heavy display cut** for scores, numerals and hero headlines, which matches the current sports norm.
   - Use a **wider, lighter companion** for UI labels, tables and body text.
   - Use tabular numerals in stats.
   - A single variable family (width and weight axes) would cover both roles in one file. That is our engineering choice, not a sourced trend.
4. **Performance budget.** Aim for LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1 at p75 on mobile. Live tickers and ad slots must reserve their space to protect CLS.
5. **Navigation.**
   - Mobile: a visible bottom tab bar of at most 5 items, e.g. Home / Live / Stats / Explainers / Search. Add a labelled "More" menu instead of a bare hamburger.
   - Desktop: visible top navigation.
6. **Targets.** Build all tappable elements at 44×44 px or more. This clears Apple 44 pt and roughly Material 48 dp; 24×24 is only the WCAG AA floor.
7. **Stats tables.** Use a sticky header and sticky first column, column pickers, and clear horizontal-scroll cues. Always offer the table as the accessible fallback for every chart.
8. **Charts.**
   - Pick chart types with the FT Visual Vocabulary.
   - Use direct labels and shape or dash encoding, not colour alone.
   - Provide alt text plus a long description or data table.
9. **Live pages.**
   - Pin a "key events" or "key moments" rail and add periodic summaries.
   - Use `LiveBlogPosting` markup, and `BroadcastEvent`/`Clip` markup for video.
   - Make the score region an `aria-live="polite"` region with `aria-atomic="true"`.
   - Give tickers a pause control.
   - Honour `prefers-reduced-motion` for all goal and score animations.
10. **Feeds.** Use "Load more" rather than pure infinite scroll on section fronts. This keeps the footer (corrections, policies) reachable and preserves scroll position when users come back.
11. **Trust and AI.**
    - If any content is AI-assisted, run a documented editorial-review workflow with a named responsible editor. That keeps AI-assisted text inside the Art. 50(4) exception.
    - Still label AI-generated media, synthetic imagery and any chatbot. Consider the EU icon set.
    - Publish a corrections page, an AI-use policy, bylines with expertise, and news/analysis/opinion labels, covering the Trust Project indicators.
    - Publish a stats glossary that names the data provider.
12. **Audience.** Global web traffic is about 50/50 mobile and desktop, and news discovery is shifting to social and video [44][45]. Design mobile-first but keep desktop dense and data-rich. Plan vertical clip formats and shareable stat cards for social distribution.

---

### Sources (all opened unless marked)

1. Pantone — "Pantone Introduces the Pantone Color of the Year 2026" (press release), 4 Dec 2025. https://www.pantone.com/articles/press-releases/pantone-announces-color-of-the-year-2026-cloud-dancer
2. Pantone — Color of the Year 2026 page (n.d.). https://www.pantone.com/na/en-us/color-of-the-year/2026
3. Young House Love — "Every 2027 Color of the Year (So Far!)", 24 Aug 2026, upd. 16 Sep 2026. https://www.younghouselove.com/2027-color-of-the-year/
4. WGSN — "Colour of the Year 2026: Transformative Teal", 3 Sep 2024. https://www.wgsn.com/en/blog/colour-year-2026-transformative-teal
5. WGSN — "Key Colours A/W 26/27", 7 Oct 2024. https://www.wgsn.com/en/blog/key-colours-w-26-27
6. WGSN — "WGSN and Coloro reveal Colour of the Year 2027, Luminous Blue, and the S/S 27 Key Colours" (press release), 29 Apr 2025. https://www.wgsn.com/en/wgsn/press/press-releases/wgsn-and-coloro-reveal-colour-year-2027-luminous-blue-and-s-s-27-key
7. FashionUnited — "WGSN and Coloro: Key colours for autumn/winter 2027/28", 17 Sep 2025. https://fashionunited.com/news/fashion/wgsn-and-coloro-key-colours-for-autumn-winter-2027-28/2025091768269
8. Adobe Express — "Top 10 graphic design trends for 2026", 12 Dec 2025. https://www.adobe.com/express/learn/blog/design-trends-2026
9. Figma — "Top Web Design Trends for 2026" (resource library, undated). https://www.figma.com/resource-library/web-design-trends/
10. Figma — State of the Designer 2026 (landing page; data gated). https://www.figma.com/reports/state-of-the-designer-2026/
11. Shutterstock — 2025 Creative Impact Report (2025). https://www.shutterstock.com/creative-impact-report
12. WebFX — Macy Storm, "Web Design Trends in 2027", 10 Oct 2025. https://www.webfx.com/blog/web-design/web-design-trends/
13. Graticle Design — "Way Too Early 2027 Web Design Predictions", early 2026. https://graticle.com/blog/way-too-early-2027-web-design-predictions/
14. 1000logos — Alexander Shapkin, "2026 FIFA World Cup identity introduces new design system", 23 May 2023. https://1000logos.net/news/2026-fifa-world-cup-identity-introduces-new-design-system/
15. Pimp my Type — Oliver Schöndorfer, "FIFA's World Cup Typography Foul: UI Design Learnings", 18 Jun 2026 (upd. 8 Jul 2026). https://pimpmytype.com/fifa-2026-font/
16. Vasava — "UEFA Champions League 24/27 Rebranding" (2024). https://www.vasava.es/en/portfolio/uefa-champions-league
17. UEFA — "Brand identity unveiled for the 2024 UEFA Champions League final", 31 Aug 2023. https://www.uefa.com/news-media/news/0284-18ddf64c1e93-e5c9c405914f-1000--brand-identity-unveiled-for-the-2024-uefa-champions-league-/
18. Creative Bloq — Heinrich Paravicini (Mutabor), "How we refreshed the German national football league identity… 5 times", 16 Feb 2026. https://www.creativebloq.com/design/branding/how-we-refreshed-the-german-national-football-league-identity-5-times
19. Marketing Brew — Alyssa Meyers, "ESPN never had one official brand identity—until now", 9 Mar 2026. https://www.marketingbrew.com/stories/2026/03/09/espn-brand-identity
20. ESPN Press Room — John Manzo, "ESPN's new brand identity: built for how fans live sports", 27 Mar 2026. https://espnpressroom.com/feature/espns-new-brand-identity-built-for-how-fans-live-sports/
21. Design Week — Rob Alderson, "Type-led Sky Sports redesign aims to 'put the love back' into the brand", 15 Oct 2025. https://www.designweek.co.uk/type-led-sky-sports-redesign-aims-to-put-the-love-back-into-the-brand/
22. Premier League — "Premier League launches fan-facing platforms as part of digital transformation", 1 Jul 2025. https://www.premierleague.com/en/news/4337361/premier-league-launches-new-fan-facing-platforms-as-part-of-digital-transformation
23. Sports Video Group — Jason Dachman, "NBA on NBC/Peacock: Livestream Offers Graphic Overlays…", 21 Oct 2025. https://www.sportsvideo.org/2025/10/21/nba-on-nbc-peacock-livestream-offers-graphic-overlays-predictive-gaming-ancillary-camera-angles-real-time-highlights/
24. ScoreVision — "Top 4 Trends for Sports Graphics 2025–2026", 6 Aug 2025. https://blog.scorevision.com/top-4-trends-for-sports-graphics-2025-2026
25. web.dev (Google) — "Web Vitals", upd. 31 Oct 2024. https://web.dev/articles/vitals
26. W3C — Web Content Accessibility Guidelines (WCAG) 2.2, W3C Recommendation, 12 Dec 2024. https://www.w3.org/TR/WCAG22/
27. W3C WAI — Understanding SC 2.4.13 Focus Appearance. https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
28. W3C WAI — Understanding SC 2.5.8 Target Size (Minimum). https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
29. Apple — Human Interface Guidelines: Accessibility (read via HIG JSON data endpoint). https://developer.apple.com/design/human-interface-guidelines/accessibility
30. Google — Android Accessibility Help, "Touch target size". https://support.google.com/accessibility/android/answer/7101858
31. Nielsen Norman Group — Kara Pernice & Raluca Budiu, "Hamburger Menus and Hidden Navigation Hurt UX Metrics", 24 Jul 2016. https://www.nngroup.com/articles/find-navigation-mobile-even-hamburger/
32. Nielsen Norman Group — Raluca Budiu, "Basic Patterns for Mobile Navigation", 15 Nov 2015. https://www.nngroup.com/articles/mobile-navigation-patterns/
33. Nielsen Norman Group — Amy Schade, "Mobile Tables", 17 Sep 2017. https://www.nngroup.com/articles/mobile-tables/
34. Nielsen Norman Group — Tim Neusesser, "Infinite Scrolling: When to Use It, When to Avoid It", 4 Sep 2022. https://www.nngroup.com/articles/infinite-scrolling-tips/
35. Nielsen Norman Group — Raluca Budiu, "Dark Mode vs. Light Mode", 2 Feb 2020. https://www.nngroup.com/articles/dark-mode/
36. Datawrapper — Lisa Charlotte Muth, "How to use colors in data visualization for colorblind readers (part 2)", 23 Jun 2020. https://www.datawrapper.de/blog/colorblindness-part2
37. Okabe, M. & Ito, K. — "Color Universal Design", 2002 (rev. 2008). https://jfly.uni-koeln.de/color/
38. W3C WAI — Images Tutorial: Complex Images, upd. 8 Apr 2026. https://www.w3.org/WAI/tutorials/images/complex/
39. Financial Times — Visual Vocabulary (chart-doctor repo). https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary
40. MDN — "prefers-reduced-motion". https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
41. MDN — "ARIA live regions". https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
42. Bootstrap — v5.3 Breakpoints. https://getbootstrap.com/docs/5.3/layout/breakpoints/
43. Tailwind CSS — Responsive design. https://tailwindcss.com/docs/responsive-design
44. StatCounter Global Stats — Desktop vs Mobile vs Tablet Market Share Worldwide, Aug 2026. https://gs.statcounter.com/platform-market-share/desktop-mobile-tablet
45. Reuters Institute — Digital News Report 2026, Executive summary, 16 Jun 2026. https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary
46. Reuters Institute — Nic Newman, Digital News Report 2025, Executive summary, 17 Jun 2025. https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025/dnr-executive-summary
47. Press Gazette — Neil Thurman, "Reuters Institute survey reveals growing global popularity of live blogs", 20 Jun 2013. https://pressgazette.co.uk/publishers/digital-journalism/reuters-institute-survey-reveals-growing-global-popularity-of-live-blogs/
48. schema.org — LiveBlogPosting. https://schema.org/LiveBlogPosting
49. Google Search Central — Video structured data (BroadcastEvent / Clip / SeekToAction), upd. 24 Sep 2026. https://developers.google.com/search/docs/appearance/structured-data/video
50. Premier League — "Premier League Match Centre update MW21-25", 21 Feb 2025. https://www.premierleague.com/en/news/4251195
51. Opta Analyst — "Opta Football Stats Definitions", 23 Jul 2024. https://theanalyst.com/articles/opta-football-stats-definitions
52. European Commission — "Safer and more transparent AI", 2 Aug 2026. https://commission.europa.eu/news-and-media/news/safer-and-more-transparent-ai-2026-08-02_en
53. European Commission (Shaping Europe's digital future) — FAQ "Transparency obligations under Article 50 of the AI Act", 24 Jul 2026. https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
54. Cooley — "EU AI Act: Transparency Obligations Take Effect 2 August 2026", 3 Aug 2026. https://www.cooley.com/news/insight/2026/2026-08-03-eu-ai-act-transparency-obligations-take-effect-2-august-2026
55. Editors Weblog (WAN-IFRA) — "The EU AI Act Timeline: Key Dates and Deadlines for Publishers", 7 Jul 2026. https://editorsweblog.org/2026/07/07/eu-ai-act-timeline-deadlines-publishers
56. artificialintelligenceact.eu — Article 50 text (Regulation (EU) 2024/1689). https://artificialintelligenceact.eu/article/50/
57. European Commission — Code of Practice on Transparency of AI-generated Content (final 10 Jun 2026). https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
58. BBC — Editorial Guidelines, Section 3 Accuracy, 3.4.34 "Correcting Mistakes" (fetched via curl). https://www.bbc.co.uk/editorialguidelines/guidelines/accuracy/guidelines
59. The Trust Project — Trust Indicators (© 2016). https://thetrustproject.org/resources-2/

**Snippet-only / not opened:**

- TIME/CNN/NPR on Pantone's "first white"
- Adobe business 2026 forecast (page timed out)
- Behance Trend Report
- Figma State of the Designer statistics
- Shutterstock investor release
- Other 2027 trend lists (viton13, Devoq, draftly, WetNose, gitinfosys)
- Design Week FIFA article (403)
- NewscastStudio ESPN CFB article (403)
- Tottenham variable font
- Premier League 2016 identity details
- Nieman Lab Guardian liveblog article (403)
- Live-blog "difficult to understand" statistic
- India DNR 68% smartphone figure
- Dark-mode sports dashboard blog
- Material dark theme (#121212, JS-only page)

