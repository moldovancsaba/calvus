
import { useIdentity } from "../components/IdentityContext";
import TriangleMeshMap from '../components/TriangleMeshMap';

const Index = () => {
  const { identity } = useIdentity();
  return (
    <div className="flex flex-col h-dvh min-h-screen w-full bg-background">
      {/* HUD bar for gametag, color, and clicks */}
      {identity && (
        <div className="flex items-center justify-between px-3 py-2 w-full max-w-full bg-white/95 shadow-sm border-b z-20">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-sm">Tag:</span>
            <span className="rounded bg-gray-50 px-2 py-1 font-mono text-base truncate max-w-[100px]">{identity.gametag}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-5 h-5 rounded-full border" style={{ background: identity.color }}></span>
            <span className="text-xs text-gray-500">Your color</span>
          </div>
        </div>
      )}
      <div className="flex-1 w-full h-full overflow-hidden">
        <TriangleMeshMap />
      </div>
    </div>
  );
};

export default Index;
