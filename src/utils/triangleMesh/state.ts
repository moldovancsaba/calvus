
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
  return currentMesh;
}

// Apply a single activity to the mesh
function applyActivityToMesh(mesh: TriangleMesh[], activity: any): TriangleMesh[] {
  return updateTriangleInMesh(mesh, activity.where, activity.what, activity.level);
}

// Update a specific triangle in the mesh
function updateTriangleInMesh(triangles: TriangleMesh[], triangleId: string, clickCount: number, level: number): TriangleMesh[] {
  return triangles.map(triangle => {
    if (triangle.id === triangleId) {
      const updatedTriangle = {
        ...triangle,
        clickCount: clickCount
      };

      if (clickCount === 11 && triangle.level < 19) {
        const children = subdivideTriangleMesh(triangle);
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
        children: updateTriangleInMesh(triangle.children, triangleId, clickCount, level)
      };
    }

    return triangle;
  });
}
