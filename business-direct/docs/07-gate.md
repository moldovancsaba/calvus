# business.direct — gate

`python3 business-direct/check.py` (also run by the root `python3 check.py`). Exit 1 on
any finding. It must print `GATE: CLEAN` before a push.

| Check | What |
|---|---|
| Links | every relative `href`/`src` in the pages and docs resolves on disk |
| Anchors | every cross-page `#anchor` points at an existing id |
| Docs nav | every docs page links every other docs page |
| Data | `data/providers.json` parses, has ≥ 1 provider, and every provider has `id`, `name`, `borough` |
| Script | `assets/app.js` parses (`node --check`) when node is installed |

## Measured in the browser (not automated — the standard's method, `PROTOTYPING.md` §6)

Run the page from `python3 -m http.server` at the repo root; open it in the app browser pane;
set the viewport explicitly (390 × 844 and 1440 × 900); walk every screen and action with a
DOM script; read the console. Pass conditions and the 2026-09-19 result:

| Condition | 390 | 1440 |
|---|---|---|
| `document.documentElement.scrollWidth == innerWidth` on every screen | pass | pass |
| no element past the viewport except inside `.tbl` (which scrolls) | pass | pass |
| every `button, a, select, input` ≥ 44 × 44 | pass | n/a |
| one `h1` per screen; every `img` has `alt` | pass | pass |
| 0 console errors through the full click path | pass | pass |

The round's findings and fixes are in `06-build-log.md`.
