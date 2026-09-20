# business.direct — build log

Every round: what was built, from which decision, what was measured. The gate is
`gate.md`; the standard is `PROTOTYPING.md` §5–6.

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
and the docs open the right screen (`assets/app.js?v=3`). Docs `business-logic.md`–`architecture.md` rendered by
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
`business-logic.md`; SSOT, architecture (ADR-9, ADR-10), technical design, plan (M5,
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

## Round 5 — 2026-09-19 — economics and planning (D26)

**Built** (`assets/app.js?v=7`, `app.css?v=3`). Platform *Economics*: eight tiles (CAC
managing / upgraded, LTV, LTV : CAC with the 3 : 1 rule, payback, value of an avid family,
avid families, cost per family from content), the next-dollar table (touch · call · content
ranked by expected LTV per $), the quarter's funnel strip, a 12-month plan with churn and
content cost, and 23 editable inputs grouped B2B / B2C with the source of each default in
its label; every figure recomputes on input and the focused field is kept. The recap's
"needs you" names the next dollar; the provider's results gain a "your return" line.
Layout fix: `main` now `align-content:start` — an empty-state card no longer floats mid-page
on short screens.

**Measured** (app browser pane, 2026-09-19): at 390 — `scrollWidth` 390, all 23 inputs
≥ 44 px, three next-dollar rows, twelve plan rows; changing the reply rate to 10.7 moved
CAC (managing) from $300 to $156 and LTV : CAC from 0.7 to 1.3 with focus retained; 0
console errors. At 1440 — `scrollWidth` 1440, the empty state sits 46 px under the title.
`python3 check.py` → `GATE: CLEAN` (exit 0).

## Round 5b — 2026-09-19 — the decision flow in the presentation, research III (D27)

**Built.** `bemutato.html`: a new section "How the machine decides — the data-driven flow"
(events → nightly metrics → the next dollar → a person approves → measure and adjust the
rules, plus the first finding with links to Economics and Research III); the hero's third
number is now the loop. `01c-research-data-driven-marketing.md` rendered as
`research-3.html` and linked from every docs page; asks #11 (P10–P12).

**Measured** (app browser pane, 2026-09-19): presentation at 390 — five sections, six
flow cards, `scrollWidth` 390, every link ≥ 44 px, 0 console errors.
`python3 check.py` → `GATE: CLEAN` (exit 0).

## Round 6 — 2026-09-19 — the research implemented (D28)

**Built** (`assets/app.js?v=8`). Platform: providers table gains a **propensity score**
column and sorts by it; the invitation sequence lists its **four steps** (three touches then
the call task) with recipients in score order; a **sending infrastructure** card (domain,
warm-up day 31 of 42, cap 60/day, bounce 0.8 %, reply within one business day); generated
pages show **readiness for AI citation** (verified · sessions · reviews, x of 4); social
publishing gains **this week's anchors** (three neighbourhoods by provider count — the
experiment's treatment and holdout first — each with its cuts) and the **media department**
(four adapters, clips v1, rules R15 / R20 / R21); every post card carries a **real media /
generated** label; the overview counts neighbourhood letters; economics shows the
**running holdout** and **cohorts by channel** with assumption / measured basis. Provider:
a **Media** screen — upload a recording (sample) → three clips into the platform's queue
marked real media; the product cards on Today appear only when delivered value exceeds
the cheapest product (R19). Family: the public neighbourhood newsletter in preferences.
`rules/social.md` carries the anchor, keyword and media rules.

**Measured** (app browser pane, 2026-09-19): at 390 — providers (7 columns, first score
100), sales (4 steps, sending card), pages (readiness 3 of 4), social (five sections, 7
real-media badges, holdout and treatment badges), economics (five sections, cohort rows),
today (R19 line), media (upload → 3 clips; queue shows 3, approvals 14), prefs (six rows):
`scrollWidth` 390 everywhere, every control ≥ 44 px, 0 errors in a fresh load (the tab's
console kept one error from a load before the fix — `score` used before its definition —
which moved the definition up). At 1440 — social anchors "Swimming in Upper West Side ·
Gymnastics in Upper East Side · Soccer in Brooklyn", provider media: `scrollWidth` 1440.
`python3 check.py` → `GATE: CLEAN` (exit 0).

## Round 7 — 2026-09-19 — the audit implemented (D30)

**Built** (`assets/app.js?v=9`). Q1 cap copy and rule (`rules/consent.md`, preferences,
campaign cards); Q2 `{postal_address}` in the invitation footer, the provider's received
e-mail, and a gate line on the sequence card (address · opt-out · recipients after
opt-outs); Q3 reachable nearby = 30 % opted in; Q4 an ask to an unclaimed provider creates
the "a family asked" sales card, moves the provider to *contacted* by `family ask`, and the
family's thread says the provider was told; Q5 R23 in `sendInvitation` (bounce ≥ 2 % blocks,
recipients paced at the daily cap, opt-outs excluded), the R19 60-day floor line, the
disclosure line on an unedited AI answer; Q6 score signals and `S.optOut` ("not my program"
excludes); Q7 `S.approvalsMade` → an operator-hours tile, *Approve all clips from real
footage* batch button, the FAQ department's "week 1 of 4" earned auto-approval and reminders
marked earned; Q8 capture measured on the avid-family tile; Q9 providers see "a child of 6";
Q11 `setStage` writes `S.history`, the drawer lists the last three moves and any opt-out,
the SMS row shows the consent proof; Q12 the `convPrice` input feeds the plan's MRR.

