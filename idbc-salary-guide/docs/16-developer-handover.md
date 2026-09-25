# IDBC Salary Guide — developer handover

*For a developer who takes the prototype into the live environment, and for anyone who reads or
edits the `IDBCSYNC` sheet. What the prototype is made of, how the data gets out of the sheet,
how the three interactive parts — survey, salary, Expert Pool — work, and how they move to
production. The target system is designed in `11-architecture.md` and `12-technical-design.md`
(PROPOSED); this is the practical path to it. Written 2026-09-25 from the code as it stands.*

## 1. What you get

| Piece | Where | Role |
|---|---|---|
| Live prototype | <https://moldovancsaba.github.io/calvus/idbc-salary-guide/> | the acceptance reference: production transcribes it, it does not redesign it (ADR-6) |
| Repository | <https://github.com/moldovancsaba/calvus>, folder `idbc-salary-guide/` (public) | everything below |
| Pages | `index.html` (Piaci trendek), `terulet/index.html` (one template for all 11 areas), `berezes/`, `sap/`, `expert-pool/`, `esettanulmanyok/`, `regisztracio/`, `kapcsolat/` | static HTML, no build step, no framework, no dependency |
| Shared assets | `assets/site.css` (idbc.hu tokens, header, footer, heroes, buttons, cards, forms), `assets/site.js` (menu), `assets/chart.css` (chart, pill, tooltip), `assets/top3-chart.js` (TOP3 chart + tooltip, `window.IDBCChart`) | loaded by every page; each page's own `<style>` holds only its own rules |
| Data | `data/guide-data.json` (survey, salary, Expert Pool, SAP catalogue; 1,1 MB), `data/areas.json` (the 11 areas) | **generated — never edit by hand** |
| Sync | `data/idbcsync.py` + `.github/workflows/idbc-sync-bertabla.yml` | sheet → data files and page texts, validated |
| Source | Google Sheet `IDBC_bertabla`, tab **`IDBCSYNC`** | every text and figure on the guide, one row each (D37) |
| Documentation | this folder | decisions `04`, data model `10`, architecture `11`, design `12`, plan `13`, tokens `14` |

## 2. Run it and rebuild it locally

The pages load their JSON with `fetch`, so they need a web server (a `file://` URL shows empty
charts).

```
git clone https://github.com/moldovancsaba/calvus.git
cd calvus
python3 -m http.server 8000        # then open http://localhost:8000/idbc-salary-guide/
```

Rebuild from the live sheet (Python 3 and `openpyxl`):

```
pip install openpyxl

# download the sheet (the same URL the scheduled job uses)
curl -sL -o /tmp/IDBC_bertabla.xlsx \
  "https://docs.google.com/spreadsheets/d/1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg/export?format=xlsx"

# validate only, write nothing
python3 idbc-salary-guide/data/idbcsync.py /tmp/IDBC_bertabla.xlsx --check

# write the data files and the page texts
python3 idbc-salary-guide/data/idbcsync.py /tmp/IDBC_bertabla.xlsx

# the gate: read the exit code, 0 = clean
python3 check.py
```

`--check` prints the counts (rows, areas, salary rows, Expert Pool rows, survey datasets) and
which files would change. Any error prints the row and stops with exit 1 before anything is
written. The messages are in Hungarian because the sheet's editors read them.

## 3. The sheet: `IDBCSYNC`

### 3.1 Columns

| Column | Read by the sync | Content |
|---|---|---|
| A `id` | yes | the technical key; the sync, the pages and the data all refer to it — never change it |
| B `változó` | no | what the value is, in words |
| C `érték` | **yes** | the value itself — the only cell an editor changes |
| D `megjelenés` | no | where it shows on the site |
| E `segítség` | no | what may be typed there |

The header row is found by its names (`id`, `érték`), so columns can be moved. Rows whose `id`
starts with `#` are section headings and are skipped. Row visibility, colours, bold, frozen rows
and conditional formatting are never read (D42–D46): hide, colour and group freely.

