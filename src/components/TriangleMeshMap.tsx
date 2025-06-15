
import React, { useEffect, useRef, useState } from 'react';
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
  settings?: WorldSettings;
};

const DEFAULT_CENTER: [number, number] = [33, 0];

function getFixedWorldSlug(slug: string) {
  return (!slug || slug === "") ? "original" : slug;
}

const TriangleMeshMap = ({ worldSlug, settings }: Props) => {
  const fixedWorldSlug = getFixedWorldSlug(worldSlug);

  // 1. Refs and state -- always run first
  const mapDivRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());
  const prevMeshRef = useRef<any[]>([]);
  const [worldSettings, setWorldSettings] = useState<WorldSettings | null>(null);
  const [meshVersion, setMeshVersion] = useState(
    () => window.localStorage.getItem(`meshVersion_${fixedWorldSlug}`) || ""
  );
  const [fitDone, setFitDone] = useState(false);

  // 2. All standard hooks (always at top)
  const { identity } = useIdentity();
  const isMobile = useIsMobile();
  const { triangleMesh, setTriangleMesh, isLoading } = useTriangleMeshLoader(fixedWorldSlug, meshVersion);

  // 3. World settings loader
  useEffect(() => {
    let mounted = true;
    async function loadWorldSettings() {
      try {
        const ws = await fetchWorldSettings(fixedWorldSlug);
        if (mounted) setWorldSettings(ws);
      } catch (e) {
        setWorldSettings(null);
      }
    }
    loadWorldSettings();
    const handler = (e: StorageEvent) => {
      if (e.key === `worldSettings_${fixedWorldSlug}`) {
        loadWorldSettings();
      }
    };
    window.addEventListener("storage", handler);
    return () => {
      mounted = false;
      window.removeEventListener("storage", handler);
    };
  }, [fixedWorldSlug]);

  // 4. Storage event mesh reloaders
  useEffect(() => {
    const reloadMeshOnStorage = (e: StorageEvent) => {
      if (
        e.key === "fixedMobileZoomLevel" ||
        e.key === "fixedMobileZoom" ||
        e.key === `refreshMesh_${fixedWorldSlug}`
      ) {
        setMeshVersion(v => v);
      }
      if (e.key === `meshVersion_${fixedWorldSlug}`) {
        setMeshVersion(e.newValue || "");
        window.localStorage.removeItem(`triangleMeshCache_${fixedWorldSlug}`);
        setTriangleMesh([]);
      }
      if (e.key === `worldReset_${fixedWorldSlug}`) {
        window.location.reload();
      }
    };
    window.addEventListener("storage", reloadMeshOnStorage);
    return () => window.removeEventListener("storage", reloadMeshOnStorage);
  }, [fixedWorldSlug, setTriangleMesh]);

  useLeafletMobileTouch(mapInstanceRef.current);

  // 5. Compute merged settings after all hooks
  const mergedWorldSettings = settings || worldSettings;

  // 6. Handle triangle click (only use settings from backend)
  const handleTriangleClick = useTriangleMeshTap(
    identity,
    setTriangleMesh,
    isMobile,
    mapInstanceRef.current,
    fixedWorldSlug,
    mergedWorldSettings // read from DB only!
  );

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

  useEffect(() => {
    if (!fitDone && mapInstanceRef.current && triangleMesh.length > 0) {
      const allCoords = triangleMesh.flatMap(t => t.vertices.map(v => [v.lat, v.lng]));
      if (allCoords.length >= 3) {
        const bounds = L.latLngBounds(allCoords as [number, number][]);
        mapInstanceRef.current.fitBounds(bounds, { padding: [24, 24], animate: true, maxZoom: 2 });
        setFitDone(true);
      }
    }
  }, [triangleMesh, fitDone]);

  // === 7. Render logic ===
  // Show loading spinner overlay if settings not ready
  if (!mergedWorldSettings) {
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
        worldSlug={fixedWorldSlug}
        onMapReady={handleMapReady}
        desktopMinZoom={mergedWorldSettings.desktop_min_zoom_level}
        desktopMaxZoom={mergedWorldSettings.desktop_max_zoom_level}
        fixedMobileZoomLevel={mergedWorldSettings.fixed_mobile_zoom_level}
        forceMobileZoom={mergedWorldSettings.force_mobile_zoom}
      />
      {isLoading && <LoadingOverlay />}
      <ErrorBanner message={null} />
      {isMapInstanceReady(mapInstanceRef.current) && (
        <TriangleMeshRenderer
          map={mapInstanceRef.current}
          triangleMesh={triangleMesh}
          triangleLayersRef={triangleLayersRef}
          onTriangleClick={(triangleId, triangle, parentPath) => {
            handleTriangleClick(triangleId, triangle, prevMeshRef);
          }}
          maxDivideLevel={mergedWorldSettings.max_divide_level}
          clicksToDivide={mergedWorldSettings.clicks_to_divide}
        />
      )}
    </div>
  );
};

export default TriangleMeshMap;
