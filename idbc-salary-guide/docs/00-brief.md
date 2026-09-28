# IDBC Salary Guide — brief

*For a first reader — client, IDBC staff, a developer picking up the build: what this is,
what is real, where it stands. Written 2026-09-18, updated 2026-09-28; the dated trail is the
process log in `README.md` and the change notes in `SOURCES-AND-GAPS.md`.*

## The client

IDBC Group — a Hungarian recruitment agency (SAP, IT and corporate functions;
idbc.hu, WordPress with WPML, HU and EN). The product is the **Talent Market & Salary
Guide 2026**: a gated, data-driven report that IDBC publishes inside its own site —
market trends from its 2026 survey, salary bands per area, an SAP guide, the Expert
Community, case studies — as a lead and positioning tool.

## The problem the client brought

Two specs (a functional one and a landing-page one), three HTML mockups and two PDF
mockups described an eight-page gated site fed from Google Sheets. What the survey and
the salary table could actually support was narrower than the specs assumed. The
prototype's job was to make the real data clickable, show every intended control in
place, and write down each gap between the spec and the data instead of papering over it.

## What the prototype is

Eight static pages on GitHub Pages, in idbc.hu's design (D39). Every value they show comes
from two JSON files, `data/guide-data.json` and `data/areas.json` — the source since D48; the
client's sheet, research workbook and copy feed them (`16-developer-handover.md` §3):

| Page | Content | Data |
|---|---|---|
| Piaci trendek (`index.html`) | 4 topics × employee/employer, whole sample, segment filters; 11 area cards | survey: 12 datasets (whole sample + 11 areas); 12 employee and 13 employer questions in the general set, 16 and 13 in the IT + Contracting set |
| Területi összefoglaló (`terulet/`) | one template, 11 areas by `?terulet=`: summary text, video or key-thought placeholder, that area's results | same, per area |
| Bérek (`berezes/`) | 12 areas: TOP3 point-line chart with LinkedIn market counts, full table with levels | bértábla: 432 rows in 13 areas (SAP on its own page), 39 TOP3 rows, Talent Insight counts 39/39 |
| SAP (`sap/`) | client's trend copy, product catalogue (5 categories, 25 items), TOP3 chart, table | bértábla SAP rows (12) |
| Expert Pool (`expert-pool/`) | Expert Community copy, join and contact forms (inert), 29 position tiles (IT 15, Non-IT 14) with the IDBC bar and market counts | pool sheet, Talent Insight 29/29; Qualified Person waits for its count |
| Esettanulmányok (`esettanulmanyok/`) | two case studies as articles, video placeholders | client copy |
| Regisztráció (`regisztracio/`) | the client's field list, inert | — |
| Kapcsolat (`kapcsolat/`) | the Ajánlatkérés page the header button opens (D30), form inert | — |

Live: <https://moldovancsaba.github.io/calvus/idbc-salary-guide/>

## What is real and what is not

- **Real:** every figure — survey percentages and weighted averages, salary bands, TOP3
  positions, IDBC pool counts, LinkedIn Talent Insight counts, the SAP catalogue, the case
  studies, the Expert Community copy, area summaries — comes from a named client file
  (`SOURCES-AND-GAPS.md`, source table).
- **Inert, visibly:** Excel download, EN switch, Kijelentkezés, the registration form, the
  join and contact forms — shown in place with an "unavailable" treatment and a title
  saying why. No backend exists on static hosting.
- **Placeholders, at the client's request:** the video slots (7 areas, 2 case studies) and
  the key-thought boxes (4 areas); the client uploads the finals.
- **Not built:** the home page (copy received, structure demo pending), the paywall.
- **A labelling caveat the client should know:** the salary chart's "companies offer / candidates expect" ends are the one range in the bértábla, named per the client's mockup — not two surveyed populations (gap 6 in `SOURCES-AND-GAPS.md`).

## Where it stands

| | |
|---|---|
| Phase | **ready for the developers (2026-09-28)** — every client correction up to 2026-09-25 is in, on idbc.hu's design; six client feedback rounds in September |
| Customer side | data provenance and gaps documented from day one; presentation (`bemutato.html`), decision register, gate and client-asks list written 2026-09-18 |
| Technical side | proposed — SSOT, architecture with a **PROPOSED** stack, technical design, implementation plan, token map (`10`–`14`), 2026-09-18; the client's own spec assumed WordPress + Google Sheets API + a paywall and that assumption is examined there |
| Handover | `16-developer-handover.md`: running it, where every value lives, the interactive parts, the path to production |
| Open with the client | content still to come and the decisions before publication — `19-implementation-prerequisites.md`; the register of asks — `08-client-asks.md` |
