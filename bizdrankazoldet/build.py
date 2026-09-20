#!/usr/bin/env python3
"""Generate the Bízd ránk a zöldet prototype (Hungarian) from one content source.
Run: python3 bizdrankazoldet/build.py → index.html and the six pages. No dependencies.
Two designed experiences (D2): phone (≤ 767, designed at 390 — Instagram-first, one column, the
quote CTA within thumb reach) and desktop (≥ 1024, designed at 1440 — Google/LinkedIn-first, the
proof before the persuasion); tablet resolves between them. Everything marked "minta" is sample."""
import pathlib, html
HERE = pathlib.Path(__file__).parent
E = html.escape

PROTO = "Prototípus — Bízd ránk a zöldet, 2026. Az űrlapok nem küldenek; a referenciák, az árak és a csapat adatai minták az ügyfél anyagáig. A szöveg az ügyfél saját hangja."
PHONE = "+36 70 850 8888"; PHONE_HREF = "tel:+36708508888"

# ---------- the client's own visual system: logo, photographs, hand-drawn illustrations (assets/img)
def img(name, alt, cls="", w=None, h=None, sizes="100vw"):
    small = f'assets/img/{name}-800.jpg'
    if (HERE / small).exists():
        return f'<img src="assets/img/{name}.jpg" srcset="{small} 800w, assets/img/{name}.jpg 1600w" sizes="{sizes}" alt="{E(alt)}" class="{cls}" loading="lazy" decoding="async"{f" width={w} height={h}" if w else ""}>'
    return f'<img src="assets/img/{name}" alt="{E(alt)}" class="{cls}" loading="lazy" decoding="async">'
def logo(): return '<img src="assets/img/logo-kez.png" alt="" width="44" height="32" class="logoimg">'

# ---------- content (Hungarian, the client's voice)
NAV = [("irodai-novenyek.html", "Irodai növények"), ("novenygondozas.html", "Növénygondozás"), ("novenyberles.html", "Növénybérlés"), ("referenciak.html", "Referenciák"), ("arak.html", "Árak"), ("rolunk.html", "Rólunk")]
PACKAGES = [
 ("Kis iroda", "5 növény", "havi 24 900 Ft-tól", "bérlés + gondozás", ["2 állónövény, 3 asztali", "kéthetente gondozás", "örökzöld garancia", "telepítés egy délelőtt"]),
 ("Közepes iroda", "12 növény", "havi 49 900 Ft-tól", "bérlés + gondozás", ["4 állónövény, 8 asztali és polcos", "kéthetente gondozás", "örökzöld garancia", "szezonális csere"]),
 ("Nagy iroda", "25+ növény", "egyedi ajánlat", "tervezéssel", ["térelválasztó zöld, tárgyalók, recepció", "hetente gondozás", "örökzöld garancia", "névre szóló gondozó"]),
]
STEPS = [
 ("1", "Küldj három fotót", "Az irodáról, telefonnal, ahogy van. Nem kell rendet rakni, a növényeknek úgyis mindegy."),
 ("2", "Két munkanapon belül látványterv és ajánlat", "A te irodád fotóin, a növényekkel a helyükön, a csomaggal és az árral. Egy PDF, amit tovább lehet küldeni annak, aki aláír."),
 ("3", "Telepítés egy délelőtt", "Jövünk, letesszük, beállítjuk. Délre olyan az iroda, mintha mindig is így lett volna."),
 ("4", "Gondozás ritmusban", "Kéthetente vagy hetente jövünk: víz, tápanyag, metszés, kártevő-ellenőrzés, tisztítás. Minden látogatás után egy kártya az asztalon. A gyakornok szabadnapos."),
]
FAQ = [
 ("Mi történik, ha kicsi az iroda, vagy kevés a hely a növényeknek?", "A tapasztalatunk szerint a méret önmagában ritkán akadály. A legtöbb irodában nem az a kérdés, hogy elfér-e növény, hanem az, hogy hol van értelme elhelyezni. Kisebb terekben különösen fontos az arányérzék és a pozicionálás, mert egy jól kiválasztott növény azonnal javít a tér érzetén."),
 ("Nem lesz ez is csak egy rövid távú, látványos megoldás?", "Nem, mert nem egyszeri élményelemként gondolunk a növényekre. Egy növény nem program és nem dekorációs attrakció, hanem folyamatosan jelen lévő háttér. Nem harsány, nem igényel figyelmet, mégis minden nap hat a térre."),
 ("Kinek a feladata a növények gondozása az irodában?", "A miénk. Nálunk a karbantartás a szolgáltatás része, nem külön opció. Így az irodának nem kell ezzel foglalkoznia, a növények pedig nem csak bekerülnek a térbe, hanem hosszú távon is jó állapotban maradnak."),
 ("Mi van, ha egy növény mégis elpusztul?", "Cseréljük, díjmentesen. Ez az örökzöld garancia: ami a mi gondozásunk alatt leépül, azt mi pótoljuk. Nem vita, nem jegyzőkönyv."),
 ("Valóban érezhető hatása van a növényeknek a mindennapi munkára?", "A hatás nem látványos és nem azonnali, de érezhető. A kutatások 6–15 % közötti javulást mérnek a közérzetben és a munkakedvben; mi annyit ígérünk, hogy könnyebb leülni dolgozni, kevésbé nyomasztó a tér, és megszűnik az az érzés, hogy egész nap egy dobozban ülünk."),
 ("Mennyi idő, amíg ajánlatot kapok?", "Két munkanap a fotók beérkezésétől — látványtervvel, a te irodád képein."),
]
REFS = [
 ("Fintech iroda, XIII. kerület", "38 növény · 2 tárgyaló · recepció", "„Három hónap után vettem észre, hogy senki nem beszél a növényekről. Ez a legjobb, ami történhet velük.”", "Irodavezető"),
 ("Ügyvédi iroda, V. kerület", "12 növény · hetente gondozás", "„Végre nem a recepciós locsol. És végre nem hal meg semmi.”", "Office manager"),
 ("Startup, IX. kerület", "bérlés · 20 növény · költözéssel", "„Költöztünk, a növények jöttek velünk, mi meg nem csináltunk semmit.”", "Alapító"),
]
TEAM = [("[Név]", "alapító, ügyvezető", "Tíz éve zöldfalakat és irodákat építünk Grofie néven. Ez a csapat annak a része, amelyik az irodákra szakosodott."), ("[Név]", "növénygondozó, a te irodád felelőse", "Kéthetente ott van. Ismeri a fikuszt névről."), ("[Név]", "tervező", "A három fotóból látványterv. Két munkanap.")]

