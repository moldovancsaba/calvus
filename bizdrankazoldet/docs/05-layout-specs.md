# Layout specifications — phone 390 and desktop 1440

*Gate 2. Two designed experiences, not one layout reflowed (D2): the phone is where the buyer
arrives from Instagram; the desktop is where the decision is checked from Google or LinkedIn.
Each is specified at its reference size; tablet (768–1023) resolves between them. The frames
below are the built pages at the two sizes — the prototype is its own frame.*

<div class="frames">
<figure><figcaption>Phone · 390 — <a href="../index.html">open the page</a></figcaption><div class="scale-p"><iframe src="../index.html" title="Phone frame, 390 wide" loading="lazy"></iframe></div></figure>
<figure><figcaption>Desktop · 1440 — <a href="../index.html">open the page</a></figcaption><div class="scale-d"><iframe src="../index.html" title="Desktop frame, 1440 wide" loading="lazy"></iframe></div></figure>
</div>

## Shared rules

- Palette and type from `../assets/tokens.css` — the client's kit: primary `#007982`, secondary `#66F5FF`, text `#0F3F43`, accent `#B3FF66`, the pale lime and cyan tints; Baloo 2 for titles and the funny line, Roboto Slab for subheads, Roboto for everything else. Every photograph and illustration is the client's (`../assets/img/`).
- Breakpoints: phone ≤ 767 (designed at 390), tablet 768–1023, desktop ≥ 1024 (designed at 1440). Each has its own navigation and its own hero composition.
- One `h1` per page; 44 px minimum on every tap target; every number that is the client's to give is badged *minta*.
- The order of every page: hook → proof → offer → guarantee → price → process → references → people → questions → the quote form. Proof before persuasion on every device.

## Phone · 390 — Instagram-first

| Block | Composition | Why |
|---|---|---|
| Banner + header | the prototype banner; the badge, the wordmark, a *Menü* button opening a sheet with the six pages and the quote link | one thumb, one hand |
| Hero | a real photograph full-width at 4 : 5, then the kicker, the `h1` in Baloo 2 at 36 px (15 ch), the lede, two full-width buttons (photos → quote; prices) | the office first, the joke second, the action within reach |
| Proof band | teal, 2 × 2 numbers, one line naming the parent | the parent's ten years in the first screen and a half |
| Offers | three stacked offers: a real photograph at 3 : 2, the funny line, the professional sentence, a text link | scan by thumb |
| Guarantee | the pale-cyan block: the client's care-ring illustration, the rule, two lists stacked | the reliability promise, readable in one scroll |
| Packages | three stacked cards, the middle one highlighted; "-tól" prices badged *minta* | the price the category hides |
| Steps, references, team, Instagram, FAQ, form | single column; references as before/after halves; FAQ as `details`; the form in one column with the photo drop zone | the journey in the order it happens |
| Dock | fixed bottom bar: "3 fotó → ajánlat 2 munkanapon belül" + a call button; 88 px of bottom padding on `main` | the one action, always one tap away |

## Desktop · 1440 — Google/LinkedIn-first

| Block | Composition | Why |
|---|---|---|
| Header | badge and wordmark left, six pages centre, "Kérek ajánlatot" right; the sheet and the dock are gone | the decision-maker checks the menu first |
| Hero | two columns without a gutter: the photograph 640 px tall on the left, the `h1` at 62 px (13 ch), the lede and two buttons on the right | the office and the joke, side by side |
| Proof band | four numbers at 40 px in one row, the parent named beneath | proof before the persuasion, above the fold with the hero |
| Offers | three photographs in a row, 28 px funny lines | the three doors at once |
| Guarantee | 260 px + three columns: the care-ring illustration, the rule, the two lists | the promise and its mechanism on one screen |
| Packages | three columns, the middle one raised; 34 px prices | the comparison the buyer came for |
| Steps | four columns, the client's step icons above the text | the process as one line |
| References, team, Instagram | three photographs, three people, four embedded Reels | proof in breadth |
| Form | two columns with the photo drop zone and the message full-width; the promise next to the button | quick to complete at a desk |

## Tablet · 768–1023

Two- and three-column grids where they fit, the phone navigation and the dock kept, the hero as two columns with the photograph beside the copy.
