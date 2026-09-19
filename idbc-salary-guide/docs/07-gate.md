# IDBC Salary Guide — gate

*What is checked before every push, how, and the state on 2026-09-18.*

## The command

`python3 idbc-salary-guide/check.py` — exit 1 on any finding:

1. every relative `href`/`src` in every guide page and docs page resolves on disk;
2. every cross-page `#anchor` points at an existing id;
3. every docs page links every other (the rendered navigation);
4. the shared chart assets are loaded with the same `?v=` on every page that uses them
   (a mismatch means one page runs the old renderer — the failure mode recorded in
   `SOURCES-AND-GAPS.md`);
5. no inert control has lost its `is-unavailable` class (Excel, EN, Kijelentkezés, the
   form submits) — a control that looks live but is not is worse than one that says so.

It prints `GATE: CLEAN` or the findings.

## The measured pass (manual, in the browser pane, per change round)

At 375 px and desktop width on all seven pages: no horizontal overflow; no tap target
under 44 × 44 px with the phone menu open; one `h1`; no console errors; the page's own
feature exercised (every area on Bérek, industry switch and join form on Expert Pool,
video/highlight on two area pages, the chart API with synthetic rows when real data
cannot reach a code path). Results are written into the change note of that round.

## Deliberate deviations from the repo standard

- **No prototype banner.** The other projects carry a one-line banner on every page. The
  guide is in client fine-tuning and the client reviews the live URL against their
  mockups; a banner would be a visible unasked change. The inert controls carry a
  `title` explaining themselves instead. Revisit if the owner wants the banner.
- **No stale-phrase scan.** The pages hold no "coming soon" copy; the docs are dated.
- **No screen-reader pass** (recorded 2026-09-15).

## State on 2026-09-18

| Check | Result |
|---|---|
| `check.py` | clean (first run after writing it) |
| Pages measured | 7 × 375 px + 7 × desktop, last full pass 2026-09-18 after the bértábla rebuild |
| Overflow, small targets, console errors | 0 / 0 / 0 |
| Live verification | every push polled on GitHub Pages with a unique marker until served |

## Tablet and desktop widths measured (2026-09-20, hub audit action 5)

The standard names phone and desktop; the earlier passes measured 375 and "desktop" (the
pane's width). Measured explicitly in the app browser pane, DOM audit per page:

| Page | 768 × 1024 | 1440 × 900 |
|---|---|---|
| index, berezes, sap, expert-pool, esettanulmanyok, terulet (IT) | `scrollWidth` 768, one `h1`, every control ≥ 44 px | `scrollWidth` 1440, one `h1` |
| regisztracio | `scrollWidth` 768; one control under 44 px — the native `adatvedelem` checkbox (the label is the tap target; left as is, fine-tuning rule) | `scrollWidth` 1440 |

No page changed. The stale-phrase scan and the decision-range check joined `check.py` the
same day and found two "not yet built" statements about pages that exist (fixed in
`data/SOURCES-AND-GAPS.md`) and a stale decision range in the docs index (fixed).
