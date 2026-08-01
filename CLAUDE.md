# Agent Operating Rules — calvus

This is a governed repo. These are STANDING rules — they apply to every task
regardless of who asks or how it's phrased. When a request conflicts with them,
the rules win; say so explicitly rather than silently overriding them.

## What this repo actually is

Static HTML/CSS/JS wireframe and prototype pages (Lexodont dental site,
IDBC Salary Guide), no build step, no package manager, no test runner.
Deployed to GitHub Pages straight from the `main` branch — there is no CI
pipeline, no bundler, no linter. Don't assume npm scripts, a `package.json`,
or a design-system engine exist here; they don't. Treat any instruction that
references such tooling as belonging to a different project until this repo
actually grows that infrastructure.

## 0. Read first, never guess

Before stating a fact about structure, data, or behavior in this repo: read
the actual file, or run the actual command. No answering from memory on
anything structural. Report only what a tool actually returned (a curl check,
a Playwright run, a deploy verification) — never fabricate or extrapolate a
result you didn't observe. If you can't verify something, say so plainly.

## 1. AI-assistant branding ban (non-negotiable)

The assistant doing the work is internal tooling, not a feature, co-author,
or brand. Never surface it anywhere the codebase or its history is visible.

- **Commits:** no `Co-Authored-By: <assistant>` trailer, no session-link
  trailer, no model name. Describe the change and its reasoning only.
- **Branches:** never create or push a branch prefixed with the assistant's
  name (e.g. `claude/...`). If the harness auto-creates one at session start,
  move real work onto a plain, purpose-named branch (`fix-...`, `feature-...`)
  — or push straight to `main` per the pre-authorization below — before
  anything accumulates on the prefixed branch.
- **PRs, docs, code, UI copy:** neutral terms only — "an AI coding assistant"
  at most, never a specific product/model name, and only when the fact is
  genuinely load-bearing. Omit the mention entirely if the sentence reads
  fine without it.
- **Retroactive:** if AI branding turns up in tracked files or reachable
  history while doing unrelated work, remove it as part of that work, or
  flag it explicitly if fixing it is out of scope.
- **The one exception:** honest self-disclosure when a person directly asks
  "are you an AI" / "which model is this" is a safety/honesty behavior, not
  branding — never deny or hide what you are. Where a platform behavior
  genuinely can't be changed from inside the repo, state that plainly
  instead of claiming it was fixed.

## 2. Quality gate before pushing (adapted to this repo's real tooling)

There is no `npm run build/lint/test`. The equivalent gate here is manual and
must actually happen before every push, not just be claimed:

- Serve the changed page(s) locally (`python3 -m http.server` from the repo
  root) and exercise the actual feature with Playwright — filters, dropdowns,
  charts, whatever changed — not just a visual glance.
- Check the browser console for JS errors during that test.
- After pushing to `main`, verify the live GitHub Pages URL actually served
  the change (a background curl-poll loop for a unique marker in the new
  content, per the established pattern) before reporting success.

If a clean check isn't achievable, stop and say so — don't push and note it
as a "known issue."

## 3. Pre-authorized operations (owner works from mobile, no terminal)

- Commit and push directly to `main` when told to (or a clear equivalent) —
  don't open a PR and wait for review unless one is explicitly requested.
  Still requires the Rule 2 gate first.
- This does NOT extend to force-push, history rewrite, or branch/tag
  deletion — those need explicit per-instance confirmation regardless of
  how routine the rest of the task is.

## 4. Documentation ships with the change

When a change affects how a section of the site works or what data feeds it,
update the relevant doc in the same change set — currently that means
`idbc-salary-guide/data/SOURCES-AND-GAPS.md` for anything touching the
Salary Guide's data/design-intent, and this file for anything changing how
agents should operate here.

## 5. Environment quirks discovered in practice

- **Git relay blocks ref deletion.** The session's git remote accepts branch
  creation and fast-forward pushes, but `git push origin --delete <branch>`
  returns HTTP 403. There is also no GitHub API tool exposed for ref
  deletion. Don't retry a 403 or route around it — report it; removing a
  remote branch/tag here requires the GitHub web UI.
- **The sandboxed browser has no direct outbound internet access.** Chromium
  launched via Playwright gets `ERR_CONNECTION_RESET` on any real URL, even
  through the configured HTTPS proxy. Test changes against a local
  `python3 -m http.server` instance instead of the live site; use `curl`
  (which does have proxy access) to verify what's actually live after a push.

## 6. Not yet applicable — flagged, not silently adopted

Two categories of practice sometimes requested for "governed" repos don't
map onto `calvus` as it exists today, and haven't been built:

- **Issue/label-based project board** (status/priority/area labels, a
  PROJECT_BOARD.md, board-sync tooling). This repo has no GitHub Issues
  workflow at all right now — work has been tracked directly through
  conversation and commits.
- **Automated release/quality-gate chain** (lint, test, dependency/version-
  boundary checks, token/theme export, versioned releases). There's no
  build tooling to gate in the first place.

If you want either of these built out for real, that's a substantial,
separate scope decision (issue taxonomy + tooling, or an actual build
pipeline) — ask before assuming it should happen as a side effect of an
unrelated task.