# ---------- CSS: mobile first; tablet and desktop as their own states
CSS = """
*{box-sizing:border-box} html{scroll-behavior:smooth} @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{margin:0;background:var(--bz-white);color:var(--bz-text);font:16px/1.6 var(--bz-sans)} img{max-width:100%;height:auto;display:block} a{color:inherit}
h1,h2{font-family:var(--bz-display);font-weight:700;line-height:1.05;margin:0} h3{font-family:var(--bz-slab);font-weight:600;line-height:1.2;margin:0} h1{font-size:36px} h2{font-size:30px} h3{font-size:19px}
p{margin:0 0 12px} .lede{color:var(--bz-muted);font-size:17px;max-width:56ch}
.wrap{width:min(100% - 32px,1200px);margin-inline:auto}
.proto{background:var(--bz-accent);color:var(--bz-text);font-size:12px;font-weight:600;text-align:center;padding:8px 14px;margin:0}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:12px 24px;border-radius:var(--bz-pill);background:var(--bz-primary);color:#fff;text-decoration:none;font-weight:700;border:0;font-size:15px;cursor:pointer;font-family:var(--bz-sans)}
.btn:hover{background:var(--bz-text)} .btn.alt{background:var(--bz-white);color:var(--bz-primary);border:2px solid var(--bz-primary)} .btn.lime{background:var(--bz-accent);color:var(--bz-text)}
.hd{position:sticky;top:0;z-index:20;background:var(--bz-white);border-bottom:1px solid var(--bz-line)}
.hd .wrap{display:flex;align-items:center;justify-content:space-between;min-height:64px;gap:10px}
.brand{display:flex;align-items:center;gap:10px;min-height:44px;text-decoration:none;font-family:var(--bz-display);font-weight:700;font-size:19px;color:var(--bz-primary)} .brand .logoimg{width:40px;height:auto;background:var(--bz-primary);border-radius:8px;padding:5px}
.hd nav{display:none} .hd .cta{display:none} .menu{min-width:48px;min-height:48px;border:0;background:none;font-weight:700;color:var(--bz-primary);font-size:15px;font-family:var(--bz-sans)}
.sheet{display:none;background:var(--bz-lime-tint);border-bottom:1px solid var(--bz-line)} .sheet[open]{display:block} .sheet a{display:flex;align-items:center;min-height:50px;padding:0 16px;text-decoration:none;font-weight:600;border-top:1px solid var(--bz-line)}
.dock{position:fixed;left:0;right:0;bottom:0;z-index:30;display:grid;grid-template-columns:1fr auto;gap:8px;padding:10px 16px calc(10px + env(safe-area-inset-bottom));background:var(--bz-white);border-top:2px solid var(--bz-accent)}
.dock .btn{width:100%} main{padding-bottom:92px}
.hero{padding:0 0 24px} .hero .photo{aspect-ratio:4/5;object-fit:cover;width:100%} .hero .txt{padding:22px 0 0} .hero h1{max-width:15ch;color:var(--bz-primary)} .hero .row{display:flex;flex-direction:column;gap:10px;margin-top:16px}
.kicker{font-family:var(--bz-slab);font-size:14px;color:var(--bz-muted);margin:0 0 6px}
.proof{background:var(--bz-lime-tint);padding:20px 0;border-top:3px solid var(--bz-accent);border-bottom:3px solid var(--bz-accent)} .proof .wrap{display:grid;grid-template-columns:1fr 1fr;gap:14px 12px} .proof b{display:block;font-family:var(--bz-display);font-size:34px;line-height:1;color:var(--bz-primary)} .proof span{font-size:13px} .proof small{grid-column:1/-1;font-size:12px;color:var(--bz-muted)}
.sec{padding:40px 0} .sec .head{margin-bottom:18px} .sec .head h2{max-width:22ch}
.offers{display:grid;gap:18px} .offer{display:grid;gap:10px} .offer img{aspect-ratio:3/2;object-fit:cover;width:100%} .offer .fun{font-family:var(--bz-display);font-size:24px;line-height:1.1;margin:0;color:var(--bz-primary)} .offer .pro{color:var(--bz-muted);margin:0 0 6px} .offer a{font-weight:700;color:var(--bz-primary);text-decoration:none;display:inline-flex;align-items:center;min-height:44px}
.guar{background:var(--bz-cyan-tint);padding:28px 0} .guar .grid{display:grid;gap:18px} .guar img{width:200px;margin:0 auto 6px} .guar ul{margin:0;padding-left:18px} .guar li{margin:4px 0} .guar h3{margin-bottom:6px}
.packs{display:grid;gap:14px} .pack{border:2px solid var(--bz-line);border-radius:18px;padding:20px} .pack.hi{border-color:var(--bz-primary);background:var(--bz-lime-tint)} .pack .price{font-family:var(--bz-display);font-size:28px;color:var(--bz-primary);margin:6px 0 0} .pack .unit{font-size:13px;color:var(--bz-muted);margin:0 0 8px} .pack ul{padding-left:18px;margin:0 0 14px}
.sample{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;background:var(--bz-secondary);color:var(--bz-text);padding:2px 8px;border-radius:var(--bz-pill)}
.steps{display:grid;gap:16px} .steps img{width:64px;height:auto} .step{display:grid;grid-template-columns:64px 1fr;gap:14px;align-items:start} .step p{color:var(--bz-muted);margin:2px 0 0} .steps .checklist{width:120px;margin:0}
.refs{display:grid;gap:18px} .ref img{aspect-ratio:3/2;object-fit:cover;width:100%} .ref h3{margin:10px 0 4px} .ref q{font-family:var(--bz-slab);display:block;margin:6px 0 4px;quotes:none;font-size:16px} .ref small{color:var(--bz-muted)}
.silly{display:grid;gap:14px;align-items:center} .silly img{width:100%} .silly h2{color:var(--bz-primary)}
.team{display:grid;gap:12px} .person{display:grid;grid-template-columns:56px 1fr;gap:12px;align-items:center;border-top:1px solid var(--bz-line);padding:12px 0} .person i{width:56px;height:56px;border-radius:50%;background:var(--bz-lime-tint);display:grid;place-items:center;font-style:normal;font-weight:700;color:var(--bz-primary)} .person small{color:var(--bz-muted);display:block}
.faq details{border-top:1px solid var(--bz-line)} .faq details:last-child{border-bottom:1px solid var(--bz-line)} .faq summary{padding:14px 0;font-weight:700;cursor:pointer;min-height:50px;display:flex;align-items:center;font-family:var(--bz-slab)} .faq p{padding:0 0 14px;color:var(--bz-muted)}
.form{display:grid;gap:12px;background:var(--bz-lime-tint);padding:20px;border-radius:18px} .form label{display:grid;gap:6px;font-size:13px;font-weight:700} .form input,.form textarea{min-height:50px;border:1px solid var(--bz-line);border-radius:12px;padding:10px 12px;font:inherit;background:#fff} .form .drop{border:2px dashed var(--bz-primary);border-radius:12px;padding:18px;text-align:center;color:var(--bz-primary);font-weight:700;background:#fff} .form .promise{font-size:13px;color:var(--bz-muted)} .form .promise a,.imp a{display:inline-flex;align-items:center;min-height:44px;font-weight:700;color:var(--bz-primary)}
.ig{display:grid;gap:12px} .ig iframe{width:100%;aspect-ratio:9/16;max-height:640px;border:0;border-radius:12px;background:var(--bz-grey)}
footer{background:var(--bz-text);color:#E9F2F1;padding:32px 0 40px;font-size:14px} footer .grid{display:grid;gap:22px} footer h4{margin:0 0 8px;font-family:var(--bz-slab);font-size:13px;color:var(--bz-accent)} footer a{color:#fff;text-decoration:none;display:flex;align-items:center;min-height:44px} footer ul{list-style:none;margin:0;padding:0} footer .imp{font-size:13px;color:#C9D9D6;line-height:1.7} footer .imp b{color:#fff} footer .logoimg{width:64px;margin-bottom:10px}
/* tablet */
@media(min-width:768px){h1{font-size:46px} h2{font-size:36px} .hero{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:center;padding:0} .hero .photo{aspect-ratio:4/5;height:100%} .hero .txt{padding:32px 0 32px 8px} .hero .row{flex-direction:row} .offers{grid-template-columns:repeat(3,1fr)} .guar .grid{grid-template-columns:200px 1fr 1fr 1fr;align-items:start} .guar img{margin:0} .packs{grid-template-columns:repeat(3,1fr)} .steps{grid-template-columns:1fr 1fr} .refs{grid-template-columns:repeat(3,1fr)} .silly{grid-template-columns:1fr 1fr} .team{grid-template-columns:repeat(3,1fr)} .proof .wrap{grid-template-columns:repeat(4,1fr)} .ig{grid-template-columns:repeat(2,1fr)} footer .grid{grid-template-columns:1.4fr 1fr 1fr}}
/* desktop — its own design: the photograph is the hero, the proof follows it, the header carries the pages, no dock */
@media(min-width:1024px){body{font-size:17px} h1{font-size:62px} h2{font-size:42px} .wrap{width:min(100% - 120px,1200px)}
 .hd .wrap{min-height:76px} .brand{font-size:21px} .hd nav{display:flex;gap:2px} .hd nav a{display:inline-flex;align-items:center;min-height:48px;padding:0 12px;text-decoration:none;font-weight:600;border-bottom:3px solid transparent} .hd nav a:hover,.hd nav a[aria-current]{border-color:var(--bz-accent);color:var(--bz-primary)} .hd .cta{display:inline-flex} .menu{display:none} .dock{display:none} main{padding-bottom:0}
 .hero{grid-template-columns:1.05fr .95fr;gap:0} .hero .photo{aspect-ratio:auto;height:640px} .hero .txt{padding:56px 48px 56px 0} .hero h1{max-width:13ch} .hero .row{margin-top:26px;gap:14px}
 .proof{padding:26px 0} .proof b{font-size:44px} .sec{padding:64px 0} .sec .head{display:grid;grid-template-columns:1fr auto;align-items:end;margin-bottom:28px}
 .offer .fun{font-size:28px} .guar{padding:48px 0} .guar .grid{grid-template-columns:260px 1fr 1fr 1fr;gap:32px} .guar img{width:260px}
 .pack{padding:26px} .pack .price{font-size:36px} .steps{grid-template-columns:repeat(4,1fr);gap:24px} .step{grid-template-columns:1fr} .step img{margin-bottom:10px}
 .refs{gap:24px} .silly{gap:40px} .form{grid-template-columns:1fr 1fr;padding:28px} .form .full{grid-column:1/-1} .ig{grid-template-columns:repeat(4,1fr)} footer .grid{grid-template-columns:1.6fr 1fr 1fr 1fr}}
"""

