# business.direct — implementation prerequisites (after the client accepts; not needed for the presentation)

*Written 2026-09-19 on the owner's instruction: the open items are tasks for the day the
client accepts the prototype, not for the presentation or the planning. Nothing in this
list is required to present, to plan, or to build the prototype further — every item is
defaulted or sampled in the prototype and declared as such on the screen. The register of
asks (`08-client-asks.md`) keeps the history; this document is the checklist the
implementation starts from.*

## 1. Before the first real message can be sent (legal and policy)

| # | Prerequisite | Who provides | Why | Unblocks |
|---|---|---|---|---|
| P-1 (ask #15) | The platform's registered **postal address** for every provider e-mail | ClassScout | CAN-SPAM requires a physical address; the site publishes only info@classscout.ai | the policy gate's "provider e-mail" row; the sequences |
| P-2 (ask #16) | The platform's **privacy policy revised** to describe the digest and alerts ("we do not yet offer email alerts; if we add them, the preferences you set will be described here") | ClassScout (we draft the paragraph on request) | the family digest and alerts must be described before they run | the gate's "digest and alerts" row |
| P-3 (ask #18) | The **policy record** for Your Field NYC confirmed: audience model (adults, per the policy), retention periods, AI-disclosure choice, quiet hours | ClassScout | the gate reads the record before every send | the whole gate |
| P-4 (ask #13) | Counsel's view on **children's data**: which of New York's Child Data Protection Act and COPPA applies to a parent's account describing a child, and the consent texts | ClassScout's counsel | the machine already stores no child's name; this confirms wording | enquiry and campaign texts |

## 2. Before Release 1b (the keyed half — data and writes from the platform)

| # | Prerequisite | Who provides | Why | Unblocks |
|---|---|---|---|---|
| P-5 (ask #17) | The **opted-in share**: how many accounts turned on activity recording (saves recorded "only after you explicitly opt in, off by default") | ClassScout | campaign audiences and the avid-family definition are only opted-in accounts | real audience counts on campaign cards |
| P-6 (asks #7, #10) | **Analytics events and counts**: families, sign-ups with source, saves, digest opens, bookings; the real prices of the three products | ClassScout | every assumption in the economics model becomes a measurement | the economics tiles; capture; cohorts |
| P-7 (ask #6) | A **key and the write contract** for claim requests, notifications, card flags, saves for audiences — or the decision that the machine stays read-only | ClassScout | apply-to-manage, upgrades' card flags, alerts | Release 1b |
| P-8 (ask #12) | Whether **review capture and price capture** are planned on the cards (0 reviews, 28 prices on 253 today) | ClassScout product | the AI-citation lever and the content engine depend on card quality | generated pages' readiness; anchors |
| P-9 (ask #8) | A **pilot provider** willing to share replies, trials booked, no-shows | ClassScout + one provider | the provider view's tiles are sample until then | provider results; "your return" |

## 3. To confirm at acceptance (assumptions the prototype runs on; a "yes" closes each)

| # | Assumption in the prototype | Where it shows |
|---|---|---|
| P-10 (asks #2, #3) | Demo personas: Brooklyn Force Soccer; a Park Slope parent with a child of 5 and a child of 9 | provider and family views |
| P-11 (ask #4) | v1 integrations = the platform API, e-mail, Instagram + Facebook, push; later = TikTok, X, SMS, Google Business Profile, calendars | integrations screen |
| P-12 (ask #5) | Money: the base machine bundled by the platform; providers buy reach (featured listing, camp placement, discovery profile — sample prices); the conversations line at 0 (bundled) or priced | economics inputs; provider today |

## 4. What the presentation needs from the owner today

Nothing. The prototype, the presentation and the plan stand on defaults and samples that
are declared on every screen. The decision to present is the only decision open.
