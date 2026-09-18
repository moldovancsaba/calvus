# Lexodont — brief

*For a first reader. Written 2026-09-18, five months after the wireframe's last change and
one month after the client's site went live from it.*

## The client

Lexodont Dental Studio — a dental practice in Budapest (1026, Trombitás út 2.). Nine
specialties, a team of four dentists, online booking. Site: lexodont.hu.

## What the prototype is

A **wireframe of the practice's new marketing site**, in two fidelities: a polished
grey-scale version (`lexodont.hu/`, 18 pages) and a Balsamiq-style sketch
(`lexodont.hu_balsamic/`, 15 pages). Home, specialties hub and nine treatment pages,
prices, case studies with before/after sliders, team, four knowledge-centre articles.
Built 2026-03-31 in twenty commits, revised on 2026-04-09 after client feedback. Every
image is a placeholder; the doctors, fun facts and prices are illustrative; the contact
details, opening hours, parking zones and partners are real.

Live prototype: <https://moldovancsaba.github.io/calvus/lexodont.hu/> · sketch:
<https://moldovancsaba.github.io/calvus/lexodont.hu_balsamic/>

## What happened next — the site went live

Measured 2026-09-18 (`02-audit.md`): **lexodont.hu is the wireframe, built.** The same
`h1` ("Szebb mosoly, nyugodt élmény, modern fogászat"), the same page set and URLs
(`/araink/`, `/csapat/`, `/szakteruletek/`, `/esettanulmanyok/`, `/tudaskozpont/`,
`/idopontfoglalas/`), the footer contact block word for word, before/after sliders on the
home page. WordPress with a custom `lexodont` theme, WPML for English, Yoast, Flexi-Dent
booking embed, Google Analytics; pages last modified 2026-07-30 to 2026-09-18. Real
prices, four real dentists, real photography. The build was not done in this repo and
not by this workflow — the wireframe was the specification, and it worked.

## Where it stands

| | |
|---|---|
| Prototype | superseded by the live site; kept as the record of what was agreed |
| Customer side | this folder, written 2026-09-18: research (none was done, said plainly), audit of the live outcome, sources, decisions reconstructed from the history, design, build log, gate (66 measurements, findings recorded), client asks |
| Technical side | `10`–`14`: the as-built stack **measured**, not proposed; the content model; a proposed second-iteration plan for the items the wireframe had that the live site does not (and the reverse) |
| Open | whether Lexodont is a client again (`08-client-asks.md`); the wireframe's phone-width findings, left as recorded |

## How to read this folder

`README.md` is the index and process log; `bemutato.html` is the client-facing page in
Hungarian; `02-audit.md` is the one to read first if you want to know what was built.
