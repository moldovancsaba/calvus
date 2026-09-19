# Lexodont — project documentation

The wireframe of Lexodont Dental Studio's website (March–April 2026), and — found on
2026-09-18 — the record that the practice's site went live from it. Standard structure
(owner decision 2026-09-18); each file is dated inside; this index is the process log.

| Slot | File | What it holds |
|---|---|---|
| Presentation | `bemutato.html` | **A rendelőnek szóló bemutató, magyarul** — mi készült, mi lett belőle, mi a következő kérdés |
| 00 brief | `00-brief.md` | Client, what the prototype is, what happened next, where it stands |
| 01 research | `01-research.md` | None was done — said plainly; what was read; what a second iteration would read |
| 02 audit | `02-audit.md` | **Start here**: the live lexodont.hu measured, wireframe → live page by page, the wireframe's own measurements |
| 03 sources | `03-sources.md` | What is real, what is placeholder, what is fictional; the removed `public/` set |
| 04 decisions | `04-decisions.md` | D1–D16 (the first fourteen reconstructed from the commits, the last two recorded as made); what the live site decided without this repo |
| 05 design | `05-design.md` | Two fidelities, tokens, layout; what the built site chose instead |
| 06 build log | `06-build-log.md` | The two build days and the 2026-09-18 measurement |
| 07 gate | `07-gate.md` + `../check.py` | Links, anchors, docs cross-links, fidelity parity; findings left open and why |
| 08 client asks | `08-client-asks.md` | The register of asks — none open for the delivered wireframe; the second iteration's prerequisites are in `19-implementation-prerequisites.md` |
| 10 SSOT | `10-ssot.md` | Glossary, page kinds, entities, rules, metrics |
| 11 architecture | `11-architecture.md` | As built, measured; five PROPOSED ADRs for a second iteration, none a rebuild |
| 12 technical design | `12-technical-design.md` | Wireframe page → live template; content model; booking; the checks a second iteration runs |
| 13 implementation plan | `13-implementation-plan.md` | Closing steps, or LX-001..006 |
| 14 token map | `14-token-map.md` | Nothing to map, and why |

Rendered: `index.html` (this), `bemutato.html`, `brief.html`, `research.html`, `audit.html`,
`sources.html`, `decisions.html`, `design.html`, `build-log.html`, `gate.html`,
`client-asks.html`, `ssot.html`, `architecture.html`, `technical-design.html`,
`implementation-plan.html`, `token-map.html` — by `build.py` (`python3 lexodont.hu/docs/build.py`).
The docs serve both fidelities: `../` is the polished set, `../../lexodont.hu_balsamic/` the sketch.

## Process log

**2026-03-31 — the wireframe, in a day.** Twenty commits: hub, structure, crew, subpages,
grey wireframe style, sliders, footer with map, Áraink and Szakterületek, the Balsamiq
variant, unified navigation. Client feedback applied the same day (crew layout, split
CTAs, prices off the home, contact into the footer).

**2026-04-09 — feedback round.** Home Szakterületek and Partnereink reworked, two-column
featured specialties, orphan links fixed, three treatment pages added (polished set only).

**2026-04-09 → 2026-09-18 — silence in this repo.** The client's developer built the
site: pages modified on lexodont.hu between 2026-07-30 and 2026-09-18.

**2026-09-18 — the record written (D14).** lexodont.hu measured and found to be the
wireframe built; this folder written; the wireframe measured (66 measurements, findings recorded);
`check.py` added with a parity check, which reported the three sketch pages missing since
April — mirrored the same day (D15); nothing else on the pages changed.

**Next.** `08-client-asks.md` #1.
