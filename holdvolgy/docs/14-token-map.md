# Holdvölgy 2026 — token and component map

*How `assets/tokens.css` and the prototype's components become a WordPress block theme
(`theme.json` + a base stylesheet), per ADR-2. The token file is the source; this table is
the contract. Every value below is copied from `tokens.css` as of 2026-09-18 — if the two
ever differ, the CSS wins and this file is wrong.*

## 1. Colour

| Token | Value | `theme.json` `settings.color.palette` slug | Role |
|---|---|---|---|
| `--hv-ground` | `#FAFAFA` | `ground` | page background (D2: light ground) |
| `--hv-card` | `#FFFFFF` | `card` | card and panel surface |
| `--hv-band` | `#F4F4F4` | `band` | full-width tinted band (wine rail) |
| `--hv-line` | `#D9D9D9` | `line` | rules, borders |
| `--hv-line-soft` | `#EAEAE6` | `line-soft` | hairlines inside cards |
| `--hv-ink` | `#1D1D1B` | `ink` | headings, wordmark, primary button |
| `--hv-text` | `#4A4744` | `text` | body copy |
| `--hv-muted` | `#666666` | `muted` | secondary copy (the live site's text colour) |
| `--hv-grey` | `#9B9796` | `grey` | labels, disabled |
| `--hv-accent` | `#B8A689` | `accent` | the only accent — greige, from the live kit |
| `--hv-accent-2` | `#BAA793` | `accent-2` | accent on tinted grounds |
| `--hv-accent-deep` | `#8B705B` | `accent-deep` | hover / pressed |

No gradients, no second accent, no dark mode (the docs' own dark-mode override was
removed for the same reason — process log 2026-09-17). `theme.json` sets
`settings.color.custom: false` so editors cannot introduce colours.

## 2. Type

| Token | Value | `theme.json` |
|---|---|---|
| `--hv-display` | `"Bodoni Moda", Didot, "Bodoni 72", "Bodoni MT", serif` | `fontFamilies[display]`, self-hosted WOFF2 (HV-015), weights 400/500, optical size axis 6–96 |
| `--hv-sans` | `"Archivo", "Helvetica Neue", Arial, sans-serif` | `fontFamilies[sans]`, WOFF2, weights 400/500/600 |
| `--hv-sans-width` | `112.5%` | `font-stretch` on body — Archivo's `wdth` axis standing in for Akzidenz BQ Extended (D3) |
| `--hv-t-hero` | `clamp(34px, 4.6vw, 64px)` | `fontSizes[hero]` (fluid) |
| `--hv-t-h2` | `clamp(26px, 2.9vw, 40px)` | `fontSizes[h2]` |
| `--hv-t-h3` | `clamp(20px, 2vw, 28px)` | `fontSizes[h3]` |
| `--hv-t-body` | `15px` | `fontSizes[body]` |
| `--hv-t-label` | `12px` | `fontSizes[label]` |
| `--hv-track-label` | `.14em` | letter-spacing on eyebrows/labels |

Roles: display face on `h1`/`h2` and the wordmark only; sans everywhere else (benchmark
finding 1.2). Editors get exactly these five sizes (`settings.typography.customFontSize:
false`).

## 3. Spacing, grid, corners, targets

| Token | Value | `theme.json` / CSS |
|---|---|---|
| `--hv-radius` | `2px` | `border-radius` on cards, buttons, fields — square-cornered brand |
| `--hv-tap` | `44px` | min tap size on every interactive element |
| `--hv-gutter` | `24px` | grid gap |
| `--hv-margin-desktop` | `80px` | page margin ≥ 1024 |
| `--hv-margin-phone` | `16px` | page margin < 768 |
| `--hv-content-max` | `1280px` | `settings.layout.contentSize` / `wideSize` |
| `--hv-measure` | `62ch` | max line length for running text |
| Breakpoints | phone ≤ 767 · tablet 768–1023 · desktop ≥ 1024 | `05-layout-specs.md`; the same three in the theme CSS |

## 4. Components → theme parts / blocks

| Prototype component (class) | Where it lives in the theme | Notes |
|---|---|---|
| `.wrap` | layout root (`contentSize`) | |
| `.btn`, `.btn-2`, `.btn-3` (+ `.short`/`.long` label pairs) | `core/button` styles `primary` / `secondary` / `text` | the short/long pair is the responsive label trick — keep as two spans |
| `.card` (three home cards) | block pattern `hv/card` | image, eyebrow, title, text, CTA pair (R1: hospitality first) |
| `.bottle` (+ `.price`) | block pattern `hv/bottle` fed by a product | one product per bottle; price from WooCommerce |
| `.rail` | `hv/wine-rail` pattern = horizontal list of `hv/bottle` | swipeable on phone |
| `.rock`, dűlő row | `hv/dulo-row` pattern | seven rows, two rock photos pending (HV-081) |
| `.hero` | `hv/hero` pattern | photograph + one sentence |
| `.top`, `.wordmark`, `.lang` (desktop nav) | `parts/header.html` + `core/navigation` | single menu (R11) |
| `.bar`, `.sheet` (phone nav) | `parts/bottom-bar.html` | bottom action bar + sheet, < 1024 |
| `.age` (`<dialog>`) | `parts/age-gate.html` | R8 |
| `.proto` (banner) | **not carried** — prototype-only | the banner is removed at cutover; the gate's "current banner" check does not apply to production |
| form field (design-system §9) | form plugin field styles | tokens applied via the base stylesheet |
| tiers (`.tiers`, `.tier`) | `hv/club-tiers` pattern reading reward-points settings | `12` §6 |
| tickets | `hv/ticket` pattern | four instances on Látogatás |
| product tabs (Kóstolási jegyzet · Az évjárat · Adatlap) | `single-product.html` sections from meta | `12` §3 |

Class names are namespaced as D18 requires; in the theme they become `hv-` prefixed
block styles so a plugin's `.card` can never collide.

## 5. What is deliberately not tokenised

Photographs (they are the colour of the site — benchmark finding 1.1), the map, the
bottle renders. Hard-coded values in the prototype that are not in `tokens.css` are
layout-local (a section's padding, a rail's item width) and move into the pattern's CSS,
not into `theme.json`.

## 6. Verification

HV-004 ships a script that reads `tokens.css` and `theme.json` and fails if any value in
§1–§3 differs. The design-system page (`design-system.html`) rendered by the theme must
look identical to the prototype's — that comparison is M1's exit criterion.
