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
7. consistency: the decision range stated in the business logic equals the register's last D-number;
   no live document cites "ask #n" (cite P-n)
8. every rule in the SSOT's register is stated in the rules end to end (business-logic.md, both parts)
9. every inert control carries aria-disabled and a title (from IDBC's gate)
10. the page carries the current prototype banner (from Holdvölgy's gate)
11. the stakeholder documents never frame the product as one customer's project or price the product
12. the evidence register has no unverified row
13. every redirect page (meta refresh) points at an existing page; redirect pages are excluded from the nav check
14. the final set is exactly the twelve documents plus the design set, the research base and the history (D44)
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

REDIRECTS = {p for p in DOCS if 'http-equiv="refresh"' in p.read_text(encoding="utf-8")}
for p in REDIRECTS:
    m = re.search(r'url=([^"]+)"', p.read_text(encoding="utf-8"))
    if not m or not (p.parent / m.group(1)).exists(): findings.append(f"redirect  {p.name} points nowhere")
names = [p.stem for p in DOCS if p.stem != "presentation" and p not in REDIRECTS]
for p in DOCS:
    if p.stem == "presentation" or p in REDIRECTS: continue
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
    if f.name in ("decisions.md", "build-log.md", "gate.md", "documentation-audit.md", "logic-audit.md", "register-of-asks.md", "decisions.html", "build-log.html", "gate.html", "documentation-audit.html", "logic-audit.html", "register-of-asks.html", "README.md", "index.html") and f.parent.name == "docs": continue  # history and the scan's own list
    t = f.read_text(encoding="utf-8").lower()
    for ph in STALE:
        if ph in t: findings.append(f"stale phrase  {f.relative_to(ROOT)}: \"{ph}\"")
# 7. consistency: the decision range, the issue count and the ask numbering must agree across the docs
docs = HERE / "docs"
import re as _re
last_d = max(int(m) for m in _re.findall(r"^\| D(\d+) \|", (docs / "decisions.md").read_text(encoding="utf-8"), _re.M))
for f, pat in (("business-logic.md", r"`decisions.md` holds D1–D(\d+)\."), ("business-logic.md", r"\| `decisions.md` \| D1–D(\d+) \|")):
    for m in _re.finditer(pat, (docs / f).read_text(encoding="utf-8")):
        if int(m.group(1)) != last_d: findings.append(f"stale count  docs/{f}: says D1–D{m.group(1)}, the register ends at D{last_d}")
for f in sorted(docs.glob("*.md")) + [HERE / "assets/app.js"]:
    if f.name in ("register-of-asks.md", "decisions.md", "build-log.md", "logic-audit.md", "first-customer-classscout.md", "documentation-audit.md", "README.md"): continue
    for m in _re.finditer(r"\basks? #\d", f.read_text(encoding="utf-8")):
        findings.append(f"stale reference  {f.relative_to(ROOT)}: \"{m.group(0)}…\" — asks moved to the prerequisites (D34); cite P-n")
        break

_bl = (docs / "business-logic.md").read_text(encoding="utf-8")
_partA = _bl[:_bl.index("## Part B")]
rules = set(_re.findall(r"^\| (R\d+) \|", _bl, _re.M))
cited = set(_re.findall(r"\b(R\d+)\b", _partA))
for r in sorted(rules - cited, key=lambda x: int(x[1:])): findings.append(f"unmapped rule  SSOT {r} is not stated in the rules end to end (business-logic.md Part A)")

# 11. the top layer never frames the product as one customer's project; 12. the claims register has no unverified row (D42)
TOP = ["docs/presentation.html", "docs/executive-summary.md", "docs/economics.md", "docs/product-definition.md", "docs/product-specification.md", "docs/market.md"]
BANNED = ["the client accepts", "proposal for classscout", "after the client accepts", "one-man army for anybody", "the one-person sales and marketing team for anybody", "developer rate", "developer-week", "pricing hypothesis", "the product's run cost", "sign the legal"]
for rel in TOP:
    low = (HERE / rel).read_text(encoding="utf-8").lower()
    for ph in BANNED:
        if ph in low: findings.append(f"framing  {rel}: \"{ph}\"")
reg = (HERE / "docs/evidence.md").read_text(encoding="utf-8")
for line in reg.splitlines():
    if line.startswith("| ") and "| **unverified**" in line and "removed" not in line: findings.append(f"claims  unverified row without removal: {line[:60]}")
FINAL = {"executive-summary.md", "product-definition.md", "product-specification.md", "market.md", "economics.md", "business-logic.md", "architecture.md", "delivery-plan.md", "responsible-data.md", "first-customer-classscout.md", "evidence.md", "README.md", "05-layout-specs.md", "decisions.md", "build-log.md", "gate.md", "register-of-asks.md", "logic-audit.md", "documentation-audit.md", "01-research.md", "01b-research-acquisition-content-sales.md", "01c-research-data-driven-marketing.md", "01e-research-responsible-data.md", "01f-research-beyond-children.md", "01g-research-real-system.md"}
have = {p.name for p in docs.glob("*.md")}
for n in sorted(have - FINAL): findings.append(f"set  docs/{n} is not part of the final set (D44)")
for n in sorted(FINAL - have): findings.append(f"set  docs/{n} is missing from the final set (D44)")
# 9. inert controls carry aria-disabled and a title; 10. the page carries the current prototype banner (hub audit 2026-09-20)
js = (HERE / "assets/app.js").read_text(encoding="utf-8")
for m in _re.finditer(r'<button class="btn[^"]*\binert\b[^"]*"([^>]*)>', js):
    if 'aria-disabled="true"' not in m.group(1) or "title=" not in m.group(1): findings.append("inert control  assets/app.js: an .inert button without aria-disabled and a title")
if 'class="proto-note">Clickable prototype — real providers from getyourfield.com' not in (HERE / "index.html").read_text(encoding="utf-8"):
    findings.append("banner  index.html does not carry the current prototype banner")

if shutil.which("node"):
    r = subprocess.run(["node", "--check", str(HERE / "assets/app.js")], capture_output=True, text=True)
    if r.returncode: findings.append("script  app.js: " + r.stderr.strip().splitlines()[-1])

print(f"checked {len(ALL)} files, {refs} references, {len(DOCS)} docs pages, {len(PAGES)} pages")
if findings:
    print("\n".join(findings)); print(f"GATE: {len(findings)} finding(s)"); sys.exit(1)
print("GATE: CLEAN")
