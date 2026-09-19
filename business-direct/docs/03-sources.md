# business.direct — sources and assets

| Content | Source | Real or sample |
|---|---|---|
| 431 listings: name, category, locality, county, address, coordinates, website, description, verified/checked date, when, hours, next session | `data/fetch-sportolok.py` → `data/listings.json`, from sport.doneisbetter.com's public API and listing pages' JSON-LD, 2026-09-19 | **real** — public data only; re-run to refresh |
| Facets, territory levels, age bands, site copy | same → `data/platform.json` | real |
| Claim state | inferred: the claim prompt appears on every listing | real (none claimed) |
| A claimed business's brand voice, offers, sessions, campaign results, approval items, integration states | written for the prototype | **sample**, declared on the page |
| Consumer personas (saved items, location, age band, channel preferences) | written for the prototype | sample |
| Research figures | `01-research.md`, each with its link; primary vs aggregator marked | real, cited |
| The target shape | two owner-supplied videos (`02-audit.md` §3), 42 frames extracted with a Swift/AVFoundation script — the videos themselves are not in the repo | owner input |
| Terms, tokens, stack | DiscountDirect's SSOT, GDS token map, ARCHITECTURE (D26) | inherited (D5) |

No listed business, consumer or platform account is contacted or written to by the
prototype. `POST /api/ingest` is documented but never called.
