# gameformative.com

## Where it stands {#situation}

<p class="lead-p">gameformative.com was registered on 25 September 2026. Its DNS points at Vercel, and the domain serves a 404: there is no site, brand, audience or content yet. The plan is to launch with articles, "to have a base with informative great edutainment content in the sport industry".</p>

The market it enters is measured:

- **Sport is the world's shared subject.** 51% of people globally call themselves football fans (Nielsen, 2025).
- **Readers find news in feeds first.** Social and video networks (54%) now beat publishers' own sites and apps (51%) as a way into news (Reuters Institute, 2026).
- **The expert sites sell numbers.** The statistics sites we measured are built around tables, ratings and predictions. Opta Analyst reaches about a million readers a month on data-led writing (Stats Perform).

## The complication {#complication}

- **Trust in news is 37%** (Reuters Institute, 2026).
- **Readers prefer human-made news.** Only 12% are comfortable with news made entirely by AI (Reuters Institute, 2025).
- **Automated sports recaps are already drawing criticism.** They have been faulted for thin copy and have carried factual errors (MLS, 2025; ESPN, 2024).
- **Sources are usually hidden.** A reader rarely sees what an article relied on, and never what it looked at and left out.
- **The law has moved.** Since 2 August 2026, the EU AI Act requires AI-generated news text to be disclosed unless a named editor is responsible for it.

## The question {#question}

Can a new sport site earn a reader's trust from its first article, and make research, tactics and the business of sport a pleasure to read?

## The answer {#answer}

**Articles that show their work, organised by what they do for the reader.** gameformative has {{desks}} desks:

| Desk | What the article does for the reader |
|---|---|
{{desk_rows}}

Each article sits on one desk and carries one of {{topics}} subjects, from sport science to sponsorship.

Every article follows three house rules, and the build refuses to publish one that breaks them:

1. **{{min_chars}}–{{max_chars}} characters**, long enough to explain and short enough to finish;
2. **always in headed segments**, listed at the top so a reader can jump to what they need;
3. **two source lists at the end:** the sources used, and the sources investigated but not used, each with a line on why.

**The first article is the editorial desk's draft.** It is about GPS load data and injury risk. Before it went in, every link was requested and both used sources were read, and they support the text.

## The value {#value}

- **Measured.** The prototype has {{articles}} articles on {{desks_used}} of the {{desks}} desks. Pages weigh {{page_kb_min}}–{{page_kb_max}} kB of HTML, with no images and {{js_kb}} kB of script. The article rules are checked on every rendered page, and a deliberately broken article fails the check.
- **The honest finding.** The difference from the sites we measured is the sourcing: the two lists at the end of every piece. We saw no site in our benchmark that publishes what it investigated and set aside. The cost of that difference is editorial time, and it grows with every article. No revenue figure is given until the business model is chosen.

## Proof — what is real {#proof}

| Real | Sample | Shown, not built |
|---|---|---|
| the first article (the editorial desk's draft), and its sources, checked; the football data behind the data articles (openfootball, public domain) | the data articles' copy, written from the data, with every figure computed | search, sign-in, newsletter; topic pages with no article yet say so plainly |

Measured on every page at 375 px and 1440 px: 0 px horizontal overflow, no tap target under 44 px on phones, one heading per page, and no console errors. Contrast is checked in the light and dark themes on every build.

## Risk removed, value added {#risk}

- **Sources you can check:** the links are requested on the day of publication. A source we could not read is recorded as such, never cited as read.
- **No invented people, quotes or images:** the covers are drawn from the numbers each article is about.
- **The rules are code, not good intentions:** the build and the gate both enforce them.
- **Accessibility is designed in:** colour is never used alone, every chart has its numbers as a table, targets are 44 px, and there is a dark theme.

## Delivery and what is needed next {#delivery}

1. **M1 — the articles launch.** Deploy to the domain. Name the editor who signs off each piece; the first draft is itself marked for staff review. The content team writes the first article for every desk. Open the corrections page.
2. **Later — the data pages.** The football statistics built in round 1 are kept live as a preview: tables, the World Cup, a match centre.

## The one decision {#decision}

<p class="lead-p"><strong>Approve the articles-first direction</strong>: the eight desks, the article template, and the house rules as implemented, counting characters as the body text, without headings or sources. Then name the editor, and M1 starts.</p>

<a class="cta" href="../index.html">Open the prototype</a> <a class="cta" href="../articles/gps-injury-risk-which-math.html">Read the first article</a>

## Appendix — what to click {#appendix}

- **Home:** [the home page](../index.html). The desk bar under the header lists all eight desks.
- **The first article:** [the GPS article](../articles/gps-injury-risk-which-math.html). Try "In this article" at the top, then the two source lists at the end.
- **A desk:** [Define](../desks/define.html) has two articles; [Deal](../desks/deal.html) shows how an empty desk reads. [All eight desks](../desks/index.html).
- **The rules, in public:** [How we work](../how-we-count/index.html).
- **The later phase:** the [data pages](../stats/index.html).
