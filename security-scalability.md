
# Security & Scalability

## Security Considerations

- MongoDB URI secured in Supabase secrets, never client-exposed.
- Input validation: Triangle IDs, click bounds, etc.
- CORS: dev permissive, restrict in prod.

## Known Vulnerabilities
- No server-side RLS yet (add soon for real security!)
- Relying on unique world_slug client-side only.

## Scalability & Future Proofing

- Sharding, caching, batch ops—all planned for further scale.
- Progressive loading by region and zoom planned for large userbases.

## Learnings
- Destroy map instances before remounting
- All code and docs now modular & ≤100 lines where possible

_Last reviewed: 2025-06-14_
