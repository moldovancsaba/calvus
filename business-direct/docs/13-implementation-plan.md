# business.direct — implementation plan

*Written 2026-09-19 on the PROPOSED architecture; phase 2 (M5) added the same day. Estimates are for a team of two
developers and the owner as product lead; they assume ADR-1 to ADR-8 stand and the open
asks in `08-client-asks.md` close in the first two weeks. Every issue has a Definition of
Done; the blocked register is honest about what waits on the client.*

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
| M0 | Foundation | 1–2 | repo, SSO, MongoDB, connector for Your Field with sync, the operator console shell with the three views' navigation, feature flags |
| M1 | Provider sales and conversations | 3–5 | sequences, Resend out + inbound, threads, drafted replies (AI optional), pipeline, apply-to-manage through `claim-requests`, provider view (today, conversations, knowledge), the family's ask |
| M2 | Social publishing | 6–8 | post drafts from the catalogue, approval queue, calendar, Meta adapter (IG + FB) publish, comments/DMs inbound, audit snapshots |
| M3 | Families | 9–10 | preferences by signed link, consent capture, caps, Sunday digest, saved-provider alerts through platform push, Stop |
| M4 | Intelligence and pages | 11–12 | overview tiles on real numbers, the intelligence recap screen, market radar note, generated pages written through the connector, operations dashboards |
| M5 | Campaigns and upgrades (phase 2) | 13–15 | provider campaigns from the card with audiences from the platform's saves, results screen, products and Stripe entitlements, the family inbox's reason line |
| M6 | Second instance | 16–17 | Sportolok connector, Hungarian dictionary, legal footers; proves ADR-2 |

## 3. Issues

| Id | Issue | Definition of Done |
|---|---|---|
| BD-0-1 | Repo, Next.js 15, Mantine + GDS tokens from `14-token-map.md` | tokens resolve; the design-system page renders from the same CSS |
| BD-0-2 | DoneIsBetter SSO for operator and provider roles | operator sees all; provider sees only its `provider_id` (test) |
| BD-0-3 | MongoDB models per `12-technical-design.md` §2 with `platform_id` and `version` | migrations; optimistic-concurrency test |
| BD-0-4 | `YourFieldConnector` + hourly `sync` | 252 providers cached; a changed `updatedAt` produces a diff event (test with a fixture) |
| BD-0-5 | Console shell: role switch, rail/bottom bar, deep links | the prototype's 13 screens reachable, empty states |
| BD-0-6 | Outbox + `send` worker + dead-letter | a Server Action cannot send (test); retry with backoff; lag metric |
| BD-1-1 | Sequence model and editor | steps, merge fields, opt-out footer mandatory (validation) |
| BD-1-2 | `ResendAdapter` out + inbound webhook (signed) | a reply lands in the right thread within 1 minute (measured) |
| BD-1-3 | Drafted replies with the AI switch | AI on: draft with `why`; AI off: template; both marked |
| BD-1-4 | Pipeline stage machine | only event-driven forward moves (test per row of §4); operator override logged |
| BD-1-5 | Apply-to-manage → `claim-requests` | needs the platform key (blocked B1); stage *applied* on 2xx |
| BD-1-6 | Provider view: invitation, today, knowledge | a provider sees its thread, its drafts, edits its files |
| BD-1-8 | Provider conversations: inbound (platform message, Resend inbound, Twilio missed call) → `enquiries` → drafted answer → approve / edit → same channel | reply time logged; the family's thread updated (phase 3) |
| BD-1-9 | Family "ask about a trial" from a saved provider | creates an enquiry as a platform message; visible in the provider's inbox within a minute |
| BD-1-7 | "Not my program" and unsubscribe | the address is excluded from every future sequence (test) |
| BD-2-1 | `draft-social` job from catalogue events | drafts only for providers with news; no duplicate per week |
| BD-2-2 | Approval queue with edit diff | edited copy sets `ai=false`; the diff is stored |
| BD-2-3 | Calendar and slots | a scheduled post publishes at its slot ± 5 min (measured) |
| BD-2-4 | `MetaAdapter` publish + inbound comments/DMs | OAuth per page; a publish writes `messages` + a Blob snapshot |
| BD-2-6 | Drafted replies to comments and DMs with the listing link | operator approves; reply sent through the adapter; comments-answered metric |
| BD-2-5 | AI-content marking | published AI content carries the mark where Art. 50 applies |
| BD-3-1 | Signed preference links from the platform | a family changes a channel without a password; link expiry |
| BD-3-2 | Consent capture and log | SMS toggle impossible without a consent row (test) |
| BD-3-3 | Caps in Redis, double check | a race of 2 sends against a cap of 1 delivers 1 (test) |
| BD-3-4 | Sunday digest | built from saved + nearby-with-session; sent 18:00; cap-aware |
| BD-3-5 | Saved-provider alerts through platform push | new session at a saved provider → push within 1 hour (measured) |
| BD-3-6 | Stop | every channel off and queued drafts cancelled in one transaction |
| BD-4-1 | Overview tiles on real numbers | every tile has a source; "sample" disappears |
| BD-4-2 | Market radar weekly note | from catalogue stats; filed by the operator |
| BD-4-3 | Generated pages through the connector | only ≥ 3 providers; JSON-LD; sitemap entry on the platform |
| BD-4-4 | Operations dashboards and alerts | the five alerts in architecture §9 fire in a drill |
| BD-4-5 | Intelligence recap screen | every tile names its source; "needs you" lists approvals, replied-not-applied, v1 integrations to connect |
| BD-5-1 | `draft-campaigns` job and the campaign model | one draft per kind per card event; kinds per `09-business-logic.md` §4 |
| BD-5-2 | Provider campaigns screen | approve / edit / skip; edit drops the AI badge; audience shown before approval |
| BD-5-3 | Audience resolution through the connector (`savesFor`, `familiesNear`) | no uploaded lists possible (test); counts logged |
| BD-5-4 | `send-campaigns` with preference and cap | a family at the cap receives nothing (test); the reason line on every message |
| BD-5-5 | Products, Stripe Checkout, entitlements webhook | first `active` → *upgraded* → card flag set through the connector |
| BD-5-6 | Provider results screen | what went out from the message log; plan ladder from entitlements |
| BD-6-1 | `SportolokConnector` incl. `ingest` | 431 listings cached; one page published to the reference instance |
| BD-6-2 | Hungarian dictionary and legal footers | every string from the dictionary; footer per market |

