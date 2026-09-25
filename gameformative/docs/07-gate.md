# Gate

*What `check.py` verifies, and the measured pass. Run `python3 gameformative/check.py` (or the
root `python3 check.py`, which runs it with every other project's gate). It exits 1 on any finding;
read the exit code, not the last line.*

## What the script checks

1. Every relative `href` and `src` on every page — site and documentation — resolves.
2. Every cross-page `#anchor` exists on its target page.
3. Every documentation page links every other (the presentation carries no documentation links).
4. Exactly one `h1`, a `<title>` and a `lang` attribute on every page.
5. Every image has alt text (the site has none today; the check stays for when it does).
6. Every site page carries the prototype banner.
7. One asset version (`?v=`) on every page, so a stale stylesheet can never pass for the new one.
8. **The data reproduces**: `data/convert.py --check` rebuilds `stats.json` from `data/raw/` in
   memory — running every data assert (goals for = goals against, points reconcile, the two files
   of a competition agree match by match, goal lists match scores, every team in the name table,
   the bracket resolves) — and fails if the committed file differs by a byte.
9. **The pages reproduce**: `build.py --check` regenerates every generated page in memory (39 since round 2, the redirects included) (which also runs
   every copy premise in `content.py`) and fails if a committed page differs — so a hand edit to a
   generated page cannot survive.
10. **Contrast**: 24 text/background pairs from `tokens.css`, in the light and the dark theme (48
    checks), against WCAG 2.2 AA — 4.5:1 for text, 3:1 for the blue and orange as chart marks.
11. **Inert controls are marked**: every `is-unavailable` element has `aria-disabled="true"` and a
    `title` that says why.
12. **The owner's article rules, measured on the page** (added 2026-09-25, round 2; the desk added in
    round 3): every `articles/*.html` sits on one of the eight desks whose page exists, has 800–3,200 characters of body text (the text of every `data-count`
    paragraph — standfirst and paragraphs, spaces included), at least three headed segments, and
    both source lists — used, and investigated but not used — each with at least one `https` link.
    This is independent of `build.py`, which asserts the same rules before it writes a page.

The root `check.py` adds: no studio name on any project page, no tooling in footers, eyebrows,
titles or the documentation brand, no internal documentation link in the presentation, and a
repo-wide link audit.

## What is measured in the browser (not by the script)

The method's measured pass (`PROTOTYPING.md` §3.3) runs in the app's browser pane on a local
server: every page loaded in a same-origin iframe at an explicit width, measured from one script.

| Criterion | Target | Result 2026-09-25 |
|---|---|---|
| Horizontal overflow at 375 px | 0 px | 0 px on all 19 pages |
| Horizontal overflow at 1440 px | 0 px | 0 px on all 19 pages |
| Tap targets under 44 × 44 at 375 px | none | none on all 19 pages (inline links in running text exempt, per WCAG 2.5.8) |
| … with the More menu open | none | none (measured on four pages) |
| `h1` per page | 1 | 1 on all 19 pages, both widths |
| Console errors | 0 | 0 |
| Interactions | work | table sort (announced), overall/home/away, All columns, league filter, Load more, theme toggle (both ways, remembered), More sheet (focus in, Escape out, focus returned) — all exercised |

The phone width measured is 375 px, the owner's stated reference for this project; `PROTOTYPING.md`
§3.3 names 390 — 375 is the stricter of the two.

## Deliberate deviations

- **No prototype banner on documentation pages** — they are not the site.
- **Desktop density below 44 px** is allowed by the method; the only such controls are the league
  tabs' pill height at desktop widths (40 px), which rise to 44 px on phones.

## Round 2 measured pass (2026-09-25)

32 site pages (home, latest, six articles, topics index and eleven topic pages, How we work, style
guide, and the ten data pages) at 375 and 1440 px: 0 px overflow, one `h1` each, no tap target under
44 px at 375, 0 console errors; the old `/analysis/` URLs redirect to `/articles/`.

## Round 3 measured pass (2026-09-25)

41 site pages (round 2's 32 plus the desks index and eight desk pages) at 375 and 1440 px: 0 px
overflow, one `h1`, no tap target under 44 px at 375 after one fix, 0 console errors.
