# business.direct — delivery plan, operating model and stakeholder sign-off

*For the delivery lead, the owner and the stakeholders who sign off. What this document holds:
the milestones and the nine sprints with an acceptance test each (§2, §2b), the development broken
into deliverable pieces with dependencies and increments (§2c), the sprint-0 checklist,
every issue with a Definition of Done (§3), the blocked register (§4), risks with owners and
triggers (§5), owners, dates relative to the go, reviews, the decision path and change control
(§5b), the release scope (§6), the operating model — onboarding, running, support, incidents,
change, offboarding (§7) — and the stakeholder sign-off sheet (§8). Estimates are for a team of
two developers with the owner as product lead and are unvalidated until the team is named; they
assume the ADRs in `architecture.md` stand and the first customer's onboarding inputs
(`first-customer-classscout.md`) arrive as §4 says.*

## 0. Conventions

Issue ids `BD-<milestone>-<n>`. A milestone ships to production behind a feature flag per
instance (`platform_id`). "Measured" means a number in the build log, not a claim.

## 1. Global Definition of Done

- The SSOT term is used in code, UI and docs; new terms are added to `business-logic.md` first.
- No outbound path exists outside the outbox (ADR-4); a test proves a Server Action cannot send.
- Every message has a `messages` row, a `why`, and an opt-out or preference link.
- Cap and consent checks have tests for the race (enqueue and send).
- Accessibility: 44 px targets below 980, one `h1`, alt text, keyboard reachable.
- The gate is green: lint, unit, an end-to-end run of the flow the issue touches.

## 2. Milestones

| M | Name | Weeks | Ships |
|---|---|---|---|
| M0 | Foundation | 1–2 | repo, SSO, MongoDB, connector for Your Field with sync, the operator console shell with the three views' navigation, feature flags, **the policy record and gate** |
| M1 | Provider sales and conversations | 3–5 | sequences, Resend out + inbound, threads, drafted replies (AI optional), pipeline, apply-to-manage through `claim-requests`, provider view (today, conversations, knowledge), the family's ask |
| M2 | Social publishing | 6–8 | post drafts from the catalogue, approval queue, calendar, Meta adapter (IG + FB) publish, comments/DMs inbound, audit snapshots |
| M3 | Families | 9–10 | preferences by signed link, consent capture, caps, Sunday digest, saved-provider alerts through platform push, Stop |
| M4 | Intelligence and pages | 11–12 | overview tiles on real numbers, the intelligence recap screen, market radar note, generated pages written through the connector, operations dashboards |
| M5 | Campaigns, retention and upgrades (phase 2) | 13–15 | provider campaigns from the card with audiences from the platform's saves, results screen, products and Stripe entitlements, the family inbox's reason line, the retention job and screen (D41) |
| M6 | Second-instance proof | 17 | a second connector against the reference API's recorded fixtures, a second policy record and instance row, strings from a dictionary; proves ADR-2 without assuming a second client |

## 2b. Sprints (two weeks each; what ships, what the owner sees at the review, what it needs)

| Sprint | Weeks | Issues | Acceptance test at the review (run on the console, measured) | Needs before it starts |
|---|---|---|---|---|
| S0 setup | 0 | — | the accounts of research VI §14 exist; `env.ts` boots; `/api/health` is green; SSO signs the owner in as operator | Vercel Pro, Atlas M0, Upstash, Resend domain DNS, Claude key, the SSO client; **Meta App Review submitted** |
| S1 foundation | 1–2 | BD-0-1 … BD-0-11 | the demo sample cached by `sync`; every screen of the specification navigates with empty states; Simple and Advanced modes; the Policy screen shows the first client's record with `postal_address` marked missing and the features it blocks; a Server Action that tries to import a channel fails the build; the outbox drains a stub row in ≤ 60 s | — |
| S2 provider sales | 3–4 | BD-1-1, 1-2, 1-4, 1-6, 1-10, 1-11, 1-12, 1-14, 1-7 | with a test policy record: step 1 sent by Resend to a test provider in score order; the reply lands in the thread within a minute; stage moves *identified → contacted → replied* by events only; a template without `{postal_address}` cannot be approved; bounce ≥ 2 % pauses; "not my program" excludes the address | a sending domain (P-11 DNS); a test policy record |
| S3 conversations | 5–6 | BD-1-3, 1-5, 1-8, 1-9, 1-13 | an inbound e-mail, a platform message and a missed call each become an enquiry with a drafted answer in ≤ 1 min; AI on / off both marked; apply-to-manage writes a claim request when keyed, else an operator task; a family's ask to an unclaimed provider becomes sales step 2 | P-7 for the keyed branch (else the task branch is demonstrated) |
| S4 social publishing | 7–8 | BD-2-1, 2-2, 2-3, 2-4, 2-6, 2-5, 2-9 | a draft from a catalogue event → approve → published to the test Page and Instagram account at its slot ± 5 min; the snapshot in Blob; a comment on the post arrives by webhook with a drafted reply; the weekly anchor on the calendar | **Meta App Review approved** (submitted S0); a test Page + Instagram account |
| S5 the clip engine | 9–10 | BD-2-7, 2-10, 2-8, 2-11 | a 20-minute recording uploaded on the provider's Media screen → four captioned 9:16 clips with C2PA in the queue in ≤ 10 min (measured); a recording flagged as showing children is refused without the consent confirmation, by the app and by the worker; a draft with "only 3 spots left" is refused | Fly.io app; Deepgram key; a C2PA certificate (self-signed for the pilot) |
| S6 families | 11–12 | BD-3-1 … BD-3-6, 3-8, 3-9 | a family opens a signed link, turns picks on → Sunday's digest arrives; a new session at a saved provider → push within 1 h (keyed) or an operator task; the cap race test (2 sends, 1 slot → 1 sent, 1 refused); Stop cancels queued rows in one transaction; the SMS toggle cannot turn on without a consent row | P-2 (digest clause) for a real send — the test instance runs with a test record |
| S7 intelligence | 13–14 | BD-4-1 … BD-4-13 | every overview tile names its source; `metrics` rolls yesterday's events; a rate flips to "measured" at 100 observations (seeded); the economics screen reads `assumptions`; the propensity score changes the sequence order; the holdout experiment configured; a generated page publishes only at readiness ≥ 3 of 4; the five alerts fire in a drill; a department earns auto-approval after four clean weeks (clock-seeded) and loses it on an edit | P-6 for real tiles (else labelled sample) |
| S8 campaigns, retention and upgrades | 15–16 | BD-5-1 … BD-5-6, BD-1-15 | a managing provider sees a campaign draft with the audience count before approval; a family at the cap receives nothing; Stripe test-mode checkout → `entitlements` → *upgraded* → card flag (keyed) or task; the results screen from the message log; cancellation within 14 days refunds (R32) | Stripe test keys; P-12 prices (sample until then) |
| S9 second-instance proof | 17 | BD-6-1, 6-2 | a second instance row + policy record + connector against fixtures runs every job without code change; the gate blocks everything on the unfilled record | — |

