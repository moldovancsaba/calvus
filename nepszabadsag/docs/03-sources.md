# Népszabadság — sources and gaps

*What every finding in this documentation set is built from, and every gap between the ask
and what is actually in hand. Written 2026-09-21.*

| Content | Source | Real or gap |
|---|---|---|
| The landing page's seven sections, copy and states | `nsz_landing_20260914_v1.docx`, read in full 2026-09-21 | **real**, quoted verbatim in `handover.md` §1 |
| The site's page set, section names, chrome and business model (registration wall, 3 290 Ft print+online from 2026-11-15, ad slot sizes) | the Figma file "Népszabadság" (`RVrEZZJdxBZdiZs2MJrJUD`), eight frames read on screen at 50%/100% zoom, 2026-09-21 | **real** structure; **not real** colours, exact type sizes and spacing — Dev Mode is not enabled here (`handover.md` §3) |
| Provisional design tokens | `assets/tokens.css`, read from the screen | **sample** — placeholders until the Figma spec is exported |
| The 25-site technical benchmark (stack, weight, TTFB, fonts, nav, colour) | `curl` from this environment, 2026-09-21 (`01-research.md` §1) | real, measured |
| The rendered-layout study (grid, colour as rendered, typography, density) at 1440 and 390 | the app's browser pane, 2026-09-21 (`01-research.md` §7) | real, measured; NYT, WSJ, FT, Zeit and WaPo could not be reached — their layouts rest on published sources instead |
| Reuters Institute Digital News Report 2026 (Hungary): trust, payment, brand reach, media-capture context | fetched directly 2026-09-21 (`01-research.md` §2) | real, cited **P** |
| Subscription/paywall conversion and pricing benchmarks | trade press and one 2025 European pricing study (Funds4Media, 101 titles) (`01-research.md` §3) | real, cited, mostly **A** (secondary); no CEE-specific print+digital bundle benchmark exists in the source |
| Népszabadság's 2016 closure | four sources cross-checked: Euronews, Human Rights Watch, RSF's own statement, Direkt36's investigative retrospective (`01-research.md` §4) | real, cited, cross-corroborated |
| Comparable relaunch cases (Magyar Nemzet, The Independent's post-print transition, **the real Népszava's 2026 crisis**) | Wikipedia, Balkan Insight, a Reuters-Institute-hosted academic study (`01-research.md` §5) | real, cited; the Népszava finding is the one item here that changes a brief-level decision — see `00-brief.md` |
| Published design-system references (Guardian Source, NYT typefaces, Spiegel's 2016 redesign) | the Guardian's own design-system site (primary), Fonts In Use (secondary, for NYT's proprietary type), Spiegel's own dev blog (fetch blocked; used via a verified search summary) (`01-research.md` §6) | real, cited; the NYT and Spiegel items lean on secondary or unverified-by-direct-fetch sources — flagged in place |
| nepszava.hu: stack, weight, cache headers, `robots.txt`, the digital-edition login system, the third-party vendor (xximedia.hu), the 2026 ad rate card | `curl`, 2026-09-21 (`01-research.md` §8) | real, measured and quoted from the vendor's own pages and PDF — but **not this project's own asset**: the owner confirmed 2026-09-21 that calling nepszava.hu "the sister site" in the original briefing was a mistake; kept here as an unaffiliated market comparable only |
| nol.hu (the old domain) | `curl`, 2026-09-21 (`02-audit.md` §4) | real — a one-line stub; the archive is sold via lapcentrum.hu, not audited here |
| The built prototype's headlines, deks, bylines, reading times and the Cikkoldal's full body text (Belföld, Gazdaság, Kultúra, Külföld, Média/Vélemény, Népszava — twenty items) | read directly off the Figma frames, 2026-09-21 (`content.py`, `source: "figma"`) | **real** — the client's own copy, used verbatim; the Cikkoldal needed no invented continuation because the Figma's paywall box marks exactly where the free text ends |
| Two Sport and Tudomány Címlap items | written for this prototype — the Figma designs no rovat front for either category | **sample**, declared `source: "original"` in `content.py`; neutral, evergreen, no real named official quoted |
| Fourteen photographs across every page | Wikimedia Commons, downloaded and resized 2026-09-21, license and author recorded per image in `content.py IMAGES` | **real** photographs, appropriately licensed (CC BY / CC BY-SA / public domain); several are topical illustrations rather than the article's literal documentary subject — marked with a `note` in `content.py` and stated in the on-page photo credit |

## Gaps — what the client (or a next session) still needs to supply

1. **~~The Népszava sub-brand name~~ — resolved 2026-09-21.** The owner confirmed the Figma's
   internal Népszava section is unrelated to the real newspaper of that name, and that
   describing nepszava.hu as this project's "sister site" during the original briefing was
   itself a mistake — see `00-brief.md` and `02-audit.md`.
2. **Exact design tokens.** Figma Dev Mode (MCP server) or an export of the eight frames as
   PNG plus the variables list — `handover.md` §3.
3. **Logo files and type licences** — the built pages use a CSS approximation of the mark
   and Google-hosted fonts (Source Serif 4, Inter), not the client's own files. **The
   frames' own photographs** are still placeholders in Figma; the built prototype uses real,
   appropriately-licensed Wikimedia Commons photos as a stand-in (no AI-generated imagery,
   per the repo rule) — real client photography is still the eventual real gap.
4. **A Szerkesztőség's "utolsó poszt"** — which channel supplies the latest post (blog,
   Instagram, Facebook) that the landing page and the front page both promise to show.
5. **Who receives the landing page's registration form** (Vezetéknév, Keresztnév, e-mail) —
   the client's developer, or this prototype.
6. **Whether the new title's paywall/reader is built in-house or through a vendor** — not a
   decision this project inherits from anyone; nepszava.hu's own unaffiliated third-party
   approach (xximedia.hu) is one real-world data point to weigh, nothing more
   (`01-research.md` §8).
