
import { useEffect, useRef, useState } from "react";
import {
  generateBaseTriangleMesh,
  getTriangleActivities,
  rebuildTriangleMeshFromActivities,
  TriangleMesh
} from "../../utils/triangleMesh";

export function useTriangleMeshLoader(worldSlug: string, meshVersion: string) {
  const [triangleMesh, setTriangleMesh] = useState<TriangleMesh[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let mounted = true;
    async function initializeMesh() {
      try {
        setIsLoading(true);
        const activities = await getTriangleActivities(worldSlug);
        if (activities.length > 0) {
          const restoredMesh = rebuildTriangleMeshFromActivities(activities);
          if (mounted) {
            setTriangleMesh(restoredMesh);
            console.log("[useTriangleMeshLoader] Loaded mesh from activities", restoredMesh.length, restoredMesh.slice(0,3));
          }
        } else {
          const initialMesh = generateBaseTriangleMesh();
          if (mounted) {
            setTriangleMesh(initialMesh);
            console.log("[useTriangleMeshLoader] Loaded canonical mesh from base", initialMesh.length, initialMesh.slice(0,3));
          }
        }
      } catch (error) {
        const initialMesh = generateBaseTriangleMesh();
        if (mounted) setTriangleMesh(initialMesh);
        console.error("[useTriangleMeshLoader] Error loading mesh activities, fallback to base:", error);
      } finally {
        if (mounted) setIsLoading(false);
      }
    }

    initializeMesh();

    pollIntervalRef.current = setInterval(async () => {
      try {
        const activities = await getTriangleActivities(worldSlug);
        const restoredMesh = rebuildTriangleMeshFromActivities(activities);
        if (mounted) setTriangleMesh(restoredMesh);
      } catch (error) {
        console.error("[useTriangleMeshLoader] Error polling activities:", error);
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
