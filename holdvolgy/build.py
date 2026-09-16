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
   cards=[("Év pincészete 2026","A Holdvölgy elnyerte az Év pincészete elismerést — hagyománytisztelő, de mégis kreatív kísérletezés Mádon.","A birtokról","birtok.html","card-ev-pinceszete.webp","Drónfelvétel a mádi birtokról"),
          ("Borkóstoló a föld alatt","Térképes kincskeresés a háromszintes labirintusban, vagy ültetett aszúkóstoló hat évjárattal.","Foglalás","#latogatas","card-pince.webp","A pince oltára, gyertyafényben"),
          ("PreCulture 2025","Szüret előtti előjegyzés 6 puttonyos tokaji aszúra, nyolcéves érleléssel.","Előjegyzés","aszu.html#preculture","preculture-barrel-2025.webp","PreCulture 2025 hordó")],
   band_h="Tokaji borok", band_all="Teljes választék", band_all_short="Mind",
   bottles=[("Culture","6 puttonyos tokaji aszú","27 500 Ft-tól","bottle-culture.webp"),("Signature 2013","édes birtokválogatás","10 000 Ft","bottle-signature-13.webp"),("Eloquence 2014","édes szamorodni","7 000 Ft","bottle-eloquence-14.webp"),("Vision 2021","száraz birtokválogatás","5 500 Ft","bottle-vision-21.webp"),("Meditation 2023","Furmint · Király-dűlő","15 500 Ft","bottle-meditation-23.webp"),("Hold and Hollo Dry","száraz válogatás 2024","4 000 Ft","bottle-hh-dry.webp")],
   dulok_h="Hét dűlő, harminc parcella", dulok_lede="Riolittufa, agyag, zeolit és barna erdőtalaj — minden dűlő más karaktert ad. Minden dűlőhöz a saját kőzete.", dulok_all="Mind a hét dűlő", map_alt="A birtok dűlőinek térképe", rock_missing="kőzetfotó hiányzik",
   dulok=[("Holdvölgy","kvarcit, riolit · száraz és édes","rock-holdvolgy.webp"),("Úrágya","kötött agyag, kvarc · Furmint",None),("Nyulászó","perlit, bentonitos riolit · Sárgamuskotály","rock-nyulaszo.webp"),("Dorgó-tető","perlit, riolittufa · Furmint, Zéta","rock-dorgo.webp"),("Becsek","zeolitos riolittufa, andezit · Hárslevelű, Furmint","rock-becsek.webp"),("Király","vasas riolittufa · Furmint","rock-kiraly.webp"),("Kakasok","zeolitos riolittufa · Furmint",None)],
   nums=[("1,8 km","pincelabirintus"),("3 szint","a föld alatt"),("500 év","pincetörténet")], visit_h="Látogass el Mádra", hours="Vasárnap–csütörtök 10:00–15:00 · péntek–szombat 10:00–17:00", hours_short="Vas–csüt 10–15 · pén–szo 10–17", tunnel_alt="Pincealagút lépcsővel a Holdvölgy pincéjében",
   news_h="Iratkozz fel hírlevelünkre", news_ph="E-mail cím", news_btn="Feliratkozom",
   foot=[("Birtok",["Történet","Dűlők és terroir","Csapat"]),("Borok",["Tokaji aszú","Édes borok","Száraz borok","Hold and Hollo"]),("Látogatás",["Borkóstoló","Experience","Bortrezor","Ajándék"]),("Kapcsolat",["visit@holdvolgy.com","+36 70 391 4643","Instagram · Facebook"])],
   responsible="Fogyaszd felelősséggel a Holdvölgy borokat", proto="Prototípus — Holdvölgy 2026. A boltoldalak a 3. fázisban készülnek; a boros linkek ideiglenesen a kezdőlap borsávjára mutatnak.",
   birtok=dict(
    title="Birtok — Holdvölgy, Mád", desc="A Holdvölgy birtok története 1998-tól, hét első osztályú mádi dűlő a saját kőzetével, szőlőfajták, évjáratok és a csapat.",
    h1="A gondolatok bora", hero_alt="Napfény bújik be a Holdvölgy szőlősorai közé", eyebrow="Birtok",
    vision_h="Vízió", vision="Olyan borokat kívánunk alkotni, amelyek Tokaj történelmi kiválóságával járulnak hozzá életünk meghatározó pillanatainak ünnepléséhez, megidézéséhez.",
    quote="A gondolatok bora ez, mely a tudás, az elvek, a fantázia és a türelem harmóniájában született. A szellemiség és a lélek ötvözte tökéletessé, akárcsak az örök értékeket. Álomszerű élmény, melyet évről évre felelősséggel gondozunk tovább, 500 évvel a legendás tokaji bor születése után is.",
    quote_by="Demkó Pascal", quote_role="alapító tulajdonos", founder_alt="Demkó Pascal, alapító",
    story_h="Történet", story_lede="Egy pár négyzetméteres születésnapi ajándéktól az 1,8 kilométeres pincelabirintusig.",
    timeline=[
     ("1998","Születésnapi ajándék","Az alapító édesanyja felveti, hogy édesapja születésnapjára vehetnének pár négyzetméter szőlőt emlékként ott, ahol a nagyszülőknek volt félholdja. Így kerül sor az első kisebb terület megvásárlására a Dorgó-tetőn.","tl-1998-ajandek.webp"),
     ("2004","A birtok megalakulása","Az első 2,5 hektár megvásárlása után elindul az ültetvények rekultivációja és a technológiai fejlesztés. A kis kapacitású tartályok lehetővé teszik, hogy minden parcelláról és fajtából külön kezelhető mikrotételek készüljenek.","tl-2004-megalakulas.webp"),
     ("2005","Vásárlás a névadó dűlőben","Elkezdődik a birtokvásárlás a Holdvölgy-dűlőben. Ez a terület volt a legnagyobb meglepetés: már akkor is csodás alapanyagot adott száraz és édes borainkhoz egyaránt, változatossága miatt az egyik legértékesebb.","tl-2005-nevado.webp"),
     ("2006","Az első minőségi aszúszüret","Az első minőségi szüret éve, amelyből megfelelő alapanyag került az első 6 puttonyos tokaji aszú évjárathoz. Ekkor kezdődött a borszortiment tudatos felépítése és a pince, a birtokközpont területének megvásárlása.","tl-2006-aszuszuret.webp"),
     ("2007","Kialakul a borportfólió","Ebben az évjáratban már átgondoltan készülnek el a márka ma is elengedhetetlen tételei: az Eloquence, a Meditation, a Signature és az Expression. Egyértelművé válik, hogy nem csak a furmintra kell építeni.","tl-2007-portfolio.webp"),
     ("2011–2013","A borászati épület és a pince","Rendkívül összetett munkálatok során épül és újul meg az 1,8 km hosszú, háromszintes pincelabirintus, amely több lejáraton keresztül közvetlenül kapcsolódik a modern feldolgozóhoz.","tl-2011-epulet.webp"),
     ("2014","Először fogad látogatókat a birtok","Elindulnak a rendhagyó, térképes kincskereső pincetúrák, megnyílik a terasz és a showroom, ahol a hét bármely napján kóstolhatók az aktuális tételek és évjáratok.","tl-2014-showroom.webp"),
     ("2016","Elindul a Trezor program","Az egyedülálló program éveken átívelő, exkluzív élményeket nyújt a bérlőknek, és biztonságos, borbefektetési célú tárolást a hosszú távon gondolkodó borkedvelőknek.","tl-2016-trezor.webp"),
     ("2018","Építészeti díj","A BORD Építész Stúdió által tervezett épületegyüttes bronzérmet szerez az olasz A'Awards nemzetközi építészeti versenyen.","tl-2018-dij.webp"),
     ("2019","Elindul a PreCulture program","Megszületik a Culture aszúk előjegyzési programja: már a szüret évében megrendelhetők a 6 puttonyos tokaji aszú tételek. Az emlékezés bora nyolcéves érlelés után vehető kézbe.","tl-2019-preculture.webp"),
    ],
    dulok_h="Dűlők és terroir", dulok_lede="Hét első osztályú mádi dűlő, harminc parcella. Riolittufa, andezit, kvarcit és perlit — minden dűlőhöz a saját kőzete, a saját kitettsége, a saját fajtái.", map_alt="A birtok dűlőinek térképe",
    f_planted="Telepítés", f_aspect="Kitettség", f_rock="Kőzet", f_grapes="Fajták", rock_missing="kőzetfotó hiányzik",
    dulok=[("Holdvölgy","1965, 2000","D","andezit, kvarcit levéllenyomat, riolittufa","Furmint, Hárslevelű, Kabar, Zéta","rock-holdvolgy"),
           ("Úrágya","1981","NY","riolit, kvarcit","Furmint",None),
           ("Nyulászó","1955, 1979","D","andezit, riolit, kvarcit","Furmint, Hárslevelű, Sárgamuskotály","rock-nyulaszo"),
           ("Dorgó-tető","1990","NY","riolit, kvarcit, perlit","Furmint, Zéta","rock-dorgo"),
           ("Becsek","1978","D, DNY","andezit, riolit","Furmint, Hárslevelű, Kövérszőlő","rock-becsek"),
           ("Király","1992","D","riolit, kvarcit","Furmint","rock-kiraly"),
           ("Kakasok","1982","NY","riolit","Furmint",None)],
    grapes_h="A birtok szőlőfajtái", grapes=["Furmint","Hárslevelű","Sárgamuskotály","Zéta","Kabar","Kövérszőlő"],
    vint_h="Évjáratok",
    vintages=[("2025","A dűlők csendes válaszai egy kiszámíthatatlan, mégis beszédes évre","A tél és a kora tavasz csapadékosabb időszaka megalapozta a talaj vízháztartását, a hűvösebb kezdet lassította a vegetáció indulását. A nyár rendkívüli hősége és csapadékhiánya koncentrált alapanyagot adott, miközben a gyors cukorfelhalmozódás és a magas savtartalom precíz szüreti ütemezést kívánt. Az évjárat feszes szerkezetű száraz borokat és kivételes sav–cukor egyensúlyú édes tételeket hozott, rekord minőségű aszúszemekkel."),
              ("2024","Stratégiaváltás a szüretben","A téli csapadék, az előkészítés és a gondos növényvédelem megakadályozta, hogy a kifejezetten meleg és száraz év nagyobb kárt okozzon a szőlőben. A szüreti menetrendet viszont teljesen átírta: teljes újratervezésre volt szükség."),
              ("2023","Az emberi odaadás és a dűlőkbe vetett hit mindig eredményre vezet","Gondos, lankadatlan figyelem. Tudatos harmóniában létezés a természettel és a szőlővel. A kézi szüret aprólékos megtervezése, precíz válogatás a minőség érdekében. Minden évben ezzel tiszteljük meg a dűlőket, a szőlőt és a készülő borokat."),
              ("2022","Egy nehéz évjárat jutalmai","A 2022-es év minden szempontból a nehézségekről szólt, amit a megszokottól extrém módon eltérő időjárás tovább fokozott. Több gondolkodás és súlyosabb döntések jellemezték az évjáratot; az elsődleges cél az volt, hogy az alapvető tételek megfelelő minőségben készüljenek el."),
              ("2021","Küzdelem az időjárás végleteivel","A 2021-es szüreti ciklus során az időjárás végleteivel kellett szembenéznie a szőlészeti csapatnak. A történelmi, első osztályú mádi dűlők ebben a nehéz évjáratban is bizonyították megbízhatóságukat.")],
    team_h="Csapat", team_note="Portrék a birtoktól érkeznek.",
    team=[("Demkó Pascal","alapító tulajdonos",None),
          ("Jójárt Gergő","birtokigazgató","Egy Holdvölgy tétel esetében nincs véletlen faktor, tisztaság és egyensúly jellemzi a márka borait minden évjáratban."),
          ("Jákób Bianka","főborász","Együttlétezés a természettel, precizitás, kristálytisztaság, éber figyelem. Mindez az alkotás szabadságával párosítva felejthetetlen élményeket ad vendégeinknek és csapatunknak is."),
          ("Erdélyi Károly","szőlész","Gondos figyelem, harmónia a természettel, tudatos tervezés, precíz válogatás. Minden évben ezzel tiszteljük meg a dűlőket és a szőlőt a minőség érdekében."),
          ("Demkó Natália","export","A Holdvölgy visszatérés a gyökereimhez. Egy csoda, amely lehetővé teszi, hogy borainkon keresztül megmutassuk a világnak e borvidék gazdagságát és szépségét."),
          ("Molnár Balázs","pinceélmény-menedzser","A Holdvölgy Birtok egy rejtett kincs Tokaj-Hegyalján, melynek ékkövei a kiváló borok. Ezeket bemutatni nem hivatás, hanem élvezet."),
          ("Körtvélyesi Kornél","pinceélmény-menedzser","A kiváló minőségű borok eleve adottak; én azért vagyok, hogy a látogató egy professzionális környezethez illő, felejthetetlen élményt kapjon."),
          ("Gellén Fruzsina","belföldi értékesítő","Bizalom, állandóság, értékteremtés. Ezek a legfontosabbak számomra, és egyben a Holdvölgy működésének és szellemiségének alapvető mozgatói.")],
    cta_h="Gyere, nézd meg", cta_p="Térképes pincelátogatás a háromszintes labirintusban, a hét minden napján.", cta_btn="Foglalás",
   ),
   aszu=dict(
    title="Tokaji aszú — Culture és PreCulture · Holdvölgy", desc="A Culture 6 puttonyos tokaji aszú: készítés, érlelés, tizenhárom évjárat 2006-tól, a PreCulture előjegyzés és a tokaji örökség.",
    eyebrow="Tokaji aszú", h1="Meghatározó, gazdag, élettel teli", hero_alt="Culture tokaji aszú a pince mélyén",
    intro="A Culture 6 puttonyos tokaji aszú készítésekor nem csak a legkiválóbb aszúszemeket, hanem az első osztályú, klasszifikált dűlők kivételességét, Tokaj gazdag történelmi és kulturális örökségét, a Holdvölgy történetének élettel teli pillanatait és az évjáratok értékeit is palackba zárjuk.",
    make_h="Tokaji aszú készítés", steps=[
      ("Az aszúszem keletkezése","A bogyók héjszövete a szürkepenész hatására megbarnul, és penészbevonat alakul ki, amely száraz, meleg időben vizet szív el a szemekből. Azok ráncolódnak, töppednek: így keletkezik a magas cukortartalmú, kiváló ízű aszúszem."),
      ("Kézi szüret és válogatás","Mindig kézzel, precíz válogatással szüreteljük a botritiszes furmint, hárslevelű és zéta bogyókat. A szelekció már a dűlőkben kezdődik, egy parcellát háromszor-négyszer bejárva. Kizárólag az évjárat legjobb aszúszemei kerülnek a Culture-be."),
      ("Az aszúszemek áztatása","Az aszúszemeket 24–48 órára makulátlan furmintból készült, erjedő alapborba áztatjuk. Dinamikus folyamat: a bogyókból további cukor, sav, színanyag, aroma és íz kerül a borba. Minden évjáratban a 6 puttonyos aszú a cél.")],
    age_h="Tokaji aszú érlelés", ages=[
      ("Hordós érlelés","Aszúink átlagosan 24 hónapot töltenek magyar és francia Seguin Moreau tölgyfahordókban — lényegesen többet a borvidéki 18 hónapos minimumnál. Minden év december 10-én, az Aszú Világnapján a tételek előjegyezhetővé válnak."),
      ("Palackos érlelés","Szűrés után az aszút saját, légfertőtlenített palackozónkban töltjük. Ezután átlagosan 72 hónapot pihen palackban a közel 2 km hosszú, történelmi pincerendszerben."),
      ("Az aszú bevezetése","A Culture tételek a szüret első napjától számítva átlagosan nyolc év múlva érik el azt a beltartalmi minőséget, amellyel egy meghatározó, gazdag és limitált hungarikum kerülhet a pohárba.")],
    wall_h="Culture — 6 puttonyos tokaji aszú", wall_lede="Tizenhárom évjárat 2006-tól. Minden évjáratból korlátozott mennyiség; az árak a birtok webshopjának 2026. szeptemberi árai.",
    wall=[("2006","67 000"),("2007","67 000"),("2008","40 500"),("2009","36 500"),("2010","60 500"),("2011","48 000"),("2012","133 000"),("2013","36 500"),("2014","30 500"),("2015","33 000"),("2016","30 500"),("2017","33 000"),("2018","27 500")],
    cap_h="Időkapszula", cap_lede="Kóstold vissza életed nagy pillanatait!",
    cap="Egy minőségi tokaji aszú véges mennyiségű és megismételhetetlen — mint életünk becsben őrzött pillanatai. Egy aszú akár egy évszázadon át tartja értékét, így legértékesebb emlékeink később is visszaidézhetők egy-egy kortyban, az esemény évében szüretelt gyümölcsből készült palackból.",
    moments=["születés","testvérek","család","diploma","eljegyzés","házasság","siker","generációk"], ring_alt="Gyűrű és aszúpalack — időkapszula",
    gift_h="Ajándék és emlék egy palackban", gift="Nászajándékot keresel? Fontos évfordulónak állítanál emléket? Ajándékozd a közös pillanatok arany albumát egy Culture tokaji aszú formájában — egy palackot, egy előjegyzést, vagy a legfontosabb évek kollekcióját.",
    pre_h="PreCulture — előjegyzés", pre_lede="A Culture aszúk általában a szüretet követő nyolcadik évben kerülnek forgalomba. Hogy a fontos évjáratokat előre biztosíthasd magadnak vagy ajándékba, a tételek már korábban előjegyezhetők. A program minden év december 10-én, az Aszú Világnapján nyílik.",
    pre_years=["2018","2019","2020","2021","2022","2023","2024","2025"], pre_6="6 palack", pre_3="3 palack", pre_btn="Előjegyzés",
    guar_h="Holdvölgy garancia", guar="Történelem, odaadó szakmaiság, kötelesség. A mindenkori aszúévjárat elkészültére a mádi első osztályú, történelmileg klasszifikált dűlők és a Holdvölgy szakmaisága a garancia. Borkészítésünkben nincs véletlen tényező.",
    her_h="Tokaj örökség", her_lede="Tokaj lenyűgöző öröksége és dűlőinek páratlansága.", heritage_alt="Tokaj öröksége",
    heritage=[("miocén","Vitis tokaiensis","A miocén kori ősszőlő levelének lenyomatát Erdőbényén találják meg az 1950-es években."),
      ("III–IV. sz.","A borászat kezdete","A tokaji borászkodás a római korban, a III–IV. században alakul ki; az aszú (azwu) mint borászati fogalom Balassa István kutatásai szerint már korán megjelenik."),
      ("1680","A legősibb bontatlan aszú","A legrégebbi ismert bontatlan tokaji aszú évjárata, a szász királyi pincészetből — páratlan érték."),
      ("1700-as évek","Vinum Regnum, Rex Vinorum","A tokaji híre az arisztokrácia és a királyi udvarok köreiben terjed. „Ez a királyok bora, a borok királya” — XIV. Lajos."),
      ("1737","Az első zárt borvidék","III. Károly rendelete a világon elsőként zárt borvidékké nyilvánítja a térséget; elindul az eredetvédelem."),
      ("1772","Az első dűlőklasszifikáció","A világon először Tokaj-Hegyalján klasszifikálják a dűlőket."),
      ("1867","A második dűlőminősítés","Megerősíti a Mádi-medence minőségi dominanciáját a régióban."),
      ("1972","A század évjárata","A XX. század legkiemelkedőbb évjárata: 1995-ben Nagy Aranyérem Bordeaux-ban, 1996-ban az évszázad bora az Egyesült Államokban."),
      ("2002","Világörökségi helyszín","Az UNESCO felveszi a Tokaji borvidéket a világörökségi listára."),
      ("2006","Az első Holdvölgy évjárat","Elkészül az első Culture 6 puttonyos tokaji aszú; azóta minden évjáratban.")],
   ),
   age_q="Betöltötted már a 18. életéved?", age_note="Weboldalunkat csak 18 éven felüliek látogathatják.", yes="Igen", no="Nem", hub="Calvus Hub", hub_href="../index.html"),
 "en": dict(lang="en", title="Holdvölgy — Tokaji wines from Mád · Winery of the Year 2026",
   desc="Holdvölgy winery, Mád: sweet and dry Tokaji wines, a 1.8 km three-level cellar labyrinth, tasting experiences. Winery of the Year 2026.",
   nav=["Estate","Wines","Visit","Wine Club","Contact"], book="Book a visit", cart="Cart", menu="Menu", close="Close", lang_other=("HU","../index.html"),
   panel_wines=[("Culture","6 puttonyos Tokaji Aszú"),("Signature","sweet estate selection"),("Eloquence","sweet Szamorodni"),("Vision","dry estate selection"),("Meditation","dry Furmint"),("Hold and Hollo","the estate's entry line")],
   panel_all="All wines", panel_visits=[("Tokaji Aszú tasting","6 Aszú vintages · about 2 hours"),("Treasure hunt — 8 wines","map-guided cellar visit with Aszú · 1.5–2 hours"),("Treasure hunt — 6 wines","map-guided cellar visit · 1.5–2 hours")],
   badge="Winery of the Year 2026", h1="We pour the Tokaji dream into the glass for life's great moments", hero_alt="The Holdvölgy cellar labyrinth, rows of barrels underground",
   cards=[("Winery of the Year 2026","Holdvölgy has been named Winery of the Year — tradition-respecting yet creative experimentation in Mád.","About the estate","birtok.html","card-ev-pinceszete.webp","Aerial view of the Mád estate"),
          ("Tasting underground","A map-guided treasure hunt through the three-level labyrinth, or a seated Aszú tasting of six vintages.","Book","#latogatas","card-pince.webp","The cellar altar by candlelight"),
          ("PreCulture 2025","Pre-harvest reservation of 6 puttonyos Tokaji Aszú, aged eight years.","Reserve","aszu.html#preculture","preculture-barrel-2025.webp","PreCulture 2025 barrel")],
   band_h="Tokaji wines", band_all="All wines", band_all_short="All",
   bottles=[("Culture","6 puttonyos Tokaji Aszú","from 27 500 Ft","bottle-culture.webp"),("Signature 2013","sweet estate selection","10 000 Ft","bottle-signature-13.webp"),("Eloquence 2014","sweet Szamorodni","7 000 Ft","bottle-eloquence-14.webp"),("Vision 2021","dry estate selection","5 500 Ft","bottle-vision-21.webp"),("Meditation 2023","Furmint · Király vineyard","15 500 Ft","bottle-meditation-23.webp"),("Hold and Hollo Dry","dry selection 2024","4 000 Ft","bottle-hh-dry.webp")],
   dulok_h="Seven vineyards, thirty parcels", dulok_lede="Rhyolite tuff, clay, zeolite and brown forest soil — every vineyard gives a different character. Each vineyard with its own rock.", dulok_all="All seven vineyards", map_alt="Map of the estate's vineyards", rock_missing="rock photo missing",
   dulok=[("Holdvölgy","quartzite, rhyolite · dry and sweet","rock-holdvolgy.webp"),("Úrágya","bound clay, quartz · Furmint",None),("Nyulászó","perlite, bentonitic rhyolite · Muscat","rock-nyulaszo.webp"),("Dorgó-tető","perlite, rhyolite tuff · Furmint, Zéta","rock-dorgo.webp"),("Becsek","zeolitic rhyolite tuff, andesite · Hárslevelű, Furmint","rock-becsek.webp"),("Király","ferrous rhyolite tuff · Furmint","rock-kiraly.webp"),("Kakasok","zeolitic rhyolite tuff · Furmint",None)],
   nums=[("1.8 km","cellar labyrinth"),("3 levels","underground"),("500 years","of cellar history")], visit_h="Visit us in Mád", hours="Sunday–Thursday 10:00–15:00 · Friday–Saturday 10:00–17:00", hours_short="Sun–Thu 10–15 · Fri–Sat 10–17", tunnel_alt="Cellar tunnel with stairs in the Holdvölgy cellar",
   news_h="Subscribe to our newsletter", news_ph="E-mail address", news_btn="Subscribe",
   foot=[("Estate",["History","Vineyards and terroir","Team"]),("Wines",["Tokaji Aszú","Sweet wines","Dry wines","Hold and Hollo"]),("Visit",["Tasting","Experience","Wine vault","Gifts"]),("Contact",["visit@holdvolgy.com","+36 70 391 4643","Instagram · Facebook"])],
   responsible="Please enjoy Holdvölgy wines responsibly", proto="Prototype — Holdvölgy 2026. Shop pages follow in phase 3; wine links point to the home page's wine band for now.",
   birtok=dict(
    title="Estate — Holdvölgy, Mád", desc="The Holdvölgy estate since 1998: seven first-growth Mád vineyards each with its own rock, the grape varieties, the vintages and the team.",
    h1="The wine of thoughts", hero_alt="Sunlight breaking through the Holdvölgy vine rows", eyebrow="Estate",
    vision_h="Vision", vision="We wish to make wines that, with Tokaj's historic excellence, help celebrate and recall the defining moments of our lives.",
    quote="This is the wine of thoughts, born in the harmony of knowledge, principles, imagination and patience. Spirit and soul made it whole, as they do all lasting values. A dreamlike experience we tend responsibly year after year, five hundred years after the legendary Tokaji wine was born.",
    quote_by="Pascal Demkó", quote_role="founder and owner", founder_alt="Pascal Demkó, founder",
    story_h="History", story_lede="From a few square metres bought as a birthday present to a cellar labyrinth 1.8 kilometres long.",
    timeline=[
     ("1998","A birthday present","The founder's mother suggests buying a few square metres of vineyard for his father's birthday, as a keepsake, where the grandparents once owned a plot. The first small parcel is bought on Dorgó-tető.","tl-1998-ajandek.webp"),
     ("2004","The estate takes shape","After the first 2.5 hectares, the vineyards are restored and the technology built up. Small-capacity tanks allow every parcel and variety to be handled as a separate micro-lot.","tl-2004-megalakulas.webp"),
     ("2005","Buying in the namesake vineyard","Purchases begin in the Holdvölgy vineyard. It was the greatest surprise: even then it gave wonderful fruit for dry and sweet wines alike, and its diversity makes it one of the most valuable sites.","tl-2005-nevado.webp"),
     ("2006","The first quality Aszú harvest","The first harvest of real quality, yielding the fruit for the first 6 puttonyos Tokaji Aszú vintage. The conscious building of the range begins, and the land for the cellar and estate centre is bought.","tl-2006-aszuszuret.webp"),
     ("2007","The portfolio forms","The wines that still define the brand are made deliberately for the first time: Eloquence, Meditation, Signature and Expression. It becomes clear the estate cannot be built on Furmint alone.","tl-2007-portfolio.webp"),
     ("2011–2013","The winery building and the cellar","In exceptionally complex works the 1.8 km, three-level cellar labyrinth is built and restored, connected through several entrances directly to the modern winery.","tl-2011-epulet.webp"),
     ("2014","The estate receives its first visitors","The unconventional map-guided treasure-hunt cellar tours begin; the terrace and the showroom open, where current wines and vintages can be tasted any day of the week.","tl-2014-showroom.webp"),
     ("2016","The Vault programme begins","A unique programme offering tenants exclusive experiences over years, and secure storage for wine as an investment for those who think long term.","tl-2016-trezor.webp"),
     ("2018","Architecture award","The complex designed by BORD Architectural Studio wins bronze at the Italian A'Awards international architecture competition.","tl-2018-dij.webp"),
     ("2019","PreCulture begins","The pre-order programme for the Culture Aszús is born: 6 puttonyos Tokaji Aszú can be ordered in the year of harvest. The wine of remembrance is released after eight years of ageing.","tl-2019-preculture.webp"),
    ],
    dulok_h="Vineyards and terroir", dulok_lede="Seven first-growth Mád vineyards, thirty parcels. Rhyolite tuff, andesite, quartzite and perlite — each vineyard with its own rock, its own exposure, its own varieties.", map_alt="Map of the estate's vineyards",
    f_planted="Planted", f_aspect="Exposure", f_rock="Rock", f_grapes="Varieties", rock_missing="rock photo missing",
    dulok=[("Holdvölgy","1965, 2000","S","andesite, quartzite with leaf imprints, rhyolite tuff","Furmint, Hárslevelű, Kabar, Zéta","rock-holdvolgy"),
           ("Úrágya","1981","W","rhyolite, quartzite","Furmint",None),
           ("Nyulászó","1955, 1979","S","andesite, rhyolite, quartzite","Furmint, Hárslevelű, Muscat","rock-nyulaszo"),
           ("Dorgó-tető","1990","W","rhyolite, quartzite, perlite","Furmint, Zéta","rock-dorgo"),
           ("Becsek","1978","S, SW","andesite, rhyolite","Furmint, Hárslevelű, Kövérszőlő","rock-becsek"),
           ("Király","1992","S","rhyolite, quartzite","Furmint","rock-kiraly"),
           ("Kakasok","1982","W","rhyolite","Furmint",None)],
    grapes_h="The estate's grape varieties", grapes=["Furmint","Hárslevelű","Sárgamuskotály (Muscat)","Zéta","Kabar","Kövérszőlő"],
    vint_h="Vintages",
    vintages=[("2025","The vineyards' quiet answers to an unpredictable, yet eloquent year","A wetter winter and early spring set up the soil's water balance; a cooler start slowed the vines. Extraordinary summer heat and drought gave concentrated fruit, while rapid sugar accumulation and high acidity demanded precise harvest timing. The vintage brought taut, structured dry wines and sweet wines of exceptional sugar–acid balance, with Aszú berries of record quality."),
              ("2024","A change of strategy in the harvest","Winter rainfall, preparation and careful vine protection prevented the markedly hot, dry year from doing greater damage. It rewrote the harvest schedule entirely: a complete re-plan was needed."),
              ("2023","Human devotion and faith in the vineyards always bear fruit","Careful, unflagging attention. Living in conscious harmony with nature and the vine. Meticulous planning of the hand harvest, precise selection for quality. Every year this is how we honour the vineyards, the grapes and the wines to come."),
              ("2022","The rewards of a difficult vintage","2022 was about difficulty in every respect, compounded on the estate by weather far from the usual. More thought and harder decisions marked the year; the first aim was to make the core wines to the right standard."),
              ("2021","A struggle with the extremes of weather","Through the 2021 harvest cycle the vineyard team faced the extremes of the weather. The historic first-growth Mád vineyards proved their reliability even in this difficult year.")],
    team_h="Team", team_note="Portraits to come from the estate.",
    team=[("Pascal Demkó","founder and owner",None),
          ("Gergő Jójárt","estate director","With a Holdvölgy wine there is no element of chance: purity and balance mark the brand's wines in every vintage."),
          ("Bianka Jákób","head winemaker","Coexistence with nature, precision, crystalline purity, alert attention. Paired with the freedom to create, it gives unforgettable experiences to our guests and our team alike."),
          ("Károly Erdélyi","viticulturist","Careful attention, harmony with nature, conscious planning, precise selection. Every year this is how we honour the vineyards and the grapes, for the sake of quality."),
          ("Natália Demkó","export","Holdvölgy is a return to my roots. A wonder that lets us show the world, through our wines, the richness and beauty of this wine region."),
          ("Balázs Molnár","cellar experience manager","The Holdvölgy estate is a hidden treasure of Tokaj-Hegyalja, and its jewels are the wines. Presenting them is not a vocation but a pleasure."),
          ("Kornél Körtvélyesi","cellar experience manager","Wines of outstanding quality are a given; I am here so that the visitor has an unforgettable experience worthy of a professional setting."),
          ("Fruzsina Gellén","domestic sales","Trust, constancy, creating value. These matter most to me, and they are also the fundamental drivers of how Holdvölgy works and thinks.")],
    cta_h="Come and see it", cta_p="A map-guided visit through the three-level labyrinth, every day of the week.", cta_btn="Book a visit",
   ),
   aszu=dict(
    title="Tokaji Aszú — Culture and PreCulture · Holdvölgy", desc="Culture 6 puttonyos Tokaji Aszú: how it is made and aged, thirteen vintages since 2006, the PreCulture en-primeur programme and Tokaj's heritage.",
    eyebrow="Tokaji Aszú", h1="Defining, rich, full of life", hero_alt="Culture Tokaji Aszú deep in the cellar",
    intro="When we make Culture 6 puttonyos Tokaji Aszú we bottle not only the finest Aszú berries but the exceptional character of first-growth classified vineyards, Tokaj's rich historical and cultural heritage, the living moments of Holdvölgy's story and the value of each vintage.",
    make_h="Making Tokaji Aszú", steps=[
      ("How the Aszú berry forms","Under noble rot the berry's skin browns and a coating of mould forms which, in dry warm weather, draws water from the grape. The berries wrinkle and shrivel: the Aszú berry, high in sugar and superb in flavour, is born."),
      ("Hand harvest and selection","Botrytised Furmint, Hárslevelű and Zéta are always picked by hand with precise selection. It begins in the vineyard, walking a parcel three or four times. Only the vintage's finest Aszú berries go into Culture."),
      ("Soaking the Aszú berries","The berries soak for 24–48 hours in a fermenting base wine made from flawless Furmint. It is a dynamic process: further sugar, acid, colour, aroma and flavour pass into the wine. In every vintage the aim is 6 puttonyos.")],
    age_h="Ageing Tokaji Aszú", ages=[
      ("In barrel","Our Aszús spend an average of 24 months in Hungarian and French Seguin Moreau oak — well beyond the region's 18-month minimum. Every year on 10 December, World Aszú Day, the lots open for reservation."),
      ("In bottle","After filtration the Aszú is bottled in our own air-sterilised bottling hall, then rests a further 72 months on average in the nearly 2 km historic cellar system."),
      ("Release","Culture lots reach the quality at which a defining, rich and limited Hungaricum can be poured about eight years from the first day of the Aszú harvest.")],
    wall_h="Culture — 6 puttonyos Tokaji Aszú", wall_lede="Thirteen vintages since 2006. Limited quantities of each; prices are the estate webshop's September 2026 prices.",
    wall=[("2006","67 000"),("2007","67 000"),("2008","40 500"),("2009","36 500"),("2010","60 500"),("2011","48 000"),("2012","133 000"),("2013","36 500"),("2014","30 500"),("2015","33 000"),("2016","30 500"),("2017","33 000"),("2018","27 500")],
    cap_h="Time capsule", cap_lede="Taste your life's great moments again.",
    cap="A fine Tokaji Aszú is finite and unrepeatable — like the treasured moments of our lives. An Aszú holds its value for up to a century, so our most precious memories can be recalled later in a sip, from a bottle made of fruit harvested in the year of the event.",
    moments=["birth","siblings","family","graduation","engagement","wedding","success","generations"], ring_alt="Ring and Aszú bottle — time capsule",
    gift_h="A gift and a memory in one bottle", gift="Looking for a wedding present? Marking an important anniversary? Give the golden album of shared moments in the form of a Culture Tokaji Aszú — one bottle, one reservation, or a collection of the years that matter most.",
    pre_h="PreCulture — en primeur", pre_lede="Culture Aszús are usually released in the eighth year after harvest. So that important vintages can be secured in advance, for yourself or as a gift, lots can be reserved years before release. The programme opens every year on 10 December, World Aszú Day.",
    pre_years=["2018","2019","2020","2021","2022","2023","2024","2025"], pre_6="6 bottles", pre_3="3 bottles", pre_btn="Reserve",
    guar_h="The Holdvölgy guarantee", guar="History, devoted professionalism, duty. The guarantee that each Aszú vintage will be made lies in Mád's first-growth, historically classified vineyards and in Holdvölgy's expertise. There is no element of chance in our winemaking.",
    her_h="Tokaj heritage", her_lede="The astonishing heritage of Tokaj and the singularity of its vineyards.", heritage_alt="Tokaj heritage",
    heritage=[("Miocene","Vitis tokaiensis","The leaf imprint of the Miocene ancestral vine is found at Erdőbénye in the 1950s."),
      ("3rd–4th c.","Winemaking begins","Tokaj winemaking takes shape in the Roman era; the Aszú (azwu) as a winemaking term appears early, per István Balassa's research."),
      ("1680","The oldest unopened Aszú","The oldest known unopened Tokaji Aszú vintage, from the Saxon royal cellar — of unparalleled value."),
      ("1700s","Vinum Regnum, Rex Vinorum","Tokaji's fame spreads through the aristocracy and royal courts. “The wine of kings, the king of wines” — Louis XIV."),
      ("1737","The first closed wine region","A decree of Charles III makes the region the world's first delimited wine region; protection of origin begins."),
      ("1772","The world's first vineyard classification","Tokaj-Hegyalja classifies its vineyards — the first in the world."),
      ("1867","The second classification","Confirms the Mád basin's dominance in quality within the region."),
      ("1972","The vintage of the century","The 20th century's greatest vintage: Grand Gold at Bordeaux in 1995, wine of the century in the United States in 1996."),
      ("2002","World Heritage site","UNESCO inscribes the Tokaj wine region on the World Heritage list."),
      ("2006","The first Holdvölgy vintage","The first Culture 6 puttonyos Tokaji Aszú is made — and in every vintage since.")],
   ),
   age_q="Are you 18 or older?", age_note="This website may only be visited by adults.", yes="Yes", no="No", hub="Calvus Hub", hub_href="../../index.html"),
}
ANCHORS = ["birtok.html","#borok","#latogatas","#borklub","#kapcsolat"]

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
/* ---- birtok page ---- */
.eyebrow{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--hv-accent-deep);margin:0 0 12px}
.sec{padding:40px 0} .sec h2{font-size:26px;margin-bottom:12px} .sec .lede{margin:0 0 20px;color:var(--hv-muted);max-width:60ch}
@media(min-width:768px){.sec{padding:64px 0} .sec h2{font-size:34px}} @media(min-width:1024px){.sec{padding:80px 0} .sec h2{font-size:40px}}
.vision{display:grid;gap:24px} .vision blockquote{margin:0;padding:0 0 0 18px;border-left:2px solid var(--hv-accent)} .vision blockquote p{font-family:var(--hv-display);font-size:20px;line-height:1.35;color:var(--hv-ink);margin:0 0 12px} .vision cite{font-style:normal;display:flex;align-items:center;gap:12px;font-size:13px;color:var(--hv-muted)} .vision cite img{width:56px;height:56px;object-fit:cover;border-radius:50%} .vision cite b{display:block;color:var(--hv-ink);font-weight:500}
@media(min-width:1024px){.vision{grid-template-columns:1fr 1fr;gap:64px;align-items:start} .vision blockquote p{font-size:26px}}
.tl{display:grid;gap:14px} .tl article{display:grid;grid-template-columns:96px 1fr;gap:14px;background:var(--hv-card);border:1px solid var(--hv-line-soft)} .tl img{width:96px;height:100%;min-height:108px;object-fit:cover} .tl div{padding:12px 14px 14px} .tl b{display:block;font-family:var(--hv-display);font-weight:400;font-size:22px;color:var(--hv-accent-deep);line-height:1} .tl h3{font-size:18px;margin:6px 0 6px} .tl p{margin:0;font-size:13px;color:var(--hv-muted)}
@media(min-width:768px){.tl{grid-template-columns:1fr 1fr;gap:24px} .tl article{display:block} .tl img{width:100%;height:220px} .tl div{padding:18px 20px 22px} .tl b{font-size:28px} .tl h3{font-size:22px} .tl p{font-size:14px}}
@media(min-width:1024px){.tl{grid-template-columns:repeat(5,1fr);gap:20px} .tl img{height:200px} .tl h3{font-size:19px} .tl p{font-size:13px}}
.dmap{display:block;border:1px solid var(--hv-line-soft);margin-bottom:20px}
.dl{display:grid;gap:12px} .d{display:grid;grid-template-columns:72px 1fr;gap:14px;background:var(--hv-card);border:1px solid var(--hv-line-soft);padding:12px} .d img,.d i{width:72px;height:72px;object-fit:cover} .d i{background:var(--hv-band);display:grid;place-items:center;font-style:normal;font-size:9px;color:var(--hv-grey);text-align:center;line-height:1.2;padding:4px} .d h3{font-size:22px;margin-bottom:6px} .d dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:2px 10px;font-size:12px} .d dt{color:var(--hv-grey);letter-spacing:.06em;text-transform:uppercase;font-size:10px;padding-top:2px} .d dd{margin:0;color:var(--hv-text)}
@media(min-width:768px){.dl{grid-template-columns:1fr 1fr;gap:20px} .d{grid-template-columns:120px 1fr;padding:16px} .d img,.d i{width:120px;height:120px} .d h3{font-size:24px} .d dl{font-size:13px}}
@media(min-width:1024px){.dmap{margin-bottom:32px} .dl{grid-template-columns:repeat(3,1fr);gap:24px} .d{display:block} .d img,.d i{width:100%;height:220px;margin-bottom:12px} .d i{height:220px}}
.grapes{display:flex;flex-wrap:wrap;gap:8px} .grapes li{list-style:none;font-family:var(--hv-display);font-size:20px;color:var(--hv-ink);border:1px solid var(--hv-line);padding:10px 16px;background:var(--hv-card)} .grapes{padding:0;margin:0} @media(min-width:768px){.grapes li{font-size:24px;padding:12px 20px}}
.vint{display:grid;gap:12px} .vint details{background:var(--hv-card);border:1px solid var(--hv-line-soft)} .vint summary{display:flex;gap:14px;align-items:baseline;min-height:56px;padding:12px 16px;cursor:pointer;list-style:none} .vint summary::-webkit-details-marker{display:none} .vint summary b{font-family:var(--hv-display);font-weight:400;font-size:26px;color:var(--hv-accent-deep)} .vint summary span{font-family:var(--hv-display);font-size:17px;color:var(--hv-ink);line-height:1.25} .vint p{margin:0;padding:0 16px 18px;font-size:14px;color:var(--hv-text);max-width:70ch}
@media(min-width:768px){.vint summary{padding:16px 20px} .vint summary b{font-size:30px} .vint summary span{font-size:20px} .vint p{padding:0 20px 22px 84px;font-size:15px}}
.team{display:grid;gap:12px} .team article{background:var(--hv-card);border:1px solid var(--hv-line-soft);padding:14px 16px} .team b{display:block;font-family:var(--hv-display);font-weight:400;font-size:20px;color:var(--hv-ink)} .team span{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--hv-accent-deep);margin:2px 0 8px} .team p{margin:0;font-size:13px;color:var(--hv-muted)} .team-note{font-size:12px;color:var(--hv-grey);margin:12px 0 0}
@media(min-width:768px){.team{grid-template-columns:1fr 1fr;gap:20px}} @media(min-width:1024px){.team{grid-template-columns:repeat(4,1fr)} .team article{padding:18px 20px}}
.cta{background:var(--hv-band);padding:32px 0} .cta h2{font-size:26px;margin-bottom:8px} .cta p{margin:0 0 16px;color:var(--hv-muted)} @media(min-width:768px){.cta{padding:56px 0} .cta h2{font-size:34px}}
/* ---- aszú page ---- */
.steps{display:grid;gap:12px;counter-reset:st} .steps article{background:var(--hv-card);border:1px solid var(--hv-line-soft);padding:16px;counter-increment:st} .steps article::before{content:counter(st,decimal-leading-zero);display:block;font-family:var(--hv-display);font-size:26px;color:var(--hv-accent-deep);line-height:1;margin-bottom:8px} .steps h3{font-size:19px;margin-bottom:6px} .steps p{margin:0;font-size:13.5px;color:var(--hv-muted)}
@media(min-width:768px){.steps{grid-template-columns:repeat(3,1fr);gap:20px} .steps article{padding:20px} .steps h3{font-size:22px} .steps p{font-size:14px}}
.wall{background:var(--hv-band);padding:28px 0 24px} .wall .rail{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:8px 0 4px;scrollbar-width:none} .wall .rail::-webkit-scrollbar{display:none}
.w{flex:0 0 96px;scroll-snap-align:start;text-align:center;text-decoration:none} .w img{height:150px;width:auto;margin-inline:auto;filter:drop-shadow(0 10px 10px rgba(29,29,27,.14));transition:transform .2s} .w:hover img{transform:translateY(-6px)} .w b{display:block;margin-top:10px;font-family:var(--hv-display);font-weight:400;font-size:18px;color:var(--hv-ink)} .w em{font-style:normal;display:block;font-size:12px;color:var(--hv-ink);font-variant-numeric:tabular-nums}
@media(min-width:768px){.wall{padding:48px 0 40px} .wall .rail{display:grid;grid-template-columns:repeat(7,1fr);gap:16px;overflow:visible;align-items:end} .w{flex:none} .w img{height:170px}}
@media(min-width:1024px){.wall .rail{grid-template-columns:repeat(13,1fr);gap:8px} .w img{height:160px} .w b{font-size:16px} .w em{font-size:11px}}
.cap{display:grid;gap:20px;align-items:center} .cap img{width:160px;margin:0 auto} .cap h3{font-family:var(--hv-display);font-weight:400;font-size:22px;color:var(--hv-ink);margin:0 0 10px} .moments{display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:14px 0 0;list-style:none} .moments li{font-family:var(--hv-display);font-size:17px;color:var(--hv-ink);border:1px solid var(--hv-line);padding:8px 14px;background:var(--hv-card)}
@media(min-width:1024px){.cap{grid-template-columns:260px 1fr;gap:56px} .cap img{width:260px} .cap h3{font-size:28px}}
.pre{display:grid;gap:12px} .pre-row{display:grid;grid-template-columns:1fr 1fr;gap:12px} .pre-y{display:grid;grid-template-columns:repeat(4,1fr);gap:8px} .pre-y a{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:6px;min-height:44px;padding:10px 4px;background:var(--hv-card);border:1px solid var(--hv-line-soft);text-decoration:none;color:var(--hv-ink)} .pre-y img{height:64px;width:auto} .pre-y b{font-family:var(--hv-display);font-weight:400;font-size:17px} .pre-opts{display:flex;gap:10px;flex-wrap:wrap;align-items:center} .pre-opts span{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--hv-muted)}
@media(min-width:768px){.pre-y{grid-template-columns:repeat(8,1fr)} .pre-y img{height:90px}}
.her{display:grid;gap:0;border-top:1px solid var(--hv-line-soft)} .her article{display:grid;grid-template-columns:96px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid var(--hv-line-soft)} .her b{font-family:var(--hv-display);font-weight:400;font-size:18px;color:var(--hv-accent-deep);line-height:1.2} .her h3{font-size:17px;margin-bottom:4px} .her p{margin:0;font-size:13px;color:var(--hv-muted)}
@media(min-width:768px){.her{grid-template-columns:1fr 1fr;gap:0 40px} .her article{grid-template-columns:120px 1fr;padding:16px 0} .her b{font-size:22px} .her h3{font-size:19px} .her p{font-size:14px}}
.guar{background:var(--hv-band);padding:32px 0} .guar h2{font-size:26px;margin-bottom:10px} .guar p{margin:0;max-width:62ch;color:var(--hv-text)} @media(min-width:768px){.guar{padding:56px 0} .guar h2{font-size:34px}}
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

