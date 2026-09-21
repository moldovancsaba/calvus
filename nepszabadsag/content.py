"""Content for the Népszabadság prototype — one source, read by build.py.

Provenance, per item: "figma" = headline/dek/byline/body copied verbatim from the client's
own Figma file (RVrEZZJdxBZdiZs2MJrJUD), read on screen 2026-09-21 — real, client-authored
content, not invented here. "original" = written for this prototype because the Figma file
did not specify content for that nav category (Sport, Tudomány) or that slot; neutral,
evergreen, no real named official quoted, declared as sample in 03-sources.md.

Every image is a real photograph from Wikimedia Commons, downloaded and resized for the
web (originals were 1-15 MB; kept at both < 1200 px and > 70 kB JPEG quality here). Where a
photo illustrates a topic rather than showing the article's own (fictional) subject, that is
on record in IMAGES[*]["note"] — carried into the page as the photo credit line, matching the
Figma's own "Fotó: NÉV / Népszabadság" convention.

Author avatars are a designed initials-mark (AUTHORS[*]["avatar_color"]), not a photograph —
Wikimedia Commons has no suitable stock of generic, anonymous portraits, and inventing a
"real" face for a fictional byline would misattribute a real person's likeness. AD_CREATIVES
are sample banner-ad content for the Figma's ad-slot placements: three fictional advertisers
invented for this prototype, not a real commercial relationship — declared as sample in
03-sources.md.
"""

IMAGES = {
    "belfold-hero": dict(file="belfold-hero.jpg", credit="Teemeah / Wikimedia Commons",
        license="CC BY-SA 4.0", alt="Vidéki városháza épülete",
        note="illusztráció — nem a cikkben leírt konkrét dunántúli kisváros"),
    "haziorvosi": dict(file="haziorvosi.jpg", credit="Czimmy / Wikimedia Commons",
        license="CC BY-SA 3.0", alt="Kórházépület homlokzata"),
    "kozlekedes": dict(file="kozlekedes.jpg", credit="Antal Gertheis / Wikimedia Commons",
        license="CC BY-SA 4.0", alt="HÉV-állomás peronja"),
    "gazdasag-ipar": dict(file="gazdasag-ipar.jpg", credit="Marek Ślusarczyk / Wikimedia Commons",
        license="CC BY 3.0", alt="Autógyári összeszerelő sor",
        note="illusztráció — külföldi üzem"),
    "gazdasag-megtakaritas": dict(file="gazdasag-megtakaritas.jpg", credit="Egrian / Wikimedia Commons",
        license="közkincs", alt="A Magyar Nemzeti Bank épülete"),
    "kultura": dict(file="kultura.jpg", credit="KovacsDaniel / Wikimedia Commons",
        license="CC BY-SA 3.0", alt="Kiállítótér a Szépművészeti Múzeumban",
        note="illusztráció — nem a cikkben szereplő galéria"),
    "kulfold": dict(file="kulfold.jpg", credit="Steven Lek / Wikimedia Commons",
        license="CC BY-SA 4.0", alt="Az Európai Parlament épülete, Brüsszel"),
    "sport": dict(file="sport.jpg", credit="OD Pictures / Wikimedia Commons",
        license="CC BY-SA 4.0", alt="A Puskás Aréna",
        note="illusztráció — nem a cikkben leírt mérkőzés helyszíne"),
    "tudomany": dict(file="tudomany.jpg", credit="Szilas / Wikimedia Commons",
        license="közkincs", alt="A Piszkéstetői Obszervatórium kupolája"),
    "lead-visszateres": dict(file="lead-visszateres.jpg", credit="közkincs, 1819",
        license="közkincs", alt="Történeti nyomdagép-metszet",
        note="szimbolikus illusztráció a lap visszatéréséhez"),
}

AUTHORS = {
    "kovacs_anna": dict(name="Kovács Anna", beat="Belpolitika", avatar_color="#1d4fd7",
        bio="Belpolitikai újságíró, önkormányzati és költségvetési témákkal foglalkozik."),
    "varga_tamas": dict(name="Varga Tamás", beat="Közlekedés", avatar_color="#2f6f4f"),
    "toth_akos": dict(name="Tóth Ákos", beat="Riport", avatar_color="#8a3324"),
    "szabo_marton": dict(name="Szabó Márton", beat="Gazdaság", avatar_color="#3c4858"),
    "nagy_eszter": dict(name="Nagy Eszter", beat="Kultúra, vélemény", avatar_color="#6a3f6b"),
    "fodor_marton": dict(name="Fodor Márton", beat="Gazdaság", avatar_color="#8a6d1d"),
    "szerkesztoseg": dict(name="Szerkesztőség", beat="", avatar_color="#6b6b6b"),
    "mti": dict(name="MTI", beat="", avatar_color="#6b6b6b"),
}

