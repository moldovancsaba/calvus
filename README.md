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
| `lexodont.hu/` | Dental clinic marketing site — services, team, pricing, case studies | Polished |
| `lexodont.hu_balsamic/` | Same site, sketch-style | Low-fidelity / Balsamiq |
| `idbc-salary-guide/` | SAP and general market salary-survey dashboard, real client data, filterable by area/segment/experience level | Polished |
| `discountdirect/` | Seller–buyer messaging app concept — communication timeline with personalised offer cards, channel selection (chat/e-mail/mailing), one-product flash campaigns with time/quantity limits, and automated per-buyer offer lists. CSS custom properties are named after GDS 6.5.0 roles for a 1:1 dev handoff (`discountdirect/GDS-TOKEN-MAP.md`) — naming only, no dependency | Interactive prototype |
| `index.html` | The hub page linking every project above | — |
| `public/` | Image assets — currently unreferenced by any page in this repo; worth checking before assuming it's live |

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
