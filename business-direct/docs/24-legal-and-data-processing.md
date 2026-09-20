# business.direct — the product's legal position: processor for the media owner, and the counsel list

*Phase D of the transformation programme (`21-documentation-audit.md` §8). The responsible-data
framework (`18-responsible-data-policy-framework.md`) governs **the customer's** policy record —
what each media owner's site may send, to whom, under which law. This document is about
**business.direct's own obligations** as the company that operates the product on the owner's
data. **Nothing here is legal advice**: every statement is the product team's reading, written so
that counsel can confirm or correct it; §6 is the list of questions for counsel. Every legal
sentence in `01e`, `01f`, `18` and `09` §7 carries the same status. Written 2026-09-20 (D42).*

## 1. The roles (the reading counsel confirms)

| Data | Who decides why and how (controller) | Who processes on instruction (processor) | Notes |
|---|---|---|---|
| Listings and the advertisers' contact details (the site's catalogue) | the media owner | business.direct | business contact data; for EU sites, a named person's e-mail is personal data (Act XLVIII, GDPR) |
| Visitors' accounts, saves, preferences, consents | the media owner (the site holds the account) | business.direct (mirrors preferences and consents, sends on instruction) | visitors never sign in to the product (ADR-6) |
| Messages sent and received through the product | the media owner | business.direct | the message log is the owner's record; the product keeps it for the retention period the owner sets |
| The product's own operational data (events, metrics, the operator's approvals) | business.direct, as necessary to run the service | — | contract; no marketing use across customers |
| The product's telemetry about the owner's users (errors, health) | business.direct | — | minimised; no visitor content in error reports |

In GDPR terms business.direct is a **processor** for the media owner (controller) — or a
sub-processor where the owner is itself a processor for its advertisers; under the CCPA/CPRA a
**service provider**. The first customer's site is US-only with adult users by its own policy
(D31); the framework's children's-data rules apply to any instance where minors may be present.

## 2. The documents the product must have before the first customer contract

| # | Document | What it must say (in outline) | Owner | Status |
|---|---|---|---|---|
| L1 | **Terms of service** (owner ↔ business.direct) | the service (the three jobs as departments with a human gate), the owner's responsibilities (the policy record's truth, the postal address, its own privacy policy, the channels' authority), acceptable use (no purchased lists, no messages to people who did not save, ask or opt in — R11, ADR-10), the human gate as an operating condition, availability, fees and cooling-off, liability caps, termination and data return | counsel drafts on the product team's outline | **to write** |
| L2 | **Data processing agreement** (Art. 28 GDPR-shaped, usable for US customers) | subject matter and duration, nature and purpose, the data categories in §1, the controller's instructions (the policy record *is* the instruction set), confidentiality, security (§4), sub-processors (§3) with notice of change, assistance with data-subject rights (export, deletion via the platform webhook — blueprint §8), breach notification (72 h to the owner), deletion or return at the end, audit rights | counsel | **to write** |
| L3 | **The product's privacy policy** | what business.direct itself collects (the operator's account via SSO, approvals, operational telemetry), the processor role for everything else, the sub-processors, retention, the children's-data stance (§5), contact | counsel | **to write** |
| L4 | **Sub-processor list** (§3) | public page; notice before a change | product team | drafted below |
| L5 | **Security statement** | blueprint §8 in plain words: encryption in transit and at rest, secrets, webhook signatures, idempotency, access scoped per instance, append-only audit collections, backups, incident process, the runbooks | product team | **to write from `20` §8, §12** |
| L6 | **Retention and deletion schedule** | per data class per instance: messages 24 months, consents account + 5 years, drafts 90 days, events 24 months (framework §2); deletion on the owner's instruction and at the end of the contract | product team | drafted in `18` §2 |
| L7 | **AI-disclosure statement** | which departments may use a model, that every output is marked internally and disclosed to recipients where the instance's law requires (R20, EU AI Act Art. 50 where EU users), that no decision about a person is automated (the human gate) | product team + counsel | **to write** |
| L8 | **Children's-data stance** (§5) | in L3 and in the DPA's data categories | counsel | drafted below |

