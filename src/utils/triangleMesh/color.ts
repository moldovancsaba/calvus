
import type { TriangleMesh } from "./geometry";

export function getTriangleMeshColor(triangle: TriangleMesh): string {
  if (triangle.level === 19 && triangle.clickCount >= 10) {
    return '#ff0000'; // Red for final level
  }
  const grayPercent = Math.min(triangle.clickCount * 10, 100);
  if (grayPercent === 0) {
    return '#ffffff';
  }
  const grayValue = Math.floor(255 * (1 - grayPercent / 100));
  return `rgb(${grayValue}, ${grayValue}, ${grayValue})`;
}
