# IDBC Salary Guide — architecture

*How the prototype becomes the gated guide inside idbc.hu. §2 is measured. The stack in §10
and the ADRs in §11 are **PROPOSED** — the client's own spec assumed one architecture and
that assumption is examined, not adopted blindly. Written 2026-09-18.*

## 1. System context

| Actor | With the guide |
|---|---|
| Visitor | reaches the teaser inside idbc.hu; registers (company or candidate) to read |
| Reader (registered) | browses trends, areas, Bérek, SAP, Expert Community, case studies; downloads the Excel; sends Ajánlatkérés or joins the community |
| IDBC marketing | supplies data and copy; receives leads; wants usage numbers |
| IDBC recruiters | answer Ajánlatkérés and community joins |
| Site maintainer (idbc.hu's developer) | runs WordPress + WPML; would host the guide |
| The studio | built the prototype and the data pipeline; wrote this package |

External: Google Drive/Sheets (where the client's workbooks live), LinkedIn Talent
Insight (numbers delivered as a workbook, no API), IDBC's CRM (unknown — to ask),
Google Tag Manager (present on idbc.hu), a video host (YouTube/Vimeo, to choose).

## 2. The host, measured (2026-09-18, `curl`)

| Measure | Value |
|---|---|
| idbc.hu | WordPress; WPML 4.8.5; `performance-lab` + `webp-uploads`; no page builder detected; theme path not exposed |
| Home HTML / requests | 78,6 KB; 9 scripts; 6 stylesheets |
| TTFB | 0,12 s |
| Tracking | Google Tag Manager |
| Languages | HU and EN (`/en/`) |

A lean, well-kept WordPress. The guide must not bring it a page builder, a heavy plugin
set, or a 1,1 MB JSON on every page.

## 3. The client's stated architecture, examined

The spec (July) says: WordPress block editor for the pages, **Google Sheets read via
API** for the data, a registration paywall in front. Three observations:

1. **The data is not live.** The client called the survey workbook final ("mást nem
   fogunk már átadni"), the bértábla changes in rounds, and Talent Insight arrives as a
   file. Nothing changes minute to minute. A runtime Sheets API call adds a credential,
   a quota, latency and a failure mode to a marketing page, for data that changes a few
   times a year.
2. **The data needs transformation, not just reading.** The pages depend on the two
   converters: crosstab flattening, the weighted-only rule, the Talent Insight matching
   table, the area-code names. Reading Sheets directly would move that logic into
   PHP and lose the deterministic, reviewable rebuild.
3. **The paywall is real work.** Accounts with a type (company / candidate), consent,
   and a hand-off to IDBC's CRM — not a static-site feature.

Hence §10: WordPress yes; Sheets API no (a build-time import, optionally scheduled);
paywall yes, as WordPress users.

## 4. Quality attributes

| Attribute | Requirement | Verified by |
|---|---|---|
| Performance | no guide page heavier than idbc.hu's home by more than 300 KB of data; TTFB as the host's | `13` M5 |
| Data integrity | every figure reproducible from the client's files by the converters; a new workbook rebuilds all pages in one command | R1, R6 |
| Access control | every guide page and the Excel behind login; teaser public | `12` §5 |
| Privacy | registration consent recorded; GDPR notice; no marketing script before consent (GTM already governs idbc.hu) | `12` §9 |
| Accessibility | one `h1`, 44 px targets, no overflow at 375, tables with real headers (the prototype's card mode kept) | `07-gate.md` criteria on staging |
| Maintainability | marketing edits copy in the block editor; a developer runs the data rebuild; no page builder | `12` §2 |
| Bilingual | not in scope until EN copy exists; the host has WPML, so nothing blocks it later | `08-client-asks.md` #11 |

## 5. Target containers (PROPOSED)

```
 reader ──▶ idbc.hu (WordPress + WPML, as today)
            ├─ theme/plugin "salary-guide": block templates for the 7 page kinds,
            │  the prototype's CSS + top3-chart.js as enqueued assets, tokens once
            ├─ WordPress users: role guide_reader (type: cég | jelölt, consent) ── gate on guide templates
            ├─ data/: per-page JSON built by the two converters (committed, versioned)
            ├─ exports/: salary-guide-2026.xlsx built from the same JSON (behind login)
            ├─ forms: registration, Ajánlatkérés, community join → e-mail + CRM webhook
            └─ media: video embeds (consent-gated), images in the media library
 Google Drive workbooks ──(developer runs converters / scheduled import)──▶ data/
 Google Tag Manager (existing) ◀── page and filter events
```

## 6. Key flows

1. **Teaser → registration → guide**: public teaser (the client's home mockup) → register
   (the field list, D19 page) → e-mail confirmation → any guide page. Logged-out hits on
   guide URLs redirect to registration and back.
2. **Data update**: the client edits the `IDBCSYNC` tab of `IDBC_bertabla` → within about
   15 minutes a scheduled job rebuilds the data and page texts (`data/idbcsync.py`), gates
   them and deploys; a value the converter cannot accept (a date where text belongs, a word
   in a salary, an unknown placeholder) stops the job and the live site keeps its last good
   version (D37).
3. **Filter**: client-side as in the prototype; the page loads only its own JSON slice.
4. **Excel download**: link to the generated file; event to GTM; login required.
5. **Ajánlatkérés / join**: form → e-mail to IDBC + entry stored + CRM webhook.

## 7. Data architecture

The JSON is the interface between the pipeline and the pages — kept, and split per page
at build (`12` §4). No new database tables beyond WordPress users and form entries. The
client's workbooks remain the source of truth for numbers; the JSON is the source for
the pages; nothing is edited by hand between them (R1).

## 8. Security and privacy

Accounts with hashed passwords (WordPress core); registration rate-limited and
spam-protected; consent stored with timestamp; personal data only in WordPress and the
CRM; the Excel behind login; no PII in URLs; GTM consent mode as idbc.hu already runs.

## 9. Deployment and operations

Staging on idbc.hu's host; the guide as a versioned theme/plugin package plus a
`data/` directory; deploy = package + data; rollback = previous package. Data rebuilds
are a developer task with a checklist (`12` §4); monitoring is the host's.

## 10. Stack (PROPOSED)

| Layer | Client's spec | Proposed | Why |
|---|---|---|---|
| Host | WordPress (idbc.hu) | **WordPress (idbc.hu), kept** | the guide is a section of the client's site by their own mockup; WPML and GTM are there |
| Pages | block editor | **block templates + patterns in a `salary-guide` theme extension or plugin, transcribed from the prototype** | marketing edits copy; layout and charts are code |
| Data | Google Sheets via API at runtime | **build-time import by the two converters → per-page JSON, committed; optional scheduled re-import from Drive** | §3; deterministic, reviewable, no runtime dependency |
| Charts / tables | — | the prototype's `top3-chart.js` and `chart.css` as-is (vanilla, no dependency) | already the measured, client-reviewed implementation |
| Paywall | "registration gate" | **WordPress users, role `guide_reader`, type meta, consent meta; server-side gate on guide templates** | no new auth system; leads are WordPress users the CRM can pull |
| Forms | — | one form plugin (the host's, if it has one) with a CRM webhook | Ajánlatkérés, join, contact |
| Excel | download CTA | **generated at data build from the same JSON** (openpyxl), served behind login | never diverges from the pages |
| Video | — | YouTube-nocookie / Vimeo embeds, loaded after consent | the client uploads links |
| EN | switch in mockup | out of scope until EN copy exists; WPML makes it possible | `08` #11 |
| Analytics | — | GTM events: register, filter change, download, Ajánlatkérés | client asked for numbers in July notes |

## 11. Architecture decision records

All **PROPOSED** 2026-09-18.

| ADR | Decision | Options | Why |
|---|---|---|---|
| ADR-1 | Inside idbc.hu's WordPress, not a separate site | (a) inside; (b) `guide.idbc.hu` static site + Cloudflare Access/Netlify Identity; (c) separate Next/Astro app | (b) cannot do typed registration, consent and CRM hand-off without building an auth service anyway; (c) is a second stack for a marketing section. (a) reuses users, WPML, GTM, hosting. |
| ADR-2 | Build-time data import, not a runtime Sheets API | runtime API (the spec) | §3: data is periodic and needs transformation; the conversion is deterministic and validated before anything is published. **Upgrade path taken 2026-09-25 (D35, then D37)**: the prototype is built from one sheet tab, `IDBCSYNC`, by `.github/workflows/idbc-sync-bertabla.yml` — every 15 minutes and on demand it downloads `IDBC_bertabla` through its public export URL (the sheet is shared "anyone with the link", so no service-account credentials), runs `data/idbcsync.py` (which writes `guide-data.json`, `areas.json` and every marked page text), gates the result with `check.py`, and pushes to `main` only when something changed. Still build-time: a reader never waits on Google, a sheet error never reaches the page, and every change is a reviewable commit. Production keeps the same shape (a scheduled import into the CMS's data files), with the sheet restricted to named editors — "anyone with the link can edit" is acceptable for a prototype, not for a published guide. |
| ADR-3 | Paywall = WordPress users with a `guide_reader` role and type/consent meta | membership plugin; external identity provider | the registration is five fields and a type; a membership plugin is heavier than the need; leads must land where IDBC can read them |
| ADR-4 | Per-page JSON slices, ≤ 300 KB each | one 1,1 MB file (the prototype) | the prototype fetches everything on every page; fine for review, not for a section of a lean site |
| ADR-5 | Excel generated from the JSON at build | client-supplied file | the CTA has been inert since July because no file exists; generated, it can never disagree with the pages |
| ADR-6 | Prototype markup, CSS and chart code are transcribed, not reinterpreted; deviations recorded as decisions | redesign in WordPress | the client has reviewed and corrected the pages three times; they are the acceptance reference |
| ADR-7 | EN edition deferred; HU only in Release 1 | build the switch now | no EN copy, no EN data labels; WPML makes it a content task later |
| ADR-8 | Home page built only after the client's structure demo | build from the July PDF | the client said a demo is coming; the PDF is lorem ipsum |
