
import L from "leaflet";
import React from "react";
import { createGeodesicTriangle } from "./GeodesicTriangle";
import type { TriangleMesh } from "../../utils/triangleMesh/geometry";

/** Helper: Compute centroid (average lat/lng) of three vertices */
function getTriangleCentroid(vertices: { lat: number; lng: number }[]): [number, number] {
  const lat = (vertices[0].lat + vertices[1].lat + vertices[2].lat) / 3;
  const lng = (vertices[0].lng + vertices[1].lng + vertices[2].lng) / 3;
  return [lat, lng];
}

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

  // Use ref for number markers so we can clean them up on mesh change
  const numberMarkersRef = React.useRef<Map<string, L.Marker>>(new Map());

  React.useEffect(() => {
    // Cleanup number markers before rendering new ones
    numberMarkersRef.current.forEach((marker) => {
      if (map.hasLayer(marker)) map.removeLayer(marker);
    });
    numberMarkersRef.current.clear();

    // Guard: if map is destroyed, do not run effect
    if (!map || !triangleMesh) return;

    const mapContainer = map.getContainer?.();
    if (!mapContainer || !mapContainer.parentNode) {
      console.warn("[TriangleMeshRenderer useEffect] map container detached, aborting");
      return;
    }

    function isMapReallyReady(map: L.Map) {
      try {
        const c = map.getContainer?.();
        return (
          !!c &&
          !!c.parentNode &&
          !!map.getPane("overlayPane")
        );
      } catch {
        return false;
      }
    }

    // In order to know base triangle indexes, flat filter base (level 0) triangles in traversal order
    const baseTrianglePaths: { triangle: TriangleMesh; path: string; index: number }[] = [];
    let runningIdx = 0;
    const collectBaseTriangles = (triangleList: TriangleMesh[], parentPath = "") => {
      for (const triangle of triangleList) {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        if (triangle.level === 0 && !triangle.subdivided) {
          runningIdx += 1;
          baseTrianglePaths.push({ triangle, path: trianglePath, index: runningIdx });
        }
        // Don't count subdivided base triangles as "base" for overlay purposes
      }
    };
    collectBaseTriangles(triangleMesh);

    // Helper to render triangle mesh
    const renderTriangleMesh = (triangleList: TriangleMesh[], parentPath: string = "") => {
      for (const triangle of triangleList) {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        if (!triangle.subdivided) {
          const container = map.getContainer?.();
          if (!map || !container || !container.parentNode || !map.getPane("overlayPane")) {
            console.warn("[TriangleMeshRenderer render] map or container/overlayPane is not fully ready, skip triangle", trianglePath);
            return;
          }

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

          if (!map || !container.parentNode || !map.getPane("overlayPane")) {
            console.warn("[TriangleMeshRenderer renderPolygon] map or container/overlayPane not fresh, skipping polygon add.");
            return;
          }

          const polygon = L.polygon(coordinates, {
            color: "#fff",                // <----- Edge always WHITE
            weight: 2,
            opacity: 0.8,
            fillColor: fill,
            fillOpacity,
            smoothFactor: 1.0,
            interactive: true,
            className: "leaflet-interactive"
          });

          const safeMap = map;
          const safeContainer = map.getContainer?.();
          if (safeMap && safeContainer && safeContainer.parentNode && map.getPane("overlayPane")) {
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

          // --- Draw label for base triangles only ---
          const baseIdx = baseTrianglePaths.find(
            t => t.path === trianglePath
          )?.index;
          if (triangle.level === 0 && !triangle.subdivided && typeof baseIdx === "number") {
            const centroid = getTriangleCentroid(triangle.vertices);
            const divIcon = L.divIcon({
              html: `<div style="color:#234;font-size:1.15em;font-weight:bold;background:rgba(255,255,255,0.85);padding:0.15em 0.45em;border-radius:1em;border:1px solid #ccc;box-shadow:0 1px 4px #0001;">${baseIdx}</div>`,
              className: "", // Don't use any custom class so it doesn't interfere.
              iconSize: [30, 22],
              iconAnchor: [15, 12],
            });
            const marker = L.marker(centroid, {
              icon: divIcon,
              interactive: false,
              zIndexOffset: 1000
            }).addTo(map);
            numberMarkersRef.current.set(trianglePath, marker);
          }
        } else if (triangle.children) {
          renderTriangleMesh(triangle.children, trianglePath);
        }
      }
    };

    // Remove all old triangle layers (polygons)
    const currentContainer = map.getContainer?.();
    if (map && currentContainer && currentContainer.parentNode && map.getPane("overlayPane")) {
      triangleLayersRef.current.forEach(layer => {
        if (map.hasLayer(layer)) map.removeLayer(layer);
      });
    }
    triangleLayersRef.current.clear();

    if (!isMapReallyReady(map)) {
      console.warn("[TriangleMeshRenderer effect] Rendering skipped: map not ready (missing overlayPane)");
      return;
    }

    renderTriangleMesh(triangleMesh);

    // Cleanup function removes polygons AND number markers
    return () => {
      const cleanupContainer = map.getContainer?.();
      if (map && cleanupContainer && cleanupContainer.parentNode && map.getPane("overlayPane")) {
        triangleLayersRef.current.forEach(layer => {
          if (map.hasLayer(layer)) map.removeLayer(layer);
        });
      }
      triangleLayersRef.current.clear();

      // Remove all number markers
      numberMarkersRef.current.forEach((marker) => {
        if (map.hasLayer(marker)) map.removeLayer(marker);
      });
      numberMarkersRef.current.clear();
    };
  }, [map, triangleMesh, triangleLayersRef, onTriangleClick]);

  return null;
}

