# Népszabadság — handover: where the project stands on 2026-09-21

*Written for whoever picks the project up next — a colleague, a new session, the owner
from a phone. Everything below was read or measured on 2026-09-21; nothing is assumed.
Where something could not be read, it says so and says what unlocks it.*

## 1. What the project is

The relaunch of **Népszabadság**, the daily closed in October 2016, as an online paper
with a weekly print edition, launching **2026-10-08 at 08:00** — "Lassan véget ér 10 év
hallgatás". Two deliverables are in scope:

1. **A landing page before launch** (`nsz_landing_20260914_v1.docx`, received 2026-09-21):
   pre-registration with a countdown to the launch. The memo's own section list, verbatim:

   | Section | Content the memo gives | State in the memo |
   |---|---|---|
   | Regisztráció | HL "Indul az elő-regisztráció!", lead ("Legyél Te is tagja közösségünknek! Értesülj elsőként az újraindulás részleteiről, kedvezményes előfizetési lehetőségekről. Hírlevelek, exkluzív tartalmak, regisztrálj még ma!"), fields Vezetéknév · Keresztnév · email, button "Regisztrálok!" | build |
   | Visszaszámláló | HL "Lassan véget ér 10 év hallgatás", lead ("Online, megújult formában, de a megszokott szakmai elhivatottsággal, kompromisszumok nélkül indul újra a Népszabadság napilap."), countdown to 2026-10-08 08:00 | build |
   | Mission | HL "Megújul a Népszabadság!" + five paragraphs of the paper's creed ("Azok napilapja, akiknek fontos a társadalmi szolidaritás…") | build, copy as written |
   | Program | — | **"egyelőre rejtsük el"** — hidden for now |
   | Idézet | "A nap idézete": Török Gábor, 2016, Index — "A Népszabadság beszántása nem gazdasági, hanem egyértelműen politikai döntés volt. A magyar sajtótörténetben ez mérföldkő, sajnos a legrosszabb értelemben." | build |
   | A Szerkesztőség | "Itt az utolsó poszt borítóképe és címe jelenjen meg mindig" — the latest post's cover and title, always | build; needs the post source |
   | Kérdőív | — | **"egyelőre rejtsük el"** — hidden for now |

2. **The site itself**, designed in Figma (file "Népszabadság",
   `RVrEZZJdxBZdiZs2MJrJUD`), eight frames on one page: **Címlap**, **Rovatfront**,
   **Cikkoldal**, **Népszava márkafront** — each as desktop (1480 wide, "1920w light"
   grid) and mobile. What each frame contains is in §3.

The owner's ask (2026-09-21): research the greatest and most popular news sites — the
best US, German, UK, Asian, Chinese and Hungarian — structure, layout, colours,
everything; then build the project the way Holdvölgy was built (research, audit, design
system, frames, generated pages, gate, presentation). The owner's follow-up the same
hour: *"I hope you started with a deep market research."* — the research is the first
deliverable, before any page.

## 2. The name — one thing to settle before the URL goes live

