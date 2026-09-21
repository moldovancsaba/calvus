#!/usr/bin/env python3
"""The Népszabadság gate:  python3 nepszabadsag/check.py — exit 1 on any finding.
1. every relative href/src on every page (site + docs) resolves; 2. every cross-page #anchor
exists; 3. every docs page links every other; 4. one h1 per page; 5. lang attribute set."""
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
names = [p.stem for p in DOCS]
for p in DOCS:
    t = p.read_text(encoding="utf-8")
    for n in names:
        if n != p.stem and f'href="{n}.html"' not in t: findings.append(f"docs nav  {p.name} does not link {n}.html")
for f in ALL:
    t = f.read_text(encoding="utf-8")
    if t.count("<h1") != 1: findings.append(f"h1  {f.relative_to(ROOT)}: {t.count('<h1')} h1 elements")
    if not re.search(r'<html[^>]+lang="', t): findings.append(f"lang  {f.relative_to(ROOT)}: no lang attribute")
print(f"checked {len(ALL)} files, {refs} references, {len(SITE)} site pages, {len(DOCS)} docs pages")
if findings: print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
