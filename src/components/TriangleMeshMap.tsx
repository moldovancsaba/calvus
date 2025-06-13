
import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { 
  generateBaseTriangleMesh, 
  subdivideTriangleMesh, 
  getTriangleMeshColor, 
  storeTriangleActivity,
  clearTriangleActivities,
  TriangleMesh 
} from '../utils/triangleMesh';

const TriangleMeshMap = () => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const [triangleMesh, setTriangleMesh] = useState<TriangleMesh[]>([]);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());

  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize the map
    const map = L.map(mapRef.current, {
      center: [33, 0],
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

    // Generate initial triangle mesh and clear MongoDB
    const initializeMesh = async () => {
      try {
        await clearTriangleActivities();
        const initialMesh = generateBaseTriangleMesh();
        setTriangleMesh(initialMesh);
        console.log('Generated base triangle mesh and cleared MongoDB');
      } catch (error) {
        console.error('Error initializing mesh:', error);
        // Fallback to local mesh if MongoDB fails
        const initialMesh = generateBaseTriangleMesh();
        setTriangleMesh(initialMesh);
      }
    };

    initializeMesh();

    return () => {
      map.remove();
    };
  }, []);

  // Create geodesic triangle coordinates
  const createGeodesicTriangle = (vertices: [any, any, any]) => {
    const greatCirclePath = (start: any, end: any, steps: number = 50) => {
      const points = [];
      
      const lat1 = start.lat * Math.PI / 180;
      const lng1 = start.lng * Math.PI / 180;
      const lat2 = end.lat * Math.PI / 180;
      const lng2 = end.lng * Math.PI / 180;
      
      const deltaLng = lng2 - lng1;
      const a = Math.sin((lat2 - lat1) / 2) ** 2 + 
               Math.cos(lat1) * Math.cos(lat2) * Math.sin(deltaLng / 2) ** 2;
      const distance = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      
      for (let i = 0; i <= steps; i++) {
        const f = i / steps;
        
        if (distance < 1e-6) {
          const lat = start.lat + (end.lat - start.lat) * f;
          const lng = start.lng + (end.lng - start.lng) * f;
          points.push([lat, lng]);
          continue;
        }
        
        if (Math.abs(distance - Math.PI) < 1e-6) {
          const lat = start.lat + (end.lat - start.lat) * f;
          const lng = start.lng + (end.lng - start.lng) * f;
          points.push([lat, lng]);
          continue;
        }
        
        const A = Math.sin((1 - f) * distance) / Math.sin(distance);
        const B = Math.sin(f * distance) / Math.sin(distance);
        
        const x1 = Math.cos(lat1) * Math.cos(lng1);
        const y1 = Math.cos(lat1) * Math.sin(lng1);
        const z1 = Math.sin(lat1);
        
        const x2 = Math.cos(lat2) * Math.cos(lng2);
        const y2 = Math.cos(lat2) * Math.sin(lng2);
        const z2 = Math.sin(lat2);
        
        const x = A * x1 + B * x2;
        const y = A * y1 + B * y2;
        const z = A * z1 + B * z2;
        
        const lat = Math.atan2(z, Math.sqrt(x * x + y * y)) * 180 / Math.PI;
        const lng = Math.atan2(y, x) * 180 / Math.PI;
        
        points.push([lat, lng]);
      }
      
      return points;
    };

    const edge1 = greatCirclePath(vertices[0], vertices[1]);
    const edge2 = greatCirclePath(vertices[1], vertices[2]);
    const edge3 = greatCirclePath(vertices[2], vertices[0]);

    const allPoints = [
      ...edge1,
      ...edge2.slice(1),
      ...edge3.slice(1, -1)
    ];
    
    return allPoints;
  };

  // Handle triangle clicks with MongoDB storage
  const handleTriangleMeshClick = async (triangleId: string) => {
    setTriangleMesh(prevMesh => {
      const updateTriangle = (triangles: TriangleMesh[]): TriangleMesh[] => {
        return triangles.map(triangle => {
          if (triangle.id === triangleId) {
            const newClickCount = triangle.clickCount + 1;
            
            // Store activity in MongoDB
            storeTriangleActivity(triangleId, newClickCount, triangle.level)
              .catch(error => console.error('Failed to store triangle activity:', error));
            
            // Check if we need to subdivide (after 10 clicks, on 11th click)
            if (newClickCount === 11 && triangle.level < 19) {
              const children = subdivideTriangleMesh(triangle);
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
          
          if (triangle.children) {
            return {
              ...triangle,
              children: updateTriangle(triangle.children)
            };
          }
          
          return triangle;
        });
      };

      return updateTriangle(prevMesh);
    });
  };

  // Render triangles on the map
  const renderTriangleMesh = (triangleList: TriangleMesh[], parentPath: string = '') => {
    if (!mapInstanceRef.current) return;

    const map = mapInstanceRef.current;

    triangleList.forEach(triangle => {
      const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
      
      if (!triangle.subdivided) {
        const existingLayer = triangleLayersRef.current.get(trianglePath);
        if (existingLayer) {
          map.removeLayer(existingLayer);
        }

        const coordinates = createGeodesicTriangle(triangle.vertices);
        
        const polygon = L.polygon(coordinates, {
          color: '#2563eb',
          weight: 2,
          opacity: 0.8,
          fillColor: getTriangleMeshColor(triangle),
          fillOpacity: 0.6,
          smoothFactor: 1.0
        });

        polygon.on('click', () => {
          console.log(`Clicked triangle ${triangle.id}, current clicks: ${triangle.clickCount}, level: ${triangle.level}`);
          handleTriangleMeshClick(triangle.id);
        });

        polygon.on('mouseover', () => {
          polygon.setStyle({ weight: 4, opacity: 1.0 });
        });

        polygon.on('mouseout', () => {
          polygon.setStyle({ weight: 2, opacity: 0.8 });
        });

        polygon.addTo(map);
        triangleLayersRef.current.set(trianglePath, polygon);
      } else if (triangle.children) {
        renderTriangleMesh(triangle.children, trianglePath);
      }
    });
  };

  // Re-render triangles when state changes
  useEffect(() => {
    if (triangleMesh.length > 0 && mapInstanceRef.current) {
      triangleLayersRef.current.forEach(layer => {
        if (mapInstanceRef.current) {
          mapInstanceRef.current.removeLayer(layer);
        }
      });
      triangleLayersRef.current.clear();

      renderTriangleMesh(triangleMesh);
    }
  }, [triangleMesh]);

  return (
    <div className="w-full h-screen relative">
      <div ref={mapRef} className="w-full h-full" />
      <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-4 shadow-lg max-w-sm">
        <h2 className="text-lg font-semibold mb-2">Spherical Triangle Mesh</h2>
        <div className="text-sm text-muted-foreground space-y-1">
          <p>• Three base triangles with geodesic edges</p>
          <p>• Triangle IDs: 1, 2, 3 → 1.1, 1.2, 1.3, 1.4</p>
          <p>• Click tracking stored in MongoDB</p>
          <p>• Activity format: when/where/what</p>
          <p>• Click triangle to change color (10% gray per click)</p>
          <p>• 11th click subdivides into 4 triangles</p>
          <p>• Up to 19 levels of subdivision</p>
          <p>• Final level turns red</p>
        </div>
      </div>
    </div>
  );
};

export default TriangleMeshMap;
