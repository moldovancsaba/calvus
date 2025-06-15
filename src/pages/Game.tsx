
import { useParams } from "react-router-dom";
import { IdentityBar } from "../components/IdentityBar";
import TriangleMeshMap from "../components/TriangleMeshMap";
import { fetchWorldSettings, WorldSettings } from "@/utils/worldSettings";
import React from "react";

function getFixedWorldSlug(raw: string | undefined) {
  // Use "original" for the original world everywhere in the codebase
  return (!raw || raw === "") ? "original" : raw;
}

export default function GamePage() {
  const { slug } = useParams<{ slug?: string }>();
  const worldSlug = getFixedWorldSlug(slug);
  const [worldSettings, setWorldSettings] = React.useState<WorldSettings | null>(null);
  
  React.useEffect(() => {
    async function loadWorldSettings() {
      try {
        const s = await fetchWorldSettings(worldSlug);
        setWorldSettings(s);
      } catch (err) {
        // fallback: silently fail to default settings in triangle logic
      }
    }
    loadWorldSettings();
  }, [worldSlug]);
  
  return (
    <div className="flex flex-col h-screen min-h-screen w-full bg-background">
      <header className="w-full flex-shrink-0">
        <IdentityBar worldSlug={worldSlug} />
        <div className="px-4 py-1 text-xs font-mono flex items-center gap-2 text-muted-foreground">
          <span>World:</span>
          <span className="font-bold text-blue-700">{worldSlug === "original" ? "(original world)" : worldSlug}</span>
        </div>
      </header>
      <main className="flex-1 w-full flex flex-col items-stretch justify-stretch bg-background p-0 m-0">
        <TriangleMeshMap
          worldSlug={worldSlug}
          settings={worldSettings ?? undefined} // Pass settings to the child mesh logic!
        />
      </main>
    </div>
  );
}
