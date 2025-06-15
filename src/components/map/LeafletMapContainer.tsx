
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

      // Map zoom settings
      const minZoom = isMobile
        ? fixedMobileZoomLevel
        : desktopMinZoom;
      const maxZoom = isMobile
        ? fixedMobileZoomLevel
        : desktopMaxZoom;

      const mapZoom = isMobile
        ? fixedMobileZoomLevel
        : desktopMinZoom;

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

      if (isMobile) {
        map.on("zoomend", () => {
          if (map.getZoom() !== fixedMobileZoomLevel) {
            map.setZoom(fixedMobileZoomLevel);
          }
        });
        map.on("movestart", () => {
          if (map.getZoom() !== fixedMobileZoomLevel) {
            map.setZoom(fixedMobileZoomLevel);
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

      // DEBUG: highlight full visible map area with border
      L.rectangle([[-89, -179], [89, 179]], { color: "#00f", weight: 2, fillOpacity: 0.01 }).addTo(map);

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
    }, [isMobile, meshVersion, worldSlug, desktopMinZoom, desktopMaxZoom, fixedMobileZoomLevel]);

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

// No changes to rest of file