NAV = ["Belföld", "Külföld", "Gazdaság", "Kultúra", "Sport", "Tudomány"]

# Sample ad creative for the ad slots the Figma marks as banner placements. Fictional
# advertisers, invented for this prototype only — declared as sample in 03-sources.md.
AD_CREATIVES = {
    "utazas": dict(brand="Városnéző Utazási Iroda", bg="#1c3b57",
        headline="Fedezd fel Európát",
        sub="Foglalj most — akár 30%-kal olcsóbban a nyári utakra.",
        cta="Ajánlatok megtekintése"),
    "otthon": dict(brand="Otthon Trend", bg="#6b4a2f",
        headline="Újítsd meg az otthonod",
        sub="Tavaszi akció — akár 20% kedvezmény a válogatott bútorokra.",
        cta="Megnézem az ajánlatot"),
    "penzugy": dict(brand="Takarék Plusz", bg="#1f5c3f",
        headline="Kezdj el megtakarítani",
        sub="0 Ft számlavezetési díj az első évben, online számlanyitással.",
        cta="Számlanyitás indítása"),
}

# The one full Cikkoldal demo article — every word of the free-to-read portion is the
# client's own Figma copy (read on screen 2026-09-21); nothing was invented to extend it,
# because the Figma frame itself ends exactly where the paywall box begins.
CIKKOLDAL = dict(
    source="figma",
    slug="onkormanyzatok-fejlesztesi-keret",
    rovat="Belföld", tag="ELEMZÉS",
    headline="Az önkormányzatok fele nem tudta elkölteni a tavalyi fejlesztési keretet",
    dek="A keretek nagy része év közben szabadul fel, a pályázati kiírások viszont csak "
        "ősszel jelentek meg — a polgármesterek szerint ez a sorrend a probléma.",
    author="kovacs_anna", date="2026. október 8.", reading="4 perc olvasás",
    image="belfold-hero",
    photo_caption="Felújítás alatt álló főtér egy dunántúli kisvárosban. Fotó: Teemeah / Wikimedia Commons",
    related_pills=["Az újraindítás", "A szerkesztőség", "Tíz év után"],
    body=[
        "A fejlesztési keretek elköltésének határideje minden évben december 31-e. "
        "Az önkormányzati szövetségek szerint a határidő önmagában nem szoros — a gond az, "
        "hogy a keret és a kiírás ritkán esik egybe.",
        "A megkérdezett polgármesterek közül többen ugyanazt mondták: a közbeszerzés "
        "átfutási ideje nem fér bele abba az ablakba, ami a kiírás és az év vége között marad.",
        "@AD@600x250",
        "A kisebb településeken ehhez jön a kapacitás kérdése is. Ahol egy fő viszi a "
        "pályázatokat, ott a párhuzamos kiírások egyszerűen kimaradnak.",
    ],
    paywall_bullets=[
        "Mit mondanak a kormányhivatalnok a visszaélési kérelmekről?",
        "Hol torlódik össze a közbeszerzés és a pályázati naptár?",
        "Melyik két megye csinálta másképp, és mit változtattak?",
    ],
    topic_pills=["Önkormányzatok", "Költségvetés", "Közbeszerzés", "Vidékfejlesztés"],
    related=["haziorvosi-ellatas", "buszhalozat", "lakossagi-megtakaritas"],
)

