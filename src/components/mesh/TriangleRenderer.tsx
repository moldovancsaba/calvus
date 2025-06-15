
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

// Utility: pastel random color by id (hash)
function pastelColorFromId(str: string): string {
  let hash = 0;
  for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
  const h = hash % 360;
  return `hsl(${h}, 82%, 80%)`;
}

// Utility: centroid for marker
function centroid(vertices: {lat:number,lng:number}[]) {
  const lat = (vertices[0].lat + vertices[1].lat + vertices[2].lat) / 3;
  const lng = (vertices[0].lng + vertices[1].lng + vertices[2].lng) / 3;
  return [lat, lng];
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
    const coordinates = renderGeodesicTriangle(triangle.vertices);

    // Strong color & bold for debug
    const fill = pastelColorFromId(triangle.id);
    const fillOpacity = 0.65;

    const polygon = L.polygon(coordinates, {
      color: "#ff2222",
      weight: 5,
      opacity: 0.95,
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

    // Debug: Add a marker at centroid with triangle ID
    const [cLat, cLng] = centroid(triangle.vertices);
    const idMarker = L.marker([cLat, cLng], {
      title: triangle.id,
      keyboard: false,
      opacity: 0.7,
      interactive: false,
    }).bindTooltip(triangle.id, { permanent: true, direction: "center", className: "bg-white text-xs rounded" });
    idMarker.addTo(map);
    numberMarkersRef.current.set(trianglePath, idMarker);

    // Cleanup on unmount
    return () => {
      const l = triangleLayersRef.current.get(trianglePath);
      if (l && map.hasLayer(l)) map.removeLayer(l);
      triangleLayersRef.current.delete(trianglePath);

      const marker = numberMarkersRef.current.get(trianglePath);
      if (marker && map.hasLayer(marker)) map.removeLayer(marker);
      numberMarkersRef.current.delete(trianglePath);
    };
  // eslint-disable-next-line
  }, [
    map, triangle.id, triangle.vertices, triangle.color, triangle.emoji, triangle.clickCount, triangle.level, triangle.gametag, trianglePath,
    maxDivideLevel, clicksToDivide
  ]);
  return null;
}

