
import { useCallback, useRef } from "react";
import { storeTriangleActivity, subdivideTriangleMesh } from "../../utils/triangleMesh";

// Helper to support tracking in-memory recently clicked per user/triangle.
const userTriangleClickStreak: Record<string, { triangleId: string, streak: number }> = {};

export function useTriangleMeshTap(
  identity: { gametag: string; color: string; emoji?: string } | null,
  setTriangleMesh: React.Dispatch<React.SetStateAction<any[]>>,
  isMobile: boolean,
  mapInstance: L.Map | null,
  worldSlug: string,
  settings?: { clicks_to_divide?: number, max_divide_level?: number, max_consecutive_clicks_per_user?: number }
) {
  const clicksToDivide = settings?.clicks_to_divide ?? 3;
  const maxDivideLevel = settings?.max_divide_level ?? 3;
  const maxConsecutiveClicks =
    settings?.max_consecutive_clicks_per_user && settings.max_consecutive_clicks_per_user > 0
      ? settings.max_consecutive_clicks_per_user
      : 1;

  // For basic toast UI, show a warning if restriction is hit:
  const shownRef = useRef<{ [k: string]: boolean }>({});

  return useCallback(
    async (
      triangleId: string,
      triangle: any,
      prevMeshRef: React.MutableRefObject<any[]>
    ) => {
      if (!identity) return;

      const isAtFinalLevel = triangle.level >= maxDivideLevel;
      const isFullyClaimed = isAtFinalLevel && triangle.clickCount >= clicksToDivide;

      // Block ALL users from interacting with a fully-claimed final triangle
      if (isFullyClaimed) return;

      // --- Enforce max consecutive clicks per user per triangle (client side memory) ---
      const userKey = `u:${identity.gametag}:${identity.color}`;
      const streakObj = userTriangleClickStreak[userKey] || { triangleId: "", streak: 0 };
      if (streakObj.triangleId === triangleId) {
        if (streakObj.streak >= maxConsecutiveClicks) {
          // Show toast if possible (checks for window.toast or window.lovableToast)
          if (typeof window !== "undefined" && !shownRef.current[triangleId]) {
            // Try shadcn/ui toast system
            // @ts-ignore
            if (window.toast) {
              // @ts-ignore
              window.toast(`You've reached the maximum consecutive clicks (${maxConsecutiveClicks}) allowed for this triangle.`, { variant: "destructive" });
            }
            shownRef.current[triangleId] = true;
            setTimeout(() => { shownRef.current[triangleId] = false; }, 1800);
          }
          return;
        }
        userTriangleClickStreak[userKey] = {
          triangleId,
          streak: streakObj.streak + 1
        };
      } else {
        // New triangle for user: reset streak
        userTriangleClickStreak[userKey] = { triangleId, streak: 1 };
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
                  emoji: identity.emoji, // Store emoji of current user
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
                  emoji: identity.emoji, // Store emoji on claim
                };
              }
              // regular increment/color change
              return {
                ...triangleEl,
                clickCount: newClickCount,
                color: identity.color,
                gametag: identity.gametag,
                emoji: identity.emoji, // Always update emoji on click
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
          identity.emoji, // Pass emoji to store function if supported
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
    [identity, isMobile, mapInstance, setTriangleMesh, worldSlug, clicksToDivide, maxDivideLevel, maxConsecutiveClicks]
  );
}