### 3.2 What the sync accepts

- **Everything is text.** A value Google turns into a date (`1-5` → a date) or into a formula
  (a leading `+` or `=`) is refused and names the row; type it with a leading apostrophe
  (`'+36 30 479 8090`).
- **Numbers**: salaries and counts are whole numbers; spaces, dots and `Ft` are tolerated.
  Survey percentages 0–100. Weighted scores 0–`SCALEMAX`.
- **Flags**: `TOP3` is `igen`/`nem` (also `i`, `x`, `yes`, `1`; empty = `nem`); area media is
  `video` or `highlight`; `SORREND` is `igen`/`nem`.
- **Placeholders**: a text used by a page script may contain only its own `{placeholders}`
  (e.g. `{terulet}`, `{n}`); an unknown one stops the build.
- **Ids are unique**; an id the pages use but the sheet lacks stops the build.
- **Any error → nothing written.** In the scheduled job this means the site keeps its last good
  version and the job log names the row.

### 3.3 Id families

| Id pattern | Becomes | Shown on |
|---|---|---|
| `SHARED-…`, `HOME-…`, `TERULET-…`, `BEREK-…`, `SAP-…`, `POOL-…`, `ESETT-…`, `REG-…`, `KAPCS-…` | page texts, placed by markers in the HTML (§3.5) | the page named in the prefix; `SHARED-` = header, footer, chart legend on every page |
| `AREA-<slug>-NAME / -SUMMARY / -MEDIA / -EDITION` | `areas.json` | area pages, home area tiles, the survey's dataset names; `-EDITION` picks the area's question set |
| `SAL-<area>-NAME`, `SAL-<area>-nnn-POZICIO / SZINT / TOP3 / MIN / IDBC / MAX / JUTTATAS / LINKEDIN` | `salary.webBertabla` | Bérek, SAP (§5.2) |
| `EXPERT-nn-IPARAG / POZICIO / DARAB / LINKEDIN` | `salary.expertPool` | Expert Pool (§5.3) |
| `SAPPROD-CATn-NAME / -ITEMm` | `sapProducts` | SAP catalogue tiles |
| `SURVEY-…` | `topics`, `segments`, `datasets`, `keepSourceOrder`, `totalLabel` | Piaci trendek and area pages (§5.1) |

**Row order matters** for lists: the order of topics, of questions inside a topic, of survey
segments, of SAP items, of salary areas and positions and of Expert Pool tiles is the sheet's
order. Do not sort the tab.

### 3.4 Editing: what anyone can do, what needs a developer

| Change | Who | How |
|---|---|---|
| Change a text or a number | any editor | type into column C; it reaches the site on the next sync |
| Remove a salary position, an Expert Pool tile or an SAP item | any editor | clear its name (`POZICIO` / `NAME` / `ITEMm`); the row is dropped from the page. An Expert Pool tile without `DARAB` is left out with a warning |
| Add a salary position | developer (or an editor with column A shown) | 8 new rows `SAL-<area>-nnn-…` with the next free `nnn` of that area, inside the area's block |
| Add an Expert Pool tile | developer | 4 rows `EXPERT-nn-…` with the next free `nn` |
| Add a survey question to a topic | developer | a row `SURVEY-TOPICt-SETn-<SIDE>-kk` whose value is the question's `Qnn`, placed where it should appear (D40 did exactly this) |
| Add a new page text | developer | a row with a new id **and** a marker in the page (§3.5) |
| Delete a row, change an id, sort the tab | nobody | the sync stops (missing id) or the order on the site changes |

### 3.5 How a page text finds its row

`idbcsync.py` rewrites the prototype's HTML in place, by marker:

