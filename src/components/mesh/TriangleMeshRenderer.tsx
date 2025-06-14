
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

    // -- Add extra check for map DOM readiness and getPane --
    function isMapReallyReady(map: L.Map) {
      try {
        const c = map.getContainer?.();
        // Pane 'overlayPane' is always used for polygons
        return (
          !!c &&
          !!c.parentNode &&
          !!map.getPane("overlayPane")
        );
      } catch {
        return false;
      }
    }

    const renderTriangleMesh = (triangleList: TriangleMesh[], parentPath: string = "") => {
      for (const triangle of triangleList) {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        if (!triangle.subdivided) {
          // Defensive: always fetch current container just before manipulating!
          const container = map.getContainer?.();
          // Extra check: map actually ready and its overlayPane present!
          if (!map || !container || !container.parentNode || !map.getPane("overlayPane")) {
            console.warn("[TriangleMeshRenderer render] map or container/overlayPane is not fully ready, skip triangle", trianglePath);
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
          if (!map || !container.parentNode || !map.getPane("overlayPane")) {
            console.warn("[TriangleMeshRenderer renderPolygon] map or container/overlayPane not fresh, skipping polygon add.");
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

          // Defensive: Ensure map and overlayPane are both valid!
          const safeMap = map;
          const safeContainer = map.getContainer?.();
          if (safeMap && safeContainer && safeContainer.parentNode && map.getPane("overlayPane")) {
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
    if (map && currentContainer && currentContainer.parentNode && map.getPane("overlayPane")) {
      triangleLayersRef.current.forEach(layer => {
        if (map.hasLayer(layer)) map.removeLayer(layer);
      });
    }
    triangleLayersRef.current.clear();

    // -- SKIP rendering if map is not really ready! --
    if (!isMapReallyReady(map)) {
      console.warn("[TriangleMeshRenderer effect] Rendering skipped: map not ready (missing overlayPane)");
      return;
    }

    renderTriangleMesh(triangleMesh);

    // Cleanup: remove layers on unmount, only if map is valid and still attached
    return () => {
      const cleanupContainer = map.getContainer?.();
      if (map && cleanupContainer && cleanupContainer.parentNode && map.getPane("overlayPane")) {
        triangleLayersRef.current.forEach(layer => {
          if (map.hasLayer(layer)) map.removeLayer(layer);
        });
      }
      triangleLayersRef.current.clear();
    };
  }, [map, triangleMesh, triangleLayersRef, onTriangleClick]);

  return null;
}

