
import React, { useEffect, useState } from "react";
import { fetchWorldSettings, updateWorldSettings, WorldSettings } from "@/utils/worldSettings";
import { SettingsControls } from "@/components/SettingsControls";
import { GamerStats } from "@/components/GamerStats";
import { useToast } from "@/hooks/use-toast";
import { getTriangleActivities, clearTriangleActivities } from "../utils/triangleMesh";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function SettingsPage() {
  const worldSlug = (window.location.pathname.split("/")[2] || "original");
  const [activities, setActivities] = useState<any[]>([]);
  const [settings, setSettings] = useState<WorldSettings | null>(null);
  const [pendingSettings, setPendingSettings] = useState<WorldSettings | null>(null);
  const [busy, setBusy] = useState(false);
  const [settingsBusy, setSettingsBusy] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

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
    load();
  }, [worldSlug]);

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
    navigate("/documents");
  }
  function handleGoToGame() {
    navigate(`/game/${worldSlug}`);
  }

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <div className="flex gap-3 mb-6 border-b pb-2 items-center">
        <div className="font-bold text-xl">Settings</div>
        <Button className="ml-auto" variant="secondary" size="sm" onClick={handleGoToGame}>
          Back to Game
        </Button>
        <Button variant="outline" size="sm" onClick={handleGoToDocuments}>
          Documentation
        </Button>
      </div>
      <SettingsControls
        pendingSettings={pendingSettings}
        settingsBusy={settingsBusy}
        handleSettingEdit={handleSettingEdit}
        handleApplySettings={handleApplySettings}
        handleStartNewWorld={handleStartNewWorld}
        busy={busy}
      />
      <div className="mt-8">
        <GamerStats activities={activities} />
      </div>
    </div>
  );
}
