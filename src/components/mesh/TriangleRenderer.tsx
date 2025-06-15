
import React from "react";
import L from "leaflet";
import { renderGeodesicTriangle } from "./renderGeodesicTriangle";
import { getTriangleMeshColor } from "../../utils/triangleMesh/color";
import type { TriangleMesh } from "../../utils/triangleMesh/geometry";

interface Props {
  map: L.Map;
  triangle: TriangleMesh;
  trianglePath: string;
  triangleLayersRef: React.MutableRefObject<Map<string, L.Polygon>>;
  numberMarkersRef: React.MutableRefObject<Map<string, L.Marker>>;
  onTriangleClick: (triangleId: string, triangle?: TriangleMesh, parentPath?: string) => void;
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
    // Remove any previous marker (shouldn't be any after last fixes)
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

    let polygon = null;
    try {
      if (!geodesicError && coordinates && Array.isArray(coordinates) && coordinates.length >= 3) {
        polygon = L.polygon(coordinates, {
          color: borderColor,
          weight,
          opacity: 1.0,
          fillColor,
          fillOpacity,
          smoothFactor: 1.0,
          interactive: true,
          className: "leaflet-interactive"
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
      // silent
    }

    // Cleanup on unmount/re-render
    return () => {
      const l = triangleLayersRef.current.get(trianglePath);
      if (l && map.hasLayer(l)) {
        map.removeLayer(l);
      }
      triangleLayersRef.current.delete(trianglePath);
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
