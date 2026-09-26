# Content handover — gameformative.com

*For the content creator taking over article writing. Prepared 2026-09-26. Everything gathered so
far that matters for content is in this folder or linked from here: the product, the eight desks,
the house rules, the sourcing workflow, what is already published, the article plan with 24 checked
candidates, a draft template and a checker. This folder is temporary — once its drafts are published
and its briefs used, it is removed; nothing in it is a permanent home for a fact.*

## 1. What gameformative is

In the owner's words (2026-09-25): *"Gameformative will be a sport analytical and educational
infotainment media site to support readers with news, tactics, techniques, scientific research
about sport and related subjects."* It launches **with articles only** — "to have a base with
informative great edutainment content in the sport industry". A set of football statistics pages
exists as a later phase; ignore it for content.

- **Live prototype:** https://moldovancsaba.github.io/calvus/gameformative/index.html
- **The standards page readers see:** https://moldovancsaba.github.io/calvus/gameformative/how-we-count/index.html
- **The owner's first article** (the model for tone and structure): https://moldovancsaba.github.io/calvus/gameformative/articles/gps-injury-risk-which-math.html

**Reader and voice.** Curious fans, coaches, athletes and people working in sport, reading on a phone
as often as a desktop, often arriving from a social feed. Trust in news is low (37%, Reuters Institute
Digital News Report 2026) and readers prefer human-made journalism, so the voice is **clear, warm,
precise, sourced — edutainment, never clickbait.** Second person is welcome. British English. Every
number carries its unit and its source; every claim is one a reader could check.

## 2. The eight desks — where every article sits

Each article sits on **exactly one** desk, chosen by what it does for the reader (owner's table,
verbatim):

| Desk | What the article does for the reader |
|---|---|
| Discover | Something new: tech, method, science finding, financing model |
| Define | Literacy: what a term/metric/rule means, and how not to get fooled |
| Design | How to build: team, tactic, training system, experience |
| Develop | Pathways: athletes and coaches getting better over time |
| Data | Analytics: models, tracking, measurement, decision support |
| Drive | What moves results: incentives, culture, leadership, audience levers |
| Defend | Risk and integrity: injury systems, load practice, governance |
| Deal | Money and rights: sponsorship, media rights, commercial structures |

