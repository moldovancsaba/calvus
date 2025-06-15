
import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

/**
 * StandaloneMeshMap: Pragmatic, always-working fallback.
 * Props: worldSlug, settings (future extension)
 */

const BASE_MESH = [
  { id: "T1",  vertices: [{lat: 0, lng:-180}, {lat:66, lng:-144}, {lat:0, lng:-108}] },
  { id: "T2",  vertices: [{lat:66, lng:-144}, {lat:0, lng:-108}, {lat:66, lng:-72}] },
  { id: "T3",  vertices: [{lat:0, lng:-108}, {lat:66, lng:-72}, {lat:0, lng:-36}] },
  { id: "T4",  vertices: [{lat:66, lng:-72}, {lat:0, lng:-36}, {lat:66, lng:0}] },
  { id: "T5",  vertices: [{lat:0, lng:-36}, {lat:66, lng:0}, {lat:0, lng:36}] },
  { id: "T6",  vertices: [{lat:66, lng:0}, {lat:0, lng:36}, {lat:66, lng:72}] },
  { id: "T7",  vertices: [{lat:0, lng:36}, {lat:66, lng:72}, {lat:0, lng:108}] },
  { id: "T8",  vertices: [{lat:66, lng:72}, {lat:0, lng:108}, {lat:66, lng:144}] },
  { id: "T9",  vertices: [{lat:0, lng:108}, {lat:66, lng:144}, {lat:0, lng:180}] },
  { id: "T10", vertices: [{lat:0, lng:-180}, {lat:-66, lng:-144}, {lat:0, lng:-108}] },
  { id: "T11", vertices: [{lat:-66, lng:-144}, {lat:0, lng:-108}, {lat:-66, lng:-72}] },
  { id: "T12", vertices: [{lat:0, lng:-108}, {lat:-66, lng:-72}, {lat:0, lng:-36}] },
  { id: "T13", vertices: [{lat:-66, lng:-72}, {lat:0, lng:-36}, {lat:-66, lng:0}] },
  { id: "T14", vertices: [{lat:0, lng:-36}, {lat:-66, lng:0}, {lat:0, lng:36}] },
  { id: "T15", vertices: [{lat:-66, lng:0}, {lat:0, lng:36}, {lat:-66, lng:72}] },
  { id: "T16", vertices: [{lat:0, lng:36}, {lat:-66, lng:72}, {lat:0, lng:108}] },
  { id: "T17", vertices: [{lat:-66, lng:72}, {lat:0, lng:108}, {lat:-66, lng:144}] },
  { id: "T18", vertices: [{lat:0, lng:108}, {lat:-66, lng:144}, {lat:0, lng:180}] },
  { id: "T19", vertices: [{lat:66, lng:-144}, {lat:90, lng:0}, {lat:66, lng:-72}] },
  { id: "T20", vertices: [{lat:66, lng:-72}, {lat:90, lng:0}, {lat:66, lng:0}] },
  { id: "T21", vertices: [{lat:66, lng:0}, {lat:90, lng:0}, {lat:66, lng:72}] },
  { id: "T22", vertices: [{lat:66, lng:72}, {lat:90, lng:0}, {lat:66, lng:144}] },
  { id: "T23", vertices: [{lat:-66, lng:-144}, {lat:-90, lng:0}, {lat:-66, lng:-72}] },
  { id: "T24", vertices: [{lat:-66, lng:-72}, {lat:-90, lng:0}, {lat:-66, lng:0}] },
  { id: "T25", vertices: [{lat:-66, lng:0}, {lat:-90, lng:0}, {lat:-66, lng:72}] },
  { id: "T26", vertices: [{lat:-66, lng:72}, {lat:-90, lng:0}, {lat:-66, lng:144}] },
];

