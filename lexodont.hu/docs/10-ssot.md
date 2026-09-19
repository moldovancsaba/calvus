# Lexodont — single source of truth (SSOT)

*The content model of the practice's site as the wireframe fixed it and the live site
confirmed it. Written 2026-09-18 from the wireframe pages and the 2026-09-18 measurement of
lexodont.hu.*

## 1. Glossary

| Term | Meaning |
|---|---|
| Szakterület | A specialty (nine): parodontológia, implantológia, gyökérkezelés, fogszabályozás, fogpótlás, szájsebészet, gyerekfogászat, fogkőeltávolítás, megtartó fogászat. Four are "featured" on the home page. |
| Kezelés / ár | A priced treatment line on Áraink; the live site prices are the truth, the wireframe's were examples. |
| Csapattag | A dentist with portrait, name, role and a personal note; live: four. |
| Esettanulmány | A before/after case: two images behind a slider, starting situation, result, a detail page. |
| Tudásközpont cikk | A knowledge article on a treatment topic; the hub links four in the wireframe. |
| Technológia | A technology page (live only: Technológiák, e-max betét, EMS). |
| Kapcsolat | The contact block: address, doorbell, phone, mobile, e-mail, hours, parking, transport, map. |
| Időpontfoglalás | Booking; wireframe: a CTA to the contact block; live: the Flexi-Dent embed page. |
| Partner | A named supplier/brand; two featured, five listed. |
| Fidelity | polished (`lexodont.hu/`) or sketch (`lexodont.hu_balsamic/`); same content (D10). |

## 2. Enumerations

| Enum | Values |
|---|---|
| Specialty | the nine above; featured: parodontológia · implantológia · gyökérkezelés · fogszabályozás |
| Navigation (wireframe) | Rólunk · Szakterületek · Áraink · Esettanulmányok · Csapat · Kapcsolat + "Időpont foglalás" CTA |
| Navigation (live) | Rólunk · Szakterületek · Technológiák · Áraink · Esettanulmányok · Tudásközpont · Csapat · Kapcsolat + Időpontfoglalás; HU / EN |
| Page kinds | home · specialties hub · specialty · prices · cases hub · case · team · knowledge hub · article · (live) technology · booking · legal |
| Language | hu (root); en under `/en/` (live only) |

## 3. Entities

| Entity | Fields (as rendered) | Where it lives today |
|---|---|---|
| Specialty page | name, lead, sections, CTA | WordPress page under `/szakterulet/` |
| Price line | treatment name, price HUF | Áraink page content |
| Team member | name, role, portrait, note | Csapat page content |
| Case | title, before image, after image, starting situation, result | `/esettanulmany/<n>-eset/` |
| Article | title, body, related specialty | `/tudaskozpont/…` |
| Contact | address, doorbell, phone, mobile, e-mail, hours (4 lines), parking (2 zones), transport, map | theme footer |
| Partner | name, featured flag, link | home content |

The wireframe holds all of these as static HTML; the live site as WordPress pages in a
custom theme. No structured data file exists in this repo for Lexodont.

## 4. Rules

| # | Rule | Origin |
|---|---|---|
| R1 | Prices are never on home cards; Áraink is the one place (D7). | client |
| R2 | Contact, hours, parking and transport are one block in the footer on every page (D8). | client |
| R3 | One navigation and CTA set on every page (D11). | owner |
| R4 | Before/after imagery only on case pages and the two home samples; each case has a detail page (D9). | owner |
| R5 | Featured specialties are the four named above, two columns (D12). | client |
| R6 | Both fidelities carry the same page set (D10); the gate's parity check enforces it (D15). | owner |
| R7 | Every published URL stays (repo rule). | repo |
| R8 | Health data never leaves the practice system into marketing: no segment, no reminder copy, no newsletter on treatment history (§4b). | GDPR Art. 9 |
| R9 | A child's data only through the parent, with consent; no child's face on the site; case photos only with written consent. | §4b |
| R10 | The newsletter, the booking embed and case photos run only when the policy record's fields for them are set (the gate). | §4b |

## 4b. Responsible-data policy record (PROPOSED, 2026-09-20)

*One record per instance, per the framework in `business-direct/docs/18-responsible-data-policy-framework.md` (owner directive 2026-09-19: responsible data for every client; hub audit 2026-09-20, action 1). Filled for a dental practice in Hungary; every value
is a proposal until the client confirms it. The wireframe stores nothing; the record binds
the site that is built from it.*

| Field | Value (PROPOSED) | Why |
|---|---|---|
| client · instance | Lexodont · lexodont.hu (HU, EN) | — |
| jurisdictions · laws | HU, EU — GDPR (Art. 9: **health data is a special category**), Hungarian Act CXII/2011 (Infotv.), Act XLVIII/2008 (advertising; no health-claim advertising beyond what the law allows), EU AI Act Art. 50 for any generated media | a dental practice processes health data the moment a patient describes a complaint |
| audienceModel | adults and **children as patients** (gyerekfogászat): a child's data only through the parent, with the parent's consent | Art. 8 GDPR, Infotv. |
| childData | none on the site; the booking and case data live in the practice system (Flexi-Dent), never in marketing | R24 of the framework |
| processors | Flexi-Dent booking embed (`publicapi.flexi-dent.hu`) — a processor agreement and a privacy notice naming it | the audit found the embed; the docs mention the privacy page once |
| sensitiveCategories | health: an enquiry that describes a condition is answered and not stored outside the practice system; no marketing segment on treatment history | Art. 9; FTC v. BetterHelp as the cautionary case |
| mediaConsent | before/after case photos only with the patient's written consent; no child's face on the site; no generated faces | R15, R30 |
| channels · consent | e-mail newsletter only by consent; no SMS marketing; appointment reminders are service messages | Act XLVIII/2008 |
| defaults · cap · optOutSla | nothing on by default; one newsletter a month at most; opt-out within one business day | R28 |
| aiDisclosure | label + text for any generated image or text (EU) | Art. 50 |
| retention | enquiries 12 months; newsletter consent until withdrawn; case photos while consent stands | to confirm with counsel |
| privacyPolicy | `/adatkezelesi-tajekoztato/` — must name the booking processor, the newsletter, cookies, and children's data through parents | the gate blocks the newsletter until it does |
| dpia | recommended (health data at scale) | GDPR Art. 35 |
| vulnerability · darkPatterns · accessibility | no pressure ("last appointment today" only if true); no pre-ticked consent; WCAG 2.2 AA (a health service) | R32, R36, R34 |

**Gate rows for the production site:** newsletter needs the privacy-policy clause and the
consent text; case photos need the written consent on file; the booking embed needs the
processor agreement named in the policy. Rules R8–R10 below.

## 5. Metrics

| Metric | Live value (2026-09-18) | Wireframe |
|---|---|---|
| TTFB | 0,24–0,38 s | n/a (static) |
| Home HTML / scripts / stylesheets | 76 KB / 6 / 5 | 16 KB / 0 external / 1 |
| `hreflang` hu/en/x-default | every page | none (HU only) |
| One `h1` | yes (booking page: none) | every page |
| Overflow at 390 | not measured | 8 px on one page |
| Tap targets < 44 px at 390 | not measured | 18 pages |

## 6. Document map

`00-brief.md` · `02-audit.md` (start here) · `04-decisions.md` · `05-design.md` ·
`07-gate.md` · `08-client-asks.md` · `11-architecture.md` (as built) ·
`12-technical-design.md` · `13-implementation-plan.md` (iteration 2, proposed) ·
`14-token-map.md`.
