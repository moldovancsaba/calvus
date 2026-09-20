#!/usr/bin/env python3
"""Render the Holdvölgy docs (markdown) to styled HTML for GitHub Pages.

Run from anywhere:  python3 holdvolgy/docs/build.py
Needs the `markdown` package (pip install markdown). Output names deliberately
differ from the .md basenames so they never collide with the .html files GitHub
Pages' Jekyll pass generates from the same markdown (00-plan.md -> 00-plan.html).
"""
import re, pathlib, markdown

HERE = pathlib.Path(__file__).parent
PAGES = [  # (source, output, nav label)
    ("README.md", "index.html", "Overview"),
    ("00-brief.md", "brief.html", "Brief"),
    ("00-plan.md", "plan.html", "Plan"),
    ("01-research-benchmarks.md", "benchmarks.html", "Benchmarks"),
    ("02-brand-and-site-audit.md", "audit.html", "Brand & site audit"),
    ("03-asset-inventory.md", "assets.html", "Assets"),
    ("04-decisions.md", "decisions.html", "Decisions"),
    ("05-layout-specs.md", "layouts.html", "Layouts"),
    ("06-home-build.md", "home-build.html", "Home build"),
    ("07-birtok-build.md", "birtok-build.html", "Birtok build"),
    ("08-aszu-build.md", "aszu-build.html", "Aszú build"),
    ("09-latogatas-build.md", "latogatas-build.html", "Látogatás build"),
    ("10-shop-build.md", "shop-build.html", "Shop build"),
    ("11-gate-sweep.md", "gate-sweep.html", "Gate sweep"),
    ("09-business-logic.md", "business-logic.html", "Business logic"),
    ("10-ssot.md", "ssot.html", "SSOT"),
    ("11-architecture.md", "architecture.html", "Architecture"),
    ("12-technical-design.md", "technical-design.html", "Technical design"),
    ("13-implementation-plan.md", "implementation-plan.html", "Implementation plan"),
    ("14-token-map.md", "token-map.html", "Token map"),
]
CSS = (HERE / "docs.css").read_text(encoding="utf-8")

def render(src, out, label):
    md = (HERE / src).read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)", md); title = m.group(1).strip() if m else label
    md = md[m.end():] if m else md
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "fenced_code"])
    body = body.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    # links between the markdown files must point at the rendered names
    for s, o, _ in PAGES:
        body = body.replace(f"<code>{s}</code>", f'<a href="{o}"><code>{s}</code></a>')
    nav = nav_html(out)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Holdvölgy</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=Archivo:wdth,wght@112.5,400;112.5,500;112.5,600&display=swap">
<link rel="stylesheet" href="../assets/tokens.css">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<nav class="docnav" aria-label="Project documentation"><span class="docnav-brand">Holdvölgy · dokumentáció</span>{nav}</nav>
<header><p class="eyebrow">Holdvölgy · project documentation</p><h1>{title}</h1></header>
{body}
<script>(function(){{function f(){{document.querySelectorAll('.scale-d').forEach(function(e){{e.style.setProperty('--w',e.clientWidth)}});document.querySelectorAll('.scale-p').forEach(function(e){{e.style.setProperty('--pw',e.clientWidth)}})}}f();addEventListener('resize',f)}})();</script>
<footer>Holdvölgy · dokumentáció, 2026</footer>
</div>
</body>
</html>
"""
    (HERE / out).write_text(html, encoding="utf-8")
    return out, len(html)

def nav_html(current):
    nav = "".join(f'<a href="{o}"{" aria-current=page" if o == current else ""}>{l}</a>' for _, o, l in PAGES)
    nav = nav.replace('<a href="layouts.html"', f'<a href="design-system.html"{" aria-current=page" if current == "design-system.html" else ""}>Design system</a><a href="layouts.html"', 1)
    return nav.replace('<a href="plan.html"', '<a href="bemutato.html">Bemutató</a><a href="plan.html"', 1)

def sync_static_nav():
    """Hand-written doc pages (design-system.html) get the same navigation as the generated ones, on every build."""
    for name in ("design-system.html",):
        f = HERE / name; t = f.read_text(encoding="utf-8")
        new = f'<nav class="docnav" aria-label="Project documentation"><span class="docnav-brand">Holdvölgy · dokumentáció</span>{nav_html(name)}</nav>'
        t2 = re.sub(r'<nav class="docnav".*?</nav>', new, t, count=1, flags=re.S)
        assert t2 != t or nav_html(name) in t, name
        f.write_text(t2, encoding="utf-8"); print("%-16s nav synced" % name)

if __name__ == "__main__":
    for src, out, label in PAGES:
        print("%-16s %6d bytes" % render(src, out, label))
    sync_static_nav()
