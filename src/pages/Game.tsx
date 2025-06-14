
import { useParams } from "react-router-dom";
import { IdentityBar } from "../components/IdentityBar";
import TriangleMeshMap from "../components/TriangleMeshMap";

function getFixedWorldSlug(raw: string | undefined) {
  // Use "original" for the original world everywhere in the codebase
  return (!raw || raw === "") ? "original" : raw;
}

const Game = () => {
  const { slug } = useParams<{ slug?: string }>();
  const worldSlug = getFixedWorldSlug(slug);
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
        <TriangleMeshMap worldSlug={worldSlug} />
      </main>
    </div>
  );
};
export default Game;

