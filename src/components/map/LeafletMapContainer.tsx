
import React, { useRef, useEffect, useImperativeHandle, forwardRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export interface LeafletMapContainerProps {
  isMobile: boolean;
  meshVersion: string;
  worldSlug: string;
  onMapReady: (map: L.Map) => void;
  desktopMinZoom?: number;
  desktopMaxZoom?: number;
  fixedMobileZoomLevel?: number;
  forceMobileZoom?: boolean;
}

export const DEFAULT_CENTER: [number, number] = [33, 0];

// Expose map instance via ref if needed
export const LeafletMapContainer = forwardRef<HTMLDivElement, LeafletMapContainerProps>(
  (
    {
      isMobile,
      meshVersion,
      worldSlug,
      onMapReady,
      desktopMinZoom = 5,
      desktopMaxZoom = 15,
      fixedMobileZoomLevel = 2,
      forceMobileZoom = true
    },
    ref
  ) => {
    const mapRef = useRef<HTMLDivElement>(null);
    const mapInstanceRef = useRef<L.Map | null>(null);

    useImperativeHandle(ref, () => mapRef.current as HTMLDivElement);

    useEffect(() => {
      if (!mapRef.current) return;
      // Clean up any existing map on this container
      if ((mapRef.current as any)._leaflet_id) {
        try {
          mapInstanceRef.current?.remove();
        } catch (e) {}
        (mapRef.current as any)._leaflet_id = undefined;
        mapRef.current.innerHTML = "";
      }

      let mobileZoomLevel = fixedMobileZoomLevel ?? 2;
      let mobileFixedZoomEnabled = forceMobileZoom;

      // Always pull in passed props for min/max zoom
      const minZoom = isMobile && mobileFixedZoomEnabled
        ? mobileZoomLevel
        : (isMobile ? 10 : desktopMinZoom);
      const maxZoom = isMobile && mobileFixedZoomEnabled
        ? mobileZoomLevel
        : (isMobile ? 10 : desktopMaxZoom);

      const mapZoom = isMobile
        ? (mobileFixedZoomEnabled ? mobileZoomLevel : 10)
        : desktopMinZoom; // center zoom to min desktop for new map

      const map = L.map(mapRef.current, {
        center: DEFAULT_CENTER,
        zoom: mapZoom,
        minZoom,
        maxZoom,
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

      if (!isMobile) {
        map.zoomControl.setPosition('topright');
      }

      if (isMobile && mobileFixedZoomEnabled) {
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
        // Enforce desktop min/max from DB
        map.on("zoomend", () => {
          const z = map.getZoom();
          if (z < desktopMinZoom) map.setZoom(desktopMinZoom);
          if (z > desktopMaxZoom) map.setZoom(desktopMaxZoom);
        });
      }

      mapInstanceRef.current = map;

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        opacity: 0.9
      }).addTo(map);

      map.getContainer().style.backgroundColor = '#f0f0f0';

      // Notify parent
      onMapReady(map);

      return () => {
        mapInstanceRef.current = null;
        try {
          map.remove();
        } catch (e) {}
        if (mapRef.current && (mapRef.current as any)._leaflet_id) {
          (mapRef.current as any)._leaflet_id = undefined;
        }
      };
    }, [isMobile, meshVersion, worldSlug, desktopMinZoom, desktopMaxZoom, fixedMobileZoomLevel, forceMobileZoom]);

    return (
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
    );
  }
);
