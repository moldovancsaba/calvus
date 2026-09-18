# IDBC Salary Guide — token and component map

*How the prototype's tokens and components become one stylesheet and a set of templates in
the production build (ADR-6). Today every page repeats the same `:root` block; production
defines it once. Written 2026-09-18.*

## 1. Tokens

| Token | Value | Role | Production |
|---|---|---|---|
| `--dark` | `#132323` | navbar, hero card, dark text on green | `--sg-dark` |
| `--dark-2` | `#0b1818` | footer | `--sg-dark-2` |
| `--light-bg` | `#eef5ec` | page ground (+ dot pattern) | `--sg-ground` |
| `--green` | `#a5df8f` | primary button, selects, summary cards, pill, highlight box | `--sg-green` |
| `--green-strong` | `#8fd474` | hover | `--sg-green-strong` |
| `--text` | `#101818` | body | `--sg-text` |
| `--muted` | `rgba(16,24,24,.66)` | secondary | `--sg-muted` |
| `--line` | `rgba(19,35,35,.18)` | borders | `--sg-line` |
| `--container` | `1210px` | content width | `--sg-container` |
| `--radius-large` / `--radius-medium` | `28px` / `14px` | hero / cards | `--sg-radius-l/-m` |
| `--shadow-soft` | `0 16px 40px rgba(0,0,0,.12)` | cards | `--sg-shadow` |
| chart ramp | `#a5df8f` → `#55aa8b` → `#245d54` | offered → IDBC → expected; pool bars | in `chart.css`, unchanged |
| type | Inter, Montserrat, Segoe UI, Arial; weights 700–900 | | idbc.hu's own font stack if it has Inter; otherwise self-host Inter |
| breakpoints | 980 (menu), 900 (grids), 700 (chart compact), 600 container (table cards) | | keep |

If idbc.hu's theme already defines a palette, the `--sg-*` names alias it where the
values match (the dark green and the light ground are IDBC's brand) — mapping to be
confirmed against the host theme in SG-010.

## 2. Components → templates and parts

| Prototype | Production |
|---|---|
| `.navbar` + `.menu-toggle` + `.nav-links` + `.nav-actions` | `parts/guide-header.html`; menu from one WordPress menu |
| `.hero` + `.hero-card` | `pattern/sg-hero` (image, eyebrow, `h1`, sentence) |
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

SG-010: a script reads every prototype page's `:root` and the production stylesheet
and fails on any differing value; the seven prototype pages and their production
counterparts are compared by computed style on the shared components.
