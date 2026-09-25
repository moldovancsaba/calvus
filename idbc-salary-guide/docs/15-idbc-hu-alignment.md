# IDBC Salary Guide — aligning the prototype with idbc.hu

*What idbc.hu looks like, measured, next to what the prototype does today; what has to
change, in which order, and what needs a decision first. Written 2026-09-25 from the live
site (home, `/go/sap/`, `/talent/`, a blog article, `/kapcsolat/`) at 1440 and 375 px.
Phase 0 applied the same day (D38); phases 1–6 delivered the same day on the §5
recommendations (D39) — see §10.*

## 1. Why

The guide is meant to live inside idbc.hu (ADR-1, `11-architecture.md`); the client's own
home mockup already places it in that template. The prototype's look came from the client's
2026-07/08 HTML demos (`05-design.md`), which share idbc.hu's colours but not its type, scale
or components. Aligning now means the client reviews the guide as it will actually look, and
the production build (ADR-6: transcribe the prototype) inherits idbc.hu's design instead of a
second one.

## 2. idbc.hu, measured

WordPress theme on Bootstrap 5 with its own stylesheet (`/includes/css/style.css`), Gilroy
self-hosted in five weights (Light–Heavy), a light noise-texture page ground, dark sections.
Every page is built from a small set of section templates:

| Template | Where | What it is |
|---|---|---|
| Header | every page | floating dark bar (`#121c1b`), 1312 px wide, 79 px tall, bottom corners 32 px; SVG logo "IDBC group" (100 px); EN/HU pills (active green); 5 links 15/600 in `#f5f9f2`; two 40 px buttons in a green-outlined group ("Ajánlatkérés", "CV feltöltés"); sticky; hamburger (green) below 1200 px |
| Hero | service pages | dark band (`#14201f`), photo(s) with 32 px corners, centred dark card (top corners 32 px) with `h1` 62/48 bold white, one line 20 px, two 56 px buttons (green filled + green outline) |
| Hero type 2 | articles, contact | light green band, `h1` 40/48, author chip |
| Section title | every section | `h1.section-title` 56/64 bold `#121c1b`, left or centred; no eyebrow |
| Numbers | home | four `#35715c` cards, 32 px corners, figure 56/64 weight 800 in `#daf1d0`, uppercase label |
| Service rows | home, GO | green (`#a4dd8c`) cards, photo left, title 24/32 bold, arrow button in a dark square |
| Callout | home | light green (`#daf1d0`) panel, 24–32 px corners, black button |
| Accordions | Talent, Projects, GO | expandable rows |
| Dark card carousel | home, GO, Talent | `#14201f` band, light cards (`#f5f9f2`, 24 px corners), author chip, tags |
| Partner quotes | most pages | light cards, 40 px corners, green glow `0 0 34px #65b1a1` |
| Contact form | bottom of every page | dark panel, 56 px corners, green glow `0 32px 128px #a4dd8c`; green title; segmented toggle (Állást keresek / Cégként…); white inner card; underline inputs (2 px bottom border) |
| Article body | blog | 840 px measure, text 18/27, `h2` 32/48 |
| Footer | every page | `#121c1b`, top corners 56 px, logo, "Your professional boost!", phone, e-mail, address, 5 social icons, four link columns, bottom bar (© line, Panaszbejelentő, Adatkezelési tájékoztató); text `#a2a9a8` |

Buttons: 8 px corners, weight 600; 40 px (header), 56 px (default, 20 px text), 64 px
(`__lg`); variants green, green-outline, black (with a soft light glow), black-outline.
Container 1280 px; section padding 48 px desktop / 32 px phone; phone side padding 16 px.
Type scale (theme variables): title 56/64 → 28/36 on phones, `h1` 40/48, `h2` 32/48, `h3`
24/32, `h5` 20/26, body 16/28.

## 3. Side by side

