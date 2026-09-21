# Népszabadság — project documentation

The relaunch of Népszabadság as an online paper with a weekly print edition, launching
2026-10-08: a pre-registration landing page before launch and the site itself (címlap,
rovatfront, cikkoldal, Népszava márkafront), designed in Figma and prototyped here. The
Hungarian presentation for the client: [bemutato.html](bemutato.html).

| Document | What it holds |
|---|---|
| `00-brief.md` | who the client is, what the brief asks, what is real and not yet, the name (settled) |
| `01-research.md` | the 25-site technical benchmark, Reuters Institute DNR 2026 (Hungary), subscription/paywall benchmarks, the 2016 closure sourced, comparable relaunch cases, design-system references, the rendered-layout study, a closer look at nepszava.hu (unaffiliated — §8), proposals for the owner |
| `02-audit.md` | the old nol.hu domain — the client's only asset there is to audit; records the correction that nepszava.hu is not a "sister site" |
| `03-sources.md` | every input and what it contributed, every gap numbered |
| `04-decisions.md` | numbered register of the build's decisions, D1 onward |
| `05-design.md` | the tokens and components as built, read from the Figma file |
| `06-build-log.md` | the build round, what was generated, what was measured, what was fixed |
| `07-gate.md` | what `check.py` verifies |
| `handover.md` | where the project stood on 2026-09-21 before the research and audit above were written — kept as the record of that session |

The technical package (stages 10–14) is created once the client has agreed the direction.

## Process log

**2026-09-21 — project opened.** Inputs received: the landing memo
`nsz_landing_20260914_v1.docx`, the Figma file (eight frames), the sister site
nepszava.hu. The memo read in full, the frames read on screen, twenty-five news home
pages measured with `curl`. The owner stopped the browser screenshot sweep and asked for
a handover document; written as `handover.md`. Open: the folder name
(`nepszabadsag` here, `nepszava` in the message), Figma Dev Mode access.

**2026-09-21 — gate added.** `nepszabadsag/check.py` wired into the root `check.py`:
every relative link and asset resolves, every cross-page anchor exists, the two docs
pages link each other, one `h1` and a `lang` attribute per page. Registered on the hub
and in `README.md` already (same commit as the handover); this closes the gate slot.

**2026-09-21 — research and audit written.** `00-brief.md`, `01-research.md`,
`02-audit.md` and `03-sources.md` added, closing stage 0 (brief), stage 1 (research and
audit) and stage 2 (sources) of `PROTOTYPING.md`. Research: the 25-site benchmark from
`handover.md` moved here and joined by sourced industry evidence (Reuters Institute DNR
2026 Hungary, subscription/paywall benchmarks, the 2016 closure cross-checked across four
sources, comparable relaunch cases, design-system references) and a rendered-layout study
in the browser pane at 1440 and 390. Audit: nepszava.hu measured in depth — its digital
edition runs on a third-party vendor (xximedia.hu), its 2026 ad rate card prices the exact
banner sizes the Figma uses, and its operating company (XXI. Század Média Zrt.) differs
from the new design's stated publisher (Liberty Press Kft.) — a fact for the owner, not a
conclusion drawn here. The owner confirmed the project's name is Népszabadság (an earlier
"nepszava" reference was a slip); a smaller, separate note — the Figma's internal Népszava
sub-brand section shares its name with a real, currently-distressed newspaper — is recorded
in `01-research.md` §5 as a one-line question for the client, not a blocker. Next: the
owner reads the research and says "direction approved," then the Figma is unlocked (Dev
Mode or exports) and the design-system gate can start.

**2026-09-21 — the first version of the prototype built.** The owner asked directly for a
first version built from the actual Figma content and the research, compressing the
design-system/frame approval into that instruction (D1 in `04-decisions.md`). The Figma file
was read again, this time for real headlines, deks, bylines, reading times and a full article
body — the client's own copy, not invented (D2–D3). Built and generated from one source
(`content.py` + `build.py`): the Címlap, the one Rovatfront the Figma designs (Belföld), the
one Cikkoldal with its paywall mechanic, the Népszava márkafront, and the memo's landing page
with a live countdown and a client-side registration form. Sport and Tudomány — the two nav
categories the Figma never designed — carry two original, neutral items (D4–D5). Fourteen
real, licensed Wikimedia Commons photographs replace the Figma's blurred placeholders (D6).
Measured at 390 and 1440: found and fixed a 70 px mobile header overflow, four `<h1>`
elements on the landing page, sixteen-plus sub-44 px tap targets, and two broken/mismatched
links the extended gate caught — `06-build-log.md` has the full list. `nepszabadsag/check.py`
extended to cover the site pages (previously docs-only) with alt-text and banner checks. The
Hungarian client presentation (`bemutato.html`) written the same round, with live embedded
previews of the built pages. Gate clean. Next: rovat fronts for the other five categories and
the technical package.

**2026-09-21 — correction: nepszava.hu is not a "sister site."** The owner said that
describing nepszava.hu as this project's sister site during the original briefing (§1 above)
was a mistake — nepszava.hu has no relationship to Népszabadság or to this project, of any
kind. `02-audit.md` is rewritten to hold only the client's actual asset (the old nol.hu
domain); the nepszava.hu findings (digital-edition vendor, 2026 ad rate card, rendered home
page) moved to `01-research.md` §8, relabelled as one unaffiliated comparable among the
twenty-five benchmarked there rather than a special or inherited precedent. Two proposals
that depended on the sister-site premise (confirming a publisher relationship; treating the
vendor and rate card as inherited) were removed or reframed accordingly — `01-research.md`
§9 (renumbered from §8) has the current list. `00-brief.md`, `03-sources.md` and
`handover.md` updated to match; `bemutato.html`'s two cards built on the sister-site framing
rewritten. Nothing about the built prototype itself needed to change — it never referenced
nepszava.hu directly.