## 3. Sub-processors (from research VI; every one under a contract with a DPA)

| Sub-processor | Purpose | Data it sees | Region |
|---|---|---|---|
| Vercel | hosting, functions, cron, Blob (media, snapshots) | all application data in transit; media files | US (iad1) |
| MongoDB Atlas | the database | all application data at rest | US-East |
| Upstash | caps, locks, idempotency | ids and counters only | US-East |
| Resend | e-mail out and inbound | recipients, message content | US |
| Meta (Instagram, Facebook) | publishing, comments, DMs | published content, commenters' public handles | Meta's |
| Twilio (when SMS is on) | SMS, missed-call capture | phone numbers, message content | US |
| Stripe | the owner's advertiser payments (on the owner's own account) | none through business.direct beyond the entitlement | — |
| Anthropic (Claude API) | drafting and classification when the department's switch is on | the knowledge files, the listing, the thread being answered — no visitor account data beyond what a message contains | US (the API's data-use terms: no training on API inputs) |
| Deepgram | transcription of uploaded recordings | the audio | US |
| Fly.io | the media worker | the recording and the clips while processing | US (iad) |
| Sentry | errors | stack traces with instance id; no message content | US |
| Better Stack | uptime | none | — |
| DoneIsBetter SSO | the operator's sign-in | operator e-mail and name | the owner's |

Rule: a sub-processor is added only with notice to every customer; a recording that shows
children never leaves the worker without the consent reference (R30).

## 4. Security commitments (what the owner can be promised, from `20` §8)

Encryption in transit (HTTPS, HSTS) and at rest (Atlas, Blob); secrets in the platform's
encrypted environment; every webhook verified by signature before it is read; idempotency on
every inbound event; access scoped to the operator's instance and to an advertiser's own
records; append-only audit collections (approvals, consents, messages, opt-outs, events); daily
backups at production tier; the incident runbooks in `20` §12; breach notice to the owner within
72 hours of confirmation.

## 5. The children's-data stance of the product itself

business.direct stores no child's name, image or location on any instance (R24); a child is
an age, and only where the instance's policy record allows the field (`childData`). It never
profiles or targets a minor, with or without consent (R27). It cuts footage that shows a child
only with the operator's confirmation of written parental consent, kept with the clip (R30). For
an instance whose audience may include minors, the policy record requires the audience model and
a DPIA before the family entity accepts any minor's field (R26, framework §3). The product's own
privacy policy says this; the owner's policy record makes it enforceable per site.

## 6. The questions for counsel (one list; every legal sentence in the set depends on it)

1. Is the processor / service-provider reading in §1 right for the first customer (US, adult
   users), and what changes if a later instance has EU users or minors?
2. Which of L1–L8 must exist before the first real message is sent, and which before the
   contract is signed?
3. CAN-SPAM: the postal address in every advertiser e-mail is the **owner's** — confirm; may the
   product's own address be used where the owner has none?
4. TCPA / A2P 10DLC: the consent text stored verbatim per visitor per advertiser (R4) — confirm
   the wording; who is the "sender" for registration, the owner or the product?
5. Children's data (New York Child Data Protection Act, COPPA 2025): a parent's account
   describing a child by age only — confirm no consent flow is needed and the wording of the
   age field (`19` P-4).
6. EU instances: named-person e-mail addresses need consent under Act XLVIII/2008 §6 — confirm;
   the connector's `contactKind` flag is the mechanism (`17` A17).
7. AI disclosure: for the first customer (US), which messages, if any, must carry a disclosure;
   for EU users, the Art. 50 wording.
8. The DPA's breach-notice window and liability cap for a product of this size.
9. Whether the retention schedule in L6 satisfies the owner's own obligations to its users.
10. Whether the product may use aggregated, de-identified metrics across customers for
    benchmarks (today: no, by design).

Until counsel answers, the product runs the pilot on test addresses and the owner's own
accounts only, and every legal sentence in the documentation reads as "the product team's
reading, to be confirmed".
