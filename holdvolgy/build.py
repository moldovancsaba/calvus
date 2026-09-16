#!/usr/bin/env python3
"""Generate the Holdvölgy 2026 home page in HU and EN from one content source (D8).
Run: python3 holdvolgy/build.py  → writes index.html and en/index.html. No dependencies."""
import pathlib, html
HERE = pathlib.Path(__file__).parent

C = {
 "hu": dict(lang="hu", title="Holdvölgy — tokaji borok Mádról · Év pincészete 2026",
   desc="Holdvölgy borászat, Mád: édes és száraz tokaji borok, 1,8 km-es háromszintes pincelabirintus, borkóstoló élmények. Az Év pincészete 2026.",
   nav=["Birtok","Borok","Látogatás","Borklub","Kapcsolat"], book="Foglalás", cart="Kosár", menu="Menü", close="Bezárás", lang_other=("EN","../holdvolgy/en/index.html"),
   panel_wines=[("Culture","6 puttonyos tokaji aszú"),("Signature","édes birtokválogatás"),("Eloquence","édes szamorodni"),("Vision","száraz birtokválogatás"),("Meditation","száraz furmint"),("Hold and Hollo","a birtok belépő vonala")],
   panel_all="Teljes választék", panel_visits=[("Tokaji aszú kóstoló","6 aszúévjárat · kb. 2 óra"),("Kincskereső — 8 bor","térképes pincelátogatás aszúval · 1,5–2 óra"),("Kincskereső — 6 bor","térképes pincelátogatás · 1,5–2 óra")],
   badge="Év pincészete 2026", h1="A tokaji álmot töltjük pohárba az élet nagy pillanataihoz", hero_alt="A Holdvölgy pincelabirintusa, hordósorok a föld alatt",
   cards=[("Év pincészete 2026","A Holdvölgy elnyerte az Év pincészete elismerést — hagyománytisztelő, de mégis kreatív kísérletezés Mádon.","A birtokról","#birtok","card-ev-pinceszete.webp","Drónfelvétel a mádi birtokról"),
          ("Borkóstoló a föld alatt","Térképes kincskeresés a háromszintes labirintusban, vagy ültetett aszúkóstoló hat évjárattal.","Foglalás","#latogatas","card-pince.webp","A pince oltára, gyertyafényben"),
          ("PreCulture 2025","Szüret előtti előjegyzés 6 puttonyos tokaji aszúra, nyolcéves érleléssel.","Előjegyzés","#borok","preculture-barrel-2025.webp","PreCulture 2025 hordó")],
   band_h="Tokaji borok", band_all="Teljes választék", band_all_short="Mind",
   bottles=[("Culture","6 puttonyos tokaji aszú","27 500 Ft-tól","bottle-culture.webp"),("Signature 2013","édes birtokválogatás","10 000 Ft","bottle-signature-13.webp"),("Eloquence 2014","édes szamorodni","7 000 Ft","bottle-eloquence-14.webp"),("Vision 2021","száraz birtokválogatás","5 500 Ft","bottle-vision-21.webp"),("Meditation 2023","Furmint · Király-dűlő","15 500 Ft","bottle-meditation-23.webp"),("Hold and Hollo Dry","száraz válogatás 2024","4 000 Ft","bottle-hh-dry.webp")],
   dulok_h="Hét dűlő, harminc parcella", dulok_lede="Riolittufa, agyag, zeolit és barna erdőtalaj — minden dűlő más karaktert ad. Minden dűlőhöz a saját kőzete.", dulok_all="Mind a hét dűlő", map_alt="A birtok dűlőinek térképe", rock_missing="kőzetfotó hiányzik",
   dulok=[("Holdvölgy","kvarcit, riolit · száraz és édes","rock-holdvolgy.webp"),("Úrágya","kötött agyag, kvarc · Furmint",None),("Nyulászó","perlit, bentonitos riolit · Sárgamuskotály","rock-nyulaszo.webp"),("Dorgó-tető","perlit, riolittufa · Furmint, Zéta","rock-dorgo.webp"),("Becsek","zeolitos riolittufa, andezit · Hárslevelű, Furmint","rock-becsek.webp"),("Király","vasas riolittufa · Furmint","rock-kiraly.webp"),("Kakasok","zeolitos riolittufa · Furmint",None)],
   nums=[("1,8 km","pincelabirintus"),("3 szint","a föld alatt"),("500 év","pincetörténet")], visit_h="Látogass el Mádra", hours="Vasárnap–csütörtök 10:00–15:00 · péntek–szombat 10:00–17:00", hours_short="Vas–csüt 10–15 · pén–szo 10–17", tunnel_alt="Pincealagút lépcsővel a Holdvölgy pincéjében",
   news_h="Iratkozz fel hírlevelünkre", news_ph="E-mail cím", news_btn="Feliratkozom",
   foot=[("Birtok",["Történet","Dűlők és terroir","Csapat"]),("Borok",["Tokaji aszú","Édes borok","Száraz borok","Hold and Hollo"]),("Látogatás",["Borkóstoló","Experience","Bortrezor","Ajándék"]),("Kapcsolat",["visit@holdvolgy.com","+36 70 391 4643","Instagram · Facebook"])],
   responsible="Fogyaszd felelősséggel a Holdvölgy borokat", proto="Prototípus — Holdvölgy 2026, 3. kapu: kezdőlap. A boltoldalak a 3. fázisban készülnek; a boros linkek ideiglenesen a borsávra mutatnak.",
   age_q="Betöltötted már a 18. életéved?", age_note="Weboldalunkat csak 18 éven felüliek látogathatják.", yes="Igen", no="Nem", hub="Calvus Hub", hub_href="../index.html"),
 "en": dict(lang="en", title="Holdvölgy — Tokaji wines from Mád · Winery of the Year 2026",
   desc="Holdvölgy winery, Mád: sweet and dry Tokaji wines, a 1.8 km three-level cellar labyrinth, tasting experiences. Winery of the Year 2026.",
   nav=["Estate","Wines","Visit","Wine Club","Contact"], book="Book a visit", cart="Cart", menu="Menu", close="Close", lang_other=("HU","../index.html"),
   panel_wines=[("Culture","6 puttonyos Tokaji Aszú"),("Signature","sweet estate selection"),("Eloquence","sweet Szamorodni"),("Vision","dry estate selection"),("Meditation","dry Furmint"),("Hold and Hollo","the estate's entry line")],
   panel_all="All wines", panel_visits=[("Tokaji Aszú tasting","6 Aszú vintages · about 2 hours"),("Treasure hunt — 8 wines","map-guided cellar visit with Aszú · 1.5–2 hours"),("Treasure hunt — 6 wines","map-guided cellar visit · 1.5–2 hours")],
   badge="Winery of the Year 2026", h1="We pour the Tokaji dream into the glass for life's great moments", hero_alt="The Holdvölgy cellar labyrinth, rows of barrels underground",
   cards=[("Winery of the Year 2026","Holdvölgy has been named Winery of the Year — tradition-respecting yet creative experimentation in Mád.","About the estate","#birtok","card-ev-pinceszete.webp","Aerial view of the Mád estate"),
          ("Tasting underground","A map-guided treasure hunt through the three-level labyrinth, or a seated Aszú tasting of six vintages.","Book","#latogatas","card-pince.webp","The cellar altar by candlelight"),
          ("PreCulture 2025","Pre-harvest reservation of 6 puttonyos Tokaji Aszú, aged eight years.","Reserve","#borok","preculture-barrel-2025.webp","PreCulture 2025 barrel")],
   band_h="Tokaji wines", band_all="All wines", band_all_short="All",
   bottles=[("Culture","6 puttonyos Tokaji Aszú","from 27 500 Ft","bottle-culture.webp"),("Signature 2013","sweet estate selection","10 000 Ft","bottle-signature-13.webp"),("Eloquence 2014","sweet Szamorodni","7 000 Ft","bottle-eloquence-14.webp"),("Vision 2021","dry estate selection","5 500 Ft","bottle-vision-21.webp"),("Meditation 2023","Furmint · Király vineyard","15 500 Ft","bottle-meditation-23.webp"),("Hold and Hollo Dry","dry selection 2024","4 000 Ft","bottle-hh-dry.webp")],
   dulok_h="Seven vineyards, thirty parcels", dulok_lede="Rhyolite tuff, clay, zeolite and brown forest soil — every vineyard gives a different character. Each vineyard with its own rock.", dulok_all="All seven vineyards", map_alt="Map of the estate's vineyards", rock_missing="rock photo missing",
   dulok=[("Holdvölgy","quartzite, rhyolite · dry and sweet","rock-holdvolgy.webp"),("Úrágya","bound clay, quartz · Furmint",None),("Nyulászó","perlite, bentonitic rhyolite · Muscat","rock-nyulaszo.webp"),("Dorgó-tető","perlite, rhyolite tuff · Furmint, Zéta","rock-dorgo.webp"),("Becsek","zeolitic rhyolite tuff, andesite · Hárslevelű, Furmint","rock-becsek.webp"),("Király","ferrous rhyolite tuff · Furmint","rock-kiraly.webp"),("Kakasok","zeolitic rhyolite tuff · Furmint",None)],
   nums=[("1.8 km","cellar labyrinth"),("3 levels","underground"),("500 years","of cellar history")], visit_h="Visit us in Mád", hours="Sunday–Thursday 10:00–15:00 · Friday–Saturday 10:00–17:00", hours_short="Sun–Thu 10–15 · Fri–Sat 10–17", tunnel_alt="Cellar tunnel with stairs in the Holdvölgy cellar",
   news_h="Subscribe to our newsletter", news_ph="E-mail address", news_btn="Subscribe",
   foot=[("Estate",["History","Vineyards and terroir","Team"]),("Wines",["Tokaji Aszú","Sweet wines","Dry wines","Hold and Hollo"]),("Visit",["Tasting","Experience","Wine vault","Gifts"]),("Contact",["visit@holdvolgy.com","+36 70 391 4643","Instagram · Facebook"])],
   responsible="Please enjoy Holdvölgy wines responsibly", proto="Prototype — Holdvölgy 2026, gate 3: home page. Shop pages follow in phase 3; wine links point to the wine band for now.",
   age_q="Are you 18 or older?", age_note="This website may only be visited by adults.", yes="Yes", no="No", hub="Calvus Hub", hub_href="../../index.html"),
}
ANCHORS = ["#birtok","#borok","#latogatas","#borklub","#kapcsolat"]

