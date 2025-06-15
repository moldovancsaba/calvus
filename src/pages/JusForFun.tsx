
import DemoMeshMap from "../components/DemoMeshMap";

export default function JusForFunPage() {
  // Render this as a fullscreen mesh, no UI, no user, no overlays
  return (
    <div className="fixed inset-0 w-screen h-screen overflow-hidden bg-black">
      <DemoMeshMap />
    </div>
  );
}
