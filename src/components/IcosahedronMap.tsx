import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { generateIcosahedronTriangles, subdivideTriangle, getTriangleColor, Triangle } from '../utils/icosahedron';

const IcosahedronMap = () => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const [triangles, setTriangles] = useState<Triangle[]>([]);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());

  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize the map centered on the triangle
    const map = L.map(mapRef.current, {
      center: [33, 0], // Center between the triangle points
      zoom: 3,
      minZoom: 1,
      maxZoom: 18,
      worldCopyJump: true,
      maxBounds: [[-90, -180], [90, 180]]
    });

    mapInstanceRef.current = map;

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      opacity: 0.9
    }).addTo(map);

    // Set map background to light gray
    map.getContainer().style.backgroundColor = '#f0f0f0';

    // Generate initial single triangle
    const initialTriangles = generateIcosahedronTriangles();
    setTriangles(initialTriangles);

    console.log('Generated single triangle');

    return () => {
      map.remove();
    };
  }, []);

  // Function to create proper geodesic lines between points
  const createGeodesicTriangle = (vertices: [any, any, any]) => {
    // Calculate great circle path between two points on sphere
    const greatCirclePath = (start: any, end: any, steps: number = 50) => {
      const points = [];
      
      // Convert to radians
      const lat1 = start.lat * Math.PI / 180;
      const lng1 = start.lng * Math.PI / 180;
      const lat2 = end.lat * Math.PI / 180;
      const lng2 = end.lng * Math.PI / 180;
      
      // Calculate the great circle distance
      const deltaLng = lng2 - lng1;
      const a = Math.sin((lat2 - lat1) / 2) ** 2 + 
               Math.cos(lat1) * Math.cos(lat2) * Math.sin(deltaLng / 2) ** 2;
      const distance = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      
      for (let i = 0; i <= steps; i++) {
        const f = i / steps;
        
        // Spherical interpolation (slerp) for great circle
        const A = Math.sin((1 - f) * distance) / Math.sin(distance);
        const B = Math.sin(f * distance) / Math.sin(distance);
        
        // Handle special cases where points are very close or antipodal
        if (distance < 1e-6) {
          // Points are very close, use linear interpolation
          const lat = start.lat + (end.lat - start.lat) * f;
          const lng = start.lng + (end.lng - start.lng) * f;
          points.push([lat, lng]);
          continue;
        }
        
        if (Math.abs(distance - Math.PI) < 1e-6) {
          // Points are antipodal, use any great circle
          const lat = start.lat + (end.lat - start.lat) * f;
          const lng = start.lng + (end.lng - start.lng) * f;
          points.push([lat, lng]);
          continue;
        }
        
        // Convert back to cartesian for interpolation
        const x1 = Math.cos(lat1) * Math.cos(lng1);
        const y1 = Math.cos(lat1) * Math.sin(lng1);
        const z1 = Math.sin(lat1);
        
        const x2 = Math.cos(lat2) * Math.cos(lng2);
        const y2 = Math.cos(lat2) * Math.sin(lng2);
        const z2 = Math.sin(lat2);
        
        // Interpolated cartesian coordinates
        const x = A * x1 + B * x2;
        const y = A * y1 + B * y2;
        const z = A * z1 + B * z2;
        
        // Convert back to lat/lng
        const lat = Math.atan2(z, Math.sqrt(x * x + y * y)) * 180 / Math.PI;
        const lng = Math.atan2(y, x) * 180 / Math.PI;
        
        points.push([lat, lng]);
      }
      
      return points;
    };

    // Create geodesic edges for the triangle
    const edge1 = greatCirclePath(vertices[0], vertices[1]);
    const edge2 = greatCirclePath(vertices[1], vertices[2]);
    const edge3 = greatCirclePath(vertices[2], vertices[0]);

    // Combine all points to form a closed triangle
    // Remove duplicate points at corners to avoid overlaps
    const allPoints = [
      ...edge1,
      ...edge2.slice(1), // Skip first point (duplicate of edge1 last)
      ...edge3.slice(1, -1) // Skip first and last points (duplicates)
    ];
    
    return allPoints;
  };

  // Function to handle triangle clicks
  const handleTriangleClick = (triangleId: string) => {
    setTriangles(prevTriangles => {
      const updateTriangle = (triangles: Triangle[]): Triangle[] => {
        return triangles.map(triangle => {
          if (triangle.id === triangleId) {
            const newClickCount = triangle.clickCount + 1;
            
            // Check if we need to subdivide (after 10 clicks, on 11th click)
            if (newClickCount === 11 && triangle.level < 19) {
              const children = subdivideTriangle(triangle);
              console.log(`Subdividing triangle ${triangleId} at level ${triangle.level} into 4 children`);
              return {
                ...triangle,
                clickCount: newClickCount,
                subdivided: true,
                children
              };
            }
            
            return {
              ...triangle,
              clickCount: newClickCount
            };
          }
          
          // Recursively check children
          if (triangle.children) {
            return {
              ...triangle,
              children: updateTriangle(triangle.children)
            };
          }
          
          return triangle;
        });
      };

      return updateTriangle(prevTriangles);
    });
  };

  // Function to render triangles on the map
  const renderTriangles = (triangleList: Triangle[], parentPath: string = '') => {
    if (!mapInstanceRef.current) return;

    const map = mapInstanceRef.current;

    triangleList.forEach(triangle => {
      const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
      
      // Only render if not subdivided or if it's a child triangle
      if (!triangle.subdivided) {
        // Remove existing layer if it exists
        const existingLayer = triangleLayersRef.current.get(trianglePath);
        if (existingLayer) {
          map.removeLayer(existingLayer);
        }

        // Create geodesic triangle coordinates
        const coordinates = createGeodesicTriangle(triangle.vertices);
        
        // Create the polygon with geodesic edges
        const polygon = L.polygon(coordinates, {
          color: '#2563eb',
          weight: 2,
          opacity: 0.8,
          fillColor: getTriangleColor(triangle),
          fillOpacity: 0.6,
          smoothFactor: 1.0
        });

        // Add click handler
        polygon.on('click', () => {
          console.log(`Clicked triangle ${triangle.id}, current clicks: ${triangle.clickCount}, level: ${triangle.level}`);
          handleTriangleClick(triangle.id);
        });

        // Add hover effect
        polygon.on('mouseover', () => {
          polygon.setStyle({ weight: 4, opacity: 1.0 });
        });

        polygon.on('mouseout', () => {
          polygon.setStyle({ weight: 2, opacity: 0.8 });
        });

        // Add to map and store reference
        polygon.addTo(map);
        triangleLayersRef.current.set(trianglePath, polygon);
      } else if (triangle.children) {
        // Render children instead
        renderTriangles(triangle.children, trianglePath);
      }
    });
  };

  // Re-render triangles when state changes
  useEffect(() => {
    if (triangles.length > 0 && mapInstanceRef.current) {
      // Clear existing layers
      triangleLayersRef.current.forEach(layer => {
        if (mapInstanceRef.current) {
          mapInstanceRef.current.removeLayer(layer);
        }
      });
      triangleLayersRef.current.clear();

      // Render all triangles
      renderTriangles(triangles);
    }
  }, [triangles]);

  return (
    <div className="w-full h-screen relative">
      <div ref={mapRef} className="w-full h-full" />
      <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-4 shadow-lg max-w-sm">
        <h2 className="text-lg font-semibold mb-2">Single Spherical Triangle</h2>
        <div className="text-sm text-muted-foreground space-y-1">
          <p>• Single triangle with vertices:</p>
          <p>  - Top: 0°, 66°</p>
          <p>  - Left: -36°, 0°</p>
          <p>  - Right: 36°, 0°</p>
          <p>• Click triangle to change color (10% gray per click)</p>
          <p>• 11th click subdivides into 4 triangles</p>
          <p>• Up to 19 levels of subdivision</p>
          <p>• Final level turns red</p>
          <p>• Geodesic edges prevent gaps/overlaps</p>
        </div>
      </div>
    </div>
  );
};

export default IcosahedronMap;
