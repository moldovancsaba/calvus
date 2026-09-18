# IDBC Salary Guide — technical design

*The detail under `11-architecture.md`, on the PROPOSED stack. Written 2026-09-18.*

## 1. Page kinds → templates

| Prototype | Template | Data it loads | Editable by marketing |
|---|---|---|---|
| Kezdőoldal (not built) | `page-salary-guide.html` — teaser inside idbc.hu's template per the client's PDF, then the copy from `SG - kezdő oldal.docx` | none | all copy, logos, podcast embed |
| `index.html` Piaci trendek | `page-trends.html` | `data/trends-total.json` + area list | intro, method note |
| `terulet/?terulet=<slug>` | `page-area.html` with the slug as a query var (one template, D11) | `data/trends-<slug>.json`, `areas.json` | summary text, media URL/key thought |
| `berezes/` | `page-berek.html` | `data/salary.json` | table note |
| `sap/` | `page-sap.html` | `data/salary.json` (SAP rows) + `data/sap-products.json` | trend copy, catalogue, contact card |
| `expert-pool/` | `page-expert-community.html` | `data/pool.json` | all copy |
| `esettanulmanyok/` | `page-case-studies.html` | none | articles, video URLs |
| `regisztracio/` | `page-register.html` | — | consent text |
| shared | `parts/guide-header.html` (the seven-item nav, D19), `parts/guide-footer.html` | | menu in one place |

Templates are the prototype's HTML with the data loop moved from inline `fetch` to
either server-rendered markup (tables) or the same client-side renderer reading a
smaller JSON (charts, filters). Chart and tooltip code is `top3-chart.js` unchanged.

## 2. Content model

| Content | Storage |
|---|---|
| Page copy (intro texts, SAP trends, Expert Community, case studies, area summaries) | page content in the block editor; area summaries as a repeatable block on the area page keyed by slug |
| Numbers | `data/*.json`, generated (never edited in the editor) |
| Media | video URL per area and per case study as page meta; key thought as a text field; images in the media library |
| Registration fields, consent text | template + options page |

## 3. Data pipeline

```
client workbook(s) ──▶ build-guide-data.py ──▶ guide-data.json ──▶ split.py ──▶ data/trends-*.json
                  └──▶ build-salary-data.py ─┘                       ├──▶ data/salary.json, pool.json, sap-products.json
                                                                     └──▶ exports/salary-guide-2026.xlsx
```

- The two converters stay as they are (deterministic, asserting); their input paths
  become arguments (today one has a hard-coded Downloads path — `13` SG-020).
- `split.py` (to write) cuts `guide-data.json` into per-page files and builds the Excel
  (openpyxl): one sheet per bértábla area + Expert Pool + Talent Insight, with the same
  labels as the pages and the footnote.
- Checklist for a data round: run the converter(s) → read the printed summaries (rows,
  areas, matches) → `git diff` the JSON → gate → deploy → verify one figure on the live
  page against the workbook.
- Optional later: a scheduled job that downloads the Drive files and runs the same
  chain, opening a review instead of deploying (ADR-2 upgrade path).

## 4. JSON slices (ADR-4)

| File | Content | Approx. size |
|---|---|---|
| `trends-total.json`, `trends-<area>.json` ×11 | one dataset + `topics` | ~90 KB each |
| `salary.json` | `webBertabla`, `talentInsightTop3` | ~110 KB |
| `pool.json` | `expertPool` | < 5 KB |
| `sap-products.json` | `sapProducts` | < 10 KB |
| `meta.json` | `filterDimensions`, `siteMap`, `readme` | documentation only, not loaded by pages |

## 5. Registration and gate

- Fields (client, 2026-09-18): Vezetéknév, Keresztnév, E-mail, Cégnév, Pozíció, fióktípus
  (cég | jelölt), Jelszó, adatvédelmi elfogadás. No newsletter checkbox.
- WordPress user with role `guide_reader`; meta `guide_type`, `guide_company`,
  `guide_position`, `guide_consent_at`. E-mail confirmation before access (double
  opt-in doubles as address validation).
- Gate: guide templates check `is_user_logged_in()` and the role; otherwise redirect to
  `/regisztracio/?next=<url>`. Teaser and registration public. Kijelentkezés = WordPress
  logout with redirect to the teaser.
- States: `registered (unconfirmed) → confirmed → active`; `active → logged out`.
  Deletion on request = WordPress user deletion + CRM note.
- CRM: on confirmation, a webhook with the six fields to the client's CRM (unknown —
  `13` SG-001); until known, an e-mail to marketing.

## 6. Forms

| Form | Fields | To | After |
|---|---|---|---|
| Ajánlatkérés (Expert Community page; header link target to confirm, `08` #8) | Cégnév, kapcsolattartó, e-mail, telefon, keresett pozíció / üzenet | e-mail to IDBC + entry + CRM | on-page thanks |
| Csatlakozom az Expert Communityhez | vezetéknév, keresztnév, pozíció, e-mail, telefon, üzenet | e-mail to recruiters + entry | thanks |
| Registration | §5 | WordPress | confirmation e-mail |

Server-side validation, honeypot + rate limit, no CAPTCHA that blocks real candidates.

## 7. Charts and tables

`top3-chart.js` and `chart.css` are enqueued once, versioned by file hash instead of
`?v=`. Wide/compact switching, the pill, the footnote, the tooltip: unchanged. Tables:
server-rendered with the same markup (`role` attributes, `data-label` cells, one
`<tbody>` per position) so card mode below 600 px keeps working without JavaScript.

## 8. Media

Video: the client supplies YouTube/Vimeo links per area (7) and case study (2); the
placeholder block becomes an embed loaded after consent (a click-to-play poster, no
third-party request before it). Key thoughts (4 areas): text field, rendered in the
green box. Infographic slot: retired (D20).

## 9. Analytics and consent

GTM already on idbc.hu. Events: `guide_register`, `guide_login`, `guide_filter`
(page, topic, segment), `guide_area_open`, `guide_download`, `guide_ajanlatkeres`,
`guide_join`. Consent mode as the host runs it; embeds and pixels wait for consent.
Monthly numbers to the client: registrations by type, downloads, most-used filters.

## 10. Performance

Per-page JSON (§4); chart JS ~10 KB; CSS from the prototype (one file, deduplicated
from the seven page copies — `14`); images WebP via the host's `webp-uploads`; fonts
the host's (Inter fallback stack already). Budget: guide page ≤ host home + 300 KB.

## 11. URLs and SEO

Teaser indexable with the client's copy; guide pages `noindex` (behind login anyway);
prototype URLs are not production URLs — the section lives under a path the client
chooses (e.g. `/salary-guide/`), and the GitHub Pages prototype stays up until the
client says otherwise (a live URL is never deleted).

## 12. Operations

Staging on the host; deploy = package + `data/`; a data round follows §3's checklist;
rollback = previous package + previous `data/`. Backups and monitoring are the host's.