def _common(c):
    e = html.escape
    nav = "".join(
        f'<div><a class="top label" href="{a}">{e(n)}</a>' +
        (('<div class="panel">' + "".join(f'<a href="{"aszu.html" if b=="Culture" else "#borok"}"><b>{e(b)}</b><span>{e(s)}</span></a>' for b,s in c["panel_wines"]) + f'<a class="all" href="#borok">{e(c["panel_all"])}</a></div>') if i==1 else
         ('<div class="panel">' + "".join(f'<a href="#latogatas"><b>{e(b)}</b><span>{e(s)}</span></a>' for b,s in c["panel_visits"]) + f'<a class="all" href="#latogatas">{e(c["book"])}</a></div>') if i==2 else '') + '</div>'
        for i,(n,a) in enumerate(zip(c["nav"],ANCHORS)))
    cards = "".join(f'<a class="card{" fit" if img.startswith("preculture") else ""}" href="{href}"><img src="{IMG}{img}" alt="{e(alt)}" width="413" height="462" loading="lazy"><div><h3>{e(t)}</h3><p class="short">{e(t2.split("—")[0].split(".")[0])}</p><p class="long">{e(t2)}</p><span class="btn btn-3">{e(cta)} →</span></div></a>' for t,t2,cta,href,img,alt in c["cards"])
    bottles = "".join(f'<a class="bottle" href="{"aszu.html" if n=="Culture" else "#borok"}"><img src="{IMG}{img}" alt="{e(n)}" height="720" loading="lazy"><b>{e(n)}</b><span>{e(s)}</span><em class="price">{e(p)}</em></a>' for n,s,p,img in c["bottles"])
    rocks = "".join(f'<a class="rock{" more" if i>=3 else ""}" href="birtok.html#dulok">' + (f'<img src="{IMG}{img}" alt="" width="256" height="256" loading="lazy">' if img else f'<i>{e(c["rock_missing"])}</i>') + f'<div><b>{e(n)}</b><span>{e(s)}</span></div></a>' for i,(n,s,img) in enumerate(c["dulok"]))
    nums = "".join(f'<div><b>{e(v)}</b><span>{e(l)}</span></div>' for v,l in c["nums"])
    foot = "".join(f'<div class="cols"><b>{e(h)}</b>' + "".join(f'<a href="#">{e(x)}</a>' for x in xs) + '</div>' for h,xs in c["foot"])
    sheet_main = "".join(f'<li><a href="{a}">{e(n)}</a></li>' for n,a in zip(c["nav"],ANCHORS))
    sub = [("Tokaji aszú","aszu.html"),("Bortrezor","#"),("Ajándék","aszu.html#ajandek"),("Experience","#")] if c["lang"]=="hu" else [("Tokaji Aszú","aszu.html"),("Wine vault","#"),("Gifts","aszu.html#ajandek"),("Experience","#")]
    sheet_sub = "".join(f'<li><a href="{h}">{e(x)}</a></li>' for x,h in sub)
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
<section class="wrap dulok"><img class="map" src="{IMG}dulok-map-1000.webp" alt="{e(c['map_alt'])}" width="1000" height="590" loading="lazy"><div><h2>{e(c['dulok_h'])}</h2><p class="lede">{e(c['dulok_lede'])}</p>{rocks}<p class="all"><a class="btn btn-3" href="birtok.html#dulok">{e(c['dulok_all'])} →</a></p></div></section>
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

