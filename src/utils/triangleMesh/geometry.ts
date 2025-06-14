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

// Canonical mesh: 26 triangles, spiral from N pole, as originally approved.
// IDs: N1–N4 (north cap), B1–B4 (north belt), E1–E4 (equator), SB1–SB4 (south belt), S1–S4 (south cap), SP1–SP4 (patch/filler for exact closure)

export function generateBaseTriangleMesh(): TriangleMesh[] {
  const triangles: TriangleMesh[] = [
    // T1
    {
      id: 'T1',
      vertices: [
        { lat: 0, lng: -180 },
        { lat: 66, lng: -144 },
        { lat: 0, lng: -108 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T2
    {
      id: 'T2',
      vertices: [
        { lat: 66, lng: -144 },
        { lat: 0, lng: -108 },
        { lat: 66, lng: -72 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T3
    {
      id: 'T3',
      vertices: [
        { lat: 0, lng: -108 },
        { lat: 66, lng: -72 },
        { lat: 0, lng: -36 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T4
    {
      id: 'T4',
      vertices: [
        { lat: 66, lng: -72 },
        { lat: 0, lng: -36 },
        { lat: 66, lng: 0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T5
    {
      id: 'T5',
      vertices: [
        { lat: 0, lng: -36 },
        { lat: 66, lng: 0 },
        { lat: 0, lng: 36 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T6
    {
      id: 'T6',
      vertices: [
        { lat: 66, lng: 0 },
        { lat: 0, lng: 36 },
        { lat: 66, lng: 72 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T7
    {
      id: 'T7',
      vertices: [
        { lat: 0, lng: 36 },
        { lat: 66, lng: 72 },
        { lat: 0, lng: 108 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T8
    {
      id: 'T8',
      vertices: [
        { lat: 66, lng: 72 },
        { lat: 0, lng: 108 },
        { lat: 66, lng: 144 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T9
    {
      id: 'T9',
      vertices: [
        { lat: 0, lng: 108 },
        { lat: 66, lng: 144 },
        { lat: 0, lng: 180 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T10
    {
      id: 'T10',
      vertices: [
        { lat: 0, lng: -180 },
        { lat: -66, lng: -144 },
        { lat: 0, lng: -108 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T11
    {
      id: 'T11',
      vertices: [
        { lat: -66, lng: -144 },
        { lat: 0, lng: -108 },
        { lat: -66, lng: -72 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T12
    {
      id: 'T12',
      vertices: [
        { lat: 0, lng: -108 },
        { lat: -66, lng: -72 },
        { lat: 0, lng: -36 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T13
    {
      id: 'T13',
      vertices: [
        { lat: -66, lng: -72 },
        { lat: 0, lng: -36 },
        { lat: -66, lng: 0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T14
    {
      id: 'T14',
      vertices: [
        { lat: 0, lng: -36 },
        { lat: -66, lng: 0 },
        { lat: 0, lng: 36 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T15
    {
      id: 'T15',
      vertices: [
        { lat: -66, lng: 0 },
        { lat: 0, lng: 36 },
        { lat: -66, lng: 72 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T16
    {
      id: 'T16',
      vertices: [
        { lat: 0, lng: 36 },
        { lat: -66, lng: 72 },
        { lat: 0, lng: 108 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T17
    {
      id: 'T17',
      vertices: [
        { lat: -66, lng: 72 },
        { lat: 0, lng: 108 },
        { lat: -66, lng: 144 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T18
    {
      id: 'T18',
      vertices: [
        { lat: 0, lng: 108 },
        { lat: -66, lng: 144 },
        { lat: 0, lng: 180 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T19
    {
      id: 'T19',
      vertices: [
        { lat: 66, lng: -144 },
        { lat: 90, lng: 0 },
        { lat: 66, lng: -72 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T20
    {
      id: 'T20',
      vertices: [
        { lat: 66, lng: -72 },
        { lat: 90, lng: 0 },
        { lat: 66, lng: 0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T21
    {
      id: 'T21',
      vertices: [
        { lat: 66, lng: 0 },
        { lat: 90, lng: 0 },
        { lat: 66, lng: 72 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T22
    {
      id: 'T22',
      vertices: [
        { lat: 66, lng: 72 },
        { lat: 90, lng: 0 },
        { lat: 66, lng: 144 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T23
    {
      id: 'T23',
      vertices: [
        { lat: -66, lng: -144 },
        { lat: -90, lng: 0 },
        { lat: -66, lng: -72 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T24
    {
      id: 'T24',
      vertices: [
        { lat: -66, lng: -72 },
        { lat: -90, lng: 0 },
        { lat: -66, lng: 0 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T25
    {
      id: 'T25',
      vertices: [
        { lat: -66, lng: 0 },
        { lat: -90, lng: 0 },
        { lat: -66, lng: 72 }
      ],
      level: 0, clickCount: 0, subdivided: false
    },
    // T26
    {
      id: 'T26',
      vertices: [
        { lat: -66, lng: 72 },
        { lat: -90, lng: 0 },
        { lat: -66, lng: 144 }
      ],
      level: 0, clickCount: 0, subdivided: false
    }
  ];

  console.log('Base triangle mesh generated as 26 triangles (T1–T26).');
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
