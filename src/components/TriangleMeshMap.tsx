import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { 
  generateBaseTriangleMesh, 
  subdivideTriangleMesh, 
  getTriangleMeshColor, 
  storeTriangleActivity,
  clearTriangleActivities,
  getTriangleActivities,
  rebuildTriangleMeshFromActivities,
  TriangleMesh 
} from '../utils/triangleMesh';
import { useIdentity } from "./IdentityContext";
import { useIsMobile } from "../hooks/use-mobile";

const TriangleMeshMap = () => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const [triangleMesh, setTriangleMesh] = useState<TriangleMesh[]>([]);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const { identity } = useIdentity();
  const isMobile = useIsMobile();

  // --- Responsive map: fill viewport height on mobile ---
  useEffect(() => {
    if (!mapRef.current) return;

    // --- Detect mobile ---
    const mobile = window.innerWidth < 768;

    const map = L.map(mapRef.current, {
      center: [33, 0],
      zoom: 3,
      minZoom: 1,
      maxZoom: 18,
      worldCopyJump: true,
      maxBounds: [[-90, -180], [90, 180]],
      preferCanvas: true,
      zoomControl: false,
      doubleClickZoom: false,
      boxZoom: false,
      tap: false,
      scrollWheelZoom: false,
      dragging: true,
      touchZoom: "center"
    });

    // --- Disable map touch gestures not wanted on mobile ---
    if (mobile) {
      // On mobile, allow only pinch to zoom and drag, disable single tap/double tap
      map.scrollWheelZoom.disable();
      map.doubleClickZoom.disable();
      map.boxZoom.disable();
      // Don't use map.tap handler (tapping is for triangles)
      if (map.tap) map.tap.disable();
      // touchZoom 'center' means only two-finger will zoom
      map.touchZoom.enable(); // still allow pinch
      map.dragging.enable();
      // Prevent default browser zoom/scroll with single finger on map
      map.getContainer().addEventListener(
        "touchstart",
        function (e) {
          if (e.touches.length === 1) {
            e.preventDefault();
            // allow drag, but prevent scroll/zoom for single finger tap/touch
          }
        },
        { passive: false }
      );
    }

    // --- Add mobile-friendly zoom controls ---
    if (window.innerWidth < 768) {
      // Add a mobile bottom right zoom control (custom or rebuilt later if needed)
    } else {
      L.control.zoom({ position: 'topright' }).addTo(map);
    }
    mapInstanceRef.current = map;

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      opacity: 0.9
    }).addTo(map);

    // Set map background to light gray
    map.getContainer().style.backgroundColor = '#f0f0f0';

    // Load existing activities and initialize mesh
    const initializeMesh = async () => {
      try {
        setIsLoading(true);
        const activities = await getTriangleActivities();
        
        if (activities.length > 0) {
          console.log(`Loading ${activities.length} stored activities`);
          const restoredMesh = rebuildTriangleMeshFromActivities(activities);
          setTriangleMesh(restoredMesh);
        } else {
          console.log('No stored activities found, starting with base mesh');
          const initialMesh = generateBaseTriangleMesh();
          setTriangleMesh(initialMesh);
        }
      } catch (error) {
        console.error('Error loading activities:', error);
        // Fallback to base mesh if loading fails
        const initialMesh = generateBaseTriangleMesh();
        setTriangleMesh(initialMesh);
      } finally {
        setIsLoading(false);
      }
    };

    initializeMesh();

    // Set up periodic polling for real-time updates
    pollIntervalRef.current = setInterval(async () => {
      try {
        const activities = await getTriangleActivities();
        const restoredMesh = rebuildTriangleMeshFromActivities(activities);
        setTriangleMesh(restoredMesh);
      } catch (error) {
        console.error('Error polling for updates:', error);
      }
    }, 5000); // Poll every 5 seconds

    return () => {
      map.remove();
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
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

  // Modified: pass color/gametag in activity, apply color logic per player
  const handleTriangleMeshClick = async (triangleId: string, triangle?: TriangleMesh) => {
    if (!identity) return;

    setTriangleMesh(prevMesh => {
      const updateTriangle = (triangles: TriangleMesh[]): TriangleMesh[] => {
        return triangles.map(triangleEl => {
          if (triangleEl.id === triangleId) {
            const newClickCount = triangleEl.clickCount + 1;

            // Store activity (now includes gametag + color)
            storeTriangleActivity(
              triangleId,
              newClickCount,
              triangleEl.level,
              identity.gametag,
              identity.color
            ).catch(error => console.error('Failed to store triangle activity:', error));

            // If subdivide
            if (newClickCount === 11 && triangleEl.level < 19) {
              const children = subdivideTriangleMesh(triangleEl);
              return {
                ...triangleEl,
                clickCount: newClickCount,
                subdivided: true,
                children,
                color: identity.color,
                gametag: identity.gametag,
              };
            }

            // Use player's color/gametag
            return {
              ...triangleEl,
              clickCount: newClickCount,
              color: identity.color,
              gametag: identity.gametag,
            };
          }

          if (triangleEl.children) {
            return {
              ...triangleEl,
              children: updateTriangle(triangleEl.children)
            };
          }
          return triangleEl;
        });
      };

      return updateTriangle(prevMesh);
    });

    // --- On mobile: zoom into triangle when tapped ---
    if (isMobile && mapInstanceRef.current && triangle) {
      // Compute triangle centroid for zoom
      const avgLat =
        (triangle.vertices[0].lat +
          triangle.vertices[1].lat +
          triangle.vertices[2].lat) /
        3;
      const avgLng =
        (triangle.vertices[0].lng +
          triangle.vertices[1].lng +
          triangle.vertices[2].lng) /
        3;
      // Animate zoom if not already zoomed in enough
      const zoomLevel = mapInstanceRef.current.getZoom();
      if (zoomLevel < 8) {
        mapInstanceRef.current.flyTo([avgLat, avgLng], 8, {
          animate: true,
          duration: 0.9
        });
      }
    }
  };

  // Modified: Show only player click count, no descriptions, use player color
  const renderTriangleMesh = (triangleList: TriangleMesh[], parentPath: string = '') => {
    if (!mapInstanceRef.current) return;
    const map = mapInstanceRef.current;

    triangleList.forEach(triangle => {
      const trianglePath = parentPath ? `${parentPath}-${triangle.id}` : triangle.id;
      if (!triangle.subdivided) {
        const existingLayer = triangleLayersRef.current.get(trianglePath);
        if (existingLayer) map.removeLayer(existingLayer);

        const coordinates = createGeodesicTriangle(triangle.vertices);

        // Color logic: white if zero clicks; own color if set; shade deeper for more clicks
        let fill = "#fff";
        if (triangle.clickCount > 0) {
          fill = triangle.color || "#222";
        }

        const fillOpacity = triangle.clickCount === 0 ? 0.50 : Math.min(0.3 + triangle.clickCount * 0.07, 0.95);

        const polygon = L.polygon(coordinates, {
          color: fill,
          weight: 2,
          opacity: 0.8,
          fillColor: fill,
          fillOpacity,
          smoothFactor: 1.0
        });

        polygon.on('click', () => {
          // Pass triangle info for mobile zoom
          handleTriangleMeshClick(triangle.id, triangle);
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

  // --- Make overlays/loader readable on all sizes ---
  return (
    <div className="w-full h-full min-h-[410px] relative">
      <div
        ref={mapRef}
        className="w-full h-full min-h-[410px]"
        style={{
          minHeight: "410px",
          height: "100%",
          maxHeight: "100dvh",
          position: "relative"
        }}
      />
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/80 backdrop-blur-[2px] z-50 rounded-lg p-4 shadow-lg">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
            <p className="text-base text-gray-600">Loading...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default TriangleMeshMap;
