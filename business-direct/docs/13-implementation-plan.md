# business.direct — implementation plan

*Written 2026-09-19 on the architecture's ADRs; phase 2 (M5) added the same day; re-cut to
sprint level on 2026-09-20 (D37) from the system blueprint (`20-system-blueprint.md`) and the
service research (`01g-research-real-system.md`). Estimates are for a team of two developers and
the owner as product lead; they assume the ADRs (ADR-1 to ADR-25) stand as the build baseline and
the prerequisites in `19-implementation-prerequisites.md` arrive as §4 says. Every issue has a
Definition of Done; every sprint has an acceptance test the owner can watch; the blocked register
is honest about what waits on the client.*

## 0. Conventions

Issue ids `BD-<milestone>-<n>`. A milestone ships to production behind a feature flag per
instance (`platform_id`). "Measured" means a number in the build log, not a claim.

## 1. Global Definition of Done

- The SSOT term is used in code, UI and docs; new terms are added to `10-ssot.md` first.
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
| S1 foundation | 1–2 | BD-0-1 … BD-0-11 | 253 providers cached by `sync`; the thirteen screens navigate with empty states; Simple and Advanced modes; the Policy screen shows the first client's record with `postal_address` marked missing and the features it blocks; a Server Action that tries to import a channel fails the build; the outbox drains a stub row in ≤ 60 s | — |
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

1. Repository created (`20-system-blueprint.md` §3), `main` protected, preview deployments on.
2. Vercel project with the environment of blueprint §9; `CRON_SECRET`; the thirteen crons in `vercel.json`.
3. Atlas M0 cluster, the collections and indexes of technical design §2 + blueprint §5 (a `scripts/indexes.ts`).
4. Upstash database in `us-east-1`; Blob store.
5. Resend: domain verified (SPF, DKIM, DMARC), `reply.` MX, webhook endpoint with the signing secret.
6. Meta developer app under the platform's Business Manager; test Page and Instagram professional account; App Review **submitted** with the screencast of the approval → publish flow.
7. Claude API key with a spend limit; `DRAFTER=template` until the knowledge files are loaded.
8. Sentry project; Better Stack monitor on `/api/health`.
9. DoneIsBetter SSO client for the machine (owner).
10. The first client's policy record entered on the Policy screen from `18-responsible-data-policy-framework.md` §6 — with `postal_address` empty until P-1.

## 3. Issues

| Id | Issue | Definition of Done |
|---|---|---|
| BD-0-1 | Repo, Next.js 15, Mantine + GDS tokens from `14-token-map.md` | tokens resolve; the design-system page renders from the same CSS |
| BD-0-2 | DoneIsBetter SSO for operator and provider roles | operator sees all; provider sees only its `provider_id` (test) |
| BD-0-3 | MongoDB models per `12-technical-design.md` §2 with `platform_id` and `version` | migrations; optimistic-concurrency test |
| BD-0-4 | `YourFieldConnector` + hourly `sync` | 253 providers cached; a changed `updatedAt` produces a diff event (test with a fixture) |
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
| BD-5-1 | `draft-campaigns` job and the campaign model | one draft per kind per card event; kinds per `09-business-logic.md` §4 |
| BD-5-2 | Provider campaigns screen | approve / edit / skip; edit drops the AI badge; audience shown before approval |
| BD-5-3 | Audience resolution through the connector (`savesFor`, `familiesNear`) | no uploaded lists possible (test); counts logged |
| BD-5-4 | `send-campaigns` with preference and cap | a family at the cap receives nothing (test); the reason line on every message |
| BD-5-5 | Products, Stripe Checkout, entitlements webhook | first `active` → *upgraded* → card flag set through the connector |
| BD-5-6 | Provider results screen | what went out from the message log; plan ladder from entitlements |
| BD-6-1 | A second `PlatformConnector` (the reference API's shape, incl. `ingest`) against recorded fixtures | 431 reference listings cached from fixtures; `publishPage` exercised against a fixture server; no live write |
| BD-6-2 | Instance dictionary and legal footer per policy record | every user-facing string from the dictionary; the footer (postal address, opt-out wording) comes from the instance's policy record |

## 4. Blocked register

Every row below is an implementation prerequisite (`19-implementation-prerequisites.md`), provided by ClassScout after acceptance; none blocks the presentation or the planning.

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
| Counsel's answers change a rule (`24-legal-and-data-processing.md` §6) | a feature waits or changes | counsel; product owner | any answer to §6 differs from the product team's reading | the gate blocks the feature until the record is updated; rules change in the SSOT first |
| The first customer's data is thinner than the pull (reviews, prices, contacts) | the content and citation levers underperform | first-customer contact | readiness < 3 of 4 on more than half of generated pages | pages publish only at readiness ≥ 3 of 4 (R6); card-quality asks in the onboarding file |

## 5b. Owners, dates and governance (phase E, D42)

| Track | Owner | Dates (G = the go) |
|---|---|---|
| Product (definition, price, rules, the D-register) | the owner (product lead) | decisions logged as D-numbers the day they are made |
| Delivery (the nine sprints, the acceptance tests, the gate) | a named delivery lead among the two developers | S0 at G; S1 G+1 w; S2 G+3 w; S3 G+5 w; S4 G+7 w (or swapped); S5 G+9 w; S6 G+11 w; S7 G+13 w; S8 G+15 w; S9 G+17 w |
| First customer (the ClassScout instance) | the customer's named contact | onboarding inputs (`19`) by the sprint that needs each: §1 before S2's first real send, §2 before S3/S6's keyed features, §3 at G |
| Legal (`24` §6) | counsel | answers before S2's first real send; the DPA and terms before the contract |
| Claims and sources (`23`) | product lead | re-verified at every contract and every quarter |

**Reviews.** A sprint review every second Friday: the acceptance test of §2b run live on the
console, the measured numbers written into the build log, the next sprint confirmed or swapped.
A monthly owner review of the D-register, the risk table and the claims register.

**Decision path.** A product rule changes in the SSOT first, then in the code, then in the
prototype's copy — never the other order. An instance setting changes in its policy record and
onboarding file. A legal question goes on `24` §6 and blocks only the feature it concerns. A
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
