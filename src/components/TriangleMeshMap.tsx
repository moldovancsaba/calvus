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

  // Called when the map is ready and instance available
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

  return (
    <div className="relative w-full h-full min-h-[0] flex-1 rounded-none border-0 p-0 m-0">
      <LeafletMapContainer
        ref={mapDivRef}
        isMobile={isMobile}
        meshVersion={meshVersion}
        worldSlug={worldSlug}
        onMapReady={handleMapReady}
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
