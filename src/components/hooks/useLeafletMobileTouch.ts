
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

    // Only preventDefault for background, never for .leaflet-interactive or .leaflet-control
    const handleTouchStart = function (e: TouchEvent) {
      if (e.touches.length === 1) {
        const target = e.target as HTMLElement;
        // Allow all interactive (triangles), and controls to work
        if (
          target.classList.contains("leaflet-interactive") ||
          target.closest(".leaflet-control")
        ) {
          // DO NOTHING, allow event to propagate
          console.log("[useLeafletMobileTouch] touchstart: allowed interactive/control", target);
          return;
        }
        // Block drawing/panning/scrolling for just background
        e.preventDefault();
        console.log("[useLeafletMobileTouch] touchstart: preventDefault on base map", target);
      }
    };

    const container = map.getContainer();
    container.addEventListener("touchstart", handleTouchStart, { passive: false });

    return () => {
      container.removeEventListener("touchstart", handleTouchStart);
    };
  }, [map]);
}
