
import { generateBaseTriangleMesh, subdivideTriangleMesh, TriangleMesh } from "./geometry";

/**
 * Aggregate all triangle activities to a simple per-triangle map.
 * Only accepts activities with a valid `where` (triangle id).
 */
function aggregateTriangleActivities(activities: any[]): Record<string, { clickCount: number, mostRecent: any }> {
  const result: Record<string, { clickCount: number, mostRecent: any }> = {};
  for (const row of activities) {
    const id = row?.where;
    if (!id) continue;
    const delta = typeof row.click_count === "number"
      ? row.click_count
      : typeof row.what === "number"
        ? row.what
        : 1;
    if (!result[id]) {
      result[id] = { clickCount: delta, mostRecent: row };
    } else {
      result[id].clickCount += delta;
      // Use most recent activity for identity/color fields
      if (!result[id].mostRecent || (row.timestamp && row.timestamp > result[id].mostRecent.timestamp)) {
        result[id].mostRecent = row;
      }
    }
  }
  return result;
}

/**
 * PURE, DETERMINISTIC: Rebuild the mesh from scratch using activities only.
 * Always starts from canonical mesh, applies clicks and subdivides "fresh".
 */
export function rebuildTriangleMeshFromActivities(
  activities: any[],
  settings?: { clicks_to_divide?: number, max_divide_level?: number }
): TriangleMesh[] {
  const baseMesh = generateBaseTriangleMesh();
  if (!activities || !Array.isArray(activities) || activities.length === 0) return baseMesh;

  const activityMap = aggregateTriangleActivities(activities);
  const clicksToDivide = settings?.clicks_to_divide ?? 3;
  const maxDivideLevel = settings?.max_divide_level ?? 3;

  function recursivelyApplyActivities(triangle: TriangleMesh): TriangleMesh {
    const activity = activityMap[triangle.id];
    const clickCount = activity?.clickCount ?? triangle.clickCount ?? 0;
    const latest = activity?.mostRecent;
    const color = latest?.color ?? triangle.color;
    const gametag = latest?.gametag ?? triangle.gametag;
    const emoji = latest?.emoji ?? triangle.emoji;

    // Only subdivide IF not at max level and clickCount >= threshold
    let children: TriangleMesh[] | undefined = undefined;
    let subdivided = triangle.subdivided;
    if (clickCount >= clicksToDivide && triangle.level < maxDivideLevel) {
      subdivided = true;
      // Recursively apply activities to each child
      children = subdivideTriangleMesh(triangle).map(child => recursivelyApplyActivities(child));
    }

    return {
      ...triangle,
      clickCount,
      color,
      gametag,
      emoji,
      subdivided: subdivided ?? false,
      ...(children ? { children } : {})
    };
  }

  // Fully pure: reconstruct from scratch for every triangle
  const rebuilt = baseMesh.map(triangle => recursivelyApplyActivities(triangle));
  if (typeof window !== "undefined") {
    console.log("[rebuildTriangleMeshFromActivities] PURE REBUILD, triangle count:", rebuilt.length, rebuilt.slice(0,2));
  }
  return rebuilt;
}
