
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

  // Log mesh each render for debugging
  React.useEffect(() => {
    console.log("[TRIANGLE_MESH]", Array.isArray(triangleMesh) ? triangleMesh.length : triangleMesh, triangleMesh);
    if (triangleMesh?.length > 0) {
      console.log("[TRIANGLE_SAMPLE]", triangleMesh[0]);
    }
  }, [triangleMesh]);
  
  // Helper to recursively render triangles FLAT (no nested arrays)
  const renderTriangles = React.useCallback(
    (list: TriangleMesh[], parentPath = "") => {
      const out: React.ReactNode[] = [];
      for (const triangle of list) {
        // Log each triangle processed for debugging
        console.log("[RENDER_TRIANGLE]", triangle);
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
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
          out.push(...renderTriangles(triangle.children, trianglePath));
        }
      }
      console.log("[TriangleMeshRenderer] renderTriangles output count:", out.length, "props.triangleMesh count:", list.length, "sample:", list.slice(0,3));
      return out;
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

  // Remove debug triangle rendering

  return <>{renderTriangles(triangleMesh)}</>;
}
