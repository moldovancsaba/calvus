#!/usr/bin/env python3
"""The gameformative gate:  python3 gameformative/check.py — exit 1 on any finding.
 1 every relative href/src on every page (site + docs) resolves;  2 every cross-page #anchor exists;
 3 every docs page links every other (the presentation carries no docs navigation);
 4 one h1, a <title> and a lang attribute per page;  5 every image has alt text;
 6 every site page carries the prototype banner;  7 one asset version (?v=) on every page;
 8 data/stats.json reproduces byte for byte from data/raw/ (convert.py --check, which also runs the
   data asserts);  9 every generated page reproduces from content.py + stats.json (build.py --check);
10 every token text pair meets WCAG 2.2 AA contrast in the light and the dark theme;
11 every inert control is marked (aria-disabled and a title that says why)."""
import re, sys, subprocess, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
SITE = sorted(p for p in HERE.rglob("*.html") if "docs" not in p.relative_to(HERE).parts)
DOCS = sorted((HERE / "docs").glob("*.html")); ALL = SITE + DOCS
findings = []; refs = 0
text = {f: f.read_text(encoding="utf-8") for f in ALL}
ids = {f.resolve(): set(re.findall(r'\bid="([^"]+)"', t)) for f, t in text.items()}
for f, t in text.items():
    for m in re.finditer(r'(?:href|src)="([^"#?]+)(?:[#?][^"]*)?"', t):
        h = m.group(1).strip()
        if not h or h.startswith(("http", "mailto:", "tel:", "data:", "javascript:")): continue
        refs += 1
        if not (f.parent / h).exists(): findings.append(f"broken link  {f.relative_to(ROOT)} → {h}")
    for m in re.finditer(r'href="([^"#:?]*)#([^"]+)"', t):
        tgt = (f.parent / m.group(1)).resolve() if m.group(1) else f.resolve()
        if tgt in ids and m.group(2) not in ids[tgt]: findings.append(f"missing anchor  {f.relative_to(ROOT)} → {m.group(1)}#{m.group(2)}")
names = [p.stem for p in DOCS if p.stem != "presentation"]
for p in DOCS:
    if p.stem == "presentation": continue
    for n in names:
        if n != p.stem and f'href="{n}.html"' not in text[p]: findings.append(f"docs nav  {p.name} does not link {n}.html")
for f, t in text.items():
    n_h1 = len(re.findall(r"<h1[\s>]", t))
    if n_h1 != 1: findings.append(f"h1  {f.relative_to(ROOT)}: {n_h1} h1 elements")
    if not re.search(r"<title>[^<]+</title>", t): findings.append(f"title  {f.relative_to(ROOT)}: no <title>")
    if not re.search(r'<html[^>]+lang="', t): findings.append(f"lang  {f.relative_to(ROOT)}: no lang attribute")
    for m in re.finditer(r"<img\b[^>]*>", t):
        if not re.search(r'\balt="', m.group(0)): findings.append(f"alt  {f.relative_to(ROOT)}: image with no alt text")
versions = set()
for f in SITE:
    t = text[f]
    if 'class="proto-banner"' not in t: findings.append(f"banner  {f.relative_to(ROOT)} lacks the prototype banner")
    versions |= set(re.findall(r'assets/(?:tokens\.css|site\.css|site\.js)\?v=([^"]+)"', t))
    for m in re.finditer(r"<[^>]*\bis-unavailable\b[^>]*>", t):
        if 'aria-disabled="true"' not in m.group(0) or 'title="' not in m.group(0): findings.append(f"inert  {f.relative_to(ROOT)}: an inert control without aria-disabled and a title")
if len(versions) != 1: findings.append(f"asset version  pages load {sorted(versions)} — one version everywhere")

for script in (["data/convert.py", "--check"], ["build.py", "--check"]):
    r = subprocess.run([sys.executable, str(HERE / script[0]), script[1]], capture_output=True, text=True, cwd=HERE / pathlib.Path(script[0]).parent)
    if r.returncode != 0: findings.append(f"reproduce  {script[0]} --check: {(r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else 'failed'}")

# contrast: every text token on every ground token, both themes
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True); return (x + 0.05) / (y + 0.05)
css = (HERE / "assets" / "tokens.css").read_text(encoding="utf-8")
light = dict(re.findall(r"(--gf-[\w-]+):\s*(#[0-9A-Fa-f]{6})", css.split("@media")[0]))
dark = dict(light, **dict(re.findall(r"(--gf-[\w-]+):\s*(#[0-9A-Fa-f]{6})", css.split(':root[data-theme="dark"]')[1])))
PAIRS = [(fg, bg, 4.5) for fg in ("--gf-ink", "--gf-text", "--gf-muted", "--gf-blue", "--gf-orange-ink") for bg in ("--gf-ground", "--gf-surface", "--gf-sunk")] + \
        [("--gf-on-blue", "--gf-blue", 4.5), ("--gf-on-orange", "--gf-orange", 4.5), ("--gf-on-draw", "--gf-draw", 4.5), ("--gf-on-band", "--gf-band", 4.5), ("--gf-band-muted", "--gf-band", 4.5),
         ("--gf-blue", "--gf-blue-soft", 4.5), ("--gf-orange-ink", "--gf-orange-soft", 4.5), ("--gf-blue", "--gf-surface", 3), ("--gf-orange", "--gf-surface", 3)]
pairs_checked = 0
for theme, T in (("light", light), ("dark", dark)):
    for fg, bg, need in PAIRS:
        r = ratio(T[fg], T[bg]); pairs_checked += 1
        if r < need: findings.append(f"contrast  {theme}: {fg} on {bg} is {r:.2f}:1, needs {need}:1")

print(f"checked {len(ALL)} files ({len(SITE)} site, {len(DOCS)} docs), {refs} references, {pairs_checked} contrast pairs, asset version {sorted(versions)}")
if findings: print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
