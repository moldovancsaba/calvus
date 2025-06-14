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
import { LoadingOverlay } from './map/LoadingOverlay';
import { ErrorBanner } from './map/ErrorBanner';

// Removed geolocation - always use this default map center
const DEFAULT_CENTER: [number, number] = [33, 0];

const TriangleMeshMap = () => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const [triangleMesh, setTriangleMesh] = useState<TriangleMesh[]>([]);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const { identity } = useIdentity();
  const isMobile = useIsMobile();

  const prevMeshRef = useRef<TriangleMesh[]>([]);

  // --- Map initialization without geolocation ---
  useEffect(() => {
    if (!mapRef.current) return;

    const map = L.map(mapRef.current, {
      center: DEFAULT_CENTER,
      zoom: 6,
      minZoom: 5,
      maxZoom: 15,
      worldCopyJump: true,
      maxBounds: [[-90, -180], [90, 180]],
      preferCanvas: true,
      zoomControl: true,
      doubleClickZoom: false,
      boxZoom: false,
      scrollWheelZoom: false,
      touchZoom: false,
      dragging: true,
    });

    map.zoomControl.setPosition('topright');

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
      mapInstanceRef.current = null;
      map.remove();
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  // Custom mobile/touch logic (refactored, hook does nothing on desktop)
  useLeafletMobileTouch(mapInstanceRef.current);

  // Use robust mesh tap handler (shared across devices)
  const handleTriangleMeshClick = useTriangleMeshTap(
    identity,
    setTriangleMesh,
    isMobile,
    mapInstanceRef.current
  );

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
      {isLoading && <LoadingOverlay />}
      {/* ErrorBanner no longer needed without geolocation, but keeping render for compatibility */}
      <ErrorBanner message={null} />
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
