
# Security & Scalability

## Security Considerations

- All database connection secrets (e.g., MongoDB URI) are stored only in Supabase secrets and never exposed to the client.
- Input validation is applied for all critical activity: triangle IDs, click bounds, and subdivision.
- CORS is permissive in development but restricted in production environments.

## Implementation Limitations
- No server-side row-level security (RLS) or API-side world_slug validation currently enforced; all triangle activities are scoped client-side. (Planned for future)
- Unique world_slug is enforced only in the client/application, not on the backend for now.

## Scalability & Future-Proofing

- Sharding, caching, and batch database operations are planned as needs grow.
- Progressive, region/zoom-based mesh loading designed for performance on large meshes.

## Implementation Learnings
- Explicitly destroy map and mesh instances during reloads to prevent resource leaks.
- All code and documentation is split into small, focused, and maintainable files (≤100–200 lines/file wherever possible).
- **Triangle mesh base is 18 triangles, matching the geometry.ts implementation.**

---

_Last reviewed: 2025-06-14_