**Measured** (app browser pane, 2026-09-19, 390 × 844): sales card shows the three gate
badges; the family's ask to an unclaimed provider produced the sales card, the *contacted*
stage with `family ask` in the drawer history and the notice in her thread; the invitation
went to "130 providers over 3 days"; enquiry heads read "Priya · a child of 6"; the sent
line carries the disclosure; batch approval scheduled 3 clips in one click; a purchase after
a campaign showed "capture measured: 1 of 1"; the conversations input at 99 changed the
plan's note; 24 inputs; `scrollWidth` 390 on every screen, every control ≥ 44 px, 0 errors
on a fresh load. Two slips caught by the browser before commit: a line comment that
swallowed the rest of a statement (`list is not defined`) and a signed shift that made a
sample audience negative (−20 nearby) — both fixed. `python3 check.py` → `GATE: CLEAN`.

## Round 7b — 2026-09-19 — the platform's policy applied (D31)

**Built** (`assets/app.js?v=10`). Children's names removed from the model: the family
persona is `kids: [{age: 5}, {age: 9}]`; every text — the inbox header, the digest line, the
SMS, the ask, the enquiry heads — reads "a child of N" / "your 5-year-old". Audit §1b of
the platform's policy and terms added.

**Measured** (390 × 844): inbox header "a child of 5, a child of 9", SMS "your 5-year-old's
trial", ask "is there a trial for my 5-year-old?", no child's name anywhere in the page
text (regex check), 0 errors. `python3 check.py` → `GATE: CLEAN`.

## Round 8 — 2026-09-19 — responsible data for every client (D32)

**Built** (`assets/app.js?v=11`). `S.policies` with two instance records (Your Field NYC /
ClassScout, the Hungarian reference) and `S.instance`; `policyGate()` with seven rows;
Platform → System → *Policy*: four tiles, the gate table, the ten principles, the record as
a six-card onboarding checklist with set / missing / placeholder badges, an instance switch;
the rail shows the number of blocked features; the invitation stops at the gate once with
the reason and continues as a sample on the second approval; the sequence card's gate line
reads "postal address missing — blocked in production (ask #15)"; the family inbox shows the
digest's policy gate; the recap's "needs you" counts blocked features; the top bar names the
client (ClassScout). The placeholder postal address was removed — the field is empty and
the gate says so.

**Measured** (390 × 844): policy screen 5 / 7 (provider e-mail and the digest blocked),
rail count 2, Hungarian instance 3 / 7; the gate line on the sequence; first approval →
the gate toast, second → "130 providers over 3 days"; digest gate note in the inbox; the
provider's received e-mail shows the missing-address footer; `scrollWidth` 390, every
control ≥ 44 px, 0 errors. `python3 check.py` → `GATE: CLEAN`.

## Round 9 — 2026-09-19 — two interfaces: Simple and Advanced (D33)

