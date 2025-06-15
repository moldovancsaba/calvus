
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
 * Deterministically rebuilds the full triangle mesh for rendering using ACTIVITIES array and world settings.
 * This function is PURE and does not mutate the canonical base mesh.
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

  /**
   * Recursive helper: applies click count/activity recursively, subdivides if needed.
   */
  function applyActivities(meshList: TriangleMesh[], currentLevel = 0): TriangleMesh[] {
    return meshList.map(baseTri => {
      const activity = activityMap[baseTri.id];
      // Use clickCount and owner/color/gametag fields from latest activity, or original value
      const clickCount = activity?.clickCount ?? baseTri.clickCount ?? 0;
      const latest = activity?.mostRecent;
      const color = latest?.color ?? baseTri.color;
      const gametag = latest?.gametag ?? baseTri.gametag;
      const emoji = latest?.emoji ?? baseTri.emoji;
      let subdivided = baseTri.subdivided;
      let children: TriangleMesh[] | undefined;

      // Subdivide if reached click threshold (unless at max level)
      if (clickCount >= clicksToDivide && (baseTri.level < maxDivideLevel)) {
        // Generate children and apply activities recursively
        subdivided = true;
        children = applyActivities(subdivideTriangleMesh(baseTri), currentLevel + 1);
      }

      return {
        ...baseTri,
        clickCount,
        color,
        gametag,
        emoji,
        subdivided: subdivided ?? false,
        children
      };
    });
  }

  const rebuilt = applyActivities(baseMesh, 0);
  // Diagnostics
  if (typeof window !== "undefined") {
    console.log("[rebuildTriangleMeshFromActivities] - Canonical rebuild, mesh triangles:", rebuilt.length, rebuilt.slice(0,2));
  }
  return rebuilt;
}