Two developers, nine sprints, seventeen weeks, matching the milestone table; a sprint that loses
its external dependency (S4 without Meta's approval) swaps with the next one — S5 and S6 need
nothing from Meta.

### Sprint 0 checklist (the day before S1)

1. Repository created (`architecture.md` §3), `main` protected, preview deployments on.
2. Vercel project with the environment of blueprint §9; `CRON_SECRET`; the crons of the cron table in `vercel.json`.
3. Atlas M0 cluster, the collections and indexes of technical design §2 + blueprint §5 (a `scripts/indexes.ts`).
4. Upstash database in `us-east-1`; Blob store.
5. Resend: domain verified (SPF, DKIM, DMARC), `reply.` MX, webhook endpoint with the signing secret.
6. Meta developer app under the platform's Business Manager; test Page and Instagram professional account; App Review **submitted** with the screencast of the approval → publish flow.
7. Claude API key with a spend limit; `DRAFTER=template` until the knowledge files are loaded.
8. Sentry project; Better Stack monitor on `/api/health`.
9. DoneIsBetter SSO client for the machine (owner).
10. The first customer's policy record entered on the Policy screen from `responsible-data.md` §6 — with `postal_address` empty until P-1.

## 2c. The development, broken into deliverable pieces (the work breakdown, D49)

*Approved by the first customer on 2026-09-20 (D48). Every piece below is a vertical slice that a
stakeholder can see working at its review: what it delivers, the modules it is built from
(`architecture.md` Part C §4), the issues it closes (§3), the sprint it lands in (§2b), what it
depends on, the acceptance test, and its size (S ≈ 2 developer-days, M ≈ 5, L ≈ 10; unvalidated
until the team is named). A piece is done when its acceptance test passes on the console, the
gate is clean, and the measured result is in the build log. Each piece is one branch and one
pull request set; nothing is merged without its test.*

| # | Piece | Delivers (what the review shows) | Modules | Issues | Sprint | Depends on | Acceptance test | Size |
|---|---|---|---|---|---|---|---|---|
| **P0** | **Foundation** | the repository, SSO for the operator and the advertiser roles, the database models with `platform_id` and versions, the instance record, the console shell with every screen reachable in Simple and Advanced mode, the outbox skeleton with a stub adapter, the health endpoint | `lib/`, `db/`, `app/(console)`, `outbox` (skeleton) | BD-0-1, 0-2, 0-3, 0-5, 0-6, 0-9 | S1 | S0 accounts | an operator signs in and sees every screen with empty states; an advertiser sees only its own record (test); a Server Action that imports a channel fails the build; a stub outbox row drains in ≤ 60 s; `/api/health` is green | L |
| **P1** | **Policy record and gate** | the Policy screen as the onboarding checklist; the gate that blocks every feature whose fields are missing and says why; the policy basis on every message | `policy` | BD-0-7, 0-8, 0-11 | S1 | P0 | each of the ten gate rows blocks its feature when its field is missing (test per row); the screen shows set / missing / placeholder per field | M |
| **P2** | **Listings connector and sync** | the first customer's listings cached hourly with diff events; the listings table with contact chips, propensity score, stage and the drawer (card, history, thread) | `catalogue`, `pipeline` (score, stages) | BD-0-4, 1-4, 1-14 | S1 | P0 | the demo sample cached; a changed `updatedAt` produces one diff event (fixture test); an illegal stage move is refused, an override is logged with who and why; the score orders the table | M |
| **P3** | **Simple mode: Home, approvals, templates, knowledge, help** | the owner's twenty minutes: ranked recommendations with the reason and one button, the one safe press, the approvals list, templates that copy into the product, the knowledge files editor, the What-is-this panels and How to use | `recommend`, `approvals`, `knowledge`, `drafting` (templates) | BD-0-9, 0-10, 2-2 | S1 | P0, P1 | the press runs only recommendations marked safe and logs each as the operator's (test); an edit removes the AI badge and stores the diff; a template copies into state and lands the operator on the edited item | M |
| **P4** | **Sales sequences and the sending guard** | the three-touch invitation in propensity order sent by e-mail to test addresses; the sending card (domain, warm-up, daily cap, bounce); the postal-address and opt-out footer enforced; "not my program" and unsubscribe honoured | `sequences`, `outbox` (checks), `channels/resend` (out) | BD-1-1, 1-2 (out), 1-10, 1-11, 1-12, 1-7 | S2 | P1, P2, P3; a sending domain | step 1 goes to the first batch in score order; a template without `{postal_address}` cannot be approved; bounce ≥ 2 % pauses; step 2 only where a save exists; an opted-out address is excluded from every later run (tests) | L |
| **P5** | **The reply inbox** | replies land in the thread within a minute with a drafted answer; the operator approves or edits; the stage moves to *replied* on the event; the classifier's vulnerability flag pauses marketing for that person | `channels/resend` (inbound), `conversations` (replies), `drafting` (answers) | BD-1-2 (inbound), 1-3 | S2 | P4 | an inbound e-mail lands in the right thread in ≤ 60 s (measured); AI on / off both produce a marked draft; "not now" pauses and opens a human task (test) | M |
| **P6** | **Enquiries: the advertiser's inbox** | a visitor's message, an e-mail and a missed call each become an enquiry with a drafted answer within a minute; the advertiser approves; reply time logged; a visitor's ask to an unclaimed listing becomes sales step 2 and the visitor is told | `conversations` (enquiries), `channels/twilio` (missed-call capture), `drafting` | BD-1-8, 1-9, 1-13 | S3 | P5 | three inbound kinds → three enquiries with drafts in ≤ 60 s; the ask to an unclaimed listing moves it to *contacted* with `by: family ask` and the visitor's thread shows the notice (tests) | L |
| **P7** | **Apply-to-manage and the advertiser's Today** | the invitation's *Apply* creates a claim request through the connector (keyed) or an operator task (unkeyed); the platform's confirmation moves the stage to *managing*; the advertiser's Today, Knowledge and Results shell | `catalogue` (writes), `pipeline`, advertiser screens | BD-1-5, 1-6 | S3 | P2, P5 | keyed: a claim request is written and *applied* set on 2xx; unkeyed: a task is written; the confirmation event sets *managing* (tests); the advertiser sees its thread, drafts and files | M |
| **P8** | **Social publishing** | drafts from catalogue events; the calendar and slots; publish to the test Page and Instagram account at the slot; comments and DMs arrive by webhook with a drafted reply; the audit snapshot; AI-content marking; the weekly anchor | `drafting` (social), `channels/meta`, `outbox` (publish), `conversations` (comments) | BD-2-1, 2-3, 2-4, 2-5, 2-6, 2-9 | S4 (or swapped with S5/S6) | P3; **Meta App Review approved**; a test Page and account | a draft exists only for a listing with news and never twice a week; a scheduled post publishes at its slot ± 5 min (measured) with a `messages` row and a Blob snapshot; a comment arrives with a drafted reply; the anchor and its cuts on the calendar | L |
| **P9** | **The clip engine and the pattern guard** | the media worker; a recording uploaded on the advertiser's Media screen becomes captioned 9:16 clips with C2PA in the queue; the consent confirmation for footage that shows children, enforced twice; the banned-pattern guard on every draft | `media`, `worker/`, `drafting` (patternGuard) | BD-2-7, 2-8, 2-10, 2-11 | S5 | P3; Fly.io, Deepgram, a C2PA certificate | a 20-minute recording → four clips with captions and credentials in ≤ 10 min (measured); a recording flagged as showing children is refused without consent by the app and by the worker; a draft with "only 3 spots left" is refused (tests per pattern) | L |
| **P10** | **Visitors: preferences, consents, caps, digest, alerts, Stop** | the signed preference link; consent capture with proof; the cap in Redis checked twice; the Sunday digest built and sent by preference; alerts on a saved listing's new session; Stop in one transaction; the public neighbourhood newsletter | `families`, `outbox` (caps), `channels/platformPush` | BD-3-1 … 3-6, 3-8, 3-9 | S6 | P1, P4; P-2 for a real send | a visitor changes a channel without a password; the SMS toggle is impossible without a consent row; two sends against one slot → one sent, one refused; the digest is built from saved + nearby and does not count toward the cap; Stop cancels queued rows in one transaction; no child's name reaches an advertiser (tests) | L |
| **P11** | **Events, metrics and the Economics screen** | the append-only event log; the nightly metrics with assumption → measured at 100 observations; the propensity score job; the Economics screen reading `assumptions`; operator hours; the holdout experiment; earned auto-approval; capture measured | `analytics`, `pipeline` (score job), `approvals` (autoApprove) | BD-4-6, 4-7, 4-8, 4-9, 4-10, 4-11, 4-12, 4-13 | S7 | P4, P5, P10 | every leaf of the metrics tree has an event; a seeded rate flips to measured at 100 (test); the score changes the sequence order; a department earns auto-approval after four clean weeks and loses it on an edit (clock-seeded test); the experiment is configured | L |
| **P12** | **The Monday recap and the overview on real numbers** | every tile names its source and "sample" disappears where a real number exists; *needs you* lists approvals, replied-not-applied, advertisers at risk, integrations, the next dollar, the gate; the market radar note | `analytics` (recap), `recommend` | BD-4-1, 4-2, 4-5 | S7 | P11 | every tile has a source; the radar note is filed by the operator; the five alerts fire in a drill | M |
| **P13** | **Generated pages** | category × area pages computed with readiness; published only at ≥ 3 listings and readiness ≥ 3 of 4 through the connector | `pages` | BD-4-3, 4-11 (readiness) | S7 | P2, P7 (key) | a page publishes only at readiness ≥ 3 of 4 with JSON-LD and a sitemap entry (test); below it the screen says why not | S |
| **P14** | **Operations** | Sentry, Better Stack on `/api/health`, the dashboards and alerts, the retention (TTL) job, the weekly delivery audit by neighbourhood, the runbooks | `lib/log`, `analytics` (audit), ops | BD-4-4, 0-11 (audit) | S7 | P0 | the five alerts of `architecture.md` §9 fire in a drill; the delivery audit runs weekly; a dead outbox row appears in the failed tab | S |
| **P15** | **Retention** | the nightly signals; one drafted touch per signal from the advertiser's own numbers; renewal reminders in Home's safe press; kept / lost into the churn rate; the Retention screen | `retention`, `drafting` (retain) | BD-1-15 | S8 | P7, P11 | a stale card, a renewal within 14 days and an unanswered enquiry each produce exactly one waiting draft; no draft contains a discount; kept / lost roll into `metrics_daily.churn` (tests) | M |
| **P16** | **Campaigns, placements and payments** | campaign drafts per card event with the audience shown before approval; audiences from the site's saves only; sending under preference and cap with the reason line; the placements, Stripe Checkout on the owner's account, entitlements, the card flag through the connector; the advertiser's Results | `campaigns`, `billing`, `catalogue` (audiences, flags) | BD-5-1 … 5-6 | S8 | P7, P10; Stripe test keys; P-12 prices | one draft per kind per card event; no uploaded list is possible (test); a visitor at the cap receives nothing; test-mode checkout → entitlement → *upgraded* → card flag or task; cancellation within 14 days refunds | L |
| **P17** | **Second-instance proof** | a second connector against the reference API's fixtures, a second policy record and instance row, strings from a dictionary; every job runs without a code change | `catalogue` (connector 2), i18n | BD-6-1, 6-2 | S9 | P1, P2 | the fixtures cached; every job runs on the second instance; the gate blocks everything on the unfilled record (tests) | M |
| **P18** | **First-customer onboarding** (runs alongside S0–S6, with the customer) | the policy record filled from `first-customer-classscout.md` Part C; the sending domain's DNS; the Meta app and review; the knowledge files from the workshop; the placements loaded; the first week in Simple mode; the first Monday recap read together | — (the operating model, §7) | — | S0–S6 | the customer's inputs by the sprint that needs each | the gate shows no blocked feature the pilot needs; the first recap read together; the first measured cohort on Economics at the end of S2 | M |

### Dependencies (what must exist before what)

```
 P0 foundation ─┬─▶ P1 policy gate ─┬─▶ P3 Simple mode ─┬─▶ P4 sequences ─▶ P5 reply inbox ─▶ P6 enquiries ─▶ P7 apply-to-manage
                │                   │                   ├─▶ P8 social publishing (Meta review)      │
                │                   │                   └─▶ P9 clip engine                          ▼
                ├─▶ P2 listings ────┘                   P10 visitors ◀────────────────────── P11 events & economics ─▶ P12 recap
                │                                        │                                            │
                └─▶ P14 operations                       └─▶ P16 campaigns & payments ◀──────────────┴─▶ P15 retention
                                                                                                 P13 pages · P17 second instance
 P18 first-customer onboarding runs beside everything from S0 and feeds P1, P4, P8, P10 their real inputs
```

### What is usable when (the increments)

| After | Usable for the first customer |
|---|---|
| S1 (P0–P3) | the console on their listings: the policy checklist, the listings worked in propensity order, the owner's Home with recommendations — nothing sends yet |
| S2 (P4, P5) | the sales flow end to end on test addresses: invitation, replies, drafted answers, the sending guard |
| S3 (P6, P7) | every enquiry answered from the advertiser's inbox; apply-to-manage; the first managing advertisers |
| S4–S5 (P8, P9) | the week's content published to the channels; clips from real footage |
| S6 (P10) | visitors' preferences, the Sunday digest, alerts, Stop — the demand side live |
| S7 (P11–P14) | the owner's economics on measured numbers; the Monday recap; generated pages; operations |
| S8 (P15, P16) | retention running; campaigns and placements sold; the three jobs complete |
| S9 (P17) | the second site provable as a record and a connector |

### Rules for every piece

1. One branch, one pull request set, the acceptance test in the description; merged only when the gate is clean and the test passed on the console.
2. The rule behind the piece (R-number) changes in `business-logic.md` first, then in the code, then in the copy.
3. A piece that loses its external dependency (Meta's review, a key, a certificate) swaps with the next one that does not need it; the swap is a line in the build log, not a re-plan.
4. The measured result of the acceptance test — the number, the time, the count — goes into the build log the day the piece is done.
5. Nothing sends to a real address until the policy record's fields for that feature are set and counsel has answered the question that concerns it (`responsible-data.md` Part B §6).

## 3. Issues

| Id | Issue | Definition of Done |
|---|---|---|
| BD-0-1 | Repo, Next.js 15, Mantine + GDS tokens from `architecture.md` | tokens resolve; the design-system page renders from the same CSS |
| BD-0-2 | DoneIsBetter SSO for operator and provider roles | operator sees all; provider sees only its `provider_id` (test) |
| BD-0-3 | MongoDB models per `architecture.md` §2 with `platform_id` and `version` | migrations; optimistic-concurrency test |
| BD-0-4 | `YourFieldConnector` + hourly `sync` | the demo sample cached; a changed `updatedAt` produces a diff event (test with a fixture) |
| BD-0-5 | Console shell: role switch, rail/bottom bar, deep links | the prototype's 13 screens reachable, empty states |
| BD-0-11 | Policy fields R30–R36 and the three gate rows; safeguarding state on the card; delivery audit by neighbourhood (R33) | fields set or the features stay blocked; the audit report runs weekly |
| BD-0-9 | Simple and Advanced modes; Home with recommendations; the one safe press (R29) | Simple shows Home, Approvals, Providers, Policy, How to use; the press runs only `auto` recommendations and logs each as the operator's (test) |
| BD-0-10 | What-is-this panels, How-to-use screen, Templates with "Use" | every screen has a panel; a template copies into state and the operator lands on the edited item |
| BD-0-7 | Policy record and gate (ADR-14) | a feature whose policy fields are missing does not run (test per row of framework §3); every message carries its policy basis |
| BD-0-8 | Policy screen as onboarding checklist | the operator sees set / missing / placeholder per field and what each blocks |
| BD-0-6 | Outbox + `send` worker + dead-letter | a Server Action cannot send (test); retry with backoff; lag metric |
| BD-1-1 | Sequence model and editor | steps, merge fields, opt-out footer mandatory (validation) |
| BD-1-2 | `ResendAdapter` out + inbound webhook (signed) | a reply lands in the right thread within 1 minute (measured) |
| BD-1-3 | Drafted replies with the AI switch | AI on: draft with `why`; AI off: template; both marked |
| BD-1-4 | Pipeline stage machine | only event-driven forward moves (test per row of §4); operator override logged |
| BD-1-5 | Apply-to-manage → `claim-requests` | needs the platform key (blocked B1); stage *applied* on 2xx |
| BD-1-6 | Provider view: invitation, today, knowledge | a provider sees its thread, its drafts, edits its files |
| BD-1-12 | Postal address merge field and template gate; opt-out register; bounce pause | a template without `{postal_address}` cannot be approved (test); bounce ≥ 2 % pauses (test) |
| BD-1-13 | A family's ask to an unclaimed provider → sales step 2; the family told | stage *contacted* with `by: 'family ask'`; the family's thread shows the notice |
| BD-1-14 | Stage history in the drawer; `contactKind` on the connector | last three changes with who and why; EU `person` addresses skipped without consent |
| BD-1-10 | Sending domain per instance with warm-up, cap, bounce guard | the outbox refuses a send past the limits (test); the sales screen shows the state |
| BD-1-11 | Three-touch sequence ordered by the propensity score | step 2 sends only where a save exists; recipients in score order (test) |
| BD-1-8 | Provider conversations: inbound (platform message, Resend inbound, Twilio missed call) → `enquiries` → drafted answer → approve / edit → same channel | reply time logged; the family's thread updated (phase 3) |
| BD-1-9 | Family "ask about a trial" from a saved provider | creates an enquiry as a platform message; visible in the provider's inbox within a minute |
| BD-1-15 | Retention job and screen (D41, R37): signals, one `retain` draft per signal from the advertiser's own numbers, renewal reminders under earned auto-approval | a stale card, a renewal within 14 days and an unanswered enquiry each produce exactly one waiting draft (test); no draft contains a discount (test); kept / lost events roll into `metrics_daily.churn` |
| BD-1-7 | "Not my program" and unsubscribe | the address is excluded from every future sequence (test) |
| BD-2-1 | `draft-social` job from catalogue events | drafts only for providers with news; no duplicate per week |
| BD-2-2 | Approval queue with edit diff | edited copy sets `ai=false`; the diff is stored |
| BD-2-3 | Calendar and slots | a scheduled post publishes at its slot ± 5 min (measured) |
| BD-2-4 | `MetaAdapter` publish + inbound comments/DMs | OAuth per page; a publish writes `messages` + a Blob snapshot |
| BD-2-7 | Clip engine (`MediaAdapter.clips`) and the provider's Media screen | a recording becomes captioned clips with the listing link in the queue, each `media.kind = real` |
| BD-2-10 | Media consent on the clip engine; captions; no child's name on a clip | a recording flagged as showing children is refused without the consent confirmation (test); every clip has captions (R30, R34) |
| BD-2-11 | Pattern guard and vulnerability pause | banned patterns refused (tests per pattern); "not now" pauses all marketing for that person and opens a human task (R32, R36) |
| BD-2-8 | Media labels and credentials | every generated asset has a C2PA credential and the platform label at publish (test per channel); a person-detection check blocks generation (R15) |
| BD-2-9 | Weekly anchor plan per neighbourhood × activity | the calendar shows the anchor and its cuts; `rules/social.md` keywords enforced in the draft |
| BD-2-6 | Drafted replies to comments and DMs with the listing link | operator approves; reply sent through the adapter; comments-answered metric |
| BD-2-5 | AI-content marking | published AI content carries the mark where Art. 50 applies |
| BD-3-1 | Signed preference links from the platform | a family changes a channel without a password; link expiry |
| BD-3-2 | Consent capture and log | SMS toggle impossible without a consent row (test) |
| BD-3-3 | Caps in Redis, double check | a race of 2 sends against a cap of 1 delivers 1 (test) |
| BD-3-4 | Sunday digest | built from saved + nearby-with-session; sent 18:00 by preference; not counted toward the provider cap (R3) |
| BD-3-5 | Saved-provider alerts through platform push | new session at a saved provider → push within 1 hour (measured) |
| BD-3-6 | Stop | every channel off and queued drafts cancelled in one transaction |
| BD-4-1 | Overview tiles on real numbers | every tile has a source; "sample" disappears |
| BD-4-2 | Market radar weekly note | from catalogue stats; filed by the operator |
| BD-4-3 | Generated pages through the connector | only ≥ 3 providers; JSON-LD; sitemap entry on the platform |
| BD-4-4 | Operations dashboards and alerts | the five alerts in architecture §9 fire in a drill |
| BD-4-9 | Propensity score job (ADR-13) | nightly; the sequence and call-list jobs read it; an audit row per change |
| BD-4-10 | Neighbourhood holdout experiment | two comparable neighbourhoods; read-out replaces "families per post" with a measured rate |
| BD-4-11 | Cohort LTV by channel; generated-page readiness | assumption → measured at 100 observations; a page publishes only at readiness ≥ 3 of 4 |
| BD-3-9 | Cap semantics: provider-originated only; consent proof on the row; age band in provider-facing text | digest and alerts do not count (test); the row shows when and where consent was given; no child's name reaches a provider (test) |
| BD-4-12 | Operator hours, batch approval, earned auto-approval | hours tile from events; one decision approves a week's clips; a department earns auto-approval after four clean weeks and loses it on an edit or a complaint (tests) |
| BD-4-13 | Capture measured; conversations line in the model | upgrades attributed to a delivered result within 30 days; the plan's MRR follows the conversations price |
| BD-3-8 | Public neighbourhood newsletter | joinable without an account; cross-recommendation between neighbourhoods; counts in the cap |
| BD-4-6 | Event log and nightly metrics (`events`, `metrics_daily`, `assumptions`) | every leaf of the metrics tree has an event; a rate flips from assumption to measured at 100 observations (test) |
| BD-4-7 | Economics screen on real metrics | the prototype's 23 inputs read from `assumptions`; measured ones are read-only and labelled |
| BD-4-8 | Next-dollar ranking in the recap; R17–R19 as jobs | cadence, content slots and the upgrade card follow the rules (tests per rule) |
| BD-4-5 | Intelligence recap screen | every tile names its source; "needs you" lists approvals, replied-not-applied, v1 integrations to connect |
| BD-5-1 | `draft-campaigns` job and the campaign model | one draft per kind per card event; kinds per `business-logic.md` §4 |
| BD-5-2 | Provider campaigns screen | approve / edit / skip; edit drops the AI badge; audience shown before approval |
| BD-5-3 | Audience resolution through the connector (`savesFor`, `familiesNear`) | no uploaded lists possible (test); counts logged |
| BD-5-4 | `send-campaigns` with preference and cap | a family at the cap receives nothing (test); the reason line on every message |
| BD-5-5 | Products, Stripe Checkout, entitlements webhook | first `active` → *upgraded* → card flag set through the connector |
| BD-5-6 | Provider results screen | what went out from the message log; plan ladder from entitlements |
| BD-6-1 | A second `PlatformConnector` (the reference API's shape, incl. `ingest`) against recorded fixtures | 431 reference listings cached from fixtures; `publishPage` exercised against a fixture server; no live write |
| BD-6-2 | Instance dictionary and legal footer per policy record | every user-facing string from the dictionary; the footer (postal address, opt-out wording) comes from the instance's policy record |

## 4. Blocked register

Every row below is an implementation prerequisite (`first-customer-classscout.md`), provided by ClassScout after acceptance; none blocks the presentation or the planning.

| # | Blocked | On | Unblocks |
|---|---|---|---|
| B1 | Writes to the platform (claim requests, notifications, pages) | prerequisite P-7: a key and the write contract | BD-1-5, BD-3-5, BD-4-3 |
| B2 | Social publishing | Meta app review for the platform's pages; prerequisite P-11 | BD-2-4 |
| B3 | SMS | Twilio account, consent text approved by counsel; prerequisite P-11 | BD-3-2's SMS branch |
| B4 | Real tiles | prerequisite P-6: platform analytics | BD-4-1 |
| B5 | Pilot provider | prerequisite P-9: one provider's real numbers | provider-view metrics |
| B6 | Product prices | prerequisites P-6 and P-12: the platform's real prices (assumed bundled base + provider-bought reach, D21) | BD-5-5 |
| B7 | Audience data | the platform's saves and family locations through keyed endpoints | BD-5-3 |
| B9 | Family, sign-up-source and booking events | the platform's analytics (prerequisite P-6) | BD-4-6's family leaves; the avid-family value |
| B8 | Stripe account | the platform's merchant account and tax setup | BD-5-5 |

## 5. Risks — with an owner and a trigger (phase E, D42)

| Risk | Effect | Owner | Trigger (when it becomes an action) | Mitigation |
|---|---|---|---|---|
| Meta App Review takes weeks | publishing (S4) slips | delivery lead | review not approved by the end of S2 | submitted in S0; swap S4 with S5/S6; publish to Facebook first if Instagram lags |
| The site's public API changes without notice (no reference page) | sync breaks | delivery lead | schema-drift test fails, or a sync returns < 90 % of the previous count | contract tests against fixtures; alert on drift; ask the site for a versioned endpoint |
| A cap or consent bug | TCPA exposure | delivery lead; counsel on wording | the zero-violation alert fires once | ADR-3 double check; consent-before-SMS test; SMS stays off until the policy record allows it |
| Advertisers read the invitation as spam | pipeline stalls; domain reputation | product owner | bounce ≥ 2 % or complaints ≥ 0.1 % in a week | the sending guard pauses (R23); the copy names the advertiser's own page and the free claim; "not my program" honoured |
| AI drafts off-brand | operator trust | product owner | more than half of a week's drafts edited | knowledge files first; AI optional per department; edits feed the prompt |
| A vendor changes price or limit (claims register V1–V16, dated 2026-09-20) | cost or cadence | product owner | any vendor invoice > 1.5× the register's figure, or a limit hit | every vendor behind an interface; the register re-read at each contract |
| The cron tick (800 s on Pro) or a days-long wait is outgrown | a job cannot finish | delivery lead | a job's tick exceeds 600 s twice in a week | ADR-18: batching first, then Vercel Workflows, then Inngest on the same outbox rows |
| One operator is a bottleneck | queue grows | product owner with the first customer | approvals older than 48 h exceed 20 | Simple mode's press; batch approval; earned auto-approval; the queue shows age |
| Counsel's answers change a rule (`responsible-data.md` §6) | a feature waits or changes | counsel; product owner | any answer to §6 differs from the product team's reading | the gate blocks the feature until the record is updated; rules change in the SSOT first |
| The first customer's data is thinner than the pull (reviews, prices, contacts) | the content and citation levers underperform | first-customer contact | readiness < 3 of 4 on more than half of generated pages | pages publish only at readiness ≥ 3 of 4 (R6); card-quality asks in the onboarding file |

## 5b. Owners, dates and governance (phase E, D42)

| Track | Owner | Dates (G = the go) |
|---|---|---|
| Product (definition, price, rules, the D-register) | the owner (product lead) | decisions logged as D-numbers the day they are made |
| Delivery (the nine sprints, the acceptance tests, the gate) | a named delivery lead among the two developers | S0 at G; S1 G+1 w; S2 G+3 w; S3 G+5 w; S4 G+7 w (or swapped); S5 G+9 w; S6 G+11 w; S7 G+13 w; S8 G+15 w; S9 G+17 w |
| First customer (the ClassScout instance) | the customer's named contact | onboarding inputs (`first-customer-classscout.md`) by the sprint that needs each: §1 before S2's first real send, §2 before S3/S6's keyed features, §3 at G |
| Legal (`responsible-data.md` §6) | counsel | answers before S2's first real send; the DPA and terms before the contract |
| Claims and sources (`evidence.md`) | product lead | re-verified at every contract and every quarter |

**Reviews.** A sprint review every second Friday: the acceptance test of §2b run live on the
console, the measured numbers written into the build log, the next sprint confirmed or swapped.
A monthly owner review of the D-register, the risk table and the claims register.

**Decision path.** A product rule changes in the SSOT first, then in the code, then in the
prototype's copy — never the other order. An instance setting changes in its policy record and
onboarding file. A legal question goes on `responsible-data.md` §6 and blocks only the feature it concerns. A
price or packaging decision is a D-number by the owner.

**Change control.** No issue is added to a sprint without removing one of equal size; a new
integration or vendor is an ADR; a change that touches a rule R1–R37 carries its test.

## 6. Release scope

**Release 1 (M0–M3, sprints S1–S6, twelve weeks), re-cut by the audit (Q10) into two halves:** **1a, read-only against the platform** — the sales sequence with the sending guard and postal address, the reply inbox, the provider view (today, conversations, media, knowledge), the content queue with labels, economics on assumptions, the family's preferences by signed link; **1b, when the platform's key and events arrive** — claim requests, campaign audiences from saves, notifications, card flags, sign-up sources, bookings. The presentation says which half is which.

**Release 1 as first planned:** Your Field NYC; provider sales end to end; Instagram and
Facebook publishing with approval; family digest, alerts and preferences; caps and consent;
the operator's approval queue as the one gate. **Release 1.1 (M4, S7):** real intelligence,
the recap, generated pages, dashboards. **Release 2 (M5, S8):** provider campaigns, results,
products and Stripe upgrades. **Release 3 (M6, S9):** the second-instance proof. Out of scope until a
decision: TikTok and X, Google Business Profile, calendars.

## 7. The operating model — how the product is run for a customer

| Stage | What happens | Who | Done when |
|---|---|---|---|
| **Onboarding (week 1)** | the policy interview (the Policy screen filled together: identity and postal address, jurisdictions, audience model, channels and consent, defaults, cap, retention, disclosure, the site's privacy-policy clauses); the connector configured against the site's API and the channels connected; the knowledge workshop (voice, rules, offers as plain files, from the templates); the placements and the sending domain loaded; the first week run in Simple mode | the product team with the site's operator | the gate shows no blocked feature the pilot needs; the first Monday recap has been read together |
| **Running** | the operator's twenty minutes a day; the product team reads the health endpoint and the dead-letter tab daily, the sprint metrics weekly | operator; product team | — |
| **Support** | one channel (e-mail to the product team); response within one business day; a fix or a workaround named in the reply; anything touching a rule R1–R37 becomes a D-number before it ships | product team | — |
| **Incidents** | severity 1 (a send that should not have happened, data exposure): stop the outbox for the instance, notify the operator within the hour and per the DPA, runbook, post-mortem within five days; severity 2 (a channel down, a job failing): runbook, notice in the recap; severity 3: the next sprint | product team | the post-mortem's actions are issues in the plan |
| **Change** | a rule changes in the SSOT first, then the code, then the copy; an instance setting changes in its policy record; every change is a D-number or an issue | owner; delivery lead | the gate is clean |
| **Offboarding** | export of the owner's data (listings cache, state, messages, consents, events) within 30 days; deletion per the retention schedule; credentials and tokens revoked; the instance row closed | product team | the owner confirms receipt; deletion logged |

## 8. Stakeholder sign-off — who accepts what, by which criterion

| Stakeholder | Accepts | Criterion | Evidence |
|---|---|---|---|
| **The owner** (product lead) | the product definition and the specification; the rules; the plan | the definition is in the owner's words; every screen of the prototype has its section in the specification; every rule has its test in the plan | `product-definition.md`, `product-specification.md`, `business-logic.md`, this plan |
| **The first customer** (ClassScout) | the value the product computes for them; their instance's policy record; the onboarding inputs and dates | the Economics screen runs on their listings; the record shows what each missing field blocks; every input has an owner and a sprint | `economics.md` §3, the Policy and Economics screens, `first-customer-classscout.md` |
| **The delivery lead** | the architecture and blueprint; the sprints and acceptance tests; the operating model | a developer can build from the blueprint; every sprint has an acceptance test the owner can watch; the runbooks exist | `architecture.md`, this plan §2b, §7 |
| **Counsel** | the responsible-data record, the product's processor position, the ten questions | every legal sentence carries the disclaimer; the questions are answered or scheduled | `responsible-data.md` §6 (counsel list) |
| **Every stakeholder** | the evidence | every figure in the stakeholder documents has a row with its source opened | `evidence.md` |

Acceptance is recorded as a D-number with the date and the stakeholder's name; an open point is
an issue in §3 with an owner, never a footnote. **Recorded: the first customer (ClassScout) approved
on 2026-09-20 (D48), reported by the owner.**