CSS = r"""
*{box-sizing:border-box} html{scroll-behavior:smooth} @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto} *{transition:none!important}}
body{margin:0;background:var(--hv-ground);color:var(--hv-text);font-family:var(--hv-sans);font-stretch:var(--hv-sans-width);font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block} a{color:inherit}
h1,h2,h3{font-family:var(--hv-display);font-weight:400;color:var(--hv-ink);line-height:1.06;margin:0;font-optical-sizing:auto;text-wrap:balance}
.label{font-size:12px;letter-spacing:.14em;text-transform:uppercase}
.wrap{width:min(100% - 32px,1280px);margin-inline:auto} @media(min-width:768px){.wrap{width:min(100% - 80px,1280px)}} @media(min-width:1024px){.wrap{width:min(100% - 160px,1280px)}}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:12px 24px;border:1px solid var(--hv-accent);border-radius:var(--hv-radius);background:var(--hv-accent);color:var(--hv-ink);font:inherit;font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;cursor:pointer;transition:background .15s,border-color .15s,color .15s}
.btn:hover{background:var(--hv-accent-deep);border-color:var(--hv-accent-deep);color:#fff}
.btn-2{background:transparent;color:var(--hv-ink)} .btn-2:hover{background:var(--hv-ink);border-color:var(--hv-ink);color:#fff}
.btn-3{background:transparent;border-color:transparent;color:var(--hv-accent-deep);padding-inline:0} .btn-3:hover{color:var(--hv-ink);background:transparent;border-color:transparent}
.btn-w{background:transparent;border-color:#fff;color:#fff} .btn-w:hover{background:#fff;color:var(--hv-ink);border-color:#fff}
:focus-visible{outline:2px solid var(--hv-accent-deep);outline-offset:3px}
.price{font-weight:500;color:var(--hv-ink);font-variant-numeric:tabular-nums}
.proto{background:var(--hv-accent);color:var(--hv-ink);font-size:12px;font-weight:600;text-align:center;padding:8px 16px;margin:0}
/* header — phone/tablet */
.hd{position:sticky;top:0;z-index:30;background:rgba(250,250,250,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--hv-line-soft)}
.hd .wrap{display:flex;align-items:center;gap:20px;min-height:60px}
.wordmark{font-family:var(--hv-display);font-size:18px;letter-spacing:.18em;color:var(--hv-ink);text-decoration:none;display:inline-flex;align-items:center;min-height:44px}
.hd nav{display:none} .hd .book{display:none}
.hd .right{margin-left:auto;display:flex;align-items:center;gap:10px}
.hd .lang{color:var(--hv-muted);text-decoration:none;display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;padding:0 6px}
.cart{width:44px;height:44px;display:grid;place-items:center;color:var(--hv-ink);text-decoration:none;border:1px solid var(--hv-line);border-radius:var(--hv-radius)}
/* header — desktop */
@media(min-width:1024px){
 .hd .wrap{min-height:88px;gap:28px} .wordmark{font-size:22px}
 .hd nav{display:flex;gap:26px;margin:0 auto} .hd nav>div{position:relative}
 .hd nav a.top{color:var(--hv-text);text-decoration:none;display:inline-flex;min-height:44px;align-items:center;border-bottom:2px solid transparent} .hd nav a.top:hover,.hd nav>div:focus-within a.top{color:var(--hv-ink);border-color:var(--hv-accent)}
 .panel{display:none;position:absolute;top:100%;left:-24px;min-width:340px;background:var(--hv-card);border:1px solid var(--hv-line);padding:18px 24px 20px;box-shadow:0 18px 30px rgba(29,29,27,.08)}
 .hd nav>div:hover .panel,.hd nav>div:focus-within .panel{display:block}
 .panel a{display:flex;justify-content:space-between;gap:20px;align-items:center;min-height:44px;text-decoration:none;color:var(--hv-ink);border-top:1px solid var(--hv-line-soft)} .panel a:first-child{border-top:0} .panel a:hover b{color:var(--hv-accent-deep)}
 .panel b{font-family:var(--hv-display);font-weight:400;font-size:18px} .panel span{font-size:12px;color:var(--hv-muted);text-align:right} .panel .all{margin-top:8px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--hv-accent-deep);border-top:1px solid var(--hv-line-soft);padding-top:12px}
 .hd .book{display:inline-flex} .hd .right{margin-left:0}
}
/* hero — art-directed per device */
.hero{position:relative;height:520px;background:#2b2621;overflow:hidden} .hero picture,.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(29,29,27,0) 40%,rgba(29,29,27,.74) 100%)}
.hero .wrap{position:absolute;left:0;right:0;bottom:28px;z-index:1;color:#fff}
.badge{display:inline-block;margin-bottom:12px;color:#F3EFE8;border:1px solid rgba(255,255,255,.5);padding:6px 10px;font-size:11px}
.hero h1{font-size:34px;color:#fff;max-width:17ch} .hero .row{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px} .hero .row .btn-w{display:none}
@media(min-width:768px){.hero{height:560px} .hero h1{font-size:48px} .hero .wrap{bottom:56px} .hero .row .btn-w{display:inline-flex}}
@media(min-width:1024px){.hero{height:720px} .hero h1{font-size:64px} .hero .wrap{bottom:80px} .badge{padding:8px 14px;font-size:12px;margin-bottom:18px} .hero .row{margin-top:32px}}
/* cards */
.cards{display:grid;gap:8px;padding:16px 0 8px}
.card{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:center;background:var(--hv-card);border:1px solid var(--hv-line-soft);min-height:112px;text-decoration:none}
.card img{width:96px;height:112px;object-fit:cover} .card.fit img{object-fit:contain;background:var(--hv-band)} .card div{padding-right:12px} .card h3{font-size:20px;margin-bottom:4px} .card p{margin:0;font-size:13px;color:var(--hv-muted)} .card p.long,.card .btn-3{display:none}
@media(min-width:768px){.cards{grid-template-columns:1fr 1fr;gap:24px;padding:32px 0 40px} .card{display:block;min-height:0} .card:last-child{grid-column:1/-1} .card img{width:100%;height:300px} .card div{padding:18px 20px 22px} .card h3{font-size:28px;margin-bottom:8px} .card p{font-size:15px;margin-bottom:12px} .card p.short{display:none} .card p.long,.card .btn-3{display:inline-flex} .card p.long{display:block}}
@media(min-width:1024px){.cards{grid-template-columns:repeat(3,1fr);gap:32px;padding:40px 0 56px} .card:last-child{grid-column:auto} .card img{height:453px}}
/* wine band */
.band{background:var(--hv-band);padding:24px 0 22px;margin-top:16px} .band .head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px} .band h2{font-size:26px} .band .head .long{display:none}
.rail{display:flex;gap:16px;overflow-x:auto;padding:8px 0 4px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none} .rail::-webkit-scrollbar{display:none}
.bottle{flex:0 0 140px;scroll-snap-align:start;text-align:center;text-decoration:none} .bottle img{height:170px;width:auto;margin-inline:auto;filter:drop-shadow(0 12px 12px rgba(29,29,27,.14));transition:transform .2s} .bottle:hover img{transform:translateY(-6px)}
.bottle b{display:block;margin-top:10px;font-weight:500;color:var(--hv-ink);font-size:14px} .bottle span{display:block;font-size:11px;color:var(--hv-muted)} .bottle em{font-style:normal;display:block;font-size:14px;margin-top:2px}
@media(min-width:768px){.band{padding:48px 0 56px;margin-top:0} .band h2{font-size:34px} .band .head{margin-bottom:28px} .band .head .short{display:none} .band .head .long{display:inline-flex} .rail{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;overflow:visible;align-items:end} .bottle{flex:none} .bottle img{height:180px} .bottle b{font-size:15px} .bottle span{font-size:12px}}
@media(min-width:1024px){.band{padding:56px 0 64px} .band h2{font-size:40px} .rail{grid-template-columns:repeat(6,1fr);gap:20px}}
/* dűlők */
.dulok{padding:28px 0 8px} .dulok h2{font-size:26px;margin-bottom:10px} .dulok .lede{display:none} .dulok .map{display:none}
.rock{display:grid;grid-template-columns:56px 1fr;gap:12px;align-items:center;min-height:60px;border-top:1px solid var(--hv-line-soft);text-decoration:none} .rock img,.rock i{width:56px;height:56px;object-fit:cover} .rock i{background:var(--hv-band);display:grid;place-items:center;font-style:normal;font-size:9px;color:var(--hv-grey);text-align:center;line-height:1.2;padding:4px}
.rock b{font-family:var(--hv-display);font-weight:400;font-size:19px;color:var(--hv-ink)} .rock span{display:block;font-size:12px;color:var(--hv-muted)} .rock.more{display:none} .dulok .all{margin-top:10px}
@media(min-width:768px){.dulok{padding:64px 0 24px} .dulok h2{font-size:34px} .dulok .lede{display:block;margin:0 0 20px;color:var(--hv-muted);max-width:52ch} .dulok .map{display:block;border:1px solid var(--hv-line-soft);margin-bottom:24px} .rock{grid-template-columns:64px 1fr;gap:14px;padding:9px 0} .rock img,.rock i{width:64px;height:64px} .rock b{font-size:22px} .rock.more{display:grid} .rock:last-of-type{border-bottom:1px solid var(--hv-line-soft)} .dulok .all{display:none}}
@media(min-width:1024px){.dulok{display:grid;grid-template-columns:1fr 1fr;gap:40px;padding:80px 0;align-items:start} .dulok h2{font-size:40px} .dulok .map{margin:0}}
/* visit */
.visit{padding:28px 0 8px} .visit .photo{display:none} .nums{display:flex;justify-content:space-between;margin-bottom:14px;gap:12px} .nums b{display:block;font-family:var(--hv-display);font-weight:400;font-size:30px;color:var(--hv-ink);line-height:1} .nums span{display:block;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--hv-muted);margin-top:4px}
.visit h2{display:none} .visit p{margin:0 0 6px;font-size:14px} .visit .long{display:none} .visit a.tel{color:var(--hv-ink);display:inline-flex;min-height:44px;align-items:center} .visit .btn{width:100%;margin-top:6px}
@media(min-width:768px){.visit{padding:48px 0 64px} .visit .photo{display:block;width:100%;height:420px;object-fit:cover;margin-bottom:28px} .nums{justify-content:flex-start;gap:40px;margin-bottom:22px} .nums b{font-size:48px} .nums span{font-size:12px} .visit h2{display:block;font-size:34px;margin-bottom:14px} .visit p{font-size:15px} .visit .short{display:none} .visit .long{display:block} .visit .btn{width:auto;margin-top:16px}}
@media(min-width:1024px){.visit{display:grid;grid-template-columns:560px 1fr;gap:40px;align-items:center;padding:0 0 80px} .visit .photo{margin:0} .nums b{font-size:56px} .visit h2{font-size:40px}}
/* newsletter + footer */
.news{border-top:1px solid var(--hv-accent);border-bottom:1px solid var(--hv-line);padding:24px 0;display:grid;gap:12px} .news h3{font-size:24px} .news form{display:flex;gap:8px;flex-wrap:wrap} .news input{font:inherit;font-stretch:inherit;min-height:44px;flex:1 1 200px;padding:10px 12px;border:1px solid var(--hv-line);background:var(--hv-card);border-radius:var(--hv-radius)}
@media(min-width:768px){.news{grid-template-columns:1fr auto;align-items:center;padding:28px 0} .news h3{font-size:28px} .news input{width:320px}}
footer{padding:24px 0 96px;font-size:13px;color:var(--hv-muted);display:grid;gap:18px} footer b{display:block;color:var(--hv-ink);font-weight:600;margin-bottom:6px} footer a{display:inline-flex;align-items:center;min-height:44px;color:var(--hv-muted);text-decoration:none;margin-right:14px} footer small{display:block;margin-top:8px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--hv-grey)} footer .cols{display:none}
@media(min-width:768px){footer{padding:40px 0 48px;grid-template-columns:1.4fr 1fr 1fr;gap:32px} footer .cols{display:block} footer a{display:flex;align-items:center;margin:0;min-height:44px;padding:0}}
@media(min-width:1024px){footer{grid-template-columns:1.4fr 1fr 1fr 1fr 1fr}}
/* bottom bar + sheet (phone/tablet) */
.bar{position:fixed;left:0;right:0;bottom:0;z-index:40;display:grid;grid-template-columns:repeat(4,1fr);background:var(--hv-ink);padding-bottom:env(safe-area-inset-bottom)}
.bar a,.bar button{color:#F3EFE8;background:none;border:0;font:inherit;font-size:11px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;min-height:64px;cursor:pointer} .bar .on{color:var(--hv-accent)} .bar i{font-style:normal;font-size:16px}
@media(min-width:1024px){.bar{display:none} footer{padding-bottom:48px}}
dialog{border:0;padding:0;background:transparent;max-width:none;max-height:none} dialog::backdrop{background:rgba(29,29,27,.55)}
.sheet{position:fixed;inset:auto 0 0 0;margin:0;width:100%;background:var(--hv-ground);border-top:1px solid var(--hv-line);padding:8px 16px calc(24px + env(safe-area-inset-bottom));border-radius:var(--hv-radius) var(--hv-radius) 0 0}
.sheet .top{display:flex;justify-content:space-between;align-items:center;min-height:52px} .sheet ul{list-style:none;margin:0;padding:0} .sheet li a{display:flex;align-items:center;min-height:52px;font-family:var(--hv-display);font-size:24px;color:var(--hv-ink);text-decoration:none;border-top:1px solid var(--hv-line-soft)} .sheet .sub a{font-family:var(--hv-sans);font-size:14px;min-height:44px;color:var(--hv-text)}
.sheet .x{background:none;border:1px solid var(--hv-line);border-radius:var(--hv-radius);min-width:44px;min-height:44px;font:inherit;color:var(--hv-ink);cursor:pointer}
.age{margin:auto;width:min(100% - 32px,440px);background:var(--hv-ground);border:1px solid var(--hv-line);padding:32px 28px;text-align:center} .age h2{font-size:28px;margin:12px 0 8px} .age p{color:var(--hv-muted);margin:0 0 20px} .age .row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
"""

