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
  color?: string; // ADDED: color of owner, for "paint"
  gametag?: string; // Identify user
}

export function point3DToLatLng(point: Point3D): LatLng {
  const lat = Math.asin(point.z) * (180 / Math.PI);
  const lng = Math.atan2(point.y, point.x) * (180 / Math.PI);
  return { lat, lng };
}

export function latLngToPoint3D(latLng: LatLng): Point3D {
  const latRad = latLng.lat * (Math.PI / 180);
  const lngRad = latLng.lng * (Math.PI / 180);
  return {
    x: Math.cos(latRad) * Math.cos(lngRad),
    y: Math.cos(latRad) * Math.sin(lngRad),
    z: Math.sin(latRad)
  };
}

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

// Generate the 24 base triangles for the spherical mesh.
// These triangles are distributed to minimize distortion and support the subdivision system.
// Canonical for v2.1+: See technical documentation.
// 
// As of June 2025, the base mesh contains the following triangles (IDs):
// [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, N1, N2, S1, S2, B1, B3, N3, NEW1, NEW2, NEW3]
// 
// All per-triangle activity and mesh logic assumes 24 triangles at mesh genesis.
export function generateBaseTriangleMesh(): TriangleMesh[] {
  const triangles: TriangleMesh[] = [
    // North hemisphere base triangles
    {
      id: '1',
      vertices: [
        { lat: 66.0, lng: 0.0 },
        { lat: 0.0, lng: -36.0 },
        { lat: 0.0, lng: 36.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '2',
      vertices: [
        { lat: 66.0, lng: 0.0 },
        { lat: 66.0, lng: 72.0 },
        { lat: 0.0, lng: 36.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '3',
      vertices: [
        { lat: 66.0, lng: 0.0 },
        { lat: 66.0, lng: -72.0 },
        { lat: 0.0, lng: -36.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },

    // South hemisphere mirrored base triangles
    {
      id: '4',
      vertices: [
        { lat: -66.0, lng: 0.0 },
        { lat: 0.0, lng: -36.0 },
        { lat: 0.0, lng: 36.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '5',
      vertices: [
        { lat: -66.0, lng: 0.0 },
        { lat: -66.0, lng: 72.0 },
        { lat: 0.0, lng: 36.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '6',
      vertices: [
        { lat: -66.0, lng: 0.0 },
        { lat: -66.0, lng: -72.0 },
        { lat: 0.0, lng: -36.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },

    // ---- Corrected Belt (Equator) Triangles (NORTH) ----
    // These form a geodesic band similar to the base triangles, not degenerate
    {
      id: '7',
      vertices: [
        { lat: 66.0, lng: -72.0 },
        { lat: 0.0, lng: -36.0 },
        { lat: 0.0, lng: -108.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '8',
      vertices: [
        { lat: 66.0, lng: 72.0 },
        { lat: 0.0, lng: 36.0 },
        { lat: 0.0, lng: 108.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '9',
      vertices: [
        { lat: 66.0, lng: 144.0 },
        { lat: 0.0, lng: 108.0 },
        { lat: 0.0, lng: 180.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '10',
      vertices: [
        { lat: 66.0, lng: -144.0 },
        { lat: 0.0, lng: -108.0 },
        { lat: 0.0, lng: -180.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },

    // ---- South hemisphere mirror belt (equatorial) triangles ----
    // These mirror triangles 7–10 but with -66 latitude
    {
      id: '11',
      vertices: [
        { lat: -66.0, lng: -72.0 },
        { lat: 0.0, lng: -36.0 },
        { lat: 0.0, lng: -108.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '12',
      vertices: [
        { lat: -66.0, lng: 72.0 },
        { lat: 0.0, lng: 36.0 },
        { lat: 0.0, lng: 108.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '13',
      vertices: [
        { lat: -66.0, lng: 144.0 },
        { lat: 0.0, lng: 108.0 },
        { lat: 0.0, lng: 180.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: '14',
      vertices: [
        { lat: -66.0, lng: -144.0 },
        { lat: 0.0, lng: -108.0 },
        { lat: 0.0, lng: -180.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },

    // North pole caps
    {
      id: 'N1',
      vertices: [
        { lat: 90.0, lng: 0.0 },
        { lat: 66.0, lng: 72.0 },
        { lat: 66.0, lng: 0.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: 'N2',
      vertices: [
        { lat: 90.0, lng: 0.0 },
        { lat: 66.0, lng: 0.0 },
        { lat: 66.0, lng: -72.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    // South pole caps
    {
      id: 'S1',
      vertices: [
        { lat: -90.0, lng: 0.0 },
        { lat: -66.0, lng: 0.0 },
        { lat: -66.0, lng: 72.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: 'S2',
      vertices: [
        { lat: -90.0, lng: 0.0 },
        { lat: -66.0, lng: -72.0 },
        { lat: -66.0, lng: 0.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },

    // Triangle A: (66°N, 72°), (66°N, 144°), (0°, 108°)
    {
      id: 'B1',
      vertices: [
        { lat: 66.0, lng: 72.0 },
        { lat: 66.0, lng: 144.0 },
        { lat: 0.0, lng: 108.0 },
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    // Triangle C: (66°N, -144°), (66°N, -72°), (0°, -108°)
    {
      id: 'B3',
      vertices: [
        { lat: 90.0, lng: 0.0 },
        { lat: 66.0, lng: 72.0 },
        { lat: 66.0, lng: 144.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },

    // New North Pole Triangle: (90°N, 0°), (66°N, -144°), (66°N, -72°)
    {
      id: 'N3',
      vertices: [
        { lat: 90.0, lng: 0.0 },
        { lat: 66.0, lng: -144.0 },
        { lat: 66.0, lng: -72.0 },
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },

    // New custom triangle with user-defined coordinates
    {
      id: 'NEW1',
      vertices: [
        { lat: 66.0, lng: -72.0 },
        { lat: 66.0, lng: -144.0 },
        { lat: 0.0, lng: -108.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: 'NEW2',
      vertices: [
        { lat: 0.0, lng: 108.0 },
        { lat: -66.0, lng: 144.0 },
        { lat: -66.0, lng: 72.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
    {
      id: 'NEW3',
      vertices: [
        { lat: -66.0, lng: -144.0 },
        { lat: -66.0, lng: -72.0 },
        { lat: 0.0, lng: -108.0 }
      ],
      level: 0,
      clickCount: 0,
      subdivided: false
    },
  ];

  // Log 24 base triangles (v2.1 as of June 2025)
  console.log('Generated base triangle mesh with 24 triangles (v2.1, June 2025)');
  return triangles;
}

export function subdivideTriangleMesh(triangle: TriangleMesh): TriangleMesh[] {
  const [v1, v2, v3] = triangle.vertices;
  const m1 = sphericalMidpoint(v1, v2);
  const m2 = sphericalMidpoint(v2, v3);
  const m3 = sphericalMidpoint(v3, v1);

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
