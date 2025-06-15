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

  React.useEffect(() => {
    console.log("[TRIANGLE_MESH]", Array.isArray(triangleMesh) ? triangleMesh.length : triangleMesh, triangleMesh);
    if (triangleMesh?.length > 0) {
      console.log("[TRIANGLE_SAMPLE]", triangleMesh[0]);
    }

    // DEBUG: Add marker at 0,0 to confirm map & overlays are visible
    if (map) {
      const debugMarker = L.circleMarker([0, 0], { color: "#d00", radius: 8 }).addTo(map);
      debugMarker.bindTooltip("DEBUG: 0,0", {permanent: true });
      return () => {
        if (map.hasLayer(debugMarker)) map.removeLayer(debugMarker);
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

  React.useEffect(() => {
    triangleLayersRef.current.forEach(layer => {
      if (map.hasLayer(layer)) map.removeLayer(layer);
    });
    triangleLayersRef.current.clear();
    numberMarkersRef.current.forEach((marker) => {
      if (map.hasLayer(marker)) map.removeLayer(marker);
    });
    numberMarkersRef.current.clear();
  }, [map, triangleMesh, triangleLayersRef]);

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

  // Always pass an array (empty allowed)
  const safeTriangles: TriangleMesh[] = Array.isArray(triangleMesh) ? triangleMesh : [];

  // Defensive render: output = array of ReactNode or null
  const output = renderTriangles(safeTriangles);

  if (!output) return null;
  return <>{output}</>;
}
