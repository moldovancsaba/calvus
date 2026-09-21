#!/usr/bin/env python3
"""Generate the Népszabadság prototype from one content source (content.py).
Run: python3 nepszabadsag/build.py — writes index.html, belfold/index.html,
cikk/<slug>.html, nepszava/index.html, regisztracio/index.html. No dependencies."""
import pathlib, html as htmlmod
import content as C

HERE = pathlib.Path(__file__).parent
CSS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;600;700;800&display=swap">'


def esc(s):
    return htmlmod.escape(s) if s else ""


def img(slug, css_class="", sizes=""):
    """Real photo, resized locally; credit carried in the alt/figcaption pattern used
    across the site — every image here is CC-licensed or public-domain, per content.py."""
    meta = C.IMAGES[slug]
    rel = f"../assets/img/{meta['file']}" if _DEPTH else f"assets/img/{meta['file']}"
    return f'<img src="{rel}" alt="{esc(meta["alt"])}" loading="lazy" class="{css_class}">'


def photo_credit(slug):
    meta = C.IMAGES[slug]
    note = f" — {meta['note']}" if meta.get("note") else ""
    return f'Fotó: {esc(meta["credit"])} ({meta["license"]}){note}'


def author_link(key):
    a = C.AUTHORS[key]
    return a["name"]


def ad_slot(w, h):
    cls = f"ad-{w}x{h}"
    return f'<div class="ad-slot {cls}"><span><span class="ad-label">Hirdetés</span>{w} × {h}</span></div>'


# Only Belföld and Népszava have a built page in this v1; Sport and Tudomány share the
# home page's combined "Külföld · Sport · Tudomány" anchor rather than each getting one.
NAV_ANCHOR = {"Belföld": None, "Külföld": "külföld", "Gazdaság": "gazdaság",
              "Kultúra": "kultúra", "Sport": "külföld", "Tudomány": "külföld", "Népszava": None}
NAV_PAGE = {"Belföld": "belfold/index.html", "Népszava": "nepszava/index.html"}


def nav_href(n, up):
    if n in NAV_PAGE:
        return f"{up}{NAV_PAGE[n]}"
    return f"{up}index.html#{NAV_ANCHOR[n]}"


def nav_list(current, up):
    return "".join(
        f'<li><a href="{nav_href(n, up)}"' + (' aria-current="page"' if n == current else "") + f'>{n}</a></li>'
        for n in C.NAV
    )


def header(current, depth):
    up = "../" * depth
    nav_items = nav_list(current, up)
    home = f"{up}index.html" if depth else "index.html"
    return f"""<header class="site-header">
  <div class="header-top">
    <a class="brand" href="{home}"><span class="brand-mark">N</span><span class="brand-word">NÉPSZABADSÁG</span></a>
    <div class="header-actions">
      <button class="icon-btn hamburger" aria-expanded="false" aria-controls="mobilenav" onclick="document.getElementById('mobilenav').hidden=!document.getElementById('mobilenav').hidden;this.setAttribute('aria-expanded',!document.getElementById('mobilenav').hidden)" aria-label="Menü">☰</button>
      <nav class="main-nav" aria-label="Fő navigáció"><ul>{nav_items}</ul></nav>
      <button class="icon-btn" aria-label="Keresés" title="Keresés (nem működik a prototípusban)">🔍</button>
      <a class="btn-subscribe" href="{up}regisztracio/index.html">Előfizetés</a>
    </div>
  </div>
  <nav class="mobile-nav" id="mobilenav" hidden aria-label="Mobil navigáció"><ul>{nav_items}</ul></nav>
</header>"""


def article_pills(pills):
    return '<div class="article-pills">' + "".join(f'<span class="pill pill-static">{esc(p)}</span>' for p in pills) + "</div>"


