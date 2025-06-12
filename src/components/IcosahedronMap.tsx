
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

    // Add OpenStreetMap tiles with 10% gray background
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      opacity: 0.9
    }).addTo(map);

    // Set map background to 10% gray
    map.getContainer().style.backgroundColor = '#e6e6e6';

    // Generate initial icosahedron triangles
    const initialTriangles = generateIcosahedronTriangles();
    setTriangles(initialTriangles);

    console.log('Generated icosahedron with', initialTriangles.length, 'triangles');

    return () => {
      map.remove();
    };
  }, []);

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

        // Create polygon coordinates
        const coordinates: [number, number][] = triangle.vertices.map(vertex => [vertex.lat, vertex.lng]);
        
        // Create the polygon
        const polygon = L.polygon(coordinates, {
          color: '#333333',
          weight: 1,
          opacity: 0.8,
          fillColor: getTriangleColor(triangle),
          fillOpacity: 0.7
        });

        // Add click handler
        polygon.on('click', () => {
          console.log(`Clicked triangle ${triangle.id}, current clicks: ${triangle.clickCount}`);
          handleTriangleClick(triangle.id);
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
      <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-4 shadow-lg">
        <h2 className="text-lg font-semibold mb-2">Icosahedral Geodesic Grid</h2>
        <div className="text-sm text-muted-foreground space-y-1">
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
