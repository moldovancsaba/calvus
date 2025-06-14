
import React, { useEffect, useState } from "react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { fetchWorldSettings, updateWorldSettings, WorldSettings } from "@/utils/worldSettings";
import { SettingsControls } from "./SettingsControls";
import { GamerStats } from "./GamerStats";
import { useToast } from "@/hooks/use-toast";
import { useIsMobile } from "@/hooks/use-mobile";
import { getTriangleActivities, clearTriangleActivities } from "../utils/triangleMesh";
import { useNavigate } from "react-router-dom";

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

  // Hide settings menu on mobile
  if (isMobile) return null;

  useEffect(() => {
    async function load() {
      setSettingsBusy(true);
      try {
        const worldSettings = await fetchWorldSettings(worldSlug);
        setSettings(worldSettings);
        setPendingSettings(worldSettings);
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
      const meshVersion = Date.now().toString();
      window.dispatchEvent(new StorageEvent("storage", { key: `meshVersion_${worldSlug}`, newValue: meshVersion }));
      setActivities([]);
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

  function handleGoToDocuments() {
    setOpen(false);
    setTimeout(() => { navigate("/documents"); }, 100);
  }

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
      </SheetContent>
    </Sheet>
  );
};
