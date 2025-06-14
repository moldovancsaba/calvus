
import React, { useEffect, useState } from "react";
import { useIdentity } from "./IdentityContext";
import { Button } from "@/components/ui/button";

// Material palette, shuffle and pick 16; remove "used"
// These colors are visually distinctive and avoid confusion.
const BASE_COLORS = [
  "#EF476F", "#FFD166", "#06D6A0", "#118AB2",
  "#FF8A5B", "#FFC93C", "#6BCB77", "#4D96FF",
  "#C36A2D", "#FFD23F", "#62B6CB", "#8A4FFF",
  "#E06D06", "#FFBE0B", "#26547C", "#06A77D",
  "#1A535C", "#FF6F59", "#F7B32B", "#3772FF",
];

function shuffle(arr: string[]) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Simulate active colors using localstorage for now
function getUsedColors(): string[] {
  const all = window.localStorage.getItem("usedColors");
  if (!all) return [];
  try {
    return JSON.parse(all) as string[];
  } catch {
    return [];
  }
}
function setUsedColor(color: string) {
  const prev = getUsedColors();
  if (!prev.includes(color)) {
    window.localStorage.setItem("usedColors", JSON.stringify([...prev, color]));
  }
}

const getAvailableColors = (): string[] => {
  const used = getUsedColors();
  return shuffle(BASE_COLORS.filter(c => !used.includes(c))).slice(0, 16);
};

const validateTag = (tag: string) => tag.length > 0 && tag.length <= 16;

const IdentityGate: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { identity, setIdentity } = useIdentity();
  const [tag, setTag] = useState("");
  const [color, setColor] = useState<string | null>(null);
  const [palette, setPalette] = useState<string[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!identity) setPalette(getAvailableColors());
  }, [identity]);

  if (identity) return <>{children}</>;

  const handleSelectColor = (c: string) => setColor(c);

  const onConfirm = () => {
    if (!validateTag(tag.trim())) {
      setError("Enter a gametag (1-16 chars)");
      return;
    }
    if (!color) {
      setError("Pick a color!");
      return;
    }
    setError("");
    setIdentity({ gametag: tag.trim(), color });
    setUsedColor(color);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 to-white">
      <div className="bg-white/90 rounded-xl shadow-xl p-8 w-full max-w-xs space-y-6">
        <h2 className="text-lg font-bold text-center">Identify Yourself</h2>
        <input
          placeholder="Gametag"
          maxLength={16}
          value={tag}
          onChange={e => setTag(e.target.value)}
          className="w-full border rounded-md px-3 py-2 text-center text-base mb-2"
        />
        <div className="grid grid-cols-4 gap-2 mb-2">
          {palette.map((c) => (
            <button
              key={c}
              style={{
                backgroundColor: c,
                border: color === c ? "3px solid #222" : undefined,
              }}
              className={`w-10 h-10 rounded-full focus:outline-none border-2 transition-all`}
              onClick={() => handleSelectColor(c)}
              aria-label={c}
              type="button"
            />
          ))}
        </div>
        <Button className="w-full" onClick={onConfirm} size="lg">Start</Button>
        {error && (
          <div className="text-center text-red-500 text-xs">{error}</div>
        )}
      </div>
    </div>
  );
};

export default IdentityGate;
