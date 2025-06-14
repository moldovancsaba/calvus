import { generateBaseTriangleMesh, subdivideTriangleMesh, TriangleMesh } from "./geometry";

// Utility to aggregate activity rows per triangle: [id]: { totalClicks, gametag, color, mostRecentActivity }
function aggregateTriangleActivity(activities: any[]) {
  const clickMap = new Map<string, { clickCount: number; latest: any | null }>();
  for (const act of activities) {
    if (!act || typeof act.where !== "string") continue;
    const id = act.where;
    const count = typeof act.click_count === "number"
      ? act.click_count
      : typeof act.what === "number"
        ? act.what
        : 1;

    // If the triangle already exists in map, sum the count, keep latest row
    if (!clickMap.has(id)) {
      clickMap.set(id, { clickCount: count, latest: act });
    } else {
      const prev = clickMap.get(id)!;
      clickMap.set(id, {
        clickCount: prev.clickCount + count,
        latest: (prev.latest.timestamp > act.timestamp) ? prev.latest : act
      });
    }
  }
  return clickMap;
}

// Rebuild triangle mesh from stored activities aggregating SUM(click) per triangle
export function rebuildTriangleMeshFromActivities(activities: any[]): TriangleMesh[] {
  // Use base mesh to start
  const baseMesh = generateBaseTriangleMesh();
  if (!Array.isArray(activities) || activities.length === 0) return baseMesh;

  // Aggregate all activity rows per triangle
  const activityMap = aggregateTriangleActivity(activities);

  // Recursively apply stored state to the mesh
  function applyStatesToMesh(triangles: TriangleMesh[]): TriangleMesh[] {
    return triangles.map(triangle => {
      // Get aggregate record for this triangle if any
      const activityAgg = activityMap.get(triangle.id);
      let clickCount = activityAgg?.clickCount ?? triangle.clickCount ?? 0;
      let gametag = activityAgg?.latest?.gametag ?? triangle.gametag;
      let color = activityAgg?.latest?.color ?? triangle.color;
      let lastActivity = activityAgg?.latest;

      let updated: TriangleMesh = {
        ...triangle,
        clickCount,
        gametag,
        color,
      };

      // Determine subdivision status using SUM(clicks) like previously
      const isSubdivided = !!lastActivity?.subdivided || clickCount >= 11;
      if (isSubdivided && triangle.level < 19) {
        // If not yet subdivided, or offspring not present, populate children
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
  console.log("[rebuildTriangleMeshFromActivities] mesh rebuilt using SUM of click activity", rebuiltMesh);
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
