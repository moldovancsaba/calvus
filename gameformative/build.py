#!/usr/bin/env python3
"""Generate the gameformative prototype:  python3 gameformative/build.py   (--check: compare only)
Reads content.py (copy) and data/stats.json (every figure, computed by data/convert.py) and writes
every page. No dependencies. --check regenerates in memory and fails if a committed page differs, so
a hand edit to a generated page cannot survive the gate."""
import json, pathlib, sys, html as H
import content as C

HERE = pathlib.Path(__file__).parent
S = json.loads((HERE / "data" / "stats.json").read_text(encoding="utf-8"))
V = "9"  # asset version — bump when tokens.css, site.css or site.js change
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap">'
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
        "left": '<path d="M15 5l-7 7 7 7"/>', "right": '<path d="M9 5l7 7-7 7"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths[name]}</svg>'


MARK = ('<svg class="gf-brand-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect width="32" height="32" rx="8" fill="#1F47E0"/>'
        '<path d="M6 21.5 11.5 16l4.5 3.5L25.5 9" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="25.5" cy="9" r="3" fill="#FF8A3D"/></svg>')


def brand(depth):
    return f'<a class="gf-brand" href="{up(depth)}index.html" aria-label="gameformative home">{MARK}<span class="gf-brand-word">game<b>formative</b></span></a>'


# ------------------------------------------------------------------ chrome
def banner():
    return (f'<div class="proto-banner"><strong>Prototype — gameformative.com, 2026.</strong> Results, tables and the World Cup are real data '
            f'(openfootball, public domain) to {DATA_TO}; the articles are sample editorial copy with every figure computed from that data. '
            'Search, sign-in and the newsletter are shown but not built.</div>')


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


def strip(depth):
    chips = []
    for l in LEAGUES:
        for m in l["latest"]:
            hw, aw = (m["hs"] > m["as_"]), (m["as_"] > m["hs"])
            chips.append(f'<a class="gf-chip-match" href="{up(depth)}stats/{l["slug"]}.html#results" aria-label="{esc(l["name"])}: {esc(m["hname"])} {m["hs"]}, {esc(m["aname"])} {m["as_"]}, full time">'
                         f'<span class="lg">{esc(l["name"])} · FT</span>'
                         f'<span class="t {"win" if hw else "lose" if aw else ""}">{esc(m["hcode"])}</span><span class="s">{m["hs"]}</span>'
                         f'<span class="t {"win" if aw else "lose" if hw else ""}">{esc(m["acode"])}</span><span class="s">{m["as_"]}</span></a>')
    return f"""<section class="gf-strip" data-strip aria-label="Latest results"><div class="gf-wrap gf-strip-row">
  <p class="gf-strip-label" style="margin:0"><b>Latest</b>results to {esc(C.short_date(S["data_to"]))}</p>
  <div class="gf-strip-scroll" tabindex="0" aria-label="Latest results, scroll sideways">{"".join(chips)}</div>
  <div class="gf-strip-btns"><button class="gf-icon-btn" type="button" data-strip-dir="-1" aria-label="Scroll results back">{icon("left")}</button><button class="gf-icon-btn" type="button" data-strip-dir="1" aria-label="Scroll results forward">{icon("right")}</button></div>
</div></section>"""


def tabbar(current, depth):
    ic = {"Home": "home", "Scores": "scores", "Tables & stats": "stats", "Analysis": "analysis"}
    items = []
    for label, href, short in C.NAV:
        if label not in C.TABBAR: continue
        items.append(f'<li><a href="{up(depth)}{href}"' + (' aria-current="page"' if label == current else "") + f'>{icon(ic[label])}<span>{esc(short)}</span></a></li>')
    items.append(f'<li><button type="button" data-sheet-open aria-expanded="false" aria-controls="gf-more"' + (' aria-current="page"' if current in ("World Cup 2026", "How we count") else "") + f'>{icon("more")}<span>More</span></button></li>')
    return f'<nav class="gf-tabbar" aria-label="Sections"><ul>{"".join(items)}</ul></nav>'


