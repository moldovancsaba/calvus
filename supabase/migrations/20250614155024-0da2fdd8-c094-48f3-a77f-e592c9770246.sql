
-- Create table to store settings per world
CREATE TABLE public.world_settings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  world_slug text NOT NULL,
  force_mobile_zoom boolean NOT NULL DEFAULT true,
  fixed_mobile_zoom_level integer NOT NULL DEFAULT 2,
  desktop_min_zoom_level integer NOT NULL DEFAULT 5,
  desktop_max_zoom_level integer NOT NULL DEFAULT 15,
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (world_slug)
);
