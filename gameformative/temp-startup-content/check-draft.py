#!/usr/bin/env python3
"""Check an article draft against the gameformative house rules:
    python3 gameformative/temp-startup-content/check-draft.py drafts/my-article.md [more.md …]

The rules are the site's own (content.py RULES, owner 2026-09-25): 800–3,200 characters of body text,
at least three headed segments, one of the eight desks, and both source lists — used, and
investigated but not used — each entry linked (https) with a publisher and a note.

"Body characters" = the standfirst and every paragraph, spaces included, markdown removed
(link text kept, link targets dropped). Not counted: the headline, segment headings, the meta block,
comments and the two source lists. This is the same count the site's build and gate apply."""
import re, sys, pathlib

MIN, MAX, SEGMENTS = 800, 3200, 3
DESKS = {"discover", "define", "design", "develop", "data", "drive", "defend", "deal"}
SUBJECTS = {"international-news", "sport-science", "tactics-technique", "sport-analytics", "data-intelligence",
            "sport-tech", "athlete-development", "fan-engagement", "sponsorship", "training-goods", "sport-goods"}
KINDS = {"Explainer", "Analysis", "News", "Opinion"}
SOURCE_HEADS = {"sources used": "used", "sources investigated but not used": "investigated"}


def plain(md):
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)            # images
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)         # links → their text
    md = re.sub(r"(\*\*|__|\*|_|`)", "", md)                 # emphasis, code
    return md.strip()


def check(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    problems = []
    meta = dict(re.findall(r"^\s*(\w+):\s*(.+?)\s*$", (re.search(r"<!--\s*meta(.*?)-->", text, re.S) or [None, ""])[1], re.M))
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    title = re.search(r"^# (.+)$", text, re.M)
    if not title: problems.append("no headline (a '# ' line)")
    for k, allowed in (("desk", DESKS), ("subject", SUBJECTS), ("kind", KINDS)):
        if meta.get(k) not in allowed: problems.append(f"meta {k}: {meta.get(k)!r} is not one of {sorted(allowed)}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", meta.get("slug", "")): problems.append(f"meta slug: {meta.get('slug')!r} — lowercase words joined by hyphens")

    # split into blocks: the part before the first "## " is the standfirst; then one block per heading
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    head, rest = parts[0], parts[1:]
    standfirst = [plain(p.replace("\n", " ")) for p in re.split(r"\n\s*\n", head.split("\n", 1)[1] if title else head) if p.strip()]
    segments, sources = [], {"used": [], "investigated": []}
    for heading, body in zip(rest[0::2], rest[1::2]):
        kind = SOURCE_HEADS.get(heading.strip().lower())
        if kind:
            sources[kind] += [l.strip()[2:] for l in body.splitlines() if l.strip().startswith(("- ", "* "))]
        else:
            paras = [plain(p.replace("\n", " ")) for p in re.split(r"\n\s*\n", body) if p.strip()]
            segments.append((heading.strip(), paras))
    chars = sum(len(p) for p in standfirst) + sum(len(p) for _, ps in segments for p in ps)
    if not MIN <= chars <= MAX: problems.append(f"{chars:,} body characters — must be {MIN:,}–{MAX:,}")
    if len(segments) < SEGMENTS: problems.append(f"{len(segments)} headed segments — at least {SEGMENTS}")
    for h, ps in segments:
        if not ps: problems.append(f"segment '{h}' has no text")
    for kind, label in (("used", "Sources used"), ("investigated", "Sources investigated but not used")):
        if not sources[kind]: problems.append(f"'## {label}' is missing or empty")
        for s in sources[kind]:
            if not re.match(r"\[[^\]]+\]\(https://[^)]+\)\s+—\s+.+?\s+—\s+.+", s):
                problems.append(f"{label}: '{s[:70]}…' — use: [Title](https://…) — Publisher, date — note")
    status = "OK" if not problems else "NOT READY"
    print(f"{status:9s} {path}: {chars:,} characters, {len(segments)} segments, {len(sources['used'])} used, "
          f"{len(sources['investigated'])} investigated, desk {meta.get('desk')}, status {meta.get('status')}")
    for p in problems: print("          -", p)
    return not problems


if __name__ == "__main__":
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    ok = all([check(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
