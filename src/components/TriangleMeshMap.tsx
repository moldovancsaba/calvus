import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {
  TriangleMesh
} from '../utils/triangleMesh';
import { useIdentity } from "./IdentityContext";
import { useIsMobile } from "../hooks/use-mobile";
import { useLeafletMobileTouch } from "./hooks/useLeafletMobileTouch";
import { TriangleMeshRenderer } from "./mesh/TriangleMeshRenderer";
import { useTriangleMeshTap } from "./mesh/useTriangleMeshTap";
import { LoadingOverlay } from './map/LoadingOverlay';
import { ErrorBanner } from './map/ErrorBanner';

import { LeafletMapContainer } from "./map/LeafletMapContainer";
import { useTriangleMeshLoader } from "./map/useTriangleMeshLoader";

import { fetchWorldSettings, WorldSettings } from "../utils/worldSettings";

type Props = {
  worldSlug: string;
};

// Always use this default map center
const DEFAULT_CENTER: [number, number] = [33, 0];

const TriangleMeshMap = ({ worldSlug }: Props) => {
  const mapDivRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());
  const prevMeshRef = useRef<any[]>([]);
  const { identity } = useIdentity();
  const isMobile = useIsMobile();
  const [meshVersion, setMeshVersion] = useState(
    () => window.localStorage.getItem(`meshVersion_${worldSlug}`) || ""
  );

  // Loader hook (fetch, poll, manage mesh state)
  const { triangleMesh, setTriangleMesh, isLoading } = useTriangleMeshLoader(worldSlug, meshVersion);

  // World settings
  const [worldSettings, setWorldSettings] = useState<WorldSettings | null>(null);

  useEffect(() => {
    let mounted = true;
    async function loadWorldSettings() {
      try {
        const ws = await fetchWorldSettings(worldSlug);
        if (mounted) setWorldSettings(ws);
      } catch (e) {
        // Handle error or fallback to defaults?
        setWorldSettings(null);
      }
    }
    loadWorldSettings();
    // Listen for changes to settings
    const handler = (e: StorageEvent) => {
      if (e.key === `worldSettings_${worldSlug}`) {
        loadWorldSettings();
      }
    };
    window.addEventListener("storage", handler);
    return () => {
      mounted = false;
      window.removeEventListener("storage", handler);
    };
  }, [worldSlug]);

  // Listen for meshVersion/storage events for reloads
  useEffect(() => {
    const reloadMeshOnStorage = (e: StorageEvent) => {
      if (
        e.key === "fixedMobileZoomLevel" ||
        e.key === "fixedMobileZoom" ||
        e.key === `refreshMesh_${worldSlug}`
      ) {
        setMeshVersion(v => v); // trigger state
      }
      if (e.key === `meshVersion_${worldSlug}`) {
        setMeshVersion(e.newValue || "");
        window.localStorage.removeItem(`triangleMeshCache_${worldSlug}`);
        setTriangleMesh([]);
      }
      if (e.key === `worldReset_${worldSlug}`) {
        window.location.reload();
      }
    };
    window.addEventListener("storage", reloadMeshOnStorage);
    return () => window.removeEventListener("storage", reloadMeshOnStorage);
  }, [worldSlug, setTriangleMesh]);

  useLeafletMobileTouch(mapInstanceRef.current);

  // Check if map instance is alive, rendered, and mounted
  function isMapInstanceReady(map: L.Map | null) {
    if (!map) return false;
    try {
      const container = map.getContainer?.();
      return !!(container && container.parentNode);
    } catch (e) {
      return false;
    }
  }

  function handleMapReady(map: L.Map) {
    mapInstanceRef.current = map;
  }

  const handleTriangleMeshClick = useTriangleMeshTap(
    identity,
    setTriangleMesh,
    isMobile,
    mapInstanceRef.current,
    worldSlug
  );

  // Show a loading overlay until worldSettings is loaded
  if (!worldSettings) {
    return (
      <div className="relative w-full h-full flex-1 flex items-center justify-center">
        <LoadingOverlay />
      </div>
    );
  }

  return (
    <div className="relative w-full h-full min-h-[0] flex-1 rounded-none border-0 p-0 m-0">
      <LeafletMapContainer
        ref={mapDivRef}
        isMobile={isMobile}
        meshVersion={meshVersion}
        worldSlug={worldSlug}
        onMapReady={handleMapReady}
        desktopMinZoom={worldSettings.desktop_min_zoom_level}
        desktopMaxZoom={worldSettings.desktop_max_zoom_level}
        fixedMobileZoomLevel={worldSettings.fixed_mobile_zoom_level}
        forceMobileZoom={worldSettings.force_mobile_zoom}
      />
      {isLoading && <LoadingOverlay />}
      <ErrorBanner message={null} />
      {isMapInstanceReady(mapInstanceRef.current) && (
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
