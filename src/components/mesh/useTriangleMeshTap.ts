import { useCallback } from "react";
import { storeTriangleActivity, subdivideTriangleMesh } from "../../utils/triangleMesh";

export function useTriangleMeshTap(
  identity: { gametag: string; color: string } | null,
  setTriangleMesh: React.Dispatch<React.SetStateAction<any[]>>,
  isMobile: boolean,
  mapInstance: L.Map | null,
  worldSlug: string,
  settings?: { clicks_to_divide?: number, max_divide_level?: number }
) {
  const clicksToDivide = settings?.clicks_to_divide ?? 3;
  const maxDivideLevel = settings?.max_divide_level ?? 3;

  return useCallback(
    async (
      triangleId: string,
      triangle: any,
      prevMeshRef: React.MutableRefObject<any[]>
    ) => {
      if (!identity) return;

      const isAtFinalLevel = triangle.level >= maxDivideLevel;
      const isFullyClaimed = isAtFinalLevel && triangle.clickCount >= clicksToDivide;

      // NEW: Block ALL users from interacting with a fully-claimed final triangle
      if (isFullyClaimed) {
        // Triangle is at the final level and has been fully claimed, no further update allowed
        return;
      }

      setTriangleMesh(currMesh => {
        let prevMesh = currMesh;
        prevMeshRef.current = currMesh;
        const updateTriangle = (triangles: any[]): any[] =>
          triangles.map(triangleEl => {
            if (triangleEl.id === triangleId) {
              const newClickCount = triangleEl.clickCount + 1;
              // -- Final level logic: just color/owner/finalize, NO subdivide
              if (triangleEl.level >= maxDivideLevel) {
                return {
                  ...triangleEl,
                  clickCount: Math.min(newClickCount, clicksToDivide),
                  color: identity.color,
                  gametag: identity.gametag,
                };
              }
              // regular subdivide if needed
              if (newClickCount === clicksToDivide && triangleEl.level < maxDivideLevel && !triangleEl.subdivided) {
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
              // regular increment/color change
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
        // Update: make sure "subdivide" never triggers on last level
        let actionType: string = "click";
        let willSubdivide = false;
        if (
          (triangle?.clickCount ?? 0) + 1 === clicksToDivide &&
          triangle?.level < maxDivideLevel
        ) {
          actionType = "subdivide";
          willSubdivide = true;
        }
        const result = await storeTriangleActivity(
          triangleId,
          Math.min((triangle?.clickCount ?? 0) + 1, clicksToDivide),
          triangle?.level ?? 0,
          willSubdivide,
          actionType,
          identity.gametag,
          identity.color,
          undefined,
          worldSlug
        );
        if (!result?.success) {
          throw new Error("No success response from storeTriangleActivity");
        }
        storeSuccess = true;
      } catch (err: any) {
        storeSuccess = false;
        setTriangleMesh(prev => prevMeshRef.current);
      }

      // -- existing mobile move-to-triangle logic unchanged --
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
    [identity, isMobile, mapInstance, setTriangleMesh, worldSlug, clicksToDivide, maxDivideLevel]
  );
}
