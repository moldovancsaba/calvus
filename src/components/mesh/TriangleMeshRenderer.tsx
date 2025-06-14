
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
  // SAFETY: Don't do anything if map not ready or not mounted
  if (!map) return null;
  const container = map.getContainer?.();
  if (!container || !container.parentNode) {
    console.warn("[TriangleMeshRenderer] map or container is not mounted, rendering aborted");
    return null;
  }

  React.useEffect(() => {
    // Guard: if map is destroyed, do not run effect
    if (!map || !triangleMesh) return;

    const mapContainer = map.getContainer?.();
    if (!mapContainer || !mapContainer.parentNode) {
      // Do not attempt any rendering if map container is not attached!
      console.warn("[TriangleMeshRenderer useEffect] map container detached, aborting");
      return;
    }

    const renderTriangleMesh = (triangleList: TriangleMesh[], parentPath: string = "") => {
      for (const triangle of triangleList) {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        if (!triangle.subdivided) {
          // Defensive: always fetch current container just before manipulating!
          const container = map.getContainer?.();
          if (!map || !container || !container.parentNode) {
            console.warn("[TriangleMeshRenderer render] map or container is not mounted (inner loop), skip triangle", trianglePath);
            return;
          }

          // Remove existing layer first
          const existingLayer = triangleLayersRef.current.get(trianglePath);
          if (existingLayer && map.hasLayer(existingLayer)) map.removeLayer(existingLayer);

          const coordinates = createGeodesicTriangle(triangle.vertices);

          let fill = "#fff";
          if (triangle.clickCount > 0) {
            fill = triangle.color || "#222";
          }
          const fillOpacity = triangle.clickCount === 0
            ? 0.5
            : Math.min(0.3 + triangle.clickCount * 0.07, 0.95);

          // Defensive: check freshness again
          if (!map || !container.parentNode) {
            console.warn("[TriangleMeshRenderer renderPolygon] map or container is not fresh, skipping polygon add.");
            return;
          }

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

          // Defensive: Ensure map and its container are valid and attached!
          const safeMap = map;
          const safeContainer = map.getContainer?.();
          if (safeMap && safeContainer && safeContainer.parentNode) {
            // --- Main interaction events ---
            polygon.on("pointerdown", (e: any) => {
              onTriangleClick(triangle.id, triangle, trianglePath);
            });
            polygon.on("click", (e: any) => {
              onTriangleClick(triangle.id, triangle, trianglePath);
            });
            polygon.on("touchstart", (e: any) => {
              onTriangleClick(triangle.id, triangle, trianglePath);
            });
            polygon.on("touchend", (e: any) => {
              // Optionally add touch end logic if needed
            });

            polygon.addTo(safeMap);
            triangleLayersRef.current.set(trianglePath, polygon);
          }
        } else if (triangle.children) {
          renderTriangleMesh(triangle.children, trianglePath);
        }
      }
    };

    // Defensive: clear existing layers only if container is still valid
    const currentContainer = map.getContainer?.();
    if (map && currentContainer && currentContainer.parentNode) {
      triangleLayersRef.current.forEach(layer => {
        if (map.hasLayer(layer)) map.removeLayer(layer);
      });
    }
    triangleLayersRef.current.clear();

    renderTriangleMesh(triangleMesh);

    // Cleanup: remove layers on unmount, only if map is valid and still attached
    return () => {
      const cleanupContainer = map.getContainer?.();
      if (map && cleanupContainer && cleanupContainer.parentNode) {
        triangleLayersRef.current.forEach(layer => {
          if (map.hasLayer(layer)) map.removeLayer(layer);
        });
      }
      triangleLayersRef.current.clear();
    };
  }, [map, triangleMesh, triangleLayersRef, onTriangleClick]);

  return null;
}