| | idbc.hu | Prototype today | Change |
|---|---|---|---|
| Dark | `#121c1b`, sections `#14201f` | `#132323`, footer `#0b1818` | take idbc.hu's |
| Green | `#a4dd8c` | `#a5df8f` | take idbc.hu's |
| Mid / pale greens | `#35715c`, `#4ca283`, `#daf1d0` | chart ramp `#55aa8b`, `#245d54` | chart ramp to idbc.hu greens (check contrast) |
| Ground | light + noise texture | `#eef5ec` + dot pattern | light ground + texture |
| Typeface | Gilroy 400–800 | Inter 700–900 | Gilroy if licensed (§5), else the closest free face |
| Section title | 56/64 bold, no eyebrow | eyebrow (12 px uppercase) + `h2` 52/51 | drop eyebrows or restyle; 56/64 titles |
| Header | 79 px, 1312 wide, links 15/600, 40 px buttons, SVG logo | 42 px, 980 wide, links 11/800, 25 px buttons, text logo | rebuild to idbc.hu's header |
| Hero | photo band + centred card, `h1` 62, two 56 px buttons | photo + card bottom-left, `h1` 42 | idbc.hu hero (service pages) or type 2 (articles) |
| Cards | 24 / 32 / 40 px corners, flat or glow | 14 / 18 / 28 px, drop shadow | idbc.hu radii and treatments |
| Buttons | 8 px, 40/56/64 px, weight 600, glow | 8–10 px, 25–44 px, weight 900, 10–13 px text | idbc.hu button set |
| Selects / filters | (none on idbc.hu) | green filled selects | keep, restyled with idbc.hu tokens and 56 px height |
| Container | 1280 | 1210 | 1280 |
| Forms | underline inputs, segmented toggle, glowing dark panel | boxed inputs | idbc.hu form |
| Footer | full idbc.hu footer | short guide footer | idbc.hu footer |

The data components have no idbc.hu equivalent and stay as the client designed them —
TOP3 chart, salary tables, Expert Pool tiles, survey charts and filters — restyled with the
tokens only (typeface, colours, radii); their behaviour and figures do not change.

## 4. Facts that differ today (content, not design)

The prototype's footer disagrees with idbc.hu:

| | idbc.hu | Prototype (IDBCSYNC row) |
|---|---|---|
| Phone | +36 30 479 **8**090 | was +36 30 479 **0**090 (`SHARED-FOOTER-36-30-479-0090`) — corrected in the sheet, Phase 0 |
| Address | Duna Tower Irodaház A torony **13.** emelet | was … **5.** emelet (`SHARED-FOOTER-CIM-DUNA-TOWER-IRODAHAZ`) — corrected in the sheet, Phase 0 |
| Legal links | Panaszbejelentő → FaceUp page; Adatkezelési tájékoztató → `/adatvedelem/` | "Panaszszabályzat" and "Adatkezelési tájékoztató", both `href="#"` |
| Social | LinkedIn, Facebook, Instagram, TikTok, YouTube | none |

These are text rows in IDBCSYNC (fixed in the sheet, not the pages); the two link targets
are page markup today and would become sheet rows with the footer rebuild.

## 5. Decisions needed before building

| # | Decision | Options | Recommendation |
|---|---|---|---|
| A-1 | Typeface | (a) IDBC confirms its Gilroy web licence covers the prototype's host, and the studio self-hosts the files; (b) a free near-match (Urbanist / Outfit) until production, where the guide sits on idbc.hu and inherits Gilroy | ask IDBC; build with (b) until they answer — idbc.hu serves the font without cross-origin headers, so it cannot be borrowed from their server |
| A-2 | Which design wins where idbc.hu and the client's own demos differ (hero card position, eyebrows, green summary cards, compact header) | idbc.hu / demos, per component | idbc.hu for the shell and page chrome; the demos for the data components — confirm with the client, since they reviewed the current pages three times |
| A-3 | Header content | (a) idbc.hu's own navigation (Szolgáltatások, Karrier…) with the guide as a sub-navigation; (b) idbc.hu's header shape with the guide's five links | (b) for the prototype, (a) is production's job; logo = idbc.hu's SVG, linking to idbc.hu |
| A-4 | Footer content | (a) idbc.hu's full footer (links to idbc.hu pages, social); (b) idbc.hu's shape with guide links | (a) — it is what a reader will see on idbc.hu |
| A-5 | Photography | stock (today) / idbc.hu's own photos (with permission) | idbc.hu's own (already client ask C-6) |
| A-6 | Correct the footer facts in §4 now | yes / wait for the rebuild | yes — two sheet edits, no design change |

## 6. Plan

Each phase ends with the gate (`check.py`), a measured pass at 390 and 1440, no console
errors, the IDBCSYNC check (§7) and a dated entry in `SOURCES-AND-GAPS.md`.

