
import L from "leaflet";
import React from "react";
import { TriangleRenderer } from "./TriangleRenderer";
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
  maxDivideLevel?: number;
  clicksToDivide?: number;
};

export function TriangleMeshRenderer({
  map,
  triangleMesh,
  triangleLayersRef,
  onTriangleClick,
  maxDivideLevel = 3,
  clicksToDivide = 3,
}: Props) {
  const numberMarkersRef = React.useRef<Map<string, L.Marker>>(new Map());

  // Always pass an array (empty allowed)
  const safeTriangles: TriangleMesh[] = Array.isArray(triangleMesh) ? triangleMesh : [];

  React.useEffect(() => {
    // DEBUG
    console.log("[TRIANGLE_MESH][MOUNT] triangleMesh length:", triangleMesh?.length, triangleMesh);
    if (triangleMesh?.length > 0) {
      console.log("[TRIANGLE_SAMPLE]", triangleMesh[0]);
    }
    // --- VISUAL DEBUGGING ---
    if (map) {
      // Confirm map and container
      console.log("[DEBUG] Leaflet map instance at mount:", map);
      const container = map.getContainer();
      console.log("[DEBUG] Leaflet map container:", container);

      // Set border/background on container
      container.style.border = "3px solid red";
      container.style.backgroundColor = "#fffbe7";

      // Try to add a debug marker at 0,0 with popup
      try {
        const debugMarker = L.marker([0,0], { title: "Debug Origin Marker" })
          .bindPopup("DEBUG MARKER (0,0)")
          .addTo(map);
        numberMarkersRef.current.set("__debug_marker", debugMarker);
        console.log("[DEBUG] Added marker (0,0):", debugMarker, debugMarker._leaflet_id);
      } catch (e) {
        console.error("[DEBUG] FAILED to add marker (0,0):", e);
      }

      // Try to add a test polygon (blue triangle) with popup
      const testCoords: [number, number][] = [
        [20, -20],
        [60, 0],
        [20, 20],
        [20, -20]
      ];
      try {
        const testPolygon = L.polygon(testCoords, {
          color: "#0074D9",
          weight: 4,
          opacity: 1.0,
          fillColor: "#0074D9",
          fillOpacity: 0.3,
          dashArray: "10,5"
        }).bindPopup("DEBUG TRIANGLE")
        .addTo(map);
        numberMarkersRef.current.set("__test_polygon", testPolygon as any);
        console.log("[DEBUG] Added test polygon, Leaflet ID:", (testPolygon as any)._leaflet_id, testPolygon.getLatLngs());
        // Fit bounds to show it
        map.fitBounds(L.latLngBounds(testCoords), { padding: [50,50], animate: false });
      } catch (e) {
        console.error("[DEBUG] FAILED to add test blue polygon:", e);
      }

      // Log all layer IDs after
      const allLayers = Object.values((map as any)._layers || {});
      const polyCount = allLayers.filter((l) => l instanceof L.Polygon).length;
      console.info(`[DEBUG - after mount] Leaflet map has ${polyCount} polygons. Layer IDs:`, allLayers.map((l: any) => l._leaflet_id));
    }

    // Cleanup debug marker and test poly
    return () => {
      const marker = numberMarkersRef.current.get("__debug_marker");
      if (marker && map && map.hasLayer(marker)) map.removeLayer(marker);
      numberMarkersRef.current.delete("__debug_marker");
      const testPoly = numberMarkersRef.current.get("__test_polygon");
      if (testPoly && map && map.hasLayer(testPoly)) map.removeLayer(testPoly);
      numberMarkersRef.current.delete("__test_polygon");
      // Unstyle
      if (map) {
        const container = map.getContainer();
        container.style.border = "";
        container.style.backgroundColor = "";
      }
    };
    // eslint-disable-next-line
  }, [map]);

  // Defensive recursive render
  const renderTriangles = React.useCallback(
    (list: TriangleMesh[], parentPath = "") => {
      if (!Array.isArray(list) || !list.length) return null;
      const out: React.ReactNode[] = [];
      for (const triangle of list) {
        const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
        // Polygon vertex safety check
        if (!Array.isArray(triangle.vertices) || triangle.vertices.length !== 3) {
          console.warn(`[TriangleMeshRenderer] Triangle ${triangle.id} has invalid vertices:`, triangle.vertices);
          continue;
        }
        let invalid = false;
        triangle.vertices.forEach((v, idx) => {
          if (!v || typeof v.lat !== "number" || typeof v.lng !== "number" || isNaN(v.lat) || isNaN(v.lng)) {
            invalid = true;
            console.error(`[TriangleMeshRenderer] Triangle ${triangle.id} vertex ${idx} is invalid:`, v);
          }
        });
        if (invalid) {
          continue;
        }
        console.log("[TriangleMeshRenderer] Will render TriangleRenderer for", triangle?.id, trianglePath, triangle.vertices);
        if (Array.isArray(triangle.vertices)) {
          console.log(
            `[TriangleMeshRenderer] Vertices for ${triangle.id}:`,
            triangle.vertices.map((v, idx) => `(${idx}: lat=${v.lat}, lng=${v.lng})`).join("; ")
          );
        }
        if (!triangle.subdivided) {
          out.push(
            <TriangleRenderer
              key={trianglePath}
              map={map!}
              triangle={triangle}
              trianglePath={trianglePath}
              triangleLayersRef={triangleLayersRef}
              numberMarkersRef={numberMarkersRef}
              onTriangleClick={onTriangleClick}
              maxDivideLevel={maxDivideLevel}
              clicksToDivide={clicksToDivide}
            />
          );
        } else if (triangle.children) {
          const childNodes = renderTriangles(triangle.children, trianglePath);
          if (childNodes) {
            if (Array.isArray(childNodes)) {
              out.push(...childNodes);
            } else {
              out.push(childNodes);
            }
          }
        }
      }
      const filteredOut = out.filter(Boolean);
      console.log("[TriangleMeshRenderer] renderTriangles output count:", filteredOut.length, "props.triangleMesh count:", list.length, "sample:", list.slice(0,3));
      return filteredOut.length > 0 ? filteredOut : null;
    },
    [
      map,
      triangleLayersRef,
      onTriangleClick,
      maxDivideLevel,
      clicksToDivide,
    ]
  );

  if (!map) {
    console.log("[TriangleMeshRenderer] No map instance supplied.");
    return null;
  }
  const container = map.getContainer?.();
  if (!container || !container.parentNode) {
    console.log("[TriangleMeshRenderer] Map container not found or not attached to DOM");
    return null;
  }

  React.useEffect(() => {
    if (safeTriangles.length === 0) return;
    triangleLayersRef.current.forEach(layer => {
      if (map.hasLayer(layer)) map.removeLayer(layer);
    });
    triangleLayersRef.current.clear();
    numberMarkersRef.current.forEach((marker) => {
      if (map.hasLayer(marker)) map.removeLayer(marker);
    });
    numberMarkersRef.current.clear();
  }, [map, triangleLayersRef, safeTriangles.length]); // Remove direct triangleMesh dependency

  React.useEffect(() => {
    console.log("[TriangleMeshRenderer] triangleMesh prop:", triangleMesh);
    console.log("[TriangleMeshRenderer] map instance:", map);
    if (map) {
      const allLayers = Object.values((map as any)._layers || {});
      const polyCount = allLayers.filter((l) => l instanceof L.Polygon).length;
      const polyIds = allLayers
        .filter((l): l is { _leaflet_id: number } => typeof l === "object" && l !== null && "_leaflet_id" in l)
        .map((l) => (l as any)._leaflet_id);
      console.log(`[TriangleMeshRenderer] (Effect) Leaflet map has ${polyCount} polygons. Layer IDs:`, polyIds);
    }
  }, [triangleMesh, map]);

  React.useEffect(() => {
    console.log("[TriangleMeshRenderer] MOUNTED, triangleMesh length:", triangleMesh?.length, "Sample:", triangleMesh?.slice(0,2));
  }, []);

  const output = renderTriangles(safeTriangles);

  if (!output) return null;
  return <>{output}</>;
}
