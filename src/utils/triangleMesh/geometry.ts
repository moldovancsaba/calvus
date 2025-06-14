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

// Canonical base triangle order for referencing throughout the system (v2.2+, June 2025):
// [NorthCap1, NorthCap2, NorthCap3, NorthCap4, NorthBelt1, NorthBelt2, NorthBelt3, NorthBelt4,
//  Equator1, Equator2, Equator3, Equator4, SouthBelt1, SouthBelt2, SouthBelt3, SouthBelt4,
//  SouthCap1, SouthCap2, SouthCap3, SouthCap4, Extra1, Extra2, Extra3, Extra4, SouthPole1, SouthPole2]
// The order is: starting at north pole, spiral downward and around the globe, then extras/patches at the end for south pole.
export function generateBaseTriangleMesh(): TriangleMesh[] {
  const triangles: TriangleMesh[] = [
    // North Pole Cap triangles (top, spiral clockwise)
    {
      id: 'N1',
      vertices: [
        { lat: 90.0, lng: 0.0 },
        { lat: 66.0, lng: 0.0 },
        { lat: 66.0, lng: 72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'N2',
      vertices: [
        { lat: 90.0, lng: 0.0 },
        { lat: 66.0, lng: 72.0 },
        { lat: 66.0, lng: 144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'N3',
      vertices: [
        { lat: 90.0, lng: 0.0 },
        { lat: 66.0, lng: 144.0 },
        { lat: 66.0, lng: -144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'N4',
      vertices: [
        { lat: 90.0, lng: 0.0 },
        { lat: 66.0, lng: -144.0 },
        { lat: 66.0, lng: -72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },

    // Northern mid-latitude/belt triangles (66N)
    {
      id: 'B1',
      vertices: [
        { lat: 66.0, lng: 0.0 },
        { lat: 0.0, lng: -36.0 },
        { lat: 66.0, lng: 72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'B2',
      vertices: [
        { lat: 66.0, lng: 72.0 },
        { lat: 0.0, lng: 36.0 },
        { lat: 66.0, lng: 144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'B3',
      vertices: [
        { lat: 66.0, lng: 144.0 },
        { lat: 0.0, lng: 108.0 },
        { lat: 66.0, lng: -144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'B4',
      vertices: [
        { lat: 66.0, lng: -144.0 },
        { lat: 0.0, lng: -108.0 },
        { lat: 66.0, lng: -72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },

    // Equator band (0° lat around globe, spiral east)
    {
      id: 'E1',
      vertices: [
        { lat: 0.0, lng: -36.0 },
        { lat: 0.0, lng: 36.0 },
        { lat: 66.0, lng: 72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'E2',
      vertices: [
        { lat: 0.0, lng: 36.0 },
        { lat: 0.0, lng: 108.0 },
        { lat: 66.0, lng: 144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'E3',
      vertices: [
        { lat: 0.0, lng: 108.0 },
        { lat: 0.0, lng: 180.0 },
        { lat: 66.0, lng: -144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'E4',
      vertices: [
        { lat: 0.0, lng: -108.0 },
        { lat: 0.0, lng: -180.0 },
        { lat: 66.0, lng: -72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },

    // Southern belt (mirror north, -66 latitude)
    {
      id: 'SB1',
      vertices: [
        { lat: -66.0, lng: 0.0 },
        { lat: 0.0, lng: -36.0 },
        { lat: -66.0, lng: 72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SB2',
      vertices: [
        { lat: -66.0, lng: 72.0 },
        { lat: 0.0, lng: 36.0 },
        { lat: -66.0, lng: 144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SB3',
      vertices: [
        { lat: -66.0, lng: 144.0 },
        { lat: 0.0, lng: 108.0 },
        { lat: -66.0, lng: -144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SB4',
      vertices: [
        { lat: -66.0, lng: -144.0 },
        { lat: 0.0, lng: -108.0 },
        { lat: -66.0, lng: -72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },

    // South Pole Cap triangles
    {
      id: 'S1',
      vertices: [
        { lat: -90.0, lng: 0.0 },
        { lat: -66.0, lng: 0.0 },
        { lat: -66.0, lng: 72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'S2',
      vertices: [
        { lat: -90.0, lng: 0.0 },
        { lat: -66.0, lng: 72.0 },
        { lat: -66.0, lng: 144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'S3',
      vertices: [
        { lat: -90.0, lng: 0.0 },
        { lat: -66.0, lng: 144.0 },
        { lat: -66.0, lng: -144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'S4',
      vertices: [
        { lat: -90.0, lng: 0.0 },
        { lat: -66.0, lng: -144.0 },
        { lat: -66.0, lng: -72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },

    // South Pole Patch triangles (extras/fill-ins for geometry closure/consistency)
    {
      id: 'X1',
      vertices: [
        { lat: 0.0,    lng: 108.0 },
        { lat: -66.0,  lng: 144.0 },
        { lat: -66.0,  lng: 72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'X2',
      vertices: [
        { lat: 0.0,    lng: -108.0 },
        { lat: -66.0,  lng: -72.0 },
        { lat: -66.0,  lng: -144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'X3',
      vertices: [
        { lat: -66.0,  lng: 144.0 },
        { lat: -66.0,  lng: 72.0 },
        { lat: -90.0,  lng: 0.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'X4',
      vertices: [
        { lat: -66.0,  lng: -144.0 },
        { lat: -66.0,  lng: -72.0 },
        { lat: -90.0,  lng: 0.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    }
  ];

  // Log new canonical order for audit trail
  console.log('Base triangle mesh generated in canonical spiral order (v2.2+). Reference by array index for all system operations.');
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
