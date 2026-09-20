# Bízd ránk a zöldet — audit of the starting point

*Measured 2026-09-20 with `curl` (the site) and the browser pane (Instagram, behind a cookie and
login wall). Every number is what the tool returned; nothing is estimated.*

## 1. The site — bizdrankazoldet.hu

| Measure | Value | What it means |
|---|---|---|
| Stack | WordPress 6.9, Elementor 3.35.9 + Elementor Pro, Royal Elementor Addons, Yoast (sitemap index), a Cloudflare e-mail obfuscator | a page-builder site; heavy by construction |
| Home | **292 KB HTML, 51 scripts, 24 stylesheets, 16 images** | four to five times the weight a page like this needs; the scripts and stylesheets are Elementor's per-widget files |
| Time to first byte | **10.5 s on a cold hit** (the two service pages and the sitemap on first request), **0.04–0.09 s warm** | a page cache exists but expires; the first visitor after expiry waits ten seconds — on a phone from an Instagram link that is a lost visitor |
| Pages | `/` (Irodai növények), `/novenygondozas/`, `/novenyberles/`, a leftover "Hello világ" post and an "Egyéb" category in the sitemap | three real pages; the leftovers should go |
| `h1` | "Irodai növények azoknak, akik már nyírtak ki kaktuszt" — twice on the home page (desktop and mobile copies of the hero) | the headline is the brand's best line; two `h1`s is a defect |
| `h2`s on the home page | 13, all in the brand's voice ("Ne a gyakornok locsoljon", "jobb, mint egy csocsóasztal") | the tone of voice already exists and is consistent |
| Images | 10 of 16 without alt text; the references block ("Akik már ránk bízták a zöldet") shows images with no client names or captions | the proof is present as pictures and absent as evidence |
| Prices | none on any page; competitors publish none either | the whole category hides the price; the first to say "from X Ft" wins the comparison |
| Reviews, ratings, Google Business Profile | none linked or shown | no third-party proof on the site |
| Company identity | only the phone and an obfuscated e-mail in the footer; the company name appears only in the privacy-notice PDF's filename; no registered seat, company number or tax number | Hungarian law (Ekertv. 2001/CVIII §4) requires the provider's name, seat, e-mail and registration data on the site — the team's reading, counsel confirms; also the first trust signal a B2B buyer looks for |
| Guarantee | none stated on the site; the parent brand states "100 % örökzöld garancia" | the strongest reliability promise the company has is not on this brand's site |
| Parent brand | not mentioned; the same phone number is on grofiezoldfal.com ("100+ projects, 10+ years, 30+ maintenance sites") | ten years of proof invisible to the visitor |
| Instagram | not linked from the site; the site is linked from Instagram | one-way |
| Forms | one Elementor form: name, e-mail, phone, office photos (upload), message, "Ajánlatot kérek" | the right ask — photos of the office — already in place |
| Tracking | Facebook pixel and gtag present; a cookie banner | consent before the pixel fires: to verify in the build (GDPR / ePrivacy) |
| Schema | WebPage, ImageObject, BreadcrumbList, WebSite (Yoast defaults); no `LocalBusiness` / `Service` / `FAQPage` / `Review` | search engines and AI answers see a web page, not a business with a service and an FAQ |
| Mobile | the hero duplicated for desktop and mobile; 44 px targets and contrast not measured here (stage 6) | to measure in the sweep |

## 2. The copy — what is strong and what is missing

**Strong.** The voice: self-aware, specific, funny about the *problem* (the dead cactus, the
intern with the watering can, the foosball table), never about the customer; every joke lands
on a real objection. The argument: plants are a system, not a decoration; maintenance is part
of the service; small offices work too; rental fits a changing office. The FAQ answers the
five questions a buyer actually asks.

**Missing.** Any *evidence*: who the clients are, what an installation looks like before and
after, how many sites are maintained, since when, by whom; what it costs, even as a range; what
happens if a plant dies (the guarantee); who the people are (a name, a face, the founder); how
fast a proposal comes; what a maintenance visit contains and how often. The site persuades and
then asks for trust it has not yet shown.

## 3. Instagram — @bizdrankazoldet (read 2026-09-20)

| Measure | Value |
|---|---|
| Followers / following | 70 / 11 |
| Bio | "Bízd ránk a zöldet!" + the site link; no what-we-do line, no city, no call to action |
| Posts visible before the login wall | 5 (1–17 September 2026): four Reels, one photo; two published by a collaborator (Szendrői Csaba) |
| Content | meme-style humour ("NEMTOM, OLYAN"), people in an office with plants, text on video |
| Cadence | roughly two a week in the first three weeks |
| Link to the site | yes; the site does not link back |

The account is three weeks old and already has the brand's voice. It has no proof formats yet
(before/after, a maintenance visit, a client's office) and no way to buy from it.

## 4. The parent brand — Grofie / Gourmet Garden Kft. (grofiezoldfal.com)

Services: indoor plant decoration, hydroculture, plant rental, vertical gardens, living green
walls, moss and lichen walls, plant care, "Örökzöld garancia" (evergreen guarantee), references.
Claims on the home page: **100+ projects, 10+ years, 30+ maintenance sites, 100 % evergreen
guarantee**; clients: offices, hospitality, hotels, retail. Same phone as the new brand. Public
record: a Portfolio.hu article (2020) on a 57 m² green wall in a WELL-certified office, the
managing director named. This is the trust the new brand can inherit in one sentence and one
logo — today it inherits none of it.

## 5. Five Hungarian competitors, measured the same way

| Competitor | Since / claim | Prices on site | Reviews on site | Guarantee | Weight (scripts) |
|---|---|---|---|---|---|
| CityPlant (cityplant.hu) | "since 1992"; showroom; green walls; air-cleaning plants | none | none | none stated | 28 |
| Plantart (plantart.hu) | catalogues, webshop, references (5 mentions) | none | none | none stated | 108 |
| Greenin (greenin.hu) | rental "without paying anything up front" | none | none | none stated | 144 |
| Bloom and Go (bloomandgo.hu) | decoration, rental, care; herbs | none | none | none stated | 92 |
| Arborica (arboricakft.hu) | care, replacement, consulting | none | none | none stated | 13 |

Nobody in the category publishes a price, shows a review, states a guarantee on the page, or
names a response time. The category sells on "contact us". That is the opening.
