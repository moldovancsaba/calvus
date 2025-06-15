
-- Add clicks_to_divide and max_divide_level columns to world_settings table if they don't exist
ALTER TABLE public.world_settings ADD COLUMN IF NOT EXISTS clicks_to_divide integer NOT NULL DEFAULT 3;
ALTER TABLE public.world_settings ADD COLUMN IF NOT EXISTS max_divide_level integer NOT NULL DEFAULT 3;