def birtok_main(c):
    e = html.escape; b = c["birtok"]
    tl = "".join(f'<article><img src="{IMG}{img}" alt="" width="413" height="462" loading="lazy"><div><b>{e(y)}</b><h3>{e(t)}</h3><p>{e(p)}</p></div></article>' for y,t,p,img in b["timeline"])
    dl = "".join('<article class="d">' + (f'<img src="{IMG}{r}.webp" srcset="{IMG}{r}.webp 256w, {IMG}{r}-640.webp 640w" sizes="(max-width: 767px) 72px, (max-width: 1023px) 120px, 400px" alt="" width="256" height="256" loading="lazy">' if r else f'<i>{e(b["rock_missing"])}</i>') + f'<div><h3 id="dulo-{i}">{e(n)}</h3><dl><dt>{e(b["f_planted"])}</dt><dd>{e(pl)}</dd><dt>{e(b["f_aspect"])}</dt><dd>{e(asp)}</dd><dt>{e(b["f_rock"])}</dt><dd>{e(rk)}</dd><dt>{e(b["f_grapes"])}</dt><dd>{e(gr)}</dd></dl></div></article>' for i,(n,pl,asp,rk,gr,r) in enumerate(b["dulok"]))
    grapes = "".join(f'<li>{e(g)}</li>' for g in b["grapes"])
    vint = "".join(f'<details{" open" if i==0 else ""}><summary><b>{e(y)}</b><span>{e(t)}</span></summary><p>{e(p)}</p></details>' for i,(y,t,p) in enumerate(b["vintages"]))
    team = "".join(f'<article><b>{e(n)}</b><span>{e(r)}</span>' + (f'<p>„{e(q)}”</p>' if q and c["lang"]=="hu" else f'<p>“{e(q)}”</p>' if q else '') + '</article>' for n,r,q in b["team"])
    return f"""
<section class="hero" id="top-hero">
  <picture>
    <source media="(max-width: 767px)" type="image/avif" srcset="{IMG}hero-vineyard-portrait-780.avif"><source media="(max-width: 767px)" type="image/webp" srcset="{IMG}hero-vineyard-portrait-780.webp">
    <source media="(max-width: 1279px)" type="image/avif" srcset="{IMG}hero-vineyard-1024.avif"><source media="(max-width: 1279px)" type="image/webp" srcset="{IMG}hero-vineyard-1024.webp">
    <source type="image/avif" srcset="{IMG}hero-vineyard-1440.avif">
    <img src="{IMG}hero-vineyard-1440.webp" alt="{e(b['hero_alt'])}" width="1440" height="960" fetchpriority="high">
  </picture>
  <div class="wrap"><span class="label badge">{e(b['eyebrow'])}</span><h1>{e(b['h1'])}</h1></div>
</section>
<section class="wrap sec vision"><div><h2>{e(b['vision_h'])}</h2><p class="lede">{e(b['vision'])}</p></div><blockquote><p>„{e(b['quote'])}”</p><cite><img src="{IMG}founder-pascal.webp" alt="{e(b['founder_alt'])}" width="305" height="200" loading="lazy"><span><b>{e(b['quote_by'])}</b>{e(b['quote_role'])}</span></cite></blockquote></section>
<section class="wrap sec" id="tortenet"><h2>{e(b['story_h'])}</h2><p class="lede">{e(b['story_lede'])}</p><div class="tl">{tl}</div></section>
<section class="wrap sec" id="dulok"><h2>{e(b['dulok_h'])}</h2><p class="lede">{e(b['dulok_lede'])}</p><img class="dmap" src="{IMG}dulok-map-1000.webp" alt="{e(b['map_alt'])}" width="1000" height="590" loading="lazy"><div class="dl">{dl}</div></section>
<section class="wrap sec" id="fajtak"><h2>{e(b['grapes_h'])}</h2><ul class="grapes">{grapes}</ul></section>
<section class="wrap sec" id="evjaratok"><h2>{e(b['vint_h'])}</h2><div class="vint">{vint}</div></section>
<section class="wrap sec" id="csapat"><h2>{e(b['team_h'])}</h2><div class="team">{team}</div><p class="team-note">{e(b['team_note'])}</p></section>
<section class="cta"><div class="wrap"><h2>{e(b['cta_h'])}</h2><p>{e(b['cta_p'])}</p><a class="btn" href="index.html#latogatas">{e(b['cta_btn'])}</a></div></section>
"""