def head(title, desc, slug):
    return f'''<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Roboto+Slab:wght@500;600&family=Roboto:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/tokens.css">
<style>{CSS}</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"LocalBusiness","name":"Bízd ránk a zöldet!","legalName":"Gourmet Garden Kft.","telephone":"{PHONE}","url":"https://bizdrankazoldet.hu/","areaServed":"Budapest","sameAs":["https://www.instagram.com/bizdrankazoldet/","https://grofiezoldfal.com/"],"makesOffer":[{{"@type":"Offer","name":"Irodai növénydekoráció"}},{{"@type":"Offer","name":"Növénygondozás"}},{{"@type":"Offer","name":"Növénybérlés"}}]}}</script>
</head>
<body>
<p class="proto">{E(PROTO)}</p>
<header class="hd"><div class="wrap">
<a class="brand" href="index.html">{logo()}<span>Bízd ránk a zöldet!</span></a>
<nav aria-label="Oldalak">{"".join(f'<a href="{h}"{" aria-current=page" if h == slug else ""}>{E(l)}</a>' for h, l in NAV)}</nav>
<a class="btn cta" href="ajanlat.html">Kérek ajánlatot</a>
<button class="menu" type="button" aria-expanded="false" aria-controls="sheet" onclick="var s=document.getElementById('sheet');s.toggleAttribute('open');this.setAttribute('aria-expanded',s.hasAttribute('open'))">Menü</button>
</div>
<div class="sheet" id="sheet"><nav aria-label="Oldalak, telefon">{"".join(f'<a href="{h}">{E(l)}</a>' for h, l in NAV)}<a href="ajanlat.html">Kérek ajánlatot</a></nav></div>
</header>
<main id="top">
'''

