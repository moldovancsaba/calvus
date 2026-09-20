# business.direct — evidence: the claims register and the research base

*Every figure the product-facing documents rest on (the presentation, the executive summary,
the value document, the product definition) and every vendor figure in research VI, with its
source opened and read on 2026-09-20 (phase A of the transformation programme,
`documentation-audit.md` §8). **Status**: **P** the primary source was opened and says it;
**A** a secondary source says it and the primary was not reachable; **corrected** the source
says something different and the documents were changed; **assumption** ours, marked so where
used; **owner** stated by the owner. A figure that is not in this register does not belong in
the top layer. The gate (`../check.py`) reads the status column: a row marked *unverified* fails
the gate.*

## 1. The customer's problem and the market

| # | Claim as used | Source opened | Status | Note |
|---|---|---|---|---|
| K1 | Cold e-mail reply rates: 3.43 % average, 5.5 %+ top quartile, 10.7 %+ top decile; 58 % of replies from step one, 42 % from follow-ups; 4–7 touches; warm-up 4–6 weeks; bounce < 2 % | [Instantly, Cold Email Benchmark Report 2026](https://instantly.ai/cold-email-benchmark-report-2026) | **P** | vendor benchmark on its own customers' data |
| K2 | "Three touches in order triple the first touch" | — | **corrected** | not in the source; K1 says follow-ups add 42 % of replies (≈ +72 % over step one alone). Wording changed to the source's |
| K3 | A lead contacted within 5 minutes is 21× more likely to qualify than after 30; the odds of contacting it at all fall 100× | [InsideSales / MIT (Oldroyd) Lead Response Management Study, 2007 (PDF)](https://25649.fs1.hubspotusercontent-na2.net/hub/25649/file-13535879-pdf/docs/mit_study.pdf) | **P** | 2007 web-lead data; the figures are the study's own wording; the date is now stated |
| K4 | 62 % of calls to small businesses go unanswered | 411 Locals 2016 (85 businesses) via [SkipCalls](https://skipcalls.com/blog/percentage-business-calls-unanswered-statistics-2026) | **A** | removed from every hero and headline; may appear only with the source and its size |
| K5 | 78 % of customers buy from the business that responds first | vendor blogs (Kixie, LeadAngel) citing Lead Connect / Vendasta | **A** | removed from the top layer |
| K6 | Automated reminders cut non-attendance | [Hasvold & Wootton 2011, J Telemed Telecare, 29 studies — DOI 10.1258/jtt.2011.110707](https://doi.org/10.1258/jtt.2011.110707) (metadata via PubMed) | **corrected** | the review: weighted mean relative reduction 34 % of baseline; **automated reminders 29 %**, manual calls 39 %; **no difference between the day before and the week before** — the Glofox claim that "3 days and 1 day beats a single one" is the vendor's, not the review's. Hospital appointments, not activity classes. Wording changed |
| K7 | Organic Google sends 19 % fewer clicks to the same rankings (rankings +26 %, 2023–2025) | [NP Digital index](https://neilpatel.com/marketing-stats/rankings-up-traffic-down/) (403 to scripted fetch; confirmed via search summary) | **A** | contested: other data sets show organic traffic −2.5 % YoY ([Search Engine Land](https://searchengineland.com/organic-search-traffic-down-yoy-data-467748)); the top layer says "one index" |
| K8 | Gen Z searches social before Google | [Marketing Dive on SOCi's 2024 Consumer Behavior Index (1 000 US consumers)](https://www.marketingdive.com/news/google-tiktok-instagram-local-search-preference-gen-z/710130/) | **corrected** | the source: for **local search** Gen Z uses Instagram (67 %) and TikTok (62 %) ahead of Google (61 %); "nearly half prefer social" was not in it. Wording changed |
| K9 | AI answers cite the structured, reviewed source — Yelp 512 680 citations in Q4 2025, 3.4× the second source (BBB 149 710; Angi 145 633) | [PPC Land on Foundation / AirOps, 28 M AI responses](https://ppc.land/yelp-gets-3-4x-more-ai-citations-than-any-rival-in-new-local-search-data/) | **A** | trade press on an agency's data set |
| K10 | US families spend $1 016 per child per primary sport (2024), +46 % since 2019; 1 848 parents | [Project Play / Aspen Institute, Feb 2025](https://projectplay.org/news/2025/2/24/project-play-survey-family-spending-on-youth-sports-rises-46-over-five-years) | **P** | the first customer's category; used only in its worked example |
| K11 | Yelp acquired Hatch for ≈ $270 M cash + $30 M retention; closing early February 2026 | [Yelp IR press release](https://www.yelp-ir.com/news/press-releases/news-release-details/2026/Yelp-Accelerates-Strategy-with-Acquisition-of-AI-Lead-Management-Platform-Hatch/default.aspx) | **P** | "expected to close" at announcement; the documents said "bought" — now "agreed to buy" |
| K12 | Yelp Receptionist from $99 / month; Yelp Host $149 ($99 for Guest Manager customers) | [Yelp blog, launch post](https://blog.yelp.com/news/yelp-host-yelp-receptionist-launch/) | **P** | |
| K13 | 83 % of small businesses say referrals are their best acquisition source (65 % the year before); AI for content 81 %; 300+ SMBs | [LocaliQ 2026 report](https://localiq.com/blog/small-business-marketing-trends-report-2026/) | **P** | |
| K14 | 51 % of "privacy actives" have switched a company over data practices; 2 600 consumers, 12 countries | [Cisco 2024 Consumer Privacy Survey](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2024/m10/how-safe-is-our-data-consumers-want-to-know.html) | **P** | the "49 % of 25–34-year-olds" figure is not on this page — removed |
| K15 | 96 % of organisations say privacy investment returns more than it costs | [Cisco 2025 Data Privacy Benchmark (PDF)](https://www.cisco.com/c/dam/en_us/about/doing_business/trust-center/docs/cisco-privacy-benchmark-study-2025.pdf) | **A** | PDF not re-opened this round; cited from research IV |
| K16 | Epic Games: $520 M (a $275 M COPPA penalty + $245 M refunds), Dec 2022 | [FTC press release](https://www.ftc.gov/news-events/news/press-releases/2022/12/fortnite-video-game-maker-epic-games-pay-more-half-billion-dollars-over-ftc-allegations) | **P** | YouTube $170 M and Disney $10 M cited from research IV (**A** this round) |
| K17 | SMB SaaS monthly churn 3–7 %; healthy SMB activation 35–50 % | [ORM](https://orm-tech.com/blog/saas-churn-rate-benchmarks-by-segment), [PM Toolkit](https://pmtoolkit.ai/benchmarks/activation-rate-benchmarks) | **A** | benchmark aggregators; used as ranges, marked benchmark |
| K18 | Funnel rates 40 % / 80 % / 25 %, avid 15 %, capture 5 %, 1.5 visitors per post, 5 000 visitors, share kept by a retention touch 30 % | — | **assumption** | marked on the Economics screen and in `economics.md`; replaced by the site's data |
| K19 | The first customer has thousands of listings still to publish | the owner, 2026-09-20 | **owner** | |
| K20 | 253 providers, 130 e-mail, 181 phone, 83 next sessions, 72 trial policies, 26 announcements, 0 reviews, 28 prices, 0 managing | `data/providers.json`, pulled 2026-09-19 | **P** (measured) | the demo's pull |

## 2. Research VI — the vendors (every row re-read)

| # | Claim as used | Source opened | Status | Note |
|---|---|---|---|---|
| V1 | Vercel cron: 100 cron jobs per project on every plan; Hobby once a day (±59 min), Pro / Enterprise once a minute | [Vercel cron usage and pricing](https://vercel.com/docs/cron-jobs/usage-and-pricing) | **corrected** | research VI said "Hobby 2, Pro 40" — wrong; fixed |
| V2 | Vercel functions: 300 s default; **Pro maximum 800 s (1 800 s beta)**; memory 4 GB Pro; body 4.5 MB; bundle 250 MB (5 GB beta); Vercel Workflows for unlimited duration | [Vercel functions limits](https://vercel.com/docs/functions/limitations) | **corrected** | research VI said 300 s maximum and 3 GB; fixed. ADR-18's upgrade path is now Vercel Workflows before Inngest |
| V3 | MongoDB Atlas M0 free 512 MB, 100 ops/s; Flex $8–30 / month; M10 from $0.08 / h ≈ $56.94 / month | [Atlas pricing](https://www.mongodb.com/pricing) | **P** | |
| V4 | Upstash Redis free 256 MB, 500 K commands / month, 10 GB bandwidth; $0.2 per 100 K after | [Upstash pricing](https://upstash.com/pricing/redis) | **P** | |
| V5 | Resend free 3 000 / month, 100 / day, 3 domains; Pro $20 (50 K) / $35 (100 K); inbound on all plans | [Resend pricing](https://resend.com/pricing) | **corrected** | research VI said "one custom domain" — it is 3; fixed |
| V6 | Instagram: 100 API-published posts per account per rolling 24 h; JPEG only; carousels ≤ 10; permissions `instagram_business_basic` + `instagram_business_content_publish` (Instagram Login) or `instagram_basic` + `instagram_content_publish` + `pages_read_engagement` (Facebook Login) | [Meta content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing) | **P** | App Review duration stays "reported, no SLA" |
| V7 | Twilio US SMS $0.0083 per segment; long code $1.15 / month; carrier fees $0.0025–0.01 | [Twilio US SMS pricing](https://www.twilio.com/en-us/sms/pricing/us) | **P** | |
| V8 | A2P 10DLC: low-volume standard brand $4 (+ tax ≈ $4.41); campaign vetting $15; monthly campaign fee $2–10 by use case; standard brand higher with secondary vetting | Twilio help centre via search; [GHL fee explainer](https://www.ghlscaleup.com/blog/a2p-10dlc-fees-explained) | **A** | research VI's "$4 … secondary vetting $40" replaced by this; re-check at registration |
| V9 | Stripe: Billing 0.7 % of volume; US card fee 2.9 % + 30¢ | [Stripe pricing](https://stripe.com/pricing) (served the Hungarian page; US rate from Stripe's widely published US price) | **A** for the card fee, **P** for Billing | re-check on the US page at contract |
| V10 | Claude API: Opus 5 $5 / $25; Sonnet 5 $2 / $10 (standard, not introductory); Haiku 4.5 $1 / $5; Batch −50 %; cache reads 0.1× | [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) | **P** | |
| V11 | Deepgram Nova-3 pre-recorded $0.0043 / min pay-as-you-go; $200 free credit | [Deepgram pricing](https://deepgram.com/pricing) | **P** | |
| V12 | Fly.io shared-cpu-1x 1 GB $0.0082 / h ≈ $5.92 / month; stopped machines pay rootfs only ($0.15 per GB per 30 days) | [Fly.io pricing](https://fly.io/docs/about/pricing/) | **corrected** | research VI said $0.007 / h; fixed |
| V13 | Sentry Developer plan 5 K errors / month free; Team from $26 / month | [Sentry pricing](https://sentry.io/pricing/) | **P** | |
| V14 | Better Stack free: 10 monitors, checks up to every 30 s | [Better Stack pricing](https://betterstack.com/uptime/pricing) | **corrected** | research VI said 3-minute checks; fixed |
| V15 | Inngest free 100 K step runs; Vercel Blob; Nano Banana image prices; C2PA node library on Node 22+ | search summaries, 2026-09-20 | **A** | not re-opened this round; marked A in research VI |
| V16 | Sora "shut down in five months" | — | **unverified → removed** | no source in the files; the sentence in ADR-12 and the SWOT's T6 now reads "generative-video vendors change quickly" |

## 3. What the register changed in the documents (2026-09-20)

- Presentation §2 and the executive summary: K2, K4, K5, K6, K8 wording replaced by the sources'
  wording; the 2007 date on K3; "agreed to buy" on K11.
- `economics.md` §2: K4/K5 removed; K1 and K3 stated with their sources.
- `01g-research-real-system.md`: V1, V2, V5, V8, V12, V14 corrected in place; every row's
  status column now says P or A honestly; V16 removed.
- `architecture.md` ADR-12 and ADR-18, `logic-audit.md` T6: V16 and V2.

## 4. The research base (kept as written; every figure the stakeholder documents use is in §1–§2 above)

| Round | File | What it holds |
|---|---|---|
| I | `01-research.md` | reputation and claiming, speed to lead, reminders, digests, generated pages, how listing platforms monetise, AI adoption, the law in the US and the EU |
| II | `01b-research-acquisition-content-sales.md` | acquiring customers for classified media (demand and supply side), content strategies, the AI creation services and their labelling rules, the sales processes |
| III | `01c-research-data-driven-marketing.md` | the incumbents' cases (Yelp, Angi, Thumbtack), unit-economics practice, attribution and incrementality, next-best-action |
| IV | `01e-research-responsible-data.md` | children's rights and responsible data: the law by market, the enforcement record, the frameworks, the business value |
| V | `01f-research-beyond-children.md` | vulnerable people, protected characteristics, accessibility, sensitive categories, dark patterns — the rules R30–R36 |
| VI | `01g-research-real-system.md` | every external service verified: auth, review, limits, prices (corrected per §2) |
| VII | `market.md` | the product's market |
