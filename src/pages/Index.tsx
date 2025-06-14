
import { useIdentity } from "../components/IdentityContext";
import TriangleMeshMap from '../components/TriangleMeshMap';

const Index = () => {
  const { identity } = useIdentity();
  return (
    <div className="w-full h-screen flex flex-col">
      {/* Hud bar - gametag, color, clicks */}
      {identity && (
        <div className="flex items-center justify-center space-x-4 py-2">
          <div className="font-bold text-base">Tag:</div>
          <span className="bg-gray-50 rounded px-2 py-1 text-base font-mono">{identity.gametag}</span>
          <span className="inline-flex items-center space-x-1">
            <span className="w-5 h-5 rounded-full border" style={{ background: identity.color }}></span>
            <span className="text-sm text-gray-500">Your color</span>
          </span>
        </div>
      )}
      <div className="flex-1">
        <TriangleMeshMap />
      </div>
    </div>
  );
};

export default Index;
