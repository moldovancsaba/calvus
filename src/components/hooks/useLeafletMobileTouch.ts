
import { useEffect } from "react";
import L from "leaflet";

// Make sure background map never receives pointer/touch/click on mobile!
export function useLeafletMobileTouch(map: L.Map | null) {
  useEffect(() => {
    if (!map) return;
    const mobile = window.innerWidth < 768;
    if (!mobile) return;

    // Fully disable touch-based zooming and double tap, only +/- buttons for zoom
    map.scrollWheelZoom.disable();
    map.doubleClickZoom.disable();
    map.boxZoom.disable();
    map.touchZoom.disable(); // crucial: disables all pinch/doubletap zoom
    map.dragging.enable();

    // PREVENT ALL TOUCH events for base map but NOT overlays
    const container = map.getContainer();
    const stopBackgroundTouch = (e: TouchEvent | PointerEvent | MouseEvent) => {
      const target = e.target as HTMLElement;
      // Only block if not an overlay (propagate if .leaflet-interactive, .leaflet-control)
      if (
        !target.classList.contains("leaflet-interactive") &&
        !target.closest(".leaflet-control")
      ) {
        e.preventDefault();
        e.stopPropagation();
        // Optionally add debug log:
        // console.log("[useLeafletMobileTouch] Blocked touch/click/pointer event on base map background", e, target);
      }
    };

    // Add event listeners for all relevant event types on background map container
    container.addEventListener("touchstart", stopBackgroundTouch, { passive: false });
    container.addEventListener("pointerdown", stopBackgroundTouch, { passive: false });
    container.addEventListener("mousedown", stopBackgroundTouch, { passive: false });

    return () => {
      container.removeEventListener("touchstart", stopBackgroundTouch);
      container.removeEventListener("pointerdown", stopBackgroundTouch);
      container.removeEventListener("mousedown", stopBackgroundTouch);
    };
  }, [map]);
}