// Helper: mid-point on sphere (great-circle, normalized)
function sphericalMidpoint(a: {lat:number, lng:number}, b: {lat:number, lng:number}) {
  const toRad = (deg: number) => deg * Math.PI / 180;
  const toDeg = (rad: number) => rad * 180 / Math.PI;
  const lat1 = toRad(a.lat), lng1 = toRad(a.lng);
  const lat2 = toRad(b.lat), lng2 = toRad(b.lng);
  const x1 = Math.cos(lat1) * Math.cos(lng1),
    y1 = Math.cos(lat1) * Math.sin(lng1),
    z1 = Math.sin(lat1);
  const x2 = Math.cos(lat2) * Math.cos(lng2),
    y2 = Math.cos(lat2) * Math.sin(lng2),
    z2 = Math.sin(lat2);
  // Average and normalize
  let x = x1 + x2,
    y = y1 + y2,
    z = z1 + z2;
  const len = Math.sqrt(x * x + y * y + z * z);
  x /= len; y /= len; z /= len;
  // to lat/lng
  const lat = Math.asin(z);
  const lng = Math.atan2(y, x);
  return { lat: toDeg(lat), lng: toDeg(lng) };
}

// Generates array of [lat,lng] along sphere (used for curved triangle edges)
function geodesicTriangleCoords(vertices: {lat:number, lng:number}[]) {
  if (!vertices || vertices.length !== 3) return [];
  const greatCirclePath = (start: any, end: any, steps = 50) => {
    const points = [];
    const lat1 = start.lat * Math.PI / 180, lng1 = start.lng * Math.PI / 180;
    const lat2 = end.lat * Math.PI / 180, lng2 = end.lng * Math.PI / 180;
    const deltaLng = lng2 - lng1;
    const a = Math.sin((lat2-lat1)/2) ** 2 +
              Math.cos(lat1) * Math.cos(lat2) * Math.sin(deltaLng/2) ** 2;
    const distance = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    for (let i = 0; i <= steps; i++) {
      const f = i / steps;
      if (distance < 1e-6 || Math.abs(distance - Math.PI) < 1e-6) {
        const lat = start.lat + (end.lat - start.lat) * f;
        const lng = start.lng + (end.lng - start.lng) * f;
        points.push([lat, lng]);
        continue;
      }
      const x1 = Math.cos(lat1) * Math.cos(lng1),
        y1 = Math.cos(lat1) * Math.sin(lng1),
        z1 = Math.sin(lat1),
        x2 = Math.cos(lat2) * Math.cos(lng2),
        y2 = Math.cos(lat2) * Math.sin(lng2),
        z2 = Math.sin(lat2);
      const A = Math.sin((1-f)*distance) / Math.sin(distance);
      const B = Math.sin(f*distance) / Math.sin(distance);
      const x = A * x1 + B * x2,
        y = A * y1 + B * y2,
        z = A * z1 + B * z2;
      const lat = Math.atan2(z, Math.sqrt(x*x + y*y)) * 180/Math.PI;
      const lng = Math.atan2(y, x) * 180/Math.PI;
      points.push([lat, lng]);
    }
    return points;
  };
  const edge1 = greatCirclePath(vertices[0], vertices[1]);
  const edge2 = greatCirclePath(vertices[1], vertices[2]);
  const edge3 = greatCirclePath(vertices[2], vertices[0]);
  return [...edge1, ...edge2.slice(1), ...edge3.slice(1, -1)];
}

// Core subdivision (returns 4 triangles for 1 parent triangle)
function subdivideTriangle(triangle: { id: string, vertices: {lat:number, lng:number}[] }, idPrefix: string) {
  const [v1, v2, v3] = triangle.vertices;
  const m1 = sphericalMidpoint(v1, v2);
  const m2 = sphericalMidpoint(v2, v3);
  const m3 = sphericalMidpoint(v3, v1);
  // Unique child IDs (for re-rendering, not persisted)
  return [
    { id: `${idPrefix}.1`, vertices: [v1, m1, m3] },
    { id: `${idPrefix}.2`, vertices: [m1, v2, m2] },
    { id: `${idPrefix}.3`, vertices: [m3, m2, v3] },
    { id: `${idPrefix}.4`, vertices: [m1, m2, m3] }
  ];
}

interface MeshTriangle {
  id: string;
  vertices: {lat: number, lng: number}[];
  children?: MeshTriangle[];
}

