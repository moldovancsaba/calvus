import React from "react";
import L from "leaflet";
import { renderGeodesicTriangle } from "./renderGeodesicTriangle";
import { getTriangleMeshColor } from "../../utils/triangleMesh/color";

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

// Utility: centroid for marker (still used internally but not for marker rendering)
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
    // Remove previous layer and marker
    const prevLayer = triangleLayersRef.current.get(trianglePath);
    if (prevLayer) {
      map.removeLayer(prevLayer);
    }
    const prevMarker = numberMarkersRef.current.get(trianglePath);
    if (prevMarker) map.removeLayer(prevMarker);

    // Create polygon styled by the real triangle's color logic
    let coordinates: [number, number][] = [];
    let geodesicError = null;
    try {
      coordinates = renderGeodesicTriangle(triangle.vertices);
    } catch (e) {
      geodesicError = e;
    }

    // Use actual game color logic for styling
    let fillColor = getTriangleMeshColor(triangle);
    let borderColor = "#222";
    let fillOpacity = 0.93;
    let weight = 2;

    let err = null;
    let polygon = null;
    try {
      if (!geodesicError && coordinates && Array.isArray(coordinates) && coordinates.length >= 3) {
        polygon = L.polygon(coordinates, {
          color: borderColor,
          weight,
          opacity: 1.0,
          fillColor: fillColor,
          fillOpacity: fillOpacity,
          smoothFactor: 1.0,
          interactive: true,
          className: "leaflet-interactive",
        });
        polygon.on("pointerdown", () =>
          onTriangleClick(triangle.id, triangle, trianglePath)
        );
        polygon.on("click", () =>
          onTriangleClick(triangle.id, triangle, trianglePath)
        );
        polygon.on("touchstart", () =>
          onTriangleClick(triangle.id, triangle, trianglePath)
        );
        polygon.addTo(map);
        triangleLayersRef.current.set(trianglePath, polygon);
      }
    } catch (e) {
      err = e;
    }

    // REMOVED: All centroid marker/pin/tooltips/ID rendering

    // Cleanup on unmount/re-render
    return () => {
      const l = triangleLayersRef.current.get(trianglePath);
      if (l && map.hasLayer(l)) {
        map.removeLayer(l);
      }
      triangleLayersRef.current.delete(trianglePath);
      // NO marker cleanup needed; not added
      const marker = numberMarkersRef.current.get(trianglePath);
      if (marker && map.hasLayer(marker)) map.removeLayer(marker);
      numberMarkersRef.current.delete(trianglePath);
    };
    // eslint-disable-next-line
  }, [
    map,
    triangle.id,
    triangle.vertices,
    triangle.color,
    triangle.emoji,
    triangle.clickCount,
    triangle.level,
    triangle.gametag,
    trianglePath,
    maxDivideLevel,
    clicksToDivide,
  ]);
  return null;
}
