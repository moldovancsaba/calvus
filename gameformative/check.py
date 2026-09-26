#!/usr/bin/env python3
"""The gameformative gate:  python3 gameformative/check.py — exit 1 on any finding.
 1 every relative href/src on every page (site + docs) resolves;  2 every cross-page #anchor exists;
 3 every docs page links every other (the presentation carries no docs navigation);
 4 one h1, a <title> and a lang attribute per page;  5 every image has alt text;
 6 every site page carries the prototype banner;  7 one asset version (?v=) on every page;
 8 data/stats.json reproduces byte for byte from data/raw/ (convert.py --check, which also runs the
   data asserts);  9 every generated page reproduces from content.py + stats.json (build.py --check);
10 every token text pair meets WCAG 2.2 AA contrast in the light and the dark theme;
11 every inert control is marked (aria-disabled and a title that says why);
12 the owner's article rules, measured on every rendered article page: one of the eight desks (its
   desk page exists), 800–3,200 characters of body text (standfirst + paragraphs, spaces included),
   at least three headed segments, and both source lists — used, and investigated but not used —
   each with at least one linked source, and every source linked to its catalogue entry;
13 discovery (added 2026-09-26): every page has a canonical URL, Open Graph and X-card tags whose
   image exists locally, and valid JSON-LD; sitemap.xml and feed.xml parse and point only at pages
   that exist, and the sitemap lists every article, desk and subject page; every article has a
   1200×630 share image within 300 kB; the icon set exists."""
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

# the article rules, measured on the page, independently of build.py's own assert
import html as _html
articles = sorted(p for p in (HERE / "articles").glob("*.html") if p.name != "index.html")
if not articles: findings.append("articles  no article pages found")
for f in articles:
    t2 = text[f]; m = re.search(r'data-article data-desk="([a-z]+)" data-min="(\d+)" data-max="(\d+)" data-segments="(\d+)"', t2)
    if not m: findings.append(f"article  {f.relative_to(ROOT)}: no desk or article rules on the page"); continue
    desk = m.group(1); lo, hi, segs = map(int, m.groups()[1:])
    if not (HERE / "desks" / f"{desk}.html").exists(): findings.append(f"article  {f.relative_to(ROOT)}: desk '{desk}' has no desk page")
    body = "".join(_html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r"<p[^>]*\bdata-count\b[^>]*>(.*?)</p>", t2, re.S))
    if not lo <= len(body) <= hi: findings.append(f"article  {f.relative_to(ROOT)}: {len(body)} characters, outside {lo}–{hi}")
    n_seg = len(re.findall(r'<section class="gf-seg-block"[^>]*><h2', t2))
    if n_seg < segs: findings.append(f"article  {f.relative_to(ROOT)}: {n_seg} headed segments, needs {segs}")
    for kind in ("used", "investigated"):
        lst = re.search(rf'<ol class="gf-source-list" data-sources="{kind}">(.*?)</ol>', t2, re.S)
        if not lst or not re.search(r'<li><a href="https://', lst.group(1)): findings.append(f"article  {f.relative_to(ROOT)}: no linked source in the '{kind}' list")

# 12b every article source links to its catalogue entry (the anchor itself is checked by §2)
for f in articles:
    for m in re.finditer(r'<ol class="gf-source-list" data-sources="\w+">(.*?)</ol>', text[f], re.S):
        for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.S):
            if 'href="../sources/index.html#src-' not in li: findings.append(f"catalogue  {f.relative_to(ROOT)}: a source with no catalogue link")

