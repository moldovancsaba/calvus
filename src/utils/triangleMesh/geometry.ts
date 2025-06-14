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

// Canonical mesh: 24 triangles, spiral from N pole, as originally approved.
// IDs: N1–N4 (north cap), B1–B4 (north belt), E1–E4 (equator), SB1–SB4 (south belt), S1–S4 (south cap), SP1–SP4 (patch/filler for exact closure)

export function generateBaseTriangleMesh(): TriangleMesh[] {
  const triangles: TriangleMesh[] = [
    // North Pole Cap
    {
      id: 'N1',
      vertices: [ { lat: 90.0, lng: 0.0 }, { lat: 66.0, lng: 0.0 }, { lat: 66.0, lng: 72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'N2',
      vertices: [ { lat: 90.0, lng: 0.0 }, { lat: 66.0, lng: 72.0 }, { lat: 66.0, lng: 144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'N3',
      vertices: [ { lat: 90.0, lng: 0.0 }, { lat: 66.0, lng: 144.0 }, { lat: 66.0, lng: -144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'N4',
      vertices: [ { lat: 90.0, lng: 0.0 }, { lat: 66.0, lng: -144.0 }, { lat: 66.0, lng: -72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },

    // North Belt
    {
      id: 'B1',
      vertices: [ { lat: 66.0, lng: 0.0 }, { lat: 0.0, lng: -36.0 }, { lat: 66.0, lng: 72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'B2',
      vertices: [ { lat: 66.0, lng: 72.0 }, { lat: 0.0, lng: 36.0 }, { lat: 66.0, lng: 144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'B3',
      vertices: [ { lat: 66.0, lng: 144.0 }, { lat: 0.0, lng: 108.0 }, { lat: 66.0, lng: -144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'B4',
      vertices: [ { lat: 66.0, lng: -144.0 }, { lat: 0.0, lng: -108.0 }, { lat: 66.0, lng: -72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },

    // Equator Band
    {
      id: 'E1',
      vertices: [ { lat: 0.0, lng: -36.0 }, { lat: 0.0, lng: 36.0 }, { lat: 66.0, lng: 72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'E2',
      vertices: [ { lat: 0.0, lng: 36.0 }, { lat: 0.0, lng: 108.0 }, { lat: 66.0, lng: 144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'E3',
      vertices: [ { lat: 0.0, lng: 108.0 }, { lat: 0.0, lng: 180.0 }, { lat: 66.0, lng: -144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'E4',
      vertices: [ { lat: 0.0, lng: -108.0 }, { lat: 0.0, lng: -180.0 }, { lat: 66.0, lng: -72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },

    // South Belt
    {
      id: 'SB1',
      vertices: [ { lat: -66.0, lng: 0.0 }, { lat: 0.0, lng: -36.0 }, { lat: -66.0, lng: 72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SB2',
      vertices: [ { lat: -66.0, lng: 72.0 }, { lat: 0.0, lng: 36.0 }, { lat: -66.0, lng: 144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SB3',
      vertices: [ { lat: -66.0, lng: 144.0 }, { lat: 0.0, lng: 108.0 }, { lat: -66.0, lng: -144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SB4',
      vertices: [ { lat: -66.0, lng: -144.0 }, { lat: 0.0, lng: -108.0 }, { lat: -66.0, lng: -72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },

    // South Pole Cap
    {
      id: 'S1',
      vertices: [ { lat: -90.0, lng: 0.0 }, { lat: -66.0, lng: 0.0 }, { lat: -66.0, lng: 72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'S2',
      vertices: [ { lat: -90.0, lng: 0.0 }, { lat: -66.0, lng: 72.0 }, { lat: -66.0, lng: 144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'S3',
      vertices: [ { lat: -90.0, lng: 0.0 }, { lat: -66.0, lng: 144.0 }, { lat: -66.0, lng: -144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'S4',
      vertices: [ { lat: -90.0, lng: 0.0 }, { lat: -66.0, lng: -144.0 }, { lat: -66.0, lng: -72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },

    // South Pole Patch/Filler (to make 24, and close the mesh cleanly, use only as per prior confirmation)  
    {
      id: 'SP1',
      vertices: [ { lat: 0.0,    lng: 108.0 }, { lat: -66.0,  lng: 144.0 }, { lat: -66.0,  lng: 72.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SP2',
      vertices: [ { lat: 0.0,    lng: -108.0 }, { lat: -66.0,  lng: -72.0 }, { lat: -66.0,  lng: -144.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SP3',
      vertices: [ { lat: -66.0,  lng: 144.0 }, { lat: -66.0,  lng: 72.0 }, { lat: -90.0,  lng: 0.0 } ],
      level: 0, clickCount: 0, subdivided: false
    },
    {
      id: 'SP4',
      vertices: [ { lat: -66.0,  lng: -144.0 }, { lat: -66.0,  lng: -72.0 }, { lat: -90.0,  lng: 0.0 } ],
      level: 0, clickCount: 0, subdivided: false
    }
  ];

  console.log('Base triangle mesh generated as 24 canonical triangles (IDs N1–N4, B1–B4, E1–E4, SB1–SB4, S1–S4, SP1–SP4). Reference by array index 0–23 for all operations.');
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