## 4. Blocked register

| # | Blocked | On | Unblocks |
|---|---|---|---|
| B1 | Writes to the platform (claim requests, notifications, pages) | ask #5: a key and the write contract | BD-1-5, BD-3-5, BD-4-3 |
| B2 | Social publishing | Meta app review for the platform's pages; ask #3 | BD-2-4 |
| B3 | SMS | Twilio account, consent text approved by counsel; ask #3 | BD-3-2's SMS branch |
| B4 | Real tiles | ask #6: platform analytics | BD-4-1 |
| B5 | Pilot provider | ask #6: one provider's real numbers | provider-view metrics |
| B6 | Product prices | ask #4: the platform's real prices (assumed bundled base + provider-bought reach, D21) | BD-5-5 |
| B7 | Audience data | the platform's saves and family locations through keyed endpoints | BD-5-3 |
| B8 | Stripe account | the platform's merchant account and tax setup | BD-5-5 |

## 5. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Meta review takes weeks | M2 slips | start the review in M0; publish to Facebook first if Instagram lags |
| The public API changes without notice (no reference page) | sync breaks | contract tests against fixtures; alert on schema drift; ask the platform for a versioned endpoint |
| A cap or consent bug | TCPA exposure | ADR-3 double check; consent-before-SMS test; zero-violation alert |
| Providers see the invitation as spam | pipeline stalls | the copy names the provider's own page and the free claim; one reminder only; "not my program" honoured |
| AI drafts off-brand | operator trust | knowledge files first; AI optional; every draft edited is a training signal for the prompt |
| One operator is a bottleneck | queue grows | departments with AI on produce fewer, better drafts; the queue shows age; nothing sends unapproved anyway |

## 6. Release scope

**Release 1 (M0–M3, ~10 weeks):** Your Field NYC; provider sales end to end; Instagram and
Facebook publishing with approval; family digest, alerts and preferences; caps and consent;
the operator's approval queue as the one gate. **Release 1.1 (M4):** real intelligence,
the recap, generated pages, dashboards. **Release 2 (M5):** provider campaigns, results,
products and Stripe upgrades. **Release 3 (M6):** the second instance. Out of scope until a
decision: TikTok and X, Google Business Profile, calendars.
