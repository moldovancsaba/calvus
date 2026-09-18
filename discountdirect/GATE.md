# DiscountDirect — gate

*What is checked before a push, and the state on 2026-09-18.*

## Automated

`python3 holdvolgy/check.py` includes every `discountdirect/*.html` in its link audit,
cross-page anchor check and stale-phrase scan (the Holdvölgy gate was written to cover
the hub and this folder as well). It must print `GATE: CLEAN`.

## Measured (browser pane, per round)

At 375 px and desktop: every seller and buyer screen opened (view toggle, three seller
tabs, four buyer tabs, persona switch); horizontal overflow; tap targets under 44 × 44
px; console errors. Numbers go into `BUILD-LOG.md`.

## State on 2026-09-18

| Check | Result |
|---|---|
| `check.py` | clean |
| Overflow at 375 / 1024 | 0 / 0 on all seven screens |
| Targets under 44 px at 375 | 0 |
| Console errors | 0 |

## Deliberate deviations

- **Desktop density**: controls under 44 px at desktop width (the view toggle is 29 px
  tall) — the 44 px floor applies to phone width, as on the other projects.
- **No `h1` on the chat screens**: the app-shell screens carry pane `h2`s; the campaign
  screens have an `h1` in their hero. Adding one to the chat shell is a visible change
  and waits for the owner.
- **Prototype banner**: the top-bar note "Kattintható prototípus — mintaadatokkal · v16"
  and the wireframe note at the bottom serve as the banner.
- **Prototype vs decisions**: not a gate failure — the documents are authoritative
  (`AUDIT.md`), the prototype is the pre-decision reference until `CLIENT-ASKS.md` #1 is
  answered.
