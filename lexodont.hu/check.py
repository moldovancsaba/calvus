#!/usr/bin/env python3
"""The Lexodont gate:  python3 lexodont.hu/check.py
Exit 1 on any finding. Covers both fidelities and the docs (docs/07-gate.md):
1. every relative href/src resolves on disk
2. every cross-page "#anchor" points at an existing id
3. every docs page links every other docs page
4. fidelity parity: the polished and sketch sets carry the same page names
"""
import re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
POLISHED = sorted(HERE.glob("*.html"))
SKETCH = sorted((ROOT / "lexodont.hu_balsamic").glob("*.html"))
DOCS = sorted((HERE / "docs").glob("*.html"))
ALL = POLISHED + SKETCH + DOCS
findings = []

ids = {f: set(re.findall(r'id="([^"]+)"', f.read_text(encoding="utf-8"))) for f in ALL}
refs = 0
for f in ALL:
    t = f.read_text(encoding="utf-8")
    for m in re.finditer(r'(?:href|src)="([^"#?]+)(?:[#?][^"]*)?"', t):
        h = m.group(1).strip()
        if not h or h.startswith(("http", "mailto:", "tel:", "data:", "javascript:")): continue
        refs += 1
        if not (f.parent / h).exists(): findings.append(f"broken link  {f.relative_to(ROOT)} → {h}")
    for m in re.finditer(r'href="([^"#:]*)#([^"]+)"', t):
        tgt = (f.parent / m.group(1)).resolve() if m.group(1) else f.resolve()
        tgt = next((k for k in ids if k.resolve() == tgt), None)
        if tgt is not None and m.group(2) not in ids[tgt]:
            findings.append(f"missing anchor  {f.relative_to(ROOT)} → {m.group(1)}#{m.group(2)}")

names = [p.stem for p in DOCS if p.stem != "bemutato"]
for p in DOCS:
    if p.stem == "bemutato": continue
    t = p.read_text(encoding="utf-8")
    for n in names:
        if n != p.stem and f'href="{n}.html"' not in t: findings.append(f"docs nav  {p.name} does not link {n}.html")

pol, ske = {p.name for p in POLISHED}, {p.name for p in SKETCH}
for n in sorted(pol - ske): findings.append(f"parity  sketch set lacks {n}")
for n in sorted(ske - pol): findings.append(f"parity  polished set lacks {n}")

print(f"checked {len(ALL)} files, {refs} references, {len(DOCS)} docs pages, {len(POLISHED)}/{len(SKETCH)} polished/sketch pages")
if findings:
    print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
