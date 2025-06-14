export interface Point3D {
  x: number;
  y: number;
  z: number;
}

export interface LatLng {
  lat: number;
  lng: number;
}

export interface TriangleMesh {
  id: string;
  vertices: [LatLng, LatLng, LatLng];
  level: number;
  clickCount: number;
  subdivided: boolean;
  children?: TriangleMesh[];
}

// TypeScript type for DB row
type TriangleActivityRow = {
  id: string;
  when: string;
  where: string;
  what: number;
  level: number;
  timestamp: string;
};

// Convert 3D point to lat/lng coordinates
export function point3DToLatLng(point: Point3D): LatLng {
  const lat = Math.asin(point.z) * (180 / Math.PI);
  const lng = Math.atan2(point.y, point.x) * (180 / Math.PI);
  
  return { lat, lng };
}

// Convert lat/lng to 3D point on unit sphere
export function latLngToPoint3D(latLng: LatLng): Point3D {
  const latRad = latLng.lat * (Math.PI / 180);
  const lngRad = latLng.lng * (Math.PI / 180);
  
  return {
    x: Math.cos(latRad) * Math.cos(lngRad),
    y: Math.cos(latRad) * Math.sin(lngRad),
    z: Math.sin(latRad)
  };
}

// Generate the eight base triangles for the spherical mesh (now with two north pole caps and two south pole caps)
export function generateBaseTriangleMesh(): TriangleMesh[] {
  const triangles: TriangleMesh[] = [
    // North hemisphere base triangles (as before)
    {
      id: '1',
      vertices: [
        { lat: 66.0, lng: 0.0 },      // Top point (north)
        { lat: 0.0, lng: -36.0 },     // Bottom left (equator)
        { lat: 0.0, lng: 36.0 }       // Bottom right (equator)
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '2',
      vertices: [
        { lat: 66.0, lng: 0.0 },      // Top point (north)
        { lat: 66.0, lng: 72.0 },     // Top right (north)
        { lat: 0.0, lng: 36.0 }       // Bottom (equator)
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '3',
      vertices: [
        { lat: 66.0, lng: 0.0 },      // Top point (north)
        { lat: 66.0, lng: -72.0 },    // Top left (north)
        { lat: 0.0, lng: -36.0 }      // Bottom (equator)
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    // South hemisphere mirrored base triangles (as before)
    {
      id: '4',
      vertices: [
        { lat: -66.0, lng: 0.0 },      // Bottom point (south)
        { lat: 0.0, lng: -36.0 },      // Top left (equator)
        { lat: 0.0, lng: 36.0 }        // Top right (equator)
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '5',
      vertices: [
        { lat: -66.0, lng: 0.0 },       // Bottom point (south)
        { lat: -66.0, lng: 72.0 },      // Bottom right (south)
        { lat: 0.0, lng: 36.0 }         // Top (equator)
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '6',
      vertices: [
        { lat: -66.0, lng: 0.0 },       // Bottom point (south)
        { lat: -66.0, lng: -72.0 },     // Bottom left (south)
        { lat: 0.0, lng: -36.0 }        // Top (equator)
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    // North pole caps
    {
      id: 'N1',
      vertices: [
        { lat: 90.0, lng: 0.0 },        // North pole
        { lat: 66.0, lng: 72.0 },       // Same as triangle 2's 2nd vertex
        { lat: 66.0, lng: 0.0 }         // "center" top shared with triangles 1-3
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: 'N2',
      vertices: [
        { lat: 90.0, lng: 0.0 },        // North pole
        { lat: 66.0, lng: 0.0 },        // "center" top
        { lat: 66.0, lng: -72.0 }       // Same as triangle 3's 2nd vertex
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    // South pole caps: NEW
    {
      id: 'S1',
      vertices: [
        { lat: -90.0, lng: 0.0 },         // South pole
        { lat: -66.0, lng: 0.0 },         // "center" bottom shared with triangles 4-6
        { lat: -66.0, lng: 72.0 }         // Same as triangle 5's 2nd vertex
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: 'S2',
      vertices: [
        { lat: -90.0, lng: 0.0 },         // South pole
        { lat: -66.0, lng: -72.0 },       // Same as triangle 6's 2nd vertex
        { lat: -66.0, lng: 0.0 }          // "center" bottom
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    }
  ];

  console.log('Generated base triangle mesh with 10 triangles (north/south hemispheres + pole caps)');
  return triangles;
}

// Calculate midpoint between two lat/lng points on sphere surface (Great Circle)
export function sphericalMidpoint(p1: LatLng, p2: LatLng): LatLng {
  const point1 = latLngToPoint3D(p1);
  const point2 = latLngToPoint3D(p2);
  
  const midpoint = {
    x: (point1.x + point2.x) / 2,
    y: (point1.y + point2.y) / 2,
    z: (point1.z + point2.z) / 2
  };
  
  // Normalize to unit sphere
  const length = Math.sqrt(midpoint.x * midpoint.x + midpoint.y * midpoint.y + midpoint.z * midpoint.z);
  midpoint.x /= length;
  midpoint.y /= length;
  midpoint.z /= length;
  
  return point3DToLatLng(midpoint);
}

// Subdivide a triangle into 4 smaller triangles with hierarchical IDs
export function subdivideTriangleMesh(triangle: TriangleMesh): TriangleMesh[] {
  const [v1, v2, v3] = triangle.vertices;
  
  // Calculate midpoints using great circle paths
  const m1 = sphericalMidpoint(v1, v2);
  const m2 = sphericalMidpoint(v2, v3);
  const m3 = sphericalMidpoint(v3, v1);
  
  // Create 4 new triangles with hierarchical naming
  const children: TriangleMesh[] = [
    {
      id: `${triangle.id}.1`,
      vertices: [v1, m1, m3],
      level: triangle.level + 1,
      clickCount: 0,
      subdivided: false
    },
    {
      id: `${triangle.id}.2`,
      vertices: [m1, v2, m2],
      level: triangle.level + 1,
      clickCount: 0,
      subdivided: false
    },
    {
      id: `${triangle.id}.3`,
      vertices: [m3, m2, v3],
      level: triangle.level + 1,
      clickCount: 0,
      subdivided: false
    },
    {
      id: `${triangle.id}.4`,
      vertices: [m1, m2, m3],
      level: triangle.level + 1,
      clickCount: 0,
      subdivided: false
    }
  ];
  
  return children;
}

// Get color based on click count and level
export function getTriangleMeshColor(triangle: TriangleMesh): string {
  if (triangle.level === 19 && triangle.clickCount >= 10) {
    return '#ff0000'; // Red for final level
  }
  
  const grayPercent = Math.min(triangle.clickCount * 10, 100);
  if (grayPercent === 0) {
    return '#ffffff'; // Snow white
  }
  
  const grayValue = Math.floor(255 * (1 - grayPercent / 100));
  return `rgb(${grayValue}, ${grayValue}, ${grayValue})`;
}

// Store triangle click activity in Supabase
export async function storeTriangleActivity(triangleId: string, clickCount: number, level: number) {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    const { error, data } = await supabase
      .from('triangle_activities')
      .insert([
        {
          when: new Date().toISOString(),
          where: triangleId,
          what: clickCount,
          level: level,
        }
      ])
      .select('id'); // get id back
    if (error) {
      throw error;
    }
    // Explicitly type the data returned from supabase
    const typedData = data as TriangleActivityRow[] | null;
    return { success: true, id: typedData?.[0]?.id };
  } catch (error) {
    console.error('Error storing triangle activity in Supabase:', error);
    throw error;
  }
}

// Clear all triangle activities from Supabase
export async function clearTriangleActivities() {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    // Delete all rows by calling delete() without a filter
    const { error } = await supabase
      .from('triangle_activities')
      .delete();
    if (error) {
      throw error;
    }
    console.log('Triangle activities cleared successfully in Supabase');
    return { success: true };
  } catch (error) {
    console.error('Error clearing triangle activities in Supabase:', error);
    throw error;
  }
}

// Get all triangle activities from Supabase
export async function getTriangleActivities() {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    const { data, error } = await supabase
      .from('triangle_activities')
      .select('*');
    if (error) {
      throw error;
    }
    // Defensive: if data is not an array, treat as empty
    if (!Array.isArray(data)) {
      console.warn("Triangle activities GET: Malformed response or 'activities' is not array", data);
      return [];
    }
    // Normalize date strings to the same format
    const activities = (data as TriangleActivityRow[]).map((act) => ({
      ...act,
      when: typeof act.when === 'string' ? act.when : new Date(act.when).toISOString(),
    }));
    console.log('Retrieved triangle activities from Supabase:', activities.length, activities);
    return activities;
  } catch (error) {
    console.error('Error getting triangle activities from Supabase:', error);
    return [];
  }
}

// Rebuild triangle mesh from stored activities
export function rebuildTriangleMeshFromActivities(activities: any[]): TriangleMesh[] {
  const baseMesh = generateBaseTriangleMesh();
  
  // Sort activities by timestamp to replay them in order
  const sortedActivities = activities.sort((a, b) => 
    new Date(a.when).getTime() - new Date(b.when).getTime()
  );
  
  // Apply each activity to rebuild the mesh state
  let currentMesh = baseMesh;
  
  for (const activity of sortedActivities) {
    currentMesh = applyActivityToMesh(currentMesh, activity);
  }
  
  return currentMesh;
}

// Apply a single activity to the mesh
function applyActivityToMesh(mesh: TriangleMesh[], activity: any): TriangleMesh[] {
  return updateTriangleInMesh(mesh, activity.where, activity.what, activity.level);
}

// Update a specific triangle in the mesh
function updateTriangleInMesh(triangles: TriangleMesh[], triangleId: string, clickCount: number, level: number): TriangleMesh[] {
  return triangles.map(triangle => {
    if (triangle.id === triangleId) {
      const updatedTriangle = {
        ...triangle,
        clickCount: clickCount
      };
      
      // Check if we need to subdivide (after 10 clicks, on 11th click)
      if (clickCount === 11 && triangle.level < 19) {
        const children = subdivideTriangleMesh(triangle);
        return {
          ...updatedTriangle,
          subdivided: true,
          children
        };
      }
      
      return updatedTriangle;
    }
    
    if (triangle.children) {
      return {
        ...triangle,
        children: updateTriangleInMesh(triangle.children, triangleId, clickCount, level)
      };
    }
    
    return triangle;
  });
}
