import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { TriangleMesh, generateBaseTriangleMesh } from '../utils/triangleMesh';
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

  // 1. Refs and state
  const mapDivRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const triangleLayersRef = useRef<Map<string, L.Polygon>>(new Map());
  const prevMeshRef = useRef<any[]>([]);
  const [worldSettings, setWorldSettings] = useState<WorldSettings | null>(null);
  const [meshVersion, setMeshVersion] = useState(
    () => window.localStorage.getItem(`meshVersion_${fixedWorldSlug}`) || ""
  );
  const [fitDone, setFitDone] = useState(false);
  const [mapIsReady, setMapIsReady] = useState(false);

  // 2. Hooks
  const { identity } = useIdentity();
  const isMobile = useIsMobile();
  const { triangleMesh, setTriangleMesh, isLoading } = useTriangleMeshLoader(fixedWorldSlug, meshVersion);

  // Debug: Log mesh contents
  React.useEffect(() => {
    console.log("[DEBUG TriangleMeshMap] triangleMesh length:", triangleMesh?.length, triangleMesh?.slice(0, 2));
    if (Array.isArray(triangleMesh)) {
      triangleMesh.forEach((t, idx) => {
        if (!t.vertices || t.vertices.length !== 3) {
          console.error(`[DEBUG TriangleMeshMap] Triangle ${idx} (${t.id}) has invalid vertices:`, t.vertices);
        }
      });
    }
  }, [triangleMesh]);

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

  const mergedWorldSettings = settings || worldSettings;

  // Reset fitDone when world changes or when triangleMesh resets (to fit new mesh)
  useEffect(() => {
    setFitDone(false);
  }, [fixedWorldSlug, triangleMesh.length]);

  // 6. Handle triangle click
  const handleTriangleClick = useTriangleMeshTap(
    identity,
    setTriangleMesh,
    isMobile,
    mapInstanceRef.current,
    fixedWorldSlug,
    mergedWorldSettings
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
    setMapIsReady(true);

    // REMOVE DEBUG: Do not add marker at 0,0 or test rectangle.
    // All debug/test overlays below have been removed.
  }

  // Fit map to mesh whenever map/mesh changes and not already fit
  useEffect(() => {
    if (
      !fitDone &&
      mapIsReady &&
      mapInstanceRef.current &&
      triangleMesh.length > 0
    ) {
      const allCoords = triangleMesh.flatMap(t => t.vertices.map(v => [v.lat, v.lng]));
      if (allCoords.length >= 3) {
        // DEBUG: Instead of fitBounds, force visible hemisphere
        const bounds = L.latLngBounds([[-90, -180], [90, 180]]);
        mapInstanceRef.current.fitBounds(bounds, { padding: [24, 24], animate: true, maxZoom: 2 });
        setFitDone(true);
        console.log("[DEBUG fitBounds] Bounds set to show full globe.");
      }
    }
  }, [triangleMesh, fitDone, mapIsReady]);

  // === 7. Render logic ===
  if (!mergedWorldSettings) {
    return (
      <div className="relative w-full h-full flex-1 flex items-center justify-center">
        <LoadingOverlay />
      </div>
    );
  }

  // Always guarantee triangleMesh is non-empty in renderer layer (NO REQUIRE, USE IMPORT)
  let trianglesToRender: TriangleMesh[] = [];
  if (Array.isArray(triangleMesh) && triangleMesh.length > 0) {
    trianglesToRender = triangleMesh;
  } else {
    // Always fallback to base mesh, never empty!
    trianglesToRender = generateBaseTriangleMesh();
    console.warn("[TriangleMeshMap] Fallback: triangleMesh empty, rendering BASE mesh with 26 triangles.");
  }

  // Defensive: always log mesh status
  if (!Array.isArray(trianglesToRender) || trianglesToRender.length === 0) {
    console.error("[TriangleMeshMap] FATAL: No triangles to render even after fallback! Check mesh loader.");
  } else {
    console.log(`[TriangleMeshMap] Will render ${trianglesToRender.length} triangles. First:`, trianglesToRender[0]);
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
      {mapIsReady && mapInstanceRef.current && trianglesToRender.length > 0 && (
        <TriangleMeshRenderer
          map={mapInstanceRef.current}
          triangleMesh={trianglesToRender}
          triangleLayersRef={triangleLayersRef}
          onTriangleClick={(triangleId, triangle, parentPath) => {
            handleTriangleClick(triangleId, triangle, prevMeshRef);
          }}
          maxDivideLevel={mergedWorldSettings.max_divide_level}
          clicksToDivide={mergedWorldSettings.clicks_to_divide}
        />
      )}
      {mapIsReady && mapInstanceRef.current && trianglesToRender.length === 0 && (
        <div className="absolute left-0 right-0 top-0 bottom-0 flex items-center justify-center bg-white/70 z-50 font-bold text-red-600">
          Error: No triangles to display!
        </div>
      )}
    </div>
  );
};

export default TriangleMeshMap;
