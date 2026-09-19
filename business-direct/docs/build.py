#!/usr/bin/env python3
"""Render the business.direct docs (markdown) to styled HTML for GitHub Pages.

Run from anywhere:  python3 business-direct/docs/build.py
Needs the `markdown` package. Output names differ from the .md basenames so they never
collide with the .html files GitHub Pages' Jekyll pass generates from the same markdown.
"""
import re, pathlib, markdown

HERE = pathlib.Path(__file__).parent
PAGES = [  # (source, output, nav label)
    ("README.md", "index.html", "Overview"),
    ("00-brief.md", "brief.html", "Brief"),
    ("01-research.md", "research.html", "Research"),
    ("01b-research-acquisition-content-sales.md", "research-2.html", "Research II"),
    ("01c-research-data-driven-marketing.md", "research-3.html", "Research III"),
    ("02-audit.md", "audit.html", "Audit"),
    ("03-sources.md", "sources.html", "Sources"),
    ("05-layout-specs.md", "05-layout-specs.html", "Layout specs"),
    ("04-decisions.md", "decisions.html", "Decisions"),
    ("06-build-log.md", "build-log.html", "Build log"),
    ("07-gate.md", "gate.html", "Gate"),
    ("08-client-asks.md", "client-asks.html", "Owner asks"),
    ("09-business-logic.md", "business-logic.html", "Business logic"),
    ("10-ssot.md", "ssot.html", "SSOT"),
    ("11-architecture.md", "architecture.html", "Architecture"),
    ("12-technical-design.md", "technical-design.html", "Technical design"),
    ("13-implementation-plan.md", "implementation-plan.html", "Plan"),
    ("14-token-map.md", "token-map.html", "Token map"),
    ("16-analytics-and-unit-economics.md", "analytics.html", "Analytics"),
    ("17-business-logic-audit-and-swot.md", "audit-swot.html", "Audit · SWOT"),
]
CSS = (HERE / "docs.css").read_text(encoding="utf-8")

def render(src, out, label):
    md = (HERE / src).read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)", md); title = m.group(1).strip() if m else label
    md = md[m.end():] if m else md
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "fenced_code"])
    body = body.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    for s, o, _ in PAGES:  # links between the markdown files point at the rendered names
        base = s.split("/")[-1]
        body = body.replace(f"<code>{base}</code>", f'<a href="{o}"><code>{base}</code></a>')
    nav = "".join(f'<a href="{o}"{" aria-current=page" if o == out else ""}>{l}</a>' for _, o, l in PAGES)
    nav = nav.replace('<a href="05-layout-specs.html"', '<a href="design-system.html">Design system</a><a href="layouts.html">Layouts</a><a href="05-layout-specs.html"', 1)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — business.direct docs</title>
<link rel="stylesheet" href="../assets/tokens.css">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<nav class="docnav" aria-label="Project documentation"><span class="docnav-brand">business.direct · docs</span>{nav}</nav>
<header><p class="eyebrow">Calvus · business.direct · project documentation</p><h1>{title}</h1></header>
{body}
<footer>Source: <code>business-direct/docs/{src}</code> · rendered by <code>docs/build.py</code>.</footer>
</div>
</body>
</html>
"""
    (HERE / out).write_text(html, encoding="utf-8")
    return out, len(html)

if __name__ == "__main__":
    for src, out, label in PAGES:
        print("%-24s %6d bytes" % render(src, out, label))
