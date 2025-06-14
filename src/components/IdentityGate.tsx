
import React, { useEffect, useState } from "react";
import { useIdentity } from "./IdentityContext";
import { Button } from "@/components/ui/button";

// Distinct palette, shuffle and pick 16, excluding used
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
    <div className="min-h-dvh h-dvh w-full flex items-center justify-center bg-gradient-to-br from-blue-100 to-white px-3">
      <div className="bg-white/95 rounded-xl shadow-2xl mx-auto p-4 pb-6 w-full max-w-xs flex flex-col items-center gap-5">
        <h2 className="text-xl font-bold text-center my-1">Identify Yourself</h2>
        <input
          placeholder="Gametag"
          maxLength={16}
          value={tag}
          onChange={e => setTag(e.target.value)}
          className="w-full border border-gray-200 rounded-lg px-3 py-3 text-center text-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
          inputMode="text"
          autoFocus
          aria-label="Enter gametag"
        />
        <div className="grid grid-cols-4 gap-2 w-full my-1">
          {palette.map((c) => (
            <button
              key={c}
              style={{
                backgroundColor: c,
                border: color === c ? "3px solid #222" : "2px solid #e5e7eb",
                boxShadow: color === c ? "0 0 0 2px #0369a1" : "none",
                touchAction: "manipulation",
              }}
              className={`transition-all w-12 h-12 sm:w-10 sm:h-10 rounded-full focus:outline-none`}
              aria-label={c}
              onClick={() => handleSelectColor(c)}
              type="button"
              tabIndex={0}
            />
          ))}
        </div>
        <Button className="w-full py-3 text-lg" onClick={onConfirm} size="lg">Start</Button>
        {error && (
          <div className="text-center text-red-500 text-xs mt-2">{error}</div>
        )}
      </div>
    </div>
  );
};

export default IdentityGate;

