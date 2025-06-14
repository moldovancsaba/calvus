
import { useCallback } from "react";
import { storeTriangleActivity, subdivideTriangleMesh } from "../../utils/triangleMesh";
import { toast } from "../ui/use-toast";

/**
 * This hook provides a robust handler function for triangle taps/clicks.
 * It ensures DB writes are awaited, handles errors, and reverts local state on failure.
 */
export function useTriangleMeshTap(
  identity: { gametag: string; color: string } | null,
  setTriangleMesh: React.Dispatch<React.SetStateAction<any[]>>,
  isMobile: boolean,
  mapInstance: L.Map | null
) {
  return useCallback(
    async (
      triangleId: string,
      triangle: any,
      prevMeshRef: React.MutableRefObject<any[]>
    ) => {
      if (!identity) return;

      let prevMesh: any[] = [];
      setTriangleMesh(currMesh => {
        prevMesh = currMesh;
        prevMeshRef.current = currMesh;
        // Local UI update (optimistic)
        const updateTriangle = (triangles: any[]): any[] =>
          triangles.map(triangleEl => {
            if (triangleEl.id === triangleId) {
              const newClickCount = triangleEl.clickCount + 1;
              if (newClickCount === 11 && triangleEl.level < 19 && !triangleEl.subdivided) {
                // Always subdivide when reaching 11 clicks and not at max level
                const children = subdivideTriangleMesh(triangleEl);
                console.log("[useTriangleMeshTap] Subdividing locally with new children", triangleEl.id, triangleEl.level);
                return {
                  ...triangleEl,
                  clickCount: newClickCount,
                  subdivided: true,
                  children,
                  color: identity.color,
                  gametag: identity.gametag,
                };
              }
              return {
                ...triangleEl,
                clickCount: newClickCount,
                color: identity.color,
                gametag: identity.gametag,
              };
            }
            if (triangleEl.children) {
              return {
                ...triangleEl,
                children: updateTriangle(triangleEl.children),
              };
            }
            return triangleEl;
          });
        return updateTriangle(currMesh);
      });

      let storeSuccess = false;
      try {
        console.log("[useTriangleMeshTap] Store activity:", triangleId, (triangle?.clickCount ?? 0) + 1);
        await storeTriangleActivity(
          triangleId,
          (triangle?.clickCount ?? 0) + 1,
          triangle?.level ?? 0,
          identity.gametag,
          identity.color
        );
        storeSuccess = true;
        console.log("[useTriangleMeshTap] Store success!");
      } catch (err: any) {
        storeSuccess = false;
        console.error("[useTriangleMeshTap] Store failed:", err);
        toast({
          title: "Failed to save activity",
          description:
            "Could not save tap to server. Please check your connection.",
          variant: "destructive",
        });
        setTriangleMesh(prev => prevMeshRef.current);
      }

      // Mobile: zoom to triangle if successful
      if (
        storeSuccess &&
        isMobile &&
        mapInstance &&
        triangle &&
        Array.isArray(triangle.vertices)
      ) {
        const avgLat =
          (triangle.vertices[0].lat +
            triangle.vertices[1].lat +
            triangle.vertices[2].lat) /
          3;
        const avgLng =
          (triangle.vertices[0].lng +
            triangle.vertices[1].lng +
            triangle.vertices[2].lng) /
          3;
        const zoomLevel = mapInstance.getZoom();
        if (zoomLevel < 8) {
          mapInstance.flyTo([avgLat, avgLng], 8, {
            animate: true,
            duration: 0.9,
          });
        }
      }
    },
    [identity, isMobile, mapInstance, setTriangleMesh]
  );
}

