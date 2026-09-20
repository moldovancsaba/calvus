#!/usr/bin/env python3
"""Render the Bízd ránk a zöldet docs (markdown) to HTML for GitHub Pages.
Run from anywhere:  python3 bizdrankazoldet/docs/build.py   (needs the `markdown` package)."""
import re, pathlib, markdown
HERE = pathlib.Path(__file__).parent
PAGES = [("README.md", "index.html", "Overview"), ("00-brief.md", "brief.html", "Brief"), ("01-research.md", "research.html", "Research"), ("02-audit.md", "audit.html", "Audit"), ("03-sources.md", "sources.html", "Sources")]
CSS = (HERE / "docs.css").read_text(encoding="utf-8")
for src, out, label in PAGES:
    md = (HERE / src).read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)", md); title = m.group(1).strip() if m else label; md = md[m.end():] if m else md
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "fenced_code"]).replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    for s, o, _ in PAGES: body = body.replace(f"<code>{s}</code>", f'<a href="{o}"><code>{s}</code></a>')
    nav = "".join(f'<a href="{o}"{" aria-current=page" if o == out else ""}>{l}</a>' for _, o, l in PAGES)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} — Bízd ránk a zöldet docs</title><style>{CSS}</style></head>
<body><div class="wrap"><nav class="docnav" aria-label="Project documentation"><span class="docnav-brand">Bízd ránk a zöldet · docs</span>{nav}</nav>
<header><p class="eyebrow">Calvus · Bízd ránk a zöldet · project documentation</p><h1>{title}</h1></header>
{body}
<footer>Source: <code>bizdrankazoldet/docs/{src}</code> · rendered by <code>docs/build.py</code>.</footer></div></body></html>
"""
    (HERE / out).write_text(html, encoding="utf-8"); print(f"{out:16s} {len(html):6d} bytes")
