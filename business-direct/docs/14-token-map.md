# business.direct — token and component map

*Written 2026-09-19. What the prototype's CSS becomes in production. The prototype does not
consume a design-system package — it is dependency-free HTML — but its custom properties
are named after General Design System 6.5.0 roles (the same convention as DiscountDirect's
`GDS-TOKEN-MAP.md`, D5/D8), so the production build maps 1:1 without a rename pass.*

## 1. How the handoff works

The whole colour and shape contract is `assets/tokens.css` (one `:root` block). In
production the app loads the GDS theme stylesheet and Mantine's theme is generated from the
same roles; `tokens.css` is deleted. Every `var(--gds-…)` in `components.css` and `app.css`
then resolves to the governed value. No selector or markup changes for the token layer.

## 2. Tokens

| Role (prototype = GDS 6.5.0 name) | Value here | Source | Production |
|---|---|---|---|
| `--gds-bg-canvas` | `#f8fafc` | GDS canonical light | GDS |
| `--gds-bg-surface` | `#ffffff` | GDS | GDS |
| `--gds-bg-inverse` | `#111827` | GDS | GDS |
| `--gds-bg-muted` | `#f1f5f9` | GDS | GDS |
| `--gds-text-body` / `-meta` / `-on-inverse` | `#111827` / `#64748b` / `#f8fafc` | GDS | GDS |
| `--gds-border-card` / `-strong` | `#e2e8f0` / `#cbd5e1` | GDS | GDS |
| `--gds-brand-accent` / `-tint` / `-strong` | `#0f766e` / `#e6f4f2` / `#115e59` | **product-owned** (D8: business.direct teal; DiscountDirect indigo) | the product's brand override in the GDS theme |
| `--gds-status-ok` / `-wait` / `-off` / `-danger` (+ tints) | `#15803d` / `#b45309` / `#64748b` / `#b91c1c` | GDS semantic status | GDS |
| `--gds-radius-card` / `-control` / `-pill` | 14 / 10 / 999 px | GDS | GDS |
| `--gds-elevation-card` | two-layer shadow | GDS | GDS |
| `--gds-font` / `--gds-font-mono` | system stacks | GDS | GDS (Inter where the platform uses it) |
| `--gds-t-title` / `-h2` / `-body` / `-meta` | clamp 22–30 / 18 / 14 / 12 px | prototype | Mantine `fontSizes` |
| `--gds-tap` | 44 px | prototype rule (PROTOTYPING.md) | Mantine component `size` at phone widths |
| `--gds-gutter` / `--gds-content-max` | 16 px / 1400 px | prototype | layout constants |

Contrast (WCAG relative luminance, computed 2026-09-19): accent on white 5.5:1,
accent-strong on tint 6.7:1, status-ok on ok-tint 4.6:1, status-wait on wait-tint 4.5:1,
meta on surface 4.8:1 — all ≥ 4.5:1; the wait pair sits exactly at the threshold and is
used only at 12 px bold badges, so production should darken `--gds-status-wait` a step if
it appears in body text.

## 3. Components → Mantine + GDS

| Prototype class (`components.css`) | Production | Notes |
|---|---|---|
| `.btn`, `.btn.sec`, `.btn.ghost`, `.btn.danger`, `.btn.inert` | `Button` variants filled / light / subtle / red; `inert` = `disabled` with a tooltip | 44 px min height below 980 |
| `.badge.b-ok/.b-wait/.b-off/.b-danger/.b-ai` | `Badge` with the status colours; `b-ai` is a product variant (✦) | the AI badge is required by ADR-7 |
| `.topbar`, `.brand`, `.roles`, `.topnote` | `AppShell.Header` + `SegmentedControl` for the role switch | roles become route groups |
| `.rail`, `.bottombar` (`app.css`) | `AppShell.Navbar` ≥ 1024; a fixed `Tabs` bar below | counts as `Indicator` |
| `.grid`, `.card`, `.dept-list`, `.toggle` | `SimpleGrid`, `Card`, `List`, `Switch` | the AI switch is a `Switch` with a label |
| `.approval`, `.preview`, `.why` | product component `ApprovalCard` (Card + actions column) | the `why` line is mandatory (R2) |
| `.post` (D15) | product component `PostCard` (media 72 px, channels, copy, link, state) | media from Blob |
| `.pipeline` (D15) | product component `PipelineStrip` (6 stages, `on`/`done`) | click filters the list |
| `.tiles`, `.tile`, `.bars` | `SimpleGrid` of `Paper` with a sparkline (`@mantine/charts`) | every tile shows its source (R7) |
| `.tbl` | `Table` with `ScrollArea`, server pagination | 50 per page |
| `.kfile` | `Textarea` in a `Code`-styled `Paper` with a path label | versioned saves |
| `.listing`, `.pin`, `.ladder` | `Card` with an avatar; the ladder is the provider's plan (products, `done` = active entitlement) | family saved, provider results, drawer |
| campaign card (= `.approval` + `.preview` + `.why`) | product component `CampaignCard` — the approval card with the audience line | provider campaigns, family inbox (read-only) |
| media adapter card, sending card, experiment card (= `.card` + `.dept-list` / `.foot`) | `Card` with status badges | social publishing, sales, economics |
| enquiry card, comment card (= `.approval` + `.why` + `.preview`) | product component `ReplyCard` — "they wrote" + the drafted answer + approve / edit / skip | provider conversations, platform social, approvals |
| product card (= `.card` + `.foot`) | `Card` with price and a `Button` → Stripe Checkout | provider today |
| `.push`, `.digest`, `.sms` | preview renderers for the three family channels | used by `ChannelAdapter.preview` |
| `.field`, `.search`, `.chip` (`app.css`) | `TextInput`, `Chip.Group` | |
| `.drawer`, `.thread`, `.msg` (`app.css`) | `Drawer` + a `ThreadView` product component | |
| `.week`, `.slot` (`app.css`) | product component `WeekCalendar` | drag-to-reschedule is a later issue |
| `.toast` (`app.css`) | `Notifications` | |
| `.empty` (`app.css`) | product `EmptyState` | every screen has one |

## 4. What has no mapping

The frames' `frame.css` and the docs' `docs.css` are documentation only. The
design-system page (`design-system.html`) is the reference for review, not a component
library; production's storybook is generated from the Mantine components above.
