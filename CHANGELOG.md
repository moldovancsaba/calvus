# Changelog

All notable changes to the Triangle Mesh project will be documented in this file.

## [1.0.0] - 2025-01-14

### Added
- **Spherical Triangle Mesh System**: Complete implementation of a geodesic triangle mesh on a world map
- **MongoDB Integration**: Real-time storage and retrieval of triangle click activities
- **Hierarchical Triangle IDs**: Dot-notation system (1, 1.1, 1.2, 1.3, 1.4) for subdivision tracking
- **Real-time Collaboration**: 5-second polling for live updates across multiple users
- **Geodesic Edge Rendering**: Proper great circle paths to prevent gaps and overlaps
- **Progressive Grayscale System**: 10% gray increment per click (up to 100%)
- **Automatic Subdivision**: 11th click triggers 4-way triangle subdivision
- **Deep Subdivision Support**: Up to 19 levels of recursive subdivision
- **Final State Indicator**: Red coloring for maximum subdivision level triangles
- **Activity Persistence**: when/where/what data structure in MongoDB

### Technical Implementation
- **Frontend**: React + TypeScript + Leaflet for interactive mapping
- **Backend**: Supabase Edge Functions for serverless API
- **Database**: MongoDB Atlas for triangle activity storage
- **Real-time Updates**: Polling-based synchronization every 5 seconds
- **Coordinate System**: Spherical geometry with lat/lng conversion

### Initial Configuration
- Three base triangles covering portions of the northern hemisphere
- Base triangle coordinates:
  - Triangle 1: (66°N, 0°E), (0°N, -36°E), (0°N, 36°E)
  - Triangle 2: (66°N, 0°E), (66°N, 72°E), (0°N, 36°E)
  - Triangle 3: (66°N, 0°E), (66°N, -72°E), (0°N, -36°E)

### Known Limitations
- 5-second polling interval may cause brief delays in collaboration
- Maximum 19 subdivision levels to prevent performance issues
- Northern hemisphere focus in initial triangle placement
- Requires MongoDB URI configuration for full functionality

## [1.1.0] - 2025-06-14

### Added
- **Mobile-first Minimal Design**: Upgraded to a fully responsive, mobile-first layout with clean minimal design
- **Identity Controls**: Gametag and 16-color color picker now always available on the main page, with "Log out" for quick switching
- **Map Zoom Range**: Map zoom is strictly limited between levels 5 and 15

### Changed
- IdentityGate is now used only for first-time users; afterwards, identity can be adjusted or cleared directly from main UI
- Triangle Mesh Map is more compact, touch-friendly, and visually streamlined

## [1.2.0] - 2025-06-14

### Changed
- **Database Model**: Triangle activity persistence is now based on full triangle state snapshots (`click_count`, `subdivided`, `action_type`, color, gametag, when).
- **Mesh Rebuild**: The mesh is reconstructed using last known state for each triangle, ensuring no loss or rollback after page reload.
- **Codebase Consistency**: Aligned all click/save/restore logic to new schema and behavior. Legacy incremental actions are discontinued.

### Data Model (as of 1.2.0)
Each triangle activity snapshot row now stores:
- `where` (triangle id)
- `when` (ISO string timestamp of event)
- `gametag` (player who acted)
- `color` (player color for that triangle state)
- `click_count` (the latest tap count for this triangle, accurate at save)
- `level` (subdivision level of triangle)
- `subdivided` (boolean: true if split into children)
- `action_type` ("click" or "subdivide" or other, for future-proofing)
- `notes` (optional, for debugging or analytics)

### Migration
- All previous mesh activity data is wiped as state is not compatible.
- Upgraded UI and backend for reliable world mesh restoration.
