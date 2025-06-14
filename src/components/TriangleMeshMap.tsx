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

// Always use this default map center
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
  const [meshVersion, setMeshVersion] = useState(
    () => window.localStorage.getItem("meshVersion") || ""
  ); // listen for mesh resets

  // Listen for mesh/zoom settings changes even if user is actively on the map,
  // so settings take effect instantly on mobile
  useEffect(() => {
    const reloadMapSettings = () => {
      if (mapRef.current && mapInstanceRef.current) {
        // Remove and re-init map on setting changes
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
        setIsLoading(true);
        setTimeout(() => setIsLoading(false), 50);
      }
    };

    const storageHandler = (e: StorageEvent) => {
      if (
        e.key === "fixedMobileZoomLevel" ||
        e.key === "fixedMobileZoom" ||
        e.key === "refreshMesh"
      ) {
        reloadMapSettings();
      }
      // Also reload/refresh mesh if meshVersion bumps
      if (e.key === "meshVersion") {
        setMeshVersion(e.newValue || "");
        // Clear old mesh/activity caches
        window.localStorage.removeItem("triangleMeshCache");
        // Remove all triangle activities from memory
        setTriangleMesh([]);
        setIsLoading(true);
        setTimeout(() => setIsLoading(false), 30);
      }
      // GLOBAL WORLD RESET: reload the window for everyone!
      if (e.key === "worldReset") {
        window.location.reload();
      }
    };
    window.addEventListener("storage", storageHandler);
    return () => {
      window.removeEventListener("storage", storageHandler);
    };
  }, []);

  useEffect(() => {
    if (!mapRef.current) return;

    // ----- Read zoom settings from localStorage -----
    let mobileZoomLevel = 10;
    let mobileFixedZoomEnabled = true;
    if (isMobile) {
      const forceMobileZoom = window.localStorage.getItem('fixedMobileZoom');
      mobileFixedZoomEnabled = forceMobileZoom === null || forceMobileZoom === "true";
      if (mobileFixedZoomEnabled) {
        const zoomVal = window.localStorage.getItem('fixedMobileZoomLevel');
        if (
          zoomVal &&
          !isNaN(Number(zoomVal)) &&
          Number(zoomVal) >= 1 &&
          Number(zoomVal) <= 20
        ) {
          // Round zoom (for OSM only integer)
          mobileZoomLevel = Math.floor(Number(zoomVal));
        }
      }
    }

    // ----- Map Init -----
    // Use fixed zoom or original fallback
    const mapZoom = isMobile
      ? (mobileFixedZoomEnabled ? mobileZoomLevel : 10)
      : 6;

    const map = L.map(mapRef.current, {
      center: DEFAULT_CENTER,
      zoom: mapZoom,
      minZoom: isMobile && mobileFixedZoomEnabled ? mobileZoomLevel : (isMobile ? 10 : 5),
      maxZoom: isMobile && mobileFixedZoomEnabled ? mobileZoomLevel : (isMobile ? 10 : 15),
      worldCopyJump: true,
      maxBounds: [[-90, -180], [90, 180]],
      preferCanvas: true,
      zoomControl: !isMobile,
      doubleClickZoom: false,
      boxZoom: false,
      scrollWheelZoom: false,
      touchZoom: false,
      dragging: true,
    });

    // Set zoom control position on desktop only
    if (!isMobile) {
      map.zoomControl.setPosition('topright');
    }

    if (isMobile && mobileFixedZoomEnabled) {
      // Prevent zoom by gestures, scroll, and programmatically
      map.on("zoomend", () => {
        if (map.getZoom() !== mobileZoomLevel) {
          map.setZoom(mobileZoomLevel);
        }
      });
      map.on("movestart", () => {
        if (map.getZoom() !== mobileZoomLevel) {
          map.setZoom(mobileZoomLevel);
        }
      });
    } else if (isMobile) {
      map.on("zoomend", () => {
        if (map.getZoom() !== 10) {
          map.setZoom(10);
        }
      });
      map.on("movestart", () => {
        if (map.getZoom() !== 10) {
          map.setZoom(10);
        }
      });
    } else {
      // Clamp zoom in all user interactions (desktop)
      map.on("zoomend", () => {
        const z = map.getZoom();
        if (z < 5) map.setZoom(5);
        if (z > 15) map.setZoom(15);
      });
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
        // After reset, this will find nothing, so baseMesh will be used
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
        console.error("[TriangleMeshMap] Error loading mesh activities, fallback to base:", error);
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
  }, [isMobile, meshVersion]); // re-run loader on meshVersion change

  // Custom mobile/touch logic (does nothing on desktop)
  useLeafletMobileTouch(mapInstanceRef.current);

  // Use mesh tap handler (shared across devices)
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
      <ErrorBanner message={null} />
      {mapInstanceRef.current && (
        <TriangleMeshRenderer
          map={mapInstanceRef.current}
          triangleMesh={triangleMesh}
          triangleLayersRef={triangleLayersRef}
          onTriangleClick={(triangleId, triangle, parentPath) => {
            handleTriangleMeshClick(triangleId, triangle, prevMeshRef);
          }}
        />
      )}
    </div>
  );
};

export default TriangleMeshMap;
