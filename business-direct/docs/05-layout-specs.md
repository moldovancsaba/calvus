# business.direct — layout specifications (gate 2)

*Four frames composed only from the approved components (`assets/components.css`, D9) and
the real providers (`data/providers.json`). Layout rules live in `docs/frames/frame.css`
and nowhere else. Approved 2026-09-19 as gate 2 (D16); the prototype (`../index.html`) implements them — round 2 measured 768 and 1024 as specified.*

## Reference widths and the tablet resolution

| Width | Navigation | Grids |
|---|---|---|
| ≥ 1024 (desktop, framed at 1440) | left rail (flows · data · system) + top bar with the three-role switch | two-column body: the flow columns 1.5 : 1; tiles auto-fit; tables full |
| 768–1023 (tablet) | the phone navigation (bottom bar), no rail | the desktop grids where they fit (tiles, department cards); flow columns stack |
| < 768 (phone, framed at 390) | bottom bar with four items and the approval count; top bar keeps the role switch | single column; tiles two-up; pipeline strip three-up; approval actions stacked, approve full-width |

Tap targets 44 px below 980; desktop density tighter. Content max 1400 px. Every frame
loads the live JSON, so a refreshed catalogue changes the frames without an edit.

## Frame 1 — Platform · Overview · 1440 (`frames/platform-desktop-1440.html`)

The control room, ordered by the two primary flows (D14):

1. Title and the day's state (7 items waiting).
2. Six intelligence tiles — four real (providers, managing, with e-mail/phone, next session known), two declared sample.
3. Left column, **B2C · Social publishing**: this week's posts as post cards (channels, copy, media, link back to the listing page, AI-draft badge, approve/edit/skip), then the approval queue.
4. Right column, **B2B · Provider sales**: the pipeline strip (253 identified, real; the rest zero), next actions (invitation sequence, call list, website-form list), then the departments (social, sales, weekly picks, generated pages, market radar).
5. Providers table with filter chips built from real counts (unclaimed flag 15, e-mail 130, phone 180, trial 72) and a stage badge.

## Frame 2 — Platform · Overview · 390 (`frames/platform-phone-390.html`)

Same content, single column, in the same order: tiles two-up → this week's posts →
pipeline strip three-up + the invitation approval → departments → providers as listing
cards with the ladder. Bottom bar: Overview · Approvals (7) · Providers · More.

## Frame 3 — Provider · Today · 390 (`frames/provider-phone-390.html`)

The provider lives on a phone. Top: the real card of Brooklyn Force Soccer (claim state
real: unclaimed). Then the B2B flow from the provider's side in two steps: **what the
coach received** (the invitation e-mail with "Apply to manage my page" and the opt-out) and
**after approval: Today** — two tiles, two approval items (a reply to a family's trial
request; a trial-class campaign with the consent rule stated), the four departments, the
knowledge files. Bottom bar: Today · Waiting (2) · Team · More.

## Frame 4 — Family · What arrives · 390 (`frames/family-phone-390.html`)

Where a new family meets the platform — the **published social post with its link back**
(the B2C flow's landing) — then this week's push and digest built from real providers,
one provider text with the consent and cap stated, and the channel/frequency controls
with a one-tap stop. Bottom bar: Find · Saved · Inbox · Account.

## Assumptions the open asks force (`08-client-asks.md`)

- Provider persona Brooklyn Force Soccer; family persona Maya in Park Slope (D13).
- Integrations shown: Your Field API, Instagram/Facebook, TikTok/X, e-mail (Resend), push, SMS with consent state, Google Business Profile.
- Social channels are the platform's own accounts (@yourfieldnyc); the provider's spotlight post is requested by the provider and published by the platform.
- Every family-facing SMS requires written consent captured on the platform; e-mail and push do not.

## What approval of these frames fixes

Section order per view, the two-column desktop body, the phone bottom bars, the tile
set, the post card and pipeline strip (D15) in place. It does not fix copy — every
sentence in the frames is sample except the provider data and the site's own phrases.

## Phase 2 and 3 screens (D22–D25, 2026-09-19)

No new layout. *Conversations*, *Campaigns* and *Results* (provider) and *Intelligence* (platform) reuse the
frames' grids: approval cards in a single stack, tiles auto-fit / two-up, the two-column
body for the recap at ≥ 1024. Measured at 390 and 1440 with the rest (`07-gate.md`).

The mode switch (D33) is a second `.roles` segment in the top bar; on the phone the two
segments wrap to two rows. *Home*, *Templates* and *How to use* reuse the approval stack,
the card grid and the two-column body. No new layout.

The provider's *Media* screen (D28) reuses the approval stack: one card for the recording,
the post cards for the clips, a listing card for the photo. No new layout.

The frames and the design-system page were re-issued 2026-09-19 with age bands in place of
children's names (R24, D31); layouts unchanged.