# Every other real headline/dek/byline read directly off the Figma frames (Címlap, Rovatfront)
# — "figma" source. Sport and Tudomány have no Figma frame content, so those two cards are
# "original": written for this prototype, neutral and evergreen.
ARTICLES = {
    "haziorvosi-ellatas": dict(source="figma", rovat="Belföld",
        headline="A kistelepülések háziorvosi ellátásáról szóló vita újraindult",
        dek="A praxisközösségek harmadik éve működnek, a lefedettség viszont nem javult ott, ahol a legnagyobb a hiány.",
        author="kovacs_anna", time="09:30", reading="6 PERC", image="haziorvosi"),
    "buszhalozat": dict(source="figma", rovat="Belföld",
        headline="Hat megyében változik a buszhálózat téli rendje",
        dek=None, author="varga_tamas", time="08:10", reading="3 PERC", image="kozlekedes"),
    "balaton-vonalak": dict(source="figma", rovat="Közlekedés",
        headline="Új menetrend jön a Balaton körüli vonalakon",
        dek=None, author="varga_tamas", time="tegnap", reading="2 PERC", image="kozlekedes"),
    "miniszteri-egyeztetes": dict(source="figma", rovat="Külföld",
        headline="Elhalasztották a jövő heti miniszteri egyeztetést",
        dek=None, author="mti", time="14:05", reading="1 PERC", image="kulfold"),
    "hagyatek-kiallitas": dict(source="figma", rovat="Kultúra",
        headline="Húsz év után újra kiállítják a teljes hagyatékot",
        dek=None, author="nagy_eszter", time="09:30", reading="5 PERC", image="kultura"),
    "ipari-termeles": dict(source="figma", rovat="Gazdaság",
        headline="Lassult az ipari termelés, a feldolgozóipar húzta le a mutatót",
        dek="A megrendelésállomány két negyedéve csökken, a bővítések viszont nem álltak le.",
        author="szabo_marton", date="2026. október 8.", reading="3 PERC", image="gazdasag-ipar"),
    "hetilap-visszaterese": dict(source="figma", rovat="Média", tag="VÉLEMÉNY",
        headline="A hetilap visszatérése és ami utána jön",
        dek="Egy márkanevet visszahozni könnyebb, mint egy olvasói szokást.",
        author="nagy_eszter", date="2026. október 8.", reading="7 PERC", image="lead-visszateres"),
    "logisztikai-piac": dict(source="figma", rovat="Gazdaság",
        headline="Új szereplő lépett be a hazai logisztikai piacra",
        dek=None, author="szabo_marton", date="2026. október 8.", reading="4 PERC", image="gazdasag-ipar"),
    "szinhaz-evad": dict(source="figma", rovat="Kultúra",
        headline="A vidéki színházak évadja: kevesebb bemutató, hosszabb szériák",
        dek="A társulatok a kockázatot csökkentik, a nézőszám viszont nem követi automatikusan.",
        author="nagy_eszter", date="2026. október 8.", reading="7 PERC", image="kultura"),
    "fotografia-seregszemle": dict(source="figma", rovat="Kultúra",
        headline="Kortárs magyar fotográfia a jövő heti seregszemlén",
        dek=None, author="nagy_eszter", date="2026. október 8.", reading="1 PERC", image="kultura"),
    "lakossagi-megtakaritas": dict(source="figma", rovat="Gazdaság",
        headline="Mire elég a lakossági megtakarítás, ha a hozamok csökkennek?",
        dek="A háztartások megtakarítási hajlandósága nem esett vissza, az összetétel viszont átrendeződött.",
        author="fodor_marton", date="2026. október 8.", reading="4 PERC", image="gazdasag-megtakaritas"),
    "sport-nb2": dict(source="original", rovat="Sport",
        headline="Idegenbeli döntetlennel zárta a fordulót a Tiszavirág FC",
        dek="Az NB II-es Tiszavirág FC 1–1-es döntetlent játszott vasárnap a Bakonyalja SE otthonában.",
        author="szerkesztoseg", date="2026. október 8.", reading="2 PERC", image="sport"),
    "tudomany-talaj": dict(source="original", rovat="Tudomány",
        headline="Magyar kutatók a talaj vízmegtartó képességének javításáról publikáltak új eredményt",
        dek="A módszer a szárazabb nyarak idején is csökkentheti a mezőgazdasági területek öntözési igényét.",
        author="szerkesztoseg", date="2026. október 8.", reading="3 PERC", image="tudomany"),
}

# The Belföld rovatfront (the only rovat the Figma file designed) — real content.
ROVATFRONT = dict(
    source="figma", rovat="Belföld",
    description="Önkormányzatok, közigazgatás, egészségügy és oktatás — ami a településeken "
                 "valóban eldől. Napi tudósítás és heti terepmunka.",
    pills=["Önkormányzatok", "Költségvetés", "Egészségügy", "Oktatás", "Közbeszerzés"],
    lead=dict(headline="Ahol a fejlesztési keret elfogyott, mielőtt megérkezett",
              dek="Hat megye, huszonnégy polgármester, egyetlen közös mondat: a pénz megvolt, az idő nem.",
              author="toth_akos", reading="21 PERC", image="belfold-hero"),
    list=["haziorvosi-ellatas", "buszhalozat", "balaton-vonalak", "miniszteri-egyeztetes"],
    authors=["kovacs_anna", "varga_tamas", "toth_akos", "szabo_marton", "nagy_eszter", "fodor_marton"],
)

