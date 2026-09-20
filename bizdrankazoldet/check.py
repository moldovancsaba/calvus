#!/usr/bin/env python3
"""The Bízd ránk a zöldet gate:  python3 bizdrankazoldet/check.py — exit 1 on any finding.
1. every relative href/src in the docs resolves; 2. every docs page links every other; 3. stale phrases;
4. every research figure's paragraph carries a P or A mark (the standard's sourcing rule)."""
import re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
DOCS = sorted((HERE / "docs").glob("*.html")); findings = []; refs = 0
for f in DOCS:
    t = f.read_text(encoding="utf-8")
    for m in re.finditer(r'(?:href|src)="([^"#?]+)(?:[#?][^"]*)?"', t):
        h = m.group(1).strip()
        if not h or h.startswith(("http", "mailto:", "tel:", "data:")): continue
        refs += 1
        if not (f.parent / h).exists(): findings.append(f"broken link  {f.relative_to(ROOT)} → {h}")
names = [p.stem for p in DOCS]
for p in DOCS:
    t = p.read_text(encoding="utf-8")
    for n in names:
        if n != p.stem and f'href="{n}.html"' not in t: findings.append(f"docs nav  {p.name} does not link {n}.html")
STALE = ["coming soon", "not yet built", "will be built", "awaits the owner"]
for f in sorted((HERE / "docs").glob("*.md")):
    if f.name == "README.md": continue
    low = f.read_text(encoding="utf-8").lower()
    for ph in STALE:
        if ph in low: findings.append(f"stale phrase  {f.relative_to(ROOT)}: \"{ph}\"")
research = (HERE / "docs/01-research.md").read_text(encoding="utf-8")
for para in research.split("\n- ")[1:]:
    if re.search(r"\d+ %|\d+×|million", para) and not re.search(r"\*\*[PA]\*\*", para): findings.append(f"unsourced  01-research.md: \"{para[:60]}…\"")
print(f"checked {len(DOCS)} docs pages, {refs} references")
if findings: print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
