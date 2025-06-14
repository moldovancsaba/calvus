

# Changelog

All notable changes to the Step project will be documented in this file.

## [2.0.1] - 2025-06-14

### Changed
- Canonical global mesh now set at **26 base triangles (T1–T26)** using agreed spiral/vertex order.
- Updated all documentation and internal references from 18/24 to **26** triangles as base mesh count.

## [2.0.0] - 2025-06-14

### Changed
- App renamed from **Icosahedral Geodesic Grid** to **Step** (historical name; only referenced here for clarity)
- Removed popup notifications for triangle activity and invalid clicks for a sleeker user experience
- Documentation modularized: All content now lives in `/documents` and is kept up to date there
- Project refactored: Code over 200 lines is split. Structure and docs now modular and maintainable

## [1.0.0] - 2025-01-14

### Added
- **Spherical Triangle Mesh System:** Geodesic mesh covering the globe
- **MongoDB Integration:** Real-time triangle state persistence
- **Triangle IDs:** Dot notation for hierarchical subdivision tracking
- **Live Sync:** Polling every 5 seconds (not real-time sockets)
- **Progress Bar:** Clicking fills triangles by 10% increments, subdivision after 11th click
- **Subdivision Limit:** Up to 19 levels max (see code)
- **Snapshot Model:** Each saved activity row is a full state/snapshot (from 1.2.0 onward)
- **Mobile Support:** Clean responsive design out of the box

### Initial Configuration
- **26 base triangles** cover the globe (see geometry.ts and technical-architecture.md for full math rationale)
  - Example (T1): (0°, -180°), (66°, -144°), (0°, -108°)

### Known Limitations
- 5-second polling may cause short delay
- Max 19 subdivision levels enforced in code
- **Canonical mesh = 26 triangles**
- Requires valid Supabase and MongoDB configuration

## [1.1.0] - 2025-06-14

### Added
- Mobile-first, minimal, and responsive mesh UI
- Identity controls always accessible (gamer tag, color picker, quick logout)
- Map zoom strictly limited to levels 5–15

### Changed
- "IdentityGate" is shown only on first load; updates/swaps in main UI
- Mesh UI compacted for mobile/touch focus

## [1.2.0] - 2025-06-14

### Changed
- **DB Model:** All activity persistence now stores full triangle state as a snapshot (not incremental logs)
- **Mesh Restore:** All mesh rebuilt from most recent per-triangle snapshot (never from deltas)
- **Schema:** `where`, `when`, `gametag`, `color`, `click_count`, `level`, `subdivided`, `action_type`, `notes`

### Data Model (from 1.2.0+)
- Each triangle activity snapshot row stores:
  - `where`, `when`, `gametag`, `color`, `click_count`, `level`, `subdivided`, `action_type`, `notes` (see technical docs)

### Migration
- **Old incremental logging removed as of 1.2.0**
- UI/state loading is now much more robust

## [1.2.1] - 2025-06-14

### Audit & Documentation

- Full security and robustness audit of mesh, map, and storage
- File-size/complexity flags added, modular code enforced
- Fixed map container reuse bug, now fully documented and handled
- Documentation unified: all technical docs now reflect canonical geometry and state

