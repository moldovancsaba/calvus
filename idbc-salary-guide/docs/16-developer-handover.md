# IDBC Salary Guide — developer handover

*For a developer who takes the prototype into the live environment. What the prototype is made
of, where every value lives, how the three interactive parts — survey, salary, Expert Pool —
work, and how they move to production. The target system is designed in `11-architecture.md`
and `12-technical-design.md` (PROPOSED); this is the practical path to it. Written 2026-09-25,
rewritten 2026-09-28 for the data setup the owner chose (D47, D48): **the JSON files are the
source.***

## 1. What you get

| Piece | Where | Role |
|---|---|---|
| Live prototype | <https://moldovancsaba.github.io/calvus/idbc-salary-guide/> | the acceptance reference: production transcribes it, it does not redesign it (ADR-6); every client correction up to 2026-09-25 is in it |
| Repository | <https://github.com/moldovancsaba/calvus>, folder `idbc-salary-guide/` (public) | everything below |
| Pages | `index.html` (Piaci trendek), `terulet/index.html` (one template for all 11 areas), `berezes/`, `sap/`, `expert-pool/`, `esettanulmanyok/`, `regisztracio/`, `kapcsolat/` | static HTML, no build step, no framework, no dependency |
| Shared assets | `assets/site.css` (idbc.hu tokens, header, footer, heroes, buttons, cards, forms), `assets/site.js` (menu), `assets/chart.css` (chart, pill, tooltip), `assets/top3-chart.js` (TOP3 chart + tooltip, `window.IDBCChart`) | loaded by every page; each page's own `<style>` holds only its own rules |
| **Data** | `data/guide-data.json` (survey, salary, Expert Pool, SAP catalogue; 1,1 MB) and `data/areas.json` (the 11 areas) | **the source of every value the pages show** — the pages read nothing else |
| Data tools | `data/build-salary-data.py`, `data/build-guide-data.py`, `data/survey_edits.py`, `.github/workflows/idbc-sync-bertabla.yml` | refresh parts of the JSON from their original sources (§3) |
| Documentation | this folder | decisions `04`, data model `10`, architecture `11`, design `12`, plan `13`, tokens `14` |

## 2. Run it locally

The pages load their JSON with `fetch`, so they need a web server (a `file://` URL shows empty
charts).

```
git clone https://github.com/moldovancsaba/calvus.git
cd calvus
python3 -m http.server 8000        # then open http://localhost:8000/idbc-salary-guide/

# the gate: read the exit code, 0 = clean
python3 check.py
```

## 3. Where every value lives

### 3.1 The map

