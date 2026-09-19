# Lexodont — decision register

*Reconstructed on 2026-09-18 from the 24 commits of 2026-03-31 and 2026-04-09; nothing
else was recorded at the time. "Client" is Lexodont; "owner" is the Calvus side.*

| # | Date | Decision | By | Trace |
|---|---|---|---|---|
| D1 | 2026-03-31 | Project named Lexodont (was "Lexodent"); a hub page links every project | owner | `c6e9874`, `7656aee` |
| D2 | 2026-03-31 | Structure: home + linked landing pages per specialty, team, cases, knowledge | owner, on the brief | `2fdd358` |
| D3 | 2026-03-31 | 13-person crew section with hero/team assets; then crew reduced and fun facts placed under names, square portraits, alternating layout | client feedback | `746ac72`, `22121cf`, `e61373c`, `e6c3d67` |
| D4 | 2026-03-31 | Subpages standardised with complete, content-ready layouts | owner | `7f1a5ee` |
| D5 | 2026-03-31 | Classic wireframe style: grey palette, no radius, no shadow, placeholder images | owner | `cc6dcf7`, `5508d4f` |
| D6 | 2026-03-31 | Booking and WhatsApp CTAs split into two buttons | client feedback | `298a2af` |
| D7 | 2026-03-31 | Treatment prices removed from the home cards; a dedicated Áraink page instead | client feedback | `f6b7cab`, `541dd96` |
| D8 | 2026-03-31 | Contact, hours, parking, transport and an OpenStreetMap embed move into the footer | client feedback | `97e870d`, `edc0dd9` |
| D9 | 2026-03-31 | Interactive before/after sliders on home and case studies | owner | `5508d4f` |
| D10 | 2026-03-31 | A Balsamiq-style sketch variant of the full page set, same content | owner | `51d2917`, `48d1c91` |
| D11 | 2026-03-31 | One navigation and CTA set on every page | owner | `2c4c296` |
| D12 | 2026-04-09 | Client feedback round applied; Szakterületek and Partnereink on the home reworked; featured specialties in two columns | client | `bacdab2`, `e896bec`, `898f55e` |
| D13 | 2026-04-09 | Orphan links fixed; three missing treatment pages (gyerekfogászat, gyökérkezelés, parodontológia) added to the polished set only | owner | `eaa8a66` |
| D14 | 2026-09-18 | The wireframe is superseded by the live lexodont.hu; it is kept as the record, its remaining defects recorded rather than fixed; the standard documentation set written | owner | this folder |
| D15 | 2026-09-18 | The three treatment pages missing from the sketch set are mirrored from the sketch template so both fidelities carry the same page set again and the gate's parity check is clean | owner | `lexodont.hu_balsamic/{parodontologia,gyokerkezeles,gyerekfogaszat}.html` |
| D16 | 2026-09-20 | A **responsible-data policy record** for the practice (SSOT §4b, PROPOSED): health data as a special category, children as patients through parents, the booking processor named, media consent, no marketing without consent — with rules R8–R10 and the gate rows for the production site | Calvus, on the owner's directive (responsible data for every client) and the hub audit | the wireframe stores nothing; the record binds the built site |

## What the live site decided without this repo

Real prices, four real dentists, real photography, Google Maps instead of OSM, a
Flexi-Dent booking page, a Technológiák page, EN via WPML, no WhatsApp CTA — see
`02-audit.md`. None of these came through a recorded decision here.