**Built** (`assets/app.js?v=12`, `app.css?v=5`). `S.mode` with a top-bar switch and
`?mode=`; `NAV_SIMPLE` / `NAV_ADV` behind a proxy; *Home* (Simple) with `recommend()` — the
policy gate, real-footage clips, this week's posts, the invitation (safe only when the gate
allows), replies, comments, the radar, the next dollar — each a card with the reason and a
button, and `runSafe` for the safe ones (R29); `HELP` texts for every screen with a
*What is this?* toggle injected under each title; *How to use* (routine, states, rules,
screens, documentation); *Templates* with "Use" for knowledge files (copied into the right
knowledge set), policy records (a new instance from a template, gate blocked until
confirmed) and sequences (a new waiting sequence). Help links and list links ≥ 44 px.

**Measured** (390 × 844 and 1440 × 900): Simple opens on Home with 5 recommendations, 2
safe; the press ran them (posts approved, radar filed; the invitation stayed waiting because
the gate blocks it); Advanced shows the overview and the full navigation; a knowledge
template landed in the provider's FAQ, a policy template created "Sports directory · EU"
at 3 / 7, a sequence template added a card; every control ≥ 44 px after two fixes (inline
help links, list links); `scrollWidth` 390 / 1440; 0 errors on a fresh load.
`python3 check.py` → `GATE: CLEAN`.

## Round 10 — 2026-09-19 — beyond children (D35)

**Built** (`assets/app.js?v=15`). Seven policy fields on both instance records; three gate
rows (clips from a recording that shows children; safeguarding on a card; any draft or
screen); the Policy screen's seventh card and the R30–R36 principle line; the provider's
Media screen asks "Children appear in this recording — written parental consent on file"
before *Upload*, and refuses the cut without it (R30); the provider hero shows
"Safeguarding: not verified by the platform (R31)"; `rules/voice.md` carries the banned
list, the pause words and the accessibility rule.

**Measured** (390 × 844): upload without consent → refused with the reason, 0 clips; with
consent → 3 clips; the hero's three badges; the policy gate 8 / 10 for Your Field, 4 / 10
for the unfilled reference record; the seventh card present; `scrollWidth` 390, every
control ≥ 44 px, 0 errors. `python3 check.py` → `GATE: CLEAN`.

## Round 10b — 2026-09-19 — the catalogue re-pulled; the presentation's phone layout

**Data.** `python3 data/fetch-yourfield.py` re-run the same evening: **253** providers
(+1: Kids In Sports NYC, Manhattan), 51 records updated (26 gained coordinates → 246, 18
new descriptions, 3 new verified fields), phone 181, sessions 74; e-mail 130, next
occurrence 83, trial 72 (34 free), announcements 26, claims 15 `unclaimed` / 238 unset
unchanged. Every figure in the docs, the presentation, the design-system samples, the hub
and the README updated; two earlier figures were wrong on the old pull too (48 free trials
was 34; 84 neighbourhoods was 83 on the cards — the facets list 21) and are corrected. The
overview tile now counts neighbourhoods from the file; the catalogue fetch carries a
cache-bust (`?v=`) to bump with every re-pull.

**Fixed.** The presentation's ask cards wrapped one word per line on a phone (the owner's
screenshot): a `<b>` and a bare text node were two grid items in a two-column grid; the text
is now one `<span>`. Measured at 390: 276 px text width, seven lines. A slip while adding
the cache-bust commented out the `.then()` and stopped the app from booting — caught in the
browser, fixed before commit.

**Measured** (390 × 844): overview tile 253, pipeline 253, every platform screen renders
with one `h1`, `scrollWidth` 390, 0 errors on a fresh load. `python3 check.py` →
`GATE: CLEAN`.

## Round 11 — 2026-09-20 — the consolidation (D44)

**What changed.** The product specification written; thirty-three documentation files merged and
renamed into the final set of twelve (plus the design set, six research rounds and the history);
eighteen redirect pages for the earlier names; the replacement notice removed; the renderer's page
list and both hand-written navigations regenerated; the gate rewritten for the final set; the app's
documentation links and comments updated (`app.js?v=23`, links only — no behaviour change).

**Measured** (browser pane, fresh tab, cache-busted): `product-specification.html`,
`business-logic.html`, `architecture.html` at 390 — scrollWidth 390, one `h1`, no overflowing
code block, no notice; `delivery-plan.html` at 1440 — scrollWidth 1440, the operating model and
the sign-off sections present; `ssot.html` → redirects to `business-logic.html`; the prototype in
Simple mode at 390 — Home with 8 recommendations, scrollWidth 390, no console errors. Gate:
`python3 check.py` exit 0, `GATE: CLEAN`, 48 files, 1 219 references in the project, 0 broken
across the repo.
