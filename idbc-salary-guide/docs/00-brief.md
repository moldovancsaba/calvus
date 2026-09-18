# IDBC Salary Guide — brief

*For a first reader — client, IDBC staff, a developer picking up the build: what this is,
what is real, where it stands. Written 2026-09-18; the dated trail is the process log in
`README.md` and the change notes in `SOURCES-AND-GAPS.md`.*

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

Seven static pages on GitHub Pages, all reading one JSON built from the client's
workbooks by two converters in `data/`:

| Page | Content | Data |
|---|---|---|
| Piaci trendek (`index.html`) | 4 topics × employee/employer, whole sample, segment filters; 11 area cards | survey: 12 datasets (whole sample + 11 areas), 12 employee and 13 employer questions per set |
| Területi összefoglaló (`terulet/`) | one template, 11 areas by `?terulet=`: summary text, video or key-thought placeholder, that area's results | same, per area |
| Bérek (`berezes/`) | 13 areas: TOP3 point-line chart with LinkedIn market counts, full table with levels | bértábla: 432 rows, 39 TOP3 rows; Talent Insight counts 37/39 |
| SAP (`sap/`) | client's trend copy, 20-item product catalogue, TOP3 chart, table | bértábla SAP rows (12) |
| Expert Pool (`expert-pool/`) | Expert Community copy, join and contact forms (inert), 15 position tiles with IDBC and market counts | pool sheet + Talent Insight 13/15 |
| Esettanulmányok (`esettanulmanyok/`) | two case studies as articles, video placeholders | client copy |
| Regisztráció (`regisztracio/`) | the client's field list, inert | — |

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
| Phase | fine-tuning with the client — 55 commits since 2026-07-30; three client feedback rounds in September |
| Customer side | data provenance and gaps documented from day one; presentation (`bemutato.html`), decision register, gate and client-asks list written 2026-09-18 |
| Technical side | proposed — SSOT, architecture with a **PROPOSED** stack, technical design, implementation plan, token map (`10`–`14`), 2026-09-18; the client's own spec assumed WordPress + Google Sheets API + a paywall and that assumption is examined there |
| Open with the client | `08-client-asks.md` |