| Marker | Example | Effect |
|---|---|---|
| `data-sync="ID"` | `<h1 data-sync="BEREK-H1-…">Bérsávok</h1>` | the element's text (a line break in the cell becomes `<br>`); the element must hold text only |
| `data-sync-attr="name:ID;name:ID"` | `alt`, `title`, `placeholder`, `content` | the attribute's value |
| `data-sync-href="tel:ID"` / `"mailto:ID"` | footer phone and e-mail | the link target |
| `/*sync:ID*/"…"` | inside a page script or `top3-chart.js` | the string literal; a changed chart text also bumps `top3-chart.js?v=` on every page |

## 4. Getting the data out

Pick one way and keep one source (R1: nothing is edited between the sheet and the pages).

| Way | Use when | How |
|---|---|---|
| **A. Take the generated JSON** | the first production build | copy `data/guide-data.json` and `data/areas.json` from `main`; split per page (ADR-4, `12` §4); the renderers read exactly this shape (entities in `10-ssot.md` §3) |
| **B. Run `idbcsync.py` in the production pipeline** | the sheet stays the source after launch (ADR-2) | a scheduled job: export the sheet as `.xlsx` → `idbcsync.py --check` → build → split → publish the JSON into the site's data directory; on any error keep the previous files and alert |
| **C. Read the sheet in another language** | a stack without Python | port `build()` from `idbcsync.py` (the id grammar and the checks in §3.2, about 190 lines); read the `.xlsx` export or the tab as CSV (`…/export?format=csv&gid=<IDBCSYNC tab id>`) |

Not recommended: calling the Google Sheets API when a page loads — a credential, a quota and a
failure mode on every page view, for data that changes a few times a year (`11` §3).

**Page texts in production — decide once.** In the prototype the sheet also owns every page
text. In production either (a) the sheet keeps them: the job writes them into the templates or a
`texts.json` the templates read; or (b) the CMS editor owns them: the page-text rows
(`SHARED-` … `KAPCS-`) are retired from the sheet. Keeping both would make two sources for one
text. The data rows (`AREA-`, `SAL-`, `EXPERT-`, `SAPPROD-`, `SURVEY-`) stay in the sheet in
either case.

**Access.** The prototype's sheet is shared "anyone with the link can edit" for the review; the
job only needs "anyone with the link can view". For production, restrict editing to named
people; if view-by-link is also closed, the job needs a service account and the Drive/Sheets
API with a stored secret.

## 5. The interactive parts

### 5.1 Survey — Piaci trendek (home) and the area pages

| | |
|---|---|
| Code | `index.html`, the inline script at the end; `terulet/index.html` has **its own copy** of the same renderer (same rules, shorter code) — merge them into one module in production (R9) |
| Data | `guide-data.json`: `datasets`, `topics`, `segments`, `totalKey` / `totalLabel`, `keepSourceOrder`; the area page also loads `areas.json` |
| Controls | home: dataset `#datasetSelect` (Összesített adatok + 11 areas), topic `#topicSelect`, employee segment `#empSegmentSelect` (experience), employer segment `#erSegmentSelect` (company size); panels `#b2cChart` (Munkavállalók), `#b2bChart` (Munkáltatók). Area page: the dataset is fixed by `?terulet=<slug>` (unknown slug → the first area; an area without data → the whole sample); topic and the two segment selects; panels `#employeeChart`, `#employerChart` |

**How a panel is built.** The question list is
`topics[topic].questionSets[dataset.questionSet][side]`. For each question: with *Összesített
adatok* selected the chart comes from `datasets[d][side].base[question]`; with a real segment
from that segment's row in `cross[question]`. Then it is drawn by kind.

**Data shapes** (`10-ssot.md` §3): `base` is `{kind: "simple", items: [{label, percent, count}]}`
or `{kind: "weighted", scaleMax, items: [{label, value}]}`; `cross` is
`{kind: "matrix-percent", groups: [answers], items: [{label: segment, values: [{group, percent, count}]}]}`.
`count` = percent × the respondents of that cell, shown in the tooltip as "(n fő)".

**Rules the code applies** (numbers from `10-ssot.md` §6):

