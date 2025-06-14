
import React, { useState } from "react";
import { useIdentity } from "./IdentityContext";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

// Same color palette as IdentityGate
const BASE_COLORS = [
  "#EF476F", "#FFD166", "#06D6A0", "#118AB2",
  "#FF8A5B", "#FFC93C", "#6BCB77", "#4D96FF",
  "#C36A2D", "#FFD23F", "#62B6CB", "#8A4FFF",
  "#E06D06", "#FFBE0B", "#26547C", "#06A77D",
];

function shuffle(arr: string[]) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const getAvailableColors = (): string[] => {
  return shuffle(BASE_COLORS);
};

export const IdentityBar: React.FC = () => {
  const { identity, setIdentity } = useIdentity();
  const [edit, setEdit] = useState(false);
  const [tag, setTag] = useState(identity?.gametag ?? "");
  const [color, setColor] = useState(identity?.color ?? "");
  const [palette] = useState(getAvailableColors());
  const [error, setError] = useState("");

  const startEdit = () => {
    setEdit(true);
    setTag(identity?.gametag ?? "");
    setColor(identity?.color ?? "");
    setError("");
  };

  const save = () => {
    if (!tag.trim() || tag.length > 16) {
      setError("Gametag 1-16 chars");
      return;
    }
    if (!color) {
      setError("Pick a color");
      return;
    }
    setIdentity({ gametag: tag.trim(), color });
    setEdit(false);
  };

  const logout = () => {
    window.localStorage.removeItem("identity");
    window.location.reload();
  };

  if (!identity) return null;

  return (
    <div className="flex items-center gap-3 w-full px-2 pt-1 pb-2 bg-background shadow-lg rounded-b-lg md:max-w-xs mx-auto z-50">
      {!edit ? (
        <>
          <div
            className="rounded-full w-7 h-7 mr-1 border-2"
            style={{ backgroundColor: identity.color, borderColor: "#18181b" }}
            aria-label={identity.color}
          />
          <span className="font-semibold text-lg tracking-tight truncate max-w-[7rem]">{identity.gametag}</span>
          <Button
            variant="ghost"
            className="px-2 py-1 ml-1 text-muted-foreground hover:text-destructive"
            onClick={logout}
            aria-label="Log out"
          >
            <LogOut size={20} />
          </Button>
          <Button
            variant="outline"
            className="px-2 py-1 ml-1 text-xs"
            onClick={startEdit}
            aria-label="Edit identity"
          >
            Change
          </Button>
        </>
      ) : (
        <form
          className="flex items-center gap-2 w-full"
          onSubmit={e => {
            e.preventDefault();
            save();
          }}
        >
          <input
            className="border rounded px-2 py-1 text-sm w-24"
            value={tag}
            maxLength={16}
            onChange={e => setTag(e.target.value)}
            autoFocus
            aria-label="Gametag"
          />
          <div className="grid grid-cols-8 gap-1">
            {palette.map((c) => (
              <button
                key={c}
                type="button"
                tabIndex={0}
                aria-label={c}
                style={{
                  backgroundColor: c,
                  border: color === c ? "2px solid #222" : "1px solid #aaa",
                }}
                className="w-4 h-4 rounded-full focus:outline-none transition"
                onClick={() => setColor(c)}
              />
            ))}
          </div>
          <Button size="sm" type="submit" className="px-2 py-1 text-xs ml-1">Save</Button>
          <Button size="sm" type="button" variant="ghost" className="px-2 py-1 text-xs" onClick={() => setEdit(false)}>Cancel</Button>
          {error && <span className="text-xs text-red-400 ml-2">{error}</span>}
        </form>
      )}
    </div>
  );
};