def aszu_main(c):
    e = html.escape; a = c["aszu"]
    steps = lambda xs: "".join(f'<article><h3>{e(t)}</h3><p>{e(p)}</p></article>' for t,p in xs)
    wall = "".join(f'<a class="w" href="#preculture"><img src="{IMG}culture-{y}.webp" alt="Culture {y}" height="560" loading="lazy"><b>{e(y)}</b><em>{e(pr)} Ft</em></a>' for y,pr in a["wall"])
    moments = "".join(f'<li>{e(m)}</li>' for m in a["moments"])
    pre = "".join(f'<a href="index.html#kapcsolat"><img src="{IMG}{"preculture-barrel-2025.webp" if y=="2025" else f"preculture-{y}.webp"}" alt="" loading="lazy"><b>{e(y)}</b></a>' for y in a["pre_years"])
    her = "".join(f'<article><b>{e(y)}</b><div><h3>{e(t)}</h3><p>{e(p)}</p></div></article>' for y,t,p in a["heritage"])
    return f"""
<section class="hero">
  <picture>
    <source media="(max-width: 767px)" type="image/avif" srcset="{IMG}hero-aszu-portrait-780.avif"><source media="(max-width: 767px)" type="image/webp" srcset="{IMG}hero-aszu-portrait-780.webp">
    <source media="(max-width: 1279px)" type="image/avif" srcset="{IMG}hero-aszu-1024.avif"><source media="(max-width: 1279px)" type="image/webp" srcset="{IMG}hero-aszu-1024.webp">
    <source type="image/avif" srcset="{IMG}hero-aszu-1440.avif">
    <img src="{IMG}hero-aszu-1440.webp" alt="{e(a['hero_alt'])}" width="1440" height="760" fetchpriority="high">
  </picture>
  <div class="wrap"><span class="label badge">{e(a['eyebrow'])}</span><h1>{e(a['h1'])}</h1></div>
</section>
<section class="wrap sec"><p class="lede" style="max-width:66ch;font-size:17px;color:var(--hv-text)">{e(a['intro'])}</p></section>
<section class="wrap sec" id="keszites"><h2>{e(a['make_h'])}</h2><div class="steps">{steps(a['steps'])}</div></section>
<section class="wrap sec" id="erleles"><h2>{e(a['age_h'])}</h2><div class="steps">{steps(a['ages'])}</div></section>
<section class="wall" id="culture"><div class="wrap"><h2>{e(a['wall_h'])}</h2><p class="lede">{e(a['wall_lede'])}</p><div class="rail">{wall}</div></div></section>
<section class="wrap sec cap" id="idokapszula"><img src="{IMG}ring-timecapsule.webp" alt="{e(a['ring_alt'])}" width="400" height="400" loading="lazy"><div><h2>{e(a['cap_h'])}</h2><h3>{e(a['cap_lede'])}</h3><p class="lede" style="color:var(--hv-text)">{e(a['cap'])}</p><ul class="moments">{moments}</ul></div></section>
<section class="wrap sec" id="ajandek"><h2>{e(a['gift_h'])}</h2><p class="lede" style="color:var(--hv-text)">{e(a['gift'])}</p></section>
<section class="wrap sec pre" id="preculture"><h2>{e(a['pre_h'])}</h2><p class="lede">{e(a['pre_lede'])}</p><div class="pre-y">{pre}</div><div class="pre-opts"><span>{e(a['pre_6'])} · {e(a['pre_3'])}</span><a class="btn" href="index.html#kapcsolat">{e(a['pre_btn'])}</a></div></section>
<section class="guar"><div class="wrap"><h2>{e(a['guar_h'])}</h2><p>{e(a['guar'])}</p></div></section>
<section class="wrap sec" id="orokseg"><h2>{e(a['her_h'])}</h2><p class="lede">{e(a['her_lede'])}</p><div class="her">{her}</div></section>
"""

