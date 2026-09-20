#!/usr/bin/env python3
"""The repo gate, in one command:  python3 check.py
Runs every project's own gate and a repo-wide link audit over every HTML file that no
project gate covers (the hub). Exit 1 if any of them finds something.

  holdvolgy/check.py          Holdvölgy site + docs, DiscountDirect pages, the hub: links, anchors,
                              docs cross-links, stale-phrase scan, prototype banner
  idbc-salary-guide/check.py  links, anchors, docs cross-links, one chart-asset version, inert controls
  lexodont.hu/check.py        both fidelities + docs: links, anchors, docs cross-links, parity
  business-direct/check.py    pages + docs: links, anchors, docs cross-links
  bizdrankazoldet/check.py    docs: links, cross-links, stale phrases, sourced figures
"""
import re, subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
GATES = ["holdvolgy/check.py", "idbc-salary-guide/check.py", "lexodont.hu/check.py", "business-direct/check.py", "bizdrankazoldet/check.py"]
failed = []
for g in GATES:
    r = subprocess.run([sys.executable, str(ROOT / g)], capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
    print(f"{g:28s} {last}")
    if r.returncode != 0:
        failed.append(g); print(r.stdout)

# Client-facing presentations (bemutato.html / presentation.html) carry no company name and no
# internal-documentation link — the client sees the product, not the workshop (owner rule, 2026-09-20).
import re as _re2
for p in list(ROOT.rglob("bemutato.html")) + list(ROOT.rglob("presentation.html")):
    if "node_modules" in p.parts: continue
    t2 = p.read_text(encoding="utf-8")
    if "Calvus" in t2: failed.append(f"{p.relative_to(ROOT)}: company name in a client-facing document")
    for m in _re2.finditer(r'href="([^"]+)"', t2):
        h = m.group(1)
        if h.startswith(("http", "mailto:", "tel:", "#", "../")) or h.endswith((".css", ".pdf")): continue
        if p.parent.name != "docs" and h == "index.html": continue  # a flat project links its own prototype
        if _re2.search(r"(index|research|audit|decisions|design-system|layouts|gate|build-log|executive|business-logic|ssot|architecture|plan|sources|evidence|market|economics|responsible|first-customer|product-|documentation|brief|benchmarks|assets|sweep|token|client-asks|prerequisites)", h) and h.endswith(".html"):
            failed.append(f"{p.relative_to(ROOT)}: internal documentation link {h} in a client-facing document"); break

# Every project page (prototype and documentation): no studio name, and no tooling in the page
# chrome — a footer or eyebrow that says "Source: … rendered by build.py" is technical
# information the client has no use for (owner rule, 2026-09-20). Body text of the technical
# documents may name files; the footer and the eyebrow may not.
for p in ROOT.rglob("*.html"):
    if any(s in p.parts for s in (".git", ".claude", "node_modules")) or p.parent == ROOT: continue
    t2 = p.read_text(encoding="utf-8", errors="replace")
    if "Calvus" in t2: failed.append(f"{p.relative_to(ROOT)}: studio name on a project page")
    for tag, rx in (("footer", r'<footer[^>]*>(.*?)</footer>'), ("eyebrow", r'class="eyebrow"[^>]*>(.*?)</p>'), ("title", r'<title>(.*?)</title>'), ("nav brand", r'class="docnav-brand"[^>]*>(.*?)</')):
        for m in _re2.finditer(rx, t2, _re2.S):
            if _re2.search(r"rendered by|build\.py|build-docs\.py|Source: <code>|\bdocs\b", m.group(1)):
                failed.append(f"{p.relative_to(ROOT)}: tooling or jargon in the page {tag}"); break

# Every HTML file in the repo, outside .git and the worktrees, whether or not a project gate
# already read it: relative href/src must resolve. Cheap, and it catches a new folder nobody
# wired a gate for yet.
skip = (".git", ".claude", "node_modules")
files = [p for p in ROOT.rglob("*.html") if not any(s in p.parts for s in skip)]
broken, refs = [], 0
for f in files:
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'(?:href|src)="([^"#?]+)(?:[#?][^"]*)?"', t):
        h = m.group(1).strip()
        if not h or h.startswith(("http", "mailto:", "tel:", "data:", "javascript:")): continue
        refs += 1
        if not (f.parent / h).exists(): broken.append(f"{f.relative_to(ROOT)} → {h}")
print(f"{'repo-wide links':28s} {len(files)} files, {refs} references, {len(broken)} broken")
for b in broken: print("  broken link ", b)
for x in failed:
    if ": " in x: print("  failed      ", x)
if failed or broken:
    print(f"GATE: {len(failed)} gate(s) failed, {len(broken)} broken link(s)"); sys.exit(1)
print("GATE: CLEAN")