def foot():
    return f'''</main>
<div class="dock" aria-label="Gyors ajánlatkérés"><a class="btn" href="ajanlat.html">3 fotó → ajánlat 2 munkanapon belül</a><a class="btn alt" href="{PHONE_HREF}">Hívás</a></div>
<footer><div class="wrap grid">
<div><img src="assets/img/logo-kez.png" alt="Bízd ránk a zöldet" class="logoimg" width="64" height="47"><h4>Bízd ránk a zöldet!</h4><p class="imp"><b>Gourmet Garden Kft.</b> (Grofie)<br>Székhely: [minta — a cég székhelye]<br>Cégjegyzékszám: [minta] · Adószám: [minta]<br>E-mail: [minta]@bizdrankazoldet.hu · Tel.: <a href="{PHONE_HREF}">{PHONE}</a></p></div>
<div><h4>Szolgáltatások</h4><ul>{"".join(f'<li><a href="{h}">{E(l)}</a></li>' for h, l in NAV[:3])}</ul></div>
<div><h4>A cég</h4><ul><li><a href="referenciak.html">Referenciák</a></li><li><a href="arak.html">Árak és folyamat</a></li><li><a href="rolunk.html">Rólunk, impresszum</a></li><li><a href="https://grofiezoldfal.com/">Grofie — zöldfalak</a></li></ul></div>
<div><h4>Kövess</h4><ul><li><a href="https://www.instagram.com/bizdrankazoldet/">Instagram @bizdrankazoldet</a></li><li><a href="https://bizdrankazoldet.hu/app/uploads/2026/08/Adatkezelesi-tajekoztato-–-Gourmet-Garden-Kft_20260319_2.pdf">Adatkezelési tájékoztató</a></li></ul></div>
</div></footer>
</body>
</html>
'''

def proof_band():
    return f'''<section class="proof" aria-label="Számok"><div class="wrap">
<div><b>10+</b><span>év irodák zöldítésében</span></div><div><b>100+</b><span>megvalósított projekt</span></div><div><b>30+</b><span>iroda folyamatos gondozás alatt</span></div><div><b>100%</b><span>örökzöld garancia</span></div>
<small>A Grofie (Gourmet Garden Kft.) számai — ugyanaz a csapat, az irodákra szakosodva.</small>
</div></section>'''

