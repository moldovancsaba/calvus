
import { useParams } from "react-router-dom";
import { IdentityBar } from "../components/IdentityBar";
import TriangleMeshMap from "../components/TriangleMeshMap";

const Game = () => {
  const { slug } = useParams<{ slug?: string }>();
  // Use empty string for the original world
  const worldSlug = slug ?? "";
  return (
    <div className="flex flex-col h-screen min-h-screen w-full bg-background">
      <header className="w-full flex-shrink-0">
        <IdentityBar />
        <div className="px-4 py-1 text-xs font-mono flex items-center gap-2 text-muted-foreground">
          <span>World:</span>
          <span className="font-bold text-blue-700">{worldSlug || "(original world)"}</span>
        </div>
      </header>
      <main className="flex-1 w-full flex flex-col items-stretch justify-stretch bg-background p-0 m-0">
        <TriangleMeshMap worldSlug={worldSlug} />
      </main>
    </div>
  );
};
export default Game;
