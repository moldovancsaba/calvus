
# Technical Implementation Notes

> **Warning:** This file is close to/exceeding 200 lines. Please split or modularize (or ask Lovable to automate) if adding more content.

## Architecture Decisions

### Why MongoDB Instead of Supabase PostgreSQL?
- **User Requirement**: Specifically requested MongoDB integration
- **Document Structure**: Natural fit for hierarchical triangle data
- **Flexibility**: Schema-less design accommodates future triangle properties
- **Atlas Integration**: Robust cloud hosting with minimal configuration

### Why Polling Instead of WebSockets?
- **Simplicity**: Easier to implement and debug than real-time subscriptions
- **Reliability**: Works consistently across different network conditions
- **Resource Management**: 5-second intervals balance real-time feel with API costs
- **Supabase Limitations**: Edge functions don't support persistent WebSocket connections

## Geometric Challenges Solved

### Spherical Triangle Subdivision
**Problem**: Standard planar triangle subdivision creates gaps on sphere surface

**Solution**: Implemented great circle midpoint calculation
```typescript
// Converts lat/lng to 3D coordinates, finds midpoint, projects back to sphere
export function sphericalMidpoint(p1: LatLng, p2: LatLng): LatLng {
  const point1 = latLngToPoint3D(p1);
  const point2 = latLngToPoint3D(p2);
  
  const midpoint = {
    x: (point1.x + point2.x) / 2,
    y: (point1.y + point2.y) / 2,
    z: (point1.z + point2.z) / 2
  };
  
  // Normalize to unit sphere - CRITICAL for maintaining sphere surface
  const length = Math.sqrt(midpoint.x * midpoint.x + midpoint.y * midpoint.y + midpoint.z * midpoint.z);
  midpoint.x /= length;
  midpoint.y /= length;
  midpoint.z /= length;
  
  return point3DToLatLng(midpoint);
}
```

### Geodesic Edge Rendering
**Problem**: Leaflet draws straight lines in map projection, not great circles

**Solution**: 50-point interpolation along great circle paths
```typescript
const greatCirclePath = (start: any, end: any, steps: number = 50) => {
  // Uses spherical linear interpolation (slerp) for accurate great circle
  const A = Math.sin((1 - f) * distance) / Math.sin(distance);
  const B = Math.sin(f * distance) / Math.sin(distance);
  // ... interpolation math
}
```

## Data Structure Design

### Hierarchical Triangle IDs
**Challenge**: Track subdivision relationships efficiently

**Solution**: Dot notation system
- Root triangles: `"1"`, `"2"`, `"3"`
- First subdivision: `"1.1"`, `"1.2"`, `"1.3"`, `"1.4"`
- Deep subdivision: `"1.4.2.3.1"`

**Benefits**:
- Easy parent-child relationship identification
- Natural sorting order
- Human-readable debugging
- Efficient string-based lookups

### Activity Storage Format
```typescript
{
  when: "2025-01-14T12:34:56.789Z",        // UTC ISO 8601 with milliseconds
  where: "1.4.2",                          // Hierarchical triangle ID
  what: 5,                                 // Click count level (alias for click_count, kept for backward comp.)
  click_count: 5,                          // Click count at write (snapshot, not delta)
  subdivided: true,                        // TRUE if subdivided at this snapshot, FALSE otherwise
  action_type: "click" | "subdivide",      // Nature of state change ("click" or "subdivide")
  level: 2,                                // Subdivision depth
  gametag: "player123",                    // Actor/player/user tag
  color: "#06D6A0",                        // Chosen color for this triangle state
  notes: "optional note about this action",// For debug/analytics, optional
  timestamp: Date                          // DB write time, can be used for ordering
}
```

**Design Rationale**:
- Each row in the table is a **full, standalone snapshot** of a triangle's state.
- `rebuildTriangleMeshFromActivities()` restores mesh by using the *latest row per triangle id* for lossless, race-free mesh recreation.
- Old incremental activities are discarded; no replay of historical deltas.

## Performance Optimizations

### Triangle Layer Management
**Problem**: Leaflet performance degrades with many overlapping polygons

**Solution**: Dynamic layer replacement
```typescript
// Remove existing layer before adding new one
const existingLayer = triangleLayersRef.current.get(trianglePath);
if (existingLayer) {
  map.removeLayer(existingLayer);
}
// Add new layer with updated properties
polygon.addTo(map);
triangleLayersRef.current.set(trianglePath, polygon);
```

### Subdivision Limiting
**Problem**: Infinite subdivision could crash browser

**Solution**: Hard limit at level 19
- Prevents exponential memory growth
- 19 levels = 4^19 potential triangles (manageable for local display)
- Visual indicator (red color) when limit reached

### Efficient State Rebuilding
**Problem**: Reconstructing triangle state from MongoDB activities

**Solution**: Sorted activity replay
```typescript
// Sort by timestamp to replay activities in chronological order
const sortedActivities = activities.sort((a, b) => 
  new Date(a.when).getTime() - new Date(b.when).getTime()
);

// Apply each activity to rebuild exact state
let currentMesh = baseMesh;
for (const activity of sortedActivities) {
  currentMesh = applyActivityToMesh(currentMesh, activity);
}
```

## Error Handling & Debugging

### MongoDB Connection Issues
- Comprehensive try-catch blocks with specific error messages
- Fallback to base mesh if loading fails
- Console logging for all database operations

### Geometric Edge Cases
- Handle antipodal points in great circle calculation
- Manage very close points with linear interpolation fallback
- Validate coordinates before conversion operations

### Real-time Sync Failures
- Graceful degradation when polling fails
- User notification via loading states
- Automatic retry mechanism through interval polling

