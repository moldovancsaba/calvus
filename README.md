# Calvus

Calvus is where client-facing prototypes and wireframes get built — before any
real product code exists.

## Why this repo exists

When a client wants a new site, dashboard, or feature, the expensive way to
find out what they actually want is to build it for real, show them, and then
rebuild the parts they didn't want. This repo exists to skip that: put
something they can click through in front of them first, cheaply, using
throwaway static pages instead of the real application stack.

The point is to absorb the "what did you actually mean" churn — layout,
navigation, wording, which numbers matter, what the client thinks the product
even is — in a medium that costs almost nothing to change, before a single
line of production code, a database schema, or a real API gets written. A
wireframe that's wrong costs an edit. A production feature that's wrong costs
a rewrite.

Once a client has agreed a direction here, that becomes the spec for the real
build — which happens in a real project, with a real stack, not in this repo.
Nothing here is meant to become production code by gradually hardening in
place; it's meant to be looked at, argued about, revised, and then left behind
once its job — getting everyone to agreement — is done.

## How we work

- **Static HTML/CSS/JS, no build step.** No framework, no package manager, no
  bundler, no compile step. A prototype is a folder of `.html` files you can
  open directly or serve with `python3 -m http.server`. This is deliberate:
  the whole point is that anyone can open a page and edit it in minutes,
  without setting up a toolchain first. Production concerns (a real
  framework, a real backend, a real database) belong in the eventual real
  build, not here.
- **One folder per client project**, each self-contained — its own HTML,
  its own `styles.css` if it needs one, its own data file if it needs one.
  Projects don't share a design system or a components folder on purpose;
  each client's prototype should look like *their* brand, not like a Calvus
  house style.
- **Real data where it exists, honestly flagged where it doesn't.** When a
  client has given us real numbers (survey results, salary bands, pricing),
  we wire those in — a prototype that shows made-up numbers next to real ones
  undermines the whole pitch. When a control has nothing real behind it yet
  (an export button with no file to export, a language switch with no
  translated content), it's shown in place, visibly disabled, rather than
  either faked or omitted — the client sees the intended shape of the product
  without us pretending a feature works. See
  `idbc-salary-guide/data/SOURCES-AND-GAPS.md` for what that looks like in
  practice: every number traced back to its source document, every gap
  between what the client asked for and what the underlying data can actually
  support written down instead of quietly papered over.
