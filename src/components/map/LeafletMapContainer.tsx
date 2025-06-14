
import React, { useRef, useEffect, useImperativeHandle, forwardRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export interface LeafletMapContainerProps {
  isMobile: boolean;
  meshVersion: string;
  worldSlug: string;
  onMapReady: (map: L.Map) => void;
}

export const DEFAULT_CENTER: [number, number] = [33, 0];

// Expose map instance via ref if needed
export const LeafletMapContainer = forwardRef<HTMLDivElement, LeafletMapContainerProps>(
  ({ isMobile, meshVersion, worldSlug, onMapReady }, ref) => {
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
            mobileZoomLevel = Math.floor(Number(zoomVal));
          }
        }
      }

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
    }, [isMobile, meshVersion, worldSlug]);

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
