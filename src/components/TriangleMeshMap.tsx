
import React, { useRef, useState, useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { generateBaseTriangleMesh, TriangleMesh } from '../utils/triangleMesh';
import { useIsMobile } from "../hooks/use-mobile";
import { TriangleMeshRenderer } from "./mesh/TriangleMeshRenderer";
import { LeafletMapContainer } from "./map/LeafletMapContainer";

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

// Core subdivision logic: returns 4 triangles from a parent
function subdivideTriangle(triangle: TriangleMesh, idPrefix: string): TriangleMesh[] {
  const [v1, v2, v3] = triangle.vertices;
  const m1 = sphericalMidpoint(v1, v2);
  const m2 = sphericalMidpoint(v2, v3);
  const m3 = sphericalMidpoint(v3, v1);
  return [
    { ...triangle, id: `${idPrefix}.1`, vertices: [v1, m1, m3], children: undefined, subdivided: false },
    { ...triangle, id: `${idPrefix}.2`, vertices: [m1, v2, m2], children: undefined, subdivided: false },
    { ...triangle, id: `${idPrefix}.3`, vertices: [m3, m2, v3], children: undefined, subdivided: false },
    { ...triangle, id: `${idPrefix}.4`, vertices: [m1, m2, m3], children: undefined, subdivided: false },
  ];
}

function divideTriangleById(triangles: TriangleMesh[], id: string): TriangleMesh[] {
  // Recursively search for the triangle matching given ID and subdivide
  return triangles.map(tri => {
    if (tri.id === id && !tri.children) {
      const children = subdivideTriangle(tri, tri.id);
      return { ...tri, children, subdivided: true };
    } else if (tri.children) {
      return { ...tri, children: divideTriangleById(tri.children, id) };
    } else {
      return tri;
    }
  });
}

type Props = {
  worldSlug: string;
  settings?: any;
};

const DEFAULT_CENTER: [number, number] = [33, 0];

function getFixedWorldSlug(slug: string) {
  return (!slug || slug === "") ? "original" : slug;
}

const TriangleMeshMap = ({ worldSlug }: Props) => {
  const fixedWorldSlug = getFixedWorldSlug(worldSlug);
  const mapDivRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());
  const isMobile = useIsMobile();

  // --- Mesh state stored in memory ONLY ---
  const [mesh, setMesh] = useState<TriangleMesh[]>(() => generateBaseTriangleMesh());
  const [fitDone, setFitDone] = useState(false);
  const [mapIsReady, setMapIsReady] = useState(false);

  // Fit map to mesh whenever map or mesh changes
  useEffect(() => {
    setFitDone(false);
  }, [fixedWorldSlug, mesh.length]);

  const handleTriangleClick = (triangleId: string) => {
    setMesh(prevMesh => divideTriangleById(prevMesh, triangleId));
  };

  function handleMapReady(map: L.Map) {
    mapInstanceRef.current = map;
    setMapIsReady(true);
  }

  useEffect(() => {
    if (
      !fitDone &&
      mapIsReady &&
      mapInstanceRef.current &&
      mesh.length > 0
    ) {
      const bounds = L.latLngBounds([[-90, -180], [90, 180]]);
      mapInstanceRef.current.fitBounds(bounds, { padding: [24, 24], animate: true, maxZoom: 2 });
      setFitDone(true);
    }
  }, [mesh, fitDone, mapIsReady]);

  const trianglesToRender: TriangleMesh[] = mesh;

  return (
    <div className="relative w-full h-full min-h-[0] flex-1 rounded-none border-0 p-0 m-0">
      <LeafletMapContainer
        ref={mapDivRef}
        isMobile={isMobile}
        meshVersion={"local"}
        worldSlug={fixedWorldSlug}
        onMapReady={handleMapReady}
        desktopMinZoom={1}
        desktopMaxZoom={4}
        fixedMobileZoomLevel={2}
        forceMobileZoom={false}
      />
      {mapIsReady && mapInstanceRef.current && trianglesToRender.length > 0 && (
        <TriangleMeshRenderer
          map={mapInstanceRef.current}
          triangleMesh={trianglesToRender}
          triangleLayersRef={triangleLayersRef}
          onTriangleClick={handleTriangleClick}
          maxDivideLevel={3}
          clicksToDivide={1}
        />
      )}
      {mapIsReady && mapInstanceRef.current && trianglesToRender.length === 0 && (
        <div className="absolute left-0 right-0 top-0 bottom-0 flex items-center justify-center bg-white/70 z-50 font-bold text-red-600">
          Error: No triangles to display!
        </div>
      )}
    </div>
  );
};

export default TriangleMeshMap;
