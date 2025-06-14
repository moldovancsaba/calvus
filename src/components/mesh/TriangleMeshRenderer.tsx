import L from "leaflet";
import React from "react";
import { createGeodesicTriangle } from "./GeodesicTriangle";
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
};

export function TriangleMeshRenderer({
  map,
  triangleMesh,
  triangleLayersRef,
  onTriangleClick
}: Props) {
  // SAFETY: Don't do anything if map not ready
  if (!map) return null;

  React.useEffect(() => {
    if (!map || !triangleMesh) return;

    const renderTriangleMesh = (triangleList: TriangleMesh[], parentPath: string = "") => {
      triangleList.forEach(triangle => {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        if (!triangle.subdivided) {
          const existingLayer = triangleLayersRef.current.get(trianglePath);
          if (existingLayer) map.removeLayer(existingLayer);

          const coordinates = createGeodesicTriangle(triangle.vertices);
          let fill = "#fff";
          if (triangle.clickCount > 0) {
            fill = triangle.color || "#222";
          }
          const fillOpacity = triangle.clickCount === 0
            ? 0.5
            : Math.min(0.3 + triangle.clickCount * 0.07, 0.95);

          const polygon = L.polygon(coordinates, {
            color: fill,
            weight: 2,
            opacity: 0.8,
            fillColor: fill,
            fillOpacity,
            smoothFactor: 1.0,
            interactive: true,
            className: "leaflet-interactive"
          });

          // --- Main interaction events ---

          // Handle pointerdown (desktop and modern mobile)
          polygon.on("pointerdown", (e: any) => {
            console.log("[TriangleMeshRenderer] pointerdown", e, triangle);
            onTriangleClick(triangle.id, triangle, trianglePath);
          });

          // Fallback for mouse click
          polygon.on("click", (e: any) => {
            console.log("[TriangleMeshRenderer] click fallback", e, triangle);
            onTriangleClick(triangle.id, triangle, trianglePath);
          });

          // Direct touch interaction for mobile browsers
          polygon.on("touchstart", (e: any) => {
            console.log("[TriangleMeshRenderer] touchstart - firing tap/click!", e, triangle);
            onTriangleClick(triangle.id, triangle, trianglePath);
          });

          // (Optional debug, can be removed after confirming touch works)
          polygon.on("touchend", (e: any) => {
            console.log("[TriangleMeshRenderer] touchend", e, triangle);
          });

          polygon.addTo(map);
          triangleLayersRef.current.set(trianglePath, polygon);
        } else if (triangle.children) {
          renderTriangleMesh(triangle.children, trianglePath);
        }
      });
    };

    // Remove all current layers first
    triangleLayersRef.current.forEach(layer => {
      map.removeLayer(layer);
    });
    triangleLayersRef.current.clear();

    renderTriangleMesh(triangleMesh);

    // Cleanup: remove layers on unmount
    return () => {
      triangleLayersRef.current.forEach(layer => {
        map.removeLayer(layer);
      });
      triangleLayersRef.current.clear();
    };
  }, [map, triangleMesh, triangleLayersRef, onTriangleClick]);

  return null;
}