def offers():
    return f'''<section class="sec" id="szolgaltatasok"><div class="wrap"><div class="head"><div><p class="kicker">Három út a zöld irodához</p><h2>Vagy megveszed, vagy béreled, vagy csak gondozzuk</h2></div></div>
<div class="offers">
<article class="offer">{img("nyitott-iroda", "Nyitott iroda növénykaspókkal az asztalsorok között", sizes="(min-width:768px) 33vw, 100vw")}<p class="fun">Irodai növények, hogy ne legyen ciki az iroda</p><p class="pro">Felmérjük a fényt, a klímát, a használatot; megtervezzük, telepítjük, gondozzuk. Egy kézben.</p><a href="irodai-novenyek.html">Növénydekoráció →</a></article>
<article class="offer">{img("asztalok-kaspok", "Íróasztalok között álló növénykaspók", sizes="(min-width:768px) 33vw, 100vw")}<p class="fun">Ne a gyakornok locsoljon</p><p class="pro">Kéthetente vagy hetente jövünk: víz, tápanyag, metszés, kártevő-ellenőrzés. A meglévő növényeidhez is.</p><a href="novenygondozas.html">Növénygondozás →</a></article>
<article class="offer">{img("lobby-narancs", "Recepció narancssárga fotelekkel és növényekkel", sizes="(min-width:768px) 33vw, 100vw")}<p class="fun">Béreld, amíg a kávéfőző sem végleges</p><p class="pro">Havidíj, gondozással. Költözéskor jönnek veletek; rendezvényre egy napra is.</p><a href="novenyberles.html">Növénybérlés →</a></article>
</div></div></section>'''

def guarantee():
    return f'''<section class="guar" id="garancia"><div class="wrap"><div class="grid">
<img src="assets/img/ill-gondozas-kor.png" alt="Növény kaspóban, körülötte a gondozás lépései: fény, víz, tápanyag, metszés" width="457" height="710" loading="lazy">
<div><p class="kicker">Örökzöld garancia</p><h2 style="font-size:28px;margin-bottom:8px">Ami a mi gondozásunk alatt leépül, azt mi cseréljük. Díjmentesen.</h2><p class="lede" style="font-size:15px">Nem vita, nem jegyzőkönyv. Ez a különbség a „majd valaki locsolja” és a „mi felelünk érte” között.</p></div>
<div><h3>Mit tartalmaz egy látogatás?</h3><ul><li>öntözés a növény igénye szerint</li><li>tápanyag, metszés, formázás</li><li>kártevő- és betegség-ellenőrzés</li><li>levél- és kaspótisztítás</li><li>egy kártya az asztalon: mi történt, mikor jövünk</li></ul></div>
<div><h3>Milyen ritmusban, mennyi idő?</h3><ul><li>kéthetente a legtöbb irodában, hetente nagy tereknél</li><li>névre szóló gondozó, aki ismeri az irodát</li><li>aznapi válasz, ha valami nem stimmel</li><li>ajánlat <b>két munkanapon belül</b> a három fotó után</li><li>telepítés egy délelőtt</li></ul></div>
</div></div></section>'''

def packages(full=False):
    cards = "".join(f'''<article class="pack{" hi" if i == 1 else ""}"><p class="kicker">{E(n)}</p><h3>{E(c)}</h3><p class="price">{E(p)}</p><p class="unit">{E(u)} · <span class="sample">mintaár</span></p><ul>{"".join(f"<li>{E(x)}</li>" for x in items)}</ul><a class="btn{"" if i == 1 else " alt"}" href="ajanlat.html">Ezt kérem</a></article>''' for i, (n, c, p, u, items) in enumerate(PACKAGES))
    return f'''<section class="sec" id="arak"><div class="wrap"><div class="head"><div><p class="kicker">Mennyibe kerül?</p><h2>Csomagok, „-tól” árakkal — mert a „kérj ajánlatot” önmagában nem ár</h2></div>{"" if full else '<a class="btn alt" href="arak.html">Minden részlet</a>'}</div>
<p class="lede">A pontos ár a növények számától, a kaspóktól és a gondozás ritmusától függ. Az itt látható számok minták az ügyfél áraiig — a szerkezet a lényeg: havidíj, gondozással, garanciával.</p>
<div class="packs">{cards}</div></div></section>'''

def steps():
    icons = ["ill-ikon-csapat.png", "ill-lepesek.png", "ill-ikon-frissit.png", "ill-checklist.png"]
    return f'''<section class="sec" id="folyamat"><div class="wrap"><div class="head"><div><p class="kicker">Hogyan működik</p><h2>Négy lépés, ebből egy a tiéd</h2></div></div>
<div class="steps">{"".join(f'<div class="step"><img src="assets/img/{ic}" alt="" loading="lazy"><div><h3>{E(tt)}</h3><p>{E(d)}</p></div></div>' for ic, (n, tt, d) in zip(icons, STEPS))}</div></div></section>'''

def references(full=False):
    photos = [("iroda-piros-folyoso", "Iroda piros ajtókeretekkel, a folyosón növénykaspók"), ("konyvespolc-lounge", "Társalgó könyvespolccal, narancssárga kanapéval és növényekkel"), ("zoldfal-oszlopok", "Zöldfal öntöttvas oszlopok között")]
    cards = "".join(f'''<article class="ref">{img(ph, alt, sizes="(min-width:768px) 33vw, 100vw")}<h3>{E(n)} <span class="sample">név: minta</span></h3><small>{E(m)}</small><q>{E(q)}</q><small>— {E(w)}</small></article>''' for (ph, alt), (n, m, q, w) in zip(photos, REFS))
    more = "" if not full else "".join(f'<article class="ref">{img(ph, alt, sizes="(min-width:768px) 33vw, 100vw")}<h3>{E(cap)}</h3></article>' for ph, alt, cap in [("bejarat-zold", "Bejárat sűrű növényzettel", "Bejárat, zöld sáv"), ("lobby-ulokkel", "Üvegfalú lobby növényágyásokkal és székekkel", "Lobby, ülőszigetek"), ("atrium-fa", "Átrium fával és növényágyással", "Átrium, egy fa"), ("etkezo-noveny", "Étkező növényekkel", "Étkező"), ("strelicia-allo", "Papagájvirág álló kaspóban", "Strelícia, a tér sarka"), ("folyoso-emberek", "Folyosó fával, emberek beszélgetnek", "Folyosó, egy fa alatt")])
    return f'''<section class="sec" id="referenciak"><div class="wrap"><div class="head"><div><p class="kicker">Akik már ránk bízták a zöldet</p><h2>Irodák, ahol a növény dolgozik</h2></div>{"" if full else '<a class="btn alt" href="referenciak.html">Minden referencia</a>'}</div>
<p class="lede">A fotók a csapat valódi munkái; a nevek és az idézetek az ügyfél anyagáig minták.</p>
<div class="refs">{cards}{more}</div>
<p class="lede" style="margin-top:16px">Google-értékelések: <span class="sample">minta</span> ★★★★★ 4,9 · 23 értékelés — a Google Cégprofil bekötése után valódi.</p></div></section>'''

