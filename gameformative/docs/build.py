#!/usr/bin/env python3
"""Render the gameformative project documentation (markdown → HTML) and the presentation.
Run from anywhere:  python3 gameformative/docs/build.py   (needs the `markdown` package).
The presentation (presentation.html) is rendered here too, from presentation-source.md's copy and the
figures in ../data/stats.json — its numbers are never typed by hand."""
import re, json, pathlib, markdown
HERE = pathlib.Path(__file__).parent
PAGES = [
    ("README.md", "index.html", "Overview"), ("00-brief.md", "brief.html", "Brief"),
    ("01-research.md", "research.html", "Research"), ("01a-source-register.md", "source-register.html", "Sources researched"),
    ("01b-evidence.md", "evidence.html", "Evidence"), ("02-audit.md", "audit.html", "Audit"),
    ("03-sources.md", "inputs.html", "Inputs and gaps"), ("04-decisions.md", "decisions.html", "Decisions"),
    ("05-design.md", "design.html", "Design"), ("06-build-log.md", "build-log.html", "Build log"),
    ("07-gate.md", "gate.html", "Gate"), ("08-client-asks.md", "asks.html", "Asks"),
    ("10-ssot.md", "ssot.html", "SSOT"), ("11-architecture.md", "architecture.html", "Architecture"),
    ("12-technical-design.md", "technical-design.html", "Technical design"), ("13-implementation-plan.md", "plan.html", "Plan"),
    ("14-token-map.md", "token-map.html", "Token map"), ("16-source-catalogue.md", "source-catalogue.html", "Source catalogue"),
    ("18-responsible-data.md", "responsible-data.html", "Responsible data"), ("20-system-blueprint.md", "system-blueprint.html", "System blueprint"),
]
CSS = (HERE / "docs.css").read_text(encoding="utf-8")
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap">'
for src, out, label in PAGES:
    md = (HERE / src).read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)", md); title = m.group(1).strip() if m else label; md = md[m.end():] if m else md
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "fenced_code", "toc"]).replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    for s, o, _ in PAGES: body = body.replace(f"<code>{s}</code>", f'<a href="{o}"><code>{s}</code></a>')
    nav = "".join(f'<a href="{o}"{" aria-current=page" if o == out else ""}>{l}</a>' for _, o, l in PAGES) + '<a href="presentation.html">Presentation</a><a href="../index.html">Prototype</a>'
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} · gameformative</title>{FONTS}<link rel="stylesheet" href="../assets/tokens.css"><style>{CSS}</style></head>
<body><div class="wrap"><nav class="docnav" aria-label="Project documentation"><span class="docnav-brand">game<b>formative</b></span>{nav}</nav>
<header><p class="eyebrow">gameformative · project documentation</p><h1>{title}</h1></header>
{body}
<footer>gameformative.com · project documentation, 2026</footer></div></body></html>
"""
    (HERE / out).write_text(html, encoding="utf-8"); print(f"{out:24s} {len(html):7,d} bytes")

# ------------------------------------------------------------------ the presentation
S = json.loads((HERE.parent / "data" / "stats.json").read_text(encoding="utf-8"))
L = {l["id"]: l for l in S["leagues"]}
vals = dict(
    data_to=__import__("datetime").date.fromisoformat(S["data_to"]).strftime("%-d %B %Y"), leagues=len(S["leagues"]),
    league_matches=sum(l["played"] for l in S["leagues"]), league_goals=sum(l["agg"]["goals"] for l in S["leagues"]),
    wc_matches=S["wc2026"]["matches"], wc_goals=S["wc2026"]["goals"], pl_matches=len(S["pl2526"]["table"]) * (len(S["pl2526"]["table"]) - 1),
    pl_goals=S["pl2526"]["goals"], inputs=len(S["inputs"]),
)
import sys; sys.path.insert(0, str(HERE.parent)); import content as C
_arts = C.articles(S)
vals.update(desks=len(C.DESKS), desks_used=len({a["desk"] for a in _arts}), desk_rows="\n".join(f"| **{n}** | {d} |" for _, n, d in C.DESKS))
vals.update(topics=len(C.TOPICS), articles=len(_arts), min_chars=f"{C.RULES['min_chars']:,}", max_chars=f"{C.RULES['max_chars']:,}")
site = [p for p in HERE.parent.rglob("*.html") if "docs" not in p.relative_to(HERE.parent).parts and "analysis" not in p.relative_to(HERE.parent).parts]
sizes = [p.stat().st_size for p in site]
vals.update(page_kb_min=round(min(sizes) / 1000), page_kb_max=round(max(sizes) / 1000),
            js_kb=round((HERE.parent / "assets" / "site.js").stat().st_size / 1000))
src = (HERE / "presentation-source.md").read_text(encoding="utf-8")
for k, v in vals.items(): src = src.replace("{{" + k + "}}", f"{v:,}" if isinstance(v, int) else str(v))
assert "{{" not in src, "presentation-source.md has a placeholder with no value"
m = re.match(r"#\s+(.+)", src); title = m.group(1).strip(); src = src[m.end():]
body = markdown.markdown(src, extensions=["tables", "sane_lists", "attr_list"]).replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
PCSS = CSS + """
.deck section{min-height:60vh;padding:28px 0;border-top:3px solid var(--gf-ink)}
.lead-p{font-size:20px;color:var(--gf-ink)}
.cta{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;border-radius:999px;background:var(--gf-blue);color:var(--gf-on-blue);font-weight:800;text-decoration:none;margin:6px 10px 6px 0}
.hero{background:var(--gf-band);color:var(--gf-on-band);border-radius:12px;padding:28px 22px;margin:22px 0}
.hero h1{color:var(--gf-on-band)}.hero p{color:var(--gf-band-muted)}
"""
html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>gameformative.com — presentation</title>{FONTS}<link rel="stylesheet" href="../assets/tokens.css"><style>{PCSS}</style></head>
<body><div class="wrap">
<div class="hero"><p style="font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#FF9E5E;margin:0 0 8px">gameformative.com · 2026</p><h1>{title}</h1><p>A football data and analysis site, built on the numbers — the prototype, the research behind it, and the one decision it asks for.</p><a class="cta" href="../index.html">Open the prototype</a></div>
<div class="deck">{body}</div>
<footer>gameformative.com, 2026</footer></div></body></html>
"""
(HERE / "presentation.html").write_text(html, encoding="utf-8"); print(f"{'presentation.html':24s} {len(html):7,d} bytes")
