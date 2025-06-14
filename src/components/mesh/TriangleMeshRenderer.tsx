import L from "leaflet";
import { useEffect } from "react";
import { createGeodesicTriangle } from "./GeodesicTriangle";
import type { TriangleMesh } from "../../utils/triangleMesh/geometry";

type Props = {
  map: L.Map | null;
  triangleMesh: TriangleMesh[];
  triangleLayersRef: React.MutableRefObject<Map<string, L.Polygon>>;
  onTriangleClick: (triangleId: string, triangle?: TriangleMesh) => void;
};

export function TriangleMeshRenderer({
  map,
  triangleMesh,
  triangleLayersRef,
  onTriangleClick
}: Props) {
  useEffect(() => {
    if (!map || !triangleMesh) return;

    const renderTriangleMesh = (triangleList: TriangleMesh[], parentPath: string = "") => {
      triangleList.forEach(triangle => {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        if (!triangle.subdivided) {
          // Remove existing layer if it exists
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

          // Robust: Use pointer events (handles touch+mouse+pen), fallback to click for legacy
          const pointerHandler = (e: any) => {
            console.log("[TriangleMeshRenderer] polygon.pointerdown", e, triangle);
            onTriangleClick(triangle.id, triangle);
          };

          polygon.on("pointerdown", pointerHandler);

          // For browsers/devices not supporting pointer events, keep "click" as safety net
          polygon.on("click", (e: any) => {
            console.log("[TriangleMeshRenderer] polygon.click", e, triangle);
            onTriangleClick(triangle.id, triangle);
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

    // Cleanup function to remove layers on unmount
    return () => {
      triangleLayersRef.current.forEach(layer => {
        map.removeLayer(layer);
      });
      triangleLayersRef.current.clear();
    };
  }, [map, triangleMesh, triangleLayersRef, onTriangleClick]);

  return null;
}
