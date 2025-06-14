
import { useCallback } from "react";
import { storeTriangleActivity, subdivideTriangleMesh } from "../../utils/triangleMesh";
import { toast } from "../ui/use-toast";

/**
 * Add worldSlug argument: all activity is scoped to a world.
 */
export function useTriangleMeshTap(
  identity: { gametag: string; color: string } | null,
  setTriangleMesh: React.Dispatch<React.SetStateAction<any[]>>,
  isMobile: boolean,
  mapInstance: L.Map | null,
  worldSlug: string
) {
  return useCallback(
    async (
      triangleId: string,
      triangle: any,
      prevMeshRef: React.MutableRefObject<any[]>
    ) => {
      if (!identity) return;

      // --- ENFORCE CLICKABILITY ---
      if (triangle?.gametag && triangle.gametag === identity.gametag && triangle.color === identity.color) {
        toast({
          title: "Try another triangle!",
          description: "You can't click repeatedly on your own triangle. Try a triangle claimed by another gamer or a new one.",
          variant: "destructive",
        });
        return;
      }

      let prevMesh: any[] = [];
      setTriangleMesh(currMesh => {
        prevMesh = currMesh;
        prevMeshRef.current = currMesh;
        const updateTriangle = (triangles: any[]): any[] =>
          triangles.map(triangleEl => {
            if (triangleEl.id === triangleId) {
              const newClickCount = triangleEl.clickCount + 1;
              if (newClickCount === 11 && triangleEl.level < 19 && !triangleEl.subdivided) {
                const children = subdivideTriangleMesh(triangleEl);
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
        const actionType =
          (triangle?.clickCount ?? 0) + 1 === 11 && (triangle?.level ?? 0) < 19
            ? "subdivide"
            : "click";
        const result = await storeTriangleActivity(
          triangleId,
          (triangle?.clickCount ?? 0) + 1,
          triangle?.level ?? 0,
          Boolean(
            ((triangle?.clickCount ?? 0) + 1 === 11) &&
            (triangle?.level ?? 0) < 19
          ),
          actionType,
          identity.gametag,
          identity.color,
          undefined,
          worldSlug // SCOPED
        );
        if (!result?.success) {
          throw new Error("No success response from storeTriangleActivity");
        }
        storeSuccess = true;
        toast({
          title: "Activity Saved!",
          description: "Your triangle tap activity was recorded.",
          variant: "default",
        });
      } catch (err: any) {
        storeSuccess = false;
        toast({
          title: "Failed to save activity",
          description:
            "Could not save tap to server. Please check your connection.",
          variant: "destructive",
        });
        setTriangleMesh(prev => prevMeshRef.current);
      }

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
    [identity, isMobile, mapInstance, setTriangleMesh, worldSlug]
  );
}
