
import React, { useEffect, useState } from "react";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { getTriangleActivities, clearTriangleActivities } from "../utils/triangleMesh";
import { useIsMobile } from "../hooks/use-mobile";

// Define type for gamer summary
type GamerSummary = { gametag: string; color: string; clicks: number };

// Helper to aggregate gamer stats from activities
function summarizeGamers(activities: any[]): GamerSummary[] {
  const stats: Record<string, GamerSummary> = {};
  for (const act of activities) {
    if (!act.gametag || !act.color) continue;
    const key = `${act.gametag}:${act.color}`;
    if (!stats[key])
      stats[key] = { gametag: act.gametag, color: act.color, clicks: 0 };
    if (typeof act.click_count === "number")
      stats[key].clicks += act.click_count;
  }
  return Object.values(stats).sort((a, b) => b.clicks - a.clicks);
}

export const SettingsMenu: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [open, setOpen] = useState(false);
  const [activities, setActivities] = useState<any[]>([]);
  const [forceMobileZoom, setForceMobileZoom] = useState(true);
  const [busy, setBusy] = useState(false);
  const isMobile = useIsMobile();

  useEffect(() => {
    async function load() {
      const acts = await getTriangleActivities();
      setActivities(acts);
      // For settings, you could load a flag from localStorage or backend if wanted.
    }
    if (open) load();
  }, [open]);

  // Setting stored in localstorage for "fixed mobile zoom"
  useEffect(() => {
    const val = window.localStorage.getItem("fixedMobileZoom");
    setForceMobileZoom(val === null || val === "true");
  }, []);

  function handleSetMobileZoom(val: boolean) {
    setForceMobileZoom(val);
    window.localStorage.setItem("fixedMobileZoom", val ? "true" : "false");
    // You may want to trigger UI reloads (location.reload or better in a real app)
  }

  async function handleRestartWorld() {
    setBusy(true);
    await clearTriangleActivities();
    setTimeout(() => {
      setBusy(false);
      window.location.reload();
    }, 1000);
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        {children}
      </PopoverTrigger>
      <PopoverContent align="end" className="w-80">
        <div className="text-lg font-semibold mb-2">Settings</div>
        {/* Fixed zoom for mobile */}
        <div className="flex items-center justify-between mb-4">
          <span>Fixed zoom for mobile</span>
          <Button
            variant={forceMobileZoom ? "default" : "outline"}
            onClick={() => handleSetMobileZoom(!forceMobileZoom)}
            size="sm"
          >
            {forceMobileZoom ? "On" : "Off"}
          </Button>
        </div>
        {/* Restart World */}
        <div className="flex items-center justify-between mb-4">
          <span>Restart world</span>
          <Button
            variant="destructive"
            onClick={handleRestartWorld}
            size="sm"
            disabled={busy}
          >
            {busy ? "Resetting..." : "Restart"}
          </Button>
        </div>
        {/* Gamer stats */}
        <div>
          <div className="font-semibold mb-2">Gamers</div>
          <div className="grid grid-cols-1 gap-1 max-h-40 overflow-y-auto">
            {summarizeGamers(activities).map(({ gametag, color, clicks }) => (
              <div className="flex items-center gap-2 p-1 rounded hover:bg-accent" key={gametag + color}>
                <span className="inline-block w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
                <span className="truncate max-w-[5rem] font-mono">{gametag}</span>
                <span className="ml-auto text-xs text-muted-foreground">{clicks} clicks</span>
              </div>
            ))}
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
};
