import L from "leaflet";
import React from "react";
import { createGeodesicTriangle } from "./GeodesicTriangle";
import type { TriangleMesh } from "../../utils/triangleMesh/geometry";
import { UserAvatar } from "../UserAvatar";
import { useIdentity } from "../IdentityContext";

// Helper: centroid for three vertices
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
  maxDivideLevel?: number; // option: for custom max levels
  clicksToDivide?: number; // option: for custom click count
};

export function TriangleMeshRenderer({
  map,
  triangleMesh,
  triangleLayersRef,
  onTriangleClick,
  maxDivideLevel = 3, // sensible defaults
  clicksToDivide = 3,
}: Props) {
  // Do not render if map not ready
  if (!map) return null;
  const container = map.getContainer?.();
  if (!container || !container.parentNode) {
    console.warn("[TriangleMeshRenderer] map or container is not mounted, rendering aborted");
    return null;
  }

  const numberMarkersRef = React.useRef<Map<string, L.Marker>>(new Map());

  // We'll need the current identity so we can associate emoji/avatar to triangles.
  // However, the triangle itself knows its owner, so we do not rely on only current user
  // The triangle stores `gametag`, `color`, and can (later maybe) have emoji.

  // Clean up effect on triangleMesh changes
  React.useEffect(() => {
    // ... keep existing code (cleanup of old layers and markers) the same ...
    numberMarkersRef.current.forEach((marker) => {
      if (map.hasLayer(marker)) map.removeLayer(marker);
    });
    numberMarkersRef.current.clear();

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

    // ---- Main triangle mesh render (recursive) ----
    const renderTriangleMesh = (
      triangleList: TriangleMesh[], 
      parentPath: string = ""
    ) => {
      for (const triangle of triangleList) {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;

        // We'll need to know at what level no further subdivision is allowed
        // Check if the triangle is at the deepest allowed (final) level
        const isFinalLevel = triangle.level >= maxDivideLevel;

        // Only subdivide if not subdivided
        if (!triangle.subdivided) {
          // ... previous checks unchanged ...
          const container = map.getContainer?.();
          if (!map || !container || !container.parentNode || !map.getPane("overlayPane")) {
            console.warn("[TriangleMeshRenderer render] map or container/overlayPane is not fully ready, skip triangle", trianglePath);
            return;
          }
          const existingLayer = triangleLayersRef.current.get(trianglePath);
          if (existingLayer && map.hasLayer(existingLayer)) map.removeLayer(existingLayer);

          const coordinates = createGeodesicTriangle(triangle.vertices);

          // Determine fill and opacity based on new rule:
          // - If final level and has max clicks, show owner's color at 100% opacity
          // - Otherwise, normal fading logic
          let fill = "#fff";
          let fillOpacity = 0.5;
          let shouldShowAvatar = false;
          let avatarProps: null | { color: string, emoji: string } = null;

          if (
            isFinalLevel && triangle.clickCount >= clicksToDivide && triangle.color
          ) {
            // (1) full owner color; (2) always at 100% opacity
            fill = triangle.color;
            fillOpacity = 1.0;
            shouldShowAvatar = true;
            // Find emoji: use optional triangle.emoji if present (future), else fallback to only color
            // We'll just show avatar with color; emoji must come from triangle.gametag (not in triangle now)
            // Optionally, you could show owner gametag, but for now, emoji.
            // We don't store emoji per triangle, only color/gametag, so use a neutral emoji when missing.
            avatarProps = { 
              color: triangle.color, 
              emoji: (triangle as any).emoji || "🌟"
            }; 
            // The emoji could be improved with a DB change, for now we fallback to a star.
          } else if (triangle.clickCount > 0) {
            fill = triangle.color || "#222";
            fillOpacity = Math.min(0.3 + triangle.clickCount * 0.07, 0.95);
          }

          if (!map || !container.parentNode || !map.getPane("overlayPane")) {
            console.warn("[TriangleMeshRenderer renderPolygon] map or container/overlayPane not fresh, skipping polygon add.");
            return;
          }
          const polygon = L.polygon(coordinates, {
            color: "#fff",                // Edge always WHITE
            weight: 2,
            opacity: 0.8,
            fillColor: fill,
            fillOpacity,
            smoothFactor: 1.0,
            interactive: true,
            className: "leaflet-interactive"
          });

          // Setup triangle click handlers
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

            // ---- NEW: Draw emoji/avatar at centroid for final level triangles ----
            if (shouldShowAvatar && avatarProps) {
              // Place a Leaflet marker at centroid with a custom emoji icon
              const centroid = getTriangleCentroid(triangle.vertices);

              // Create a simple React render into static markup for the avatar.
              const size = 34;
              const markerDiv = document.createElement("div");
              markerDiv.style.width = `${size}px`;
              markerDiv.style.height = `${size}px`;
              markerDiv.style.display = "flex";
              markerDiv.style.alignItems = "center";
              markerDiv.style.justifyContent = "center";
              markerDiv.style.borderRadius = "50%";
              markerDiv.style.border = "2.2px solid #333";
              markerDiv.style.boxShadow = "0 3px 8px 0 #2222";
              markerDiv.style.background = avatarProps.color;
              markerDiv.style.fontSize = "1.45rem";
              markerDiv.style.userSelect = "none";
              markerDiv.innerText = avatarProps.emoji;

              const icon = L.divIcon({
                className: "",
                html: markerDiv,
                iconSize: [size, size],
                iconAnchor: [size / 2, size / 2],
                popupAnchor: [0, 0],
              });
              const marker = L.marker(centroid, {
                icon,
                interactive: false,
                keyboard: false,
                zIndexOffset: 10000,
              });
              marker.addTo(safeMap);
              numberMarkersRef.current.set(trianglePath, marker);
            }
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

      numberMarkersRef.current.forEach((marker) => {
        if (map.hasLayer(marker)) map.removeLayer(marker);
      });
      numberMarkersRef.current.clear();
    };
  }, [map, triangleMesh, triangleLayersRef, onTriangleClick, maxDivideLevel, clicksToDivide]);

  return null;
}
