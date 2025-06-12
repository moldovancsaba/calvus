
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

// Predefined triangle grid with custom geographic coordinates
// Based on your specification: Arctic Circle (66.5°), Equator (0°), Antarctic Circle (-66.5°)
const CUSTOM_TRIANGLES = [
  // Triangle _01
  { id: "triangle-01", vertices: [[66.5, 0.0], [66.5, 36.0], [0.0, 0.0]] },
  // Triangle _02
  { id: "triangle-02", vertices: [[0.0, 72.0], [0.0, 0.0], [66.5, 36.0]] },
  // Triangle _03
  { id: "triangle-03", vertices: [[66.5, 108.0], [66.5, 36.0], [0.0, 72.0]] },
  // Triangle _04
  { id: "triangle-04", vertices: [[0.0, 144.0], [0.0, 72.0], [66.5, 108.0]] },
  // Triangle _05
  { id: "triangle-05", vertices: [[66.5, 180.0], [66.5, 108.0], [0.0, 144.0]] },
  // Triangle _06
  { id: "triangle-06", vertices: [[0.0, -144.0], [0.0, 144.0], [66.5, 180.0]] },
  // Triangle _07
  { id: "triangle-07", vertices: [[66.5, -108.0], [66.5, 180.0], [0.0, -144.0]] },
  // Triangle _08
  { id: "triangle-08", vertices: [[0.0, -72.0], [0.0, -144.0], [66.5, -108.0]] },
  // Triangle _09
  { id: "triangle-09", vertices: [[66.5, -36.0], [66.5, -108.0], [0.0, -72.0]] },
  // Triangle _10
  { id: "triangle-10", vertices: [[0.0, 0.0], [0.0, -72.0], [66.5, -36.0]] },
  // Triangle _11
  { id: "triangle-11", vertices: [[66.5, 0.0], [66.5, -36.0], [0.0, 0.0]] },
  // Triangle _12
  { id: "triangle-12", vertices: [[-66.5, 0.0], [-66.5, 36.0], [0.0, 0.0]] },
  // Triangle _13
  { id: "triangle-13", vertices: [[0.0, 72.0], [0.0, 0.0], [-66.5, 36.0]] },
  // Triangle _14
  { id: "triangle-14", vertices: [[-66.5, 108.0], [-66.5, 36.0], [0.0, 72.0]] },
  // Triangle _15
  { id: "triangle-15", vertices: [[0.0, 144.0], [0.0, 72.0], [-66.5, 108.0]] },
  // Triangle _16
  { id: "triangle-16", vertices: [[-66.5, 180.0], [-66.5, 108.0], [0.0, 144.0]] },
  // Triangle _17
  { id: "triangle-17", vertices: [[0.0, -144.0], [0.0, 144.0], [-66.5, 180.0]] },
  // Triangle _18
  { id: "triangle-18", vertices: [[-66.5, -108.0], [-66.5, 180.0], [0.0, -144.0]] },
  // Triangle _19
  { id: "triangle-19", vertices: [[0.0, -72.0], [0.0, -144.0], [-66.5, -108.0]] },
  // Triangle _20
  { id: "triangle-20", vertices: [[-66.5, -36.0], [-66.5, -108.0], [0.0, -72.0]] },
  // Triangle _21
  { id: "triangle-21", vertices: [[0.0, 0.0], [0.0, -72.0], [-66.5, -36.0]] },
  // Triangle _22
  { id: "triangle-22", vertices: [[-66.5, 0.0], [-66.5, -36.0], [0.0, 0.0]] }
];

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

// Generate the custom triangle grid
export function generateIcosahedronTriangles(): Triangle[] {
  const triangles: Triangle[] = [];
  
  CUSTOM_TRIANGLES.forEach((triangleData) => {
    const triangle: Triangle = {
      id: triangleData.id,
      vertices: triangleData.vertices.map(([lat, lng]) => ({
        lat,
        lng: lng > 180 ? lng - 360 : lng // Normalize longitude to [-180, 180]
      })) as [LatLng, LatLng, LatLng],
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
