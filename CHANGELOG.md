
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
