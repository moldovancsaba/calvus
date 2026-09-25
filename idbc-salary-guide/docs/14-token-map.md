# IDBC Salary Guide — token and component map

*How the prototype's tokens and components become one stylesheet and a set of templates in
the production build (ADR-6). Written 2026-09-18; since 2026-09-25 the prototype itself
defines its tokens once (`assets/site.css`, idbc.hu's values).*

## 1. Tokens

Since 2026-09-25 (D39) the tokens are defined once, in `assets/site.css`, with idbc.hu's
values; the table in `05-design.md` lists them. Production maps them onto the host theme:

| Token (prototype) | Value | Production |
|---|---|---|
| `--dark` | `#121c1b` | idbc.hu's own dark — already the same value |
| `--dark-2` | `#14201f` | idbc.hu's section dark |
| `--ground` | `#f5f9f2` + noise | idbc.hu's ground (its noise texture image) |
| `--green` / `--green-strong` | `#a4dd8c` / `#93d17a` | idbc.hu's green |
| `--green-mid`, `--green-teal`, `--green-pale` | `#35715c`, `#4ca283`, `#daf1d0` | idbc.hu's palette |
| `--font` | Outfit (stand-in) | Gilroy, which idbc.hu already serves |
| type scale, radii, buttons, container | as in `05-design.md` | idbc.hu's theme variables (`--title-font-size` etc.) |
| chart ramp | `#a4dd8c` → `#4ca283` → `#35715c` | in `chart.css`, unchanged |

## 2. Components → templates and parts

| Prototype | Production |
|---|---|
| `.sg-header` / `.sg-nav` (idbc.hu's header) | idbc.hu's own header part; the guide's links as a menu |
| `.sg-hero` + `.sg-hero-card`; `.sg-hero--plain` | idbc.hu's hero and "hero type 2" patterns |
| `.sg-footer` (idbc.hu's footer) | idbc.hu's own footer part |
| `.intro-block` | `pattern/sg-intro` |
| `.top-cards` / `.range-card` | `pattern/sg-summary-cards` (rendered from data) |
| `.top3-chart-card` + `top3-chart.js` | `block/sg-top3-chart` (client-side renderer, unchanged JS) |
| `.salary-table` (Bérek grouped; SAP flat) + card mode | `block/sg-salary-table` (server-rendered markup, same classes) |
| `.expert-card` tiles | `block/sg-pool-tiles` |
| `.audience-card`, `.proto-form` | `pattern/sg-audience` + the form plugin's fields with the token classes |
| `.area-summary`, `.area-media` (video / highlight) | `pattern/sg-area-summary` with media meta |
| `.article`, `.trend-title`, `.trend-copy` | `pattern/sg-article` |
| `.is-unavailable` | removed in production where the control works (Excel, logout, forms); kept for EN until ADR-7 flips |
| `.talent-pill`, `.talent-note` | in `chart.css`, unchanged |

## 3. What is not tokenised

Photographs (Unsplash placeholders in the hero today — to be replaced by IDBC's own,
`08-client-asks.md` should gain this if the client agrees), the client's infographic
(retired), the SVG chart internals (sized in viewBox units, not tokens).

## 4. Verification

SG-010: a script reads `assets/site.css`'s `:root` and the production stylesheet
and fails on any differing value; the seven prototype pages and their production
counterparts are compared by computed style on the shared components.
