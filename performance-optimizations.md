
# Performance Optimizations & Edge Cases

## Triangle Layer Management
- Cleans up Leaflet layers for optimal redraw speed.

## Subdivision Limiting
- Level 19 hard stop (prevents memory overload).

## Efficient State Rebuilding
- Snapshots replace deltas; replay is robust and resilient against network issues.

## Error Handling & Debugging
- Graceful fallbacks, try-catch for DB, console logs for map and mesh loading.

## Known Edge Cases (2025-06-14)
- Rapid join/leave: Clean up map instances!
- Mesh coloring: level 19 turns red, no further clicks allowed.

---

_For security, database, and scaling, see [`security-scalability.md`](security-scalability.md)._
