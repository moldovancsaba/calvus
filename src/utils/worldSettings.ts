import { supabase } from "@/integrations/supabase/client";

function fixedWorldSlug(slug: string) {
  return (!slug || slug === "") ? "original" : slug;
}

export type WorldSettings = {
  id: string;
  world_slug: string;
  force_mobile_zoom: boolean;
  fixed_mobile_zoom_level: number;
  desktop_min_zoom_level: number;
  desktop_max_zoom_level: number;
  updated_at: string;
};

export async function fetchWorldSettings(worldSlug: string): Promise<WorldSettings> {
  const fixedSlug = fixedWorldSlug(worldSlug);
  const { data, error } = await supabase
    .from("world_settings")
    .select("*")
    .eq("world_slug", fixedSlug)
    .maybeSingle();
  if (error) throw error;
  if (data) return data as WorldSettings;

  // If not exist, create defaults
  const insertDefaults = {
    world_slug: fixedSlug,
    force_mobile_zoom: true,
    fixed_mobile_zoom_level: 2,
    desktop_min_zoom_level: 5,
    desktop_max_zoom_level: 15,
  };
  const { data: created, error: insErr } = await supabase
    .from("world_settings")
    .insert([insertDefaults])
    .select("*")
    .maybeSingle();
  if (insErr) throw insErr;
  if (!created) throw new Error("Failed to initialize world settings");
  return created as WorldSettings;
}

export async function updateWorldSettings(worldSlug: string, values: Partial<WorldSettings>) {
  const fixedSlug = fixedWorldSlug(worldSlug);
  const { data, error } = await supabase
    .from("world_settings")
    .update({
      ...values,
      updated_at: new Date().toISOString(),
    })
    .eq("world_slug", fixedSlug)
    .select("*")
    .maybeSingle();
  if (error) throw error;
  return data as WorldSettings;
}
