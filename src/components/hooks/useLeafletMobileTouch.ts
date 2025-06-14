
import { useEffect } from "react";
import L from "leaflet";

export function useLeafletMobileTouch(map: L.Map | null) {
  useEffect(() => {
    if (!map) return;
    // Detect mobile
    const mobile = window.innerWidth < 768;
    if (!mobile) return;

    // Enable only pinch-zoom and drag, disable others
    map.scrollWheelZoom.disable();
    map.doubleClickZoom.disable();
    map.boxZoom.disable();
    map.touchZoom.enable(); // only pinch
    map.dragging.enable();

    // Only preventDefault if tapping base map, allow triangle interaction
    const handleTouchStart = function (e: TouchEvent) {
      if (e.touches.length === 1) {
        const target = e.target as HTMLElement;
        if (!(target.classList.contains("leaflet-interactive"))) {
          e.preventDefault();
        }
        // else: allow the triangle tap
      }
    };

    const container = map.getContainer();
    container.addEventListener("touchstart", handleTouchStart, { passive: false });

    return () => {
      container.removeEventListener("touchstart", handleTouchStart);
    };
  }, [map]);
}
