
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
    // --- VISUAL DEBUGGING ---
    if (map) {
      // Place a debugging marker at (0,0)
      const debugMarker = L.marker([0,0], { title: "Debug Origin Marker" }).addTo(map);
      numberMarkersRef.current.set("__debug_marker", debugMarker);
      // Style the map container for visibility
      const container = map.getContainer();
      container.style.border = "3px solid red";
      container.style.backgroundColor = "#fffbe7";
      // Log out current polygons
      const allLayers = Object.values((map as any)._layers || {});
      const polyCount = allLayers.filter((l) => l instanceof L.Polygon).length;
      console.info(`[DEBUG - after mount] Leaflet map has ${polyCount} polygons. Layer IDs:`, allLayers.map((l: any) => l._leaflet_id));
    }
    // Cleanup debug marker
    return () => {
      const marker = numberMarkersRef.current.get("__debug_marker");
      if (marker && map && map.hasLayer(marker)) map.removeLayer(marker);
      numberMarkersRef.current.delete("__debug_marker");
      // Unstyle
      if (map) {
        const container = map.getContainer();
        container.style.border = "";
        container.style.backgroundColor = "";
      }
    };
    // eslint-disable-next-line
  }, [map]);

  // Defensive recursive render
  const renderTriangles = React.useCallback(
    (list: TriangleMesh[], parentPath = "") => {
      if (!Array.isArray(list) || !list.length) return null;
      const out: React.ReactNode[] = [];
      for (const triangle of list) {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        console.log("[TriangleMeshRenderer] Will render TriangleRenderer for", triangle?.id, trianglePath, triangle.vertices);
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

  const output = renderTriangles(safeTriangles);

  if (!output) return null;
  return <>{output}</>;
}
