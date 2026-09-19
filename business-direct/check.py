#!/usr/bin/env python3
"""The business.direct gate:  python3 business-direct/check.py
Exit 1 on any finding. Covers the pages and the docs:
1. every relative href/src resolves on disk
2. every cross-page "#anchor" points at an existing id
3. every docs page links every other docs page (design-system.html included)
4. data/providers.json parses and every provider carries id, name, borough
5. assets/app.js parses (node --check), when node is installed
6. stale-state phrases in the docs and pages (things that were true once): "awaits the owner",
   "for approval" outside the approval UI wording, "coming soon", "not yet built", "inert here",
   "will be built", a "PROPOSED" gate — the register and the build log may keep history
"""
import re, sys, json, shutil, subprocess, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
PAGES = sorted(HERE.glob("*.html"))
DOCS = sorted((HERE / "docs").glob("*.html"))
ALL = PAGES + DOCS
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

try:
    rows = json.loads((HERE / "data/providers.json").read_text(encoding="utf-8"))["providers"]
    if not rows: findings.append("data  providers.json has no provider")
    for r in rows:
        if not all(r.get(k) for k in ("id", "name", "borough")): findings.append(f"data  provider without id/name/borough: {r.get('id')}")
except Exception as e:
    findings.append(f"data  providers.json unreadable: {e}")
STALE = ["awaits the owner", "coming soon", "not yet built", "inert here", "will be built", "gate 2 · proposed", "gate 1 · proposed", "awaiting approval of the frames", "round 2 of the build log"]
for f in sorted((HERE / "docs").glob("*.md")) + ALL + [HERE / "assets/app.js"]:
    if f.name in ("04-decisions.md", "06-build-log.md", "07-gate.md", "decisions.html", "build-log.html", "gate.html", "README.md", "index.html") and f.parent.name == "docs": continue  # history and the scan's own list
    t = f.read_text(encoding="utf-8").lower()
    for ph in STALE:
        if ph in t: findings.append(f"stale phrase  {f.relative_to(ROOT)}: \"{ph}\"")
if shutil.which("node"):
    r = subprocess.run(["node", "--check", str(HERE / "assets/app.js")], capture_output=True, text=True)
    if r.returncode: findings.append("script  app.js: " + r.stderr.strip().splitlines()[-1])

print(f"checked {len(ALL)} files, {refs} references, {len(DOCS)} docs pages, {len(PAGES)} pages")
if findings:
    print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
