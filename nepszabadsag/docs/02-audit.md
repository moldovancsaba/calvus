# Népszabadság — audit of the starting point

*The new Népszabadság has no current site of its own — the old domain (nol.hu) is a dead
archive stub. What is measured here is the sister brand the design names throughout
(nepszava.hu, "A Népszabadság almárkája") and the old domain, both with `curl` from this
environment, 2026-09-21. Every figure below is what a tool returned; nothing is estimated.*

## 1. nepszava.hu — the sister site named in the design

| Measure | Value | What it means |
|---|---|---|
| Stack | Cloudflare in front; home rendered client-side by `/js/home/index.js`; AdSense, `gemius.js` (audience measurement), `pegapoll.com` embed, D3.js, Swiper | a JS-rendered front page — `curl` sees an empty shell for the nav and most content; a real DOM read needs a browser |
| Weight (curl, 2026-09-21) | 48 KB HTML, 27 scripts, 57 stylesheets, 30 `<img>` | 57 stylesheet links on one page is unusually high — see `01-research.md` §1 for how this compares to the other 24 sites measured |
| Cache | `cache-control: no-store, no-cache, must-revalidate` on the home page | every visit is a fresh render — no edge cache for the front page, which the site's own headers confirm |
| `robots.txt` | disallows `/digitalisujsag`, `/digitalisujsag_bejelentkezes`, `/json/*`, `/default.asp`, `/articles/article.php`, `/PrintArticle.asp`; sitemap at `/sitemapindex.xml` | the disallow list names a `digitalisujsag` ("digital newspaper") product with its own login page — see §2 |
| Meta | `description`: "Népszava politikai napilap"; `og:site_name` "Népszava"; Google Play app id `hu.nepszava.mobile`, Apple App Store id `1446287033` | the sister brand runs its own native apps, separate from the web site |

