
import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { WorldSettings } from "@/utils/worldSettings";

type SettingsControlsProps = {
  pendingSettings: WorldSettings | null;
  settingsBusy: boolean;
  handleSettingEdit: <K extends keyof WorldSettings>(key: K, value: WorldSettings[K]) => void;
  handleApplySettings: () => void;
  handleStartNewWorld: () => void;
  busy: boolean;
};

export const SettingsControls: React.FC<SettingsControlsProps> = ({
  pendingSettings,
  settingsBusy,
  handleSettingEdit,
  handleApplySettings,
  handleStartNewWorld,
  busy,
}) => {
  if (!pendingSettings) {
    return <div className="text-xs text-muted-foreground">Loading settings...</div>;
  }

  return (
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
    </>
  );
};
