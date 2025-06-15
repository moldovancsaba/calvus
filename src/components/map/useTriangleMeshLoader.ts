import { useEffect, useRef, useState } from "react";
import {
  generateBaseTriangleMesh,
  getTriangleActivities,
  rebuildTriangleMeshFromActivities,
  TriangleMesh
} from "../../utils/triangleMesh";

// Always initializes and restores mesh from canonical mesh robustly, like /jusforfun
export function useTriangleMeshLoader(worldSlug: string, meshVersion: string) {
  // Always start with the canonical base mesh (like /jusforfun)
  const [triangleMesh, setTriangleMesh] = useState<TriangleMesh[]>(() => {
    const base = generateBaseTriangleMesh();
    if (!base || base.length !== 26) {
      console.error("[STRICT useTriangleMeshLoader] Initial base mesh is missing/corrupt!", base);
    }
    return base;
  });
  const [isLoading, setIsLoading] = useState(true);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Robustly enforces presence of mesh: if mesh goes empty/corrupt, fallback to canonical
  useEffect(() => {
    if (!Array.isArray(triangleMesh) || triangleMesh.length !== 26) {
      const base = generateBaseTriangleMesh();
      setTriangleMesh(base);
      console.warn("[STRICT useTriangleMeshLoader] Mesh was empty or corrupt—forced to canonical base mesh (26 triangles)");
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
          if (
            mounted &&
            Array.isArray(restoredMesh) &&
            restoredMesh.length === 26
          ) {
            setTriangleMesh(restoredMesh);
            console.log("[STRICT useTriangleMeshLoader] Loaded mesh from activities (26 triangles)");
          } else {
            // Corrupt or empty mesh, fallback
            const baseMesh = generateBaseTriangleMesh();
            setTriangleMesh(baseMesh);
            console.warn("[STRICT useTriangleMeshLoader] Fallback to canonical base mesh (26 triangles)", baseMesh);
          }
        } else {
          const initialMesh = generateBaseTriangleMesh();
          if (mounted) {
            setTriangleMesh(initialMesh);
            console.log("[STRICT useTriangleMeshLoader] Loaded canonical mesh from base (26 triangles)");
          }
        }
      } catch (error) {
        // Fallback: always show canonical mesh
        const initialMesh = generateBaseTriangleMesh();
        if (mounted) setTriangleMesh(initialMesh);
        console.error("[STRICT useTriangleMeshLoader] Error loading mesh activities—fallback to base:", error);
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
          console.warn("[STRICT useTriangleMeshLoader] Poll fallback to canonical base mesh (26 triangles)", restoredMesh);
        }
        if (restoredMesh.length === 26 && mounted) {
          setTriangleMesh(restoredMesh);
        }
      } catch (error) {
        // on polling error, keep the last mesh (do not clear)
        console.error("[STRICT useTriangleMeshLoader] Error polling activities:", error);
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
