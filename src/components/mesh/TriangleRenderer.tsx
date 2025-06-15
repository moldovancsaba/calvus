
import React from "react";
import L from "leaflet";
import { renderGeodesicTriangle } from "./renderGeodesicTriangle";
import { renderAvatarMarker } from "./renderAvatarMarker";

/**
 * Props for rendering a single triangle. 
 */
type Triangle = {
  id: string;
  vertices: { lat: number; lng: number }[];
  color?: string;
  emoji?: string;
  gametag?: string;
  children?: Triangle[];
  clickCount: number;
  subdivided?: boolean;
  level: number;
};
interface Props {
  map: L.Map;
  triangle: Triangle;
  trianglePath: string;
  triangleLayersRef: React.MutableRefObject<Map<string, L.Polygon>>;
  numberMarkersRef: React.MutableRefObject<Map<string, L.Marker>>;
  onTriangleClick: (triangleId: string, triangle?: Triangle, parentPath?: string) => void;
  maxDivideLevel: number;
  clicksToDivide: number;
}

export function TriangleRenderer({
  map,
  triangle,
  trianglePath,
  triangleLayersRef,
  numberMarkersRef,
  onTriangleClick,
  maxDivideLevel,
  clicksToDivide,
}: Props) {
  React.useEffect(() => {
    console.log("[TriangleRenderer] Render", { triangle, trianglePath, maxDivideLevel, clicksToDivide, map });
    // Remove previous layer
    const prevLayer = triangleLayersRef.current.get(trianglePath);
    if (prevLayer) {
      map.removeLayer(prevLayer);
    }
    // Remove marker if any
    const prevMarker = numberMarkersRef.current.get(trianglePath);
    if (prevMarker) {
      map.removeLayer(prevMarker);
    }
    // --- RENDER POLYGON ---
    const isFinalLevel = triangle.level >= maxDivideLevel;
    const coordinates = renderGeodesicTriangle(triangle.vertices);

    let fill = "#fff";
    let fillOpacity = 0.5;
    let shouldShowAvatar = false;
    let avatarProps: null | { color: string, emoji: string } = null;
    const claimedEmoji =
      triangle.emoji && triangle.emoji.trim() !== "" ? triangle.emoji : null;

    if (
      isFinalLevel && triangle.clickCount >= clicksToDivide && triangle.color
    ) {
      fill = triangle.color;
      fillOpacity = 1.0;
      shouldShowAvatar = true;
      avatarProps = {
        color: triangle.color,
        emoji: claimedEmoji ?? "🌟"
      };
    } else if (triangle.clickCount > 0) {
      fill = triangle.color || "#222";
      fillOpacity = Math.min(0.3 + triangle.clickCount * 0.07, 0.95);
    }

    // --- DEBUG: draw a demo polygon at a fixed place for visual debugging
    if (triangle.level === 0 && trianglePath.endsWith(".meshDebug")) {
      const debugPolygon = L.polygon([
        [33, 0],
        [35, 3],
        [31, 6],
      ], { color: "red", weight: 3, fillColor: "#f004", fillOpacity: 0.7 });
      debugPolygon.addTo(map);
      console.log("[TriangleRenderer] Debug polygon drawn", debugPolygon.getLatLngs());
    }

    const polygon = L.polygon(coordinates, {
      color: "#fff",
      weight: 2,
      opacity: 0.8,
      fillColor: fill,
      fillOpacity,
      smoothFactor: 1.0,
      interactive: true,
      className: "leaflet-interactive"
    });

    polygon.on("pointerdown", () => onTriangleClick(triangle.id, triangle, trianglePath));
    polygon.on("click", () => onTriangleClick(triangle.id, triangle, trianglePath));
    polygon.on("touchstart", () => onTriangleClick(triangle.id, triangle, trianglePath));
    polygon.addTo(map);
    triangleLayersRef.current.set(trianglePath, polygon);

    // Post-render check: see how many polygons are on the map
    const allLayers = Object.values((map as any)._layers || {});
    const polyCount = allLayers.filter((l) => l instanceof L.Polygon).length;
    // Type safe: print only if leaflet id present
    const polyIds = allLayers
      .filter((l): l is { _leaflet_id: number } => typeof l === "object" && l !== null && "_leaflet_id" in l)
      .map((l) => (l as any)._leaflet_id);
    console.log(`[TriangleRenderer] After add: Leaflet map has ${polyCount} polygons. Layer IDs:`, polyIds);
    // DEBUG: Log polygon shape/info
    console.log("[TriangleRenderer] Created polygon for", trianglePath, polygon.getLatLngs());

    // -- AVATAR --
    if (shouldShowAvatar && avatarProps) {
      renderAvatarMarker({
        map,
        vertices: triangle.vertices,
        color: avatarProps.color,
        emoji: avatarProps.emoji,
        trianglePath,
        numberMarkersRef,
      });
    }

    // Cleanup on unmount
    return () => {
      const l = triangleLayersRef.current.get(trianglePath);
      if (l && map.hasLayer(l)) map.removeLayer(l);
      triangleLayersRef.current.delete(trianglePath);

      const marker = numberMarkersRef.current.get(trianglePath);
      if (marker && map.hasLayer(marker)) map.removeLayer(marker);
      numberMarkersRef.current.delete(trianglePath);
    };
    // We want a full rerender if any relevant param changes
    // eslint-disable-next-line
  }, [
    map, triangle.id, triangle.vertices, triangle.color, triangle.emoji, triangle.clickCount, triangle.level, triangle.gametag, trianglePath,
    maxDivideLevel, clicksToDivide
  ]);
  return null;
}
