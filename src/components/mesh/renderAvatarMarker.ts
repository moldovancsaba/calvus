
import L from "leaflet";
import { getTriangleCentroid } from "./triangleUtils";

interface RenderAvatarMarkerOptions {
  map: L.Map;
  vertices: { lat: number; lng: number }[];
  color: string;
  emoji: string;
  trianglePath: string;
  numberMarkersRef: React.MutableRefObject<Map<string, L.Marker>>;
}
export function renderAvatarMarker({
  map, vertices, color, emoji, trianglePath, numberMarkersRef
}: RenderAvatarMarkerOptions) {
  const centroid = getTriangleCentroid(vertices);
  const size = 34;
  const markerDiv = document.createElement("div");
  markerDiv.style.width = `${size}px`;
  markerDiv.style.height = `${size}px`;
  markerDiv.style.display = "flex";
  markerDiv.style.alignItems = "center";
  markerDiv.style.justifyContent = "center";
  markerDiv.style.borderRadius = "50%";
  markerDiv.style.border = "2.2px solid #333";
  markerDiv.style.boxShadow = "0 3px 8px 0 #2222";
  markerDiv.style.background = color;
  markerDiv.style.fontSize = "1.45rem";
  markerDiv.style.userSelect = "none";
  markerDiv.innerText = emoji;

  const icon = L.divIcon({
    className: "",
    html: markerDiv,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    popupAnchor: [0, 0],
  });
  const marker = L.marker(centroid, {
    icon,
    interactive: false,
    keyboard: false,
    zIndexOffset: 10000,
  });
  marker.addTo(map);
  numberMarkersRef.current.set(trianglePath, marker);
}
