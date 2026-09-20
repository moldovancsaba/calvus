# Build log

## Round 1 — 2026-09-20 — the prototype, seven pages (D1–D9)

**Built.** `build.py` generates seven Hungarian pages from one content source: `index.html`,
`irodai-novenyek.html`, `novenygondozas.html`, `novenyberles.html`, `referenciak.html`,
`arak.html`, `rolunk.html`, `ajanlat.html`. Shared blocks: the proof band, the three offers,
the guarantee with the care rhythm and the response promise, the packages with "-tól" prices,
the four steps, the references (before/after), the team, the Instagram strip, the FAQ (the
client's own questions plus the guarantee and the response time), the quote form with the photo
drop zone. The character in four states. `LocalBusiness` JSON-LD with the three offers and the
Instagram / Grofie `sameAs`. No JavaScript beyond the menu sheet and the inert form.

**Measured** (browser pane, cache-busted).
- Phone 390: `index.html` scrollWidth 390, one `h1`, no element past the viewport, no console errors; every button ≥ 48 px; the two inline phone links were 16 and 38 px tall and were raised to 44 px (`.promise a`, `.imp a`).
- Desktop 1440: scrollWidth 1440, the header navigation shown and the dock hidden, one `h1`, no console errors; the guarantee heading reduced to 30 px so the three lists sit beside it.
- Weight: `index.html` 29 KB HTML, one stylesheet inline, one token file, two Google Fonts families, no images (the character is inline SVG) — against the client's live 292 KB and 51 scripts.

**Sample, declared**: prices, references, team names, the Google rating, the impresszum's fields.

## Round 2 — 2026-09-20 — the client's own material (D5, D6, D10)

**Changed.** The owner rejected round 1's look as generic ("Claude AI design") and asked for the
client's real photos, videos and visual elements. Rebuilt: the tokens are now the site's Elementor
kit (colours, Baloo 2 / Roboto Slab / Roboto, the 50 px pill); sixteen real installation
photographs, the logo and the hand-drawn illustration set pulled from the client's uploads into
`assets/img/` (alpha preserved, photographs at 1600 and 800 wide); the four Instagram Reels
embedded; the invented character, the shadowed cards, the uppercase eyebrow labels and the emoji
removed; a "Spoiler" section with the client's planters-with-faces photograph. Grammar pass on
every string.

**Measured** (browser pane, cache-busted, fresh navigation).
- Phone 390: scrollWidth 390, one `h1`, 15 images all loading, no console errors; every tap target ≥ 44 px after the brand link and the footer phone were raised.
- Desktop 1440: scrollWidth 1440, one `h1`, no target under 44 px, no console errors; transferred weight 1.65 MB with the four Instagram embeds (each loads Instagram's own scripts) — the page's own assets are ≈ 0.5 MB; the embeds are `loading="lazy"`.
