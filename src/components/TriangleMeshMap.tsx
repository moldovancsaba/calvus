
import { useEffect, useRef, useState } from 'react';
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
import { useTriangleMeshTap } from "./mesh/useTriangleMeshTap";

// Helper to get user's geolocation (promise-based)
function getUserLatLng(): Promise<[number, number]> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) return reject(new Error('Geolocation is not supported.'));
    navigator.geolocation.getCurrentPosition(
      pos => resolve([pos.coords.latitude, pos.coords.longitude]),
      err => reject(err)
    );
  });
}

const TriangleMeshMap = () => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const [triangleMesh, setTriangleMesh] = useState<TriangleMesh[]>([]);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const { identity } = useIdentity();
  const isMobile = useIsMobile();

  // For UI revert on DB failure
  const prevMeshRef = useRef<TriangleMesh[]>([]);

  // New: Store initial center
  const [mapCenter, setMapCenter] = useState<[number, number] | null>(null);
  const [locationError, setLocationError] = useState<string | null>(null);

  // Try to get user geolocation on initial mount
  useEffect(() => {
    let active = true;
    getUserLatLng()
      .then(center => {
        if (active) {
          setMapCenter(center);
        }
      })
      .catch((err) => {
        setLocationError("Could not get your location, showing map at default location.");
        setMapCenter([33, 0]); // fallback
      });
    // Give 2s for geolocation, fallback to default after timeout if still waiting
    const fallbackTimeout = setTimeout(() => {
      if (!mapCenter) setMapCenter([33, 0]);
    }, 2000);
    return () => {
      active = false;
      clearTimeout(fallbackTimeout);
    };
    // eslint-disable-next-line
  }, []);

  // Map initialization (runs when mapCenter first resolved)
  useEffect(() => {
    if (!mapRef.current) return;
    if (!mapCenter) return; // Wait for center

    // Always enable zoomControl (the +/- buttons) and DISABLE ALL other zooming gestures
    const map = L.map(mapRef.current, {
      center: mapCenter,
      zoom: 6,
      minZoom: 5,
      maxZoom: 15,
      worldCopyJump: true,
      maxBounds: [[-90, -180], [90, 180]],
      preferCanvas: true,
      zoomControl: true,    // Show +/- buttons for zoom
      doubleClickZoom: false,
      boxZoom: false,
      scrollWheelZoom: false,
      touchZoom: false,     // FULLY disable ALL touch zooming
      dragging: true,       // Pan still works
    });

    // Remove existing controls and add zoom control top right
    map.zoomControl.setPosition('topright');

    // Clamp zoom in all user interactions
    map.on("zoomend", () => {
      const z = map.getZoom();
      if (z < 5) map.setZoom(5);
      if (z > 15) map.setZoom(15);
    });

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
        console.log("[TriangleMeshMap] Activities loaded:", activities);
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
        console.error("[TriangleMeshMap] Error loading mesh activities, fallback to base:", error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeMesh();

    pollIntervalRef.current = setInterval(async () => {
      try {
        const activities = await getTriangleActivities();
        console.log("[TriangleMeshMap] Activities polled:", activities);
        const restoredMesh = rebuildTriangleMeshFromActivities(activities);
        setTriangleMesh(restoredMesh);
      } catch (error) {
        console.error("[TriangleMeshMap] Error polling activities:", error);
      }
    }, 5000);

    return () => {
      map.remove();
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
    // eslint-disable-next-line
  }, [mapCenter]);

  // Recenter map if mapCenter changes after map constructed
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (map && mapCenter) {
      const current = map.getCenter();
      // only recenter if center is different from desired center
      if (current.lat !== mapCenter[0] || current.lng !== mapCenter[1]) {
        map.setView(mapCenter, map.getZoom(), { animate: true });
      }
    }
  }, [mapCenter]);

  // Custom mobile/touch logic (refactored, hook does nothing on desktop)
  useLeafletMobileTouch(mapInstanceRef.current);

  // Use robust mesh tap handler (shared across devices)
  const handleTriangleMeshClick = useTriangleMeshTap(
    identity,
    setTriangleMesh,
    isMobile,
    mapInstanceRef.current
  );

  // --- Responsive, full-screen map shell ---
  return (
    <div className="relative w-full h-full min-h-[0] flex-1 rounded-none border-0 p-0 m-0">
      <div
        ref={mapRef}
        className="w-full h-full min-h-[0] rounded-none"
        style={{
          minHeight: "0",
          maxHeight: "none",
          height: "100%",
          position: "relative"
        }}
      />
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/90 backdrop-blur-[2px] z-50 rounded-none p-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
            <p className="text-base text-gray-600">Loading...</p>
          </div>
        </div>
      )}
      {locationError && (
        <div className="absolute top-2 left-1/2 -translate-x-1/2 z-50 rounded bg-yellow-100 text-yellow-900 px-4 py-2 text-xs shadow border border-yellow-300">
          {locationError}
        </div>
      )}
      {/* Only render the mesh renderer if the map instance is present */}
      {mapInstanceRef.current && (
        <TriangleMeshRenderer
          map={mapInstanceRef.current}
          triangleMesh={triangleMesh}
          triangleLayersRef={triangleLayersRef}
          onTriangleClick={(triangleId, triangle, parentPath) => {
            console.log("[TriangleMeshMap] onTriangleClick", triangleId, triangle, parentPath);
            handleTriangleMeshClick(triangleId, triangle, prevMeshRef);
          }}
        />
      )}
    </div>
  );
};

export default TriangleMeshMap;

