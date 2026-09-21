# Design system — as built

*Tokens and components as implemented in `assets/tokens.css` and `assets/site.css`. Every
value is a direct visual read of the Figma file (no Dev Mode access — `00-brief.md`), refined
against the file itself on 2026-09-21 (not just the earlier screenshots). Confirm against
Figma Dev Mode or an exact export before this is treated as final — see the open item in
`03-sources.md` #2.*

## Colour

| Token | Value | Used for |
|---|---|---|
| `--nsz-ink` | `#111111` | headlines, body text, the logo mark |
| `--nsz-text` | `#222222` | body copy |
| `--nsz-muted` | `#6b6b6b` | bylines, reading time, captions |
| `--nsz-line` | `#dcdcdc` | hairlines between stories, borders |
| `--nsz-ground` | `#ffffff` | page background |
| `--nsz-panel` | `#f4f4f4` | ad slots, footer, paywall box |
| `--nsz-blue` | `#1d4fd7` | logo, nav active state, links, pill borders, subscribe/registration controls |
| `--nsz-lime` | `#c8f000` | the one warm accent — "Regisztrálok", the ELEMZÉS/VÉLEMÉNY tag background |

One blue, one lime — confirmed directly on screen (D3 in `01-research.md` §0 also flags this
as the pattern every measured competitor follows: a single brand accent plus a warm highlight,
not a rainbow of section colours). Deviates from `01-research.md`'s "colour by editorial section" proposal
(P3) — that stays a proposal for the design-system gate proper, not applied here since the
Figma itself uses one blue throughout.

## Type

| Token | Stack | Used for |
|---|---|---|
| `--nsz-serif` | Source Serif 4, Noto Serif, Georgia, serif | headlines, deks, article body — confirmed serif on screen at 200% zoom on the Cikkoldal frame |
| `--nsz-sans` | Inter, system-ui, sans-serif | the logo wordmark, navigation, pills, meta text, buttons |

The masthead wordmark ("NÉPSZABADSÁG") is bold sans-serif caps, not serif — confirmed directly
(zoomed to 200%), correcting an assumption a purely-serif brand might invite.

## Components (as read from the Figma, built here)

- **Header**: logo mark (34×34, blue rounded square, "N") + wordmark (sans, bold, hidden under
  780px per the mobile pattern observed) · main nav (desktop) / hamburger + slide-down list
  (mobile) · search icon (inert) · a blue pill "Előfizetés" button, always visible.
- **Article pills row**: outlined blue pills under the header on article/rovat pages
  ("Az újraindítás", "A szerkesztőség", "Tíz év után" on the Cikkoldal).
- **Card row** (photo left, text right) and **photo card** (photo above, text below) — the two
  teaser patterns used throughout Címlap, Rovatfront and Népszava.
- **Tag**: lime background, dark text, uppercase, small — ELEMZÉS, VÉLEMÉNY.
- **Paywall box**: panel background, blue top border, heading, three bullet teasers, two
  buttons (filled blue "Ingyenes regisztráció", outlined blue "Print+online előfizetés"), a
  login link, a note line — matches the Figma's Cikkoldal frame component for component.
- **Registration band**: full-width blue bar, white text, a lime pill button — appears at the
  foot of every page, matching the Figma's "blue band" on every frame.
- **Footer**: four columns (Rovatok, Almárka, A lapról, Jogi és egyéb) + a copyright line.
- **Countdown**: four number tiles (nap/óra/perc/mp), live via `setInterval`, targeting the
  memo's 2026-10-08 08:00 launch instant.

## What is not yet confirmed

Exact pixel values (type scale, spacing unit, precise hex) still rest on visual estimation, not
Dev Mode inspection or an exported spec — the same limitation the handover recorded on
2026-09-21 and still open. Nothing here should be read as a Figma variable.