def silly():
    return f'''<section class="sec"><div class="wrap silly">
{img("kaspok-arcokkal", "Irodai kaspók arcokkal, tárgyaló székek előtt", sizes="(min-width:768px) 50vw, 100vw")}
<div><p class="kicker">Spoiler</p><h2>Nem minden növény akar az irodádban élni</h2><p class="lede">A legtöbb kudarc a katalógusnál kezdődik: szép növény, rossz iroda. Mi a fényből, a klímából és abból indulunk ki, hogy ki mennyit foglalkozik vele — és olyat választunk, ami bírja a légkondit, a kevesebb fényt és a péntek délutánt.</p><a class="btn" href="ajanlat.html">Küldj el 3 fotót az irodáról</a></div>
</div></section>'''

def team():
    return f'''<section class="sec" id="csapat"><div class="wrap"><div class="head"><div><p class="kicker">Kik jönnek</p><h2>Emberek, nem „csapat”</h2></div></div>
<div class="team">{"".join(f'<div class="person"><i>?</i><div><b>{E(n)} <span class="sample">minta</span></b><small>{E(r)}</small><small>{E(d)}</small></div></div>' for n, r, d in TEAM)}</div></div></section>'''

def faq(items=None):
    items = items or FAQ
    return f'''<section class="sec faq" id="gyik"><div class="wrap"><div class="head"><div><p class="kicker">Ezeket kérdeztétek a legtöbbször</p><h2>Kérdések, mielőtt fotóznál</h2></div></div>
{"".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items)}</div></section>'''

def quote_form():
    return f'''<section class="sec" id="ajanlat"><div class="wrap"><div class="head"><div><p class="kicker">Zöld érdekel?</p><h2>Dobd be az iroda fotóit, és visszajelzünk</h2></div></div>
<form class="form" onsubmit="event.preventDefault();alert('Prototípus: az űrlap nem küld. Élesben: ajánlat 2 munkanapon belül.')">
<label>Kapcsolattartó neve<input type="text" name="name" autocomplete="name"></label>
<label>E-mail cím<input type="email" name="email" autocomplete="email"></label>
<label>Telefonszám<input type="tel" name="phone" autocomplete="tel"></label>
<label>Hány ember dolgozik az irodában?<input type="number" name="people" min="1"></label>
<div class="full"><label>Csatolj 3 képet az irodádról<div class="drop">Fotók ide — telefonról is, rendrakás nélkül</div></label></div>
<label class="full">Üzenet<textarea name="message" rows="3" placeholder="Mi zavar most a legjobban? (a csupasz tárgyaló, a haldokló fikusz, a gyakornok…)"></textarea></label>
<div class="full"><button class="btn" type="submit">Ajánlatot kérek</button> <p class="promise">Két munkanapon belül látványterv és ajánlat, a te irodád fotóin. Sürgős? <a href="{PHONE_HREF}">{PHONE}</a></p></div>
</form></div></section>'''

REELS = ["bizdrankazoldet/reel/DdRaPpFsHho", "bizdrankazoldet/reel/Dc_OM9XMM1y", "bizdrankazoldet/reel/Dcv7ruNKDFo", "szendroi_csaba/reel/DdGcqlPtmsn"]
def instagram():
    return f'''<section class="sec" id="instagram"><div class="wrap"><div class="head"><div><p class="kicker">@bizdrankazoldet</p><h2>Ahol a vicc történik</h2></div><a class="btn alt" href="https://www.instagram.com/bizdrankazoldet/">Instagram</a></div>
<div class="ig">{"".join(f'<iframe src="https://www.instagram.com/{r.split("/",1)[1]}/embed/" title="Instagram Reel — {r.split("/")[0]}" loading="lazy" allow="encrypted-media"></iframe>' for r in REELS)}</div>
<p class="lede" style="margin-top:12px">A saját Reelek, beágyazva — az Instagram-fiók a bizonyíték-formátumokat még nem tartalmazza (előtte/utána, gondozási kör, ügyfél irodája); ezek a tervezett következő videók.</p></div></section>'''

# ---------- pages
def hero(photo, alt, kicker, h1, lede, buttons):
    return f'''<section class="hero">{img(photo, alt, "photo", sizes="(min-width:768px) 50vw, 100vw")}<div class="wrap txt"><p class="kicker">{E(kicker)}</p><h1>{E(h1)}</h1><p class="lede">{E(lede)}</p><div class="row">{buttons}</div></div></section>'''

