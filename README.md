# Step

A collaborative spherical triangle mesh system built with React, Leaflet, and MongoDB.  
**Version: 2.0.0 – June 2025**

## Overview
**Step** is an interactive, collaborative mesh on the globe, enabling shared exploration and graph-based gameplay.
- All documentation is modularized under `/documents` for easy navigation.
- This README acts as a quick reference and project intro.

### Key Features
- Interactive world mesh (**24 base triangles**, 19 subdivision levels)
- Live collaboration across devices (updates each 5 seconds for all users)
- Instant “gamer tag” and color personalization (change anytime in UI)
- Subdivision, coloring, and subdivision limits (see below)
- All code and docs are modular, well-annotated, and organized

## How It Works

- **Live Polling:** The mesh syncs every 5 seconds for smooth, collaborative gameplay. Data is never stale more than 5s.
- **Gamer Identity:** Choose a unique "gamer tag" and color—instantly visible on your actions. Logout resets identity.
- **Mesh Tapping:** Click/tap a triangle to “claim” and shade it by increments. The 11th click subdivides the triangle, up to level 19.
- **Persistence:** Snapshots record each triangle’s state. State is always restored via the latest snapshot—never legacy deltas.
- **Current Model:** Activity is per-triangle (not an incremental log).  
- **Security:** No user secrets are exposed to clients. Client updates are checked only for correct world. RLS not yet applied server-side.
- **Limitations:** 
  - Final (level 19) triangles turn red, no further actions allowed.
  - Up to 19 subdivision levels per triangle.
  - No true real-time/WebSocket support (see roadmap in `/documents`).

## Documentation Modules

Find complete details in `/documents`:

- [User Guide (README)](/documents)
- [Technical Architecture](technical-architecture.md)
- [Performance Optimizations](performance-optimizations.md)
- [Security & Scalability](security-scalability.md)
- [Changelog](CHANGELOG.md)

All files above are linked in the app (via settings or /documents route).

---

### Contributing

- Stick to modular, clear code organization. Refactor files >200 lines, maintain readability.
- See `/documents/TECHNICAL_NOTES.md` for coding and onboarding guides.
- **Support:** For help, [open an issue on your code host or join our Discord] (link).

---

### Terms Glossary

| Term            | Definition                                                                        |
|-----------------|-----------------------------------------------------------------------------------|
| Step mesh       | The project’s core interactive triangle mesh on the globe                         |
| Subdivision     | Splitting a triangle into four smaller triangles (occurs at 11th click if allowed)|
| Polygon/Triangle| Used interchangeably for mesh faces                                               |
| Gamer tag       | Your personal display name for mesh actions                                       |
| Snapshot        | Aggregate state of a triangle at the time of a user action                        |
| World slug      | Unique key for parallel session/mesh worlds (route: `/game/:slug`)                |
| Activity        | A row in the DB recording a triangle’s click/subdivision + owner/color            |
| **Base mesh**   | Canonical set of 24 initial (level 0) triangles as of v2.1 (see technical docs)   |

---

## License

MIT

---

> **Note:** All substantive documentation and guides are in `/documents` as Markdown.
> - `README.md` — user & dev intro  
> - `TECHNICAL_NOTES.md` — architecture, code, and onboarding  
> - `CHANGELOG.md` — version history

**If this file exceeds 200 lines, modularize by splitting off sections as shown above.**
