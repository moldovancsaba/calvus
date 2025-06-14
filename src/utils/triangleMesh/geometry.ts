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

// Canonical base triangle order for referencing throughout the system (v2.2, rolled back to 24):
// Order: Spiral downward from North Pole, four bands, then four triangles for the South Pole patch—**total = 24**
// [NorthCap1–4, NorthBelt1–4, Equator1–4, SouthBelt1–4, SouthCap1–4, PatchA–D]
// The system uses array indices 0–23 for all operations.
export function generateBaseTriangleMesh(): TriangleMesh[] {
  const triangles: TriangleMesh[] = [
    // 1–4: North Pole Cap triangles (spiral clockwise)
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

    // 5–8: North mid-latitude/belt triangles
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

    // 9–12: Equator band
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

    // 13–16: Southern belt (mirrored, -66 latitude)
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

    // 17–20: South Pole Cap triangles (spiral, -90 latitude)
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

    // 21–24: South Pole Patch/Filler triangles to seal the geometry
    {
      id: 'SP1',
      vertices: [
        { lat: 0.0,    lng: 108.0 },
        { lat: -66.0,  lng: 144.0 },
        { lat: -66.0,  lng: 72.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SP2',
      vertices: [
        { lat: 0.0,    lng: -108.0 },
        { lat: -66.0,  lng: -72.0 },
        { lat: -66.0,  lng: -144.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SP3',
      vertices: [
        { lat: -66.0,  lng: 144.0 },
        { lat: -66.0,  lng: 72.0 },
        { lat: -90.0,  lng: 0.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SP4',
      vertices: [
        { lat: -66.0,  lng: -144.0 },
        { lat: -66.0,  lng: -72.0 },
        { lat: -90.0,  lng: 0.0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    }
  ];

  // Log the canonical order for audit
  console.log('Base triangle mesh generated in canonical spiral order (v2.2, 24 triangles). Reference by array index 0–23 for all system ops.');
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
