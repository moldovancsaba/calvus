#!/usr/bin/env python3
"""Render the Népszabadság docs (markdown) to HTML for GitHub Pages.
Run from anywhere:  python3 nepszabadsag/docs/build.py   (needs the `markdown` package)."""
import re, pathlib, markdown
HERE = pathlib.Path(__file__).parent
PAGES = [("README.md", "index.html", "Overview"), ("handover.md", "handover.html", "Handover")]
CSS = (HERE / "docs.css").read_text(encoding="utf-8")
for src, out, label in PAGES:
    md = (HERE / src).read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)", md); title = m.group(1).strip() if m else label; md = md[m.end():] if m else md
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "fenced_code"]).replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    for s, o, _ in PAGES: body = body.replace(f"<code>{s}</code>", f'<a href="{o}"><code>{s}</code></a>')
    nav = "".join(f'<a href="{o}"{" aria-current=page" if o == out else ""}>{l}</a>' for _, o, l in PAGES)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} · Népszabadság</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;600;700;800&display=swap"><link rel="stylesheet" href="../assets/tokens.css"><style>{CSS}</style></head>
<body><div class="wrap"><nav class="docnav" aria-label="Project documentation"><span class="docnav-brand">Népszabadság · dokumentáció</span>{nav}</nav>
<header><p class="eyebrow">Népszabadság · project documentation</p><h1>{title}</h1></header>
{body}
<footer>Népszabadság · dokumentáció, 2026</footer></div></body></html>
"""
    (HERE / out).write_text(html, encoding="utf-8"); print(f"{out:16s} {len(html):6d} bytes")
