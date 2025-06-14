
import TriangleMeshMap from "../components/TriangleMeshMap";
import { IdentityBar } from "../components/IdentityBar";

const Index = () => {
  return (
    <div className="flex flex-col min-h-screen w-full bg-background">
      <header className="w-full">
        <IdentityBar />
      </header>
      <main className="flex-1 w-full flex flex-col items-center justify-center bg-background">
        <TriangleMeshMap />
      </main>
    </div>
  );
};

export default Index;