def sheet(depth):
    links = "".join(f'<li><a href="{up(depth)}{href}">{esc(label)}</a></li>' for label, href, _ in C.NAV)
    leagues = "".join(f'<li><a href="{up(depth)}stats/{l["slug"]}.html">{esc(l["name"])}</a></li>' for l in LEAGUES)
    return f"""<div class="gf-sheet" id="gf-more" hidden role="dialog" aria-modal="true" aria-labelledby="gf-more-h"><div class="gf-sheet-panel">
  <div class="gf-sheet-head"><h2 id="gf-more-h">More</h2><button class="gf-icon-btn" type="button" data-sheet-close aria-label="Close">{icon("close")}</button></div>
  <ul>{links}</ul>
  <h2 class="gf-kicker" style="margin-top:18px">Leagues</h2>
  <ul>{leagues}</ul>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px">
    <button class="gf-btn gf-btn--quiet" type="button" data-theme-toggle aria-pressed="false">{icon("theme")} Theme</button>
    <a class="gf-btn gf-btn--quiet is-unavailable" href="#" aria-disabled="true" title="Accounts are not built in the prototype" onclick="return false">Sign in</a>
  </div>
</div></div>"""


def footer(depth):
    u = up(depth)
    sec = "".join(f'<li><a href="{u}{href}">{esc(label)}</a></li>' for label, href, _ in C.NAV[1:])
    lg = "".join(f'<li><a href="{u}stats/{l["slug"]}.html">{esc(l["name"])}</a></li>' for l in LEAGUES)
    std = "".join(f'<li><a href="{u}how-we-count/index.html#{a}">{t}</a></li>' for a, t in (("glossary", "Glossary"), ("data", "Where the data comes from"), ("corrections", "Corrections"), ("automation", "Automation and AI"), ("labels", "Labels we use")))
    return f"""<footer class="gf-footer"><div class="gf-wrap">
  <div class="gf-footer-grid">
    <div class="about">{brand(depth)}<p style="margin-top:8px">{esc(C.SITE["tagline"])} Results and tables from openfootball, public-domain data (CC0 1.0).</p></div>
    <div><h2>Sections</h2><ul>{sec}</ul></div>
    <div><h2>Leagues</h2><ul>{lg}</ul></div>
    <div><h2>Standards</h2><ul>{std}</ul></div>
  </div>
  <div class="gf-footer-bottom"><span>© 2026 gameformative.com</span><span>Data to {esc(DATA_TO)}</span></div>
</div></footer>"""


