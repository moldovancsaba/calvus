# Holdvölgy 2026 — project documentation

Owner directive 2026-09-16: the whole process is documented next to the project —
research, findings, decisions, assets, and every build round. This folder is that
record. Each file is dated inside; this index is the process log.

| File | What it holds |
|---|---|
| `00-plan.md` | Research findings and the phased implementation plan — the approval document |
| `01-research-benchmarks.md` | Every estate site read, what it returned, and the sites that could not be reached |
| `02-brand-and-site-audit.md` | Holdvölgy's measured brand tokens, fonts, page architecture, product/booking/club pages, and defects found |
| `03-asset-inventory.md` | The 180 real images on the live site, grouped by use, with formats and sizes read from headers |
| `asset-inventory.json` | The same inventory, machine-readable: base image URL → pages it appears on |
| `04-decisions.md` | Decision log — what was decided, by whom, why, and what it replaced |

## Process log

**2026-09-16 — first prototype (withdrawn as a direction).** Commit `8342956` built a
two-page prototype on a dark ground with a gold accent and a serif display face, from
content fetched off holdvolgy.com. Owner rejected the aesthetic as generic ("the same
colour and typography everywhere") and required industry research before any
further build.

**2026-09-16 — technical context received.** The client's technical situation report,
25-task work list, offer template, the incumbent developer's priced offer and their
scheduling note were shared so the prototype work has the full picture. Commercial
response to those is explicitly not part of this project; the four acceptance
targets (server response < 800 ms, home page < 1,5 MB, < 12 front-end plugins, live
alerting) and the 15 Oct – 15 Jan change freeze are carried as constraints.

**2026-09-16 — research round.** 21 estate sites read (Napa, Sonoma, Bordeaux,
Champagne, Sauternes, Tuscany, Bolgheri, Mendoza, Lebanon, Uruguay, Chile, South
Africa, Rheingau, Tokaj/Mád, Armenia), the World's 50 Best Vineyards 2025 list, the
Awwwards wine gallery; Holdvölgy's own Elementor kit, fonts, page structures, product
pages, booking form, loyalty and Trezor pages read from the live site; 180 images
inventoried without downloading any. Findings in `01`–`03`, plan in `00`.

**2026-09-16 — decisions.** Owner: mobile and desktop are two designed experiences
(D5); commercially free web fonts, Google Fonts preferred (D3); the five-item
navigation is approved (D4); item data will be supplied by the client; full
documentation next to the project (this folder). Plan updated accordingly.

**Next.** Phase 1 of `00-plan.md` on approval of the direction in its §4.
