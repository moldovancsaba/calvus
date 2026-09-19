# business.direct — research II: acquiring customers, content, AI creation services, sales processes

*Second research round, 2026-09-19, on the owner's ask: "based on what we have now and what
the market says about the trends — how to find and acquire customers for classified media
sites, what content strategies content providers use, how to deliver those contents (which
services to add: Higgsfield or other image and video creators, audio creators, other AI
content creation tools and more) — and the same for the sales processes." Every figure
links to where it was read; **P** = primary (the platform, vendor or report itself),
**A** = aggregator or trade article; **V** = read on the vendor's own site with `curl`.
Where a claim could not be verified, §7 says so. The first research round
(`01-research.md`) stands; this one does not repeat it.*

## 1. What we have now

The prototype (`../index.html`, rounds 1–4) already runs the shape the market below
describes: **B2C social publishing** (posts drafted from listing data, approved, scheduled,
with the link back to the listing page), a **B2B provider sales pipeline** (invitation
sequence → reply inbox → apply-to-manage → managing → upgraded), **provider campaigns**
(trial, open spots, announcement, registration), **conversations** (family enquiries with
drafted answers; comments on posts), the **weekly digest and alerts**, **generated pages**
where ≥ 3 providers exist, an **intelligence recap**, **integrations** with a v1 / later
split, a **knowledge layer** of plain files, and the **human gate** on everything that
leaves. What it does *not* have: any content *production* beyond copy — no image, video or
audio creation; no channel adapters (v1 = Instagram + Facebook, e-mail, push); no
deliverability or sending infrastructure; no AI-content marking pipeline; no defined
outbound cadence beyond "invitation → reminder after 5 days → call task". This round asks
what the market says each of those should be.

## 2. How to find and acquire customers for classified media sites — what the market says

### 2.1 The demand side (families / consumers): search is splitting three ways

