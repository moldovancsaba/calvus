
import type { TriangleMesh } from "./geometry";

export function getTriangleMeshColor(triangle: TriangleMesh): string {
  if (triangle.level === 19 && triangle.clickCount >= 10 && triangle.color) {
    return triangle.color;
  }
  if (triangle.clickCount === 0) {
    return '#ffffff';
  }
  return triangle.color || "#888";
}
