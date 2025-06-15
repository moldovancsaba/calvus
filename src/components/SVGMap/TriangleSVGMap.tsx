
import React, { useState } from "react";

// Each triangle has a list of vertex points, an id, a level, clickCount, and optional children
type Triangle = {
  id: string;
  vertices: [number, number, number, number, number, number]; // [x1,y1, x2,y2, x3,y3]
  level: number;
  clickCount: number;
  ownerColor?: string;
  children?: Triangle[];
};

const COLORS = [
  "#fff",      // Initial
  "#ffc107",   // 1+
  "#43a047",   // 5+
  "#1976d2",   // 8+
  "#e91e63"    // 11+
];

const USER_COLOR = "#1976d2";

function getTriangleColor(triangle: Triangle): string {
  if (triangle.clickCount >= 11) return USER_COLOR;
  if (triangle.clickCount >= 8) return COLORS[3];
  if (triangle.clickCount >= 5) return COLORS[2];
  if (triangle.clickCount >= 1) return COLORS[1];
  return COLORS[0];
}

// Generate a set of "base" triangles that roughly form a decagon/icosahedron
function generateBaseTriangles(): Triangle[] {
  // For readability, layout is a decagon in SVG space (centered)
  const center = [200, 200];
  const radius = 140;
  const angleOffset = Math.PI / 2;
  const triangles: Triangle[] = [];
  for (let i = 0; i < 10; i++) {
    const a1 = angleOffset + (i * 2 * Math.PI) / 10;
    const a2 = angleOffset + ((i + 1) * 2 * Math.PI) / 10;
    triangles.push({
      id: String(i + 1),
      vertices: [
        center[0], center[1],
        center[0] + radius * Math.cos(a1), center[1] - radius * Math.sin(a1),
        center[0] + radius * Math.cos(a2), center[1] - radius * Math.sin(a2)
      ],
      level: 0,
      clickCount: 0,
    });
  }
  return triangles;
}

// Subdivide triangle into four smaller triangles using midpoints
function subdivideTriangle(triangle: Triangle): Triangle[] {
  const [x1,y1,x2,y2,x3,y3] = triangle.vertices;
  // Calculate midpoints
  const m1 = [(x1+x2)/2, (y1+y2)/2];
  const m2 = [(x2+x3)/2, (y2+y3)/2];
  const m3 = [(x3+x1)/2, (y3+y1)/2];
  const level = triangle.level + 1;
  // Create 4 new triangles
  return [
    { id: triangle.id+".1", vertices: [x1,y1, m1[0],m1[1], m3[0],m3[1]], level, clickCount: 0 },
    { id: triangle.id+".2", vertices: [m1[0],m1[1], x2,y2, m2[0],m2[1]], level, clickCount: 0 },
    { id: triangle.id+".3", vertices: [m3[0],m3[1], m2[0],m2[1], x3,y3], level, clickCount: 0 },
    { id: triangle.id+".4", vertices: [m1[0],m1[1], m2[0],m2[1], m3[0],m3[1]], level, clickCount: 0 }
  ];
}

// Recursive render
function TriangleSVG({ triangle, onClick }: { triangle: Triangle, onClick: (t: Triangle) => void }) {
  if (triangle.clickCount >= 11 && !triangle.children) {
    // Subdivide, but only render children!
    triangle.children = subdivideTriangle(triangle);
  }
  if (triangle.children) {
    return triangle.children.map(child => (
      <TriangleSVG key={child.id} triangle={child} onClick={onClick} />
    ));
  }
  return (
    <polygon
      points={`
        ${triangle.vertices[0]},${triangle.vertices[1]}
        ${triangle.vertices[2]},${triangle.vertices[3]}
        ${triangle.vertices[4]},${triangle.vertices[5]}
      `}
      fill={getTriangleColor(triangle)}
      stroke="#222"
      strokeWidth={1}
      onPointerDown={e => { e.stopPropagation(); onClick(triangle); }}
      style={{ cursor: 'pointer', transition: 'fill 0.2s' }}
    />
  );
}

export default function TriangleSVGMap() {
  const [triangles, setTriangles] = useState<Triangle[]>(generateBaseTriangles);

  function handleTriangleClick(tri: Triangle) {
    setTriangles(oldTris => {
      // Recursively find and update the right triangle by ID
      const update = (list: Triangle[]): Triangle[] =>
        list.map(t => {
          if (t.id === tri.id) {
            const clickCount = t.clickCount + 1;
            // Allow subdivision for demo, color by user
            return {
              ...t,
              clickCount,
              ownerColor: clickCount >= 11 ? USER_COLOR : undefined,
              // Remove children so it regenerates on next render
              children: clickCount >= 11 ? undefined : t.children
            };
          }
          if (t.children) return { ...t, children: update(t.children) };
          return t;
        });
      return update(oldTris);
    });
  }

  return (
    <div className="flex items-center justify-center w-full h-full bg-gradient-to-br from-blue-100 to-indigo-100">
      <svg
        width={420}
        height={420}
        viewBox="0 0 400 400"
        className="border bg-white shadow rounded-lg max-w-[95vw] max-h-[80vh] transition-all"
        style={{ touchAction: 'manipulation' }}
      >
        {triangles.map(tri =>
          <TriangleSVG key={tri.id} triangle={tri} onClick={handleTriangleClick} />
        )}
      </svg>
    </div>
  );
}