def page(c):
    e = html.escape
    nav = "".join(
        f'<div><a class="top label" href="{a}">{e(n)}</a>' +
        (('<div class="panel">' + "".join(f'<a href="#borok"><b>{e(b)}</b><span>{e(s)}</span></a>' for b,s in c["panel_wines"]) + f'<a class="all" href="#borok">{e(c["panel_all"])}</a></div>') if i==1 else
         ('<div class="panel">' + "".join(f'<a href="#latogatas"><b>{e(b)}</b><span>{e(s)}</span></a>' for b,s in c["panel_visits"]) + f'<a class="all" href="#latogatas">{e(c["book"])}</a></div>') if i==2 else '') + '</div>'
        for i,(n,a) in enumerate(zip(c["nav"],ANCHORS)))
    cards = "".join(f'<a class="card{" fit" if img.startswith("preculture") else ""}" href="{href}"><img src="{IMG}{img}" alt="{e(alt)}" width="413" height="462" loading="lazy"><div><h3>{e(t)}</h3><p class="short">{e(t2.split("—")[0].split(".")[0])}</p><p class="long">{e(t2)}</p><span class="btn btn-3">{e(cta)} →</span></div></a>' for t,t2,cta,href,img,alt in c["cards"])
    bottles = "".join(f'<a class="bottle" href="#borok"><img src="{IMG}{img}" alt="{e(n)}" height="720" loading="lazy"><b>{e(n)}</b><span>{e(s)}</span><em class="price">{e(p)}</em></a>' for n,s,p,img in c["bottles"])
    rocks = "".join(f'<a class="rock{" more" if i>=3 else ""}" href="#birtok">' + (f'<img src="{IMG}{img}" alt="" width="256" height="256" loading="lazy">' if img else f'<i>{e(c["rock_missing"])}</i>') + f'<div><b>{e(n)}</b><span>{e(s)}</span></div></a>' for i,(n,s,img) in enumerate(c["dulok"]))
    nums = "".join(f'<div><b>{e(v)}</b><span>{e(l)}</span></div>' for v,l in c["nums"])
    foot = "".join(f'<div class="cols"><b>{e(h)}</b>' + "".join(f'<a href="#">{e(x)}</a>' for x in xs) + '</div>' for h,xs in c["foot"])
    sheet_main = "".join(f'<li><a href="{a}">{e(n)}</a></li>' for n,a in zip(c["nav"],ANCHORS))
    sub = ["Tokaji aszú","Bortrezor","Ajándék","Experience"] if c["lang"]=="hu" else ["Tokaji Aszú","Wine vault","Gifts","Experience"]
    sheet_sub = "".join(f'<li><a href="#">{e(x)}</a></li>' for x in sub)
    alt_lang = "en" if c["lang"]=="hu" else "hu"
    alt_href = "en/index.html" if c["lang"]=="hu" else "../index.html"
    return f"""<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c['title'])}</title>
<meta name="description" content="{e(c['desc'])}">
<link rel="alternate" hreflang="hu" href="https://moldovancsaba.github.io/calvus/holdvolgy/index.html">
<link rel="alternate" hreflang="en" href="https://moldovancsaba.github.io/calvus/holdvolgy/en/index.html">
<link rel="alternate" hreflang="x-default" href="https://moldovancsaba.github.io/calvus/holdvolgy/index.html">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=Archivo:wdth,wght@112.5,400;112.5,500;112.5,600&display=swap">
<link rel="stylesheet" href="{TOK}">
<style>{CSS}</style>
</head>
<body>
<p class="proto">{e(c['proto'])}</p>
<header class="hd"><div class="wrap">
  <a class="wordmark" href="#top">HOLDVÖLGY</a>
  <nav aria-label="{'Fő navigáció' if c['lang']=='hu' else 'Main navigation'}">{nav}</nav>
  <a class="btn btn-2 book" href="#latogatas">{e(c['book'])}</a>
  <div class="right"><a class="lang label" href="{alt_href}" lang="{alt_lang}" hreflang="{alt_lang}">{e(c['lang_other'][0])}</a><a class="cart" href="#borok" aria-label="{e(c['cart'])}">◯</a></div>
</div></header>
<main id="top">
<section class="hero" id="birtok">
  <picture>
    <source media="(max-width: 767px)" type="image/avif" srcset="{IMG}hero-cellar-portrait-780.avif"><source media="(max-width: 767px)" type="image/webp" srcset="{IMG}hero-cellar-portrait-780.webp">
    <source media="(max-width: 1279px)" type="image/avif" srcset="{IMG}hero-cellar-1024.avif"><source media="(max-width: 1279px)" type="image/webp" srcset="{IMG}hero-cellar-1024.webp">
    <source type="image/avif" srcset="{IMG}hero-cellar-1440.avif">
    <img src="{IMG}hero-cellar-1440.webp" alt="{e(c['hero_alt'])}" width="1440" height="659" fetchpriority="high">
  </picture>
  <div class="wrap"><span class="label badge">{e(c['badge'])}</span><h1>{e(c['h1'])}</h1><div class="row"><a class="btn" href="#latogatas">{e(c['book'])}</a><a class="btn btn-w" href="#borok">{e(c['nav'][1])}</a></div></div>
</section>
<section class="wrap cards">{cards}</section>
<section class="band" id="borok"><div class="wrap"><div class="head"><h2>{e(c['band_h'])}</h2><a class="btn btn-3 short" href="#borok">{e(c['band_all_short'])} →</a><a class="btn btn-3 long" href="#borok">{e(c['band_all'])} →</a></div><div class="rail">{bottles}</div></div></section>
<section class="wrap dulok"><img class="map" src="{IMG}dulok-map-1000.webp" alt="{e(c['map_alt'])}" width="1000" height="590" loading="lazy"><div><h2>{e(c['dulok_h'])}</h2><p class="lede">{e(c['dulok_lede'])}</p>{rocks}<p class="all"><a class="btn btn-3" href="#birtok">{e(c['dulok_all'])} →</a></p></div></section>
<section class="wrap visit" id="latogatas"><img class="photo" src="{IMG}visit-tunnel-1120.webp" alt="{e(c['tunnel_alt'])}" width="1120" height="1484" loading="lazy"><div><div class="nums">{nums}</div><h2>{e(c['visit_h'])}</h2><p class="short">{e(c['hours_short'])}</p><p class="long">{e(c['hours'])}</p><p>3909 Mád, Árpád u. 13.</p><p><a class="tel" href="tel:+36703914643">+36 70 391 4643</a> · <a class="tel" href="mailto:visit@holdvolgy.com">visit@holdvolgy.com</a></p><a class="btn" href="mailto:visit@holdvolgy.com">{e(c['book'])}</a></div></section>
<section class="wrap news" id="borklub"><h3>{e(c['news_h'])}</h3><form onsubmit="return false"><input type="email" id="news-email" placeholder="{e(c['news_ph'])}" aria-label="{e(c['news_ph'])}"><button class="btn btn-2" type="submit">{e(c['news_btn'])}</button></form></section>
</main>
<footer class="wrap" id="kapcsolat"><div><span class="wordmark" style="font-size:16px">HOLDVÖLGY</span><p style="margin:8px 0 0">3909 Mád, Árpád u. 13. · Tokaj-Hegyalja</p><p style="margin:4px 0 0"><a href="mailto:visit@holdvolgy.com">visit@holdvolgy.com</a><a href="tel:+36703914643">+36 70 391 4643</a></p><small>{e(c['responsible'])}</small><p style="margin:10px 0 0"><a href="{c['hub_href']}">← {e(c['hub'])}</a></p></div>{foot}</footer>
<nav class="bar" aria-label="{'Alsó navigáció' if c['lang']=='hu' else 'Bottom navigation'}"><a class="on" href="#latogatas"><i>◷</i>{e(c['book'].split(' ')[0])}</a><a href="#borok"><i>▯</i>{e(c['nav'][1])}</a><a href="#borok"><i>◯</i>{e(c['cart'])}</a><button type="button" id="menuBtn"><i>≡</i>{e(c['menu'])}</button></nav>
<dialog class="sheet" id="menu" aria-label="{e(c['menu'])}"><div class="top"><span class="wordmark">HOLDVÖLGY</span><button class="x" type="button" id="menuClose" aria-label="{e(c['close'])}">✕</button></div><ul>{sheet_main}</ul><ul class="sub">{sheet_sub}</ul></dialog>
<dialog class="age" id="age" aria-labelledby="ageQ"><svg width="40" height="40" viewBox="0 0 40 40" aria-hidden="true" style="margin:0 auto"><circle cx="20" cy="20" r="13" fill="none" stroke="#B8A689" stroke-width="1.2"/><circle cx="25" cy="16" r="10" fill="#FAFAFA"/></svg><h2 id="ageQ">{e(c['age_q'])}</h2><p>{e(c['age_note'])}</p><div class="row"><button class="btn" type="button" id="ageYes">{e(c['yes'])}</button><a class="btn btn-2" href="https://www.google.com">{e(c['no'])}</a></div></dialog>
<script>
(function(){{
  var age=document.getElementById('age'),ok=false;
  try{{ok=sessionStorage.getItem('hv-age')==='ok'}}catch(e){{}}
  if(!ok&&age.showModal){{age.showModal();}}
  document.getElementById('ageYes').addEventListener('click',function(){{try{{sessionStorage.setItem('hv-age','ok')}}catch(e){{}} age.close();}});
  var m=document.getElementById('menu');
  document.getElementById('menuBtn').addEventListener('click',function(){{m.showModal();}});
  document.getElementById('menuClose').addEventListener('click',function(){{m.close();}});
  m.addEventListener('click',function(ev){{if(ev.target===m)m.close();}});
  m.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',function(){{m.close();}});}});
}})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    for lang, rel, tok, img in (("hu", "index.html", "assets/tokens.css", "assets/img/"), ("en", "en/index.html", "../assets/tokens.css", "../assets/img/")):
        TOK, IMG = tok, img
        out = HERE / rel; out.parent.mkdir(exist_ok=True)
        out.write_text(page(C[lang]), encoding="utf-8")
        print(f"{rel:14s} {out.stat().st_size:6d} bytes")
