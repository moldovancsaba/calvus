# DiscountDirect — design

*Screens, components and tokens of the prototype, and what was never designed. There was no
design-system or layout approval gate: the prototype was built in one day as a wireframe to
make the business logic clickable. Written 2026-09-18.*

## Screens

| View | Screen | Purpose |
|---|---|---|
| Eladó | Csevegések | roster of buyers (left), channel-aware timeline with offer cards (centre), purchase history and recommended offers (right) |
| Eladó | ⚡ Villámajánlat | one-product flash campaign: product, discount, time and quantity limits, channels, targeting preview |
| Eladó | 🗞 Ajánlatlisták | recurring per-buyer lists: products, cadence, channels, per-buyer preview, active automations |
| Vevő | Csevegés | the buyer's inbox and thread, persona switch |
| Vevő | E-mail · Postai levél · Hírlevél | how the same offers arrive on each channel |

## Components

Top bar with view toggle and persona select; tab rail; pane with head; conversation
button with badge; timeline event (message, offer card with reason, price, status,
channels; channel event); composer; recommendation card with send; campaign form fields
(segmented choices, checkboxes); targeting row; preview cards; letter and newsletter
mock-ups; wireframe note with the document links.

## Tokens

Custom properties named after GDS 6.5.0 semantic roles — `--gds-bg-canvas`, `--gds-bg-surface`,
`--gds-bg-inverse`, `--gds-text-body`, `--gds-text-meta`, `--gds-border-card`,
`--gds-brand-accent` (`#3b5bdb`, prototype-owned), `--gds-radius-card`, `--gds-elevation-card`
— one `:root` block; the full mapping and the hand-off mechanism (delete the block, load
the GDS theme stylesheet) are in `GDS-TOKEN-MAP.md`. Type: the system sans stack.

## Layout

Three-pane grid `290px / 1fr / 330px` above 1080 px, one column below; campaign screens
on an `auto-fit, minmax(340px, 1fr)` grid; buyer mock-ups centred at 720 px. Phone
width (≤ 700 px, added 2026-09-18): single column everywhere, 44 px minimum on every
control, 12 px side padding.

## What was never designed

A brand (the wordmark is text), a buyer-facing app beyond the mock-ups, the rules block
on every message (D14), the sold-out notice (D2), advanced-mode settings screens (D13),
the seller print flow (D15), onboarding, empty states, error states. These are Release 1
scope in `IMPLEMENTATION-PLAN.md` and will need design before build.