## Known Technical Debt

### File Size Issues
- `TriangleMeshMap.tsx`: 299 lines (consider refactoring into smaller components)
- `triangleMesh.ts`: 296 lines (could split geometry utils from state management)

### Potential Improvements
1. **WebSocket Integration**: Replace polling with real-time subscriptions
2. **Spatial Indexing**: MongoDB geospatial queries for regional triangle loading
3. **Caching Layer**: Redis or in-memory cache for frequently accessed triangles
4. **Batch Operations**: Combine multiple triangle updates into single API calls
5. **Progressive Loading**: Load only visible triangles at current zoom level

## Security Considerations

### MongoDB URI Storage
- Stored securely in Supabase secrets (encrypted at rest)
- Never exposed to client-side code
- Accessed only through edge functions

### Input Validation
- Triangle ID format validation (dot notation pattern)
- Click count bounds checking (0-11 range)
- Level validation (0-19 range)
- Coordinate validation for triangle vertices

### CORS Configuration
- Permissive CORS for development (`Access-Control-Allow-Origin: *`)
- Should be restricted to specific domains in production

## Future Scalability Considerations

### Database Optimization
- Consider sharding by geographic regions
- Implement activity archiving for old data
- Add indexes on frequently queried fields (triangle ID, timestamp)

### Real-time Performance
- WebSocket implementation for instant updates
- Event-driven architecture for triangle state changes
- Conflict resolution for simultaneous clicks

### Global Distribution
- CDN for static assets
- Regional MongoDB clusters
- Edge function deployment in multiple regions

---

### Security, Edge, & Robustness (2025-06-14 Audit)

#### Security Threats & Fixes
- **Open Data:** All activities store world_slug but no RLS; multi-tenant attacks possible. Recommend strict RLS policies ASAP!
- **Input Sanitization:** All world slugs and gametags filtered for valid characters on the client, but server API could be hardened further.
- **Map Instance Reuse:** Leaflet would error when a container is initialized twice. We now forcibly destroy pre-existing map instances and clear container state in `LeafletMapContainer.tsx` before re-initialization, preventing memory leaks and stale state errors.
- **Edge Function Exposure:** API routes should validate action type AND ensure user is allowed to mutate target world.

#### Geometry & Mesh Learnings
- **Subdivision Limit:** 19-level hard stop works and prevents resource exhaustion. Attempting to subdivide further returns error or is ignored.
- **Restoration:** Mesh state is always rebuilt with last snapshot row per triangle. Sorting by timestamp is robust, but verify time sync between clients and DB.
- **Internal Concurrency:** Minor risk if two clients act on the same triangle at the same instant; last write wins. True real-time would require websocket conflation or consensus.

#### Performance Optimizations
- **Layer Cleanup:** To maintain correct Leaflet layers, all previous triangle polygons are cleaned up before redraw (no memory leaks).
- **Polling:** 5s interval balances real-time with reasonable API/DB load.

#### Known Gaps
- **No RLS on `triangle_activities`:** Security vulnerability, add policies!
- **No server-side slug collision detection:** Relying on world_slug being unique is client-enforced only.
- **No rate limiting in functions.**
- **No global undo/redo for mesh actions.**

---

## Learnings

- **Always destroy previous Leaflet map instances before mounting new ones.**  
- **Keep component and hook files < 50 lines where possible.**  
- **Test all edge cases on mobile (fixed zoom, slow drag, reload during subdivision).**  
- **Activity snapshotting is robust—never combine incremental & snapshot state models!**  
- **Throttle user actions per triangle to prevent accidental mesh spamming on mobile.**

---

## Edge Cases (2025-06-14)

- **Rapid join/leave of worlds can lead to zombie map instances.** Use effect cleanup aggressively!
- **Late arrival of polling can cause triangle overwrite, not actual data loss.**
- **DB downtime means mesh reconstructs to latest persisted shape at next reconnect.**
- **Max level (19) triangles turn red; clicks silently ignored past level 19.**

## Known Technical Debt

### File Size Issues
- `TriangleMeshMap.tsx`: 299 lines (consider refactoring into smaller components)
- `triangleMesh.ts`: 296 lines (could split geometry utils from state management)

### Potential Improvements
1. **WebSocket Integration**: Replace polling with real-time subscriptions
2. **Spatial Indexing**: MongoDB geospatial queries for regional triangle loading
3. **Caching Layer**: Redis or in-memory cache for frequently accessed triangles
4. **Batch Operations**: Combine multiple triangle updates into single API calls
5. **Progressive Loading**: Load only visible triangles at current zoom level

## Security Considerations

### MongoDB URI Storage
- Stored securely in Supabase secrets (encrypted at rest)
- Never exposed to client-side code
- Accessed only through edge functions

### Input Validation
- Triangle ID format validation (dot notation pattern)
- Click count bounds checking (0-11 range)
- Level validation (0-19 range)
- Coordinate validation for triangle vertices

### CORS Configuration
- Permissive CORS for development (`Access-Control-Allow-Origin: *`)
- Should be restricted to specific domains in production

## Future Scalability Considerations

### Database Optimization
- Consider sharding by geographic regions
- Implement activity archiving for old data
- Add indexes on frequently queried fields (triangle ID, timestamp)

### Real-time Performance
- WebSocket implementation for instant updates
- Event-driven architecture for triangle state changes
- Conflict resolution for simultaneous clicks

### Global Distribution
- CDN for static assets
- Regional MongoDB clusters
- Edge function deployment in multiple regions

---

This technical documentation serves as a guide for future development and debugging of the Triangle Mesh system.
**If this file reaches 300 lines, split into smaller docs. Use the modular docs reader at `/documents`.**