def render(c, rel, main_override=None, title=None, desc=None, slug=None):
    doc = _common(c)
    if main_override is not None:
        start = doc.index('<main id="top">') + len('<main id="top">'); end = doc.index('</main>')
        doc = doc[:start] + main_override + doc[end:]
        doc = doc.replace(f"<title>{html.escape(c['title'])}</title>", f"<title>{html.escape(title)}</title>",1)
        doc = doc.replace(f'<meta name="description" content="{html.escape(c["desc"])}">', f'<meta name="description" content="{html.escape(desc)}">',1)
        # hreflang + language switch for this page
        doc = doc.replace('holdvolgy/index.html">',f'holdvolgy/{slug}.html">').replace('holdvolgy/en/index.html">',f'holdvolgy/en/{slug}.html">')
        doc = doc.replace('href="en/index.html" lang="en"',f'href="en/{slug}.html" lang="en"').replace('href="../index.html" lang="hu"',f'href="../{slug}.html" lang="hu"')
        # in-page anchors that live on the home page must point back to it
        doc = doc.replace('href="#borok"','href="index.html#borok"').replace('href="#latogatas"','href="index.html#latogatas"').replace('href="#borklub"','href="index.html#borklub"').replace('href="#kapcsolat"','href="index.html#kapcsolat"')
    out = HERE / rel; out.parent.mkdir(exist_ok=True); out.write_text(doc, encoding="utf-8")
    print(f"{rel:16s} {out.stat().st_size:6d} bytes")

if __name__ == "__main__":
    for lang, rel, tok, img in (("hu", "index.html", "assets/tokens.css", "assets/img/"), ("en", "en/index.html", "../assets/tokens.css", "../assets/img/")):
        TOK, IMG = tok, img
        render(C[lang], rel)
        b = C[lang]["birtok"]
        render(C[lang], rel.replace("index.html","birtok.html"), main_override=birtok_main(C[lang]), title=b["title"], desc=b["desc"], slug="birtok")
        a = C[lang]["aszu"]
        render(C[lang], rel.replace("index.html","aszu.html"), main_override=aszu_main(C[lang]), title=a["title"], desc=a["desc"], slug="aszu")
