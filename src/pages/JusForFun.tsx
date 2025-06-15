
import React from "react";
import TriangleMeshMap from "../components/TriangleMeshMap";
import { fetchWorldSettings, WorldSettings } from "@/utils/worldSettings";

export default function JusForFunPage() {
  // Render the canonical mesh for the "original" world, without user context.
  const [worldSettings, setWorldSettings] = React.useState<WorldSettings | null>(null);
  React.useEffect(() => {
    let mounted = true;
    fetchWorldSettings("original").then(s => {
      if (mounted) setWorldSettings(s);
    }).catch(() => setWorldSettings(null));
    return () => { mounted = false; };
  }, []);
  return (
    <div className="flex flex-col h-screen w-screen bg-background m-0 p-0 overflow-hidden">
      <main className="flex-1 w-full h-full flex flex-col items-stretch justify-stretch p-0 m-0">
        <TriangleMeshMap worldSlug="original" settings={worldSettings ?? undefined}/>
      </main>
    </div>
  );
}