- *Összesített adatok* is first and the default; a real segment is offered only if at least one
  question of the topic has a non-zero row for it; a segment dropdown with no real choice is
  hidden (R2).
- A question with no data under the chosen segment is left out — the whole-sample figures are
  never shown in its place; if the whole panel empties, one sentence (`SHARED-JS-NO-DATA`)
  replaces it (R3). On the home page a topic with no question for the dataset's question set
  shows `HOME-JS-NO-QUESTION`; the area page shows the no-data sentence.
- Answers nobody chose (0 %) are dropped.
- Shape: up to 5 single-choice answers → one stacked bar with a legend; multi-choice (the
  percentages add up to more than 110 %) or more than 5 answers → one bar per answer.
- Order: questions flagged `SORREND = igen` keep the questionnaire's order; answer scales that
  are numeric ranges or home-office days keep scale order; everything else is sorted by
  percentage.
- The two 1–4 scale questions show the weighted average only, with "(súlyozott átlag, 1–4
  skála)" (R4).

**Sheet rows.** `SURVEY-TOTAL-LABEL`, `SURVEY-TOTAL-EDITION`, `SURVEY-SETn-NAME` (question sets),
`SURVEY-TOPICt-NAME`, membership `SURVEY-TOPICt-SETn-<SIDE>-kk` = `Qnn` (order = display order),
`SURVEY-<SIDE>-SEGk` (segment labels), `SURVEY-<SIDE>-Qnn-TEXT / -OPTmm / -SCALEMAX / -SORREND`
(question text, answer labels — each once for all areas), and the figures
`SURVEY-<DATASET>-<SIDE>-Qnn-[SEGk-](N|OPTmm)` (respondents and percentages per dataset,
hidden). A question text must be unique on its side.

**In production.** Keep the renderer client-side (it is filter-driven); load only the page's
dataset (`trends-total.json`, `trends-<slug>.json`, `12` §4) instead of the 1,1 MB file.

### 5.2 Salary — Bérek and SAP

| | |
|---|---|
| Code | `berezes/index.html` and `sap/index.html`, inline scripts; `assets/top3-chart.js` (shared chart); `assets/chart.css`; the table's styles in each page's `<style>` |
| Data | `salary.webBertabla`: `{id, kod, terulet, szint, pozicio, top3, min, idbc, max, juttatas, linkedin?}`. SAP shows the rows with `kod = "SAP"`, Bérek all the others — the key is fixed, so renaming the SAP area in the sheet cannot move rows between the pages (D37) |
| Controls | Bérek: area `#teruletSelect` (areas in sheet order); chart `#top3Panel`; table `.table-wrap table`. SAP: no filter; catalogue `#productGrid` from `sapProducts` |

**TOP3 chart.** The rows flagged `top3` for the area go to
`IDBCChart.renderTop3Chart(rows, {idPrefix, chartLabel, emptyText})`, which returns SVG markup;
`IDBCChart.attachTooltip(container)` then binds the tooltips (call it after every re-render).
Above 700 px of viewport one wide chart; at 700 px and below one small chart per position with
its own scale in millions (`1,25M`) — the pages re-render when the viewport crosses 700 px.
Each position shows three points: offered (`min`, light green), IDBC recommended (`idbc`),
expected (`max`, dark green); amounts close together stack upward over their own dots (D41). A
LinkedIn count adds the pill "n elérhető jelölt*" and the footnote. An area with no TOP3 row
shows a sentence instead of the chart.

**Table.** Every position of the area, TOP3 ones included (R10). One `<tbody>` per position;
its levels sorted Trainee → Junior → Medior → Senior → Team Leader → Manager; Junior, Medior
and Senior carry their experience text (`BEREK-JS-SZINT-…`). Columns: level, minimum, maximum,
other benefits. Below 600 px of **container** width (a CSS container query) the table turns
into cards: each position is a card with its band (min–max) and a toggle, collapsed at first.