# 13 discovery
import json as _json, struct, xml.etree.ElementTree as ET
bases = set()
for f in SITE:
    t2 = text[f]
    if 'http-equiv="refresh"' in t2: continue  # redirect stubs
    can = re.search(r'<link rel="canonical" href="([^"]+)"', t2)
    if not can: findings.append(f"discovery  {f.relative_to(ROOT)}: no canonical"); continue
    rel = f.relative_to(HERE).as_posix()
    base = can.group(1)[: len(can.group(1)) - len(rel[:-10] if rel.endswith("index.html") else rel)] if (can.group(1).endswith(rel) or rel.endswith("index.html")) else None
    bases.add(base)
    for tag in ("og:title", "og:description", "og:url", "og:image", "og:type"):
        if f'property="{tag}"' not in t2: findings.append(f"discovery  {f.relative_to(ROOT)}: no {tag}")
    if 'name="twitter:card" content="summary_large_image"' not in t2: findings.append(f"discovery  {f.relative_to(ROOT)}: no X card")
    img = re.search(r'property="og:image" content="([^"]+)"', t2)
    if img and base and not (HERE / img.group(1)[len(base):]).exists(): findings.append(f"discovery  {f.relative_to(ROOT)}: og:image {img.group(1)} does not exist")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t2, re.S):
        try: _json.loads(block)
        except ValueError as e: findings.append(f"discovery  {f.relative_to(ROOT)}: JSON-LD does not parse ({e})")
if len(bases) != 1 or None in bases: findings.append(f"discovery  canonical URLs do not share one base: {sorted(map(str, bases))}")
base = next(iter(bases)) if len(bases) == 1 else ""
def local(u):
    p = HERE / u[len(base):]
    return p / "index.html" if (u.endswith("/") or p.is_dir()) else p
try:
    locs = [e.text for e in ET.parse(HERE / "sitemap.xml").getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    for u in locs:
        if not u.startswith(base) or not local(u).exists(): findings.append(f"discovery  sitemap lists {u}, which does not exist")
    for d in ("articles", "desks", "topics"):
        for f in (HERE / d).glob("*.html"):
            if f.name == "index.html": continue
            if base + f.relative_to(HERE).as_posix() not in locs: findings.append(f"discovery  sitemap misses {f.relative_to(HERE)}")
except (ET.ParseError, FileNotFoundError) as e: findings.append(f"discovery  sitemap.xml: {e}")
try:
    items = ET.parse(HERE / "feed.xml").getroot().findall("./channel/item")
    if len(items) != len(articles): findings.append(f"discovery  feed.xml has {len(items)} items for {len(articles)} articles")
    for it in items:
        if not local(it.findtext("link")).exists(): findings.append(f"discovery  feed item {it.findtext('link')} does not exist")
except (ET.ParseError, FileNotFoundError) as e: findings.append(f"discovery  feed.xml: {e}")
def png_size(p):
    b = p.read_bytes()[:24]
    return struct.unpack(">II", b[16:24]) if b[:8] == b"\x89PNG\r\n\x1a\n" else None
for f in articles + [HERE / "default.html"]:
    img = HERE / "assets" / "share" / (f.stem + ".png")
    if not img.exists(): findings.append(f"discovery  no share image for {f.stem}"); continue
    if png_size(img) != (1200, 630): findings.append(f"discovery  {img.name} is {png_size(img)}, not 1200×630")
    if img.stat().st_size > 300_000: findings.append(f"discovery  {img.name} is {img.stat().st_size:,} bytes, over 300 kB")
for name, size in (("icon-32.png", (32, 32)), ("icon-192.png", (192, 192)), ("icon-512.png", (512, 512)), ("apple-touch-icon.png", (180, 180))):
    p2 = HERE / "assets" / "icons" / name
    if not p2.exists() or png_size(p2) != size: findings.append(f"discovery  icon {name} missing or not {size}")
for name in ("robots.txt", "llms.txt", "manifest.webmanifest", "assets/icons/favicon.svg"):
    if not (HERE / name).exists(): findings.append(f"discovery  {name} missing")

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

print(f"checked {len(ALL)} files ({len(SITE)} site, {len(DOCS)} docs), {refs} references, {len(articles)} articles against the house rules, {pairs_checked} contrast pairs, asset version {sorted(versions)}")
if findings: print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
