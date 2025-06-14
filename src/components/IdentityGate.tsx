
import React, { useEffect, useState } from "react";
import { useIdentity } from "./IdentityContext";
import { Button } from "@/components/ui/button";

// --- Fun emoji palette ---
const EMOJIS = [
  "🐱", "🌈", "😎", "🌟", "🚀", "🦄", "🎩", "🍉",
  "🧊", "👾", "🦊", "🐸", "🧸", "🍕", "🌿", "🐙",
  "🧀", "🍩", "🐧", "🌺", "🐼", "🍪", "🐻", "🌵",
  "🪐", "🎸", "🐲", "🐼", "🎈", "🥑", "🦥", "🥨"
];

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

// Each color gets a random emoji for the picker during session. But user can click color+emoji combo.
function getColorEmojiPairs(palette: string[]) {
  // Shuffle EMOJIS, pick unique for each color (repeat if needed)
  const shuffled = shuffle(EMOJIS);
  return palette.map((color, i) => ({
    color,
    emoji: shuffled[i % shuffled.length],
  }));
}

const IdentityGate: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { identity, setIdentity } = useIdentity();
  const [tag, setTag] = useState("");
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const [palette, setPalette] = useState<string[]>([]);
  const [colorEmojiPairs, setColorEmojiPairs] = useState<{color:string,emoji:string}[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!identity) {
      const pal = getAvailableColors();
      setPalette(pal);
      const pairs = getColorEmojiPairs(pal);
      setColorEmojiPairs(pairs);
      // Randomly preselect one index if available
      if (pairs.length > 0) {
        setSelectedIdx(Math.floor(Math.random() * pairs.length));
      }
    }
  }, [identity]);

  if (identity) return <>{children}</>;

  const handleSelect = (idx: number) => setSelectedIdx(idx);

  const onConfirm = () => {
    if (!validateTag(tag.trim())) {
      setError("Enter a gametag (1-16 chars)");
      return;
    }
    if (selectedIdx === null) {
      setError("Pick an emoji + color!");
      return;
    }
    setError("");
    const { color, emoji } = colorEmojiPairs[selectedIdx];
    setIdentity({ gametag: tag.trim(), color, emoji });
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
        <div className="grid grid-cols-4 gap-3 w-full my-1">
          {colorEmojiPairs.map(({ color, emoji }, i) => (
            <button
              key={color}
              type="button"
              aria-label={`${emoji} on ${color}`}
              tabIndex={0}
              className="flex flex-col items-center justify-center transition-all group outline-none"
              onClick={() => handleSelect(i)}
            >
              <span
                style={{
                  backgroundColor: color,
                  border: selectedIdx === i ? "3px solid #222" : "2px solid #e5e7eb",
                  boxShadow: selectedIdx === i ? "0 0 0 2px #0369a1" : "none",
                  width: 48,
                  height: 48,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  borderRadius: "100%",
                  marginBottom: 0,
                  outline: "none",
                  transition: "border 0.15s, box-shadow 0.15s",
                  fontSize: "1.7rem",
                  userSelect: "none",
                  position: "relative"
                }}
                className="sm:w-10 sm:h-10"
              >
                <span className="select-none" style={{ lineHeight: 1 }}>{emoji}</span>
              </span>
            </button>
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