**Sheet rows.** `SAL-<area>-NAME` (the area's name in the dropdown and titles), then 8 rows per
position `SAL-<area>-nnn-POZICIO / SZINT / TOP3 / MIN / IDBC / MAX / JUTTATAS / LINKEDIN`.
`MIN`/`IDBC`/`MAX` whole numbers; `LINKEDIN` optional; clearing `POZICIO` removes the position.
In the sheet the positions alternate two shades and each area's name row is bold (D44).

**In production.** Render the table on the server with the same markup (`role` attributes,
`data-label` cells, one `<tbody>` per position) so card mode works without JavaScript; keep the
chart client-side with `top3-chart.js` unchanged (`12` §7); generate the Excel from the same
JSON (ADR-5).

### 5.3 Expert Pool

| | |
|---|---|
| Code | `expert-pool/index.html`, inline script; tile styles in the page's `<style>`; the tooltip and the footnote text come from `assets/top3-chart.js` (`attachTooltip`, `TALENT_NOTE`) |
| Data | `salary.expertPool`: `{iparag, pozicio, darab, linkedin?}` — a row without `darab` is not in the file (the sync warns) |
| Controls | industry `#iparagSelect` (values from the data, IT and Non-IT today); tiles `#expertGrid`; footnote `#talentNote` |

**A tile** shows the industry, the position, the market line "Piacon elérhető szakember: n fő*"
when a LinkedIn count exists, and a bar labelled IDBC Expert Community whose width is `darab`
divided by the largest `darab` of the **whole** pool, so switching industries compares like with
like. The IDBC headcount itself is not printed on the tile (D32); it is in the tooltip with the
industry total and the share. The footnote shows only when a starred number is on screen.

**Sheet rows.** `EXPERT-nn-IPARAG / POZICIO / DARAB / LINKEDIN`, in the section "EXPERT POOL —
CSEMPÉK" (bold, D46). Qualified Person (`EXPERT-27`) has no `DARAB` or `LINKEDIN` yet, so it is
not shown (C-10).

**In production.** A small `pool.json`; the same markup; keep `attachTooltip` (or lift it out of
`top3-chart.js` into a shared helper).

## 6. From prototype to production, step by step

1. **Decide** the ADRs (`11` §11) and who owns the page texts (§4). Milestone M0 in `13`.
2. **Shell**: the tokens of `assets/site.css` into the theme (`14-token-map.md`); header and
   footer as template parts.
3. **Templates**: transcribe each page's markup; keep the ids and classes the scripts use
   (§5).
4. **Scripts**: move the inline scripts into files; merge the two survey copies; point each
   `fetch('…/data/guide-data.json')` at the page's own slice; keep `escapeHtml` and the `fill()`
   placeholder helper.
5. **Data job**: scheduled export → `idbcsync.py` → split → publish, keeping the last good
   version on error; restrict the sheet's editors.
6. **Verify** against the prototype: same figures for sampled values in every part (survey per
   dataset, topic and segment; salary per area; every tile), the gate criteria in `07-gate.md`
   at 375 px and desktop, page weight within budget.
7. **Keep** the prototype URL live; it stays the reference until launch.

## 7. Open items a developer should know (2026-09-25)

| Item | State | Where |
|---|---|---|
| Scheduled sync | GitHub has not started a scheduled run of the workflow; every sync so far was started by hand (Actions → "IDBC — sync from IDBCSYNC" → Run workflow). Production should use a scheduler it controls | README process log |
| Data gaps | IT Contracting salaries (C-8), Qualified Person counts (C-10), two Építőipar Talent Insight counts (C-3) | `19-implementation-prerequisites.md` |
| Decisions before publication | the bértábla banner (P-1), Excel (P-4), EN (P-5), the stack (T-1), the data policy (T-2), the Gilroy licence (A-1) | `19`, `15` |
| Inert controls | Excel download, EN, Kijelentkezés and the form submits carry `is-unavailable`; production makes them work or removes them | `14` §2 |
| Data size | one 1,1 MB JSON on every page; split per page (ADR-4) | `12` §4 |
