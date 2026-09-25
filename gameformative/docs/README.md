# gameformative — project documentation

gameformative.com is a sport analytical and educational infotainment site — news, tactics,
techniques and the science of sport, organised in eight desks (Discover, Define, Design, Develop,
Data, Drive, Defend, Deal). It launches with articles only; every
article runs 800–3,200 characters in headed segments and ends with the sources used and the
sources investigated but not used. The football statistics built in round 1 (real public-domain
data, openfootball CC0) are a later phase, kept live. The presentation for the owner: [presentation.html](presentation.html). The prototype:
[home page](../index.html). The design system, live: [style guide](../styleguide/index.html).

| Document | What it holds |
|---|---|
| `00-brief.md` | the ask verbatim, what the prototype is, what is real / sample / inert / not built |
| `01-research.md` | the synthesis: industry, how fans get news, the benchmark (global, Germany, India, China, stats sites), colour and 2027 forecasts, type, UX best practice, trust and AI, proposals P1–P12 |
| `01a-source-register.md` | **every source researched, one row each, with its status and what we learned** — the sites and rankings (G, R, DE, IN, CN, ST), the industry (I), open data (O), colour and design forecasts (T), standards and practice (S) |
| `01b-evidence.md` | the four research passes in full: methods, timestamps, raw measurements |
| `02-audit.md` | gameformative.com measured: registered 2026-09-25, Vercel DNS, no deployment |
| `03-sources.md` | the build's inputs and every gap, numbered |
| `04-decisions.md` | D1–D16 |
| `05-design.md` | tokens, type, layout at the reference widths, components |
| `06-build-log.md` | the build round, what was measured, what was fixed |
| `07-gate.md` | what `check.py` verifies and the measured pass |
| `08-client-asks.md` | the asks A0–A7, none blocking the review |
| `10-ssot.md` | glossary, entities, the rules register, settings, document map |
| `11-architecture.md` | the real build: targets, containers, ADR-01–06 (PROPOSED) |
| `12-technical-design.md` | the pipeline, content model, data mapping, templates, the live match centre spec |
| `13-implementation-plan.md` | milestones M0–M4, issues with a Definition of Done, blocked register, risks |
| `14-token-map.md` | prototype tokens and components → production |
| `18-responsible-data.md` | what is stored (nothing personal), the policy record, the gate |

Regenerate: `python3 gameformative/data/convert.py` (only after a fetch), `python3
gameformative/build.py`, `python3 gameformative/docs/build.py`, then `python3 check.py` at the root.

## Process log

**2026-09-25 — project opened; research.** The owner asked for gameformative.com: deep research on
the sport media industry, 2027 colour and layout trends, BBC Sport, ESPN, NBA.com, FIFA and the top
sports sites of Germany, India and China, colour, UX and mobile/desktop best practice — and the best
possible prototype with documentation, checking Népszabadság as the precedent. Four research passes
ran the same day: 31 sites measured with `curl` (nine blocked, named, not described), rankings from
Similarweb and Semrush, industry sources read at source, forecasts labelled as projections, open-data
licences read. The owner declined an external site in the in-app browser; it was used only on the
local prototype from then on (D16). The domain audited: registered that day, no deployment.

**2026-09-25 — the first version built.** Data converted from openfootball with asserts (one stop,
four nation spellings, fixed by an alias table). Design system from the research: warm off-white,
ink navy, Form Blue and Energy Orange (projections read into sRGB, contrast-gated), Archivo in three
widths. 19 pages generated; five articles written from the data with premises. Measured at 375 and
1440 px in the browser pane; found and fixed a hidden sign-in leak, strip padding, four kinds of
small tap target, a twelve-column table unreadable on phones (now compact with "All columns"), card
labels stretching, and bracket headings drifting (`06-build-log.md`). Gate written and wired into the
root `check.py`; clean.

**2026-09-25 — sources register.** The owner asked that the documentation list every source
researched with a short summary of what we learned: `01a-source-register.md`, one row per source,
with its status (measured, opened, secondary, blocked, snippet only, projection).

**2026-09-25 — round 2: articles first.** The owner set the launch to articles only, repositioned
gameformative as a sport analysis and education site across ten named topics ("and similar"), set
the house rules (800–3,200 characters, always segmented, sources used and investigated at the end,
not counted) and sent the first article draft. The draft's five links were requested and the two
used sources read — both support the text; two investigated sources could not be read (MDPI 403,
Springer challenge). Built: eleven topics (the owner's ten plus Tactics & technique, from the owner's
own description), a topic bar, an articles-first home, `articles/` with the owner's piece as the lead
and the five data pieces restructured into headed segments with honest source lists, topic pages,
How we work, redirects from `/analysis/`, and the data pages moved to "a later phase". An unsourced
claim in our own explainer was sourced (D24). The rules are enforced by the build and by a new gate
check measured on the rendered pages; a deliberately broken page proved it fails. Measured at 375 and
1440 px, clean. Decisions D17–D25; asks A8–A10.

**2026-09-25 — round 3: the eight desks.** The owner gave the article structure: Discover, Define,
Design, Develop, Data, Drive, Defend, Deal — each defined by what the article does for the reader.
They are now the site's sections (desk bar, desk pages, desk tiles, How we work); every article sits
on one desk, enforced by the build and the gate; the round-2 topics stay as subject tags, their live
pages kept (D26–D28). Measured at 375 and 1440 px, clean. Ask A11: the GPS article's desk.