def home():
    return head("Irodai növények — Bízd ránk a zöldet! Tervezés, bérlés, gondozás, örökzöld garanciával", "Irodai növények azoknak, akik már nyírtak ki kaktuszt: tervezés, telepítés és gondozás egy kézben, örökzöld garanciával, ajánlat két munkanapon belül. Budapest.", "index.html") + hero("strelicia-iroda", "Papagájvirágok és zöld növények egy világos irodában, fapadlón", "Irodai növények · Budapest", "Irodai növények azoknak, akik már nyírtak ki kaktuszt", "Ha most vigyorogsz, jó helyen jársz. Az iroda nem trópusi esőerdő — mi olyan növényeket választunk, amelyek bírják a légkondit és a péntek délutánt, és mi is gondozzuk őket. Ami leépül, azt cseréljük.", '<a class="btn" href="ajanlat.html">Küldj el 3 fotót az irodáról</a><a class="btn alt" href="#arak">Nézd meg az árakat</a>') + f'''
{proof_band()}
{offers()}
{silly()}
{guarantee()}
{packages()}
{steps()}
{references()}
{team()}
{instagram()}
{faq()}
{quote_form()}
''' + foot()

def service(slug, title, desc, photo, alt, kicker, h1, lede, blocks, faq_idx):
    return head(title, desc, slug) + hero(photo, alt, kicker, h1, lede, '<a class="btn" href="ajanlat.html">Kérek ajánlatot</a><a class="btn alt" href="arak.html">Árak</a>') + f'''
{proof_band()}
<section class="sec"><div class="wrap"><div class="offers">{"".join(f'<article class="offer">{img(ph, palt, sizes="(min-width:768px) 33vw, 100vw")}<p class="fun">{E(f)}</p><p class="pro">{E(pr)}</p></article>' for (f, pr), (ph, palt) in zip(blocks, [("bejarat-zold", "Bejárat sűrű növényzettel"), ("tarsalgo", "Társalgó növényekkel és székekkel"), ("etkezo-noveny", "Étkező növényekkel")]))}</div></div></section>
{guarantee()}
{faq([FAQ[i] for i in faq_idx])}
{quote_form()}
''' + foot()

