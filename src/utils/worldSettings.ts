import { supabase } from "@/integrations/supabase/client";

function fixedWorldSlug(slug: string) {
  return (!slug || slug === "") ? "original" : slug;
}

export type WorldSettings = {
  id: string;
  world_slug: string;
  fixed_mobile_zoom_level: number;
  desktop_min_zoom_level: number;
  desktop_max_zoom_level: number;
  updated_at: string;
  clicks_to_divide: number;
  max_divide_level: number;
  force_mobile_zoom: boolean;
  max_consecutive_clicks_per_user: number; // NEW FIELD
};

export async function fetchWorldSettings(worldSlug: string): Promise<WorldSettings> {
  const fixedSlug = fixedWorldSlug(worldSlug);
  const { data, error } = await supabase
    .from("world_settings")
    .select("*")
    .eq("world_slug", fixedSlug)
    .maybeSingle();
  if (error) throw error;
  if (data) {
    // Coerce, fill in missing props from defaults as needed
    const defaults = {
      fixed_mobile_zoom_level: 2,
      desktop_min_zoom_level: 5,
      desktop_max_zoom_level: 15,
      clicks_to_divide: 3,
      max_divide_level: 3,
      force_mobile_zoom: true,
      max_consecutive_clicks_per_user: 1,
    };
    return {
      ...defaults,
      ...data,
    } as WorldSettings;
  }

  // If not exist, create defaults
  const insertDefaults = {
    world_slug: fixedSlug,
    fixed_mobile_zoom_level: 2,
    desktop_min_zoom_level: 5,
    desktop_max_zoom_level: 15,
    clicks_to_divide: 3,
    max_divide_level: 3,
    force_mobile_zoom: true,
    max_consecutive_clicks_per_user: 1,
  };
  const { data: created, error: insErr } = await supabase
    .from("world_settings")
    .insert([insertDefaults])
    .select("*")
    .maybeSingle();
  if (insErr) throw insErr;
  if (!created) throw new Error("Failed to initialize world settings");
  return {
    ...insertDefaults,
    ...created,
  } as WorldSettings;
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
  if (!data) throw new Error("Settings update failed");
  // Apply defaults if necessary
  const defaults = {
    fixed_mobile_zoom_level: 2,
    desktop_min_zoom_level: 5,
    desktop_max_zoom_level: 15,
    clicks_to_divide: 3,
    max_divide_level: 3,
    force_mobile_zoom: true,
    max_consecutive_clicks_per_user: 1,
  };
  return {
    ...defaults,
    ...data,
  } as WorldSettings;
}
