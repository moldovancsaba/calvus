#!/usr/bin/env python3
"""Generate the gameformative prototype:  python3 gameformative/build.py   (--check: compare only)
Reads content.py (copy) and data/stats.json (every figure, computed by data/convert.py) and writes
every page. No dependencies. --check regenerates in memory and fails if a committed page differs, so
a hand edit to a generated page cannot survive the gate."""
import json, pathlib, sys, html as H
from urllib.parse import quote
import content as C
import catalogue as K

HERE = pathlib.Path(__file__).parent
S = json.loads((HERE / "data" / "stats.json").read_text(encoding="utf-8"))
V = "20"  # asset version — bump when tokens.css, site.css or site.js change
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap">'
SITE_URL = C.SITE["url"]
LEAGUES = S["leagues"]
LG = {l["id"]: l for l in LEAGUES}
ARTICLES = C.articles(S)
DATA_TO = C.nice_date(S["data_to"])
OUT = {}


def esc(s):
    return H.escape(str(s), quote=True)


def up(depth):
    return "../" * depth


# ------------------------------------------------------------------ icons (inline, decorative)
def icon(name):
    paths = {
        "home": '<path d="M3 11.5 12 4l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
        "scores": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M12 4v16"/>',
        "stats": '<path d="M5 20V11M12 20V5M19 20v-7"/>',
        "analysis": '<path d="M6 3h9l4 4v14H6z"/><path d="M9 12h7M9 16h7M9 8h4"/>',
        "more": '<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>',
        "theme": '<circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 0 0 16z" fill="currentColor"/>',
        "search": '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
        "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths[name]}</svg>'


MARK = ('<svg class="gf-brand-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect width="32" height="32" rx="8" fill="#1F47E0"/>'
        '<path d="M6 21.5 11.5 16l4.5 3.5L25.5 9" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="25.5" cy="9" r="3" fill="#FF8A3D"/></svg>')


def brand(depth):
    return f'<a class="gf-brand" href="{up(depth)}index.html" aria-label="gameformative home">{MARK}<span class="gf-brand-word">game<b>formative</b></span></a>'


# ------------------------------------------------------------------ chrome
def banner():
    return ('<div class="proto-banner"><strong>Prototype — gameformative.com, 2026.</strong> The launch is articles only. '
            'The lead article is the editorial desk’s draft; the data articles are sample copy whose every figure comes from openfootball’s public-domain results '
            f'(to {DATA_TO}). Search, sign-in and the newsletter are shown but not built.</div>')


def header(current, depth):
    items = "".join(f'<li><a href="{up(depth)}{href}"' + (' aria-current="page"' if label == current else "") + f'>{esc(label)}</a></li>' for label, href, _ in C.NAV)
    return f"""<a class="gf-skip" href="#main">Skip to content</a>
<header class="gf-header"><div class="gf-wrap gf-header-row">
  {brand(depth)}
  <nav class="gf-nav" aria-label="Main"><ul>{items}</ul></nav>
  <div class="gf-tools">
    <button class="gf-icon-btn" type="button" aria-disabled="true" title="Search is not built in the prototype" aria-label="Search (not built in the prototype)">{icon("search")}</button>
    <button class="gf-icon-btn" type="button" data-theme-toggle aria-pressed="false" aria-label="Switch theme">{icon("theme")}</button>
    <a class="gf-btn gf-btn--quiet gf-signin is-unavailable" href="#" aria-disabled="true" title="Accounts are not built in the prototype" onclick="return false">Sign in</a>
  </div>
</div></header>"""


def deskbar(depth, current_desk=None):
    """The eight desks, always visible under the header — scrolls sideways on phones (visible navigation, S7)."""
    items = "".join(f'<li><a href="{up(depth)}desks/{s}.html"' + (' aria-current="page"' if s == current_desk else "") + f'>{esc(n)}</a></li>' for s, n, _ in C.DESKS)
    return f'<nav class="gf-topicbar" aria-label="Desks"><div class="gf-wrap"><ul tabindex="0" aria-label="Desks, scroll sideways">{items}</ul></div></nav>'


def tabbar(current, depth):
    ic = {"Home": "home", "Latest": "analysis", "Desks": "scores", "Sources": "analysis", "How we work": "stats"}
    items = []
    for label, href, short in C.NAV:
        if label not in C.TABBAR: continue
        items.append(f'<li><a href="{up(depth)}{href}"' + (' aria-current="page"' if label == current else "") + f'>{icon(ic[label])}<span>{esc(short)}</span></a></li>')
    items.append(f'<li><button type="button" data-sheet-open aria-expanded="false" aria-controls="gf-more">{icon("more")}<span>More</span></button></li>')
    return f'<nav class="gf-tabbar" aria-label="Sections"><ul>{"".join(items)}</ul></nav>'


def sheet(depth):
    links = "".join(f'<li><a href="{up(depth)}{href}">{esc(label)}</a></li>' for label, href, _ in C.NAV)
    desks = "".join(f'<li><a href="{up(depth)}desks/{s}.html">{esc(n)}</a></li>' for s, n, _ in C.DESKS)
    return f"""<div class="gf-sheet" id="gf-more" hidden role="dialog" aria-modal="true" aria-labelledby="gf-more-h"><div class="gf-sheet-panel">
  <div class="gf-sheet-head"><h2 id="gf-more-h">More</h2><button class="gf-icon-btn" type="button" data-sheet-close aria-label="Close">{icon("close")}</button></div>
  <ul>{links}</ul>
  <h2 class="gf-kicker" style="margin-top:18px">Desks</h2>
  <ul>{desks}</ul>
  <ul><li><a href="{up(depth)}topics/index.html">All subjects</a></li></ul>
  <h2 class="gf-kicker" style="margin-top:18px">A later phase</h2>
  <ul><li><a href="{up(depth)}stats/index.html">Data pages (preview)</a></li></ul>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px">
    <button class="gf-btn gf-btn--quiet" type="button" data-theme-toggle aria-pressed="false">{icon("theme")} Theme</button>
    <a class="gf-btn gf-btn--quiet is-unavailable" href="#" aria-disabled="true" title="Accounts are not built in the prototype" onclick="return false">Sign in</a>
  </div>
</div></div>"""


def footer(depth):
    u = up(depth)
    sec = "".join(f'<li><a href="{u}{href}">{esc(label)}</a></li>' for label, href, _ in C.NAV[1:])
    tp = "".join(f'<li><a href="{u}desks/{s}.html">{esc(n)}</a></li>' for s, n, _ in C.DESKS) + f'<li><a href="{u}topics/index.html">All subjects</a></li>'
    std = f'<li><a href="{u}sources/index.html">Source catalogue</a></li>' + "".join(f'<li><a href="{u}how-we-count/index.html#{a}">{t}</a></li>' for a, t in (("desks", "The eight desks"), ("rules", "Article rules"), ("sources", "How we source"), ("corrections", "Corrections"), ("automation", "Automation and AI"), ("labels", "Labels we use")))
    return f"""<footer class="gf-footer"><div class="gf-wrap">
  <div class="gf-footer-grid">
    <div class="about">{brand(depth)}<p style="margin-top:8px">{esc(C.SITE["tagline"])} Every article lists the sources we used and the sources we investigated but did not use.</p></div>
    <div><h2>Sections</h2><ul>{sec}</ul><h2 style="margin-top:16px">A later phase</h2><ul><li><a href="{u}stats/index.html">Data pages (preview)</a></li></ul></div>
    <div class="topics"><h2>Desks</h2><ul>{tp}</ul></div>
    <div><h2>Standards</h2><ul>{std}</ul></div>
  </div>
  <div class="gf-footer-bottom"><span>© 2026 gameformative.com</span><span>Articles checked against their sources</span></div>
</div></footer>"""


def abs_url(path):
    return SITE_URL + (path[:-10] if path.endswith("index.html") else path)


def social(path, title, desc, depth, og):
    """Canonical, robots, Open Graph and X-card tags (docs/15-discoverability.md §2–§4)."""
    og = og or {}
    img = og.get("image", "assets/share/default.png")
    alt = og.get("image_alt", "gameformative — sport, explained. Eight desks: Discover, Define, Design, Develop, Data, Drive, Defend, Deal.")
    kind = og.get("type", "website")
    tags = [f'<link rel="canonical" href="{esc(abs_url(path))}">',
            # the prototype stays out of search indexes so it never competes with gameformative.com (D33)
            '<meta name="robots" content="noindex, follow, max-image-preview:large">',
            f'<meta property="og:site_name" content="gameformative"><meta property="og:locale" content="en_GB">',
            f'<meta property="og:type" content="{kind}"><meta property="og:title" content="{esc(og.get("title", title))}">',
            f'<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(abs_url(path))}">',
            f'<meta property="og:image" content="{esc(SITE_URL + img)}"><meta property="og:image:type" content="image/png">',
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{esc(alt)}">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{esc(og.get("title", title))}"><meta name="twitter:description" content="{esc(desc)}">',
            f'<meta name="twitter:image" content="{esc(SITE_URL + img)}"><meta name="twitter:image:alt" content="{esc(alt)}">']
    if kind == "article":
        tags.append(f'<meta property="article:published_time" content="{og["published"]}"><meta property="article:section" content="{esc(og["section"])}"><meta property="article:tag" content="{esc(og["tag"])}">')
    u = up(depth)
    tags.append(f'<link rel="icon" href="{u}assets/icons/favicon.svg" type="image/svg+xml"><link rel="icon" href="{u}assets/icons/icon-32.png" sizes="32x32" type="image/png">'
                f'<link rel="apple-touch-icon" href="{u}assets/icons/apple-touch-icon.png"><link rel="manifest" href="{u}manifest.webmanifest">'
                f'<link rel="alternate" type="application/rss+xml" title="gameformative — latest articles" href="{u}feed.xml">')
    return "\n".join(tags)


def page(path, title, desc, current, body, depth, jsonld=None, desk=None, later=False, extra_head="", og=None):
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld if isinstance(jsonld, list) else [jsonld] if jsonld else []))
    notice = (f'<div class="gf-later"><div class="gf-wrap"><p><b>A later phase.</b> gameformative launches with articles only; these data pages preview what comes after. '
              f'<a href="{up(depth)}index.html">Back to the articles</a></p></div></div>') if later else ""
    html_out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{social(path, title, desc, depth, og)}
