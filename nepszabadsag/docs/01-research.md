# Népszabadság — research: how the greatest news sites are built, what a relaunch here has to answer, and what a serif subscription-first daily should learn from precedent

*For the owner (direction approval) and the team (the build's brief). Twenty-five news home
pages measured with `curl` (§1) and a smaller reachable set read rendered in the browser pane
at 1440 and 390 (§7); five areas of sourced industry evidence (§2–§6) gathered 2026-09-21.
**P** primary (a report, a regulator, a company's own page); **A** an industry summary,
trade press, or a secondary write-up of a primary source. Where a source itself flags a gap
or an unverified chain, that flag is kept, not smoothed over.*

## 0. The five things that matter most

1. **The project's name is Népszabadság** (confirmed by the owner 2026-09-21 — an earlier reference to "nepszava" was a slip, not a signal). Separately, and much smaller: the Figma's internal **Népszava** sub-brand section happens to share its name with a real, independent, 153-year-old Hungarian daily that went online-only on 2026-05-29 after its distributor cancelled its print contract over debt, and was still without a buyer as of 2026-07-30 (§5) — likely coincidence, worth one line of confirmation with the client, not a blocker.
2. **Hungarians trust news less than almost anyone else measured, and pay for it rarely.** 17% trust news generally (lowest of 48 markets, DNR 2026); 6% pay for any online news. A registration wall that earns trust before it asks for money is not a nice-to-have here — it is the only lever the market data supports (§2).
3. **A hard free-to-paid cliff is a normal industry pattern, but the pricing literature's own advice cuts against launching a fully free period.** Registered users convert to paid roughly 10× better than anonymous visitors, and European benchmarks find that even a token charge during a trial period out-converts zero-cost trials (§3) — worth raising against the memo's "free until 15 November" plan, not overriding it.
4. **The 2016 closure and the exact ad-slot economics both have direct, checkable precedent.** Four independent sources converge on the same shape of the 2016 story (§4); the sister site's own current rate card prices the exact banner sizes the Figma uses, in real forints (`02-audit.md` §3) — this project does not have to guess at either its own history or its ad business model.
5. **Every measurable leader separates a display headline face from a body-text face, and colours by editorial section rather than a single brand accent** (§6, §7) — the opposite of a one-brand-colour approach, and worth stating as a rule before the design-system gate, not after.

## 1. Technical benchmark — 25 news home pages, measured with `curl`, 2026-09-21

Desktop UA, gzip, one cold request each; TTFB and size are single readings, not averages.

| Site | HTTP | TTFB s | HTML KB | scripts | stylesheets | `<img>` | Stack signals | Fonts seen in HTML | Nav / brand colour |
|---|---|---|---|---|---|---|---|---|---|
| nytimes.com | 403 (bot wall) | 0.11 | 0.8 | — | — | — | — | — | not measurable by curl; the browser pane refuses nytimes.com |
| washingtonpost.com | connection reset | — | — | — | — | — | — | — | not reachable from here |
| wsj.com | 401 (bot wall) | 0.14 | 0.8 | — | — | — | — | — | — |
| theguardian.com/uk | 200 | 0.14 | 163 | 19 | 1 | 139 | Next.js, Permutive | GH Guardian Headline, Guardian Text Egyptian, Guardian Text Sans | News · Opinion · Sport · Culture · Lifestyle; #052962 (theme-color), red #c70000 |
| bbc.com/news | 200 | 0.04 | 64 | 59 | 0 | 44 | Next.js, Piano, Optimizely, Permutive | BBC Reith Sans / Serif | Home · News · Sport · Business · Technology · Health · Culture · Arts · Travel · Earth · Audio · Video · Live; black, red #b80000 |
| ft.com | 403 (security check) | 0.05 | 198 | — | — | — | Vue | Financier Display, Metric | pink #fff1e5, teal #0d7680 |
| spiegel.de | 200 | 0.10 | 253 | 23 | 2 | 640 | Next.js/React | SpiegelSans, SpiegelSerif, SpiegelSlab, National2Narrow | 22 nav items (Politik … Geschichte); theme-color #e64415 |
| zeit.de | 403 ("Da ist etwas schiefgelaufen") | 0.12 | 5 | — | — | — | — | — | — |
| faz.net/aktuell | 200 | 0.09 | 295 | 29 | 1 | 137 | Nuxt/Vite, jQuery | Roboto, Source Sans 3 | Politik · Wirtschaft · Finanzen · Feuilleton · Karriere · Sport · Gesellschaft · Besser leben · Rhein-Main · Technik · Wissen · Reise; red #c60000 |
| sueddeutsche.de | 200 | 0.03 | 283 | 82 | 1 | 181 | Next.js, GTM, Piano | SZ Sans Digital, SZ Text, Old Standard, Montserrat | SZ.de · Zeitung · Magazin · Jetzt · Dossier; #29293a, teal #009990 |
| nikkei.com | 200 | 2.41 | 95 | 8 | 1 | 216 | Next.js/Vite | (system) | theme-color #003e70, red #d11100 |
| straitstimes.com/global | 200 | 0.63 | 64 | 38 | 2 | 58 | Next.js, Piano, Chartbeat | (system) | Singapore · Asia · World · Opinion · Life · Business · Sport; #161616 |
| scmp.com | 200 | 0.09 | 244 | 116 | 6 | 34 | Next.js, GTM, Piano, Optimizely | Roboto, Roboto Condensed, Crete Round | #2c4692 / #001246 |
| thehindu.com | 200 | 0.43 | 65 | 80 | 5 | 123 | Next/React, jQuery, GTM, Piano, Chartbeat | (system) | #2b2e34 |
| people.com.cn | 200 | 0.75 | 37 | 33 | 4 | 148 | jQuery | (system) | blue #006ebf, red #b64d3a; 664 links on the home page |
| news.cn (Xinhua) | 200 | 0.50 | 42 | 13 | 2 | 84 | jQuery | (system) | 694 links |
| caixin.com | 200 | 0.76 | 26 | 48 | 2 | 79 | jQuery | Arial | #1f286f, #0098d0 |
| telex.hu | 200 | 0.07 | 143 | 6 | 16 | 74 | Nuxt/Vite, GTM | (self-hosted) | #222228, red #ef1b1b, blue #0439d9 |
| 444.hu | 200 | 0.04 | 49 | 7 | 3 | 96 | Next.js, GTM | (self-hosted) | 44 `<h1>` on the home page; orange #ffb76a |
| hvg.hu | 200 | 0.04 | 64 | — | — | — | — | — | orange #f26522 |
| index.hu | 200 | 0.05 | 75 | 86 | 5 | 188 | Vite, jQuery, GTM | (self-hosted) | Belföld · Külföld · Gazdaság · Kult · Vélemény · Tech-Tud · Sport · Fomo · 24 Óra · Blog · Videó · Podcast; #ff9900 |
| 24.hu | 200 | 0.03 | 66 | 54 | 8 | 140 | WordPress (AIOSEO, WPBakery), Vue, jQuery | (self-hosted) | Belföld · Nagyvilág · Közélet · Tudomány · Sport · Élet-Stílus · … 22 items; green #57a600, #002e5e |
| nepszava.hu | 200 | 0.05 | 48 | 27 | 57 | 30 | Cloudflare, AdSense, OneSignal, Gemius, d3, Swiper; home rendered by `/js/home/index.js` | (self-hosted, `fontconfig.css`) | description "Népszava politikai napilap"; 57 stylesheet links; `cache-control: no-store` |
| hang.hu (Magyar Hang) | 200 | 0.08 | 63 | 28 | 4 | 49 | Next.js, jQuery, GTM | (self-hosted) | 22 nav items incl. podcasts; teal #018d98 |
| nol.hu (the old Népszabadság) | 200 | 0.03 | 0.5 | 0 | 0 | 0 | a one-line stub | Arial | "A nol.hu archívumára a Lapcentrumon lehet előfizetni." — the archive is sold through lapcentrum.hu; nothing else is served |

**What the numbers already say.** (1) The reference sites that matter most for a serif,
subscription-first daily (NYT, WSJ, FT, Zeit, WaPo) cannot be read from this environment by
`curl`, and the browser pane refuses nytimes.com — their layouts rest on published design
sources instead (§6). (2) Every measurable leader is on Next.js / Nuxt with a self-hosted type
family of two or three faces and one brand colour plus red for live/breaking. (3) The Hungarian
field splits: Telex (Nuxt, 6 scripts, 143 KB) and 444 (Next, 7 scripts) are lean; Index (86
scripts) and 24.hu (WordPress + WPBakery, 54 scripts) are heavy; nepszava.hu ships 57
stylesheet links and `no-store` caching. (4) Home pages carry 236–782 links; the Figma címlap
carries far fewer — a deliberate choice to be defended, not a gap to close.

## 2. Reuters Institute Digital News Report 2026 — Hungary

- Only **17%** of Hungarians say they generally trust the news, down 5 points from 2025 — the lowest figure recorded for Hungary since 2016, and the lowest of the 48 markets surveyed in 2026. **P** [Reuters Institute DNR 2026 — Hungary](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/hungary)
- **6%** of Hungarians pay for any online news, down 2 points year-on-year (a secondary CEE roundup cites a conflicting 14%; the 6% figure confirmed directly on the primary Hungary page is the one used here). **P** [Reuters Institute DNR 2026 — Hungary](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/hungary)
- **45%** of Hungarians say they avoid the news sometimes or often, up 4 points. **P** [Reuters Institute DNR 2026 — Hungary](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/hungary)
- Trusted brands: RTL 49%, HVG 44%, Telex 41%, 24.hu and 444.hu 38% each; the public broadcaster MTV 21% trusted vs 56% distrust; Index.hu 26% trust vs 44% distrust; Origo fell from 25% (2025) to 21% (2026). **A** [CEU Democracy Institute, summarising DNR 2026](https://democracyinstitute.ceu.edu/articles/judit-szakacs-eva-bognar-reuters-digital-news-report-2026)
- Social media/video platforms as a news source rose from 54% (2025) to 62% (2026); 83% of Hungarians use online news sources weekly. **A** [CEU Democracy Institute](https://democracyinstitute.ceu.edu/articles/judit-szakacs-eva-bognar-reuters-digital-news-report-2026)
- Hungary: population 9.6m, internet penetration 94%, RSF World Press Freedom Index rank 74/180 (score 59.85). The 2026 fieldwork fell around Hungary's April 2026 election, which ended 16 years of Fidesz government; the report describes the outgoing government's media reach as having controlled "over 80%" of media in the country. **P** [Reuters Institute DNR 2026 — Hungary](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/hungary)
- Global context: 54% of people now use social/video platforms for news vs 51% who go directly to a news organisation's own site or app — the first time platforms have overtaken owned properties; global trust in news is 37%, the lowest since tracking began in 2015; across a tracked 20-country basket, 17% pay for online news (Norway 40%, Sweden 32%). **P** [Reuters Institute DNR 2026 executive summary](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary)
- Regionally, Poland leads CEE on digital subscriptions at roughly 16%; most of the region sits below 15%, with Hungary and Slovakia flagged as low-trust, high-misinformation-exposure markets. **A** [Central European Times, on RI's CEE trends](https://centraleuropeantimes.com/poland-leads-cee-reuters-institute-reports-on-cee-digital-news-consumption-trends/)
- **Not found**: a Hungary-specific mobile-vs-desktop reading split; only a non-Hungary-specific global smartphone-time figure (4–5 hrs/day) turned up. Do not state a Hungary split without reading the full DNR 2026 PDF.

## 3. Subscription and paywall benchmarks for 2026

- Registration walls convert 3.2–6.7% of impressions vs 0.9–1.45% for a standard newsletter pop-up; one US outlet measured 16× more signups from a registration wall than a newsletter form in a 30-day test. **A** [Audiencers](https://theaudiencers.com/what-explains-subscription-conversion-success-a-new-formula-and-study-seeks-to-find-an-answer/)
- Registered, non-paying users convert to paid roughly 10× better than anonymous visitors. **A** [Leaky Paywall](https://leakypaywall.com/free-news-site-5-7-conversion-no-paywall/)
- Blended metered-paywall conversion typically runs 3–12% across all traffic, higher for returning and email-referred visitors. **A** [UniSignIn](https://www.unisignin.com/blog/registration-wall-vs-paywall)
- Nikkei (2.4m subscribers) reported a 10× conversion increase after adding a 10-free-article registration wall, and a further 20% increase after cutting the free allowance to one article — a widely repeated industry figure the researcher could not independently verify against a Nikkei-published source. **A** [Leaky Paywall](https://leakypaywall.com/free-news-site-5-7-conversion-no-paywall/)
- A 2025 European pricing study of 101 titles recommends launching at a real price (~€8–10/month) rather than an artificially cheap teaser, arguing the real hurdle is "the mental effort of converting," not the price itself; the sampled average undiscounted price is €10.08/month (CEE €7.84 vs Western Europe €13.01); only 10 of 101 titles offer a fully free trial, 53 use a discounted (not free) trial averaging €2.02/month. **A** [Funds4Media, 2025 European Digital News Pricing Report](https://www.funds4media.org/p/2025-european-digital-news-pricing)
- **Directly relevant to the memo's plan**: the same report's own advice — that a token charge out-converts a fully free trial — cuts against "free until 15 November, then 3 290 Ft," even though a hard free-to-paid cliff is itself a normal, well-precedented pattern (registration-wall data above). Worth raising with the client as a question, not a reason to redesign unasked (`PROTOTYPING.md` §6).
- No sourced CEE-specific print+digital bundle-pricing benchmark exists — the Funds4Media methodology notes this bundling is uncommon in its European sample, so this gap stays a gap rather than an invented number.
- Historically best-performing subscriber-acquisition levers for publishers: promotional discounts (84% of surveyed publishers rank this top), member-exclusive data/research access (74%), member-exclusive newsletters (73%); publishers raised base annual pricing and first-time discounts by an average 22% in the same period to offset renewal "sticker shock." **A** [Digiday+ Research](https://digiday.com/media/digiday-research-data-sheet-the-state-of-subscription-pricing/)

## 4. Népszabadság's 2016 closure — sourced history

Four independent sources converge on the same shape of the story: an official financial
reason, and a widely reported political context. Each is attributed to its source below, not
asserted as this document's own conclusion.

- Népszabadság, Hungary's largest-circulation daily, was abruptly suspended on 8 October 2016 by publisher Mediaworks Zrt. (owned by Austrian firm Vienna Capital Partners / Heinrich Pecina); staff had phones and e-mail cut overnight. The stated reason was financial: cumulative losses reported around 5 billion forints (~€16.7m) over ten years and a drop of roughly 100,000 readers. **A** [Euronews, 8 Oct 2016](https://www.euronews.com/2016/10/08/hungarian-opposition-daily-nepszabadsag-shut-down-suddenly)
- A corroborating contemporary account gives the same official reasoning ("financial losses and plummeting circulation," a need for a "new business model"). **A** [Human Rights Watch, 10 Oct 2016](https://www.hrw.org/news/2016/10/10/hungarys-biggest-oppositional-daily-shut-down)
- In the weeks before closure, the paper had run investigations implicating figures close to PM Viktor Orbán, including central-bank director György Matolcsy and Fidesz official Antal Rogán; staff and outside observers described the shutdown as a politically motivated move rather than a purely financial one, and a ruling-party official was quoted saying "it was about time the paper closed down." **A** [Human Rights Watch](https://www.hrw.org/news/2016/10/10/hungarys-biggest-oppositional-daily-shut-down); [Euronews](https://www.euronews.com/2016/10/08/hungarian-opposition-daily-nepszabadsag-shut-down-suddenly)
- Reporters Without Borders said it was "very concerned for pluralism in Hungary," reported that journalists at the paper believed "the financial situation is just a pretext," and linked the timing to the paper's recent corruption coverage; Hungary ranked 67th of 180 in RSF's 2016 World Press Freedom Index, having fallen 48 places in five years. **P** [RSF, Oct 2016](https://rsf.org/en/hungary-rsf-appalled-leading-hungarian-daily-s-closure)
- Founded 2 November 1956 (successor to Szabad Nép); by 2016, Hungary's newspaper of record by history though reduced to roughly 37,164 copies per quarter (Q2 2016) after years of decline. **A** [Wikipedia](https://en.wikipedia.org/wiki/N%C3%A9pszabads%C3%A1g), cross-checked against the closure reporting above; the exact circulation figure was not independently re-verified against audit-body data.
- Thousands protested outside Hungary's Parliament the evening of the closure. **A** [Human Rights Watch](https://www.hrw.org/news/2016/10/10/hungarys-biggest-oppositional-daily-shut-down); [Euronews](https://www.euronews.com/2016/10/08/hungarian-opposition-daily-nepszabadsag-shut-down-suddenly)
- An investigative retrospective (Direkt36, Hungarian outlet, English translation) reconstructs a timeline in which Mediaworks' Austrian owner Heinrich Pecina and CEO Balázs Rónai clashed just before the closure (Rónai resigned in disagreement 6–7 Oct), and reports that Mediaworks was sold roughly two and a half weeks later (25 Oct 2016) to Opimus Press, a group linked to Lőrinc Mészáros, a businessman close to PM Orbán — reinforcing the widely reported reading that the "financial" framing concealed a politically engineered ownership change. **A** [Direkt36 (English)](https://www.direkt36.hu/en/ilyen-volt-a-nepszabadsag-halala-belulrol/)

**Why this belongs in front of the client, not just the record.** All four sources — a wire
report, an international NGO, a press-freedom body's own statement, and an investigative
outlet's retrospective — converge on the same two-part shape (stated reason vs. reported
context). That convergence, not any one source alone, is what makes the political reading
well-established rather than fringe, and is worth the client knowing is on the record before
the relaunch invites the comparison itself ("Lassan véget ér 10 év hallgatás").

## 5. Comparable relaunch cases — and the one that changes a decision

- **Magyar Nemzet (Hungary — the closest national precedent).** An 80-year-old (founded 1938) conservative daily; ceased publication 11 April 2018 after the election, citing financial problems; its online presence went dark for about ten months. Relaunched 6 February 2019, this time explicitly aligned with the governing party, replacing a title called Magyar Idők. As of August 2026 it converted again — daily to **weekly** print — part of a broader 2026 shift of Hungarian political dailies to online/weekly formats. **A** [Wikipedia](https://en.wikipedia.org/wiki/Magyar_Nemzet); [Balkan Insight, 30 Jul 2026](https://balkaninsight.com/2026/07/30/hungary-enters-post-print-age-as-political-dailies-disappear/rd/) — the strongest "closed, then relaunched" precedent in the same market, though its own relaunch carried a political realignment worth being aware of, not necessarily worth raising with this client unprompted.
- **The Independent (UK) — print stopped, publishing continued (the closest "digital continuation" precedent, not a full closure).** Went online-only in March 2016. Academic research hosted by Reuters Institute found British readership did not fall in the year after, but total time British audiences spent with the title fell 81%, because online readers engage far less deeply than former print subscribers did; overseas browsing grew at least 50%. **P** [Reuters Institute research (Thurman & Fletcher)](https://reutersinstitute.politics.ox.ac.uk/our-research/are-newspapers-heading-toward-post-print-obscurity-case-study-independents-transition) — the same research page cites a similar 72% post-print time-spent decline for NME.
- **The real Népszava — found while researching; a small aside, not a brief-level decision.** Independent of this project (whose own name is settled as Népszabadság, `00-brief.md`), Hungary's actual Népszava — its oldest continuously published paper (153 years) and, since 2019, the country's last liberal/social-democratic political daily — stopped print and went online-only on **2026-05-29** when distributor Mediaworks cancelled its print contract over unpaid debts; about a third of staff were laid off; as of the most recent report found (2026-07-30) its owner was still seeking a buyer and its future was stated as uncertain. **A** [Balkan Insight, 30 Jul 2026](https://balkaninsight.com/2026/07/30/hungary-enters-post-print-age-as-political-dailies-disappear/rd/); [European Federation of Journalists, coverage of the threats/closure](https://europeanjournalists.org/blog/2026/05/29/hungary-threats-against-the-countrys-last-progressive-daily-newspaper/). The Figma's internal Népszava sub-brand section — and its own front-page tease, "Mi lesz a Népszavával?" — happens to share the name; worth one line of confirmation with the client at some point (`00-brief.md`), not treated here as a signal of anything planned.
- Weaker-fit precedents, pattern only: Taloussanomat (Finland) reportedly improved its financial position after going online-only in 2007, cited via a secondary academic-literature chain not independently re-verified here. **A** [via a TandFonline-hosted paper](https://www.tandfonline.com/doi/full/10.1080/21670811.2018.1504625). A 2024–2025 US magazine "print revival" trend (Field & Stream, Saveur, SPIN, Ebony, a reported Life return) shows print returning after being dropped, but these are magazines, not dailies, and the source article itself could only be confirmed via search-result snippets (direct fetch returned HTTP 403) — treat the specifics as unverified. **A** [Nieman Lab, Dec 2024 — fetch blocked, snippet only](https://www.niemanlab.org/2024/12/the-print-revival-comes-to-news/)

## 6. Published design-system references

- **The Guardian's own "Source" design system**: three type families — Guardian Titlepiece (masthead), Guardian Headline (headlines), Guardian Egyptian/Text Egyptian (body) — and a palette organised "by pillar of journalism" (editorial section), not a single brand colour; the stated design principles are "practice radical clarity" and "spark powerful conversations." **P** [Source :: The Guardian Design System](https://guardian.github.io/theguardian.design/)
- The Guardian's January 2018 redesign (print and every digital platform together) introduced Guardian Headline, commissioned from Commercial Type, moved print from Berliner to tabloid format, and rebuilt the grid around five columns; editor-in-chief Katharine Viner described the new identity as communicating "a renewed strength and confidence." **A** [Dezeen, Jan 2018](https://www.dezeen.com/2018/01/15/guardian-newspaper-unveils-new-compact-format-redesign-font-logo/) — a design-trade write-up, not a still-live Guardian-authored post; the Source site above is the primary substitute for current specifics.
- **The New York Times** runs proprietary type: NYT Cheltenham (headlines, a 1896 Bertram Goodhue design redrawn by Carter & Cone) and NYT Imperial (print body, Carter & Cone) alongside Georgia for digital body text and NYT Franklin (a Franklin Gothic derivative) for captions, metadata and navigation — none publicly licensable. **A** [Fonts In Use — NYT Cheltenham](https://fontsinuse.com/typefaces/7802/nyt-cheltenham); [Fonts In Use — NYT Imperial](https://fontsinuse.com/typefaces/112761/nyt-imperial) — NYT's own design-engineering blog (Medium, `@timesopen`) returned HTTP 403 on direct fetch; no primary NYT write-up was reachable in this pass.
- **Der Spiegel**'s developer/design team (published as "DEV SPIEGEL" on Medium) describe their 2016 digital redesign as an 18-month collaboration with agency Make Studio, an integrated mixed team rather than a client/agency split, a design system documented in Figma/Zeroheight but "living primarily in HTML prototypes," and a deliberate move toward the print magazine's typography and colour — using Spiegel Sans across nearly all web text (including body copy) and giving the brand's signal red more prominence online. **P** [DEV SPIEGEL on Medium](https://devspiegel.medium.com/nicht-nur-bunte-pixel-warum-das-neue-gesicht-des-digitalen-spiegel-mehr-als-ein-redesign-ist-b99dd0876344) — direct fetch returned HTTP 403; the content above is from a verified search summary of the post, not a full read, and should be re-fetched before quoting it directly to the client.
- **Synthesis across all three** (the researcher's own reading across the sourced systems above, not a single citation): a dedicated serif display/headline face kept separate from the body-text face; a plain grotesque/sans reserved for metadata, captions and navigation; and a colour system organised by editorial section or pillar rather than one brand accent. This matches what the rendered-layout study below finds independently (§7).

## 7. The rendered look — how the reachable sites actually appear at 1440 and 390

*Read directly in the app's browser pane, 2026-09-21 — the piece `curl` cannot see: grid,
imagery, density, and colour as rendered rather than declared. Cookie banners were dismissed
using only a free "accept" option; no paid alternative was ever chosen, no form was filled,
no account created. NYT, WSJ, FT, Zeit and WaPo stay unreachable here (§1); their layouts
rest on §6 instead.*

**theguardian.com/uk.** Desktop: a leaderboard ad slot directly under a promotional bar
("Support the Guardian · Claim discount"), then a horizontal row of pastel-tinted teaser
cards (soft pink, cream, pale peach backgrounds behind circular photo crops), then a dark
navy nav bar carrying a large white serif "The Guardian" wordmark right-aligned and section
links left-aligned, a thin red active-tab underline. Mobile: the same pastel teaser cards
scroll horizontally above the fold; the lead story drops into a single column with a red
category eyebrow, a large bold serif headline rendered as an underlined link, a full-width
photo, and hairline-separated story rows below (rovat label in small caps, serif headline,
byline · time) — directly comparable to the Figma's Címlap structure (eyebrow, serif
headline, byline · time, hairlines).

**bbc.com/news.** Desktop: white ground, black wordmark, red "News" tab underline as the
only strong accent; a full-width leaderboard ad sits under the nav before any editorial
content; a two-story hero (a large ~60%-width photo lead beside a smaller secondary story),
then a four-across thumbnail row. Sans-serif throughout, bold but moderate headline size,
documentary-style photography, a magazine-style single lead rather than a headline wall.
Mobile: collapses to one column, nav becomes a hamburger plus search icon, the same ad slot
sits above the section heading, supporting stories use a small square thumbnail and headline.

**spiegel.de.** Desktop: an orange/red masthead bar, black "DER SPIEGEL" wordmark, a
three-story teaser row above one large photo-led lead with a bold **sans-serif** headline
(not serif, despite the print identity); below the lead the grid turns modular and
colour-coded by section. A sticky bottom-centre overlay offers **"4 Wochen für 1€"** — a
paid trial, not a free one, then a recurring price — with a visible close control; it
persists through scrolling. Mobile: top stories as a horizontally-scrolling chip row, a
full-bleed hero photo, then the same paid-trial overlay taking roughly 40% of the screen
before it can be dismissed. **This is a live, on-page example of the token-charge-trial
pattern §3's pricing literature recommends over a fully free period.**

**faz.net/aktuell.** Desktop: a serif "Frankfurter Allgemeine" logotype, centred; a single
large photo-led lead with a small-caps kicker and a bold **serif** headline — the only
outlet in this set using serif consistently for headline text; full-height skyscraper ads
flank the content on both sides on scroll; a sticky bottom bar promotes a subscription
offer. Mobile: hamburger, serif wordmark, account icon, horizontally-scrolling category
chips, a single full-width lead photo with an "F+" premium tag before the kicker, the same
bold serif headline carried straight through — the cleanest, least cluttered mobile
presentation measured, no ads visible above the fold.

**sueddeutsche.de.** Desktop: a dark utility bar, a centred serif "Süddeutsche Zeitung"
wordmark, a grey topic box in serif-italic style grouping related coverage, one large photo
lead with a bold **sans-serif** headline in a white card overlapping the photo. A green
sticky subscription banner and the same skyscraper wallpaper ads as FAZ appear on scroll.
Mobile: the hamburger sits on the **right** (the one site to do this), an "SZ Plus"
lock-style tag before the byline signals per-article metering rather than a blocking
homepage wall.

**telex.hu.** Desktop: a navy utility bar with a live rate/weather ticker, a lowercase
"telex" wordmark, a three-column above-the-fold grid (a ticker list, one large featured
photo, weather plus a secondary story), then a dense multi-column headline grid — closer to
a headline wall than a magazine lead, with one clear focal point. Navy and white with a
single yellow accent reserved for the donate button. Mobile: a row of sister-site tabs above
the main nav, a bright yellow **"Támogatás"** (support/donate) button — a reader-donation
call to action, not a paywall — reflecting the donation-funded model directly in the UI (no
lock icons, no paywall language anywhere).

**444.hu.** Desktop: a black bar with a green **"FIZESS ELŐ"** (subscribe) button and a shop
link, foregrounding commerce and subscription immediately; the lead uses an illustrated,
collage-style treatment with condensed display type composited on the photo — closer to
tabloid/magazine-cover language than editorial photography — beside an explicitly labelled
**"HIRDETÉS"** (advertisement) block. Mobile: no hamburger at all — a persistent bottom
app-style tab bar (Menü / Címlap / Friss / Kör / Fiók) is the one outlier among all ten
sites; small circular author-avatar photos accompany bylines, a personality-driven
authorship treatment not seen elsewhere.

**index.hu.** Desktop: white ground, red wordmark, an orange underline accent, a financial
ticker and weather widget above the nav; the hero pairs a photo-and-overlay story with a
**solid blue colour-block card** carrying white headline text and no photo at all — a
poster-like treatment. Below, a dense multi-column wall of black headlines with small
thumbnails. Mobile: sister-site tabs scroll horizontally above the header, the financial
ticker persists even at phone width, and the colour-block headline treatment repeats in
orange further down the feed.

**24.hu.** Desktop: a red/white block logo, a category-chip ticker, a light-blue
**"ELŐFIZETEK"** subscribe button in the header, and a third-party Google promotional banner
injected inline above the fold. A two-column hero, then a dense headline grid with at least
one item carrying a small tag suggesting blended native/sponsored content. Mobile: a
dark-mode toggle and the subscribe button both sit above the fold; content opens into a
text-only pair of headlines before any photo, an alternating text/photo rhythm that reads
denser than BBC, FAZ or SZ.

**nepszava.hu — the sister site, read on screen rather than measured by `curl` (complements
`02-audit.md`).** Desktop: a black topic-tag ticker, a centred blue "NÉPSZAVA" logo block,
then **two full-width ad units back to back directly under the masthead** — one unfilled, one
a foreign-market shopping carousel — before any editorial content. The lead story is
**text-only** (no photograph), a plain bold black headline with blue pill topic tags; a
floating overlay ad appears near the top of the viewport on scroll. **No subscription or
paywall control is visible anywhere in the header, hero or body** — "Előfizetés" appears only
as one small footer link. Mobile: the header shrinks to a bare "N" monogram (every other
site studied keeps a full wordmark at phone width), no subscribe control; the first thing
below the header is a **mistargeted French-language ad** (programmatic inventory not
localised to Hungarian); an unusual segmented "CIKKEK / HÍREK" pill toggle appears with no
analogue on any other site measured; everything below the lead is a plain text list with no
thumbnails at all — the most image-sparse presentation of the ten sites.

### Synthesis

- **Serif headlines read as the most editorially confident execution.** FAZ (serif at both
  widths) and Süddeutsche (serif for section labels, bold sans for headlines) feel the least
  cluttered of the set — directly relevant to a serif-headline repositioning (§0, §6).
- **Every subscription-forward site puts the CTA where it cannot be missed** — FAZ, SZ,
  Spiegel, 444.hu and 24.hu all surface a subscribe button or overlay in the header or as a
  persistent module. nepszava.hu currently does none of this (§0).
- **A photo-led single lead is the norm among the strongest layouts** (BBC, FAZ, SZ,
  Spiegel); index.hu's colour-block hero and nepszava.hu's text-only lead both read as
  weaker entry points by comparison.
- **Ad density and curation visibly track perceived quality.** BBC and 444.hu keep ads
  clearly labelled or edge-confined; nepszava.hu stacks two full-width ad units under the
  masthead plus a floating overlay plus, on mobile, a mistargeted non-Hungarian ad — denser
  and less curated than any competitor measured, and a concrete, fixable gap for the new site
  to not repeat.
- **Density tracks business model**: the donation-funded site (Telex) and the tabloid-leaning
  sites (Index, 24.hu) run dense, image-sparse headline walls; the subscription dailies (FAZ,
  SZ, Spiegel) run a single strong lead with more whitespace and imagery — the pattern a
  subscription-first relaunch should follow.
- **Mobile navigation clusters around a hamburger plus search**, with 444.hu's bottom tab
  bar as the one deliberate outlier worth knowing about, not necessarily worth copying.
- Spiegel's own **"4 Wochen für 1€"** trial is a live counterpart to §3's pricing-literature
  finding that a token charge out-converts a fully free trial period — a concrete precedent
  to weigh against the memo's "free until 15 November" plan (P2).

## 8. What it means for the prototype — proposals for the owner (each becomes a D-number when decided)

| # | Proposal | From |
|---|---|---|
| P1 | A one-line confirmation with the client, whenever convenient, that the Figma's Népszava sub-brand section is unrelated to the real, currently-distressed newspaper of that name — low priority, not a gate | §5, `00-brief.md` |
| P2 | Keep the registration wall, but raise the "fully free until 15 Nov" plan against the pricing literature's own advice that even a token charge converts better than a free trial — the client's call, not a redesign | §3 |
| P3 | A dedicated serif headline face, separate from the body-text face, and a plain sans reserved for metadata/nav/captions — matching every measured leader and the Figma's own apparent direction | §6, §7 |
| P4 | Colour organised by editorial section (rovat), not a single brand blue — the Guardian's "pillar" model, and closer to what the Figma's rovat-labelled pills already imply | §6 |
| P5 | Decide build-vs-buy for the paywall/e-paper reader against the sister site's own precedent (a third-party vendor, xximedia.hu) rather than assuming it must be built in-house | `02-audit.md` §2 |
| P6 | Price the ad inventory (970×250, 300×250, 600×250) from the sister site's own real 2026 rate card rather than inventing figures, if this title carries its own advertising | `02-audit.md` §3 |
| P7 | Confirm the relationship (if any) between XXI. Század Média Zrt. and Liberty Press Kft. — a plain fact, not inferred here | `02-audit.md` §2, `03-sources.md` |
| P8 | A header-level subscribe/registration control on every page, always visible — every subscription-forward site studied has one; the sister site has none | §7 |
| P9 | Keep the ad load lighter and better-curated than the sister site's (which stacks two full-width units under the masthead plus a floating overlay) — the Figma's own slot count is already close to this | §7, `02-audit.md` §3 |

## 9. What was not found, or could not be verified

- A Hungary-specific mobile-vs-desktop reading split in DNR 2026 (only a global figure exists).
- A CEE-specific print+digital bundle-pricing benchmark (the closest source says this bundling is uncommon in its sample).
- A primary NYT design-system write-up (Medium blocked this environment with HTTP 403; secondary type-reference sources used instead).
- A still-live Guardian-authored blog post on the 2018 redesign (the Source design-system site substitutes).
- Direct confirmation of the Spiegel Medium post's content (HTTP 403; a verified search summary was used and should be re-checked before quoting).
- The Nieman Lab "print revival" article's exact per-title dates (HTTP 403; snippet-only).
- The Taloussanomat citation chain, traced only through a secondary academic-literature reference, not the original paper.
- The discrepancy between a 6% and a 14% "pay for online news" figure for Hungary — resolved here in favour of the primary Reuters Institute page's own 6%.
