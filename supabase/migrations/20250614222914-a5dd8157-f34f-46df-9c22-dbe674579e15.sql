
-- Add "max_consecutive_clicks_per_user" column to world_settings table
ALTER TABLE public.world_settings
  ADD COLUMN IF NOT EXISTS max_consecutive_clicks_per_user integer NOT NULL DEFAULT 1;