| What the site shows | Lives in | Comes from | To change it |
|---|---|---|---|
| Salary rows (Bérek, SAP): position, level, TOP3 flag, min / IDBC / max, benefits, LinkedIn count | `guide-data.json` → `salary.webBertabla` | Google Sheet `IDBC_bertabla`, tab `WEB_BERTABLA_IMPORT` | edit the sheet tab, then run the sync (§3.2) — an edit made only in the JSON is overwritten by the next sync |
| Expert Pool tiles: industry, position, count, LinkedIn count | `guide-data.json` → `salary.expertPool` | the same sheet, tab `EXPERT_POOL_IMPORT` | the same as above |
| Survey figures, answer labels, question texts | `guide-data.json` → `datasets` | the client's research workbook *Salary Guide- kutatási eredmények-final.xlsx* (final; not in the repository) | edit the JSON (the workbook is final and is not re-imported) |
| Survey topics and which question shows where | `guide-data.json` → `topics` | the workbook's topic sheet + `data/survey_edits.py` (the client's later additions, D40) | add the change to `survey_edits.py` and run it, so a rebuild keeps it |
| Piaci trendek dataset names and order | `guide-data.json` → `datasets[…].label` and key order | `data/survey_edits.py`, from `areas.json` (the client's names, D31) | change the area's name in `areas.json`, run `survey_edits.py` |
| Area pages and home tiles: name, summary, video / highlight, question set | `areas.json` | the client's area texts (D13, D20) | edit `areas.json` |
| SAP catalogue: 5 categories, 25 items | `guide-data.json` → `sapProducts` | the client's SAP spec, entered 2026-07 | edit the JSON |
| Every page text: headings, paragraphs, buttons, header, footer, forms | the page's HTML | the client's copy, as last corrected | edit the HTML |
| Bérek area names and order | `data/build-salary-data.py` (`CANONICAL_AREAS`, `AREA_ALIASES`) | the client's Bérek list (D31) | edit the list, run the sync |
| Survey settings: segment orders, the question kept in questionnaire order | page constants in `index.html` and `terulet/index.html` | the questionnaire, the client (D32) | edit both pages |

The pages read the JSON only. The sheet, the workbook and the scripts are upstream tools: nothing
reaches a page unless it is in `guide-data.json` or `areas.json` (or the page's own HTML).

### 3.2 Refreshing salary and Expert Pool from the sheet

```
pip install openpyxl

# download the sheet (the export URL the workflow uses)
curl -sL -o /tmp/IDBC_bertabla.xlsx \
  "https://docs.google.com/spreadsheets/d/1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg/export?format=xlsx"

# rewrite salary.webBertabla and salary.expertPool in guide-data.json; the survey half is kept
python3 idbc-salary-guide/data/build-salary-data.py /tmp/IDBC_bertabla.xlsx
```

The same runs in GitHub: Actions → "IDBC — sync IDBC_bertabla" → Run workflow. It downloads the
sheet, runs the converter and the gate, and commits `guide-data.json` only when something
changed. It does not run on a schedule.

What the converter reads: in `WEB_BERTABLA_IMPORT`, the table under the header row that starts
with `rekord_azonosito` — `terulet`, `tapasztalati_szint`, `pozicio`, `top3`,
`vallalatok_altal_kinalt_huf`, `idbc_javasolt_ber_huf`, `jeloltek_altal_elvart_huf`,
`juttatasi_megjegyzes`, `linkedin_talent_insight`; in `EXPERT_POOL_IMPORT`, `iparag`, `pozicio`,
`darab`, `linkedin_talent_insight`. A `terulet` value it cannot map to a Bérek area stops it. An
Expert Pool row without `darab` is skipped and printed (Qualified Person, today).

### 3.3 Survey edits

`data/survey_edits.py` holds the client's decisions made after the workbook: the three employer
questions added on 2026-09-25 (Home office: the recruiting-impact question; AI, general set: the
budget and the recruiting questions) and the dataset names and order taken from `areas.json`. It
is safe to run any number of times; `build-guide-data.py` runs it too, so a rebuild from the
workbook keeps the edits. It stops if a question has no figures in a dataset.

```
python3 idbc-salary-guide/data/survey_edits.py
```

### 3.4 The JSON, field by field

`guide-data.json`:

| Key | Content | Read by |
|---|---|---|
| `totalKey`, `totalLabel` | `__total__`, *Összesített adatok* — the whole-sample dataset | survey |
| `datasets` | the whole sample + one per area, **keyed by the area's original name** (e.g. `"BSC"`, `"Sales & Marketing"`); each `{label, questionSet, employee: {base, cross}, employer: {base, cross}}` | survey |
| `topics` | `[{topic, questionSets: {"Általános" / "IT + Contracting": {"Munkavállalók": [question texts], "Munkáltatók": [...]}}}]` | survey |
| `salary.webBertabla` | `[{id, kod, terulet, szint, pozicio, top3, min, idbc, max, juttatas, linkedin?}]` — `kod = "SAP"` for the SAP page | Bérek, SAP |
| `salary.expertPool` | `[{iparag, pozicio, darab, linkedin?}]` | Expert Pool |
| `sapProducts` | `[{category, items[]}]` | SAP |
| `generatedFrom`, `siteMap`, `filterDimensions`, `salary.readme`, `salary.talentInsightTop3` | provenance and reference blocks | no page |

`base[question]` is `{kind: "simple", items: [{label, percent, count}]}` or
`{kind: "weighted", scaleMax, items: [{label, value}]}`; `cross[question]` is
`{kind: "matrix-percent", groups: [answers], items: [{label: segment, values: [{group, percent, count}]}]}`.

`areas.json`: `{areas: [{slug, name, dataKey, edition, summary, media}]}` — `slug` is the area
page's `?terulet=` value, `dataKey` the area's dataset key in `guide-data.json`, `edition` its
question set, `media` `video` or `highlight`.

### 3.5 Leftovers, harmless

The pages carry `data-sync` attributes and `/*sync:…*/` comments from a sheet-driven setup that
ran on 2026-09-25 (D37) and is parked (D47); nothing reads them now. The sheet's `IDBCSYNC` tab
(hidden) is a complete copy of every value as of 2026-09-25 and is not used. Both can be removed
in production.

## 4. The interactive parts

### 4.1 Survey — Piaci trendek (home) and the area pages

| | |
|---|---|
| Code | `index.html`, the inline script at the end; `terulet/index.html` has **its own copy** of the same renderer (same rules, shorter code) — merge them into one module in production (R9) |
| Data | `guide-data.json`: `datasets`, `topics`, `totalKey` / `totalLabel`; the area page also loads `areas.json` |
| Controls | home: dataset `#datasetSelect` (Összesített adatok + 11 areas, the client's names in tile order), topic `#topicSelect`, employee segment `#empSegmentSelect` (experience), employer segment `#erSegmentSelect` (company size); panels `#b2cChart` (Munkavállalók), `#b2bChart` (Munkáltatók). Area page: `?terulet=<slug>` picks the area; its dataset is `datasets[area.dataKey]` (an unknown slug → the first area; an area without data → the whole sample); topic and the two segment selects; panels `#employeeChart`, `#employerChart` |

**How a panel is built.** The question list is
`topics[topic].questionSets[dataset.questionSet][side]`. For each question: with *Összesített
adatok* selected the chart comes from `datasets[d][side].base[question]`; with a real segment
from that segment's row in `cross[question]`. Then it is drawn by kind.

**Rules the code applies** (numbers from `10-ssot.md` §6):

- *Összesített adatok* is first and the default; a real segment is offered only if at least one
  question of the topic has a non-zero row for it; a segment dropdown with no real choice is
  hidden (R2). Segment order: the page constants (experience bands, company sizes).
- A question with no data under the chosen segment is left out — the whole-sample figures are
  never shown in its place; if the whole panel empties, one sentence replaces it (R3). On the
  home page a topic with no question for the dataset's question set says so.
- Answers nobody chose (0 %) are dropped.
- Shape: up to 5 single-choice answers → one stacked bar with a legend; multi-choice (the
  percentages add up to more than 110 %) or more than 5 answers → one bar per answer.
- Order: the recruiting-strategy question keeps the questionnaire's order (page constant,
  D32); answer scales that are numeric ranges or home-office days keep scale order; everything
  else is sorted by percentage.
- The two 1–4 scale questions show the weighted average only, with "(súlyozott átlag, 1–4
  skála)" (R4). `count` = percent × respondents, shown in the tooltip as "(n fő)".

**In production.** Keep the renderer client-side (it is filter-driven); load only the page's
dataset instead of the 1,1 MB file (`12` §4).

### 4.2 Salary — Bérek and SAP

| | |
|---|---|
| Code | `berezes/index.html` and `sap/index.html`, inline scripts; `assets/top3-chart.js` (shared chart); `assets/chart.css`; the table's styles in each page's `<style>` |
| Data | `salary.webBertabla`. SAP shows the rows with `kod = "SAP"`, Bérek all the others |
| Controls | Bérek: area `#teruletSelect` (the Bérek areas in the converter's order); chart `#top3Panel`; table `.table-wrap table`. SAP: no filter; catalogue `#productGrid` from `sapProducts` |

**TOP3 chart.** The rows flagged `top3` for the area go to
`IDBCChart.renderTop3Chart(rows, {idPrefix, chartLabel, emptyText})`, which returns SVG markup;
`IDBCChart.attachTooltip(container)` then binds the tooltips (call it after every re-render).
Above 700 px of viewport one wide chart; at 700 px and below one small chart per position with
its own scale in millions (`1,25M`) — the pages re-render when the viewport crosses 700 px.
Each position shows three points: offered (`min`, light green `#a4dd8c`), IDBC recommended
(`idbc`, `#4ca283`), expected (`max`, dark green `#35715c`); amounts close together stack upward
over their own dots (D41). A LinkedIn count adds the pill "n elérhető jelölt*" and the footnote.
An area with no TOP3 row shows a sentence instead of the chart.

**Table.** Every position of the area, TOP3 ones included (R10). One `<tbody>` per position;
its levels sorted Trainee → Junior → Medior → Senior → Team Leader → Manager; Junior, Medior and
Senior carry their experience text. Columns: level, minimum, maximum, other benefits. Below
600 px of **container** width (a CSS container query) the table turns into cards: each position
is a card with its band (min–max) and a toggle, collapsed at first.

**In production.** Render the table on the server with the same markup (`role` attributes,
`data-label` cells, one `<tbody>` per position) so card mode works without JavaScript; keep the
chart client-side with `top3-chart.js` unchanged (`12` §7); generate the Excel from the same
JSON (ADR-5).

### 4.3 Expert Pool

| | |
|---|---|
| Code | `expert-pool/index.html`, inline script; tile styles in the page's `<style>`; the tooltip and the footnote text come from `assets/top3-chart.js` (`attachTooltip`, `TALENT_NOTE`) |
| Data | `salary.expertPool` — a row without `darab` is not in the file |
| Controls | industry `#iparagSelect` (values from the data, IT and Non-IT today); tiles `#expertGrid`; footnote `#talentNote` |

**A tile** shows the industry, the position, the market line "Piacon elérhető szakember: n fő*"
when a LinkedIn count exists, and a bar labelled IDBC Expert Community whose width is `darab`
divided by the largest `darab` of the **whole** pool, so switching industries compares like with
like. The IDBC headcount itself is not printed on the tile (D32); it is in the tooltip with the
industry total and the share. The footnote shows only when a starred number is on screen.
Qualified Person has no count yet, so it is not shown (C-10).

**In production.** A small `pool.json`; the same markup; keep `attachTooltip` (or lift it out of
`top3-chart.js` into a shared helper).

## 5. From prototype to production, step by step

1. **Decide** the ADRs (`11` §11). Milestone M0 in `13`.
2. **Shell**: the tokens of `assets/site.css` into the theme (`14-token-map.md`); header and
   footer as template parts.
3. **Templates**: transcribe each page's markup; keep the ids and classes the scripts use (§4).
4. **Scripts**: move the inline scripts into files; merge the two survey copies; point each
   `fetch('…/data/guide-data.json')` at the page's own slice; keep `escapeHtml` and the `fill()`
   placeholder helper.
5. **Data**: take `guide-data.json` and `areas.json` as they are and split them per page
   (ADR-4); for salary updates keep the sheet → `build-salary-data.py` step (§3.2) as the one
   way in.
6. **Verify** against the prototype: the same figures for sampled values in every part (survey
   per dataset, topic and segment; salary per area; every tile), the gate criteria in
   `07-gate.md` at 375 px and desktop, page weight within budget.
7. **Keep** the prototype URL live; it stays the reference until launch.

## 6. Open items (2026-09-28)

| Item | State | Where |
|---|---|---|
| Content still to come from the client | home page structure demo (C-1), area videos and key thoughts (C-4), chamber logos and podcast (C-5), own photographs (C-6), IT Contracting salaries (C-8), Qualified Person count (C-10), two Építőipar Talent Insight counts (C-3) | `19-implementation-prerequisites.md` |
| Decisions before publication | the bértábla banner (P-1), Excel (P-4), EN (P-5), the stack (T-1), the data policy (T-2), the Gilroy licence (A-1) | `19`, `15` |
| Inert controls | Excel download, EN, Kijelentkezés and the form submits carry `is-unavailable`; production makes them work or removes them | `14` §2 |
| Data size | one 1,1 MB JSON on every page; split per page (ADR-4) | `12` §4 |
| Raw sources | the research workbook and the July Drive files are not in the repository; keep the originals in the client's Drive | `SOURCES-AND-GAPS.md` |