PAGES = {
 "index.html": home,
 "irodai-novenyek.html": lambda: service("irodai-novenyek.html", "Irodai növénydekoráció tervezéstől gondozásig — Bízd ránk a zöldet!", "Irodai növénydekoráció: felmérés, tervezés, telepítés és gondozás egy kézben. A csupasz iroda 2018-ban is ciki volt.", "iroda-piros-2", "Iroda piros keretekkel és növénykaspókkal", "Irodai növénydekoráció", "A csupasz iroda már 2018-ban is ciki volt", "A fehér fal, a szürke padló és a sorban álló asztalok nem minimalizmus, hanem üresség. Néhány jól elhelyezett növény már elég, hogy az iroda ne két meeting közti átmeneti hely legyen.",
   [("Spoiler: nem minden növény akar az irodádban élni", "Nem a katalógusból indulunk ki, hanem a fényből, a klímából és abból, hogy ki mennyit foglalkozik vele. Olyat választunk, ami bírja a légkondit és a kevesebb fényt."), ("A pénzügyes otthoni kaspója vs. „ez így összeállt”", "Otthon belefér az impulzus; az irodában rendszerben gondolkodunk: méret, forma, elhelyezés, kaspó — a munkáltatói márka arculatával összehangolva."), ("Kicsi iroda, nagy iroda, tökmindegy", "Nem a négyzetméter dönt, hanem az arány. Egy jól elhelyezett állónövény megnyit egy sarkot; a zöld irányítja a tekintetet, nem elvesz a térből.")], [0, 1, 3, 5]),
 "novenygondozas.html": lambda: service("novenygondozas.html", "Növénygondozás irodáknak — ne a gyakornok locsoljon | Bízd ránk a zöldet!", "Irodai növénygondozás rendszerben: kéthetente vagy hetente, víz, tápanyag, metszés, kártevő-ellenőrzés, örökzöld garanciával. A meglévő növényeidhez is.", "asztalok-kaspok", "Íróasztalok között álló növénykaspók", "Növénygondozás", "Ne a gyakornok locsoljon", "A „majd locsoljuk, amikor eszünkbe jut” — így kezdődik minden növénytragédia. A gondozás rendszer — mint az IT-karbantartás: struktúra, következetesség, felelős.",
   [("Így kezdődik minden növénytragédia", "Először csak elveszíti a formáját, lassabban nő, fakóbb lesz, aztán leépül. Ez az a pont, amikor a növény már nem hozzáad a térhez, hanem ront rajta."), ("Nem csak víz", "Növényvédelem, tápanyag, metszés, tisztítás és az irodai túlélés alapszabályai — minden látogatáson, egy kártyával az asztalon, hogy tudd, mi történt."), ("A meglévő növényeidhez is", "Nem kell újakat venned. Felmérjük, mi menthető, mit cserélünk, és attól a naptól a miénk a felelősség.")], [2, 3, 4, 5]),
 "novenyberles.html": lambda: service("novenyberles.html", "Növénybérlés irodába és rendezvényre — Bízd ránk a zöldet!", "Növénybérlés havidíjjal, gondozással: ha az iroda még formálódik, ha költöztök, ha csak egy rendezvényre kell a zöld. Örökzöld garanciával.", "lobby-narancs", "Recepció narancssárga fotelekkel és növényekkel", "Növénybérlés", "Béreld, amíg a kávéfőző sem végleges", "Ha az iroda még alakul, minden fix döntés gyanús. A bérelt növények együtt változnak az irodával: költözéskor jönnek veletek, rendezvényre egy napra is.",
   [("Nem kötelez el egy még nem létező jövő mellett", "Havidíj, gondozással, csere, ha változik a tér. Ha rájöttök, hogy az open office mégsem akkora szerelem, a növények is átrendezhetők."), ("Rendezvényre", "Egy napra, egy hétre: kihelyezzük, elvisszük. A tér úgy néz ki, mintha mindig is zöld lett volna."), ("Növésben lévő cégnek", "Öt növénnyel kezditek, húsznál tartotok fél év múlva — a csomag nő veletek, a garancia marad.")], [0, 1, 2, 5]),
 "referenciak.html": lambda: head("Referenciák — irodák, ahol a növény dolgozik | Bízd ránk a zöldet!", "Akik már ránk bízták a zöldet: irodák fotókkal, számokkal és egy-egy mondattal az irodavezetőtől. Grofie: 100+ projekt, 10+ év.", "referenciak.html") + hero("zoldfal-oszlopok", "Zöldfal öntöttvas oszlopok között, halszálkás padlón", "Referenciák", "Akik már ránk bízták a zöldet", "Nem logófal: irodák, fotókkal, azzal a mondattal, amit az irodavezető mondott három hónap múlva. A fotók a csapat valódi munkái; a nevek az ügyfél anyagáig minták.", '<a class="btn" href="ajanlat.html">Kérek ajánlatot</a>') + f'''
{proof_band()}{references(True)}{team()}{quote_form()}''' + foot(),
 "arak.html": lambda: head("Árak és folyamat — csomagok „-tól” árakkal | Bízd ránk a zöldet!", "Mennyibe kerül az irodai növény bérléssel és gondozással? Csomagok „-tól” árakkal, ami benne van, a garancia és a négy lépés az ajánlatig.", "arak.html") + hero("konyvespolc-lounge", "Társalgó könyvespolccal, kanapéval és növényekkel", "Árak és folyamat", "Mennyibe kerül, és mi történik utána", "A kategóriában senki nem ír árat. Mi „-tól” árat írunk, és azt is, mi van benne. A pontos szám a te irodádtól függ — két munkanapon belül megkapod.", '<a class="btn" href="ajanlat.html">Kérek ajánlatot</a>') + f'''
{packages(True)}{guarantee()}{steps()}{faq([FAQ[3], FAQ[5], FAQ[2]])}{quote_form()}''' + foot(),
 "rolunk.html": lambda: head("Rólunk — Gourmet Garden Kft. / Grofie, tíz év zöld | Bízd ránk a zöldet!", "A Bízd ránk a zöldet a Grofie (Gourmet Garden Kft.) irodákra szakosodott csapata: tíz év, több mint száz projekt, zöldfalak WELL-minősített irodaházban. Impresszum.", "rolunk.html") + hero("folyoso-emberek", "Folyosó egy fával, emberek beszélgetnek", "Rólunk", "Tíz éve építünk zöldet. Most az irodákra szakosodtunk.", "A Bízd ránk a zöldet a Grofie (Gourmet Garden Kft.) irodai csapata. Zöldfalak, beltéri növényesítés, kertek — több mint száz projekt, köztük egy 57 m²-es zöldfal egy WELL-minősített irodaházban. Ezt a tapasztalatot hoztuk el egy vicces névvel és egy komoly garanciával.", '<a class="btn" href="ajanlat.html">Kérek ajánlatot</a>') + f'''
{proof_band()}{team()}
<section class="sec"><div class="wrap"><div class="head"><div><p class="kicker">Impresszum</p><h2>Ki áll a név mögött</h2></div></div><p class="imp"><b>Gourmet Garden Kft.</b> · Székhely: <span class="sample">minta</span> [a cég székhelye] · Cégjegyzékszám: <span class="sample">minta</span> · Adószám: <span class="sample">minta</span> · Ügyvezető: <span class="sample">minta</span> [név] · E-mail: [minta]@bizdrankazoldet.hu · Telefon: <a href="{PHONE_HREF}">{PHONE}</a> · Márkák: Grofie (zöldfalak), Bízd ránk a zöldet (irodák).</p><p class="lede" style="font-size:15px">A „zöld” nálunk növényt jelent, nem környezetvédelmi állítást: nem ígérünk klímasemleges irodát, csak élő növényeket, amelyek jó kezekben vannak.</p></div></section>
{instagram()}{quote_form()}''' + foot(),
 "ajanlat.html": lambda: head("Ajánlatkérés — 3 fotó, 2 munkanap | Bízd ránk a zöldet!", "Küldj három fotót az irodáról, és két munkanapon belül látványtervet és ajánlatot kapsz a te irodád képein. Telefon: +36 70 850 8888.", "ajanlat.html") + hero("kaspok-arcokkal", "Irodai kaspók arcokkal, tárgyaló székek előtt", "Ajánlatkérés", "Három fotó tőled, két munkanap tőlünk", "Nem kell rendet rakni, nem kell tudni a növények nevét. Fotózd le az irodát, ahogy van; a többi a mi dolgunk.", f'<a class="btn alt" href="{PHONE_HREF}">Inkább hívlak: {PHONE}</a>') + f'''
{quote_form()}{steps()}{faq([FAQ[5], FAQ[3]])}''' + foot(),
}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        out = HERE / name; out.write_text(fn(), encoding="utf-8"); print(f"{name:24s} {out.stat().st_size:6d} bytes")
