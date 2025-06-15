
import DemoMeshMap from "../components/DemoMeshMap";

export default function GamePage() {
  // Render this as a fullscreen mesh, *just like* JusForFunPage
  return (
    <div className="fixed inset-0 w-screen h-screen overflow-hidden bg-black">
      <DemoMeshMap />
    </div>
  );
}
