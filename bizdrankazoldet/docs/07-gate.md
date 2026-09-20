# Gate

`python3 bizdrankazoldet/check.py` — exit 1 on any finding; run by the root `check.py`.

| Check | What it verifies |
|---|---|
| Links | every relative href/src on every page and docs page resolves |
| Anchors | every cross-page `#anchor` points at an existing id |
| Docs cross-links | every docs page links every other |
| One `h1` | every site page has exactly one |
| Banner | every site page carries the current prototype banner |
| Stale phrases | nothing that was true once (the gate holds the list; this page and the registers are exempt) |
| Invented images | every image on a site page comes from `assets/img` — the client's own material |
| Sourced figures | every research paragraph with a number carries a P or A mark |

Measured pass: `06-build-log.md`.
