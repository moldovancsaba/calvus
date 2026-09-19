# business.direct — build log

Every round: what was built, from which decision, what was measured. The gate is
`07-gate.md`; the standard is `PROTOTYPING.md` §5–6.

## Round 1 — 2026-09-19 — the prototype (D16–D18)

**Built.** `index.html` + `assets/app.css` (layout, mirrors the gate-2 frames) +
`assets/app.js` (state and screens). Tokens and components untouched since gate 1
(`assets/tokens.css`, `assets/components.css`).

| View | Screens | Driven by |
|---|---|---|
| Platform | Overview · Social publishing · Provider sales · Approvals · Providers · Generated pages · Integrations · Knowledge and rules | 252 real providers; the pipeline, posts, sequences, replies and AI toggles in memory |
| Provider | Today (invitation → apply → managing) · Knowledge | the persona select lists the 60 first providers with an e-mail; default Brooklyn Force Soccer (D13) |
| Family | Inbox (a published post, the weekly picks digest, a provider text) · Saved · Preferences | Maya, Park Slope, two children (D13); saved providers are real; nearby providers are real Park Slope rows with a next session |

**What moves.** Approve / edit / skip a post → scheduled on the calendar and shown in the
family's inbox as published. Approve the invitation → 130 providers *contacted*, three
sample replies with drafted answers in the inbox, three providers *replied*. Approve a reply
whose text says "yes" → *applied*. The drawer's stage chips move a provider by hand. The
provider's "Apply to manage" → *managing* and the today screen changes shape. AI toggles
per department; the social toggle relabels every waiting draft. The family's toggles change
what the inbox shows; "Stop" turns everything off. Knowledge files are editable textareas.

**Declared.** The banner under the top bar says it on every screen: real providers, sample
activity, nothing sends, state resets on reload. Every tile says *real* or *sample*.

**Measured** (app browser pane, DOM audit, 2026-09-19): at 1440 and 390 every screen
`scrollWidth == innerWidth`; 0 elements past the viewport outside the scrolling table
container; at 390 every button, link, select and input ≥ 44 × 44; one `h1` per screen;
every `img` has `alt`; 0 console errors through the full click path (all screens, all
actions, both widths). Two findings fixed on the way: the digest's meta line inherited
`white-space: nowrap` and pushed the family inbox to 475 px; the preference toggles were
36 px wide. `python3 check.py` → `GATE: CLEAN`.

**Not built, on purpose.** Sequence and reply editing show a toast instead of an editor (the
copy lives in the knowledge files); tablet 1024 is the phone layout with wider cards
(`05-layout-specs.md`); no persistence (D17).
