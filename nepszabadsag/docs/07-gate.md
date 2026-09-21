# Gate

`python3 nepszabadsag/check.py` — exit 1 on any finding; run by the root `check.py`.

| Check | What it verifies |
|---|---|
| Links | every relative href/src on every page and docs page resolves |
| Anchors | every cross-page `#anchor` points at an existing id |
| Docs cross-links | every docs page links every other |
| One `h1` | every page (site and docs) has exactly one |
| `lang` attribute | every page declares one |
| Alt text | every `<img>` on a site page has `alt` |
| Banner | every site page carries the current prototype banner |

Measured pass: `06-build-log.md`. Deliberate deviations from a stricter reading of the
standard: no stale-phrase scan yet (the project is one day old; add it the day stale text is
first caught, per the repo rule) and no invented-image check (every image is a real Wikimedia
Commons photograph tracked in `content.py IMAGES`, not a project-local asset folder pattern the
other gates check for — `03-sources.md` records provenance instead).
