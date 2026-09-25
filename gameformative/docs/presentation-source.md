# gameformative.com

## Where it stands {#situation}

<p class="lead-p">gameformative.com was registered on 25 September 2026. Its DNS points at Vercel, and the domain serves a 404: there is no site, brand, audience or content yet.</p>

The market it enters is measured:

- **Football is the world's sport.** 51% of people globally call themselves fans (Nielsen, 2025).
- **The leaders put scores before stories.** Every top sports site we measured in Germany, India and China opens with live scores or latest results.
- **The stats sites own the numbers.** Opta Analyst reaches about a million readers a month on data-led writing (Stats Perform). FotMob gets 72.9% of its traffic direct (Similarweb, August 2026).

## The complication {#complication}

- **Readers find news in feeds first.** Social and video networks (54%) now beat publishers' own sites and apps (51%) as a way into news (Reuters Institute, 2026).
- **Trust is low, and automation is under scrutiny.** Trust in news is 37% (Reuters Institute, 2026). Only 12% of people are comfortable with news made entirely by AI (Reuters Institute, 2025). Since 2 August 2026, the EU AI Act requires AI-generated news text to be disclosed unless an editor is responsible for it.
- **The data fans expect is licensed.** xG, shots and player ratings come from licensed providers, and their prices are not public. Using the wrong free source is a legal risk: StatsBomb's and NBA.com's terms forbid commercial use.

A new site has to be worth a direct visit, visibly sourced and human-edited, and legal about its data from the first page.

## The question {#question}

Can gameformative launch as a credible football analytics and news site on data it may legally use today? And what does it need to become a daily habit?

## The answer {#answer}

**Yes. The prototype shows how.** It runs on real, public-domain data (openfootball, CC0) and covers:

- {{leagues}} leagues with {{league_matches}} results and {{league_goals}} goals to {{data_to}};
- the complete 2025/26 Premier League: {{pl_matches}} matches and {{pl_goals}} goals;
- all {{wc_matches}} matches and {{wc_goals}} goals of the 2026 World Cup.

Every figure on every page is computed from {{inputs}} source files by a converter that refuses to publish a table that does not add up.

What it gives each party:

- **For readers:**
  - scores first on every page;
  - tables that work on a phone;
  - charts that read in black and white;
  - a page that says what every number means and where it comes from.
- **For the editors:**
  - copy that cannot silently go out of date, because the build stops if a data refresh makes a sentence untrue;
  - automated round-ups that are labelled as such;
  - a corrections and AI policy already written.
- **For the owner:**
  - a brand read from the 2027 colour forecasts (WGSN × Coloro's projected Luminous Blue and Energy Orange), which is also the colour-blind-safe pair;
  - a design system ready to hand to developers;
  - a plan whose open decisions are all business decisions.

## The value {#value}

- **Measured:** data cost on open data is zero. Pages weigh {{page_kb_min}}–{{page_kb_max}} kB of HTML, with no images and {{js_kb}} kB of script, well inside the Core Web Vitals budget the leaders miss (NBA.com: 5.1 s to first byte on our measurement).
- **Benchmark:** a data-led football publication can reach about a million monthly readers (Opta Analyst). Direct traffic dominates at the stats sites (FotMob, 72.9%).
- **The honest finding:** open data carries the tables, reviews and analysis product, but not the live and xG product. The licence for event data is the one cost that decides whether gameformative competes with FotMob and Opta Analyst or sits beside them. Its price is not public, so no return figure is given until quotes are in.

## Proof — what is real {#proof}

| Real | Sample | Shown, not built |
|---|---|---|
| every result, table, scorer, line-up, attendance; every chart | the article copy (from the data desk; every figure computed) | search, sign-in, newsletter, xG/shots/ratings panels, live scores |

Measured on every page at 375 px and 1440 px: 0 px horizontal overflow, no tap target under 44 px on phones, one heading per page. Contrast is checked in the light and dark themes on every build.

## Risk removed, value added {#risk}

- **Legal data only:** the licences were read before a single row was used.
- **No invented people, quotes or images:** the byline is the data desk, and the covers are drawn from the numbers.
- **Automation is labelled:** it comes from a template, not a language model. The policy follows Article 50 of the EU AI Act.
- **Accessibility is designed in, not retrofitted:** colour is never used alone, every chart has a data table, and there are 44 px targets and a dark theme.

## Delivery and what is needed next {#delivery}

1. **M1 — static launch on open data.** Deploy to the domain, refresh daily, name the newsroom, open the corrections page.
2. **M2 — licensed data.** xG, shots and ratings.
3. **M3 — live.** Score strip and match centre.
4. **M4 — growth.** Newsletter, social stat cards, the first regional expansion.

After the decision, the owner chooses a data provider, names an editor-in-chief, and confirms the business model.

## The one decision {#decision}

<p class="lead-p"><strong>Approve the direction</strong>: the design system, the page set and the open-data-first approach. Then M1 starts and provider quotes are requested.</p>

<a class="cta" href="../index.html">Open the prototype</a> <a class="cta" href="../styleguide/index.html">See the design system</a>

## Appendix — what to click {#appendix}

- **Home:** [the home page](../index.html).
- **A league:** a [league table](../stats/premier-league.html). On a phone, press "All columns"; sort by any heading; switch Overall, Home and Away.
- **Tournament:** the [World Cup bracket](../world-cup-2026/index.html) and [the final's match centre](../world-cup-2026/final.html).
- **Analysis:** an [analysis piece](../analysis/how-spain-won-the-world-cup.html), and under any chart "Show the numbers as a table".
- **Standards:** [How we count](../how-we-count/index.html).
- **Theme:** the theme button in the header switches light and dark.
