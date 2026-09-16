# Holdvölgy 2026 — bemutató a birtoknak

Ez az oldal az, amit a Holdvölgy Birtoknak mutatunk és mondunk. Magyarul, a birtok
nyelvén; a mögötte lévő munkanapló és a kutatás angolul, ugyanebben a mappában.

## Mit nézzenek meg

A prototípus él, telefonon és asztali gépen egyaránt. Az első megnyitáskor a 18+
kapu jelenik meg — ez a bor törvényi feltétele, ezért tervezett eleme az oldalnak,
nem utólag ráragasztott ablak.

| Oldal | Magyar | Angol |
|---|---|---|
| Kezdőlap | [holdvolgy/](../index.html) | [holdvolgy/en/](../en/index.html) |
| Birtok — történet, hét dűlő a saját kőzetével, fajták, évjáratok, csapat | [birtok](../birtok.html) | [estate](../en/birtok.html) |
| Tokaji aszú — Culture 2006–2018 évjáratfal árakkal, készítés, érlelés, Időkapszula, PreCulture, Tokaj öröksége | [aszú](../aszu.html) | [aszú](../en/aszu.html) |
| Látogatás — jegyek, Experience, Millennium Bortrezor, geológia, foglalás | [látogatás](../latogatas.html) | [visit](../en/latogatas.html) |
| Borok — 32 tétel, szűrés, rendezés | [borok](../borok.html) | [wines](../en/borok.html) |
| Egy termékoldal — kóstolási jegyzet, évjárat, teljes adatlap | [Vision 2021](../bor/vision-2021.html) | [Vision 2021](../en/bor/vision-2021.html) |
| Borklub — a valódi kedvezményszintek | [borklub](../borklub.html) | [wine club](../en/borklub.html) |

## Miért így néz ki

Mielőtt egyetlen oldalt megterveztünk volna, végignéztük, hogyan mutatják be és adják
el magukat a világ legjobb birtokai — Château Margaux, Krug, Château d'Yquem, Opus
One, Antinori, Penfolds, Bodega Garzón, Klein Constantia és a tokaji szomszédok,
Royal Tokaji, Disznókő, Barta: huszonegy oldal.

Amit ez adott:

- **Világos alap, nem sötét.** Tizenhárom világos hátterű oldal egy sötéttel szemben.
  A prémium borvilág a fényképre bízza a színt, nem a felületre.
- **A birtok saját arculata.** A jelenlegi holdvolgy.com színei és betűi jók — a
  meleg pezsgőszín (#B8A689) a majdnem-fekete tintával, a széles groteszk betű a
  Didot-címekkel. Ezt tartottuk meg, és ezt vittük végig következetesen; a betűket
  ingyenes, Google Fonts-os megfelelőikkel (Archivo, Bodoni Moda) helyettesítettük.
- **Fénykép és egy mondat.** Minden oldal a birtok saját fotójával és egyetlen
  mondattal nyit — „A tokaji álmot töltjük pohárba az élet nagy pillanataihoz”.
- **Hét dűlő, hét kőzet.** A dűlők saját kőzetfotói olyan eszköz, amivel egyetlen
  versenytárs sem rendelkezik — ezért kapnak főszerepet.
- **Culture évjáratfal.** Tizenhárom évjárat 2006-tól, saját palackfotóval és árral.
  Tokajban senki más nem mutat vertikálist.
- **Két élmény, nem egy összenyomott elrendezés.** Az asztali változat a birtok
  „magazinja”; a telefonos változat foglalási és vásárlási eszköz, alul rögzített
  sávval — Foglalás · Borok · Kosár · Menü — a hüvelykujj alatt.

## Mi valódi benne

Minden szöveg, ár és kép a birtoké. A borok neve, kategóriája, kiszerelése, ára,
szlogenje és leírása a webshopból; a 31 tétel technikai adatlapja (alkohol, cukor,
sav, illósav, SO₂, cukormentes extrakt, besorolás, tárolás, fogyasztási
hőmérséklet), 22 tétel kóstolási és évjáratjegyzete a termékoldalakról; az angol
szövegek a birtok saját angol oldalairól. A 130 kép a birtok 180 saját képéből
készült, mindegyik visszakövethető a forrásáig.

Ami **nem** működik, mert prototípus: a kosár és az űrlapok nem küldenek — a
vásárlás és a foglalás a holdvolgy.com-on él. Ezt minden oldal tetején egy sáv
mondja ki.

## Amit mértünk

| | Jelenlegi holdvolgy.com | Prototípus |
|---|---|---|
| Kezdőlap súlya | 8,8 MB | 600 KB telefonon, 734 KB asztalon |
| Kérések száma | 226 | 4 a betűk és képek előtt |
| Oldalanként egy főcím | nincs (négy a kezdőlapon) | igen, mind a 76 oldalon |
| Érintési célok ≥ 44 px | — | mind a 76 oldalon, két méretben |

A műszaki átvételi célértéket (kezdőlap 1,5 MB alatt) minden oldal teljesíti.

## Amit a birtoktól kérünk

1. **Portrék** — az alapítóról nagy felbontásban, és a csapat nyolc tagjáról.
2. **Két kőzetfotó** — Úrágya és Kakasok; a jelenlegi oldalon nincs.
3. **Álló formátumú fényképek** a telefonos nyitóképekhez (pince, szőlő, aszú).
4. **Strukturált adatok**, amiket a jelenlegi oldalról nem lehetett megbízhatóan
   átvenni: szüreti dátumok (minden termékoldalon „2012. október” szerepel), díjak,
   érlelési potenciál.
5. **Döntés az angol szövegekről** — a Vision 2021 angol oldala magyarul van.
6. **A jelenlegi oldal hibái**, amiket közben találtunk: két termék-URL 404-et ad,
   az Exaltation 2017 Reserve 0 Ft-on szerepel, három kép mesterséges
   intelligenciával generált — ezeket a prototípus nem vette át.

## Hogyan tovább

Visszajelzés a fenti oldalakra; a módosításokat ugyanígy, mérve és dokumentálva
építjük be. Az október 15. és január 15. közötti változtatási tilalom miatt az új
oldal élesítése 2027 első negyedévére tervezhető — a prototípus addig érhet.
