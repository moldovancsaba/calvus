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

## 2. The name — settled

The owner's message first called the project **"nepszava"**; every written input said
**Népszabadság**: the memo ("indul újra a Népszabadság napilap", "Megújul a
Népszabadság!"), the Figma file's name, the logo in every frame, and the frame
"Népszava márkafront", which reads *"A Népszabadság almárkája: a Népszava
szerkesztőségének online anyagai és a nyomtatott lapszámok cikkei, egy helyen."* — so in
this design **Népszava is a sub-brand of Népszabadság**, a rovat in the main navigation
and a brand front of its own, and the front page teases "Mi lesz a Népszavával? A két
márka viszonya". The publisher line in every footer is **© 2026 Liberty Press Kft.**

The owner confirmed 2026-09-21 that "nepszava" was their own slip: the project is
**Népszabadság**. The folder `nepszabadsag/`, already live, needs no rename. **Same-day
correction:** the owner also said that a third-party news site mentioned during this
briefing, described at the time as "the sister site," has no relationship to this project of
any kind — it has been removed from this documentation set entirely, at the owner's direct
instruction (`04-decisions.md` D10–D11).

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

## 4. Market research — what was measured that day

Twenty-five home pages were fetched with `curl` that day (desktop UA, gzip, one cold
request each). The full table, since folded into the project's single research document
along with the rendered-layout pass and the sourced industry evidence that followed, now
lives in **`01-research.md` §1** — this handover keeps no separate copy of it. Raw HTML of
every fetch and `bench.json` are in that session's scratchpad, not in the repo.

## 5. Where each stage stands now — the order, per `PROTOTYPING.md`

| Stage | State | What it needs |
|---|---|---|
| Brief (`00-brief.md`) | **written 2026-09-21** — client, brief, what's real, the name (settled) | owner reads it |
| Research (`01-research.md`) | **written 2026-09-21** — the 24-site technical benchmark, a rendered-layout pass at 1440/390 for nine reachable sites, Reuters Institute DNR 2026 (Hungary), subscription/paywall benchmarks, the 2016 closure cross-checked across four sources, comparable relaunch cases, design-system references, proposals P1–P4 | owner says "direction approved" |
| Audit (`02-audit.md`) | **written 2026-09-21** — the old nol.hu domain, the client's only asset there is to audit | — |
| Sources (`03-sources.md`) | **written 2026-09-21** — every input and every gap numbered | the gaps listed there (Figma spec, logo files, photographs, the registration back end, the "utolsó poszt" source) |
| Design system | **written 2026-09-21** (`05-design.md`) — tokens/components as built, from direct visual read, not Dev Mode | exact pixel values still rest on an export or Dev Mode access |
| Frames 1440 / 390 | Figma has them; not separately transcribed as static frames — built straight into the five pages instead, on the owner's direct build instruction (D1) | — |
| Build | **first version built 2026-09-21** — Címlap, the Belföld rovatfront, one Cikkoldal with the paywall, the Népszava almárka, the landing page; generated from `content.py` + `build.py`; measured clean at 390 and 1440 | rovat fronts for Külföld/Gazdaság/Kultúra/Sport/Tudomány; real client photography and logo files |
| Gate, sweep, presentation, technical package | gate covers the site pages (`check.py`); the Hungarian presentation (`bemutato.html`) written 2026-09-21 | a full sweep once more pages exist; the technical package (stages 10–14) once the direction is confirmed |

## 6. Questions for the owner (none blocks the research)

1. Folder and URL: `nepszabadsag/` or `nepszava/`? **Settled 2026-09-21** — Népszabadság, `nepszabadsag/`.
2. Figma: enable the Dev Mode MCP server, or export the eight frames as PNG at 1× plus the variables — either gives exact tokens.
3. The landing goes live before 2026-10-08: is it a page inside this prototype, or a page the client's developer ships from our spec? Who receives the registration form (Vezetéknév, Keresztnév, e-mail)?
4. "A Szerkesztőség — az utolsó poszt": which channel is the post source (a blog, Instagram, Facebook)?
5. Photographs: the frames use placeholders; are there press photos or an archive to build with (no AI imagery, by the repo rule)?

## 7. Environment notes for the next session

- The Drive connector can read the Figma link's page text but not its canvas; the built-in browser renders the canvas, and keyboard shortcuts do not reach it — use the zoom menu ("Zoom to fit", "Zoom to 50%") and hand-drags.
- `curl` from here reaches most news sites; NYT, WSJ, FT and Zeit answer with bot walls, the Washington Post resets the connection.
- The browser pane refuses `nytimes.com` outright.
- Cookie banners: decline non-essential.
