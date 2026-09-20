# Prototyping at Calvus — requirements and method

*How a client prototype is built here, what it must contain, and what "done" means at each
stage. Distilled on 2026-09-18 from the four projects in this repo — Holdvölgy (the
customer-side reference), DiscountDirect (the technical reference), the IDBC Salary Guide
(real data, live client fine-tuning) and Lexodont (a wireframe that became a site). Every
rule below has a project behind it; the project is named where it matters. This is the
standard for the next prototype. `README.md` says why this repo exists; `CLAUDE.md` says
how to act in it; this file says what to build and how to know it is good.*

## 1. What a prototype is here, and is not

A prototype is **the cheapest thing a client can click through and argue with**, built to
absorb the "what did you actually mean" churn before production code exists. It is static
HTML/CSS/JS, no framework, no build step beyond a generator you can read in one sitting,
served from this repo on GitHub Pages so the deliverable is always a URL.

It is **not** production code that hardens in place, and it is **not** a design exercise:
its output is agreement — on structure, content, data, rules — recorded so the production
build has a specification. Lexodont proves the point in both directions: a two-day
wireframe became the live site, and because nobody recorded that, the repo presented a
superseded sketch as a live project for five months.

Three kinds have been built, and the method fits all three:

| Kind | Example | What it fixes |
|---|---|---|
| Wireframe (two fidelities) | Lexodont | page set, navigation, section order, copy tone |
| Data prototype | IDBC | which data exists, what it supports, how it reads on a phone |
| Site or product prototype | Holdvölgy, DiscountDirect | the whole experience, generated from one source, with the rules written down |

## 2. The lifecycle — stages and gates

Nothing skips a stage; a stage can be one paragraph if the project is small, but it exists
and it is dated.