def footer(depth):
    up = "../" * depth
    rovatok = "".join(f'<li><a href="{nav_href(n, up)}">{esc(n)}</a></li>' for n in C.FOOTER_ROVATOK)
    almarka = "".join(f'<li><a href="{up}nepszava/index.html">{esc(i)}</a></li>' for i in C.FOOTER_ALMARKA)
    laprol = "".join(f'<li><a href="{up}index.html">{esc(i)}</a></li>' for i in C.FOOTER_LAPROL)
    jogi = "".join(f'<li><a href="{up}index.html">{esc(i)}</a></li>' for i in C.FOOTER_JOGI)
    return f"""<footer class="site-footer">
  <div class="footer-cols">
    <div><h5>Rovatok</h5><ul>{rovatok}</ul></div>
    <div><h5>Almárka</h5><ul>{almarka}</ul></div>
    <div><h5>A lapról</h5><ul>{laprol}</ul></div>
    <div><h5>Jogi és egyéb</h5><ul>{jogi}</ul></div>
  </div>
  <div class="footer-bottom wrap">{C.COPYRIGHT}</div>
</footer>"""


def reg_band(depth=0):
    up = "../" * depth
    return f"""<div class="reg-band"><div class="wrap">
  <p>{esc(C.REGISTRATION_BAND['text'])}</p>
  <a class="btn-lime" href="{up}regisztracio/index.html">{esc(C.REGISTRATION_BAND['button'])}</a>
</div></div>"""


def proto_banner():
    return '<div class="proto-banner">Prototípus — Népszabadság, 2026. A cikkek egy része a klienstől kapott Figma-terv valós szövege; a Sport és Tudomány rovat, valamint minden fénykép a prototípus számára készült vagy gyűjtött minta.</div>'


def article_href(slug, depth):
    """Every teaser links through to the one built Cikkoldal demo (v1's only full article
    page) — a stand-in for "what an article page looks like", not a claim that each
    headline has its own page yet."""
    up = "../" * depth
    return f"{up}cikk/{C.CIKKOLDAL['slug']}.html"


def article_card_row(slug, depth=0, show_image=True):
    a = C.ARTICLES[slug]
    dek = f"<p>{esc(a['dek'])}</p>" if a.get("dek") else ""
    tag = f' <span class="tag">{esc(a["tag"])}</span>' if a.get("tag") else ""
    when = a.get("time") or a.get("date", "")
    reading = f" · {a['reading']}" if a.get("reading") else ""
    image_html = img(a["image"], "") if show_image else ""
    return f"""<a class="card card-row" href="{article_href(slug, depth)}">
  {image_html}
  <div class="card-body">
    <span class="eyebrow">{esc(a['rovat'])}</span>{tag}
    <h3>{esc(a['headline'])}</h3>
    {dek}
    <div class="meta">{author_link(a['author'])} · {esc(when)}{reading}</div>
  </div>
</a>"""


def article_card_photo(slug, depth=0):
    a = C.ARTICLES[slug]
    when = a.get("time") or a.get("date", "")
    reading = f" · {a['reading']}" if a.get("reading") else ""
    return f"""<a class="card photo-card" href="{article_href(slug, depth)}">
  {img(a['image'])}
  <span class="eyebrow">{esc(a['rovat'])}</span>
  <h3>{esc(a['headline'])}</h3>
  <div class="meta">{author_link(a['author'])} · {esc(when)}{reading}</div>
</a>"""


_DEPTH = 0


