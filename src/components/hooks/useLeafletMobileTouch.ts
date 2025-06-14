
import { useEffect } from "react";
import L from "leaflet";

export function useLeafletMobileTouch(map: L.Map | null) {
  useEffect(() => {
    if (!map) return;
    const mobile = window.innerWidth < 768;
    if (!mobile) return;

    // Enable gestures
    map.scrollWheelZoom.disable();
    map.doubleClickZoom.disable();
    map.boxZoom.disable();
    map.touchZoom.enable();
    map.dragging.enable();

    // Improved: only preventDefault on map base, never on triangles or controls
    const handleTouchStart = function (e: TouchEvent) {
      if (e.touches.length === 1) {
        const target = e.target as HTMLElement;
        // Allow all interactive (triangles), and controls to work
        if (
          target.classList.contains("leaflet-interactive") ||
          target.closest(".leaflet-control") // do not block controls
        ) {
          // DO NOTHING, allow
          return;
        }
        // Block drawing/panning/scrolling for just background
        e.preventDefault();
      }
    };

    const container = map.getContainer();
    // passive: false is required so we can call preventDefault
    container.addEventListener("touchstart", handleTouchStart, { passive: false });

    return () => {
      container.removeEventListener("touchstart", handleTouchStart);
    };
  }, [map]);
}
