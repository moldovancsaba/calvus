#!/usr/bin/env python3
"""The Bízd ránk a zöldet gate:  python3 bizdrankazoldet/check.py — exit 1 on any finding.
1. every relative href/src/srcset on every page and docs page resolves; 2. every cross-page #anchor exists;
3. every docs page links every other; 4. one h1 per site page; 5. the prototype banner on every site page;
6. stale phrases; 7. every research figure carries a P or A mark; 8. no invented element: every image is the client's (assets/img)."""
import re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
SITE = sorted(HERE.glob("*.html")); DOCS = sorted((HERE / "docs").glob("*.html")); ALL = SITE + DOCS
findings = []; refs = 0
ids = {f: set(re.findall(r'id="([^"]+)"', f.read_text(encoding="utf-8"))) for f in ALL}
for f in ALL:
    t = f.read_text(encoding="utf-8")
    for m in re.finditer(r'(?:href|src|srcset)="([^"#?]+)(?:[#?][^"]*)?"', t):
        h = m.group(1).strip()
        if not h or h.startswith(("http", "mailto:", "tel:", "data:", "javascript:")): continue
        for part in h.split(","):
            p = part.strip().split(" ")[0]
            if p:
                refs += 1
                if not (f.parent / p).exists(): findings.append(f"broken link  {f.relative_to(ROOT)} → {p}")
    for m in re.finditer(r'href="([^"#:]*)#([^"]+)"', t):
        tgt = (f.parent / m.group(1)).resolve() if m.group(1) else f.resolve()
        tgt = next((k for k in ids if k.resolve() == tgt), None)
        if tgt is not None and m.group(2) not in ids[tgt]: findings.append(f"missing anchor  {f.relative_to(ROOT)} → {m.group(1)}#{m.group(2)}")
names = [p.stem for p in DOCS if p.stem != "bemutato"]
for p in DOCS:
    if p.stem == "bemutato": continue
    t = p.read_text(encoding="utf-8")
    for n in names:
        if n != p.stem and f'href="{n}.html"' not in t: findings.append(f"docs nav  {p.name} does not link {n}.html")
for f in SITE:
    t = f.read_text(encoding="utf-8")
    if t.count("<h1") != 1: findings.append(f"h1  {f.name}: {t.count('<h1')} h1 elements")
    if 'class="proto">Prototípus — Bízd ránk a zöldet, 2026.' not in t: findings.append(f"banner  {f.name} lacks the prototype banner")
    for m in re.finditer(r'<img[^>]+src="([^"]+)"', t):
        if not m.group(1).startswith("assets/img/"): findings.append(f"invented image  {f.name}: {m.group(1)}")
STALE = ["coming soon", "not yet built", "will be built", "awaits the owner"]
for f in sorted((HERE / "docs").glob("*.md")):
    if f.name in ("README.md", "06-build-log.md", "04-decisions.md", "07-gate.md"): continue
    low = f.read_text(encoding="utf-8").lower()
    for ph in STALE:
        if ph in low: findings.append(f"stale phrase  {f.relative_to(ROOT)}: \"{ph}\"")
research = (HERE / "docs/01-research.md").read_text(encoding="utf-8")
for para in research.split("\n- ")[1:]:
    if re.search(r"\d+ %|\d+×|million", para) and not re.search(r"\*\*[PA]\*\*", para): findings.append(f"unsourced  01-research.md: \"{para[:60]}…\"")
print(f"checked {len(ALL)} files, {refs} references, {len(SITE)} pages, {len(DOCS)} docs pages")
if findings: print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
