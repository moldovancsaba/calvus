
/**
 * Returns a closed array of LatLng points for a triangle with (optionally curved) edges.
 * Each vertex must have .lat and .lng (degrees)
 */
export function createGeodesicTriangle(vertices: [any, any, any]) {
  const greatCirclePath = (start: any, end: any, steps: number = 50) => {
    const points = [];
    const lat1 = start.lat * Math.PI / 180,
      lng1 = start.lng * Math.PI / 180,
      lat2 = end.lat * Math.PI / 180,
      lng2 = end.lng * Math.PI / 180;
    const deltaLng = lng2 - lng1;
    const a =
      Math.sin((lat2 - lat1) / 2) ** 2 +
      Math.cos(lat1) * Math.cos(lat2) * Math.sin(deltaLng / 2) ** 2;
    const distance = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    for (let i = 0; i <= steps; i++) {
      const f = i / steps;
      if (distance < 1e-6) {
        points.push([
          start.lat + (end.lat - start.lat) * f,
          start.lng + (end.lng - start.lng) * f
        ]);
        continue;
      }
      if (Math.abs(distance - Math.PI) < 1e-6) {
        points.push([
          start.lat + (end.lat - start.lat) * f,
          start.lng + (end.lng - start.lng) * f
        ]);
        continue;
      }
      const A = Math.sin((1 - f) * distance) / Math.sin(distance);
      const B = Math.sin(f * distance) / Math.sin(distance);
      const x1 = Math.cos(lat1) * Math.cos(lng1),
        y1 = Math.cos(lat1) * Math.sin(lng1),
        z1 = Math.sin(lat1),
        x2 = Math.cos(lat2) * Math.cos(lng2),
        y2 = Math.cos(lat2) * Math.sin(lng2),
        z2 = Math.sin(lat2);
      const x = A * x1 + B * x2,
        y = A * y1 + B * y2,
        z = A * z1 + B * z2;
      const lat = Math.atan2(z, Math.sqrt(x * x + y * y)) * 180 / Math.PI,
        lng = Math.atan2(y, x) * 180 / Math.PI;
      points.push([lat, lng]);
    }
    return points;
  };

  const edge1 = greatCirclePath(vertices[0], vertices[1]);
  const edge2 = greatCirclePath(vertices[1], vertices[2]);
  const edge3 = greatCirclePath(vertices[2], vertices[0]);

  return [...edge1, ...edge2.slice(1), ...edge3.slice(1, -1)];
}
