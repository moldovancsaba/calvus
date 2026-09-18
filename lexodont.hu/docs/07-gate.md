# Lexodont — gate

*What is checked, how, and the state on 2026-09-18.*

## The command

`python3 lexodont.hu/check.py` — exit 1 on any finding:

1. every relative `href`/`src` in both page sets and the docs resolves on disk;
2. every cross-page `#anchor` points at an existing id;
3. every docs page links every other;
4. **parity**: every page in the polished set exists in the sketch set and vice versa.

Run 2026-09-18: the first run reported the three sketch pages missing since D13; they were
added (D15) and the gate is clean — 49 files, 708 references.

## The measured pass

66 measurements (33 pages × 390 and 1440) via same-origin iframes in the browser pane:
overflow, `h1` count, `alt` coverage, `<title>`, `lang`, tap targets under 44 px at 390.
Results in `06-build-log.md`.

## Findings left open, and why

- 18 pages with tap targets under 44 px at 390 and one 8 px overflow. The wireframe is
  superseded by the live site (`02-audit.md`); fixing a sketch nobody will present again
  is work without a reader. If the wireframe is ever shown again, the fix is one
  phone-width rule per stylesheet (as done for DiscountDirect on the same day).
- No prototype banner on the pages; the home hero carries a "Wireframe megjegyzés" note
  and every `<title>` says wireframe.
- Live-URL rule (never delete a published URL) applies: nothing is removed.