- **Fidelity is a dial, not a fixed target.** `lexodont.hu/` and
  `lexodont.hu_balsamic/` are the same site at two different fidelity levels
  — a full-colour, close-to-final version and a deliberately rough,
  Balsamiq-style grayscale sketch. Which one to show depends on how early the
  conversation is: rough sketches invite structural feedback ("should this
  section exist at all"), polished mockups invite detail feedback ("move
  this button"). Asking for the wrong kind of feedback at the wrong stage
  wastes a client meeting.
- **Deployed where a link can be shared.** Each push to `main` goes live on
  GitHub Pages, so "here's the prototype" is always just a URL, not a zip
  file or a screen-share. See `CLAUDE.md` for the actual mechanics — direct
  push to `main` is pre-authorized here (the owner works from mobile with no
  terminal, so a PR-and-wait workflow isn't practical), gated by a manual
  check before every push since there's no CI to run one automatically.

## What's in here right now

| Project | What it is | Fidelity |
|---|---|---|
| `lexodont.hu/` | Dental clinic marketing site — services, team, pricing, case studies. The live lexodont.hu was built from this wireframe (measured 2026-09-18); `lexodont.hu/docs/` is the record — presentation, audit of the built site, decisions, gate | Polished — delivered |
| `lexodont.hu_balsamic/` | Same site, sketch-style | Low-fidelity / Balsamiq |
| `idbc-salary-guide/` | Talent Market & Salary Guide 2026 — survey trends (12 datasets), area pages, Bérek with TOP3 and LinkedIn counts, SAP, Expert Community, case studies, registration mock; all from the client's workbooks via two converters; `docs/` holds the standard set incl. the Hungarian `bemutato.html`; `check.py` is its gate | Polished — in client fine-tuning |
| `discountdirect/` | Seller–buyer messaging app concept — communication timeline with personalised offer cards, channel selection (chat/e-mail/mailing), one-product flash campaigns with time/quantity limits, and automated per-buyer offer lists. CSS custom properties are named after GDS 6.5.0 roles for a 1:1 dev handoff (`discountdirect/GDS-TOKEN-MAP.md`) — naming only, no dependency. `discountdirect/EXECUTIVE.md`, `RESEARCH.md` and `BUSINESS-LOGIC.md` (rendered by `build-docs.py`) carry the executive summary, the sourced research on B2C upsell/cross-sell and next-best-action, and the rule-by-rule breakdown for development; `SSOT.md`, `ARCHITECTURE.md`, `TECHNICAL-DESIGN.md` and `IMPLEMENTATION-PLAN.md` are the engineering package (definitions, containers and flows, schema/API/algorithms, milestones and issues with DoD); `README.md` there indexes the standard documentation set incl. the Hungarian `bemutato.html`, audit, design, build log, gate and client asks | Interactive prototype |
| `holdvolgy/` | Tokaji winery (holdvolgy.com) 2026 rebuild on the estate's own brand. Every page in HU and EN generated by `holdvolgy/build.py` from one content source; desktop and phone designed separately; research, audit, assets, decisions, design system, frames and every gate live in `holdvolgy/docs/` — read `docs/README.md` first | All five phases built: home, Birtok, Tokaji aszú, Látogatás, shop with 32 product pages, Borklub — HU and EN throughout; technical package (SSOT, architecture with a proposed stack, technical design, implementation plan, token map) in `holdvolgy/docs/10`–`14` |
| `PRODUCT.md` → `product.html` | The product standard: the premise (the product is the subject, the first customer the example), the twelve documents, the acceptance criteria, the rules from business.direct's audit (2026-09-20) | current |
| `HUB-AUDIT.md` → `hub-audit.html` | Cross-project audit (2026-09-20): every project measured against every other and the standard; what business.direct misses, what the others miss, recommended actions prioritised — all PROPOSED | current |
| `business-direct/` | A standalone product for classified media owners: marketing (content generated from the listings and delivered to every medium), B2B sales (contact, acquire), retention (reduce churn), a human gate on everything, and the owner's economics — listing price, advertiser CAC and LTV, visitor cost and value, churn, the next dollar — as a service in the product; one responsible-data policy record per site. Example persona and first buyer: ClassScout (Your Field NYC); `index.html` is the clickable prototype on their real listings (nothing sends). `docs/` is the final set of twelve: presentation, executive summary, product definition, product specification, market, economics, business logic and SSOT, architecture and blueprint, delivery plan with the operating model and the sign-off sheet, responsible data and the legal position, the first-customer file, evidence — plus the design set, six research rounds and the history; every earlier page name redirects | Prototype, presentation and the full set done 2026-09-20 (D44); next: the stakeholders' sign-off |
| `index.html` | The hub page linking every project above | — |

## How a prototype is built — the method

`PROTOTYPING.md` (rendered as `prototyping.html`, linked from the hub) is the standard
for every future prototype: the lifecycle and its gates, the requirements for pages
(real data honestly flagged, generation, measured phone and desktop passes), the
documentation set, the gate, the fine-tuning rules, a starter checklist and a definition
of done per stage. Distilled 2026-09-18 from the four projects here.

## The standard documentation structure

Every project carries the same set next to its prototype, in its `docs/` (DiscountDirect:
flat in its folder), indexed by a `README.md` that is also the process log: a
client presentation in the client's language (`bemutato.html` for the Hungarian clients,
`presentation.html` for business.direct); brief, research, audit, sources, decisions, design,
build log, gate, client asks; and a technical package — SSOT, architecture, technical
design, implementation plan, token map — with every stack decision marked PROPOSED until
the owner or client flips it (business.direct's became the build baseline with its real-system
blueprint, D37). `python3 build-docs.py` renders all of them; `python3
check.py` is the one gate. Adopted 2026-09-18.

## How agents (and humans) should behave here

`CLAUDE.md` is the operational rule set for this repo — read-first discipline,
the AI-attribution policy, what counts as pre-authorized (direct pushes to
`main`) versus what needs confirmation (force-push, ref deletion), and the
manual quality gate to run before every push since there's no CI to do it
automatically. This README is the "why we're doing any of this" companion to
that; CLAUDE.md is the "how to act while doing it."

## A note on this repo's history

The commit history goes back further than the client-wireframe work — this
repo was previously used for an unrelated prototype (`git log` shows old
commits about a game/mesh viewer). That work has no live pages left in the
current tree; it's inert history, not a second project living alongside this
one.
