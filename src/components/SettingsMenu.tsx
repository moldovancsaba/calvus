import React, { useEffect, useState } from "react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getTriangleActivities, clearTriangleActivities } from "../utils/triangleMesh";
import { useToast } from "@/hooks/use-toast";

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
  const [fixedZoomLevel, setFixedZoomLevel] = useState<number>(2); // default 2
  const [busy, setBusy] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    async function load() {
      const acts = await getTriangleActivities();
      setActivities(acts);
    }
    if (open) load();
  }, [open]);

  useEffect(() => {
    const val = window.localStorage.getItem("fixedMobileZoom");
    setForceMobileZoom(val === null || val === "true");
    const zoomVal = window.localStorage.getItem("fixedMobileZoomLevel");
    if (
      zoomVal &&
      !isNaN(Number(zoomVal)) &&
      Number(zoomVal) > 0 &&
      Number(zoomVal) <= 20
    ) {
      setFixedZoomLevel(Math.floor(Number(zoomVal)));
    }
  }, []);

  function handleSetMobileZoom(val: boolean) {
    setForceMobileZoom(val);
    window.localStorage.setItem("fixedMobileZoom", val ? "true" : "false");
    toast({
      title: "Setting updated",
      description: val
        ? `Fixed zoom enabled (level: ${fixedZoomLevel})`
        : "Fixed zoom disabled",
      duration: 2000,
    });
    // Broadcast storage event for map tab to sync instantly
    window.dispatchEvent(new StorageEvent("storage", { key: "fixedMobileZoom", newValue: val ? "true" : "false" }));
  }

  function handleSetFixedZoomLevel(level: number) {
    // clamp to range [1, 20], integer only
    let clamped = Math.min(Math.max(Math.round(level), 1), 20);
    setFixedZoomLevel(clamped);
    window.localStorage.setItem("fixedMobileZoomLevel", String(clamped));
    toast({
      title: "Zoom level set",
      description: `Mobile zoom level set to ${clamped}`,
      duration: 2000,
    });
    // Broadcast storage event so the map knows to re-read
    window.dispatchEvent(new StorageEvent("storage", { key: "fixedMobileZoomLevel", newValue: String(clamped) }));
  }

  async function handleRestartWorld() {
    setBusy(true);
    try {
      await clearTriangleActivities();
      window.localStorage.removeItem("triangleMeshCache");
      setActivities([]); // clear gamer list instantly
      // Broadcast a custom event so TriangleMeshMap refreshes itself instantly
      window.dispatchEvent(new StorageEvent("storage", { key: "refreshMesh", newValue: Date.now().toString() }));
      // Also reload the page for a guaranteed hard reset
      window.location.reload();
    } catch (e) {
      toast({
        title: "Error",
        description: "Failed to reset the world.",
        duration: 3000,
        variant: "destructive"
      });
      setBusy(false);
    }
  }

  // Settings UI content reused for fullscreen drawer
  const settingsContent = (
    <div className="flex flex-col h-full w-full">
      <div className="text-lg font-semibold mb-2">Settings</div>
      {/* Fixed zoom for mobile */}
      <div className="flex items-center justify-between mb-4 gap-1">
        <span>Fixed zoom for mobile</span>
        <Button
          variant={forceMobileZoom ? "default" : "outline"}
          onClick={() => handleSetMobileZoom(!forceMobileZoom)}
          size="sm"
        >
          {forceMobileZoom ? "On" : "Off"}
        </Button>
      </div>
      {/* Fixed zoom level input */}
      {forceMobileZoom && (
        <div className="flex items-center justify-between mb-4 gap-2">
          <label htmlFor="fixed-zoom-level" className="text-sm">
            Fixed zoom level
          </label>
          <Input
            id="fixed-zoom-level"
            type="number"
            min={1}
            max={20}
            step={1}
            pattern="[0-9]*"
            inputMode="numeric"
            className="w-20 text-right"
            value={fixedZoomLevel}
            onChange={e => {
              // keep only integer
              const n = Math.floor(Number((e.target as HTMLInputElement).value));
              if (!isNaN(n)) handleSetFixedZoomLevel(n);
            }}
            onBlur={e => {
              // Clamp on blur in case user enters out-of-bounds or decimal
              let val = Math.round(Number((e.target as HTMLInputElement).value));
              if (isNaN(val)) val = 2;
              handleSetFixedZoomLevel(val);
            }}
          />
        </div>
      )}
      {/* Restart World */}
      <div className="flex items-center justify-between mb-4 gap-1">
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
      <div className="flex-1 flex flex-col">
        <div className="font-semibold mb-2">Gamers</div>
        <div className="grid grid-cols-1 gap-1 max-h-40 overflow-y-auto">
          {summarizeGamers(activities).length === 0 ? (
            <div className="text-xs text-muted-foreground">No gamers yet</div>
          ) : (
            summarizeGamers(activities).map(({ gametag, color, clicks }) => (
              <div className="flex items-center gap-2 p-1 rounded hover:bg-accent" key={gametag + color}>
                <span className="inline-block w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
                <span className="truncate max-w-[5rem] font-mono">{gametag}</span>
                <span className="ml-auto text-xs text-muted-foreground">{clicks} clicks</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );

  // Always render fullscreen sheet for settings (over map), regardless of device
  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>{children}</SheetTrigger>
      <SheetContent
        side="bottom"
        className="p-6 h-full max-h-screen w-full flex flex-col items-stretch rounded-none fixed inset-0 z-[9999] bg-background"
        style={{
          borderRadius: 0,
        }}
      >
        {settingsContent}
      </SheetContent>
    </Sheet>
  );
};
