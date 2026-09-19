#!/usr/bin/env python3
"""The Lexodont gate:  python3 lexodont.hu/check.py
Exit 1 on any finding. Covers both fidelities and the docs (docs/07-gate.md):
1. every relative href/src resolves on disk
2. every cross-page "#anchor" points at an existing id
3. every docs page links every other docs page
4. fidelity parity: the polished and sketch sets carry the same page names
5. stale-state phrases in the docs; the decision range in the docs index and the SSOT equals the register (ported 2026-09-20)
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


# stale-state phrases and consistency (ported from business.direct's gate, hub audit 2026-09-20)
docs_md = sorted((HERE / "docs").glob("*.md")) if (HERE / "docs").exists() else []
STALE = ["awaits the owner", "coming soon", "not yet built", "inert here", "will be built", "for approval", "awaiting approval of", "várja a jóváhagyást", "hamarosan"]
EXEMPT = ("04-decisions.md", "06-build-log.md", "07-gate.md", "README.md", "decisions.html", "build-log.html", "gate.html", "index.html", "bemutato.html")
for f in docs_md + DOCS:
    if f.name in EXEMPT: continue
    t = f.read_text(encoding="utf-8").lower()
    for ph in STALE:
        if ph in t: findings.append(f"stale phrase  {f.relative_to(ROOT)}: \"{ph}\"")
dec = HERE / "docs" / "04-decisions.md"
if dec.exists():
    nums = [int(x) for x in re.findall(r"^\| D(\d+) \|", dec.read_text(encoding="utf-8"), re.M)]
    if nums:
        last = max(nums)
        for f in (HERE / "docs" / "README.md", HERE / "docs" / "10-ssot.md"):
            if f.exists():
                for m in re.finditer(r"D1–D(\d+)", f.read_text(encoding="utf-8")):
                    if int(m.group(1)) != last: findings.append(f"stale count  {f.relative_to(ROOT)}: says D1–D{m.group(1)}, the register ends at D{last}")

print(f"checked {len(ALL)} files, {refs} references, {len(DOCS)} docs pages, {len(POLISHED)}/{len(SKETCH)} polished/sketch pages")
if findings:
    print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