| Phase | Work | Done when |
|---|---|---|
| **0 — facts** (done 2026-09-25) | §4 phone and floor fixed in IDBCSYNC (A-6); the phone is typed `'+36 …` — without the apostrophe Sheets reads it as a formula and exports `#ERROR!`, which the sync now refuses | the live footer matches idbc.hu |
| **1 — one stylesheet** | the `:root` block every page repeats today becomes `assets/site.css` with idbc.hu's tokens (colours, type scale, radii, spacing, container 1280, buttons, ground texture) and the chosen face (A-1); pages keep only their page-specific rules | every page loads one token file; a script compares every page's computed tokens with idbc.hu's measured values (the SG-010 check from `14-token-map.md`, brought forward) |
| **2 — shell** | header and footer rebuilt on idbc.hu's pattern on all eight pages (A-3, A-4): SVG logo, EN/HU pills, 15 px links, 40 px button group, sticky bar, green hamburger; full footer with social links and the real legal targets | header and footer measure within 2 px of idbc.hu at 1440 and 375 |
| **3 — page chrome** | heroes (service hero on Kezdőoldal, Bérek, SAP, Expert Pool; type 2 on Esettanulmányok, Regisztráció, Kapcsolat, area pages); section titles 56/64; the home figures ("11+ év", "11 terület"…) as idbc.hu's numbers cards; buttons; callouts; the contact and registration forms as idbc.hu's form; article pages at 840 px, 18/27 | each page's chrome is idbc.hu's template, side-by-side screenshots in the log |
| **4 — data components** | charts, tables, filters, tiles restyled with the tokens only; chart ramp moved to idbc.hu greens if contrast holds | every chart and table renders the same figures as before (the render comparison used for D37), only style differs |
| **5 — phone** | idbc.hu's phone scale (titles 28/36, 16 px sides, 32 px sections), menu, 44 px tap floor kept | 375 px pass on every page, no horizontal scroll |
| **6 — record** | `05-design.md`, `14-token-map.md`, decisions, bemutató updated | docs match the pages |

## 7. Keeping IDBCSYNC intact

Every visible text is a sheet row now (D37), so the rebuild follows three rules:

1. **Kept texts keep their ids** — moving an element keeps its `data-sync` attribute, so
   whatever the client has edited survives.
2. **New texts get rows before the pages go live.** A page that references an id the sheet
   lacks stops the sync, so new rows (header links, footer columns, social labels, hero
   buttons) are added to the sheet first — the converter only warns about rows no page uses
   yet — then the pages are pushed.
3. **Read the sheet before touching it.** The client edits it every day now; any import
   starts from a fresh export, never from the studio's copy.

## 8. Risks

- **Licence** — Gilroy is a commercial face; nothing ships until A-1 is answered.
- **Client-approved layouts** — the current pages were reviewed and corrected three times;
  A-2 has to be the client's call, not the studio's.
- **Cached assets** — the shared stylesheet and chart script carry `?v=` and are bumped on
  every change.
- **A moving source** — IDBCSYNC changes under the work; §7 keeps it safe.

## 9. Order and size

Phase 0 is minutes. Phases 1–2 are the foundation and change every page at once; 3 is page by
page; 4 and 5 are small once 1 exists. Each phase can go live on its own.

## 10. Delivered (2026-09-25, D39)

The owner asked to deliver the plan; the §5 decisions were taken as recommended:

| # | Taken |
|---|---|
| A-1 | Outfit (Google Fonts) stands in for Gilroy — the closest measured free face (1.7 % mean width difference over five samples) with a large x-height like Gilroy's; one line in `assets/site.css` swaps it for Gilroy once IDBC confirms the licence |
| A-2 | idbc.hu for the frame (header, footer, heroes, titles, buttons, cards, forms); the client's demos for the data components — **to confirm with the client** |
| A-3 | idbc.hu's header with the guide's five links and a "Salary Guide" link next to idbc.hu's logo |
| A-4 | idbc.hu's full footer, plus the guide's own column |
| A-5 | stock photos kept until IDBC supplies its own (C-6) |

What changed: `assets/site.css` (tokens, type, header, footer, heroes, buttons, cards,
forms, page copy) and `assets/site.js` (the menu) are shared by all eight pages; each page's
own style lost its duplicated shell rules (about half its CSS); the chart and pool colours
moved to idbc.hu's greens (`top3-chart.js?v=10`, `chart.css?v=8`); the documentation and the
bemutató moved to the same tokens and face. 29 new footer rows went into IDBCSYNC before the
pages (the sync kept running throughout).

Measured: every chart, table and tile shows the same text and figures as before in all
1,142 rendered states (every home filter combination, all 11 area pages with every topic
and segment, Bérek for every area, SAP, Expert Pool); no horizontal scroll at 375 or 1440 on
any page; tap targets ≥ 44 px on phones; the menu opens and closes with the right
`aria-expanded`; no console errors; `check.py` clean; `idbcsync.py --check` against the live
sheet changes nothing.

