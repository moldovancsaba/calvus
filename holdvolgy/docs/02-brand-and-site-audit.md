# Holdvölgy brand and live-site audit — 2026-09-16

Everything here was read from holdvolgy.com over HTTP; nothing is inferred.

## Brand tokens (Elementor kit `post-16.css`)

| Role | Value |
|---|---|
| primary | `#B8A689` warm greige |
| secondary | `#1D1D1B` near-black |
| text | `#666666` |
| grounds | `#FFFFFF`, `#FAFAFA`, `#F4F4F4`, `#D9D9D9` |
| supporting | `#BAA793`, `#8B705B` brown, `#9B9796` grey |
| accent (Elementor default, unused in design) | `#61CE70` |

Fonts: `AkzidenzGroteskBQ-Ext` on all four Elementor typography roles (196
declarations, `akzidenzgroteskbq-ext-webfont.ttf`); `Didot` on `h1`–`h6` at kit
level (`Didot-Regular.ttf`) and on a few scroll-text widgets; Open Sans residual.
Both brand fonts are served as TTF — no WOFF2 (work-list item HV-W14).

## Page architecture as rendered (heading order)

**Home** — four `h1`s compete: Év pincészete 2026 · Borkóstolóélmény ajándékba ·
TOKAJI ASZÚ · TOKAJI ASZÚ ELŐJEGYZÉS. Then ten wine-category `h2`s (6 puttonyos
aszúk · édes birtokszelekció · édes szamorodni · Zéta szamorodni · fordítás · édes
sárgamuskotály · száraz birtokszelekció · száraz furmint Király · száraz hárslevelű
Becsek), Holdvölgy kezdetek, "több mint borászat", the tagline, Aktualitások,
"látogass meg minket", team roles, newsletter. CTAs: BŐVEBBEN · TOVÁBB · ÉRDEKEL ·
TELJES VÁLASZTÉK · időpontfoglalás · "ahol megtalálod borainkat".

**EN home** mirrors HU (Winery of the Year 2026 · THE PERFECT GIFT · TOKAJI ASZÚ ·
EN PRIMEUR …) but three news headings remain in Hungarian.

**Birtok** — A birtok alapjai → tagline → ten-step timeline (születésnapi ajándék
1998 → megalakulás 2004 → névadó dűlő 2005 → első aszú 2006 → portfólió 2007 →
épület és pince 2011–13 → első látogatók 2014 → Trezor 2016 → építészeti díj 2018 →
PreCulture 2019) → gallery → Dűlők és terroir → kőzetek → szőlőfajták → évjáratok
2021–2025 → Csapat (Demkó Pascal, Jójárt Gergő, Erdélyi Károly, Jákób Bianka, Demkó
Natália, Molnár Balázs, Körtvélyesi Kornél, Gellén Fruzsina) → per-dűlő panels with
Telepítések · Expozíció · Kőzet · Fajták for Holdvölgy, Úrágya, Nyulászó,
Dorgó-tető, Becsek, Király, Kakasok.

**Tokaji aszú** — Culture → készítés → érlelés → Időkapszula (születés · testvérek ·
család · diploma · eljegyzés · házasság · siker · generációk) → ajándék → Holdvölgy
garancia → Culture 6 puttonyos → PreCulture 6 / 3 palack → Tokaj örökség (eleven
milestones from Vitis Tokaiensis to "Az első Holdvölgy évjárat").

**Borkóstoló** — "Borkóstoló a föld alatt" (duplicated `h1`) → 1,8 km · 3 szint ·
500 év (each rendered twice) → pincetörténet (seven milestones incl. Vince díj,
építészeti díj) → jegyek: 6 aszú évjárat / térképes aszúval / térképes → Experience →
Geológia "10 millió éves vulkáni nyomok" → látogatás → hasznos információk →
vendégkönyv.

**Shop** — categories Borválogatások · Culture · Édes borok · Száraz és félszáraz ·
Hold and Hollo · Díszdobozok és ajándéktasakok; tasting tickets sold as products.
EN shop exists and mirrors.

## Product pages

`/bor/szaraz-valogatas-vision`: 1 705 characters of visible text; product-specific
content = name, three vintages, prices (5 500 / 9 500 / 19 000 Ft). No tasting
note, dűlő, variety, alcohol, sugar, acidity, serving, award or pairing.
`/bor/culture-aszu`: one paragraph on Culture, then thirteen vintages 2006–2018
with prices (2006/2007 67 000, 2008 40 500, 2009 36 500 … 2018 27 500; a 133 000 Ft
item also appears — format unconfirmed). The information architecture puts wine
facts in category names, not on product pages.

## Booking, gift, club, Trezor

- `/borkostolo-idopontfoglalas/` is a contact form: Név · E-mail · Telefonszám ·
  Borkóstolók (select: Kincskereső 6 / 8 borral / Tokaji aszú élmény) · Dátum ·
  Vendégek száma · Üzenet · GDPR. No availability, no payment.
- Gift cards from 6 500 Ft/fő; five programmes listed.
- Borklub is a real loyalty ladder: 5 % at 50 000 Ft, 10 % at 150 000, 15 % at
  300 000, up to 20 %; 12-month tier validity; quarterly offers; limited reserves.
- Bortrezor: guests take part in the blend ("házasítás") and receive a certificate.

## Defects observed (beyond the technical brief)

- Four `h1`s on home, two on Borkóstoló (W22 cites three on one page).
- Three AI-generated images live (`ChatGPT-Image-2026.-apr.-27…`) on Borkóstoló
  and Experience.
- Hungarian news headings on the EN home.
- Eleven top-level nav items plus a mega-menu duplicate.
- Product pages carry no product information.
- Fonts served as TTF only.