def render_page(title, desc, depth, current_nav, body_html, extra_head=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="hu">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{CSS}
<link rel="stylesheet" href="{up}assets/tokens.css">
<link rel="stylesheet" href="{up}assets/site.css">
{extra_head}
</head>
<body>
{proto_banner()}
{header(current_nav, depth)}
{body_html}
{footer(depth)}
</body>
</html>
"""


# ---------------------------------------------------------------- Címlap (home)
def build_cimlap():
    global _DEPTH
    _DEPTH = 0
    L = C.LEAD
    teasers = "".join(
        f'<li><a href="{href or "cikk/" + C.CIKKOLDAL["slug"] + ".html"}">{esc(t)}</a></li>'
        for t, href in L["teasers"]
    )
    lead_html = f"""<section class="lead-story wrap">
  {ad_slot(970, 250)}
  {img(L['image'])}
  <h1>{esc(L['headline'])}</h1>
  <p class="dek">{esc(L['dek'])}</p>
  <div class="meta">{L['reading']}</div>
  <ul class="teasers">{teasers}</ul>
</section>"""

    belfold_block = f"""<section class="wrap">
  <h2 class="section-h first" id="belföld">Belföld</h2>
  <div class="hairline-list">
    {article_card_row('haziorvosi-ellatas')}
    {article_card_row('buszhalozat')}
  </div>
  <a class="card card-row" href="cikk/{C.CIKKOLDAL['slug']}.html">
    {img(C.CIKKOLDAL['image'])}
    <div class="card-body">
      <span class="eyebrow">{esc(C.CIKKOLDAL['rovat'])}</span> <span class="tag">{esc(C.CIKKOLDAL['tag'])}</span>
      <h3>{esc(C.CIKKOLDAL['headline'])}</h3>
      <p>{esc(C.CIKKOLDAL['dek'])}</p>
      <div class="meta">{author_link(C.CIKKOLDAL['author'])} · {esc(C.CIKKOLDAL['date'])} · {esc(C.CIKKOLDAL['reading'])}</div>
    </div>
  </a>
</section>"""

    gazdasag_block = f"""<section class="wrap">
  <h2 class="section-h" id="gazdaság">Gazdaság</h2>
  <div class="grid grid-3">
    {article_card_photo('ipari-termeles')}
    {article_card_photo('logisztikai-piac')}
    {article_card_photo('lakossagi-megtakaritas')}
  </div>
</section>"""

    kultura_block = f"""<section class="wrap">
  <h2 class="section-h" id="kultúra">Kultúra</h2>
  <div class="grid grid-3">
    {article_card_photo('hagyatek-kiallitas')}
    {article_card_photo('szinhaz-evad')}
    {article_card_photo('fotografia-seregszemle')}
  </div>
</section>"""

    kulfold_sport_tud = f"""<section class="wrap">
  <h2 class="section-h" id="külföld">Külföld · Sport · Tudomány</h2>
  <div class="grid grid-3">
    {article_card_photo('miniszteri-egyeztetes')}
    {article_card_photo('sport-nb2')}
    {article_card_photo('tudomany-talaj')}
  </div>
</section>"""

    media_velemeny = f"""<section class="wrap">
  <h2 class="section-h">Média · Vélemény</h2>
  {article_card_row('hetilap-visszaterese')}
</section>"""

    n_items = "".join(
        f"""<div class="photo-card">{img(it['image'])}<h3>{esc(it['short'])}</h3><div class="meta">{author_link(it['author'])} · {esc(it['time'])}</div></div>"""
        for it in C.NEPSZAVA_ITEMS[:6]
    )
    nepszava_block = f"""<section class="wrap" id="népszava">
  <span class="nepszava-badge">Népszava</span>
  <h2 class="section-h" style="border-top:0;margin-top:0">A Népszabadság almárkája</h2>
  <div class="grid grid-3">{n_items}</div>
  <a class="older-btn" href="nepszava/index.html">Tovább a Népszava oldalára</a>
</section>"""

    body = lead_html + belfold_block + gazdasag_block + kulfold_sport_tud + kultura_block + media_velemeny + nepszava_block + reg_band()
    html_out = render_page(
        "Népszabadság — a napilap, 2026",
        "Népszabadság: Belföld, Külföld, Gazdaság, Kultúra, Sport, Tudomány és a Népszava almárka — a lap online kiadása.",
        0, None, body,
    )
    (HERE / "index.html").write_text(html_out, encoding="utf-8")
    print(f"index.html            {len(html_out):6d} bytes")


# ---------------------------------------------------------------- Rovatfront (Belföld)
def build_rovatfront():
    global _DEPTH
    _DEPTH = 1
    R = C.ROVATFRONT
    pills = "".join(f'<span class="pill pill-static">{esc(p)}</span>' for p in R["pills"])
    lead = R["lead"]
    lead_html = f"""<a class="card lead-story" href="../cikk/{C.CIKKOLDAL['slug']}.html" style="display:block">
  {img(lead['image'])}
  <h2 style="font-size:clamp(24px,5vw,34px)">{esc(lead['headline'])}</h2>
  <p class="dek">{esc(lead['dek'])}</p>
  <div class="meta">{author_link(lead['author'])} · {lead['reading']}</div>
</a>"""
    list_html = "".join(article_card_row(s, depth=1) for s in R["list"])
    authors_html = "".join(
        f"""<div class="author-card"><div class="ph-box" style="width:100%;aspect-ratio:1/1;background:#e2e2e2;border-radius:6px;margin-bottom:8px"></div><h4>{esc(C.AUTHORS[k]['name'])}</h4><p>{esc(C.AUTHORS[k]['beat'])}</p></div>"""
        for k in R["authors"]
    )
    body = f"""{article_pills(["Az újraindítás", "A szerkesztőség", "Tíz év után"])}
<section class="wrap">
  <div class="rovat-head">
    <h1>{esc(R['rovat'])}</h1>
    <p>{esc(R['description'])}</p>
    <div class="rovat-pills">{pills}</div>
  </div>
  {lead_html}
  <div class="hairline-list" style="margin-top:20px">{list_html}</div>
  <h2 class="section-h">A rovat szerzői</h2>
  <div class="authors-grid">{authors_html}</div>
  <a class="older-btn" href="../index.html">Régebbi cikkek</a>
</section>
{reg_band(1)}"""
    out_dir = HERE / "belfold"
    out_dir.mkdir(exist_ok=True)
    html_out = render_page(
        "Belföld — Népszabadság",
        "Önkormányzatok, közigazgatás, egészségügy és oktatás — a Belföld rovat a Népszabadságon.",
        1, "Belföld", body,
    )
    (out_dir / "index.html").write_text(html_out, encoding="utf-8")
    print(f"belfold/index.html    {len(html_out):6d} bytes")


# ---------------------------------------------------------------- Cikkoldal
def build_cikkoldal():
    global _DEPTH
    _DEPTH = 1
    A = C.CIKKOLDAL
    body_paras = []
    for block in A["body"]:
        if block.startswith("@AD@"):
            w, h = block[4:].split("x")
            body_paras.append(ad_slot(int(w), int(h)))
        else:
            body_paras.append(f"<p>{esc(block)}</p>")
    body_html = "\n".join(body_paras)

    paywall = f"""<div class="paywall-box">
  <h2>{esc(C.PAYWALL['heading'])}</h2>
  <ul>{"".join(f"<li>{esc(b)}</li>" for b in A['paywall_bullets'])}</ul>
  <div class="paywall-actions">
    <button class="btn-primary" type="button" onclick="alert('Ez a gomb a prototípusban nem regisztrál — a valódi regisztrációs folyamat még nem épült meg (lásd 03-sources.md, 5. pont).')">{esc(C.PAYWALL['register'])}</button>
    <button class="btn-outline" type="button" onclick="alert('Ez a gomb a prototípusban nem indít fizetést.')">{esc(C.PAYWALL['subscribe'])}</button>
  </div>
  <a class="login-link" href="#" onclick="return false">{esc(C.PAYWALL['login'])}</a>
  <p class="note">{esc(C.PAYWALL['note'])}</p>
</div>"""

    topic_pills = "".join(f'<span class="pill pill-static">{esc(p)}</span>' for p in A["topic_pills"])
    related = "".join(article_card_photo(s, depth=1) for s in A["related"])

    main_col = f"""<div class="article-header">
  <span class="eyebrow">{esc(A['rovat'])}</span> <span class="tag">{esc(A['tag'])}</span>
  <h1>{esc(A['headline'])}</h1>
  <p class="dek">{esc(A['dek'])}</p>
</div>
<div class="article-hero">{img(A['image'])}</div>
<p class="photo-caption">{esc(A['photo_caption'])}</p>
<div class="author-row">
  <div class="ph-box" style="width:52px;height:52px;border-radius:50%;background:#e2e2e2"></div>
  <div>
    <div class="name">{esc(C.AUTHORS[A['author']]['name'])}</div>
    <div class="bio">{esc(C.AUTHORS[A['author']]['bio'])} · {esc(A['date'])} · {esc(A['reading'])}</div>
    <button class="primary-source-btn" type="button" onclick="alert('A forrásjelölés a prototípusban nem működik.')">Beállítás elsődleges forrásként</button>
  </div>
</div>
<div class="article-body">{body_html}</div>
{paywall}
<h2 class="section-h">Még a témában</h2>
<div class="rovat-pills">{topic_pills}</div>
<h2 class="section-h">Ezt is ajánljuk</h2>
<div class="grid grid-3">{related}</div>"""

    rail = f"""<aside class="rail">{ad_slot(300, 250)}</aside>"""

    body = f"""{article_pills(A['related_pills'])}
<div class="wrap">
  <div class="cikk-layout">
    <div>{main_col}</div>
    {rail}
  </div>
</div>
{reg_band(1)}"""

    out_dir = HERE / "cikk"
    out_dir.mkdir(exist_ok=True)
    html_out = render_page(
        f"{A['headline']} — Népszabadság",
        A["dek"], 1, "Belföld", body,
    )
    out_path = out_dir / f"{A['slug']}.html"
    out_path.write_text(html_out, encoding="utf-8")
    print(f"cikk/{A['slug']}.html {len(html_out):6d} bytes")


# ---------------------------------------------------------------- Népszava márkafront
def build_nepszava():
    global _DEPTH
    _DEPTH = 1
    pills = "".join(f'<span class="pill pill-static">{esc(p)}</span>' for p in ["A nyomtatott lapból", "Vélemény", "Riport", "Interjú", "Jegyzet"])
    lead = C.NEPSZAVA_ITEMS[0]
    lead_html = f"""<div class="lead-story">
  {img(lead['image'])}
  <h2 style="font-size:clamp(24px,5vw,34px)">{esc(lead['headline'])}</h2>
  <p class="dek">{esc(lead['dek'])}</p>
  <div class="meta">{author_link(lead['author'])} · {lead['time']} · {lead['reading']}</div>
</div>"""
    items = "".join(
        f"""<div class="photo-card">{img(it['image'])}<h3>{esc(it['headline'])}</h3><div class="meta">{author_link(it['author'])} · {esc(it['time'])}{' · ' + it['reading'] if it.get('reading') else ''}</div></div>"""
        for it in C.NEPSZAVA_ITEMS[1:]
    )
    print_block = "".join(
        f"""<div class="card-row">{img(it['image'])}<div class="card-body"><h3>{esc(it['headline'])}</h3><div class="meta">{author_link(it['author'])} · Nyomtatásban: 2026. október 8., {it.get('print_page','1')}. oldal · {esc(it.get('reading') or '')}</div></div></div>"""
        for it in C.NEPSZAVA_ITEMS if it.get("print_page")
    )
    velemeny = "".join(
        f"""<div class="card-row"><div class="card-body"><h3>{esc(v['headline'])}</h3><div class="meta">{author_link(v['author'])} · {esc(v['date'])} · {esc(v['reading'])}</div></div></div>"""
        for v in C.NEPSZAVA_VELEMENY
    )
    authors_html = "".join(
        f"""<div class="author-card"><div class="ph-box" style="width:100%;aspect-ratio:1/1;background:#e2e2e2;border-radius:6px;margin-bottom:8px"></div><h4>{esc(C.AUTHORS[k]['name'])}</h4><p>{esc(C.AUTHORS[k]['beat'])}</p></div>"""
        for k in ["toth_akos", "nagy_eszter", "varga_tamas"]
    )
    body = f"""<section class="wrap">
  <div class="rovat-head">
    <span class="nepszava-badge">Népszava</span>
    <h1>Népszava</h1>
    <p>A Népszabadság almárkája: a Népszava szerkesztőségének online anyagai és a nyomtatott lapszámok cikkei, egy helyen.</p>
    <div class="rovat-pills">{pills}</div>
  </div>
  {lead_html}
  <div class="grid grid-3" style="margin-top:20px">{items}</div>
  <h2 class="section-h">A nyomtatott lapból</h2>
  <div class="hairline-list">{print_block}</div>
  <h2 class="section-h">Vélemény</h2>
  <div class="hairline-list">{velemeny}</div>
  <h2 class="section-h">A Népszava szerzői</h2>
  <div class="authors-grid">{authors_html}</div>
  <a class="older-btn" href="../index.html">Régebbi cikkek</a>
</section>
{reg_band(1)}"""
    out_dir = HERE / "nepszava"
    out_dir.mkdir(exist_ok=True)
    html_out = render_page(
        "Népszava — a Népszabadság almárkája",
        "A Népszava: a Népszabadság almárkája — a nyomtatott lapszám cikkei, vélemények, riportok és interjúk egy helyen.",
        1, "Népszava", body,
    )
    (out_dir / "index.html").write_text(html_out, encoding="utf-8")
    print(f"nepszava/index.html   {len(html_out):6d} bytes")


# ---------------------------------------------------------------- Landing (pre-registration)
def build_landing():
    global _DEPTH
    _DEPTH = 1
    L = C.LANDING
    reg = L["registration"]
    fields = "".join(f'<input type="text" placeholder="{esc(f)}" required>' if f != "E-mail cím" else '<input type="email" placeholder="E-mail cím" required>' for f in reg["fields"])
    countdown = L["countdown"]
    mission = L["mission"]
    paras = "".join(f"<p>{esc(p)}</p>" for p in mission["paragraphs"])
    szerk = L["szerkesztoseg"]

    body = f"""<section class="landing-section wrap">
  <span class="eyebrow">{esc(reg['eyebrow'])}</span>
  <h1>{esc(reg['h1'])}</h1>
  <p class="lead-text">{esc(reg['lead'])}</p>
  <form class="reg-form" onsubmit="event.preventDefault();document.getElementById('regok').classList.add('is-shown');this.reset();">
    {fields}
    <button class="btn-primary" type="submit">{esc(reg['button'])}</button>
  </form>
  <div class="reg-success" id="regok">Köszönjük a regisztrációt! (A prototípusban ez az üzenet csak a böngészőben jelenik meg — a valódi feliratkozás fogadó rendszere még nincs kijelölve, lásd 03-sources.md, 5. pont.)</div>
</section>

<section class="landing-section wrap">
  <h2>{esc(countdown['h1'])}</h2>
  <p class="lead-text">{esc(countdown['lead'])}</p>
  <div class="countdown" id="countdown" data-launch="{L['launch_iso']}">
    <div class="unit"><span class="num" id="cd-d">–</span><span class="label">nap</span></div>
    <div class="unit"><span class="num" id="cd-h">–</span><span class="label">óra</span></div>
    <div class="unit"><span class="num" id="cd-m">–</span><span class="label">perc</span></div>
    <div class="unit"><span class="num" id="cd-s">–</span><span class="label">mp</span></div>
  </div>
</section>

<section class="landing-section wrap">
  <h2>{esc(mission['h1'])}</h2>
  {paras}
</section>

<section class="landing-section wrap">
  <div class="quote-block">„{esc(C.QUOTE['text'])}”<cite>{esc(C.QUOTE['by'])}, {esc(C.QUOTE['role'])}</cite></div>
</section>

<section class="landing-section wrap">
  <h2>{esc(szerk['h1'])}</h2>
  <p class="lead-text">{esc(szerk['lead'])}</p>
  <div class="editor-post"><div class="ph-box"></div><p>{esc(szerk['placeholder'])}</p></div>
</section>

<script>
(function(){{
  var el = document.getElementById('countdown');
  var target = new Date(el.dataset.launch).getTime();
  function tick(){{
    var diff = Math.max(0, target - Date.now());
    var d = Math.floor(diff/86400000), h = Math.floor(diff%86400000/3600000),
        m = Math.floor(diff%3600000/60000), s = Math.floor(diff%60000/1000);
    document.getElementById('cd-d').textContent = d;
    document.getElementById('cd-h').textContent = String(h).padStart(2,'0');
    document.getElementById('cd-m').textContent = String(m).padStart(2,'0');
    document.getElementById('cd-s').textContent = String(s).padStart(2,'0');
  }}
  tick(); setInterval(tick, 1000);
}})();
</script>"""
    out_dir = HERE / "regisztracio"
    out_dir.mkdir(exist_ok=True)
    html_out = render_page(
        "Előregisztráció — Népszabadság, 2026. október 8.",
        "Indul az elő-regisztráció! Iratkozz fel, hogy elsőként értesülj a Népszabadság újraindulásáról 2026. október 8-án.",
        1, None, body,
    )
    (out_dir / "index.html").write_text(html_out, encoding="utf-8")
    print(f"regisztracio/index.html {len(html_out):6d} bytes")


if __name__ == "__main__":
    build_cimlap()
    build_rovatfront()
    build_cikkoldal()
    build_nepszava()
    build_landing()
