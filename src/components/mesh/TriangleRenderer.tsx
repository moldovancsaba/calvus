
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
