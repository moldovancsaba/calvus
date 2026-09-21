# Népszabadság — brief

*Stage 0 of the prototyping standard (`PROTOTYPING.md`). For the owner and the team. Written
2026-09-21 from the landing memo, the Figma file, and what `01-research.md` and `02-audit.md`
found once read and measured.*

## The client

**Népszabadság** — Hungary's largest-circulation daily until it was abruptly shut down on
8 October 2016 by its then-publisher; the official reason given was financial (cumulative
losses, falling readership), while contemporary press-freedom reporting (RSF, HRW) and a later
investigative retrospective describe the closure as widely read at the time as a politically
engineered removal of a paper then running stories critical of figures close to the governing
party, with the publisher sold to a government-aligned buyer weeks later — sourced in full in
`01-research.md` §4. It is relaunching as an online paper with a weekly print edition,
**launching 2026-10-08 at 08:00** — the memo's own line, *"Lassan véget ér 10 év hallgatás"*
("Ten years of silence are slowly ending"). The publisher named in the new design's every
footer is **Liberty Press Kft.**

## What they publish, per the memo and the Figma

General Hungarian news across **Belföld, Külföld, Gazdaság, Kultúra, Sport, Tudomány**, plus
**Népszava** as a named section and its own brand front for opinion, interviews and the print
weekly's own content — presented in the Figma as *"A Népszabadság almárkája: a Népszava
szerkesztőségének online anyagai és a nyomtatott lapszámok cikkei, egy helyen."* The
front page itself teases the question **"Mi lesz a Népszavával? A két márka viszonya"**
("What will happen to Népszava? The relationship between the two brands") — see the name
question below; the design is already asking the question the research independently raised.

## The brief

The owner's ask (2026-09-21): research the greatest and most popular news sites — US, German,
UK, Asian, Chinese and Hungarian — structure, layout, colours, everything; then build the
project the way Holdvölgy was built (research, audit, design system, frames, generated pages,
gate, presentation). Two deliverables are in scope: **a pre-registration landing page**
before launch (the memo's seven sections, two marked "hide for now") and **the site itself**,
eight Figma frames — Címlap, Rovatfront, Cikkoldal, Népszava márkafront, each desktop and
mobile.

## What the prototype covers

A serif-headline, subscription-first daily: a front page, section fronts, an article template
with a registration/paywall mechanic (free registration until 2026-11-15, then a print+online
subscription at 3 290 Ft), a named sub-brand front, and the pre-registration landing page —
built from the approved design system and frames once the owner has gated them (`PROTOTYPING.md`
stages 3–4), in Hungarian, phone and desktop measured separately.

## What is real, and what is not yet

**Real:** the memo's copy, quoted as written; the Figma's structure, page set and section
names, read on screen 2026-09-21; the technical and rendered-layout benchmark of 24 news home
pages and the sourced industry research (`01-research.md`); the old-domain audit (`02-audit.md`).
**Not yet real:** exact colours, type sizes and spacing (the Figma's Dev Mode is not enabled
here — provisional tokens only, `assets/tokens.css`); the photographs (every frame uses
placeholders); the logo files; who receives the landing page's registration form; the source
of "the last post" for A Szerkesztőség; whether the new title's registration/paywall is built
in-house or through a vendor.

## The name — settled

The owner's own message called the project "nepszava"; every written input (the memo, the
Figma file's name, the logo, the footer) says **Népszabadság**, with **Népszava** as its
sub-brand. The owner confirmed 2026-09-21 that calling it "nepszava" was their own slip: the
project is **Népszabadság**. The folder stays `nepszabadsag/`, live since 2026-09-21 — no
rename needed.

**A separate correction, same day.** A third-party news site the owner mentioned during the
original briefing, describing it as this project's "sister site," has no relationship to
Népszabadság or to this project of any kind — the owner said so directly, and it has been
removed from this documentation set entirely (`02-audit.md`, `04-decisions.md` D10–D11).

## Where it stands

Stage 0 (this brief), stage 1 (research and audit) and stage 2 (sources) written 2026-09-21.
**Next:** the owner reads the research and says "direction approved"; then the Figma is
unlocked (Dev Mode or exports) and the design system gate can start.
