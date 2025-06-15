
import React, { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Your demo mesh triangles: array of {id: string, vertices: [{lat, lng}, ...]}
const DEMO_MESH = [
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

// Geodesic path util copied from your project
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

const DemoMeshMap: React.FC = () => {
  const mapDiv = useRef<HTMLDivElement>(null);
  const mapRef = useRef<L.Map | null>(null);
  const polygonLayers = useRef<L.Polygon[]>([]);

  useEffect(() => {
    if (!mapDiv.current) return;
    // Create map (do once)
    if (!mapRef.current) {
      mapRef.current = L.map(mapDiv.current, {
        center: [0, 0],
        zoom: 2,
        minZoom: 1,
        maxZoom: 4,
        zoomControl: true,              // SHOW zoom in/out controls!
        worldCopyJump: true,
        attributionControl: false,
        dragging: true,                 // Enable drag/move
        doubleClickZoom: true,         // Enable double click zoom
        boxZoom: true,                 // Enable box zoom
        scrollWheelZoom: true,         // Enable scroll wheel zoom
        keyboard: true,                // Enable keyboard navigation
        touchZoom: true,               // Enable pinch zoom
        maxBounds: [[-90, -180], [90, 180]],
      });

      // Set bg color black faintly for demo page
      mapRef.current.getContainer().style.backgroundColor = "#000";
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

    // Remove old polygons
    polygonLayers.current.forEach(layer => {
      map.removeLayer(layer);
    });
    polygonLayers.current = [];

    // Draw triangles
    DEMO_MESH.forEach(tri => {
      const coords = geodesicTriangleCoords(tri.vertices);
      const polygon = L.polygon(coords, {
        color: "#fff",            // 2px white border
        weight: 2,
        opacity: 1,
        fillColor: "#000",        // black fill
        fillOpacity: 0.5,
        interactive: false,       // No mouse interactions on mesh
        smoothFactor: 1.0
      });
      polygon.addTo(map);
      polygonLayers.current.push(polygon);
    });

    // Fit world on mount
    map.fitBounds([[-90, -180], [90, 180]], { padding: [0, 0], animate: false, maxZoom: 2 });

    // Do NOT disable map movement/zoom! (because user requested controls)

    return () => {
      map.remove();
      mapRef.current = null;
      polygonLayers.current = [];
    };
  }, []);

  return (
    <div className="w-screen h-screen">
      <div ref={mapDiv} className="w-full h-full" style={{ minHeight: "100vh", minWidth: "100vw" }} />
    </div>
  );
};

export default DemoMeshMap;

