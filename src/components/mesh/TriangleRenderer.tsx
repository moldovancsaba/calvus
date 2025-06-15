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

// Utility: random bright color by id (hash)
function randomBrightColorById(str: string): string {
  // Use a hash to generate distinct and high-contrast colors per triangle.
  let hash = 0;
  for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
  const h = (hash % 360 + 360) % 360;
  return `hsl(${h}, 94%, 56%)`;
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
    // Add heavy debug for vertex validity
    if (!triangle || !triangle.vertices || triangle.vertices.length !== 3) {
      console.error("[DEBUG TriangleRenderer] Invalid triangle or vertices", triangle);
    }
    triangle.vertices.forEach((v, i) => {
      if (typeof v.lat !== "number" || typeof v.lng !== "number" || isNaN(v.lat) || isNaN(v.lng)) {
        console.error(`[DEBUG TriangleRenderer] Triangle ${triangle.id} vertex ${i} invalid:`, v);
      }
    });

    // Remove previous layer and marker
    const prevLayer = triangleLayersRef.current.get(trianglePath);
    if (prevLayer) map.removeLayer(prevLayer);
    const prevMarker = numberMarkersRef.current.get(trianglePath);
    if (prevMarker) map.removeLayer(prevMarker);

    // Create polygon with bold, colored outline and highly visible fill
    const coordinates = renderGeodesicTriangle(triangle.vertices);
    // For debug, use fully opaque fill and outline
    const fill = "#ff00dd"; // magenta for max visibility
    const polygon = L.polygon(coordinates, {
      color: "#000",          // black outline for debug
      weight: 5,
      opacity: 1.0,
      fillColor: fill,
      fillOpacity: 0.85,      // almost fully opaque for debug
      smoothFactor: 1.0,
      interactive: true,
      className: "leaflet-interactive"
    });

    polygon.on("pointerdown", () => onTriangleClick(triangle.id, triangle, trianglePath));
    polygon.on("click", () => onTriangleClick(triangle.id, triangle, trianglePath));
    polygon.on("touchstart", () => onTriangleClick(triangle.id, triangle, trianglePath));
    polygon.addTo(map);
    triangleLayersRef.current.set(trianglePath, polygon);

    // Add marker and always-visible tooltip at centroid
    const [cLat, cLng] = centroid(triangle.vertices);
    const idMarker = L.marker([cLat, cLng], {
      title: triangle.id,
      keyboard: false,
      opacity: 0.88,
      interactive: false
    }).bindTooltip(`<b>${triangle.id}</b>`, { permanent: true, direction: "center", className: "bg-white text-xs rounded shadow-lg" });
    idMarker.addTo(map);
    numberMarkersRef.current.set(trianglePath, idMarker);

    // Cleanup
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
