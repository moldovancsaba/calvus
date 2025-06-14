
import TriangleMeshMap from "../components/TriangleMeshMap";
import { IdentityBar } from "../components/IdentityBar";

const Index = () => {
  return (
    <div className="flex flex-col h-screen min-h-screen w-full bg-background">
      <header className="w-full flex-shrink-0">
        <IdentityBar />
      </header>
      <main className="flex-1 w-full flex flex-col items-stretch justify-stretch bg-background p-0 m-0">
        <TriangleMeshMap />
      </main>
    </div>
  );
};

export default Index;
