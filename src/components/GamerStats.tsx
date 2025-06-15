
import React from "react";

type GamerSummary = { gametag: string; color: string; clicks: number; };

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

export function GamerStats({ activities }: { activities: any[] }) {
  const summaries = summarizeGamers(activities);
  return (
    <div className="flex-1 flex flex-col">
      <div className="font-semibold mb-2">Gamers</div>
      <div className="grid grid-cols-1 gap-1 max-h-40 overflow-y-auto">
        {summaries.length === 0 ? (
          <div className="text-xs text-muted-foreground">No gamers yet</div>
        ) : (
          summaries.map(({ gametag, color, clicks }) => (
            <div className="flex items-center gap-2 p-1 rounded hover:bg-accent" key={gametag + color}>
              <span className="inline-block w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
              <span className="truncate max-w-[5rem] font-mono">{gametag}</span>
              <span className="ml-auto text-xs text-muted-foreground">{clicks} clicks</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
