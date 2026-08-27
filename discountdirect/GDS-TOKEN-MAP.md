# DiscountDirect — GDS token alignment

**What this is:** the prototype's CSS custom properties are named after
[General Design System](../../general-design-system) **6.5.0** semantic roles, so the eventual
production build maps 1:1 without a rename pass.

**What this is not:** DiscountDirect does **not** consume GDS. There is no npm dependency, no
`@sovereignsquad/gds*` import, no React, no build step, and no `gds-adoption.json` — this repo's
prototypes are deliberately dependency-free single HTML files (see the root `README.md`). This is
naming alignment only.

## How the handoff works

The whole colour contract lives in one `:root` block in `index.html`. To move the markup onto real
GDS, the dev build **deletes that block** and loads `@sovereignsquad/gds-theme/styles.css` instead;
every `var(--gds-…)` reference in the file then resolves to the governed value. No selector, class
or markup change is required for the token layer.

## The mapping

| Prototype role (was) | GDS 6.5.0 role | Value here | Source of the value |
|---|---|---|---|
| `--bg` | `--gds-bg-canvas` | `#f8fafc` | GDS canonical light |
| `--surface` | `--gds-bg-surface` | `#ffffff` | GDS canonical light |
| *(hardcoded `#141a2e`)* | `--gds-bg-inverse` | `#111827` | GDS canonical light |
| `--text` | `--gds-text-body` | `#111827` | GDS canonical light |
| `--muted` | `--gds-text-meta` | `#64748b` | GDS canonical light |
| `--line` | `--gds-border-card` | `#e2e8f0` | GDS canonical light |
| *(white on shell)* | `--gds-text-on-inverse` | `#f8fafc` | GDS canonical light |
| `--accent` | `--gds-brand-accent` | `#3b5bdb` | prototype-owned |
| `--accent-soft` | `--gds-brand-accent-tint` | `#e7ecfb` | prototype-owned |
| `--green` | `--gds-state-success` | `#2f9e6e` | prototype-owned |
| `--green-soft` | `--gds-badge-soft-success` | `#e3f5ec` | prototype-owned |
| `--red` | `--gds-state-danger` | `#d64545` | prototype-owned |
| `--red-soft` | `--gds-badge-soft-danger` | `#fbecec` | prototype-owned |
| `--amber` | `--gds-state-warning` | `#b07716` | prototype-owned |
| `--amber-soft` | `--gds-badge-soft-warning` | `#fdf3e0` | prototype-owned |
| `--radius` | `--gds-radius-card` | `14px` | prototype-owned |
| `--shadow` | `--gds-elevation-card` | `0 10px 30px rgba(28,35,51,.08)` | prototype-owned |

**Why two sources.** GDS 6.5.0 defines the **structural** roles (backgrounds, text, border,
on-inverse) at `:root` as a governed default layer with a hard-gated contrast contract, so this
prototype adopts those values verbatim — what you see here is what the dev build renders. GDS
deliberately does **not** default the **brand / state / accent** roles when no preset is active,
because their hue is a brand decision; those keep the prototype's own values until a brand theme or
vibe preset is chosen. See `docs/SEMANTIC_ROLE_TOKENS.md` in the GDS repo.

## Notes for the dev build

- **Contrast is already GDS-gated** for the structural pairs (`text-body` on `bg-surface` 17.74:1,
  `text-meta` on `bg-surface` 4.76:1). The prototype-owned brand/state colours are **not** yet
  checked against that bar — run `checkGdsContrast()` on them when a brand theme is picked.
- Roles used here that GDS also governs, if the components are adopted later:
  `--gds-radius-pill` (the chips and toggles use `999px` literals), `--gds-space-*` (spacing is
  still literal px), `--gds-focus-ring` (focus styling is currently the browser default).
- The Hungarian UI strings and all data are inline mock data — see the prototype note in the page
  footer.
