import { useEffect, useRef, useState, useCallback } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {
  generateBaseTriangleMesh,
  subdivideTriangleMesh,
  storeTriangleActivity,
  getTriangleActivities,
  rebuildTriangleMeshFromActivities,
  TriangleMesh
} from '../utils/triangleMesh';
import { useIdentity } from "./IdentityContext";
import { useIsMobile } from "../hooks/use-mobile";
import { useLeafletMobileTouch } from "./hooks/useLeafletMobileTouch";
import { TriangleMeshRenderer } from "./mesh/TriangleMeshRenderer";

const TriangleMeshMap = () => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const [triangleMesh, setTriangleMesh] = useState<TriangleMesh[]>([]);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const { identity } = useIdentity();
  const isMobile = useIsMobile();

  // Map initialization
  useEffect(() => {
    if (!mapRef.current) return;

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
      scrollWheelZoom: false,
      dragging: true,
      touchZoom: "center"
    });

    if (!mobile) {
      L.control.zoom({ position: 'topright' }).addTo(map);
    }

    mapInstanceRef.current = map;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      opacity: 0.9
    }).addTo(map);

    map.getContainer().style.backgroundColor = '#f0f0f0';

    const initializeMesh = async () => {
      try {
        setIsLoading(true);
        const activities = await getTriangleActivities();

        if (activities.length > 0) {
          const restoredMesh = rebuildTriangleMeshFromActivities(activities);
          setTriangleMesh(restoredMesh);
        } else {
          const initialMesh = generateBaseTriangleMesh();
          setTriangleMesh(initialMesh);
        }
      } catch (error) {
        const initialMesh = generateBaseTriangleMesh();
        setTriangleMesh(initialMesh);
      } finally {
        setIsLoading(false);
      }
    };

    initializeMesh();

    pollIntervalRef.current = setInterval(async () => {
      try {
        const activities = await getTriangleActivities();
        const restoredMesh = rebuildTriangleMeshFromActivities(activities);
        setTriangleMesh(restoredMesh);
      } catch (error) {
        // ignore
      }
    }, 5000);

    return () => {
      map.remove();
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  // Custom mobile/touch logic (refactored, hook does nothing on desktop)
  useLeafletMobileTouch(mapInstanceRef.current);

  // Handler: robust tap/click/press - always await DB write and revert on fail
  const handleTriangleMeshClick = useCallback(
    async (triangleId: string, triangle?: TriangleMesh) => {
      if (!identity) return;

      let uiUpdated = false;
      let prevMesh: TriangleMesh[] = [];
      setTriangleMesh(currMesh => {
        prevMesh = currMesh;
        const updateTriangle = (triangles: TriangleMesh[]): TriangleMesh[] => {
          return triangles.map(triangleEl => {
            if (triangleEl.id === triangleId) {
              const newClickCount = triangleEl.clickCount + 1;

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
        uiUpdated = true;
        return updateTriangle(currMesh);
      });

      let storeSuccess = false;
      try {
        // Wait for DB to store the activity, toast if error!
        await storeTriangleActivity(
          triangleId,
          (triangle?.clickCount ?? 0) + 1,
          triangle?.level ?? 0,
          identity.gametag,
          identity.color
        );
        storeSuccess = true;
      } catch (err: any) {
        storeSuccess = false;
        import("./ui/use-toast").then(({ toast }) => {
          toast({
            title: "Failed to save activity",
            description: "Could not save tap to server. Please check your connection.",
            variant: "destructive",
          });
        });
        // Revert the UI change (to make state reliable)
        setTriangleMesh(prev => prevMesh);
      }

      // On mobile: zoom to triangle centroid on tap
      if (storeSuccess && isMobile && mapInstanceRef.current && triangle) {
        const avgLat = (
          triangle.vertices[0].lat +
          triangle.vertices[1].lat +
          triangle.vertices[2].lat
        ) / 3;
        const avgLng = (
          triangle.vertices[0].lng +
          triangle.vertices[1].lng +
          triangle.vertices[2].lng
        ) / 3;
        const zoomLevel = mapInstanceRef.current.getZoom();
        if (zoomLevel < 8) {
          mapInstanceRef.current.flyTo([avgLat, avgLng], 8, {
            animate: true,
            duration: 0.9
          });
        }
      }
    },
    [identity, isMobile]
  );

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
      {/* Renders mesh */}
      <TriangleMeshRenderer
        map={mapInstanceRef.current}
        triangleMesh={triangleMesh}
        triangleLayersRef={triangleLayersRef}
        onTriangleClick={handleTriangleMeshClick}
      />
    </div>
  );
};

export default TriangleMeshMap;
