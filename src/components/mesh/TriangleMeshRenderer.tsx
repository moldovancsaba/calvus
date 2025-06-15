
import L from "leaflet";
import React from "react";
import { TriangleRenderer } from "./TriangleRenderer";
import type { TriangleMesh } from "../../utils/triangleMesh/geometry";

/**
 * Recursively renders the triangle mesh using individual TriangleRenderer components.
 */
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

  // Helper to recursively render triangles FLAT (no nested arrays)
  const renderTriangles = React.useCallback(
    (list: TriangleMesh[], parentPath = "") => {
      const out: React.ReactNode[] = [];
      for (const triangle of list) {
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
          // For our debug: also push a debug-only polygon on first triangle
          if (triangle.level === 0 && out.length === 1) {
            out.push(
              <TriangleRenderer
                key={trianglePath + ".meshDebug"}
                map={map!}
                triangle={{ ...triangle, level: 0, vertices: [{lat:33,lng:0},{lat:35,lng:3},{lat:31,lng:6}], id: triangle.id + ".meshDebug" }}
                trianglePath={trianglePath + ".meshDebug"}
                triangleLayersRef={triangleLayersRef}
                numberMarkersRef={numberMarkersRef}
                onTriangleClick={onTriangleClick}
                maxDivideLevel={maxDivideLevel}
                clicksToDivide={clicksToDivide}
              />
            );
          }
        } else if (triangle.children) {
          out.push(...renderTriangles(triangle.children, trianglePath));
        }
      }
      console.log("[TriangleMeshRenderer] renderTriangles result:", out, list);
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

  // Clean up: remove all triangle layers & markers on mesh change
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
      // How many polygons are present?
      const allLayers = Object.values((map as any)._layers || {});
      const polyCount = allLayers.filter((l) => l instanceof L.Polygon).length;
      console.log(`[TriangleMeshRenderer] (Effect) Leaflet map has ${polyCount} polygons. Layer IDs:`, allLayers.map(l => l._leaflet_id));
    }
  }, [triangleMesh, map]);

  // Recursively render all triangles as effects (not DOM elements)
  return <>{renderTriangles(triangleMesh)}</>;
}

