
# Technical Architecture

## Why MongoDB Instead of Supabase PostgreSQL?
- User requirement and natural hierarchical fit for triangles
- Flexible, schema-less, easy geometric data expansion
- Hosted on MongoDB Atlas with secure access via Supabase edge

## Why Polling Not WebSockets?
- Simpler, robust, fits Supabase Edge limitations
- 5-second polling is practical for near-real-time collaboration

## Geometric Challenges Solved

### Spherical Triangle Subdivision
- Ensures seamless great circle subdivision (see code snippet in docs).

### Geodesic Edge Rendering
- 50-point interpolation on great circle, accuracy critical for world mesh.

## Data Structure Design
- Triangle IDs: dot notation (e.g., `"1.2.4"`)
- Activity snapshots (see changelog and performance docs for rationale)
- State is restored by taking the latest snapshot per triangle

---

_For performance, error handling, and more, see [`performance-optimizations.md`](performance-optimizations.md)._

<!-- Updated: base triangle mesh = 18 triangles (not 20) -->
