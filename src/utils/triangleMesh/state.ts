import { generateBaseTriangleMesh, subdivideTriangleMesh, TriangleMesh } from "./geometry";

// Rebuild triangle mesh from stored activities representing full triangle state
export function rebuildTriangleMeshFromActivities(activities: any[]): TriangleMesh[] {
  // Use base mesh to start
  const baseMesh = generateBaseTriangleMesh();
  if (!Array.isArray(activities) || activities.length === 0) return baseMesh;

  // Use a map { id: activityRow } for quick update
  const stateMap = new Map<string, any>();
  activities.forEach(act => {
    // always keep the latest activity for any triangle id
    stateMap.set(act.where, act);
  });

  // Recursively apply stored state to the mesh
  function applyStatesToMesh(triangles: TriangleMesh[]): TriangleMesh[] {
    return triangles.map(triangle => {
      // Get record for this triangle if any
      const activity = stateMap.get(triangle.id);

      let updated: TriangleMesh = {
        ...triangle,
        clickCount: activity?.click_count ?? triangle.clickCount ?? 0,
        gametag: activity?.gametag ?? triangle.gametag,
        color: activity?.color ?? triangle.color,
      };

      // Determine subdivision status using db/subdivided and clicks
      const isSubdivided = !!activity?.subdivided || updated.clickCount >= 11;
      if (isSubdivided && (triangle.level < 19)) {
        // If not yet subdivided, or offspring not present, populate
        if (!triangle.subdivided || !triangle.children) {
          updated = {
            ...updated,
            subdivided: true,
            children: subdivideTriangleMesh(triangle),
          };
        }
        if (updated.children) {
          // recursively update children if present in state
          updated = {
            ...updated,
            children: applyStatesToMesh(updated.children),
          };
        }
        return updated;
      }

      // If triangle is subdivided but does not have children, that's a data error - keep empty children.
      if (activity?.subdivided && !updated.children) {
        updated = {
          ...updated,
          children: [],
        };
      }

      // Recursively update children (should not be subdivided unless flagged)
      if (triangle.children) {
        updated = {
          ...updated,
          children: applyStatesToMesh(triangle.children),
        };
      }

      return updated;
    });
  }

  const rebuiltMesh = applyStatesToMesh(baseMesh);
  // Log for debug
  console.log("[rebuildTriangleMeshFromActivities] Rebuilt mesh from activities", rebuiltMesh);
  return rebuiltMesh;
}

// Apply a single activity to the mesh, INCLUDING color and gametag restore
function applyActivityToMesh(mesh: TriangleMesh[], activity: any): TriangleMesh[] {
  return updateTriangleInMesh(
    mesh,
    activity.where,
    activity.what,
    activity.level,
    activity.gametag,
    activity.color
  );
}

// Update a specific triangle in the mesh & add identity fields
function updateTriangleInMesh(
  triangles: TriangleMesh[],
  triangleId: string,
  clickCount: number,
  level: number,
  gametag?: string | null,
  color?: string | null
): TriangleMesh[] {
  return triangles.map(triangle => {
    if (triangle.id === triangleId) {
      const updatedTriangle = {
        ...triangle,
        clickCount: clickCount,
        gametag: gametag ?? triangle.gametag,
        color: color ?? triangle.color,
      };

      if (clickCount === 11 && triangle.level < 19 && !triangle.subdivided) {
        // Subdivide if not yet subdivided and at correct clickCount
        const children = subdivideTriangleMesh(triangle);
        console.log("[updateTriangleInMesh] Subdividing triangle!", triangle.id, triangle.level);
        return {
          ...updatedTriangle,
          subdivided: true,
          children
        };
      }

      return updatedTriangle;
    }

    if (triangle.children) {
      return {
        ...triangle,
        children: updateTriangleInMesh(triangle.children, triangleId, clickCount, level, gametag, color)
      };
    }

    return triangle;
  });
}
