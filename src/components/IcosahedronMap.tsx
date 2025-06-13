
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

    // Initialize the map
    const map = L.map(mapRef.current, {
      center: [0, 0],
      zoom: 2,
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

    // Generate initial spherical triangle grid
    const initialTriangles = generateIcosahedronTriangles();
    setTriangles(initialTriangles);

    console.log('Generated spherical grid with', initialTriangles.length, 'triangles');

    return () => {
      map.remove();
    };
  }, []);

  // Function to create geodesic lines between points
  const createGeodesicTriangle = (vertices: [any, any, any]) => {
    // For spherical triangles, we need to create curved edges
    // Leaflet's polygon will automatically handle this when we provide enough intermediate points
    const interpolatePoints = (start: any, end: any, steps: number = 10) => {
      const points = [];
      for (let i = 0; i <= steps; i++) {
        const ratio = i / steps;
        // Simple spherical interpolation (great circle)
        const lat = start.lat + (end.lat - start.lat) * ratio;
        const lng = start.lng + (end.lng - start.lng) * ratio;
        points.push([lat, lng]);
      }
      return points;
    };

    // Create geodesic edges for the triangle
    const edge1 = interpolatePoints(vertices[0], vertices[1], 20);
    const edge2 = interpolatePoints(vertices[1], vertices[2], 20);
    const edge3 = interpolatePoints(vertices[2], vertices[0], 20);

    // Combine all points to form a smooth triangle
    const allPoints = [...edge1, ...edge2.slice(1), ...edge3.slice(1, -1)];
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
        <h2 className="text-lg font-semibold mb-2">Spherical Geodesic Grid</h2>
        <div className="text-sm text-muted-foreground space-y-1">
          <p>• 5 latitude bands: Arctic Circle, Tropic of Cancer, Equator, Tropic of Capricorn, Antarctic Circle</p>
          <p>• 5 longitude segments of 72° each</p>
          <p>• Click triangles to change color (10% gray per click)</p>
          <p>• 11th click subdivides into 4 triangles</p>
          <p>• Up to 19 levels of subdivision</p>
          <p>• Final level turns red</p>
        </div>
      </div>
    </div>
  );
};

export default IcosahedronMap;
