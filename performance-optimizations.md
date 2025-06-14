

# Performance Optimizations & Edge Cases

## Triangle Layer Management
- Old layers are always cleaned up to ensure optimal map draw speed and prevent memory leaks.

## Subdivision Limiting
- Strictly capped at level 19 subdivisions (enforced in code, cannot exceed).

## State Restoration & Rebuilding
- Triangle state is **always** restored from the latest snapshot per triangle. No incremental/delta replay logic remains.
- "Replay" is resilient against network or user interruptions; the mesh always matches the underlying DB snapshot.

## Edge Cases (2025-06-14)
- Rapid user join/leave: Re-creates and destroys map and mesh instances to prevent artifacting.
- Mesh coloring: When a triangle hits level 19, it turns red—no further actions allowed (fully enforced).

## Canonical Base Mesh Shape
- The canonical base mesh is now **26 triangles** (from June 2025 on), with IDs T1–T26 and agreed vertex order. All other mesh structure, state, and hierarchy is unchanged.

---

_For security, database, and scaling strategies, see [`security-scalability.md`](security-scalability.md)._