The owner's message calls the project **"nepszava"** and points at **nepszava.hu**. Every
input says **Népszabadság**: the memo ("indul újra a Népszabadság napilap", "Megújul a
Népszabadság!"), the Figma file's name, the logo in every frame, and the frame
"Népszava márkafront", which reads *"A Népszabadság almárkája: a Népszava
szerkesztőségének online anyagai és a nyomtatott lapszámok cikkei, egy helyen."* — so in
this design **Népszava is a sub-brand of Népszabadság**, a rovat in the main navigation
and a brand front of its own, and the front page teases "Mi lesz a Népszavával? A két
márka viszonya". The publisher line in every footer is **© 2026 Liberty Press Kft.**

This folder is therefore `nepszabadsag/`. It is not live yet; if the owner wants
`nepszava/`, rename before the first push (after a push a redirect stub must stay, per
the repo rule). nepszava.hu stays in the audit as the sister brand's current site.

## 3. What the Figma frames contain (read on screen, 2026-09-21)

Read in the app's browser pane as an anonymous viewer at 50 % (desktop) and 100 %
(mobile). Text was legible; exact sizes, colours and spacing were **not** readable —
the Dev Mode MCP server is not enabled in the Figma desktop app here, and the anonymous
viewer has no inspect panel. What unlocks the exact spec: either the owner enables
*Preferences → Enable Dev Mode MCP Server* in the Figma desktop app, or exports the eight
frames as PNG at 1× and the tokens as a variables list.

**Shared chrome (every frame).** Header: search icon left, the logo centre (a blue
square "N" mark + NÉPSZABADSÁG wordmark), a blue **Előfizetés** button right. Main
navigation: **Belföld · Külföld · Gazdaság · Kultúra · Sport · Tudomány · Népszava**.
Article pages add a second row of outlined pills (e.g. "Az újraindulás · A
szerkesztőség · Tíz év után"). Every page ends with a full-width **blue band**:
*"November 15-ig ingyenes regisztrációval minden cikk teljes egészében olvasható."* with a
**lime "Regisztrálok"** button, then a four-column footer — Rovatok (Belföld … Tudomány)
· Almárka (Népszava, A nyomtatott lapról) · A lapról (Impresszum, Etikai kódex, A
szerkesztőség, Kapcsolat) · Jogi és egyéb (Adatvédelmi tájékoztató, Előfizetési
feltételek, RSS) — and "© 2026 Liberty Press Kft. · Minden jog fenntartva."

**Címlap — desktop (1480 × 3810).** Leaderboard ad slot 970 × 250 under the nav. Lead
block: the lead story left (headline "Tíz év csend után újra megjelenik a Népszabadság",
dek, "6 PERC"), its photo centre with caption, a right rail **Legfrissebb** (rovat label,
headline, byline · time, thumbnail). Under the lead: a second story (MÉDIA rovat) and a
teaser line of two links ("Ki írja majd a lapot? A szerkesztőség névsora" · "Mi lesz a
Népszavával? A két márka viszonya"). Three columns Belföld / Gazdaság / Kultúra
(headline, dek, byline, "N PERC"). Right rail continues: **A nyomtatott lapból**
(stories with "Nyomtatásban: október 8., 1. oldal"), **Vélemény**, a 300 × 250 ad. Then
section blocks **Belföld** and **Gazdaság** (large photo + headline + dek left; two
smaller stories right), a **NÉPSZAVA** block (label pill, 3 × 2 photo grid: "A lapszám
vezető interjúja", "Jegyzet a hétről", "Riport a Nyírségből", "Az olvasói levelek
nyomában", "A hét képe", "Mire jó még a hetilap?"), the blue band, the footer.

**Címlap — mobil.** Header: hamburger · logo · search · a solid blue **Előfizetés**
block at the right edge. Lead headline in large serif, lead text, full-width photo,
the two teaser links, then a single column of stories: rovat label (small caps),
headline, dek in larger serif, byline · date, "N PERC"; hairlines between stories.

**Rovatfront — desktop.** Rovat title (e.g. "Belföld") with a one-line description
("Önkormányzatok, közigazgatás, egészségügy és oktatás — ami a településeken valóban
eldől. Napi tudósítás és heti terepmunka."), a row of outlined topic pills
(Önkormányzatok · Költségvetés · Egészségügy · Oktatás · Közbeszerzés), the lead story
(headline, dek, byline, "21 PERC", photo right), a two-column list of stories (headline,
byline · time, thumbnail), **A rovat szerzői** (six author portraits with name and
beat), a "Régebbi cikkek" outlined button, the blue band, the footer.

**Cikkoldal — desktop.** Rovat label + a lime **ELEMZÉS** tag, headline, dek, hero
photo with caption ("Felújítás alatt álló főtér egy dunántúli kisvárosban. Fotó: [FOTÓS
NEVE] / Népszabadság"), the author card (portrait, name, one-line bio, date · "4 perc
olvasás", a "Beállítás elsődleges forrásként" button), body, an inline 600 × 250 ad, the
**paywall box** "A cikk folytatása regisztrációhoz kötött" with three bullet teasers of
what the rest answers and three actions — blue **Ingyenes regisztráció**, outlined
**Print+online előfizetés — 3 290 Ft**, link "Már van fiókom — belépés", note "November
15-től a fal mögötti tartalom élő előfizetéssel olvasható." — then **Még a témában**
(topic pills), a 300 × 250 ad in the right rail, **Ezt is ajánljuk** (3 × 2 photo grid),
**Szerkesztői válogatás** (3 photos), footer. Mobile stacks the same in one column with
the right-rail modules inline.

**Népszava márkafront — desktop.** Title "Népszava", the sub-brand description quoted in
§2, pills (A nyomtatott lapból · Vélemény · Riport · Interjú · Jegyzet), the lead
("Az interjú, amit a lapszám címoldalán hoztunk"), a two-column story list, **A Népszava
szerzői** (six portraits), "Régebbi cikkek", the band, the footer.

**Provisional tokens** (`assets/tokens.css`, read from the screen, to be confirmed):
white ground, near-black serif for headlines, leads and body; a sans for labels, nav,
meta; one blue (logo, Előfizetés, rovat labels, links, the band); one lime (the
Regisztrálok button, the ELEMZÉS tag); hairlines; light-grey panels for ad slots, the
paywall box and the footer. Photos are placeholders (blurred) in every frame.

**The business model the design encodes:** registration wall now (free registration
opens every article until 2026-11-15), a **print + online subscription at 3 290 Ft**
from 2026-11-15, a print weekly ("A hetilap október 8-án kerül az újságosokhoz"), ad
slots on every page (970 × 250, 300 × 250, 600 × 250), and the reader-relationship
mechanics (author cards with "set as primary source", topic pills, "Legfrissebb").

## 4. Market research — what was measured today

Twenty-five home pages fetched with `curl` from this environment (desktop UA, gzip,
one cold request each; TTFB and size are single readings, not averages):

| Site | HTTP | TTFB s | HTML KB | scripts | stylesheets | `<img>` | Stack signals | Fonts seen in HTML | Nav / brand colour |
|---|---|---|---|---|---|---|---|---|---|
| nytimes.com | 403 (bot wall) | 0.11 | 0.8 | — | — | — | — | — | not measurable by curl; the browser pane refuses nytimes.com |
| washingtonpost.com | connection reset | — | — | — | — | — | — | — | not reachable from here |
| wsj.com | 401 (bot wall) | 0.14 | 0.8 | — | — | — | — | — | — |
| theguardian.com/uk | 200 | 0.14 | 163 | 19 | 1 | 139 | Next.js, Permutive | GH Guardian Headline, Guardian Text Egyptian, Guardian Text Sans | News · Opinion · Sport · Culture · Lifestyle; #052962 (theme-color), red #c70000 |
| bbc.com/news | 200 | 0.04 | 64 | 59 | 0 | 44 | Next.js, Piano, Optimizely, Permutive | BBC Reith Sans / Serif | Home · News · Sport · Business · Technology · Health · Culture · Arts · Travel · Earth · Audio · Video · Live; black, red #b80000 |
| ft.com | 403 (security check) | 0.05 | 198 | — | — | — | Vue | Financier Display, Metric | pink #fff1e5, teal #0d7680 |
| spiegel.de | 200 | 0.10 | 253 | 23 | 2 | 640 | Next.js/React | SpiegelSans, SpiegelSerif, SpiegelSlab, National2Narrow | 22 nav items (Politik … Geschichte); theme-color #e64415 |
| zeit.de | 403 ("Da ist etwas schiefgelaufen") | 0.12 | 5 | — | — | — | — | — | — |
| faz.net/aktuell | 200 | 0.09 | 295 | 29 | 1 | 137 | Nuxt/Vite, jQuery | Roboto, Source Sans 3 | Politik · Wirtschaft · Finanzen · Feuilleton · Karriere · Sport · Gesellschaft · Besser leben · Rhein-Main · Technik · Wissen · Reise; red #c60000 |
| sueddeutsche.de | 200 | 0.03 | 283 | 82 | 1 | 181 | Next.js, GTM, Piano | SZ Sans Digital, SZ Text, Old Standard, Montserrat | SZ.de · Zeitung · Magazin · Jetzt · Dossier; #29293a, teal #009990 |
| nikkei.com | 200 | 2.41 | 95 | 8 | 1 | 216 | Next.js/Vite | (system) | theme-color #003e70, red #d11100 |
| straitstimes.com/global | 200 | 0.63 | 64 | 38 | 2 | 58 | Next.js, Piano, Chartbeat | (system) | Singapore · Asia · World · Opinion · Life · Business · Sport; #161616 |
| scmp.com | 200 | 0.09 | 244 | 116 | 6 | 34 | Next.js, GTM, Piano, Optimizely | Roboto, Roboto Condensed, Crete Round | #2c4692 / #001246 |
| thehindu.com | 200 | 0.43 | 65 | 80 | 5 | 123 | Next/React, jQuery, GTM, Piano, Chartbeat | (system) | #2b2e34 |
| people.com.cn | 200 | 0.75 | 37 | 33 | 4 | 148 | jQuery | (system) | blue #006ebf, red #b64d3a; 664 links on the home page |
| news.cn (Xinhua) | 200 | 0.50 | 42 | 13 | 2 | 84 | jQuery | (system) | 694 links |
| caixin.com | 200 | 0.76 | 26 | 48 | 2 | 79 | jQuery | Arial | #1f286f, #0098d0 |
| telex.hu | 200 | 0.07 | 143 | 6 | 16 | 74 | Nuxt/Vite, GTM | (self-hosted) | #222228, red #ef1b1b, blue #0439d9 |
| 444.hu | 200 | 0.04 | 49 | 7 | 3 | 96 | Next.js, GTM | (self-hosted) | 44 `<h1>` on the home page; orange #ffb76a |
| hvg.hu | 200 | 0.04 | 64 | — | — | — | — | — | orange #f26522 |
| index.hu | 200 | 0.05 | 75 | 86 | 5 | 188 | Vite, jQuery, GTM | (self-hosted) | Belföld · Külföld · Gazdaság · Kult · Vélemény · Tech-Tud · Sport · Fomo · 24 Óra · Blog · Videó · Podcast; #ff9900 |
| 24.hu | 200 | 0.03 | 66 | 54 | 8 | 140 | WordPress (AIOSEO, WPBakery), Vue, jQuery | (self-hosted) | Belföld · Nagyvilág · Közélet · Tudomány · Sport · Élet-Stílus · … 22 items; green #57a600, #002e5e |
| nepszava.hu | 200 | 0.05 | 48 | 27 | 57 | 30 | Cloudflare, AdSense, OneSignal, Gemius, d3, Swiper; home rendered by `/js/home/index.js` | (self-hosted, `fontconfig.css`) | description "Népszava politikai napilap"; 57 stylesheet links; `cache-control: no-store` |
| hang.hu (Magyar Hang) | 200 | 0.08 | 63 | 28 | 4 | 49 | Next.js, jQuery, GTM | (self-hosted) | 22 nav items incl. podcasts; teal #018d98 |
| nol.hu (the old Népszabadság) | 200 | 0.03 | 0.5 | 0 | 0 | 0 | a one-line stub | Arial | "A nol.hu archívumára a Lapcentrumon lehet előfizetni." — the archive is sold through lapcentrum.hu; nothing else is served |

Raw HTML of every fetch and `bench.json` are in the session scratchpad
(`scratchpad/bench/`), not in the repo.

**What the numbers already say.** (1) The reference sites that matter most for a
serif, subscription-first daily (NYT, WSJ, FT, Zeit, WaPo) cannot be read from this
environment by `curl`, and the browser pane refuses nytimes.com — their layouts must be
read in the owner's own browser or from published design sources. (2) Every measurable
leader is on Next.js / Nuxt with a self-hosted type family of two or three faces and one
brand colour plus red for live/breaking. (3) The Hungarian field splits: Telex (Nuxt,
6 scripts, 143 KB) and 444 (Next, 7 scripts) are lean; Index (86 scripts) and 24.hu
(WordPress + WPBakery, 54 scripts) are heavy; nepszava.hu ships 57 stylesheet links and
`no-store` caching. (4) Home pages carry 236–782 links; the Figma címlap carries far
fewer — a deliberate choice to be defended in the research.

## 5. What is not done yet — the order, per `PROTOTYPING.md`

| Stage | State | What it needs |
|---|---|---|
| Research (`01-research.md`) | **measurements only** (§4); no layout study, no colour study, no industry sources yet | a rendered look at each site at 1440 and 390 (the browser pane can open all but nytimes.com; the owner stopped the screenshot sweep at 2026-09-21 — restart it or supply screenshots); Reuters Institute Digital News Report 2026 (Hungary page: trust, paid news, brand reach), Press Gazette / FIPP subscription benchmarks, relaunch cases (Népszabadság 2016 closure sources; comparable relaunches), the NYT / Guardian / Spiegel design-system write-ups |
| Audit (`02-audit.md`) | nepszava.hu measured once (§4); nol.hu measured | the sister site's page architecture and its subscription flow; the memo's landing has no current site to audit |
| Brief (`00-brief.md`) | this handover stands in | to be cut from §1–§3 once the name is settled |
| Sources (`03-sources.md`) | memo read in full; Figma read on screen | the Figma spec (Dev Mode or PNG + variables), the logo files, the type licences, the photographs, the "utolsó poszt" source, the registration back end (who receives the form) |
| Design system | `assets/tokens.css` provisional | confirmation from Figma, then the live components page → owner gate |
| Frames 1440 / 390 | Figma has them | transcribe once tokens are confirmed → owner gate |
| Build | — | generator for címlap / rovat / cikk / márkafront + the landing; sample data declared sample |
| Gate, sweep, presentation, technical package | — | as the standard |

## 6. Questions for the owner (none blocks the research)

1. Folder and URL: `nepszabadsag/` (as every input says) or `nepszava/` (as the message says)?
2. Figma: enable the Dev Mode MCP server, or export the eight frames as PNG at 1× plus the variables — either gives exact tokens.
3. The landing goes live before 2026-10-08: is it a page inside this prototype, or a page the client's developer ships from our spec? Who receives the registration form (Vezetéknév, Keresztnév, e-mail)?
4. "A Szerkesztőség — az utolsó poszt": which channel is the post source (a blog, Instagram, Facebook)?
5. Photographs: the frames use placeholders; are there press photos or an archive to build with (no AI imagery, by the repo rule)?

## 7. Environment notes for the next session

- The Drive connector can read the Figma link's page text but not its canvas; the built-in browser renders the canvas, and keyboard shortcuts do not reach it — use the zoom menu ("Zoom to fit", "Zoom to 50%") and hand-drags.
- `curl` from here reaches most news sites; NYT, WSJ, FT and Zeit answer with bot walls, the Washington Post resets the connection.
- The browser pane refuses `nytimes.com` outright.
- Cookie banners: decline non-essential.
