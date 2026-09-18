#!/usr/bin/env python3
"""The IDBC Salary Guide gate, in one command:  python3 idbc-salary-guide/check.py
Exit 1 on any finding. Run before every push (CLAUDE.md rule 2). What it checks is
described in docs/07-gate.md:
1. every relative href/src in every guide page and docs page resolves on disk
2. every cross-page "#anchor" points at an existing id
3. every docs page links every other docs page
4. the shared chart assets carry the same ?v= on every page that loads them
5. every inert control still carries is-unavailable
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
PAGES = sorted(p for p in ROOT.rglob("*.html") if "docs" not in p.parts)
DOCS = sorted((ROOT / "docs").glob("*.html"))
ALL = PAGES + DOCS
findings = []

# 1 + 2
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

# 3 — every documentation page links every other; the client-facing bemutató carries no docs menu
names = [p.stem for p in DOCS if p.stem != "bemutato"]
for p in DOCS:
    if p.stem == "bemutato": continue
    t = p.read_text(encoding="utf-8")
    for n in names:
        if n != p.stem and f'href="{n}.html"' not in t: findings.append(f"docs nav  {p.name} does not link {n}.html")

# 4 — one renderer version everywhere
versions = {}
for f in PAGES:
    for m in re.finditer(r'assets/(top3-chart\.js|chart\.css)\?v=(\d+)', f.read_text(encoding="utf-8")):
        versions.setdefault(m.group(1), {}).setdefault(m.group(2), []).append(f.relative_to(ROOT).as_posix())
for asset, byv in versions.items():
    if len(byv) > 1: findings.append(f"asset version  {asset} loaded as " + ", ".join(f"v={v} by {', '.join(fs)}" for v, fs in byv.items()))

# 5 — inert controls say so
INERT = {"Excel letöltése": "Excel CTA", "Kijelentkezés": "logout", "Regisztrálok": "registration submit",
         "Csatlakozás elküldése": "join submit", "Ajánlatkérés elküldése": "contact submit"}
for f in PAGES:
    t = f.read_text(encoding="utf-8")
    for label, what in INERT.items():
        for m in re.finditer(r'<(?:a|button|span)\b[^>]*>[^<]*' + re.escape(label), t):
            if "is-unavailable" not in m.group(0): findings.append(f"inert control live  {f.relative_to(ROOT)}: {what}")

print(f"checked {len(ALL)} files, {refs} references, {len(DOCS)} docs pages, {sum(len(v) for v in versions.values())} asset versions")
if findings:
    print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
