#!/usr/bin/env python3
"""The repo gate, in one command:  python3 check.py
Runs every project's own gate and a repo-wide link audit over every HTML file that no
project gate covers (the hub, `public/`-free). Exit 1 if any of them finds something.

  holdvolgy/check.py          Holdvölgy site + docs, DiscountDirect pages, the hub: links, anchors,
                              docs cross-links, stale-phrase scan, prototype banner
  idbc-salary-guide/check.py  links, anchors, docs cross-links, one chart-asset version, inert controls
  lexodont.hu/check.py        both fidelities + docs: links, anchors, docs cross-links, parity
"""
import re, subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
GATES = ["holdvolgy/check.py", "idbc-salary-guide/check.py", "lexodont.hu/check.py"]
failed = []
for g in GATES:
    r = subprocess.run([sys.executable, str(ROOT / g)], capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
    print(f"{g:28s} {last}")
    if r.returncode != 0:
        failed.append(g); print(r.stdout)

# Every HTML file in the repo, outside .git and the worktrees, whether or not a project gate
# already read it: relative href/src must resolve. Cheap, and it catches a new folder nobody
# wired a gate for yet.
skip = (".git", ".claude")
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
if failed or broken:
    print(f"GATE: {len(failed)} gate(s) failed, {len(broken)} broken link(s)"); sys.exit(1)
print("GATE: CLEAN")
