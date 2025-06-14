
import { generateBaseTriangleMesh, subdivideTriangleMesh, TriangleMesh } from "./geometry";

// Rebuild triangle mesh from stored activities
export function rebuildTriangleMeshFromActivities(activities: any[]): TriangleMesh[] {
  const baseMesh = generateBaseTriangleMesh();
  const sortedActivities = activities.sort((a, b) =>
    new Date(a.when).getTime() - new Date(b.when).getTime()
  );
  let currentMesh = baseMesh;
  for (const activity of sortedActivities) {
    currentMesh = applyActivityToMesh(currentMesh, activity);
  }
  console.log("[rebuildTriangleMeshFromActivities] Final mesh:", JSON.parse(JSON.stringify(currentMesh)));
  return currentMesh;
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