// Helper: recursively updates triangle in mesh by ID and subdivides it
function divideTriangleById(triangles: MeshTriangle[], id: string): MeshTriangle[] {
  // Recursively search for the triangle matching given ID and subdivide
  return triangles.map(tri => {
    if (tri.id === id) {
      // Only subdivide if not already subdivided
      if (!tri.children) {
        const children = subdivideTriangle(tri, tri.id);
        return { ...tri, children };
      }
      return tri; // already subdivided, ignore further click
    } else if (tri.children) {
      return { ...tri, children: divideTriangleById(tri.children, id) };
    } else {
      return tri;
    }
  });
}

// Recursive rendering of triangles (leaves only—non subdivided ones can be clicked & subdivided)
function renderTriangles(
  map: L.Map,
  mesh: MeshTriangle[],
  polygonLayers: React.MutableRefObject<L.Polygon[]>,
  onTriangleClick: (id: string) => void
) {
  // Remove old polygons for redraw
  polygonLayers.current.forEach(layer => {
    map.removeLayer(layer);
  });
  polygonLayers.current = [];
  // Recursively draw mesh
  function draw(tris: MeshTriangle[]) {
    tris.forEach(tri => {
      if (tri.children) {
        draw(tri.children);
        return;
      }
      const coords = geodesicTriangleCoords(tri.vertices);
      const polygon = L.polygon(coords, {
        color: "#fff",
        weight: 2,
        opacity: 1,
        fillColor: "#000",
        fillOpacity: 0.5,
        interactive: true,
        smoothFactor: 1.0
      });
      polygon.on("click", () => onTriangleClick(tri.id));
      polygon.on("touchstart", () => onTriangleClick(tri.id));
      polygon.addTo(map);
      polygonLayers.current.push(polygon);
    });
  }
  draw(mesh);
}

type Props = {
  worldSlug: string;
  settings?: any;
};

// Always use fullscreen, same as jusforfun page
const StandaloneMeshMap: React.FC<Props> = ({ worldSlug }) => {
  const mapDiv = useRef<HTMLDivElement>(null);
  const mapRef = useRef<L.Map | null>(null);
  const polygonLayers = useRef<L.Polygon[]>([]);

  // Store the mesh triangles in state for runtime-only subdivisions
  const [mesh, setMesh] = useState<MeshTriangle[]>(() =>
    BASE_MESH.map(t => ({ id: t.id, vertices: t.vertices }))
  );

  // Invalidate and redraw mesh when triangles change
  useEffect(() => {
    if (!mapRef.current) return;
    const map = mapRef.current;
    renderTriangles(map, mesh, polygonLayers, (id: string) => {
      setMesh(prev => divideTriangleById(prev, id));
    });
    // eslint-disable-next-line
  }, [mesh]);

  useEffect(() => {
    if (!mapDiv.current) return;
    // Create map (once)
    if (!mapRef.current) {
      mapRef.current = L.map(mapDiv.current, {
        center: [0, 0],
        zoom: 2,
        minZoom: 1,
        maxZoom: 4,
        zoomControl: true,
        worldCopyJump: true,
        attributionControl: false,
        dragging: true,
        doubleClickZoom: true,
        boxZoom: true,
        scrollWheelZoom: true,
        keyboard: true,
        touchZoom: true,
        maxBounds: [[-90, -180], [90, 180]],
      });

      // Set bg color black faintly for demo page
      mapRef.current.getContainer().style.backgroundColor = "#232323";
      // Hide UI controls
      const el = mapRef.current.getContainer();
      if (el) el.style.borderRadius = "0";

      // Add OpenStreetMap tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        opacity: 0.9
      }).addTo(mapRef.current);
    }

    const map = mapRef.current;

    // Draw the mesh initially
    renderTriangles(map, mesh, polygonLayers, (id: string) => {
      setMesh(prev => divideTriangleById(prev, id));
    });

    // Fit world on mount
    map.fitBounds([[-90, -180], [90, 180]], { padding: [0, 0], animate: false, maxZoom: 2 });

    return () => {
      map.remove();
      mapRef.current = null;
      polygonLayers.current = [];
    };
    // eslint-disable-next-line
  }, []);

  return (
    <div className="absolute inset-0 w-full h-full">
      <div ref={mapDiv} className="w-full h-full" style={{ minHeight: "100vh", minWidth: "100vw" }} />
    </div>
  );
};

export default StandaloneMeshMap;
