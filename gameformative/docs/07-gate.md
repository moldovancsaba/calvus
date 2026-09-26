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

13. **Discovery** (added 2026-09-26): canonical on every page; Open Graph and X-card tags whose image
    exists locally; JSON-LD that parses; `sitemap.xml` and `feed.xml` that parse and list only real
    pages (and the sitemap every article, desk and subject page); a 1200×630 share image within
    300 kB for every article; the icon set. 12b: every article source links its catalogue entry.

## What is measured in the browser (not by the script)

The method's measured pass (`PROTOTYPING.md` §3.3) runs in the app's browser pane on a local
server: every page loaded in a same-origin iframe at an explicit width, measured from one script.

| Criterion | Target | Result 2026-09-26 (after the round-4 clean-up) |
|---|---|---|
| Horizontal overflow at 375 px | 0 px | 0 px on all 41 site pages and all 19 documentation pages |
| Horizontal overflow at 1440 px | 0 px | 0 px on all 41 site pages and all 19 documentation pages |
| Tap targets under 44 × 44 at 375 px | none | none on any of the 60 pages (inline links in running text exempt, per WCAG 2.5.8) |
| `h1` per page | 1 | 1 on every page, both widths |
| Console errors | 0 | 0 |
| Interactions | work | Load more (5 → 6 articles), theme toggle both ways, More sheet (opens; Escape closes and returns focus), on a data page All columns, sort by goals for, the home view — all exercised |

The 41 site pages: home, latest, the desks index and eight desk pages, the subjects index and eleven
subject pages, six articles, How we work, the style guide, and the ten later-phase data pages. The
seven redirects from `/analysis/` are checked to land on `/articles/`. Earlier passes are in
`06-build-log.md`.

The phone width measured is 375 px, the owner's stated reference for this project; `PROTOTYPING.md`
§3.3 names 390 — 375 is the stricter of the two.

## Deliberate deviations

- **No prototype banner on documentation pages** — they are not the site.
- **Desktop density below 44 px** is allowed by the method; the only such controls are the league
  tabs' pill height at desktop widths (40 px), which rise to 44 px on phones.
