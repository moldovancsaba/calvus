
-- Add click_to_divide and max_divide_level to world_settings
ALTER TABLE public.world_settings ADD COLUMN IF NOT EXISTS clicks_to_divide integer NOT NULL DEFAULT 3;
ALTER TABLE public.world_settings ADD COLUMN IF NOT EXISTS max_divide_level integer NOT NULL DEFAULT 3;
