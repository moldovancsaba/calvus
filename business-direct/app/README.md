# business.direct — the product's code

The application described in `../docs/architecture.md` (Part C, the module catalogue) and built in
the pieces of `../docs/delivery-plan.md` §2c. It lives here until the product's own repository
exists; nothing in it is served by the hub's static site.

## Run

```bash
cd business-direct/app && npm install && npm test && npm run typecheck
```

Node 22+; no accounts, keys or network needed — every module runs against in-memory stores and
the demo sample (`fixtures/providers.json`), so the rules are proven before any vendor is connected.

## What is done (tests are the acceptance record)

| Piece | Module | Proven by |
|---|---|---|
| P1 the policy record and gate | `src/modules/policy` | `tests/policy.test.ts` — every gate row of `responsible-data.md` Part A §3, quiet hours, the child-field rule, the screen's inversion |
| P2 listings connector and sync; the stage machine; the score | `src/modules/catalogue`, `src/modules/pipeline` | `tests/catalogue.test.ts` (contract against the demo sample: one diff event per change), `tests/pipeline.test.ts` (R9 forward on events, override logged; R22 ordering) |
| P3 (part) the template drafter and the pattern guard | `src/modules/drafting` | `tests/drafting.test.ts` — R10, R32, R36, R13/R37; every step carries the footer |
| P4 (core) the outbox: the double check, the cap race, the sending guard, the message log with the policy basis | `src/modules/outbox` | `tests/outbox.test.ts` — ADR-3/ADR-4, R3, R4, R23, R26 |
| P10 (core) Stop in one operation; a child is an age, never a name | `src/modules/families`, `src/db/schemas.ts` | `tests/outbox.test.ts` — R28, R24 |
| P15 (core) retention signals and drafts | `src/modules/retention` | `tests/retention.test.ts` — R37 |

## What needs the owner's accounts before it can be enabled (sprint 0, `delivery-plan.md` §2b)

Vercel, MongoDB Atlas, Upstash, Resend (the sending domain's DNS), the Meta developer app and
its review, the Claude API key, DoneIsBetter SSO's client — and the first customer's policy
record. The modules take their stores, counters and adapters as dependencies (`Deps` in
`src/modules/outbox/index.ts`), so connecting a vendor is an adapter, not a rewrite.

## Layout

```
src/db/schemas.ts        Zod contracts: Policy, FamilyPrefs (no child's name possible), OutboxRow
src/lib/store.ts         Store and Counter interfaces + in-memory implementations (Mongo / Upstash in production)
src/lib/events.ts        the append-only event log
src/modules/policy       gate(feature, ctx), blockedBy(policy), basis()
src/modules/catalogue    PlatformConnector, FixtureConnector, sync() with diff events
src/modules/pipeline     STAGES, ensure(), setStage() (R9), score() (R22)
src/modules/drafting     patternGuard() (R32, R36), templateDrafter (R10)
src/modules/outbox       checks() at enqueue and at send, enqueue(), send() with lock, backoff and dead-letter, cancelFor()
src/modules/families     stop()
src/modules/retention    signals(), drafts() (R37)
tests/                   one file per module; `tests/helpers.ts` builds a complete and an empty policy record
```
