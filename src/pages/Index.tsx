
import TriangleSVGMap from "../components/SVGMap/TriangleSVGMap";

const Index = () => {
  return (
    <div className="flex flex-col h-dvh min-h-screen w-full bg-background">
      <div className="flex-1 w-full h-full overflow-hidden flex items-center justify-center">
        <TriangleSVGMap />
      </div>
    </div>
  );
};

export default Index;
