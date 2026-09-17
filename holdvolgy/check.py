#!/usr/bin/env python3
"""The Holdvölgy gate, in one command:  python3 holdvolgy/check.py
Exit 1 on any finding. Run before every push (CLAUDE.md rule 2).
1. every relative href/src/srcset in every HTML file resolves on disk
2. every cross-page "#anchor" points at an existing id
3. every docs page links every other docs page
4. no stale-state phrase on any site page or docs index (things that were true once:
   "in Phase N", "coming soon", "for approval", "not yet built", placeholders)
5. every site page carries the current prototype banner, none the old one
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = [p for p in (ROOT/"holdvolgy").rglob("*.html") if "docs" not in p.parts]
DOCS = sorted((ROOT/"holdvolgy"/"docs").glob("*.html"))
ALL  = SITE + DOCS + [ROOT/"index.html"] + sorted((ROOT/"discountdirect").glob("*.html"))
findings = []

# 1 + 2
ids = {f: set(re.findall(r'id="([^"]+)"', f.read_text(encoding="utf-8"))) for f in ALL}
refs = 0
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

# 3 — every documentation page links every other; client-facing pages carry no documentation menu by design
CLIENT_PAGES = {"bemutato"}
names = [p.stem for p in DOCS if p.stem not in CLIENT_PAGES]
for p in DOCS:
    if p.stem in CLIENT_PAGES: continue
    t = p.read_text(encoding="utf-8")
    for q in names:
        if q != p.stem and f'href="{q}.html"' not in t: findings.append(f"docs nav gap  {p.name} lacks {q}.html")

# 4 — stale-state phrases; the docs' dated build records are allowed to say what was true then
STALE = [r"\b[0-9]\.\s+fázisban\s+készül", r"\bPhase\s+[0-9]\s+(?:builds|will|follow)", r"Shop\s+pages\s+follow", r"ideiglenesen\s+a", r"for\s+approval\b", r"gate\s+[0-9]\s+of\s+[0-9]",
         r"hamarosan\s+elérhető", r"coming\s+soon", r"not\s+yet\s+(?:built|coded)", r"Nothing\s+here\s+is\s+coded", r"lorem\s+ipsum", r"\bTODO\b", r"\bplaceholder\b(?!=)", r"until\s+Phase\s+[0-9]"]
SCAN = SITE + [ROOT/"holdvolgy"/"docs"/"index.html", ROOT/"holdvolgy"/"docs"/"design-system.html", ROOT/"holdvolgy"/"docs"/"layouts.html", ROOT/"holdvolgy"/"docs"/"plan.html", ROOT/"index.html", ROOT/"README.md"]
for f in SCAN:
    t = f.read_text(encoding="utf-8")
    for pat in STALE:
        for m in re.finditer(pat, t, re.I):
            ctx = t[max(0, m.start()-40):m.end()+40].replace("\n", " ")
            findings.append(f"stale phrase  {f.relative_to(ROOT)}: …{ctx}…")

# 5 — one banner, current, everywhere (the redirect stub has none)
site_pages = [p for p in SITE if p.name != "index.html" or p.parent.name != "borok"]
banners = {}
for p in site_pages:
    m = re.search(r'<p class="proto">(.*?)</p>', p.read_text(encoding="utf-8"))
    banners.setdefault(m.group(1) if m else "MISSING", []).append(p)
if len(banners) > 2 or "MISSING" in banners:
    findings.append("banner  " + "; ".join(f"{len(v)} pages: {k[:60]}" for k, v in banners.items()))

print(f"checked {len(ALL)} files, {refs} references, {len(SCAN)} stale-scan targets, {len(site_pages)} banners")
for x in findings: print("  ", x)
print("GATE:", "CLEAN" if not findings else f"{len(findings)} FINDINGS")
sys.exit(1 if findings else 0)
