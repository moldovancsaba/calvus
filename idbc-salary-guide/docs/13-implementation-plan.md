# IDBC Salary Guide — implementation plan

*Milestones, issues with a Definition of Done, blocked register, risks, Release 1 scope —
for the production build of the guide inside idbc.hu under the PROPOSED stack. The
prototype's fine-tuning with the client continues in parallel and is not planned here
(it is reactive by nature: reported item → fix → URL). Written 2026-09-18.*

## 0. Conventions

Issue ids `SG-nnn`; epics E0–E7; milestones M0–M6. "Matches the prototype" = same
sections, same copy, same figures, the gate criteria (`07-gate.md`) green at 375 and
desktop, side-by-side screenshot in the build log.

## 1. Global Definition of Done

Built on staging; gate criteria measured and recorded; every figure on the page equals
the JSON, and the JSON equals the client's workbook for a sampled value; no page
heavier than budget; the build log entry written; nothing behind an inert control
left inert without a reason in `08-client-asks.md`.

## 2. Milestones

| M | Name | Exit criterion |
|---|---|---|
| M0 | Decisions and access | ADRs decided; staging access; CRM target known; path chosen |
| M1 | Guide shell | header/footer parts, tokens once, page templates for the seven kinds rendering the prototype markup with static data |
| M2 | Data pipeline | converters parameterised; `split.py`; per-page JSON; Excel generated; a data round run end to end on staging |
| M3 | Registration and gate | accounts, confirmation, gate, logout, CRM hand-off |
| M4 | Forms and media | Ajánlatkérés, join, video embeds, key thoughts |
| M5 | Home page and QA | teaser per the client's demo; measurements; content freeze with the client |
| M6 | Launch | DNS/path live; prototype URL kept; monitoring the host's |

Indicative effort for one WordPress developer with the prototype: M0 one week; M1 two;
M2 one; M3 two; M4 one; M5 two; M6 one. About ten weeks; M5 depends on the client's
home demo.

## 3. Issues

### E0 Decisions and access (M0)
- **SG-000** Client decides ADR-1..8 — DoD: each recorded in `04-decisions.md`.
- **SG-001** CRM named and a webhook/API path agreed — DoD: a test lead lands.
- **SG-002** Staging access on idbc.hu's host; guide path chosen — DoD: staging URL.
- **SG-003** Content freeze list with the client (copy that still changes) — DoD: list in `08-client-asks.md`.

### E1 Guide shell (M1)
- **SG-010** Tokens once (`14`); the seven page copies of `:root` collapse into one stylesheet — DoD: computed styles identical on every page.
- **SG-011** Header/footer parts with the seven-item nav (D19) — DoD: matches.
- **SG-012** Templates for trends, area, Bérek, SAP, Expert Community, case studies, registration — DoD each: matches the prototype with the prototype's JSON.
- **SG-013** Chart assets enqueued, hash-versioned — DoD: one version everywhere (gate check 4 equivalent).

### E2 Data pipeline (M2)
- **SG-020** Converter inputs as arguments; documented one-command rebuild — DoD: `README` line; runs from a clean checkout.
- **SG-021** `split.py`: per-page JSON ≤ 300 KB — DoD: sizes in the build log.
- **SG-022** Excel export generated from the JSON with the pages' labels and footnote — DoD: a reader opens it; one figure checked against the page.
- **SG-023** Data round rehearsal with the current workbooks — DoD: checklist in `12` §3 executed; diff reviewed.

### E3 Registration and gate (M3)
- **SG-030** Role, meta, registration form per the field list; e-mail confirmation — DoD: a company and a candidate account created on staging.
- **SG-031** Gate on guide templates; redirect back after login; logout — DoD: logged-out hit on every guide URL redirects; logged-in reads.
- **SG-032** Consent recorded with timestamp; privacy text linked — DoD: visible in the user record.
- **SG-033** CRM hand-off on confirmation — DoD: SG-001 path receives the six fields.

### E4 Forms and media (M4)
- **SG-040** Ajánlatkérés and join forms with e-mail, entry, CRM — DoD: both deliver; spam protection verified.
- **SG-041** Video embeds after consent for 7 areas + 2 case studies; key thoughts for 4 areas — DoD: with the client's links; placeholders gone.
- **SG-042** Header Ajánlatkérés target confirmed (`08` #8) — DoD: decision recorded.

### E5 Home page and QA (M5)
- **SG-050** Teaser/home per the client's structure demo with the received copy, logos, podcast — DoD: matches the demo.
- **SG-051** Full measured pass (375, desktop) on staging; weights — DoD: numbers in the build log; under budget.
- **SG-052** Bértábla banner vs page note resolved with the client (`08` #13) — DoD: one wording.

### E6 Launch (M6)
- **SG-060** Go-live on the chosen path; `noindex` on guide pages; teaser indexable — DoD: live URL; a registration completes in production.
- **SG-061** Hand-over: marketing edits copy; developer runs a data round — DoD: both done unaided once.

### E7 Client items (content, not code)
- **SG-070..081** the items in `08-client-asks.md` #1–#12 — DoD each: received and on the page.

## 4. Blocked register

| Item | Blocked on | Unblocks |
|---|---|---|
| ADR-1..8 | client | M0 onward |
| CRM target | client | SG-001, SG-033, SG-040 |
| Home structure demo | client (promised week of 2026-09-21) | SG-050 |
| Four Talent Insight numbers | client | content completeness only |
| Videos, key thoughts | client | SG-041 |
| EN | client decision + copy | out of Release 1 |

## 5. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| The client expects the Sheets-API architecture from the July spec | disagreement at M0 | §3 of `11-architecture.md` puts the reasons in writing; the scheduled import is the compromise |
| Registration friction reduces readers | fewer leads | five fields, confirmation only; measure conversion (`12` §9) |
| The bértábla is still "sample values" per its own banner at launch | credibility | SG-052 before M6 |
| Copy keeps changing during the build | rework | SG-003 content freeze |
| The prototype and production diverge during parallel fine-tuning | two truths | every prototype change is a `SOURCES-AND-GAPS.md` entry; production transcribes from the prototype at M5, not before |

## 6. Release scope

**Release 1:** the seven page kinds + home teaser, HU, gated, Excel export, forms,
video embeds, GTM events. **Not in Release 1:** EN edition (ADR-7), scheduled Drive
import (ADR-2 upgrade path), Generáció / Cégtulajdon filters (the survey does not
carry them — gap 5), any redesign.
