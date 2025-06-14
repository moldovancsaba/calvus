import React, { useEffect, useState } from "react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getTriangleActivities, clearTriangleActivities } from "../utils/triangleMesh";
import { useToast } from "@/hooks/use-toast";
import { useIsMobile } from "@/hooks/use-mobile";
import { fetchWorldSettings, updateWorldSettings, WorldSettings } from "@/utils/worldSettings";

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

export const SettingsMenu: React.FC<{ children: React.ReactNode; worldSlug: string }> = ({ children, worldSlug }) => {
  const [open, setOpen] = useState(false);
  const [activities, setActivities] = useState<any[]>([]);
  const [settings, setSettings] = useState<WorldSettings | null>(null);
  const [pendingSettings, setPendingSettings] = useState<WorldSettings | null>(null);
  const [busy, setBusy] = useState(false);
  const [settingsBusy, setSettingsBusy] = useState(false);
  const { toast } = useToast();
  const isMobile = useIsMobile();

  // Hide settings menu on mobile, including SheetTrigger
  if (isMobile) return null;

  // Load settings and activities on open
  useEffect(() => {
    async function load() {
      setSettingsBusy(true);
      try {
        const worldSettings = await fetchWorldSettings(worldSlug);
        setSettings(worldSettings);
        setPendingSettings(worldSettings); // track pending edits
      } catch (e) {
        toast({ title: "Error loading settings", description: String((e as Error).message), variant: "destructive" });
      } finally {
        setSettingsBusy(false);
      }
      const acts = await getTriangleActivities(worldSlug);
      setActivities(acts);
    }
    if (open) load();
  }, [open, worldSlug]);

  // Only apply changes via Apply button
  function handleSettingEdit<K extends keyof WorldSettings>(key: K, value: WorldSettings[K]) {
    if (!pendingSettings) return;
    setPendingSettings({ ...pendingSettings, [key]: value });
  }

  async function handleApplySettings() {
    if (!pendingSettings) return;
    setSettingsBusy(true);
    try {
      const updated = await updateWorldSettings(worldSlug, pendingSettings);
      setSettings(updated);
      setPendingSettings(updated);
      toast({ title: "Settings updated", duration: 1500 });
      window.dispatchEvent(
        new StorageEvent("storage", { key: `worldSettings_${worldSlug}`, newValue: Date.now().toString() })
      );
    } catch (e) {
      toast({ title: "Error updating settings", description: String((e as Error).message), variant: "destructive", duration: 2000 });
    } finally {
      setSettingsBusy(false);
    }
  }

  async function handleStartNewWorld() {
    setBusy(true);
    try {
      await clearTriangleActivities(worldSlug);
      // MeshVersion notification for cache busting etc
      const meshVersion = Date.now().toString();
      window.dispatchEvent(new StorageEvent("storage", { key: `meshVersion_${worldSlug}`, newValue: meshVersion }));
      setActivities([]); // clear gamer list instantly

      // World reset event
      const resetEpoch = Date.now().toString();
      window.dispatchEvent(new StorageEvent("storage", { key: `worldReset_${worldSlug}`, newValue: resetEpoch }));

      toast({
        title: "World started",
        description: "A brand new world has been launched! All previous clicks/data are cleared for this world.",
        duration: 2500,
      });
      setBusy(false);
      setTimeout(() => {
        window.location.reload();
      }, 300);
    } catch (e) {
      toast({
        title: "Error",
        description: "Failed to start a new world.",
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
      {!pendingSettings ? (
        <div className="text-xs text-muted-foreground">Loading settings...</div>
      ) : (
        <>
          {/* Fixed zoom for mobile */}
          <div className="flex items-center justify-between mb-4 gap-1">
            <span>Fixed zoom for mobile</span>
            <Button
              variant={pendingSettings.force_mobile_zoom ? "default" : "outline"}
              onClick={() => handleSettingEdit("force_mobile_zoom", !pendingSettings.force_mobile_zoom)}
              size="sm"
              disabled={settingsBusy}
            >
              {pendingSettings.force_mobile_zoom ? "On" : "Off"}
            </Button>
          </div>
          {/* Fixed zoom level input for mobile */}
          {pendingSettings.force_mobile_zoom && (
            <div className="flex items-center justify-between mb-4 gap-2">
              <label htmlFor="fixed-zoom-level" className="text-sm">
                Fixed mobile zoom level
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
                value={pendingSettings.fixed_mobile_zoom_level}
                disabled={settingsBusy}
                onChange={e => {
                  const n = Math.floor(Number((e.target as HTMLInputElement).value));
                  if (!isNaN(n)) handleSettingEdit("fixed_mobile_zoom_level", n);
                }}
                onBlur={e => {
                  let val = Math.round(Number((e.target as HTMLInputElement).value));
                  if (isNaN(val)) val = 2;
                  handleSettingEdit("fixed_mobile_zoom_level", val);
                }}
              />
            </div>
          )}
          {/* Desktop zoom levels */}
          <div className="flex items-center justify-between mb-4 gap-2">
            <label htmlFor="desktop-min-zoom" className="text-sm">Desktop min zoom</label>
            <Input
              id="desktop-min-zoom"
              type="number"
              min={1}
              max={20}
              step={1}
              className="w-20 text-right"
              value={pendingSettings.desktop_min_zoom_level}
              disabled={settingsBusy}
              onChange={e => {
                const n = Math.max(1, Math.floor(Number((e.target as HTMLInputElement).value)));
                handleSettingEdit("desktop_min_zoom_level", n);
              }}
              onBlur={e => {
                let val = Math.max(1, Math.round(Number((e.target as HTMLInputElement).value)));
                handleSettingEdit("desktop_min_zoom_level", val);
              }}
            />
          </div>
          <div className="flex items-center justify-between mb-4 gap-2">
            <label htmlFor="desktop-max-zoom" className="text-sm">Desktop max zoom</label>
            <Input
              id="desktop-max-zoom"
              type="number"
              min={1}
              max={20}
              step={1}
              className="w-20 text-right"
              value={pendingSettings.desktop_max_zoom_level}
              disabled={settingsBusy}
              onChange={e => {
                const n = Math.max(1, Math.floor(Number((e.target as HTMLInputElement).value)));
                handleSettingEdit("desktop_max_zoom_level", n);
              }}
              onBlur={e => {
                let val = Math.max(1, Math.round(Number((e.target as HTMLInputElement).value)));
                handleSettingEdit("desktop_max_zoom_level", val);
              }}
            />
          </div>
          {/* Apply Button */}
          <div className="flex justify-end mb-4">
            <Button
              variant="default"
              size="sm"
              onClick={handleApplySettings}
              disabled={settingsBusy}
            >
              Apply
            </Button>
          </div>
        </>
      )}
      {/* Start a New World */}
      <div className="flex items-center justify-between mb-4 gap-1">
        <span>Start a new world</span>
        <Button
          variant="destructive"
          onClick={handleStartNewWorld}
          size="sm"
          disabled={busy}
        >
          {busy ? "Starting..." : "Start"}
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
