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

## Round 1b — 2026-09-19 — presentation, deep links, technical package (D19)

**Built.** `docs/bemutato.html` (English, the product's tokens, standalone, four steps with
phone previews and a desktop preview of the prototype, what is real, six asks, what comes
next). `app.js`: `?view=platform|provider|family&screen=<id>` deep links so the previews
and the docs open the right screen (`assets/app.js?v=3`). Docs `10`–`14` rendered by
`build.py`; the two hand-written docs pages gained the package links.

**Measured** (app browser pane, 2026-09-19): presentation at 1440 — five iframes load the
intended screens (overview, overview, provider sales, Brooklyn Force Soccer, What arrives),
`scrollWidth` 1440; at 390 — `scrollWidth` 390, every link ≥ 44 px, 0 console errors.
`architecture.html` at 390: the two ASCII diagrams scroll inside their `pre` (682 and
610 px content in a 358 px box), page width 390. `python3 check.py` → `GATE: CLEAN`
(216 files, 5,827 references).

## Round 2 — 2026-09-19 — editors real, tablet measured (D20)

**Built.** The sequence card's *Edit* opens the subject and body in place (save keeps the
sequence waiting, in the operator's words, without the AI badge; approve then sends). The
reply card's *Edit* opens the draft in place; *Save and send* sends the edited text and
writes it to the provider's thread. `assets/app.js?v=4`. Nothing else changed.

**Measured** (app browser pane, 2026-09-19): at **1024 × 768** the rail shows, tiles
auto-fit, `scrollWidth` 1024 on every screen and view; at **768 × 1024** the phone
navigation (bottom bar, no rail) as `05-layout-specs.md` specifies, tiles two-up on the
overview, every control ≥ 44 px, `scrollWidth` 768 on every screen and view; edited
sequence shows the new subject and loses the AI badge; edited reply appears in the
provider's drawer thread; 0 console errors. `python3 check.py` → `GATE: CLEAN`.

## Round 3 — 2026-09-19 — phase 2: campaigns, upgrades, recap (D21–D24)

**Built** (`assets/app.js?v=5`). Provider view: *Campaigns* — drafts built from the card
(trial class, open spots, announcement, registration; the fallback "hello" when the card
has none), audience line (sample counts), approve / edit / skip; *Results* — six tiles,
"what went out" from this session's approvals, the plan ladder; *Today* — the campaigns
department reads from state, "Reach more families" with the platform's three products
(sample prices), *Choose* → *upgraded*. Platform: *Intelligence* screen (six tiles, by
department, market radar from the catalogue, needs-you); the drawer shows a managing
provider's plan; integrations carry v1 / later (D21). Family inbox: "From providers" shows
approved campaigns from saved providers with the reason line, by preference. New doc
`09-business-logic.md`; SSOT, architecture (ADR-9, ADR-10), technical design, plan (M5,
seven issues, B6–B8), token map, layout spec, brief and presentation updated.

**Measured** (app browser pane, 2026-09-19): at 390 — intelligence, integrations, provider
today (locked and managing), campaigns, results, family inbox: `scrollWidth` 390, every
control ≥ 44 px; the campaign path (edit → save and approve → approve) leaves states
Scheduled · Scheduled · Awaiting; results lists 2 items; *Choose* moves the stage to
Upgraded (drawer badge) and the recap sums $49 / month; the family inbox shows 2 campaigns
with the reason line; 0 console errors. At 1440 — intelligence, campaigns, results, today:
`scrollWidth` 1440, one `h1`, 0 console errors. `python3 check.py` → `GATE: CLEAN`.

## Round 4 — 2026-09-19 — phase 3: conversations (D25)

**Built** (`assets/app.js?v=6`). Provider *Conversations*: three sample enquiries per
provider (platform message, missed call, e-mail) with answers drafted from the provider's
`knowledge/faq.md` and `offer.md` and the card (next session, trial policy, ages, the
coach's first name from the card's e-mail); tiles for waiting, answered, reply time and
missed calls texted back, computed from state; approve / edit / skip. *Today*'s "Waiting for
you" now shows enquiries (it showed the platform's replies to the provider — wrong side).
Family *Saved*: *Ask about a trial* on every saved provider → an enquiry from Maya at the
top of that provider's inbox; her inbox's *Your conversations* shows the thread and the
approved answer. Platform *Social publishing*: approving a post creates a sample comment
with a drafted reply that links to the listing; in the queue, the approvals list and the
pending count; *Intelligence* counts comments answered.

**Measured** (app browser pane, 2026-09-19): at 390 — social (comment arrives on approve,
edit → save and reply → Sent), provider today (1 enquiry shown, link "3"), conversations
(3 cards; approve + edit-save → tiles 1 · 2 · 4 min · 1), family saved → ask → inbox
thread "Sent just now"; provider inbox shows "Maya · Leo (5) · Park Slope" first (4 cards);
approve → the family's thread shows the answer; results tile "3 / 4"; `scrollWidth` 390
throughout, every control ≥ 44 px, 0 console errors. At 1440 — conversations via the
`&stage=managing` deep link: 3 cards, one `h1`, `scrollWidth` 1440, 0 errors.
`python3 check.py` → `GATE: CLEAN`.
