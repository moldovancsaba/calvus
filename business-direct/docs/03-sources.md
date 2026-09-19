# business.direct — sources and assets

| Content | Source | Real or sample |
|---|---|---|
| 252 providers with every field listed in `02-audit.md` §2 | `data/fetch-yourfield.py` → `data/providers.json`, from getyourfield.com's public API, 2026-09-19 | **real** — public data only; re-run to refresh |
| Boroughs, neighbourhoods, activity counts, site copy | same → `data/platform.json` | real |
| Claim state | the API's `claimStatus` (15 `unclaimed`; the rest unset) | real |
| The Hungarian reference instance (431 listings) | `data/fetch-sportolok.py` → `data/reference-sportolok/` | real, reference only |
| The provider persona's brand voice, knowledge files, campaign results, approval items, integration states | written for the prototype around **Brooklyn Force Soccer** (a real, explicitly unclaimed provider) | **sample**, declared on the page |
| The family persona (a Park Slope parent, two children, saved items, channel preferences) | written for the prototype; the saved providers are real | sample |
| Research figures | `01-research.md`, each with its link; primary vs aggregator marked | real, cited |
| The target shape | two owner-supplied videos (`02-audit.md` §4), 42 frames extracted with a Swift/AVFoundation script — the videos themselves are not in the repo | owner input |
| Terms, tokens, stack | DiscountDirect's SSOT, GDS token map, ARCHITECTURE (D26) | inherited (D5) |

No provider, family or platform account is contacted or written to by the prototype.
