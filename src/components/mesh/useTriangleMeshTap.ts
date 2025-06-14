
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
      // ENFORCE FINALITY: if triangle at max level, block further interaction!
      if (triangle.level >= maxDivideLevel) return;

      if (triangle?.gametag && triangle.gametag === identity.gametag && triangle.color === identity.color) {
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
          (triangle?.clickCount ?? 0) + 1 === clicksToDivide && (triangle?.level ?? 0) < maxDivideLevel
            ? "subdivide"
            : "click";
        const result = await storeTriangleActivity(
          triangleId,
          (triangle?.clickCount ?? 0) + 1,
          triangle?.level ?? 0,
          Boolean(
            ((triangle?.clickCount ?? 0) + 1 === clicksToDivide) &&
            (triangle?.level ?? 0) < maxDivideLevel
          ),
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
