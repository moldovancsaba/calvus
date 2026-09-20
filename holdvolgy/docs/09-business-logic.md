# Holdvölgy — business logic

*Written 2026-09-20 (hub audit action 7). The rules of the built site end to end, in the
order a visitor and the estate meet them: who the parties are, what the site sells and
what it only presents, the age gate, the shop, the club, the visit, the two languages, the
data, and what the site never does. Terms are the SSOT's (`10-ssot.md`); the decisions
behind each rule are in `04-decisions.md`; every rule below is stated where the generator
(`build.py`) or the pages implement it.*

## 1. The parties

| Party | Gets | Gives |
|---|---|---|
| **The estate** (Holdvölgy, Mád) | a site that tells the estate first and sells second (R1), in HU and EN from one source (R3); booking requests; club members; orders (when the shop is live) | the catalogue, the prices, the photography, the visit programmes, the club terms |
| **The visitor** (18+, R8/R12) | the story of the estate, the wines with the estate's own prices, a visit to request, a club to join, a shop | an age confirmation; a booking request with contact details; consent for the newsletter and the club |
| **The studio** | — | the generator, the pages, the documentation |

## 2. What the site sells, and what it only presents (R2)

- **Wines** — the catalogue (`data/catalogue.json`) is the only source of names, lines,
  types, vintages and prices; product pages are generated, never hand-edited (R3). Prices
  are the estate's. Stock is never shown; nothing claims availability it cannot know.
- **PreCulture** — listed as a pre-order product; not purchasable in the prototype.
- **Visits** — four ticketed programmes on Látogatás with a price and a duration; **booking
  is a request** (name, e-mail, phone, programme, date, guests, message, GDPR), not a
  purchase: no availability, no payment.
- **The Trezor programme** — a section and a ticket, not a product.
- **Borklub** — four discount tiers earned by 12-month spend (5 % at 50 000 Ft, 10 % at
  150 000 Ft, 15 % at 300 000 Ft, 20 % at 600 000 Ft); presented, joined by consent.

Hospitality comes before the shop in every CTA pair (R1): the estate is a place first.

## 3. The age gate (R8, R12)

Alcohol. The 18+ dialog shows before any content on every page, in both languages; "Nem"
leaves the site; acceptance is kept for the session only. For the built shop the age is
confirmed again at checkout and at delivery (SSOT §6b). No minor appears in any image; no
message, post or discount is framed so a minor could read it as aimed at them.

## 4. The shop (when it is built)

Cart and checkout are inert in the prototype and the banner says so (R10). In production:
the catalogue drives the cart; prices are the estate's; excise and distance-selling rules
for alcohol apply to delivery; orders are kept as the accounting law requires; the club
discount applies by tier at checkout; no fake scarcity ("last bottles" only if literally
true — R2). The responsible-data record (SSOT §6b) gates checkout on the age confirmation
and the privacy policy's shop clause.

## 5. The club and the newsletter (R13)

Both by consent, nothing pre-ticked, at most two mails a month across the two, opt-out
within one business day. The club's spend history is a tier calculation and nothing else —
no profile, no segment beyond the tier. Membership data is kept while active plus twelve
months.

## 6. The visit

A booking request is a message to the estate. The estate answers; the site promises no
slot. The GDPR box on the form is an acknowledgement of the privacy notice; it is not a
marketing consent (the newsletter has its own).

## 7. Two languages, one source (R3, R5)

HU at the root, EN under `/en/`; every page generated from one content source and one
catalogue; `hreflang` hu / en / x-default on every page; one `h1`, every image with `alt`;
a published URL is never deleted, it redirects (R6). No AI-generated imagery (R7): every
photograph is the estate's.

## 8. The data

The site stores nothing by itself. A booking request, a club application and a newsletter
sign-up go to the estate; the policy record (SSOT §6b) names retention, the privacy
policy's clauses and the gate rows for checkout, delivery, the club and the newsletter.

## 9. The rules, mapped

| Rule | Where | Rule | Where |
|---|---|---|---|
| R1 hospitality before shop | §2 | R8 the age gate | §3 |
| R2 no fake availability | §2, §4 | R9 namespaced components | `build.py`, the gate |
| R3 one catalogue, two languages | §2, §7 | R10 no stale phrase; the banner says only what is inert | §4 |
| R4 images keep alpha, `height: auto` | §7 | R11 navigation single-sourced | `build.py` |
| R5 one `h1`, `alt`, `hreflang` | §7 | R12 adults only, age at checkout and delivery, no minor in images | §3 |
| R6 a URL is never deleted | §7 | R13 club and newsletter by consent, two mails a month | §5 |
| R7 no AI imagery | §7 | R14 the gate on checkout, delivery, club, newsletter | §4, §5, §8 |

## 10. What the site never does

Shows content before the age gate; claims availability or stock; changes a price outside
the catalogue; hand-edits a generated page; deletes a published URL; shows a minor; uses
a generated image; pre-ticks a consent; sends more than two mails a month; frames a wine
as a party or a performance.
