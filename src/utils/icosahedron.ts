
export interface Point3D {
  x: number;
  y: number;
  z: number;
}

export interface LatLng {
  lat: number;
  lng: number;
}

export interface Triangle {
  id: string;
  vertices: [LatLng, LatLng, LatLng];
  level: number;
  clickCount: number;
  subdivided: boolean;
  children?: Triangle[];
}

// Golden ratio constant for icosahedron calculations
const PHI = (1 + Math.sqrt(5)) / 2;

// Generate the 12 vertices of a regular icosahedron
export function generateIcosahedronVertices(): Point3D[] {
  const vertices: Point3D[] = [];
  
  // Normalize factor to ensure unit sphere
  const norm = Math.sqrt(1 + PHI * PHI);
  
  // Generate vertices in 3 perpendicular rectangles
  const coords = [
    [1, PHI, 0],
    [-1, PHI, 0],
    [1, -PHI, 0],
    [-1, -PHI, 0],
    [0, 1, PHI],
    [0, -1, PHI],
    [0, 1, -PHI],
    [0, -1, -PHI],
    [PHI, 0, 1],
    [-PHI, 0, 1],
    [PHI, 0, -1],
    [-PHI, 0, -1]
  ];

  coords.forEach(([x, y, z]) => {
    vertices.push({
      x: x / norm,
      y: y / norm,
      z: z / norm
    });
  });

  return vertices;
}

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

// Generate the 20 triangular faces of an icosahedron
export function generateIcosahedronTriangles(): Triangle[] {
  const vertices = generateIcosahedronVertices();
  const triangles: Triangle[] = [];
  
  // Define the 20 triangular faces by vertex indices
  const faces = [
    [0, 4, 8], [0, 8, 10], [0, 10, 6], [0, 6, 1], [0, 1, 4],
    [2, 5, 9], [2, 9, 11], [2, 11, 7], [2, 7, 3], [2, 3, 5],
    [1, 6, 11], [1, 11, 9], [1, 9, 4], [4, 9, 5], [4, 5, 8],
    [8, 5, 3], [8, 3, 10], [10, 3, 7], [10, 7, 6], [6, 7, 11]
  ];

  faces.forEach((face, index) => {
    const [v1, v2, v3] = face.map(i => vertices[i]);
    const triangle: Triangle = {
      id: `triangle-${index}`,
      vertices: [
        point3DToLatLng(v1),
        point3DToLatLng(v2),
        point3DToLatLng(v3)
      ] as [LatLng, LatLng, LatLng],
      level: 0,
      clickCount: 0,
      subdivided: false
    };
    triangles.push(triangle);
  });

  return triangles;
}

// Calculate midpoint between two lat/lng points on sphere surface
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

// Subdivide a triangle into 4 smaller triangles
export function subdivideTriangle(triangle: Triangle): Triangle[] {
  const [v1, v2, v3] = triangle.vertices;
  
  // Calculate midpoints
  const m1 = sphericalMidpoint(v1, v2);
  const m2 = sphericalMidpoint(v2, v3);
  const m3 = sphericalMidpoint(v3, v1);
  
  // Create 4 new triangles
  const children: Triangle[] = [
    {
      id: `${triangle.id}-0`,
      vertices: [v1, m1, m3],
      level: triangle.level + 1,
      clickCount: 0,
      subdivided: false
    },
    {
      id: `${triangle.id}-1`,
      vertices: [m1, v2, m2],
      level: triangle.level + 1,
      clickCount: 0,
      subdivided: false
    },
    {
      id: `${triangle.id}-2`,
      vertices: [m3, m2, v3],
      level: triangle.level + 1,
      clickCount: 0,
      subdivided: false
    },
    {
      id: `${triangle.id}-3`,
      vertices: [m1, m2, m3],
      level: triangle.level + 1,
      clickCount: 0,
      subdivided: false
    }
  ];
  
  return children;
}

// Get color based on click count and level
export function getTriangleColor(triangle: Triangle): string {
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