- **Google organic sends fewer clicks to the same rankings.** From January 2023 to
  December 2025 organic rankings rose 26 % while organic traffic fell 19 %; more than 58 %
  of US Google searches ended without a click in 2025. **A** [NP Digital](https://neilpatel.com/marketing-stats/rankings-up-traffic-down/),
  [Grow & Convert](https://www.growandconvert.com/ai/seo-traffic-decline-chatgpt-ai/)
- **Programmatic (generated) pages are under enforcement.** Google's March 2026 scaled-content
  action stripped 50–80 % of traffic from low-value programmatic sites; marketplaces that
  kept traffic paired templates with real differentiators — reviews, trust signals, local
  intent, schema, internal links. **A** [Vizup](https://www.tryvizup.com/blog/programmatic-seo-trends-2026),
  [Passionfruit](https://www.getpassionfruit.com/blog/programmatic-seo-traffic-cliff-guide),
  [Journey](https://www.journeyh.io/blog/marketplace-seo-playbook). *Our R6 (≥ 3 providers per
  generated page) is the right instinct; the bar is now "a page a parent would bookmark".*
- **Being cited by AI answers is the new listing.** Yelp earned 512,680 citations across
  ChatGPT, Gemini, Perplexity and Google AI Mode in Q4 2025 — 3.4× the second source (BBB
  149,710; Angi 145,633; Thumbtack 56,004; Nextdoor 10,308); AI Mode and Perplexity account
  for 95 % of local-discovery citations. **A** [PPC Land on Foundation/AirOps data](https://ppc.land/yelp-gets-3-4x-more-ai-citations-than-any-rival-in-new-local-search-data/),
  [Foundation](https://foundationinc.co/lab/yelp-ai-local-discovery/). Brands cited in AI
  Overviews get ~35 % more organic clicks than uncited ones. **A** [MADX](https://www.madx.digital/learn/programmatic-seo-ai-overviews)
- **Marketplaces are plugging into the assistants directly.** Thumbtack shipped inside
  ChatGPT (October 2025) and Anthropic's Claude (23 April 2026: find, compare and hire from
  300,000+ businesses inside the conversation). **P** [Claude connector page](https://claude.com/connectors/thumbtack), [Business Wire release, 23 Apr 2026](https://www.businesswire.com/news/home/20260423884720/en/Thumbtack-Delivers-Home-Services-Experience-in-Anthropics-Claude) (the wire blocks scripted fetches; read through the search result); **A** [Viirl](https://viirl.com/blog/yelp-thumbtack-ai-partnerships-home-service-marketing/)
- **Social platforms are the search engine for the parents of 2026.** ~46 % of Gen Z and
  35 % of millennials prefer social platforms over search engines; 40–46 % of young users
  go to TikTok or Instagram before Google Maps for a place to eat, shop or explore; Reels
  and Shorts are indexed by keyword and surfaced to non-followers. **A** [Marketing Dive](https://www.marketingdive.com/news/google-tiktok-instagram-local-search-preference-gen-z/710130/),
  [Surmado](https://www.surmado.com/blog/gen-z-tiktok-local-discovery),
  [ALM](https://almcorp.com/blog/youtube-tiktok-instagram-social-seo-2026/). 73 % of internet
  users 16+ research brands on social. **P** [HubSpot statistics](https://www.hubspot.com/marketing-statistics)
- **Owned audiences beat rented ones.** Newsletter platforms grow "product- and community-led":
  beehiiv reports ~90 % of monthly growth unpaid and sells subscriber acquisition at ~$1.50
  per confirmed opt-in through cross-recommendations. **A** [Sacra](https://sacra.com/c/beehiiv/),
  [emailtooltester](https://www.emailtooltester.com/en/reviews/beehiiv/). The parent-media
  incumbent in Your Field's city, Mommy Poppins, sells exactly this: newsletter placements
  and social campaigns targeted by metro, child age bracket and interest. **P** [Mommy Poppins advertising](https://mommypoppins.com/advertise-in-mommy-poppins-newsletters)
- **The category itself is growing and the buyer trusts programmes, not ads.** US families
  spent an average $1,016 per child on the primary sport in 2024 (+46 % since 2019). **P**
  [Project Play](https://projectplay.org/news/2025/2/24/project-play-survey-family-spending-on-youth-sports-rises-46-over-five-years).
  80 % of parents would choose the brand that sponsors their child's programme between two
  similar ones (YouGov Sport, 2026). **A** [Youth Sports Business Report](https://youthsportsbusinessreport.com/new-youth-sports-parents-poll-five-numbers-that-challenge-the-industry-narrative/)

**Reading.** For a listing platform in 2026 the acquisition stack is, in order: (1) be the
source AI answers and social search cite — structured, reviewed, current listing pages;
(2) short-form video on Instagram/TikTok that leads to those pages; (3) an owned weekly
audience (newsletter/digest) that does not depend on any algorithm; (4) referral loops
between families and programmes; (5) generated pages only where they carry real
differentiators. Paid search is the last lever, not the first.

### 2.2 The supply side (providers / listed businesses): activation is the bottleneck

- Two-thirds of failed marketplaces die on the supply side. **P** [a16z marketplace glossary](https://a16z.com/the-marketplace-glossary/),
  [a16z on supply strategy](https://a16z.com/marketplace-supply-strategy-comprehensive-exclusive-or-curated/)
- The pattern Your Field already follows — scrape the supply that is already online, then
  "claim your listing" with pre-populated photos and descriptions to shorten activation —
  is the documented playbook (Adzuna in recruitment). **A** [Antler](https://www.antler.co/blog/how-to-grow-marketplace-supply-fast),
  [The Marketplace Guide](https://themarketplaceguide.com/patterns/supply-acquisition/)
- Cold-start sequencing: give the harder side (supply) single-player utility first, seed,
  concierge-match, then flip the network; teams that skip single-player utility fail ~4×
  more often. **A** [FORKOFF](https://forkoff.xyz/blog/founder-growth/two-sided-marketplace-cold-start-2026)
  *Our provider view is that single-player utility: conversations, reminders, campaigns work
  the day the provider claims, before the platform has sent it a single family.*
- SMB decision-makers prefer digital self-service (>70 %); SMB sales cycles run one to four
  weeks; healthy SMB activation is 35–50 %; SMB churn is structurally high and "cheap
  self-serve acquisition + fast payback" is the business model — expensive retention
  interventions can destroy value. **A** [ZoomInfo](https://pipeline.zoominfo.com/sales/smb-sales-strategy),
  [PM Toolkit](https://pmtoolkit.ai/benchmarks/activation-rate-benchmarks),
  [ORM](https://orm-tech.com/blog/saas-churn-rate-benchmarks-by-segment)
- Directory referrals convert: niche directories send intent-bearing visitors; profiles at
  85–95 % completeness out-click "100 % stuffed" ones. **A** [Ascendly](https://ascendlymarketing.com/online-business-directories-a-2026-guide-for-smbs/),
  [Jasmine Directory](https://www.jasminedirectory.com/blog/small-business-marketing-2026-directories-beat-ads/)

**Reading.** The provider is won by (1) a claim that costs one click and lands on a page
that already looks finished, (2) a tool that works alone on day one (answer enquiries, text
back missed calls, remind booked families), (3) self-serve upgrades with a price on the
page, and (4) accepting churn rather than fighting it with humans. That is D21's "bundled
base, provider buys reach" — the research supports it.

## 3. Content strategies used by content providers

- **Short-form video is the ROI format.** Marketers name short-form video (49 %), long-form
  video (29 %) and live video (25 %) as the three highest-ROI formats; Instagram is the
  most-cited ROI platform, Facebook 43 %, TikTok 32 %; the top five platforms marketers will
  invest in all carry short-form video. **P** [HubSpot State of Marketing 2026 (statistics page)](https://www.hubspot.com/marketing-statistics),
  [HubSpot social report](https://blog.hubspot.com/marketing/hubspot-blog-social-media-marketing-report)
- **Human-made first; AI for insight and process.** Sprout's 2026 content-strategy study
  (2,300+ consumers, 1,200 marketers) finds consumers want brands to make human-generated
  content the #1 priority and to use AI for audience insight and efficiency, not to replace
  taste. **P** [Sprout Social](https://sproutsocial.com/insights/data/2026-social-media-content-strategy-report/).
  61 % of marketers plan to increase creator-content investment; micro-creators (1K–100K)
  are the top-performing tier for 32 %. **P** [Sprout influencer report](https://sproutsocial.com/insights/data/2026-influencer-marketing-report/),
  [HubSpot](https://blog.hubspot.com/marketing/hubspot-blog-social-media-marketing-report)
- **Small businesses have already moved.** Among 300+ US/Canadian SMBs (Feb 2026): 66 % use
  unpaid social, 56 % social ads; Facebook 90 %, Instagram 74 %, TikTok 22 % (down from
  34 %); 53 % will invest in video in 2026; AI for content creation 81 % (up from 52 %), for
  design 54 %, for social management 35 %; 83 % say referrals are their best acquisition
  source (up from 65 %). **P** [LocaliQ 2026 report](https://localiq.com/blog/small-business-marketing-trends-report-2026/)
- **The "content engine": one source, many cuts.** Creators and publishers produce one
  anchor piece a week and cut it into clips, carousels, posts, a newsletter item and a
  page — short-form for discovery, long-form for search and proof, the newsletter for the
  owned relationship. **A** [Postiv](https://postiv.ai/blog/content-repurposing-strategies),
  [Newzenler](https://www.newzenler.com/blog/content-repurposing-system-creators-2026),
  [OpusClip on 2026 short-form](https://www.opus.pro/blog/short-form-video-trends-reshaping-creator-marketing-2026)
- **Social search optimisation is a content rule, not an SEO afterthought.** Keywords in
  the on-screen text, caption and spoken audio; a location and an activity in every post;
  a series format so the platform learns the account. **A** [Sked Social](https://skedsocial.com/blog/social-search-how-to-optimize-for-discoverability-on-tiktok-and-instagram-2025),
  [ALM](https://almcorp.com/blog/youtube-tiktok-instagram-social-seo-2026/)
- **What the parent audience responds to** (from the platform incumbents' own sell sheets):
  age-bracketed, neighbourhood-specific, "this week" content; the trusted curator voice;
  real people demonstrating real experiences. **P** [Mommy Poppins](https://mommypoppins.com/content/advertise-on-mommy-poppins);
  **A** [The Ad Firm](https://www.theadfirm.net/social-search-is-eating-discovery-what-your-business-needs-before-search-and-social-fully-merge)

**Reading.** The content strategy for business.direct is a weekly *engine*, not a queue of
one-off posts: one anchor per neighbourhood or activity per week (a real session filmed or
photographed by the provider, or a provider spotlight built from the card), cut into a
Reel/Short, a carousel, a story, a digest item and a listing-page update — each carrying
the neighbourhood, the activity and the age in text, caption and voice. Human footage from
the provider first; generated media fills the gaps, labelled.

## 4. How to deliver those contents — which services to add

### 4.1 The landscape in one table (September 2026)

| Layer | Services | What they are for here | Price points read | Notes |
|---|---|---|---|---|
| **Video (generative)** | **Higgsfield** (aggregator over Veo 3.1, Kling 3.0, Sora 2, Wan, Seedance; Cinema Studio, Marketing Studio, UGC Factory, Lipsync Studio, Soul image model, MCP/CLI + API, ChatGPT plugin) **V**; Google **Veo 3.1** (native synced audio); **Kling 3.0**; **Runway Gen-4.5** (reference-image control, character consistency); Pika, Luma, Hailuo, Wan | provider spotlights when no footage exists; b-roll behind a real photo; camera moves on a still | Higgsfield tiers read as Starter $15 / Plus $39 / Ultra $99 monthly (annual billing), ~200 / 1,000 / 3,000 credits, ~50–100 credits per short clip, credits expire monthly **A** ([Layer3 Labs, updated 5 Sep 2026](https://www.layer3labs.io/guides/higgsfield-ai-pricing)); other pages list Plus ~$49 and a Business seat ~$89 **A** ([bleap](https://www.bleap.finance/en-us/blog/what-is-higgsfield-ai)) — **the pricing page itself is JavaScript-rendered and could not be read**, so treat every figure as third-party | **Do not build on Sora**: the Sora app closed 26 Apr 2026 and the Sora 2 API shuts on 24 Sep 2026 **P** ([OpenAI help centre](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation), [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| **Video (avatar / UGC-style)** | **HeyGen** (Avatar IV, 1,100+ avatars, Veo/Kling b-roll), **Synthesia**, **Arcads**, **Creatify**, Oakgen | a "coach explains the trial policy" clip when the coach will not film; ad variants | HeyGen and Synthesia from ~$29/mo; Synthesia ~15–25 % cheaper per finished minute at entry; Creatify free/10 credits, $39/100, $99/300 (quality videos ~20 credits); Arcads $110 list **A** ([Colossyan](https://www.colossyan.com/posts/heygen-vs-synthesia/), [Vidico](https://vidico.com/news/heygen-vs-synthesia/), [Creatify on Arcads](https://creatify.ai/blog/arcads-pricing-%282026%29-plans-credits-and-what-you-ll-actually-pay), [Hyperfx](https://www.hyperfx.ai/blog/arcads-vs-creatify-vs-higgs-field-vs-hyper-2026)) | a synthetic "coach" is a realistic-person deepfake under every platform's rules — label it, or better, do not do it for a children's-activity brand (§4.3) |
| **Video (from real footage)** | **OpusClip** (long → clips, captions, b-roll, scheduling to 6 platforms), **CapCut** (free, 300M MAU), **Descript**, Captions | the real lever: a provider's 30-minute session recording becomes a week of Reels | OpusClip free 60 min/mo, Starter $15/150, Pro $29/300 processing minutes **A** ([eesel](https://www.eesel.ai/blog/opusclip-pricing), [Creatify](https://creatify.ai/blog/opusclip-pricing-plans-and-what-you-ll-actually-pay-in-2026)) | this is where "human-made first" (§3) and cost meet |
| **Image** | **Nano Banana 2 / Pro** (Google, photorealism, editing), **FLUX.2** (photoreal, API from ~3 ¢/image), **Ideogram 4.0** (best text-in-image → social tiles), **GPT Image 1.5 / 2**, **Midjourney v8** (art direction), **Adobe Firefly** (licensed training data, IP indemnification) | digest headers, "this week in Park Slope" tiles, activity × neighbourhood page art, editing a provider's photo (crop, extend, clean) | free to ~€120/mo; FLUX API cents per image **A** ([Provimedia](https://www.provimedia.de/en/blog/ai-image-generation-2026-best-tools), [AI Magicx](https://www.aimagicx.com/blog/midjourney-vs-flux-vs-ideogram-image-comparison-2026), [aicomparison](https://aicomparison.ai/best-ai-image-generators/)) | never generate children; edit the provider's own photos; Firefly where indemnity matters |
| **Audio** | **ElevenLabs** (voice, dubbing; ElevenLabs Music commercially licensed from the $6 Starter), **Suno v5** / **Udio** (full songs; label settlements late 2025), Google **Lyria 3** (Vertex), licensed libraries (Epidemic Sound, Artlist), Murf | voice-over for Reels and the digest's audio version; bed music; the provider's "text back" voice | ElevenLabs from $6/mo **A** ([AI Magicx](https://www.aimagicx.com/blog/suno-vs-udio-vs-elevenlabs-music-comparison-2026), [Internet Pros](https://internet-pros.com/blog/generative-music-ai-suno-udio-2026/)) | choose a service with clear licensing and indemnity for a commercial brand |
| **Design and assembly** | **Canva Magic Studio** (free–$15/mo: brand templates, auto-resize, text-to-image inside the layout), **Adobe Express / Firefly** ($9.99/mo standalone) | the layer a one-person operator actually lives in: brand kit, resize per channel, captions | **A** [SocialPilot](https://www.socialpilot.co/ai-social-media-content-creation-tools), [Upskillist](https://www.upskillist.com/blog/best-ai-graphic-design-tools/) | |
| **Scheduling and inbox** | **Buffer**, **Later**, **Metricool**, **Hootsuite**; all-in-one SMB tools (Brand Brain $29/mo, Enrich Labs $39/mo) | publishing at the slot, comments/DMs inbox, analytics per post | $29–$200/mo **A** [Zapier](https://zapier.com/blog/best-ai-social-media-management/), [aifwd](https://aifwd.net/blog/ai-social-media-management-2026/) | business.direct's outbox + Meta adapter replaces this for the platform; a provider on the free page may still use one |
| **Copy and drafting** | Claude / GPT class models behind an interface (ADR-7) | every draft the machine writes | per-token | already in the architecture |
| **Research and signals** (from the reference videos) | Google Trends, Semrush, SparkToro, Surfer | the market-radar department | subscription | keep as "later" |

### 4.2 What this means for delivery — the pipeline to add

1. **Real media first, generated second.** The provider's own session photo or clip is
   the input (upload from the provider view; the card's image is the fallback). Generation
   fills three gaps only: a *still-to-motion* spotlight when the provider has no video (a
   camera move on its real photo — Higgsfield/Runway class); *tiles and headers* with text
   (Ideogram/Nano Banana class, or Canva); *voice-over* for a Reel or the digest's audio
   (ElevenLabs class). This matches Sprout's "human first" finding and the platform rules.
2. **One "media" department, three adapters behind one interface** — `MediaAdapter.image`,
   `.video`, `.audio` — so the vendor can change (Sora already did). Higgsfield's value is
   exactly that it is an aggregator with an API/MCP over the leading video models; treat it
   as one candidate adapter, not a dependency.
3. **The clip engine is the highest-return service** (OpusClip class): a provider records
   one session, the machine cuts it into the week's Reels with captions and the listing
   link; approval per clip as today's post card.
4. **Labelling in the pipeline, not as a checkbox**: every generated asset carries C2PA
   Content Credentials at creation and the platform-specific disclosure at publish time;
   real footage carries none (§4.3).
5. **Never generate a child.** Edit the provider's real photos; generate places, objects,
   type, motion — not people, and certainly not children. This is a product rule (proposed
   R15), not a legal footnote.

### 4.3 Labelling and law for generated media (state on 2026-09-19)

- EU AI Act **Article 50** applies from **2 August 2026**: AI-generated or manipulated
  content that resembles real people, places or events must be visibly marked when used
  for professional purposes. **A** [Billo](https://billo.app/blog/ai-labeling/),
  [QBS](https://qbsglobal.blog/labeling-ai-generated-content-rules-2026) (the first round's
  §7 cites the regulation itself)
- **TikTok** requires visible labels on realistic AI visuals and audio, detects C2PA
  credentials automatically, and reduces reach ~60 % for 30 days after three unlabelled AI
  videos. **A** [Storrito](https://storrito.com/resources/tiktoks-2026-ai-labeling-rules-and-what-they-signal-for-platform-governance/),
  [Influencer Marketing Hub](https://influencermarketinghub.com/ai-disclosure-rules/)
- **Meta** unified Instagram/Facebook AI disclosure in February 2026: an in-post tag above
  the content, like a paid-partnership label. **A** [Digital Applied](https://www.digitalapplied.com/blog/ai-content-labeling-rules-advertisers-2026-reference)
- **YouTube** has required disclosure of realistic altered or synthetic content since 2025.
  **A** [Influencer Marketing Hub](https://influencermarketinghub.com/ai-disclosure-rules/)
- **C2PA 2.3** (February 2026) is the credential format the platforms read. **A** [Billo](https://billo.app/blog/ai-labeling/)

**Reading.** Four platforms, four label systems, one pipeline rule: mark at creation, disclose
at publish, keep the credential in the audit snapshot (architecture §4, Blob).

## 5. The sales processes — what the market says

### 5.1 Outbound to small businesses (our B2B provider sales)

- **Benchmarks (billions of sends, Jan–Dec 2025):** average reply 3.43 %; top quartile
  5.5 %+; top decile 10.7 %+; **58 % of replies come from step one**; 4–7 touches, 3–4 days
  apart; first e-mail under 80 words with one CTA; bounce < 2 %; warm a domain 4–6 weeks
  from 5–10 sends a day; stable domains see +15–20 % replies. **P** [Instantly benchmark report 2026](https://instantly.ai/cold-email-benchmark-report-2026)
- SMB targets reply 20–40 % more than enterprise; keep SMB sequences to 4–5 touches over
  14–21 days. **A** [Cleverly](https://www.cleverly.co/blog/cold-email-benchmarks-by-industry),
  [Puzzle Inbox](https://puzzleinbox.com/blog/cold-email-reply-rate-benchmarks-2026-by-segment)
- Multi-channel (e-mail + phone + LinkedIn) outperforms single-channel by ~40 % in
  engagement; top teams reach 15–25 % across channels with tight targeting and a signal
  in the first line. **A** [Belkins](https://belkins.io/blog/sales-outreach-strategy),
  [Salesmotion](https://salesmotion.io/blog/cold-outreach-best-practices)
- **Deliverability is the failure mode of AI outbound**: domain-reputation collapse from
  over-sending caps 47 % of AI-SDR deployments in their first 90 days; Microsoft 365
  inboxes filter strictest. **A** [Digital Applied](https://www.digitalapplied.com/blog/ai-sdr-statistics-2026-outbound-sales-data-points)
- **The tool tiers**: data + sequencing (Apollo; Clay for enrichment), e-mail-first volume
  with warm-up (Instantly, Smartlead, lemlist), and "autonomous SDR" workers (11x Alice,
  Artisan, AiSDR). **A** [ZoomInfo](https://pipeline.zoominfo.com/sales/ai-sdr-for-outbound-sales),
  [Cirrus Insight](https://www.cirrusinsight.com/blog/ai-outbound-sales),
  [11x](https://www.11x.ai/guides/ai-sdr-tools-b2b-sales-teams)
- **Voice**: 62 % of inbound SMB calls go unanswered at peak; AI voice agents pay back
  fastest on inbound qualification, after-hours and follow-ups; outbound voice works when
  it verifies the person, asks few questions and stops. **A** [CloudTalk](https://www.cloudtalk.io/blog/best-ai-voice-agents/),
  [B2BNN](https://www.b2bnn.com/2026/09/how-b2b-teams-use-ai-voice-agents-for-outbound-without-burning-lead-lists/),
  [Aloware](https://aloware.com/blog/best-ai-voice-agents-complete-guide-for-smbs)

**Reading against what we have.** Our invitation sequence (1 e-mail + 1 reminder + a call
task) is one touch short of the evidence; the copy's "your programme is already listed —
manage it in one click" *is* the signal-in-the-first-line the benchmarks reward, and 130
addresses is small enough that deliverability is a warm-up problem, not a volume problem.
What is missing: a **sending domain per platform with warm-up and bounce handling**, a
**third touch** (a different angle: "a family saved you this week"), a **phone step** that
is a real call task or a compliant voice agent for the 72 phone-only providers, and
**reply-time SLAs** on the inbox — the same speed-to-lead rule we sell to providers.

### 5.2 Selling the upgrade (self-serve, in-product)

- SMB buyers self-serve (>70 % prefer digital), cycles run days to weeks, and PLG with a
  sales-assist on high-activity accounts is the pattern that fits. **A** [ZoomInfo](https://pipeline.zoominfo.com/sales/smb-sales-strategy),
  [UserMotion](https://usermotion.com/blog/4-plg-funnels-for-smb-and-enterprise-sales)
- Activation is the strongest predictor of conversion (top quartile 65–75 % vs 52 %
  median); the activation moment for a provider is the first answered enquiry or the first
  filled trial — measurable in our conversations screen. **A** [ProductQuant](https://productquant.dev/blog/saas-activation-benchmarks-by-industry-2026/),
  [Flint](https://www.flint.com/articles/b2b-saas-free-trial-conversion-rate-statistics)

**Reading.** The upgrade is sold by the product at the activation moment: "your trial-class
campaign reached 22 families — featured listing puts you first in Park Slope for $49" —
one card, one Stripe checkout (ADR-9), no salesperson. A human touch only for providers
with high activity and no purchase after 30 days.

### 5.3 The provider's own sales process (what business.direct runs for them)

Speed to lead (research I §2), reminders (§3) and the campaign kinds (business logic §4)
are the provider's sales process; the market adds the **missed-call text-back** and
**after-hours voice** as the two highest-ROI automations for an SMB. Both are already in the
provider's conversations department; voice is "later" until consent and Twilio are decided.

## 6. What it means for business.direct — proposed additions (each is a D-number when the owner decides)

| # | Proposal | Where it lands | Why (section) |
|---|---|---|---|
| P1 | **A media department** with one `MediaAdapter` interface and three candidate services (video: Higgsfield-class aggregator or Runway; image: Nano Banana / Ideogram / Firefly; audio: ElevenLabs) — generation only where real media is missing; **never a person, never a child** (R15) | architecture §4/§7, technical design §6, SSOT R15 | §3, §4.2 |
| P2 | **The clip engine**: a provider uploads one session recording; the machine cuts the week's Reels with captions and the listing link; approval per clip | provider view (a *Media* screen), social queue | §3, §4.1 |
| P3 | **Labelling in the pipeline**: C2PA at creation, platform disclosure at publish, credential kept in the audit snapshot | outbox, channel adapters | §4.3 |
| P4 | **Content engine cadence**: one anchor per neighbourhood or activity per week → Reel, carousel, story, digest item, page update; keywords (neighbourhood · activity · age) in text, caption and audio | social department rules file, calendar | §3 |
| P5 | **AI-citation readiness**: listing pages and generated pages carry reviews, schema, "last verified" dates and a plain-language answer block — the properties the cited sources share | generated pages, platform connector | §2.1 |
| P6 | **Owned audience as a channel**: the digest becomes a public neighbourhood newsletter families can join without an account, with cross-recommendation as the growth loop | family view, digest job | §2.1 |
| P7 | **Sending infrastructure**: a dedicated sending domain per platform instance, 4–6-week warm-up, bounce < 2 %, three touches (invitation → "a family saved you" → reminder), then the call task; reply within one business day | sequences, outbox, `rules/consent.md` | §5.1 |
| P8 | **Upgrade at the activation moment**: the product card appears on the first campaign result or the first answered enquiry; sales-assist only after 30 days of activity without a purchase | provider results, drawer | §5.2 |
| P9 | **Voice, later**: missed-call text-back stays; an inbound voice agent for providers and an outbound verification call for phone-only providers wait on Twilio and consent (asks #4/#5) | integrations | §5.1, §5.3 |

None of these changes the approved design system or layouts; P2 adds one provider screen
on the existing grids.

## 7. What was not found or could not be verified

- **Higgsfield's own pricing page** is JavaScript-rendered; `curl` returned only the
  navigation (which did confirm the product set: Marketing Studio, UGC Factory, Lipsync
  Studio, Soul, Cinema Studio, MCP/CLI API, ChatGPT plugin, Veo/Sora/Kling/Wan/Seedance).
  Prices above are third-party readings of September 2026 and disagree with each other by
  tier; confirm on the site before any decision.
- **Sprout's full 2026 report figures** sit behind a download; only its headline findings
  are on the public page and are quoted as such.
- **No "claim your listing" conversion benchmark** for directories was found; the closest
  evidence is SMB activation (35–50 %) and the marketplace playbooks in §2.2.
- **No published data on how NYC parents specifically find activities**; the parent-media
  sell sheets (Mommy Poppins) and youth-sports spending are the nearest primary sources.
- **AIM Group's classifieds reports** are paid; only their scope was readable.
- **Link check** (`curl`, 2026-09-19): every source resolved except six that block scripted
  fetches (403: OpenAI help centre, NP Digital, emailtooltester, Internet Pros, The Ad Firm;
  no response: Business Wire) — each was read through the search tool and is kept because it
  is the primary or the clearest statement; open them in a browser.