**P** [nepszava.hu](https://nepszava.hu/) (curl, 2026-09-21); [nepszava.hu/robots.txt](https://nepszava.hu/robots.txt)

## 2. The digital edition — a real subscription product, run by a third party

Fetching the disallowed paths directly (curl, not a crawler, so `robots.txt` does not block
the request) shows a working product: `/digitalisujsag` loads a page-flip e-paper reader
(`pdfobject.js`, a Swiper-based page viewer, a calendar to pick a past issue, dark mode, a
resizable font — read from the page's own `<meta>` and `<script>` tags) gated by a login
form. The login form itself resolves to a **third-party vendor**, not code on nepszava.hu:

- The registration link on the login screen points to `https://xximedia.hu/felhasznalo?reg=reg`
  and the product-information link to `https://xximedia.hu/mobilnsz` — a Hungarian e-paper /
  digital-newsstand platform, not a nepszava.hu-built system. **P** (the site's own login
  fragment, fetched directly, 2026-09-21)
- The vendor's product page for "mobil Népszava" states, in its own words (2026-09-21):
  *"A kiadvány jelenleg nem elérhető"* — the publication is **currently not offered** — with
  a note that the newsroom still produces the paper at the same standard but "jelenleg
  azonban csak digitális formában tudjuk ezeket kínálni" (currently only in digital form), and
  a subscription is what makes the mobile app and the full nepszava.hu content
  accessible. **P** [xximedia.hu/mobilnsz](https://xximedia.hu/mobilnsz), 2026-09-21
- The vendor page names the operating company as **XXI. Század Média Zrt.**, KÖKI Terminál
  B irodaépület, 1191 Budapest, Vak Bottyán u. 75/A-C — not the "Liberty Press Kft." the new
  Népszabadság's Figma footer names (`handover.md` §2). **This is a plain fact, not a
  conclusion**: it says the sister brand's current publisher differs from the new project's
  stated publisher; whether that is a change of ownership, a separate holding entity, or
  something to raise with the client is for the owner, not this document. **P** [xximedia.hu
  media kit PDF](https://xximedia.hu/files/public/cikkepek/261/File/2026/NEPSZAVA_ONLINE_MEDIAAJANLO_2026_03.pdf),
  2026-09-21 (see §3)

**What it means here.** The design's "November 15-ig ingyenes regisztrációval… utána
Print+online előfizetés — 3 290 Ft" mechanic has a direct precedent one click away: the
sister brand already runs a paid digital-edition reader, already outsourced to a specialist
vendor rather than built in-house. That is a real build-vs-buy option for the new site's own
paywall/reader, not a hypothetical — worth a line in `03-sources.md` and a question for the
owner (who has the commercial relationship with the vendor, if any, for the new title).

## 3. Advertising — a real, priced rate card for the exact slot sizes the Figma uses

nepszava.hu's own 2026 online rate card (PDF, effective 2026-08-27, downloaded from
`xximedia.hu`, prices in HUF, list price, ex-VAT, per week) prices the same header/rail/
inline banner sizes the client's Figma frames show (970×250, 300×250, 300×300, 300×600):

| Placement | Sizes | Weekly list price (Ft, ex-VAT) |
|---|---|---|
| Multiscreen premium, header, home page | 970×250 + 300×300 | 4 790 000 |
| Multiscreen premium, header, article pages | 970×250 + 300×300 | 3 590 000 |
| Multiscreen basic, header, home page | 728×90 + 300×250 | 4 390 000 |
| Multiscreen basic, header, article pages | 728×90 + 300×250 | 2 990 000 |
| Desktop premium, right rail, home page | 300×600 | 3 590 000 |
| Desktop basic, right rail, home page | 300×250 | 2 700 000 |
| Desktop basic, right rail, article pages | 300×250 | 2 000 000 |
| Sponsored article (agency-written), front-page feature | — | 3 000 000 |
| Sponsored article (client-supplied), front-page feature | — | 2 700 000 |

**P** [Népszava Online Tarifa 2026, XXI. Század Média Zrt.](https://xximedia.hu/files/public/cikkepek/261/File/2026/NEPSZAVA_ONLINE_MEDIAAJANLO_2026_03.pdf),
effective 2026-08-27

**What it means here.** The Figma's ad slots (970×250, 300×250, 600×250 per `handover.md`
§3) are not a designer's placeholder convention — they are the exact commercial inventory
sizes the Hungarian market (or at least this publisher) already sells, at these prices. If
the new site inherits or competes with this inventory, these are the real numbers to build
a rate card from rather than invent one; a video-banner surcharge of 50% and a 70 KB static
creative limit are stated in the same document.

## 4. nol.hu — the old Népszabadság domain

| Measure | Value |
|---|---|
| HTTP | 200 |
| Content | a one-line stub, Arial, no scripts, no stylesheets, no images: *"A nol.hu archívumára a Lapcentrumon lehet előfizetni."* |
| What it means | the historic domain is fully retired; the archive itself is sold as a subscription through a third party, lapcentrum.hu, not served here |

**P** [nol.hu](https://nol.hu/), curl 2026-09-21 (also recorded in `01-research.md` §1)

## 5. The rendered home page — read in the browser pane, 2026-09-21

`curl` only returns the JS shell (§1); read directly in the browser at 1440 and 390 instead
(full write-up and the nine-site comparison in `01-research.md` §7). In short: two full-width
ad units stack directly under the masthead before any editorial content, one of them unfilled
and the other a foreign-market shopping carousel; the lead story runs with no photograph at
all; a floating overlay ad appears on scroll; **no subscription or registration control is
visible anywhere in the header, hero or body** — "Előfizetés" is one small footer link; and on
mobile the header shrinks to a bare "N" monogram with a mistargeted French-language ad
immediately below it. Against the other nine sites measured the same way, this is the least
curated and least subscription-forward home page of the set — a concrete, fixable gap for the
new site to not repeat (`01-research.md` §7 proposals P8–P9).

## 6. What was not measured, and why

- **Whether XXI. Század Média Zrt. and Liberty Press Kft. are related** — a fact for the owner
  to confirm or correct, not something this audit infers from public pages.
- **The App Store / Play Store listings for "mobil Népszava"** — the Apple listing rate-limited
  this environment (HTTP 429) and the Play Store page did not expose price text to a plain
  fetch (client-rendered); neither was pursued further.
