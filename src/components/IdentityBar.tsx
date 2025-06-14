
import React, { useMemo } from "react";
import { useIdentity } from "./IdentityContext";
import { Button } from "@/components/ui/button";
import { LogOut, Settings as SettingsIcon } from "lucide-react";
import { useIsMobile } from "../hooks/use-mobile";
import { getTriangleActivities } from "../utils/triangleMesh";
import { useEffect, useState } from "react";
import { SettingsMenu } from "./SettingsMenu";

// Helper to summarize click counts from activities
function countClicksAndUserClicks(activities, identity) {
  let totalClicks = 0;
  let userClicks = 0;
  if (!Array.isArray(activities)) return [0, 0];
  for (const act of activities) {
    if (typeof act.click_count === "number") {
      totalClicks += act.click_count;
      if (identity && act.gametag === identity.gametag && act.color === identity.color)
        userClicks += act.click_count;
    }
  }
  return [userClicks, totalClicks];
}

export const IdentityBar: React.FC = () => {
  const { identity } = useIdentity();
  const [activities, setActivities] = useState([]);
  const isMobile = useIsMobile();
  const [settingsOpen, setSettingsOpen] = useState(false);

  // Always fetch click counts on load and periodically (for live updates)
  useEffect(() => {
    let running = true;
    async function fetchActivities() {
      const all = await getTriangleActivities();
      if (running) setActivities(all);
    }
    fetchActivities();
    const interval = setInterval(fetchActivities, 5000);
    return () => {
      running = false;
      clearInterval(interval);
    };
  }, []);

  const [userClicks, allClicks] = useMemo(() => countClicksAndUserClicks(activities, identity), [activities, identity]);

  const logout = () => {
    window.localStorage.removeItem("identity");
    window.location.reload();
  };

  if (!identity) return null;

  return (
    <div className="flex items-center gap-3 w-full px-2 pt-1 pb-2 bg-background shadow-lg rounded-b-lg md:max-w-xs mx-auto z-50">
      <div
        className="rounded-full w-7 h-7 mr-1 border-2"
        style={{ backgroundColor: identity.color, borderColor: "#18181b" }}
        aria-label={identity.color}
      />
      <span className="font-semibold text-lg tracking-tight truncate max-w-[7rem]">{identity.gametag}</span>
      <span className="mx-2 font-mono text-xs text-muted-foreground select-none">{userClicks}/{allClicks}</span>
      <Button
        variant="ghost"
        className="px-2 py-1 ml-1 text-muted-foreground hover:text-destructive"
        onClick={logout}
        aria-label="Log out"
      >
        <LogOut size={20} />
      </Button>
      {/* Desktop-only settings */}
      {!isMobile && (
        <SettingsMenu>
          <Button
            variant="outline"
            className="px-1 py-1 ml-1 text-xs"
            type="button"
            onClick={() => setSettingsOpen(o => !o)}
            aria-label="Settings"
          >
            <SettingsIcon size={20} />
          </Button>
        </SettingsMenu>
      )}
    </div>
  );
};
