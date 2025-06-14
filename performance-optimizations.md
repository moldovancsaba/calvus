
# Performance Optimizations & Edge Cases

## Triangle Layer Management
- Old layers are always cleaned up to ensure optimal map draw speed and prevent memory leaks.

## Subdivision Limiting
- Strictly capped at level 19 subdivisions (enforced in code, cannot exceed).

## State Restoration & Rebuilding
- Triangle state is **always** restored from the latest snapshot per triangle. No incremental/delta replay logic remains.
- "Replay" is resilient against network or user interruptions; the mesh always matches the underlying DB snapshot.

## Error Handling & Debug UX
- Where possible, failures to save or fetch are caught and logged to the console.
- The UI always remains interactable and never locks up; lost actions can always be retried.
- Map and mesh hot-reload errors are handled gracefully with clear code (no user confusion or blank map after reload).

## Edge Cases (2025-06-14)
- Rapid user join/leave: Re-creates and destroys map and mesh instances to prevent artifacting.
- Mesh coloring: When a triangle hits level 19, it turns red—no further actions allowed (fully enforced).

---

_For security, database, and scaling strategies, see [`security-scalability.md`](security-scalability.md)._

<!--
NOTE:
- Triangle state is now only reconstructed from per-triangle snapshots.
- All code and docs reference the 18-triangle canonical mesh, as of the current version.
-->
