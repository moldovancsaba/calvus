#!/usr/bin/env python3
"""Render the share images and icons:  python3 gameformative/tools/render_images.py
One 1200×630 PNG per article (assets/share/<slug>.png) and a default card (assets/share/default.png),
drawn from the site's own tokens and each article's cover graphic; and the icon set
(assets/icons/: favicon.svg, icon-32/192/512.png, apple-touch-icon.png).

Rendering uses the local Chrome in headless mode (cards) and ImageMagick (icons) — tools on the
workstation, not dependencies of the site. Run it when an article is added or its headline changes;
the gate checks every article has an image of the right size and weight (docs/15-discoverability.md)."""
import pathlib, subprocess, sys, tempfile, html as H
HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import build as B  # noqa: E402  (loads content, catalogue and stats; does not write pages)
import content as C  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SHARE, ICONS = HERE / "assets" / "share", HERE / "assets" / "icons"
BUDGET = 300_000  # bytes per share image (docs/15-discoverability.md §4)
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=block">'

MARK = ('<svg viewBox="0 0 32 32" width="{s}" height="{s}"><rect width="32" height="32" rx="{r}" fill="#1F47E0"/>'
        '<path d="M6 21.5 11.5 16l4.5 3.5L25.5 9" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="25.5" cy="9" r="3" fill="#FF8A3D"/></svg>')

CARD = """<!doctype html><html><head><meta charset="utf-8">{fonts}
<link rel="stylesheet" href="{css}"><style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#0C1222}}
.card{{box-sizing:border-box;width:1200px;height:630px;padding:56px 64px 48px;display:grid;grid-template-columns:1fr 400px;grid-template-rows:auto 1fr auto;gap:28px 48px;font-family:Archivo,Arial Narrow,sans-serif;color:#F3F5F9}}
.brand{{grid-column:1/-1;display:flex;align-items:center;gap:14px;font-size:34px;font-stretch:72%;font-weight:500;letter-spacing:-.01em}} .brand b{{font-weight:800}}
.text{{display:flex;flex-direction:column;justify-content:center;gap:18px;min-width:0}}
.kicker{{font-size:24px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#FF9E5E}}
h1{{margin:0;font-size:{hsize}px;line-height:1.02;font-stretch:72%;font-weight:800;letter-spacing:-.01em;color:#F3F5F9}}
.art{{align-self:center;border-radius:16px;overflow:hidden;border:1px solid #27314A}} .art .gf-cover{{aspect-ratio:16/9}}
.foot{{grid-column:1/-1;display:flex;justify-content:space-between;font-size:22px;color:#9AA3B6;border-top:1px solid #27314A;padding-top:18px}}
.desks{{display:grid;grid-template-columns:repeat(4,auto);gap:10px 26px;font-size:30px;font-weight:800;font-stretch:80%;color:#9DB0FF}}
</style></head><body><div class="card">
<div class="brand">{mark}<span>game<b>formative</b></span></div>
<div class="text">{kicker}<h1>{title}</h1>{extra}</div>
<div class="art">{art}</div>
<div class="foot"><span>{left}</span><span>{right}</span></div>
</div></body></html>"""


def shoot(html, out):
    with tempfile.TemporaryDirectory() as tmp:
        f = pathlib.Path(tmp) / "card.html"; f.write_text(html, encoding="utf-8")
        raw = pathlib.Path(tmp) / "raw.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1200,630", "--virtual-time-budget=8000", f"--screenshot={raw}", f.as_uri()],
                       check=True, capture_output=True)
        subprocess.run(["magick", str(raw), "-strip", "-colors", "256", "-define", "png:compression-level=9", str(out)], check=True)
    size = out.stat().st_size
    assert size <= BUDGET, f"{out.name}: {size:,} bytes over the {BUDGET:,}-byte budget"
    print(f"{out.relative_to(HERE)}  {size:,} bytes")


def cards():
    SHARE.mkdir(parents=True, exist_ok=True)
    css = (HERE / "assets" / "site.css").as_uri()
    for a in B.ARTICLES:
        n_used, n_inv = len(a["sources_used"]), len(a["sources_investigated"])
        size = 64 if len(a["title"]) <= 70 else 56 if len(a["title"]) <= 95 else 50
        html = CARD.format(fonts=FONTS, css=css, hsize=size, mark=MARK.format(s=48, r=8),
                           kicker=f'<div class="kicker">{H.escape(C.DESK[a["desk"]]["name"])} · {H.escape(a["kind"])}</div>',
                           title=H.escape(a["title"]), extra="", art=B.cover(a["cover"], a["title"]),
                           left=f"Sources listed: {n_used} used · {n_inv} investigated", right="gameformative.com")
        shoot(html, SHARE / f"{a['slug']}.png")
    desks = "".join(f"<span>{H.escape(n)}</span>" for _, n, _ in C.DESKS)
    html = CARD.format(fonts=FONTS, css=css, hsize=76, mark=MARK.format(s=48, r=8), kicker='<div class="kicker">Sport, explained</div>',
                       title="Every article with its sources on the table.", extra=f'<div class="desks">{desks}</div>',
                       art=B.cover(B.ARTICLES[0]["cover"], ""), left="Eight desks · sources used and investigated", right="gameformative.com")
    shoot(html.replace('grid-template-columns:1fr 400px', 'grid-template-columns:1fr 360px'), SHARE / "default.png")


def icons():
    ICONS.mkdir(parents=True, exist_ok=True)
    (ICONS / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" ' + MARK.format(s=32, r=8)[5:], encoding="utf-8")
    # apple-touch-icon: full-bleed square (iOS rounds the corners itself), no transparency
    full = '<svg xmlns="http://www.w3.org/2000/svg" ' + MARK.format(s=32, r=0)[5:]
    with tempfile.TemporaryDirectory() as tmp:
        fb = pathlib.Path(tmp) / "full.svg"; fb.write_text(full, encoding="utf-8")
        for name, px, src in (("icon-32.png", 32, ICONS / "favicon.svg"), ("icon-192.png", 192, ICONS / "favicon.svg"),
                              ("icon-512.png", 512, ICONS / "favicon.svg"), ("apple-touch-icon.png", 180, fb)):
            out = ICONS / name
            subprocess.run(["magick", "-background", "none" if name != "apple-touch-icon.png" else "#1F47E0", "-density", "1200", str(src),
                            "-resize", f"{px}x{px}", "-strip", str(out)], check=True)
            print(f"{out.relative_to(HERE)}  {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    icons(); cards()