| # | Stage | Output | Gate (who approves) |
|---|---|---|---|
| 0 | **Brief** | `00-brief.md`: client, problem, what will be built, what is real | owner reads it |
| 1 | **Research and audit** | `01-research.md` (benchmarks with sources, or "none, because…"), `02-audit.md` (the client's current site/data/brand, **measured**) | owner: "direction approved" (Holdvölgy D10) |
| 2 | **Sources** | `03-sources…md`: every input file, what it contributed, every gap between the ask and the data | — |
| 3 | **Design system** | tokens + a live components page | **owner approves before any layout** (Holdvölgy D11/D12 — the order was corrected once and is now fixed) |
| 4 | **Layout frames** | desktop 1440 and phone 390 composed from the approved components and real assets | owner approves (D13) |
| 5 | **Build** | pages, generated where anything repeats; one commit per page or round; build log with measurements | the gate script + measured pass |
| 6 | **Sweep** | every page at 390 and 1440, zero defects | recorded in the gate doc |
| 7 | **Presentation** | `bemutato.html` in the client's language and brand | client review |
| 8 | **Fine-tuning** | reported item → minimal fix → measured → URL | client |
| 9 | **Technical package** | SSOT, architecture, technical design, implementation plan, token map; stack decisions PROPOSED | owner / client flips ADRs |
| 10 | **Real-system blueprint** (when the owner calls the next phase) | `01g` research: every external service verified against the vendor's own terms on the day (auth, review, limits, prices, alternative, cost); `20-system-blueprint.md`: drawings, repository layout, modules with what each owns and pseudo code, data contracts, jobs, security, tests, operations; the ADRs become the build baseline; the plan re-cut into sprints with an acceptance test each and a sprint-0 checklist — business.direct D37 is the reference | owner: "build" |

Stages 3–4 are the ones people are tempted to skip. Holdvölgy's first prototype skipped
them and was withdrawn as "generic"; the second went through both gates and was approved
in three steps without a redesign. DiscountDirect and IDBC skipped them (the client
supplied mockups, or the wireframe was built in a day) and both later paid in unmeasured
mobile layouts. For a small wireframe the gate can be a single frame; it still exists.

## 3. Requirements for the pages

### 3.1 Content and data — real, or honestly absent

- **Every number, text and image traces to a client file**, named in the sources doc.
  IDBC's `SOURCES-AND-GAPS.md` is the model: file → what it contributed → where the
  build diverges from the client's intent, numbered.
- **No figure is invented or estimated.** If the client's list and the data do not match
  by name, match by an explicit, reviewed table that fails the build on a mismatch (IDBC
  `build-salary-data.py`); never fuzzy-match at runtime, never guess.
- **A control with nothing behind it is shown in place, visibly inert** — `is-unavailable`,
  `aria-disabled`, and a `title` that says why (Excel export with no file, an EN switch
  with no copy, a logout with no auth). Never faked, never omitted.
- **Placeholders only at the client's request**, labelled as such, naming what goes there
  ("A terület videója ide kerül"). Lorem ipsum does not ship.
- **Sample data is declared sample** in the page itself (DiscountDirect's top-bar note and
  wireframe note; the prototype banner on Holdvölgy).
- **The client's own copy ships as written**, even where it asserts more than the data
  does — and the divergence is recorded, not hidden (IDBC's "valós piaci adatok" vs the
  sheet's own "mintaértékek" banner, gap 6).
- **No AI-generated imagery** (Holdvölgy D6). Stock placeholders are flagged as a client
  ask (IDBC #15).

### 3.2 Structure and generation

- **One source for anything that repeats.** Eleven area pages are one template with a
  query parameter (IDBC); 32 product pages in two languages are one catalogue and one
  generator (Holdvölgy); navigation and document indexes are single-sourced (D15).
  Never eleven copies of a renderer in a repo with no build step.
- **Data enters through a converter, not by hand.** Converters are deterministic, take
  their inputs as arguments, print what they did, and assert what must hold (every
  question resolves; every listed position exists). Re-running on the same input must
  reproduce the committed output byte for byte.
- **Shared assets are versioned** (`?v=N` or a hash) and the gate checks every page loads
  the same version — GitHub Pages and the browser pane both serve stale copies otherwise,
  and the failure looks exactly like the change silently not working.
- **Every page** has exactly one `h1`, a `<title>`, `lang`, `alt` on every image, and —
  when the project is bilingual — `hreflang` hu / en / x-default. Product-like pages carry
  JSON-LD.
- **Images**: conversions keep alpha (never `.convert('RGB')` on a transparent PNG);
  `img { height: auto }` in base CSS so width/height attributes never distort; images in
  aspect-ratio boxes are absolutely bounded (Holdvölgy D16/D17 — found as a black,
  stretched map on the live site).
- **Class names are namespaced** where they could read as generic (`.sheet`, `.bar`,
  `.card`); the gate checks for a second definition (D18 — a fact sheet floated over the
  page because it shared `.sheet` with the menu dialog).
- **A published URL is never deleted.** Content that moves leaves a redirect stub (D14 —
  a cached hub card led to a 404).

### 3.3 Phone and desktop — measured, not eyeballed

Reference widths are **390 (phone) and 1440 (desktop)**; tablet is resolved explicitly in
the layout spec. Phone and desktop may be two designed experiences (Holdvölgy D5), but
both are measured. At both widths, on every page:

| Criterion | Target |
|---|---|
| Horizontal overflow | 0 px |
| Tap targets (phone width, menus open) | none under 44 × 44 px — including short menu labels ("SAP" was 27 px wide) |
| Console errors | 0 |
| `h1` / `alt` / `title` / `lang` / `hreflang` | as §3.2 |
| Tables on phones | cards or real horizontal scrolling with a labelled, focusable region — never 419 px of silent overflow (IDBC, 2026-09-15) |
| Home page weight (when a client sets a budget) | measured with real assets in place |

Desktop density is allowed to be tighter than 44 px; the floor is a phone rule.

The measurement is done in the app's browser pane (Playwright is not installed here):
`resize_window` to the phone preset, exercise the feature, read the DOM — or, for a whole
site, load every page in same-origin iframes at both widths and measure from one script
(Holdvölgy's 152-measurement sweep, Lexodont's 66). Screenshots are a supplement; when the
pane is hidden they come back blank, so the gate must not depend on them — and a hidden
pane reports a 0 px viewport, so every measurement sets an explicit width first and
records `clientWidth` with the result.

### 3.4 Interaction and the two interfaces

A prototype that a client's operator will run day to day has **two interfaces on one
machine**: a *Simple* one that shows what needs a person as ranked recommendations with
the reason and one button, plus a single press for the actions the machine judges safe;
and an *Advanced* one with every screen and input. Every screen carries a *What is this?*
panel; a *How to use* screen and *Templates* the operator can copy exist from the first
build round that has a second screen (business.direct, D33). The rules are identical in
both modes — Simple changes what is shown, never what may happen.

The feature that changed is exercised, not glanced at: every filter value, every tab,
every persona, both views. When real data cannot reach a code path (IDBC's TOP3 pill before
the new bértábla), the path is exercised with synthetic rows through the component's API
and that is written down.

## 4. The documentation set — one structure, every project

Next to every prototype, in `docs/` (or flat, as DiscountDirect, when the URLs are already
live), indexed by a `README.md` that is also the dated process log:

| Slot | File | Must contain |
|---|---|---|
| Presentation | `bemutato.html` | client's language, client's brand tokens, standalone page: one sentence, three numbers, the pages in a recommended order with previews and open buttons, what is real, the asks, what comes next — no documentation chrome. A one-page prototype with views takes `?view=&screen=` deep links so each preview and open button lands on the right screen (business.direct) |
| 00 | `00-brief.md` | client, problem, what the prototype is, what is real / inert / placeholder / not built, where it stands, how to read the folder |
| 01 | `01-research.md` | benchmarks with sources; or the honest sentence that none was done and what a next round would read |
| 02 | `02-audit.md` | the client's current site, data or brand, **measured** (platform, plugins, weight, TTFB, page architecture, defects) |
| 03 | `03-sources…md` | every input, what it contributed, what is sample, every gap numbered |
| 04 | `04-decisions.md` | numbered register: date, decision, by whom, why, what it replaced; standing rules that came out of them |
| 05 | `05-design.md` | tokens, components, layout at the reference widths; or the client's mockups the pages transcribe |
| 06 | `06-build-log.md` | every round: what changed, what was measured |
| 07 | `07-gate.md` + `check.py` | what the script checks, the measured pass, deliberate deviations with reasons |
| 08 | `08-client-asks.md` | the register of asks with states; **nothing the client must answer to be presented to** — open items that only matter after acceptance move to `19-implementation-prerequisites.md` (before the first real action · before the keyed release · to confirm at acceptance) |
| 10 | `10-ssot.md` | glossary, enumerations, entities, settings, rules register, metrics, document map |
| 11 | `11-architecture.md` | context, the target measured, quality attributes, containers, flows, stack, ADRs |
| 12 | `12-technical-design.md` | templates, content model, data mapping, forms, state machines, i18n, SEO/URLs, media, performance, operations |
| 13 | `13-implementation-plan.md` | milestones, issues with a Definition of Done, blocked register, risks, release scope |
| 14 | `14-token-map.md` | prototype tokens and components → production; or why there is nothing to map |
| 18 | `18-responsible-data-policy-framework.md` (or the project's equivalent) | **required for any prototype that sends, stores or targets people**: the policy record per client instance (jurisdictions and laws, audience model, child-data rule, consent per channel, high-privacy defaults, cap, opt-out SLA, AI disclosure, retention, the client's published policy clauses) and the gate that blocks a feature until its fields are set — see business.direct for the reference |
| 19 | `19-implementation-prerequisites.md` | what the client provides after acceptance, grouped by when it blocks; the presentation's "what we ask of you today" is one decision |
| 20 | `20-system-blueprint.md` (+ a research round on the services) | stage 10 only: the document a developer builds from — every service verified and priced on the day, drawings, modules with pseudo code, contracts, jobs, security, tests, operations; the prototype → module map so nothing built in the prototype is lost |

Rules for the set:

- **Markdown is the source; HTML is rendered** by the project's `build.py` with output
  names that differ from the `.md` basenames (Jekyll on GitHub Pages renders `x.md` to
  `x.html` on its own — the two must never collide).
- **Every docs page links every other** (the gate checks); the presentation carries no
  docs navigation and is linked from the index and the hub.
- **Dates inside every file**; the process log entry is written in the same commit as the
  change. A decision is a numbered entry before it is code.
- **Stack decisions are ADRs in status PROPOSED** with options and reasons; the owner or
  client flips one, and the flip is the next D-number. Where production already exists
  (Lexodont), the architecture records the as-built stack as fact and proposes only
  measured next steps.
- **The audit measures.** `curl` reaches the client's site from this environment: platform
  generator tags, plugin slugs in the HTML, script and stylesheet counts, HTML size, TTFB
  warm and cold, cache headers. Numbers, not impressions — Holdvölgy's 23 plugins against
  a target of 12 and 4,5 s cold TTFB are the whole argument for its stack proposal.
- **Client asks are a list with owners**, not sentences in prose; when one closes it moves
  to the process log. **An ask is never a presentation blocker**: the prototype runs on
  declared defaults and samples; what only matters after acceptance is a prerequisite, not
  an ask (owner directive 2026-09-19).
- **Responsible data is not client-specific.** A child is an age, never a name; no profiling
  or targeting on a minor's data, with or without consent; high-privacy defaults; consent
  that names channel and sender; the postal address and the opt-out on every commercial
  e-mail; disclosure when a machine wrote or made something. These hold whatever the client
  — the client's record changes values, not rules (owner directive 2026-09-19).
- **Docs pass the same page rules**: no horizontal overflow at 375 (long `code` strings
  need `overflow-wrap: anywhere`), 44 px links, one `h1`.

## 5. The gate — what runs before every push

There is no CI. The gate is a script per project plus a repo-wide one, and it must print
`GATE: CLEAN` before a push — a red gate is never pushed as a "known issue"; either the
finding is fixed or the check is wrong and is changed with a recorded reason.

`python3 check.py` at the root runs all of them and a repo-wide link audit. A project's
`check.py` checks at least: every relative link and asset resolves; every cross-page anchor
exists; every docs page links every other; plus the project's own invariants — stale-state
phrases and the prototype banner (Holdvölgy), one asset version and inert controls still
marked (IDBC), fidelity parity (Lexodont). A new invariant is added the day its absence
costs a review round: the stale-phrase scan exists because the owner caught stale text
four times.

Then the measured pass (§3.3), then push, then **verify live**: poll the GitHub Pages URL
with a cache-busting query for a marker unique to the change until it is served (four to
seven tries at ten seconds is normal), and put the URL in the message. A push without the
live URL is not finished.

## 6. Working with the client — fine-tuning rules

Once a client has seen a URL, the project is in fine-tuning, and the rules change:

- **Only the reported item changes.** Nothing is restructured, hidden, removed or
  "improved" unasked. A table that disappears because a data rebuild made it empty is a
  defect the client sees within the hour (IDBC D24).
- **A data rebuild keeps the page's behaviour** — complete tables stay complete, blocks
  stay visible — and adapts the minimum.
- **When the data suggests a layout change, say so in one line and leave the layout alone**
  until told.
- **The client's words are the headings.** Feedback is answered item by item under the
  client's own headings, with status: done / done-already / needs X from you.
- **Never let the client see "nothing happened".** When a change cannot show (the TOP3
  pills before the matching bértábla), the message says so before the client asks.
- **Every message with a change ends with the live URL.**

## 7. Attribution and voice

The product speaks as the product. No AI system is an author, contributor, reviewer or
brand anywhere — commits, pages, docs, metadata (CLAUDE.md rule 1, non-negotiable).
Documentation is written to the reader (client, staff, developer), in English for the
engineering set and in the client's language for the presentation; the client's own terms
are kept (dűlő, bértábla, Expert Community) rather than translated into ours.

## 8. Starting a new project — checklist

1. **Folder**: `<client>/` self-contained; its own `styles.css` or tokens; no shared
   components folder. Add it to the hub card list and to `README.md`'s table.
2. **Brief** (`docs/00-brief.md`) before any page: who, what problem, what will be real.
3. **Audit the client's current state with `curl`** and write `02-audit.md` the same day;
   read every file the client sent and write `03-sources.md` with the gaps.
4. **Tokens first**: a `tokens.css` (or a `:root` block) and a live design-system page;
   get it approved. Then two frames (1440 / 390); get them approved.
5. **Generate what repeats**; write the converter for any data with asserts; commit the
   data file, never edit it by hand.
6. **Build one page per commit** with its measurement in `06-build-log.md`.
7. **Write `check.py`** the day the second page exists; wire it into the root `check.py`.
8. **Sweep** at both widths; write `07-gate.md`.
9. **Presentation** in the client's language on the client's tokens; link it from the
   docs index and the hub.
10. **Decisions as they happen** in `04-decisions.md`; client asks as a numbered list.
11. **Technical package** (`10`–`14`) once the client has agreed the direction — the stack
    as PROPOSED ADRs with the audit's numbers behind them.
12. **Every push**: `python3 check.py` → measured pass → push → live poll → URL.

The fastest way to start is to copy `idbc-salary-guide/docs/build.py` and `docs.css`,
change the tokens and the brand line, and create the fifteen files from the table in §4 —
each can be a paragraph on day one, but each exists and is dated.

## 9. Definition of done, per stage

| Stage | Done when |
|---|---|
| Brief | a stranger can say what the prototype is, what is real and where it stands from two pages |
| Audit | every claim about the client's site or data has a measurement or a file behind it |
| Design system | approved by the owner on a rendered page, before any layout |
| Frames | approved at both widths, composed from approved components and real assets |
| Page | matches the frame; gate clean; 0 overflow, 0 small targets, 0 console errors at 390 and 1440; measurement in the build log; live URL served |
| Sweep | every page, both widths, zero defects, written down |
| Presentation | in the client's language and brand, standalone, with previews and asks; the client can review from a phone |
| Fine-tuning round | the reported item changed and nothing else; measured; URL sent under the client's heading |
| Technical package | SSOT defines every term the others use; architecture cites the audit's numbers; every ADR has options and a reason; the plan has DoD per issue and an honest blocked register |
| Real-system blueprint | every service's limits and prices carry the date they were read and a primary link; every module says what it owns and has pseudo code for what is not obvious; every rule that is code names a test; every sprint has an acceptance test the owner can watch; nothing in the prototype lacks a module |
| Project | all fifteen slots exist and are dated; `check.py` clean; hub, README and CLAUDE.md know about it |