<meta name="theme-color" content="#F7F6F2" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0B0F1A" media="(prefers-color-scheme: dark)">
<script>try{{var t=localStorage.getItem("gf-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
{extra_head}{FONTS}
<link rel="stylesheet" href="{up(depth)}assets/tokens.css?v={V}">
<link rel="stylesheet" href="{up(depth)}assets/site.css?v={V}">
{ld}
</head>
<body>
{banner()}
{header(current, depth)}
{deskbar(depth, desk)}
{notice}
<main id="main" class="gf-main"><div class="gf-wrap">
{body}
</div></main>
{footer(depth)}
{tabbar(current, depth)}
{sheet(depth)}
<script src="{up(depth)}assets/site.js?v={V}" defer></script>
</body>
</html>
"""
    OUT[path] = html_out


# ------------------------------------------------------------------ components
def form(chips):
    return '<span class="gf-form" aria-label="Form, oldest first: ' + esc(", ".join({"W": "won", "D": "drew", "L": "lost"}[f["r"]] + f" {f['score']} {'v' if f['ha'] == 'H' else 'at'} {f['opp']}" for f in chips)) + '">' + "".join(
        f'<span class="{f["r"].lower()}" title="{"Won" if f["r"] == "W" else "Drew" if f["r"] == "D" else "Lost"} {f["score"]} {"v" if f["ha"] == "H" else "at"} {f["opp"]}, {C.short_date(f["date"])}">{f["r"]}</span>' for f in chips) + "</span>"


def team_cell(r):
    return f'<th scope="row" class="team" data-v="{esc(r["name"])}"><span class="name">{esc(r["name"])}</span><span class="code">{esc(r["code"])}</span></th>'


XS = {"w", "d", "l", "gf", "ga", "ppg", "form"}  # columns a phone hides until "All columns" is pressed


def sort_th(label, key, title, cls=""):
    cls = (cls + " gf-xs").strip() if key in XS else cls
    return f'<th scope="col" data-key="{key}" class="{cls}" title="{esc(title)}"><button class="gf-sort" type="button">{label}</button></th>'


def league_table(l, view="all", zones=True, tid=""):
    t = l["table"]
    n = len(t)
    if view == "all":
        head = ("<tr>" + '<th scope="col" class="pos">#</th>' + '<th scope="col" class="team l">Team</th>'
                + sort_th("P", "p", "Played") + sort_th("W", "w", "Won") + sort_th("D", "d", "Drawn") + sort_th("L", "l", "Lost")
                + sort_th("GF", "gf", "Goals for") + sort_th("GA", "ga", "Goals against") + sort_th("GD", "gd", "Goal difference")
                + sort_th("Pts", "pts", "Points") + sort_th("PPG", "ppg", "Points per game") + '<th scope="col" class="l gf-xs">Form</th></tr>')
        rows = []
        for r in t:
            z = " is-zone-top" if zones and r["pos"] <= 4 else " is-zone-bottom" if zones and r["pos"] > n - 3 else ""
            rows.append(f'<tr class="{z.strip()}"><td class="pos" data-v="{r["pos"]}">{r["pos"]}</td>{team_cell(r)}'
                        + "".join(f'<td{" class=gf-xs" if k in XS else ""} data-v="{r[k]}">{r[k]}</td>' for k in ("p", "w", "d", "l", "gf", "ga"))
                        + f'<td data-v="{r["gd"]}">{r["gd"]:+d}</td>'.replace("+0", "0")
                        + f'<td class="pts" data-v="{r["pts"]}">{r["pts"]}</td><td class="gf-xs" data-v="{r["ppg"]}">{r["ppg"]:.2f}</td>'
                        + f'<td class="l gf-xs" data-v="{"".join(f["r"] for f in r["form"])}">{form(r["form"])}</td></tr>')
    else:
        sub = sorted(t, key=lambda r: (-r[view]["pts"], -(r[view]["gf"] - r[view]["ga"]), -r[view]["gf"], r["name"]))
        head = ("<tr>" + '<th scope="col" class="pos">#</th>' + '<th scope="col" class="team l">Team</th>'
                + sort_th("P", "p", "Played") + sort_th("W", "w", "Won") + sort_th("D", "d", "Drawn") + sort_th("L", "l", "Lost")
                + sort_th("GF", "gf", "Goals for") + sort_th("GA", "ga", "Goals against") + sort_th("Pts", "pts", "Points") + "</tr>")
        rows = []
        for i, r in enumerate(sub, 1):
            x = r[view]
            rows.append(f'<tr><td class="pos" data-v="{i}">{i}</td>{team_cell(r)}' + "".join(f'<td{" class=gf-xs" if k in XS else ""} data-v="{x[k]}">{x[k]}</td>' for k in ("p", "w", "d", "l", "gf", "ga")) + f'<td class="pts" data-v="{x["pts"]}">{x["pts"]}</td></tr>')
    cap = {"all": "Overall", "home": "Home matches only", "away": "Away matches only"}[view]
    return (f'<div class="gf-table-wrap" tabindex="0" role="region" aria-label="{esc(l["name"])} table, {cap.lower()} — scroll sideways for more columns">'
            f'<table class="gf-table" data-sortable data-live="{tid}-live"><caption class="gf-sr">{esc(l["name"])} {esc(l["source_name"].split()[-1])} — {cap}, to {esc(DATA_TO)}</caption>'
            f'<thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>')


def results_list(rows, fixtures=False):
    items = []
    for m in rows:
        if fixtures or m["hs"] is None:
            sc = f'<span class="sc ko">{esc(m["time"][:5]) or "TBC"}</span>'
            hc = ac = ""
        else:
            sc = f'<span class="sc" aria-label="{m["hs"]} to {m["as_"]}">{m["hs"]}–{m["as_"]}</span>'
            hc = "win" if m["hs"] > m["as_"] else ""; ac = "win" if m["as_"] > m["hs"] else ""
        items.append(f'<li><span class="h {hc}">{esc(m["hname"])}</span>{sc}<span class="a {ac}">{esc(m["aname"])}</span><span class="date">{esc(C.nice_date(m["date"], False))}</span></li>')
    return f'<ul class="gf-results">{"".join(items)}</ul>'


def figure(title, sub, inner, caption, fid, data_table=""):
    dt = f'<details class="gf-data"><summary>Show the numbers as a table</summary>{data_table}</details>' if data_table else ""
    return f'<figure class="gf-figure" id="{fid}" aria-labelledby="{fid}-t"><h3 id="{fid}-t">{esc(title)}</h3><p class="sub">{esc(sub)}</p>{inner}<figcaption>{caption}</figcaption>{dt}</figure>'


SRC = "Source: openfootball (public domain, CC0 1.0); computed by gameformative."


def simple_table(headers, rows, label):
    th = "".join(f'<th scope="col" class="{"team l" if i == 0 else ""}">{esc(h)}</th>' for i, h in enumerate(headers))
    tr = "".join("<tr>" + "".join((f'<th scope="row" class="team">{esc(c)}</th>' if i == 0 else f"<td>{esc(c)}</td>") for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="gf-table-wrap" tabindex="0" role="region" aria-label="{esc(label)}"><table class="gf-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def bars(items, maxv=None, fmt=lambda v: str(v)):
    """items: (label, sublabel, value, cls)"""
    maxv = maxv or max(v for _, _, v, _ in items) or 1
    sm = lambda s: f"<small>{esc(s)}</small>" if s else ""
    li = "".join(f'<li class="{c}"><span class="lab">{esc(l)}{sm(s)}</span><span class="track" aria-hidden="true"><span class="fill" style="width:{100 * v / maxv:.1f}%"></span></span><span class="val">{esc(fmt(v))}</span></li>' for l, s, v, c in items)
    return f'<ul class="gf-bars">{li}</ul>'


def stack(items):
    legend = '<ul class="gf-legend" aria-hidden="true"><li><i class="h"></i>Home win</li><li><i class="d"></i>Draw</li><li><i class="a"></i>Away win</li></ul>'
    li = "".join(f'<li><span class="lab">{esc(l)}</span><span class="bar" role="img" aria-label="{esc(l)}: home wins {h:.1f}%, draws {d:.1f}%, away wins {a:.1f}%">'
                 f'<span class="h" style="width:{h}%">H {h:.0f}%</span><span class="d" style="width:{d}%">D {d:.0f}%</span><span class="a" style="width:{a}%">A {a:.0f}%</span></span></li>' for l, h, d, a in items)
    return legend + f'<ul class="gf-stack">{li}</ul>'


def cols(items):
    maxv = max(v for _, v, _ in items)
    c = "".join(f'<div class="col {cl}"><span class="v">{v}</span><span class="bar" style="height:{100 * v / maxv:.1f}%"></span></div>' for _, v, cl in items)
    lab = "".join(f"<span>{esc(l)}</span>" for l, _, _ in items)
    return f'<div aria-hidden="true"><div class="gf-cols">{c}</div><div class="gf-cols-labels">{lab}</div></div>'


def line_chart(series, rounds, label):
    """series: list of (name, points list, style class s1/s2/s3/''). HTML labels over a stretched SVG,
    so the text stays legible at 375 px and at 1440 px."""
    ymax = max(max(p) for _, p, _ in series)
    ymax = ((ymax + 4) // 5) * 5 or 5
    X = lambda i: 100 * i / max(rounds - 1, 1)
    Y = lambda v: 100 - 100 * v / ymax
    grid = "".join(f'<line class="gl" x1="0" x2="100" y1="{Y(v):.2f}" y2="{Y(v):.2f}"/>' for v in range(0, ymax + 1, 5))
    lines = "".join(f'<polyline class="ln {c}" points="{" ".join(f"{X(i):.2f},{Y(v):.2f}" for i, v in enumerate(p))}"/>' for n, p, c in sorted(series, key=lambda s: s[2] != ""))
    yl = "".join(f'<span class="yl" style="top:{Y(v):.2f}%">{v}</span>' for v in range(0, ymax + 1, 5))
    step = 1 if rounds <= 10 else 5
    xs = [i for i in range(0, rounds, step)] + ([rounds - 1] if (rounds - 1) % step else [])
    xl = "".join(f'<span class="xl" style="left:{X(i):.2f}%">{i + 1}</span>' for i in xs)
    # end labels, nudged apart so they never overlap (min 7% of height)
    ends = sorted(((Y(p[-1]), n, c, p[-1]) for n, p, c in series), key=lambda e: e[0])
    placed = []
    for y, n, c, v in ends:
        if placed and y - placed[-1][0] < 7: y = placed[-1][0] + 7
        placed.append((y, n, c, v))
    el = "".join(f'<span class="el {c}" style="top:{y:.2f}%">{esc(n)} {v}</span>' for y, n, c, v in placed)
    return (f'<div class="gf-line" role="img" aria-label="{esc(label)}"><svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">{grid}{lines}</svg>{yl}{xl}{el}</div>'
            f'<p class="gf-meta" style="text-align:center;margin:0">Matchday</p>')


def race_figure(l, fid, title=None):
    ser = l["race"]["series"]
    styles = ["s1", "s2", "s3", "", "", ""]
    series = [(s["code"], s["points"], styles[i]) for i, s in enumerate(ser)]
    rows = [[s["name"]] + [str(x) for x in s["points"]] for s in ser]
    return figure(title or f"{l['name']}: the points race", f"Cumulative points by matchday, top six after matchday {l['rounds_done']}.",
                  line_chart(series, l["race"]["rounds"], f"Line chart of cumulative points; {', '.join(f'{s[0]} {s[1][-1]}' for s in series)}"),
                  SRC, fid, simple_table(["Team"] + [f"MD{i + 1}" for i in range(l["race"]["rounds"])], rows, "Points by matchday"))


def chart(cid):
    """Charts embedded in the articles, by id."""
    p = S["pl2526"]; w = S["wc2026"]
    if cid == "race-en":
        return race_figure(LG["en"], cid)
    if cid == "after5-2526":
        ser = sorted(((s["points"][4], i + 1, s) for i, s in enumerate(p["race"]["series"])), key=lambda x: (-x[0], x[1]))[:6]
        items = [(s["name"], f"finished {C.ordinal(pos)} · {p['table'][pos - 1]['pts']} pts", v, "hi" if pos == 1 else "hi2" if i == 0 else "") for i, (v, pos, s) in enumerate(ser)]
        return figure("2025/26: points after five matchdays", "The six best starts last season, and where each team finished.",
                      bars(items, fmt=lambda v: f"{v} pts"), SRC + " Blue: the eventual champions. Orange: the best start.", cid,
                      simple_table(["Team", "Pts after 5", "Final position", "Final pts"], [[s["name"], v, pos, p["table"][pos - 1]["pts"]] for v, pos, s in ser], "Points after five"))
    if cid == "gpg-big5":
        ls = sorted(LEAGUES, key=lambda l: -l["agg"]["gpg"])
        items = [(l["name"], f"{l['agg']['matches']} matches", l["agg"]["gpg"], "hi" if i == 0 else "") for i, l in enumerate(ls)]
        return figure("Goals per game, 2026/27 so far", f"All goals divided by matches played, to {DATA_TO}.", bars(items, fmt=lambda v: f"{v:.2f}"), SRC, cid,
                      simple_table(["League", "Matches", "Goals", "Goals per game"], [[l["name"], l["agg"]["matches"], l["agg"]["goals"], f"{l['agg']['gpg']:.2f}"] for l in ls], "Goals per game"))
    if cid == "outcomes-big5":
        return figure("How matches end", "Share of results that were home wins, draws and away wins.",
                      stack([(l["name"], l["agg"]["home_pct"], l["agg"]["draw_pct"], l["agg"]["away_pct"]) for l in LEAGUES]), SRC, cid,
                      simple_table(["League", "Home win %", "Draw %", "Away win %", "Both scored %"], [[l["name"], l["agg"]["home_pct"], l["agg"]["draw_pct"], l["agg"]["away_pct"], l["agg"]["btts_pct"]] for l in LEAGUES], "Outcomes"))
    if cid == "spain-path":
        rows = [r for r in w["results"] if "Spain" in (r["home"], r["away"])]
        li = "".join(f'<li><span class="h {"win" if r["hs"] > r["as_"] else ""}">{esc(r["home"])}</span><span class="sc">{r["hs"]}–{r["as_"]}{" aet" if r["how"] == "aet" else ""}</span><span class="a {"win" if r["as_"] > r["hs"] else ""}">{esc(r["away"])}</span><span class="date">{esc(("Group " + r["group"]) if r["group"] else r["round"])} · {esc(C.nice_date(r["date"], False))}</span></li>' for r in rows)
        return figure("Spain’s eight matches", "Group H to the final.", f'<ul class="gf-results">{li}</ul>', SRC, cid)
    if cid == "wc-stages":
        st = w["stage_goals"]
        items = [(s["stage"].replace("Match for third place", "Third place"), f"{s['matches']} match{'es' if s['matches'] > 1 else ''} · {s['goals']} goals", s["gpg"], "hi2" if s["gpg"] == max(x["gpg"] for x in st) else "") for s in st]
        return figure("Goals per game by stage", "World Cup 2026. Single matches (third place, final) are one game each — read them as results, not rates.",
                      bars(items, fmt=lambda v: f"{v:.2f}"), SRC, cid,
                      simple_table(["Stage", "Matches", "Goals", "Per game"], [[s["stage"], s["matches"], s["goals"], f"{s['gpg']:.2f}"] for s in st], "Goals by stage"))
    if cid == "minutes-2526":
        bm = p["by_minute"]; mx = max(b["goals"] for b in bm)
        return figure("When the goals came, 2025/26", f"All {p['goals']:,} Premier League goals by the minute recorded; added time counted with the period it ends.",
                      cols([(b["label"], b["goals"], "hi" if b["goals"] == mx else "") for b in bm]), SRC, cid,
                      simple_table(["Minutes", "Goals", "Share"], [[b["label"], b["goals"], C.pct(100 * b["goals"] / p["goals"])] for b in bm], "Goals by minute"))
    if cid == "scorers-2526":
        sc = p["scorers"][:8]
        return figure("Top scorers, 2025/26", "Premier League goals, own goals excluded; penalties in brackets.",
                      bars([(s["name"], s["team"], s["goals"], "hi" if i == 0 else "") for i, s in enumerate(sc)], fmt=lambda v: str(v)), SRC + " Names as the source records them; accents the source omits are not restored.", cid,
                      simple_table(["Player", "Team", "Goals", "Penalties"], [[s["name"], s["team"], s["goals"], s["pens"]] for s in sc], "Top scorers"))
    if cid == "form-example":
        rows = [LG[x]["table"][0] for x in ("en", "es", "de", "it", "fr")]
        li = "".join(f'<li><span class="lab">{esc(r["name"])}</span>{form(r["form"])}</li>' for r in rows)
        return figure("Reading a form guide", "The leaders of the big five, last five results, oldest first.",
                      f'<ul class="gf-bars" style="grid-template-columns:1fr">{li}</ul>'.replace("<li>", '<li style="grid-template-columns:minmax(84px,30%) 1fr">'), SRC, cid)
    raise KeyError(cid)


def cover(spec, title):
    """Decorative data graphic for a story card (aria-hidden; the headline is the link text)."""
    t = spec["type"]
    svg = '<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
    if t == "race":
        l = LG[spec["league"]]; ser = l["race"]["series"]; ymax = max(max(s["points"]) for s in ser) + 2
        n = l["race"]["rounds"]
        svg += "".join(f'<line class="k-faint" x1="24" x2="296" y1="{150 - 120 * v / ymax:.1f}" y2="{150 - 120 * v / ymax:.1f}"/>' for v in range(0, ymax, 5))
        for i, s in enumerate(reversed(ser)):
            cls = "k-line" if s is ser[0] else "k-line2" if s is ser[1] else "k-faint"
            pts = " ".join(f"{24 + 272 * j / (n - 1):.1f},{150 - 120 * v / ymax:.1f}" for j, v in enumerate(s["points"]))
            svg += f'<polyline class="{cls}" points="{pts}"/>'
        svg += f'<text class="k-small" x="24" y="30" font-size="11">{esc(l["name"].upper())} · POINTS RACE</text>'
    elif t == "bars":
        ls = sorted(LEAGUES, key=lambda l: -l["agg"]["gpg"]); mx = ls[0]["agg"]["gpg"]
        for i, l in enumerate(ls):
            h = 110 * l["agg"]["gpg"] / mx
            svg += f'<rect class="{"k-bar2" if i == 0 else "k-bar"}" x="{34 + i * 56}" y="{156 - h:.1f}" width="40" height="{h:.1f}" rx="3"/>'
            svg += f'<text class="k-big" x="{54 + i * 56}" y="{150 - h:.1f}" font-size="15" text-anchor="middle">{l["agg"]["gpg"]:.2f}</text>'
        svg += '<text class="k-small" x="24" y="24" font-size="11">GOALS PER GAME · BIG FIVE</text>'
    elif t == "final":
        f = S["wc2026"]["final"]["row"]
        svg += f'<text class="k-small" x="160" y="44" font-size="11" text-anchor="middle">WORLD CUP 2026 · FINAL · AET</text>'
        svg += f'<text class="k-big" x="160" y="118" font-size="64" text-anchor="middle">{f["hcode"]} {f["hs"]}–{f["as_"]} {f["acode"]}</text>'
        svg += '<rect class="k-bar2" x="130" y="136" width="60" height="5" rx="2"/>'
    elif t == "minutes":
        bm = S["pl2526"]["by_minute"]; mx = max(b["goals"] for b in bm)
        for i, b in enumerate(bm):
            h = 110 * b["goals"] / mx
            svg += f'<rect class="{"k-bar2" if b["goals"] == mx else "k-bar3"}" x="{34 + i * 45}" y="{156 - h:.1f}" width="34" height="{h:.1f}" rx="3"/>'
        svg += '<text class="k-small" x="24" y="24" font-size="11">2025/26 · GOALS BY MINUTE</text>'
    elif t == "explainer":
        seq = "WWDLWDWWLD"
        for i, r in enumerate(seq):
            cls = "k-bar" if r == "W" else "k-bar3" if r == "D" else "k-bar2"
            x = 28 + (i % 5) * 56; y = 52 + (i // 5) * 58
            svg += f'<rect class="{cls}" x="{x}" y="{y}" width="46" height="46" rx="8"/><text class="k-big" x="{x + 23}" y="{y + 33}" font-size="26" text-anchor="middle" style="fill:#0B0F1A">{r}</text>'
        svg += '<text class="k-small" x="24" y="30" font-size="11">EXPLAINER · PPG · GD · FORM</text>'
    elif t == "evidence":
        # The seed review's two pooled estimates (Sport Mont 2026, doi 10.26773/smj.260219): OR 1.33
        # (95% CI 0.85–2.07, not significant) and RR 2.33 (1.65–3.30). A line at 1 = no effect.
        X = lambda v: 40 + 240 * v / 3.5
        svg += f'<line class="k-faint" x1="{X(1):.1f}" x2="{X(1):.1f}" y1="52" y2="150" stroke-dasharray="4 4"/>'
        for y, lo, mid, hi_, cls, lab in ((82, 0.85, 1.33, 2.07, "k-line", "ODDS RATIO 1.33"), (128, 1.65, 2.33, 3.30, "k-line2", "RELATIVE RISK 2.33")):
            svg += f'<line class="{cls}" x1="{X(lo):.1f}" x2="{X(hi_):.1f}" y1="{y}" y2="{y}"/><circle class="{"k-bar" if cls == "k-line" else "k-bar2"}" cx="{X(mid):.1f}" cy="{y}" r="9"/>'
            svg += f'<text class="k-small" x="{X(lo):.1f}" y="{y - 16}" font-size="10">{lab}</text>'
        svg += f'<text class="k-small" x="{X(1) + 4:.1f}" y="164" font-size="9">1 = NO EFFECT</text>'
        svg += '<text class="k-small" x="24" y="30" font-size="11">ONE REVIEW · TWO ANSWERS · “HIGH LOAD”</text>'
    return f'<span class="gf-cover">{svg}</svg></span>'


THROUGH = ' <span class="gf-through" title="Reached the round of 32">✓</span>'


def data_label(kind):
    return f'<span class="gf-label gf-label--data">{esc(kind)}</span>'


def label(kind):
    return f'<span class="gf-label{" gf-label--explainer" if kind == "Explainer" else ""}">{esc(kind)}</span>'


def topic_link(a, depth):
    tp = C.TOPIC[a["topic"]]
    return f'<a class="gf-topiclink" href="{up(depth)}topics/{tp["slug"]}.html">{esc(tp["name"])}</a>'


def desk_link(a, depth):
    dk = C.DESK[a["desk"]]
    return f'<a class="gf-topiclink" href="{up(depth)}desks/{dk["slug"]}.html">{esc(dk["name"])}</a>'


def meta(a):
    return f'{esc(C.DESK[a["desk"]]["name"])} · {esc(a["kind"])}'


def excerpt(a, n=170):
    """A card's text: the standfirst, or — for an article without one — the opening of its first paragraph."""
    if a["standfirst"]: return a["standfirst"]
    first = next(x for _, items in a["segments"] for x in items if isinstance(x, str))
    return first if len(first) <= n else first[:first.rfind(" ", 0, n)] + "…"


def story_card(a, depth, h="h3"):
    return (f'<article class="gf-story-card"><a class="gf-card-link" href="{up(depth)}articles/{a["slug"]}.html">{cover(a["cover"], a["title"])}'
            f'<span class="body"><span class="gf-cardmeta">{meta(a)}</span><{h}>{esc(a["title"])}</{h}><p>{esc(excerpt(a))}</p><span class="gf-meta">{esc(C.SITE["published"])} · {reading(a)}</span></span></a></article>')


def reading(a):
    return f"{max(1, round(C.body_chars(a) / 1000))} min read"


def roundup(l):
    """Automated: a template fills this from the match data. Labelled as such wherever it appears."""
    ms = l["latest"]; goals = sum(m["hs"] + m["as_"] for m in ms)
    big = max(ms, key=lambda m: (abs(m["hs"] - m["as_"]), m["hs"] + m["as_"]))
    unbeaten = [r["name"] for r in l["table"] if r["l"] == 0]
    winless = [r["name"] for r in l["table"] if r["w"] == 0]
    win_side = (big["hname"], big["aname"]) if big["hs"] >= big["as_"] else (big["aname"], big["hname"])
    parts = [f"{len(ms)} matches, {goals} goals ({goals / len(ms):.2f} a game).",
             f"Biggest margin: {big['hname']} {big['hs']}–{big['as_']} {big['aname']}." if big["hs"] != big["as_"] else f"Every match was level on the day, the highest {big['hs']}–{big['as_']}.",
             f"Top after the round: {l['table'][0]['name']}, {l['table'][0]['pts']} points.",
             ("Still unbeaten: " + ", ".join(unbeaten) + ".") if unbeaten else "No team is unbeaten.",
             ("Still without a win: " + ", ".join(winless) + ".") if winless else "Every team has won at least once."]
    return (f'<div class="gf-card"><p style="margin-bottom:6px"><span class="gf-label gf-label--automated">Automated</span></p>'
            f'<h3 style="font-size:19px;font-stretch:85%;margin-bottom:6px">Matchday {l["rounds_done"]} in numbers: {esc(l["name"])}</h3>'
            f'<p style="margin:0">{esc(" ".join(parts))}</p>'
            f'<p class="gf-meta" style="margin:8px 0 0">Written by a template from the match data, no human edit. <a href="{{UP}}how-we-count/index.html#automation">How automation works here</a></p></div>')


# ------------------------------------------------------------------ pages
def desk_tiles(depth, link_prefix=None):
    pre = up(depth) + "desks/" if link_prefix is None else link_prefix
    out = []
    for s, n, does in C.DESKS:
        k = sum(1 for a in ARTICLES if a["desk"] == s)
        out.append(f'<li><a class="gf-topic-tile gf-desk-tile" href="{pre}{s}.html"><span class="n">{esc(n)}</span><span class="b">{esc(does)}</span>'
                   f'<span class="c">{k} article{"s" if k != 1 else ""}{"" if k else " · none published yet"}</span></a></li>')
    return "".join(out)


def build_home():
    d = 0
    lead, rest = ARTICLES[0], ARTICLES[1:]
    latest = "".join(f'<li><a href="articles/{a["slug"]}.html"><span class="gf-cardmeta">{esc(C.DESK[a["desk"]]["name"])}</span><span class="t">{esc(a["title"])}</span><span class="gf-meta">{reading(a)}</span></a></li>' for a in rest[:4])
    cards = "".join(story_card(a, d) for a in rest[:3])
    tiles = desk_tiles(d)
    body = f"""<h1 class="gf-sr">gameformative — sport, explained</h1>
<div class="gf-lead">
  <a class="gf-lead-story" href="articles/{lead["slug"]}.html">{cover(lead["cover"], lead["title"])}
    <span class="gf-cardmeta" style="display:block;margin-top:14px">{meta(lead)}</span>
    <h2>{esc(lead["title"])}</h2><p>{esc(excerpt(lead, 230))}</p><span class="gf-meta">{esc(lead["byline"])} · {esc(C.SITE["published"])} · {reading(lead)}</span></a>
  <aside class="gf-rail" aria-labelledby="latest-h"><div class="gf-card gf-latest"><h2 id="latest-h" class="gf-kicker">Latest</h2><ol>{latest}</ol><a class="gf-btn gf-btn--quiet" href="articles/index.html">All articles</a></div></aside>
</div>
<section class="gf-section" aria-labelledby="an-h"><div class="gf-section-head"><h2 id="an-h">More to read</h2><a href="articles/index.html">All articles</a></div><div class="gf-grid gf-grid--3">{cards}</div></section>
<section class="gf-section" aria-labelledby="tp-h"><div class="gf-section-head"><h2 id="tp-h">The eight desks</h2><a href="desks/index.html">All desks</a></div><p class="gf-meta" style="margin:-6px 0 14px">Every article sits on one desk — by what it does for you.</p><ul class="gf-topic-grid gf-desk-grid">{tiles}</ul></section>
<section class="gf-section gf-band" aria-labelledby="pr-h"><div class="gf-band-grid"><div><p class="gf-kicker">How we work</p><h2 id="pr-h" class="gf-display" style="font-size:clamp(28px,5.5vw,44px)">Every source on the table</h2>
<p>Each article ends with two lists: the sources we used, and the sources we investigated but did not use — with the reason. Articles run from 800 to 3,200 characters, always in segments you can scan.</p>
<p><a class="gf-btn" href="how-we-count/index.html#sources">How we source</a></p></div>
<ul class="gf-promise"><li><b>{C.RULES["min_chars"]:,}–{C.RULES["max_chars"]:,}</b><span>characters of body text per article</span></li><li><b>{C.RULES["min_segments"]}+</b><span>headed segments, every time</span></li><li><b>2</b><span>source lists: used, and investigated but not used</span></li></ul></div></section>
<section class="gf-section gf-band" aria-labelledby="nl-h"><div class="gf-band-grid"><div><p class="gf-kicker">Newsletter</p><h2 id="nl-h" class="gf-display" style="font-size:clamp(26px,5vw,38px)">The Monday brief</h2><p>The week’s best reads across sport science, tactics, tech and the business of sport. Once a week.</p></div>
<form class="gf-signup" onsubmit="return false" aria-describedby="nl-note"><label class="gf-sr" for="nl-email">E-mail address</label><input id="nl-email" type="email" placeholder="you@example.com" disabled><button class="gf-btn is-unavailable" type="submit" aria-disabled="true" title="The newsletter is not built in the prototype">Subscribe</button><p id="nl-note" class="gf-meta" style="grid-column:1/-1;margin:0">Not built in the prototype — nothing is collected. Consent and sender are set before launch.</p></form></div></section>"""
    page("index.html", "gameformative — sport, explained", C.SITE["description"], "Home", body, d,
         jsonld=[{"@context": "https://schema.org", "@type": "WebSite", "name": "gameformative", "url": SITE_URL, "description": C.SITE["description"], "inLanguage": "en-GB"},
                 {"@context": "https://schema.org", "@type": "Organization", "name": "gameformative", "url": SITE_URL, "logo": SITE_URL + "assets/icons/icon-512.png"}])


def build_scores():
    d = 1
    btns = '<button type="button" data-league="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-league="{l["id"]}" aria-pressed="false">{esc(l["name"])}</button>' for l in LEAGUES)
    blocks = []
    for l in LEAGUES:
        blocks.append(f"""<section class="gf-section" data-league-block="{l["id"]}" aria-labelledby="sc-{l["id"]}"><div class="gf-section-head"><h2 id="sc-{l["id"]}">{esc(l["name"])}</h2><a href="../stats/{l["slug"]}.html">Table & stats</a></div>
<div class="gf-grid gf-grid--2"><div><h3 class="gf-kicker">Results · matchday {l["rounds_done"]}</h3>{results_list(l["latest"])}</div>
<div><h3 class="gf-kicker">Next fixtures · as scheduled</h3>{results_list(l["upcoming"][:len(l["latest"])], fixtures=True)}</div></div>
<div style="margin-top:12px">{roundup(l).replace("{UP}", up(d))}</div></section>""")
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Scores</p><h1>Results and fixtures</h1><p>The latest round in Europe’s big five leagues, with every result recorded to {esc(DATA_TO)}, and the next fixtures as the published schedule lists them. Kick-off times are local to the venue, as the source gives them.</p></div>
<div class="gf-seg" data-filter role="group" aria-label="Filter by league">{btns}</div>
{"".join(blocks)}
<div class="gf-inert" style="margin-top:28px"><h3>Live scores</h3><p style="margin:0">A live feed with minute-by-minute updates needs a licensed real-time data provider; the prototype shows final results only. On the live site the score strip and this page update in place, announced politely to screen readers, with a pause control.</p></div>"""
    page("scores/index.html", "Results and fixtures — gameformative", "Latest results and next fixtures in the Premier League, LaLiga, Bundesliga, Serie A and Ligue 1.", None, body, d, later=True)


def build_stats_hub():
    d = 1
    rows = "".join(f'<li><a class="gf-card" style="display:grid;grid-template-columns:1fr auto;gap:6px 12px;text-decoration:none;color:inherit" href="{l["slug"]}.html"><span><b style="font-size:20px;color:var(--gf-ink)">{esc(l["name"])}</b><br><span class="gf-meta">{esc(l["country"])} · matchday {l["rounds_done"]} · leader {esc(l["table"][0]["name"])} ({l["table"][0]["pts"]} pts)</span></span><span class="gf-stat" style="border:0;padding:0;text-align:right"><span class="n" style="font-size:34px">{l["agg"]["gpg"]:.2f}</span><span class="ctx">goals / game</span></span></a></li>' for l in LEAGUES)
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Tables & stats</p><h1>Europe’s big five, 2026/27</h1><p>Full tables with home and away splits, form, points per game and the points race for each league — and the five compared. Every figure is computed from the recorded results to {esc(DATA_TO)}.</p></div>
<ul class="gf-grid gf-grid--2" style="list-style:none;margin:0;padding:0">{rows}</ul>
<section class="gf-section" aria-labelledby="cmp-h"><div class="gf-section-head"><h2 id="cmp-h">The five compared</h2><a href="../articles/big-five-first-month.html">Read the analysis</a></div>
<div class="gf-grid gf-grid--2">{chart("gpg-big5")}{chart("outcomes-big5")}</div></section>
<section class="gf-section" aria-labelledby="arc-h"><div class="gf-section-head"><h2 id="arc-h">Season reviews</h2></div>
<div class="gf-grid gf-grid--2"><a class="gf-card" href="premier-league-2025-26.html" style="text-decoration:none;color:inherit"><span class="gf-label gf-label--data">Complete season</span><h3 style="font-size:24px;font-stretch:85%;margin:8px 0 4px">Premier League 2025/26</h3><p class="gf-meta" style="margin:0">Final table, the points race over 38 matchdays, top scorers, goals by minute, attendances.</p></a>
<a class="gf-card" href="../world-cup-2026/index.html" style="text-decoration:none;color:inherit"><span class="gf-label gf-label--data">Complete tournament</span><h3 style="font-size:24px;font-stretch:85%;margin:8px 0 4px">World Cup 2026</h3><p class="gf-meta" style="margin:0">All 104 matches: groups, the bracket, scorers and the final.</p></a></div></section>"""
    page("stats/index.html", "Tables & stats — gameformative", "Tables, form and statistics for Europe's big five football leagues, 2026/27.", None, body, d, later=True)


def build_league(l):
    d = 1
    a = l["agg"]
    tabs = "".join(f'<a href="{x["slug"]}.html"' + (' aria-current="page"' if x is l else "") + f'>{esc(x["name"])}</a>' for x in LEAGUES)
    views = (f'<div data-views><div class="gf-seg" role="group" aria-label="Table view"><button type="button" data-view="all" aria-pressed="true">Overall</button><button type="button" data-view="home" aria-pressed="false">Home</button><button type="button" data-view="away" aria-pressed="false">Away</button><button type="button" class="gf-xs-toggle" data-cols aria-pressed="false">All columns</button></div>'
             f'<div data-panel="all">{league_table(l, "all", tid=l["id"] + "a")}</div><div data-panel="home" hidden>{league_table(l, "home", False, l["id"] + "h")}</div><div data-panel="away" hidden>{league_table(l, "away", False, l["id"] + "w")}</div>'
             f'<p class="gf-sr" aria-live="polite" id="{l["id"]}a-live"></p><p class="gf-sr" aria-live="polite" id="{l["id"]}h-live"></p><p class="gf-sr" aria-live="polite" id="{l["id"]}w-live"></p></div>')
    stats = [(f"{a['gpg']:.2f}", "goals per game", f"{a['goals']} in {a['matches']} matches"),
             (f"{a['home_pct']:.0f}%", "home wins", f"draws {a['draw_pct']:.0f}% · away {a['away_pct']:.0f}%"),
             (f"{a['btts_pct']:.0f}%", "both teams scored", f"{a['nil_nil']} goalless draw{'s' if a['nil_nil'] != 1 else ''}"),
             (f"{a['biggest']['hs']}–{a['biggest']['as_']}", "biggest margin", f"{a['biggest']['home']} v {a['biggest']['away']}, {C.short_date(a['biggest']['date'])}")]
    tiles = "".join(f'<div class="gf-stat{" gf-stat--accent" if i == 0 else ""}"><span class="n">{esc(n)}</span><span class="what">{esc(w)}</span><span class="ctx">{esc(c)}</span></div>' for i, (n, w, c) in enumerate(stats))
    best_att = max(l["table"], key=lambda r: (r["gf"], -r["pos"])); best_def = min(l["table"], key=lambda r: (r["ga"], r["pos"]))
    home_best = max(l["table"], key=lambda r: (r["home"]["pts"], r["home"]["gf"] - r["home"]["ga"])); away_best = max(l["table"], key=lambda r: (r["away"]["pts"], r["away"]["gf"] - r["away"]["ga"]))
    cs = sorted(l["table"], key=lambda r: (-r["cs"], r["pos"]))[:5]
    body = f"""<nav class="gf-seg" aria-label="Leagues">{tabs}</nav>
<div class="gf-pagehead"><p class="gf-kicker">{esc(l["country"])} · 2026/27</p><h1>{esc(l["name"])}</h1><p>After matchday {l["rounds_done"]} — {l["played"]} of {l["fixtures"]} matches played, results to {esc(C.nice_date(l["last_date"]))}. Ordered by points, goal difference, goals scored.</p></div>
<div class="gf-stats-row">{tiles}</div>
<section class="gf-section" aria-labelledby="t-h"><div class="gf-section-head"><h2 id="t-h">Table</h2></div>{views}
<div class="gf-table-foot"><span class="gf-key"><i class="top"></i>Top four</span><span class="gf-key"><i class="bottom"></i>Bottom three</span><span>Form: oldest left · W won · D drawn · L lost</span><span>Tap a column heading to sort</span><span>Tie order is the site’s own; <a href="../how-we-count/index.html#data">official tie-breakers differ</a></span></div></section>
<section class="gf-section" aria-labelledby="r-h"><div class="gf-section-head"><h2 id="r-h">Form and leaders</h2></div>
<div class="gf-grid gf-grid--2">{race_figure(l, "race")}
<div class="gf-grid">{figure("Team leaders", "Across all matches so far.", bars([(best_att["name"], "most goals scored", best_att["gf"], "hi"), (best_def["name"], "fewest conceded", best_def["ga"], ""), (home_best["name"], f"best at home · {home_best['home']['w']}W {home_best['home']['d']}D {home_best['home']['l']}L", home_best["home"]["pts"], ""), (away_best["name"], f"best away · {away_best['away']['w']}W {away_best['away']['d']}D {away_best['away']['l']}L", away_best["away"]["pts"], "")], fmt=lambda v: str(v)), SRC + " Values: goals, goals, home points, away points.", "leaders")}
{figure("Clean sheets", "Matches without conceding.", bars([(r["name"], "", r["cs"], "hi" if i == 0 else "") for i, r in enumerate(cs)]), SRC, "cleansheets")}</div></div></section>
<section class="gf-section" id="results" aria-labelledby="res-h"><div class="gf-section-head"><h2 id="res-h">Matchday {l["rounds_done"]} results</h2><a href="../scores/index.html">All leagues</a></div>
<div class="gf-grid gf-grid--2"><div>{results_list(l["latest"])}</div><div>{roundup(l).replace("{UP}", up(d))}<h3 class="gf-kicker" style="margin-top:18px">Next fixtures · as scheduled</h3>{results_list(l["upcoming"][:5], fixtures=True)}</div></div></section>
<div class="gf-inert" style="margin-top:28px"><h3>Expected goals, shots and player ratings</h3><p style="margin:0">Shown on the live site from a licensed event-data provider (shot-level data: xG, shots, possession, player ratings). The prototype’s public-domain source carries results only, so these panels are not filled — and never estimated.</p></div>"""
    page(f"stats/{l['slug']}.html", f"{l['name']} table and stats 2026/27 — gameformative", f"{l['name']} 2026/27: table, home and away, form, points per game, points race and results.", None, body, d, later=True)


def build_pl2526():
    d = 1
    p = S["pl2526"]
    t = dict(name="Premier League", source_name="2025/26", table=p["table"])
    ser = p["race"]["series"][:4]
    race = figure("The title race, 2025/26", "Cumulative points over 38 matchdays, the final top four.",
                  line_chart([(s["code"], s["points"], ["s1", "s2", "s3", ""][i]) for i, s in enumerate(ser)], 38, "Line chart of cumulative points for the final top four; " + ", ".join(f"{s['code']} {s['points'][-1]}" for s in ser)),
                  SRC, "race2526", simple_table(["Team", "After 10", "After 19", "After 29", "Final"], [[s["name"], s["points"][9], s["points"][18], s["points"][28], s["points"][-1]] for s in ser], "Points at stages"))
    att = p["attendance"]
    tiles = [(f"{p['goals']:,}", "goals", f"{p['agg']['gpg']:.2f} per game"), (f"{p['table'][0]['pts']}", f"points for {p['champion']}", f"{p['table'][0]['pts'] - p['table'][1]['pts']} clear of {p['table'][1]['name']}"),
             (f"{p['scorers'][0]['goals']}", p["scorers"][0]["name"], f"top scorer, {p['scorers'][0]['team']}"), (f"{att['avg']:,}", "average attendance", f"{att['total']:,} in total")]
    tiles_h = "".join(f'<div class="gf-stat{" gf-stat--accent" if i == 0 else ""}"><span class="n">{esc(n)}</span><span class="what">{esc(w)}</span><span class="ctx">{esc(c)}</span></div>' for i, (n, w, c) in enumerate(tiles))
    lt = f'<div data-views><div class="gf-seg gf-seg--xs" role="group" aria-label="Table columns"><button type="button" class="gf-xs-toggle" data-cols aria-pressed="false">All columns</button></div>{league_table(dict(t, id="p25"), "all", tid="p25")}</div>'
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Season review · complete</p><h1>Premier League 2025/26</h1><p>All 380 matches, from {esc(C.nice_date("2025-08-15"))} to {esc(C.nice_date("2026-05-24"))}. {esc(p["champion"])} champions on {p["table"][0]["pts"]} points.</p></div>
<div class="gf-stats-row">{tiles_h}</div>
<section class="gf-section" aria-labelledby="ft-h"><div class="gf-section-head"><h2 id="ft-h">Final table</h2></div>{lt}<p class="gf-sr" aria-live="polite" id="p25-live"></p>
<div class="gf-table-foot"><span>Form: the last five matches of the season</span><span>Tap a column heading to sort</span></div></section>
<section class="gf-section" aria-labelledby="rc-h"><div class="gf-section-head"><h2 id="rc-h">How it was won</h2><a href="../articles/premier-league-five-matchdays-in.html">Five matchdays in, this season</a></div><div class="gf-grid gf-grid--2">{race}{chart("after5-2526")}</div></section>
<section class="gf-section" aria-labelledby="gl-h"><div class="gf-section-head"><h2 id="gl-h">Goals</h2><a href="../articles/premier-league-2025-26-goals-by-minute.html">Read the analysis</a></div><div class="gf-grid gf-grid--2">{chart("minutes-2526")}{chart("scorers-2526")}</div>
<p class="gf-note">Largest crowd: {att["top"]["n"]:,} at {esc(att["top"]["ground"])}, {esc(att["top"]["home"])} v {esc(att["top"]["away"])}, {esc(C.nice_date(att["top"]["date"]))}. {p["pens"]} penalties scored and {p["owngoals"]} own goals across the season.</p></section>"""
    page("stats/premier-league-2025-26.html", "Premier League 2025/26 season review — gameformative", "The complete 2025/26 Premier League: final table, title race, top scorers, goals by minute and attendances.", None, body, d, later=True)


def tie(m, final=False):
    def side(team, code, g, won):
        return f'<div class="{"won" if won else "lost"}"><span>{esc(team)}</span><b>{g}</b></div>'
    note = " · pens " + "–".join(map(str, m["pens"])) if m["pens"] else " · aet" if m["how"] == "aet" else ""
    return (f'<div class="gf-tie{" gf-tie--final" if final else ""}">{side(m["home"], m["hcode"], m["hs"], m["winner"] == m["home"])}{side(m["away"], m["acode"], m["as_"], m["winner"] == m["away"])}'
            f'<small>{esc(C.short_date(m["date"]))}{esc(note)}</small></div>')


def build_wc():
    d = 1
    w = S["wc2026"]; f = w["final"]["row"]; ts = w["scorers"][0]
    br = "".join(f'<div class="gf-bracket-col"><h3>{esc(r["round"])}</h3><div class="gf-ties">{"".join(tie(m, r["round"] == "Final") for m in r["matches"])}</div></div>' for r in w["bracket"])
    groups = []
    for g, t in w["groups"].items():
        rows = "".join(f'<tr><td class="pos">{r["pos"]}</td><th scope="row" class="team"><span class="name">{esc(r["name"])}</span><span class="code">{esc(r["code"])}</span>{THROUGH if r["through"] else ""}</th><td>{r["p"]}</td><td>{r["w"]}</td><td>{r["d"]}</td><td>{r["l"]}</td><td>{r["gd"]:+d}</td><td class="pts">{r["pts"]}</td></tr>'.replace("+0<", "0<") for r in t)
        groups.append(f'<div class="gf-group"><h3>Group {esc(g)}</h3><div class="gf-table-wrap" tabindex="0" role="region" aria-label="Group {esc(g)} table"><table class="gf-table"><thead><tr><th scope="col" class="pos">#</th><th scope="col" class="team l">Team</th><th scope="col">P</th><th scope="col">W</th><th scope="col">D</th><th scope="col">L</th><th scope="col">GD</th><th scope="col">Pts</th></tr></thead><tbody>{rows}</tbody></table></div></div>')
    sc = w["scorers"][:10]
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Tournament review · complete</p><h1>World Cup 2026</h1><p>Canada, Mexico and the United States, {esc(C.nice_date("2026-06-11", False))} to {esc(C.nice_date("2026-07-19"))}: the first 48-team World Cup, all {w["matches"]} matches.</p></div>
<section class="gf-band" aria-labelledby="ch-h"><div class="gf-band-grid"><div><p class="gf-kicker">Final · after extra time</p><h2 id="ch-h" class="gf-display" style="font-size:clamp(30px,6vw,48px);margin-bottom:12px">{esc(w["champion"])} win the World Cup</h2>
<div class="gf-scoreline"><span class="team">{esc(f["home"])}</span><span class="score">{f["hs"]}–{f["as_"]}</span><span class="team">{esc(f["away"])}</span></div>
<p style="margin-top:12px"><a class="gf-btn" href="final.html">Match centre</a></p></div>
<div class="gf-stats-row" style="grid-template-columns:repeat(2,minmax(0,1fr))"><div class="gf-stat"><span class="n">{w["goals"]}</span><span class="what">goals</span><span class="ctx">{w["gpg"]:.2f} per game</span></div><div class="gf-stat"><span class="n">{w["extra_time"]}</span><span class="what">extra times</span><span class="ctx">{w["shootouts"]} shoot-outs</span></div><div class="gf-stat"><span class="n">{ts["goals"]}</span><span class="what">{esc(ts["name"])}</span><span class="ctx">top scorer, {esc(ts["team"])}</span></div><div class="gf-stat"><span class="n">{w["attendance"]["avg"]:,}</span><span class="what">average crowd</span><span class="ctx">{w["owngoals"]} own goals · {w["pens_scored"]} penalties</span></div></div></div></section>
<section class="gf-section" aria-labelledby="ko-h"><div class="gf-section-head"><h2 id="ko-h">The knockout rounds</h2></div><div class="gf-bracket">{br}</div>
<p class="gf-note">Third place: {esc(w["third"]["home"])} {w["third"]["hs"]}–{w["third"]["as_"]} {esc(w["third"]["away"])}, {esc(C.nice_date(w["third"]["date"], False))} — the highest-scoring match of the tournament.</p></section>
<section class="gf-section" aria-labelledby="gs-h"><div class="gf-section-head"><h2 id="gs-h">Goals</h2><a href="../articles/how-spain-won-the-world-cup.html">How Spain won it</a></div>
<div class="gf-grid gf-grid--2">{chart("wc-stages")}{figure("Top scorers", "Own goals excluded; penalties counted.", bars([(s["name"], s["team"], s["goals"], "hi" if i == 0 else "") for i, s in enumerate(sc)]), SRC + " Names as the source records them.", "wcscorers", simple_table(["Player", "Team", "Goals", "Penalties"], [[s["name"], s["team"], s["goals"], s["pens"]] for s in sc], "Top scorers"))}</div></section>
<section class="gf-section" aria-labelledby="gr-h"><div class="gf-section-head"><h2 id="gr-h">The groups</h2></div><p class="gf-meta">✓ reached the round of 32 (the top two in each group and the eight best third-placed teams). Ordered by points, goal difference, goals scored; FIFA’s full tie-breakers are not applied here.</p><div class="gf-groups">{"".join(groups)}</div></section>"""
    page("world-cup-2026/index.html", "World Cup 2026 in numbers — gameformative", "The 2026 World Cup, all 104 matches: the bracket, the groups, top scorers and the final.", None, body, d, later=True)


def build_final():
    d = 1
    w = S["wc2026"]; F = w["final"]; f = F["row"]
    tl = "".join(f'<li class="{e["kind"]}"><span class="min">{esc(e["minute"])}′</span><span class="ev"><span class="tag">{"Goal" if e["kind"] == "goal" else "Sub"}</span><b>{esc(e["name"])}</b> · {esc(e["team"])}</span></li>' for e in F["timeline"])
    def lineup(side):
        ol = "".join(f"<li>{esc(p['name'])}{' (c)' if p['captain'] else ''}</li>" for p in side["starters"])
        subs = "; ".join(f"{s['on']} for {s['off']} {s['minute']}′" for s in side["subs"])
        return f'<div class="gf-card"><h3 style="font-size:20px;font-stretch:85%;margin-bottom:8px">{esc(side["team"])}</h3><ol>{ol}</ol><p class="gf-meta" style="margin:8px 0 0">Substitutions: {esc(subs)}.</p></div>'
    lu = "".join(lineup(side) for side in F["lineups"])
    ld = {"@context": "https://schema.org", "@type": "SportsEvent", "name": "World Cup 2026 Final: Spain v Argentina", "startDate": f["date"], "sport": "Football",
          "location": {"@type": "Place", "name": F["ground"]}, "homeTeam": {"@type": "SportsTeam", "name": f["home"]}, "awayTeam": {"@type": "SportsTeam", "name": f["away"]}}
    body = f"""<p class="gf-meta"><a href="index.html">World Cup 2026</a> › Final</p>
<div class="gf-matchhead"><p class="gf-meta" style="margin:0">Final · {esc(C.nice_date(f["date"]))} · {esc(F["ground"])} · attendance {F["attendance"]:,}</p>
<h1 class="gf-sr">World Cup 2026 final: {esc(f["home"])} {f["hs"]}, {esc(f["away"])} {f["as_"]}, after extra time</h1>
<div class="row" aria-hidden="true"><span class="tm" style="text-align:right">{esc(f["home"])}</span><span class="sc">{f["hs"]}–{f["as_"]}</span><span class="tm" style="text-align:left">{esc(f["away"])}</span></div>
<span class="how">After extra time</span><p class="gf-meta" style="margin:10px 0 0">Half-time {F["ht"][0]}–{F["ht"][1]} · 90 minutes {F["ft"][0]}–{F["ft"][1]} · extra time {F["et"][0]}–{F["et"][1]}</p></div>
<div class="gf-article-layout" style="margin-top:24px"><div>
<section aria-labelledby="km-h"><div class="gf-section-head"><h2 id="km-h">Key moments</h2></div><ol class="gf-timeline">{tl}</ol></section>
<section class="gf-section" aria-labelledby="lu-h"><div class="gf-section-head"><h2 id="lu-h">Line-ups</h2></div><div class="gf-lineups">{lu}</div></section></div>
<aside class="gf-rail" aria-label="Match statistics"><div class="gf-inert"><h3>Match statistics</h3><p style="margin:0">Possession, shots, xG and passes come from a licensed event-data provider on the live site. The prototype’s public-domain source records goals, line-ups, substitutions and attendance — shown here in full — and nothing is estimated.</p></div>
<div class="gf-card"><h3 style="font-size:18px;font-stretch:85%;margin-bottom:6px">The road to the final</h3>{"".join(f'<p style="margin:0 0 6px;font-size:14.5px"><b>{esc(r["round"])}</b> · {esc(r["home"])} {r["hs"]}–{r["as_"]} {esc(r["away"])}{" (aet)" if r["how"] == "aet" else ""}</p>' for r in w["results"] if "Spain" in (r["home"], r["away"]) and not r["group"] and r["round"] != "Final")}</div>
<a class="gf-btn gf-btn--ghost" href="../articles/how-spain-won-the-world-cup.html">How Spain won the World Cup</a></aside></div>"""
    page("world-cup-2026/final.html", "Spain 1–0 Argentina (aet): World Cup 2026 final, match centre — gameformative", "Match centre for the 2026 World Cup final: key moments, line-ups and substitutions.", None, body, d, jsonld=ld, later=True)


def source_list(items, kind, depth=1):
    li = []
    for s in items:
        date = f", {esc(s['date'])}" if s.get("date") else ""
        k = K.CATALOGUE[s["url"]]
        li.append(f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a><span class="pub"> — {esc(s["publisher"])}{date}</span>'
                  f'<span class="why">{esc(s["note"])}</span>'
                  f'<a class="gf-catlink" href="{up(depth)}sources/index.html#src-{k["id"]}">{esc(K.TYPES[k["type"]][0])} · catalogue entry<span class="gf-sr">: {esc(k["title"])}</span></a></li>')
    return f'<ol class="gf-source-list" data-sources="{kind}">{"".join(li)}</ol>'


def check_rules(a):
    """The owner's house rules — the build stops on any breach (check.py measures the same on the page)."""
    n = C.body_chars(a); R = C.RULES
    assert R["min_chars"] <= n <= R["max_chars"], f"{a['slug']}: {n} characters, outside {R['min_chars']}–{R['max_chars']}"
    assert len(a["segments"]) >= R["min_segments"], f"{a['slug']}: {len(a['segments'])} segments, needs {R['min_segments']}"
    assert all(h for h, _ in a["segments"]), f"{a['slug']}: a segment without a heading"
    assert a["sources_used"] and a["sources_investigated"], f"{a['slug']}: both source lists are required"
    assert a["desk"] in C.DESK, f"{a['slug']}: desk {a['desk']!r} is not one of the eight"
    for s in a["sources_used"] + a["sources_investigated"]:
        assert s["url"].startswith("https://") and s["title"] and s["publisher"] and s["note"], f"{a['slug']}: incomplete source {s}"
        assert s["url"] in K.CATALOGUE, f"{a['slug']}: {s['url']} has no entry in catalogue.py"
    for s in a["sources_used"]:
        assert not K.CATALOGUE[s["url"]]["checked"][1].startswith("Not read"), f"{a['slug']}: cites as used a source we could not read: {s['url']}"


def build_article(a):
    d = 1
    check_rules(a)
    blocks = []
    for i, (h, items) in enumerate(a["segments"], 1):
        inner = "".join(chart(x[1]) if isinstance(x, tuple) else f"<p data-count>{esc(x)}</p>" for x in items)
        blocks.append(f'<section class="gf-seg-block" aria-labelledby="s{i}"><h2 id="s{i}">{esc(h)}</h2>{inner}</section>')
    toc = "".join(f'<li><a href="#s{i}">{esc(h)}</a></li>' for i, (h, _) in enumerate(a["segments"], 1))
    others = [x for x in ARTICLES if x is not a]
    same = [x for x in others if x["desk"] == a["desk"]]
    rail = "".join(story_card(x, d, "h3") for x in (same + [x for x in others if x not in same])[:2])
    n = C.body_chars(a)
    origin = ("From the editorial desk’s draft; checked against its sources before publishing." if a["origin"] == "owner"
              else "Written by the data desk. Every figure is computed from public-domain match records by the site’s own converter; nothing is estimated.")
    url = abs_url(f"articles/{a['slug']}.html")
    org = {"@type": "Organization", "name": "gameformative", "url": SITE_URL, "logo": {"@type": "ImageObject", "url": SITE_URL + "assets/icons/icon-512.png", "width": 512, "height": 512}}
    ld = [{"@context": "https://schema.org", "@type": "NewsArticle", "headline": a["title"], "description": excerpt(a),
           "datePublished": C.SITE["published_iso"], "dateModified": C.SITE["published_iso"], "mainEntityOfPage": url, "url": url,
           "image": [SITE_URL + f"assets/share/{a['slug']}.png"], "inLanguage": "en-GB",
           "articleSection": C.DESK[a["desk"]]["name"], "keywords": [C.DESK[a["desk"]]["name"], C.TOPIC[a["topic"]]["name"]],
           "wordCount": len(" ".join(x for _, items in a["segments"] for x in items if isinstance(x, str)).split()),
           "author": {"@type": "Organization", "name": a["byline"], "url": SITE_URL + "how-we-count/index.html"}, "publisher": org,
           "citation": [{"@type": "ScholarlyArticle" if K.CATALOGUE[s["url"]]["type"] == "research" else "CreativeWork", "name": K.CATALOGUE[s["url"]]["title"], "url": s["url"],
                         **({"identifier": "https://doi.org/" + K.CATALOGUE[s["url"]]["doi"]} if K.CATALOGUE[s["url"]].get("doi") else {})} for s in a["sources_used"]]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
              {"@type": "ListItem", "position": 2, "name": C.DESK[a["desk"]]["name"], "item": abs_url(f"desks/{a['desk']}.html")},
              {"@type": "ListItem", "position": 3, "name": a["title"], "item": url}]}]
    share = share_bar(url, a["title"])
    sf = f'<p class="dek" data-count>{esc(a["standfirst"])}</p>' if a["standfirst"] else ""
    body = f"""<div class="gf-article-layout"><article class="gf-article" data-article data-desk="{a["desk"]}" data-min="{C.RULES["min_chars"]}" data-max="{C.RULES["max_chars"]}" data-segments="{C.RULES["min_segments"]}">
<header class="gf-article-head"><p class="gf-cardmeta">{desk_link(a, d)} · {esc(a["kind"])} · <span class="gf-subject">Subject: {topic_link(a, d)}</span></p><p class="gf-deskline">{esc(C.DESK[a["desk"]]["name"])} — {esc(C.DESK[a["desk"]]["does"])}</p><h1>{esc(a["title"])}</h1>{sf}
<div class="gf-byline"><span>By <b>{esc(a["byline"])}</b></span><span>{esc(C.SITE["published"])}</span><span>{reading(a)}</span><span>{len(a["segments"])} segments</span></div>{share}</header>
<nav class="gf-toc-box" aria-label="In this article"><h2 class="gf-kicker">In this article</h2><ol>{toc}</ol></nav>
<div class="gf-body">{"".join(blocks)}</div>
<section class="gf-sources" aria-labelledby="src-h"><h2 id="src-h">Sources</h2>
<h3>Sources used</h3>{source_list(a["sources_used"], "used")}
<h3>Sources investigated but not used</h3>{source_list(a["sources_investigated"], "investigated")}
<p class="gf-meta">Links checked on {esc(C.SITE["published"])}. {esc(origin)} Body text: {n:,} characters. Found an error? <a href="../how-we-count/index.html#corrections">Our corrections policy</a>.</p></section>
</article>
<aside class="gf-rail" aria-label="More to read"><h2 class="gf-kicker">More to read</h2>{rail}</aside></div>"""
    og = dict(type="article", title=a["title"], image=f"assets/share/{a['slug']}.png", image_alt=f"{C.DESK[a['desk']]['name']} · {a['title']}",
              published=C.SITE["published_iso"], section=C.DESK[a["desk"]]["name"], tag=C.TOPIC[a["topic"]]["name"])
    page(f"articles/{a['slug']}.html", f"{a['title']} — gameformative", excerpt(a), "Latest", body, d, jsonld=ld, desk=a["desk"], og=og)


def share_bar(url, title):
    """Plain share links — no third-party widgets, no tracking; the native share sheet where the
    browser has one (docs/15-discoverability.md §4)."""
    u, tt = quote(url, safe=""), quote(title, safe="")
    links = [("WhatsApp", f"https://wa.me/?text={tt}%20{u}"), ("Telegram", f"https://t.me/share/url?url={u}&text={tt}"),
             ("X", f"https://x.com/intent/post?url={u}&text={tt}"), ("LinkedIn", f"https://www.linkedin.com/sharing/share-offsite/?url={u}"),
             ("Facebook", f"https://www.facebook.com/sharer/sharer.php?u={u}"), ("Email", f"mailto:?subject={tt}&body={u}")]
    a = "".join(f'<a class="gf-share-link" href="{esc(h)}" rel="noopener" target="_blank">{n}<span class="gf-sr"> — share this article</span></a>' for n, h in links)
    return (f'<div class="gf-share" data-share data-url="{esc(url)}" data-title="{esc(title)}"><span class="gf-share-label">Share</span>'
            f'<button class="gf-share-link" type="button" data-share-native hidden>Share…</button>{a}'
            f'<button class="gf-share-link" type="button" data-copy>Copy link</button><span class="gf-sr" aria-live="polite" data-share-status></span></div>')


def list_item(a, depth, hidden=False):
    return (f'<article class="gf-list-item"{" data-more hidden" if hidden else ""}><a class="gf-card-link" href="{up(depth)}articles/{a["slug"]}.html">{cover(a["cover"], a["title"])}'
            f'<span class="body"><span class="gf-cardmeta">{meta(a)}</span><h2>{esc(a["title"])}</h2>'
            f'<p style="margin:0;color:var(--gf-muted)">{esc(excerpt(a))}</p><span class="gf-meta">{esc(C.SITE["published"])} · {reading(a)}</span></span></a></article>')


def build_articles_index():
    d = 1
    SHOW = 5
    li = "".join(list_item(a, d, n >= SHOW) for n, a in enumerate(ARTICLES))
    more = '<button class="gf-btn gf-btn--quiet gf-loadmore" type="button" data-loadmore="4">Load more</button>' if len(ARTICLES) > SHOW else ""
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Latest</p><h1>All articles</h1><p>News, research, tactics and the business of sport — explained. Every article ends with the sources we used and the sources we investigated but did not use.</p></div>
<div class="gf-list">{li}</div>{more}"""
    page("articles/index.html", "Latest articles — gameformative", "The latest gameformative articles across every topic.", "Latest", body, d)


def empty_panel(what):
    return (f'<div class="gf-inert"><h2 style="font-size:20px;margin-bottom:6px">No {esc(what)} articles published yet</h2>'
            f'<p style="margin:0">Every article published here follows the same rules: {C.RULES["min_chars"]:,}–{C.RULES["max_chars"]:,} characters, '
            f'at least {C.RULES["min_segments"]} headed segments, and the sources used and investigated listed at the end.</p></div>')


def build_desks():
    d = 1
    for s, n, does in C.DESKS:
        arts = [a for a in ARTICLES if a["desk"] == s]
        inner = f'<div class="gf-list">{"".join(list_item(a, d) for a in arts)}</div>' if arts else empty_panel(n + " desk")
        others = "".join(f'<li><a href="{x}.html">{esc(m)}</a></li>' for x, m, _ in C.DESKS if x != s)
        body = f"""<div class="gf-pagehead"><p class="gf-kicker"><a href="index.html">The desks</a></p><h1>{esc(n)}</h1><p class="gf-deskdoes">{esc(does)}</p></div>
{inner}
<section class="gf-section" aria-labelledby="ot-h"><div class="gf-section-head"><h2 id="ot-h">The other desks</h2></div><ul class="gf-toc">{others}</ul></section>"""
        page(f"desks/{s}.html", f"{n} — gameformative", does, "Desks", body, d, desk=s)
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">The desks</p><h1>Eight desks, one job each</h1><p>Every gameformative article sits on one desk, chosen by what it does for you — whatever the sport or subject.</p></div>
<ul class="gf-topic-grid gf-desk-grid">{desk_tiles(d, "")}</ul>
<p class="gf-meta" style="margin-top:18px">Looking for a subject instead — sport science, sponsorship, sport tech? <a href="../topics/index.html">All subjects</a>.</p>"""
    page("desks/index.html", "The desks — gameformative", "The eight gameformative desks: Discover, Define, Design, Develop, Data, Drive, Defend, Deal.", "Desks", body, d)


def build_topics():
    """Subjects: the owner's round-2 topic list, now the subject tag on each article (the desks are the
    sections). The pages were live, so they stay — as subject pages."""
    d = 1
    tiles = []
    for s, n, b in C.TOPICS:
        arts = [a for a in ARTICLES if a["topic"] == s]
        tiles.append(f'<li><a class="gf-topic-tile" href="{s}.html"><span class="n">{esc(n)}</span><span class="b">{esc(b)}</span><span class="c">{len(arts)} article{"s" if len(arts) != 1 else ""}{"" if arts else " · none published yet"}</span></a></li>')
        inner = f'<div class="gf-list">{"".join(list_item(a, d) for a in arts)}</div>' if arts else empty_panel(n.lower())
        others = "".join(f'<li><a href="{x}.html">{esc(m)}</a></li>' for x, m, _ in C.TOPICS if x != s)
        body = f"""<div class="gf-pagehead"><p class="gf-kicker"><a href="index.html">Subjects</a></p><h1>{esc(n)}</h1><p>{esc(b)}</p></div>
{inner}
<section class="gf-section" aria-labelledby="ot-h"><div class="gf-section-head"><h2 id="ot-h">Other subjects</h2></div><ul class="gf-toc">{others}</ul></section>"""
        page(f"topics/{s}.html", f"{n} — gameformative", b, None, body, d)
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Subjects</p><h1>What we write about</h1><p>The subjects gameformative covers, from the research lab to the sponsor’s balance sheet. The site is organised by <a href="../desks/index.html">desk</a> — what an article does for you; each article is also tagged with its subject.</p></div>
<ul class="gf-topic-grid">{"".join(tiles)}</ul>"""
    page("topics/index.html", "Subjects — gameformative", "Every gameformative subject: news, sport science, tactics, analytics, data, tech, development, fans, sponsorship and goods.", None, body, d)


def build_catalogue():
    """The source catalogue: every source any article cites or consulted, grouped by type, each with
    how we checked it and the articles that use it (docs/16-source-catalogue.md)."""
    d = 1
    used, consulted = {}, {}
    for a in ARTICLES:
        for s in a["sources_used"]: used.setdefault(s["url"], []).append(a)
        for s in a["sources_investigated"]: consulted.setdefault(s["url"], []).append(a)
    entries = {u: k for u, k in K.CATALOGUE.items() if u in used or u in consulted}
    unused = [k["id"] for u, k in K.CATALOGUE.items() if u not in entries]
    assert not unused, f"catalogue entries no article uses: {unused}"
    def art_links(lst):
        return ", ".join(f'<a href="../articles/{a["slug"]}.html">{esc(a["title"])}</a>' for a in lst)
    sections, counts = [], {}
    for tkey, (tlabel, tdesc) in K.TYPES.items():
        items = sorted(((u, k) for u, k in entries.items() if k["type"] == tkey), key=lambda x: (x[1]["publisher"], x[1]["title"]))
        counts[tkey] = len(items)
        if not items: continue
        cards = []
        for u, k in items:
            bits = [esc(k["publisher"])] + ([esc(k["issue"])] if k.get("issue") else []) + ([C.nice_date(k["date"]) if len(k["date"]) == 10 else esc(k["date"])] if k.get("date") else [])
            doi = f' · DOI <a href="https://doi.org/{esc(k["doi"])}" rel="noopener">{esc(k["doi"])}</a>' if k.get("doi") else ""
            lic = f'<p class="lic">Licence: {esc(k["licence"])}</p>' if k.get("licence") else ""
            role = []
            if u in used: role.append(f'<p class="role"><b>Cited in:</b> {art_links(used[u])}</p>')
            if u in consulted: role.append(f'<p class="role"><b>Consulted, not cited, for:</b> {art_links(consulted[u])}</p>')
            cards.append(f'<article class="gf-src" id="src-{k["id"]}"><h3><a href="{esc(u)}" rel="noopener">{esc(k["title"])}</a></h3>'
                         f'<p class="meta">{" · ".join(bits)}{doi}</p>{lic}'
                         f'<p class="check"><b>Checked {esc(C.nice_date(k["checked"][0]))}:</b> {esc(k["checked"][1])}</p>{"".join(role)}</article>')
        sections.append(f'<section class="gf-section" aria-labelledby="t-{tkey}"><div class="gf-section-head"><h2 id="t-{tkey}">{esc(tlabel)}</h2><span class="gf-meta">{len(items)}</span></div>'
                        f'<p class="gf-meta" style="margin:-6px 0 12px">{esc(tdesc)}</p><div class="gf-src-list">{"".join(cards)}</div></section>')
    pubs = {}
    for u, k in entries.items(): pubs.setdefault(k["publisher"], []).append(k["id"])
    publist = "".join(f'<li><a href="#src-{ids[0]}">{esc(p)}</a> <span class="gf-meta">{len(ids)}</span></li>' for p, ids in sorted(pubs.items(), key=lambda x: x[0].lower()))
    n_cited = sum(1 for u in entries if u in used)
    toc = "".join(f'<li><a href="#t-{t}">{esc(K.TYPES[t][0])} ({n})</a></li>' for t, n in counts.items() if n)
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Sources</p><h1>The source catalogue</h1><p>Every source our articles cite or consulted — what kind of source it is, who publishes it, exactly how we checked it, and the articles that use it. {len(entries)} sources from {len(pubs)} publishers; {n_cited} cited, the rest consulted and set aside with a reason.</p></div>
<ul class="gf-toc">{toc}<li><a href="#publishers">Publishers</a></li></ul>
{"".join(sections)}
<section class="gf-section" aria-labelledby="publishers"><div class="gf-section-head"><h2 id="publishers">Publishers and institutions</h2></div><ul class="gf-publist">{publist}</ul>
<p class="gf-meta">How we choose and check sources: <a href="../how-we-count/index.html#sources">How we source</a>.</p></section>"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "The gameformative source catalogue", "url": SITE_URL + "sources/index.html",
          "mainEntity": {"@type": "ItemList", "numberOfItems": len(entries), "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "item": {"@type": "ScholarlyArticle" if k["type"] == "research" else "CreativeWork", "name": k["title"], "url": u,
               "publisher": {"@type": "Organization", "name": k["publisher"]}, **({"identifier": f"https://doi.org/{k['doi']}"} if k.get("doi") else {})}}
              for i, (u, k) in enumerate(sorted(entries.items(), key=lambda x: x[1]["id"]))]}}
    page("sources/index.html", "The source catalogue — gameformative", "Every source gameformative articles cite or consulted: type, publisher, how we checked it, and the articles that use it.", "Sources", body, d, jsonld=ld)


def build_redirects():
    """The articles lived under /analysis/ until 2026-09-25 (live then) — never delete a live URL."""
    moved = [(f"analysis/{a['slug']}.html", f"../articles/{a['slug']}.html", a["title"]) for a in ARTICLES if a["origin"] == "data"]
    moved.append(("analysis/index.html", "../articles/index.html", "All articles"))
    for old, new, title in moved:
        OUT[old] = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Moved: {esc(title)} — gameformative</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{new}"><meta http-equiv="refresh" content="0; url={new}"></head>
<body><div class="proto-banner">Prototype — gameformative.com, 2026.</div><h1>This page has moved</h1><p><a href="{new}">{esc(title)}</a></p></body>
</html>
"""


def build_method():
    d = 1
    gl = "".join(f"<dt>{esc(t)}</dt><dd>{esc(x)}</dd>" for t, x in C.GLOSSARY)
    R = C.RULES
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">How we work</p><h1>Our standards</h1><p>What gameformative publishes, how every article is built and sourced, how we label, automate and correct — and what our numbers mean.</p></div>
<ul class="gf-toc"><li><a href="#desks">Desks</a></li><li><a href="#rules">Article rules</a></li><li><a href="#sources">How we source</a></li><li><a href="#labels">Labels</a></li><li><a href="#automation">Automation and AI</a></li><li><a href="#corrections">Corrections</a></li><li><a href="#data">Data</a></li><li><a href="#glossary">Glossary</a></li><li><a href="#accessibility">Accessibility</a></li></ul>
<div class="gf-prose">
<h2 id="desks">The eight desks</h2>
<p>gameformative is organised by what an article does for you. Every article sits on exactly one desk.</p>
<div class="gf-table-wrap" tabindex="0" role="region" aria-label="The eight desks"><table class="gf-table gf-desk-table"><thead><tr><th scope="col" class="l">Desk</th><th scope="col" class="l">What the article does for the reader</th></tr></thead><tbody>{"".join(f'<tr><th scope="row" class="l"><a href="../desks/{s}.html">{esc(n)}</a></th><td class="l">{esc(does)}</td></tr>' for s, n, does in C.DESKS)}</tbody></table></div>
<h2 id="rules">Article rules</h2>
<p>Whatever its desk, every article follows three rules.</p>
<dl><dt>Length</dt><dd>{R["min_chars"]:,} to {R["max_chars"]:,} characters of body text — the standfirst and every paragraph, spaces included. Headline, segment headings, charts and the source lists are not counted. Long enough to explain, short enough to finish.</dd>
<dt>Segments</dt><dd>At least {R["min_segments"]} segments, each under its own heading, listed at the top of the article so you can jump to the part you need.</dd>
<dt>Sources</dt><dd>Two lists close every article: the sources used, and the sources investigated but not used — each with a line on why.</dd></dl>
<h2 id="sources">How we source</h2>
<p>We read the source itself — the paper, the dataset, the report — not a summary of it. We list what we used so you can check us, and what we looked at and set aside so you can see what we chose not to rely on and why. Links are checked on the day of publication. Where a publisher blocks us from reading a source, we say so rather than cite it unread. Every source — used or set aside — has an entry in the <a href="../sources/index.html">source catalogue</a>: what kind of source it is, who publishes it, and how we checked it.</p>
<h2 id="labels">Labels we use</h2><dl><dt>Explainer</dt><dd>How something works and how to read it.</dd><dt>Analysis</dt><dd>Reporting that interprets evidence or data.</dd><dt>News</dt><dd>What happened, sourced and dated.</dd><dt>Automated</dt><dd>Text a template fills from data, published without a human edit — always labelled, only ever stating computed facts. Used on the data pages only.</dd><dt>Opinion</dt><dd>Reserved for signed columns; none are published yet.</dd></dl>
<h2 id="automation">Automation and AI</h2><p>The “in numbers” round-ups on the data pages are written by a fixed template, not a language model, and carry the <b>Automated</b> label. If gameformative publishes text generated by an AI system, it says so on the piece unless an editor has reviewed it and a named person takes editorial responsibility — the standard set by Article 50 of the EU AI Act, applicable from 2 August 2026. AI-generated or manipulated images or video are always labelled. No image on this site is AI-generated.</p>
<h2 id="corrections">Corrections</h2><p>When we get something wrong we correct it promptly, say on the page what was wrong and when it changed, and list the change on a public corrections page. The corrections page and the reporting form open with the live site; in the prototype this section states the policy.</p>
<h2 id="data">Data</h2><p>The data articles and the data pages (a later phase) use <a href="https://github.com/openfootball">openfootball</a>’s results, dedicated to the public domain under CC0 1.0. The site’s converter checks every file — goals for equal goals against, points reconcile, two files for one competition agree match by match — and refuses to publish a table that does not add up. Results are recorded to {esc(DATA_TO)}. Shots, possession, expected goals and live events need a licensed provider; where a figure would need them, the page says so instead of estimating it. Tables are ordered by points, goal difference, goals scored, then name; official tie-breakers differ by competition.</p>
<h2 id="glossary">Glossary</h2><dl>{gl}</dl>
<h2 id="accessibility">Accessibility</h2><p>Every chart has a text alternative and its numbers as a table; colour never carries meaning alone; text meets WCAG 2.2 AA contrast in the light and dark themes; every control is at least 44 pixels square on a phone; motion follows the system’s reduced-motion setting.</p>
</div>"""
    page("how-we-count/index.html", "How we work: our standards — gameformative", "gameformative's article rules, sourcing, labels, automation and AI policy, corrections and glossary.", "How we work", body, d)


def build_styleguide():
    d = 1
    toks = [("--gf-ground", "Ground"), ("--gf-surface", "Surface"), ("--gf-sunk", "Sunk"), ("--gf-ink", "Ink"), ("--gf-text", "Text"), ("--gf-muted", "Muted"), ("--gf-line", "Line"),
            ("--gf-blue", "Form Blue — brand, links"), ("--gf-orange", "Energy Orange — accent"), ("--gf-draw", "Neutral chip"), ("--gf-band", "Band")]
    sw = "".join(f'<div class="gf-swatch"><i style="background:var({t})"></i><div><b>{esc(n)}</b><br><code>{t}</code></div></div>' for t, n in toks)
    a = ARTICLES[0]
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Design system · v2</p><h1>gameformative style guide</h1><p>The tokens and components every page is built from, live. Switch the theme to see both palettes.</p></div>
<section class="gf-section" aria-labelledby="c-h"><div class="gf-section-head"><h2 id="c-h">Colour</h2></div><div class="gf-swatches">{sw}</div></section>
<section class="gf-section" aria-labelledby="t-h"><div class="gf-section-head"><h2 id="t-h">Type — Archivo, one variable family</h2></div>
<p class="gf-display" style="font-size:56px;line-height:1;color:var(--gf-ink);margin-bottom:8px">Display 72% width · 800</p>
<p style="font-size:26px;font-stretch:85%;font-weight:750;color:var(--gf-ink)">Card headline 85% · 750</p><p style="font-size:18px">Body 100% · 400 — tabular numerals: 1,045 · 2.33 · 3,200</p><p class="gf-kicker">Kicker · 800 · tracked caps</p></section>
<section class="gf-section" aria-labelledby="k-h"><div class="gf-section-head"><h2 id="k-h">Labels and buttons</h2></div>
<p style="display:flex;gap:8px;flex-wrap:wrap">{label("Analysis")}{label("Explainer")}<span class="gf-label gf-label--automated">Automated</span><span class="gf-label gf-label--data">Season review</span></p>
<p style="display:flex;gap:10px;flex-wrap:wrap"><a class="gf-btn" href="#k-h">Primary</a><a class="gf-btn gf-btn--ghost" href="#k-h">Secondary</a><a class="gf-btn gf-btn--quiet" href="#k-h">Quiet</a><a class="gf-btn gf-btn--quiet is-unavailable" href="#k-h" aria-disabled="true" onclick="return false" title="Inert controls look like this">Inert</a></p></section>
<section class="gf-section" aria-labelledby="s-h"><div class="gf-section-head"><h2 id="s-h">Story card, desk tile</h2></div>
<div class="gf-grid gf-grid--3">{story_card(ARTICLES[0], d)}{story_card(ARTICLES[2], d)}<ul class="gf-topic-grid gf-desk-grid" style="grid-template-columns:1fr">{desk_tiles(d).split("</li>")[1]}</li></ul></div></section>
<section class="gf-section" aria-labelledby="src-h"><div class="gf-section-head"><h2 id="src-h">The source lists</h2></div><div class="gf-sources" style="margin-top:0"><h3>Sources used</h3>{source_list(a["sources_used"][:1], "used")}<h3>Sources investigated but not used</h3>{source_list(a["sources_investigated"][:1], "investigated")}</div></section>
<section class="gf-section" aria-labelledby="ch-h"><div class="gf-section-head"><h2 id="ch-h">Charts</h2></div><div class="gf-grid gf-grid--2">{chart("gpg-big5")}{chart("minutes-2526")}</div></section>"""
    page("styleguide/index.html", "Style guide — gameformative", "The gameformative design system: tokens and components, live.", None, body, d)


def indexable():
    """The pages that belong in search: the article site. The style guide, the later-phase data pages
    and the redirects are left out (docs/15-discoverability.md §3)."""
    pages = ["index.html", "articles/index.html", "desks/index.html", "topics/index.html", "sources/index.html", "how-we-count/index.html"]
    pages += [f"articles/{a['slug']}.html" for a in ARTICLES] + [f"desks/{s}.html" for s, _, _ in C.DESKS] + [f"topics/{s}.html" for s, _, _ in C.TOPICS]
    return pages


def build_discovery():
    """sitemap.xml, feed.xml (RSS 2.0), robots.txt, llms.txt, manifest.webmanifest — generated, so the
    gate can check they reproduce. In production they sit at the domain root."""
    iso = C.SITE["published_iso"]
    urls = "".join(f"  <url><loc>{esc(abs_url(p))}</loc><lastmod>{iso}</lastmod></url>\n" for p in indexable())
    OUT["sitemap.xml"] = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    rfc = "Fri, 25 Sep 2026 08:00:00 +0000"  # the prototype's publication date; production uses each article's own
    items = "".join(f"""  <item>
    <title>{esc(a["title"])}</title>
    <link>{esc(abs_url(f"articles/{a['slug']}.html"))}</link>
    <guid isPermaLink="true">{esc(abs_url(f"articles/{a['slug']}.html"))}</guid>
    <pubDate>{rfc}</pubDate>
    <category>{esc(C.DESK[a["desk"]]["name"])}</category>
    <description>{esc(excerpt(a))}</description>
  </item>
""" for a in ARTICLES)
    OUT["feed.xml"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>gameformative — latest articles</title>
  <link>{esc(SITE_URL)}</link>
  <atom:link href="{esc(SITE_URL)}feed.xml" rel="self" type="application/rss+xml"/>
  <description>{esc(C.SITE["description"])}</description>
  <language>en-gb</language>
  <lastBuildDate>{rfc}</lastBuildDate>
{items}</channel>
</rss>
"""
    OUT["robots.txt"] = f"""# gameformative — robots.txt
# The prototype's copy; in production this file is served from the domain root, where crawlers read it.
# The AI-crawler section follows docs/15-discoverability.md §1 and the owner's decision (ask A12).
User-agent: *
Allow: /

Sitemap: {SITE_URL}sitemap.xml
"""
    arts = "".join(f"- [{a['title']}]({abs_url('articles/' + a['slug'] + '.html')}): {C.DESK[a['desk']]['name']} desk. {excerpt(a)}\n" for a in ARTICLES)
    desks = "".join(f"- [{n}]({abs_url('desks/' + s + '.html')}): {d}\n" for s, n, d in C.DESKS)
    OUT["llms.txt"] = f"""# gameformative

> {C.SITE["description"]} Every article is 800–3,200 characters in headed segments and ends with two source lists: the sources used and the sources investigated but not used.

The site is organised in eight desks, each defined by what an article does for the reader. Every cited source has an entry in the source catalogue saying what kind of source it is and how it was checked.

## Articles

{arts}
## Desks

{desks}
## Standards and sources

- [How we work]({abs_url("how-we-count/index.html")}): the desks, the article rules, how we source, labels, automation and AI, corrections.
- [Source catalogue]({abs_url("sources/index.html")}): every source cited or consulted, with its type, publisher and how it was checked.
- [RSS feed]({SITE_URL}feed.xml): the latest articles.
"""
    OUT["manifest.webmanifest"] = json.dumps({"name": "gameformative", "short_name": "gameformative", "description": C.SITE["description"],
        "start_url": "./", "scope": "./", "display": "browser", "background_color": "#F7F6F2", "theme_color": "#0C1222",
        "icons": [{"src": "assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "assets/icons/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=1, ensure_ascii=False) + "\n"


def build_all():
    build_home(); build_articles_index(); build_desks(); build_topics(); build_catalogue(); build_method(); build_styleguide()
    build_discovery()
    for a in ARTICLES: build_article(a)
    build_redirects()
    # the data pages — a later phase, kept live and linked from the footer
    build_scores(); build_stats_hub()
    for l in LEAGUES: build_league(l)
    build_pl2526(); build_wc(); build_final()



if __name__ == "__main__":
    build_all()
    if "--check" in sys.argv:
        bad = [p for p, t in OUT.items() if not (HERE / p).exists() or (HERE / p).read_text(encoding="utf-8") != t]
        print(f"{len(OUT)} pages regenerated in memory; {len(bad)} differ from the committed files")
        for b in bad: print("  differs:", b)
        sys.exit(1 if bad else 0)
    for p, t in OUT.items():
        f = HERE / p; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(t, encoding="utf-8")
        print(f"{p:52s} {len(t.encode()):7,d} bytes")
