#!/usr/bin/env python3
"""Render the DiscountDirect documents (markdown) to HTML in the prototype's own tokens.
Run: python3 discountdirect/build-docs.py  (needs the `markdown` package)."""
import re, pathlib, markdown
HERE = pathlib.Path(__file__).parent
PAGES = [
  ("README.md", "docs.html", "Overview"),
  ("EXECUTIVE.md", "executive.html", "Executive summary"), ("RESEARCH.md", "research.html", "Research"),
  ("AUDIT.md", "audit.html", "Audit"), ("SOURCES.md", "sources.html", "Sources"),
  ("BUSINESS-LOGIC.md", "business-logic.html", "Business logic"), ("DESIGN.md", "design.html", "Design"),
  ("BUILD-LOG.md", "build-log.html", "Build log"), ("GATE.md", "gate.html", "Gate"), ("CLIENT-ASKS.md", "client-asks.html", "Client asks"),
  ("SSOT.md", "ssot.html", "SSOT"), ("ARCHITECTURE.md", "architecture.html", "Architecture"),
  ("TECHNICAL-DESIGN.md", "technical-design.html", "Technical design"), ("IMPLEMENTATION-PLAN.md", "implementation-plan.html", "Implementation plan"),
  ("GDS-TOKEN-MAP.md", "token-map.html", "Token map"),
]
def render(src, out, label):
  md = (HERE / src).read_text(encoding="utf-8")
  title = re.match(r"#\s+(.+)", md).group(1)
  for s, o, _ in PAGES:  # links between the markdown files point at the rendered names
    md = md.replace(f"`{s}`", f"[`{s}`]({o})")
  body = markdown.markdown(md[md.index("\n"):], extensions=["tables", "fenced_code", "sane_lists"])
  body = body.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
  nav = "".join(f'<a href="{o}"{" class=on" if o == out else ""}>{l}</a>' for _, o, l in PAGES)
  nav = nav.replace('<a href="executive.html"', '<a href="bemutato.html">Bemutató</a><a href="executive.html"', 1)
  html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root{{--gds-bg-canvas:#f8fafc;--gds-bg-surface:#ffffff;--gds-bg-inverse:#111827;--gds-text-body:#111827;--gds-text-meta:#64748b;--gds-border-card:#e2e8f0;--gds-brand-accent:#3b5bdb;--gds-brand-accent-tint:#e7ecfb;--gds-radius-card:14px}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--gds-bg-canvas);color:var(--gds-text-body);font:15.5px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;padding-block:0 64px;padding-inline:clamp(16px,4vw,40px)}}
.wrap{{max-width:76ch;margin-inline:auto}}
.top{{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;padding:16px 0;border-bottom:1px solid var(--gds-border-card);font-size:13px;color:var(--gds-text-meta)}}
.top b{{color:var(--gds-text-body)}} .top a{{color:var(--gds-brand-accent);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}} .top a.on{{color:var(--gds-text-body);font-weight:600}}
h1{{font-size:clamp(26px,5vw,38px);line-height:1.15;margin:32px 0 10px;letter-spacing:-.01em}}
h2{{font-size:22px;margin:44px 0 10px;padding-top:18px;border-top:1px solid var(--gds-border-card)}}
h3{{font-size:17px;margin:26px 0 8px}}
p{{margin:0 0 12px}} li{{margin:4px 0}} strong{{font-weight:600}}
code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;background:var(--gds-brand-accent-tint);padding:1px 5px;border-radius:5px}}
pre{{background:var(--gds-bg-inverse);color:#f8fafc;padding:16px;border-radius:var(--gds-radius-card);overflow-x:auto;font-size:13px;line-height:1.5}} pre code{{background:none;color:inherit;padding:0;font-size:inherit}}
.tbl{{overflow-x:auto;margin:12px 0 20px;border:1px solid var(--gds-border-card);border-radius:var(--gds-radius-card);background:var(--gds-bg-surface)}}
table{{border-collapse:collapse;width:100%;font-size:13.5px;min-width:560px}}
th{{text-align:left;font-weight:600;background:var(--gds-bg-canvas);padding:10px 12px;border-bottom:1px solid var(--gds-border-card);font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--gds-text-meta)}}
td{{padding:10px 12px;border-top:1px solid var(--gds-border-card);vertical-align:top}}
a{{color:var(--gds-brand-accent)}}
footer{{margin-top:48px;padding-top:16px;border-top:1px solid var(--gds-border-card);font-size:12px;color:var(--gds-text-meta)}}
</style>
</head>
<body><div class="wrap">
<div class="top"><b>DiscountDirect</b>{nav}<a href="index.html">Open the prototype →</a><a href="../index.html">Calvus Hub</a></div>
<h1>{title}</h1>
{body}
<footer>Source: <code>discountdirect/{src}</code>, rendered by <code>build-docs.py</code>. Token names follow GDS 6.5.0 roles (<code>GDS-TOKEN-MAP.md</code>).</footer>
</div></body></html>
"""
  (HERE / out).write_text(html, encoding="utf-8")
  print(out, len(html), "bytes")
for src, out, label in PAGES: render(src, out, label)
