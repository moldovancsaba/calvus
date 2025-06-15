import L from "leaflet";
import React from "react";
import { TriangleRenderer } from "./TriangleRenderer";
import type { TriangleMesh } from "../../utils/triangleMesh/geometry";

type Props = {
  map: L.Map | null;
  triangleMesh: TriangleMesh[];
  triangleLayersRef: React.MutableRefObject<Map<string, L.Polygon>>;
  onTriangleClick: (
    triangleId: string,
    triangle?: TriangleMesh,
    parentPath?: string
  ) => void;
  maxDivideLevel?: number;
  clicksToDivide?: number;
};

export function TriangleMeshRenderer({
  map,
  triangleMesh,
  triangleLayersRef,
  onTriangleClick,
  maxDivideLevel = 3,
  clicksToDivide = 3,
}: Props) {
  const numberMarkersRef = React.useRef<Map<string, L.Marker>>(new Map());

  // Always pass an array (empty allowed)
  const safeTriangles: TriangleMesh[] = Array.isArray(triangleMesh) ? triangleMesh : [];

  React.useEffect(() => {
    console.log("[TRIANGLE_MESH]", Array.isArray(triangleMesh) ? triangleMesh.length : triangleMesh, triangleMesh);
    if (triangleMesh?.length > 0) {
      console.log("[TRIANGLE_SAMPLE]", triangleMesh[0]);
    }

    // DEBUG: Add marker at 0,0 to confirm map & overlays are visible
    if (map) {
      const debugMarker = L.circleMarker([0, 0], { color: "#d00", radius: 8 }).addTo(map);
      debugMarker.bindTooltip("DEBUG: 0,0", {permanent: true });

      // *** NEW: add a hardcoded triangle in visible area as a baseline ***
      // Explicit typing so TypeScript recognizes this as LatLngTuple[]
      const hardCodedPolygonLatLngs: [number, number][] = [
        [3, -2],
        [7, 4],
        [8, -8],
      ];
      const debugPoly = L.polygon(hardCodedPolygonLatLngs, {
        color: "#f0c",
        weight: 5,
        fillColor: "#f8f",
        fillOpacity: 0.7,
      }).addTo(map);
      debugPoly.bindTooltip("HARDCODED POLY", {permanent: false});

      return () => {
        if (map.hasLayer(debugMarker)) map.removeLayer(debugMarker);
        if (map.hasLayer(debugPoly)) map.removeLayer(debugPoly);
      };
    }
  }, [triangleMesh, map]);
  
  // Defensive recursive render
  const renderTriangles = React.useCallback(
    (list: TriangleMesh[], parentPath = "") => {
      if (!Array.isArray(list) || !list.length) return null;
      const out: React.ReactNode[] = [];
      for (const triangle of list) {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        // Add strong console logs before rendering
        console.log("[TriangleMeshRenderer] Will render TriangleRenderer for", triangle?.id, trianglePath, triangle.vertices);

        // LOG: Output triangle vertices and their format for ALL triangles
        if (Array.isArray(triangle.vertices)) {
          console.log(
            `[TriangleMeshRenderer] Vertices for ${triangle.id}:`,
            triangle.vertices.map((v, idx) => `(${idx}: lat=${v.lat}, lng=${v.lng})`).join("; ")
          );
        } else {
          console.error(`[TriangleMeshRenderer] Triangle ${triangle.id} has invalid vertices:`, triangle.vertices);
        }

        if (!triangle.subdivided) {
          out.push(
            <TriangleRenderer
              key={trianglePath}
              map={map!}
              triangle={triangle}
              trianglePath={trianglePath}
              triangleLayersRef={triangleLayersRef}
              numberMarkersRef={numberMarkersRef}
              onTriangleClick={onTriangleClick}
              maxDivideLevel={maxDivideLevel}
              clicksToDivide={clicksToDivide}
            />
          );
        } else if (triangle.children) {
          const childNodes = renderTriangles(triangle.children, trianglePath);
          if (childNodes) {
            if (Array.isArray(childNodes)) {
              out.push(...childNodes);
            } else {
              out.push(childNodes);
            }
          }
        }
      }
      const filteredOut = out.filter(Boolean);
      console.log("[TriangleMeshRenderer] renderTriangles output count:", filteredOut.length, "props.triangleMesh count:", list.length, "sample:", list.slice(0,3));
      return filteredOut.length > 0 ? filteredOut : null;
    },
    [
      map,
      triangleLayersRef,
      onTriangleClick,
      maxDivideLevel,
      clicksToDivide,
    ]
  );

  if (!map) {
    console.log("[TriangleMeshRenderer] No map instance supplied.");
    return null;
  }
  const container = map.getContainer?.();
  if (!container || !container.parentNode) {
    console.log("[TriangleMeshRenderer] Map container not found or not attached to DOM");
    return null;
  }

  // Only clear existing polygons/markers if new mesh is non-empty
  React.useEffect(() => {
    // Only clear if we have triangles to render (prevents flicker if mesh is temporarily empty)
    if (safeTriangles.length === 0) return;

    triangleLayersRef.current.forEach(layer => {
      if (map.hasLayer(layer)) map.removeLayer(layer);
    });
    triangleLayersRef.current.clear();
    numberMarkersRef.current.forEach((marker) => {
      if (map.hasLayer(marker)) map.removeLayer(marker);
    });
    numberMarkersRef.current.clear();
  }, [map, triangleLayersRef, safeTriangles.length]); // Remove direct triangleMesh dependency

  React.useEffect(() => {
    console.log("[TriangleMeshRenderer] triangleMesh prop:", triangleMesh);
    console.log("[TriangleMeshRenderer] map instance:", map);
    if (map) {
      const allLayers = Object.values((map as any)._layers || {});
      const polyCount = allLayers.filter((l) => l instanceof L.Polygon).length;
      const polyIds = allLayers
        .filter((l): l is { _leaflet_id: number } => typeof l === "object" && l !== null && "_leaflet_id" in l)
        .map((l) => (l as any)._leaflet_id);
      console.log(`[TriangleMeshRenderer] (Effect) Leaflet map has ${polyCount} polygons. Layer IDs:`, polyIds);
    }
  }, [triangleMesh, map]);

  React.useEffect(() => {
    console.log("[TriangleMeshRenderer] MOUNTED, triangleMesh length:", triangleMesh?.length, "Sample:", triangleMesh?.slice(0,2));
  }, []);

  // Defensive render: output = array of ReactNode or null
  const output = renderTriangles(safeTriangles);

  if (!output) return null;
  return <>{output}</>;
}