LEAD = dict(source="figma",
    headline="Tíz év csend után újra megjelenik a Népszabadság",
    dek="A hetilap október 8-án kerül az újságosokhoz, az online kiadás ugyanaznap reggel "
        "indul. A szerkesztőség a lap megszűnésének tizedik évfordulóján kezdi meg a munkát.",
    reading="6 PERC", image="lead-visszateres",
    teasers=[
        ("Ki írja majd a lapot? A szerkesztőség névsora", None),
    ],
)

QUOTE = dict(
    text="A Népszabadság beszántása nem gazdasági, hanem egyértelműen politikai döntés "
         "volt. A magyar sajtótörténetben ez mérföldkő, sajnos a legrosszabb értelemben.",
    by="Török Gábor", role="2016, Index",
)

FOOTER_ROVATOK = NAV
FOOTER_LAPROL = ["Impresszum", "Etikai kódex", "A szerkesztőség"]
FOOTER_JOGI = ["Kapcsolat", "Adatvédelmi tájékoztató", "Előfizetési feltételek", "RSS"]
COPYRIGHT = "© 2026 Liberty Press Kft. Minden jog fenntartva."

REGISTRATION_BAND = dict(
    text="November 15-ig ingyenes regisztrációval minden cikk teljes egészében olvasható.",
    button="Regisztrálok",
)
PAYWALL = dict(
    heading="A cikk folytatása regisztrációhoz kötött",
    register="Ingyenes regisztráció",
    subscribe="Print+online előfizetés — 3 290 Ft",
    login="Már van fiókom — belépés",
    note="November 15-től a fal mögötti tartalom élő előfizetéssel olvasható.",
)

# The landing page — the client's memo (nsz_landing_20260914_v1.docx), copy as written.
LANDING = dict(
    launch_iso="2026-10-08T08:00:00+02:00",
    registration=dict(
        eyebrow="Előfizetés",
        h1="Indul az elő-regisztráció!",
        lead="Legyél Te is tagja közösségünknek! Értesülj elsőként az újraindulás "
             "részleteiről, kedvezményes előfizetési lehetőségekről. Hírlevelek, "
             "exkluzív tartalmak, regisztrálj még ma!",
        fields=["Vezetéknév", "Keresztnév", "E-mail cím"],
        button="Regisztrálok!",
    ),
    countdown=dict(
        h1="Lassan véget ér 10 év hallgatás",
        lead="Online, megújult formában, de a megszokott szakmai elhivatottsággal, "
             "kompromisszumok nélkül indul újra a Népszabadság napilap.",
    ),
    mission=dict(
        h1="Megújul a Népszabadság!",
        paragraphs=[
            "Azok napilapja, akiknek fontos a társadalmi szolidaritás, a tények tisztelete "
            "és a független újságírás.",
            "Tíz évig tartott a csend — ez idő alatt a médiakörnyezet gyökeresen "
            "átalakult, de a szakmai elhivatottság, amivel ezt a munkát végezni "
            "szeretnénk, nem változott.",
            "Független, alapos, a tényekhez ragaszkodó újságírás, amely nem hátrál meg, "
            "ha egy témát kényelmetlennek talál valaki.",
            "A Belföld, a Külföld, a Gazdaság, a Kultúra, a Sport és a Tudomány "
            "rovatainkban ugyanolyan gonddal dolgozunk majd, mint ahogyan azt egy nagy "
            "múltú napilaptól elvárható.",
            "A bizalmat nem lehet egyetlen lapszámmal visszaszerezni — azt minden egyes "
            "nappal újra ki kell érdemelni.",
        ],
    ),
    szerkesztoseg=dict(
        h1="A Szerkesztőség",
        lead="Itt az utolsó poszt borítóképe és címe jelenjen meg mindig.",
        placeholder="A szerkesztőség legutóbbi bejegyzése — a forrás megerősítésére vár "
                     "(03-sources.md, 4. pont).",
    ),
)
