# Triangle Mesh Interactive Map

A collaborative spherical triangle mesh system built with React, Leaflet, and MongoDB. Users can click on triangles to progressively subdivide them, creating a real-time collaborative mapping experience.

![Triangle Mesh Demo](https://via.placeholder.com/800x400/2563eb/ffffff?text=Triangle+Mesh+Map)

## Features

### 🌍 Interactive Spherical Mesh
- Fully mobile-first, minimal, responsive interface 🚀
- Identify yourself with a gametag & pick one of 16 colors, right from the main page
- Instantly log out/switch identity with one click/tap ("Log out" button)
- Leaflet-based map always keeps zoom between levels 5 and 15 (for a better global view)
- Three base triangles with geodesic edges on world map
- Click-based progressive subdivision (up to 19 levels)
- Hierarchical triangle identification system
- Real-time visual feedback with grayscale progression

### 🤝 Real-time Collaboration
- MongoDB-powered activity storage
- 5-second polling for live updates
- Persistent state across sessions
- Multi-user simultaneous interaction

### 🎨 Visual System
- Progressive grayscale: 10% darker per click
- Automatic subdivision after 10 clicks
- Red highlighting for maximum subdivision level
- Geodesic edge rendering prevents gaps/overlaps

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- MongoDB Atlas account
- Supabase project (for edge functions)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd triangle-mesh-map
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure MongoDB**
   - Create a MongoDB Atlas cluster
   - Add your MongoDB URI to Supabase secrets as `MONGODB_URI`
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`

4. **Start development server**
   ```bash
   npm run dev
   ```

## Architecture

### Frontend Components
- **TriangleMeshMap**: Main map component with Leaflet integration
- **Index**: Root page component

### Backend Services
- **triangle-activity**: Supabase Edge Function for MongoDB operations
- **triangleMesh.ts**: Core triangle geometry and subdivision logic

### Data Structure

#### Triangle Activity Schema
```typescript
{
  when: "2025-01-14T12:34:56.789Z",  // UTC ISO 8601 with milliseconds
  where: "1.4.2",                   // Hierarchical triangle ID
  what: 5,                          // Click count on this triangle (snapshot, not delta)
  level: 2,                         // Subdivision level
  click_count: 5,                   // Synonymous with 'what', full state at time of write
  subdivided: true,                 // Boolean, full state at time of write
  action_type: "click" | "subdivide", // Nature of the action leading to this state
  gametag: "player123",             // User identifier for the action
  color: "#06D6A0",                 // Player's chosen color for this triangle state
  notes: "optional debug info",     // For analytics or debug
  timestamp: Date                   // Database write timestamp
}
```
> The table stores a **snapshot** of the triangle's state at each relevant action (tap or subdivision).
> On reload, the mesh is *reconstructed using the latest row per triangle ID*, so no historical state is required.

#### Triangle Mesh Interface
```typescript
interface TriangleMesh {
  id: string;                       // Hierarchical ID (1, 1.1, 1.2, etc.)
  vertices: [LatLng, LatLng, LatLng]; // Three corner coordinates
  level: number;                    // Subdivision depth (0-19)
  clickCount: number;               // Number of user clicks
  subdivided: boolean;              // Whether triangle has children
  children?: TriangleMesh[];        // Sub-triangles after subdivision
}
```

## Configuration

### Environment Variables (Supabase Secrets)
- `MONGODB_URI`: MongoDB Atlas connection string
- `SUPABASE_URL`: Auto-configured Supabase project URL
- `SUPABASE_ANON_KEY`: Auto-configured Supabase anonymous key

### MongoDB Setup
1. Create a new database called `triangle_mesh`
2. Collection `triangle_activities` will be auto-created
3. No additional configuration required

## Usage Guide

### Basic Interaction
1. **Click any triangle**: Increases gray level by 10%
2. **10 clicks**: Triangle becomes fully gray
3. **11th click**: Triangle subdivides into 4 smaller triangles
4. **Continue clicking**: Subdivide up to 19 levels deep
5. **Final level**: Triangles turn red when fully subdivided

### Collaboration
- **Real-time updates**: Changes appear across all connected users
- **Persistent state**: Return anytime to see accumulated changes
- **Global activity**: See worldwide triangle interactions

### Data Management
- Activities are automatically stored in MongoDB
- Database is cleared on initial deployment for clean start
- All triangle interactions are permanently logged

## API Reference

### Edge Function Endpoints

#### Store Triangle Activity
```javascript
POST /functions/v1/triangle-activity
Content-Type: application/json

{
  "action": "click",
  "triangleId": "1.4.2",
  "clickCount": 5,
  "level": 2
}
```

#### Get All Activities
```javascript
GET /functions/v1/triangle-activity
```

#### Clear All Activities
```javascript
POST /functions/v1/triangle-activity
Content-Type: application/json

{
  "action": "clear"
}
```

## Development

### Key Files
- `src/components/TriangleMeshMap.tsx`: Main map component (299 lines)
- `src/utils/triangleMesh.ts`: Core triangle logic (296 lines)
- `supabase/functions/triangle-activity/index.ts`: MongoDB API

### Geometric Algorithms
- **Spherical midpoint calculation**: Great circle interpolation
- **Geodesic triangle rendering**: 50-point great circle approximation
- **Coordinate conversion**: 3D sphere ↔ lat/lng transformation

### Performance Considerations
- 5-second polling interval balances real-time feel with API load
- Triangle subdivision limited to 19 levels to prevent memory issues
- Geodesic rendering uses 50 interpolation points for smooth edges

## Troubleshooting

### Common Issues

1. **Triangles not appearing**
   - Check MongoDB URI configuration in Supabase secrets
   - Verify edge function deployment status

2. **No real-time updates**
   - Confirm MongoDB connection in function logs
   - Check browser console for polling errors

3. **Subdivision not working**
   - Ensure 11 clicks registered (check console logs)
   - Verify triangle level < 19

### Debug Information
- All triangle interactions logged to browser console
- Edge function logs available in Supabase dashboard
- MongoDB operations logged with timestamps

## Contributing

### Code Style
- TypeScript strict mode enabled
- Tailwind CSS for styling
- Functional React components with hooks
- Comprehensive error logging

### Testing Workflow
1. Test triangle clicking and subdivision
2. Verify real-time synchronization with multiple browser tabs
3. Check MongoDB data persistence after page reload
4. Validate geodesic edge rendering at various zoom levels

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section above
- Review browser console and edge function logs
- Verify MongoDB connection and Supabase configuration

## Security & Technical Audit (2025-06-14)

### Security & Vulnerability Assessment
- **Access Controls:** All sensitive write/clear actions are funneled through Supabase Edge Functions. RLS (Row Level Security) should be added to `triangle_activities` for further safety; currently, this is still open (⚠ see tech notes).
- **User Data:** Gametag/identity is stored locally and attached to mesh activity. Input validation exists for gametag and worldSlug, but consider additional server-side validation.
- **Secrets:** Project uses Supabase secrets for DB credentials; never exposed to the client.
- **Container Reuse:** Map reuse errors are now trapped and prevented by the initialization logic, protecting map state on fast page transitions.
- **Input Validation:** All user inputs for slugs and gametags are regex filtered for allowed chars.

### Resilience & Edge Case Handling
- **Subdivision:** Recursive mesh logic stops cleanly at 19, never deeper (avoiding memory/DOM explosion).
- **State Corruption:** Triangle activity snapshots are always the latest per-triangle; mesh restoration is repeatable and lossless unless DB is tampered/corrupted.
- **Race Conditions:** Polling logic means some rare conflicting writes can result in delayed updates between clients, but not data loss.

### Recommendations from Audit
- **Add RLS to `triangle_activities` for secure multi-tenant worlds.**
- **Add more toasts/UI feedback for poll error states.**
- **Break up large files for maintainability.**
- **Improve global error banners for major API/db failures.**
- **Automated e2e testing for user and mesh flows.**

## Troubleshooting—Audit Edition

- Container reuse: If you see “Map container is being reused,” ensure you don’t have stale components or open tabs rapidly switching worlds; refresh solves the state.
- Slow polling: Check Supabase Function logs for triangle-activity. DB slowness causes lag.
- Mesh not updating: Try leaving/rejoining the world, or clearing browser cache if mesh is stuck.
- Edge Function errors: Review the Supabase logs for activity.

---

## Technical Achievements & Learnings
### Learnings & Innovations
- **Geodesic Geometry**: Implemented proper spherical triangle subdivision
- **Real-time Collaboration**: Achieved multi-user synchronization without WebSockets
- **Hierarchical Data**: Created intuitive dot-notation triangle identification
- **Progressive Interaction**: Designed engaging click-to-subdivide mechanic
- **Cross-Platform Storage**: Successfully integrated MongoDB with Supabase Edge Functions

### Performance Optimizations
- Efficient triangle rendering with polygon caching
- Minimal API calls through batched updates
- Memory-conscious subdivision limiting
- Smooth geodesic edge approximation

---

Built with ❤️ using React, Leaflet, MongoDB, and Supabase