Each article also carries one **subject** tag (the owner's earlier topic list): international news,
sport science, tactics & technique, sport analytics, data intelligence, sport tech, athlete
development, fan engagement, sponsorship, training goods, sport goods. And one **kind**: Explainer,
Analysis or News (Opinion only for signed columns).

## 3. The house rules (owner, 2026-09-25) — enforced by the site

1. **800–3,200 characters of body text.** Body = the standfirst (optional) and every paragraph,
   spaces included. **Not counted:** headline, segment headings, charts, the source lists.
2. **Always segmented:** at least **three** segments, each under its own heading. The owner's first
   article uses seven: *Why this matters now · The landscape · What you can do with this · What we
   would keep · What we would question · How the field is arguing it · Closing note* — a good default.
3. **Two source lists close every article, not counted in the length:**
   - **Sources used** — every source the text relies on;
   - **Sources investigated but not used** — what you opened or requested and set aside, **with the
     honest reason** (weaker, wrong population, unreadable/paywalled, duplicative, older).
   Each entry: linked title — publisher, date — one line on what it contributed / why not used.

The site's build refuses an article that breaks these rules, and its gate re-measures every
published page. Check a draft before handing it over:

```
python3 gameformative/temp-startup-content/check-draft.py gameformative/temp-startup-content/drafts/<slug>.md
```

It counts exactly as the site does (tested: the owner's article → 2,358 characters, 7 segments).

## 4. How we source — the workflow

1. **Start from a seed you can read:** a paper, an official report or decision, a published dataset,
   a financial statement, credible reporting. Primary before secondary. Seeds should be recent
   (2026; ideally the last three months).
2. **Open every source yourself** and record what you read. Labels used in the briefs:
   **OPENED (verbatim)** — read and checked word for word; **OPENED (fetch tool)** — read through a
   summarising tool, **re-check verbatim before writing**; **SNIPPET ONLY** — seen in a search result,
   **never a seed and never a figure**; **BLOCKED** — 403, paywall, JavaScript wall: not read.
3. **A source you could not read is never cited as read.** It may appear under *investigated but not
   used*, with the reason "could not be read (paywall / 403)".
4. **Our own calculations are labelled** ("≈13.6% — our calculation from the audited accounts").
   Other people's calculations are attributed to them.
5. **Check every link on the day the article is handed over** (it must resolve).
6. **Never invent** a figure, a quote, a date, a source or a person. If the evidence gives no pooled
   number, the article gives none.
7. **Legal and fair:** no allegations against named people; governance stories stick to published
   decisions; no private individuals, and never minors by name; short quotes only, attributed;
   paraphrase the rest; never copy a paywalled text.
8. **Say what the evidence cannot show** — small samples, preliminary data, association vs cause.
   Each brief's *Risks* section lists the traps for that story.

## 5. Editorial responsibility and AI

Drafts end at **status: ready-for-editor**. Nothing is published without review by the site's
**named editor**, who takes editorial responsibility — the owner has still to name that person
(open question A2). This is also the legal line: under Article 50 of the EU AI Act (applicable from
2 August 2026), AI-generated text published to inform the public must be disclosed unless it has had
a substantive human review under a named person's editorial responsibility. The site's policy is
stated on How we work. Content speaks as gameformative; no tool, model or assistant is named in an
article, a byline or a source note.

## 6. Already published — do not duplicate

| Article | Desk · kind · subject |
|---|---|
| Your GPS says "injury risk." The new football evidence says: which math are we using? (owner's article) | Define · Explainer · Sport science |
| Five from five: what Man City's perfect start does — and doesn't — tell us | Data · Analysis · Sport analytics |
| Europe's big five after a month: the Bundesliga scores most, the Premier League draws most | Data · Analysis · Sport analytics |
| How Spain won the 2026 World Cup: 14 scored, 1 conceded | Data · Analysis · International news |
| One goal in four came after the 75th minute: the 2025/26 Premier League by the clock | Data · Analysis · Sport analytics |
| Points per game, goal difference and form: how to read a table in September | Define · Explainer · Sport analytics |

The five data pieces are sample copy computed from public-domain football results (openfootball, CC0);
treat them as placeholders the newsroom can replace. The GPS / ACWR / injury angle is taken.

## 7. What to write — the plan

**`article-plan.md`** — the first eight articles, one per desk, in writing order, each with its
seed, its core fact, what it must not overclaim, and the brief to open; the conflicts between desks
resolved; 14 reserves.

**`find/`** — the four find briefs (2026-09-26): 24 candidates, three per desk, each with a working
headline, the seed (title, publisher, date, URL, the exact finding), supporting sources, sources
investigated and not used with reasons, a segment outline and risks; plus parked leads.

| File | Desks |
|---|---|
| `find/01-discover-define.md` | Discover, Define |
| `find/02-design-develop.md` | Design, Develop |
| `find/03-data-drive.md` | Data, Drive |
| `find/04-defend-deal.md` | Defend, Deal |

## 8. Everything else gathered so far — where it lives

Kept in one place each (not copied here, to keep a single source):

| What | Where |
|---|---|
| The research: the sport media industry, how fans get news, the benchmark of 31 sites, 2027 colour forecasts, UX, trust and AI | `../docs/01-research.md` |
| **Every source researched, with its status and what we learned** — industry (Reuters Institute DNR 2026, PwC, Deloitte, Nielsen, Ampere…), open-data licences, standards, and the checks of the published articles' sources | `../docs/01a-source-register.md` |
| The raw research notes in full (figures, quotes, fetch times) | `../docs/01b-evidence.md` |
| The check of the owner's first article's sources, link by link | `../docs/03-sources.md` §3 |
| Decisions (desks, rules, what a character is, subject tags) | `../docs/04-decisions.md` D17–D28 |
| Open questions for the owner | `../docs/08-client-asks.md` |
| The text of every published article, and how the site stores one | `../content.py` (`articles()`) |

Useful background facts for articles, all sourced in the register: 54% reach news through social and
video networks, 51% through publishers' own sites (DNR 2026); 12% are comfortable with news made
entirely by AI, 62% prefer human-made (Reuters Institute, 2025); women's elite sport revenue is
**projected** at US$3bn in 2026 (Deloitte); 51% of people globally are football fans (Nielsen 2025).

## 9. Handing drafts back

1. Copy `article-template.md` to `drafts/<slug>.md`, write, and fill the meta block (desk, subject,
   kind, slug, byline, status).
2. Run `check-draft.py` until it prints **OK**.
3. Set `status: ready-for-editor`. Add, at the foot of the draft (in an HTML comment), the date you
   checked the links and anything the editor must decide.
4. The site maintainer moves an approved draft into `content.py`, runs `python3
   gameformative/build.py` and `python3 check.py`, and publishes.

## 10. Open questions from the owner that touch content

- **A2** — who is the named editor who signs articles off?
- **A8** — is the character count right (body text only, as above)?
- **A9** — source notes in the first article use editorial shorthand ("Seed", "curiosity gap"); keep
  that style or write notes for readers? *Until answered, write notes for readers.*
- **A11** — the GPS article sits on Define; the owner may move it to Defend.
