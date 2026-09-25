#!/usr/bin/env python3
"""Render every project's documentation:  python3 build-docs.py
Runs the four per-project renderers in place (each keeps its own page list, tokens and
template — projects do not share a look on purpose). Needs the `markdown` package.
Follow with `python3 check.py`.
"""
import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
for r in ["holdvolgy/docs/build.py", "idbc-salary-guide/docs/build.py", "discountdirect/build-docs.py", "lexodont.hu/docs/build.py", "business-direct/docs/build.py", "bizdrankazoldet/docs/build.py", "nepszabadsag/docs/build.py", "gameformative/docs/build.py"]:
    print(f"== {r}")
    subprocess.run([sys.executable, str(ROOT / r)], check=True)

# The repo-level documents (the method and the hub audit), rendered in the hub's own look.
import re, markdown
CSS = """:root{--bg:#f7f7f7;--surface:#fff;--text:#1e1e1e;--muted:#626262;--line:#e5e5e5;--accent:#111}
*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);font-size:15.5px;line-height:1.6;padding:0 clamp(16px,4vw,40px) 64px}
.wrap{max-width:76ch;margin:0 auto}.top{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;padding:16px 0;border-bottom:1px solid var(--line);font-size:13px;color:var(--muted)}
.top a{color:var(--accent);text-decoration:none;min-height:44px;display:inline-flex;align-items:center;font-weight:600}
h1{font-size:clamp(28px,5vw,40px);line-height:1.1;margin:32px 0 10px;letter-spacing:-.01em}h2{font-size:22px;margin:44px 0 10px;padding-top:18px;border-top:1px solid var(--line)}h3{font-size:17px;margin:26px 0 8px}
p{margin:0 0 12px}li{margin:4px 0}strong{font-weight:700}em{color:var(--muted)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;background:#ececec;padding:1px 5px;border-radius:5px;overflow-wrap:anywhere}
.tbl{overflow-x:auto;margin:12px 0 20px;border:1px solid var(--line);border-radius:12px;background:var(--surface)}table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:560px}
th{text-align:left;font-weight:700;background:var(--bg);padding:10px 12px;border-bottom:1px solid var(--line);font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}td{padding:10px 12px;border-top:1px solid var(--line);vertical-align:top}
footer{margin-top:48px;padding-top:16px;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}"""
for src, out in (("PROTOTYPING.md", "prototyping.html"), ("HUB-AUDIT.md", "hub-audit.html"), ("PRODUCT.md", "product.html")):
    md = (ROOT / src).read_text(encoding="utf-8")
    title = re.match(r"#\s+(.+)", md).group(1)
    body = markdown.markdown(md[md.index("\n"):], extensions=["tables", "sane_lists", "fenced_code"])
    body = body.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body><div class="wrap">
<div class="top"><b>Calvus</b><a href="index.html">Project Hub</a><a href="prototyping.html">How we prototype</a><a href="hub-audit.html">Hub audit</a><a href="holdvolgy/docs/index.html">Holdvölgy docs</a><a href="discountdirect/docs.html">DiscountDirect docs</a><a href="idbc-salary-guide/docs/index.html">IDBC docs</a><a href="lexodont.hu/docs/index.html">Lexodont docs</a><a href="business-direct/docs/index.html">business.direct docs</a></div>
<h1>{title}</h1>
{body}
<footer>Source: <code>{src}</code>, rendered by <code>build-docs.py</code>.</footer>
</div></body></html>
"""
    (ROOT / out).write_text(html, encoding="utf-8")
    print("==", out, len(html), "bytes")
