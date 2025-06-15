import { useEffect, useRef, useState } from "react";
import {
  generateBaseTriangleMesh,
  getTriangleActivities,
  rebuildTriangleMeshFromActivities,
  TriangleMesh
} from "../../utils/triangleMesh";

// Fix: ALWAYS initialize and restore game mesh from the canonical BASE mesh if failed
export function useTriangleMeshLoader(worldSlug: string, meshVersion: string) {
  const [triangleMesh, setTriangleMesh] = useState<TriangleMesh[]>(() => {
    // Always start with the canonical base mesh
    const base = generateBaseTriangleMesh();
    if (!base || base.length !== 26) {
      console.error("[FIXED useTriangleMeshLoader] Initial base mesh missing/corrupt! Should be 26 triangles.", base);
    }
    return base;
  });
  const [isLoading, setIsLoading] = useState(true);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Defensive effect: always re-assert mesh is non-empty
  useEffect(() => {
    if (!Array.isArray(triangleMesh) || triangleMesh.length === 0) {
      // Always reset to canonical base mesh
      const base = generateBaseTriangleMesh();
      setTriangleMesh(base);
      console.warn("[FIXED useTriangleMeshLoader] Fallback: mesh was empty, forced base mesh (26 triangles)");
    }
  }, [triangleMesh]);

  useEffect(() => {
    let mounted = true;
    async function initializeMesh() {
      try {
        setIsLoading(true);
        const activities = await getTriangleActivities(worldSlug);
        if (activities.length > 0) {
          const restoredMesh = rebuildTriangleMeshFromActivities(activities);
          if (mounted && Array.isArray(restoredMesh) && restoredMesh.length > 0) {
            // Always ensure canonical mesh (26)
            if (restoredMesh.length === 26) {
              setTriangleMesh(restoredMesh);
              console.log("[FIXED useTriangleMeshLoader] Loaded mesh from activities", restoredMesh.length);
            } else {
              // Corrupt mesh, fallback
              const baseMesh = generateBaseTriangleMesh();
              setTriangleMesh(baseMesh);
              console.warn("[FIXED useTriangleMeshLoader] Fallback to canonical base mesh (26 triangles):", baseMesh);
            }
          } else {
            // Defensive fallback
            const baseMesh = generateBaseTriangleMesh();
            setTriangleMesh(baseMesh);
            console.warn("[FIXED useTriangleMeshLoader] Restored mesh empty, fallback to base mesh");
          }
        } else {
          const initialMesh = generateBaseTriangleMesh();
          if (mounted) {
            setTriangleMesh(initialMesh);
            console.log("[FIXED useTriangleMeshLoader] Loaded canonical mesh from base", initialMesh.length);
          }
        }
      } catch (error) {
        // Fallback: canonical mesh (26)
        const initialMesh = generateBaseTriangleMesh();
        if (mounted) setTriangleMesh(initialMesh);
        console.error("[FIXED useTriangleMeshLoader] Error loading mesh activities, fallback to base:", error);
      } finally {
        if (mounted) setIsLoading(false);
      }
    }

    initializeMesh();

    pollIntervalRef.current = setInterval(async () => {
      try {
        const activities = await getTriangleActivities(worldSlug);
        let restoredMesh = rebuildTriangleMeshFromActivities(activities);
        if (!Array.isArray(restoredMesh) || restoredMesh.length !== 26) {
          restoredMesh = generateBaseTriangleMesh();
          console.warn("[FIXED useTriangleMeshLoader] Poll fallback to canonical base mesh (26 triangles):", restoredMesh);
        }
        if (restoredMesh.length > 0 && mounted) {
          setTriangleMesh(restoredMesh);
        }
      } catch (error) {
        // on polling error, keep last mesh
        console.error("[FIXED useTriangleMeshLoader] Error polling activities:", error);
      }
    }, 5000);

    return () => {
      mounted = false;
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, [worldSlug, meshVersion]);

  return { triangleMesh, setTriangleMesh, isLoading };
}