def page(path, title, desc, current, body, depth, jsonld=None, show_strip=True):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    html_out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#F7F6F2" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0B0F1A" media="(prefers-color-scheme: dark)">
<script>try{{var t=localStorage.getItem("gf-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
{FONTS}
<link rel="stylesheet" href="{up(depth)}assets/tokens.css?v={V}">
<link rel="stylesheet" href="{up(depth)}assets/site.css?v={V}">
{ld}
</head>
<body>
{banner()}
{header(current, depth)}
{strip(depth) if show_strip else ""}
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
    return f'<span class="gf-cover">{svg}</svg></span>'


THROUGH = ' <span class="gf-through" title="Reached the round of 32">✓</span>'


def data_label(kind):
    return f'<span class="gf-label gf-label--data">{esc(kind)}</span>'


def label(kind):
    return f'<span class="gf-label{" gf-label--explainer" if kind == "Explainer" else ""}">{esc(kind)}</span>'


def story_card(a, depth, h="h3"):
    return (f'<a class="gf-story-card" href="{up(depth)}analysis/{a["slug"]}.html">{cover(a["cover"], a["title"])}'
            f'<span class="body">{label(a["kind"])}<{h}>{esc(a["title"])}</{h}><p>{esc(a["dek"])}</p><span class="gf-meta">{esc(C.SITE["published"])}</span></span></a>')


def snapshot(l, depth, n=5):
    li = "".join(f'<li><span class="p">{r["pos"]}</span><span class="t">{esc(r["name"])}</span>{form(r["form"][-3:])}<span class="pts">{r["pts"]}</span></li>' for r in l["table"][:n])
    return (f'<section class="gf-snap" aria-labelledby="snap-{l["id"]}"><div class="gf-snap-head"><h3 id="snap-{l["id"]}">{esc(l["name"])}</h3>'
            f'<a href="{up(depth)}stats/{l["slug"]}.html">Full table<span class="gf-sr"> — {esc(l["name"])}</span></a></div>'
            f'<p class="gf-meta" style="padding:6px 14px 0;margin:0">After matchday {l["rounds_done"]} · last three results · points</p><ol>{li}</ol></section>')


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
def build_home():
    d = 0
    lead = ARTICLES[0]
    side = snapshot(LG["en"], d, 6)
    ex = ARTICLES[4]
    explainer = (f'<a class="gf-card" href="analysis/{ex["slug"]}.html" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:8px">{label(ex["kind"])}'
                 f'<span style="font-size:19px;font-weight:750;font-stretch:85%;color:var(--gf-ink);line-height:1.15">{esc(ex["title"])}</span><span class="gf-meta">{esc(ex["dek"])}</span></a>')
    def tile(n):
        unit = f"<small>{esc(n['unit'])}</small>" if n["unit"] else ""
        acc = " gf-stat--accent" if n.get("accent") else ""
        return f'<a class="gf-stat{acc}" href="{n["href"]}" style="text-decoration:none"><span class="n">{esc(n["n"])}{unit}</span><span class="what">{esc(n["what"])}</span><span class="ctx">{esc(n["ctx"])}</span></a>'
    nums = "".join(tile(n) for n in C.numbers(S))
    cards = "".join(story_card(a, d) for a in ARTICLES[1:4])
    snaps = "".join(snapshot(l, d) for l in LEAGUES[1:])
    w = S["wc2026"]; f = w["final"]["row"]; ts = w["scorers"][0]
    wc = f"""<section class="gf-section gf-band" aria-labelledby="wc-h"><div class="gf-band-grid">
  <div><p class="gf-kicker">World Cup 2026 · in review</p><h2 id="wc-h" class="gf-display" style="font-size:clamp(30px,6vw,48px);margin-bottom:12px">{esc(w["champion"])} are world champions</h2>
    <div class="gf-scoreline"><span class="team">{esc(f["home"])}</span><span class="score">{f["hs"]}–{f["as_"]}</span><span class="team">{esc(f["away"])}</span></div>
    <p style="margin-top:12px">After extra time, {esc(C.nice_date(f["date"]))}, {esc(w["final"]["ground"])}.</p>
    <p style="display:flex;gap:10px;flex-wrap:wrap"><a class="gf-btn" href="world-cup-2026/index.html">The tournament in numbers</a><a class="gf-btn gf-btn--ghost" style="color:#9DB0FF;border-color:#9DB0FF" href="world-cup-2026/final.html">Match centre: the final</a></p></div>
  <div class="gf-stats-row" style="grid-template-columns:repeat(2,minmax(0,1fr))">
    <div class="gf-stat"><span class="n">{w["goals"]}</span><span class="what">goals</span><span class="ctx">in {w["matches"]} matches</span></div>
    <div class="gf-stat"><span class="n">{w["gpg"]:.2f}</span><span class="what">per game</span><span class="ctx">{w["extra_time"]} went to extra time</span></div>
    <div class="gf-stat"><span class="n">{ts["goals"]}</span><span class="what">{esc(ts["name"])}</span><span class="ctx">top scorer, {esc(ts["team"])}</span></div>
    <div class="gf-stat"><span class="n">{w["attendance"]["avg"]:,}</span><span class="what">average crowd</span><span class="ctx">{w["attendance"]["total"]:,} in total</span></div>
  </div></div></section>"""
    roundups = "".join(roundup(l).replace("{UP}", up(d)) for l in LEAGUES[:3])
    body = f"""<h1 class="gf-sr">gameformative — football, explained by the numbers</h1>
<div class="gf-lead">
  <a class="gf-lead-story" href="analysis/{lead["slug"]}.html">{cover(lead["cover"], lead["title"])}
    <span style="display:block;margin-top:14px">{label(lead["kind"])}</span>
    <h2>{esc(lead["title"])}</h2><p>{esc(lead["dek"])}</p><span class="gf-meta">{esc(C.SITE["byline"])} · {esc(C.SITE["published"])}</span></a>
  <aside class="gf-rail" aria-label="Premier League table and explainer">{side}{explainer}</aside>
</div>
<section class="gf-section" aria-labelledby="num-h"><div class="gf-section-head"><h2 id="num-h">The numbers this week</h2><a href="stats/index.html">All stats</a></div><div class="gf-stats-row">{nums}</div></section>
<section class="gf-section" aria-labelledby="an-h"><div class="gf-section-head"><h2 id="an-h">Analysis</h2><a href="analysis/index.html">More analysis</a></div><div class="gf-grid gf-grid--3">{cards}</div></section>
<section class="gf-section" aria-labelledby="lg-h"><div class="gf-section-head"><h2 id="lg-h">Across Europe</h2><a href="stats/index.html">Tables & stats</a></div><div class="gf-grid gf-grid--4">{snaps}</div></section>
{wc}
<section class="gf-section" aria-labelledby="ru-h"><div class="gf-section-head"><h2 id="ru-h">The round in numbers</h2><a href="scores/index.html">All results</a></div><div class="gf-grid gf-grid--3">{roundups}</div></section>
<section class="gf-section gf-band" aria-labelledby="nl-h"><div class="gf-band-grid"><div><p class="gf-kicker">Newsletter</p><h2 id="nl-h" class="gf-display" style="font-size:clamp(26px,5vw,38px)">The Monday numbers</h2><p>The weekend’s results, what changed in the tables, one chart that explains it. Once a week.</p></div>
<form class="gf-signup" onsubmit="return false" aria-describedby="nl-note"><label class="gf-sr" for="nl-email">E-mail address</label><input id="nl-email" type="email" placeholder="you@example.com" disabled><button class="gf-btn is-unavailable" type="submit" aria-disabled="true" title="The newsletter is not built in the prototype">Subscribe</button><p id="nl-note" class="gf-meta" style="grid-column:1/-1;margin:0">Not built in the prototype — nothing is collected. Consent and sender are set before launch.</p></form></div></section>"""
    page("index.html", "gameformative — football, explained by the numbers", C.SITE["description"], "Home", body, d,
         jsonld={"@context": "https://schema.org", "@type": "WebSite", "name": "gameformative", "url": "https://gameformative.com/", "description": C.SITE["description"]})


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
    page("scores/index.html", "Results and fixtures — gameformative", "Latest results and next fixtures in the Premier League, LaLiga, Bundesliga, Serie A and Ligue 1.", "Scores", body, d)


def build_stats_hub():
    d = 1
    rows = "".join(f'<li><a class="gf-card" style="display:grid;grid-template-columns:1fr auto;gap:6px 12px;text-decoration:none;color:inherit" href="{l["slug"]}.html"><span><b style="font-size:20px;color:var(--gf-ink)">{esc(l["name"])}</b><br><span class="gf-meta">{esc(l["country"])} · matchday {l["rounds_done"]} · leader {esc(l["table"][0]["name"])} ({l["table"][0]["pts"]} pts)</span></span><span class="gf-stat" style="border:0;padding:0;text-align:right"><span class="n" style="font-size:34px">{l["agg"]["gpg"]:.2f}</span><span class="ctx">goals / game</span></span></a></li>' for l in LEAGUES)
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Tables & stats</p><h1>Europe’s big five, 2026/27</h1><p>Full tables with home and away splits, form, points per game and the points race for each league — and the five compared. Every figure is computed from the recorded results to {esc(DATA_TO)}.</p></div>
<ul class="gf-grid gf-grid--2" style="list-style:none;margin:0;padding:0">{rows}</ul>
<section class="gf-section" aria-labelledby="cmp-h"><div class="gf-section-head"><h2 id="cmp-h">The five compared</h2><a href="../analysis/big-five-first-month.html">Read the analysis</a></div>
<div class="gf-grid gf-grid--2">{chart("gpg-big5")}{chart("outcomes-big5")}</div></section>
<section class="gf-section" aria-labelledby="arc-h"><div class="gf-section-head"><h2 id="arc-h">Season reviews</h2></div>
<div class="gf-grid gf-grid--2"><a class="gf-card" href="premier-league-2025-26.html" style="text-decoration:none;color:inherit"><span class="gf-label gf-label--data">Complete season</span><h3 style="font-size:24px;font-stretch:85%;margin:8px 0 4px">Premier League 2025/26</h3><p class="gf-meta" style="margin:0">Final table, the points race over 38 matchdays, top scorers, goals by minute, attendances.</p></a>
<a class="gf-card" href="../world-cup-2026/index.html" style="text-decoration:none;color:inherit"><span class="gf-label gf-label--data">Complete tournament</span><h3 style="font-size:24px;font-stretch:85%;margin:8px 0 4px">World Cup 2026</h3><p class="gf-meta" style="margin:0">All 104 matches: groups, the bracket, scorers and the final.</p></a></div></section>"""
    page("stats/index.html", "Tables & stats — gameformative", "Tables, form and statistics for Europe's big five football leagues, 2026/27.", "Tables & stats", body, d)


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
<div class="gf-table-foot"><span class="gf-key"><i class="top"></i>Top four</span><span class="gf-key"><i class="bottom"></i>Bottom three</span><span>Form: oldest left · W won · D drawn · L lost</span><span>Tap a column heading to sort</span><span>Tie order is the site’s own; <a href="../how-we-count/index.html#tables">official tie-breakers differ</a></span></div></section>
<section class="gf-section" aria-labelledby="r-h"><div class="gf-section-head"><h2 id="r-h">Form and leaders</h2></div>
<div class="gf-grid gf-grid--2">{race_figure(l, "race")}
<div class="gf-grid">{figure("Team leaders", "Across all matches so far.", bars([(best_att["name"], "most goals scored", best_att["gf"], "hi"), (best_def["name"], "fewest conceded", best_def["ga"], ""), (home_best["name"], f"best at home · {home_best['home']['w']}W {home_best['home']['d']}D {home_best['home']['l']}L", home_best["home"]["pts"], ""), (away_best["name"], f"best away · {away_best['away']['w']}W {away_best['away']['d']}D {away_best['away']['l']}L", away_best["away"]["pts"], "")], fmt=lambda v: str(v)), SRC + " Values: goals, goals, home points, away points.", "leaders")}
{figure("Clean sheets", "Matches without conceding.", bars([(r["name"], "", r["cs"], "hi" if i == 0 else "") for i, r in enumerate(cs)]), SRC, "cleansheets")}</div></div></section>
<section class="gf-section" id="results" aria-labelledby="res-h"><div class="gf-section-head"><h2 id="res-h">Matchday {l["rounds_done"]} results</h2><a href="../scores/index.html">All leagues</a></div>
<div class="gf-grid gf-grid--2"><div>{results_list(l["latest"])}</div><div>{roundup(l).replace("{UP}", up(d))}<h3 class="gf-kicker" style="margin-top:18px">Next fixtures · as scheduled</h3>{results_list(l["upcoming"][:5], fixtures=True)}</div></div></section>
<div class="gf-inert" style="margin-top:28px"><h3>Expected goals, shots and player ratings</h3><p style="margin:0">Shown on the live site from a licensed event-data provider (shot-level data: xG, shots, possession, player ratings). The prototype’s public-domain source carries results only, so these panels are not filled — and never estimated.</p></div>"""
    page(f"stats/{l['slug']}.html", f"{l['name']} table and stats 2026/27 — gameformative", f"{l['name']} 2026/27: table, home and away, form, points per game, points race and results.", "Tables & stats", body, d)


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
<section class="gf-section" aria-labelledby="rc-h"><div class="gf-section-head"><h2 id="rc-h">How it was won</h2><a href="../analysis/premier-league-five-matchdays-in.html">Five matchdays in, this season</a></div><div class="gf-grid gf-grid--2">{race}{chart("after5-2526")}</div></section>
<section class="gf-section" aria-labelledby="gl-h"><div class="gf-section-head"><h2 id="gl-h">Goals</h2><a href="../analysis/premier-league-2025-26-goals-by-minute.html">Read the analysis</a></div><div class="gf-grid gf-grid--2">{chart("minutes-2526")}{chart("scorers-2526")}</div>
<p class="gf-note">Largest crowd: {att["top"]["n"]:,} at {esc(att["top"]["ground"])}, {esc(att["top"]["home"])} v {esc(att["top"]["away"])}, {esc(C.nice_date(att["top"]["date"]))}. {p["pens"]} penalties scored and {p["owngoals"]} own goals across the season.</p></section>"""
    page("stats/premier-league-2025-26.html", "Premier League 2025/26 season review — gameformative", "The complete 2025/26 Premier League: final table, title race, top scorers, goals by minute and attendances.", "Tables & stats", body, d)


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
<section class="gf-section" aria-labelledby="gs-h"><div class="gf-section-head"><h2 id="gs-h">Goals</h2><a href="../analysis/how-spain-won-the-world-cup.html">How Spain won it</a></div>
<div class="gf-grid gf-grid--2">{chart("wc-stages")}{figure("Top scorers", "Own goals excluded; penalties counted.", bars([(s["name"], s["team"], s["goals"], "hi" if i == 0 else "") for i, s in enumerate(sc)]), SRC + " Names as the source records them.", "wcscorers", simple_table(["Player", "Team", "Goals", "Penalties"], [[s["name"], s["team"], s["goals"], s["pens"]] for s in sc], "Top scorers"))}</div></section>
<section class="gf-section" aria-labelledby="gr-h"><div class="gf-section-head"><h2 id="gr-h">The groups</h2></div><p class="gf-meta">✓ reached the round of 32 (the top two in each group and the eight best third-placed teams). Ordered by points, goal difference, goals scored; FIFA’s full tie-breakers are not applied here.</p><div class="gf-groups">{"".join(groups)}</div></section>"""
    page("world-cup-2026/index.html", "World Cup 2026 in numbers — gameformative", "The 2026 World Cup, all 104 matches: the bracket, the groups, top scorers and the final.", "World Cup 2026", body, d)


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
<a class="gf-btn gf-btn--ghost" href="../analysis/how-spain-won-the-world-cup.html">How Spain won the World Cup</a></aside></div>"""
    page("world-cup-2026/final.html", "Spain 1–0 Argentina (aet): World Cup 2026 final, match centre — gameformative", "Match centre for the 2026 World Cup final: key moments, line-ups and substitutions.", "World Cup 2026", body, d, jsonld=ld)


def build_article(a):
    d = 1
    blocks = []
    for b in a["body"]:
        if isinstance(b, tuple): blocks.append(chart(b[1]))
        elif b.startswith("## "): blocks.append(f"<h2>{esc(b[3:])}</h2>")
        else: blocks.append(f"<p>{esc(b)}</p>")
    kf = "".join(f"<li>{esc(k)}</li>" for k in a["keyfacts"])
    others = [x for x in ARTICLES if x is not a][:3]
    rail = "".join(story_card(x, d, "h3") for x in others[:2])
    related = {"en": "../stats/premier-league.html", "all": "../stats/index.html", "wc": "../world-cup-2026/index.html"}[a["league"]]
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": a["title"], "description": a["dek"], "datePublished": C.SITE["published_iso"],
          "author": {"@type": "Organization", "name": C.SITE["byline"]}, "publisher": {"@type": "Organization", "name": "gameformative"},
          "isBasedOn": "https://github.com/openfootball"}
    body = f"""<div class="gf-article-layout"><article class="gf-article">
<header class="gf-article-head">{label(a["kind"])}<h1>{esc(a["title"])}</h1><p class="dek">{esc(a["dek"])}</p>
<div class="gf-byline"><span>By <b>{esc(C.SITE["byline"])}</b></span><span>{esc(C.SITE["published"])}</span><span>Data to {esc(DATA_TO)}</span></div></header>
<section class="gf-keyfacts" aria-labelledby="kf-h"><h2 id="kf-h">Key numbers</h2><ul>{kf}</ul></section>
<div class="gf-body">{"".join(blocks)}</div>
<aside class="gf-transparency" aria-label="How this article was made"><p style="margin:0"><b>How this was made.</b> Written by the gameformative data desk. Every figure is computed from openfootball’s public-domain match records by the site’s own converter; nothing is estimated or taken from another publication. Found an error? <a href="../how-we-count/index.html#corrections">Our corrections policy</a>.</p></aside>
<p style="margin-top:20px"><a class="gf-btn gf-btn--ghost" href="{related}">See the full numbers</a></p>
</article>
<aside class="gf-rail" aria-label="More analysis"><h2 class="gf-kicker">More analysis</h2>{rail}</aside></div>"""
    page(f"analysis/{a['slug']}.html", f"{a['title']} — gameformative", a["dek"], "Analysis", body, d, jsonld=ld)


def build_analysis_index():
    d = 1
    extra = [dict(href="../stats/premier-league-2025-26.html", kind="Season review", title="Premier League 2025/26, the complete season", dek="Final table, the title race over 38 matchdays, top scorers, goals by minute and attendances.", cover=dict(type="minutes")),
             dict(href="../world-cup-2026/index.html", kind="Tournament review", title="World Cup 2026 in numbers", dek="The bracket, the twelve groups, the scorers and the final.", cover=dict(type="final"))]
    items = [dict(href=f"{a['slug']}.html", kind=a["kind"], title=a["title"], dek=a["dek"], cover=a["cover"]) for a in ARTICLES] + extra
    SHOW = 5
    li = "".join(f'<a class="gf-list-item" href="{i["href"]}"{" data-more hidden" if n >= SHOW else ""}>{cover(i["cover"], i["title"])}<span class="body">{label(i["kind"]) if i["kind"] in ("Analysis", "Explainer") else data_label(i["kind"])}<h2>{esc(i["title"])}</h2><p style="margin:0;color:var(--gf-muted)">{esc(i["dek"])}</p><span class="gf-meta">{esc(C.SITE["published"])}</span></span></a>' for n, i in enumerate(items))
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Analysis</p><h1>The numbers behind the game</h1><p>Analysis and explainers from the data desk. Every figure is computed from the recorded results; each piece says what the data can and cannot show.</p></div>
<div class="gf-list">{li}</div>
<button class="gf-btn gf-btn--quiet gf-loadmore" type="button" data-loadmore="4">Load more</button>"""
    page("analysis/index.html", "Analysis — gameformative", "Football analysis and explainers built on the numbers.", "Analysis", body, d)


def build_method():
    d = 1
    gl = "".join(f"<dt>{esc(t)}</dt><dd>{esc(x)}</dd>" for t, x in C.GLOSSARY)
    inputs = "".join(f"<li><code>{esc(k)}</code></li>" for k in S["inputs"])
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">How we count</p><h1>Method, glossary and standards</h1><p>What every number on gameformative means, where it comes from, what the data cannot show, and how we label, automate and correct.</p></div>
<ul class="gf-toc"><li><a href="#glossary">Glossary</a></li><li><a href="#data">Data</a></li><li><a href="#tables">Tables</a></li><li><a href="#labels">Labels</a></li><li><a href="#automation">Automation and AI</a></li><li><a href="#corrections">Corrections</a></li><li><a href="#accessibility">Accessibility</a></li></ul>
<div class="gf-prose">
<h2 id="glossary">Glossary</h2><dl>{gl}</dl>
<h2 id="data">Where the data comes from</h2>
<p>Results, goals, line-ups, substitutions and attendances come from <a href="https://github.com/openfootball">openfootball</a>, a volunteer-maintained football data project whose files are dedicated to the public domain under CC0 1.0 — free to use with no restrictions. The files used for this edition:</p><ul>{inputs}</ul>
<p>The site’s converter reads those files, checks them (every table’s goals for equal its goals against; points reconcile with results; where the source has two files for the same competition they agree match by match; every goal list matches its score) and refuses to publish if a check fails. Results are recorded to {esc(DATA_TO)}. The source records them by hand, so a result can appear a few days after the match; we show the date the data runs to on every page.</p>
<p>What the source does not carry, we do not show: shots, possession, expected goals (xG), player ratings and live minute-by-minute events need a licensed provider. Those panels are marked in place, and nothing is estimated to fill them.</p>
<h2 id="tables">How tables are ordered</h2><p>Points, then goal difference, then goals scored, then name. That is our rule on every table. Official tie-breakers differ — LaLiga and Serie A use head-to-head results first; FIFA’s group rules add further steps — so for teams level on points an official table can differ from ours. Home and away tables count only those matches.</p>
<h2 id="labels">Labels we use</h2><dl><dt>Analysis</dt><dd>Reporting that interprets the numbers, written and checked by the data desk.</dd><dt>Explainer</dt><dd>How a measure works and how to read it.</dd><dt>Automated</dt><dd>Text a template fills from the match data, published without a human edit. Always labelled, always factual, never a quote or an opinion.</dd><dt>Season review · Tournament review</dt><dd>Complete competitions, every figure final.</dd><dt>Opinion</dt><dd>Reserved for signed columns; none are published yet.</dd></dl>
<h2 id="automation">Automation and AI</h2><p>The “in numbers” round-ups are written by a fixed template from the results, not by a language model, and carry the <b>Automated</b> label. If gameformative ever publishes text generated by an AI system, it will say so on the piece unless an editor has reviewed it and a named person takes editorial responsibility — the standard set by Article 50 of the EU AI Act, applicable from 2 August 2026. AI-generated or manipulated images or video are always labelled. No image on this site is AI-generated.</p>
<h2 id="corrections">Corrections</h2><p>When we get something wrong we correct it promptly, say on the page what was wrong and when it changed, and list the change on a public corrections page. Data errors in the source are reported upstream to openfootball as well as corrected here. The corrections page and the reporting form open with the live site; in the prototype this section states the policy.</p>
<h2 id="accessibility">Accessibility</h2><p>Every chart has a text alternative and its numbers as a table; colour never carries meaning alone (form guides print the letter; outcome bars print H, D and A); text meets WCAG 2.2 AA contrast in the light and dark themes; every control is at least 44 pixels square on a phone; motion follows the system’s reduced-motion setting.</p>
</div>"""
    page("how-we-count/index.html", "How we count: method, glossary and standards — gameformative", "What every number on gameformative means, where the data comes from, and how we label, automate and correct.", "How we count", body, d)


def build_styleguide():
    d = 1
    toks = [("--gf-ground", "Ground"), ("--gf-surface", "Surface"), ("--gf-sunk", "Sunk"), ("--gf-ink", "Ink"), ("--gf-text", "Text"), ("--gf-muted", "Muted"), ("--gf-line", "Line"),
            ("--gf-blue", "Form Blue — brand, links, W"), ("--gf-orange", "Energy Orange — accent, L"), ("--gf-draw", "Draw grey — D"), ("--gf-band", "Band")]
    sw = "".join(f'<div class="gf-swatch"><i style="background:var({t})"></i><div><b>{esc(n)}</b><br><code>{t}</code></div></div>' for t, n in toks)
    l = LG["en"]
    body = f"""<div class="gf-pagehead"><p class="gf-kicker">Design system · v1</p><h1>gameformative style guide</h1><p>The tokens and components every page is built from, live. Switch the theme to see both palettes. Reasoning and sources: the project’s design document.</p></div>
<section class="gf-section" aria-labelledby="c-h"><div class="gf-section-head"><h2 id="c-h">Colour</h2></div><div class="gf-swatches">{sw}</div></section>
<section class="gf-section" aria-labelledby="t-h"><div class="gf-section-head"><h2 id="t-h">Type — Archivo, one variable family</h2></div>
<p class="gf-display" style="font-size:56px;line-height:1;color:var(--gf-ink);margin-bottom:8px">Display 72% width · 800</p>
<p style="font-size:26px;font-stretch:85%;font-weight:750;color:var(--gf-ink)">Card headline 85% · 750</p><p style="font-size:18px">Body 100% · 400 — tabular numerals everywhere: 1,045 · 2.75 · 41,643</p><p class="gf-kicker">Kicker · 800 · tracked caps</p></section>
<section class="gf-section" aria-labelledby="k-h"><div class="gf-section-head"><h2 id="k-h">Labels, buttons, form</h2></div>
<p style="display:flex;gap:8px;flex-wrap:wrap">{label("Analysis")}{label("Explainer")}<span class="gf-label gf-label--automated">Automated</span><span class="gf-label gf-label--data">Season review</span></p>
<p style="display:flex;gap:10px;flex-wrap:wrap"><a class="gf-btn" href="#k-h">Primary</a><a class="gf-btn gf-btn--ghost" href="#k-h">Secondary</a><a class="gf-btn gf-btn--quiet" href="#k-h">Quiet</a><a class="gf-btn gf-btn--quiet is-unavailable" href="#k-h" aria-disabled="true" onclick="return false" title="Inert controls look like this">Inert</a></p>
<p>{form(l["table"][0]["form"])} {form(l["table"][-1]["form"])}</p></section>
<section class="gf-section" aria-labelledby="s-h"><div class="gf-section-head"><h2 id="s-h">Stat tiles, snapshot, story card</h2></div>
<div class="gf-grid gf-grid--3"><div class="gf-stat gf-stat--accent"><span class="n">3.81</span><span class="what">goals per game</span><span class="ctx">Stat tile with accent</span></div>{snapshot(l, d, 4)}{story_card(ARTICLES[1], d)}</div></section>
<section class="gf-section" aria-labelledby="ch-h"><div class="gf-section-head"><h2 id="ch-h">Charts</h2></div><div class="gf-grid gf-grid--2">{chart("gpg-big5")}{chart("minutes-2526")}</div></section>
<section class="gf-section" aria-labelledby="tb-h"><div class="gf-section-head"><h2 id="tb-h">Table</h2></div><div data-views><div class="gf-seg gf-seg--xs" role="group" aria-label="Table columns"><button type="button" class="gf-xs-toggle" data-cols aria-pressed="false">All columns</button></div>{league_table(l, "all", tid="sg")}</div><p class="gf-sr" aria-live="polite" id="sg-live"></p></section>"""
    page("styleguide/index.html", "Style guide — gameformative", "The gameformative design system: tokens and components, live.", None, body, d)


def build_all():
    build_home(); build_scores(); build_stats_hub()
    for l in LEAGUES: build_league(l)
    build_pl2526(); build_wc(); build_final()
    for a in ARTICLES: build_article(a)
    build_analysis_index(); build_method(); build_styleguide()


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
