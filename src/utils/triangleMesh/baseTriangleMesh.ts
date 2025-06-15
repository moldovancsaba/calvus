
import type { TriangleMesh } from "./geometry";

// The canonical base triangle mesh: 26 triangles in spiral order, T1–T26.
export const BASE_TRIANGLE_MESH: TriangleMesh[] = [
  {
    id: 'T1',
    vertices: [
      { lat: 0, lng: -180 },
      { lat: 66, lng: -144 },
      { lat: 0, lng: -108 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T2',
    vertices: [
      { lat: 66, lng: -144 },
      { lat: 0, lng: -108 },
      { lat: 66, lng: -72 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T3',
    vertices: [
      { lat: 0, lng: -108 },
      { lat: 66, lng: -72 },
      { lat: 0, lng: -36 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T4',
    vertices: [
      { lat: 66, lng: -72 },
      { lat: 0, lng: -36 },
      { lat: 66, lng: 0 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T5',
    vertices: [
      { lat: 0, lng: -36 },
      { lat: 66, lng: 0 },
      { lat: 0, lng: 36 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T6',
    vertices: [
      { lat: 66, lng: 0 },
      { lat: 0, lng: 36 },
      { lat: 66, lng: 72 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T7',
    vertices: [
      { lat: 0, lng: 36 },
      { lat: 66, lng: 72 },
      { lat: 0, lng: 108 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T8',
    vertices: [
      { lat: 66, lng: 72 },
      { lat: 0, lng: 108 },
      { lat: 66, lng: 144 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T9',
    vertices: [
      { lat: 0, lng: 108 },
      { lat: 66, lng: 144 },
      { lat: 0, lng: 180 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T10',
    vertices: [
      { lat: 0, lng: -180 },
      { lat: -66, lng: -144 },
      { lat: 0, lng: -108 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T11',
    vertices: [
      { lat: -66, lng: -144 },
      { lat: 0, lng: -108 },
      { lat: -66, lng: -72 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T12',
    vertices: [
      { lat: 0, lng: -108 },
      { lat: -66, lng: -72 },
      { lat: 0, lng: -36 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T13',
    vertices: [
      { lat: -66, lng: -72 },
      { lat: 0, lng: -36 },
      { lat: -66, lng: 0 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T14',
    vertices: [
      { lat: 0, lng: -36 },
      { lat: -66, lng: 0 },
      { lat: 0, lng: 36 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T15',
    vertices: [
      { lat: -66, lng: 0 },
      { lat: 0, lng: 36 },
      { lat: -66, lng: 72 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T16',
    vertices: [
      { lat: 0, lng: 36 },
      { lat: -66, lng: 72 },
      { lat: 0, lng: 108 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T17',
    vertices: [
      { lat: -66, lng: 72 },
      { lat: 0, lng: 108 },
      { lat: -66, lng: 144 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T18',
    vertices: [
      { lat: 0, lng: 108 },
      { lat: -66, lng: 144 },
      { lat: 0, lng: 180 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T19',
    vertices: [
      { lat: 66, lng: -144 },
      { lat: 90, lng: 0 },
      { lat: 66, lng: -72 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T20',
    vertices: [
      { lat: 66, lng: -72 },
      { lat: 90, lng: 0 },
      { lat: 66, lng: 0 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T21',
    vertices: [
      { lat: 66, lng: 0 },
      { lat: 90, lng: 0 },
      { lat: 66, lng: 72 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T22',
    vertices: [
      { lat: 66, lng: 72 },
      { lat: 90, lng: 0 },
      { lat: 66, lng: 144 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T23',
    vertices: [
      { lat: -66, lng: -144 },
      { lat: -90, lng: 0 },
      { lat: -66, lng: -72 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T24',
    vertices: [
      { lat: -66, lng: -72 },
      { lat: -90, lng: 0 },
      { lat: -66, lng: 0 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
  {
    id: 'T25',
    vertices: [
      { lat: -66, lng: 0 },
      { lat: -90, lng: 0 },
      { lat: -66, lng: 72 }
    ],
    level: 0, clickCount: 0, subdivided: false
  },
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
