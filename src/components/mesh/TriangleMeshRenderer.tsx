
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
        } else if (triangle.children) {
          out.push(...renderTriangles(triangle.children, trianglePath));
        }
      }
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

  if (!map) return null;
  const container = map.getContainer?.();
  if (!container || !container.parentNode) return null;

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

  // Recursively render all triangles as effects (not DOM elements)
  return <>{renderTriangles(triangleMesh)}</>;
}

