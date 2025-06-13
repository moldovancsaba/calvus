
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

// Spherical triangle grid with 5 latitudinal bands and 5 longitude segments
// Latitude bands: Arctic Circle (66.5°), Tropic of Cancer (23.5°), Equator (0°), Tropic of Capricorn (-23.5°), Antarctic Circle (-66.5°)
// Longitude points: -180°, -108°, -36°, 36°, 108°, 180° (but we use -144°, -72°, 0°, 72°, 144° for 5 segments)
const LATITUDE_BANDS = [66.5, 23.5, 0, -23.5, -66.5];
const LONGITUDE_POINTS = [-144, -72, 0, 72, 144]; // 5 segments of 72° each

function generateTriangleGrid(): any[] {
  const triangles: any[] = [];
  let triangleId = 1;

  // Generate triangles between adjacent latitude bands
  for (let latBand = 0; latBand < LATITUDE_BANDS.length - 1; latBand++) {
    const upperLat = LATITUDE_BANDS[latBand];
    const lowerLat = LATITUDE_BANDS[latBand + 1];

    for (let lonSegment = 0; lonSegment < LONGITUDE_POINTS.length; lonSegment++) {
      const lng1 = LONGITUDE_POINTS[lonSegment];
      const lng2 = LONGITUDE_POINTS[(lonSegment + 1) % LONGITUDE_POINTS.length];

      // Create two triangles for each rectangular segment
      // Triangle 1: Upper-left, Lower-left, Upper-right
      triangles.push({
        id: `triangle-${triangleId.toString().padStart(2, '0')}`,
        vertices: [
          [upperLat, lng1], // Upper-left
          [lowerLat, lng1], // Lower-left
          [upperLat, lng2]  // Upper-right
        ]
      });
      triangleId++;

      // Triangle 2: Lower-left, Lower-right, Upper-right
      triangles.push({
        id: `triangle-${triangleId.toString().padStart(2, '0')}`,
        vertices: [
          [lowerLat, lng1], // Lower-left
          [lowerLat, lng2], // Lower-right
          [upperLat, lng2]  // Upper-right
        ]
      });
      triangleId++;
    }
  }

  return triangles;
}

const CUSTOM_TRIANGLES = generateTriangleGrid();

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

// Generate the spherical triangle grid
export function generateIcosahedronTriangles(): Triangle[] {
  const triangles: Triangle[] = [];
  
  CUSTOM_TRIANGLES.forEach((triangleData) => {
    const triangle: Triangle = {
      id: triangleData.id,
      vertices: triangleData.vertices.map(([lat, lng]) => ({
        lat,
        lng: lng > 180 ? lng - 360 : lng < -180 ? lng + 360 : lng // Normalize longitude to [-180, 180]
      })) as [LatLng, LatLng, LatLng],
      level: 0,
      clickCount: 0,
      subdivided: false
    };
    triangles.push(triangle);
  });

  console.log(`Generated ${triangles.length} triangles in spherical grid`);
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

// Subdivide a triangle into 4 smaller triangles
export function subdivideTriangle(triangle: Triangle): Triangle[] {
  const [v1, v2, v3] = triangle.vertices;
  
  // Calculate midpoints using great circle paths
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
