# Decision log

Format: what was decided · who · when · why · what it replaces.

**D1 — The first prototype's visual direction is withdrawn.** Owner, 2026-09-16.
Dark ground, gold accent, serif display read as a generic template rather than the
brand. Replaces commit `8342956` as a direction; the code stays in history only.

**D2 — Light ground with Holdvölgy's own palette.** Derived from research, 2026-09-16.
13 of 14 benchmark sites sit on white or cream; Holdvölgy's Elementor kit is
`#FAFAFA`/`#FFFFFF` ground, `#1D1D1B` ink, `#B8A689` accent, `#8B705B` hover. No
saturated gold, no dark sections. Replaces the prototype's `#14100c` / `#c8a55c`.

**D3 — Fonts: Bodoni Moda + Archivo (expanded), Google Fonts, SIL OFL.** Owner
constraint 2026-09-16: commercially free web fonts, Google Fonts preferred. These
reproduce the live site's Didot (h1–h6) + Akzidenz-Grotesk BQ Extended (everything
else) pairing. Archivo is used at `wdth` 112–125 to keep the extended character;
Bodoni Moda with `opsz` for display sizes only. Replaces the open question in the
plan's first draft about licensing Akzidenz-Grotesk BQ.

**D4 — Five-item navigation.** Owner approved 2026-09-16. Birtok · Borok ·
Látogatás · Borklub · Kapcsolat, plus Foglalás button and cart. Aszú, Trezor,
Ajándék and Experience move one level down. Replaces the live site's eleven items
plus mega-menu duplicate; matches the ≤ 7-item pattern across every benchmark.

**D5 — Mobile and desktop are two designed experiences.** Owner, 2026-09-16.
Desktop is the editorial estate; phone is a hospitality-and-buying tool with a
persistent bottom action bar; art-directed image crops per device; two navigation
systems; two QA checklists. Replaces "responsive reflow" as the mobile strategy.
Grounded in the brief's finding that over half of gifting-season purchases are
mobile.

**D6 — AI-generated images are excluded.** Standing, 2026-09-16. Three
`ChatGPT-Image-2026…png` files are live on Borkóstoló and Experience; they are not
carried into the prototype. Real photography or a marked placeholder instead.

**D7 — No asset is downloaded before the build phase.** Standing, 2026-09-16.
Inventory was taken from URLs, HTTP headers and the first 33 bytes of PNGs. Assets
are fetched only when a page that uses them is built, per the owner's sequencing
("before that make a research and implementation plan first").

**D8 — One JSON catalogue drives HU and EN.** Derived, 2026-09-16. Product data
(line, name, vintage, dűlő, variety, price, render URL, technical data when supplied)
lives once; both language trees render from it. Replaces duplicated inline arrays in
the first prototype.

**D9 — Commercial model is shop-and-hospitality, not allocation-only.** Derived,
2026-09-16. Holdvölgy already shows prices, runs a 5–20 % loyalty ladder, gift cards,
en-primeur and the Trezor experience — the Penfolds/Garzón model with an Opus-One
style allocation layer. Nobody else in Tokaj sells online. Design accordingly.

**D10 — Direction approved; Phase 1 started.** Owner "Go", 2026-09-16, on the
§4 direction of `00-plan.md`. First deliverable is `05-layout-specs.md` (desktop
1440, phone 390, tablet resolved), to be approved before the home page is coded.
D7 is lifted for the assets that the specified pages actually use.

**D11 — Design-system approval is a gate before layouts.** Owner challenge
2026-09-16 ("do we have the design system already approved?") — it was not; the
plan had gone from direction straight to layout specs. Phase 1 now has three gates
in order: design system → layouts → home page. `docs/design-system.html` is gate 1
and renders the system live from the tokens and the converted assets. Replaces the
two-step Phase 1 in the plan's first draft.

**D12 — Design system approved (gate 1).** Owner, 2026-09-16: "I am satisfied."
`docs/design-system.html` is the fixed system; layouts arrange it, pages are built
from it, anything new is brought to that page first. Gate 2 opened the same day
with composed frames at 1440 and 390 in `docs/frames/`.

**D13 — Layout frames approved (gate 2); gate 3 built.** Owner "Approved",
2026-09-16. The home page is generated for HU and EN by `holdvolgy/build.py` from
one content dictionary (D8 applied), with the phone and desktop experiences as
separate breakpoint designs per D5, mega-panels on hover and focus, a native
`<dialog>` sheet and age gate, and an art-directed hero via `<picture>`. The
withdrawn first-prototype shop page (`holdvolgy/borok/`) is removed; wine links
point to the wine band until Phase 3 builds the shop.

**D14 — A published URL is never deleted; it redirects.** Standing, 2026-09-16.
Removing `holdvolgy/borok/` left a cached hub card on the owner's phone pointing at a
404. Any URL that has been live gets a redirect page when its content moves.
Recorded in CLAUDE.md rule 2 so it applies to every project here.

**D15 — Navigation and document indexes are single-sourced.** Standing,
2026-09-16. The docs navigation lives once in `docs/build.py` and is written into
hand-authored pages on every build; the project pages' navigation lives once in
`holdvolgy/build.py`. A build-time check verifies every doc page links every other,
and a whole-project link audit runs in the gate before every push.

**D16 — Image conversions keep alpha; the base stylesheet releases attribute
heights.** Standing, 2026-09-16, after the owner found the vineyard map black and
stretched on the live Birtok page. Any source PNG with an alpha channel is encoded
to WebP/AVIF with alpha, never flattened; every page's base rule is
`img { max-width: 100%; height: auto; display: block }` so width/height attributes
(kept for layout stability) never distort. The gate now includes a rendered look at
every image-led section, not only measurements.

**D17 — Images in aspect-ratio boxes are absolutely bounded.** Standing, 2026-09-16.
A percentage height inside an `aspect-ratio` grid cell resolves to `auto`, so the
image falls back to its attribute height and overflows. Figure boxes are
`position: relative` and the image is absolutely centred with `max-height` and
`max-width` bounds. Found in the Phase 3 gate by looking, not by the numbers.

**D18 — Component class names are namespaced; the gate checks for collisions.**
Standing, 2026-09-16. A fact-sheet section named `.sheet` collided with the menu
dialog's `.sheet` (fixed-position) and floated over the page. Section classes that
could read as generic (`sheet`, `bar`, `card`, `grid`) are either namespaced
(`factsheet`) or checked for a second definition before use.

**D19 — Standard documentation structure; technical package in status PROPOSED.**
Owner, 2026-09-18. Every project carries the same documentation set next to its
prototype (customer side: presentation, brief, research, audit, sources, decisions,
design, build log, gate, client asks; technical side: SSOT, architecture, technical
design, implementation plan, token map). For Holdvölgy the customer side existed; the
technical side was written the same day. Stack recommendations are ADRs in
`11-architecture.md` and stay PROPOSED until the owner or the client flips one — the
flip is recorded here as the next D-number. Replaces: nothing; before this the project
had no technical package at all.

**D20 — A responsible-data policy record for the estate (SSOT §6b, PROPOSED).** The studio, 2026-09-20, on the owner's directive (responsible data for every client) and the hub audit. Alcohol: adults only with the age gate on every entry (built) and age confirmation at checkout and delivery (the gap); no minor in any image; newsletter and club by consent; retention per the accounting law; rules R12–R14 and the gate rows for the production site. Replaces nothing; documents what the built site must keep.
