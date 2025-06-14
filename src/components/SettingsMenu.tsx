import React, { useEffect, useState } from "react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getTriangleActivities, clearTriangleActivities } from "../utils/triangleMesh";
import { useToast } from "@/hooks/use-toast";
import { useIsMobile } from "@/hooks/use-mobile";
import { fetchWorldSettings, updateWorldSettings, WorldSettings } from "@/utils/worldSettings";
import { SettingsControls } from "./SettingsControls";
import { GamerStats } from "./GamerStats";
import { useNavigate } from "react-router-dom";

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
  const navigate = useNavigate();

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

  // NEW: documentation menu item handler
  function handleGoToDocuments() {
    setOpen(false);
    setTimeout(() => { navigate("/documents"); }, 100);
  }

  // Settings UI content reused for fullscreen drawer
  const settingsContent = (
    <div className="flex flex-col h-full w-full">
      <div className="text-lg font-semibold mb-2">Settings</div>
      <SettingsControls
        pendingSettings={pendingSettings}
        settingsBusy={settingsBusy}
        handleSettingEdit={handleSettingEdit}
        handleApplySettings={handleApplySettings}
        handleStartNewWorld={handleStartNewWorld}
        busy={busy}
      />
      {/* Documentation menu item */}
      <div className="flex items-center justify-between mb-4 gap-1">
        <span>Documentation</span>
        <Button
          variant="secondary"
          onClick={handleGoToDocuments}
          size="sm"
        >
          Open
        </Button>
      </div>
      {/* Gamer stats */}
      <GamerStats activities={activities} />
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
