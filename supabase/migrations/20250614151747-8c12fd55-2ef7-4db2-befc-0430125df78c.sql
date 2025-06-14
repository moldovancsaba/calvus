
-- Add a simple 'world_slug' column to manage separate parallel worlds
ALTER TABLE public.triangle_activities
ADD COLUMN IF NOT EXISTS world_slug TEXT NOT NULL DEFAULT '';

-- Add an index for fast lookups/filtering by world
CREATE INDEX IF NOT EXISTS triangle_activities_world_slug_idx
ON public.triangle_activities (world_slug);

-- (Optional, but good practice) 
-- Update existing rows to set world_slug='' (original world) if needed
UPDATE public.triangle_activities SET world_slug = '' WHERE world_slug IS NULL;
